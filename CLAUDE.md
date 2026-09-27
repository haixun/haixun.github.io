# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal site for Haixun Wang, served by **classic GitHub Pages** (no Actions workflow) from `master` at `haixun.github.io`. It is really two Jekyll sites plus a pile of static files:

1. **Root site**: Jekyll with the `minima` theme, built by GitHub Pages on push (`github-pages` gem). The pages are `index.markdown`, `about.markdown`, `probase.markdown`, `tangshi*.markdown`, `readinglist.markdown`, and others.
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

If you change anything under `_stories_src/` and don't rebuild, the live site won't change. `stories/_site/` is a stray, gitignored artifact. Ignore it.

## Generated files: edit the source, not the output

- **Reading list**: `readinglist.json` is the source. Run `python3 readinglist.py` to regenerate both `readinglist.markdown` (public) and `myreadinglist.markdown` (adds the `local` Dropbox links). Entries are grouped by week, newest week first. `readinglist.txt` is legacy and not used by the script.
- **VLDB 2024 workshop proceedings**: `vldb/vldb.py` reads the two TSVs in `vldb/` and prints org-mode to stdout (run it from inside `vldb/`). The org file is then exported to `vldb/vldb.html` / `workshop.html` outside this repo's tooling. Paper PDFs live in `vldb/VLDB-Workshop-2024/<workshop>/`.

## `vldb-supplemental-material/`

This is an anonymized research artifact bundle for a paper. It's most of the tracked files in the repo, and it's served as-is. Its `README.md` maps each paper claim to an artifact and to the script that regenerates it. `MANIFEST.sha256` covers every shipped file, so if you add, remove, or edit files there, regenerate the manifest. Keep the bundle anonymous: no author names, affiliations, emails, or absolute local paths.
