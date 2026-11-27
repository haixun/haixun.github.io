# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal site for Haixun Wang, served by **classic GitHub Pages** (no Actions workflow) from `master` at `haixun.github.io`. It is really two Jekyll sites plus a pile of static files:

1. **Root site**: Jekyll with **no theme**, built by GitHub Pages on push (`github-pages` gem). Every page uses the single self-contained `_layouts/default.html`, which holds all the CSS inline. There are no includes and no Sass. Pages are `index.markdown`, `about.markdown`, `probase.markdown`, `tangshi*.markdown`, `readinglist.markdown`, and others.
2. **Stories site** (`/stories/`): its own Jekyll project in `_stories_src/`, which has a custom theme and its own `_config.yml` with `baseurl: /stories`. The root `_config.yml` excludes it. GitHub Pages does **not** build it. You build it locally and commit the generated HTML to `stories/`. See `_stories_src/CLAUDE.md` for its content rules, front matter, and allowed categories.
3. **Static artifacts**: hand-written or exported HTML (`genai.html`, `ecommerce.html`, `trinity.html`, `spanish.html`, `Simulation.html`, `vldb/*.html`). These have no front matter, so Jekyll copies them unchanged.

## Commands

```bash
# Root site local preview (http://localhost:4000). The root Gemfile.lock pins
# 2020-era gems that don't install on current Ruby, so this borrows _stories_src's bundle.
./serve.sh

# Stories site: edit in _stories_src/, then rebuild into stories/ and commit both
cd _stories_src
bundle exec jekyll serve                      # http://localhost:4000/stories
bundle exec jekyll build --destination ../stories
```

Markdown files without front matter (`movies`, `tangshi*`, `readinglist*`) are still rendered on GitHub Pages by its `jekyll-optional-front-matter` plugin, but plain Jekyll 4 skips them, so they won't appear in the local preview. Give a page front matter (`layout: default`) if you need to preview it.

If you change anything under `_stories_src/` and don't rebuild, the live site won't change. `stories/_site/` is a stray, gitignored artifact. Ignore it.

## Home page (`index.markdown`)

The header is an HTML `<header class="intro">` block (photo + name + current title), styled in `_layouts/default.html`. In Experience and Honors, current roles are bold, every entry carries years, and lists run newest first.

`Haixun Wang CV Mar 2026.md` in the repo root is the source for Experience and Honors. It is deliberately untracked because it contains a phone number, and anything committed here gets published. Never commit it.

After pushing, `gh api repos/haixun/haixun.github.io/pages/builds/latest` shows whether the Pages build for your commit has finished.

## Generated files: edit the source, not the output

- **Reading list**: `readinglist.json` is the source. Run `python3 readinglist.py` to regenerate both `readinglist.markdown` (public) and `myreadinglist.markdown` (adds the `local` Dropbox links). Entries are grouped by week, newest week first. `readinglist.txt` is legacy and not used by the script.
- **VLDB 2024 workshop proceedings**: `vldb/vldb.py` reads the two TSVs in `vldb/` and prints org-mode to stdout (run it from inside `vldb/`). The org file is then exported to `vldb/vldb.html` / `workshop.html` outside this repo's tooling. Paper PDFs live in `vldb/VLDB-Workshop-2024/<workshop>/`.

## `vldb-supplemental-material/`

This is an anonymized research artifact bundle for a paper. It's most of the tracked files in the repo, and it's served as-is. Its `README.md` maps each paper claim to an artifact and to the script that regenerates it. `MANIFEST.sha256` covers every shipped file, so if you add, remove, or edit files there, regenerate the manifest. Keep the bundle anonymous: no author names, affiliations, emails, or absolute local paths.

## `Memorize/`

Static study sites for learning a text by heart. `Memorize/Cien Años/` is a 40-lesson Spanish course on the first two paragraphs of *Cien años de soledad* (Part 1: lessons 1 to 20, paragraph 1; Part 2: lessons 21 to 40, paragraph 2). Its HTML and `data.js` are generated: edit the files in `content/` (lessons, vocabulary, phrase breakdown), `style.css` or `app.js`, then run `python3 build.py` from inside that directory and commit the output.

Each paragraph has its own `content/paraN.txt`, `chunksN.txt`, `vocabN.txt` and `timingsN.json`, and its own audio excerpt `audio/paraN.m4a` (paragraph 1's content files carry no number). Sentence numbers in the content files are local to their paragraph; the build also gives every sentence a global number, which audio targets, practice ranges and saved progress use. Adding a paragraph means adding those files, an entry in `PARAS` in `build.py`, and lessons.

The course is organised as book → chapter → paragraph → lesson. `BOOK` in `build.py` lists the chapters and which paragraphs belong to each; `INDEX_GROUPS` groups each paragraph's lessons. From these the build writes the navigation tree into `data.js`, and `app.js` renders the **Lessons** menu (chapters and paragraphs on the left, that paragraph's lessons on the right; a full-screen sheet on phones), the collapsible paragraph blocks on the overview page, and the breadcrumb on each lesson. A new chapter or paragraph needs no menu code, only entries in `BOOK`, `PARAS` and `INDEX_GROUPS`. Each lesson also gets a sticky row of links to its own sections, built from the section headings in `section_nav()`.

`content/examplesN.txt` holds one original example sentence (Spanish and English) for every noun, verb and adjective in `vocabN.txt`. They are written for the course and must never be taken from the novel. The build fails if one is missing or does not contain the exact word form.

`build.py` fails if a phrase breakdown stops matching its `paraN.txt`, if any word lacks a vocabulary entry, or if an expression does not occur in the text. `content/timings*.json` (audio time ranges) and `content/links.json` (checked pronunciation links) were measured from the source audiobook and the live dictionary site with scripts kept in the private `carpediem` repo under `memorize/CienAños/tools/`; the build does not regenerate them. All links inside the course are relative, so it works under the path with the space and the ñ.
