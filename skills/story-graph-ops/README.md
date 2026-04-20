---
# One line for catalogue cards and grids (YAML string).
catalogue_summary: "Create, read, update, and delete story-graph.json (whole file or parts—epics, sub-epics, stories, AC, scenarios) as a standalone artifact—no host app required. Agents must complete the ops loop: use this skill’s CLI or Python modules under scripts/, then validate the file—do not stop after …"
---

# story-graph-ops

## Overview

Create, read, update, and delete story-graph.json (whole file or parts—epics, sub-epics, stories, AC, scenarios) as a standalone artifact—no host app required. Agents must complete the ops loop: use this skill’s CLI or Python modules under scripts/, then validate the file—do not stop after hand-writing JSON from memory or from reading other repositories for “schema hints.” Prefer the story-graph CLI; use story_map and related modules for richer edits. Complements ABD practice skills—ops skill owns the serialized graph lifecycle on disk.

_Maintainer / AI: expand this section; it becomes the HTML **Description**. If the whole README is still a stub or wrong, replace the file after reading `SKILL.md` — the generator never overwrites an existing README. `SKILL.md` stays authoritative for behaviour._

## How it fits together

_Put one ASCII diagram in the fenced block below (flow, triggers, artifacts). The catalogue renders this block literally in a `<pre>`._

```ascii
story-graph.json (file)
           |
           v
  read / validate -----> filter (increment, scope) -----> JSON fragments for tools
```

## Source

- [SKILL.md](SKILL.md)
- Regenerated site: `python skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
