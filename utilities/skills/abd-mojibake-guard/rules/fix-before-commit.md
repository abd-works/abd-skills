# Fix before commit

**DO** — Before every commit that touches text files, run the staged check:

```bash
python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py check-staged
```

Or from repo root:

```bash
python scripts/scan_encoding.py --staged --check
```

**DO** — When issues are found, auto-fix when safe, then re-scan:

```bash
python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py fix
python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py scan
```

**DO** — Install repo guards once per clone (CI workflow + pre-commit):

```bash
python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py install-guard
```

This copies `scripts/mojibake-check.yml` to `.github/workflows/` and installs `scripts/pre-commit-mojibake.sh` via `scripts/deploy-mojibake-guard.sh`.

Alternative pre-commit (scan_encoding-based): `./scripts/install-hooks.sh` from repo root.

**DO NOT** — Commit with `--no-verify` to bypass encoding checks unless the user explicitly requests it and accepts the risk.

**DO NOT** — Hand-edit garbled byte sequences without re-running scan — fix the file encoding or use `--fix`, then verify the intended Unicode character appears.
