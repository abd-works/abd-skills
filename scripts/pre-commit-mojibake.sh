#!/usr/bin/env bash
# pre-commit hook: block commits containing mojibake.
#
# Install: cp this file to .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
# Or:      git config core.hooksPath .githooks  (and place this in .githooks/)
# ------------------------------------------------------------------
set -euo pipefail

# Only check staged text files that are being committed
STAGED=$(git diff --cached --name-only --diff-filter=ACM)

if [[ -z "$STAGED" ]]; then exit 0; fi

# Same pattern as the CI workflow
MOJIBAKE_RE='(Ã©|Ã¨|Ã |Ã¡|Ã¢|Ã£|Ã¤|Ã¥|Ã¦|Ã§|Ã¨|Ã©|Ãª|Ã«|Ã¬|Ã­|Ã®|Ã¯|Ã°|Ã±|Ã²|Ã³|Ã´|Ãµ|Ã¶|Ã¹|Ãº|Ã»|Ã¼|Ã½|Ã¾|Ã¿|Ã€|Ã|Ã‚|Ãƒ|Ã„|Ã…|Ã†|Ã‡|Ãˆ|Ã‰|ÃŠ|Ã‹|ÃŒ|Ã|ÃŽ|Ã|Â©|Â®|Â°|Â±|Â²|Â³|Â´|Âµ|Â¶|Â·|Â¸|Â¹|Âº|Â»|Â¼|Â½|Â¾|â€™|â€œ|â€\x9d|â€"|â€"|â€"|"|"|'|'|â€¦|â€¹|â€›|â‚¬|â„¢|Ã\x83|Ã\x82)'

FOUND=0
while IFS= read -r file; do
    # Skip binary files
    if ! file "$file" 2>/dev/null | grep -q 'text'; then continue; fi
    # Check only text-like extensions
    case "$file" in
        *.md|*.json|*.yaml|*.yml|*.txt|*.py|*.ts|*.js|*.mdc|*.html|*.css|*.sh|*.ps1|*.toml|*.cfg)
            # Check the staged content (not the working copy)
            if git show ":$file" 2>/dev/null | grep -qP "$MOJIBAKE_RE"; then
                echo "❌ Mojibake detected in: $file"
                git show ":$file" 2>/dev/null | grep -nP "$MOJIBAKE_RE" | head -5
                FOUND=1
            fi
            ;;
    esac
done <<< "$STAGED"

if [[ "$FOUND" -eq 1 ]]; then
    echo ""
    echo "========================================="
    echo "  Commit blocked: mojibake detected.     "
    echo "  Fix the garbled text and try again.    "
    echo "========================================="
    exit 1
fi

exit 0
