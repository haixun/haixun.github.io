# Extraction and Matching Prompt Specification

This directory documents the prompt-based extraction and matching procedures used
for the "Automatic structural methods" rows of the diagnostic (Supplement Table S3)
and the frozen structural-mapping study (Supplement Table S5/S6). No raw prompt
text files were stored separately in the frozen artifact; the operative behavior is
fully specified below and is reproducible from the cached, content-hashed responses
shipped with the artifact.

## Extractor configuration

- **Model snapshot:** `gpt-4o-2024-08-06` (primary); `gpt-4o-mini-2024-07-18`
  (robustness reproduction).
- **Decoding:** temperature `0`, JSON-mode (structured output).
- **Caching:** every request/response is keyed by a content hash of the prompt +
  model snapshot and cached, so the *evaluated outputs are frozen and reproducible
  from the artifact* even though the API itself is not deterministic.
- **Isolation:** each unique episode is extracted **once, independently** — the
  model never sees the sibling episodes of a triplet — and all outputs are cached
  **before** any matching runs.
- **Prompt development discipline:** prompts were worded using **only** the 20-item
  development block. The 40 held-out triplets and the frozen 40-item mapping set
  were never inspected while wording prompts. The mapping set was checksum-pinned
  before the extractor was run once.

## Scaffold schema (the extraction target)

Each episode is mapped to an abstract relational **scaffold**:

```json
{
  "roles":     ["AGENT", "TARGET", "THIRD_PARTY"],
  "relations": [["AGENT", "predicate", "TARGET"], ...],
  "pattern":   "one abstract sentence with no surface nouns"
}
```

- **roles:** generic labels from a closed vocabulary
  (`AGENT`, `TARGET`, `THIRD_PARTY`; the canonical-role variant adds an
  `ACTUALITY` literal role). No domain nouns.
- **relations:** `[source, predicate, target]` triples over a **fixed,
  schema-agnostic vocabulary of 20 abstract predicates** —
  `intends`, `conceals`, `deceives`, `appears_positive`, `actually_negative`,
  `manufactures_threat`, ... — with **no explicit schema-ID field**. (Combinations
  of predicates could still act as an *implicit* schema code; because every schema
  appears in the development block, schema-holdout generalization remains open.)
- **pattern:** a single abstract sentence describing the mechanism, with no
  surface nouns.

## Canonicalization

- Predicates are lower-cased and restricted to the 20-predicate vocabulary;
  out-of-vocabulary predicates are dropped.
- Roles are upper-cased and restricted to the closed role vocabulary
  (canonical-role variant); free-form extraction leaves unbound role labels as
  domain literals (counted as misses under coverage-aware role-map F1).

## Model-free matcher (the cheap query-time comparison)

The prespecified model-free matcher scores

```
score = Jaccard(predicate_set_q, predicate_set_c)
        + 0.15 * (matching appearance/reality polarity axes)
```

and prefers the higher-scoring candidate. It is order-invariant by construction.

Post-hoc model-free matcher family (Supplement S8): a triple-aware matcher
`max_pi Jaccard(E_q, pi(E_c)) - lambda * Contra` over directed labelled triples
(`lambda = 0.5`, maximizing over the six relabelings of the generic roles), a soft
doubly-substochastic partial-alignment matcher, and a predicate-only Jaccard
matcher. See Supplement S8 for results and the negative result that predicate-only
Jaccard is the strongest model-free matcher.

## Model-based matcher (`Extract + model match`, `Pairwise judge`)

- **Extract + model match:** the same cached scaffolds are compared by one model
  call per candidate at query time.
- **Pairwise judge:** the model is shown the query and a candidate episode
  directly (no scaffold) — an expensive automatic reference, an `O(N)` per-pair
  scan, **not** an oracle and **not** a scalable method.
- Model-based judgments use a single randomized candidate order (seed `42`), which
  mitigates but does not fully rule out position effects; evaluating both orders is
  left to follow-on work.

## Robustness checks

- **Foreign-scaffold control:** replacing the query with a *foreign* scaffold drops
  model-free overlap accuracy to chance (52%), confirming the score reflects
  genuine query--candidate correspondence and not a candidate-side artifact.
- **Weaker extractor:** `gpt-4o-mini-2024-07-18` reproduces the pattern
  (73% overlap, 88% model match).
