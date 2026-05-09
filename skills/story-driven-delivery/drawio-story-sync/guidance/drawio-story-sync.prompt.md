---
description: Render or sync Draw.io story diagrams from story-graph.json using drawio-story-sync
---

Render or sync Draw.io diagrams using **drawio-story-sync** (`skills/story-driven-delivery/drawio-story-sync/SKILL.md`).

1. **Never hand-build `.drawio` XML** — always use `drawio_story_sync_cli.py render` or `sync`.
2. To render after a graph change: `drawio_story_sync_cli.py render` (gate: `drawio_render`).
3. To sync diagram edits back to JSON: `drawio_story_sync_cli.py sync` (gate: `drawio_sync`).
4. After `sync`, companion diagrams refresh automatically — no separate render step needed.
