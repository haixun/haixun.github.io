#!/usr/bin/env python3
"""
Generate a spreadsheet for 3 human annotators to validate the Q2/Q3 diagnostic.

The task: For each item, decide which candidate (A or B) shares the same
underlying relational structure as the Query.

Output: CSV file with columns for 3 annotators
"""

import json
import csv
import random
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "triplets_60.json"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "human_validation_3annotators.csv"

def main():
    random.seed(42)  # For reproducible randomization

    with open(DATA_PATH) as f:
        data = json.load(f)

    rows = []
    answer_key = []

    for t in data["triplets"]:
        # Randomize which is A and which is B
        if random.random() < 0.5:
            candidate_a = t["q2_far_analogy"]
            candidate_b = t["q3_near_disanalogy"]
            correct_answer = "A"  # Q2 is structurally similar
        else:
            candidate_a = t["q3_near_disanalogy"]
            candidate_b = t["q2_far_analogy"]
            correct_answer = "B"  # Q2 is structurally similar

        rows.append({
            "item_id": t["id"],
            "block": t["block"],
            "query": t["query"],
            "candidate_a": candidate_a,
            "candidate_b": candidate_b,
            "annotator_1": "",
            "annotator_2": "",
            "annotator_3": "",
            "notes": ""
        })

        answer_key.append({
            "item_id": t["id"],
            "correct": correct_answer,
            "q2_position": correct_answer
        })

    # Write main spreadsheet
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "item_id", "block", "query", "candidate_a", "candidate_b",
            "annotator_1", "annotator_2", "annotator_3", "notes"
        ])
        writer.writeheader()
        writer.writerows(rows)

    # Write answer key (keep separate!)
    answer_key_path = OUTPUT_PATH.parent / "human_validation_answer_key.json"
    with open(answer_key_path, "w") as f:
        json.dump(answer_key, f, indent=2)

    print(f"Created spreadsheet: {OUTPUT_PATH}")
    print(f"Created answer key: {answer_key_path}")
    print(f"\nItems: {len(rows)}")
    print(f"  Block A (development): {sum(1 for r in rows if r['block'] == 'A')}")
    print(f"  Block B (test): {sum(1 for r in rows if r['block'] == 'B')}")
    print(f"  Block C (test): {sum(1 for r in rows if r['block'] == 'C')}")

    print("\n" + "="*70)
    print("INSTRUCTIONS FOR ANNOTATORS")
    print("="*70)
    print("""
For each row, read the Query and both Candidates (A and B).

TASK: Enter 'A' or 'B' in your annotator column based on:
  "Which candidate shares the same underlying RELATIONAL STRUCTURE as the Query?"

Think about:
- Roles (e.g., deceiver/deceived, helper/helped, betrayer/betrayed)
- Intentions (e.g., manipulative vs genuine, strategic vs sincere)
- Causal patterns (e.g., deception leads to harm, sacrifice goes unrecognized)
- Outcomes (e.g., trust violated, hidden effort revealed)

DO NOT base your answer on:
- Surface similarity (same words, same domain, same setting)
- One candidate may use similar vocabulary but have opposite structure

Example:
  Query: "My boss invents fake emergencies to motivate us."
  Candidate A: "My dad lied about the time to make me rush."
  Candidate B: "My boss warned about a real client complaint."

  Answer: A (both involve authority figure fabricating urgency through deception)
  Even though B shares more words with the Query (boss, client), A shares the structure.
""")

if __name__ == "__main__":
    main()
