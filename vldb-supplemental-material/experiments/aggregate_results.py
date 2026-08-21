#!/usr/bin/env python3
"""
Aggregate all baseline results into a summary.
"""

import json
from datetime import datetime
from pathlib import Path


def load_results(results_dir):
    """Load all result files."""
    results = {}

    # TF-IDF
    tfidf_path = results_dir / "tfidf_results.json"
    if tfidf_path.exists():
        with open(tfidf_path) as f:
            results["tfidf"] = json.load(f)

    # BM25
    bm25_path = results_dir / "bm25_results.json"
    if bm25_path.exists():
        with open(bm25_path) as f:
            results["bm25"] = json.load(f)

    # Dense
    dense_path = results_dir / "dense_results.json"
    if dense_path.exists():
        with open(dense_path) as f:
            results["dense"] = json.load(f)

    return results


def create_summary_table(results):
    """Create summary table for paper."""
    rows = []

    # TF-IDF results
    if "tfidf" in results:
        for config_name, config_data in results["tfidf"]["by_config"].items():
            overall = config_data["overall"]
            test = config_data["test"]
            rows.append({
                "model": f"TF-IDF ({config_name.replace('tfidf_', '')})",
                "method_type": "sparse",
                "overall_n": overall["n"],
                "overall_q2_wins": overall["q2_wins"],
                "overall_pct": overall["q2_wins_pct"],
                "overall_ci_low": overall["ci_95_low"],
                "overall_ci_high": overall["ci_95_high"],
                "test_n": test["n"],
                "test_q2_wins": test["q2_wins"],
                "test_pct": test["q2_wins_pct"]
            })

    # BM25 results
    if "bm25" in results:
        for config_name, config_data in results["bm25"]["by_config"].items():
            if config_name == "bm25_standard":
                overall = config_data["overall"]
                test = config_data["test"]
                rows.append({
                    "model": "BM25 (k1=1.5, b=0.75)",
                    "method_type": "sparse",
                    "overall_n": overall["n"],
                    "overall_q2_wins": overall["q2_wins"],
                    "overall_pct": overall["q2_wins_pct"],
                    "overall_ci_low": overall["ci_95_low"],
                    "overall_ci_high": overall["ci_95_high"],
                    "test_n": test["n"],
                    "test_q2_wins": test["q2_wins"],
                    "test_pct": test["q2_wins_pct"]
                })

    # Dense results
    if "dense" in results:
        for model_name, model_data in results["dense"]["by_model"].items():
            if model_data.get("status") == "completed":
                overall = model_data["overall"]
                test = model_data["test"]
                rows.append({
                    "model": model_name,
                    "method_type": "dense",
                    "overall_n": overall["n"],
                    "overall_q2_wins": overall["q2_wins"],
                    "overall_pct": overall["q2_wins_pct"],
                    "overall_ci_low": overall["ci_95_low"],
                    "overall_ci_high": overall["ci_95_high"],
                    "test_n": test["n"],
                    "test_q2_wins": test["q2_wins"],
                    "test_pct": test["q2_wins_pct"]
                })

    return rows


def generate_latex_table(rows):
    """Generate LaTeX table for paper."""
    latex = r"""
\begin{table}[t]
\centering
\caption{Baseline Q2 vs.\ Q3 evaluation on 60 triplets (20 development + 40 test)}
\label{tab:baseline-results}
\small
\begin{tabular}{lcccc}
\toprule
\textbf{Model} & \textbf{Q2 $>$ Q3 (All)} & \textbf{95\% CI} & \textbf{Q2 $>$ Q3 (Test)} \\
\midrule
"""
    for row in rows:
        model = row["model"].replace("_", r"\_")
        overall = f"{row['overall_q2_wins']}/{row['overall_n']} ({row['overall_pct']:.0%})"
        ci = f"[{row['overall_ci_low']:.0%}, {row['overall_ci_high']:.0%}]"
        test = f"{row['test_q2_wins']}/{row['test_n']} ({row['test_pct']:.0%})"
        latex += f"{model} & {overall} & {ci} & {test} \\\\\n"

    latex += r"""\bottomrule
\end{tabular}
\vspace{0.5em}

\small
\emph{Q2 $>$ Q3}: count and percentage where far analogy ranks above near disanalogy.\\
\emph{95\% CI}: Wilson score interval. \emph{Test}: held-out blocks B and C.
\end{table}
"""
    return latex


def main():
    script_dir = Path(__file__).parent.parent
    results_dir = script_dir / "results" / "per_item"
    output_dir = script_dir / "results" / "aggregate"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load all results
    results = load_results(results_dir)
    print(f"Loaded results from: {list(results.keys())}")

    # Create summary
    rows = create_summary_table(results)

    # Print summary
    print("\n" + "="*80)
    print("AGGREGATE RESULTS SUMMARY")
    print("="*80)
    print(f"\n{'Model':<30} {'Q2>Q3 (All)':<15} {'95% CI':<20} {'Q2>Q3 (Test)':<15}")
    print("-"*80)
    for row in rows:
        overall = f"{row['overall_q2_wins']}/{row['overall_n']} ({row['overall_pct']:.0%})"
        ci = f"[{row['overall_ci_low']:.0%}, {row['overall_ci_high']:.0%}]"
        test = f"{row['test_q2_wins']}/{row['test_n']} ({row['test_pct']:.0%})"
        print(f"{row['model']:<30} {overall:<15} {ci:<20} {test:<15}")

    # Save summary JSON
    summary = {
        "generated": datetime.now().isoformat(),
        "dataset": {
            "total_triplets": 60,
            "development": 20,
            "test": 40,
            "schemas": 20
        },
        "results": rows
    }

    with open(output_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Generate LaTeX
    latex = generate_latex_table(rows)
    with open(output_dir / "results_table.tex", "w") as f:
        f.write(latex)

    print(f"\nSaved summary to {output_dir / 'summary.json'}")
    print(f"Saved LaTeX table to {output_dir / 'results_table.tex'}")

    # Print LaTeX table
    print("\n" + "="*80)
    print("LATEX TABLE")
    print("="*80)
    print(latex)


if __name__ == "__main__":
    main()
