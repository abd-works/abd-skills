---
# One line for catalogue cards and grids (YAML string).
catalogue_summary: "{{CATALOGUE_SUMMARY}}"
---

# {{NAME}}

## Overview

{{OVERVIEW_STUB}}

_Maintainer / AI: expand this section; it becomes the HTML **Description**. If the whole README is still a stub or wrong, replace the file after reading `SKILL.md` — the generator never overwrites an existing README. `SKILL.md` stays authoritative for behaviour._

## How it fits together

_Put one ASCII diagram in the fenced block below (flow, triggers, artifacts). The catalogue renders this block literally in a `<pre>`._

```ascii
  inputs / context
        |
        v
  this skill (SKILL.md) -----> artifacts + feedback
```

## Source

- [SKILL.md](SKILL.md)
- Regenerated site: `python agents/abd-practice-skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
