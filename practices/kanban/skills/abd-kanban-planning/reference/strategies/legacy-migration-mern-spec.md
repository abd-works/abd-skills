# Strategy: Legacy Migration ? MERN (spec stop)

**When to use:** Replacing BESS28 (or similar legacy NonStop) with a **domain-first MERN** target. Legacy **source + code research** is the behavioral spec. **No runnable legacy system** — ATDD RED tests are written against documented legacy behavior for the **new** stack only. **Stop at specification** — no engineering/clean-code until a later engagement.

**Typical scope:** Grouped by abd-domain-glossary boundaries from `context/` + `code-research/`.

**Related:** `legacy-migration.md` (full migration with old-system characterization). `brownfield-current-state.md` (map only).

---

## System of work

| Stage | Scope | Skills (ordered) |
| --- | --- | --- |
| Context | — | **Skip** — BESS28 Source is readable; `code-research/` already indexed |
| Shaping | **project** | **abd-domain-glossary** (detailed — use `code-research/` + `context/BESS28 Source/`), **abd-bounded-context-map**, **abd-story-mapping** (outline from legacy flows), **abd-architecture-outline** (MERN target — read `specs/mern` + `abd-architecture-code`) |
| Discovery | **partition** | ****, **abd-story-mapping** (full), **abd-thin-slicing**, **abd-architecture-blueprint**, **abd-information-architecture** (optional) |
| Exploration | **increment** | **abd-domain-language**, **abd-acceptance-criteria** (legacy behavior is spec), **abd-ux-mockup** (optional), **abd-architecture-specification** (assign/create MERN mechanism reference from blueprint — gate at execution) |
| Specification | **sprint** | **abd-domain-model**, **abd-specification-by-example**, **abd-ux-specification** (optional), **abd-architecture-template** (MERN mechanism templates for sprint scope) |
| Engineering | **sprint** | **abd-acceptance-test-driven-development RED only (PO)** (tests for new system; legacy research + spec as oracle — **no old-system execution**). No abd-domain-specification, abd-clean-code, or GREEN — engagement stops after RED tests. |

### Shaping — module partition (mandatory depth)

1. Read merged `code-research/agent-1-explorer/research-paths.md`, `sources.md`, and all `agent-2-deep-dive/*.md`.
2. Walk `context/BESS28 Source/` — every file must appear in partition (`full-source-coverage` scanner).
3. Produce **6–8 modules** aligned to migration increments (payment, wire-room, messaging, access, platform-runtime, external-integration, persistence, operations — or better names from source).
4. Cross-reference code-research path names in each module's scope statement.

### Architecture target

- **`specs/mern`** via **`abd-architecture-code`** — domain-first `packages/<domain>/{shared,server,client,tests}`.
- **Tighter domain structure:** one MERN package per partition module; shared kernel only for true cross-cutting types (ICN, office, queue envelope) — not a generic util dump.
- Blueprint maps each legacy server/requestor cluster ? MERN domain module + layer participants.

### ATDD policy (no legacy runtime)

| Standard legacy-migration | This strategy |
| --- | --- |
| Tests pass on OLD system first | **Not applicable** — no runnable BESS28 |
| Characterization from production | **Code research + source excerpts + abd-specification-by-example** are the oracle |
| GREEN on new system in engineering | **Deferred** — engineering stage delivers **RED** acceptance tests only |

---

## Scatter rules

**Partitioning enabled** (`abd-domain-glossary` in shaping). Four ticket tiers: **project ? partition ? increment ? sprint**.

| Transition | Rule |
| --- | --- |
| Shaping (project) ? Discovery (partition) | One **partition** ticket per **module** from abd-domain-glossary. Order: simplest boundary ? dependencies ? remainder |
| Discovery (partition) ? Exploration (increment) | One **increment** ticket per thin-slice from partition thin-slicing; **each increment = 10–20 stories** (merge MVIs if needed); JIT after partition discovery complete |
| Exploration (increment) ? Specification (sprint) | 3–4 stories per sprint by data domain |

### Increment sizing (scope call — BESS28 2026-05-31)

Kanban lead verified story counts: **modules = 35–60 stories each** ? modules are **partitions**, not increments. Existing 2–10 story MVIs are **too small**; merge into **~3–4 increments per module** before scatter. See `<workspace>/docs/kanban/scope-call.md`.

When **no** abd-domain-glossary: project runs shaping through discovery and scatters directly to **increments** (three tiers — no partition tickets).

---

## JIT policy

- Scatter all **partitions** after shaping (boundaries from abd-domain-glossary)
- Scatter **increments** JIT — current partition only
- Scatter sprints JIT — current increment only
- After first increment proves pattern: scatter next 2 increments

---

## Checkpoint policy

| Level | When |
| --- | --- |
| Per skill | First increment (prove migration + MERN mapping pattern) |
| Per module | After first increment spec complete |
| Per sprint | Spec review before engagement pause |

---

## Key constraints

- Legacy **source behavior** is the spec — do not invent features.
- **Stop after ATDD RED** — engineering column runs RED tests only; no `abd-clean-code`, no GREEN in this engagement.
- **Wrong partition = wrong migration** — confirm module boundaries before Discovery.
- MERN packages follow **domain module** boundaries from partition, not legacy folder names.
