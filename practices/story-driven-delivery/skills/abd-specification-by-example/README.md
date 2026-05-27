---
# One line for catalogue cards and grids (YAML string).
catalogue_summary: "Produce specification-by-example scenarios: concrete Given/When/Then steps with real domain values, bold concept names, italic values. Two templates: plain scenarios (inline values, default) and outline (same steps, multiple data rows). Use when writing BDD scenarios, refining AC into specs, or …"
---

# abd-specification-by-example

## Overview

Write Given/When/Then scenarios that make a story's expected behavior concrete and testable, using real domain values and named outcomes so the team can verify what the system must do.

_Maintainer / AI: expand this section; it becomes the HTML **Description**. If the whole README is still a stub or wrong, replace the file after reading `SKILL.md` — the generator never overwrites an existing README. `SKILL.md` stays authoritative for behaviour._

## How it fits together

_Put one ASCII diagram in the fenced block below (flow, triggers, artifacts). The catalogue renders this block literally in a `<pre>`._

```ascii
behaviour examples (Given-When-Then)
           |
           v
  living documentation -----> automation hooks -----> regression safety
```

## Source

- [SKILL.md](SKILL.md)
- Regenerated site: `python agents/abd-practice-skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
