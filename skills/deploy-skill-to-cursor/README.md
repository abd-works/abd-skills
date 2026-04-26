---
# One line for catalogue cards and grids (YAML string).
catalogue_summary: "Deploy a skill from agilebydesign-skills into Cursor's user skills folder using a Windows directory junction (no duplicate copy). Run scripts/Deploy-SkillToCursor.ps1 with the skill folder name. Use when you want the global Cursor skills path to point at the repo canonical skill."
---

# deploy-skill-to-cursor

## Overview

Deploy a skill from agilebydesign-skills into Cursor's user skills folder using a Windows directory junction (no duplicate copy). Run scripts/Deploy-SkillToCursor.ps1 with the skill folder name. Use when you want the global Cursor skills path to point at the repo canonical skill.

_Maintainer / AI: expand this section; it becomes the HTML **Description**. If the whole README is still a stub or wrong, replace the file after reading `SKILL.md` — the generator never overwrites an existing README. `SKILL.md` stays authoritative for behaviour._

## How it fits together

_Put one ASCII diagram in the fenced block below (flow, triggers, artifacts). The catalogue renders this block literally in a `<pre>`._

```ascii
skill folder (SKILL.md + assets)
           |
           v
  package / validate -----> Cursor skills path -----> installed SKILL
```

## Source

- [SKILL.md](SKILL.md)
- Regenerated site: `python agents/abd-practice-skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
