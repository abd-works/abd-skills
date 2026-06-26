#!/usr/bin/env bash
#
# deploy-mojibake-guard.sh — Install mojibake detection across all repos
#
# SYNOPSIS
#   ./deploy-mojibake-guard.sh [--local | --ci | --all] [repo-root ...]
#
# DESCRIPTION
#   Two-layer defense against UTF-8 mojibake:
#
#   --ci    Deploys the GitHub Actions workflow to .github/workflows/.
#           Blocks PRs/merges that contain garbled text.
#           Works org-wide when placed in abd-works/.github repo.
#
#   --local Installs a git pre-commit hook that blocks commits
#           containing mojibake before they reach the remote.
#
#   --all   Both (default).
#
#   When repo roots are given, deploys to those. Otherwise scans
#   the current directory for git repos.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:---all}"
shift 2>/dev/null || true

# --- Locate source files ---
WORKFLOW_SRC="$SCRIPT_DIR/mojibake-check.yml"
HOOK_SRC="$SCRIPT_DIR/pre-commit-mojibake.sh"

if [[ ! -f "$WORKFLOW_SRC" ]]; then
    echo "Error: $WORKFLOW_SRC not found." >&2
    exit 1
fi
if [[ ! -f "$HOOK_SRC" ]]; then
    echo "Error: $HOOK_SRC not found." >&2
    exit 1
fi

# --- Collect repos ---
REPOS=()
if [[ $# -gt 0 ]]; then
    REPOS=("$@")
else
    # Find all git repos in the current directory tree
    while IFS= read -r d; do
        REPOS+=("$(dirname "$d")")
    done < <(find . -maxdepth 3 -name '.git' -type d 2>/dev/null)
fi

if [[ ${#REPOS[@]} -eq 0 ]]; then
    echo "No git repos found." >&2
    exit 1
fi

do_ci() {
    local repo="$1"
    local dst="$repo/.github/workflows/mojibake-check.yml"
    mkdir -p "$(dirname "$dst")"
    cp "$WORKFLOW_SRC" "$dst"
    echo "  ✅ CI workflow → $dst"
}

do_local() {
    local repo="$1"
    local dst="$repo/.git/hooks/pre-commit"
    # If a pre-commit hook already exists, append ours as a segment
    if [[ -f "$dst" ]]; then
        if grep -q 'mojibake' "$dst" 2>/dev/null; then
            echo "  ⏭️  Pre-commit hook already has mojibake check — skipping"
            return
        fi
        echo "" >> "$dst"
        echo "# --- Mojibake guard (added by deploy-mojibake-guard.sh) ---" >> "$dst"
        cat "$HOOK_SRC" >> "$dst"
        echo "  ✅ Pre-commit hook (appended) → $dst"
    else
        cp "$HOOK_SRC" "$dst"
        chmod +x "$dst"
        echo "  ✅ Pre-commit hook → $dst"
    fi
}

echo ""
echo "Deploying mojibake guard ($(echo "$MODE" | tr -d '-'))"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

for repo in "${REPOS[@]}"; do
    if [[ ! -d "$repo/.git" ]]; then
        echo "⏭️  $repo — not a git repo, skipping"
        continue
    fi
    echo "📦 $repo"
    case "$MODE" in
        --ci)    do_ci "$repo" ;;
        --local) do_local "$repo" ;;
        --all|*) do_ci "$repo"; do_local "$repo" ;;
    esac
    echo ""
done

echo "Done. Mojibake guard deployed to ${#REPOS[@]} repo(s)."
