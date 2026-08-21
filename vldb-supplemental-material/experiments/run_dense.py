#!/usr/bin/env python3
"""
Dense embedding baseline evaluation for Q2 vs Q3 diagnostic.
"""

import json
import hashlib
import math
from datetime import datetime
from pathlib import Path
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    HAS_SBERT = True
except ImportError:
    HAS_SBERT = False
    print("WARNING: sentence-transformers not available. Install with: pip install sentence-transformers")


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)


def evaluate_triplet(query_emb, q2_emb, q3_emb, epsilon=1e-12):
    """Evaluate a single triplet with proper tie handling."""
    q2_sim = cosine_similarity(query_emb, q2_emb)
    q3_sim = cosine_similarity(query_emb, q3_emb)

    # Proper outcome determination with epsilon tolerance
    margin = float(q2_sim - q3_sim)
    if margin > epsilon:
        outcome = "Q2_WIN"
    elif margin < -epsilon:
        outcome = "Q3_WIN"
    else:
        outcome = "TIE"

    return {
        "q2_similarity": float(q2_sim),
        "q3_similarity": float(q3_sim),
        "q2_rank": 0 if q2_sim > q3_sim else 1,
        "q3_rank": 1 if q2_sim > q3_sim else 0,
        "q2_beats_q3": outcome == "Q2_WIN",
        "outcome": outcome,
        "similarity_margin": margin
    }


def run_dense_evaluation(triplets, model_name, model):
    """Run dense embedding evaluation."""
    # Collect all texts
    queries = [t["query"] for t in triplets]
    q2s = [t["q2_far_analogy"] for t in triplets]
    q3s = [t["q3_near_disanalogy"] for t in triplets]

    # Encode all at once for efficiency
    print(f"  Encoding {len(triplets)} queries...")
    query_embs = model.encode(queries, show_progress_bar=True)
    print(f"  Encoding {len(triplets)} Q2 passages...")
    q2_embs = model.encode(q2s, show_progress_bar=True)
    print(f"  Encoding {len(triplets)} Q3 passages...")
    q3_embs = model.encode(q3s, show_progress_bar=True)

    results = []
    for i, t in enumerate(triplets):
        result = evaluate_triplet(query_embs[i], q2_embs[i], q3_embs[i])
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

    # Count outcomes properly
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
        "std_margin": math.sqrt(sum((m - sum(margins)/len(margins))**2 for m in margins) / len(margins)) if len(margins) > 1 else 0
    }


def main():
    if not HAS_SBERT:
        print("ERROR: sentence-transformers required")
        return

    script_dir = Path(__file__).parent.parent
    data_path = script_dir / "data" / "triplets_60.json"

    with open(data_path) as f:
        data = json.load(f)

    triplets = data["triplets"]
    print(f"Loaded {len(triplets)} triplets")

    # Models to evaluate (Tier 1 required + Tier 2 recommended)
    models_to_test = [
        # Tier 1: Required reproducibility baselines
        ("all-MiniLM-L6-v2", "sentence-transformers/all-MiniLM-L6-v2"),
        ("all-mpnet-base-v2", "sentence-transformers/all-mpnet-base-v2"),
        # Tier 2: Strongly recommended contemporary baselines
        ("e5-large-v2", "intfloat/e5-large-v2"),
        ("bge-large-en-v1.5", "BAAI/bge-large-en-v1.5"),
    ]

    all_results = {
        "metadata": {
            "evaluation_date": datetime.now().isoformat(),
            "dataset_version": data["metadata"]["version"],
            "dataset_checksum": hashlib.sha256(json.dumps(data).encode()).hexdigest()[:16],
            "method": "Dense sentence embeddings with cosine similarity"
        },
        "by_model": {}
    }

    for short_name, full_name in models_to_test:
        print(f"\n{'='*60}")
        print(f"Loading {short_name}...")
        try:
            model = SentenceTransformer(full_name)
        except Exception as e:
            print(f"  ERROR loading model: {e}")
            all_results["by_model"][short_name] = {"status": "blocked", "error": str(e)}
            continue

        print(f"Running evaluation...")
        results = run_dense_evaluation(triplets, short_name, model)

        overall = compute_statistics(results)
        dev_stats = compute_statistics(results, "development")
        test_stats = compute_statistics(results, "test")

        all_results["by_model"][short_name] = {
            "model_name": full_name,
            "status": "completed",
            "overall": overall,
            "development": dev_stats,
            "test": test_stats,
            "per_triplet": results
        }

        print(f"\n  Results for {short_name}:")
        print(f"  Overall: Q2 wins {overall['q2_wins']}/{overall['n']} ({overall['q2_wins_pct']:.1%})")
        print(f"    95% CI: [{overall['ci_95_low']:.1%}, {overall['ci_95_high']:.1%}]")
        print(f"  Development: Q2 wins {dev_stats['q2_wins']}/{dev_stats['n']}")
        print(f"  Test: Q2 wins {test_stats['q2_wins']}/{test_stats['n']}")

    # Save results
    output_dir = script_dir / "results" / "per_item"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "dense_results.json"
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
