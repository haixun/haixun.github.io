# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Writing portfolio site served at `haixun.github.io/stories`. Uses a custom elegant literary theme with Cormorant Garamond typography. The site is pre-built and served as static HTML via GitHub Pages.

## Directory Structure

```
haixun.github.io/
├── _stories_src/          # Jekyll source (this folder)
│   ├── _posts/            # Story/essay markdown files
│   ├── _layouts/          # HTML templates
│   ├── _data/stories.yml  # Metadata (optional)
│   ├── assets/            # Source images and CSS
│   └── _config.yml        # Jekyll config
├── stories/               # Built static output (served at /stories/)
└── [other root site files]
```

## Development Commands

```bash
cd /Users/haixun/haixun.github.io/_stories_src

# Install dependencies (first time)
bundle install

# Local preview
bundle exec jekyll serve    # Preview at http://localhost:4000/stories

# Build for production
bundle exec jekyll build --destination ../stories
```

## Deployment Workflow

After making changes:

```bash
cd /Users/haixun/haixun.github.io/_stories_src
bundle exec jekyll build --destination ../stories
cd ..
git add -A && git commit -m "Update stories" && git push
```

## Adding/Editing Content

Posts are in `_posts/` with filename `YYYY-MM-DD-slug.md`:

```markdown
---
layout: post
title: "Story Title"
date: YYYY-MM-DD
categories: [short-story]   # or [essay]
image: "/assets/images/story-name.jpg"
subtitle: "Optional subtitle"
---

Story content here...
```

Images go in `assets/images/`.

## Strict Rules

1. **Categories**: Use only `short-story` or `essay`
2. **File Naming**: Posts must follow `YYYY-MM-DD-slug.md` format
3. **Always rebuild**: After any change, run `bundle exec jekyll build --destination ../stories`
4. **No Node.js**: Ruby/Jekyll only
