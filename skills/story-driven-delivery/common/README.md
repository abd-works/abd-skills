# common

Shared Python packages used across multiple Agile by Design skills. Each
package is platform-agnostic — it never imports from a specific backend skill.

## Contents

- **`diagram_story_sync/`** — geometry (`Position`, `Boundary`), persisted
  layouts (`LayoutData`), render summaries, story-graph update reports
  (re-export from `story_graph_ops`), shared style defaults and layout
  constants, abstract diagram nodes (`DiagramEpic`, `DiagramSubEpic`,
  `DiagramStory`, `DiagramIncrement`), and the structural diff helpers in
  `node_comparison`. Used by:
  - `skills/drawio-story-sync` — DrawIO XML backend
  - `skills/miro-story-sync` — Miro REST API backend

## Layout

The expected monorepo layout is:

```
agilebydesign-skills/
    common/
        diagram_story_sync/      <- this folder
    skills/
        story-graph-ops/scripts/
        drawio-story-sync/scripts/
        miro-story-sync/scripts/
```

Backend skills auto-detect this layout via their `_bootstrap.py` modules. If
your project does not follow it, prepend `common/` and
`skills/story-graph-ops/scripts` to `PYTHONPATH` manually.

## Running tests

Backend skills that depend on `common` keep their tests under their own
`tests/` directories. The repo root `pytest.ini` lists each test path; see
`skills/drawio-story-sync/tests` and `skills/miro-story-sync/tests`.
