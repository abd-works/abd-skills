# Skill Package Layout

For scanners to run against a skill, the skill package must have this structure:

| Piece | Role |
| --- | --- |
| **`SKILL.md`** | Thin router: purpose, when-to-use, output file resolution, read-gates, validate gate. No inlined rule prose. |
| **`rules/<name>.md`** | **Source of truth** for rule prose — the only place rule text lives. |
| **`reference/*.md`** | Concept teaching, examples, heuristics — read on demand before authoring. |
| **`scanners/*-scanner.py`** | Optional: CLI entrypoint per concern (beside scanner modules); linked from rule frontmatter via `scanner:` |

**Rule file → scanner linkage:** Put `scanner: <stem>` in the YAML frontmatter of `rules/<stem>.md`; the CLI script is expected at `scanners/<stem>-scanner.py`.

**Shared scanner bases** (`import scanner_bases`) are provided by `common/scripts/scanner_bases/` and are on `PYTHONPATH` when `run_scanners.py` runs. Story-domain types (`StoryScanner`, `StoryMap`, …) live in the sibling `story-graph-ops/scripts/` — not in `scanner_bases`.
