---
name: drawio-story-sync
catalog_garden_tier: foundational
catalogue_one_liner: >-
  story-graph.json to Draw.io story maps; validated load/save and diagram sync.
description: >-
  Renders and synchronizes story-map Draw.io diagrams (outline, exploration with acceptance
  criteria, prioritization increments) from story-graph.json. Use when producing or diffing
  story-map.drawio files, or when wiring CI/scripts for diagram refresh and update reports.
---

# drawio-story-sync

## What this skill owns

- Python package **`drawio_story_sync/`** (under `scripts/`) — DrawIO story map render, layout extraction, and update-report generation (story diagrams only; CRC / map-model DrawIO helpers are not bundled here).
- CLI **`scripts/drawio_story_sync_cli.py`**: `render`, `save-layout`, `report`, **`apply-report`**, **`sync`** (outline → graph + refresh companion diagrams).

## Story diagram kinds

| Workflow | `renderer_command` | CLI `--mode` aliases | Default output file |
| --- | --- | --- | --- |
| Outline | `render-outline` (default) | `outline`, `story-map` | `story-map.drawio` |
| Acceptance Criteria | `render-exploration` | `acceptance-criteria`, `exploration` | `acceptance-criteria.drawio` |
| Thin-slicing | `render-increments` | `thin-slicing`, `increments`, `prioritization`, `thin-slices` | `thin-slicing.drawio` |

## Dependencies (PYTHONPATH)

1. **This skill’s `scripts/` directory** (so `import drawio_story_sync` works).
2. **story-graph-ops** `scripts/` — auto-prepended by `drawio_story_sync._bootstrap` and `story_io_synchronizer` when the sibling skill exists at `skills/story-graph-ops/scripts`. You can add it explicitly to `PYTHONPATH` if your layout differs.

DrawIO code imports **`story_graph_ops`** (same domain types as **story-graph-ops**): `StoryMap`, `Epic`, `SubEpic`, `Story`, `StoryGroup`, `StoryNode`, `DomainConcept`, `StoryUser`, etc.

## story-graph-ops integration

- **`load_story_graph_json`** in `story_io_synchronizer.py` calls **`story_graph_file.load_story_graph_dict`** when **story-graph-ops** is importable, so the same walk validation as **story-graph-ops** applies before building `StoryMap`.

## Commands

```text
python drawio_story_sync_cli.py sync --drawio <path/story-map.drawio> --graph <path/story-graph.json>
python drawio_story_sync_cli.py render --mode outline            --graph <path/to/story-graph.json> --out <path/story-map.drawio>
python drawio_story_sync_cli.py render --mode acceptance-criteria --graph ... --out <path/acceptance-criteria.drawio>
python drawio_story_sync_cli.py render --mode thin-slicing        --graph ... --out <path/thin-slicing.drawio>
python drawio_story_sync_cli.py save-layout --drawio <path/file.drawio>
python drawio_story_sync_cli.py report --drawio <path/file.drawio> --graph <path/story-graph.json> [--scope "Node Name"]
python drawio_story_sync_cli.py apply-report --graph <path/story-graph.json> --report <path/*-update-report.json> [--dry-run]
```

### `sync` (preferred for outline edits)

Use **`sync`** when the **outline** diagram (`story-map.drawio` or any `<stem>.drawio`) is the source of truth for hierarchy/story renames **and**, where the diagram is explicit, for **personas** (`users`).

1. Runs the same **report** diff as `report` (writes `<stem>-extracted.json`, `<stem>-update-report.json`, updates `*-layout.json`). After a successful apply (not `--dry-run`), those three stem sidecars beside the synced diagram are **removed** so they do not go stale; use `report` alone if you need to keep them on disk.
2. **Applies** the report to **`story-graph.json`** (same as `apply-report`). **Personas:** chips use the same **actor** fill as the renderer (`STYLE_DEFAULTS` / serializer). Per leaf sub-epic row (left-to-right), a chip **above** a story column sets an explicit persona; following stories **inherit** until the next explicit. The report compares that row model to the graph using the **same forward-fill** on stored `users`, then applies changes. Rows with **no** persona chips leave JSON `users` untouched for those stories.
3. Re-renders **`acceptance-criteria.drawio`** and **`thin-slicing.drawio`** next to the outline so exploration/increment views match the graph and **do not undo** outline renames on a later apply.

Optional: `--no-refresh-diagrams` (graph only), `--out-exploration` / `--out-increments` (custom paths to override the default `acceptance-criteria.drawio` / `thin-slicing.drawio`), `--dry-run` (no file writes), `--scope` (filtered diff/apply).

**Do not** chain `apply-report` from multiple diagrams (outline then stale exploration) unless exploration/increments already match the graph—use **`sync`** instead.

`report` writes `<stem>-extracted.json` and `<stem>-update-report.json` beside the diagram.

`apply-report` loads the report JSON and applies it with **`story_graph_ops.StoryMap.apply_update_report`**, then saves `story-graph.json` (unless `--dry-run`).

## Agent checklist

1. Put **this** `scripts/` and **story-graph-ops** `scripts/` on `PYTHONPATH` (or rely on sibling auto-insert).
2. When the user edits the **outline** DrawIO and wants JSON + other diagrams aligned, run **`sync --drawio <outline> --graph <story-graph.json>`** (not separate `report` / `apply-report` / manual re-renders unless `--no-refresh-diagrams` is intended). For **thin-slicing** (or acceptance-criteria) as the edited diagram, use the same command with **`--diagram-type thin-slicing`** (or **`acceptance-criteria`**) and the matching `thin-slicing.drawio` / `acceptance-criteria.drawio` path; companion re-renders always write `acceptance-criteria.drawio` and `thin-slicing.drawio` beside the source diagram.
3. Run **`story_graph_cli.py read --file story-graph.json`** from **story-graph-ops** after graph writes (per **story-graph-ops** obligations).
4. For merges from a **single** report file only (no companion refresh), use **`apply-report`**. Report generation stays in this skill; apply uses **story-graph-ops** only.

## Tests (acceptance shape)

New and changed tests under `tests/drawio_story_sync/` follow **abd-acceptance-test-driven-development**: epic folder **`drawio_story_sync`**, lowest-area subfolders (`cli/`, `outline_story_graph_sync/`, …), files named **`test_*.py`** for pytest discovery, **`Test<Story>`** classes, **`test_<scenario>`** methods, and shared **`given_*` / `when_*` / `then_*`** helpers in **`drawio_story_sync_helper.py`**. After **`sync`**-driven graph writes in tests, assert **`story_graph_cli.py read`** succeeds when that CLI is present.

## See also

- **story-graph-ops** — canonical read/write/validate for `story-graph.json` and **`story_graph_ops`** domain model.
