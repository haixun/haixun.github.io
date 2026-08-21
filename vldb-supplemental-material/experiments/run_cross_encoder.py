#!/usr/bin/env python3
"""
Cross-encoder reranker baseline evaluation for Q2 vs Q3 diagnostic.

Cross-encoders jointly encode query-candidate pairs and output a relevance score.
"""

import json
import hashlib
import math
from datetime import datetime
from pathlib import Path

try:
    from sentence_transformers import CrossEncoder
    HAS_CROSS_ENCODER = True
except ImportError:
    HAS_CROSS_ENCODER = False
    print("WARNING: sentence-transformers not available. Install with: pip install sentence-transformers")


def evaluate_triplet(query, q2, q3, model, epsilon=1e-12):
    """Evaluate a single triplet with cross-encoder."""
    # Cross-encoder scores pairs directly
    q2_score = model.predict([(query, q2)])[0]
    q3_score = model.predict([(query, q3)])[0]

    margin = float(q2_score - q3_score)
    if margin > epsilon:
        outcome = "Q2_WIN"
    elif margin < -epsilon:
        outcome = "Q3_WIN"
    else:
        outcome = "TIE"

    return {
        "q2_similarity": float(q2_score),
        "q3_similarity": float(q3_score),
        "q2_rank": 0 if q2_score > q3_score else 1,
        "q3_rank": 1 if q2_score > q3_score else 0,
        "q2_beats_q3": outcome == "Q2_WIN",
        "outcome": outcome,
        "similarity_margin": margin
    }


def run_cross_encoder_evaluation(triplets, model_name, model):
    """Run cross-encoder evaluation."""
    results = []
    for i, t in enumerate(triplets):
        if (i + 1) % 10 == 0:
            print(f"  Processing triplet {i+1}/{len(triplets)}...")
        result = evaluate_triplet(
            t["query"],
            t["q2_far_analogy"],
            t["q3_near_disanalogy"],
            model
        )
        result["triplet_id"] = t["id"]
        result["schema_id"] = t["schema_id"]
        result["block"] = t["block"]
        result["split"] = t["split"]
        results.append(result)
    return results


def compute_statistics(results, split_filter=None):
    """Compute aggregate statistics with proper tie handling."""
    if split_filter:
        filtered = [r for r in results if r["split"] == split_filter]
    else:
        filtered = results

    n = len(filtered)
    if n == 0:
        return {"error": "No results"}

    q2_wins = sum(1 for r in filtered if r.get("outcome") == "Q2_WIN")
    q3_wins = sum(1 for r in filtered if r.get("outcome") == "Q3_WIN")
    ties = sum(1 for r in filtered if r.get("outcome") == "TIE")

    # Wilson score interval
    z = 1.96
    p = q2_wins / n
    denominator = 1 + z**2 / n
    center = (p + z**2 / (2*n)) / denominator
    spread = z * math.sqrt(p*(1-p)/n + z**2/(4*n**2)) / denominator
    ci_low = max(0, center - spread)
    ci_high = min(1, center + spread)

    margins = [r["similarity_margin"] for r in filtered]

    return {
        "n": n,
        "q2_wins": q2_wins,
        "q3_wins": q3_wins,
        "ties": ties,
        "q2_wins_pct": q2_wins / n,
        "ci_95_low": ci_low,
        "ci_95_high": ci_high,
        "ci_method": "wilson",
        "mean_margin": sum(margins) / len(margins),
        "std_margin": math.sqrt(sum((m - sum(margins)/len(margins))**2 for m in margins) / len(margins))
    }


def main():
    if not HAS_CROSS_ENCODER:
        print("ERROR: sentence-transformers required for cross-encoder evaluation")
        return

    script_dir = Path(__file__).parent.parent
    data_path = script_dir / "data" / "triplets_60.json"

    with open(data_path) as f:
        data = json.load(f)

    triplets = data["triplets"]
    print(f"Loaded {len(triplets)} triplets")

    # Cross-encoder models to evaluate
    models = [
        {
            "name": "ms-marco-MiniLM-L-6-v2",
            "model_id": "cross-encoder/ms-marco-MiniLM-L-6-v2",
            "description": "MS MARCO trained MiniLM cross-encoder"
        },
    ]

    all_results = {
        "metadata": {
            "evaluation_date": datetime.now().isoformat(),
            "dataset_version": data["metadata"]["version"],
            "dataset_checksum": hashlib.sha256(json.dumps(data).encode()).hexdigest()[:16],
            "method": "Cross-encoder pairwise scoring",
            "note": "Cross-encoders jointly encode query-candidate pairs"
        },
        "by_model": {}
    }

    for model_info in models:
        print(f"\n{'='*60}")
        print(f"Loading {model_info['name']}...")
        try:
            model = CrossEncoder(model_info["model_id"])
        except Exception as e:
            print(f"  ERROR loading model: {e}")
            all_results["by_model"][model_info["name"]] = {"error": str(e)}
            continue

        print("Running evaluation...")
        results = run_cross_encoder_evaluation(triplets, model_info["name"], model)

        overall = compute_statistics(results)
        dev_stats = compute_statistics(results, "development")
        test_stats = compute_statistics(results, "test")

        all_results["by_model"][model_info["name"]] = {
            "model_id": model_info["model_id"],
            "description": model_info["description"],
            "overall": overall,
            "development": dev_stats,
            "test": test_stats,
            "per_triplet": results
        }

        print(f"\n  Results for {model_info['name']}:")
        print(f"  Overall: Q2 wins {overall['q2_wins']}/{overall['n']} ({overall['q2_wins_pct']:.1%}), ties: {overall['ties']}")
        print(f"    95% CI: [{overall['ci_95_low']:.1%}, {overall['ci_95_high']:.1%}]")
        print(f"  Development: Q2 wins {dev_stats['q2_wins']}/{dev_stats['n']}")
        print(f"  Test: Q2 wins {test_stats['q2_wins']}/{test_stats['n']}")

    # Save results
    output_dir = script_dir / "results" / "per_item"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "cross_encoder_results.json"
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
