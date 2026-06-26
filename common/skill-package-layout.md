# Skill Package Layout

For scanners to run against a skill, the skill package must have this structure:

| Piece | Role |
| --- | --- |
| **`SKILL.md`** | Thin router: purpose, when-to-use, output file resolution, read-gates, validate gate. No inlined rule prose. |
| **`rules/<name>.md`** | **Source of truth** for rule prose — the only place rule text lives. |
| **`reference/*.md`** | Concept teaching, examples, heuristics — read on demand before authoring. |
| **`scanners/*-scanner.py`** | Optional: CLI entrypoint per concern (beside scanner modules); linked from rule frontmatter via `scanner:` |

---

## `## Diagram workflow` section in SKILL.md

Skills that produce a diagram deliverable include a `## Diagram workflow` section directly in `SKILL.md`. This section:

- States the output file path (relative to the deliverables folder).
- Provides the exact CLI command to run to generate or regenerate the diagram.
- Names the source-of-truth input (e.g. the markdown file or state JSON the CLI reads from).
- States when to run it (typically: once after the primary artifact is written; re-run whenever the source changes).

The diagram output is **not optional** — if the section exists, the file it describes must exist on disk before the task is marked done. Agents check for this section after the scanner pass and execute it as a background step (see `common/prompts/run-practice-skill.prompt.md` and `common/prompts/diagram-skill-output.prompt.md` step 3 and `common/prompts/diagram-skill-output.prompt.md`).

**Rule file → scanner linkage:** Put `scanner: <stem>` in the YAML frontmatter of `rules/<stem>.md`; the CLI script is expected at `scanners/<stem>-scanner.py`.

**Shared scanner bases** (`import scanner_bases`) are provided by `common/scripts/scanner_bases/` and are on `PYTHONPATH` when `run_scanners.py` runs. Story-domain types (`StoryScanner`, `StoryMap`, …) live in the sibling `story-graph-ops/scripts/` — not in `scanner_bases`.
