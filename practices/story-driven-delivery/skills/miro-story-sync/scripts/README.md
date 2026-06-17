# miro-story-sync scripts

- **`miro_story_sync/`** — Miro story-map package (transport, items, nodes, orchestrator).
- **`miro_story_sync_cli.py`** — CLI entrypoint (`render` today; `report` /
  `apply-report` / `sync` planned to mirror **drawio-story-sync**).

Run with `PYTHONPATH` including `common/` (repo root), this directory, and
**story-graph-ops** `scripts/` (`skills/story-graph-ops/scripts`). See
`../SKILL.md`. Use `--dry-run` to render via the in-memory transport without
contacting Miro.
