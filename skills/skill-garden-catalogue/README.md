---
# One line for catalogue cards and grids (YAML string).
catalogue_summary: "Scan a folder of deployed skills and regenerate a one-pager Markdown inventory and an HTML catalogue. Each entry shows the challenge the skill addresses and the solution it provides, hyperlinked to the skill directory. Re-run on command to keep the catalogue current."
---

# skill-garden-catalogue

## Overview

Scan a folder of deployed skills and regenerate a one-pager Markdown inventory and an HTML catalogue. Each entry shows the challenge the skill addresses and the solution it provides, hyperlinked to the skill directory. Re-run on command to keep the catalogue current.

_Maintainer / AI: expand this section; it becomes the HTML **Description**. If the whole README is still a stub or wrong, replace the file after reading `SKILL.md` — the generator never overwrites an existing README. `SKILL.md` stays authoritative for behaviour._

## How it fits together

_Put one ASCII diagram in the fenced block below (flow, triggers, artifacts). The catalogue renders this block literally in a `<pre>`._

```ascii
repo skill roots
           |
           v
  scan SKILL.md -----> table / index -----> consumer (Cursor, docs)
```

## Source

- [SKILL.md](SKILL.md)
- Regenerated site: `python agents/abd-practice-skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
