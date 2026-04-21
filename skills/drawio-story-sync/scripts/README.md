# drawio-story-sync scripts

- **`drawio_story_sync/`** — DrawIO story map package (render, layout, update reports).
- **`drawio_story_sync_cli.py`** — CLI entrypoint (`render`, `report`, `apply-report`, **`sync`**).

Run with `PYTHONPATH` including this directory and **story-graph-ops** `scripts/` (sibling `skills/story-graph-ops/scripts`). See **`../SKILL.md`**. Use **`sync`** to apply an outline `.drawio` to `story-graph.json` and re-render `<stem>-exploration.drawio` / `<stem>-increments.drawio`.
