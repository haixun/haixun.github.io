# FREEZE — 40-item structural-mapping test (Phase 1 freeze protocol)

Status: **pipeline frozen specification**. This document pins every component that
touches the 40-item held-out mapping set *before* the extractor is run once on the
frozen texts. Nothing listed here may be tuned on the 40 items. The 6-item
`mapping_pilot.json` prototype and the 24-item `relation_only_candidates.json` set
are permanently **development evidence** and are excluded from the held-out claim.

Rule (Phase 1.5 step 6): the frozen extractor is run on the 40 frozen texts
**exactly once**; the resulting scaffold caches are committed and never regenerated.

---

## 1. Extractor snapshot

| Field | Frozen value |
|---|---|
| Model | `gpt-4o-2024-08-06` |
| Temperature | `0.0` |
| Response format | JSON mode (`response_format={"type":"json_object"}`) |
| Max tokens | `800` |
| Decode seed | `SEED` as set in `scripts/llm_experiments.py` |
| Prompt source of truth | `scripts/llm_experiments.py` (SHA below) |

Two extractor entry points are frozen:
- free-form: `extract_scaffold` (system prompt `EXTRACT_SYS`);
- role-constrained (Option A, primary for the mapping test):
  `extract_scaffold_constrained` (system prompt `EXTRACT_ROLES_SYS`).

Node labels are **never** rewritten post hoc (that would be model-in-the-loop
curation, violating protocol P1). Out-of-vocabulary node leakage is left visible and
measured as an extraction-faithfulness screen (`node_vocab_leakage`).

## 2. Predicate ontology (frozen; `RELATION_VOCAB`, 20 predicates)

```
intends, causes, prevents, enables, conceals, deceives,
manufactures_threat, sacrifices_for, exploits, misattributes_credit,
appears_positive, actually_negative, appears_negative, actually_positive,
reverses_expectation, tests_loyalty, feigns_inability, protects_by_withholding,
harms_by_helping, reveals_hidden_trait
```

Temporal-order predicates are intentionally **absent** (the ontology cannot express
them; we do not extend the ontology to hit a transformation-type count).

## 3. Role vocabulary (frozen; `ROLE_VOCAB`)

```
AGENT, TARGET, THIRD_PARTY, ACTUALITY
```

Matcher-permutable roles: `AGENT, TARGET, THIRD_PARTY` (`relation_aware_match.ROLES`).
`ACTUALITY` is a non-permuted literal slot (a known limitation on directional/causal
items; recorded here, not tuned away).

## 4. Matcher parameters (frozen; `scripts/relation_aware_match.py`)

| Param | Frozen value |
|---|---|
| `LAMBDA` (contradiction penalty, triple-aware) | `0.5` |
| `SOFT_LAMBDA` (soft-align edge weight) | `1.0` |
| `SOFT_ETA` (entropic mirror-ascent step) | `1.0` |
| Role permutation search | exhaustive over `permutations(ROLES)` |
| Primary matcher | `triple_aware` |
| Secondary matcher | `soft_align` (reported as footnote/secondary row) |
| Controls | `node_only` (edge-blind), `edge_shuffle` (destroyer) |

## 5. Eval / harness state

- Mapping harness: `scripts/mapping_eval.py`
  (`--mode {gold,end2end}`, `--constrain-roles`, `ALLOWED_NODES = ROLES ∪ {ACTUALITY}`).
  DATA is pinned to `data/mapping_frozen_40.json`. Phase-2 metrics: role-map F1
  (micro), false-contradiction rate, C+/C- score split, family-clustered ranking CI.
- Construction validators: `scripts/validate_triplets.py` (+ Phase-1 `validate_mapping40.py`).
- Table builder: `scripts/build_mapping_table.py` -> `results/ablation/mapping40_table.tex`
  (5 rows: node inventory, predicate-only, free-form relational, canonical-role
  relational, gold ceiling) + go/no-go gate.
- Frozen free-form cache: `results/llm/scaffolds_mapping40.json`.
- Frozen constrained cache: `results/llm/scaffolds_mapping40_constrained.json`.
- Frozen-run outputs: `results/ablation/mapping40_{gold,end2end,end2end_constrained}.json`.
  (The n=6 pilot caches `scaffolds_mapping*.json` and outputs `mapping_pilot_*.json`
  are DEV and kept separate; the frozen run never reuses them.)

## 6. Component checksums (SHA-256, at freeze time)

```
486c691a9174daadcff787b4faa543fc2975482706a034a13cf58811fa4b7e50  scripts/llm_experiments.py
781c17c5ff8c92140d9d2bf4636907424e2d53723deaa5efcbdd3ac0d60a0cc2  scripts/relation_aware_match.py
095129941f780700895a97473903034234dd37dc6e26630daeee47d144e2a9e9  scripts/mapping_eval.py
516a6dc9db34dc21c93b4bb6f6c9cdb5f6df8681cfc0f155f381fcb92abf4486  scripts/validate_triplets.py
fc2b61379abf6fba09959207a898e866abb3d83e27088daf4743f2781eb26fe2  data/mapping_pilot.json  (DEV prototype, reference only)
```

Regenerate/verify with:

```bash
shasum -a 256 scripts/llm_experiments.py scripts/relation_aware_match.py \
  scripts/mapping_eval.py scripts/validate_triplets.py
```

## 7. 40-text checksum (Phase 1.5 step 5 — freeze commit)

Author-validated, **pre-adjudication** payload checksum (sha256 over the canonical
item payload; see `scripts/build_mapping40.py` and `data/mapping_frozen_40.manifest.json`):

```
e6e325d9ab1ed4102a2aac96e2d24bab2b80ab2200b599bf21d760696a149728  data/mapping_frozen_40.json (item payload)
```

Status: the 40 items are authored, pass all deterministic construction asserts
A1–A7 (`scripts/validate_mapping40.py`; report in
`results/ablation/validate_mapping40_report.json`), AND have been through human
adjudication (Phase 1.5 step 4). A7 is the Phase 1.4b far-analogy gate: every
candidate is lexically far from its query (token-Jaccard ≤ 0.35; observed mean
0.20, max 0.33), so a structural match cannot be won by string copying.
Adjudication of prose realization is now RESOLVED (see resolution log below).
ACCEPT sign-off given; the frozen extractor has now been run exactly once on
these texts (Phase 1.5 step 6 — COMPLETE; see §8). The scaffold caches are
committed and must never be regenerated.

Checksum history (authoring / adjudication revisions):
- `13b2345…` — initial author-validated payload (A1–A6); candidates were
  near-paraphrases of their queries (query↔candidate Jaccard up to ~0.76).
- `5c22051…` — all 40 candidate pairs re-authored as genuine far analogies and
  A7 added to the validator.
- `e6e325d…` — adjudication plausibility pass (current). chk1/chk2/chk3/chk5 = Y
  on all 40 in the returned annotation. chk4 (both-candidates-plausible) was
  flagged N on the reversal/reassignment families; triage found the annotation
  over-flags (identical structures rated both N and Y; the clearly-plausible
  edge_redirection items 321–330 all flagged N with no notes). Resolution:
  items 301–320 (role_rebinding + causal_direction) were re-authored to remove
  genuine and mild plausibility strains — subordinate-acts-on-superior reversals
  reframed (303, 304, 307, 310), trust-presupposition clashes repaired (301, 302,
  305, 306, 308, 309), and bare reverse-causation counterfactuals given an
  explicit plausible mechanism (311–320). Items 321–340 accepted as-is (adjudicator
  decision). Item 307 (harms_by_helping reversal, irreducibly strained) took the
  agreed marginal fix ("constant propping-up"). A1–A7 still pass 40/40; graphs are
  generated from `base`/`edit`, so prose edits cannot change the structural
  asserts.

## 8. Frozen extractor run (Phase 1.5 step 6 — COMPLETE, run once)

Ran `gpt-4o` once per entry point on the 40 frozen texts (120 extractions each);
caches at `results/llm/scaffolds_mapping40{,_constrained}.json`; eval outputs at
`results/ablation/mapping40_end2end{,_constrained}.json`; table at
`results/ablation/mapping40_table.tex`. Primary matcher = `triple_aware`.

| Method | Ranking acc (95% CI) | Role-map F1 | Edit-loc. | Node OOV |
|---|---|---|---|---|
| Node inventory (control)   | 50.0 [50,50]  | n/a  | n/a  | — |
| Predicate-only (control)   | 50.0 [50,50]  | n/a  | n/a  | — |
| Free-form relational       | 78.8 [62,95]  | 95.4 | 5.0  | 34.9% (122/350) |
| Canonical-role relational  | 87.5 [80,95]  | 89.7 | 32.5 | 0.2% (1/427) |
| Gold (ceiling)             | 100.0 [100,100] | 100.0 | 100.0 | — |

- False-contradiction rate = 0.0% for both extractors (no hallucinated polarity
  contradiction on the isomorphic C+).
- edge_shuffle destroyer control (gold) = 53.6% ranking, 40.8% edge-preservation
  (structure genuinely carries the signal; scrambling edges collapses to chance).
- C+/C- margin (canonical, triple_aware): C+=0.593, C-=0.337, margin=+0.256.

**Go/no-go gate outcome: REVIEW (not a clean GO).**
- PASS: canonical ranking beats the best structure-blind control by +37.5 pts
  (87.5% vs 50.0%; gate needs ≥10) — the headline structure-over-surface claim holds.
- PASS: canonical role-map F1 = 89.7 (gate needs ≥50) — roles are recovered.
- FAIL: canonical edit-localization = 32.5% (gate needs ≥50) — the matcher scores
  the correct candidate above the counterfactual but pinpoints *which* single edge
  was flipped only ~1/3 of the time. This is an honest limitation, not tuned away;
  it reflects the `ACTUALITY` non-permuted-slot limitation recorded in §3 and the
  difficulty of single-edge edit isolation on causal/directional items.

Interpretation to carry into the paper: report the ranking + role-map result as the
positive finding, and report edit-localization as an open weakness (do not claim
edit-localization is solved). Free-form extraction additionally leaks vocabulary
badly (34.9% OOV) and localizes at 5.0%, motivating the canonical-role constraint.
