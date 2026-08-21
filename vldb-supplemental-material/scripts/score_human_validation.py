#!/usr/bin/env python3
"""
Score the 3-rater human-validation study for the 60-item structural battery.

Each rater assigns Surface / Structure / Confidence scores (1-5) to two
candidates (A, B) per item. The rater's implied choice is the candidate with
the HIGHER Structure score. A choice is correct when it matches the answer
key's q2_position (the far analogy). Ties (equal Structure) count as non-wins.

Metrics:
  * per-rater accuracy
  * majority-vote accuracy (2/3 raters)
  * pairwise agreement on the choice
  * Gwet's AC1 (imbalance-robust chance-corrected agreement; pre-specified)
  * schema-clustered bootstrap 95% CIs (20 schemas x 3 realizations)

Outputs a \\Res... macro block for result_macros.tex.
"""

import csv
import json
import numpy as np
from pathlib import Path

ROOT = Path(__file__).parent.parent
CSV_PATHS = [ROOT / f"human-annotation-{i}.csv" for i in (1, 2, 3)]
ANSWER_KEY = ROOT / "data" / "battery_answer_key.json"

N_BOOTSTRAP = 10000
RANDOM_SEED = 42

# Column positions (identical across all three files):
COL_ITEM = 0
COL_A_STRUCT = 5
COL_B_STRUCT = 9


def load_answer_key():
    with open(ANSWER_KEY) as f:
        data = json.load(f)
    key = {}
    for it in data["items"]:
        key[int(it["item_id"])] = it["q2_position"].strip().upper()
    return key


def find_header_row(rows):
    """Return index of the row whose first cell is 'item_id'."""
    for i, r in enumerate(rows):
        if r and r[0].strip() == "item_id":
            return i
    raise ValueError("No item_id header row found")


def load_rater(path):
    """Return dict item_id -> choice ('A'/'B'/'TIE') from one rater's CSV."""
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    hdr = find_header_row(rows)
    choices = {}
    for r in rows[hdr + 1:]:
        if not r or not r[COL_ITEM].strip().isdigit():
            continue
        tid = int(r[COL_ITEM])
        a = float(r[COL_A_STRUCT])
        b = float(r[COL_B_STRUCT])
        if a > b:
            choices[tid] = "A"
        elif b > a:
            choices[tid] = "B"
        else:
            choices[tid] = "TIE"
    return choices


def gwet_ac1(rater_choices, item_ids, categories=("A", "B"), drop_missing=True):
    """
    Gwet's AC1 for r raters over the given categories.

    drop_missing=True: a choice not in `categories` (e.g. a TIE when only
    A/B are scored) is dropped for that rater, allowing a variable number of
    raters r_i per item. drop_missing=False requires every choice to be a
    listed category.
    """
    categories = list(categories)
    q = len(categories)
    pa_terms = []
    pi_num = {c: 0.0 for c in categories}
    pi_den = 0.0
    for tid in item_ids:
        counts = {c: 0 for c in categories}
        r_i = 0
        for rc in rater_choices:
            ch = rc[tid]
            if ch in counts:
                counts[ch] += 1
                r_i += 1
        if r_i < 2:
            continue
        pa_i = sum(counts[c] * (counts[c] - 1) for c in categories) / (r_i * (r_i - 1))
        pa_terms.append(pa_i)
        for c in categories:
            pi_num[c] += counts[c] / r_i
        pi_den += 1
    pa = float(np.mean(pa_terms))
    pi = {c: pi_num[c] / pi_den for c in categories}
    pe = (1.0 / (q - 1)) * sum(pi[c] * (1 - pi[c]) for c in categories)
    ac1 = (pa - pe) / (1 - pe)
    return ac1, pa, pe


def schema_id(tid):
    return ((tid - 1) % 20) + 1


def cluster_bootstrap_ci(correct_by_item, item_ids, n_boot=N_BOOTSTRAP, alpha=0.05):
    """Resample the 20 schemas with replacement; percentile CI on the mean."""
    rng = np.random.default_rng(RANDOM_SEED)
    by_schema = {}
    for tid in item_ids:
        by_schema.setdefault(schema_id(tid), []).append(correct_by_item[tid])
    schemas = list(by_schema.keys())
    n = len(schemas)
    obs = np.mean([correct_by_item[t] for t in item_ids])
    means = []
    for _ in range(n_boot):
        samp = rng.choice(schemas, size=n, replace=True)
        vals = []
        for s in samp:
            vals.extend(by_schema[s])
        means.append(np.mean(vals))
    lo = np.percentile(means, 100 * alpha / 2)
    hi = np.percentile(means, 100 * (1 - alpha / 2))
    return obs, lo, hi


def main():
    key = load_answer_key()
    item_ids = sorted(key.keys())
    raters = [load_rater(p) for p in CSV_PATHS]

    print("=" * 72)
    print("3-RATER HUMAN VALIDATION — structural battery (60 items)")
    print("=" * 72)

    # Per-rater accuracy (ties = non-win)
    per_rater_acc = []
    per_rater_ties = []
    for i, rc in enumerate(raters, 1):
        correct = sum(1 for t in item_ids if rc[t] == key[t])
        ties = sum(1 for t in item_ids if rc[t] == "TIE")
        acc = correct / len(item_ids)
        per_rater_acc.append(acc)
        per_rater_ties.append(ties)
        print(f"Rater {i}: {correct}/{len(item_ids)} = {100*acc:.1f}%  (ties={ties})")

    mean_acc = float(np.mean(per_rater_acc))
    print(f"\nMean per-rater accuracy: {100*mean_acc:.1f}%")

    # Majority vote (over non-tie choices; tie in the vote = non-win)
    maj_correct_by_item = {}
    maj_correct = 0
    for t in item_ids:
        votes = [rc[t] for rc in raters if rc[t] in ("A", "B")]
        if not votes:
            maj_correct_by_item[t] = 0
            continue
        a = votes.count("A")
        b = votes.count("B")
        if a > b:
            choice = "A"
        elif b > a:
            choice = "B"
        else:
            choice = "TIE"
        win = 1 if choice == key[t] else 0
        maj_correct_by_item[t] = win
        maj_correct += win
    maj_acc = maj_correct / len(item_ids)
    print(f"Majority-vote accuracy: {maj_correct}/{len(item_ids)} = {100*maj_acc:.1f}%")

    # Unanimity
    unanimous = sum(
        1 for t in item_ids
        if len({rc[t] for rc in raters}) == 1 and raters[0][t] in ("A", "B")
    )
    unanimous_correct = sum(
        1 for t in item_ids
        if len({rc[t] for rc in raters}) == 1
        and raters[0][t] in ("A", "B")
        and raters[0][t] == key[t]
    )
    print(f"Unanimous items: {unanimous}/{len(item_ids)}  "
          f"(of which correct: {unanimous_correct})")

    # Pairwise agreement on the choice
    print("\nPairwise agreement (on candidate choice):")
    pair_agrees = []
    for (i, j) in [(0, 1), (0, 2), (1, 2)]:
        agree = sum(1 for t in item_ids if raters[i][t] == raters[j][t])
        frac = agree / len(item_ids)
        pair_agrees.append(frac)
        print(f"  R{i+1} vs R{j+1}: {agree}/{len(item_ids)} = {100*frac:.1f}%")
    mean_pair = float(np.mean(pair_agrees))
    print(f"  mean pairwise: {100*mean_pair:.1f}%")

    # Gwet's AC1 (two ways of handling the tie)
    ac1_drop, pa_d, pe_d = gwet_ac1(raters, item_ids, categories=("A", "B"))
    ac1_tie, pa_t, pe_t = gwet_ac1(
        raters, item_ids, categories=("A", "B", "TIE"), drop_missing=False
    )
    print(f"\nGwet's AC1 (ties dropped):        {ac1_drop:.3f}  "
          f"(p_a={pa_d:.3f}, p_e={pe_d:.3f})")
    print(f"Gwet's AC1 (tie as 3rd category): {ac1_tie:.3f}  "
          f"(p_a={pa_t:.3f}, p_e={pe_t:.3f})")

    # Schema-clustered bootstrap CIs
    print("\nSchema-clustered bootstrap 95% CIs (20 schemas):")
    obs_maj, lo_maj, hi_maj = cluster_bootstrap_ci(maj_correct_by_item, item_ids)
    print(f"  Majority-vote accuracy: {100*obs_maj:.1f}% "
          f"[{100*lo_maj:.1f}%, {100*hi_maj:.1f}%]")

    # Per-rater pooled correctness CI (average rater)
    pooled = {}
    for t in item_ids:
        pooled[t] = np.mean([1 if rc[t] == key[t] else 0 for rc in raters])
    obs_pool, lo_pool, hi_pool = cluster_bootstrap_ci(pooled, item_ids)
    print(f"  Mean per-rater accuracy: {100*obs_pool:.1f}% "
          f"[{100*lo_pool:.1f}%, {100*hi_pool:.1f}%]")

    # Macro block
    print("\n" + "=" * 72)
    print("MACRO BLOCK for result_macros.tex")
    print("=" * 72)
    macros = [
        ("ResHumanNRaters", "3"),
        ("ResHumanNItems", str(len(item_ids))),
        ("ResHumanMeanAcc", f"{100*mean_acc:.1f}"),
        ("ResHumanMeanAccLo", f"{100*lo_pool:.1f}"),
        ("ResHumanMeanAccHi", f"{100*hi_pool:.1f}"),
        ("ResHumanMajAcc", f"{100*maj_acc:.1f}"),
        ("ResHumanMajCorrect", str(maj_correct)),
        ("ResHumanMajLo", f"{100*lo_maj:.1f}"),
        ("ResHumanMajHi", f"{100*hi_maj:.1f}"),
        ("ResHumanUnanimous", str(unanimous)),
        ("ResHumanMeanPairAgree", f"{100*mean_pair:.1f}"),
        ("ResHumanACOne", f"{ac1_tie:.2f}"),
    ]
    for name, val in macros:
        print(f"\\newcommand{{\\{name}}}{{{val}}}")


if __name__ == "__main__":
    main()
