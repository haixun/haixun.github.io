#!/usr/bin/env python3
"""
Relation-aware, model-free structural matching over the cached scaffolds.

The Exp-3 "overlap" matcher scores Jaccard over the *set of predicates*, which
discards role bindings and edge directions -- it is closer to bag-of-abstract-
predicates retrieval than to structural matching. This script adds a genuinely
relation-aware matcher over the SAME cached scaffolds (no new API calls) and two
structure-destruction controls, to test whether relational organization -- not
just predicate vocabulary overlap -- carries the signal.

For scaffolds G_q, G_c with directed labelled triples E=(src, predicate, tgt):

  predicate_only : Jaccard over the predicate sets (roles/direction discarded).
  triple_aware   : max over role permutations pi of
                     Jaccard(E_q, pi(E_c)) - lambda * Contradictions(E_q, pi(E_c)),
                   where pi permutes the generic agent roles {AGENT,TARGET,
                   THIRD_PARTY} (6 permutations), non-role nodes are literals, and
                   a Contradiction is a polarity inversion (appears/actually
                   positive vs negative) on the same ordered node pair.
  soft_align     : model-free relaxed-QAP soft correspondence P (doubly
                   sub-stochastic, so matching is partial) maximizing node
                   compatibility + relation preservation - typed contradictions,
                   solved by entropic mirror ascent -- the model-free analog of
                   the learned P* matcher, tolerant to noisy endpoints.
  triple_reverse : triple_aware after reversing every candidate edge's direction.
  triple_shuffle : triple_aware after randomly rewiring candidate edge endpoints
                   (predicate multiset preserved, relational organization
                   destroyed), averaged over several seeds.

A genuine structural method should satisfy triple_aware >= predicate_only and
degrade under reverse/shuffle. predicate_only is invariant to endpoint shuffling
by construction, which is exactly the point.

Outputs per-item files (results/per_item/relmatch_*_results.json) so the existing
schema-clustered analyzer picks them up, plus a split-aware summary with held-out
(40) as the primary number.
"""

import hashlib
import itertools
import json
import random
from pathlib import Path
from collections import defaultdict

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SCAFFOLDS = ROOT / "results" / "llm" / "scaffolds.json"
DATA = ROOT / "data" / "triplets_60.json"
PI_DIR = ROOT / "results" / "per_item"
OUT = ROOT / "results" / "ablation" / "relation_aware_summary.json"

ROLES = ("AGENT", "TARGET", "THIRD_PARTY")
LAMBDA = 0.5
SHUFFLE_SEEDS = 20
POLARITY_OPP = [("appears_positive", "appears_negative"),
                ("actually_positive", "actually_negative")]


def key(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def edges(sc):
    """Directed labelled triples as tuples."""
    out = []
    for tr in sc.get("relations", []):
        if isinstance(tr, list) and len(tr) == 3:
            out.append((str(tr[0]).upper(), str(tr[1]).lower(), str(tr[2]).upper()))
    return out


def pred_set(E):
    return {p for _, p, _ in E}


def jaccard(A, B):
    A, B = set(A), set(B)
    if not A and not B:
        return 0.0
    return len(A & B) / len(A | B)


def role_perms():
    """All 6 relabelings of the three generic agent roles."""
    for perm in itertools.permutations(ROLES):
        yield dict(zip(ROLES, perm))


def apply_perm(E, pi):
    return [(pi.get(s, s), p, pi.get(t, t)) for s, p, t in E]


def contradictions(Eq, Ec):
    """Polarity inversions on the same ordered node pair."""
    q = defaultdict(set)
    for s, p, t in Eq:
        q[(s, t)].add(p)
    n = 0
    for s, p, t in Ec:
        for a, b in POLARITY_OPP:
            if p == a and b in q[(s, t)]:
                n += 1
            if p == b and a in q[(s, t)]:
                n += 1
    return n


def predicate_only(Eq, Ec):
    return jaccard(pred_set(Eq), pred_set(Ec))


def triple_aware(Eq, Ec):
    best = -1e9
    Sq = set(Eq)
    for pi in role_perms():
        Ecp = apply_perm(Ec, pi)
        s = jaccard(Sq, set(Ecp)) - LAMBDA * contradictions(Eq, Ecp)
        if s > best:
            best = s
    return best


# ---------------------------------------------------------------------------
# Soft partial graph alignment (model-free, no learning).
#
# The directed-triple matcher hard-maximizes over the 6 relabelings of the three
# generic roles and scores exact triple Jaccard. That is brittle: a single noisy
# endpoint drops a whole triple, and only roles (not object nodes) may be rebound.
# The soft matcher instead *solves* for a doubly sub-stochastic correspondence P
# between the two graphs' nodes -- the model-free analog of the learned P* of the
# paper's retrieval stage -- maximizing
#
#     f(P) = <P, S_H> + lambda * sum_{p,p'} g(p,p') <P^T A_q^p P, A_c^{p'}>
#
# where S_H is node compatibility (identical label -> 1; two generic roles -> 0.5,
# so roles may rebind while object literals stay pinned), A_q^p / A_c^p are the
# per-predicate adjacency matrices, and g(p,p') = +1 if p==p', -SOFT_CONTRA if the
# pair is a polarity inversion (appears/actually positive vs negative), else 0 --
# folding relation preservation and typed contradictions into one quadratic term.
# Null rows/columns (row/col sums < 1) leave structure unmatched, i.e. partial.
# Optimized by entropic mirror ascent (Frank-Wolfe-style) with a sub-stochastic
# Sinkhorn projection; the graphs are tiny so this is cheap and deterministic.
# ---------------------------------------------------------------------------
SOFT_LAMBDA = 1.0
SOFT_CONTRA = 0.5
SOFT_ITERS = 60
SOFT_ETA = 1.0
_OPP = {(a, b) for a, b in POLARITY_OPP} | {(b, a) for a, b in POLARITY_OPP}


def _nodes(E):
    ns = []
    for s, _, t in E:
        for n in (s, t):
            if n not in ns:
                ns.append(n)
    return ns


def _adj(E, ns):
    idx = {n: i for i, n in enumerate(ns)}
    A = {}
    for s, p, t in E:
        A.setdefault(p, np.zeros((len(ns), len(ns))))[idx[s], idx[t]] = 1.0
    return A


def _node_compat(nq, nc):
    S = np.zeros((len(nq), len(nc)))
    for i, a in enumerate(nq):
        for j, b in enumerate(nc):
            if a == b:
                S[i, j] = 1.0
            elif a in ROLES and b in ROLES:
                S[i, j] = 0.5
    return S


def _substochastic(P, iters=20):
    """Project onto doubly sub-stochastic matrices (row/col sums <= 1)."""
    P = np.clip(P, 0.0, None)
    for _ in range(iters):
        rs = np.maximum(P.sum(1, keepdims=True), 1.0)
        P = P / rs
        cs = np.maximum(P.sum(0, keepdims=True), 1.0)
        P = P / cs
    return P


def _pred_weights(predsq, predsc):
    """Ordered list of (p, p', weight) with non-zero interaction."""
    out = []
    for p in predsq:
        for pp in predsc:
            if p == pp:
                out.append((p, pp, 1.0))
            elif (p, pp) in _OPP:
                out.append((p, pp, -SOFT_CONTRA))
    return out


def soft_align_P(Eq, Ec):
    """Return (obj, P, nq, nc): the soft correspondence and the node orderings.

    P[i, j] is the (doubly sub-stochastic) mass matching query node nq[i] to
    candidate node nc[j]. Exposes the recovered correspondence so a caller can
    read off the role map (argmax over candidate nodes) and edge preservation,
    not just the scalar objective.
    """
    nq, nc = _nodes(Eq), _nodes(Ec)
    if not nq or not nc:
        return 0.0, np.zeros((0, 0)), nq, nc
    Aq, Ac = _adj(Eq, nq), _adj(Ec, nc)
    S = _node_compat(nq, nc)
    weights = _pred_weights(set(Aq), set(Ac))

    def quad_grad(P):
        G = np.zeros_like(P)
        for p, pp, w in weights:
            G += SOFT_LAMBDA * w * (Aq[p] @ P @ Ac[pp].T + Aq[p].T @ P @ Ac[pp])
        return G

    P = _substochastic(np.maximum(S, 1e-6))
    for _ in range(SOFT_ITERS):
        G = S + quad_grad(P)
        P = P * np.exp(SOFT_ETA * G / (np.abs(G).max() + 1e-9))
        P = _substochastic(P)

    obj = float((P * S).sum())
    for p, pp, w in weights:
        obj += SOFT_LAMBDA * w * float((P * (Aq[p] @ P @ Ac[pp].T)).sum())
    return obj, P, nq, nc


def soft_align(Eq, Ec):
    return soft_align_P(Eq, Ec)[0]


def reverse(E):
    return [(t, p, s) for s, p, t in E]


def shuffle_endpoints(E, rng):
    """Keep predicate multiset; randomly rewire src/tgt from the node multiset."""
    nodes = [n for s, p, t in E for n in (s, t)]
    out = []
    for s, p, t in E:
        out.append((rng.choice(nodes), p, rng.choice(nodes)))
    return out


def decide(scorer, Eq, E2, E3):
    s2, s3 = scorer(Eq, E2), scorer(Eq, E3)
    return 1 if s2 > s3 else (0.5 if s2 == s3 else 0)


def clustered_ci(o, ids, schema, seed=42, nb=10000):
    rng = np.random.RandomState(seed)
    by = defaultdict(list)
    for i in ids:
        by[schema[i]].append(o[i])
    sch = list(by)
    m = np.mean([x for s in sch for x in by[s]])
    bm = [np.mean([x for s in rng.choice(sch, len(sch), replace=True) for x in by[s]])
          for _ in range(nb)]
    return m * 100, np.percentile(bm, 2.5) * 100, np.percentile(bm, 97.5) * 100


def write_per_item(name, per_item, triplets):
    rows = []
    for t in triplets:
        v = per_item[t["id"]]
        rows.append({"triplet_id": t["id"], "schema_id": t["schema_id"],
                     "block": t["block"], "split": t["split"],
                     "q2_beats_q3": bool(v == 1), "score": v})
    n = len(rows)
    wins = sum(1 for r in rows if r["q2_beats_q3"])
    out = {"metadata": {"experiment": name, "matcher": "model-free relation-aware"},
           "by_config": {name: {"config": name,
                                "overall": {"q2_wins": wins, "n": n, "accuracy": wins / n},
                                "per_triplet": rows}}}
    (PI_DIR / f"{name}_results.json").write_text(json.dumps(out, indent=2))


def main():
    scaffolds = json.loads(SCAFFOLDS.read_text())
    triplets = json.loads(DATA.read_text())["triplets"]
    schema = {t["id"]: ((t["id"] - 1) % 20) + 1 for t in triplets}
    split = {t["id"]: t["split"] for t in triplets}
    test = [i for i in split if split[i] == "test"]
    allids = list(split)

    def sc(text):
        return edges(scaffolds[key(text)])

    matchers = {
        "predicate_only": lambda Eq, E2, E3: decide(predicate_only, Eq, E2, E3),
        "triple_aware": lambda Eq, E2, E3: decide(triple_aware, Eq, E2, E3),
        "soft_align": lambda Eq, E2, E3: decide(soft_align, Eq, E2, E3),
        "triple_reverse": lambda Eq, E2, E3: decide(
            lambda a, b: triple_aware(a, reverse(b)), Eq, E2, E3),
    }

    results = {name: {} for name in matchers}
    # deterministic matchers
    for t in triplets:
        Eq, E2, E3 = sc(t["query"]), sc(t["q2_far_analogy"]), sc(t["q3_near_disanalogy"])
        for name, fn in matchers.items():
            results[name][t["id"]] = fn(Eq, E2, E3)

    # structure-destruction: shuffle candidate endpoints, averaged over seeds
    shuffle_acc_test, shuffle_acc_all = [], []
    for s in range(SHUFFLE_SEEDS):
        rng = random.Random(2000 + s)
        per = {}
        for t in triplets:
            Eq = sc(t["query"])
            E2 = shuffle_endpoints(sc(t["q2_far_analogy"]), rng)
            E3 = shuffle_endpoints(sc(t["q3_near_disanalogy"]), rng)
            per[t["id"]] = decide(triple_aware, Eq, E2, E3)
        shuffle_acc_test.append(np.mean([per[i] for i in test]))
        shuffle_acc_all.append(np.mean([per[i] for i in allids]))

    summary = {"lambda": LAMBDA, "shuffle_seeds": SHUFFLE_SEEDS, "matchers": {}}
    print(f"{'matcher':<18}{'held-out 40':<26}{'all 60':<14}")
    print("-" * 58)
    for name in matchers:
        o = results[name]
        write_per_item(f"relmatch_{name}", o, triplets)
        tw = sum(1 for i in test if o[i] == 1)
        aw = sum(1 for i in allids if o[i] == 1)
        # ties counted as 0.5 in accuracy mean
        m, lo, hi = clustered_ci(o, test, schema)
        am = 100 * np.mean([o[i] for i in allids])
        summary["matchers"][name] = {
            "held_out_wins": tw, "held_out_n": len(test),
            "held_out_acc": m, "held_out_ci": [lo, hi],
            "all_wins": aw, "all_n": len(allids), "all_acc": am}
        print(f"{name:<18}{f'{tw}/40 ({m:.1f}%) [{lo:.0f},{hi:.0f}]':<26}"
              f"{f'{aw}/60 ({am:.1f}%)':<14}")

    sm_t = 100 * np.mean(shuffle_acc_test)
    sm_a = 100 * np.mean(shuffle_acc_all)
    summary["matchers"]["triple_shuffle"] = {
        "held_out_acc": sm_t, "all_acc": sm_a,
        "held_out_std": 100 * float(np.std(shuffle_acc_test)),
        "note": f"triple_aware after endpoint shuffle, mean over {SHUFFLE_SEEDS} seeds"}
    print(f"{'triple_shuffle':<18}{f'~{sm_t:.1f}% (destroyed)':<26}{f'~{sm_a:.1f}%':<14}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2))
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
