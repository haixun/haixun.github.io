#!/usr/bin/env python3
"""Build the static course site for the opening paragraphs of "Cien años de soledad".

    python3 build.py

Reads everything under content/ and writes index.html, lesson-01.html ... lesson-40.html,
paragraph.html, paragraph-2.html, vocabulary.html, practice.html and data.js next to this file.
Standard library only.  Edit the files in content/, never the generated HTML.

Per paragraph N (the files of paragraph 1 have no number, for historical reasons):
  content/paraN.txt        the supplied text: Spanish, a line with "-" or "==", then the English translation
  content/chunksN.txt      phrase-by-phrase breakdown with literal glosses
  content/vocabN.txt       vocabulary and expressions (only forms not already in an earlier paragraph)
  content/examplesN.txt    one original example sentence for every noun, verb and adjective in vocabN.txt
  content/timingsN.json    sentence / phrase time ranges inside audio/paraN.m4a (measured, see the text pages)
Shared:
  content/lessons_a.py ... lessons_d.py   the lessons (a, b: paragraph 1; c, d: paragraph 2)
  content/links.json                      verified pronunciation links (written by the link checker)

Sentence numbers in the content files are local to their paragraph.  Internally every sentence
also has a global number g (paragraph 1: 1-17, paragraph 2: 18-47); audio targets, practice
ranges and saved progress use g, so paragraph 1 keeps the numbers it had before paragraph 2 existed.
"""
import hashlib, html, json, re, sys, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
C = HERE / "content"
sys.dont_write_bytecode = True
sys.path.insert(0, str(C))
from lessons_a import LESSONS_A  # noqa: E402
from lessons_b import LESSONS_B  # noqa: E402
from lessons_c import LESSONS_C  # noqa: E402
from lessons_d import LESSONS_D  # noqa: E402

LESSONS = LESSONS_A + LESSONS_B + LESSONS_C + LESSONS_D
NL = len(LESSONS)
TITLE = "Cien años de soledad: the opening paragraphs"
esc = html.escape

# The course is organised as book -> chapter -> paragraph -> lesson.  Add chapters and paragraphs here.
BOOK = dict(title="Cien años de soledad", chapters=[dict(n=1, title="Chapter 1", paras=[1, 2])])

PARAS = [
    dict(n=1, file="para1.txt", chunks="chunks.txt", vocab="vocab.txt", examples="examples.txt", timings="timings.json", page="paragraph.html",
         scenes=[(1, 1, "The memory"), (2, 3, "The village"), (4, 8, "The gypsies"), (9, 13, "The bargain"), (14, 17, "The search")],
         stats=dict(mismatches=6, min_pause=0.41), source_note="the opening"),
    dict(n=2, file="para2.txt", chunks="chunks2.txt", vocab="vocab2.txt", examples="examples2.txt", timings="timings2.json", page="paragraph-2.html",
         scenes=[(1, 6, "The telescope"), (7, 12, "The burning glass"), (13, 19, "The weapon of war"),
                 (20, 25, "The instruments"), (26, 30, "The discovery")],
         stats={}, source_note="the stretch that follows paragraph 1"),
]

# ---------------------------------------------------------------- text
ES_SPLIT = re.compile(r"(?<=[.»])\s+(?=[«A-ZÁÉÍÓÚÑ])")
EN_SPLIT = re.compile(r"(?:(?<=\.)|(?<=\.”))\s+(?=[“A-ZÁÉÍÓÚ])")


def _sentences(block, rx):
    out = []
    for part in re.split(r"\n\s*\n", block.strip()):      # a blank line always ends a sentence
        out += rx.split(" ".join(part.split()))
    return out


def load_para(name):
    raw = (C / name).read_text(encoding="utf-8")
    es, en = re.split(r"\n(?:-|==)\n", raw)
    S, E = _sentences(es, ES_SPLIT), _sentences(en, EN_SPLIT)
    # the published translation does not always keep the sentence divisions of the original
    if name == "para1.txt":
        E[7:9] = [E[7] + " " + E[8]]            # Melquíades' speech: two English sentences, one Spanish
    if name == "para2.txt":
        a, b = E[8].split(", but ", 1)          # one English sentence covers Spanish sentences 9 and 10
        E[8:9] = [a + ",", "but " + b]
    assert len(S) == len(E), (name, len(S), len(E))
    return S, E


WORD_RE = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+")


def words(s):
    return WORD_RE.findall(s)


def fold(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


SENT = []      # global list; SENT[g-1] = dict(es, en, p, n, t)
CHUNKS = []    # dict(g, p, es, en, t)
for P in PARAS:
    S, E = load_para(P["file"])
    P["off"] = len(SENT)
    P["len"] = len(S)
    T = json.loads((C / P["timings"]).read_text())
    assert len(T["sentences"]) == len(S), P["file"]
    P["clip"] = round(T["clip"][1] - T["clip"][0], 2)
    P["stats"] = {**T.get("stats", {}), **P["stats"]}
    for i, (s, e) in enumerate(zip(S, E)):
        SENT.append(dict(es=s, en=e, p=P["n"], n=i + 1, t=T["sentences"][i]))
    mine, cur = [], None
    for line in (C / P["chunks"]).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        m = re.match(r"# S(\d+)$", line)
        if m:
            cur = int(m.group(1))
            continue
        if not line or line.startswith("#"):
            continue
        a, b = [x.strip() for x in line.split("|")]
        mine.append(dict(g=P["off"] + cur, p=P["n"], es=a, en=b))
    for i, s in enumerate(S):
        joined = " ".join(c["es"] for c in mine if c["g"] == P["off"] + i + 1)
        assert joined == s, f"chunks of paragraph {P['n']} sentence {i+1} do not reproduce the source text:\n{joined}\n{s}"
    assert len(T["chunks"]) == len(mine), P["chunks"]
    for c, t in zip(mine, T["chunks"]):
        c["t"] = t
    P["chunk_n"] = len(mine)
    P["chunk_audio"] = sum(1 for c in mine if c["t"])
    P["words"] = sum(len(words(s)) for s in S)
    CHUNKS += mine
PBY = {P["n"]: P for P in PARAS}


def G(p, n):
    return PBY[p]["off"] + n


def para_of(g):
    return SENT[g - 1]["p"]


def loc(g):
    return SENT[g - 1]["n"]


# ---------------------------------------------------------------- vocabulary
VOCAB, EXPR = {}, []
for P in PARAS:
    for line in (C / P["vocab"]).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        is_expr = line.startswith("+")
        f = [x.strip() for x in line.lstrip("+").split("|")]
        assert len(f) == 4, line
        d = dict(f=f[0], b=f[1], g=f[2], m=f[3])
        if is_expr:
            EXPR.append(d)
        else:
            assert f[0] not in VOCAB, f"{f[0]} is defined twice"
            VOCAB[f[0]] = d
try:
    LINKS = json.loads((C / "links.json").read_text(encoding="utf-8"))
except FileNotFoundError:
    LINKS = {}


def key_of(word):
    if word in VOCAB:
        return word
    if word.lower() in VOCAB:
        return word.lower()
    raise KeyError(f"no vocabulary entry for {word!r}")


missing = sorted({w for s in SENT for w in words(s["es"]) if w not in VOCAB and w.lower() not in VOCAB})
assert not missing, f"words with no vocabulary entry: {missing}"
for g, s in enumerate(SENT, 1):
    for w in words(s["es"]):
        v = VOCAB[key_of(w)]
        v.setdefault("s", [])
        if g not in v["s"]:
            v["s"].append(g)
unused = [k for k, v in VOCAB.items() if "s" not in v]
assert not unused, f"vocabulary entries that never occur: {unused}"
SENT_TOKENS = [[w.lower() for w in words(s["es"])] for s in SENT]
for e in EXPR:
    toks = [w.lower() for w in words(e["f"])]
    e["s"] = [i + 1 for i, st in enumerate(SENT_TOKENS)
              if any(st[j:j + len(toks)] == toks for j in range(len(st) - len(toks) + 1))]
    assert e["s"], f"expression not found in the text: {e['f']}"

# ---------------------------------------------------------------- syllables and sound notes
STRONG, WEAK, ACCW = set("aeoáéó"), set("iuü"), set("íú")


def units(word):
    out, i, w = [], 0, word
    while i < len(w):
        two = w[i:i + 2].lower()
        nxt = w[i + 2:i + 3].lower()
        if two in ("ch", "ll", "rr", "qu") or (two == "gu" and nxt and nxt in "eiéí"):
            out.append(w[i:i + 2]); i += 2
        else:
            out.append(w[i]); i += 1
    return out


def syllables(word):
    """-> (list of syllables, index of the stressed one)"""
    us = units(word)

    def kind(j):
        u = us[j].lower()
        if u in STRONG: return "S"
        if u in WEAK: return "W"
        if u in ACCW: return "A"
        if u == "y" and j == len(us) - 1: return "W"
        return "C"
    kinds = [kind(j) for j in range(len(us))]
    nuclei, j = [], 0
    while j < len(us):
        if kinds[j] == "C":
            j += 1; continue
        a = j; strong = kinds[j] == "S"; last = kinds[j]; j += 1
        while j < len(us) and kinds[j] != "C":
            k = kinds[j]
            if last == "A" or k == "A" or (k == "S" and strong):
                break
            strong = strong or k == "S"; last = k; j += 1
        nuclei.append((a, j))
    if not nuclei:
        return [word], 0
    bounds = [0]
    for (a0, b0), (a1, b1) in zip(nuclei, nuclei[1:]):
        cl = [u.lower() for u in us[b0:a1]]
        n = len(cl)
        insep = lambda x, y: y in "lr" and x in "bcdfgkptv" and not (x == "d" and y == "l")
        if n <= 1: cut = b0
        elif n == 2: cut = b0 if insep(cl[0], cl[1]) else b0 + 1
        elif n == 3: cut = b0 + 1 if insep(cl[1], cl[2]) else b0 + 2
        else: cut = b0 + 2
        bounds.append(cut)
    bounds.append(len(us))
    syl = ["".join(us[bounds[i]:bounds[i + 1]]) for i in range(len(bounds) - 1)]
    stress = None
    for i, sy in enumerate(syl):
        if any(ch in "áéíóúÁÉÍÓÚ" for ch in sy):
            stress = i
    if stress is None:
        stress = len(syl) - 1 if len(syl) == 1 or word[-1].lower() not in "aeiouns" else len(syl) - 2
    return syl, stress


SYL_OVERRIDE = {"XV": "<b>quin</b>·ce", "Hermann": "<b>Her</b>·mann", "personalmente": "per·so·<b>nal</b>·<b>men</b>·te"}


def syl_html(word):
    if word in SYL_OVERRIDE:
        return SYL_OVERRIDE[word]
    syl, st = syllables(word)
    return "·".join(f"<b>{esc(s)}</b>" if i == st and len(syl) > 1 else esc(s) for i, s in enumerate(syl))


def sound_notes(word):
    w = word.lower()
    if word == "XV":
        return ["read as the number quince: qu = k; c = s (Latin America) or th (Spain)"]
    if word == "Hermann":
        return ["a German name: in Spanish the H is silent or lightly breathed"]
    n = []
    if re.search(r"(?<!c)h", w): n.append("h is silent")
    if re.search(r"hu[aeiáéí]", w): n.append("hu + vowel = w")
    if "j" in w: n.append("j = breathy h")
    if re.search(r"g[eiéí]", w): n.append("g before e / i = breathy h")
    if re.search(r"gu[eiéí]", w): n.append("gu before e / i = hard g, u silent")
    if re.search(r"gu[aoáó]", w): n.append("gu + a = gw")
    if "ll" in w: n.append("ll = y")
    if "ñ" in w: n.append("ñ = ny")
    if "qu" in w: n.append("qu = k")
    if re.search(r"cu[aeiáéíoó]", w): n.append("cu + vowel = kw")
    if "z" in w or re.search(r"c[eiéí]", w): n.append("c before e / i, and z = s (Latin America) or th (Spain)")
    if "v" in w: n.append("v = soft b")
    if "rr" in w or w.startswith("r") or re.search(r"[nls]r", w): n.append("rolled r")
    if "x" in w: n.append("x = ks")
    if w.endswith("y"): n.append("final y = ee")
    if w.endswith("mente") and len(w) > 7: n.append("-mente words keep two stresses")
    return n


SAY = {"XV": "quince"}
for k, v in VOCAB.items():
    v["syl"] = syl_html(v["f"])
    v["sn"] = sound_notes(v["f"])
    L = LINKS.get(k, {})
    if L.get("ok"):
        v["u"] = L["url"]; v["uk"] = L["kind"]
        if L["kind"] == "base": v["ub"] = L.get("base", v["b"])
for e in EXPR:
    L = LINKS.get(e["f"], {})
    if L.get("ok"):
        e["u"] = L["url"]

# ---------------------------------------------------------------- example sentences
CONTENT_WORD = ("verb", "noun", "adjective", "past participle", "gerund", "infinitive", "ordinal")


def needs_example(v):
    return v["g"].lower().startswith(CONTENT_WORD)


for P in PARAS:
    for line in (C / P["examples"]).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        f = [x.strip() for x in line.split("|")]
        assert len(f) == 3, line
        assert f[0] in VOCAB, f"example for a word that is not in the vocabulary: {f[0]}"
        assert "x" not in VOCAB[f[0]], f"two examples for {f[0]}"
        assert f[0].lower() in [w.lower() for w in words(f[1])], f"the example for {f[0]} does not contain that exact form: {f[1]}"
        VOCAB[f[0]]["x"] = [f[1], f[2]]
no_example = [k for k, v in VOCAB.items() if needs_example(v) and "x" not in v]
assert not no_example, f"nouns, verbs or adjectives without an example sentence: {no_example}"


def ex_html(v):
    if "x" not in v:
        return ""
    return (f'<div class="ex"><span class="ex-l">Example</span> <span class="es" lang="es">{esc(v["x"][0])}</span>'
            f'<span class="ex-en">{esc(v["x"][1])}</span></div>')

# ---------------------------------------------------------------- lesson bookkeeping
for n, L in enumerate(LESSONS, 1):
    L["n"] = n
    p = L["p"] = L.get("para", 1)
    L["new_g"] = [G(p, x) for x in L["new"]]
    L["review_g"] = [G(p, x) for x in L["review"]]
    if L.get("part"):
        s, a, b = L["part"]
        ids = [i for i, c in enumerate(CHUNKS) if c["g"] == G(p, s)][a - 1:b]
    else:
        ids = [i for i, c in enumerate(CHUNKS) if c["g"] in L["new_g"]]
    L["chunk_ids"] = ids
seen_words, seen_expr = set(), set()
for L in LESSONS:
    text = " ".join(CHUNKS[i]["es"] for i in L["chunk_ids"])
    toks = [w.lower() for w in words(text)]
    L["new_words"] = []
    for w in words(text):
        k = key_of(w)
        if k not in seen_words:
            seen_words.add(k); L["new_words"].append(k)
    L["new_expr"] = []
    for j, e in enumerate(EXPR):
        et = [w.lower() for w in words(e["f"])]
        if j not in seen_expr and any(toks[i:i + len(et)] == et for i in range(len(toks) - len(et) + 1)):
            seen_expr.add(j); L["new_expr"].append(j)
    L["upto"] = max([CHUNKS[i]["g"] for i in L["chunk_ids"]] or L["review_g"])     # last sentence reached, global
assert seen_words == set(VOCAB), set(VOCAB) - seen_words
assert len(seen_expr) == len(EXPR), [EXPR[j]["f"] for j in range(len(EXPR)) if j not in seen_expr]
PART_LESSONS = {P["n"]: [L["n"] for L in LESSONS if L["p"] == P["n"]] for P in PARAS}


# ---------------------------------------------------------------- html helpers
def wordify(text):
    """wrap every Spanish word in a tappable span"""
    out, pos = [], 0
    for m in WORD_RE.finditer(text):
        out.append(esc(text[pos:m.start()]))
        out.append(f'<span class="w" data-k="{esc(key_of(m.group()))}">{esc(m.group())}</span>')
        pos = m.end()
    out.append(esc(text[pos:]))
    return "".join(out)


def rich(s, lesson=None):
    s = re.sub(r"<es>(.*?)</es>", r'<span class="es" lang="es">\1</span>', s, flags=re.S)
    s = re.sub(r"<rs>(.*?)</rs>", r'<span class="rs">\1</span>', s, flags=re.S)
    if lesson:
        s = re.sub(r'<li data-check="(\w+)">(.*?)</li>',
                   lambda m: f'<li><label class="tick"><input type="checkbox" data-check="L{lesson}:{m.group(1)}"> <span>{m.group(2)}</span></label></li>',
                   s, flags=re.S)
    return s


def play_btn(target, label="", title="Play the audiobook recording", cls=""):
    return (f'<button class="btn play {cls}" data-play="{target}" title="{esc(title)}" aria-label="{esc(title)}">'
            f'<span class="ico">▶</span>{label}</button>')


def say_btn(text, label="Voice"):
    return (f'<button class="btn say" data-say="{esc(text)}" title="Browser voice: synthesized speech, not the audiobook" '
            f'aria-label="Say with the browser voice">{label}</button>')


def range_target(gs):
    """audio target for a run of sentences inside one paragraph"""
    p = para_of(gs[0])
    if len(gs) == PBY[p]["len"]:
        return f"all{p}"
    return f"s{gs[0]}" if len(gs) == 1 else f"r{gs[0]}-{gs[-1]}"


def sentence_block(g):
    s = SENT[g - 1]
    return f'''<div class="sent" id="s{s["n"]}" data-s="{g}">
  <div class="sent-bar"><span class="num">{s["n"]}</span>{play_btn(f"s{g}", " Recording", f"Play sentence {s['n']} from the audiobook")}
    <button class="btn rep" data-repeat="s{g}" title="Repeat this sentence until stopped">Repeat</button>{say_btn(s["es"])}</div>
  <div class="pair"><p class="es-text" lang="es">{wordify(s["es"])}</p><p class="en-text">{esc(s["en"])}</p></div>
</div>'''


def reading_view(p):
    P = PBY[p]
    return '<div class="reading" lang="es">' + " ".join(
        f'<span class="rs-sent" data-s="{g}">{wordify(SENT[g-1]["es"])}</span>' for g in range(P["off"] + 1, P["off"] + P["len"] + 1)) + "</div>"


def chunk_rows(ids):
    rows = []
    for i in ids:
        c = CHUNKS[i]
        rec = play_btn(f"c{i}", "", "Play this phrase from the audiobook") if c["t"] else '<span class="norec" title="The narrator does not pause around this phrase, so it cannot be cut cleanly from the recording">–</span>'
        rows.append(f'<tr><td class="ctl">{rec}{say_btn(c["es"])}</td>'
                    f'<td class="es-text" lang="es">{wordify(c["es"])}</td><td class="gloss">{esc(c["en"])}</td></tr>')
    return ('<div class="tablewrap"><table class="chunks"><thead><tr><th>Hear</th><th>Spanish</th><th>Close English</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def link_html(v, short=False):
    if not v.get("u"):
        return ""
    if v.get("uk") == "base":
        lab = f'SpanishDict: base form <i lang="es">{esc(v["ub"])}</i>'
    elif v.get("uk") == "entry":
        lab = "SpanishDict entry"
    else:
        lab = "SpanishDict" if short else "Hear on SpanishDict"
    return f'<a class="ext" href="{esc(v["u"])}" target="_blank" rel="noopener">{lab} ↗</a>'


def vocab_rows(keys):
    rows = []
    for k in keys:
        v = VOCAB[k]
        base = f'<i lang="es">{esc(v["b"])}</i>' if v["b"] != v["f"] else '<span class="same" title="This is already the base form">=</span>'
        rows.append(f'<tr><td><span class="w head" data-k="{esc(k)}" lang="es">{esc(v["f"])}</span><div class="syl" lang="es">{v["syl"]}</div></td>'
                    f'<td class="basecol" data-label="Base form">{base}</td>'
                    f'<td>{esc(v["m"])}{ex_html(v)}</td><td class="gram">{rich(esc(v["g"]))}</td>'
                    f'<td class="ctl">{say_btn(SAY.get(k, v["f"]))}{link_html(v, True)}</td></tr>')
    return ('<div class="tablewrap"><table class="vocab lessonwords"><thead><tr><th>Word</th><th>Base form</th><th>Meaning here, and an example</th><th>Grammar</th><th>Hear</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def expr_rows(idxs):
    rows = []
    for j in idxs:
        e = EXPR[j]
        link = f'<a class="ext" href="{esc(e["u"])}" target="_blank" rel="noopener">SpanishDict ↗</a>' if e.get("u") else ""
        pat = "" if fold(e["b"]) == fold(e["f"]) else f'<div class="base">pattern: <i lang="es">{esc(e["b"])}</i></div>'
        rows.append(f'<tr><td class="es-text" lang="es">{wordify(e["f"])}{pat}</td><td>{esc(e["m"])}</td>'
                    f'<td class="gram">{esc(e["g"])}</td><td class="ctl">{say_btn(e["f"])}{link}</td></tr>')
    return ('<div class="tablewrap"><table class="vocab"><thead><tr><th>Expression</th><th>Meaning here</th><th>How it works</th><th>Hear</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def cloze(options, default=0):
    """options: list of (label, [global sentence numbers])"""
    opts = "".join(f'<option value="{",".join(map(str, s))}"{" selected" if i == default else ""}>{esc(l)}</option>'
                   for i, (l, s) in enumerate(options))
    return f'''<div class="cloze" data-cloze>
  <div class="cz-bar">
    <label>Text <select class="cz-range">{opts}</select></label>
    <div class="cz-levels" role="group" aria-label="Difficulty">
      <button class="btn" data-level="0" title="Full text">0</button><button class="btn" data-level="1" title="One word in four hidden">1</button><button class="btn" data-level="2" title="Half the words hidden">2</button><button class="btn" data-level="3" title="Three words in four hidden">3</button><button class="btn" data-level="4" title="First letters only">4</button><button class="btn" data-level="5" title="Everything hidden">5</button>
    </div>
  </div>
  <p class="cz-hint"></p>
  <div class="cz-body" lang="es"></div>
  <div class="cz-foot">
    <button class="btn" data-cz="reveal">Reveal all</button><button class="btn" data-cz="reset">Hide again</button><button class="btn" data-cz="shuffle">Hide different words</button>
    <label class="tick"><input type="checkbox" class="cz-en"> <span>English prompts</span></label>
    <span class="cz-count"></span>
    <button class="btn solid" data-cz="done">I recited this level</button>
  </div>
</div>'''


def rng(gs):
    """describe a run of sentences by their local numbers"""
    ns = sorted(loc(g) for g in gs)
    return f"sentence {ns[0]}" if len(ns) == 1 else f"sentences {ns[0]} to {ns[-1]}"


def grange(p, a, b):
    return list(range(G(p, a), G(p, b) + 1))


def scene_options(p, prefix=""):
    return [(f"{prefix}Scene: {name} ({a}–{b})" if a != b else f"{prefix}Scene: {name} ({a})", grange(p, a, b)) for a, b, name in PBY[p]["scenes"]]


def whole(p):
    return grange(p, 1, PBY[p]["len"])


ASSET_V = ""
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%232563c9'/%3E"
           "%3Ctext x='16' y='23' font-size='20' text-anchor='middle' fill='white' font-family='Georgia,serif'%3E%C3%B1%3C/text%3E%3C/svg%3E")


def page(fname, title, body, desc="", final=False):
    nav = [("paragraph.html", "Text"), ("vocabulary.html", "Vocabulary"), ("practice.html", "Practice")]
    here = "paragraph.html" if fname.startswith("paragraph") else fname
    on_course = fname == "index.html" or fname.startswith("lesson-")
    # Without JavaScript the button is an ordinary link to the overview; app.js turns it into the menu.
    links = (f'<a href="index.html" id="menu-btn" class="menu-btn" role="button" aria-haspopup="dialog" aria-expanded="false"{" aria-current=page" if on_course else ""}>'
             'Lessons <span class="caret" aria-hidden="true">▾</span></a>'
             + "".join(f'<a href="{h}"{" aria-current=page" if h == here else ""}>{t}</a>' for h, t in nav))
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{esc(desc or 'A course for understanding, reading aloud and memorising the opening paragraphs of Cien años de soledad, starting from no Spanish.')}">
<title>{esc(title)}</title>
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="style.css?v={ASSET_V}">
</head>
<body data-page="{fname}"{" data-final" if final else ""}>
<nav class="topbar"><div class="wrap">
  <a class="home" href="index.html">Cien años <span>· chapter 1</span></a>
  <span class="navlinks">{links}</span>
</div></nav>
{body}
<footer><div class="wrap">
  <p><span class="ico">▶</span> plays the supplied audiobook recording. <b>Voice</b> uses your browser's synthesized Spanish voice, which is not the audiobook. Tap any Spanish word for its meaning.</p>
  <p>Text: Gabriel García Márquez, <i>Cien años de soledad</i>, opening paragraphs; English translation by Gregory Rabassa. Quoted for private language study. <a href="../../">haixun.github.io</a></p>
</div></footer>
<script src="data.js?v={ASSET_V}"></script>
<script src="app.js?v={ASSET_V}"></script>
</body>
</html>
'''


def lesson_file(n):
    return f"lesson-{n:02d}.html"


# ---------------------------------------------------------------- lesson pages
def build_lesson(L):
    n, p = L["n"], L["p"]
    P = PBY[p]
    kind_tag = {"lesson": "", "review": '<span class="tag">checkpoint</span>', "final": '<span class="tag">assessment</span>'}[L["kind"]]
    ch = chapter_of(p)
    parts = []
    prev = f'<a class="pn prev" href="{lesson_file(n-1)}">← Lesson {n-1}</a>' if n > 1 else '<a class="pn prev" href="index.html">← Course overview</a>'
    nxt = f'<a class="pn next" href="{lesson_file(n+1)}">Lesson {n+1} →</a>' if n < NL else '<a class="pn next" href="index.html">Course overview →</a>'
    pn = f'<div class="prevnext">{prev}{nxt}</div>'
    target_g = L["new_g"] or L["review_g"]
    is_whole = len(target_g) == P["len"]
    covers = "the whole paragraph" if is_whole else rng(target_g)
    parts.append(f'''<header class="mast"><div class="wrap">
  <nav class="crumbs" aria-label="Where you are"><a href="index.html">{esc(BOOK["title"])}</a><span class="sep">›</span><a href="index.html#chapter{ch["n"]}">{esc(ch["title"])}</a><span class="sep">›</span><a href="index.html#part{p}">Paragraph {p}</a><span class="sep">›</span><b>Lesson {n}</b></nav>
  <h1>{rich(L["title"])}</h1>
  <p class="lmeta">Lesson {n} of {NL} · {covers}{kind_tag}</p>
</div></header>
<!--SECNAV-->
<div class="wrap doc">
{pn}
<section><h2>Objectives</h2><ul class="objectives">{"".join(f"<li>{rich(o)}</li>" for o in L["objectives"])}</ul>
{rich(L["intro"])}</section>''')

    # --- text
    if L["new_g"]:
        if L.get("part"):
            s, a, b = L["part"]
            g = G(p, s)
            ids = L["chunk_ids"]
            total = len([c for c in CHUNKS if c["g"] == g])
            frag = " ".join(CHUNKS[i]["es"] for i in ids)
            lead = "… " if a > 1 else ""
            trail = " …" if b < total else ""
            note = f"Today's portion is part of sentence {s}. The recording button plays the whole sentence; the phrase buttons below play shorter pieces."
            parts.append(f'''<section><h2>Today's text</h2>
<div class="sent" data-s="{g}"><div class="sent-bar"><span class="num">{s}</span>{play_btn(f"s{g}", " Recording (whole sentence)", f"Play sentence {s} from the audiobook")}
<button class="btn rep" data-repeat="s{g}">Repeat</button>{say_btn(frag)}</div>
<div class="pair"><p class="es-text" lang="es">{lead}{wordify(frag)}{trail}</p><p class="en-text">{esc(SENT[g-1]["en"])}</p></div></div>
<p class="fine">{note}</p></section>''')
        else:
            parts.append('<section><h2>Today\'s text</h2>' + "".join(sentence_block(g) for g in L["new_g"]) + "</section>")
        parts.append('<section><h2>Phrase by phrase</h2><p class="fine">Listen to each phrase, say it, then read the close English. '
                     'A ▶ appears where the narrator pauses on both sides of the phrase, so the piece can be played cleanly from the recording.</p>'
                     + chunk_rows(L["chunk_ids"]) + "</section>")
        if L["new_words"]:
            parts.append(f'<section><h2>New words <span class="count">{len(L["new_words"])}</span></h2>'
                         '<p class="fine">Bold marks the stressed syllable. Nouns, verbs and adjectives come with an everyday example sentence, written for this course and not taken from the novel; tap it to hear the browser voice. Words from earlier lessons are not repeated here: tap any word in the text, or open the '
                         '<a href="vocabulary.html">vocabulary reference</a>.</p>' + vocab_rows(L["new_words"]) + "</section>")
        if L["new_expr"]:
            parts.append('<section><h2>Expressions</h2>' + expr_rows(L["new_expr"]) + "</section>")
    else:
        rv = L["review_g"]
        if is_whole:
            parts.append(f'<section><h2>The text for today</h2><p>The whole of paragraph {p}. {play_btn(f"all{p}", f" Play paragraph {p}", "Play the whole paragraph from the audiobook", "solid")} '
                         f'Each sentence, with translation and its own controls, is on the <a href="{P["page"]}">text page</a>.</p>' + reading_view(p) + "</section>")
        else:
            parts.append(f'<section><h2>The text for today</h2><p>{play_btn(range_target(rv), f" Play {rng(rv)}", "Play these sentences from the audiobook", "solid")}</p>'
                         + "".join(sentence_block(g) for g in rv) + "</section>")

    head = {"lesson": "Grammar and expressions", "review": "Pulling it together", "final": "The tests"}[L["kind"]]
    parts.append(f'<section><h2>{head}</h2>' + "".join(f'<h3>{rich(t)}</h3>{rich(b, n)}' for t, b in L["grammar"]) + "</section>")
    if L["pron"]:
        parts.append('<section><h2>Pronunciation</h2><p class="fine">Respellings such as <span class="rs">a-BEE-a</span> are rough guides for an English speaker, with the stressed syllable in capitals. Trust the recording over the respelling.</p>'
                     + "".join(f'<h3>{rich(t)}</h3>{rich(b, n)}' for t, b in L["pron"]) + "</section>")

    # --- read aloud routine
    what = f"paragraph {p}" if is_whole else rng(target_g)
    parts.append(f'''<section><h2>Read aloud</h2>
<p>{play_btn(range_target(target_g), f" Play {what}", "Play from the audiobook", "solid")} <span class="fine">Change the speed in the player bar that appears at the bottom.</span></p>
<ul class="checks">
<li><label class="tick"><input type="checkbox" data-check="L{n}:ra1"> <span>Listen twice at normal speed, following the Spanish with your eyes.</span></label></li>
<li><label class="tick"><input type="checkbox" data-check="L{n}:ra2"> <span>Set the speed to 0.75× and speak along with the narrator, slightly behind, like an echo.</span></label></li>
<li><label class="tick"><input type="checkbox" data-check="L{n}:ra3"> <span>Read it aloud alone, slowly, phrase by phrase. Check any doubtful word with its Voice button or dictionary link.</span></label></li>
<li><label class="tick"><input type="checkbox" data-check="L{n}:ra4"> <span>Read it aloud alone twice more at a natural pace, without stopping.</span></label></li>
</ul></section>''')

    # --- exercises
    qa = "".join(f'<details class="qa"><summary><span class="qn">{i}</span>{rich(q)}</summary><div class="ans">{rich(a)}'
                 f'<label class="tick got"><input type="checkbox" data-check="L{n}:q{i}"> <span>I got this right</span></label></div></details>'
                 for i, (q, a) in enumerate(L["exercises"], 1))
    parts.append(f'<section><h2>Check yourself</h2><p class="fine">Answer aloud or on paper first, then open the answer. '
                 f'<span class="score" data-prefix="L{n}:q" data-total="{len(L["exercises"])}"></span></p>{qa}</section>')

    # --- review
    rv_html = ""
    if L["kind"] == "lesson" and L["review_g"]:
        rv_html = '<div class="review-list">' + "".join(
            f'<details class="rv"><summary><span class="num">{loc(g)}</span>{play_btn(f"s{g}", "", f"Play sentence {loc(g)}")}<span class="rv-first" lang="es">{esc(" ".join(SENT[g-1]["es"].split()[:4]))} …</span><span class="rv-show">show text</span></summary>'
            f'<div class="pair"><p class="es-text" lang="es">{wordify(SENT[g-1]["es"])}</p><p class="en-text">{esc(SENT[g-1]["en"])}</p></div></details>' for g in L["review_g"]) + "</div>"
    parts.append(f'<section><h2>Review</h2>{rich(L["review_html"])}{rv_html}</section>')

    # --- memorise
    opts = []
    upto_local = loc(L["upto"])
    done_para = upto_local >= P["len"]
    if L["new_g"]:
        opts.append((f"This lesson: {rng(L['new_g'])}", L["new_g"]))
    elif not is_whole:
        opts.append((f"This checkpoint: {rng(L['review_g'])}", L["review_g"]))
    if 1 < upto_local and not done_para:
        opts.append((f"Everything so far: sentences 1 to {upto_local}", grange(p, 1, upto_local)))
    default = 0
    if done_para:
        if L["kind"] != "final":
            opts += scene_options(p)
        default = len(opts) if L["kind"] == "final" else 0
        opts.append((f"The whole of paragraph {p}", whole(p)))
        if p > 1 and L["kind"] == "final":
            opts.append(("Both paragraphs", [g for q in range(1, p + 1) for g in whole(q)]))
    parts.append(f'<section><h2>Memorise</h2>{rich(L["memo"])}{cloze(opts, default)}</section>')

    parts.append(f'''<section class="finish"><button class="btn solid big" data-done="{n}">Mark lesson {n} complete</button>
<p class="fine">Progress is saved in this browser only.</p></section>
{pn}
</div>''')
    return page(lesson_file(n), f"Lesson {n}: {re.sub('<[^>]+>', '', L['title'])} · {TITLE}", section_nav("\n".join(parts)), final=L["kind"] == "final")


SECTION_IDS = [("Objectives", "objectives", "Objectives"), ("Today's text", "text", "Text"), ("The text for today", "text", "Text"),
               ("Phrase by phrase", "phrases", "Phrases"), ("New words", "words", "Words"), ("Expressions", "expressions", "Expressions"),
               ("Grammar and expressions", "grammar", "Grammar"), ("Pulling it together", "grammar", "Summary"), ("The tests", "grammar", "Tests"),
               ("Pronunciation", "pronunciation", "Pronunciation"), ("Read aloud", "read-aloud", "Read aloud"), ("Check yourself", "check", "Check"),
               ("Review", "review", "Review"), ("Memorise", "memorise", "Memorise")]


def section_nav(body):
    """give every lesson section an id and build the row of jump links under the header"""
    chips = []

    def tag(m):
        title = re.sub("<[^>]+>.*", "", m.group(1)).strip()
        for t, sid, label in SECTION_IDS:
            if title == t:
                chips.append(f'<a href="#{sid}">{label}</a>')
                return f'<section id="{sid}"><h2>{m.group(1)}</h2>'
        return m.group(0)
    body = re.sub(r"<section><h2>(.*?)</h2>", tag, body)
    return body.replace("<!--SECNAV-->", '<nav class="secnav" aria-label="Sections of this lesson"><div class="wrap">' + "".join(chips) + "</div></nav>")


def chapter_of(p):
    return next(c for c in BOOK["chapters"] if p in c["paras"])


# ---------------------------------------------------------------- other pages
INDEX_GROUPS = {
    1: [("Sounds and the opening", [1, 2]), ("The village", [3, 4]), ("The gypsies", [5, 6, 7, 8, 9, 10]),
        ("The bargain", [11, 12, 13, 14]), ("The search", [15, 16, 17, 18]), ("The whole paragraph", [19, 20])],
    2: [("The telescope and the burning glass", [21, 22, 23, 24, 25]), ("The weapon of war", [26, 27, 28, 29, 30]),
        ("The instruments", [31, 32, 33, 34, 35]), ("The discovery", [36, 37]), ("The whole paragraph", [38, 39, 40])],
}
PART_BLURB = {
    1: "Paragraph 1, from <i>Muchos años después</i> to the locket with a woman's curl. Starts from zero: the sounds of Spanish, then one sentence at a time.",
    2: "Paragraph 2, from the return of the gypsies to <i>La tierra es redonda como una naranja</i>. Assumes Part 1 and moves two or three sentences at a time.",
}


def lesson_cov(L):
    gs = L["new_g"] or L["review_g"]
    return f"all {PBY[L['p']]['len']} sentences" if len(gs) == PBY[L["p"]]["len"] else rng(gs)


def build_index():
    out = []
    for ch in BOOK["chapters"]:
        out.append(f'<h2 id="chapter{ch["n"]}" class="chapter">{esc(ch["title"])}</h2>')
        for p in ch["paras"]:
            P = PBY[p]
            ns = PART_LESSONS[p]
            inner = [f'<p>{PART_BLURB[p]} <span class="fine">{P["len"]} sentences, {P["words"]} words, recording {int(P["clip"]//60)}:{int(P["clip"]%60):02d}. '
                     f'<a href="{P["page"]}">Read and hear paragraph {p}</a>.</span></p>']
            for gname, lns in INDEX_GROUPS[p]:
                items = []
                for n in lns:
                    L = LESSONS[n - 1]
                    tag = {"lesson": "", "review": '<span class="tag">checkpoint</span>', "final": '<span class="tag">assessment</span>'}[L["kind"]]
                    items.append(f'<li class="lcard" data-lesson="{n}"><a href="{lesson_file(n)}"><span class="ln">{n}</span>'
                                 f'<span class="lt">{rich(L["title"])}{tag}<small>{lesson_cov(L)}</small></span><span class="lcheck" aria-hidden="true"></span></a></li>')
                inner.append(f'<h3 class="group">{gname}</h3><ol class="lessons">{"".join(items)}</ol>')
            out.append(f'<details class="part" id="part{p}" data-part="{p}" open><summary><span class="part-t">Paragraph {p}</span>'
                       f'<span class="part-m">Lessons {ns[0]} to {ns[-1]}</span><span class="part-p" data-count="{len(ns)}"></span></summary>'
                       f'<div class="part-body">{"".join(inner)}</div></details>')
    total_words = sum(P["words"] for P in PARAS)
    body = f'''<header class="mast"><div class="wrap">
  <p class="kicker">A {NL}-lesson Spanish course · from zero</p>
  <h1>The opening of <i>Cien años de soledad</i></h1>
  <p class="lede">Understand it, read it aloud, and know it by heart. The course teaches exactly the Spanish these two paragraphs need:
  {total_words} words in {len(SENT)} sentences, {len(VOCAB)} different word forms, taught in English, with the audiobook narrator as your model.</p>
</div></header>
<div class="wrap doc">
<section class="progress-panel"><div class="pbar"><div class="pfill"></div></div>
  <p><span class="ptext">0 of {NL} lessons complete</span> <a class="btn solid" id="continue" href="lesson-01.html">Start lesson 1</a></p></section>

<section><h2>What you will be able to do</h2>
<ol><li><b>Understand</b> every sentence: each word, each expression, and how the grammar holds it together.</li>
<li><b>Read aloud</b> both paragraphs with sound pronunciation and rhythm.</li>
<li><b>Recite</b> them from memory, knowing what you are saying.</li></ol></section>

<section><h2>How a lesson works</h2>
<p>Each lesson takes 30 to 45 minutes and has the same parts: objectives, a portion of the text with audio, a phrase-by-phrase breakdown, new words,
grammar, pronunciation, a read-aloud routine, questions with answers, a review of earlier sentences, and a memorisation exercise with a practice box that hides more words as you improve.
One lesson a day is a good pace; the checkpoints consolidate before you move on. Each paragraph ends with an assessment of all three goals.
The <b>Lessons</b> menu at the top of every page takes you to any lesson; inside a lesson, the row of links under the title jumps between its sections.</p>
<ul><li><span class="ico">▶</span> buttons play the <b>audiobook recording</b> you supplied, cut to the sentence or phrase. You can slow it down and repeat it.</li>
<li><b>Voice</b> buttons use your browser's <b>synthesized</b> Spanish voice. It is useful for single words and phrases, but it is not the audiobook and is less natural.</li>
<li>Tap any Spanish word, anywhere, to see its meaning, grammar, syllables and a dictionary link.</li></ul></section>

<section class="parts"><p class="fine book-line">{esc(BOOK["title"])}</p>{"".join(out)}</section>

<section><h2>Always available</h2>
<ul class="cards">
<li class="card"><h3><a href="paragraph.html">The text</a></h3><p>Both paragraphs, sentence by sentence with the English beside the Spanish, the recording for a whole paragraph or any single sentence, slow playback and repeat.
<a href="paragraph.html">Paragraph 1</a> · <a href="paragraph-2.html">Paragraph 2</a></p></li>
<li class="card"><h3><a href="vocabulary.html">Vocabulary reference</a></h3><p>All {len(VOCAB)} word forms and {len(EXPR)} expressions: base form, meaning here, grammar, syllables and stress, and a link to hear it.</p></li>
<li class="card"><h3><a href="practice.html">Memorisation practice</a></h3><p>Hide one word in four, then half, then show first letters only, then nothing. Any sentence, any scene, a whole paragraph, or both.</p></li>
</ul></section>

<section><p class="fine"><button class="btn" id="reset-progress">Reset my progress on this device</button></p></section>
</div>'''
    return page("index.html", TITLE, body)


def build_paragraph(P):
    p = P["n"]
    st = P["stats"]
    gs = whole(p)
    switch = " · ".join(f'<b>Paragraph {Q["n"]}</b>' if Q["n"] == p else f'<a href="{Q["page"]}">Paragraph {Q["n"]}</a>' for Q in PARAS)
    mm, ss = int(P["clip"] // 60), int(P["clip"] % 60)
    npause = P["len"] - 1
    body = f'''<header class="mast"><div class="wrap">
  <p class="kicker">The text · {switch}</p>
  <h1>Cien años de soledad, paragraph {p}</h1>
  <p class="lede">{P["len"]} sentences. The Spanish is exactly as supplied; the English is Gregory Rabassa's published translation, which is freer than the phrase-by-phrase glosses in the lessons.</p>
</div></header>
<div class="wrap doc">
<section class="controls">
  {play_btn(f"all{p}", f" Play paragraph {p}", "Play the whole paragraph from the audiobook", "solid big")}
  <label class="tick"><input type="checkbox" id="toggle-en" checked> <span>Show English</span></label>
  <span class="fine">Recording length {mm}:{ss:02d}. The speed and repeat controls are in the player bar at the bottom while audio plays.</span>
</section>
<section id="sentences">{"".join(sentence_block(g) for g in gs)}</section>

<section><h2>Reading view</h2><p class="fine">The paragraph as continuous text. Tap any word to look it up; the sentence being played is highlighted.</p>
{reading_view(p)}</section>

<section id="about-audio"><h2>About the audio</h2>
<p><b>Source.</b> The audio is {P["source_note"]} of the supplied recording of chapter 1 (<code>CienAnos-01.mp3</code>), {mm} minutes {ss} seconds, re-encoded as one short clip. Nothing in it is synthesized.</p>
<p><b>How the sentence boundaries were found.</b> The recording was transcribed by a speech-recognition model with word-level timestamps, and the transcript was aligned word by word with the supplied text
({P["words"]} words; the recogniser misheard or dropped a word or name at {st["mismatches"]} places). Each sentence boundary was then moved to the silence the narrator leaves between sentences,
measured directly from the audio signal: the shortest of the {npause} pauses is {st["min_pause"]:.2f} seconds, so every cut falls in silence, not inside a word.
Finally each cut sentence was transcribed again on its own and compared with the text; all {P["len"]} begin and end on the right words.</p>
<p><b>Phrase-level playback.</b> Inside sentences, a phrase gets a ▶ button only where the narrator pauses for at least 0.15 seconds on both sides of it ({P["chunk_audio"]} of {P["chunk_n"]} phrases).
The other phrases run straight into their neighbours and cannot be cut cleanly, so they offer the browser voice only.</p>
<p><b>Limits.</b> The boundaries were measured by software and checked by re-transcription, not by a human listener; a breath or the tail of a consonant may occasionally be clipped by a few hundredths of a second.
Slow playback is done by your browser, which keeps the pitch but can sound slightly grainy below 0.75×.</p>
<p><b>The Voice buttons</b> use your device's built-in Spanish text-to-speech. They are clearly a different, synthetic voice and are offered only as a convenience for single words and phrases. If your device has no Spanish voice installed, they do nothing and a notice appears.</p>
</section>
</div>'''
    return page(P["page"], f"Paragraph {p} · {TITLE}", body)


def sref(g):
    s = SENT[g - 1]
    return f'<a class="sref" href="{PBY[s["p"]]["page"]}#s{s["n"]}" title="Paragraph {s["p"]}, sentence {s["n"]}">{s["p"]}.{s["n"]}</a>'


def build_vocab():
    keys = sorted(VOCAB, key=lambda k: (fold(k), k))

    def attrs(d, text):
        ps = sorted({para_of(g) for g in d["s"]})
        return f'data-f="{esc(fold(text))}" data-s=",{",".join(map(str, d["s"]))}," data-p=",{",".join(map(str, ps))},"'
    rows = []
    for k in keys:
        v = VOCAB[k]
        base = "" if v["b"] == v["f"] else f'<i lang="es">{esc(v["b"])}</i>'
        sn = f'<div class="sn">{esc("; ".join(v["sn"]))}</div>' if v["sn"] else ""
        rows.append(f'<tr id="w-{esc(k)}" {attrs(v, k + " " + v["b"] + " " + v["m"])}>'
                    f'<td><span class="head" lang="es">{esc(v["f"])}</span><div class="syl" lang="es">{v["syl"]}</div>{sn}</td>'
                    f'<td>{base}</td><td>{esc(v["m"])}{ex_html(v)}</td><td class="gram">{esc(v["g"])}</td><td class="srefs">{" ".join(sref(g) for g in v["s"])}</td>'
                    f'<td class="ctl">{say_btn(SAY.get(k, v["f"]))}{link_html(v, True)}</td></tr>')
    xrows = []
    for j, e in enumerate(EXPR):
        link = f'<a class="ext" href="{esc(e["u"])}" target="_blank" rel="noopener">SpanishDict ↗</a>' if e.get("u") else ""
        xrows.append(f'<tr id="x{j}" {attrs(e, e["f"] + " " + e["b"] + " " + e["m"])}>'
                     f'<td><span class="head" lang="es">{esc(e["f"])}</span></td><td><i lang="es">{esc(e["b"])}</i></td><td>{esc(e["m"])}</td>'
                     f'<td class="gram">{esc(e["g"])}</td><td class="srefs">{" ".join(sref(g) for g in e["s"])}</td><td class="ctl">{say_btn(e["f"])}{link}</td></tr>')
    sopts = "".join(f'<option value="p{P["n"]}">Paragraph {P["n"]}</option>' for P in PARAS)
    for P in PARAS:
        sopts += f'<optgroup label="Paragraph {P["n"]}">' + "".join(
            f'<option value="{G(P["n"], i)}">{P["n"]}.{i} · sentence {i}</option>' for i in range(1, P["len"] + 1)) + "</optgroup>"
    n_form = sum(1 for v in VOCAB.values() if v.get("uk") == "form")
    n_base = sum(1 for v in VOCAB.values() if v.get("uk") == "base")
    n_entry = sum(1 for v in VOCAB.values() if v.get("uk") == "entry")
    body = f'''<header class="mast"><div class="wrap">
  <p class="kicker">Reference</p>
  <h1>Vocabulary</h1>
  <p class="lede">Every one of the {len(VOCAB)} word forms in the two paragraphs, exactly as it appears, plus {len(EXPR)} expressions and constructions.</p>
</div></header>
<div class="wrap doc wide">
<section class="controls sticky">
  <input type="search" id="vq" placeholder="Search Spanish or English" aria-label="Search the vocabulary">
  <select id="vs" aria-label="Filter by paragraph or sentence"><option value="">Both paragraphs</option>{sopts}</select>
  <span class="fine" id="vcount"></span>
</section>
<section><p class="fine"><b>Reading the table.</b> Under each word are its syllables, with the stressed one in bold, and any letters that do not sound the way an English speaker expects.
The numbers are where the word occurs: <b>2.14</b> is paragraph 2, sentence 14. <b>Voice</b> is your browser's synthesized voice.
The <b>SpanishDict</b> link opens that word's pronunciation page, with recordings by Latin American and Spanish speakers.
SpanishDict has a pronunciation page for {n_form} of the forms exactly as they appear. For {n_base} others (conjugated verbs, plurals, feminine forms) its page pronounces the base form, and the link says so;
use the Voice button or the recording for the exact form. For {n_entry} names and rarer words the link opens the SpanishDict entry, which has a speaker button.
Every link was fetched and checked when the site was built.</p></section>
<section><h2>Words</h2><div class="tablewrap"><table class="vocab full" id="vt"><thead><tr><th>Word</th><th>Base form</th><th>Meaning here</th><th>Grammar</th><th>Where</th><th>Hear</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></div></section>
<section><h2 id="expressions">Expressions and constructions</h2><div class="tablewrap"><table class="vocab full" id="xt"><thead><tr><th>As it appears</th><th>Pattern</th><th>Meaning here</th><th>How it works</th><th>Where</th><th>Hear</th></tr></thead>
<tbody>{"".join(xrows)}</tbody></table></div></section>
</div>'''
    return page("vocabulary.html", f"Vocabulary · {TITLE}", body)


def build_practice():
    opts = []
    for P in PARAS:
        p = P["n"]
        opts.append((f"Paragraph {p}: the whole paragraph", whole(p)))
        opts += scene_options(p, f"Paragraph {p} · ")
    opts.append(("Both paragraphs", [g for P in PARAS for g in whole(P["n"])]))
    for P in PARAS:
        for i in range(1, P["len"] + 1):
            opts.append((f"Paragraph {P['n']} · sentence {i}", [G(P["n"], i)]))
    hear = ""
    for P in PARAS:
        p = P["n"]
        hear += (f'<p>{play_btn(f"all{p}", f" Paragraph {p}", "Play the whole paragraph from the audiobook", "solid")} '
                 + "".join(play_btn(range_target(grange(p, a, b)), f" {name}", f"Play the scene: {name}") for a, b, name in P["scenes"]) + "</p>")
    body = f'''<header class="mast"><div class="wrap">
  <p class="kicker">Memorisation</p>
  <h1>Practice from memory</h1>
  <p class="lede">Choose a stretch of text and a level. Say the text aloud; tap a blank only when you are stuck. When you get through a level cleanly, record it and move up.</p>
</div></header>
<div class="wrap doc">
<section><ul class="levels-key"><li><b>0</b> full text</li><li><b>1</b> one word in four hidden</li><li><b>2</b> half hidden</li><li><b>3</b> three in four hidden</li><li><b>4</b> first letters only</li><li><b>5</b> everything hidden</li></ul>
{cloze(opts, 1)}</section>
<section><h2>Your record</h2><p class="fine">Highest level you have recorded for each scene and for each whole paragraph, saved in this browser.</p><div id="practice-record"></div></section>
<section><h2>Hear it first</h2>{hear}</section>
</div>'''
    return page("practice.html", f"Practice · {TITLE}", body)


def build_data():
    data = dict(
        sent=[dict(es=s["es"], en=s["en"], t=s["t"], p=s["p"], n=s["n"]) for s in SENT],
        chunks=[dict(s=c["g"], t=c["t"]) for c in CHUNKS],
        paras=[dict(n=P["n"], clip=P["clip"], audio=f"audio/para{P['n']}", first=P["off"] + 1, last=P["off"] + P["len"]) for P in PARAS],
        vocab={k: {x: v[x] for x in ("f", "b", "g", "m", "syl", "sn", "s", "u", "uk", "ub", "x") if x in v} for k, v in VOCAB.items()},
        say=SAY,
        scenes=[dict(a=G(P["n"], a), b=G(P["n"], b), name=n, p=P["n"]) for P in PARAS for a, b, n in P["scenes"]],
        lessons=NL,
        nav=dict(book=BOOK["title"], chapters=[dict(n=ch["n"], title=ch["title"], paras=[dict(
            n=p, page=PBY[p]["page"], first=PART_LESSONS[p][0], last=PART_LESSONS[p][-1],
            groups=[dict(name=g, lessons=[dict(n=n, t=re.sub("<[^>]+>", "", LESSONS[n - 1]["title"]), k=LESSONS[n - 1]["kind"], c=lesson_cov(LESSONS[n - 1])) for n in lns])
                    for g, lns in INDEX_GROUPS[p]]) for p in ch["paras"]]) for ch in BOOK["chapters"]]),
    )
    return "window.CA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"


def main():
    global ASSET_V
    h = hashlib.sha1()
    for f in ("style.css", "app.js"):
        h.update((HERE / f).read_bytes())
    data = build_data()
    h.update(data.encode())
    ASSET_V = h.hexdigest()[:8]
    (HERE / "data.js").write_text(data, encoding="utf-8")
    out = {"index.html": build_index(), "vocabulary.html": build_vocab(), "practice.html": build_practice()}
    for P in PARAS:
        out[P["page"]] = build_paragraph(P)
    for L in LESSONS:
        out[lesson_file(L["n"])] = build_lesson(L)
    for name, text in out.items():
        (HERE / name).write_text(text, encoding="utf-8")
    print(f"built {len(out)} pages; {len(SENT)} sentences, {sum(P['words'] for P in PARAS)} words, {len(VOCAB)} forms, {len(EXPR)} expressions, "
          f"{sum(1 for v in VOCAB.values() if v.get('u'))} word links, {sum(1 for e in EXPR if e.get('u'))} expression links")
    for P in PARAS:
        print(f"  paragraph {P['n']}: {P['len']} sentences, {P['words']} words, clip {P['clip']} s, {P['chunk_audio']}/{P['chunk_n']} phrases with audio, stats {P['stats']}")
    nolink = [k for k, v in VOCAB.items() if not v.get("u")] + [e["f"] for e in EXPR if not e.get("u")]
    if nolink:
        print(f"  WITHOUT a pronunciation link ({len(nolink)}): run the link checker.  e.g. {nolink[:8]}")


if __name__ == "__main__":
    main()
