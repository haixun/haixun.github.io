#!/usr/bin/env python3
r"""
Roadmap6 Section 8/10 -- single source of truth for every empirical number.

Reads the frozen machine-readable result files and emits:
  experiments/results/result_macros.tex        -- \newcommand for every paper number
  experiments/figures/quality_vs_comparisons.tex -- corrected Fig 2 (adds predicate-only
                                                    curve; gold oracle is the ONLY ceiling;
                                                    exhaustive noisy refiner is a baseline)
  experiments/figures/scaling_fixed_targets.tex   -- nested fixed-target N* vs bank size
  experiments/figures/shortlist_matrix_table.tex  -- corrected Table 4 (predicate-only filled)
  experiments/figures/mapping_per_family_table.tex-- Table 3 augmentation (per-family + baselines)

No number is ever hand-copied into LaTeX: the manuscript \input{result_macros.tex}
and uses \Res... macros.  Rerun after any experiment changes.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
RES = ROOT / "experiments" / "results"
FIG = ROOT / "experiments" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

MATRIX = json.loads((RES / "shortlist_full_matrix.json").read_text())
PAIRED = json.loads((RES / "shortlist_paired_deltas.json").read_text())
SCALE = json.loads((RES / "scaling_fixed_targets.json").read_text())
MAP = json.loads((RES / "mapping_per_family.json").read_text())
STRUCT = json.loads((RES / "structured_noise_sensitivity.json").read_text())

MACROS = []


def mac(name, value):
    """Register a LaTeX \newcommand. `name` letters only (no digits)."""
    MACROS.append((name, value))


def pct(x, d=1):
    return f"{100 * x:.{d}f}"


def num(x, d=1):
    return f"{x:.{d}f}"


# ----------------------------- shortlist (1K / 10K, calibrated) -----------------------------
for tag, tw in (("1k", "OneK"), ("10k", "TenK")):
    c = MATRIX[tag]["calibrated"]
    fr = c["family_recall_at_n"]
    rp = c["refine_precision_at1"]
    mac(f"Res{tw}Bank", f"{c['bank_n']:,}".replace(",", "{,}"))
    mac(f"Res{tw}Relevant", str(c["relevant_per_query"]))
    mac(f"Res{tw}RaRecallFifty", pct(fr["relation_aware"]["50"]))
    mac(f"Res{tw}PredRecallFifty", pct(fr["predicate_only"]["50"]))
    mac(f"Res{tw}TextRecallFifty", pct(fr["surface_text"]["50"]))
    mac(f"Res{tw}RaPOne", pct(rp["relation_aware"]["5"]))
    mac(f"Res{tw}PredPOne", pct(rp["predicate_only"]["5"]))
    mac(f"Res{tw}TextPOne", pct(rp["surface_text"]["5"]))
    # P@1 at N=1 (single refinement): the filter alone, before any escalation
    mac(f"Res{tw}RaPOneAtOne", pct(rp["relation_aware"]["1"]))
    mac(f"Res{tw}PredPOneAtOne", pct(rp["predicate_only"]["1"]))
    mac(f"Res{tw}ExhaustiveNoisy", pct(c["exhaustive_noisy_refiner_p1"]))
    mac(f"Res{tw}GoldOracle", pct(c["gold_exhaustive_oracle_p1"]))
    mac(f"Res{tw}NstarFamRa", str(c["n_star_90_family_recall"]["relation_aware"]))
    mac(f"Res{tw}NstarFamPred", str(c["n_star_90_family_recall"]["predicate_only"]))
    mac(f"Res{tw}NstarFamRaFrac", pct(c["n_star_90_family_frac_bank"]["relation_aware"]))
    mac(f"Res{tw}RaBytesPerEp", num(c["systems"]["relation_aware_bytes_per_episode"], 0))

# paired relation-aware vs predicate-only at N=5
for tag, tw in (("1k", "OneK"), ("10k", "TenK")):
    p = PAIRED[tag]["calibrated"]["refined_p1_paired"]["5"]
    mac(f"Res{tw}PairDelta", pct(p["paired_delta"]))
    mac(f"Res{tw}PairLo", pct(p["ci95"][0]))
    mac(f"Res{tw}PairHi", pct(p["ci95"][1]))
    mac(f"Res{tw}PairCorrected", str(p["corrected_ra_over_pred"]))
    mac(f"Res{tw}PairBroken", str(p["newly_broken_ra_vs_pred"]))
mac("ResPairNQueries", str(PAIRED["1k"]["calibrated"]["refined_p1_paired"]["5"]["n_queries"]))

# ----------------------------- scaling (fixed targets) -----------------------------
mac("ResScaleTargets", str(SCALE["m_rel_per_schema"] * 20))
mac("ResScaleSizes", "$\\{1\\text{K},2\\text{K},5\\text{K},10\\text{K}\\}$")
for cond, cw in (("random", "Rand"), ("hard", "Hard")):
    for meth, mw in (("relation_aware", "Ra"), ("predicate_only", "Pred"), ("surface_text", "Text")):
        s = SCALE["conditions"][cond]["calibrated"]["loglog_slope"][meth]
        mac(f"ResScale{cw}{mw}Slope", num(s["mean_loglog_slope"], 2))
        mac(f"ResScale{cw}{mw}SlopeLo", num(s["ci95"][0], 2))
        mac(f"ResScale{cw}{mw}SlopeHi", num(s["ci95"][1], 2))
        ns = s["n_star_by_size"]
        mac(f"ResScale{cw}{mw}NstarLo", str(ns[0]))
        mac(f"ResScale{cw}{mw}NstarHi", str(ns[-1]))

# ----------------------------- mapping (frozen 40) -----------------------------
rk = MAP["ranking_overall"]
mac("ResMapRankCanon", num(rk["canonical"], 1))
mac("ResMapRankFree", num(rk["free"], 1))
mac("ResMapRankGold", num(rk["gold"], 0))
mac("ResMapRankCanonLo", num(rk["canonical_ci95"][0], 1))
mac("ResMapRankCanonHi", num(rk["canonical_ci95"][1], 1))
pr = MAP["ranking_paired_canonical_minus_free"]
mac("ResMapPairDelta", num(pr["paired_delta"], 1))
mac("ResMapPairLo", num(pr["ci95"][0], 1))
mac("ResMapPairHi", num(pr["ci95"][1], 1))
mac("ResMapPairCorrected", str(pr["corrected_canonical_over_free"]))
mac("ResMapPairBroken", str(pr["newly_broken_canonical_vs_free"]))
mac("ResMapRoleFOne", num(MAP["role_map_f1"]["canonical"], 1))
mac("ResMapRoleFOneFree", num(MAP["role_map_f1"]["free"], 1))
# coverage-aware precision / recall / coverage / exact-mapping (unbound gold roles = FN)
mac("ResMapRolePrecCanon", num(MAP["role_map_precision"]["canonical"], 1))
mac("ResMapRolePrecFree", num(MAP["role_map_precision"]["free"], 1))
mac("ResMapRoleRecCanon", num(MAP["role_map_recall"]["canonical"], 1))
mac("ResMapRoleRecFree", num(MAP["role_map_recall"]["free"], 1))
mac("ResMapCoverageCanon", num(MAP["role_coverage"]["canonical"], 1))
mac("ResMapCoverageFree", num(MAP["role_coverage"]["free"], 1))
mac("ResMapExactCanon", num(MAP["role_map_exact_acc"]["canonical"], 1))
mac("ResMapExactFree", num(MAP["role_map_exact_acc"]["free"], 1))
# per-family causal-reversal ranking (canonical): high ranking, zero localization
mac("ResMapRankCausalCanon", num(MAP["ranking_acc_by_family"]["canonical"]["causal_direction"], 1))
# four-way ranking transitions free -> canonical (ties earn half credit)
_tr = pr["transitions_free_to_canonical"]
mac("ResMapTransWrongToCorrect", str(_tr["wrong_to_correct"]))
mac("ResMapTransTieToCorrect", str(_tr["tie_to_correct"]))
mac("ResMapTransCorrectToTie", str(_tr["correct_to_tie"]))
mac("ResMapTransCorrectToWrong", str(_tr["correct_to_wrong"]))
mac("ResMapTransTieToWrong", str(_tr["tie_to_wrong"]))
mac("ResMapEditLocCanon", num(MAP["edit_localization_overall"]["canonical"], 1))
mac("ResMapEditLocFree", num(MAP["edit_localization_overall"]["free"], 1))
mac("ResMapEditLocCausal", num(MAP["edit_localization_by_family"]["canonical"]["causal_direction"], 1))
mac("ResMapEdgePresCanon", num(MAP["edge_preservation"]["canonical"], 1))
mac("ResMapEdgePresFree", num(MAP["edge_preservation"]["free"], 1))
mac("ResMapLocRandom", num(MAP["localization_baselines"]["random_pct"], 1))
mac("ResMapLocEdgeBlind", num(MAP["localization_baselines"]["edge_blind_predicate_only_pct"], 1))
mac("ResMapAvgEdges", num(MAP["localization_baselines"]["avg_candidate_edges"], 1))

# ----------------------------- structured-noise sensitivity (§7) -----------------------------
_sdeltas = [c["paired_delta_at5"]["relation_aware_minus_predicate_only"]
            for c in STRUCT["conditions"].values()]
_sbroken = [c["paired_delta_at5"]["broken"] for c in STRUCT["conditions"].values()]
mac("ResStructNoiseConds", str(len(STRUCT["conditions"])))
mac("ResStructNoiseDeltaLo", pct(min(_sdeltas)))
mac("ResStructNoiseDeltaHi", pct(max(_sdeltas)))
mac("ResStructNoiseBrokenMax", str(max(_sbroken)))

# ----------------------------- write macros -----------------------------
lines = ["% Auto-generated by experiments/analysis/export_result_macros.py -- DO NOT EDIT.",
         "% Every empirical number in the paper is defined here (roadmap6 rule 1.1)."]
for name, value in MACROS:
    lines.append(f"\\newcommand{{\\{name}}}{{{value}}}")
(RES / "result_macros.tex").write_text("\n".join(lines) + "\n")


# ----------------------------- corrected quality-vs-comparisons figure -----------------------------
def coords(series, grid):
    return " ".join(f"({n},{series[str(n)]:.4f})" for n in grid if str(n) in series)


c = MATRIX["1k"]["calibrated"]
grid = c["n_grid"]
rp = c["refine_precision_at1"]
gold = c["gold_exhaustive_oracle_p1"]
exh = c["exhaustive_noisy_refiner_p1"]
fig = rf"""% Auto-generated by experiments/analysis/export_result_macros.py -- do not edit.
% Requires \usepackage{{pgfplots}}\pgfplotsset{{compat=1.16}}.
% SYNTHETIC 1K bank ({c['bank_n']} episodes, {c['n_queries']} queries), calibrated i.i.d. noise.
\begin{{tikzpicture}}
\begin{{axis}}[
    width=0.92\linewidth, height=6cm,
    xlabel={{Expensive relational comparisons per query (shortlist size $N$)}},
    ylabel={{End-to-end P@1 after refinement}},
    xmode=log, log basis x=10, xmin=0.9, xmax=1100,
    ymin=0, ymax=1.05, ytick={{0,0.2,0.4,0.6,0.8,1.0}},
    legend pos=south east, legend cell align=left, legend style={{font=\scriptsize}},
    grid=both, major grid style={{gray!20}}, thick,
]
\addplot[mark=*,color=blue] coordinates {{{coords(rp['relation_aware'], grid)}}};
\addlegendentry{{relation-aware shortlist+refine}}
\addplot[mark=triangle*,color=teal,densely dashed] coordinates {{{coords(rp['predicate_only'], grid)}}};
\addlegendentry{{predicate-only shortlist+refine}}
\addplot[mark=square*,color=red] coordinates {{{coords(rp['surface_text'], grid)}}};
\addlegendentry{{surface-text shortlist+refine}}
\addplot[color=black,dotted,thick,samples=2,domain=0.9:1100] {{{gold:.4f}}};
\addlegendentry{{gold structural oracle (ceiling)}}
\addplot[color=gray,dashdotted,samples=2,domain=0.9:1100] {{{exh:.4f}}};
\addlegendentry{{exhaustive noisy refiner (baseline)}}
\end{{axis}}
\end{{tikzpicture}}
"""
(FIG / "quality_vs_comparisons.tex").write_text(fig)


# ----------------------------- scaling figure (hard + random, relation-aware & predicate-only) -----------------------------
def nstar_coords(cond, meth):
    s = SCALE["conditions"][cond]["calibrated"]["loglog_slope"][meth]
    return " ".join(f"({m},{n})" for m, n in zip(SCALE["sizes"], s["n_star_by_size"]))


sc = SCALE["conditions"]["hard"]["calibrated"]["loglog_slope"]
fig2 = rf"""% Auto-generated by experiments/analysis/export_result_macros.py -- do not edit.
% Nested fixed-target scaling: {SCALE['m_rel_per_schema']*20} fixed gold targets, banks 1K subset 2K subset 5K subset 10K.
% SYNTHETIC construction, calibrated noise. Slope = per-query log--log fit of N* vs bank size.
\begin{{tikzpicture}}
\begin{{axis}}[
    width=0.92\linewidth, height=6cm,
    xlabel={{Bank size $M$ (episodes)}},
    ylabel={{$N^\star$ for 90\% recall of fixed targets}},
    xmode=log, ymode=log, log basis x=10,
    xmin=800, xmax=13000,
    legend pos=north west, legend cell align=left, legend style={{font=\scriptsize}},
    grid=both, major grid style={{gray!20}}, thick,
]
\addplot[mark=*,color=blue] coordinates {{{nstar_coords('hard','relation_aware')}}};
\addlegendentry{{relation-aware, hard negatives (slope {sc['relation_aware']['mean_loglog_slope']:.2f})}}
\addplot[mark=triangle*,color=teal,densely dashed] coordinates {{{nstar_coords('hard','predicate_only')}}};
\addlegendentry{{predicate-only, hard negatives (slope {sc['predicate_only']['mean_loglog_slope']:.2f})}}
\addplot[mark=o,color=blue!50] coordinates {{{nstar_coords('random','relation_aware')}}};
\addlegendentry{{relation-aware, random negatives (slope {SCALE['conditions']['random']['calibrated']['loglog_slope']['relation_aware']['mean_loglog_slope']:.2f})}}
\end{{axis}}
\end{{tikzpicture}}
"""
(FIG / "scaling_fixed_targets.tex").write_text(fig2)


# ----------------------------- corrected Table 4 -----------------------------
def g(d, *ks):
    for k in ks:
        d = d[k]
    return d


c1 = MATRIX["1k"]["calibrated"]
tab = rf"""% Auto-generated by experiments/analysis/export_result_macros.py -- do not edit.
% Shortlist matrix, SYNTHETIC 1K bank ({c1['bank_n']} episodes), calibrated i.i.d. noise
% (level set to the Phase-2 canonical role-map F1). Refiner + tie policy identical across rows.
\begin{{tabular}}{{lcccc}}
\toprule
Shortlist signature & Recall@50 & $N^\star$ (fam.\ 90\%) & \% bank & Refine P@1 ($N{{=}}5$) \\
\midrule
Surface text & {pct(g(c1,'family_recall_at_n','surface_text','50'))} & {c1['n_star_90_family_recall']['surface_text']} & {pct(c1['n_star_90_family_frac_bank']['surface_text'])} & {pct(g(c1,'refine_precision_at1','surface_text','5'))} \\
Predicate-only & {pct(g(c1,'family_recall_at_n','predicate_only','50'))} & {c1['n_star_90_family_recall']['predicate_only']} & {pct(c1['n_star_90_family_frac_bank']['predicate_only'])} & {pct(g(c1,'refine_precision_at1','predicate_only','5'))} \\
\textbf{{Relation-aware}} & \textbf{{{pct(g(c1,'family_recall_at_n','relation_aware','50'))}}} & \textbf{{{c1['n_star_90_family_recall']['relation_aware']}}} & \textbf{{{pct(c1['n_star_90_family_frac_bank']['relation_aware'])}}} & \textbf{{{pct(g(c1,'refine_precision_at1','relation_aware','5'))}}} \\
\midrule
Exhaustive noisy refiner (baseline) & -- & -- & 100 & {pct(c1['exhaustive_noisy_refiner_p1'])} \\
Gold structural oracle (ceiling) & -- & -- & 100 & {pct(c1['gold_exhaustive_oracle_p1'])} \\
\bottomrule
\end{{tabular}}
"""
(FIG / "shortlist_matrix_table.tex").write_text(tab)


# ----------------------------- Table 3 augmentation (mapping per-family) -----------------------------
locc = MAP["edit_localization_by_family"]["canonical"]
rkf = MAP["ranking_acc_by_family"]
fams = MAP["families"]
fam_label = {"role_rebinding": "Role rebinding", "causal_direction": "Causal reversal",
             "edge_redirection": "Edge redirection", "participant_reassignment": "Participant reassign."}
rows = "\n".join(
    rf"{fam_label[f]} & {rkf['canonical'][f]:.0f} & {rkf['free'][f]:.0f} & {locc[f]:.0f} \\"
    for f in fams)
tab3 = rf"""% Auto-generated by experiments/analysis/export_result_macros.py -- do not edit.
% Frozen 40-item mapping test, canonical-role extraction, relational matcher.
% Ranking = P(C+ ranked above surface-matched C-); Edit-loc = exact single-edge localization.
% Random edit-loc baseline = {MAP['localization_baselines']['random_pct']:.1f}\% (mean 1/edges, {MAP['localization_baselines']['avg_candidate_edges']:.0f} edges/graph);
% predicate-only (edge-blind) baseline = {MAP['localization_baselines']['edge_blind_predicate_only_pct']:.1f}\% (all edits preserve the predicate multiset).
\begin{{tabular}}{{lccc}}
\toprule
Transformation family & \multicolumn{{2}}{{c}}{{Ranking acc.}} & Edit-loc. \\
 & canon. & free & (canon.) \\
\midrule
{rows}
\midrule
All (n={MAP['n_items']}) & {MAP['ranking_overall']['canonical']:.1f} & {MAP['ranking_overall']['free']:.1f} & {MAP['edit_localization_overall']['canonical']:.1f} \\
\bottomrule
\end{{tabular}}
"""
(FIG / "mapping_per_family_table.tex").write_text(tab3)

print(f"wrote result_macros.tex ({len(MACROS)} macros)")
print("wrote figures: quality_vs_comparisons.tex, scaling_fixed_targets.tex,")
print("               shortlist_matrix_table.tex, mapping_per_family_table.tex")
