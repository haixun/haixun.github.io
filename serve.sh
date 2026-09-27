#!/bin/sh
# Preview the root site at http://localhost:4000 (auto-rebuilds on save).
# Uses the stories site's gems because the root Gemfile.lock pins gems that
# no longer install on current Ruby.
cd "$(dirname "$0")" || exit 1
BUNDLE_GEMFILE=_stories_src/Gemfile exec bundle exec jekyll serve "$@"
