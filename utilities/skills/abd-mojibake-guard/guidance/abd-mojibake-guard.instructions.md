# Mojibake guard — agent instructions

Apply after **document creation** and **before commit** in any abd-skills repo (or repo where the guard is deployed).

## When to run

| Trigger | Action |
| --- | --- |
| Finished generating `.md`, `.mdc`, catalog HTML sources, prompts, instructions, YAML, or JSON | **Scan** |
| User says "check encoding", "check mojibake" | **Scan** |
| Scan reports issues | **Fix**, then **Scan** again |
| User is about to commit or says "ready to commit" | **Check staged** |
| New clone / new repo needs protection | **Install guard** |

## Commands (from abd-skills repo root)

```bash
# Report all encoding issues
python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py scan

# Auto-fix mojibake, U+FFFD → em-dash, strip BOM
python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py fix

# Pre-commit gate — staged files only
python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py check-staged

# Deploy CI + pre-commit to repo(s)
python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py install-guard
```

Direct scripts (same behavior):

| Script | Role |
| --- | --- |
| `scripts/scan_encoding.py` | Scan, `--fix`, `--staged --check` |
| `scripts/deploy-mojibake-guard.sh` | Install workflow + hook |
| `scripts/pre-commit-mojibake.sh` | Bash pre-commit hook source |
| `scripts/mojibake-check.yml` | GitHub Actions reusable workflow |

## Agent workflow

1. **After doc create** — run **scan**. If clean, stop.
2. **If issues** — run **fix**, then **scan** again. Report files changed and any remaining issues (binary previews may legitimately contain `�`).
3. **Before commit** — run **check-staged**. If it fails, fix affected staged files and re-run until clean.
4. **Manual review** — for U+FFFD replacements, confirm em-dash is correct in context; re-read sentences that had replacement characters.

## What counts as mojibake

UTF-8 text that was misread as Latin-1/Windows-1252 and re-saved — e.g. `â€™` instead of `'`, garbled em-dashes and curly quotes. Also flag UTF-8 BOM and lone U+FFFD replacement characters.
