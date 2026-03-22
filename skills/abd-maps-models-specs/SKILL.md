---
name: abd-maps-models-specs
description: Maps, models, and specs pipeline — evidence-first context audit (Phase 0), layered terms/mechanisms/story map (Phases 2–3), then sparse domain types and validation.
---

# Maps / Models / Specs

Repeatable path from **source markdown** through **evidence**, **vocabulary**, **behavioral stories**, and **sparse domain types**, with explicit promotion gates.

**Normative process:** [`content/parts/process.md`](content/parts/process.md) — one table row per **phase** (0–8); **steps** live in [`content/parts/phases/`](content/parts/phases/). **`python scripts/build.py`** writes [`content/built/agents-staged.md`](content/built/agents-staged.md) (staged merge), then **`AGENTS.md`** (same body + title), and **[`content/built/phases/`](content/built/phases/)** — one **built phase bundle** per phase (operator role + [`rules/*.md`](rules/README.md) filtered by YAML `phase_files` + library excerpts + phase steps). Operator preamble is **omitted** from the merge (it stays in source phase files); see [documentation standards](../abd-skill-builder/content/parts/library/documentation-standards.md).

## When to use

- You have a large handbook or corpus and need **traceable** story maps and domain artifacts.
- You want **process discipline** (Phase 0 audit before heavy modeling) per [`docs/principles-and-rules.md`](docs/principles-and-rules.md) and [`docs/execution-and-success.md`](docs/execution-and-success.md).

## Operator

- **Operator preamble:** edit **`content/parts/operator-role.md`**, then run **`python scripts/sync_operator_preamble.py`** so every file under **`content/parts/phases/`** gets that block at the top, then **`python scripts/build.py`** to refresh **`AGENTS.md`** (HTML sync markers are stripped from the merged phase sections in **`AGENTS.md`**).
- **Build:** `python scripts/build.py` — writes **`AGENTS.md`** and **`content/built/phases/*.md`** (per-phase bundles) from `content/parts/`, then runs Phase 0 audit → **`validate_context_contract.py`** (when `context/context_index.json` exists) → Phase 2 artifacts → Phase 3 validation → bundle manifest.
- **Fixture:** `test/mm3/` — set **`active_skill_workspace`** in [`conf/abd-config.json`](conf/abd-config.json); canonical sources are declared in **`solution.conf` → `manifest_sources`** (MM3 includes `docs/HeroesHandbook.md`); greenfield path is **PDF → Markdown → first chunking + index** per [`docs/context-package.md`](docs/context-package.md) and [`conf/README.md`](conf/README.md).
- **Output:** `test/mm3/abd-maps-models-specs/` only (generated).

## Docs

| Path | Purpose |
|------|---------|
| `content/parts/process.md` | **Process table** — ordered phases; links to phase docs and `docs/` library |
| `content/parts/operator-role.md` | **Operator preamble** (single source); injected into each phase file by `scripts/sync_operator_preamble.py` |
| `content/parts/phases/*.md` | **Phase** normative steps (include operator preamble for editing) |
| `content/built/agents-staged.md` | Generated — staged merge before `AGENTS.md` (do not edit) |
| `content/built/phases/*.md` | Generated — one bundle per phase: role + rules + library + phase steps (do not edit) |
| `content/built/README.md` | Explains the staged build |
| `AGENTS.md` | Generated — title + same body as `agents-staged.md` |
| `docs/README.md` | **Index** of enduring docs |
| `docs/principles-and-rules.md` | Principles table, cross-cutting rules, fixture inventory |
| `docs/execution-and-success.md` | Execution order + success definition |
| `docs/context-corpus.md` | Chunk/index contract; how the corpus is built and validated here |
| `docs/context-package.md` | **Phase 1:** chunks, `context_index.json`, manifest, chunking spec, validators, single pipeline entry point |
| `docs/terms-mechanisms-contract.md` | Terms, mechanisms, candidate queue — layers before `concepts[]` |
| `docs/domain-model.md` | Modules, concepts, `map-model-spec` scaffold |
| `docs/story-map-narrative.md` | Full interaction-tree story map (prose) |
| `docs/behavioral-story-map.md` | Phase 3 JSON shape + story-before-types rationale |
| `docs/pipeline_invariants.md` | Gates summary (layers 1–4) |
