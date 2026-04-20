---
# One line for catalogue cards and grids (YAML string).
catalogue_summary: "Set and read the agent engagement root (skill-config.json → workspace.active_skill_workspace). Run scripts from this folder; they resolve the agent root automatically."
---

# workspace

## Overview

Set and read the agent engagement root (skill-config.json → workspace.active_skill_workspace). Run scripts from this folder; they resolve the agent root automatically.

_Maintainer / AI: expand this section; it becomes the HTML **Description**. If the whole README is still a stub or wrong, replace the file after reading `SKILL.md` — the generator never overwrites an existing README. `SKILL.md` stays authoritative for behaviour._

## How it fits together

_Put one ASCII diagram in the fenced block below (flow, triggers, artifacts). The catalogue renders this block literally in a `<pre>`._

```ascii
CLI / agent session
           |
           v
  workspace_skill -----> resolved workspace root -----> all paths relative to it
```

## Source

- [SKILL.md](SKILL.md)
- Regenerated site: `python skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
