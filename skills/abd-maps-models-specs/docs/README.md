# abd-maps-models-specs — documentation

Long-lived reference for the skill: **why** (principles), **what order** (execution), **construct-specific** norms (Phase 1 package, Phase 2 terms, Phase 3 story map, …), and **domain / story** prose. These files are written so an operator can run the pipeline without prior context from a planning session or chat history.

## Read first

| Document | Purpose |
|----------|---------|
| [`principles-and-rules.md`](principles-and-rules.md) | Principles table, cross-cutting rules, how to revise a principle, fixture inventory |
| [`execution-and-success.md`](execution-and-success.md) | Execution order (what to do next) + reusable success definition |
| [`context-corpus.md`](context-corpus.md) | Chunk/index contract; how the corpus is built and validated in this skill |
| [`pipeline_invariants.md`](pipeline_invariants.md) | Cross-cutting gates: layers 1–4 and promotion discipline |
| [`context-package.md`](context-package.md) | **Phase 1 only:** provenance, single script surface, validation |

## Domain and story artifacts

| Document | Purpose |
|----------|---------|
| [`domain-model.md`](domain-model.md) | Modules, concepts, properties, operations, examples, `map-model-spec` JSON fields |
| [`story-map-narrative.md`](story-map-narrative.md) | Full interaction-tree story map (epic → step), tables, grounding — complements **behavioral** Phase 3 JSON |
| [`terms-mechanisms-contract.md`](terms-mechanisms-contract.md) | Terms, mechanisms, candidate queue — layers before `concepts[]` |
| [`behavioral-story-map.md`](behavioral-story-map.md) | Story map **shape** (actor, behavior, anchor) **and** rationale for stories before domain types |

## Where normative process lives

Anything that **must** land in **`AGENTS.md`** or other generated agent context is authored under **`content/parts/`** (and, when a skill merges bases + rules + roles, the **staged** output can live under **`content/built/`** before the final file). **`docs/`** is **reference** you open beside the skill—schemas, contracts, long-form narrative—not a substitute for those sources unless the build copies them in.

Construct docs under `docs/` (schemas, artifact contracts, long-lived reference) are **not** duplicates of `content/parts/` for process steps; they **complement** them with one construct per file where useful (per [skill documentation standards](../abd-skill-builder/docs/documentation-standards.md)).

- **Stage and phase table:** [`../content/parts/process.md`](../content/parts/process.md)
- **Per-phase steps:** [`../content/parts/phases/`](../content/parts/phases/)
- **Generated agent view:** [`../AGENTS.md`](../AGENTS.md) — run `python scripts/build.py` from the skill root
