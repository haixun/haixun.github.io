# Human Validation Analysis Plan

**Status:** Pre-registered before seeing any human responses
**Created:** 2026-07-19
**Dataset Version:** v2.4
**Dataset Checksum:** `6d25163bb59e176fb1015b05e761fc79e0f4f11f09dffccae52fa14837797cf7`

## 1. Study Design

### 1.1 Task
Annotators independently evaluate each triplet (Query + Candidate A + Candidate B) and determine which candidate shares more of the query's underlying relational structure.

### 1.2 Input Data
- 60 triplets (20 schemas × 3 realizations)
- Candidates are randomized per annotator (A/B order varies)
- Annotators are blind to:
  - Q2/Q3 labels
  - Schema IDs
  - Answer-key annotations
  - Intended correct answer

### 1.3 Annotator Requirements
- Minimum 3 annotators
- English fluency required
- No access to this analysis plan until completion
- Independent work (no discussion between annotators)

## 2. Data Collection Fields

### 2.1 Per-Item Fields
| Field | Type | Description |
|-------|------|-------------|
| item_id | int | Triplet ID (1-60) |
| annotator_id | string | Anonymized annotator identifier |
| structural_choice | A/B/Neither/Unclear | Which candidate shares query's structure |
| confidence | 1-5 | Confidence in structural judgment |
| rationale | text | Brief explanation (optional) |
| completion_time | seconds | Time spent on item |

### 2.2 Excluded Responses
Before analysis, exclude:
- Items with completion_time < 10 seconds (too fast)
- Items with completion_time > 600 seconds (likely distraction)
- Annotators with > 20% "Unclear" responses
- Annotators who fail > 50% of attention checks (if used)

## 3. Primary Analysis

### 3.1 Agreement with Intended Labels
For each item, compute whether annotator's structural_choice matches the intended Q2 answer:
- Map A/B to Q2/Q3 using randomization key
- Q2 is the intended structurally-similar candidate
- "Match" = annotator chose Q2; "Mismatch" = annotator chose Q3

**Primary metric:** Proportion of items where majority (≥2/3) of annotators chose Q2

### 3.2 Inter-Annotator Agreement
- Fleiss' Kappa for 3+ annotators on structural_choice
- Percent exact agreement (all 3 same answer)
- Percent majority agreement (≥2/3 same answer)

### 3.3 Confidence Analysis
- Mean confidence by outcome (match vs mismatch)
- Correlation between confidence and agreement

## 4. Secondary Analysis

### 4.1 Schema Consistency
- Per-schema agreement rate across 3 realizations
- Identify schemas with low agreement (potential construct issues)

### 4.2 Realization Effects
- Compare agreement rates: Realization A vs B vs C
- Test for systematic differences between realizations

### 4.3 Error Analysis
- Identify items with low agreement
- Categorize disagreement sources:
  - Both Q2 and Q3 seem structurally similar
  - Neither seems structurally similar
  - Ambiguous relational structure
  - Surface features overwhelm structure judgment

## 5. Adjudication Rules

### 5.1 Item Acceptance
Accept item for final diagnostic if:
- ≥2/3 annotators chose Q2 (intended answer)
- Mean confidence ≥ 3.0 for correct responses

### 5.2 Item Revision Candidates
Flag for revision if:
- Majority chose Q3 (wrong answer)
- Majority chose "Neither" or "Unclear"
- High disagreement (no majority)

### 5.3 Item Exclusion
Exclude from final diagnostic if:
- After revision attempt, still fails acceptance criteria
- Annotators report fundamental construct issue

## 6. Reporting

### 6.1 Summary Statistics
- N items passing acceptance criteria
- Overall agreement with intended labels
- Inter-annotator reliability
- Confidence distributions

### 6.2 By-Schema Report
- Schema-level acceptance rates
- Schemas requiring revision
- Schemas excluded

### 6.3 Limitations Acknowledged
- Annotator selection bias
- Possible cultural/domain biases
- Training effects across items
- Fatigue effects

## 7. Pre-Registration Commitment

This analysis plan was written before viewing any annotator responses. Any deviations will be documented in the final report with justification.

**DO NOT MODIFY THIS FILE AFTER ANNOTATION BEGINS.**

## 8. Synthetic Test Fixtures

For code development, use synthetic data only:
- `test_fixtures/synthetic_annotations.csv` - clearly labeled test data
- Never mix synthetic and real annotations
- Synthetic data never enters paper results
