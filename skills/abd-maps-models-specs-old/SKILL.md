---
name: abd-maps-models-specs
description: >-
  Synthesizes a map-model-spec (domain model + story map) from chunked context.
  Pipeline: context (Stages 1–3) then map-and-model steps per parts/process.md
  (scaffold, classify, deepen, integrate, evidence, structure, finalize).
  Use when the user wants to "synthesize map model spec", "build story map from context",
  or "extract domain and stories from chunks".
license: MIT
metadata:
  version: "0.1.0"
---

# abd-maps-models-specs

Synthesizes a **map-model-spec** (domain model + story map) from chunked context. End-to-end pipeline: **`parts/process.md`** **Stages 1–3** (context) then **Stage 2 onward** (map → model → spec). The **step parts** below map to the process tables — not necessarily the same row numbers. The **foundational spine** and **modules/epics scaffold (breadth)** use **two** part files (`modules-epics-foundational-spine`, `modules-epics-scaffold-breadth`).

## When to Activate

- User asks to "synthesize map model spec", "build story map from context", "extract domain and stories from chunks"
- Has a **configured workspace** with `context/context_index.json` and `context/chunks/*.md` (paths from `solution.conf`), and wants a validated domain model + story map
- Wants module/epic pairs with concepts, stories, and evidence citations

## Inputs

- **Workspace (required):** `conf/abd-config.json` **must** set `solution_workspace` to the root directory that contains `solution.conf`. Scripts **do not** run without it. Context path = `context_path` in `solution.conf`, defaulting to `<output_dir>/context`, with **`context_index.json`** plus **`chunks/*.md`** (not a legacy `context_chunks.json` at skill root).
- Optional: `mms-junk-defaults.json` — junk term patterns for concept name validation (skill root)

## Outputs

- `map-model-spec.json` — domain model + story map (modules, epics, concepts, stories)
- `map-model-spec.md` — readable summary
- `mms-chunk-index.json` — reverse index (chunk → concepts/epics/stories)
- `evidence/` — actions.json, decisions.json, states.json, relationships.json (process **Evidence** row in Stage 3)

## Structure

**`AGENTS.md`** (skill root) is the full assembled instruction bundle for agents. It is **generated** by `python scripts/build.py` from `parts/process.md`, `parts/domain.md`, `parts/story-map.md`, `parts/context.md`, and `parts/steps/built/*.md`. Do not edit it by hand—the file begins with a regeneration notice.

**Part** = one file under `parts/steps/` (and matching `built/`). **Process row** = numbering in `parts/process.md` (Stage 2 table). Code-only **5a / 7a / 8a** = `build_chunk_index.py` after scaffold breadth, deepen, integrate.

| Part | Process row(s) | Part file (edit) | Built (agents) | Actor | Output |
|------|------------------|------------------|----------------|-------|--------|
| 1 | **Foundational mechanisms** (spine) | `parts/steps/modules-epics-foundational-spine.md` | `parts/steps/built/modules-epics-foundational-spine.md` | AI | map-model-spec.json (spine), optional map-model-spec.md |
| 1 | **Modules and Epics** (+ **5a** index) | `parts/steps/modules-epics-scaffold-breadth.md` | `parts/steps/built/modules-epics-scaffold-breadth.md` | AI | map-model-spec.json (scaffold), map-model-spec.md, mms-chunk-index.json |
| 2 | **6**, **6a** | `parts/steps/concept-classification.md` | `parts/steps/built/concept-classification.md` | AI+Code | map-model-spec.json (evidence merged), summary.md, relationships.md |
| 3 | **7** (+ **7a** index) | `parts/steps/concept-classes-stories.md` | `parts/steps/built/concept-classes-stories.md` | AI | map-model-spec.json (deepened) |
| 4 | **8** (+ **8a** index) | `parts/steps/integrate-harmonize.md` | `parts/steps/built/integrate-harmonize.md` | AI | map-model-spec.json (canonical) |
| 5 | **9** | `parts/steps/evidence.md` | `parts/steps/built/evidence.md` | Code | evidence/*.json |
| 6 | **10** | `parts/steps/structure.md` | `parts/steps/built/structure.md` | AI | map-model-spec.json (structured) |
| 7 | **11** | `parts/steps/finalize.md` | `parts/steps/built/finalize.md` | AI | map-model-spec.json (final) |

## Concept classes and stories discipline (agents)

**Concept classes and stories** must be **model-authored** (interactive edits **or** the listed **`scripts/deepen_pair_chat_api.py`**, which calls the chat API, uses the **same chunk batching as `classify_chunks.py`**, and passes the **full** pair JSON plus batched chunk clusters — no silo’d summaries). No ad-hoc merge/replay scripts. See `rules/step6-deepen-ai-only-no-merge-scripts.md`. Afterward, run scanners and `build_chunk_index.py`.

## Scripts

- `scripts/get_prompt_bundle.py` — Print a prompt bundle to **stdout** for the agent to run and follow. **`--operation <slug>`** (or `-o`): `process.md` + `domain.md` + `story-map.md` + `context.md` + `parts/steps/built/<slug>.md` (same resolution as `build_agents.py`, one step only). **`--list-operations`**: print valid slugs. **`--built-step`** / **`--file`** / stdin: single file only. Examples: `python scripts/get_prompt_bundle.py --operation modules-epics-scaffold-breadth`, `python scripts/get_prompt_bundle.py --built-step modules-epics-scaffold-breadth`.
- `scripts/build.py` — Run `build_steps.py` (bake rules into `parts/steps/built/`) then assemble `AGENTS.md`
- **`modules-epics-foundational-spine` / `modules-epics-scaffold-breadth`:** Foundational spine + human gate — **`parts/steps/built/modules-epics-foundational-spine.md`**. Scaffold breadth = AI **full-reads ~30%** of corpus (**K ≈ round(0.3×N)** distinct `chunks/<id>.md`, **N** = **`forward_index`** size) with a **counter** and **breadth** — **no** orientation manifest in `map-model-spec.json` — **`parts/steps/built/modules-epics-scaffold-breadth.md`**. See **`parts/process.md`** Stage 2 table.
- `scripts/build_chunk_index.py` — Build mms-chunk-index.json from map-model-spec.json
- **Scanners** (`scripts/scanners/*.py` unless noted otherwise): **After foundational spine + scaffold breadth:** chunks_must_be_referenced, no_duplicates, epic_requires_confirming_stories, no_junk_concepts. **After concept classes and stories (deepen):** add concepts_have_owns, stories_have_trigger_response, domain_interaction_sync, hierarchy_sizing. **After integrate and harmonize:** cross_cutting_resolved (see built integrate-harmonize for command names). **Evidence row:** evidence_files_exist, evidence_scaffold_refs, evidence_schema (`evidence_schema.py`). **Structure / finalize:** re-run structural scanners per built `finalize.md`. Exit 0 = pass, 1 = violations.

## Parts

- **Step sources** (clean): `parts/steps/<name>.md` — same pattern as solution modeler `pieces/phases/<name>.md`
- **Built step specs** (rules baked in): `parts/steps/built/<name>.md` — regenerate with `python scripts/build_steps.py`; do not edit by hand
- `parts/steps/modules-epics-foundational-spine.md` — Foundational spine only (Stage 2 **Foundational mechanisms**)
- `parts/steps/modules-epics-scaffold-breadth.md` — Modules/epics scaffold + **K** reads + chunk index (**Modules and Epics** + **5a**)
- `parts/steps/concept-classification.md` — Classify chunks; merge evidence into map-model-spec
- `parts/steps/concept-classes-stories.md` — Deepen concepts and stories per module/epic (chat); built copy adds rules
- `parts/steps/integrate-harmonize.md` — Unify naming, resolve cross-cutting, finalize subtypes
- `parts/steps/evidence.md` — Evidence extraction (code)
- `parts/steps/structure.md` — AI builds full model from scaffold + evidence
- `parts/steps/finalize.md` — Behavior, variation, consolidate, assess, finalize
- `parts/domain.md` — Domain model format
- `parts/story-map.md` — Story map format (Epic → Sub-Epic → Story → Scenario → Step)
- `parts/process.md` — Pipeline overview; Ref column links to **built** step docs

## Documentation

- **`docs/pipeline-deep-dive.md`** — Domain-neutral analysis of the pipeline: what it optimizes for, failure modes by stage, and recommended gates (any domain using story mapping + OO-oriented solution modeling).
- Fixture-specific critiques (e.g. under `test/`) illustrate failure modes on one corpus; they are **not** normative vocabulary for the skill.

## Rules

Rules in `rules/` enforce quality per process row. Scanners check structural violations mechanically. AI performs adversarial validation after scanners. **Finalize AI-only rules:** no-anemia, no-over-centralization, assessment-complete.
