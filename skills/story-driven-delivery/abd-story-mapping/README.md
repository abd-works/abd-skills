---
# One line for catalogue cards and grids (YAML string).
catalogue_summary: "Teaches Patton-style story mapping: epics, sub-epics, stories, verb–noun naming, and actors via story_type. When building a map from sources, outputs all template artifacts in templates/ (currently story-map.md and story-map.txt) with the same tree — not one or the other. Use when structuring …"
---

# abd-story-mapping

## Overview

Teaches Patton-style story mapping: epics, sub-epics, stories, verb–noun naming, and actors via story_type. When building a map from sources, outputs all template artifacts in templates/ (currently story-map.md and story-map.txt) with the same tree — not one or the other. Use when structuring product discovery, decomposing user journeys, identifying epics and flows, story mapping, organizing requirements into a hierarchical map, or when the user mentions story maps, epics, sub-epics, or Jeff Patton–style backlog structure.

_Maintainer / AI: expand this section; it becomes the HTML **Description**. If the whole README is still a stub or wrong, replace the file after reading `SKILL.md` — the generator never overwrites an existing README. `SKILL.md` stays authoritative for behaviour._

## How it fits together

_Put one ASCII diagram in the fenced block below (flow, triggers, artifacts). The catalogue renders this block literally in a `<pre>`._

```ascii
discovery inputs (users, journey)
           |
           v
  templates/ -----> story-map.md / .txt -----> epics / sub-epics / stories
```

## Source

- [SKILL.md](SKILL.md)
- Regenerated site: `python agents/abd-practice-skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
