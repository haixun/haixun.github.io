#!/usr/bin/env python3
"""Build the /kb/ section: the enterprise-knowledge-layer catalog plus one essay.

The sources live in the private explore repository:
    <src>/catalog/entries/**.json     one file per catalog entry
    <src>/catalog/taxonomy.json       tag definitions
    <src>/landscape.md                map

    python3 build.py                        # default --src ~/explore/kb
    python3 build.py --src /path/to/kb
    python3 build.py --no-docs              # skip the essays (no network needed)

Standard library only. The two essays are rendered by GitHub's Markdown API
through the `gh` CLI, so they look exactly as they do on github.com.
Writes into this directory; style.css is hand-written and not touched.
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;'
         '0,6..72,500;0,6..72,600;1,6..72,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">')
TYPES = [("paper", "Papers", "papers.html"), ("company", "Companies", "companies.html"),
         ("product", "Products", "products.html"), ("article", "Articles", "articles.html"),
         ("benchmark", "Benchmarks", "benchmarks.html")]
TYPE_TITLE = {t: n for t, n, _ in TYPES}
TYPE_PAGE = {t: f for t, _, f in TYPES}
DIMS = ["commits", "route", "grounds", "layer", "domain", "topics"]
DIM_LABEL = {"commits": "Where meaning is committed", "route": "How structure is arrived at",
             "grounds": "What warrants the answer", "layer": "Market layer",
             "domain": "Domain", "topics": "Topics"}

DOCS = [  # (source file, output page, kicker, short title)
    ("agentic-ontology-report.md", "field-guide.html", "Guide", "Ontologies for AI Agents"),
    ("landscape.md", "landscape.html", "Map", "The Knowledge Layer"),
]
# Internal references in the essay -> (label, href or None). Matched on the path's basename.
DOC_REFS = {
    "landscape.md": ("The Knowledge Layer", "landscape.html"),
    "enterprise-business-knowledge-vish.md": ("an underlying research report (not published)", None),
    "opportunity.md": ("our internal assessment of the opportunity (not published)", None),
    "report.md": ("our complete internal report (not published)", None),
    "README.md": ("the company entries in the catalog", "companies.html"),
}
PROSE_FIXES = [
    ("one page per entry, with sources and evidence labels, in `catalog/`.",
     "one page per entry, with sources and evidence labels. [Search and filter everything](browse.html)."),
    ("from the 109 entries in the catalog and the underlying research report on enterprise business knowledge.",
     "from the entries in this catalog and an underlying research report on enterprise business knowledge."),
]


def esc(s):
    return html.escape(str(s or ""), quote=True)


NAV = {"types": {}, "themes": {}}
import hashlib
CSS_VERSION = hashlib.sha1(open(os.path.join(HERE, "style.css"), "rb").read()).hexdigest()[:8]


def sidebar(up, active):
    def item(href, label, key, count=None):
        cls = ' class="on"' if key == active else ""
        c = ' <span class="n">(%d)</span>' % count if count is not None else ""
        return '<li><a%s href="%s%s">%s%s</a></li>' % (cls, up, href, label, c)
    S = ['<aside class="side"><details class="sidebox" open><summary>Menu</summary>',
         '<a class="brand" href="%sindex.html">Knowledge Layer</a>' % up, '<ul>',
         item("index.html", "Overview", "index"), item("whats-new.html", "What&rsquo;s new", "news"),
         item("browse.html", "Browse &amp; search", "browse"), '</ul>',
         '<p class="side-h">Read</p><ul>',
         item("field-guide.html", "Field guide", "doc:field-guide.html"),
         item("landscape.html", "The Knowledge Layer", "doc:landscape.html"), '</ul>',
         '<p class="side-h">Catalog</p><ul>']
    for t, name, f in TYPES:
        S.append(item(f, name, t, NAV["types"].get(t, 0)))
    S.append(item("timeline.html", "Timeline", "timeline"))
    S.append("</ul>")
    for dim, label in (("topics", "Themes"), ("commits", "What it commits"), ("route", "How"), ("layer", "Market layer"), ("grounds", "What grounds"), ("domain", "Domain")):
        vals = NAV["themes"].get(dim, [])
        if not vals:
            continue
        opened = " open" if (active.startswith("topic:%s--" % dim) or dim == "topics") else ""
        S.append('<details class="side-group"%s><summary>%s</summary><ul>' % (opened, label))
        for v, c in vals:
            S.append(item("topics/%s--%s.html" % (dim, v.replace("/", "-")), esc(v), "topic:%s--%s" % (dim, v), c))
        S.append("</ul></details>")
    S.append("</details></aside>")
    return "\n".join(S)


def page(title, body, crumb, description="", depth=0, wide=False, home=False, active=""):
    up = "../" * depth
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="%s">
<title>%s</title>
%s
<link rel="stylesheet" href="%sstyle.css?v=%s">
</head>
<body%s>
<nav class="topbar"><div class="wrap">
  <a href="%s">%s</a>
  <span class="crumb">%s</span>
  <span class="navlinks"><a href="%sbrowse.html">Browse</a><a href="%swhats-new.html">New</a><a href="%slandscape.html">Map</a></span>
</div></nav>
<div class="layout">
%s
<div class="content">
%s
<footer><div class="wrap">
  <p>The Knowledge Layer &middot; a research catalog of enterprise knowledge, ontology and retrieval, kept by Haixun Wang.</p>
  <p>Facts are labelled by source: author-reported, vendor-reported, independent, press or estimate. &ldquo;Our take&rdquo; notes are opinions. Built %s. <a href="%s../">haixun.github.io</a></p>
</div></footer>
</div>
</div>
<script>if(window.matchMedia('(max-width: 760px)').matches){var s=document.querySelector('.sidebox');if(s)s.removeAttribute('open');}</script>
</body>
</html>
""" % (esc(description), esc(title), FONTS, up, CSS_VERSION, ' class="wide"' if wide else "", (up + "../") if home else (up + "index.html"), "&larr; haixun.github.io" if home else "&larr; Knowledge Layer", crumb, up, up, up, sidebar(up, active), body,
       date.today().isoformat(), up)


def write(rel, text):
    path = os.path.join(HERE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def first_sentence(s, n=170):
    s = " ".join(str(s or "").split())
    m = re.match(r"(.+?[.!?])(\s|$)", s)
    s = m.group(1) if m else s
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def load(src):
    cat = os.path.join(src, "catalog")
    tax = json.load(open(os.path.join(cat, "taxonomy.json")))
    entries = {}
    for dp, _, fns in os.walk(os.path.join(cat, "entries")):
        for fn in fns:
            if fn.endswith(".json"):
                e = json.load(open(os.path.join(dp, fn)))
                entries[e["id"]] = e
    news_path = os.path.join(cat, "news.json")
    news = json.load(open(news_path)) if os.path.exists(news_path) else []
    return tax, entries, news


def tag_href(dim, v, up=""):
    return "%stopics/%s--%s.html" % (up, dim, v.replace("/", "-"))


def chips(e, up="", dims=DIMS):
    out = []
    for dim in dims:
        for v in (e.get("tags") or {}).get(dim, []):
            if v in ("none", "n/a"):
                continue
            out.append('<a class="chip chip-%s" href="%s" title="%s">%s</a>' % (dim, tag_href(dim, v, up), esc(DIM_LABEL[dim]), esc(v)))
    return "".join(out)


def entry_link(eid, entries, up=""):
    e = entries.get(eid)
    if not e:
        return esc(eid)
    return '<a href="%sentries/%s.html">%s</a>' % (up, eid, esc(e["name"]))


def status_badge(e):
    st = e.get("status")
    if not st:
        return ""
    return '<span class="badge st-%s">%s</span>' % (esc(st), esc(st))


def related_by_tags(e, entries, k=6):
    def bag(x):
        b = set()
        for dim, vals in (x.get("tags") or {}).items():
            if dim == "grounds":
                continue
            b |= {dim + ":" + v for v in vals if v not in ("none", "n/a", "general")}
        return b
    mine = bag(e)
    scored = []
    for oid, o in entries.items():
        if oid == e["id"]:
            continue
        theirs = bag(o)
        if mine and theirs:
            j = len(mine & theirs) / float(len(mine | theirs))
            if j > 0.25:
                scored.append((j, oid))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [o for _, o in scored[:k]]


# ---------------- entry pages ----------------

def render_entry(e, entries, incoming):
    up = "../"
    meta = [TYPE_TITLE[e["type"]][:-1] if e["type"] != "company" else "Company"]
    if e.get("date"):
        meta.append(esc(e["date"]))
    if e.get("org"):
        meta.append(esc(e["org"]))
    if e.get("venue"):
        meta.append(esc(e["venue"]))
    B = ['<header class="mast"><div class="wrap">',
         '<p class="kicker">%s</p>' % " &middot; ".join(meta),
         '<h1>%s</h1>' % esc(e["name"]),
         '<p class="entry-meta">%s%s</p>' % (status_badge(e), ('<span class="badge ev">%s</span>' % esc(e["evidence"])) if e.get("evidence") else ""),
         '<p class="chips">%s</p>' % chips(e, up),
         '</div></header>', '<div class="wrap"><main class="doc entry">']
    links = ['<a href="%s">%s</a>' % (esc(e["url"]), esc(re.sub(r"^https?://(www\.)?", "", e["url"]).rstrip("/")[:70]))]
    for k, v in (e.get("links") or {}).items():
        links.append('%s: <a href="%s">%s</a>' % (esc(k.replace("-", " ")), esc(v), esc(re.sub(r"^https?://(www\.)?", "", v).rstrip("/")[:60])))
    B.append('<p class="links">%s</p>' % "<br>".join(links))
    if e.get("people"):
        B.append('<p class="people"><span class="lbl">People</span> %s</p>' % esc(", ".join(e["people"])))
    B.append("<h2>Summary</h2><p>%s</p>" % esc(e.get("summary")))
    if e.get("our_take"):
        B.append('<h2>Our take</h2><blockquote><p>%s</p></blockquote>' % esc(e["our_take"]))
    if e.get("key_numbers"):
        B.append("<h2>Key numbers</h2><ul>%s</ul>" % "".join("<li>%s</li>" % esc(n) for n in e["key_numbers"]))
    if e["type"] == "company":
        rows = "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (esc(f.get("date")), esc(f.get("round")), esc(f.get("amount")), esc(f.get("lead")))
                       for f in e.get("funding") or [])
        if rows:
            B.append('<h2>Funding</h2><div class="tablewrap"><table><thead><tr><th>Date</th><th>Round</th><th>Amount</th><th>Lead</th></tr></thead><tbody>%s</tbody></table></div>' % rows)
        facts = []
        for f, lbl in (("hq", "HQ"), ("customers", "Customers"), ("pricing", "Pricing")):
            v = e.get(f)
            if v:
                facts.append("<li><strong>%s:</strong> %s</li>" % (lbl, esc(v if isinstance(v, str) else ", ".join(v))))
        if facts:
            B.append("<ul class=\"facts\">%s</ul>" % "".join(facts))
    out = e.get("relations") or []
    inc = incoming.get(e["id"], [])
    if out or inc:
        items = []
        for r in out:
            items.append('<li><span class="rel">%s</span> %s%s</li>' % (esc(r["type"].replace("-", " ")), entry_link(r["target"], entries, up),
                                                                        (' <span class="rnote">%s</span>' % esc(r["note"])) if r.get("note") else ""))
        for src, r in inc:
            items.append('<li>%s <span class="rel">%s</span> this%s</li>' % (entry_link(src, entries, up), esc(r["type"].replace("-", " ")),
                                                                            (' <span class="rnote">%s</span>' % esc(r["note"])) if r.get("note") else ""))
        B.append('<h2>Relations</h2><ul class="relations">%s</ul>' % "".join(items))
    rel = related_by_tags(e, entries)
    if rel:
        B.append('<h2>Related by tags</h2><ul class="related">%s</ul>' % "".join(
            "<li>%s <span class=\"tp\">%s</span></li>" % (entry_link(o, entries, up), esc(entries[o]["type"])) for o in rel))
    docrefs = []
    for r in e.get("repo_refs") or []:
        b = os.path.basename(r)
        if b in ("landscape.md", "enterprise-business-knowledge-vish.md"):
            docrefs.append('<a href="%s%s">%s</a>' % (up, DOC_REFS[b][1], esc(DOC_REFS[b][0])))
    if docrefs:
        B.append("<h2>Discussed in</h2><p>%s</p>" % ", ".join(docrefs))
    B.append('<p class="stamp">Added %s &middot; last checked against the source %s</p>' % (esc(e.get("added")), esc(e.get("checked"))))
    B.append("</main></div>")
    return page(e["name"] + " · Knowledge Layer", "\n".join(B), '<a href="../%s">%s</a> &middot; <b>%s</b>' % (TYPE_PAGE[e["type"]], TYPE_TITLE[e["type"]], esc(e["name"])),
                first_sentence(e.get("summary")), depth=1, active=e["type"])


# ---------------- list pages ----------------

def list_table(items, entries, up="", company=False):
    if company:
        head = ("<tr><th>Company</th><th>Status</th><th>Layer</th><th>Latest funding</th><th>What it does</th></tr>")
        rows = []
        for e in sorted(items, key=lambda x: x["name"].lower()):
            f = (e.get("funding") or [{}])[-1]
            top = " ".join(x for x in [f.get("amount"), f.get("round")] if x)
            fs = esc(top) + ('<div class="sub">%s</div>' % esc(f.get("date")) if f.get("date") else "")
            rows.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                entry_link(e["id"], entries, up), status_badge(e), chips(e, up, ["layer"]), fs, esc(" ".join(str(e.get("summary") or "").split()))))
        return ('<div class="tablewrap"><table class="list companies"><colgroup><col style="width:13%%"><col style="width:10%%">'
                '<col style="width:15%%"><col style="width:12%%"><col style="width:50%%"></colgroup><thead>%s</thead><tbody>%s</tbody></table></div>') % (head, "".join(rows))
    else:
        head = "<tr><th>Date</th><th>Name</th><th>Tags</th><th>What it is</th></tr>"
        rows = []
        for e in sorted(items, key=lambda x: (str(x.get("date") or ""), x["name"]), reverse=True):
            rows.append("<tr><td class=\"nowrap\">%s</td><td>%s<div class=\"org\">%s</div></td><td>%s</td><td>%s</td></tr>" % (
                esc(e.get("date")), entry_link(e["id"], entries, up), esc(e.get("org")), chips(e, up, ["commits", "route", "grounds"]),
                esc(first_sentence(e.get("summary")))))
    return '<div class="tablewrap"><table class="list"><thead>%s</thead><tbody>%s</tbody></table></div>' % (head, "".join(rows))


def render_type(t, items, entries):
    body = ('<header class="mast"><div class="wrap"><p class="kicker">Catalog</p><h1>%s</h1>'
            '<p class="lede">%d entries. <a href="browse.html#type=%s">Filter and search them</a>.</p></div></header>'
            '<div class="wrap"><main class="doc">%s</main></div>') % (TYPE_TITLE[t], len(items), t, list_table(items, entries, "", t == "company"))
    return page(TYPE_TITLE[t] + " · Knowledge Layer", body, "<b>%s</b>" % TYPE_TITLE[t], "%s in the Knowledge Layer catalog" % TYPE_TITLE[t], wide=True, active=t)


def render_topic(tax, dim, v, items, entries):
    desc = tax["tags"][dim].get(v, "")
    by = defaultdict(list)
    for e in items:
        by[e["type"]].append(e)
    parts = []
    for t, name, _ in TYPES:
        if by.get(t):
            parts.append("<h2>%s (%d)</h2>%s" % (name, len(by[t]), list_table(by[t], entries, "../", t == "company")))
    body = ('<header class="mast"><div class="wrap"><p class="kicker">%s</p><h1>%s</h1><p class="lede">%s</p>'
            '<p class="lede small">%d entries. <a href="../browse.html#%s=%s">Combine with other filters</a>.</p></div></header>'
            '<div class="wrap"><main class="doc">%s</main></div>') % (esc(DIM_LABEL[dim]), esc(v), esc(desc), len(items), dim, esc(v), "".join(parts))
    return page("%s: %s · Knowledge Layer" % (DIM_LABEL[dim], v), body, "%s &middot; <b>%s</b>" % (esc(DIM_LABEL[dim]), esc(v)), desc, depth=1, wide=True, active="topic:%s--%s" % (dim, v))


def render_timeline(entries):
    by = defaultdict(list)
    for e in entries.values():
        by[str(e.get("date") or "")[:4] or "Undated"].append(e)
    parts = []
    for y in sorted(by, reverse=True):
        lis = "".join('<li><span class="d">%s</span> <span class="tp">%s</span> %s <span class="s">%s</span></li>' % (
            esc(e.get("date")), esc(e["type"]), entry_link(e["id"], entries), esc(first_sentence(e.get("summary"), 120)))
            for e in sorted(by[y], key=lambda x: str(x.get("date") or ""), reverse=True))
        parts.append('<h2>%s <span class="count">%d</span></h2><ul class="timeline">%s</ul>' % (esc(y), len(by[y]), lis))
    body = ('<header class="mast"><div class="wrap"><p class="kicker">Catalog</p><h1>Timeline</h1>'
            '<p class="lede">How the field moved, newest first.</p></div></header><div class="wrap"><main class="doc">%s</main></div>') % "".join(parts)
    return page("Timeline · Knowledge Layer", body, "<b>Timeline</b>", "The Knowledge Layer catalog by date", active="timeline")


# ---------------- what's new ----------------

def news_entries_html(item, entries, up=""):
    ids = [i for i in item.get("entries", []) if i in entries]
    if not ids:
        return ""
    by = defaultdict(list)
    for i in ids:
        by[entries[i]["type"]].append(entries[i])
    parts = []
    for t, name, _ in TYPES:
        if by.get(t):
            lis = "".join('<li>%s <span class="s">%s</span></li>' % (entry_link(e["id"], entries, up), esc(first_sentence(e.get("summary"), 140)))
                          for e in sorted(by[t], key=lambda x: x["name"].lower()))
            parts.append('<h3>%s <span class="count">%d</span></h3><ul class="timeline">%s</ul>' % (name, len(by[t]), lis))
    return "".join(parts)


def render_whats_new(news, entries):
    parts = []
    for item in news:
        notes = "".join("<p>%s</p>" % esc(p) for p in item.get("note", []))
        n = len([i for i in item.get("entries", []) if i in entries])
        parts.append('<section class="news"><p class="kicker">%s%s</p><h2>%s</h2>%s%s</section>' % (
            esc(item.get("date")), (" &middot; %d added" % n) if n else "", esc(item.get("title")), notes, news_entries_html(item, entries)))
    body = ('<header class="mast"><div class="wrap"><p class="kicker">Catalog</p><h1>What&rsquo;s new</h1>'
            '<p class="lede">Each sweep or batch of additions, newest first: what changed in the field, and what we added.</p></div></header>'
            '<div class="wrap"><main class="doc">%s</main></div>') % "".join(parts)
    return page("What's new · Knowledge Layer", body, "<b>What&rsquo;s new</b>", "Recent additions to the Knowledge Layer catalog", active="news")


# ---------------- browse (client-side filters) ----------------

BROWSE_JS = r"""
const D = JSON.parse(document.getElementById('data').textContent);
const DIMS = ["type","status","commits","route","grounds","layer","domain","topics"];
const q = document.getElementById('q'), out = document.getElementById('out'), n = document.getElementById('n');
const sel = {};
function opts(){
  for (const d of DIMS){
    const s = document.getElementById('f-'+d); sel[d]=s;
    const counts = {};
    for (const e of D){ for (const v of vals(e,d)) counts[v]=(counts[v]||0)+1; }
    for (const v of Object.keys(counts).sort()){
      const o=document.createElement('option'); o.value=v; o.textContent=v+' ('+counts[v]+')'; s.appendChild(o);
    }
    s.addEventListener('change', run);
  }
  q.addEventListener('input', run);
  document.getElementById('reset').addEventListener('click', ()=>{ q.value=''; for(const d of DIMS) sel[d].value=''; run(); });
}
function vals(e,d){ if(d==='type') return [e.type]; if(d==='status') return e.status?[e.status]:[]; return (e.tags&&e.tags[d])||[]; }
function readHash(){
  const p = new URLSearchParams(location.hash.slice(1));
  for (const d of DIMS) if (p.get(d)) sel[d].value = p.get(d);
  if (p.get('q')) q.value = p.get('q');
}
function writeHash(){
  const p = new URLSearchParams();
  for (const d of DIMS) if (sel[d].value) p.set(d, sel[d].value);
  if (q.value) p.set('q', q.value);
  const h = p.toString(); history.replaceState(null,'', h ? '#'+h : location.pathname);
}
function esc(s){ return String(s||'').replace(/[&<>"]/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
function run(){
  const terms = q.value.toLowerCase().split(/\s+/).filter(Boolean);
  const res = D.filter(e => {
    for (const d of DIMS){ const v=sel[d].value; if (v && !vals(e,d).includes(v)) return false; }
    const hay = (e.name+' '+e.org+' '+e.summary+' '+(e.people||[]).join(' ')+' '+Object.values(e.tags||{}).flat().join(' ')).toLowerCase();
    return terms.every(t => hay.includes(t));
  }).sort((a,b)=> String(b.date||'').localeCompare(String(a.date||'')));
  n.textContent = res.length + (res.length===1?' entry':' entries');
  out.innerHTML = res.map(e => `<li class="hit"><div class="hit-h"><a href="entries/${e.id}.html">${esc(e.name)}</a>
    <span class="tp">${esc(e.type)}</span>${e.status?`<span class="badge st-${esc(e.status)}">${esc(e.status)}</span>`:''}</div>
    <div class="hit-m">${esc([e.date,e.org].filter(Boolean).join(' · '))}</div>
    <p>${esc(e.summary)}</p>
    <div class="chips">${['commits','route','grounds','layer'].flatMap(d=>((e.tags||{})[d]||[]).filter(v=>v!=='none'&&v!=='n/a').map(v=>`<span class="chip chip-${d}">${esc(v)}</span>`)).join('')}</div></li>`).join('');
  writeHash();
}
opts(); readHash(); run();
window.addEventListener('hashchange', ()=>{ readHash(); run(); });
"""


def render_browse(entries):
    data = [{"id": e["id"], "type": e["type"], "name": e["name"], "date": e.get("date", ""), "org": e.get("org", ""),
             "status": e.get("status", ""), "summary": first_sentence(e.get("summary"), 240), "people": e.get("people", [])[:6],
             "tags": e.get("tags", {})} for e in entries.values()]
    selects = "".join('<label><span>%s</span><select id="f-%s"><option value="">All</option></select></label>' % (
        esc({"type": "Type", "status": "Status"}.get(d, DIM_LABEL.get(d, d))), d) for d in
        ["type", "status", "commits", "route", "grounds", "layer", "domain", "topics"])
    body = ('<header class="mast"><div class="wrap"><p class="kicker">Catalog</p><h1>Browse</h1>'
            '<p class="lede">Search and filter every entry. The address bar keeps your filters, so you can share a view.</p></div></header>'
            '<div class="wrap"><main class="doc"><div class="filters"><label class="search"><span>Search</span>'
            '<input id="q" type="search" placeholder="name, author, company, idea…" autocomplete="off"></label>%s'
            '<button id="reset" type="button">Reset</button></div><p class="count" id="n"></p><ul class="hits" id="out"></ul>'
            '<noscript><p>Filtering needs JavaScript. The <a href="papers.html">papers</a>, <a href="companies.html">companies</a> and '
            '<a href="timeline.html">timeline</a> pages work without it.</p></noscript></main></div>'
            '<script id="data" type="application/json">%s</script><script>%s</script>') % (
        selects, json.dumps(data, ensure_ascii=False).replace("</", "<\\/"), BROWSE_JS)
    return page("Browse · Knowledge Layer", body, "<b>Browse</b>", "Search and filter the Knowledge Layer catalog", active="browse")


# ---------------- index ----------------

def render_index(tax, entries, by_type, tag_index, news=()):
    opt = [v for v in tax["tags"]["commits"] if not v.startswith("_") and v != "none"]
    routes = [v for v in tax["tags"]["route"] if not v.startswith("_") and v not in ("n/a",)]
    grid = defaultdict(int)
    for e in entries.values():
        for o in (e.get("tags") or {}).get("commits", []):
            for r in (e.get("tags") or {}).get("route", []):
                grid[(o, r)] += 1
    rows_used = [o for o in opt if any(grid[(o, r)] for r in routes)]
    cols_used = [r for r in routes if any(grid[(o, r)] for o in opt)]
    mx = max(grid.values() or [1])
    cells = []
    for o in rows_used:
        tds = []
        for r in cols_used:
            c = grid[(o, r)]
            if c:
                tds.append('<td><a class="cell" style="--w:%.2f" href="browse.html#commits=%s&amp;route=%s">%d</a></td>' % (0.15 + 0.85 * c / mx, o, r, c))
            else:
                tds.append('<td class="empty">·</td>')
        cells.append('<tr><th><a href="%s">%s</a></th>%s</tr>' % (tag_href("commits", o), esc(o), "".join(tds)))
    grid_html = ('<div class="tablewrap"><table class="grid"><thead><tr><th>commits &darr; &nbsp; route &rarr;</th>%s</tr></thead><tbody>%s</tbody></table></div>' % (
        "".join('<th><a href="%s">%s</a></th>' % (tag_href("route", r), esc(r)) for r in cols_used), "".join(cells)))
    counts = "".join('<li class="card"><h3><a href="%s">%s</a></h3><p class="big">%d</p></li>' % (f, n, len(by_type.get(t, []))) for t, n, f in TYPES)
    recent = sorted(entries.values(), key=lambda e: (str(e.get("added")), str(e.get("date") or "")), reverse=True)[:12]
    recent_html = "".join('<li><span class="tp">%s</span> %s <span class="s">%s</span></li>' % (esc(e["type"]), entry_link(e["id"], entries), esc(first_sentence(e.get("summary"), 110))) for e in recent)
    latest_html = ""
    if news:
        it = news[0]
        n = len([i for i in it.get("entries", []) if i in entries])
        latest_html = ('<div class="newsbox"><p class="section-label">What&rsquo;s new &middot; %s</p><h3><a href="whats-new.html">%s</a></h3>'
                       '<p>%s</p><p class="more"><a href="whats-new.html">%sRead the update &rarr;</a></p></div>') % (
            esc(it.get("date")), esc(it.get("title")), esc((it.get("note") or [""])[0]), ("%d new entries. " % n) if n else "")
    topics = []
    for dim in ("topics", "layer", "grounds", "domain"):
        vals = [(v, len(tag_index[(dim, v)])) for v in tax["tags"][dim] if not v.startswith("_") and tag_index.get((dim, v))]
        topics.append('<p class="tagrow"><span class="lbl">%s</span> %s</p>' % (esc(DIM_LABEL[dim]), " ".join(
            '<a class="chip chip-%s" href="%s">%s <b>%d</b></a>' % (dim, tag_href(dim, v), esc(v), c) for v, c in vals)))
    body = """<header class="mast"><div class="wrap">
<p class="kicker">Research catalog &middot; November 2026</p>
<h1>The Knowledge Layer</h1>
<p class="lede">Enterprises are rebuilding the semantic web so that agents can use what they know. The field is split on
how: either meaning is <b>committed</b> in advance &mdash; a glossary, an ontology, a semantic model, a rule base &mdash; and data
conforms to it, or the corpus is left alone and the agent <b>derives</b> meaning at query time with search and tools. Both
camps are winning at once. This catalog organises the companies, papers, products, articles, benchmarks and standards
working on that question, and tracks the one thing neither camp supplies: something that warrants the answer.</p>
</div></header>
<div class="wrap">
%s
<p class="section-label">Start here</p>
<ul class="cards">
  <li class="card wide"><h3><a href="field-guide.html">Ontologies for AI Agents</a></h3>
  <p>A guide to the field, written to be read cold: the problem, the vocabulary, the two strategies, what every large
  platform built in 2026, how they decide which definition to trust, what about forty-five research papers actually
  show, the problems nobody has solved, the standards, and the debate in the participants' own words.</p>
  <div class="meta"><span>Guide</span><span>November 2026</span></div></li>
  <li class="card wide"><h3><a href="landscape.html">The Knowledge Layer</a></h3>
  <p>The map: commit versus derive, the commitment ladder from raw corpus to rules, the commercial tiers, and the
  acquisitions that show the standalone product being absorbed by whoever already owns the corpus. Then the one thing
  empty from every direction &mdash; across this catalog, 58 entries claim to enforce permissions, 24 record who
  decided, 16 carry valid time, and 12 can report logical entailment.</p>
  <div class="meta"><span>Map</span><span>November 2026</span></div></li>
</ul>
<p class="section-label">The catalog</p>
<p class="section-note">%d entries, each with a summary, key numbers labelled by source, tags, and relations to other entries.
<a href="browse.html">Search and filter everything</a>, or start from a type.</p>
<ul class="cards counts">%s</ul>
<p class="section-label">Where meaning is committed, and how</p>
<p class="section-note">Papers, products and companies by where they fix meaning (rows) and how they get there (columns). Click a number to see them.</p>
%s
<p class="section-label">By theme</p>
%s
<p class="section-label">Recently added</p>
<ul class="timeline">%s</ul>
<p class="more"><a href="timeline.html">Full timeline &rarr;</a></p>
</div>""" % (latest_html, len(entries), counts, grid_html, "".join(topics), recent_html)
    return page("The Knowledge Layer", body, "<b>Knowledge Layer</b>",
                "A research catalog of the enterprise knowledge layer: ontology, retrieval, governance, agent memory and what warrants an answer.", home=True, active="index")


# ---------------- essays ----------------

def rewrite_refs(md):
    for a, b in PROSE_FIXES:
        md = md.replace(a, b)
    stash = []

    def hide(m):
        stash.append(m.group(0))
        return "\x00%d\x00" % (len(stash) - 1)

    def link(m):
        text, target = m.group(1), m.group(2)
        if re.match(r"https?://|#|mailto:", target):
            return m.group(0)
        base = os.path.basename(target.split("#")[0].rstrip("/")) or "README.md"
        label, href = DOC_REFS.get(base, (None, None))
        shown = label if re.match(r"^`?[\w./-]+\.md`?$|^`?\.\./[\w/-]*`?$", text.strip()) else text
        if label is None:
            return shown
        return "[%s](%s)" % (shown, href) if href else "*%s*" % shown
    md = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: hide(re.match(r".*", link(m))), md)
    md = re.sub(r"`((?:\.\./)?[\w/-]*?([\w-]+\.md))`", lambda m: (lambda d: ("*%s*" % d[0]) if d[0] else m.group(0))(DOC_REFS.get(m.group(2), (None, None))), md)
    return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], md)


def gh_render(md):
    r = subprocess.run(["gh", "api", "markdown", "-f", "mode=markdown", "-F", "text=@-"], input=md.encode(), capture_output=True)
    if r.returncode != 0:
        sys.exit("gh api markdown failed: %s" % r.stderr.decode())
    return r.stdout.decode()


def tidy_html(h):
    h = re.sub(r'<a id="user-content-[^"]*" class="anchor"[^>]*>.*?</a>', "", h, flags=re.S)
    h = re.sub(r'<svg[^>]*class="octicon[^"]*"[^>]*>.*?</svg>', "", h, flags=re.S)
    h = re.sub(r'<div class="markdown-heading"[^>]*>(.*?)</div>', r"\1", h, flags=re.S)
    h = re.sub(r'\s(dir|class)="auto"', "", h)
    h = h.replace("<table>", '<div class="tablewrap"><table>').replace("</table>", "</table></div>")
    h = re.sub(r'<div class="tablewrap"><div class="tablewrap">', '<div class="tablewrap">', h)
    h = re.sub(r'<markdown-accessiblity-table[^>]*>|</markdown-accessiblity-table>', "", h)
    return h


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", s).lower()).strip("-")


def render_doc(src, fn, out, kicker, short):
    md = open(os.path.join(src, fn)).read()
    md = rewrite_refs(md)
    m = re.match(r"#\s+(.+)\n+(\*[^\n]+\*)\n", md)
    title = m.group(1).strip() if m else short
    standfirst = ""
    if m:
        standfirst = gh_render(m.group(2))
        standfirst = re.sub(r"^<p>(.*)</p>\s*$", r"\1", standfirst.strip(), flags=re.S)
        md = md[m.end():]
    body = tidy_html(gh_render(md))
    toc = []

    def h2(mm):
        inner = mm.group(1)
        sid = slug(inner)
        toc.append('<li><a href="#%s">%s</a></li>' % (sid, re.sub(r"<[^>]+>", "", inner)))
        return '<h2 id="%s">%s</h2>' % (sid, inner)
    body = re.sub(r"<h2[^>]*>(.*?)</h2>", h2, body, flags=re.S)
    toc_html = '<nav class="toc"><h2>Contents</h2><ol class="plain">%s</ol></nav>' % "".join(toc) if len(toc) > 2 else ""
    page_body = ('<header class="mast"><div class="wrap"><p class="kicker">%s</p><h1>%s</h1><p class="standfirst">%s</p></div></header>'
                 '<div class="wrap">%s<main class="doc">%s</main></div>') % (kicker, esc(title), standfirst, toc_html, body)
    write(out, page(title + " · Knowledge Layer", page_body, "%s &middot; <b>%s</b>" % (kicker, esc(short)), re.sub(r"<[^>]+>", "", standfirst)[:300], active="doc:" + out))


# ---------------- main ----------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.path.expanduser("~/explore/kb"))
    ap.add_argument("--no-docs", action="store_true")
    a = ap.parse_args()
    tax, entries, news = load(a.src)
    incoming = defaultdict(list)
    for eid, e in entries.items():
        for r in e.get("relations") or []:
            if r.get("target") in entries:
                incoming[r["target"]].append((eid, r))
    by_type, tag_index = defaultdict(list), defaultdict(list)
    for e in entries.values():
        by_type[e["type"]].append(e)
        for dim, vals in (e.get("tags") or {}).items():
            for v in vals:
                tag_index[(dim, v)].append(e)
    NAV["types"] = {t: len(v) for t, v in by_type.items()}
    for dim in ("topics", "commits", "route", "layer", "grounds", "domain"):
        NAV["themes"][dim] = [(v, len(tag_index[(dim, v)])) for v in tax["tags"][dim]
                              if not v.startswith("_") and v not in ("none", "n/a") and tag_index.get((dim, v))]
    for sub in ("entries", "topics"):
        d = os.path.join(HERE, sub)
        if os.path.isdir(d):
            for fn in os.listdir(d):
                if fn.endswith(".html"):
                    os.remove(os.path.join(d, fn))
    for e in entries.values():
        write("entries/%s.html" % e["id"], render_entry(e, entries, incoming))
    for t, items in by_type.items():
        write(TYPE_PAGE[t], render_type(t, items, entries))
    for (dim, v), items in tag_index.items():
        write("topics/%s--%s.html" % (dim, v.replace("/", "-")), render_topic(tax, dim, v, items, entries))
    write("timeline.html", render_timeline(entries))
    write("browse.html", render_browse(entries))
    write("index.html", render_index(tax, entries, by_type, tag_index, news))
    write("whats-new.html", render_whats_new(news, entries))
    if not a.no_docs:
        for fn, out, kicker, short in DOCS:
            render_doc(a.src, fn, out, kicker, short)
    print("Built %d entry pages, %d topic pages, %d type pages%s." % (
        len(entries), len(tag_index), len(by_type), "" if a.no_docs else ", 2 essays"))


if __name__ == "__main__":
    main()
