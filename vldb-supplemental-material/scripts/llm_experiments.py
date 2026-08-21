#!/usr/bin/env python3
"""
LLM-based structural retrieval experiments on the 60-triplet diagnostic.

Each triplet has a query Q1, a far analogy Q2 (same relational structure,
different surface), and a near disanalogy Q3 (same surface, inverted/altered
structure). A system "succeeds" on a triplet when it prefers Q2 over Q3.

Experiments
-----------
Exp 2  Pairwise structural judge:
       Show Q1 and the two candidates (order randomized per triplet) to one
       frontier LLM and ask which candidate shares the same underlying
       relational pattern. This is the expensive O(N) pairwise baseline the
       paper argues does not scale.

Exp 3  Independent extract-then-match (the encoder-vision test):
       Step 1  Extract a relational scaffold from EACH story in isolation
               (the model never sees the other two stories). Cached per text.
       Step 2  Match the query scaffold against each candidate scaffold, with
               the surface text removed. Two matchers:
                 3a  LLM chooses given only the scaffolds.
                 3b  Deterministic: Jaccard over the typed-relation set plus a
                     polarity-pattern bonus. Fully model-free / reproducible.

No answer key is ever shown to the model. Raw responses are cached under
results/llm/cache/ for audit and to make re-runs free. Outputs are written to
results/per_item/ in the same schema the existing schema-clustered analyzer
consumes (by_config -> per_triplet with q2_beats_q3).

Usage:
    OPENAI_API_KEY_AVARY=... python3 scripts/llm_experiments.py --model gpt-4o
"""

import argparse
import hashlib
import json
import os
import random
import re
import time
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "triplets_60.json"
PER_ITEM_DIR = ROOT / "results" / "per_item"
LLM_DIR = ROOT / "results" / "llm"
CACHE_DIR = LLM_DIR / "cache"

SEED = 42

# Fixed, schema-agnostic relation vocabulary. These are abstract relational
# predicates, NOT the 20 schema labels, so extraction cannot trivially encode
# the answer key. Used by the deterministic matcher (3b).
RELATION_VOCAB = [
    "intends", "causes", "prevents", "enables", "conceals", "deceives",
    "manufactures_threat", "sacrifices_for", "exploits", "misattributes_credit",
    "appears_positive", "actually_negative", "appears_negative", "actually_positive",
    "reverses_expectation", "tests_loyalty", "feigns_inability", "protects_by_withholding",
    "harms_by_helping", "reveals_hidden_trait",
]


# --------------------------------------------------------------------------
# Client + caching
# --------------------------------------------------------------------------
def get_client():
    key = os.environ.get("OPENAI_API_KEY_AVARY") or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise SystemExit("No OpenAI key found (OPENAI_API_KEY_AVARY / OPENAI_API_KEY).")
    return OpenAI(api_key=key)


def _cache_path(key: str) -> Path:
    h = hashlib.sha256(key.encode()).hexdigest()[:24]
    return CACHE_DIR / f"{h}.json"


def cached_chat(client, model, messages, tag, temperature=0.0, max_tokens=800):
    """Deterministic (temp=0) chat call with on-disk caching keyed by content."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    key = json.dumps({"m": model, "t": temperature, "msg": messages, "tag": tag},
                     sort_keys=True)
    cp = _cache_path(key)
    if cp.exists():
        return json.loads(cp.read_text())["content"]
    for attempt in range(5):
        try:
            resp = client.chat.completions.create(
                model=model, messages=messages, temperature=temperature,
                max_tokens=max_tokens, response_format={"type": "json_object"},
            )
            content = resp.choices[0].message.content
            cp.write_text(json.dumps({"key": key, "content": content}, indent=0))
            return content
        except Exception as e:  # noqa: BLE001 - retry transient errors
            wait = 2 ** attempt
            print(f"  [retry {attempt+1}/5 after {wait}s] {e}")
            time.sleep(wait)
    raise RuntimeError(f"chat call failed after retries: {tag}")


def parse_json(text):
    try:
        return json.loads(text)
    except Exception:  # noqa: BLE001
        m = re.search(r"\{.*\}", text, re.DOTALL)
        return json.loads(m.group(0)) if m else {}


# --------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------
def load_triplets():
    data = json.loads(DATA_PATH.read_text())
    return data["triplets"]


def make_record(t, q2_wins, extra=None):
    rec = {
        "triplet_id": t["id"],
        "schema_id": t["schema_id"],
        "block": t["block"],
        "split": t["split"],
        "q2_beats_q3": bool(q2_wins),
        "outcome": "Q2_WIN" if q2_wins else "Q3_WIN",
    }
    if extra:
        rec.update(extra)
    return rec


def write_per_item(name, config_name, model, per_triplet):
    PER_ITEM_DIR.mkdir(parents=True, exist_ok=True)
    n = len(per_triplet)
    wins = sum(1 for r in per_triplet if r["q2_beats_q3"])
    def split_acc(s):
        rows = [r for r in per_triplet if r["split"] == s]
        return (sum(r["q2_beats_q3"] for r in rows), len(rows))
    dev_w, dev_n = split_acc("development")
    test_w, test_n = split_acc("test")
    out = {
        "metadata": {"experiment": name, "model": model, "seed": SEED},
        "by_config": {
            config_name: {
                "config": config_name,
                "overall": {"q2_wins": wins, "n": n, "accuracy": wins / n},
                "development": {"q2_wins": dev_w, "n": dev_n,
                                "accuracy": dev_w / dev_n if dev_n else None},
                "test": {"q2_wins": test_w, "n": test_n,
                         "accuracy": test_w / test_n if test_n else None},
                "per_triplet": per_triplet,
            }
        },
    }
    path = PER_ITEM_DIR / f"{name}_results.json"
    path.write_text(json.dumps(out, indent=2))
    print(f"  wrote {path.relative_to(ROOT)}  overall {wins}/{n}="
          f"{100*wins/n:.1f}%  dev {dev_w}/{dev_n}  test {test_w}/{test_n}")
    return out


# --------------------------------------------------------------------------
# Experiment 2 - pairwise structural judge
# --------------------------------------------------------------------------
JUDGE_SYS = (
    "You compare short personal anecdotes by their underlying relational "
    "structure - the pattern of intentions, causes, deceptions, reversals, and "
    "outcomes among the people involved - NOT by their surface topic, setting, "
    "or vocabulary. Two stories can be about totally different situations yet "
    "share the same deep structure; two stories can share the same topic yet "
    "have opposite structure."
)


def exp2_pairwise(client, model, triplets):
    rng = random.Random(SEED)
    rows = []
    for t in triplets:
        # randomize which candidate is shown as A vs B
        q2_is_a = rng.random() < 0.5
        cand_a = t["q2_far_analogy"] if q2_is_a else t["q3_near_disanalogy"]
        cand_b = t["q3_near_disanalogy"] if q2_is_a else t["q2_far_analogy"]
        user = (
            f"SITUATION:\n{t['query']}\n\n"
            f"CANDIDATE A:\n{cand_a}\n\n"
            f"CANDIDATE B:\n{cand_b}\n\n"
            "Which candidate shares the same underlying relational structure as "
            "the SITUATION (ignore surface topic similarity)? "
            'Respond as JSON: {"choice": "A" or "B", "reason": "<one sentence>"}.'
        )
        content = cached_chat(
            client, model,
            [{"role": "system", "content": JUDGE_SYS},
             {"role": "user", "content": user}],
            tag=f"exp2:{t['id']}")
        ans = parse_json(content)
        choice = str(ans.get("choice", "")).strip().upper()[:1]
        chose_q2 = (choice == "A" and q2_is_a) or (choice == "B" and not q2_is_a)
        rows.append(make_record(t, chose_q2, {
            "choice": choice, "q2_position": "A" if q2_is_a else "B",
            "reason": ans.get("reason", ""),
        }))
        print(f"  [exp2] t{t['id']:>2} choice={choice} q2@{'A' if q2_is_a else 'B'} "
              f"-> {'Q2' if chose_q2 else 'Q3'}")
    return rows


# --------------------------------------------------------------------------
# Experiment 3 - independent extraction, then match
# --------------------------------------------------------------------------
EXTRACT_SYS = (
    "You extract the abstract relational skeleton of a single short anecdote. "
    "Focus on the pattern of intentions, causes, concealment, deception, "
    "reversals of appearance vs reality, and who is helped or harmed. "
    "Abstract away all surface details (names, jobs, objects, settings): use "
    "generic role labels like AGENT, TARGET, THIRD_PARTY."
)


def extract_scaffold(client, model, text):
    vocab = ", ".join(RELATION_VOCAB)
    user = (
        f"ANECDOTE:\n{text}\n\n"
        "Extract its relational skeleton. Respond as JSON with keys:\n"
        '  "roles": list of generic role labels used (e.g. ["AGENT","TARGET"]),\n'
        '  "relations": list of [source_role, predicate, target_role] triples,\n'
        f"      where predicate is chosen ONLY from this set: [{vocab}],\n"
        '  "pattern": one abstract sentence describing the deep structure with '
        "no surface nouns.\n"
        "Use only the allowed predicates. Do not mention the concrete topic."
    )
    content = cached_chat(
        client, model,
        [{"role": "system", "content": EXTRACT_SYS},
         {"role": "user", "content": user}],
        tag="extract")
    sc = parse_json(content)
    # normalize
    rels = []
    for tr in sc.get("relations", []):
        if isinstance(tr, list) and len(tr) == 3:
            pred = str(tr[1]).strip().lower()
            if pred in RELATION_VOCAB:
                rels.append([str(tr[0]).strip().upper(), pred, str(tr[2]).strip().upper()])
    sc["relations"] = rels
    return sc


# --------------------------------------------------------------------------
# Role-constrained extractor variant (Option A representation change).
#
# The free-form extractor above is told to "use generic role labels LIKE
# AGENT/TARGET/THIRD_PARTY" but is free to invent node labels; on multi-entity
# causal anecdotes it emits domain nouns (POLICY, INDUSTRY, CEO, LAYOFFS).
# The model-free matcher only permutes the three generic roles, so those
# domain-noun nodes are pinned literals that never align across domains and the
# directed-triple Jaccard collapses. This variant forces every node position
# into a CLOSED role vocabulary so cross-domain alignment is possible. Node
# labels are NOT rewritten post hoc (that would be model-in-the-loop curation);
# out-of-vocabulary leakage is left in the scaffold so it stays visible to the
# matcher and measurable as an extraction-faithfulness screen.
ROLE_VOCAB = ["AGENT", "TARGET", "THIRD_PARTY", "ACTUALITY"]

EXTRACT_ROLES_SYS = (
    "You extract the abstract relational skeleton of a single short anecdote. "
    "Focus on the pattern of intentions, causes, concealment, deception, "
    "reversals of appearance vs reality, and who is helped or harmed. "
    "Abstract away ALL surface details. Every participant or object MUST be "
    "labelled with a generic role from a fixed closed set; never use a concrete "
    "noun (no names, jobs, policies, companies, conditions, or outcome nouns)."
)


def extract_scaffold_constrained(client, model, text):
    """Like extract_scaffold, but node labels are restricted to ROLE_VOCAB."""
    vocab = ", ".join(RELATION_VOCAB)
    roles = ", ".join(ROLE_VOCAB)
    user = (
        f"ANECDOTE:\n{text}\n\n"
        "Extract its relational skeleton. Respond as JSON with keys:\n"
        f'  "roles": the subset of the CLOSED role set [{roles}] that you use,\n'
        '  "relations": list of [source_role, predicate, target_role] triples,\n'
        f"      where EVERY source_role and target_role is chosen ONLY from "
        f"[{roles}], and predicate ONLY from [{vocab}],\n"
        '  "pattern": one abstract sentence describing the deep structure with '
        "no surface nouns.\n"
        "Role rules: the primary actor is AGENT; the person or thing acted upon "
        "is TARGET; any additional party is THIRD_PARTY; an abstract state, "
        "truth, intention, or outcome that is concealed/intended is ACTUALITY. "
        "Do NOT invent any other node label and do NOT use concrete nouns."
    )
    content = cached_chat(
        client, model,
        [{"role": "system", "content": EXTRACT_ROLES_SYS},
         {"role": "user", "content": user}],
        tag="extract_roles")
    sc = parse_json(content)
    # normalize: keep only allowed predicates; keep node labels verbatim
    # (uppercased) so out-of-vocab leakage stays visible/measurable.
    rels = []
    for tr in sc.get("relations", []):
        if isinstance(tr, list) and len(tr) == 3:
            pred = str(tr[1]).strip().lower()
            if pred in RELATION_VOCAB:
                rels.append([str(tr[0]).strip().upper(), pred, str(tr[2]).strip().upper()])
    sc["relations"] = rels
    return sc


def scaffold_predicate_set(sc):
    return set(r[1] for r in sc.get("relations", []))


# polarity predicates: presence signals appearance-vs-reality direction
POS_APP = {"appears_positive", "actually_positive"}
NEG_APP = {"appears_negative", "actually_negative"}


def overlap_score(q, c):
    """Deterministic structural similarity between two scaffolds (3b)."""
    pq, pc = scaffold_predicate_set(q), scaffold_predicate_set(c)
    if not pq or not pc:
        return 0.0
    jac = len(pq & pc) / len(pq | pc)
    # polarity-pattern agreement bonus: reward matching the appears/actually mix
    def pol(p):
        return (("appears_positive" in p) - ("appears_negative" in p),
                ("actually_positive" in p) - ("actually_negative" in p))
    bonus = 0.15 * sum(1 for a, b in zip(pol(pq), pol(pc)) if a == b and a != 0)
    return jac + bonus


def exp3_extract_then_match(client, model, triplets):
    # Step 1: extract every unique story once (independent, cached).
    scaffolds = {}
    def get(text):
        h = hashlib.sha256(text.encode()).hexdigest()[:16]
        if h not in scaffolds:
            scaffolds[h] = extract_scaffold(client, model, text)
        return scaffolds[h]

    rng = random.Random(SEED)
    rows_llm, rows_ov = [], []
    for t in triplets:
        sq = get(t["query"])
        s2 = get(t["q2_far_analogy"])
        s3 = get(t["q3_near_disanalogy"])

        # ---- 3b deterministic overlap matcher ----
        ov2, ov3 = overlap_score(sq, s2), overlap_score(sq, s3)
        rows_ov.append(make_record(t, ov2 > ov3, {
            "overlap_q2": round(ov2, 3), "overlap_q3": round(ov3, 3)}))

        # ---- 3a LLM matcher over scaffolds only (surface removed) ----
        q2_is_a = rng.random() < 0.5
        sa = s2 if q2_is_a else s3
        sb = s3 if q2_is_a else s2
        def fmt(s):
            return json.dumps({"roles": s.get("roles", []),
                               "relations": s.get("relations", []),
                               "pattern": s.get("pattern", "")}, indent=0)
        user = (
            "Each item below is the abstract relational skeleton of a story "
            "(surface details removed).\n\n"
            f"QUERY SKELETON:\n{fmt(sq)}\n\n"
            f"CANDIDATE A SKELETON:\n{fmt(sa)}\n\n"
            f"CANDIDATE B SKELETON:\n{fmt(sb)}\n\n"
            "Which candidate skeleton has the same relational structure as the "
            'QUERY? Respond as JSON: {"choice":"A" or "B"}.'
        )
        content = cached_chat(
            client, model,
            [{"role": "system", "content":
              "You match stories by relational structure using only their "
              "abstract skeletons."},
             {"role": "user", "content": user}],
            tag=f"exp3match:{t['id']}")
        choice = str(parse_json(content).get("choice", "")).strip().upper()[:1]
        chose_q2 = (choice == "A" and q2_is_a) or (choice == "B" and not q2_is_a)
        rows_llm.append(make_record(t, chose_q2, {
            "choice": choice, "q2_position": "A" if q2_is_a else "B"}))
        print(f"  [exp3] t{t['id']:>2} overlap {ov2:.2f}v{ov3:.2f}->"
              f"{'Q2' if ov2>ov3 else 'Q3'}  llm={choice}->"
              f"{'Q2' if chose_q2 else 'Q3'}")

    # persist scaffolds for audit
    LLM_DIR.mkdir(parents=True, exist_ok=True)
    (LLM_DIR / "scaffolds.json").write_text(json.dumps(scaffolds, indent=2))
    return rows_llm, rows_ov


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gpt-4o")
    ap.add_argument("--exp", choices=["2", "3", "all"], default="all")
    ap.add_argument("--limit", type=int, default=0, help="first N triplets (smoke test)")
    args = ap.parse_args()

    client = get_client()
    triplets = load_triplets()
    if args.limit:
        triplets = triplets[: args.limit]
    print(f"model={args.model}  triplets={len(triplets)}  seed={SEED}")

    if args.exp in ("2", "all"):
        print("\n== Exp 2: pairwise structural judge ==")
        rows = exp2_pairwise(client, args.model, triplets)
        write_per_item("llm_pairwise", f"pairwise_{args.model}", args.model, rows)

    if args.exp in ("3", "all"):
        print("\n== Exp 3: independent extract-then-match ==")
        rows_llm, rows_ov = exp3_extract_then_match(client, args.model, triplets)
        write_per_item("llm_extract_match", f"extract_llm_{args.model}",
                       args.model, rows_llm)
        write_per_item("llm_extract_overlap", f"extract_overlap_{args.model}",
                       args.model, rows_ov)


if __name__ == "__main__":
    main()
