---
description: Persist story-skill markdown changes to story-graph.json using story-graph-ops
---

Save the current story-skill markdown output to `story-graph.json` using **story-graph-ops** (`skills/story-driven-delivery/story-graph-ops/SKILL.md`).

1. **Never hand-edit** `story-graph.json` — use `story_graph_cli.py write` then `read` to validate.
2. Ask the user before saving if `story_ops` gate is set to `prompt`.
3. After saving, check for companion Draw.io diagrams and offer to re-render via **drawio-story-sync**.
