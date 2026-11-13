#!/usr/bin/env python3
"""Render the drug-design research documents to static HTML.

The sources are Markdown files in a separate, private, local-only
repository. Point --src at its `research` directory; the default is where
that repository lives.

    python3 build.py                       # uses ~/carpediem/drug-design/research
    python3 build.py --src /path/to/research

Needs the `markdown` package (pip install markdown). Writes one .html per
source document into this directory, alongside the hand-written index.html
and the shared style.css, neither of which this script touches.

The sources refer to each other by filename, which means nothing to a reader
of the published site. Every such reference is rewritten to the document's
title: a link when that document is published here, plain italics when it
is not. See DISPLAY below.
"""

import argparse
import html
import pathlib
import re
import sys

try:
    import markdown
except ImportError:
    sys.exit("needs the markdown package: pip install markdown")

# Source stem -> (kicker shown above the title, output filename)
DOCS = [
    ("computational-drug-design-primer", "Primer", "computational-drug-design-primer.html"),
    ("what-gets-funded-at-seed", "Study", "what-gets-funded-at-seed.html"),
    ("sources/seed-protein-design-companies", "Evidence file", "seed-protein-design-companies.html"),
    ("sources/seed-extracellular-degraders", "Evidence file", "seed-extracellular-degraders.html"),
    ("sources/seed-founder-credentials", "Evidence file", "seed-founder-credentials.html"),
    ("sources/seed-round-mechanics-and-investors", "Evidence file", "seed-round-mechanics-and-investors.html"),
    ("sources/seed-failures-and-survivorship", "Evidence file", "seed-failures-and-survivorship.html"),
    ("sources/seed-investor-requirements", "Evidence file", "seed-investor-requirements.html"),
]

# Markdown basename -> (name to show a reader, page to link to or None).
# The display names match the cards on index.html so each document has one
# name everywhere on the site.
DISPLAY = {
    "computational-drug-design-primer":
        ("How a Designed Molecule Becomes a Candidate", "computational-drug-design-primer.html"),
    "what-gets-funded-at-seed":
        ("What Gets Funded at Seed in AI Drug Design", "what-gets-funded-at-seed.html"),
    "seed-protein-design-companies":
        ("Protein and Antibody Design Companies", "seed-protein-design-companies.html"),
    "seed-extracellular-degraders":
        ("Extracellular and Targeted Degraders", "seed-extracellular-degraders.html"),
    "seed-founder-credentials":
        ("Founder Credentials", "seed-founder-credentials.html"),
    "seed-round-mechanics-and-investors":
        ("Round Mechanics and Investors", "seed-round-mechanics-and-investors.html"),
    "seed-failures-and-survivorship":
        ("Failures and Survivorship", "seed-failures-and-survivorship.html"),
    "seed-investor-requirements":
        ("What Investors Say They Require", "seed-investor-requirements.html"),
    # Documents that live only in the private repository. Named, never linked.
    "landscape": ("Where AI Actually Enters Drug Discovery", None),
    "plan": ("the research plan", None),
    "README": ("the folder index", None),
    "resources": ("the research log", None),
    "the-pairing": ("The Pairing", None),
    "outcomes-and-deals": ("Outcomes and Deals", None),
    "ai-native-companies": ("AI-native Companies in Biology and Drug Discovery", None),
    "pipeline-map": ("The Drug Discovery Pipeline", None),
    "labs-and-cros": ("Labs and CROs", None),
    "models-and-data": ("Models and Data", None),
}

# A reference to a sibling document: an optional path, a stem, and .md,
# optionally wrapped in backticks.
MD_REF = re.compile(r"`?(?:\.\./)?(?:ai4bio/)?(?:sources/)?([A-Za-z0-9._-]+)\.md`?")

# Phrases that only make sense when the documents sit in a repository.
PROSE_FIXES = [
    ("**In this repository**", "**Related reading**"),
    ("Related work in this repository:", "Related reading:"),
    ("Related work in this repository", "Related reading"),
]

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{description}">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="style.css">
</head>
<body>

<nav class="topbar"><div class="wrap">
  <a href="index.html">&larr; All documents</a>
  <span class="crumb">{kicker} &middot; <b>{shorttitle}</b></span>
</div></nav>

<header class="mast"><div class="wrap">
  <p class="kicker">{kicker}</p>
  <h1>{h1}</h1>
  {standfirst}
</div></header>

<div class="wrap">
{toc}
<main class="doc">
{bodyhtml}
</main>
</div>

<footer><div class="wrap">
  <p>{h1}</p>
  <p>Rendered from Markdown research notes. <a href="index.html">Back to the index</a>.</p>
</div></footer>

</body>
</html>
"""


def retitle(text, self_page):
    """Replace filename references with document titles.

    URLs are stashed first so that an http address is never treated as a
    document reference. One source carries a news URL with a stray '.md'
    suffix, which is dropped on the way back in.
    """
    stash = []

    def hide(m):
        stash.append(m.group(0))
        return "\x00%d\x00" % (len(stash) - 1)

    text = re.sub(r"https?://[^\s)\"'<>]+", hide, text)

    def sub(m):
        stem = m.group(1)
        name, page = DISPLAY.get(stem, (stem.replace("-", " "), None))
        if page and page != self_page:
            return "[%s](%s)" % (name, page)
        return "*%s*" % name

    text = MD_REF.sub(sub, text)

    for old, new in PROSE_FIXES:
        text = text.replace(old, new)

    def show(m):
        url = stash[int(m.group(1))]
        return url[:-3] if url.endswith(".md") else url

    return re.sub(r"\x00(\d+)\x00", show, text)


def build_toc(body):
    """A contents list from the h2 headings, which carry ids from the toc extension."""
    items = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, re.S)
    if len(items) < 3:
        return ""
    rows = "\n".join(
        '    <li><a href="#{}">{}</a></li>'.format(i, re.sub(r"<[^>]+>", "", t).strip())
        for i, t in items
    )
    return '<nav class="toc">\n  <h2>Contents</h2>\n  <ol>\n%s\n  </ol>\n</nav>' % rows


def render(path, kicker, self_page):
    text = retitle(path.read_text(encoding="utf-8"), self_page)

    md = markdown.Markdown(
        extensions=["tables", "attr_list", "sane_lists", "toc", "md_in_html"],
        extension_configs={"toc": {"toc_depth": "2-2"}},
    )
    body = md.convert(text)

    # Pull the h1 out of the flow; it belongs in the masthead.
    m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    h1 = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else path.stem
    if m:
        body = body[: m.start()] + body[m.end():]

    # The convention in these documents is a single italic paragraph under the
    # title saying what the document is. Promote it to a standfirst.
    standfirst, description = "", h1
    m = re.match(r"\s*<p><em>(.*?)</em></p>", body, re.S)
    if m:
        inner = m.group(1)
        standfirst = '<p class="standfirst">%s</p>' % inner
        plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", inner)).strip()
        description = plain[:197].rsplit(" ", 1)[0] + "..." if len(plain) > 200 else plain
        body = body[: m.start()] + body[m.end():]

    body = re.sub(r"<table>", '<div class="tablewrap"><table>', body)
    body = re.sub(r"</table>", "</table></div>", body)

    short = h1 if len(h1) <= 42 else h1[:39].rstrip() + "..."
    return PAGE.format(
        title=html.escape(h1),
        shorttitle=html.escape(short),
        description=html.escape(description, quote=True),
        kicker=html.escape(kicker),
        h1=html.escape(h1),
        standfirst=standfirst,
        toc=build_toc(body),
        bodyhtml=body.strip(),
    )


def main():
    here = pathlib.Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(pathlib.Path.home() / "carpediem" / "drug-design" / "research"),
                    help="directory holding the Markdown sources")
    args = ap.parse_args()
    src = pathlib.Path(args.src).expanduser()

    if not src.is_dir():
        sys.exit("source directory not found: %s" % src)

    for stem, kicker, out in DOCS:
        path = src / (stem + ".md")
        if not path.exists():
            print("  skip  %s (not found)" % stem)
            continue
        (here / out).write_text(render(path, kicker, out), encoding="utf-8")
        print("  wrote %-46s %6.0f KB" % (out, (here / out).stat().st_size / 1024))


if __name__ == "__main__":
    main()
