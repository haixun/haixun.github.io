#!/usr/bin/env python3
"""
BM25 baseline evaluation for Q2 vs Q3 diagnostic.

Uses the actual BM25 algorithm (Okapi BM25), not TF-IDF.
BM25 parameters: k1 (term frequency saturation), b (length normalization)
"""

import json
import hashlib
import math
from datetime import datetime
from pathlib import Path
from collections import Counter
import re


class BM25:
    """
    Okapi BM25 implementation.

    BM25 formula:
    score(D, Q) = sum over q in Q of:
        IDF(q) * (f(q,D) * (k1 + 1)) / (f(q,D) + k1 * (1 - b + b * |D|/avgdl))

    where:
        f(q,D) = term frequency of q in D
        |D| = document length
        avgdl = average document length
        IDF(q) = log((N - n(q) + 0.5) / (n(q) + 0.5) + 1)
        N = total documents
        n(q) = documents containing q
    """

    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.doc_freqs = {}
        self.doc_lens = []
        self.avgdl = 0
        self.N = 0

    def tokenize(self, text):
        """Simple tokenization: lowercase, split on non-alphanumeric."""
        return re.findall(r'\b\w+\b', text.lower())

    def fit(self, corpus):
        """Fit BM25 on corpus."""
        self.corpus = [self.tokenize(doc) for doc in corpus]
        self.N = len(self.corpus)
        self.doc_lens = [len(doc) for doc in self.corpus]
        self.avgdl = sum(self.doc_lens) / self.N if self.N > 0 else 0

        # Compute document frequencies
        self.doc_freqs = {}
        for doc in self.corpus:
            for term in set(doc):
                self.doc_freqs[term] = self.doc_freqs.get(term, 0) + 1

    def idf(self, term):
        """Compute IDF for a term."""
        n = self.doc_freqs.get(term, 0)
        return math.log((self.N - n + 0.5) / (n + 0.5) + 1)

    def score(self, query_tokens, doc_idx):
        """Compute BM25 score for a document given query tokens."""
        doc = self.corpus[doc_idx]
        doc_len = self.doc_lens[doc_idx]
        term_freqs = Counter(doc)

        score = 0
        for term in query_tokens:
            if term not in term_freqs:
                continue

            tf = term_freqs[term]
            idf = self.idf(term)

            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)

            score += idf * numerator / denominator

        return score

    def rank(self, query):
        """Rank all documents for a query."""
        query_tokens = self.tokenize(query)
        scores = [self.score(query_tokens, i) for i in range(self.N)]
        rankings = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return rankings, scores


def evaluate_triplet(query, q2, q3, k1=1.5, b=0.75, epsilon=1e-12):
    """Evaluate a single triplet with BM25 and proper tie handling."""
    bm25 = BM25(k1=k1, b=b)
    bm25.fit([q2, q3])  # Corpus is [q2, q3]

    rankings, scores = bm25.rank(query)

    q2_score = scores[0]  # q2 is index 0
    q3_score = scores[1]  # q3 is index 1

    q2_rank = rankings.index(0)
    q3_rank = rankings.index(1)

    # Proper outcome determination with epsilon tolerance
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
        "q2_rank": q2_rank,
        "q3_rank": q3_rank,
        "q2_beats_q3": outcome == "Q2_WIN",
        "outcome": outcome,
        "similarity_margin": margin
    }


def run_bm25_evaluation(triplets, k1=1.5, b=0.75):
    """Run BM25 evaluation."""
    results = []
    for t in triplets:
        result = evaluate_triplet(
            t["query"],
            t["q2_far_analogy"],
            t["q3_near_disanalogy"],
            k1=k1,
            b=b
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

    # Wilson score interval
    import math
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
    script_dir = Path(__file__).parent.parent
    data_path = script_dir / "data" / "triplets_60.json"

    with open(data_path) as f:
        data = json.load(f)

    triplets = data["triplets"]
    print(f"Loaded {len(triplets)} triplets")

    # Standard BM25 parameters
    configs = [
        {"name": "bm25_standard", "k1": 1.5, "b": 0.75, "description": "Standard BM25 (k1=1.5, b=0.75)"},
        {"name": "bm25_k1_1.2", "k1": 1.2, "b": 0.75, "description": "BM25 with k1=1.2"},
    ]

    all_results = {
        "metadata": {
            "evaluation_date": datetime.now().isoformat(),
            "dataset_version": data["metadata"]["version"],
            "dataset_checksum": hashlib.sha256(json.dumps(data).encode()).hexdigest()[:16],
            "method": "Okapi BM25",
            "note": "This is actual BM25 (Okapi BM25), not TF-IDF.",
            "tokenizer": "simple whitespace + lowercase"
        },
        "by_config": {}
    }

    for config in configs:
        print(f"\nRunning {config['name']}...")
        results = run_bm25_evaluation(triplets, k1=config["k1"], b=config["b"])

        overall = compute_statistics(results)
        dev_stats = compute_statistics(results, "development")
        test_stats = compute_statistics(results, "test")

        all_results["by_config"][config["name"]] = {
            "config": {"k1": config["k1"], "b": config["b"], "description": config["description"]},
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

    output_path = output_dir / "bm25_results.json"
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
