#!/usr/bin/env python3
"""
Surface-balanced STRUCTURAL-MAPPING prototype harness (proof-of-concept).

Motivation. The relation-only pilot put the correct analogy in a *different*
domain from the near-disanalogy, so a noisy cross-domain extraction could sink
the correct candidate for reasons unrelated to structure (causal family collapsed
to chance because Q and its different-domain analogy shared almost no directed
triples). This harness prototypes the fix proposed in review:

  * BOTH candidates live in the SAME foreign domain B; the query is in domain A.
    cand_correct is graph-isomorphic to the query (gold map = identity on roles);
    cand_counterfactual differs from cand_correct by EXACTLY ONE declared edge edit
    with the predicate multiset preserved. So the two candidates are near-identical
    in wording -- surface (predicate bag + tokens) ties -- and cross-domain
    extraction noise is symmetric across the ranking. Only relational organization
    separates them.
  * We evaluate the MAPPING, not just the winner: recovered role correspondence,
    edge preservation, and localization of the single edit -- the things a
    structure-blind method cannot produce even when it happens to rank correctly.

Metrics (per item, per matcher that yields a correspondence):
  1. ranking        : score(Q, C+) > score(Q, C-)?  tie -> 0.5
  2. role_map       : recovered Q->C+ node map == gold map (identity on roles)?
  3. edge_preserve  : fraction of query edges preserved under recovered Q->C+ map
  4. edit_localize  : under recovered Q->C- map, is the set of UNPRESERVED query
                      edges exactly {changed_query_edge}?  (found the one edit?)

Baselines:
  predicate_only : Jaccard over predicate SETS (structure-blind; ranking only).
  node_only      : Jaccard over node LABELS, edges discarded (ranking only). Ties
                   on pure edge edits; can separate THIRD_PARTY-introducing edits
                   for a non-structural reason (flagged by the data's purity_note).
  triple_aware   : best role permutation; yields a map -> all four metrics.
  soft_align     : relaxed-QAP soft correspondence P; argmax gives the map.
  edge_shuffle   : triple_aware on endpoint-shuffled candidate edges (structure
                   destroyed, predicate multiset kept) -- a control that MUST
                   collapse all four metrics.

Modes:
  --mode gold      : score the authored gold graphs directly. Validates the harness
                     math and the construction (no API). Ranking/role_map/edge must
                     be perfect for the relational matchers; edge_shuffle collapses.
  --mode end2end   : run the FROZEN extractor (llm_experiments, gpt-4o, temp=0,
                     cached) on the raw text, then score the extracted scaffolds.
                     --constrain-roles selects the canonical role-constrained
                     extractor (Option A); omit it for the free-form extractor.

Phase-2 metrics added for the frozen 40-item set (n=40, four families x 10):
  role_map_f1               : micro-F1 of recovered role->node bindings on C+
                              (graded companion to the exact-match role_map_acc).
  false_contradiction_rate  : fraction of items where the matcher hallucinates a
                              polarity contradiction on the ISOMORPHIC C+ (should
                              be 0 for a faithful matcher).
  cand_split (C+/C-)         : mean matcher score to the correct vs counterfactual
                              candidate and the mean margin (score(C+)-score(C-)).
  family_clustered_ranking   : ranking accuracy with a family-clustered bootstrap
                              CI (resample the 4 families) + per-family win counts,
                              because 40 items from 4 families are not independent.

Writes results/ablation/mapping40_<mode>[_constrained].json.
"""

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

import relation_aware_match as R
import llm_experiments as L

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "mapping_frozen_40.json"
# Frozen-run scaffold caches (distinct from the n=6 pilot caches so the frozen
# run is committed and never regenerated -- FREEZE_mapping40.md Phase 1.5 step 6).
EXTRACTED = ROOT / "results" / "llm" / "scaffolds_mapping40.json"
EXTRACTED_CONSTRAINED = ROOT / "results" / "llm" / "scaffolds_mapping40_constrained.json"
SLOTS = ("query", "cand_correct", "cand_counterfactual")
SHUFFLE_SEEDS = 20
# node labels a role-constrained extractor is allowed to emit; anything else is
# out-of-vocabulary leakage (a domain noun) that pins as a literal and cannot
# align across domains.
ALLOWED_NODES = set(R.ROLES) | {"ACTUALITY"}


# --------------------------------------------------------------------------
# recovered correspondences (query-node -> candidate-node)
# --------------------------------------------------------------------------
def norm_edge(tr):
    return (str(tr[0]).upper(), str(tr[1]).lower(), str(tr[2]).upper())


def triple_best_perm(Eq, Ec):
    """Best candidate-relabel perm pi and its score (as triple_aware uses it)."""
    best, best_pi = -1e9, None
    Sq = set(Eq)
    for pi in R.role_perms():
        Ecp = R.apply_perm(Ec, pi)
        s = R.jaccard(Sq, set(Ecp)) - R.LAMBDA * R.contradictions(Eq, Ecp)
        if s > best:
            best, best_pi = s, pi
    return best, best_pi


def map_from_triple(Eq, Ec):
    """query-node -> candidate-node map recovered by triple_aware.

    triple_aware relabels candidate node x -> pi[x] then intersects with the
    query, so query node pi[x] corresponds to candidate node x; the query->cand
    map is therefore pi^{-1} on the roles, identity on literals.
    """
    _, pi = triple_best_perm(Eq, Ec)
    inv = {v: k for k, v in pi.items()}          # query role -> candidate role
    m = {}
    for n in R._nodes(Eq):
        m[n] = inv.get(n, n)                      # literals map to themselves
    return m


def map_from_soft(Eq, Ec):
    """query-node -> candidate-node map from the soft correspondence P (argmax)."""
    _, P, nq, nc = R.soft_align_P(Eq, Ec)
    m = {}
    for i, n in enumerate(nq):
        if P.shape[1] == 0:
            m[n] = n
            continue
        j = int(np.argmax(P[i]))
        # only accept a rebinding with positive mass; else keep the label
        m[n] = nc[j] if P[i, j] > 1e-6 else n
    return m


# --------------------------------------------------------------------------
# mapping-level metrics given a recovered map
# --------------------------------------------------------------------------
def preserved_edges(Eq, Ec, m):
    Ec_set = set(Ec)
    keep, drop = [], []
    for (s, p, t) in Eq:
        if (m.get(s, s), p, m.get(t, t)) in Ec_set:
            keep.append((s, p, t))
        else:
            drop.append((s, p, t))
    return keep, drop


def role_map_correct(m, gold_map, roles_present):
    """Recovered map matches the gold correspondence on the roles that occur."""
    for r in roles_present:
        if r in R.ROLES and m.get(r, r) != gold_map.get(r, r):
            return False
    return True


def eval_pair_with_map(Eq, Ec, map_fn):
    """(role-agnostic) edge-preservation fraction + the recovered map + drops."""
    m = map_fn(Eq, Ec)
    keep, drop = preserved_edges(Eq, Ec, m)
    frac = len(keep) / len(Eq) if Eq else 0.0
    return m, frac, drop


def map_edges(E, m):
    """Push query edges through the recovered query->candidate node map."""
    return [(m.get(s, s), p, m.get(t, t)) for (s, p, t) in E]


def role_binding_counts(m, gold_map, gold_roles, extracted_roles):
    """Coverage-aware micro counts for role-map precision/recall/F1.

    gold_roles     : canonical roles present in the GOLD query graph
                     (the should-bind set; recall denominator).
    extracted_roles: canonical roles present in the EXTRACTED query graph
                     (the roles the extractor actually asserted; precision
                     denominator).  A gold role the extractor never produced
                     as a canonical role is an UNBOUND gold role and must
                     count as a false negative, not be dropped.

    A binding r is correct iff r is asserted by the extractor (r in
    extracted_roles), is a real gold role (r in gold_roles), and maps to its
    gold image (m[r] == gold_map[r]).  Returns
    (tp, n_gold, n_pred, n_overlap):
        tp        = #correct bindings,
        n_gold    = #gold roles (recall denom),
        n_pred    = #asserted roles (precision denom),
        n_overlap = #gold roles the extractor produced at all (coverage num).
    """
    gold_set = {r for r in gold_roles if r in R.ROLES}
    pred_set = {r for r in extracted_roles if r in R.ROLES}
    correct = {r for r in (gold_set & pred_set) if m.get(r, r) == gold_map.get(r, r)}
    return len(correct), len(gold_set), len(pred_set), len(gold_set & pred_set)


def _prf_f1(tp, n_gold, n_pred):
    """Harmonic mean of coverage-aware micro precision (tp/n_pred) and
    recall (tp/n_gold), scaled to a percentage."""
    if not n_gold or not n_pred:
        return 0.0
    prec = tp / n_pred
    rec = tp / n_gold
    return 0.0 if (prec + rec) == 0 else 100.0 * 2 * prec * rec / (prec + rec)


def false_contradiction(Eq, Ecp, m):
    """1.0 if the matcher hallucinates a polarity contradiction on the
    isomorphic C+ under the recovered map (should be 0 for a faithful match)."""
    return 1.0 if R.contradictions(map_edges(Eq, m), Ecp) > 0 else 0.0


def family_clustered_ci(values_by_id, ids, family_of, seed=42, nb=10000):
    """Ranking-accuracy point estimate + bootstrap CI resampling the FAMILIES
    (4 clusters of 10), since items from one family are not independent."""
    by = defaultdict(list)
    for i in ids:
        by[family_of[i]].append(values_by_id[i])
    fams = list(by)
    m = float(np.mean([x for f in fams for x in by[f]]))
    rng = np.random.RandomState(seed)
    boot = [float(np.mean([x for f in rng.choice(fams, len(fams), replace=True)
                           for x in by[f]])) for _ in range(nb)]
    return 100 * m, float(np.percentile(boot, 2.5) * 100), float(np.percentile(boot, 97.5) * 100)


# --------------------------------------------------------------------------
# scaffold access for the two modes
# --------------------------------------------------------------------------
def gold_edges(it, slot):
    return [norm_edge(tr) for tr in it["gold_scaffold"][slot]["relations"]]


def make_end2end_reader(items, model, constrain_roles=False):
    path = EXTRACTED_CONSTRAINED if constrain_roles else EXTRACTED
    extract_fn = (L.extract_scaffold_constrained if constrain_roles
                  else L.extract_scaffold)
    store = json.loads(path.read_text()) if path.exists() else {}
    client = L.get_client()
    n_new = 0
    for it in items:
        for slot in SLOTS:
            h = R.key(it[slot])
            if h not in store:
                store[h] = extract_fn(client, model, it[slot])
                n_new += 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(store, indent=2))

    def reader(it, slot):
        return R.edges(store[R.key(it[slot])])
    return reader, n_new


def node_vocab_leakage(items, reader):
    """Extraction-faithfulness screen: fraction of extracted node labels that
    fall outside the allowed closed role vocabulary, plus the offending labels.
    A high rate explains a cross-domain alignment collapse."""
    total, oov = 0, 0
    labels = Counter()
    for it in items:
        for slot in SLOTS:
            for n in R._nodes(reader(it, slot)):
                total += 1
                if n not in ALLOWED_NODES:
                    oov += 1
                    labels[n] += 1
    return {
        "oov_node_rate": round(100 * oov / total, 1) if total else 0.0,
        "oov_nodes": oov, "total_nodes": total,
        "oov_labels": dict(labels.most_common()),
    }


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["gold", "end2end"], default="gold")
    ap.add_argument("--model", default="gpt-4o")
    ap.add_argument("--constrain-roles", action="store_true",
                    help="end2end: use the role-constrained extractor (closed "
                         "node vocabulary) instead of the free-form one.")
    args = ap.parse_args()

    data = json.loads(DATA.read_text())
    items = data["items"]

    leakage = None
    if args.mode == "gold":
        reader = gold_edges
        n_new = 0
    else:
        reader, n_new = make_end2end_reader(items, args.model, args.constrain_roles)
        leakage = node_vocab_leakage(items, reader)

    map_fns = {"triple_aware": map_from_triple, "soft_align": map_from_soft}
    rank_scorers = {
        "predicate_only": R.predicate_only,
        "node_only": lambda Eq, Ec: R.jaccard(set(R._nodes(Eq)), set(R._nodes(Ec))),
        "triple_aware": R.triple_aware,
        "soft_align": R.soft_align,
    }

    per_item = []
    # accumulators
    rank = {k: [] for k in list(rank_scorers) + ["edge_shuffle"]}
    role_ok = {k: [] for k in map_fns}
    edge_pres = {k: [] for k in map_fns}
    localize = {k: [] for k in map_fns}
    shuffle_edge_pres = []
    # Phase-2 additions (coverage-aware micro role-binding P/R/F1)
    rolef1_tp = {k: 0 for k in map_fns}          # correct role->node bindings
    rolef1_ngold = {k: 0 for k in map_fns}       # recall denom  = #gold roles
    rolef1_npred = {k: 0 for k in map_fns}       # precision denom = #asserted roles
    rolef1_cov = {k: 0 for k in map_fns}         # coverage num  = #gold roles produced
    role_exact = {k: [] for k in map_fns}        # per-item complete-mapping accuracy
    false_contra = {k: [] for k in map_fns}      # hallucinated contradiction on C+
    score_pos = {k: [] for k in rank_scorers}    # matcher score to C+  (C+/C- split)
    score_neg = {k: [] for k in rank_scorers}    # matcher score to C-
    family_of = {it["id"]: it["family"] for it in items}
    id_order = [it["id"] for it in items]
    rank_by_id = {k: {} for k in rank}

    for it in items:
        Eq = reader(it, "query")
        Ecp = reader(it, "cand_correct")
        Ecm = reader(it, "cand_counterfactual")
        changed = norm_edge(it["changed_query_edge"])
        gold_map = {r: r for r in R.ROLES}           # identity on roles (per design)
        roles_present = [n for n in R._nodes(Eq) if n in R.ROLES]
        # coverage-aware denominator: canonical roles in the GOLD query graph
        gold_roles = [n for n in R._nodes(gold_edges(it, "query")) if n in R.ROLES]

        row = {"id": it["id"], "family": it["family"]}

        # 1. ranking (all scorers): correct should beat counterfactual.
        #    Also record the raw C+ vs C- scores (the ranking MARGIN, not just
        #    the win indicator) for the C+/C- split diagnostic.
        for name, fn in rank_scorers.items():
            s_pos, s_neg = fn(Eq, Ecp), fn(Eq, Ecm)
            v = 1 if s_pos > s_neg else (0.5 if s_pos == s_neg else 0)
            rank[name].append(v)
            rank_by_id[name][it["id"]] = v
            score_pos[name].append(float(s_pos))
            score_neg[name].append(float(s_neg))
            row[f"rank_{name}"] = v
            row[f"score_{name}_pos"] = round(float(s_pos), 3)
            row[f"score_{name}_neg"] = round(float(s_neg), 3)

        # edge_shuffle ranking control (mean over seeds)
        sh = []
        for s in range(SHUFFLE_SEEDS):
            rng = random.Random(3000 + s)
            v = R.decide(R.triple_aware, Eq,
                         R.shuffle_endpoints(Ecp, rng),
                         R.shuffle_endpoints(Ecm, rng))
            sh.append(v)
        rank["edge_shuffle"].append(float(np.mean(sh)))
        rank_by_id["edge_shuffle"][it["id"]] = float(np.mean(sh))
        row["rank_edge_shuffle"] = float(np.mean(sh))

        # 2-4. mapping metrics (matchers that yield a correspondence)
        for name, mfn in map_fns.items():
            m_pos, frac_pos, _ = eval_pair_with_map(Eq, Ecp, mfn)
            role_ok[name].append(1.0 if role_map_correct(m_pos, gold_map, roles_present) else 0.0)
            edge_pres[name].append(frac_pos)
            # role-map P/R/F1 (micro, coverage-aware): unbound gold roles = FN
            tp, ng, npred, nov = role_binding_counts(
                m_pos, gold_map, gold_roles, roles_present)
            rolef1_tp[name] += tp
            rolef1_ngold[name] += ng
            rolef1_npred[name] += npred
            rolef1_cov[name] += nov
            role_exact[name].append(1.0 if (ng > 0 and tp == ng) else 0.0)
            # faithfulness screen: contradiction hallucinated on the ISOMORPHIC C+
            fc = false_contradiction(Eq, Ecp, m_pos)
            false_contra[name].append(fc)
            # localization: drops under the Q->C- map must be exactly the edit
            m_neg, _, drop_neg = eval_pair_with_map(Eq, Ecm, mfn)
            loc = 1.0 if (len(drop_neg) == 1 and drop_neg[0] == changed) else 0.0
            localize[name].append(loc)
            row[f"rolemap_{name}"] = role_ok[name][-1]
            row[f"edgepres_{name}"] = round(frac_pos, 3)
            row[f"localize_{name}"] = loc
            row[f"false_contra_{name}"] = fc

        # edge_shuffle mapping collapse (edge preservation on C+ after shuffle)
        rng = random.Random(9999)
        _, frac_sh, _ = eval_pair_with_map(Eq, R.shuffle_endpoints(Ecp, rng), map_from_triple)
        shuffle_edge_pres.append(frac_sh)
        row["edgepres_edge_shuffle"] = round(frac_sh, 3)

        per_item.append(row)

    def pct(xs):
        return round(100 * float(np.mean(xs)), 1)

    # family-clustered ranking CI (resample the 4 families) for every scorer
    family_clustered = {}
    for k in rank:
        m, lo, hi = family_clustered_ci(rank_by_id[k], id_order, family_of)
        family_clustered[k] = {"acc": round(m, 1),
                               "ci95": [round(lo, 1), round(hi, 1)]}

    summary = {
        "mode": args.mode, "model": args.model if args.mode == "end2end" else None,
        "constrain_roles": bool(args.constrain_roles) if args.mode == "end2end" else None,
        "extraction_faithfulness": leakage,
        "n": len(items),
        "dataset": "data/mapping_frozen_40.json (FROZEN held-out, 4 families x 10)",
        "ranking_acc": {k: pct(v) for k, v in rank.items()},
        "ranking_wins": {k: {"wins": sum(1 for x in v if x == 1),
                             "ties": sum(1 for x in v if x == 0.5),
                             "n": len(v)} for k, v in rank.items()},
        "ranking_family_clustered_ci": family_clustered,
        "role_map_acc": {k: pct(v) for k, v in role_ok.items()},
        # coverage-aware micro precision / recall / F1 (unbound gold roles = FN),
        # plus role coverage and exact complete-mapping accuracy.
        "role_map_precision": {k: (round(100 * rolef1_tp[k] / rolef1_npred[k], 1)
                                   if rolef1_npred[k] else None) for k in map_fns},
        "role_map_recall": {k: (round(100 * rolef1_tp[k] / rolef1_ngold[k], 1)
                                if rolef1_ngold[k] else None) for k in map_fns},
        "role_map_f1_micro": {k: (round(_prf_f1(rolef1_tp[k], rolef1_ngold[k],
                                                rolef1_npred[k]), 1)
                                  if (rolef1_ngold[k] and rolef1_npred[k]) else None)
                              for k in map_fns},
        "role_coverage": {k: (round(100 * rolef1_cov[k] / rolef1_ngold[k], 1)
                              if rolef1_ngold[k] else None) for k in map_fns},
        "role_map_exact_acc": {k: pct(v) for k, v in role_exact.items()},
        "edge_preservation": {k: pct(v) for k, v in edge_pres.items()},
        "edit_localization": {k: pct(v) for k, v in localize.items()},
        "false_contradiction_rate": {k: pct(v) for k, v in false_contra.items()},
        "cand_split": {k: {"mean_score_correct": round(float(np.mean(score_pos[k])), 3),
                           "mean_score_counterfactual": round(float(np.mean(score_neg[k])), 3),
                           "mean_margin": round(float(np.mean(score_pos[k]) - np.mean(score_neg[k])), 3)}
                       for k in rank_scorers},
        "edge_shuffle_edge_preservation": pct(shuffle_edge_pres),
        "per_family_ranking": {},
        "per_family_wins": {},
        "per_item": per_item,
    }

    # per-family ranking (descriptive) + win counts (independence diagnostic)
    fam_idx = defaultdict(list)
    for i, it in enumerate(items):
        fam_idx[it["family"]].append(i)
    for fam, idx in fam_idx.items():
        summary["per_family_ranking"][fam] = {
            k: pct([rank[k][i] for i in idx]) for k in rank_scorers}
        summary["per_family_wins"][fam] = {
            k: {"wins": sum(1 for i in idx if rank[k][i] == 1),
                "ties": sum(1 for i in idx if rank[k][i] == 0.5),
                "n": len(idx)} for k in list(rank_scorers) + ["edge_shuffle"]}

    suffix = "_constrained" if (args.mode == "end2end" and args.constrain_roles) else ""
    out = ROOT / "results" / "ablation" / f"mapping40_{args.mode}{suffix}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2))

    # ---- report ----
    print(f"FROZEN 40-item structural-mapping eval: mode={args.mode}"
          + (f", model={args.model}"
             + (" [ROLE-CONSTRAINED]" if args.constrain_roles else " [free-form]")
             + f", {n_new} new extractions" if args.mode == "end2end" else "")
          + f", n={len(items)}\n")
    if leakage is not None:
        print(f"extraction faithfulness: out-of-vocab node rate "
              f"{leakage['oov_node_rate']:.1f}% "
              f"({leakage['oov_nodes']}/{leakage['total_nodes']} node labels)"
              + (f"  leaked={leakage['oov_labels']}" if leakage['oov_labels'] else "")
              + "\n")
    print(f"{'metric':<22}" + "".join(f"{k:<16}" for k in
          ["predicate_only", "node_only", "triple_aware", "soft_align", "edge_shuffle"]))
    print("-" * 102)

    def line(label, d, keys):
        cells = []
        for k in keys:
            cells.append(f"{d[k]:.1f}%" if k in d and d[k] is not None else "--")
        print(f"{label:<22}" + "".join(f"{c:<16}" for c in cells))

    keys = ["predicate_only", "node_only", "triple_aware", "soft_align", "edge_shuffle"]
    line("ranking acc", summary["ranking_acc"], keys)
    line("role-map acc", summary["role_map_acc"], keys)
    line("role-map F1 (micro)", summary["role_map_f1_micro"], keys)
    line("edge-preservation", {**summary["edge_preservation"],
                               "edge_shuffle": summary["edge_shuffle_edge_preservation"]}, keys)
    line("edit-localization", summary["edit_localization"], keys)
    line("false-contradiction", summary["false_contradiction_rate"], keys)

    print("\nranking acc with family-clustered 95% CI (resample 4 families):")
    for k in keys:
        fc = summary["ranking_family_clustered_ci"][k]
        w = summary["ranking_wins"][k]
        print(f"  {k:<16} {fc['acc']:.1f}%  CI[{fc['ci95'][0]:.0f},{fc['ci95'][1]:.0f}]"
              f"  ({w['wins']}/{w['n']} wins, {w['ties']} ties)")

    print("\nC+/C- score split (mean score to correct vs counterfactual, margin):")
    for k in ["predicate_only", "node_only", "triple_aware", "soft_align"]:
        cs = summary["cand_split"][k]
        print(f"  {k:<16} C+={cs['mean_score_correct']:.3f}  "
              f"C-={cs['mean_score_counterfactual']:.3f}  "
              f"margin={cs['mean_margin']:+.3f}")

    print("\nper-family ranking accuracy:")
    for fam, d in summary["per_family_ranking"].items():
        print(f"  {fam:<26}" + "  ".join(f"{k}={d[k]:.0f}" for k in
              ["predicate_only", "node_only", "triple_aware", "soft_align"]))

    print(f"\nwrote {out.relative_to(ROOT)}")
    if args.mode == "gold":
        print("NOTE: gold mode scores the authored graphs directly (harness + "
              "construction check, no API). It is the ceiling row, not a model result.")


if __name__ == "__main__":
    main()
