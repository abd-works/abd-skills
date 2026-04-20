# Story graph parity: agile_bots → story-graph-ops

This document answers why `story_graph.nodes` still matters, what “full migration” means, and how tests (including CLI-style tests) should follow.

## Two different `StoryMap` implementations today

| Location | Role |
| --- | --- |
| `agile_bots/src/story_graph/nodes.py` | **Full domain**: `StoryMap`, `Epic`, `SubEpic`, `Story`, AC, scenarios, increments, `create_*`, `move_*`, `save()`, navigation, scope/submit hooks via `_bot`, trace generation, test-class moves, merge/updater entry points. |
| `agilebydesign-skills/.../story-graph-ops/scripts/story_map.py` | **Ops façade**: dict-backed tree walk (`Epic` / `Story` wrappers), `from_json_file`, `from_bot`, scanners—**no** parity with `nodes.StoryMap` mutations. |

The skill’s `SKILL.md` already describes CRUD on the artifact; the **implementation** has not caught up. That gap is the source of confusion—not a naming mistake.

## What “bring everything over” includes

Minimum set that is **not** optional if the skill truly owns the graph lifecycle:

1. **`nodes.py`** (large): hierarchy + mutations + serialization to `story-graph.json`.
2. **`domain.py`**: `DomainConcept`, `StoryUser`, etc.
3. **`story_graph_paths.py`**: path layout (or an injectable `StoryGraphPaths`-compatible object).
4. **`test_class_mover.py`**: used from nodes for test-class moves (logging paths should be neutralized for standalone use).
5. **`updater.py`**: merge/report application; today it imports **`synchronizers.story_io`** (`DrawIOStoryMap`, `UpdateReport`). Full parity either vendors that subtree or splits “file-only StoryMap updates” from DrawIO sync.

Cross-cutting refactors required for **standalone** use (no agile_bots `Bot`):

- **`_bot`**: today gates `save()`, scope, `submit_action`, `openStoryFile`, `render_diagram`, behaviors list, etc. Standalone mode needs a small **host protocol** (e.g. optional `StoryGraphHost` with `workspace_directory`, `story_graph_path`, `save()`, and no-op or delegated behaviors) so mutations still call `save()` without a full bot.
- **`utils`**: `sanitize_json_string`, `find_test_class_line`, `find_test_method_line`, `find_matching_test_files`, `name_to_test_stem`—either copy minimal helpers into the skill or depend on a tiny shared util package.
- **`traceability.trace_generator`**: optional lazy import or stub when trace is not needed for file ops.

## Why CLI tests (`TTYBotTestHelper`, `story_graph.create_*`) were called “stay in agile_bots”

Those tests assert the **agile_bots REPL/CLI** contract: `story_graph.<path>.create_epic`, `move_story_node`, etc., wired through `TTYBotTestHelper` and bot state.

That is **not** the same as `story_graph_cli.py` today, which only implements **read / names / search / filter / write** on JSON.

**Intended end state:** once `story_graph_cli.py` (or a sibling `story_graph_mutate.py`) exposes the **same operations** as the bot’s `story_graph.*` commands, the **scenarios** from `TestCreateEpic`, `TestMoveStoryNode`, etc. should be **ported** as:

- subprocess tests: `python scripts/story_graph_cli.py create-epic --file ...` with golden JSON or `read` assertions; or  
- in-process tests: import `story_graph_full.StoryMap` (or final package name) and assert on dict/file.

`TTYBotTestHelper` itself stays **bot-specific**; the **behaviors and assertions** port to the skill’s CLI or Python API. There is no good reason to exclude them from the migration—only a sequencing reason: they depend on the mutation surface existing first.

## Suggested phases

1. **Vendor core graph domain** under `story-graph-ops/scripts/` (package name TBD, e.g. `story_graph_full/`) with `domain.py` + `nodes.py` + `story_graph_paths.py` + `test_class_mover.py`, adjusted imports and `_bot`/host protocol.
2. **Wire `story_map.py`**: either deprecate in favor of the full `StoryMap` for walks, or make `story_map` a thin alias over the same tree types to remove duplicate `Epic`/`Story` classes.
3. **Extend `story_graph_cli.py`** with mutation subcommands mirroring bot CLI where feasible.
4. **Port tests** from `agile_bots/test/invoke_bot/edit_story_map/` in order: pure graph mutations → file save/load → scope (if host stubbed) → CLI subprocess tests mirroring old TTY scenarios.

## Tests to track (agile_bots)

Under `test/invoke_bot/edit_story_map/` (and related helpers): graph edits, increments, scope, display, submit scoped action, etc. Each file should be listed in a checklist as it gains a skill-side equivalent.

## DrawIO / synchronizers

Stories that merge from DrawIO depend on `synchronizers.story_io` and friends. Either:

- keep DrawIO merge in **agile_bots** only and document that `updater.generate_report_from` for non-DrawIO sources stays `NotImplementedError` in the skill build until ported, or  
- vendor the synchronizer package as a further phase.

---

**Summary:** Confusion comes from two `StoryMap`s and a CLI that only covers half the skill’s stated obligations. Full migration means **nodes-level domain + dependencies + mutation CLI + tests**; TTY tests should reappear as **skill CLI or API tests**, not abandoned.
