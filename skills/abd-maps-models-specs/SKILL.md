---
name: abd-maps-models-specs
description: Maps, models, and specs pipeline — source structure & chunking rules (Phase 0), canonical context package (Phase 1), layered terms/mechanisms/story map (Phases 2–3), then sparse domain types and validation.
---

# Maps / Models / Specs

Repeatable path from **source markdown** through **evidence**, **vocabulary**, **shaped story map**, and **sparse domain types**, with explicit promotion gates.

**Normative process:** [`content/parts/process.md`](content/parts/process.md) — one table row per **phase** (0–8); **steps** live in [`content/parts/phases/`](content/parts/phases/) (phase steps only—no embedded role). **`process.md`** does **not** repeat the solution analyst role at the top; that context appears in **built** per-phase bundles and is not duplicated here. **Manifest:** [`skill-config.json`](skill-config.json) — `phase_files`, `library_files`, `phase_library`, `phase_rules`, `every_phase_rules`, `phase_critical_quality_notes`. **`python scripts/build.py`** uses **`MapsInstructions`** (same contract as **abd-skill-builder** `Instructions` / `ContentAssembler`) to write [`content/built/agents-staged.md`](content/built/agents-staged.md), **[`content/built/phases/<slug>.md`](content/built/phases/)**, and **`AGENTS.md`**. **`python scripts/generate_prompt.py --phase <slug>`** emits the phase bundle; **static vs dynamic** is set in **`skill-config.json`** (**`generate_prompt.assembly_mode`**, or **`delivery.mode`**); this skill defaults to **static** (reads **`content/built/phases/<slug>.md`** when present). Each **built** bundle (in order): **role** → **phase** → **library** → **rules** → **principles** (Stage 2+ only; Stage 1 ends after **rules** — see [`content/built/phases/README.md`](content/built/phases/README.md)). Repo layout: **abd-skill-builder** [`skill-structure-and-concepts.md`](../../abd-skill-builder/content/parts/library/skill-structure-and-concepts.md).

## When to use

- You have a large handbook or corpus and need **traceable** story maps and domain artifacts.
- You want **process discipline** (Phase 0 audit before heavy modeling) per [`content/parts/library/principles.md`](content/parts/library/principles.md) and [`content/parts/process.md`](content/parts/process.md).

## Maintainer

- **Solution analyst role:** edit **`content/parts/solution-analyst-role.md`**, then **`python scripts/build.py`** to refresh built phase bundles and **`AGENTS.md`**. Use **`python scripts/sync_solution_preamble.py`** only to strip legacy **`<!-- solution-analyst-role:* -->`** blocks from a source phase file if present.
- **Build:** `python scripts/build.py` — writes **`AGENTS.md`**, **`content/built/agents-staged.md`**, **`content/built/phases/*.md`**, **`content/built/README.md`**, then runs **`operator.build_pipeline`** (emitters, **rule-bound** scanners per **`rules/scanners.json`**, manifest, rule-example lint).
- **Prompts:** `python scripts/generate_prompt.py --phase <slug>` — assembly mode from **`skill-config.json`** (**`generate_prompt.assembly_mode`**: `static` \| `dynamic`, defaulting via **`delivery.mode`**); **`static`** uses **`content/built/phases/<slug>.md`** when present; otherwise (or when **`dynamic`**) assembles from sources via **`AgileContextEngine`** + **`MapsInstructions`**.
- **Example workspace:** `test/sample-workspace/` — set **`active_skill_workspace`** in [`skill-config.json`](skill-config.json); canonical sources are declared in **`solution.conf` → `manifest_sources`** (the sample lists `docs/sample.md`); greenfield path is **PDF → Markdown → first chunking + index** per [`content/parts/library/context-spec.md`](content/parts/library/context-spec.md) and [`conf/README.md`](conf/README.md).
- **Output:** under `<active_skill_workspace>/<output_dir>/` only (generated; default `output_dir` is the skill folder name, e.g. `abd-maps-models-specs/`).

## Docs

| Path | Purpose |
|------|---------|
| `content/parts/phases/*.md` | **Authoritative** phase procedure (steps, exit criteria); no embedded role |
| `content/parts/process.md` | **Summary** — pipeline spine + one row per phase; links to `phases/` and `library/` |
| `content/parts/solution-analyst-role.md` | **Solution analyst role** (single source); prepended in **built** bundles by `scripts/build.py` via `MapsInstructions` |
| `skill-config.json` | **Phase manifest** — `phase_files`, `library_files`, `phase_library`, `phase_rules`, `every_phase_rules`, `phase_critical_quality_notes`, **`operator.build_pipeline`** (post-merge steps; rule-bound scanners listed in `rules/scanners.json`) |
| `content/built/agents-staged.md` | Generated — staged merge before `AGENTS.md` (do not edit) |
| `content/built/phases/*.md` | Generated — per-phase static bundle (same assembly as `generate_prompt`); do not edit |
| `content/built/README.md` | Index of everything under `content/built/` |
| `AGENTS.md` | Generated — title + same body as `agents-staged.md` |
| `docs/README.md` | **Index** of enduring docs (links into `content/parts/library/`) |
| `content/parts/library/principles.md` | Principles table only; checkable rules in `rules/` (inlined in built bundles) |
| `content/parts/phases/canonical-context.md` | Phase 1 steps — corpus flow, structure, evidence typing (chunk/index contract: `context-spec.md`) |
| `content/parts/library/context-spec.md` | **Phase 1:** chunks, `context_index.json`, manifest, chunking spec, validators, single pipeline entry point |
| `content/parts/library/terms-mechanisms-contract.md` | Terms, mechanisms, candidate queue — layers before `concepts[]` |
| `content/parts/library/domain-model.md` | Modules, concepts, `map-model-spec` scaffold |
| `content/parts/library/story-map.md` | Interaction-tree story map (prose) + **why story mapping before domain types** |
| `content/parts/library/shaped-story-map.md` | Phase 3 JSON shape + validators (rationale → `story-map.md` section) |
