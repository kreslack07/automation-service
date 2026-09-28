#!/usr/bin/env bash
# GitHub Pages deploy helper.
# Requires gh CLI with kreslack07 logged in.
#
# Usage:
#   ./deployment/deploy.sh [target-branch]
#   Default target: gh-pages on kreslack07/automation-service
#
# Pre-requisites:
#   - gh auth login (kreslack07)
#   - git init in repo root
#   - gh repo create automation-service (or existing)

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DST_BRANCH="${1:-gh-pages}"

if ! command -v gh >/dev/null 2>&1; then
  echo "Missing gh CLI. Install: https://cli.github.com/"
  exit 1
fi

cd "$ROOT_DIR"

# Ensure index.html exists
if [[ ! -f "demo-site/index.html" ]]; then
  echo "Missing demo-site/index.html"
  exit 1
fi

# Remove stale gh-pages branch if present, then recreate
git branch -D "$DST_BRANCH" >/dev/null 2>&1 || true
git checkout --orphan "$DST_BRANCH"
git reset --hard
git clean -fdx
cp demo-site/index.html index.html
cp README.md README.md

git add -A
git commit -m "feat: deploy automation-service landing page"

# Push to remote (kreslack07/automation-service or equivalent)
if git remote get-url origin >/dev/null 2>&1; then
  git push -u origin "$DST_BRANCH" --force
  echo "Pushed to origin:$DST_BRANCH"
else
  echo "No origin remote - push manually to kreslack07/automation-service"
fi

# Enable GitHub Pages branch
gh api "repos/kreslack07/automation-service/pages" -X POST \
  -F source='{"branch":"gh-pages","path":"/"}' \
  -f _method=PUT >/dev/null 2>&1 || echo "Could not enable Pages - do it manually in GitHub repo Settings > Pages."

git checkout -

# Expected outcome:
#   - gh-pages branch with index.html on kreslack07/automation-service
#   - GitHub Pages enabled (or manual step remaining)
#   - Site live at https://kreslack07.github.io/automation-service/
