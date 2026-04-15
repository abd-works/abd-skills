# abd-maps-models-specs — documentation



Long-lived reference for the skill: **why** (principles), **construct-specific** norms (Phase 1 package, Phase 2 terms, Phase 3 story map, …), and **domain / story** prose. These files are written so a **solution analyst** can run the pipeline without prior context from a planning session or chat history. **Execution order** is in [`content/parts/process.md`](../content/parts/process.md) (not duplicated here).



**Note:** Normative markdown for contracts and reference lives under **`content/parts/library/`** (not under `docs/`). This folder only holds this index.



## Read first



| Document | Purpose |

|----------|---------|

| [`principles.md`](../content/parts/library/principles.md) | Principles table only (why we work this way); checkable rules live in `rules/` and phase bundles |

| [`phases/context-chunking-approach.md`](../content/parts/phases/context-chunking-approach.md) | Phase 0 — scan big Markdown, write **context_chunking_spec** (structure, not pass/fail) |
| [`phases/canonical-context.md`](../content/parts/phases/canonical-context.md) | Phase 1 — build chunks + index; evidence typing vs promotion |

| [`context-spec.md`](../content/parts/library/context-spec.md) | **Phase 1 only:** provenance, single script surface, validation |



## Domain and story artifacts



| Document | Purpose |

|----------|---------|

| [`domain-model.md`](../content/parts/library/domain-model.md) | Modules, concepts, properties, operations, examples, `map-model-spec` JSON fields |

| [`story-map.md`](../content/parts/library/story-map.md) | Full interaction-tree story map (epic → step), tables, grounding — complements Phase 3 **shaped story map** JSON |

| [`terms-mechanisms-contract.md`](../content/parts/library/terms-mechanisms-contract.md) | Terms, mechanisms, candidate queue — layers before `concepts[]` |

| [`shaped-story-map.md`](../content/parts/library/shaped-story-map.md) | Phase 3 **shape** (actor, behavior, anchor) + validators; ordering rationale in [`story-map.md`](../content/parts/library/story-map.md#why-story-mapping-before-domain-types) |



## Where normative process lives



Anything that **must** land in **`AGENTS.md`** or other generated agent context is authored under **`content/parts/`** (and, when a skill merges bases + rules + roles, the **staged** output can live under **`content/built/`** before the final file). **`docs/`** is **reference** you open beside the skill—this index—not a substitute for those sources unless the build copies them in.



Construct docs under `content/parts/library/` (schemas, artifact contracts, long-form narrative) **complement** phase steps; they are **not** duplicates of `content/parts/phases/` for process steps unless explicitly noted (see **abd-skill-builder** [`skill-structure-and-concepts.md`](../../abd-skill-builder/content/parts/library/skill-structure-and-concepts.md) — library vs phases, §3).



- **Stage and phase table:** [`../content/parts/process.md`](../content/parts/process.md)

- **Per-phase steps:** [`../content/parts/phases/`](../content/parts/phases/) — **Phase 1 (canonical context)** is fully specified in [`canonical-context.md`](../content/parts/phases/canonical-context.md)

- **Generated agent view:** [`../AGENTS.md`](../AGENTS.md) — run `python scripts/build.py` from the skill root

