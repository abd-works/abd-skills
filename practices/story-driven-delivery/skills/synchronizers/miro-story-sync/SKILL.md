---
name: miro-story-sync
catalog_garden_tier: foundational
catalogue_one_liner: >-
  story-graph.json to Miro story maps; validated load and REST-driven board sync.
description: >-
  Renders and synchronizes story-map Miro boards (outline; exploration and increments planned)
  from story-graph.json. Use when producing or refreshing Miro story maps from story-graph.json,
  or when wiring CI/scripts for Miro board updates.
---

# miro-story-sync

## What this skill owns

- Python package **`miro_story_sync/`** (under `scripts/`) — Miro-specific
  story node hierarchy, transport abstractions, and story-map orchestrator.
- CLI **`scripts/miro_story_sync_cli.py`**: `render` (today; `report` /
  `apply-report` / `sync` planned and will mirror **drawio-story-sync**).

## Story diagram kinds

| Workflow | `renderer_command` | CLI `--mode` aliases | Output role |
| --- | --- | --- | --- |
| Outline | `render-outline` (default) | `outline`, `story-map` | Epic / sub-epic / story map |
| Exploration | `render-exploration` | `exploration`, `acceptance-criteria` | Outline plus AC boxes (planned) |
| Prioritization | `render-increments` | `increments`, `prioritization`, `thin-slices` | Outline base plus increment lanes (planned) |

## Dependencies (PYTHONPATH)

1. **`common/`** at the repo root (so `import diagram_story_sync` works).
2. **This skill's `scripts/`** (so `import miro_story_sync` works).
3. **story-graph-ops** `scripts/` — same domain types as
   **drawio-story-sync**: `StoryMap`, `Epic`, `SubEpic`, `Story`, etc.

All three are auto-prepended by `miro_story_sync._bootstrap` and
`miro_story_sync_cli.py` when the standard monorepo layout is present.

## Transport options

`MiroTransport` is the abstract seam; the CLI defaults to `RestMiroTransport`
but tests and dry runs use `InMemoryMiroTransport`.

| Transport | Use case | Auth / state |
| --- | --- | --- |
| **`RestMiroTransport`** | Production. Talks to `https://api.miro.com/v2/boards/{board_id}/items`. Creates `shape`, `sticky_note`, `text`, `frame` items with absolute geometry. | `MIRO_ACCESS_TOKEN` env var (Bearer); board ID in CLI. |
| **`InMemoryMiroTransport`** | Tests. Stores items in a Python dict keyed by item id; rendering can re-read what it just wrote. | None — no network. |

## Common module

This skill **never duplicates** geometry, layout, or comparison code. It
imports from `common/diagram_story_sync` (under `skills/story-analysis/`):

- `Position`, `Boundary`, `LayoutData`, `RenderSummary`
- `DiagramStoryNode`, `DiagramEpic`, `DiagramSubEpic`, `DiagramStory`,
  `DiagramIncrement`
- `STYLE_DEFAULTS`, layout constants (`CELL_SIZE`, `EPIC_Y`, ...)
- `compare_node_lists`, `collect_all_names`, `RowPositions`,
  `max_sub_epic_depth`
- `UpdateReport` (re-export from `story_graph_ops`)

`MiroEpic` / `MiroSubEpic` / `MiroStory` subclass the common
`DiagramEpic` / `DiagramSubEpic` / `DiagramStory`.

## Commands

```text
python miro_story_sync_cli.py render --mode outline --graph <story-graph.json> --board <BOARD_ID>
python miro_story_sync_cli.py render --mode outline --graph <story-graph.json> --dry-run
```

`--dry-run` swaps in `InMemoryMiroTransport` so you can verify rendering
without hitting Miro. `MIRO_ACCESS_TOKEN` is read from the environment by
`RestMiroTransport`; without it `render` falls back to dry-run.

## Agent checklist

1. Put **`skills/story-analysis/common/`**, this skill's **`scripts/`**, and **story-graph-ops**
   `scripts/` on `PYTHONPATH` (or rely on the auto-bootstrap).
2. Set `MIRO_ACCESS_TOKEN` in the environment for real-board writes.
3. For local validation, run with `--dry-run` to render via the in-memory
   transport (no network, no token required).
4. Run **`story_graph_cli.py read --file story-graph.json`** from
   **story-graph-ops** before / after graph-affecting operations once
   `report` and `apply-report` ship.

## Tests (acceptance shape)

Tests under `tests/miro_acceptance/` follow
**abd-story-test**: epic folder
**`miro_acceptance`** (named to avoid shadowing the production
`miro_story_sync` package — pytest resolves test packages by directory name
and would otherwise import the test folder when production code imports
`miro_story_sync`), lowest-area subfolders (`cli/`, `outline_render/`, …),
files named **`test_*.py`** for pytest discovery, **`Test<Story>`** classes,
**`test_<scenario>`** methods, and shared **`given_*` / `when_*` / `then_*`**
helpers in **`miro_story_sync_helper.py`**.

### Connectivity testing strategy (no stubs, no secrets)

Tests do **not** stub the production transport. They stand up a
**`LocalMiroServer`** (`tests/miro_acceptance/local_miro_server.py`) — a real
in-process `ThreadingHTTPServer` bound to a random `127.0.0.1` port that
implements the same Miro v2 routes the production transport calls
(`POST /v2/boards/{board_id}/shapes` / `/sticky_notes` / `/items`,
`GET /v2/boards/{board_id}/items`, `DELETE .../items/{item_id}`). Tests
construct the production **`RestMiroTransport`** with
`base_url=server.base_url` (so `urllib` connects to the loopback) and a
test-only Bearer token (the local server accepts any non-empty token, so
no real secret is committed or required). The production transport sends
real HTTP requests — real wire format, real `Authorization` header, real
JSON body, real status codes — and the test asserts on what the localhost
server received.

This satisfies the **Mock Only Boundaries** rule: the boundary (the Miro
service) is replaced with a real localhost server speaking the same
protocol, while every production class (`RestMiroTransport`,
`MiroSynchronizer`, `MiroStoryMap`, `MiroStoryNodeSerializer`, `MiroElement`)
runs unaltered. CLI tests run a real Python subprocess of
`miro_story_sync_cli.py`, set `MIRO_ACCESS_TOKEN` and `MIRO_API_BASE_URL` in
the subprocess environment, and verify the localhost server received the
items the user-visible CLI promised it would post.

Real Miro account access is gated by the same env vars in production:
`MIRO_ACCESS_TOKEN` and (optionally) `MIRO_API_BASE_URL`. `--dry-run` keeps
the production `InMemoryMiroTransport` for local smoke tests where a Miro
account is not desired; tests do not depend on it.

## See also

- **drawio-story-sync** — sibling skill rendering the same model to DrawIO XML.
- **skills/story-analysis/common/diagram_story_sync** — shared platform-agnostic primitives.
- **story-graph-ops** — canonical read/write/validate for `story-graph.json`.
