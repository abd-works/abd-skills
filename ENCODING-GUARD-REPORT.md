# Content Guard — Setup Report

**Date:** 2026-06-16  
**Repo:** abd-works/abd-skills  
**Branch:** main

---

## Issues found and fixed

### Encoding issues

| Category | Instances | Files affected | Resolution |
|----------|----------|----------------|------------|
| **UTF-8 BOM** | 188 | 188 | Auto-stripped (`--fix-bom`) |
| **Mojibake — right double quote (`"`)** | 259 | 17 | Replaced with correct Unicode |
| **Mojibake — left double quote (`"`)** | 14 | 5 | Replaced with correct Unicode |
| **U+FFFD replacement char (``)** | 172 | 13 | Replaced with em-dash (`—`) |
| **U+FFFD in binary previews** | 21 | 1 | Skipped (not a real issue) |
| **Encoding subtotal** | **654** | **203 files** | |

### Deploy-path issues

| Category | Instances | Files affected | Resolution |
|----------|----------|----------------|------------|
| **Hardcoded `.cursor/skills/`** | 30+ | 10 | Changed to `../skills/` |
| **Bare `skills/` without `../`** | 22 | 12 | Changed to `../skills/` |
| **`~/../skills/` paths** | 4 | 3 | Changed to `../skills/` |
| **Deploy-path subtotal** | **56+** | **19 files** | |

**Total: 222 files changed, 2856 insertions, 2782 deletions.**

### Root causes

**Mojibake:** UTF-8 text (smart quotes, em-dashes, bullets, ellipses) was misread as Windows-1252 or ISO-8859-1, then re-saved as UTF-8 — producing double-encoded byte sequences like `â€™` instead of `'`.

**U+FFFD:** Original bytes were lost during a previous encoding conversion. The replacement character `` (U+FFFD) was inserted as a placeholder. Context analysis showed these were all em-dashes (`—`), so they were repaired automatically. The 21 remaining in `catalog/outline.md` are binary file previews (PNG/DOCX) and are not real encoding issues.

**Deploy paths:** Prompt and instruction files used hardcoded `.cursor/skills/` paths that only work for Cursor deployment. When deployed to VS Code (`.github/prompts/`), these paths don't resolve. Fixed by using IDE-agnostic relative paths (`../skills/<name>/SKILL.md`) that work from both `.cursor/commands/` and `.github/prompts/`.

---

## Guard infrastructure created

### 1. Versioning (`VERSION` file)

Single source of truth for the repo version. Displayed in the README header and included in deploy receipts.

| Component | Purpose |
|---|---|
| `VERSION` | Semver string (e.g. `1.0.0`) |
| `README.md` | `<!-- VERSION -->X.Y.Z<!-- /VERSION -->` marker |
| CI check | Fails if new skills/agents/prompts are added without bumping VERSION |

### 2. Deploy manifest (`scripts/generate_manifest.py`)

Tracks what's deployed to each target workspace:

| Feature | How it works |
|---|---|
| **Manifest** | Commit hash, version, file inventory with SHA-256 hashes |
| **Deploy receipt** | `.abd-deploy.json` written to target workspace after each deploy |
| **Delta detection** | Compares source manifest vs deployed receipt |
| **Status check** | `--status` / `-Status` flag shows what's current or changed |

### 3. Scanner (`scripts/scan_encoding.py`)

CLI tool that detects and optionally fixes encoding issues in `.md` / `.mdc` files.

| Mode | Purpose |
|------|---------|
| `--check` | Exit non-zero if issues found (for CI/hooks) |
| `--fix` | Auto-fix all: mojibake → correct Unicode, U+FFFD → em-dash, strip BOM |
| `--fix-bom` | Strip BOM only |
| `--staged` | Scan only staged files (for pre-commit) |

### 2. Validation test (`tests/test_deploy_paths.py`)

8 checks that enforce IDE-agnostic conventions for all new content:

| Check | What it catches |
|---|---|
| No hardcoded `.cursor/skills/` | Cursor-only paths in dual-deployed files |
| No bare `skills/` paths | Missing `../` prefix |
| No `~/../skills/` paths | Incorrect home-relative paths |
| No mojibake | Double-encoded Unicode |
| No U+FFFD | Irrecoverable encoding corruption |
| No UTF-8 BOM | Byte-order mark |
| SKILL.md frontmatter | Missing `name` or `description` |
| Agent entry files | Agent dirs without AGENT.md/AGENTS.md |

### 3. Pre-commit hook (`scripts/hooks/pre-commit`)

Blocks commits that introduce encoding issues in staged `.md` / `.mdc` files.

Install: `./scripts/install-hooks.sh`

### 4. GitHub Actions (`.github/workflows/encoding-guard.yml`)

Runs both the encoding scan and deploy-path validation on every push/PR to `main`.

---

## Slash command / Codespaces investigation

### Findings

1. **Encoding corruption in SKILL.md frontmatter** — The `name:` and `description:` fields in YAML frontmatter contained mojibake and U+FFFD, which would break slash command parsing. **Fixed** by the encoding repair.

2. **Hardcoded `.cursor/` paths in prompt/instruction files** — Files deployed to both IDEs referenced `.cursor/skills/` which doesn't exist after VS Code deployment. **Fixed** by using `../skills/` relative paths.

3. **No `.devcontainer` configuration** — Codespaces has no auto-setup to run the deploy script. Skills must be deployed manually after opening a Codespace.

### Recommendation

Create a `.devcontainer/devcontainer.json` that runs the deploy script on Codespace creation, so skills are automatically available for slash command invocation.

---

## Files created/modified

| File | Action |
|------|--------|
| `VERSION` | Created — semver version file |
| `scripts/generate_manifest.py` | Created — manifest generator with delta detection |
| `scripts/scan_encoding.py` | Created — encoding scanner |
| `tests/test_deploy_paths.py` | Created — deploy-path, encoding, structure, and version validation |
| `scripts/hooks/pre-commit` | Created — pre-commit hook |
| `scripts/install-hooks.sh` | Created — hook installer |
| `.github/workflows/encoding-guard.yml` | Created — CI workflow (scan + test) |
| `README.md` | Updated — version display, encoding guard, deploy docs |
| `scripts/deploy-skills.sh` | Updated — pre-deploy checks, status, receipt writing |
| `scripts/deploy-skills.ps1` | Updated — pre-deploy checks, status, receipt writing |
| 203 `.md` / `.mdc` files | Fixed — encoding issues |
| 19 `.prompt.md` / `.instructions.md` files | Fixed — deploy paths |
