# AGENTS — abd-maps-models-specs

## Process — abd-maps-models-specs

**Pipeline (navigation spine):** Context readiness → Canonical context → Terms & mechanisms → Story map → Domain types → Variants → Deepen → Integrate → Validate & render

## Your role (single source of truth)

The canonical operator narrative lives in **[operator-role.md](content/parts/operator-role.md)**. The same text is **inserted at the top of every phase file** under `phases/` by `scripts/sync_operator_preamble.py` (between `<!-- operator-role:start -->` and `<!-- operator-role:end -->`). After editing `operator-role.md`, run that script, then `python scripts/build.py` to refresh `content/built/agents-staged.md` and `AGENTS.md`.

---

## How to use this document

The **tables in each stage** list Phases 0 through 8 at the row level. You will open `[phases/](content/parts/phases/)` for **step-by-step** instructions for a given phase. If you are reading `AGENTS.md`, the build merges this process section with the full text of every phase file below it.

For long-form rules and artifact shapes, you will open **`content/parts/library/`** (normative contracts and narrative the skill injects or merges):

- [principles-and-rules.md](library/principles-and-rules.md) for principles and cross-cutting rules.
- [execution-and-success.md](library/execution-and-success.md) for what to run next and what “done” means.
- [pipeline_invariants.md](library/pipeline_invariants.md) for gates that apply across phases.
- [context-package.md](library/context-package.md) and [terms-mechanisms-contract.md](library/terms-mechanisms-contract.md) (and the other rows in the documentation library below) when you need **construct-specific** norms.

You will keep `test/mm3/` as the fixture and output root for generated artifacts under `test/mm3/abd-maps-models-specs/` (see [fixture inventory](library/principles-and-rules.md#fixture-inventory-mm3)).

---

## Stage 1 — Context & evidence

### Your role

You establish a **defensible evidence base** before you name terms, write behavioral stories, or promote types. Everything you do here answers one question: *Is this corpus good enough, honestly, for the rest of this pipeline?*

### What you must do

- **Phase 0.** You will assess readiness. You must understand how chunks and the index relate, what the corpus contains, and whether metadata supports later decisions (for example, what should **not** be treated as a subtype). You will record a decision to **adopt**, **extend and freeze**, or **rebuild** the package. Details live in [context-readiness](content/parts/phases/context-readiness.md).
- **Phase 1.** You will define chunking in `context_chunking_spec.yaml` and produce `chunks/*.md` and `context_index.json` according to [context-package.md](library/context-package.md). You will run the Phase 1 pipeline in the **same** stage as the spec (not as a hidden pre-step). You will keep a manifest with source integrity (for example **sha256**) and generator provenance. Then you will run `validate_context_contract.py` when the index exists so the package is enforceable.

You do **not** introduce inheritance or `extends` edges here. You only **package and pin** evidence the later stages will cite by `chunk_id`.

### What you produce

- A recorded **readiness** position.
- When you build, a **frozen context package** that downstream work can treat as **the** evidence layer, without ad hoc files or mystery sources.

### How you know you succeeded

Stage 1 is **done for handoff** to Stages 2–4 only when **all** of the following are true—there is no partial or alternate path:

1. `**context_index.json`** exists and `**validate_context_contract.py` exits zero** (the context contract defines validity; nothing else counts as “validated”).
2. **Chunk files** on disk match the index and the chunking spec—no orphan chunks, no missing files for referenced `chunk_id`s.
3. A **manifest** pins sources and generator provenance (for example **sha256**), per [context-package.md](library/context-package.md).
4. **Readiness** and **audit** outputs describe the **same** package you are freezing—not an aspiration or an older snapshot.

Until (1)–(4) are true, you **do not** start Stage 2. After they are true, Stages 2 through 4 may cite `chunk_id` without inventing provenance.


| #   | Phase                     | Actor        | Script                                                                                                                                                                                                                 | Ref                                                                                                     | Outputs (fixture)                                                            | Summary                                                                                                                                                                                                                                                                              |
| --- | ------------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 0   | Context readiness         | Human + Code | `scripts/phase0_context_audit.py`; `scripts/validate_context_contract.py` (hard gate when `context_index.json` exists)                                                                                                 | [context-readiness](content/parts/phases/context-readiness.md)                                                        | `phase0/phase0_audit_metrics.json`, finding                                  | You measure whether the corpus and chunk or index plumbing are fit for the rest of the pipeline. You profile what is in the package and record a decision to adopt it, extend and freeze it, or rebuild. The outcome is an evidence-backed readiness position, not a finished model. |
| 1   | Canonical context (build) | Human + Code | `test/mm3/context_chunking_spec.yaml` (config); `scripts/validate_context_contract.py`; Phase 1 runnable pipeline per `[context-package.md](library/context-package.md)` (e.g. `build_context.py` when implemented) | [canonical-context](content/parts/phases/canonical-context.md), `[context-package.md](library/context-package.md)` | `context/chunks/*.md` + `context/context_index.json` / frozen **v1** package | You write chunking rules, produce chunk files and a validated index, and pin sources in a manifest so provenance is enforceable. You validate the package when the index exists. The outcome is a frozen context package later work cites by `chunk_id`, without inventing files.    |


---

## Stage 2 — Vocabulary & behavior

### Your role

You separate **language** and **observable behavior** from **domain types**. You ground terms and mechanisms in the **frozen chunks**. You write a **behavioral** story map (who does what to which state) **before** you lock a sparse type system. Evidence and stories must lead type choices, not the reverse.

### What you must do

- **Phase 2.** You will consume the frozen index and chunks. You will emit **terms**, **mechanisms**, and a **candidate queue** (possible types with rationale, still not promoted). Automation and optional AI passes must cite `chunk_id` as [terms-mechanisms-contract.md](library/terms-mechanisms-contract.md) requires.
- **Phase 3.** You will author `mm3_story_map.json` with actor, behavior, anchors, `term_refs`, and `evidence_chunk_ids` where stories are substantive. You will run `validate_phase3_story_map.py`. Details live in [terms-mechanisms](content/parts/phases/terms-mechanisms.md) and [story-map](content/parts/phases/story-map.md).

You do **not** put types in `concepts[]` yet.

### What you produce

- Shared **vocabulary** and **mechanism** artifacts tied to the corpus.
- A **candidate queue** for types (still not promoted).
- A **story map JSON** that reads as **capabilities and anchors**, not a type checklist.

### How you know you succeeded

Your Phase 2 artifacts trace back to `chunk_id`s. Your story map reads as **interaction capability**, not a list aligned to a future type catalog. Substantive stories tie to evidence where it matters. **Promotion** to domain types waits for Stage 3.


| #   | Phase                             | Actor      | Script                                 | Ref                                            | Outputs (fixture)                                                                | Summary                                                                                                                                                                                                                                       |
| --- | --------------------------------- | ---------- | -------------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2   | Terms & mechanisms (layers 1 & 2) | Code + AI  | `scripts/build_phase2_artifacts.py`    | [terms-mechanisms](content/parts/phases/terms-mechanisms.md) | `phase2/mm3_terms_layer.json`, `mm3_mechanisms.json`, `mm3_candidate_queue.json` | You derive terms, mechanisms, and a candidate type queue from the frozen chunks, with mandatory `chunk_id` citations. Automation may assist. The outcome is shared vocabulary and possible types that are still not promoted to `concepts[]`. |
| 3   | Story map (behavioral)            | Human + AI | `scripts/validate_phase3_story_map.py` | [story-map](content/parts/phases/story-map.md)               | `phase3/mm3_story_map.json`                                                      | You author a behavioral story map with actors, behaviors, anchors, and evidence links for substantive stories. You validate against the phase rules. The outcome is a JSON map of capabilities and interactions, not a type catalog.          |


---

## Stage 3 — Domain modeling

### Your role

You add `concepts[]` only where stories and evidence justify **distinct** behavioral contracts. You avoid a large upfront ontology. You decide **variant shape** (enum versus subtypes versus other) **before** you spread properties across types. You deepen approved types with responsibilities, dependencies, and citations so the model is **arguable**.

### What you must do

- **Phase 4.** You will run the **promotion gate**: candidate to **concept** with per-type rationale and explicit rejections (for example, “just a property on X”).
- **Phase 5.** You will write **variant decisions** per family (format is yours to standardize).
- **Phase 6.** You will attach responsibilities, cross-type dependencies, and evidence to types in scope. Optional AI passes must still respect `chunk_id` discipline.

### What you produce

- A **small promoted set** with clear accept and reject rationale.
- **Per-family variant rules** before you churn structure.
- **Deepen** artifacts: responsibilities, `depends_on`, and evidence links for types in scope.

### How you know you succeeded

Your types are explainable at the depth you chose. Variant rules are stable before rework. Every promoted type has evidence. You use `extends` only where real substitution behavior requires it.


| #   | Phase                       | Actor      | Script | Ref                                                        | Outputs (fixture)                        | Summary                                                                                                                                                                                                                      |
| --- | --------------------------- | ---------- | ------ | ---------------------------------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 4   | Domain types (`concepts[]`) | Human + AI | —      | [domain-types](content/parts/phases/domain-types.md)                     | Sparse types + rationale                 | You promote a minimal set of concepts from the candidate queue with per-type rationale and explicit rejections. The outcome is `concepts[]` only where behavior justifies a distinct contract, not a large upfront ontology. |
| 5   | Variant classification      | Human + AI | —      | [variant-classification](content/parts/phases/variant-classification.md) | Written variant decisions per family     | You decide how each variation family is represented before you assign properties broadly. The outcome is written variant decisions per family so structure stays stable through deepen.                                      |
| 6   | Deepen                      | Human + AI | —      | [deepen](content/parts/phases/deepen.md)                                 | Responsibilities, evidence, `depends_on` | You attach responsibilities, cross-type dependencies, and evidence to types in scope, still citing chunks where claims matter. The outcome is an arguable model reviewers can trace to the corpus.                           |


---

## Stage 4 — Integration & delivery

### Your role

You merge parallel work into **one coherent** map, model, and spec (or a deliberate split). You **drain** the candidate queue with explicit decisions. You **prove** quality with automation and visible outputs so reviewers get something **repeatable**, not a one-off edit.

### What you must do

- **Phase 7.** You will integrate synonyms, repoint references, and merge the story map with types and terms. You will **close** or **defer** remaining candidates with rationale.
- **Phase 8.** You will run **scanners** and schema checks, **render** reports, update `generate_context_bundle_manifest.py`, and optionally run a critic pass against [principles and rules](library/principles-and-rules.md). You will wire **CI** on the MM3 fixture for the scope you care about.

### What you produce

- An integrated **map-model-spec** narrative (or an intentional split).
- A **candidate queue** brought to explicit decisions.
- **Validation and reporting** output plus a bundle manifest that ties back to the principles doc.

### How you know you succeeded

Your checks and manifest reproduce for the chosen scope. Your **CI** passes where you wired it. You can **explain** deliverables using provenance, behavioral stories, sparse types, and explicit variants without hand-waving.


| #   | Phase             | Actor      | Script                                                   | Ref                                          | Outputs (fixture)                          | Summary                                                                                                                                                                                                                                  |
| --- | ----------------- | ---------- | -------------------------------------------------------- | -------------------------------------------- | ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 7   | Integrate         | Human + AI | —                                                        | [integrate](content/parts/phases/integrate.md)             | Drained candidate queue → `map-model-spec` | You merge synonyms, align references, and combine story map with types and terms. You close or defer every remaining candidate with rationale. The outcome is one coherent map-model-spec narrative, or a deliberate split you document. |
| 8   | Validate & render | Code + AI  | scanners, reports, `generate_context_bundle_manifest.py` | [validate-render](content/parts/phases/validate-render.md) | CI checks, rendered reports, manifest      | You run scanners and schema checks, render reports, refresh the bundle manifest, and optionally wire CI. The outcome is reproducible validation and visible proof of quality for the chosen scope.                                       |


**Bundle manifest (cross-phase):** `scripts/generate_context_bundle_manifest.py` records hashes for sources and phase outputs. `scripts/build.py` invokes it.

### What `build.py` does for you

`build.py` follows the phase order in this file. It does **not** run a separate “pre-pipeline” ahead of Phase 0.

1. It merges this file and `phases/*.md` into **`content/built/agents-staged.md`**, then writes **`AGENTS.md`** (same body + title). The merge **drops** operator preamble blocks from phases; see [content/built/README.md](../built/README.md).
2. It runs `phase0_context_audit.py` for Phase 0 readiness metrics. When `context_index.json` exists, it runs `validate_context_contract.py` in the same build. That step is a hard gate on the frozen Phase 1 package.
3. It runs the **Phase 1** context build when that entry point exists. It may run `validate_context_contract.py` again afterward. Shapes and contracts are defined in [context-package.md](library/context-package.md).
4. It runs `build_phase2_artifacts.py` after Phase 1 outputs exist and validate.
5. It runs `validate_phase3_story_map.py` according to [behavioral-story-map.md](library/behavioral-story-map.md).
6. It runs `generate_context_bundle_manifest.py` to record hashes of frozen inputs.

Until the Phase 1 entry point exists, you may produce `chunks/` and `context_index.json` by other means. When those files appear, `validate_context_contract.py` still enforces [context-package.md](library/context-package.md).

---

## Documentation library (`docs/`)

The `docs/` folder is the reference library for this skill. Normative process lives in this file and in `phases/`. Construct-specific docs describe one artifact or phase. Cross-cutting docs state rules and order without copying every phase. When you change a stage or phase, you update this file and the phase files, and you align `docs/principles-and-rules.md` and `docs/execution-and-success.md`.


| Document                                                                | Role                                                                                                      |
| ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| [principles-and-rules.md](library/principles-and-rules.md)           | Principles table, cross-cutting rules, fixture inventory                                                  |
| [execution-and-success.md](library/execution-and-success.md)         | Execution order (what to do next) + reusable success definition                                           |
| [context-package.md](library/context-package.md)                     | **Phase 1 only:** `chunks/`, `context_index.json`, manifest, chunking spec, validators, runnable pipeline |
| [context-corpus.md](library/context-corpus.md)                       | How the chunked corpus fits the pipeline (conceptual + flow)                                              |
| [terms-mechanisms-contract.md](library/terms-mechanisms-contract.md) | Phase 2 artifacts + automation                                                                            |
| [behavioral-story-map.md](library/behavioral-story-map.md)           | Phase 3 JSON, validation, rationale                                                                       |
| [pipeline_invariants.md](library/pipeline_invariants.md)             | Cross-cutting gates; layers 1–4; Phases 4–8 artifact summary                                              |
| [domain-model.md](library/domain-model.md)                           | Modules, concepts, `map-model-spec` scaffold                                                              |
| [story-map-narrative.md](library/story-map-narrative.md)             | Full interaction-tree story map (prose)                                                                   |
| [README.md](library/README.md)                                       | Index of this library                                                                                     |


---

## Context readiness (Stage 1 — assessment)



**Goal:** Answer whether the **evidence package** supports downstream modeling **honestly**—traceability, promotion gates, right grain—not to tick a “maturity” box.



**0.1–0.3** are **questions** answered with documents, metrics, and samples—not a numeric “maturity” ladder. If the corpus is **already** inadequate, **record that** and move to **rebuild** ([canonical-context](content/parts/phases/canonical-context.md), Phase 1 in [`content/parts/process.md`](content/parts/process.md)).



When **`chunks/` do not exist yet**, you may **skip** a formal audit; the **same criteria** become **acceptance tests** for the **first** chunking output from Phase 1.



**MM3 fixture (current):** Treat **qualitative spot-check** as **no** (metadata alone does not tell you what **not** to subclass) until a rebuilt package proves otherwise → outcome **insufficient** → **rebuild**.



**Authoritative context:** Phase 0 row in [`content/parts/process.md`](content/parts/process.md); this file expands that row.



## Actor



**Human** judges; **Code** may emit metrics (e.g. `scripts/phase0_context_audit.py`) into `test/mm3/abd-maps-models-specs/phase0/`. When `test/mm3/context/context_index.json` exists, **`scripts/validate_context_contract.py`** runs as part of `scripts/build.py` and enforces the **Phase 1 package** ([`docs/context-package.md`](docs/context-package.md)).



---



## 0.1 Map the plumbing



1. **ID mapping** — Document how chunk files relate to index rows (e.g. `unit_*.md` ↔ `blk_*`). If implicit or missing, **record debt**.

2. **Coverage** — Every chunk in the index; every domain-relevant block has a chunk or **explicit** exclusion.

3. **Version pin** — Hash/date for canonical Markdown and for the index **generator** (if known).



---



## 0.2 Corpus profile (quantitative)



Short report — see plan table: counts by `evidence_type`, `reason` distribution, section spread, `%` noise.



---



## 0.3 Qualitative spot-check



Sample **N** chunks (definitions, tables, examples, rules). **Would a modeler know, from metadata alone, what not to subclass?** If **no** → Phase 1 must supply `modeling_kind` (or equivalent) via schema + chunking +/or re-extraction.



---



## 0.4 Outcomes



| Outcome | Action |

| --- | --- |

| **Sufficient** | Adopt / small schema extension; then **freeze** v1 in Phase 1. |

| **Insufficient** | **Rebuild** in Phase 1 (chunking spec from Markdown—often after **PDF → MD**). |



---



## Exit



Readiness **finding** recorded (adopt vs rebuild). If rebuild: Phase 1 produces the new package; **freeze** contract there.



**See also:** [`docs/context-corpus.md`](docs/context-corpus.md).


---

## Canonical context layer (Stage 1 — build or freeze the contract)



**Goal:** A **single, versioned** contract for “what evidence is,” independent of map/model/spec JSON.



**Normal path** when `chunks/` are not present yet:



1. **Canonical Markdown** — Declare paths in **`solution.conf` → `manifest_sources[]`** (resolved by `_config.py`). The MM3 fixture lists `docs/HeroesHandbook.md` from **PDF → MD** (or other conversion); pin versions.

2. **Chunking + index** — **Written chunking spec first** (grain, metadata, exclusions), then scripts—aligned with **principles** (provenance-first, evidence typing for promotion gates, explicit noise). See Phase 1 in [`content/parts/process.md`](content/parts/process.md) and [`docs/context-corpus.md`](docs/context-corpus.md) *First chunking is more than…*.



If an existing package is **adopted** after [context-readiness](content/parts/phases/context-readiness.md), this phase **migrates / extends** schema and **freezes** v1.



**Authoritative context:** Phase 1 row in [`content/parts/process.md`](content/parts/process.md); this file expands that row.

**Normative file/schema detail:** [`docs/context-package.md`](docs/context-package.md) — chunk front matter, `context_index.json`, chunking spec path from `solution.conf`, validators, single script surface.



---



## 1.1 Artifacts



- `context_index.json` with at minimum: `chunk_id`, `source_anchor`, `modeling_kind`, `evidence_type`, `modeling_priority`, optional `candidate_terms[]`.

- **Rules:** Promotion of `example` / `narrative_aside` / `metadata/noise` into `extends` or `concepts[]` uses an explicit **promotion** record.



---



## 1.2 Validation



- **`scripts/validate_context_contract.py`** — bidirectional alignment: every `blocks[]` row has `chunks/{chunk_id}.md`; every chunk file is indexed or listed under `excluded[]`; required front matter `chunk_id`. Rules evolve with [`docs/context-package.md`](docs/context-package.md).

- **Relationship edges** (e.g. `extends`, `inherits`) enter the model through **explicit** later phases with stated criteria.



---



## 1.3 Exit criteria



- Readiness outcome **documented** ([context-readiness](content/parts/phases/context-readiness.md)).

- Index schema **frozen** as v1 of the **context package** for this skill.



### 1.4 Where the full schema lives



Phase 1 **provenance** (files, validators, config, runnable pipeline) is specified in [`docs/context-package.md`](docs/context-package.md). Phases 2–3 have their own docs ([`terms-mechanisms-contract.md`](docs/terms-mechanisms-contract.md), [`behavioral-story-map.md`](docs/behavioral-story-map.md)); they are not “extra steps before Phase 1.”



---



**See also:** [`docs/context-corpus.md`](docs/context-corpus.md).


---

## Terms & mechanisms (layers A & B)



**Goal:** Glossary and **named processes** exist **before** sparse `concepts[]`.



**Authoritative context:** Phase 2 row in [`content/parts/process.md`](content/parts/process.md); this file expands that row.



## Actor



**Code** runs `scripts/build_phase2_artifacts.py`. **Human / AI** curate terms and mechanisms.



## What this phase produces



- **Terms** — surface vocabulary + chunk links; not classes.

- **Mechanisms** — workflows/lifecycles with steps + evidence.

- **Candidate queue** — “possible type” with rationale; **not** in `concepts[]` yet.



## Exit



Promotion rule written: **candidate → concept** only through the **domain-types** gate (Phase 4)—not by renaming a mention or string co-occurrence.



**Outputs:** `test/mm3/abd-maps-models-specs/phase2/mm3_terms_layer.json`, `mm3_mechanisms.json`, `mm3_candidate_queue.json`.



**Implementation notes:** [`docs/terms-mechanisms-contract.md`](docs/terms-mechanisms-contract.md) (includes **inputs** and **`chunk_id` citation** rules for Phase 2).


---

## Story map (behavioral)



**Goal:** Epics/stories that satisfy **actor → behavior → anchor** (domain state **read** and/or **write**); alignment allows **term** references without minting types.



**Authoritative context:** Phase 3 row in [`content/parts/process.md`](content/parts/process.md); this file expands that row.



## Actor



**Code** runs `scripts/validate_phase3_story_map.py`. **Human / AI** maintain `mm3_story_map.json`.



## Requirements



- Every story has a **clear** behavioral reading and **traceability** to concepts.

- No story exists solely to **match strings** in the type list.

- Every story states its **anchor** (read path, write path, or both)—not every story requires **mutation** of the core write model.

- **Query/read/forward** stories are as valid as **mutating** stories when the anchor is explicit.

- Substantive stories carry **`evidence_chunk_ids[]`** referencing frozen **`context_index.json`** / `chunks/` ([`docs/behavioral-story-map.md`](docs/behavioral-story-map.md)); `validate_phase3_story_map.py` extends to enforce this when authored.



## Exit



Story map validated; **domain types** (`concepts[]`) follow after the behavioral story map is sound.



**Output:** `test/mm3/abd-maps-models-specs/phase3/mm3_story_map.json` (when present).



**Docs:** [`docs/behavioral-story-map.md`](docs/behavioral-story-map.md) (shape + why stories before types), full narrative [`docs/story-map-narrative.md`](docs/story-map-narrative.md).


---

## Domain types (`concepts[]`)



**Goal:** **Sparse** types; **reject gate** (“not just a property on a broader type”).



**Authoritative context:** Phase 4 row in [`content/parts/process.md`](content/parts/process.md); this file expands that row.



## Steps



1. Promote candidates through **explicit** domain-types gate only (no string co-occurrence shortcuts).

2. Record **per-type rationale**; keep type count tractable for the fixture depth.

3. Align prose and JSON with [`docs/domain-model.md`](docs/domain-model.md) (modules, properties, `extends`, examples).



## Exit



Type count and rationale remain reviewable for the MM3 fixture at the chosen depth.


---

## Variant classification



**Goal:** Per family: **enum vs `extends`** **before** property churn.



**Authoritative context:** Phase 5 row in [`content/parts/process.md`](content/parts/process.md); this file expands that row.



## Steps



1. For each variant family, record the **decision**: enum vs subtypes vs other **before** bulk property assignment.

2. Align with **Explicit variant representation** in [`docs/principles-and-rules.md`](docs/principles-and-rules.md) / plan principles table.



## Exit



Written **variant decision** per family before bulk modeling.


---

## Deepen



**Goal:** Responsibilities and evidence on **approved** types only; **topological** `depends_on`.



**Authoritative context:** Phase 6 row in [`content/parts/process.md`](content/parts/process.md); this file expands that row.



## Steps



1. Attach evidence citations to approved types; citations **support** claims—they do not **auto-create** types.

2. Model `depends_on` where appropriate (acyclic, reviewable).



## Exit



Every type has **evidence** citations; relationships follow explicit gates from the principles table.


---

## Integrate



**Goal:** Synonyms, repointing, **drain candidate queue** into final `map-model-spec` (or split artifacts if story map stays separate).



**Authoritative context:** Phase 7 row in [`content/parts/process.md`](content/parts/process.md); this file expands that row.



## Steps



1. Reconcile synonyms and duplicate references.

2. Move approved candidates from the queue into `concepts[]` / final spec per promotion rules.

3. Keep **domain narrative** and **story map** aligned when both artifacts exist.



## Exit



Single coherent map-model-spec (or documented split) ready for validation.


---

## Validate & render



**Goal:** Automated checks (scanners, schema) + **rendered** reports; CI on MM3; optional **critic** checklist against the **principles table** in [`docs/principles-and-rules.md`](docs/principles-and-rules.md).



**Authoritative context:** Phase 8 row in [`content/parts/process.md`](content/parts/process.md); this file expands that row.



## Actor



**Code** — `skill-config` scanners, `scripts/generate_context_bundle_manifest.py` (invoked from `scripts/build.py`). **Human / AI** — review reports.



## Steps



1. Run structural / schema scanners defined for the skill.

2. Render reports as configured (paths under fixture output root).

3. Optional: critique pass against [`docs/principles-and-rules.md`](docs/principles-and-rules.md) (external expert or checklist).



## Exit



Reproducible validation + manifest; CI green for the MM3 fixture at the chosen scope.
