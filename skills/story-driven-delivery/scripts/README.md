# scripts (shared story-diagram Python)

Shared Python packages used across multiple abd.works **story-driven-delivery** skills. Each
package is platform-agnostic — it never imports from a specific backend skill.

## Contents

- **`diagram_story_sync/`** — geometry (`Position`, `Boundary`), persisted
  layouts (`LayoutData`), render summaries, story-graph update reports
  (re-export from `story_graph_ops`), shared style defaults and layout
  constants, abstract diagram nodes (`DiagramEpic`, `DiagramSubEpic`,
  `DiagramStory`, `DiagramIncrement`), and the structural diff helpers in
  `node_comparison`. Used by:
  - `skills/story-driven-delivery/drawio-story-sync` — DrawIO XML backend
  - `skills/story-driven-delivery/miro-story-sync` — Miro REST API backend

## Layout

The expected monorepo layout is:

```
agilebydesign-skills/
    skills/
        story-driven-delivery/
            scripts/
                diagram_story_sync/      <- this folder
            story-graph-ops/scripts/
            drawio-story-sync/scripts/
            miro-story-sync/scripts/
```

Backend skills auto-detect this layout via their `_bootstrap.py` modules. If
your project does not follow it, prepend `skills/story-driven-delivery/scripts/` and
`skills/story-driven-delivery/story-graph-ops/scripts` to `PYTHONPATH` manually.

## Running tests

Backend skills that depend on this shared folder keep their tests under their own
`tests/` directories. The repo root `pytest.ini` lists each test path; see
`skills/story-driven-delivery/drawio-story-sync/tests` and
`skills/story-driven-delivery/miro-story-sync/tests`.
