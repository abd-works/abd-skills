---
name: abd-mojibake-guard
description: >-
  Scan and fix UTF-8 mojibake, U+FFFD, and BOM in text files after doc creation
  and before commit. Wraps scripts/scan_encoding.py, deploy-mojibake-guard.sh,
  pre-commit-mojibake.sh, and mojibake-check.yml. Use when generated markdown
  may be garbled, before committing docs, or when setting up encoding CI/hooks.
---
# abd-mojibake-guard

## Purpose

Keep repos free of **mojibake** (double-encoded UTF-8), **U+FFFD** replacement characters, and **UTF-8 BOM** in text deliverables.

Canonical tooling lives under **`scripts/`** at the abd-skills repo root; this skill wraps those scripts and documents when agents and humans must run them.

---

## Core concepts

### Mojibake

UTF-8 bytes misread as Latin-1 or Windows-1252, then saved again as UTF-8 — e.g. `â€™` instead of `'`, or garbled em-dashes and curly quotes. Breaks frontmatter, search, and catalog generation.

### Two-layer guard

| Layer | Script | When it runs |
| --- | --- | --- |
| **Local** | `pre-commit-mojibake.sh` (via `deploy-mojibake-guard.sh`) or `scan_encoding.py --staged --check` | Before commit |
| **CI** | `mojibake-check.yml` | Push / PR on text paths |

### Scan vs fix

| Mode | Command | Effect |
| --- | --- | --- |
| Scan | `run_encoding_guard.py scan` | Report issues; exit 0 |
| Fix | `run_encoding_guard.py fix` | Replace known mojibake, repair U+FFFD → em-dash, strip BOM |
| Check staged | `run_encoding_guard.py check-staged` | Exit 1 if staged files fail — use before commit |

---

## Agent Instructions

Read every file in **`rules/`** and **`guidance/abd-mojibake-guard.instructions.md`**.

### Operations

| Operation | Trigger |
| --- | --- |
| `scan` | After creating or bulk-editing docs; "check mojibake", "check encoding" |
| `fix` | Scan found issues; "fix mojibake", "remove mojibake", "clean encoding" |
| `check_staged` | Before commit; "ready to commit" on text changes |
| `install_guard` | New clone; "install mojibake guard", "set up encoding CI" |

### Process

1. **After doc create** — `scan`. Stop if clean.
2. **Fix** — `fix`, then `scan` again. Manually fix anything `--fix` cannot resolve.
3. **Before commit** — `check-staged`. Do not commit until it passes.
4. **Optional setup** — `install-guard` deploys CI workflow and pre-commit hook to the repo.

### Commands

From **abd-skills repo root**:

```bash
python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py scan
python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py fix
python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py check-staged
python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py install-guard
```

Direct equivalents:

```bash
python scripts/scan_encoding.py
python scripts/scan_encoding.py --fix
python scripts/scan_encoding.py --staged --check
bash scripts/deploy-mojibake-guard.sh --all .
```

**Install guard** requires Git Bash or WSL on Windows (`bash scripts/deploy-mojibake-guard.sh`). For Python-only pre-commit on Windows, use `./scripts/install-hooks.sh` (calls `scan_encoding.py --staged --check`).

### Slash / IDE assets

- **Instructions:** `guidance/abd-mojibake-guard.instructions.md`
- **Prompt:** `guidance/abd-mojibake-guard.prompt.md` — "remove mojibake" / pre-commit cleanup

---

## Validate

- **Scan clean** — `scan` reports no issues (or only documented skip paths such as detector source files).
- **Fix applied** — after `fix`, re-scan shows fewer or zero mojibake / U+FFFD / BOM hits in edited deliverables.
- **Staged gate** — `check-staged` exits 0 before commit.
- **Guard deployed** — when requested, `.github/workflows/mojibake-check.yml` exists and pre-commit includes mojibake check.
