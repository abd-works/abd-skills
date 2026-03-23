# AGENTS — abd-maps-models-specs

## Process — abd-maps-models-specs

**Pipeline (navigation spine):** Context chunking approach → Canonical context → Terms & mechanisms → Story map → Domain types → Variants → Deepen → Integrate → Validate & render

---

## How to use this document

**Normative procedure** for each phase lives in **`content/parts/phases/<phase>.md`**. **This file** is a **summary only**: pipeline spine, staged goals, and a **one-row sketch** per phase in the tables—**not** a substitute for the phase document. Open `[phases/](content/parts/phases/)` for authoritative steps, exit criteria, and artifacts. If you are reading `AGENTS.md`, the build merges this process section with the full text of every phase file below it.

For long-form rules and artifact shapes, you will open `**content/parts/library/`** (normative contracts and narrative the skill injects or merges):

- [principles-and-rules.md](library/principles-and-rules.md) for principles and cross-cutting rules.
- [execution-and-success.md](library/execution-and-success.md) for what to run next and what “done” means.
- [pipeline_invariants.md](library/pipeline_invariants.md) for gates that apply across phases.
- [context-spec.md](library/context-spec.md) and [terms-mechanisms-contract.md](library/terms-mechanisms-contract.md) (and the other rows in the documentation library below) when you need **construct-specific** norms.

You will keep `test/mm3/` as the fixture and output root for generated artifacts under `test/mm3/abd-maps-models-specs/` (see [fixture inventory](library/principles-and-rules.md#fixture-inventory-mm3)).

**Phase tables — Actor column:** Each row names a **single** leading mode: **AI-led** (the agent carries the substantive work; humans review or accept per the phase file) or **Code-led** (scripts, validators, and emitters carry the repeatable steps). Do not read **Actor** as a list of separate roles; detail lives in **Script** and **Summary** and in `phases/<slug>.md`.

---

## Stage 1 — Context & evidence

### Your role

You establish a **defensible evidence base** before you name terms, author the shaped story map, or promote types. Stage 1 is **evidence layout**: **understand** the big Markdown and **encode chunking rules**, then **build** the chunk/index package the pipeline cites.

### What you must do

- **Phase 0.** **§1 — Convert** sources to canonical Markdown where needed (own scripts/tooling). **§2–§4 —** **AI-led** pass over **`manifest_sources`**: draft **`context_chunking_spec`** and disclose assumptions/gaps; **human** secondary review—see [context-chunking-approach](content/parts/phases/context-chunking-approach.md). This is **design**, not a pass/fail test. Skip a full re-run when the spec already matches current sources.
- **Phase 1.** **`context_chunking_spec`** is named by **`solution.conf` → `context_chunking_spec`** (workspace-relative; default `context_chunking_spec.yaml`). You **produce** `chunks/*.md` and `context_index.json` per [context-spec.md](library/context-spec.md), keep manifest provenance (**sha256**, generator), and run `scripts/scanners/context_index_contract.py` (same as `validate_context_contract.py`) when the index exists. The spec is **not** shipped by the skill—you own it for your workspace.

You do **not** introduce inheritance or `extends` edges here. You only **package and pin** evidence the later stages will cite by `chunk_id`.

### What you produce

- A **chunking spec** (AI draft + human-reviewed) aligned to how the sources are structured, when Phase 0 work is needed.
- A **Phase 1 context package** (`chunks/*.md` + `context_index.json` + manifest) that downstream work treats as **the** evidence layer, without ad hoc files or mystery sources.

### How you know you succeeded

Stage 1 is **done for handoff** to Stages 2–4 only when **all** of the following are true—there is no partial or alternate path:

1. `**context_index.json`** exists and `**validate_context_contract.py` exits zero** (the context contract defines validity; nothing else counts as “validated”).
2. **Chunk files** on disk match the index and the chunking spec—no orphan chunks, no missing files for referenced `chunk_id`s.
3. A **manifest** pins sources and generator provenance (for example **sha256**), per [context-spec.md](library/context-spec.md).
4. The **chunking spec** and built artifacts refer to the **same** source snapshot (no stale rules against new files).

Until (1)–(4) are true, you **do not** start Stage 2. After they are true, Stages 2 through 4 cite `chunk_id` from that Phase 1 context package only—**no** invented provenance.


| #   | Phase             | Actor     | Script                                                                                                                                                                                                                    | Ref                                                                                                  | Outputs (fixture)                                                             | Summary                                                                                                                                                                                                                                                                            |
| --- | ----------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0   | Context chunking approach | AI-led | —                                                                                              | [context-chunking-approach](content/parts/phases/context-chunking-approach.md)                                                     | **`solution.conf`** wired, **`context_chunking_spec`** (reviewed) | Agent reads **`manifest_sources`**, drafts **`context_chunking_spec`**, discloses assumptions/gaps; human configures workspace + reviews spec before Phase 1. Not a pass/fail assessment. Revisit when sources change.                       |
| 1   | Canonical Context | Code-led | Chunking YAML from **`solution.conf` → `context_chunking_spec`**; Phase 1 emit per [context-spec.md](library/context-spec.md) (e.g. `build_context.py` when implemented); `scripts/scanners/context_index_contract.py` | [canonical-context](content/parts/phases/canonical-context.md), `[context-spec.md](library/context-spec.md)` | `context/chunks/*.md` + `context/context_index.json` / **v1** context package | Deterministic emit + manifest + contract validation. Outcome: Phase 1 package cited by `chunk_id` downstream. |


---

## Stage 2 — Vocabulary & behavior

### Your role

You separate **language** and **observable behavior** from **domain types**. You ground terms and mechanisms in **context chunks** (indexed by `context_index.json`). You write a **shaped** story map (who does what to which state) **before** you lock a sparse type system. Evidence and stories must lead type choices, not the reverse.

### What you must do

- **Phase 2.** You will consume `**context_index.json`** and context chunks. You will emit **terms**, **mechanisms**, and a **candidate queue** (possible types with rationale, still not promoted). `**scripts/build_phase2_artifacts.py`** writes **empty** JSON scaffolds (`terms[]`, `mechanisms[]`, `candidates[]`) under `phase2/`; it does **not** read chunks or fill vocabulary. **Authors** (human or AI) edit those files and **must** cite `chunk_id` on substantive rows per [terms-mechanisms-contract.md](library/terms-mechanisms-contract.md).
- **Phase 3.** You will author `mm3_story_map.json` with trigger/response, anchor, `term_refs`, and `evidence_chunk_ids` where stories are substantive. You will run `scripts/scanners/phase3_story_map_evidence.py` (same as `validate_phase3_story_map.py`). Details live in [terms-mechanisms](content/parts/phases/terms-mechanisms.md) and [shaped-story-map](content/parts/phases/shaped-story-map.md).

You do **not** put types in `concepts[]` yet.

### What you produce

- Shared **vocabulary** and **mechanism** artifacts tied to the corpus.
- A **candidate queue** for types (still not promoted).
- A **story map JSON** that reads as **capabilities and anchors**, not a type checklist.

### How you know you succeeded

Your Phase 2 artifacts trace back to `chunk_id`s. Your story map reads as **interaction capability**, not a list aligned to a future type catalog. Substantive stories tie to evidence where it matters. **Promotion** to domain types waits for Stage 3.


| #   | Phase                             | Actor   | Script                                          | Ref                                            | Outputs (fixture)                                                                | Summary                                                                                                                                                                                                                                                                    |
| --- | --------------------------------- | ------- | ----------------------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2   | Terms & mechanisms (layers 1 & 2) | AI-led  | `scripts/build_phase2_artifacts.py`             | [terms-mechanisms](content/parts/phases/terms-mechanisms.md) | `phase2/mm3_terms_layer.json`, `mm3_mechanisms.json`, `mm3_candidate_queue.json` | `**build_phase2_artifacts.py`** emits **empty** schema shells; agent authors populate terms, mechanisms, and the candidate queue from context chunks with mandatory `chunk_id` citations per the contract. **Nothing** is promoted to `concepts[]` here. |
| 3   | Shaped story map                  | AI-led  | `scripts/scanners/phase3_story_map_evidence.py` | [shaped-story-map](content/parts/phases/shaped-story-map.md) | `phase3/mm3_story_map.json`                                                      | Agent authors shaped story map (trigger/response, anchors, evidence links); validator checks phase rules. Outcome: JSON map of capabilities and interactions, not a type catalog.                                            |


---

## Stage 3 — Domain modeling

### Your role

You add `concepts[]` only where stories and evidence justify **distinct** behavioral contracts. You avoid a large upfront ontology. You decide **variant shape** (enum versus subtypes versus other) **before** you spread properties across types. You deepen approved types with responsibilities, dependencies, and citations so the model is **arguable**.

### What you must do

- **Phase 4.** You will run the **promotion gate**: candidate to **concept** with per-type rationale and explicit rejections (for example, “just a property on X”).
- **Phase 5.** You will write **variant decisions** per family (format is yours to standardize).
- **Phase 6.** You will attach responsibilities, cross-type dependencies, and evidence to types in scope. Every substantive claim you add in AI-assisted passes **must** respect `chunk_id` discipline per the contract.

### What you produce

- A **small promoted set** with clear accept and reject rationale.
- **Per-family variant rules** before you churn structure.
- **Deepen** artifacts: responsibilities, `depends_on`, and evidence links for types in scope.

### How you know you succeeded

Your types are explainable at the depth you chose. Variant rules are stable before rework. Every promoted type has evidence. You use `extends` only where real substitution behavior requires it.


| #   | Phase                       | Actor   | Script | Ref                                                        | Outputs (fixture)                        | Summary                                                                                                                                                                                                                      |
| --- | --------------------------- | ------- | ------ | ---------------------------------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 4   | Domain types (`concepts[]`) | AI-led  | —      | [domain-types](content/parts/phases/domain-types.md)                     | Sparse types + rationale                 | Promote a minimal set of concepts from the candidate queue with per-type rationale and explicit rejections. Outcome: `concepts[]` only where behavior justifies a distinct contract, not a large upfront ontology. |
| 5   | Variant classification      | AI-led  | —      | [variant-classification](content/parts/phases/variant-classification.md) | Written variant decisions per family     | Decide how each variation family is represented before bulk property assignment. Outcome: written variant decisions per family so structure stays stable through deepen.                                      |
| 6   | Deepen                      | AI-led  | —      | [deepen](content/parts/phases/deepen.md)                                 | Responsibilities, evidence, `depends_on` | Attach responsibilities, cross-type dependencies, and evidence to types in scope, citing chunks where claims matter. Outcome: an arguable model traceable to the corpus.                           |


---

## Stage 4 — Integration & delivery

### Your role

You merge parallel work into **one coherent** map, model, and spec (or a deliberate split). You **drain** the candidate queue with explicit decisions. You **prove** quality with automation and visible outputs so reviewers get something **repeatable**, not a one-off edit.

### What you must do

- **Phase 7.** You will integrate synonyms, repoint references, and merge the story map with types and terms. You will **close** or **defer** remaining candidates with rationale.
- **Phase 8.** You will run **scanners** and schema checks, **render** reports, update `generate_context_bundle_manifest.py`, and run a critic pass against [principles and rules](library/principles-and-rules.md) when you add that step to your workflow. You will wire **CI** on the MM3 fixture for the scope you care about.

### What you produce

- An integrated **map-model-spec** narrative (or an intentional split).
- A **candidate queue** brought to explicit decisions.
- **Validation and reporting** output plus a bundle manifest that ties back to the principles doc.

### How you know you succeeded

Your checks and manifest reproduce for the chosen scope. Your **CI** passes where you wired it. You can **explain** deliverables using provenance, the shaped story map, sparse types, and explicit variants without hand-waving.


| #   | Phase             | Actor     | Script                                                   | Ref                                          | Outputs (fixture)                          | Summary                                                                                                                                                                                                                                                                                                                                           |
| --- | ----------------- | --------- | -------------------------------------------------------- | -------------------------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 7   | Integrate         | AI-led    | —                                                        | [integrate](content/parts/phases/integrate.md)             | Drained candidate queue → `map-model-spec` | Merge synonyms, align references, combine story map with types and terms; close or defer every remaining candidate with rationale. Outcome: one coherent map-model-spec narrative, or a documented deliberate split.                                                                                                          |
| 8   | Validate & render | Code-led  | scanners, reports, `scripts/generate_context_bundle_manifest.py`, `scripts/build.py` | [validate-render](content/parts/phases/validate-render.md) | CI checks, rendered reports, manifest      | `**build.py`** runs scanners, `**generate_context_bundle_manifest.py`**, and rule-example checks; wire CI in your host when you want automated runs. Outcome: reproducible validation and visible proof of quality for the scope you wire. |


**Bundle manifest (cross-phase):** `scripts/generate_context_bundle_manifest.py` records hashes for sources and phase outputs. `scripts/build.py` invokes it.

### What `build.py` does for you

`build.py` does **not** run a separate “pre-pipeline” ahead of Phase 0. It does **not** generate `chunks/` or `context_index.json`; that is the **Phase 1** pipeline per [context-spec.md](library/context-spec.md).

`**python scripts/build.py --merge-only`** runs step **1** only (AGENTS + built phase bundles). **Skips** `test/mm3` fixture scripts.

`**python scripts/build.py`** (full pipeline) runs **1** then **2–7** in order:

1. `**MapsContentAssembler`** — merges this file and `phases/*.md` into `**content/built/agents-staged.md`** and `**AGENTS.md**`; writes `**content/parts/phases/built/<slug>.md**` and `**content/built/phases/<slug>.md**`. Strips legacy solution-role markers from phase bodies in the merge. See [content/built/README.md](../built/README.md).
2. `**scripts/scanners/context_index_contract.py**` — validates `**context_index.json**` when present (same behavior as `validate_context_contract.py`).
3. `**scripts/build_phase2_artifacts.py**` — writes **empty** `phase2/mm3_terms_layer.json`, `mm3_mechanisms.json`, `mm3_candidate_queue.json` (schema shells only).
4. `**scripts/scanners/phase3_story_map_evidence.py`** — validates Phase 3 story map JSON (same entry as `validate_phase3_story_map.py`).
5. `**scripts/scanners/chunks_must_be_referenced.py`** — if `**map-model-spec.json**` exists at the path from `**_config.map_model_spec_path()**`, checks evidence fields cite chunks; if that file is **missing**, prints **skip** and exits **0**.
6. `**scripts/generate_context_bundle_manifest.py`** — records hashes for sources and phase outputs.
7. `**scripts/test_rule_examples.py`** — fails the build if any rule under `rules/` is missing `****DO****` / `****DON'T****`.

**Authors** produce `chunks/` and `context_index.json` outside this script (Phase 1). When those files exist, step **2** enforces [context-spec.md](library/context-spec.md).

---

## Documentation library (`content/parts/library/`)

Long-form contracts and narrative live under **`content/parts/library/`**. **`docs/README.md`** is an index that links into that folder (the `docs/` tree does not duplicate those files). Normative process lives in this file and in `phases/`. **Phase-specific narrative** (how to execute that phase end-to-end) belongs in **`phases/<slug>.md`**—e.g. **Phase 0** (AI-led spec + human review) in [`context-chunking-approach.md`](content/parts/phases/context-chunking-approach.md); **Phase 1** build, coherence, and validation in [`canonical-context.md`](content/parts/phases/canonical-context.md). **Shared** contracts (referenced by several phases or by validators) stay in the table below. Cross-cutting docs state rules and order without copying every phase. When you change a stage or phase, you update this file and the phase files, and you align [`principles-and-rules.md`](library/principles-and-rules.md) and [`execution-and-success.md`](library/execution-and-success.md).


| Document                                                             | Role                                                                                                      |
| -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| [principles-and-rules.md](library/principles-and-rules.md)           | Principles table, cross-cutting rules, fixture inventory                                                  |
| [execution-and-success.md](library/execution-and-success.md)         | Execution order (what to do next) + reusable success definition                                           |
| [context-spec.md](library/context-spec.md)                     | **Contract:** `chunks/`, `context_index.json`, manifest, chunking spec shapes (process: phase files + `phases/canonical-context.md`) |
| [terms-mechanisms-contract.md](library/terms-mechanisms-contract.md) | Phase 2 artifacts + automation                                                                            |
| [shaped-story-map.md](library/shaped-story-map.md)                   | Phase 3 JSON, validation, rationale                                                                       |
| [pipeline_invariants.md](library/pipeline_invariants.md)             | Cross-cutting gates; layers 1–4; Phases 4–8 artifact summary                                              |
| [domain-model.md](library/domain-model.md)                           | Modules, concepts, `map-model-spec` scaffold                                                              |
| [story-map.md](library/story-map.md)                                 | Full interaction-tree story map (prose)                                                                   |
| [README.md](library/README.md)                                       | Index of this library                                                                                     |


---

## Context chunking approach (Phase 0)

**Normative procedure for Phase 0:** **this document**. It covers **(1)** getting **canonical Markdown** for every evidence source, **(2)** workspace wiring, and **(3)** how **`context_chunking_spec`** is produced so splits and labels match real structure. You cannot honestly inventory headings, tables, lists, or export noise until the manuscript exists as Markdown the pipeline can read.

**Phase 1 procedure** (produce **`chunks/`** + **`context_index.json`**, coherence, contract validation) is **[canonical-context.md](content/parts/phases/canonical-context.md)**—a separate process file. **Artifact shapes and validation rules** are **[context-spec.md](content/parts/library/context-spec.md)**.

**You will** read every **`manifest_sources`** file **after** §1 conversion, perform the structural inventory in **§3**, **draft** the YAML (**`section_boundaries`**, **`splitting`**, **`defaults`**, **`taxonomy`**, …) per [context-spec.md](content/parts/library/context-spec.md) § Chunking spec, and **disclose** what **you** did—assumptions, uncertainties, and anything **you** could not infer from structure alone.

**You will not skip this:** After **your** draft, you will present results to the user to spot‑check against the real Markdown, correct wrong patterns, tighten taxonomy, and **accept** the spec before Phase 1 runs.

**If the spec already fits the sources,** **you will** **not** re-run a full inventory—only revisit when layout or **`manifest_sources`** change materially.

[`process.md`](content/parts/process.md) is the pipeline **summary** (table row), not the full procedure.

---

## 1. Convert to canonical Markdown (step one)

**Role:** Human + tooling (and optionally an AI-assisted pass for cleanup). **Phase 0 owns this:** any importers, converters, or one-off scripts (for example PDF, DOCX, PPTX → Markdown) live in **your** workspace or toolchain—not as an unnamed prerequisite of Phase 1.

**You will:**

1. Produce **canonical Markdown** for each source that is not already Markdown (fix encoding, strip or tag conversion artifacts you already know about, and land paths you can list in **`manifest_sources`**).
2. Keep conversion **repeatable** where it matters: document the command, script, or skill (e.g. a content-to-memory / document-ingest pipeline) so a refresh of the source file does not silently change chunk boundaries.
3. Only after those **`.md`** files exist and are stable enough to open, run the **structural inventory** in **§3** and draft **`context_chunking_spec`** (landed per **§4**).

Phase 1 emitters assume **`manifest_sources[]`** points at **Markdown** on disk. They do **not** substitute for Phase 0 conversion.

---

## 2. Configure the workspace and which files you cover

**Configure (human):** Land **`solution.conf`** in the active skill workspace: **`manifest_sources`**, **`context_path`** / output conventions, and the **`context_chunking_spec`** pointer (default `context_chunking_spec.yaml` beside `solution.conf`). The chunking YAML **contents** follow **§3–§4** and are reviewed before Phase 1. Phase 1 emitters **read** this same wiring via **`scripts/_config.py`**—[canonical-context.md](content/parts/phases/canonical-context.md) assumes it already exists.

**You will** cover **every** file that matters for evidence.

**You will** use **`solution.conf` → `manifest_sources[]`** in the **active skill workspace** (the folder that contains `solution.conf`; the skill selects it via `conf/abd-config.json` → `active_skill_workspace`).

- Each entry has a **`path`** (Markdown file, **relative to the workspace root**) and a **`role`** (source anchor for provenance).
- **You will** ingest **full contents** of those paths—**your** rules **must** speak to **this** export, not a generic handbook. **Human (solution analyst)** **will** confirm nothing important was skipped or misread.

The list of **`path`** values is the corpus **your** **`context_chunking_spec`** **must** cover. When the workspace **runs** Phase 1, path resolution for **`solution.conf`**, chunking YAML, **`context_path`**, and outputs follows **`scripts/_config.py`** (same **skill workspace** as above).

---

## 3. Structural scan (inventory you will encode)

**You will** model the manuscript’s real shape before YAML is finalized. **You are going to** deliver **(a)** a short **structural report** (what **you** observed, risks, open questions) and **(b)** the **draft `context_chunking_spec`**. This is not a pass/fail score. If **your** inventory is shallow, Phase 1 code will split mid-table or treat boilerplate as rules—and Phase 1 coherence **still needs the source** to catch drift; neither pass can fix a wrong **split policy** without updating the spec or the emitter.

### 3.1 Outline and navigation

**You will** examine and record:

- **Heading ladder** — Which `#` … `######` levels mean part, chapter, section, subsection? Are levels consistent?
- **Numbering** — Do `1.`, `1.2.3`, or appendix letters align with headings, or do lists float without a heading boundary?
- **Navigation chrome** — ToCs, “in this section,” breadcrumbs: **content** to chunk, or **noise** to exclude or tag per [context-spec.md](content/parts/library/context-spec.md)?

### 3.2 Dense and atomic regions

**You will** apply these constraints when **you** encode rules:

- **Tables** — Never split **through** a row; split above/below the table block.
- **Lists and definition lists** — A rule plus its bullets is often **one** unit.
- **Stat blocks, callouts, boxed examples** — Note delimiters. Repeated shapes → **pattern rules** in YAML, not one-off IDs.
- **Code fences** — Often stay with the prose that introduces them.

### 3.3 Noise vs signal

**You will** classify:

- **Export junk** — Running headers, page numbers, license blobs, conversion artifacts.
- **Policy** — Exclude (and use **`excluded[]`** where the contract allows), or **include and tag** (`metadata_noise`, `noise`, `structural_only`). Field meanings: [context-spec.md](content/parts/library/context-spec.md).

### 3.4 Repeated templates

**You will** encode the **pattern** in **`section_boundaries`** / splitting rules and set **`defaults`** + **`taxonomy`** for that pattern.

### 3.5 Capture sheet (you fill; human verifies)

| You will determine… | So the spec can encode… |
| ------------------- | ----------------------- |
| What **starts** a new major unit? | `chapter_break_regex` / `section_break_regex` ([context-spec.md](content/parts/library/context-spec.md) § Chunking spec). |
| What must **never** be split inside? | **`splitting`** (e.g. keep tables intact). |
| When tiny bits **merge**? | **`min_chunk_chars`**, merge rules. |
| What is **out of scope** for modeling? | **`modeling_kind`** defaults, exclusions. |
| Which **taxonomy** values apply? | Closed-world enums aligned with [context-spec.md](content/parts/library/context-spec.md). |

---

## 4. Produce and land `context_chunking_spec`

1. **You will** write the YAML at **`solution.conf` → `context_chunking_spec`** (default basename `context_chunking_spec.yaml` beside `solution.conf`). **Fields and examples:** [context-spec.md](content/parts/library/context-spec.md) § Chunking spec. **Minimum areas:** **`section_boundaries`**, **`splitting`**, **`defaults`**, **`taxonomy`**.

2. **You will** disclose in the same turn or an accompanying note: **sources read**, **assumptions**, **low-confidence rules**, and **gaps** (e.g. “could not infer appendix boundary pattern”). **Human (solution analyst)** **will** use this during review.

3. **Human (solution analyst):** **You will** run a secondary pass on the manuscript vs draft YAML: fix wrong headings/tables/noise calls, tighten taxonomy, and ensure the spec is **valid** per [context-spec.md](content/parts/library/context-spec.md). The landed file is **owned** by the workspace; the AI draft is not sufficient without this review.

---

## 5. If `chunks/` and an index already exist

**You will** feed learning back into the spec when asked—often **you** run another full Phase 0 pass (structural report + draft YAML) and **Human (solution analyst)** **will** review again: coverage, misfiring defaults, new section shapes. That is **spec maintenance** for Phase 0—not Phase 1’s validator.

---

## See also

- **[canonical-context.md](content/parts/phases/canonical-context.md)** — Phase 1: emit package, coherence, validate.
- **[context-spec.md](content/parts/library/context-spec.md)** — Normative chunk/index/manifest shapes and checklist.


---

## Canonical context (Phase 1) — build and validate the package

**Goal:** A **single, versioned** context package—`**chunks/*.md`**, `**context_index.json`**, manifest provenance—so later phases cite stable `**chunk_id**` values. This is **not** vocabulary, story maps, or domain types.

**Prerequisite:** [Phase 0 — Context chunking approach](content/parts/phases/context-chunking-approach.md) yields a `**context_chunking_spec`** aligned with current `**manifest_sources`**. **Normative procedure for Phase 1:** **this document**. **Artifact shapes and checklist:** [context-spec.md](content/parts/library/context-spec.md). `[process.md](content/parts/process.md)` is pipeline **summary** only.

---

## 1. What Phase 1 is for

You turn **canonical Markdown** (declared sources) into a **validated** context package:

- Later work can cite `**chunk_id`** rows that exist on disk and in the index.
- **No** invented files, **no** mystery sources—paths and hashes live in `**solution.conf`** and the index `**manifest`**.

**Skill workspace:** The folder that contains `**solution.conf`**, selected by `**conf/abd-config.json` → `active_skill_workspace`** (paths inside `**solution.conf**` are relative to that folder—same rules as `**scripts/_config.py**`).

Downstream **consumes** this package; it does not replace it.

---

## 2. Pipeline shape and context build

**Producing** the package: canonical Markdown (from `**solution.conf` → `manifest_sources[]`**, resolved by `**scripts/_config.py`**) → chunking per `**context_chunking_spec**` → `**chunks/**` + `**context_index.json**` → **coherence** → **contract** validation. Example paths like `docs/HeroesHandbook.md` are **fixtures**; **your** workspace lists **your** files.

**Why code then AI/human (two stages):** The intent—**deterministic cut first**, then **sense-check against the original Markdown**—is spelled out in [context-chunking-approach.md](content/parts/phases/context-chunking-approach.md). **This section** is **procedure** only.

**Prerequisite (Phase 0):** Canonical Markdown for every source (**[context-chunking-approach.md](content/parts/phases/context-chunking-approach.md) §1**), **`solution.conf`** (workspace wiring: **`manifest_sources`**, paths), and the reviewed **`context_chunking_spec`** (chunking YAML) are **Phase 0** deliverables. Phase 1 **consumes** them; it does **not** run PDF/DOCX conversion or replace that work. The table below starts after Phase 0—**emit**, **coherence**, **validate** only.


| Step          | Role            | What happens                                                                                                                                                                 |
| ------------- | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Build**     | Code            | Read `**manifest_sources`** + `**context_chunking_spec`** → write `**chunks/*.md**` + `**context_index.json**` (how you run that step is up to your workspace; see **§2.1**) |
| **Coherence** | LLM or human    | Align schema-allowed fields with chunk text and index (**§2.1**)                                                                                                             |
| **Validate**  | Code            | Contract scanner (**§7.4**) enforces [context-spec.md](content/parts/library/context-spec.md)                                                                                           |


Substantive vs noise, default labels, and **taxonomy** are declared in `**context_chunking_spec`** during [Phase 0](content/parts/phases/context-chunking-approach.md). Phase 1 **applies** that YAML; it does not invent structure you never scanned for.

### 2.1 Automation: emit package, coherence, validate

**Contract** (what “valid” means): `**context_index_contract.py`** / `**validate_context_contract.py`** per [context-spec.md](content/parts/library/context-spec.md). That is **not** Pass 1—it runs **after** `**chunks/`** and `**context_index.json`** exist.

**Emit (Pass 1):** Deterministic code reads `**manifest_sources`** + `**context_chunking_spec`** and writes `**chunks/*.md**` + `**context_index.json**`. This skill’s repo **does not ship** that emitter yet; you may use your own script, a one-off, or external tooling—as long as outputs match [context-spec.md](content/parts/library/context-spec.md). A dedicated module under `**scripts/`** may appear later; there is **no** fixed filename today.

**Typical emit flow** (one script or several—your choice):

1. Load Markdown from `**manifest_sources[]`** (`path` + `role`); use `**source_path`** when the workspace names a docs directory for discovery. Load chunking rules from `**context_chunking_spec**` (default `context_chunking_spec.yaml`).
2. Write chunk files and `**context_index.json**` per [context-spec.md](content/parts/library/context-spec.md)—deterministic **code-first** generation.

**Coherence (Pass 2):** LLM or human uses `**manifest_sources`** Markdown as **ground truth**—check that **splits and labels** fit the manuscript; then, within **schema-allowed fields only**, align front matter, index rows (`evidence_type`, `modeling_kind`, `preview`, …), and chunk bodies so they **do not contradict** each other or the source. Re-run `**validate_context_contract.py`** after edits. No free-text “evidence” without `**chunk_id**`.

`**scripts/build.py**` (full workspace run, not `--merge-only`): runs `**validate_context_contract.py**` / `**context_index_contract.py**` when an index exists. It does **not** emit chunks—emit is **outside** this script until an emitter is added here.

**Generation (code-first, then coherence)**

- **Pass 1 — deterministic Python** applies **only** rules from the chunking spec, assigns `**chunk_id`** deterministically, writes chunks + index.
- **Pass 2 — coherence:** LLM or **human** checks those artifacts **against the original Markdown** (strategy sense-check), then refines **allowed** fields so labels and previews **match** chunk text and the **source**. **Promotion** to terms/types is **not** Phase 1. Final output **must** pass `**validate_context_contract.py**` / `**context_index_contract.py**`.

### 2.2 Which script does what (and run order)

**Python** checks **shape** or prints **stats**; it does not re-read the **whole source** for “does this chunking strategy make sense?” **Coherence** (**§2.1**) does that (LLM or human), using **original Markdown** plus chunk/index output.


| Kind                                                                 | What it is                                                                                                                    | What it does **not** do                                          |
| -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `**context_index_contract.py`** / `**validate_context_contract.py`** | Contract validation per [context-spec.md](content/parts/library/context-spec.md)                                                         | Not an LLM; not coherence; not “strategy vs source” review       |
| **Coherence (**§2.1**)**                                             | Second pass: LLM or human uses **source Markdown** + artifacts to validate chunking **sense**, then aligns **allowed** fields | Not the contract scanner; does not replace fixing a bad **spec** |


**Run order** (workspace `**scripts/build.py`**, not `--merge-only`): `**validate_context_contract.py**` / `**context_index_contract.py**` when `**context_index.json**` exists (after your Phase 1 emitter runs). **Emit** Pass 1 is **separate**—run your emitter **before** the contract scanner can pass.

`**python scripts/build.py --merge-only`** (this **skill repo** only) rebuilds composed docs (`AGENTS.md`, `content/built/`, embedded bundles). It does **not** run workspace audits or contract scanners—use when **editing skill markdown**, not when **building a context package**.

**Injectable paths:** `**rules/scanners.json`**.

---

## 3. What a healthy package provides

1. **Stable IDs** — `chunk_id` / `block_id` aligned with files and index.
2. **Evidence typing** — `evidence_type` and related fields usable for sampling and promotion gates—see **§5** and [context-spec.md](content/parts/library/context-spec.md).
3. **Coverage** — Domain-relevant material represented; exclusions **explicit** where allowed (`excluded[]`, …).
4. **Versioning** — Manifest pins sources and generator provenance.

---

## 4. Chunking spec (from Phase 0, used here)

`**context_chunking_spec`** is **produced** during [Phase 0](content/parts/phases/context-chunking-approach.md) (**Markdown conversion §1**, **configure §2**, **AI-led draft + human review §3–§4**). **Normative** fields: [context-spec.md](content/parts/library/context-spec.md) § Chunking spec. Phase 1 **points** `**solution.conf` → `context_chunking_spec`** at that file and **uses** it when emitting chunks and the index.

---

## 5. Evidence types, `modeling_kind`, and promotion

Chunk front matter and index rows carry `**evidence_type`** (form in the source) and `**modeling_kind`** (stance for modeling). Enums come from chunking spec `**taxonomy**`—[context-spec.md](content/parts/library/context-spec.md) § Chunking spec and § Chunk files.

**Promotion vs evidence:** Phase 1 **packages** evidence only. Turning a citation into a **term**, **mechanism**, **story**, **property**, or `**concepts[]` row** is **not** automatic. See [principles-and-rules.md](content/parts/library/principles-and-rules.md), [pipeline_invariants.md](content/parts/library/pipeline_invariants.md), and later-phase contracts. `**example`** / `**metadata/noise`** do not silently become types or edges here.

---

## 6. Illustrative chunk and index

```yaml
---
chunk_id: blk_00042
source: HeroesHandbook
evidence_type: domain-rule
section_path: ["Chapter 3", "Abilities", "Ability Ranks"]
---
The actual chunk content in markdown.
```

**Index:** metadata + refs; full text in chunk files. **Lookup:** index → `chunk_id`s → `chunks/{chunk_id}.md`. Full schema: [context-spec.md](content/parts/library/context-spec.md).

---

## 7. What you do (ordered work)

### 7.1 Wire the chunking spec

Ensure `**context_chunking_spec`** reflects current sources ([Phase 0](content/parts/phases/context-chunking-approach.md)). Set `**context_chunking_spec`** in `**solution.conf**`. Schema: [context-spec.md](content/parts/library/context-spec.md).

### 7.2 Produce `chunks/*.md` and `context_index.json`

- **Emit** per **§2.1**: any deterministic process you use is fine **if** outputs satisfy [context-spec.md](content/parts/library/context-spec.md).

Outputs: `<workspace>/<context_path>/chunks/*.md` and `context_index.json`.

### 7.3 Pin provenance

Index `**manifest`**: sha256 (and generator id where applicable) for `**manifest_sources`**, per [context-spec.md](content/parts/library/context-spec.md).

### 7.4 Validate

When `**context_index.json**` exists, run `**scripts/scanners/context_index_contract.py**` (same as `**validate_context_contract.py**`) — **hard gate**: bidirectional chunk ↔ index, required front matter, duplicate IDs, line bounds. Fix all violations before handoff.

### 7.5 Do **not**

- Do **not** add `**concepts[]`**, story-map JSON, or terms/mechanisms here.
- Do **not** introduce `**extends` / inheritance** edges as a shortcut.
- You **only** package evidence cited by `**chunk_id`**.

---

## 8. How you know Phase 1 is complete

Before Stages 2–4 cite `**chunk_id`**:

1. `**context_index.json**` exists and `**validate_context_contract.py**` / `**context_index_contract.py**` exits **0** ([context-spec.md](content/parts/library/context-spec.md)).
2. **Chunk files** match the index—no orphans, no missing files.
3. **Manifest** pins sources and provenance (**sha256**, etc.).
4. **Chunking spec** and **manifest** match the **same** source snapshot you split.

---

## 9. Artifacts (summary)


| Artifact                   | Role                                                                               |
| -------------------------- | ---------------------------------------------------------------------------------- |
| Chunking YAML              | `**solution.conf` → `context_chunking_spec`**                                      |
| `**chunks/{chunk_id}.md`** | One chunk per file; front matter per [context-spec.md](content/parts/library/context-spec.md) |
| `**context_index.json**`   | `**manifest**` + `**blocks[]**` (+ optional `**excluded[]**`)                      |
| Contract scanner           | [context-spec.md](content/parts/library/context-spec.md); paths in `**rules/scanners.json**`  |


---

## 10. Adoption and migration

Migrate or extend schema in place, fill `**modeling_kind**` where required, **pin** v1 in the manifest. Revisit [Phase 0](content/parts/phases/context-chunking-approach.md) if sources change.

---

## 11. Where to read more


| Topic                                          | Document                                                                                   |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **Phase 0** — AI-led spec draft + human review | [context-chunking-approach.md](content/parts/phases/context-chunking-approach.md)                               |
| **Schema / contract**                          | [context-spec.md](content/parts/library/context-spec.md)                                              |
| **Principles, gates, pipeline summary**        | [principles-and-rules.md](content/parts/library/principles-and-rules.md), [process.md](content/parts/process.md) |


---

## Terms & mechanisms (layers A & B)



**Goal:** Glossary and **named processes** exist **before** sparse `concepts[]`.



**Normative for Phase 2:** this document. [`process.md`](content/parts/process.md) is pipeline **summary** only (table row)—not the procedure.



## Actor



**Code** runs `scripts/build_phase2_artifacts.py`, which writes **empty** `terms[]`, `mechanisms[]`, and `candidates[]` JSON files (schema shells only). **Human / AI** author all substantive content and cite evidence per the contract.



## What this phase produces



- **Terms** — surface vocabulary + chunk links; not classes.

- **Mechanisms** — workflows/lifecycles with steps + evidence.

- **Candidate queue** — “possible type” with rationale; **not** in `concepts[]` yet.



## Exit



Promotion rule written: **candidate → concept** only through the **domain-types** gate (Phase 4)—not by renaming a mention or string co-occurrence.



**Outputs:** `test/mm3/abd-maps-models-specs/phase2/mm3_terms_layer.json`, `mm3_mechanisms.json`, `mm3_candidate_queue.json`.



**Implementation notes:** [`terms-mechanisms-contract.md`](content/parts/library/terms-mechanisms-contract.md) (includes **inputs** and **`chunk_id` citation** rules for Phase 2).


---

## Shaped story map



**Goal:** Epics/stories that satisfy **actor → behavior → anchor** (domain state **read** and/or **write**); alignment allows **term** references without minting types.



**Normative for Phase 3:** this document. [`process.md`](content/parts/process.md) is pipeline **summary** only (table row)—not the procedure.



## Actor



**Code** runs `scripts/scanners/phase3_story_map_evidence.py` (wrapper: `validate_phase3_story_map.py`). **Human / AI** maintain `mm3_story_map.json`.



## Requirements



- Every story has a **clear** behavioral reading and **traceability** to concepts.

- No story exists solely to **match strings** in the type list.

- Every story states its **anchor** (read path, write path, or both)—not every story requires **mutation** of the core write model.

- **Query/read/forward** stories are as valid as **mutating** stories when the anchor is explicit.

- Substantive stories carry **`evidence_chunk_ids[]`** referencing **`context_index.json`** / `chunks/` ([`shaped-story-map.md`](content/parts/library/shaped-story-map.md)); `phase3_story_map_evidence.py` extends to enforce this when authored.



## Exit



Story map validated; **domain types** (`concepts[]`) follow after the shaped story map is sound.



**Output:** `test/mm3/abd-maps-models-specs/phase3/mm3_story_map.json` (when present).



**Docs:** [`shaped-story-map.md`](content/parts/library/shaped-story-map.md) (Phase 3 JSON shape + validators), [`story-map.md`](content/parts/library/story-map.md) (interaction tree prose + [why story mapping before domain types](content/parts/library/story-map.md#why-story-mapping-before-domain-types)).


---

## Domain types (`concepts[]`)



**Goal:** **Sparse** types; **reject gate** (“not just a property on a broader type”).



**Normative for Phase 4:** this document. [`process.md`](content/parts/process.md) is pipeline **summary** only (table row)—not the procedure.



## Steps



1. Promote candidates through **explicit** domain-types gate only (no string co-occurrence shortcuts).

2. Record **per-type rationale**; keep type count tractable for the fixture depth.

3. Align prose and JSON with [`domain-model.md`](content/parts/library/domain-model.md) (modules, properties, **`Base:Extension`** in `concepts[].name` for inheritance — no separate `extends` field — examples).



## Exit



Type count and rationale remain reviewable for the MM3 fixture at the chosen depth.


---

## Variant classification



**Goal:** Per family: **enum vs `extends`** **before** property churn.



**Normative for Phase 5:** this document. [`process.md`](content/parts/process.md) is pipeline **summary** only (table row)—not the procedure.



## Steps



1. For each variant family, record the **decision**: enum vs subtypes vs other **before** bulk property assignment.

2. Align with **Explicit variant representation** in [`principles-and-rules.md`](content/parts/library/principles-and-rules.md) / plan principles table.



## Exit



Written **variant decision** per family before bulk modeling.


---

## Deepen



**Goal:** Responsibilities and evidence on **approved** types only; **topological** `depends_on`.



**Normative for Phase 6:** this document. [`process.md`](content/parts/process.md) is pipeline **summary** only (table row)—not the procedure.



## Steps



1. Attach evidence citations to approved types; citations **support** claims—they do not **auto-create** types.

2. Model `depends_on` where appropriate (acyclic, reviewable).



## Exit



Every type has **evidence** citations; relationships follow explicit gates from the principles table.


---

## Integrate



**Goal:** Synonyms, repointing, **drain candidate queue** into final `map-model-spec` (or split artifacts if story map stays separate).



**Normative for Phase 7:** this document. [`process.md`](content/parts/process.md) is pipeline **summary** only (table row)—not the procedure.



## Steps



1. Reconcile synonyms and duplicate references.

2. Move approved candidates from the queue into `concepts[]` / final spec per promotion rules.

3. Keep **domain narrative** and **story map** aligned when both artifacts exist.



## Exit



Single coherent map-model-spec (or documented split) ready for validation.


---

## Validate & render



**Goal:** Automated checks (scanners, schema) + **rendered** reports; CI on MM3; optional **critic** checklist against the **principles table** in [`principles-and-rules.md`](content/parts/library/principles-and-rules.md).



**Normative for Phase 8:** this document. [`process.md`](content/parts/process.md) is pipeline **summary** only (table row)—not the procedure.



## Actor



**Code** — `skill-config` scanners, `scripts/generate_context_bundle_manifest.py` (invoked from `scripts/build.py`). **Human / AI** — review reports.



## Steps



1. Run structural / schema scanners defined for the skill.

2. Render reports as configured (paths under fixture output root).

3. Optional: critique pass against [`principles-and-rules.md`](content/parts/library/principles-and-rules.md) (external expert or checklist).



## Exit



Reproducible validation + manifest; CI green for the MM3 fixture at the chosen scope.
