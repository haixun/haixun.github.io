#!/usr/bin/env python3
"""
Compute schema-clustered bootstrap confidence intervals for baseline results.

The 60 triplets derive from 20 schemas (3 realizations each). Item-level
Wilson intervals treat observations as independent, which understates
uncertainty. This script uses cluster bootstrap resampling.
"""

import json
import numpy as np
from pathlib import Path
from collections import defaultdict

RESULTS_DIR = Path(__file__).parent.parent / "results" / "per_item"
DATA_PATH = Path(__file__).parent.parent / "data" / "triplets_60.json"
OUTPUT_PATH = Path(__file__).parent.parent / "results" / "aggregate" / "schema_clustered_results.json"

N_BOOTSTRAP = 10000
RANDOM_SEED = 42


def load_results():
    """Load per-item results from all baselines."""
    results = {}

    for result_file in RESULTS_DIR.glob("*_results.json"):
        model_name = result_file.stem.replace("_results", "")
        with open(result_file) as f:
            results[model_name] = json.load(f)

    return results


def load_schema_mapping():
    """Load mapping from triplet ID to schema ID."""
    with open(DATA_PATH) as f:
        data = json.load(f)

    # Schema ID is (triplet_id - 1) % 20 + 1 for the current structure
    # Or we can infer from the schema_id field if present
    mapping = {}
    for t in data["triplets"]:
        tid = t["id"]
        # Schema ID: items 1,21,41 share schema 1; items 2,22,42 share schema 2; etc.
        schema_id = ((tid - 1) % 20) + 1
        mapping[tid] = schema_id

    return mapping


def cluster_bootstrap_ci(outcomes_by_schema, n_bootstrap=N_BOOTSTRAP, alpha=0.05):
    """
    Compute cluster bootstrap confidence interval.

    Args:
        outcomes_by_schema: dict mapping schema_id -> list of 0/1 outcomes
        n_bootstrap: number of bootstrap samples
        alpha: significance level (default 0.05 for 95% CI)

    Returns:
        (mean, ci_lower, ci_upper)
    """
    np.random.seed(RANDOM_SEED)

    schema_ids = list(outcomes_by_schema.keys())
    n_schemas = len(schema_ids)

    # Compute observed mean
    all_outcomes = []
    for sid in schema_ids:
        all_outcomes.extend(outcomes_by_schema[sid])
    observed_mean = np.mean(all_outcomes)

    # Bootstrap: resample schemas with replacement
    bootstrap_means = []
    for _ in range(n_bootstrap):
        # Sample schemas with replacement
        sampled_schemas = np.random.choice(schema_ids, size=n_schemas, replace=True)

        # Collect all outcomes from sampled schemas
        bootstrap_outcomes = []
        for sid in sampled_schemas:
            bootstrap_outcomes.extend(outcomes_by_schema[sid])

        bootstrap_means.append(np.mean(bootstrap_outcomes))

    # Compute percentile CI
    ci_lower = np.percentile(bootstrap_means, 100 * alpha / 2)
    ci_upper = np.percentile(bootstrap_means, 100 * (1 - alpha / 2))

    return observed_mean, ci_lower, ci_upper


def extract_per_item_outcomes(model_results):
    """Extract per-item Q2 win/loss from various result formats."""
    outcomes = {}  # triplet_id -> q2_wins (bool)

    # Try different formats
    config_container = None
    for container_key in ["by_config", "by_model"]:
        if container_key in model_results:
            config_container = model_results[container_key]
            break

    if config_container:
        # Use first config/model
        for config_name, config_data in config_container.items():
            # Try per_triplet first, then per_item
            per_item_key = None
            for key in ["per_triplet", "per_item", "items"]:
                if key in config_data:
                    per_item_key = key
                    break

            if per_item_key:
                for item in config_data[per_item_key]:
                    tid = item.get("triplet_id", item.get("id"))
                    # Try various field names for q2 wins
                    q2_wins = item.get("q2_wins") or item.get("q2_beats_q3") or item.get("q2_higher") or item.get("correct")
                    outcomes[tid] = bool(q2_wins)
                break
    elif "per_triplet" in model_results:
        for item in model_results["per_triplet"]:
            tid = item.get("triplet_id", item.get("id"))
            q2_wins = item.get("q2_wins") or item.get("q2_beats_q3") or item.get("q2_higher") or item.get("correct")
            outcomes[tid] = bool(q2_wins)
    elif "per_item" in model_results:
        for item in model_results["per_item"]:
            tid = item.get("triplet_id", item.get("id"))
            q2_wins = item.get("q2_wins") or item.get("q2_beats_q3") or item.get("q2_higher") or item.get("correct")
            outcomes[tid] = bool(q2_wins)
    elif "items" in model_results:
        for item in model_results["items"]:
            tid = item.get("triplet_id", item.get("id"))
            q2_wins = item.get("q2_wins") or item.get("q2_beats_q3") or item.get("q2_higher") or item.get("correct")
            outcomes[tid] = bool(q2_wins)

    return outcomes


def analyze_model(model_results, schema_mapping):
    """Analyze a single model's results with schema clustering."""

    # Extract per-item outcomes
    outcomes = extract_per_item_outcomes(model_results)

    if not outcomes:
        return None

    # Group outcomes by schema
    outcomes_by_schema = defaultdict(list)
    for tid, q2_wins in outcomes.items():
        schema_id = schema_mapping[tid]
        outcomes_by_schema[schema_id].append(1 if q2_wins else 0)

    # Compute clustered CI
    mean, ci_lower, ci_upper = cluster_bootstrap_ci(outcomes_by_schema)

    # Also compute per-schema consistency
    schema_consistency = {}
    for sid, schema_outcomes in outcomes_by_schema.items():
        if len(schema_outcomes) == 3:
            # All same = consistent
            if len(set(schema_outcomes)) == 1:
                schema_consistency[sid] = "consistent"
            else:
                schema_consistency[sid] = "mixed"

    consistent_count = sum(1 for v in schema_consistency.values() if v == "consistent")

    return {
        "mean": mean,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "n_items": sum(len(v) for v in outcomes_by_schema.values()),
        "n_schemas": len(outcomes_by_schema),
        "consistent_schemas": consistent_count,
        "total_schemas": len(schema_consistency)
    }


def main():
    print("=" * 70)
    print("Schema-Clustered Bootstrap Analysis")
    print("=" * 70)

    results = load_results()
    schema_mapping = load_schema_mapping()

    output = {
        "method": "cluster_bootstrap",
        "n_bootstrap": N_BOOTSTRAP,
        "random_seed": RANDOM_SEED,
        "n_schemas": 20,
        "realizations_per_schema": 3,
        "models": {}
    }

    print(f"\n{'Model':<25} {'Q2>Q3':<12} {'95% CI (clustered)':<25} {'Consistent schemas'}")
    print("-" * 80)

    for model_name, model_results in sorted(results.items()):
        if model_name == "oracle":
            # Oracle is 100% by construction
            analysis = {
                "mean": 1.0,
                "ci_lower": 1.0,
                "ci_upper": 1.0,
                "n_items": 60,
                "n_schemas": 20,
                "consistent_schemas": 20,
                "total_schemas": 20,
                "note": "100% by construction (reads answer key)"
            }
        else:
            analysis = analyze_model(model_results, schema_mapping)

        if analysis is None:
            print(f"{model_name:<25} [Could not parse results]")
            continue

        output["models"][model_name] = analysis

        mean_pct = analysis["mean"] * 100
        ci_str = f"[{analysis['ci_lower']*100:.1f}%, {analysis['ci_upper']*100:.1f}%]"
        consist_str = f"{analysis['consistent_schemas']}/{analysis['total_schemas']}"

        print(f"{model_name:<25} {mean_pct:>5.1f}%       {ci_str:<25} {consist_str}")

    # Save results
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n✓ Results saved to {OUTPUT_PATH}")

    # Print comparison with item-level intervals
    print("\n" + "=" * 70)
    print("Comparison: Item-level vs Schema-clustered 95% CIs")
    print("=" * 70)
    print("\nNote: Clustered intervals are wider because they account for")
    print("within-schema correlation (items from same schema are not independent).")


if __name__ == "__main__":
    main()
