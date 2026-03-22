# Principles, cross-cutting rules, and fixture inventory

This document **lives in `docs/`** as the enduring, skill-owned reference for **why** we work this way. **Execution order** is in [`execution-and-success.md`](execution-and-success.md); the **phase table** is in [`content/parts/process.md`](../content/parts/process.md). When principles change, update **this file**, [`execution-and-success.md`](execution-and-success.md), and the process table in the **same edit** where the change matters downstream. **Phase 1** shapes (chunk/index schema, validators) are normative in [`context-package.md`](context-package.md)—update that doc when provenance rules or Phase 1 gates change.

---

## Principles we commit to (positive)

These are **normative**: we implement the process **because** of them. If evidence shows a principle is wrong for a domain, **change the principle** (this file and the process docs above)—do not silently bend the process.

| Principle | Grounding (research / practice) | What we commit to | Outcomes we want | States we avoid |
| --- | --- | --- | --- | --- |
| **Provenance-first evidence** | Traceability in requirements engineering (e.g. IEEE-style bidirectional trace); evidence-based methods in policy and safety-critical domains; DDD emphasis on **distilling** the model **from** the source, not inventing ahead of it. | **Two separate moves:** (1) **Evidence** ties claims to **where** they come from (`chunk_id` / anchors). (2) **Promotion** decides **what** they become—term, mechanism, story, property, enum, type, relationship—using **that layer’s** criteria. Citations are **necessary** for substantive choices; they are **not sufficient** to mint a class or edge. | Same links can support honest **layering**; traceability without **automatic** typing. | Treating “cited here” as “therefore a `concepts[]` row”; skipping promotion because traceability already passed. |
| **Behavioral description of value** | Use-case and scenario modeling (e.g. Jacobson); story mapping (Patton); realized **through** **story maps**, **stories**, and **story specifications** (BDD-style **when/then** scenarios). | **Stories** are **interactions**: primary **actor** performs an **operation** on a **subject** in the domain. **Anchor** each story: **what** state (or read model / projection) the interaction **uses** or **changes** (and name **policy/SLO** only when it is part of the spec for that story—not a separate mandatory template in *this* process). Distinguish **mutation** of authoritative domain state vs **observation**—**reads**, **pass-through**, **forward**, **query** all count; not every story implies an aggregate **write**. **When/then** still asserts something **verifiable** (including observable reads or effects). Optional secondary actors. Structure lives in the **story map**; the written **spec** is scenarios / when-then / AC on each story. | Maps that read as **capability**, not noun lists; one clear behavioral lane (map → story → spec). | Stories that are only labels, tables, or ungrounded fragments; **extra** behavioral write-ups that **duplicate** map/story/spec without a stated reason. |
| **Layered vocabulary** | Ontology engineering: **terms** vs **classes**; DDD **ubiquitous language** vs **model**; separation of **glossary** from **type system**. | **Terms** and **named mechanisms** (processes, lifecycles) live in **their own** artifacts; **domain types** are promoted **only** through the type gate—not by renaming a mention. | Shared language; controlled growth of types; **distinct** promotion paths per layer. | One-step “surface word → class” without a **separate** promotion decision. |
| **Sparse, intentional domain types** | Classic OO/domain modeling: types for things with **identity**, **lifecycle**, and **distinct** responsibilities (Evans, Rumbaugh-style information modeling). | `concepts[]` holds **types** only where the problem space needs **separate** behavioral/state contracts; otherwise properties, enums, or terms. | Small, explainable type system; composition where it fits. | Unbounded type list; duplicate abstractions differing only by name. |
| **Justified specialization** | Liskov substitutability: subtyping where **substitution** is meaningful in the **operations** that matter. | `extends` (or equivalent) only where specialization is **semantically** warranted and **checked** against use. | Predictable hierarchies; safe generalization. | Decorative inheritance; “is-a” from layout or co-occurrence alone. |
| **Explicit variant representation** | Analysis patterns: **enumeration** vs **classification hierarchy** (Fowler et al.); domain-driven choice per **family** of variation. | For each variant family, record the **decision**: enum vs subtypes vs other, **before** mass property assignment. | Consistent representation; fewer migration surprises. | Defaulting to inheritance because it is fewer JSON fields. |
| **Corpus understanding before type design** | Qualitative coding / corpus profiling; information architecture of large documents. | **Readiness (Stage 1)** produces **metrics and samples** on the evidence base **before** a full type set—or validates the **first** chunking pass against the same bar. **Not** a maturity “step”: honest judgment; rebuild when insufficient. | Right grain of evidence; prioritized reading; defensible gates. | Modeling before knowing what the source actually contains. |

---

## Cross-cutting rules

- **Where vs what:** **Where** something is anchored (evidence) and **what** it is in the model (term, story, property, type, …) are **different states**. The process may reuse the same `chunk_id` in more than one layer; each layer applies its own gate.

- **Behavioral anchoring:** A story need not **mutate** core domain state; it must be **anchored**—**which** state or projection is **read**, **passed**, or **forwarded**, **or** **which** state is **written**, **or** **which** constraint/SLO applies. **Read** and **write** paths are both **first-class**; silence on anchor is not.

---

## How to attack a principle

Bring **counterexamples** from a domain, or **citations** that the grounding does not hold; then **revise** the table and [`content/parts/process.md`](../content/parts/process.md) / phase files in the **same edit**.

---

## Fixture inventory (MM3)

Paths are relative to **`active_skill_workspace`** in `<skill_path>/conf/abd-config.json` (the MM3 fixture uses `test/mm3/`). Deprecated keys `solution_workspace` / `skill_space_path` are still read by `scripts/_config.py`.

| Asset | Role |
| --- | --- |
| `solution.conf` | **Workspace config** — `manifest_sources[]`, `output_dir`, `context_path`, chunking spec path, etc. (`scripts/_config.py` reads this). |
| `docs/*.md` (e.g. `docs/HeroesHandbook.md`) | Canonical **source** markdown when listed in `manifest_sources[]` (pin or version when it changes). |
| `<context_path>/chunks/<chunk_id>.md` | **Chunk files** — one file per id; front matter includes **`chunk_id`** matching the filename stem. **Optional** until Phase 1 materializes chunks. |
| `<context_path>/context_index.json` | **Index** — **optional** until Phase 1; `blocks[]` rows use **`chunk_id`** and/or **`block_id`** (validator accepts either). Other fields per [`context-package.md`](context-package.md). |
| `<output_dir>/` (e.g. `abd-maps-models-specs/`) | **Generated outputs only** — `phase0/`, `phase2/`, `phase3/mm3_story_map.json`, `maps-models-specs/map-model-spec.json`, manifest, etc. **Not** the skill package. |

**Not the skill package:** The skill (`SKILL.md`, `content/`, `scripts/`, …) lives **beside** the MM3 workspace folder; pipeline writes go under **`<workspace>/<output_dir>/`**, not into the skill tree.

**See also:** [`context-corpus.md`](context-corpus.md) (corpus → chunking). **Normative Phase 1 shapes and validators:** [`context-package.md`](context-package.md); `scripts/validate_context_contract.py` implements the chunk/index contract when `context_index.json` exists.
