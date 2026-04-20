---
name: drawio-story-sync
description: >-
  Render and synchronize story-map DrawIO diagrams (outline, exploration with acceptance
  criteria, prioritization increments) from story-graph.json. Uses **story-graph-ops** for
  validated JSON load/save and agile_bots **story_graph.nodes.StoryMap** for the rich domain
  tree DrawIO rendering expects. Use when producing or diffing story-map.drawio files outside
  the story bot, or when wiring CI/scripts for diagram refresh and update reports.
---

# drawio-story-sync

## What this skill owns

- Python package **`drawio_story_sync/`** (under `scripts/`) migrated from `agile_bots` `synchronizers/story_io` (story diagrams only; CRC / map-model DrawIO helpers are not bundled here).
- CLI **`scripts/drawio_story_sync_cli.py`**: `render`, `save-layout`, `report`, **`apply-report`** (writes graph via **story_graph_ops**; no DrawIO read).

## Story diagram kinds (same logic as story bot render specs)

| Bot / workflow | `renderer_command` | CLI `--mode` aliases | Output role |
| --- | --- | --- | --- |
| Shape outline | `render-outline` (default) | `outline`, `story-map` | Epic / sub-epic / story map |
| Exploration | `render-exploration` | `exploration`, `acceptance-criteria` | Outline plus AC boxes |
| Prioritization | `render-increments` | `increments`, `prioritization`, `thin-slices` | Outline base plus increment lanes |

## Dependencies (PYTHONPATH)

1. **This skill’s `scripts/` directory** (so `import drawio_story_sync` works).
2. **`agile_bots/src`** on `PYTHONPATH` so `from story_graph.nodes import StoryMap` and `story_graph.domain` resolve (DrawIO render code is built on that domain model).
3. **story-graph-ops** `scripts/` is auto-prepended by `drawio_story_sync.story_io_synchronizer` when it sits next to this skill under `skills/story-graph-ops/scripts`. You can also add it explicitly.

Optional: set **`AGILE_BOTS_SRC`** to the absolute path of `agile_bots/src` if the CLI default sibling lookup (`…/agile_bots/src` from repo root) does not match your layout.

## story-graph-ops integration

- **`load_story_graph_json`** in `story_io_synchronizer.py` calls **`story_graph_file.load_story_graph_dict`** when **story-graph-ops** is importable, so the same walk validation as **story-graph-ops** applies before building `StoryMap`.
- **`agile_bots`** `synchronizers/story_io/story_io_synchronizer.py` uses the same optional import so bots pick up validation when `story-graph-ops/scripts` is on `PYTHONPATH`.

## Commands

```text
python drawio_story_sync_cli.py render --mode outline --graph <path/to/story-graph.json> --out <path/out.drawio>
python drawio_story_sync_cli.py render --mode exploration --graph ... --out ...
python drawio_story_sync_cli.py render --mode increments --graph ... --out ...
python drawio_story_sync_cli.py save-layout --drawio <path/file.drawio>
python drawio_story_sync_cli.py report --drawio <path/file.drawio> --graph <path/story-graph.json> [--scope "Node Name"]
python drawio_story_sync_cli.py apply-report --graph <path/story-graph.json> --report <path/*-update-report.json> [--dry-run]
```

`report` writes `<stem>-extracted.json` and `<stem>-update-report.json` beside the diagram (same behavior as the bot’s **generateReport** path).

`apply-report` loads the report JSON and applies it with **`story_graph_ops.StoryMap.apply_update_report`**, then saves `story-graph.json` (unless `--dry-run`). **story-graph-ops** `scripts/` must be on `PYTHONPATH` (the synchronizer prepends the sibling skill automatically).

## Agent checklist

1. Set `PYTHONPATH` (see above).
2. Run **`story_graph_cli.py read --file story-graph.json`** from **story-graph-ops** after any hand-edited graph write (per **story-graph-ops** obligations).
3. For merges back into the graph from a report, run **`apply-report`** (or call **`story_graph_ops`** from Python). Report generation stays in this skill; apply uses **story-graph-ops** only.

## See also

- **story-graph-ops** — canonical read/write/validate for `story-graph.json`.
- **agile_bots** `src/synchronizers/story_io/README.md` — original design notes (still valid for behavior).
