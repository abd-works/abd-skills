#!/usr/bin/env bash
#
# org-deploy-mojibake-guard.sh — Roll out mojibake detection across ALL abd-works repos
#
# SYNOPSIS
#   ./org-deploy-mojibake-guard.sh
#
# DESCRIPTION
#   Three-layer org-wide mojibake defense:
#
#   1. Pushes the reusable workflow to abd-works/.github repo
#   2. Pushes a thin caller workflow to every other repo in the org
#   3. Prints instructions for the org-level branch protection ruleset
#
# PREREQUISITES
#   - gh CLI authenticated with org admin scope
#   - Push access to abd-works/.github repo
#
# ------------------------------------------------------------------
set -euo pipefail

ORG="abd-works"
ORG_DOT_GITHUB_REPO="$ORG/.github"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Source file for the reusable workflow
REUSABLE_SRC="$SCRIPT_DIR/mojibake-check.yml"
if [[ ! -f "$REUSABLE_SRC" ]]; then
    echo "Error: $REUSABLE_SRC not found." >&2
    exit 1
fi

# Thin caller workflow (placed in each consumer repo)
CALLER_WORKFLOW=$(cat <<'YAML'
# Auto-deployed by org-deploy-mojibake-guard.sh
# Calls the org-wide reusable workflow from abd-works/.github
name: Mojibake check

on:
  push:
    branches: [main, master]
    paths:
      - '**/*.md'
      - '**/*.json'
      - '**/*.yaml'
      - '**/*.yml'
      - '**/*.txt'
      - '**/*.py'
      - '**/*.ts'
      - '**/*.js'
      - '**/*.mdc'
  pull_request:
    paths:
      - '**/*.md'
      - '**/*.json'
      - '**/*.yaml'
      - '**/*.yml'
      - '**/*.txt'
      - '**/*.py'
      - '**/*.ts'
      - '**/*.js'
      - '**/*.mdc'

jobs:
  mojibake:
    uses: abd-works/.github/.github/workflows/mojibake-check.yml@main
YAML
)

# =====================================================================
# STEP 1: Push reusable workflow to abd-works/.github
# =====================================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Step 1: Reusable workflow in $ORG_DOT_GITHUB_REPO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Create a temp clone
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

echo "  Cloning $ORG_DOT_GITHUB_REPO..."
if ! gh repo clone "$ORG_DOT_GITHUB_REPO" "$TMPDIR/.github" -- --depth=1 2>/dev/null; then
    echo "  ⚠️  $ORG_DOT_GITHUB_REPO doesn't exist yet."
    echo "  Creating it..."
    gh repo create "$ORG_DOT_GITHUB_REPO" --public --description "Org-wide defaults and shared workflows for $ORG"
    gh repo clone "$ORG_DOT_GITHUB_REPO" "$TMPDIR/.github" -- --depth=1
fi

mkdir -p "$TMPDIR/.github/.github/workflows"
cp "$REUSABLE_SRC" "$TMPDIR/.github/.github/workflows/mojibake-check.yml"

cd "$TMPDIR/.github"
if git diff --quiet 2>/dev/null; then
    echo "  ⏭️  Reusable workflow already up to date."
else
    git add .github/workflows/mojibake-check.yml
    git commit -m "feat: add org-wide mojibake detection workflow"
    git push
    echo "  ✅ Reusable workflow pushed."
fi

# =====================================================================
# STEP 2: Push caller workflow to every repo in the org
# =====================================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Step 2: Caller workflows in all $ORG repos"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# List all repos in the org (excluding .github itself)
REPOS=$(gh repo list "$ORG" --limit 500 --json name,isEmpty --jq '.[] | select(.isEmpty == false) | .name')

COUNT=0
SKIPPED=0

for repo_name in $REPOS; do
    full_repo="$ORG/$repo_name"
    # Skip the .github repo (it has the reusable workflow, not a caller)
    [[ "$repo_name" == ".github" ]] && continue

    # Check if caller workflow already exists
    existing=$(gh api "repos/$full_repo/contents/.github/workflows/mojibake.yml" 2>/dev/null \
        | python3 -c "import json,sys; print(json.load(sys.stdin).get('content',''))" 2>/dev/null \
        | base64 -d 2>/dev/null || true)

    if [[ -n "$existing" ]]; then
        SKIPPED=$((SKIPPED + 1))
        echo "  ⏭️  $full_repo — already has mojibake.yml"
        continue
    fi

    # Create via GitHub API (no local clone needed)
    ENCODED=$(echo "$CALLER_WORKFLOW" | base64)
    gh api "repos/$full_repo/contents/.github/workflows/mojibake.yml" \
        -X PUT \
        -f message="ci: add mojibake detection (org-wide)" \
        -f content="$ENCODED" \
        -f branch="$(gh repo view "$full_repo" --json defaultBranchRef -q .defaultBranchRef.name)" \
        --silent 2>/dev/null

    COUNT=$((COUNT + 1))
    echo "  ✅ $full_repo — mojibake.yml added"
done

echo ""
echo "  Pushed to $COUNT repo(s), skipped $SKIPPED (already had it)."

# =====================================================================
# STEP 3: Org branch protection (manual instructions)
# =====================================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Step 3: Org-level enforcement (manual)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Go to: https://github.com/organizations/$ORG/settings/rules"
echo ""
echo "  Create a Repository ruleset:"
echo "    1. Name: 'Mojibake guard'"
echo "    2. Target: All repositories (or select specific ones)"
echo "    3. Rules → Add rule → 'Require a status check to pass'"
echo "    4. Status check name: 'Detect mojibake (UTF-8 garble)'"
echo "    5. Check 'Require branches to be up to date'"
echo "    6. Save"
echo ""
echo "  This makes the mojibake check a HARD GATE — no PR merges"
echo "  in any repo unless the check passes."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Done. $COUNT repos now have mojibake protection."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
