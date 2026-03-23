---
name: abd-maps-models-specs
description: Maps, models, and specs pipeline — source structure & chunking rules (Phase 0), canonical context package (Phase 1), layered terms/mechanisms/story map (Phases 2–3), then sparse domain types and validation.
---

# Maps / Models / Specs

Repeatable path from **source markdown** through **evidence**, **vocabulary**, **shaped story map**, and **sparse domain types**, with explicit promotion gates.

**Normative process:** [`content/parts/process.md`](content/parts/process.md) — one table row per **phase** (0–8); **steps** live in [`content/parts/phases/`](content/parts/phases/) (phase steps only—no embedded role). **`process.md`** does **not** repeat the solution analyst role at the top; that context appears in **built** per-phase bundles and is not duplicated here. **Manifest:** [`skill-config.json`](skill-config.json) — `phase_files`, `PHASE_LIBRARY_SLICES`, `phase_critical_quality_notes`. **`python scripts/build.py`** uses **`MapsInstructions`** (same contract as **abd-skill-builder** `Instructions` / `ContentAssembler`) to write [`content/built/agents-staged.md`](content/built/agents-staged.md), **`AGENTS.md`**, and per-phase bundles under **[`content/parts/phases/built/`](content/parts/phases/built/)** (canonical for **`python scripts/generate_prompt.py --phase <slug> --mode static`**) with a duplicate under [`content/built/phases/`](content/built/phases/). Each **built** bundle: **solution analyst role** + YAML-filtered [`rules/*.md`](rules/README.md) + library slice + phase steps + critical quality. See [documentation standards](../../abd-skill-builder/parts/library/documentation-standards.md).

## When to use

- You have a large handbook or corpus and need **traceable** story maps and domain artifacts.
- You want **process discipline** (Phase 0 audit before heavy modeling) per [`content/parts/library/principles-and-rules.md`](content/parts/library/principles-and-rules.md) and [`content/parts/library/execution-and-success.md`](content/parts/library/execution-and-success.md).

## Maintainer

- **Solution analyst role:** edit **`content/parts/solution-analyst-role.md`**, then **`python scripts/build.py`** to refresh built phase bundles and **`AGENTS.md`**. Use **`python scripts/sync_solution_preamble.py`** only to strip legacy **`<!-- solution-analyst-role:* -->`** blocks from a source phase file if present.
- **Build:** `python scripts/build.py` — writes **`AGENTS.md`**, **`content/parts/phases/built/*.md`**, and **`content/built/phases/*.md`**, then runs Phase 0 audit → **`validate_context_contract.py`** (when `context/context_index.json` exists) → Phase 2 artifacts → Phase 3 validation → bundle manifest.
- **Prompts:** `python scripts/generate_prompt.py --phase <slug> --mode static|dynamic` — **`static`** reads **`content/parts/phases/built/<slug>.md`** when present; **`dynamic`** assembles from sources via **`AgileContextEngine`** + **`MapsInstructions`**.
- **Fixture:** `test/mm3/` — set **`active_skill_workspace`** in [`conf/abd-config.json`](conf/abd-config.json); canonical sources are declared in **`solution.conf` → `manifest_sources`** (MM3 includes `docs/HeroesHandbook.md`); greenfield path is **PDF → Markdown → first chunking + index** per [`content/parts/library/context-spec.md`](content/parts/library/context-spec.md) and [`conf/README.md`](conf/README.md).
- **Output:** `test/mm3/abd-maps-models-specs/` only (generated).

## Docs

| Path | Purpose |
|------|---------|
| `content/parts/phases/*.md` | **Authoritative** phase procedure (steps, exit criteria); no embedded role |
| `content/parts/process.md` | **Summary** — pipeline spine + one row per phase; links to `phases/` and `library/` |
| `content/parts/solution-analyst-role.md` | **Solution analyst role** (single source); prepended in **built** bundles by `scripts/build.py` via `MapsInstructions` |
| `skill-config.json` | **Phase manifest** — `phase_files`, `PHASE_LIBRARY_SLICES`, `phase_critical_quality_notes`, scanners (`operator.scanners` in JSON) |
| `content/parts/phases/built/*.md` | Generated — canonical per-phase bundle (same assembly as `generate_prompt`); do not edit |
| `content/built/agents-staged.md` | Generated — staged merge before `AGENTS.md` (do not edit) |
| `content/built/phases/*.md` | Generated — duplicate of `content/parts/phases/built/` (legacy path; same bytes) |
| `content/built/README.md` | Explains the staged build |
| `AGENTS.md` | Generated — title + same body as `agents-staged.md` |
| `docs/README.md` | **Index** of enduring docs (links into `content/parts/library/`) |
| `content/parts/library/principles-and-rules.md` | Principles table, cross-cutting rules, fixture inventory |
| `content/parts/library/execution-and-success.md` | Execution order + success definition |
| `content/parts/phases/canonical-context.md` | Phase 1 steps — corpus flow, structure, evidence typing (chunk/index contract: `context-spec.md`) |
| `content/parts/library/context-spec.md` | **Phase 1:** chunks, `context_index.json`, manifest, chunking spec, validators, single pipeline entry point |
| `content/parts/library/terms-mechanisms-contract.md` | Terms, mechanisms, candidate queue — layers before `concepts[]` |
| `content/parts/library/domain-model.md` | Modules, concepts, `map-model-spec` scaffold |
| `content/parts/library/story-map.md` | Interaction-tree story map (prose) + **why story mapping before domain types** |
| `content/parts/library/shaped-story-map.md` | Phase 3 JSON shape + validators (rationale → `story-map.md` section) |
| `content/parts/library/pipeline_invariants.md` | Gates summary (layers 1–4) |
