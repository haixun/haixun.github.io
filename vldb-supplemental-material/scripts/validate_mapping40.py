#!/usr/bin/env python3
"""
Deterministic construction validators for data/mapping_frozen_40.json.

These are ARTIFACT ASSERTS, not accuracy gates (Roadmap Phase 1.3). They read the
frozen gold scaffolds and verify the construction is valid on ALL 40 items:

  A1. predicate multiset equal across query / cand_correct / cand_counterfactual
  A2. node inventory equal across cand_correct / cand_counterfactual (and query)
  A3. query is graph-isomorphic to cand_correct under the identity role map
  A4. cand_counterfactual differs from cand_correct by EXACTLY the one declared
      directed-edge edit (one edge removed == changed_query_edge, one added)
  A5. the gold triple-aware matcher ranks cand_correct > cand_counterfactual, and
      localizes the edit (the single unpreserved query edge under the recovered
      Q->C- map is exactly changed_query_edge); role map on C+ is the identity
  A6. node_only (edge-blind) is forced to a TIE on every item  [Phase 1.2 guarantee]
  A7. the query is LEXICALLY FAR from BOTH candidates: token-Jaccard(query, cand) is
      at most QUERY_FAR_MAX for cand_correct and cand_counterfactual [Phase 1.4b
      far-analogy gate], so a structural match cannot be won by string copying.

Also reports surface controls (Phase 1.4): token-Jaccard SurfaceSim within the
candidate minimal pair vs. query-to-candidate, as an authoring diagnostic.

Writes results/ablation/validate_mapping40_report.json. Exit code 0 iff A1-A7 pass
on all 40 items.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

import relation_aware_match as R

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "mapping_frozen_40.json"
REPORT = ROOT / "results" / "ablation" / "validate_mapping40_report.json"
SLOTS = ("query", "cand_correct", "cand_counterfactual")

# A7 far-analogy gate: query/candidate token-Jaccard upper bound. Genuine far
# analogies share only function words (~0.1-0.2); near-paraphrase word-swaps run
# far higher (~0.7+). 0.35 cleanly separates the two regimes.
QUERY_FAR_MAX = 0.35


def edges(it, slot):
    return [R.norm_edge(tr) if hasattr(R, "norm_edge") else
            (str(tr[0]).upper(), str(tr[1]).lower(), str(tr[2]).upper())
            for tr in it["gold_scaffold"][slot]["relations"]]


def norm_edge(tr):
    return (str(tr[0]).upper(), str(tr[1]).lower(), str(tr[2]).upper())


def pred_multiset(E):
    return Counter(p for _, p, _ in E)


def node_set(E):
    return set(R._nodes(E))


def triple_best_perm(Eq, Ec):
    best, best_pi = -1e9, None
    Sq = set(Eq)
    for pi in R.role_perms():
        Ecp = R.apply_perm(Ec, pi)
        s = R.jaccard(Sq, set(Ecp)) - R.LAMBDA * R.contradictions(Eq, Ecp)
        if s > best:
            best, best_pi = s, pi
    return best, best_pi


def map_from_triple(Eq, Ec):
    _, pi = triple_best_perm(Eq, Ec)
    inv = {v: k for k, v in pi.items()}
    return {n: inv.get(n, n) for n in R._nodes(Eq)}


def dropped_query_edges(Eq, Ec, m):
    Ec_set = set(Ec)
    return [(s, p, t) for (s, p, t) in Eq
            if (m.get(s, s), p, m.get(t, t)) not in Ec_set]


_TOK = re.compile(r"[a-z]+")


def surface_sim(a, b):
    ta = set(_TOK.findall(a.lower()))
    tb = set(_TOK.findall(b.lower()))
    if not ta and not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def validate():
    data = json.loads(DATA.read_text())
    items = data["items"]
    rows = []
    fails = []

    for it in items:
        Eq = edges(it, "query")
        Ecp = edges(it, "cand_correct")
        Ecm = edges(it, "cand_counterfactual")
        changed = norm_edge(it["changed_query_edge"])

        r = {"id": it["id"], "family": it["family"], "asserts": {}}

        # A1 predicate multiset equal Q / C+ / C-
        a1 = pred_multiset(Eq) == pred_multiset(Ecp) == pred_multiset(Ecm)
        r["asserts"]["A1_pred_multiset_equal"] = a1

        # A2 node inventory equal C+ / C- (and query)
        a2 = node_set(Ecp) == node_set(Ecm) == node_set(Eq)
        r["asserts"]["A2_node_inventory_equal"] = a2

        # A3 query == C+ (isomorphic under identity role map)
        a3 = set(Eq) == set(Ecp)
        r["asserts"]["A3_query_iso_correct"] = a3

        # A4 C- differs from C+ by exactly the declared single edge edit
        added = set(Ecm) - set(Ecp)
        removed = set(Ecp) - set(Ecm)
        a4 = (len(added) == 1 and len(removed) == 1 and changed in removed)
        r["asserts"]["A4_single_declared_edit"] = a4
        r["edit_removed"] = sorted(f"{s} {p} {t}" for s, p, t in removed)
        r["edit_added"] = sorted(f"{s} {p} {t}" for s, p, t in added)

        # A5 gold matcher ranks C+ > C-, localizes edit, identity role map on C+
        s_pos, pi_pos = triple_best_perm(Eq, Ecp)
        s_neg, _ = triple_best_perm(Eq, Ecm)
        ranks = s_pos > s_neg
        role_id = all(pi_pos.get(rr, rr) == rr for rr in R.ROLES)
        m_neg = map_from_triple(Eq, Ecm)
        drops = dropped_query_edges(Eq, Ecm, m_neg)
        localizes = (len(drops) == 1 and drops[0] == changed)
        a5 = ranks and role_id and localizes
        r["asserts"]["A5_gold_rank_localize"] = a5
        r["gold_scores"] = {"cand_correct": round(s_pos, 3), "cand_counterfactual": round(s_neg, 3)}
        r["gold_localizes"] = localizes

        # A6 node_only forced to a tie
        node_only = lambda Ea, Eb: R.jaccard(node_set(Ea), node_set(Eb))
        v_node = R.decide(node_only, Eq, Ecp, Ecm)
        a6 = (v_node == 0.5)
        r["asserts"]["A6_node_only_tie"] = a6
        r["node_only_decision"] = v_node

        # surface controls (diagnostic, not a hard gate)
        s_pair = surface_sim(it["cand_correct"], it["cand_counterfactual"])
        s_qcp = surface_sim(it["query"], it["cand_correct"])
        s_qcm = surface_sim(it["query"], it["cand_counterfactual"])
        r["surface"] = {
            "sim_candidate_pair": round(s_pair, 3),
            "sim_query_correct": round(s_qcp, 3),
            "sim_query_counterfactual": round(s_qcm, 3),
            "minimal_pair_ok": bool(s_pair > s_qcp and s_pair > s_qcm),
            "query_balanced_ok": bool(abs(s_qcp - s_qcm) <= 0.15),
            "query_far_ok": bool(max(s_qcp, s_qcm) <= QUERY_FAR_MAX),
        }

        # A7 query lexically far from BOTH candidates (far-analogy gate)
        a7 = max(s_qcp, s_qcm) <= QUERY_FAR_MAX
        r["asserts"]["A7_query_lexically_far"] = a7

        all_ok = all(r["asserts"].values())
        r["PASS"] = all_ok
        if not all_ok:
            fails.append(it["id"])
        rows.append(r)

    n = len(items)
    assert_names = ["A1_pred_multiset_equal", "A2_node_inventory_equal",
                    "A3_query_iso_correct", "A4_single_declared_edit",
                    "A5_gold_rank_localize", "A6_node_only_tie",
                    "A7_query_lexically_far"]
    summary = {name: sum(1 for r in rows if r["asserts"][name]) for name in assert_names}
    surface_flags = {
        "minimal_pair_ok": sum(1 for r in rows if r["surface"]["minimal_pair_ok"]),
        "query_balanced_ok": sum(1 for r in rows if r["surface"]["query_balanced_ok"]),
    }

    report = {
        "n": n,
        "all_pass": len(fails) == 0,
        "failed_ids": fails,
        "assert_pass_counts": {k: f"{v}/{n}" for k, v in summary.items()},
        "surface_diagnostics": {k: f"{v}/{n}" for k, v in surface_flags.items()},
        "human_adjudication": "PENDING (Roadmap Phase 1.5 step 4)",
        "per_item": rows,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2))

    print(f"validate_mapping40: n={n}")
    for k in assert_names:
        mark = "OK " if summary[k] == n else "!! "
        print(f"  [{mark}] {k:<28} {summary[k]}/{n}")
    print("  surface (diagnostic, not a gate):")
    for k, v in surface_flags.items():
        print(f"        {k:<28} {v}/{n}")
    print(f"\nwrote {REPORT.relative_to(ROOT)}")
    if fails:
        print(f"FAIL: construction asserts failed on ids {fails}")
        return 1
    print("PASS: all 40 items satisfy A1-A7.  Human adjudication still PENDING.")
    return 0


if __name__ == "__main__":
    sys.exit(validate())
