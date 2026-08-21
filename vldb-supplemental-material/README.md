# Supplemental Material

Artifacts supporting **"Toward Human-Like Memory: Learning to Remember by Structure"**
(`boss-vision.pdf`). Everything here backs a number, table, or protocol claim in the
paper. Nothing here depends on a trained model: the paper's architecture is
prospective, and this bundle contains only the *demonstrated* evidence — the
diagnostic, the human study, the baseline sweep, and the two structure-aware probes.

**Bundle:** 72 files + a 1,637-file response cache, 8.1 MB.
**Integrity:** `MANIFEST.sha256` (SHA-256 of every shipped file; the response cache
is fingerprinted in aggregate on the last line).
**Anonymity:** no author names, affiliations, emails, or absolute local paths.

---

## 1. What each paper claim maps to

| Paper claim | Value | Artifact | Regenerate |
|---|---|---|---|
| Baseline Q2-over-Q3 (Table 2) | 2–10%, 8 retrievers | `results/per_item/*.json` | `experiments/run_{tfidf,bm25,dense,cross_encoder}.py` |
| Schema-clustered 95% CIs | 20 schemas, 10k bootstrap, seed 42 | `results/aggregate/schema_clustered_results.json` | `scripts/schema_clustered_analysis.py` |
| Human recognition | 99.4% mean [98.3, 100] | `human-study/human-annotation-{1,2,3}.csv` | `scripts/score_human_validation.py` |
| Extract + overlap (Table 3) | 75.0% (30/40) | `results/ablation/extract_overlap_gpt-4o-mini.json` | `scripts/llm_experiments.py` |
| Extract + model match (Table 3) | 87.5% (35/40) | `results/ablation/extract_match_gpt-4o-mini.json` | `scripts/llm_experiments.py` |
| Pairwise reference (Table 3) | 100% (40/40), exhaustive *O(N)* | `results/ablation/pairwise_gpt-4o-mini.json` | `scripts/llm_experiments.py` |
| Minimal-pair ranking | 87.5% [80.0, 95.0] | `results/ablation/mapping40_end2end_constrained.json` | `scripts/mapping_eval.py` |
| Edge localization ≈ chance | 32.5% vs 33.3% | same | same |
| Causal-reversal localization | 0.0% | same | same |
| Role-map F1 / coverage | 88.5 / 97.3% | same | same |
| All `\Res*` macros used in the paper | — | `results/result_macros.tex` | `scripts/export_result_macros.py` |

`results/result_macros.tex` is the single source of truth: every empirical number in
the manuscript is a macro defined there, so no figure is typed by hand.

---

## 2. Directory guide

### `data/` — the diagnostic
- `triplets_60.json` — the 60-triplet diagnostic (20 schemas × 3 realizations).
  Each triplet: query, Q2 far analogy, Q3 surface-matched near-disanalogy.
- `schema_definitions.json` — the 20 relational schemas.
- `dataset_manifest.json`, `checksums.sha256` — version (v2.4.0) and checksums.
- `battery_answer_key.json` — authoritative key (seed 42, `q2_position` per item);
  what the human study is scored against.
- `mapping_frozen_40.json` + `.manifest.json`, `FREEZE_mapping40.md` — the frozen
  40-item **minimal-pair** set: four transformation families (role rebinding,
  causal-direction reversal, edge redirection, participant reassignment), 10 each.
  Both candidates sit in the same foreign domain; the foil differs by a **single
  directed-edge edit** preserving the predicate multiset and node inventory.
  Checksum-pinned *before* the extractor was run.
- `mapping_pilot.json` — the authoring pilot (kept separate from the frozen block).
- `SEALED_TEST_SET.md`, `ANNOTATOR_INSTRUCTIONS.md` — freeze note and instructions.

### `human-study/` — the 3-rater blinded validation
- `human-annotation-{1,2,3}.csv` — per-item judgments. Each rater scored **both**
  candidates on Surface and Structure (1–5, plus confidence); the rater's implied
  choice is the candidate with the higher **Structure** score. There was no separate
  direct-choice question and no foil triplets.
- `human_validation_instructions.md`, `human_validation_analysis_plan.md` — the
  instrument and the analysis plan, both fixed before annotation.
- `human_scores.json` — scored output.

Two reading notes a reviewer will want:
1. **CSV layout differs.** File 1's header is on row 0; files 2 and 3 have a title
   block and their header on row 3. The scorer handles both.
2. **Label typo.** Files 2 and 3 *both* carry the title "Annotator 2". Their data
   differ; they are distinct raters. This is a spreadsheet-title typo, not duplicated
   data.
3. **Disclosed revision.** Two Q3 candidates (items 23, 28) were clarified and
   re-rated mid-study. The paper therefore reports the **58-item frozen subset** as
   confirmatory and the repaired 60-item set as robustness; the headline is unchanged
   either way. Pre- and post-revision ratings are never mixed within an item.

### `results/`
- `per_item/` — 13 files of per-item outcomes: the 8 evaluated retrievers (TF-IDF,
  BM25, `text-embedding-3-large`, cross-encoder, and the four open bi-encoders,
  which share `dense_results.json`), the three LLM conditions, four model-free
  relation-matcher variants, and the answer-key ceiling (`oracle`, 100% **by
  construction** — it reads annotation fields directly and is not an inference
  method).
- `ablation/` — the 40-item abstraction probe, the minimal-pair mapping study
  (gold / end-to-end / role-constrained), a shuffled-assignment control, and a
  weaker-extractor reproduction (`gpt-4o-mini`: 73% overlap, 88% model match).
- `aggregate/` — schema-clustered bootstrap CIs and the summary table.
- `result_macros.tex` — all `\Res*` macros.

### `scaffolds/` — cached structural extractions
Frozen relational scaffolds, extracted **one episode at a time** (the extractor never
saw a triplet's siblings) and cached **before** any matching ran. This is what makes
the structure-aware rows auditable: the abstraction step is fixed and inspectable,
independent of the matcher applied on top.

### `llm-cache/responses/` — 1,637 cached model responses
Every request/response keyed by a content hash of prompt + model snapshot. The
evaluated LLM outputs are therefore **reproducible without API access**, even though
the API itself is not deterministic.

### `scripts/` and `experiments/`
Scoring and evaluation code: the human-study scorer, the schema-clustered bootstrap,
the mapping/minimal-pair evaluator, the relation-aware matcher, the four baseline
runners, `BASELINE_PROTOCOL.md`, and the macro exporter.

### `prompts/`
- `PROMPT_SPEC.md` — full extractor/matcher specification: model snapshots
  (`gpt-4o-2024-08-06`, `gpt-4o-mini-2024-07-18`), temperature 0, JSON mode, the
  scaffold schema, the closed 20-predicate vocabulary, canonicalization rules, the
  model-free matcher formula, and the prompt-development discipline (prompts were
  worded on the 20-item pilot only; the frozen 40 were never inspected).
- `mask_integrity_frozen.yaml` — frozen config for the mask-integrity probe.

---

## 3. Reproducing

```bash
python3 scripts/score_human_validation.py       # human study: 99.4% [98.3,100], AC1
python3 scripts/schema_clustered_analysis.py     # clustered CIs (10k boot, seed 42)
python3 experiments/run_tfidf.py                # sparse baselines
python3 experiments/run_dense.py                # open bi-encoders (downloads weights)
python3 scripts/mapping_eval.py                 # minimal-pair rank + edge localization
```

Open-model baselines and every scoring step run offline. Reproducing the LLM rows
from scratch needs `OPENAI_API_KEY`; reading them from `llm-cache/responses/` does
not. `run_dense.py` downloads public sentence-transformer weights.

**AC1, both variants.** The scorer prints Gwet's AC1 two ways: **1.00** with ties
dropped, and **0.985** (→ 0.99) treating the single tie as a third category. The
`\ResHumanACOne` macro carries the conservative 0.99. Neither choice moves the
headline: 179 of 180 rater–item comparisons favored Q2, one tied, none favored Q3.

---

## 4. Scope — what is *not* here

Stated plainly, because the paper's central architecture is a proposal:

- **No trained consolidation engine.** No learned state `Z`, routing key `c=ρ(Z)`,
  residual channel, or trained matcher. These are proposed (paper Table 1) and
  tested by H-Structure / H-Consolidation / H-Generation / H-Interface, none of which
  this bundle settles.
- **The structure-aware rows use a stand-in extractor** (a general-purpose LLM), not
  the proposed `Z`. They support automatic *abstraction*, not schema generalization.
- **No held-out split.** All realizations were authored together; no split is
  genuinely held out. The 40-item block is a frozen *reporting* block, not a test set.
- **The 100% pairwise row is an exhaustive O(N) reference**, not a scalable retriever.
- **No natural-analogy corpus.** Dataset (b) — the decisive transfer falsifier — does
  not exist yet.
- **Embedding cache excluded** (11 MB): the open-model vectors are recomputable via
  `run_dense.py`.

---

## 5. Note on the companion paper

A separate systems-framed version (`boss-vision-short.tex`, VLDB) shares this
diagnostic and these result macros but adds scaling/shortlist experiments
(H-Scale, H-System) that the position paper deliberately drops. Those artifacts —
shortlist matrices, fixed-target scaling, the 1K/10K probes — live in the repo's
`supplement/` directory and are **not** duplicated here.
