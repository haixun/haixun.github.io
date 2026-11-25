#!/usr/bin/env python3
"""Build the static course site for paragraph 1 of "Cien años de soledad".

    python3 build.py

Reads everything under content/ and writes index.html, lesson-01.html ... lesson-20.html,
paragraph.html, vocabulary.html, practice.html and data.js next to this file.
Standard library only.  Edit the files in content/, never the generated HTML.

content/para1.txt      the supplied paragraph: Spanish, a line with "-", then the English translation
content/chunks.txt     phrase-by-phrase breakdown with literal glosses
content/vocab.txt      vocabulary and expressions
content/lessons_a.py   lessons 1-10
content/lessons_b.py   lessons 11-20
content/timings.json   sentence / phrase time ranges inside audio/para1.m4a (measured, see paragraph.html)
content/links.json     verified pronunciation links (written by the link checker)
"""
import hashlib, html, json, re, sys, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
C = HERE / "content"
sys.dont_write_bytecode = True
sys.path.insert(0, str(C))
from lessons_a import LESSONS_A  # noqa: E402
from lessons_b import LESSONS_B  # noqa: E402

LESSONS = LESSONS_A + LESSONS_B
assert len(LESSONS) == 20
SCENES = [(1, 1, "The memory"), (2, 3, "The village"), (4, 8, "The gypsies"),
          (9, 13, "The bargain"), (14, 17, "The search")]
TITLE = "Cien años de soledad: the first paragraph"
esc = html.escape


# ---------------------------------------------------------------- text
def load_para():
    raw = (C / "para1.txt").read_text(encoding="utf-8")
    es, en = re.split(r"\n-\n", raw)
    es, en = " ".join(es.split()), " ".join(en.split())
    S = re.split(r"(?<=[.»])\s+(?=[«A-ZÁÉÍÓÚÑ])", es)
    E = re.split(r"(?<=[.”])\s+(?=[“A-ZÁÉÍÓÚ])", en)
    E[7:9] = [E[7] + " " + E[8]]          # the English splits Melquíades' speech in two
    assert len(S) == 17 and len(E) == 17, (len(S), len(E))
    return S, E


WORD_RE = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+")


def words(s):
    return WORD_RE.findall(s)


def fold(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


S, E = load_para()

# ---------------------------------------------------------------- chunks
CHUNKS = []   # dict(s=sentence index, es, en)
cur = None
for line in (C / "chunks.txt").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    m = re.match(r"# S(\d+)$", line)
    if m:
        cur = int(m.group(1)) - 1
        continue
    if not line or line.startswith("#"):
        continue
    a, b = [x.strip() for x in line.split("|")]
    CHUNKS.append(dict(s=cur, es=a, en=b))
for i, s in enumerate(S):
    joined = " ".join(c["es"] for c in CHUNKS if c["s"] == i)
    assert joined == s, f"chunks of sentence {i+1} do not reproduce the source text:\n{joined}\n{s}"

T = json.loads((C / "timings.json").read_text())
assert len(T["sentences"]) == 17 and len(T["chunks"]) == len(CHUNKS)
for c, t in zip(CHUNKS, T["chunks"]):
    c["t"] = t
CLIP_LEN = round(T["clip"][1] - T["clip"][0], 2)

# ---------------------------------------------------------------- vocabulary
VOCAB, EXPR = {}, []
for line in (C / "vocab.txt").read_text(encoding="utf-8").splitlines():
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
        assert f[0] not in VOCAB, f[0]
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


for i, s in enumerate(S):
    for w in words(s):
        k = key_of(w)
        VOCAB[k].setdefault("s", [])
        if i + 1 not in VOCAB[k]["s"]:
            VOCAB[k]["s"].append(i + 1)
unused = [k for k, v in VOCAB.items() if "s" not in v]
assert not unused, f"vocabulary entries that never occur: {unused}"
SENT_TOKENS = [[w.lower() for w in words(s)] for s in S]
for e in EXPR:
    toks = [w.lower() for w in words(e["f"])]
    e["s"] = [i + 1 for i, st in enumerate(SENT_TOKENS)
              if any(st[j:j + len(toks)] == toks for j in range(len(st) - len(toks) + 1))]
    assert e["s"], f"expression not found in the paragraph: {e['f']}"

# ---------------------------------------------------------------- syllables and sound notes
STRONG, WEAK, ACCW = set("aeoáéó"), set("iuü"), set("íú")
VOWELS = STRONG | WEAK | ACCW


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
    nuclei, j = [], 0            # (start, end) unit ranges of vowel nuclei
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
    bounds = [0]                 # unit index where each syllable starts
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


def syl_html(word):
    if word == "XV":
        return "<b>quin</b>·ce"
    syl, st = syllables(word)
    return "·".join(f"<b>{esc(s)}</b>" if i == st and len(syl) > 1 else esc(s) for i, s in enumerate(syl))


def sound_notes(word):
    w = word.lower()
    if word == "XV":
        return ["read as the number quince: qu = k; c = s (Latin America) or th (Spain)"]
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
    return n


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

# ---------------------------------------------------------------- lesson bookkeeping
for n, L in enumerate(LESSONS, 1):
    L["n"] = n
    if L.get("part"):
        s, a, b = L["part"]
        ids = [i for i, c in enumerate(CHUNKS) if c["s"] == s - 1][a - 1:b]
    else:
        ids = [i for i, c in enumerate(CHUNKS) if c["s"] + 1 in L["new"]]
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
    L["upto"] = max([c["s"] + 1 for c in CHUNKS[:max(L["chunk_ids"]) + 1]] if L["chunk_ids"] else L["review"])
assert seen_words == set(VOCAB), set(VOCAB) - seen_words
assert len(seen_expr) == len(EXPR), [EXPR[j]["f"] for j in range(len(EXPR)) if j not in seen_expr]


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


def sentence_block(i, show_num=True):
    """i is 0-based"""
    return f'''<div class="sent" id="s{i+1}" data-s="{i+1}">
  <div class="sent-bar"><span class="num">{i+1}</span>{play_btn(f"s{i+1}", " Recording", f"Play sentence {i+1} from the audiobook")}
    <button class="btn rep" data-repeat="s{i+1}" title="Repeat this sentence until stopped">Repeat</button>{say_btn(S[i])}</div>
  <div class="pair"><p class="es-text" lang="es">{wordify(S[i])}</p><p class="en-text">{esc(E[i])}</p></div>
</div>'''


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
        base = "" if v["b"] == v["f"] else f'<div class="base">from <i lang="es">{esc(v["b"])}</i></div>'
        rows.append(f'<tr><td><span class="w head" data-k="{esc(k)}" lang="es">{esc(v["f"])}</span><div class="syl" lang="es">{v["syl"]}</div></td>'
                    f'<td>{esc(v["m"])}{base}</td><td class="gram">{rich(esc(v["g"]))}</td>'
                    f'<td class="ctl">{say_btn(v["f"] if k != "XV" else "quince")}{link_html(v, True)}</td></tr>')
    return ('<div class="tablewrap"><table class="vocab"><thead><tr><th>Word</th><th>Meaning here</th><th>Grammar</th><th>Hear</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def expr_rows(idxs):
    rows = []
    for j in idxs:
        e = EXPR[j]
        link = f'<a class="ext" href="{esc(e["u"])}" target="_blank" rel="noopener">SpanishDict ↗</a>' if e.get("u") else ""
        pat = "" if fold(e["b"]) == fold(e["f"]) else f'<div class="base">pattern: <i lang="es">{esc(e["b"])}</i></div>'
        rows.append(f'<tr id="x{j}"><td class="es-text" lang="es">{wordify(e["f"])}{pat}</td><td>{esc(e["m"])}</td>'
                    f'<td class="gram">{esc(e["g"])}</td><td class="ctl">{say_btn(e["f"])}{link}</td></tr>')
    return ('<div class="tablewrap"><table class="vocab"><thead><tr><th>Expression</th><th>Meaning here</th><th>How it works</th><th>Hear</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def cloze(options, default=0, idp="cz"):
    """options: list of (label, [sentence numbers])"""
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


def rng(nums):
    nums = sorted(nums)
    return f"sentence {nums[0]}" if len(nums) == 1 else f"sentences {nums[0]} to {nums[-1]}"


ASSET_V = ""


def page(fname, title, body, crumb="", desc=""):
    nav = [("index.html", "Course"), ("paragraph.html", "Paragraph"), ("vocabulary.html", "Vocabulary"), ("practice.html", "Practice")]
    links = "".join(f'<a href="{h}"{" aria-current=page" if h == fname else ""}>{t}</a>' for h, t in nav)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{esc(desc or 'A 20-lesson course for understanding, reading aloud and memorising the first paragraph of Cien años de soledad, starting from no Spanish.')}">
<title>{esc(title)}</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%232563c9'/%3E%3Ctext x='16' y='23' font-size='20' text-anchor='middle' fill='white' font-family='Georgia,serif'%3E%C3%B1%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="style.css?v={ASSET_V}">
</head>
<body data-page="{fname}">
<nav class="topbar"><div class="wrap">
  <a class="home" href="index.html">Cien años <span>· paragraph 1</span></a>
  <span class="navlinks">{links}</span>
</div></nav>
{body}
<footer><div class="wrap">
  <p><span class="ico">▶</span> plays the supplied audiobook recording. <b>Voice</b> uses your browser's synthesized Spanish voice, which is not the audiobook. Tap any Spanish word for its meaning.</p>
  <p>Text: Gabriel García Márquez, <i>Cien años de soledad</i>, opening paragraph; English translation by Gregory Rabassa. Quoted for private language study. <a href="../../">haixun.github.io</a></p>
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
    n = L["n"]
    kind_label = {"lesson": "Lesson", "review": "Checkpoint", "final": "Assessment"}[L["kind"]]
    parts = []
    prev = f'<a class="pn prev" href="{lesson_file(n-1)}">← Lesson {n-1}</a>' if n > 1 else '<a class="pn prev" href="index.html">← Course overview</a>'
    nxt = f'<a class="pn next" href="{lesson_file(n+1)}">Lesson {n+1} →</a>' if n < 20 else '<a class="pn next" href="index.html">Course overview →</a>'
    pn = f'<div class="prevnext">{prev}{nxt}</div>'
    covers = rng(L["new"]) if L["new"] else rng(L["review"])
    parts.append(f'''<header class="mast"><div class="wrap">
  <p class="kicker">Lesson {n} of 20 · {kind_label} · {covers}</p>
  <h1>{rich(L["title"])}</h1>
</div></header>
<div class="wrap doc">
{pn}
<section><h2>Objectives</h2><ul class="objectives">{"".join(f"<li>{rich(o)}</li>" for o in L["objectives"])}</ul>
{rich(L["intro"])}</section>''')

    # --- text
    if L["new"]:
        sents = L["new"]
        if L.get("part"):
            s, a, b = L["part"]
            ids = L["chunk_ids"]
            total = len([c for c in CHUNKS if c["s"] == s - 1])
            frag = " ".join(CHUNKS[i]["es"] for i in ids)
            lead = "… " if a > 1 else ""
            trail = " …" if b < total else ""
            note = f"Today's portion is part of sentence {s}. The recording button plays the whole sentence; the phrase buttons below play shorter pieces."
            parts.append(f'''<section><h2>Today's text</h2>
<div class="sent" data-s="{s}"><div class="sent-bar"><span class="num">{s}</span>{play_btn(f"s{s}", " Recording (whole sentence)", f"Play sentence {s} from the audiobook")}
<button class="btn rep" data-repeat="s{s}">Repeat</button>{say_btn(frag)}</div>
<div class="pair"><p class="es-text" lang="es">{lead}{wordify(frag)}{trail}</p><p class="en-text">{esc(E[s-1])}</p></div></div>
<p class="fine">{note}</p></section>''')
        else:
            parts.append('<section><h2>Today\'s text</h2>' + "".join(sentence_block(i - 1) for i in sents) + "</section>")
        parts.append('<section><h2>Phrase by phrase</h2><p class="fine">Listen to each phrase, say it, then read the close English. '
                     'A ▶ appears where the narrator pauses on both sides of the phrase, so the piece can be played cleanly from the recording.</p>'
                     + chunk_rows(L["chunk_ids"]) + "</section>")
        if L["new_words"]:
            parts.append(f'<section><h2>New words <span class="count">{len(L["new_words"])}</span></h2>'
                         '<p class="fine">Bold marks the stressed syllable. Words from earlier lessons are not repeated here: tap any word in the text, or open the '
                         '<a href="vocabulary.html">vocabulary reference</a>.</p>' + vocab_rows(L["new_words"]) + "</section>")
        if L["new_expr"]:
            parts.append('<section><h2>Expressions</h2>' + expr_rows(L["new_expr"]) + "</section>")
    else:
        rv = L["review"]
        if len(rv) <= 6:
            parts.append(f'<section><h2>The text for today</h2><p>{play_btn(f"r{rv[0]}-{rv[-1]}", f" Play {rng(rv)}", "Play these sentences from the audiobook", "solid")}</p>'
                         + "".join(sentence_block(i - 1) for i in rv) + "</section>")
        else:
            parts.append(f'<section><h2>The text for today</h2><p>The whole paragraph. {play_btn("all", " Play the whole paragraph", "Play the whole paragraph from the audiobook", "solid")} '
                         'Each sentence, with translation and its own controls, is on the <a href="paragraph.html">paragraph page</a>.</p>'
                         '<div class="reading" lang="es">' + " ".join(f'<span class="rs-sent" data-s="{i+1}">{wordify(S[i])}</span>' for i in range(17)) + "</div></section>")

    head = {"lesson": "Grammar and expressions", "review": "Pulling it together", "final": "The three tests"}[L["kind"]]
    parts.append(f'<section><h2>{head}</h2>' + "".join(f'<h3>{rich(t)}</h3>{rich(b, n)}' for t, b in L["grammar"]) + "</section>")
    if L["pron"]:
        parts.append('<section><h2>Pronunciation</h2><p class="fine">Respellings such as <span class="rs">a-BEE-a</span> are rough guides for an English speaker, with the stressed syllable in capitals. Trust the recording over the respelling.</p>'
                     + "".join(f'<h3>{rich(t)}</h3>{rich(b, n)}' for t, b in L["pron"]) + "</section>")

    # --- read aloud routine
    tgt = L["new"] or L["review"]
    whole = len(tgt) > 6
    ptarget = "all" if whole else (f"s{tgt[0]}" if len(tgt) == 1 else f"r{tgt[0]}-{tgt[-1]}")
    what = "the whole paragraph" if whole else rng(tgt)
    parts.append(f'''<section><h2>Read aloud</h2>
<p>{play_btn(ptarget, f" Play {what}", "Play from the audiobook", "solid")} <span class="fine">Change the speed in the player bar that appears at the bottom.</span></p>
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
    rv = [r for r in L["review"]] if L["kind"] == "lesson" else []
    rv_html = ""
    if rv:
        rv_html = '<div class="review-list">' + "".join(
            f'<details class="rv"><summary><span class="num">{r}</span>{play_btn(f"s{r}", "", f"Play sentence {r}")}<span class="rv-first" lang="es">{esc(" ".join(S[r-1].split()[:4]))} …</span><span class="rv-show">show text</span></summary>'
            f'<div class="pair"><p class="es-text" lang="es">{wordify(S[r-1])}</p><p class="en-text">{esc(E[r-1])}</p></div></details>' for r in rv) + "</div>"
    parts.append(f'<section><h2>Review</h2>{rich(L["review_html"])}{rv_html}</section>')

    # --- memorise
    opts = []
    if L["new"]:
        opts.append((f"This lesson: {rng(L['new'])}", L["new"]))
    elif len(L["review"]) < 17:
        opts.append((f"This checkpoint: {rng(L['review'])}", L["review"]))
    if L["upto"] > 1 and L["upto"] < 17:
        opts.append((f"Everything so far: sentences 1 to {L['upto']}", list(range(1, L["upto"] + 1))))
    if L["upto"] >= 17:
        if L["kind"] != "final":
            for a, b, name in SCENES:
                opts.append((f"Scene: {name} ({a}–{b})" if a != b else f"Scene: {name} ({a})", list(range(a, b + 1))))
        opts.append(("The whole paragraph", list(range(1, 18))))
    default = len(opts) - 1 if L["kind"] == "final" else 0
    parts.append(f'<section><h2>Memorise</h2>{rich(L["memo"])}{cloze(opts, default)}</section>')

    parts.append(f'''<section class="finish"><button class="btn solid big" data-done="{n}">Mark lesson {n} complete</button>
<p class="fine">Progress is saved in this browser only.</p></section>
{pn}
</div>''')
    return page(lesson_file(n), f"Lesson {n}: {re.sub('<[^>]+>', '', L['title'])} · {TITLE}", "\n".join(parts))


for L in LESSONS:       # the lesson dicts use "review" for the sentence list and "review"/"memo" html
    pass


# ---------------------------------------------------------------- other pages
def build_index():
    cards = []
    for a, b, name in SCENES + []:
        pass
    groups = [("Sounds and the opening", [1, 2]), ("The village", [3, 4]), ("The gypsies", [5, 6, 7, 8, 9, 10]),
              ("The bargain", [11, 12, 13, 14]), ("The search", [15, 16, 17, 18]), ("The whole paragraph", [19, 20])]
    out = []
    for g, ns in groups:
        items = []
        for n in ns:
            L = LESSONS[n - 1]
            cov = rng(L["new"]) if L["new"] else ("all 17 sentences" if len(L["review"]) == 17 else rng(L["review"]))
            tag = {"lesson": "", "review": '<span class="tag">checkpoint</span>', "final": '<span class="tag">assessment</span>'}[L["kind"]]
            items.append(f'<li class="lcard" data-lesson="{n}"><a href="{lesson_file(n)}"><span class="ln">{n}</span>'
                         f'<span class="lt">{rich(L["title"])}{tag}<small>{cov}</small></span><span class="lcheck" aria-hidden="true"></span></a></li>')
        out.append(f'<h3 class="group">{g}</h3><ol class="lessons">{"".join(items)}</ol>')
    body = f'''<header class="mast"><div class="wrap">
  <p class="kicker">A 20-lesson Spanish course · from zero</p>
  <h1>The first paragraph of <i>Cien años de soledad</i></h1>
  <p class="lede">Understand it, read it aloud, and know it by heart. The course teaches exactly the Spanish this one paragraph needs:
  {sum(len(words(s)) for s in S)} words in 17 sentences, {len(VOCAB)} different word forms, taught in English, with the audiobook narrator as your model.</p>
</div></header>
<div class="wrap doc">
<section class="progress-panel"><div class="pbar"><div class="pfill"></div></div>
  <p><span class="ptext">0 of 20 lessons complete</span> <a class="btn solid" id="continue" href="lesson-01.html">Start lesson 1</a></p></section>

<section><h2>What you will be able to do</h2>
<ol><li><b>Understand</b> every sentence: each word, each expression, and how the grammar holds it together.</li>
<li><b>Read aloud</b> the whole paragraph with sound pronunciation and rhythm.</li>
<li><b>Recite</b> the whole paragraph from memory, knowing what you are saying.</li></ol></section>

<section><h2>How a lesson works</h2>
<p>Each lesson takes 30 to 45 minutes and has the same parts: objectives, a portion of the text with audio, a phrase-by-phrase breakdown, new words,
grammar, pronunciation, a read-aloud routine, questions with answers, a review of earlier sentences, and a memorisation exercise with a practice box that hides more words as you improve.
One lesson a day is a good pace; the checkpoints (lessons 6, 10, 14 and 18) consolidate before you move on.</p>
<ul><li><span class="ico">▶</span> buttons play the <b>audiobook recording</b> you supplied, cut to the sentence or phrase. You can slow it down and repeat it.</li>
<li><b>Voice</b> buttons use your browser's <b>synthesized</b> Spanish voice. It is useful for single words and phrases, but it is not the audiobook and is less natural.</li>
<li>Tap any Spanish word, anywhere, to see its meaning, grammar, syllables and a dictionary link.</li></ul></section>

<section><h2>The lessons</h2>{"".join(out)}</section>

<section><h2>Always available</h2>
<ul class="cards">
<li class="card"><h3><a href="paragraph.html">The complete paragraph</a></h3><p>All 17 sentences with the English beside them, the recording for the whole paragraph or any single sentence, slow playback and repeat.</p></li>
<li class="card"><h3><a href="vocabulary.html">Vocabulary reference</a></h3><p>Every word form and {len(EXPR)} expressions: base form, meaning here, grammar, syllables and stress, and a link to hear it.</p></li>
<li class="card"><h3><a href="practice.html">Memorisation practice</a></h3><p>Hide one word in four, then half, then show first letters only, then nothing. Any sentence, any scene, or the whole paragraph.</p></li>
</ul></section>

<section><p class="fine"><button class="btn" id="reset-progress">Reset my progress on this device</button></p></section>
</div>'''
    return page("index.html", TITLE, body)


def build_paragraph():
    body = f'''<header class="mast"><div class="wrap">
  <p class="kicker">The complete paragraph</p>
  <h1>Cien años de soledad, paragraph 1</h1>
  <p class="lede">Seventeen sentences. The Spanish is exactly as supplied; the English is Gregory Rabassa's published translation, which is freer than the phrase-by-phrase glosses in the lessons.</p>
</div></header>
<div class="wrap doc">
<section class="controls">
  {play_btn("all", " Play the whole paragraph", "Play the whole paragraph from the audiobook", "solid big")}
  <label class="tick"><input type="checkbox" id="toggle-en" checked> <span>Show English</span></label>
  <span class="fine">Recording length {int(CLIP_LEN//60)}:{int(CLIP_LEN%60):02d}. The speed and repeat controls are in the player bar at the bottom while audio plays.</span>
</section>
<section id="sentences">{"".join(sentence_block(i) for i in range(17))}</section>

<section><h2>Reading view</h2><p class="fine">The paragraph as continuous text, as it is printed. Tap a sentence's first word to look it up; the sentence being played is highlighted.</p>
<div class="reading" lang="es">{" ".join(f'<span class="rs-sent" data-s="{i+1}">{wordify(S[i])}</span>' for i in range(17))}</div></section>

<section id="about-audio"><h2>About the audio</h2>
<p><b>Source.</b> The audio is the opening {int(CLIP_LEN//60)} minutes {int(CLIP_LEN%60)} seconds of the supplied recording of chapter 1 (<code>CienAnos-01.mp3</code>), re-encoded as one short clip. Nothing in it is synthesized.</p>
<p><b>How the sentence boundaries were found.</b> The recording was transcribed by a speech-recognition model with word-level timestamps, and the transcript was aligned word by word with the supplied text
(all {sum(len(words(s)) for s in S)} words matched except six rare words and names that the recogniser misheard). Each sentence boundary was then moved to the silence the narrator leaves between sentences,
measured directly from the audio signal: the shortest of the sixteen pauses is 0.4 seconds, so every cut falls in silence, not inside a word.
Finally each cut sentence was transcribed again on its own and compared with the text; all seventeen begin and end on the right words.</p>
<p><b>Phrase-level playback.</b> Inside sentences, a phrase gets a ▶ button only where the narrator pauses for at least 0.15 seconds on both sides of it ({sum(1 for c in CHUNKS if c["t"])} of {len(CHUNKS)} phrases).
The other phrases run straight into their neighbours and cannot be cut cleanly, so they offer the browser voice only.</p>
<p><b>Limits.</b> The boundaries were measured by software and checked by re-transcription, not by a human listener; a breath or the tail of a consonant may occasionally be clipped by a few hundredths of a second.
Slow playback is done by your browser, which keeps the pitch but can sound slightly grainy below 0.75×.</p>
<p><b>The Voice buttons</b> use your device's built-in Spanish text-to-speech. They are clearly a different, synthetic voice and are offered only as a convenience for single words and phrases. If your device has no Spanish voice installed, they do nothing and a notice appears.</p>
</section>
</div>'''
    return page("paragraph.html", f"The paragraph · {TITLE}", body)


def build_vocab():
    keys = sorted(VOCAB, key=lambda k: (fold(k), k))
    rows = []
    for k in keys:
        v = VOCAB[k]
        base = "" if v["b"] == v["f"] else f'<i lang="es">{esc(v["b"])}</i>'
        sn = f'<div class="sn">{esc("; ".join(v["sn"]))}</div>' if v["sn"] else ""
        sents = " ".join(f'<a class="sref" href="paragraph.html#s{s}" title="Sentence {s}">{s}</a>' for s in v["s"])
        rows.append(f'<tr id="w-{esc(k)}" data-f="{esc(fold(k + " " + v["b"] + " " + v["m"]))}" data-s=",{",".join(map(str, v["s"]))},">'
                    f'<td><span class="head" lang="es">{esc(v["f"])}</span><div class="syl" lang="es">{v["syl"]}</div>{sn}</td>'
                    f'<td>{base}</td><td>{esc(v["m"])}</td><td class="gram">{esc(v["g"])}</td><td class="srefs">{sents}</td>'
                    f'<td class="ctl">{say_btn(v["f"] if k != "XV" else "quince")}{link_html(v, True)}</td></tr>')
    xrows = []
    for j, e in enumerate(EXPR):
        link = f'<a class="ext" href="{esc(e["u"])}" target="_blank" rel="noopener">SpanishDict ↗</a>' if e.get("u") else ""
        sents = " ".join(f'<a class="sref" href="paragraph.html#s{s}">{s}</a>' for s in e["s"])
        xrows.append(f'<tr id="x{j}" data-f="{esc(fold(e["f"] + " " + e["b"] + " " + e["m"]))}" data-s=",{",".join(map(str, e["s"]))},">'
                     f'<td><span class="head" lang="es">{esc(e["f"])}</span></td><td><i lang="es">{esc(e["b"])}</i></td><td>{esc(e["m"])}</td>'
                     f'<td class="gram">{esc(e["g"])}</td><td class="srefs">{sents}</td><td class="ctl">{say_btn(e["f"])}{link}</td></tr>')
    sopts = "".join(f'<option value="{i}">Sentence {i}</option>' for i in range(1, 18))
    n_form = sum(1 for v in VOCAB.values() if v.get("uk") == "form")
    n_base = sum(1 for v in VOCAB.values() if v.get("uk") == "base")
    n_entry = sum(1 for v in VOCAB.values() if v.get("uk") == "entry")
    body = f'''<header class="mast"><div class="wrap">
  <p class="kicker">Reference</p>
  <h1>Vocabulary</h1>
  <p class="lede">Every one of the {len(VOCAB)} word forms in the paragraph, exactly as it appears, plus {len(EXPR)} expressions and constructions.</p>
</div></header>
<div class="wrap doc wide">
<section class="controls sticky">
  <input type="search" id="vq" placeholder="Search Spanish or English" aria-label="Search the vocabulary">
  <select id="vs" aria-label="Filter by sentence"><option value="">All sentences</option>{sopts}</select>
  <span class="fine" id="vcount"></span>
</section>
<section><p class="fine"><b>Reading the table.</b> Under each word are its syllables, with the stressed one in bold, and any letters that do not sound the way an English speaker expects.
The numbers are the sentences where the word occurs. <b>Voice</b> is your browser's synthesized voice.
The <b>SpanishDict</b> link opens that word's pronunciation page, with recordings by Latin American and Spanish speakers.
SpanishDict has a pronunciation page for {n_form} of the forms exactly as they appear. For {n_base} others (conjugated verbs, plurals, feminine forms) its page pronounces the base form, and the link says so;
use the Voice button or the recording for the exact form. For {n_entry} names and rarer words the link opens the SpanishDict entry, which has a speaker button.
Every link was fetched and checked when the site was built.</p></section>
<section><h2>Words</h2><div class="tablewrap"><table class="vocab full" id="vt"><thead><tr><th>Word</th><th>Base form</th><th>Meaning here</th><th>Grammar</th><th>Sent.</th><th>Hear</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></div></section>
<section><h2 id="expressions">Expressions and constructions</h2><div class="tablewrap"><table class="vocab full" id="xt"><thead><tr><th>As it appears</th><th>Pattern</th><th>Meaning here</th><th>How it works</th><th>Sent.</th><th>Hear</th></tr></thead>
<tbody>{"".join(xrows)}</tbody></table></div></section>
</div>'''
    return page("vocabulary.html", f"Vocabulary · {TITLE}", body)


def build_practice():
    opts = [("The whole paragraph", list(range(1, 18)))]
    for a, b, name in SCENES:
        opts.append((f"Scene: {name} ({a}–{b})" if a != b else f"Scene: {name} ({a})", list(range(a, b + 1))))
    for i in range(1, 18):
        opts.append((f"Sentence {i}", [i]))
    body = f'''<header class="mast"><div class="wrap">
  <p class="kicker">Memorisation</p>
  <h1>Practice from memory</h1>
  <p class="lede">Choose a stretch of text and a level. Say the text aloud; tap a blank only when you are stuck. When you get through a level cleanly, record it and move up.</p>
</div></header>
<div class="wrap doc">
<section><ul class="levels-key"><li><b>0</b> full text</li><li><b>1</b> one word in four hidden</li><li><b>2</b> half hidden</li><li><b>3</b> three in four hidden</li><li><b>4</b> first letters only</li><li><b>5</b> everything hidden</li></ul>
{cloze(opts, 1)}</section>
<section><h2>Your record</h2><p class="fine">Highest level you have recorded for each scene and for the whole paragraph, saved in this browser.</p><div id="practice-record"></div></section>
<section><h2>Hear it first</h2><p>{play_btn("all", " Play the whole paragraph", "Play the whole paragraph from the audiobook", "solid")}
{"".join(play_btn(f"r{a}-{b}" if a != b else f"s{a}", f" {name}", f"Play the scene: {name}") for a, b, name in SCENES)}</p></section>
</div>'''
    return page("practice.html", f"Practice · {TITLE}", body)


def build_data():
    data = dict(
        sent=[dict(es=S[i], en=E[i], t=T["sentences"][i]) for i in range(17)],
        chunks=[dict(s=c["s"] + 1, t=c["t"]) for c in CHUNKS],
        vocab={k: {x: v[x] for x in ("f", "b", "g", "m", "syl", "sn", "s", "u", "uk", "ub") if x in v} for k, v in VOCAB.items()},
        lessons=[dict(n=L["n"], title=re.sub("<[^>]+>", "", L["title"])) for L in LESSONS],
        scenes=[dict(a=a, b=b, name=n) for a, b, n in SCENES],
        clip=CLIP_LEN,
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
    out = {"index.html": build_index(), "paragraph.html": build_paragraph(),
           "vocabulary.html": build_vocab(), "practice.html": build_practice()}
    for L in LESSONS:
        out[lesson_file(L["n"])] = build_lesson(L)
    for name, text in out.items():
        (HERE / name).write_text(text, encoding="utf-8")
    nw = sum(len(words(s)) for s in S)
    print(f"built {len(out)} pages; {nw} words, {len(VOCAB)} forms, {len(EXPR)} expressions, "
          f"{sum(1 for v in VOCAB.values() if v.get('u'))} word links, {sum(1 for e in EXPR if e.get('u'))} expression links")
    small = sum(1 for s in S for w in words(s) if w.lower() in
                "de a en por para con y que como el la los las un una al del se su lo".split())
    print(f"'de' occurs {sum(1 for s in S for w in words(s) if w.lower() == 'de')} times; small words {small}/{nw}")


if __name__ == "__main__":
    main()
