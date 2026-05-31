# Strategy: Brownfield Current State

**When to use:** Map and test an **existing** system where **running behavior is the spec** — legacy code, DB, monolith module, or repo with little product documentation. You are **not** replacing the whole system (see `legacy-migration.md`). You **are** mapping what exists today, locking it with AC and tests, then making **explicit change slices**.

**Typical scope:** One **boundary** at a time — module partition, service group, user journey, or API surface.

**Related:** `legacy-migration.md` (full rewrite/cutover). `bug-fix.md` (single defect after map exists). `new-thin-slice.md` (new capability on already-mapped brownfield base).

---

## System of work

| Stage | Scope | Skills (ordered) |
| --- | --- | --- |
| Context (optional) | all | convert-to-markdown, semantic-context-chunker, chunk-markdown, embed-vectors |
| Shaping | all | module-partition, architecture-outline, story-mapping, thin-slicing |
| Discovery | increment | domain-terms, architecture-blueprint, information-architecture (optional) |
| Exploration | increment | ubiquitous-language, acceptance-criteria, ux-mockup (optional), architecture-template (conditional — skip when mechanisms exist) |
| Specification | sprint | CRC (optional), spec-by-example |
| Engineering | sprint | object-model (optional), ATDD, clean-code / stack skill |

### Context stage (when to include)

Include context stage when source material is in non-markdown formats (PDF, PPTX, DOCX, code repos), there are many files to index, or agents need RAG during later stages. Skip when the codebase is the only source and it's already readable, or when context is a short brief.

---

## Scatter rules

| Transition | Rule |
| --- | --- |
| Shaping (all) → Discovery (increment) | Scatter by boundary: thin-slicing produces increments per module boundary. Scatter all — boundaries are known from partition. |
| Exploration (increment) → Specification (sprint) | Group 3-4 stories per sprint. Characterization stories first, change slices last. |

### Sprint grouping heuristic (brownfield)

- **Characterization sprints first**: group stories that describe current behavior together
- **Change slices separate**: stories that modify behavior go into later sprints
- **Per boundary**: don't mix boundaries in a sprint
- Default 3-4 stories per sprint; reduce if stories are complex

---

## JIT policy

- **Scatter all increments** after shaping (boundaries are known from partition)
- **Scatter sprints JIT** — only the next 1-2 increments get sprint decomposition
- Later increments stay as increment-level backlog items until their turn

---

## Checkpoint policy

| Level | When |
| --- | --- |
| Per skill | During shaping (partition + outline are critical) |
| Per stage | After first increment completes exploration |
| Per increment | After first increment finishes engineering (characterization tests pass) |

**Hard gate:** Brownfield boundary gate before exploration. Do not write AC until the map for this boundary passes the gate.

---

## Key constraints

- **Story map is the behavioral spec** for current state — not a separate forensic ledger.
- **Trace before you map** — entry points and flows from code; follow evidence.
- **Bugs and quirks are observed behavior** until a change slice approves a delta.
- **No fix-while-mapping** — no refactor, rename, or redesign during story mapping.
- **Tests against current system** are mandatory before trusting a change.
- **Behavioral deltas** require explicit user/stakeholder approval.
- If **no tests** exist on legacy, characterization tests come before new feature or refactor work.

---

## AI error rate adjustment

- If AI output errors > 10% during exploration (AC quality): shrink scope to per-story tickets for spec
- If errors drop below 5%: expand back to sprint-level across flow
- Tighten checkpoints to per-skill when error rate spikes

---

## Terminal artifacts

| Artifact | Skill | Stage |
| --- | --- | --- |
| Module partition | abd-module-partition | shaping |
| Architecture outline | abd-architecture-outline | shaping |
| Story map + graph | abd-story-mapping | shaping |
| Thin slices | abd-thin-slicing | shaping |
| Domain terms | abd-domain-terms | discovery |
| Ubiquitous language | abd-ubiquitous-language | exploration |
| Architecture blueprint | abd-architecture-blueprint | discovery |
| Information architecture (opt) | abd-information-architecture | discovery |
| AC | abd-acceptance-criteria | exploration |
| UX mockup (opt) | abd-ux-mockup | exploration |
| Architecture template (conditional) | abd-architecture-template | exploration — skip when all increment mechanisms already documented |
| CRC cards (opt) | abd-class-responsibility-collaborator | specification |
| Spec-by-example | abd-specification-by-example | specification |
| Object model (opt) | abd-object-model | engineering |
| Characterization / change tests | abd-acceptance-test-driven-development | engineering |
| Production code (change slices) | abd-clean-code / stack skill | engineering |
