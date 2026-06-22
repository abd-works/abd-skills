# Scan after doc create

**DO** — After creating or bulk-editing markdown, YAML, JSON, prompts, instructions, or catalog output, run an encoding scan before moving on.

```bash
python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py scan
```

Or from repo root:

```bash
python scripts/scan_encoding.py
```

**DO** — If the scan reports mojibake, U+FFFD replacement characters, or UTF-8 BOM, fix before commit — do not leave garbled text in deliverables.

**DO NOT** — Assume the editor saved UTF-8 correctly after paste from Word, PDF exports, or chat output.

**DO NOT** — Skip the scan because "it looks fine" — double-encoded smart quotes and em-dashes often render acceptably in some viewers but break search, frontmatter, and CI.
