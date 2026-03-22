# abd-maps-models-specs — reusable process plan

*Working plan — lives in `plan/` (transient). Long-lived reference docs belong in `docs/`.*

This plan describes a **repeatable** path from **source markdown** through **evidence**, **vocabulary layers**, **behavioral stories**, and **sparse domain types**, to a **validated** map / model / spec. It is written so principles can be **argued on merit**: each has **stated grounding** (research and established practice), not reactions to any prior attempt.

**Fixture in scope:** `skills/abd-maps-models-specs/test/mm3/` — operator paths and roles for canonical sources live in **`solution.conf` → `manifest_sources`** (MM3 lists `docs/HeroesHandbook.md`); `context/chunks/` and `context/context_index.json` **when present** (they may **not** exist yet—see Stage 1 below).

**Not the skill package:** Generated pipeline artifacts go **only** under `test/mm3/abd-maps-models-specs/` (output root — same name as the skill **by convention**, not a second copy of the skill). The skill itself (plan, `SKILL.md`, automation) lives in `skills/abd-maps-models-specs/` **above** `test/`.

---

## Stages vs. “Phase 0” (read this)

The **process table** in `content/parts/process.md` groups work into **stages** (e.g. Stage 1 — Context & evidence). **Stage 1 is not a maturity ladder** where you tick boxes to feel done.

- **Phase 0** is a **readiness stage**: *Is the evidence package good enough to support downstream asks (terms, behavioral story map, sparse types)—honestly?* The substeps **0.1–0.3** are **questions you answer with documents + metrics + samples**, not a ritual “step” on a scale.
- If you **already know** the answer is **no** (wrong grain, bad metadata, IDs unusable, or spot-check fails), **do not** perform a fake open “keep vs rebuild” debate—**document the finding** and **rebuild** per Phase 1.
- **Phase 1** **does not assume** `chunks/` already exist. A normal greenfield path is **PDF (or other source) → canonical Markdown → first chunking + index** (see Phase 1). Phase 0’s criteria still define **what “good enough” means** for the **first** cut you ship from Phase 1.

---

## Principles we commit to (positive)

These are **normative**: we implement the process **because** of them. If evidence shows a principle is wrong for a domain, **change the principle** (and this document)—do not silently bend the process.


| Principle                                   | Grounding (research / practice)                                                                                                                                                                                                        | What we commit to                                                                                                                                                                                                                                                                                                                                             | Outcomes we want                                                                                  | States we avoid                                                                                                                                          |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Provenance-first evidence**               | Traceability in requirements engineering (e.g. IEEE-style bidirectional trace); evidence-based methods in policy and safety-critical domains; DDD emphasis on **distilling** the model **from** the source, not inventing ahead of it. | **Two separate moves:** (1) **Evidence** ties claims to **where** they come from (`chunk_id` / anchors). (2) **Promotion** decides **what** they become—term, mechanism, story, property, enum, type, relationship—using **that layer’s** criteria. Citations are **necessary** for substantive choices; they are **not sufficient** to mint a class or edge. | Same links can support honest **layering**; traceability without **automatic** typing.            | Treating “cited here” as “therefore a `concepts[]` row”; skipping promotion because traceability already passed.                                         |
| **Behavioral description of value**         | Use-case and scenario modeling (e.g. Jacobson); story mapping (Patton); realized **through** **story maps**, **stories**, and **story specifications** (BDD-style **when/then** scenarios).                                            | **Stories** are **interactions**: primary **actor** performs an **operation** on a **subject** in the domain. **Anchor** each story: **what** state (or read model / projection) the interaction **uses** or **changes** (and name **policy/SLO** only when it is part of the spec for that story—not a separate mandatory template in *this* process). Distinguish **mutation** of authoritative domain state vs **observation**—**reads**, **pass-through**, **forward**, **query** all count; not every story implies an aggregate **write**. **When/then** still asserts something **verifiable** (including observable reads or effects). Optional secondary actors. Structure lives in the **story map**; the written **spec** is scenarios / when-then / AC on each story. | Maps that read as **capability**, not noun lists; one clear behavioral lane (map → story → spec). | Stories that are only labels, tables, or ungrounded fragments; **extra** behavioral write-ups that **duplicate** map/story/spec without a stated reason. |
| **Layered vocabulary**                      | Ontology engineering: **terms** vs **classes**; DDD **ubiquitous language** vs **model**; separation of **glossary** from **type system**.                                                                                             | **Terms** and **named mechanisms** (processes, lifecycles) live in **their own** artifacts; **domain types** are promoted **only** through the type gate—not by renaming a mention.                                                                                                                                                                           | Shared language; controlled growth of types; **distinct** promotion paths per layer.              | One-step “surface word → class” without a **separate** promotion decision.                                                                               |
| **Sparse, intentional domain types**        | Classic OO/domain modeling: types for things with **identity**, **lifecycle**, and **distinct** responsibilities (Evans, Rumbaugh-style information modeling).                                                                         | `concepts[]` holds **types** only where the problem space needs **separate** behavioral/state contracts; otherwise properties, enums, or terms.                                                                                                                                                                                                               | Small, explainable type system; composition where it fits.                                        | Unbounded type list; duplicate abstractions differing only by name.                                                                                      |
| **Justified specialization**                | Liskov substitutability: subtyping where **substitution** is meaningful in the **operations** that matter.                                                                                                                             | `extends` (or equivalent) only where specialization is **semantically** warranted and **checked** against use.                                                                                                                                                                                                                                                | Predictable hierarchies; safe generalization.                                                     | Decorative inheritance; “is-a” from layout or co-occurrence alone.                                                                                       |
| **Explicit variant representation**         | Analysis patterns: **enumeration** vs **classification hierarchy** (Fowler et al.); domain-driven choice per **family** of variation.                                                                                                  | For each variant family, record the **decision**: enum vs subtypes vs other, **before** mass property assignment.                                                                                                                                                                                                                                             | Consistent representation; fewer migration surprises.                                             | Defaulting to inheritance because it is fewer JSON fields.                                                                                               |
| **Corpus understanding before type design** | Qualitative coding / corpus profiling; information architecture of large documents.                                                                                                                                                    | **Readiness for modeling** (Stage 1) produces **metrics and samples** on the evidence base **before** committing to a full type set. That may mean auditing an **existing** chunk/index **or** validating the **first** chunking pass against the same criteria.                                                                                                                                                                                                                           | Right grain of evidence; prioritized reading; defensible gates.                                   | Modeling before knowing what the source actually contains.                                                                                               |


**Rule (cross-cutting):** **Where** something is anchored (evidence) and **what** it is in the model (term, story, property, type, …) are **different states**. The process may reuse the same `chunk_id` in more than one layer; each layer applies its own gate.

**Rule (behavioral anchoring):** A story need not **mutate** core domain state; it must be **anchored**—**which** state or projection is **read**, **passed**, or **forwarded**, **or** **which** state is **written**, **or** **which** constraint/SLO applies. **Read** and **write** paths are both **first-class**; silence on anchor is not.

**How to attack a principle:** Bring **counterexamples** from a domain, or **citations** that the grounding does not hold; then **revise** the table and the phases below in the same edit.

---

## A. Current fixture inventory


| Asset                                 | Role                                                                                                                             |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `test/mm3/solution.conf`              | **Workspace config** — `manifest_sources[]`, `context_path`, `context_chunking_spec`, etc. (same layering as the prior skill).     |
| `test/mm3/docs/HeroesHandbook.md`     | Canonical **source** markdown for the MM3 fixture (listed in `manifest_sources`; pin version when it changes).                     |
| `test/mm3/context/chunks/unit_*.md`   | **Evidence units** — text + stable IDs for citation.                                                                             |
| `test/mm3/context/context_index.json` | Index: **manifest** (sources, section counts) + **blocks** with `block_id`, `section_path`, `reason`, `evidence_type`, previews. |
| `test/mm3/abd-maps-models-specs/`     | **Output only** — phase artifacts the skill **generates** (not the skill package; see folder README).                            |


**Readiness (Phase 0)** decides whether an **evidence package**—when it exists—satisfies the **context contract**, or whether **chunking and indexing** must be **redefined** from canonical Markdown under explicit rules (same principles; fresh artifacts). When there is no package yet, **Phase 1** is where you **build** that package; Phase 0’s questions remain the **acceptance bar** for that build.

---

## Phase 0 — Context readiness (Stage 1: assessment, not a “maturity step”)

**Goal:** Answer one question: **Is this context good enough** for downstream modeling (terms, mechanisms, story map, sparse types)—**with traceability and promotion gates intact**?

This is **analysis-first**. Deliverables are **documents + metrics + samples**, not a domain model.

**Important:** Subsections **0.1–0.3** are **assessment prompts**, not a linear checklist you complete to “pass” a scale. If the honest answer is already **no** (e.g. MM3 today: **spot-check fails**—a modeler **cannot** tell what **not** to subclass from metadata alone), **record that** and move to **rebuild** (Phase 1). Do not pretend the decision is still open.

**When `chunks/` do not exist yet:** You may **skip** a formal audit and treat Phase 0 as **embedded acceptance criteria** for the **first** chunking output from Phase 1—the same questions still apply before you freeze the contract.

### 0.1 Map the plumbing

1. **ID mapping** — Document how chunk files relate to index rows (e.g. `unit_*.md` ↔ `blk_*` / `chunk_id`)—one-to-one, many-to-one, naming convention. If the link is implicit or missing, **record that as debt**.
2. **Coverage** — Does every chunk file appear in the index? Does every **domain-relevant** block have a chunk (or **explicit** exclusion in the index)?
3. **Version pin** — Hash or date for canonical **Markdown** (e.g. `HeroesHandbook.md`) and for the **generator** that produced the index (if known).

### 0.2 Corpus profile (quantitative)

Produce a **short report** (markdown or JSON summary):


| Metric                                      | Why it matters                                                                                                                                  |
| ------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Count of chunks / blocks by `evidence_type` | See if “noise” vs “rule” vs “example” is usable for **promotion gates**.                                                                        |
| Distribution of `reason`                    | e.g. `structural heading only`, `below_min_chunk` — assess whether chunk **grain** matches **semantic** use (definitions vs noise vs examples). |
| Section path depth / chapter spread         | For **stratified sampling** (high-signal chapters first).                                                                                       |
| % blocks flagged `metadata/noise`           | Informs whether **modeling_kind** is already there or must be **re-inferred**.                                                                  |


### 0.3 Qualitative spot-check

- Sample **N** chunks across chapters: definitions, tables, examples, rule blocks.
- Ask: **Would a modeler** know, from metadata alone, what **not** to subclass? If **no**, the **canonical context** work must supply `modeling_kind` (or equivalent)—via **schema**, **re-chunking**, or **re-run** of extraction—not wishful thinking.

**MM3 (current fixture):** Treat the answer here as **no** until a rebuilt package proves otherwise.

### 0.4 Outcomes (honest, not theatrical)


| Outcome | Action |
| --- | --- |
| **Sufficient** — IDs stable, evidence types usable for gates, mapping clear; spot-check **yes** or fixable with a **small** schema extension | **Adopt** current chunks + index; **extend** schema (e.g. `modeling_kind`, `modeling_priority`) in place or via sidecar JSON, then **freeze** v1 in Phase 1. |
| **Insufficient** — noisy blocks dominate, chunk/blocks misaligned, IDs unusable, or spot-check **no** | **Rebuild:** Phase 1 — **chunking spec** from canonical Markdown (often after **PDF → MD**), regenerate chunks + index, **version** the bundle. Record the decision and move to rebuild when the evidence fails the principles. |

---

## Phase 1 — Canonical context: source Markdown → chunking → frozen contract

**Goal:** A **single, versioned** contract for “what evidence is,” independent of map/model/spec JSON.

**Do not assume** pre-existing `chunks/`. Typical upstream steps:

1. **Canonical source Markdown** — Often **`HeroesHandbook.md`** produced by **PDF (or DOCX, etc.) → Markdown** conversion. Pin version (hash/date) of the **source file** and of the **converter** when relevant.
2. **First chunking + index** — Chunking is **designed** (not ad hoc splits) so downstream work can honor the **principles**:
   - **Provenance-first evidence:** stable `chunk_id` / anchors; traceable citations.
   - **Layered vocabulary / promotion:** per-chunk **evidence typing** (and related fields) so **terms** vs **types** stays honest—**citation ≠ class**.
   - **Corpus understanding before type design:** grain supports **stratified reading**; **noise** is labeled and excluded **explicitly** in the index, not silently dropped.
   - **Spot-check test:** metadata should make it **plausible** to see what is **not** a subtype candidate (`modeling_kind` or equivalent).

**Automation:** implement **one** Phase 1 context-build path under **`skills/abd-maps-models-specs/scripts/`** (see [`docs/context-package.md`](../docs/context-package.md) — runnable pipeline is part of Phase 1, not a separate pre-phase): canonical Markdown → rules in `context_chunking_spec.yaml` → `chunks/` + `context_index.json`. **Rules first**, then code.

### 1.1 Artifacts

- `chunk-index.json` (or evolved `context_index.json`) with at minimum: `chunk_id`, `source_anchor`, `modeling_kind`, `evidence_type`, `modeling_priority`, optional `candidate_terms[]`.
- **Rules:** Promotion of `example` / `narrative_aside` / `metadata/noise` into `extends` or `concepts[]` uses an explicit **promotion** record.

### 1.2 Validation

- Script: every file under `chunks/` has index row; every index row has a file (or documented orphan).
- **Relationship edges** (e.g. `extends`, `inherits`) enter the model only through **explicit** steps with **stated** criteria—not from **string co-occurrence** heuristics in code.

### 1.3 Exit criteria

- Readiness outcome **documented** (adopt vs rebuild—and **rebuild** is expected when starting from a bad or missing package).
- Index schema **frozen** as v1 of the **context contract** for this skill.

### 1.4 Phase 1 package (how Phase 1 proves provenance)

Principles are not enough: **Phase 1** must be specified as **files, validators, and config**—not “whatever the script outputs.” The normative detail lives in **[`docs/context-package.md`](../docs/context-package.md)**. Summary:

| Mechanism | What we use |
| --- | --- |
| **Single pipeline** | Runnable automation under **`skills/abd-maps-models-specs/scripts/`** — one Phase 1 context builder entry point per [`context-package.md`](../docs/context-package.md). |
| **Chunk files** | `test/mm3/context/chunks/{chunk_id}.md` with YAML front matter: `chunk_id`, `source` (canonical path + **line range and/or heading_path**), `evidence_type`, `modeling_kind`. |
| **Index** | `test/mm3/context/context_index.json`: `manifest.sources[]` with **sha256** of canonical handbook; `manifest.generator`; `blocks[]` with duplicate `source_anchor` + previews; optional `excluded[]`. |
| **Config** | `test/mm3/context_chunking_spec.yaml` — section/chapter break rules, split limits, taxonomy enums (operators edit **this**, not scattered magic in multiple scripts). |
| **Code vs LLM** | **Deterministic** Python applies the spec and writes chunks + index. Optional LLM may **refine** `evidence_type` / `modeling_kind` **after** blocks exist; output must still pass the same validator. |
| **Validation** | `scripts/validate_context_contract.py` — bidirectional chunk ↔ index, line bounds, duplicate IDs. Phase 0/CI use this as the **hard** gate. |

Downstream (Phases 2–8): same doc spells out **inputs/outputs**, how **`build_phase2_artifacts.py`** must cite `chunk_id`s, how **`validate_phase3_story_map.py`** checks `evidence_chunk_ids[]` against the index, and how Phases 4–8 use JSON, prompts, or scanners—so each step has an implementable shape.

---

## Phase 2 — Terms & mechanisms (layers A & B)

**Goal:** Glossary and **named processes** exist **before** sparse `concepts[]`.

- **Terms** — surface vocabulary + chunk links; not classes.
- **Mechanisms** — workflows/lifecycles with steps + evidence.
- **Candidate queue** — “possible type” with rationale; **not** in `concepts[]` yet.

**Exit:** Promotion rule written: **candidate → concept** only through Phase 4 gate.

---

## Phase 3 — Story map (behavioral)

**Goal:** Epics/stories that satisfy **actor → behavior → anchor** (domain state **read** and/or **write**); alignment allows **term** references without minting types. **Query/read/forward** stories are as valid as **mutating** stories when the anchor is explicit.

**Exit:** Every story has a **clear** behavioral reading and **traceability** to concepts; no story exists solely to **match strings** in the type list. Every story states its **anchor** (read path, write path, or both)—not every story requires **mutation** of the core write model.

**Why before domain types (Phase 4)?** Short rationale: [`docs/why-story-mapping-first.md`](../docs/why-story-mapping-first.md).

---

## Phase 4 — Domain types (`concepts[]`)

**Goal:** **Sparse** types; **reject gate** (“not just a property on a broader type”).

**Exit:** Type count and **per-type rationale** remain tractable for the MM3 fixture at the chosen depth.

---

## Phase 5 — Variant classification

**Goal:** Per family: **enum vs `extends`** **before** property churn.

**Exit:** Written **variant decision** per family before bulk modeling.

---

## Phase 6 — Deepen

**Goal:** Responsibilities and evidence on **approved** types only; **topological** `depends_on`.

**Exit:** Every type has **evidence** citations; citations **support** claims, they do not **auto-create** types.

---

## Phase 7 — Integrate

**Goal:** Synonyms, repointing, **drain candidate queue** into final `map-model-spec` (or split artifacts if you keep story map separate).

---

## Phase 8 — Validate & render

**Goal:** Automated checks (scanners, schema) + **rendered** reports; CI on MM3; optional **critic** checklist against the **principles table** at the top of this document.

---

## Execution order (what to do next)

1. **Context path A — Greenfield or known bad:** Ensure **canonical Markdown** (e.g. PDF → `HeroesHandbook.md`). **Write the chunking spec** (what grain, what metadata, what exclusions), then implement **Phase 1** (chunks + index + version pin). Use **Phase 0** questions as **acceptance** for that package before freezing v1.
2. **Context path B — Existing `context/`:** Run **readiness** (Phase 0: metrics + spot-check)—**or** skip straight to rebuild if you already know it fails (e.g. MM3: spot-check **no**).
3. If **adopt with extensions:** migrate or sidecar into canonical schema; fill `modeling_kind`; **freeze** v1.
4. If **rebuild or first build:** complete Phase 1; **freeze** the Phase 1 package (see **§1.4** below and [`docs/context-package.md`](../docs/context-package.md)).
5. Only then: **Phase 2** onward in order — run `python scripts/build_phase2_artifacts.py` — emits `test/mm3/abd-maps-models-specs/phase2/` (terms, mechanisms, candidate queue). See [`docs/terms-mechanisms-contract.md`](../docs/terms-mechanisms-contract.md). Re-run `generate_context_bundle_manifest.py` to record phase2 hashes.
6. **Phase 3**: maintain `test/mm3/abd-maps-models-specs/phase3/mm3_story_map.json` (behavioral epics/stories with **anchor** + `term_refs` / `evidence_chunk_ids`). Validate with `python scripts/validate_phase3_story_map.py` (extend per [`docs/behavioral-story-map.md`](../docs/behavioral-story-map.md)). Re-run `generate_context_bundle_manifest.py` for phase3 hash.
7. **Phase 4–8**: types → variants → deepen → integrate → validate/render (per sections above and [`docs/pipeline_invariants.md`](../docs/pipeline_invariants.md)).

---

## Success definition (reusable)

Another domain (another handbook) should be able to:

1. Supply **source material** (typically **PDF → Markdown**, then chunking) and land on the **same context contract** after Phase 1 (frozen index + rules).
2. Run **2–8** such that **relationships** and **types** follow **explicit** gates and the **principles table**—not accidental **co-occurrence** or **string matching**.

---

*This file is operational **what next**. Enduring **why** and historical analysis may live in `docs/` when promoted from `plan/`. When the process stabilizes, archive or replace `plan/PROCESS-PLAN.md` with a shorter operator guide in `docs/`.*