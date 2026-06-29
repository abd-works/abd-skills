---
name: ux-ops
catalog_garden_tier: foundational
catalogue_one_liner: >-
  Keep the UX graph valid and consistent — so downstream mockup tools always read trusted structure.
description: >-
  Create, read, update, and validate ux-graph.json as the single source of truth for UX structure. Use when editing the UX graph or managing its lifecycle on disk.
context-perspective: ux
context-role: support
context-fidelity:
  - level: exploration
    mode: graph-ops
---

# ux-ops

## Agent obligations (do not skip)

This skill is **not** satisfied by hand-rolling JSON without validation.

| Must | Detail |
| --- | --- |
| **Use this skill's tooling** | Run **`scripts/ux_graph_cli.py`** and/or import from **`ux_map`** with **`PYTHONPATH`** including **`…/ux-ops/scripts`**. |
| **Finish with validation** | After creating or changing a graph file, run **`ux_graph_cli.py read --file <path>`** so bad structure fails early. |
| **Declare completion** | Say what you ran (e.g. "validated with `read`") — not only "wrote JSON." |

## Skill root and PYTHONPATH

```text
practices/user-experience-design/skills/supporting/ux-ops/
  scripts/
    ux_map.py           ← typed walk model (Flow → Screen → Region)
    ux_graph_file.py    ← validate + load/save
    ux_graph_cli.py     ← CLI
    graph_filters.py    ← subset by flow/screen names
```

```bash
export PYTHONPATH="/workspace/practices/user-experience-design/skills/supporting/ux-ops/scripts"
python3 scripts/ux_graph_cli.py read --file docs/ux/mockup/ux-graph.json
```

## Mandatory workflow

1. Set **`PYTHONPATH`** to include **`ux-ops/scripts`**.
2. Produce JSON via CLI `write`, Python (`ux_map`), or careful hand-edit against **`references/ux-graph-template.json`**.
3. **Validate:** `python3 scripts/ux_graph_cli.py read --file <path>`.
4. Optional: `names`, `search`, `filter`.
5. Report the validation command you ran.

## Architecture (mirrors story-graph-ops and domain-ops)

| Layer | Module | Role |
| --- | --- | --- |
| **Class model** | `ux_map.py` | `UxGraph`, `Flow`, `Screen`, `Region` — dict-backed tree walk |
| **Persistence** | `ux_graph_file.py` | `load_ux_graph_dict`, `save_ux_graph_dict`, `validate_ux_graph_dict` |
| **CLI** | `ux_graph_cli.py` | read, names, search, filter, sha, write (+ lock / expect-sha) |
| **Transforms** | `graph_filters.py` | subset by flow or screen names |

Schema: **`abd-ux-graph/v1`** — see **`../../references/ux-graph-json.md`**.

## CLI

```text
python3 scripts/ux_graph_cli.py read   --file <path/to/ux-graph.json> [--pretty]
python3 scripts/ux_graph_cli.py names  --file <path>
python3 scripts/ux_graph_cli.py search --file <path> --substring <text>
python3 scripts/ux_graph_cli.py filter --file <path> --flows "Shop in store" [--pretty]
python3 scripts/ux_graph_cli.py filter --file <path> --screens "Search Results","Product Detail" [--pretty]
python3 scripts/ux_graph_cli.py sha    --file <path>
python3 scripts/ux_graph_cli.py write  --file <out.json> [--input <in.json>|stdin]
                                        [--expect-sha <hex>] [--no-lock] [--force]
```

**Exit codes for `write`:** `0` success · `1` validation failure · `2` path error · `3` `--expect-sha` mismatch · `4` active lock.

## Relationship to UX practice skills

| Piece | Role |
| --- | --- |
| **abd-ux-mockup** (and siblings) | **Guidance** — what good wireframe structure looks like; produces markdown and drawio projections |
| **ux-ops** | **Lifecycle on disk** — create, validate, read, write `ux-graph.json` |

Whenever work touches **`ux-graph.json`**, load **ux-ops** and complete the checklist above.

## Tests

```bash
cd practices/user-experience-design/skills/supporting/ux-ops
python3 -m pytest tests/ -v
```

Tests follow the story-graph-ops AC style (`Given` / `When` / `Then` helpers) and validate practice reference fixtures under `practices/user-experience-design/references/`.

## Clean code (abd-clean-code)

After changing Python under `scripts/`, run **abd-clean-code** scanners with an **explicit code folder**:

```bash
python3 common/scripts/run_scanners.py \
  --skill-root stages/engineering/abd-clean-code \
  --workspace practices/user-experience-design/skills/supporting/ux-ops \
  --language python \
  --code-dir scripts \
  --report-dir practices/user-experience-design/skills/supporting/ux-ops/tests/scanner-report
```

Confirm the driver prints `[CODE] 4 Python file(s):` (or current count) before trusting results. Latest report: `tests/scanner-report/abd-clean-code.md`.

Graph-ops CLI tooling mirrors **story-graph-ops** — same structural patterns; full clean-code compliance is incremental.
