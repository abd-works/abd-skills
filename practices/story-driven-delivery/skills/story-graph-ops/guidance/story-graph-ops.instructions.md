# story-graph-ops — keep the graph in sync (always-on)

## Golden rule

**NEVER hand-edit `story-graph.json` directly.** Always use the **story-graph-ops** skill's CLI or Python modules (`scripts/story_graph_cli.py`, `story_map` package). Read the skill: **`../skills/story-graph-ops/SKILL.md`**.

## When a story-skill writes or changes a Markdown deliverable

After any skill that produces story-map, thin-slicing, or acceptance-criteria markdown:

1. **Ask the user** whether to save changes to `story-graph.json` — default is to prompt (`story_ops: prompt`).
   - If the user has previously said **"auto"** in this session → save without asking.
   - If the user has previously said **"don't"** or **"no"** → skip.
2. Use **story-graph-ops** tooling to persist the changes (CLI `write` / `read`, or Python `story_map` modules).
3. **Validate** with `story_graph_cli.py read --file <path>` — do not declare done without validation.

## When `story-graph.json` is updated

After any successful update to `story-graph.json`, check whether companion **Draw.io diagrams** exist alongside it.

- If diagrams exist → **ask the user** whether to re-render them (`drawio_render: yes` by default).
- Use the **drawio-story-sync** skill for rendering — read **`../skills/drawio-story-sync/SKILL.md`**.
