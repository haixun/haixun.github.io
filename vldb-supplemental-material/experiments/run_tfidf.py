#!/usr/bin/env python3
"""
TF-IDF baseline evaluation for Q2 vs Q3 diagnostic.

This is TF-IDF cosine similarity, NOT BM25. They are different methods.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
import numpy as np

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("ERROR: scikit-learn required. Install with: pip install scikit-learn")


def compute_rankings(query_vec, corpus_vecs):
    """Compute rankings by cosine similarity (descending)."""
    similarities = cosine_similarity(query_vec, corpus_vecs)[0]
    rankings = np.argsort(-similarities)
    return rankings, similarities


def evaluate_triplet(query, q2, q3, vectorizer, epsilon=1e-12):
    """Evaluate a single triplet with proper tie handling."""
    # Fit on all three texts
    all_texts = [query, q2, q3]
    vecs = vectorizer.fit_transform(all_texts)

    query_vec = vecs[0:1]
    corpus_vecs = vecs[1:]  # [q2, q3]

    rankings, similarities = compute_rankings(query_vec, corpus_vecs)

    q2_sim = similarities[0]  # q2 is index 0
    q3_sim = similarities[1]  # q3 is index 1

    # Find ranks (0-indexed)
    q2_rank = int(np.where(rankings == 0)[0][0])
    q3_rank = int(np.where(rankings == 1)[0][0])

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
        "q2_rank": q2_rank,
        "q3_rank": q3_rank,
        "q2_beats_q3": outcome == "Q2_WIN",  # Strict Q2 win only
        "outcome": outcome,
        "similarity_margin": margin
    }


def run_tfidf_evaluation(triplets, config):
    """Run TF-IDF evaluation with specified configuration."""
    vectorizer = TfidfVectorizer(
        ngram_range=config["ngram_range"],
        stop_words=config.get("stop_words", "english"),
        max_features=config.get("max_features", 10000),
        lowercase=True
    )

    results = []
    for t in triplets:
        result = evaluate_triplet(
            t["query"],
            t["q2_far_analogy"],
            t["q3_near_disanalogy"],
            vectorizer
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

    # Count outcomes properly
    q2_wins = sum(1 for r in filtered if r.get("outcome") == "Q2_WIN")
    q3_wins = sum(1 for r in filtered if r.get("outcome") == "Q3_WIN")
    ties = sum(1 for r in filtered if r.get("outcome") == "TIE")

    # Wilson score interval for binomial proportion (Q2 wins only)
    from math import sqrt
    z = 1.96  # 95% CI
    p = q2_wins / n
    denominator = 1 + z**2 / n
    center = (p + z**2 / (2*n)) / denominator
    spread = z * sqrt(p*(1-p)/n + z**2/(4*n**2)) / denominator
    ci_low = max(0, center - spread)
    ci_high = min(1, center + spread)

    return {
        "n": n,
        "q2_wins": q2_wins,
        "q3_wins": q3_wins,
        "ties": ties,
        "q2_wins_pct": q2_wins / n,
        "ci_95_low": ci_low,
        "ci_95_high": ci_high,
        "ci_method": "wilson",
        "mean_margin": np.mean([r["similarity_margin"] for r in filtered]),
        "std_margin": np.std([r["similarity_margin"] for r in filtered])
    }


def main():
    if not HAS_SKLEARN:
        return

    script_dir = Path(__file__).parent.parent
    data_path = script_dir / "data" / "triplets_60.json"

    with open(data_path) as f:
        data = json.load(f)

    triplets = data["triplets"]
    print(f"Loaded {len(triplets)} triplets")

    # Configuration
    configs = [
        {
            "name": "tfidf_unigram",
            "ngram_range": (1, 1),
            "stop_words": "english",
            "description": "TF-IDF with word unigrams, English stop words removed"
        },
        {
            "name": "tfidf_bigram",
            "ngram_range": (1, 2),
            "stop_words": "english",
            "description": "TF-IDF with word 1-2 grams, English stop words removed"
        }
    ]

    all_results = {
        "metadata": {
            "evaluation_date": datetime.now().isoformat(),
            "dataset_version": data["metadata"]["version"],
            "dataset_checksum": hashlib.sha256(json.dumps(data).encode()).hexdigest()[:16],
            "method": "TF-IDF cosine similarity",
            "note": "This is TF-IDF, NOT BM25. They are different methods."
        },
        "by_config": {}
    }

    for config in configs:
        print(f"\nRunning {config['name']}...")
        results = run_tfidf_evaluation(triplets, config)

        # Overall stats
        overall = compute_statistics(results)
        dev_stats = compute_statistics(results, "development")
        test_stats = compute_statistics(results, "test")

        all_results["by_config"][config["name"]] = {
            "config": {k: v for k, v in config.items() if k != "name"},
            "overall": overall,
            "development": dev_stats,
            "test": test_stats,
            "per_triplet": results
        }

        print(f"  Overall: Q2 wins {overall['q2_wins']}/{overall['n']} ({overall['q2_wins_pct']:.1%})")
        print(f"    95% CI: [{overall['ci_95_low']:.1%}, {overall['ci_95_high']:.1%}]")
        print(f"  Development: Q2 wins {dev_stats['q2_wins']}/{dev_stats['n']}")
        print(f"  Test: Q2 wins {test_stats['q2_wins']}/{test_stats['n']}")

    # Save results
    output_dir = script_dir / "results" / "per_item"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "tfidf_results.json"
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
