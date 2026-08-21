# Contemporary Baseline Protocol for Q2/Q3 Diagnostic

This document specifies the protocol for running contemporary baselines on the 60-triplet diagnostic.

## Study V2: Contemporary Baseline Stress Test

**Question:** Which existing retrieval and reasoning strategies fail when surface and structure conflict, and which already succeed?

## Baselines to Include

### 1. Sparse and Dense Retrieval (Already Implemented)

| Model | Status | Script |
|-------|--------|--------|
| TF-IDF (unigram, bigram) | Complete | `experiments/run_tfidf.py` |
| BM25 (k1=1.5, b=0.75) | Complete | `experiments/run_bm25.py` |
| all-MiniLM-L6-v2 | Complete | `experiments/run_dense.py` |
| all-mpnet-base-v2 | Complete | `experiments/run_dense.py` |

### 2. Additional Dense Embeddings (Planned)

| Model | Specification | Priority |
|-------|---------------|----------|
| E5-large-v2 | `intfloat/e5-large-v2` | High |
| BGE-large-en-v1.5 | `BAAI/bge-large-en-v1.5` | High |
| GTE-large | `thenlper/gte-large` | Medium |

**Protocol:**
- Use mean pooling over token embeddings
- Normalize vectors before cosine similarity
- Report: Q2>Q3 accuracy, similarity margins, confidence intervals

### 3. Cross-Encoder Reranker (Planned)

| Model | Specification |
|-------|---------------|
| ms-marco-MiniLM-L-6-v2 | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| BGE-reranker-large | `BAAI/bge-reranker-large` |

**Protocol:**
- Input format: `(query, candidate)` pairs
- Score both Q2 and Q3 against query
- Rank by score
- Report: Q2>Q3 accuracy, score margins

### 4. LLM Pairwise Judge (Planned)

**Models to test:**
- GPT-4o (or latest available)
- Claude 3.5 Sonnet
- Llama 3.1 70B (if available)

**Prompt template:**
```
You are evaluating structural similarity between narratives.

Query: {query}

Candidate A: {candidate_a}
Candidate B: {candidate_b}

Which candidate shares more of the Query's underlying relational structure?
Consider: roles, intentions, causal patterns, and outcomes.
Ignore: surface vocabulary, domain, specific entities.

Answer with just "A" or "B".
```

**Protocol:**
- Run twice with position swap (A/B vs B/A)
- Report: Q2>Q3 accuracy, position sensitivity, consistency
- Fixed temperature (0.0 if available)
- Record exact model version and timestamp

### 5. LLM Abstraction + Embedding (Planned)

**Protocol:**
1. Use LLM to generate structural abstract for each episode:
   ```
   Extract the core relational pattern from this narrative.
   Focus on: roles, intentions, causal relationships, outcomes.
   Provide a 2-3 sentence abstract.

   Narrative: {text}
   ```

2. Embed the abstracts using a dense model (e.g., E5-large)
3. Compare abstract embeddings
4. Report: Q2>Q3 accuracy

### 6. YARN (If Available)

Reference: Khojasteh et al., 2026. "Enhancing Structural Mapping with LLM-derived Abstractions for Analogical Reasoning in Narratives"

**Protocol:**
- Use published code if available
- Otherwise, implement core components:
  1. LLM-derived structural abstraction
  2. Structure-Mapping Engine (SME) alignment
- Report: Q2>Q3 accuracy, alignment quality

### 7. SME over Independently Annotated Structures (Future Work)

**Prerequisites:**
- Independent per-episode structural annotations (roles, events, relations)
- Annotations must not use pair-level labels

**Protocol:**
1. Annotate Query, Q2, Q3 independently
2. Apply SME or similar matcher
3. Report: Q2>Q3 accuracy, alignment scores

**Status:** Deferred to future work (requires independent annotations)

## Reporting Requirements

For each baseline, report:

1. **Configuration**
   - Exact model version/checkpoint
   - Preprocessing steps
   - Hyperparameters
   - Random seed (if applicable)

2. **Results**
   - Q2>Q3 accuracy (all 60 items)
   - Q2>Q3 accuracy (Realizations B+C)
   - 95% CI (item-level Wilson + schema-clustered bootstrap)
   - Per-schema consistency

3. **Error Analysis**
   - Items where Q2>Q3 (successes)
   - Items where Q3>Q2 (failures)
   - Tie handling

4. **Position Controls (for LLM baselines)**
   - Accuracy with original ordering
   - Accuracy with swapped ordering
   - Position bias metrics

## Analysis

1. Compare all baselines on common metrics
2. Identify which methods succeed (if any)
3. Characterize failure modes
4. Report if strong baselines solve the diagnostic without structural training

## Timeline

| Phase | Baselines | Priority |
|-------|-----------|----------|
| Phase 1 | E5-large, BGE-large | High |
| Phase 2 | Cross-encoder, LLM judge | High |
| Phase 3 | LLM abstraction, YARN | Medium |
| Future | SME with independent annotations | After annotations |
