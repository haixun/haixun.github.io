# Human Validation Instructions for Q2 vs Q3 Diagnostic Dataset

## Overview

You are being asked to evaluate a dataset designed to test whether retrieval systems can distinguish **structural similarity** from **surface similarity** between narrative episodes.

Each item consists of:
- A **Query** episode
- A **Candidate A** episode
- A **Candidate B** episode

Your task is to rate similarity and identify structural relationships, **without knowing which candidate is intended to be structurally similar vs. surface similar**.

## Important: This is a Blinded Evaluation

- Candidate labels (A/B) are **randomized** and do not indicate intended similarity type
- Do not try to guess which is the "correct" answer
- Rate based on your honest assessment of the text

## Rating Scales

Use the following 1-5 scales:

### Surface Similarity (1-5)
How similar are the surface features: vocabulary, domain, entities, setting?

1. **Very Different**: Completely different domain, vocabulary, and entities
2. **Mostly Different**: Different domain with occasional shared words
3. **Somewhat Similar**: Some overlap in domain or vocabulary
4. **Mostly Similar**: Same domain, many shared terms
5. **Very Similar**: Same domain, very similar vocabulary and entities

### Structural Similarity (1-5)
How similar is the underlying relational structure: roles, intentions, causal mechanisms, outcomes?

1. **Very Different**: Different roles, intentions, and causal patterns
2. **Mostly Different**: Some shared elements but key differences in structure
3. **Somewhat Similar**: Parallel structure with notable differences
4. **Mostly Similar**: Same basic structure with minor variations
5. **Very Similar**: Essentially the same relational pattern

### Confidence (1-5)
How confident are you in your structural similarity rating?

1. **Very Uncertain**: Hard to determine structure
2. **Somewhat Uncertain**: Structure is ambiguous
3. **Neutral**: Moderately confident
4. **Somewhat Confident**: Structure is fairly clear
5. **Very Confident**: Structure is unambiguous

## Task Procedure

For each item:

1. Read the Query episode carefully
2. Read Candidate A and Candidate B
3. For **each candidate**, rate:
   - Surface similarity to Query (1-5)
   - Structural similarity to Query (1-5)
   - Your confidence in the structural rating (1-5)
4. Provide a brief explanation (1-2 sentences) of:
   - What structure you perceive in the Query
   - How each candidate relates to that structure

## Example

**Query**: "My boss invents fake emergencies to motivate us. Last week he said our client was leaving but they'd actually just renewed."

**Candidate A**: "My dad would shout it's 7 AM when it was 6:15. He thought fake urgency made me punctual."

**Candidate B**: "My boss warned about a real client complaint. We worked late and fixed it. His warning was accurate."

Example ratings for Candidate A:
- Surface: 2 (different domain - family vs. workplace)
- Structure: 5 (same pattern - authority fabricates urgency through deception)
- Confidence: 5

Example ratings for Candidate B:
- Surface: 5 (same domain - workplace, boss, client)
- Structure: 2 (different - warning is genuine, not fabricated)
- Confidence: 5

## Data Entry Format

Use the provided CSV template. Each row should contain:
- `item_id`: The item number
- `candidate`: "A" or "B"
- `surface_rating`: 1-5
- `structure_rating`: 1-5
- `confidence`: 1-5
- `explanation`: Brief free-text explanation

## Time Estimate

- Each item should take 2-3 minutes
- Total for 60 items: approximately 2-3 hours
- Please take breaks as needed

## Questions?

Contact the study coordinator if you have questions about:
- What counts as "structure" vs. "surface"
- How to handle ambiguous cases
- Technical issues with the rating form

Thank you for your participation!
