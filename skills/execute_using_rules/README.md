---
# One line for catalogue cards and grids (YAML string).
catalogue_summary: "Bundle rules into SKILL.md, run scanners, quality steps (rules before work), and the correction process after mistakes — commands first, details after."
---

# execute-rules

## Overview

Bundle rules into SKILL.md, run scanners, quality steps (rules before work), and the correction process after mistakes — commands first, details after.

_Maintainer / AI: expand this section; it becomes the HTML **Description**. If the whole README is still a stub or wrong, replace the file after reading `SKILL.md` — the generator never overwrites an existing README. `SKILL.md` stays authoritative for behaviour._

## How it fits together

_Put one ASCII diagram in the fenced block below (flow, triggers, artifacts). The catalogue renders this block literally in a `<pre>`._

```ascii
rules/*.md (DO / DON'T)
           |
           v
  scanners / checks -----> violations list -----> correction loop
```

## Source

- [SKILL.md](SKILL.md)
- Regenerated site: `python agents/abd-practice-skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
