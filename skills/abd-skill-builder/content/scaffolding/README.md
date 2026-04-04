# Scaffolding content

This folder contains standalone reference files that are **copied into a new skill** during scaffolding. They are the clean, author-facing standards set a skill builder drops into place.

Copies of these files are also maintained in `content/parts/library/` where the `abd-skill-builder` agent itself reads them as part of its own phase bundles. Duplication is intentional — each copy has its own job.

## Files

| File | Where it goes in a new skill | Purpose |
|------|------------------------------|---------|
| `authoring-checklist.md` | `docs/skill-plan.md` (Authoring checklist section) | Human + AI checklist to track skill build progress |
| `documentation-standards.md` | `content/parts/library/` | Voice, where content belongs, process table rules |
| `process-table-standards.md` | `content/parts/library/` | Column definitions and workspace row requirements for `process.md` |
| `skill-repo-standards.md` | `content/parts/library/` | Layout index: entry, operator config, delivery, phases, rules, scripts |
| `skill-standards-section-3.md` | `content/parts/library/` | Full normative §3 — directory conventions, rule naming, assembly |
| `rules-and-automated-checks.md` | `content/parts/library/` | Wiring rules, `scanners.json`, `build_pipeline`, `operator.scanners` |
| `process-approach.md` | `content/parts/library/` | IDE usage model, code phases vs AI-chat phases, `generate_prompt` |
| `delivery-modes.md` | `content/parts/library/` | `static_built` vs `runtime_injection` delivery modes |

## Usage

`scripts/scaffold_skill.py` (or equivalent) copies these into the target skill tree. After copying, the new skill's author owns those files — edits to this folder do not automatically propagate to existing skills.
