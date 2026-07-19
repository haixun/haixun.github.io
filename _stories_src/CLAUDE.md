# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Writing portfolio site served at `haixun.github.io/stories`. Uses Jekyll with the Type-on-Strap remote theme, hosted on GitHub Pages.

## Development Commands

```bash
cd /Users/haixun/haixun.github.io/stories
bundle install
bundle exec jekyll serve --livereload    # Preview at http://localhost:4000/stories
bundle exec jekyll build
```

## Adding Content

1. Add metadata to `_data/stories.yml`:
   ```yaml
   - slug: the-last-train
     title: "The Last Train"
     category: short-story
     date: 2024-01-15
   ```

2. Create post in `_posts/` with filename `YYYY-MM-DD-slug.md`:
   ```markdown
   ---
   layout: post
   ---

   Your story content here...
   ```

The title and category come from `_data/stories.yml`, not the post's front matter.

## Directory Structure

- `_posts/`: Story and essay markdown files (naming: `YYYY-MM-DD-slug.md`)
- `_data/stories.yml`: Central metadata for all content
- `_layouts/`: Override theme layouts if needed
- `_config.yml`: Site config with remote theme

## Strict Rules

1. **No Custom Plugins**: Only GitHub Pages-supported plugins
2. **Categories**: `short-story` or `essay` only
3. **No Node.js**: Ruby/Jekyll only
4. **File Naming**: Posts must follow `YYYY-MM-DD-slug.md` format
