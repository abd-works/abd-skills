# drawio-story-sync — keep diagrams in sync (always-on)

## When `story-graph.json` changes and diagrams exist

After `story-graph.json` is updated (by any means — story-graph-ops CLI, Python script, or skill pipeline):

1. Check whether companion Draw.io diagrams exist beside the graph file (outline, exploration, increments, per-increment AC exploration).
2. If they exist → **ask the user** whether to re-render. Default: `drawio_render: yes`.
   - If the user has previously said **"auto"** in this session → render without asking.
   - If the user has previously said **"don't"** or **"no"** → skip.
3. Use the **drawio-story-sync** skill's CLI to render. Read the skill: **`skills/story-driven-delivery/drawio-story-sync/SKILL.md`**.

## When a Draw.io outline diagram is saved or edited

If the user saves or edits an **outline** `.drawio` file and a companion `story-graph.json` exists:

1. **Ask the user** whether to sync diagram changes back to `story-graph.json` (`drawio_sync: prompt` by default).
2. Use `drawio_story_sync_cli.py sync` — companion diagrams (exploration, increments) are automatically refreshed.

## Rendering rule

Always use the **drawio-story-sync** skill's CLI (`drawio_story_sync_cli.py render` or `sync`) — never hand-build `.drawio` XML.
