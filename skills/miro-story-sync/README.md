---
catalogue_summary: "Render and synchronize story-map Miro boards (outline today; exploration with acceptance criteria and prioritization increments planned) from story-graph.json. Reuses common/diagram_story_sync primitives and a pluggable MiroTransport (REST API v2 + in-memory fake)."
---

# miro-story-sync

## Overview

Render and synchronize story-map Miro boards from `story-graph.json`. Mirror
of **drawio-story-sync** for Miro; both skills share the
**`common/diagram_story_sync`** package (geometry, layout, comparison,
abstract diagram nodes) and only differ in how the rendered nodes are
materialised — DrawIO writes XML, Miro talks to the REST API.

_Maintainer / AI: expand this section once exploration / increments shipping
the second phase is in. The generator never overwrites an existing README;
`SKILL.md` stays authoritative for behaviour._

## How it fits together

```ascii
story-graph.json
           |
           v
  render -> MiroStoryMap -> MiroTransport.create_item(...) -> Miro Board
                              ^                                    |
                              |                                    v
                          InMemoryMiroTransport (tests) <----- RestMiroTransport
```

## Source

- [SKILL.md](SKILL.md)
- Regenerated site: `python agents/abd-practice-skill-builder/skills/abd-skill-catalog/scripts/generate_abd_catalog.py` from repo root.
