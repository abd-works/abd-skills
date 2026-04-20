---
name: drawio-story-sync
description: >-
  Render and synchronize story-map DrawIO diagrams (outline, exploration with acceptance
  criteria, prioritization increments) from story-graph.json. Uses **story-graph-ops**
  for validated JSON load/save and **story_graph_ops** (StoryMap, nodes, domain) for the
  story tree that DrawIO rendering expects. Use when producing or diffing story-map.drawio
  files, or when wiring CI/scripts for diagram refresh and update reports.
---

# drawio-story-sync

## What this skill owns

- Python package **`drawio_story_sync/`** (under `scripts/`) — DrawIO story map render, layout extraction, and update-report generation (story diagrams only; CRC / map-model DrawIO helpers are not bundled here).
- CLI **`scripts/drawio_story_sync_cli.py`**: `render`, `save-layout`, `report`, **`apply-report`** (writes graph via **story_graph_ops**; no DrawIO read).

## Story diagram kinds

| Workflow | `renderer_command` | CLI `--mode` aliases | Output role |
| --- | --- | --- | --- |
| Outline | `render-outline` (default) | `outline`, `story-map` | Epic / sub-epic / story map |
| Exploration | `render-exploration` | `exploration`, `acceptance-criteria` | Outline plus AC boxes |
| Prioritization | `render-increments` | `increments`, `prioritization`, `thin-slices` | Outline base plus increment lanes |

## Dependencies (PYTHONPATH)

1. **This skill’s `scripts/` directory** (so `import drawio_story_sync` works).
2. **story-graph-ops** `scripts/` — auto-prepended by `drawio_story_sync._bootstrap` and `story_io_synchronizer` when the sibling skill exists at `skills/story-graph-ops/scripts`. You can add it explicitly to `PYTHONPATH` if your layout differs.

DrawIO code imports **`story_graph_ops`** (same domain types as **story-graph-ops**): `StoryMap`, `Epic`, `SubEpic`, `Story`, `StoryGroup`, `StoryNode`, `DomainConcept`, `StoryUser`, etc.

## story-graph-ops integration

- **`load_story_graph_json`** in `story_io_synchronizer.py` calls **`story_graph_file.load_story_graph_dict`** when **story-graph-ops** is importable, so the same walk validation as **story-graph-ops** applies before building `StoryMap`.

## Commands

```text
python drawio_story_sync_cli.py render --mode outline --graph <path/to/story-graph.json> --out <path/out.drawio>
python drawio_story_sync_cli.py render --mode exploration --graph ... --out ...
python drawio_story_sync_cli.py render --mode increments --graph ... --out ...
python drawio_story_sync_cli.py save-layout --drawio <path/file.drawio>
python drawio_story_sync_cli.py report --drawio <path/file.drawio> --graph <path/story-graph.json> [--scope "Node Name"]
python drawio_story_sync_cli.py apply-report --graph <path/story-graph.json> --report <path/*-update-report.json> [--dry-run]
```

`report` writes `<stem>-extracted.json` and `<stem>-update-report.json` beside the diagram.

`apply-report` loads the report JSON and applies it with **`story_graph_ops.StoryMap.apply_update_report`**, then saves `story-graph.json` (unless `--dry-run`).

## Agent checklist

1. Put **this** `scripts/` and **story-graph-ops** `scripts/` on `PYTHONPATH` (or rely on sibling auto-insert).
2. Run **`story_graph_cli.py read --file story-graph.json`** from **story-graph-ops** after any hand-edited graph write (per **story-graph-ops** obligations).
3. For merges back into the graph from a report, run **`apply-report`** (or call **`story_graph_ops`** from Python). Report generation stays in this skill; apply uses **story-graph-ops** only.

## See also

- **story-graph-ops** — canonical read/write/validate for `story-graph.json` and **`story_graph_ops`** domain model.
