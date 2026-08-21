# Experiments & Artifacts (BOSS Vision, roadmap6 revision)

All paper numbers are generated from machine-readable files here; none are
hand-copied into LaTeX. The manuscript `\input`s `results/result_macros.tex` and the
figure/table `.tex` files under `figures/`.

## Evidence taxonomy (roadmap6 §1.2)

| Kind | What | Where |
| --- | --- | --- |
| Construction validity | facts guaranteed by authored gold graphs (e.g. predicate-only / node-only ties, gold oracle 100%) | `results/mapping_per_family.json` (gold rows), `shortlist_full_matrix.json` (`gold_exhaustive_oracle_p1`) |
| Automatic end-to-end | independently extracted representations | `results/mapping_per_family.json` (canonical / free) |
| Synthetic feasibility | indexed-shortlist probe on seeded synthetic banks + calibrated noise | `results/shortlist_full_matrix.json`, `scaling_fixed_targets.json` |
| Future work | learned state Z, natural-corpus scale, consolidation, generation | not implemented (Vision paper) |

## Reproduce (in order)

```bash
python3 experiments/analysis/run_full_shortlist_matrix.py     # Table 4 matrix (+ gold oracle, exhaustive noisy)
python3 experiments/analysis/analyze_paired_deltas.py          # relation-aware vs predicate-only paired CIs
python3 experiments/analysis/analyze_fixed_target_scaling.py   # nested fixed-target scaling (sublinear test)
python3 experiments/analysis/mapping_per_family.py             # frozen 40-item paired/per-family + baselines
python3 experiments/analysis/analyze_structured_noise.py       # (optional) noise sensitivity sweep
python3 experiments/analysis/export_result_macros.py           # -> result_macros.tex + figures + tables
python3 experiments/analysis/test_ceiling_invariant.py         # guard: only the gold oracle may be a "ceiling"
```

Frozen inputs (do not retune): banks/queries under `data/phase3/`, the 40-item set
`data/mapping_frozen_40.json`, the refiner `scripts/relation_aware_match.py`. Seeds,
noise rates, signatures, grid, and checksums are pinned in
`configs/shortlist_frozen.yaml` and `results/v12_audit.md`.

## Key outcomes (calibrated, synthetic)

- Relation-aware vs predicate-only shortlist is a **small, uncertain** gain: refined
  P@1 @N=5 Δ = +5.0 pts (1K), family-clustered 95% CI [0.0, +13.3], corrects 3 / breaks 0.
  Predicate abstraction supplies most of the shortlist signal.
- The **exhaustive noisy refiner (0.83) is a baseline, not a ceiling** — the shortlisted
  system reaches 0.90; the filter can regularize the noisy refiner. The **gold
  structural oracle (1.00)** is the only ceiling.
- **Sublinear empirical growth** holds only under the nested fixed-target construction
  with hard negatives: relation-aware log-log slope 0.66, CI [0.45, 0.84] (< 1).
- Frozen mapping test: canonical ranking 87.5 vs surface-matched foils, but **edit
  localization 32.5% ≈ random 33.3%** and **causal-reversal localization 0%** — an
  honest limit motivating counterfactual hard negatives and learned relational state.

## Files

- `configs/` — frozen run configs + checksums.
- `results/` — JSON result files, `result_macros.tex`, `v12_audit.md`.
- `figures/` — pgfplots/TikZ `.tex` figures & tables (compiled inline by pdflatex;
  matplotlib is not used).
- `analysis/` — the scripts above; each imports the frozen harness verbatim and only
  ADDS analyses.
- `results/phase3/v12_snapshot/` — preserved pre-revision artifacts.
