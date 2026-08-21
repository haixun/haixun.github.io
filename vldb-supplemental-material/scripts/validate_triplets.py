#!/usr/bin/env python3
"""
Validate the triplets_60.json dataset for structural and content integrity.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
import hashlib

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


def validate_json_schema(triplets):
    """Validate required fields exist and are non-empty."""
    errors = []
    required_fields = ["id", "schema_id", "schema", "split", "block",
                       "query", "q2_far_analogy", "q3_near_disanalogy",
                       "structural_difference"]

    for t in triplets:
        tid = t.get("id", "UNKNOWN")
        for field in required_fields:
            if field not in t:
                errors.append(f"Triplet {tid}: Missing field '{field}'")
            elif isinstance(t[field], str) and not t[field].strip():
                errors.append(f"Triplet {tid}: Empty field '{field}'")

    return errors


def validate_ids(triplets):
    """Validate unique IDs from 1-60."""
    errors = []
    ids = [t["id"] for t in triplets]

    if len(ids) != 60:
        errors.append(f"Expected 60 triplets, found {len(ids)}")

    if len(ids) != len(set(ids)):
        duplicates = [i for i in ids if ids.count(i) > 1]
        errors.append(f"Duplicate IDs: {set(duplicates)}")

    expected = set(range(1, 61))
    actual = set(ids)
    missing = expected - actual
    extra = actual - expected

    if missing:
        errors.append(f"Missing IDs: {sorted(missing)}")
    if extra:
        errors.append(f"Unexpected IDs: {sorted(extra)}")

    return errors


def validate_schema_distribution(triplets):
    """Validate 20 schemas with 3 realizations each."""
    errors = []
    schema_counts = defaultdict(list)

    for t in triplets:
        schema_counts[t["schema_id"]].append(t["id"])

    if len(schema_counts) != 20:
        errors.append(f"Expected 20 schemas, found {len(schema_counts)}")

    for sid, tids in sorted(schema_counts.items()):
        if len(tids) != 3:
            errors.append(f"Schema {sid} has {len(tids)} triplets (expected 3): {tids}")

    return errors


def validate_splits(triplets):
    """Validate development/test split assignments."""
    errors = []

    for t in triplets:
        tid = t["id"]
        split = t.get("split")
        block = t.get("block")

        if tid <= 20:
            if split != "development":
                errors.append(f"Triplet {tid}: Should be development split, is '{split}'")
            if block != "A":
                errors.append(f"Triplet {tid}: Should be block A, is '{block}'")
        else:
            if split != "test":
                errors.append(f"Triplet {tid}: Should be test split, is '{split}'")
            if tid <= 40 and block != "B":
                errors.append(f"Triplet {tid}: Should be block B, is '{block}'")
            if tid > 40 and block != "C":
                errors.append(f"Triplet {tid}: Should be block C, is '{block}'")

    return errors


def validate_no_duplicates(triplets):
    """Check for duplicate or near-duplicate passages."""
    errors = []

    # Collect all texts
    texts = {}
    for t in triplets:
        tid = t["id"]
        texts[f"{tid}_query"] = t["query"]
        texts[f"{tid}_q2"] = t["q2_far_analogy"]
        texts[f"{tid}_q3"] = t["q3_near_disanalogy"]

    # Check exact duplicates
    seen = {}
    for key, text in texts.items():
        normalized = " ".join(text.lower().split())
        if normalized in seen:
            errors.append(f"Exact duplicate: {key} matches {seen[normalized]}")
        seen[normalized] = key

    return errors


def validate_grammar(triplets):
    """Basic grammar checks."""
    errors = []

    # Check for common errors
    patterns = [
        (r"\ba [aeiou]", "article 'a' before vowel"),
        (r"\ban [^aeiou\s]", "article 'an' before consonant"),
        (r"\s{2,}", "multiple spaces"),
        (r"[.!?]{2,}", "repeated punctuation"),
    ]

    for t in triplets:
        tid = t["id"]
        for field in ["query", "q2_far_analogy", "q3_near_disanalogy"]:
            text = t[field]
            for pattern, desc in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    # Special handling for "a [aeiou]" - skip "a unique", "a European", etc.
                    if "a [aeiou]" in pattern:
                        if not re.search(r"\ba uni|\ba eu|\ba one", text, re.IGNORECASE):
                            match = re.search(pattern, text, re.IGNORECASE)
                            if match:
                                errors.append(f"Triplet {tid} {field}: Possible {desc} near '{match.group()}'")

    return errors


def compute_surface_similarity(triplets):
    """Compute surface similarity diagnostics."""
    if not HAS_SKLEARN:
        return {"error": "scikit-learn not available"}

    results = []

    for t in triplets:
        query = t["query"]
        q2 = t["q2_far_analogy"]
        q3 = t["q3_near_disanalogy"]

        # TF-IDF unigram
        vectorizer_uni = TfidfVectorizer(ngram_range=(1, 1), stop_words='english')
        try:
            vecs = vectorizer_uni.fit_transform([query, q2, q3])
            q2_sim_uni = cosine_similarity(vecs[0:1], vecs[1:2])[0][0]
            q3_sim_uni = cosine_similarity(vecs[0:1], vecs[2:3])[0][0]
        except:
            q2_sim_uni = q3_sim_uni = 0

        # TF-IDF bigram
        vectorizer_bi = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
        try:
            vecs = vectorizer_bi.fit_transform([query, q2, q3])
            q2_sim_bi = cosine_similarity(vecs[0:1], vecs[1:2])[0][0]
            q3_sim_bi = cosine_similarity(vecs[0:1], vecs[2:3])[0][0]
        except:
            q2_sim_bi = q3_sim_bi = 0

        # Token Jaccard
        def jaccard(a, b):
            a_tokens = set(a.lower().split())
            b_tokens = set(b.lower().split())
            if not a_tokens or not b_tokens:
                return 0
            return len(a_tokens & b_tokens) / len(a_tokens | b_tokens)

        q2_jaccard = jaccard(query, q2)
        q3_jaccard = jaccard(query, q3)

        results.append({
            "id": t["id"],
            "schema_id": t["schema_id"],
            "block": t["block"],
            "tfidf_unigram": {"q2": q2_sim_uni, "q3": q3_sim_uni, "q3_minus_q2": q3_sim_uni - q2_sim_uni},
            "tfidf_bigram": {"q2": q2_sim_bi, "q3": q3_sim_bi, "q3_minus_q2": q3_sim_bi - q2_sim_bi},
            "jaccard": {"q2": q2_jaccard, "q3": q3_jaccard, "q3_minus_q2": q3_jaccard - q2_jaccard},
            "q3_more_similar_unigram": q3_sim_uni > q2_sim_uni,
            "q3_more_similar_bigram": q3_sim_bi > q2_sim_bi,
            "q3_more_similar_jaccard": q3_jaccard > q2_jaccard
        })

    return results


def main():
    script_dir = Path(__file__).parent.parent
    data_path = script_dir / "data" / "triplets_60.json"

    if not data_path.exists():
        print(f"ERROR: Dataset not found at {data_path}")
        return

    with open(data_path) as f:
        data = json.load(f)

    triplets = data["triplets"]
    print(f"Loaded {len(triplets)} triplets from {data_path}")

    # Run validations
    all_errors = []

    print("\n1. Validating JSON schema...")
    errors = validate_json_schema(triplets)
    all_errors.extend(errors)
    print(f"   {len(errors)} errors")

    print("\n2. Validating IDs...")
    errors = validate_ids(triplets)
    all_errors.extend(errors)
    print(f"   {len(errors)} errors")

    print("\n3. Validating schema distribution...")
    errors = validate_schema_distribution(triplets)
    all_errors.extend(errors)
    print(f"   {len(errors)} errors")

    print("\n4. Validating splits...")
    errors = validate_splits(triplets)
    all_errors.extend(errors)
    print(f"   {len(errors)} errors")

    print("\n5. Checking for duplicates...")
    errors = validate_no_duplicates(triplets)
    all_errors.extend(errors)
    print(f"   {len(errors)} errors")

    print("\n6. Checking grammar...")
    errors = validate_grammar(triplets)
    all_errors.extend(errors)
    print(f"   {len(errors)} errors")

    # Surface similarity analysis
    print("\n7. Computing surface similarity diagnostics...")
    sim_results = compute_surface_similarity(triplets)

    if isinstance(sim_results, dict) and "error" in sim_results:
        print(f"   {sim_results['error']}")
    else:
        # Count how many have Q3 more similar than Q2
        uni_correct = sum(1 for r in sim_results if r["q3_more_similar_unigram"])
        bi_correct = sum(1 for r in sim_results if r["q3_more_similar_bigram"])
        jac_correct = sum(1 for r in sim_results if r["q3_more_similar_jaccard"])

        print(f"   Q3 more surface-similar than Q2:")
        print(f"     TF-IDF unigram: {uni_correct}/60 ({uni_correct/60:.1%})")
        print(f"     TF-IDF bigram:  {bi_correct}/60 ({bi_correct/60:.1%})")
        print(f"     Token Jaccard:  {jac_correct}/60 ({jac_correct/60:.1%})")

        # Flag cases where Q2 is more similar
        flags = [r for r in sim_results if not r["q3_more_similar_unigram"]]
        if flags:
            print(f"\n   WARNING: {len(flags)} triplets have Q2 more surface-similar than Q3 (TF-IDF unigram):")
            for f in flags[:5]:
                print(f"     Triplet {f['id']} (Schema {f['schema_id']}, Block {f['block']})")

    # Summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)

    if all_errors:
        print(f"\nFOUND {len(all_errors)} ERRORS:")
        for e in all_errors:
            print(f"  - {e}")
    else:
        print("\nAll validations passed!")

    # Compute final checksum
    with open(data_path, "rb") as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()
    print(f"\nDataset checksum: {sha256}")

    # Save report
    report_path = script_dir / "data_quality_report.md"
    with open(report_path, "w") as f:
        f.write("# Data Quality Report\n\n")
        f.write(f"**Dataset:** triplets_60.json\n")
        f.write(f"**Checksum:** {sha256}\n")
        f.write(f"**Generated:** {data['metadata'].get('creation_timestamp', 'unknown')}\n\n")

        f.write("## Validation Results\n\n")
        f.write(f"- Total triplets: {len(triplets)}\n")
        f.write(f"- Unique schemas: 20\n")
        f.write(f"- Realizations per schema: 3\n")
        f.write(f"- Development (Block A): 20\n")
        f.write(f"- Test (Blocks B, C): 40\n\n")

        if all_errors:
            f.write(f"### Errors ({len(all_errors)})\n\n")
            for e in all_errors:
                f.write(f"- {e}\n")
        else:
            f.write("### All validations passed\n\n")

        if isinstance(sim_results, list):
            f.write("\n## Surface Similarity Diagnostics\n\n")
            f.write("| Metric | Q3 > Q2 Count | Percentage |\n")
            f.write("|--------|--------------|------------|\n")
            f.write(f"| TF-IDF unigram | {uni_correct}/60 | {uni_correct/60:.1%} |\n")
            f.write(f"| TF-IDF bigram | {bi_correct}/60 | {bi_correct/60:.1%} |\n")
            f.write(f"| Token Jaccard | {jac_correct}/60 | {jac_correct/60:.1%} |\n")

    print(f"\nReport saved to {report_path}")


if __name__ == "__main__":
    main()
