#!/usr/bin/env python3
"""Render the drug-design research documents to static HTML.

The sources are Markdown files in a separate, private repository. Point
--src at its `ai4bio` directory; the default assumes the two repositories
sit side by side in the same parent folder.

    python3 build.py                       # uses ../../explore/ai4bio
    python3 build.py --src ~/explore/ai4bio

Needs the `markdown` package (pip install markdown). Writes one .html per
source document into this directory, alongside the hand-written index.html
and the shared style.css, neither of which this script touches.
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

# Markdown references to sibling documents, rewritten to the built pages.
CROSSLINKS = {
    "`sources/seed-protein-design-companies.md`": "seed-protein-design-companies.html",
    "`sources/seed-extracellular-degraders.md`": "seed-extracellular-degraders.html",
    "`sources/seed-founder-credentials.md`": "seed-founder-credentials.html",
    "`sources/seed-round-mechanics-and-investors.md`": "seed-round-mechanics-and-investors.html",
    "`sources/seed-failures-and-survivorship.md`": "seed-failures-and-survivorship.html",
    "`sources/seed-investor-requirements.md`": "seed-investor-requirements.html",
    "`computational-drug-design-primer.md`": "computational-drug-design-primer.html",
    "`what-gets-funded-at-seed.md`": "what-gets-funded-at-seed.html",
}

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


def slug(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    return re.sub(r"[\s-]+", "-", text).strip("-")


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


def render(path, kicker):
    text = path.read_text(encoding="utf-8")

    for ref, target in CROSSLINKS.items():
        label = ref.strip("`").split("/")[-1]
        text = text.replace(ref, "[`%s`](%s)" % (label, target))

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
    ap.add_argument("--src", default=str(here.parent.parent / "explore" / "ai4bio"),
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
        (here / out).write_text(render(path, kicker), encoding="utf-8")
        print("  wrote %-46s %6.0f KB" % (out, (here / out).stat().st_size / 1024))


if __name__ == "__main__":
    main()
