---
# One line for catalogue cards and grids (YAML string).
catalogue_summary: "Render and synchronize story-map DrawIO diagrams (outline, exploration with acceptance criteria, prioritization increments) from story-graph.json. Uses story-graph-ops for validated JSON and story_graph_ops StoryMap for rendering. Use when …"
---

# drawio-story-sync

## Overview

Render and synchronize story-map DrawIO diagrams (outline, exploration with acceptance criteria, prioritization increments) from story-graph.json. Uses **story-graph-ops** for validated JSON load/save and **story_graph_ops** (`StoryMap` and related nodes) for the story tree DrawIO rendering uses.

_Maintainer / AI: expand this section; it becomes the HTML **Description**. If the whole README is still a stub or wrong, replace the file after reading `SKILL.md` — the generator never overwrites an existing README. `SKILL.md` stays authoritative for behaviour._

## How it fits together

_Put one ASCII diagram in the fenced block below (flow, triggers, artifacts). The catalogue renders this block literally in a `<pre>`._

```ascii
story-graph.json
           |
           v
  render / layout -----> *.drawio -----> extract / merge -----> graph updates
```

## Source

- [SKILL.md](SKILL.md)
- Regenerated site: `python agents/abd-practice-skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
