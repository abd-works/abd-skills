---
name: domain-ops
catalog_garden_tier: foundational
catalogue_one_liner: >-
  Keep the domain model graph valid and consistent — so downstream DDD tools always read trusted structure.
description: >-
  Create, read, update, and validate domain-model.json as the single source of truth for domain structure. Use when editing the domain model graph or managing its lifecycle on disk.
context-perspective: domain
context-role: support
context-fidelity:
  - level: exploration
    mode: graph-ops
---

# domain-ops

## Agent obligations (do not skip)

This skill is **not** satisfied by hand-rolling JSON without validation.

| Must | Detail |
| --- | --- |
| **Use this skill's tooling** | Run **`scripts/domain_graph_cli.py`** and/or import from **`domain_map`** with **`PYTHONPATH`** including **`…/domain-ops/scripts`**. |
| **Finish with validation** | After creating or changing a graph file, run **`domain_graph_cli.py read --file <path>`** so bad structure fails early. |
| **Declare completion** | Say what you ran (e.g. "validated with `read`") — not only "wrote JSON." |

## Skill root and PYTHONPATH

```text
practices/domain-driven-design/skills/supporting/domain-ops/
  scripts/
    domain_map.py           ← typed walk model (Module → KA → Class)
    domain_graph_file.py    ← validate + load/save
    domain_graph_cli.py     ← CLI
    graph_filters.py        ← subset by module/class names
```

```bash
export PYTHONPATH="/workspace/practices/domain-driven-design/skills/supporting/domain-ops/scripts"
python3 scripts/domain_graph_cli.py read --file docs/domain/model/domain-model.json
```

## Mandatory workflow

1. Set **`PYTHONPATH`** to include **`domain-ops/scripts`**.
2. Produce JSON via CLI `write`, Python (`domain_map`), or careful hand-edit against **`references/domain-model-template.json`**.
3. **Validate:** `python3 scripts/domain_graph_cli.py read --file <path>`.
4. Optional: `names`, `search`, `filter`.
5. Report the validation command you ran.

## Architecture (mirrors story-graph-ops)

| Layer | Module | Role |
| --- | --- | --- |
| **Class model** | `domain_map.py` | `DomainMap`, `Module`, `KeyAbstraction`, `DomainClass` — dict-backed tree walk |
| **Persistence** | `domain_graph_file.py` | `load_domain_model_dict`, `save_domain_model_dict`, `validate_domain_model_dict` |
| **CLI** | `domain_graph_cli.py` | read, names, search, filter, sha, write (+ lock / expect-sha) |
| **Transforms** | `graph_filters.py` | subset by module or class names |

Schema: **`abd-domain-model/v1`** — see **`../../references/domain-model-json.md`**.

## CLI

```text
python3 scripts/domain_graph_cli.py read   --file <path/to/domain-model.json> [--pretty]
python3 scripts/domain_graph_cli.py names  --file <path>
python3 scripts/domain_graph_cli.py search --file <path> --substring <text>
python3 scripts/domain_graph_cli.py filter --file <path> --modules "A","B" [--pretty]
python3 scripts/domain_graph_cli.py filter --file <path> --classes "Check","Trait" [--pretty]
python3 scripts/domain_graph_cli.py sha    --file <path>
python3 scripts/domain_graph_cli.py write  --file <out.json> [--input <in.json>|stdin]
                                          [--expect-sha <hex>] [--no-lock] [--force]
```

**Exit codes for `write`:** `0` success · `1` validation failure · `2` path error · `3` `--expect-sha` mismatch · `4` active lock.

## Relationship to DDD practice skills

| Piece | Role |
| --- | --- |
| **abd-domain-model** (and siblings) | **Guidance** — what good domain structure looks like; produces `domain-model.md` |
| **domain-ops** | **Lifecycle on disk** — create, validate, read, write `domain-model.json` |

Whenever work touches **`domain-model.json`**, load **domain-ops** and complete the checklist above.

## Tests

```bash
cd practices/domain-driven-design/skills/supporting/domain-ops
python3 -m pytest tests/ -v
```

Tests follow the story-graph-ops AC style (`Given` / `When` / `Then` helpers) and validate practice reference fixtures under `practices/domain-driven-design/references/`.

## Clean code (abd-clean-code)

After changing Python under `scripts/` or `tests/`, run **abd-clean-code** scanners:

```bash
python3 common/scripts/run_scanners.py \
  --skill-root stages/engineering/abd-clean-code \
  --workspace practices/domain-driven-design/skills/supporting/domain-ops/scripts \
  --language python \
  --report-dir practices/domain-driven-design/skills/supporting/domain-ops/tests/scanner-report
```

Latest report: `tests/scanner-report/abd-clean-code.md` — **ALL CLEAN** (17/17 rules).
