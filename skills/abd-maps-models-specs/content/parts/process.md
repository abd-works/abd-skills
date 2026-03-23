# Process — abd-maps-models-specs

**Pipeline (navigation spine):** Context chunking approach → Canonical context → Terms & mechanisms → Story map → Domain types → Variants → Deepen → Integrate → Validate & render

---

## How to use this document

**Normative procedure** for each phase lives in **`content/parts/phases/<phase>.md`**. **This file** is a **summary only**: pipeline spine, staged goals, and a **one-row sketch** per phase in the tables—**not** a substitute for the phase document. Open `[phases/](phases/)` for authoritative steps, exit criteria, and artifacts. If you are reading `AGENTS.md`, the build merges this process section with the full text of every phase file below it.

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

- **Phase 0.** **§1 — Convert** sources to canonical Markdown where needed (own scripts/tooling). **§2–§4 —** **AI-led** pass over **`manifest_sources`**: draft **`context_chunking_spec`** and disclose assumptions/gaps; **human** secondary review—see [context-chunking-approach](phases/context-chunking-approach.md). This is **design**, not a pass/fail test. Skip a full re-run when the spec already matches current sources.
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
| 0   | Context chunking approach | AI-led | —                                                                                              | [context-chunking-approach](phases/context-chunking-approach.md)                                                     | **`solution.conf`** wired, **`context_chunking_spec`** (reviewed) | Agent reads **`manifest_sources`**, drafts **`context_chunking_spec`**, discloses assumptions/gaps; human configures workspace + reviews spec before Phase 1. Not a pass/fail assessment. Revisit when sources change.                       |
| 1   | Canonical Context | Code-led | Chunking YAML from **`solution.conf` → `context_chunking_spec`**; Phase 1 emit per [context-spec.md](library/context-spec.md) (e.g. `build_context.py` when implemented); `scripts/scanners/context_index_contract.py` | [canonical-context](phases/canonical-context.md), `[context-spec.md](library/context-spec.md)` | `context/chunks/*.md` + `context/context_index.json` / **v1** context package | Deterministic emit + manifest + contract validation. Outcome: Phase 1 package cited by `chunk_id` downstream. |


---

## Stage 2 — Vocabulary & behavior

### Your role

You separate **language** and **observable behavior** from **domain types**. You ground terms and mechanisms in **context chunks** (indexed by `context_index.json`). You write a **shaped** story map (who does what to which state) **before** you lock a sparse type system. Evidence and stories must lead type choices, not the reverse.

### What you must do

- **Phase 2.** You will consume `**context_index.json`** and context chunks. You will emit **terms**, **mechanisms**, and a **candidate queue** (possible types with rationale, still not promoted). `**scripts/build_phase2_artifacts.py`** writes **empty** JSON scaffolds (`terms[]`, `mechanisms[]`, `candidates[]`) under `phase2/`; it does **not** read chunks or fill vocabulary. **Authors** (human or AI) edit those files and **must** cite `chunk_id` on substantive rows per [terms-mechanisms-contract.md](library/terms-mechanisms-contract.md).
- **Phase 3.** You will author `mm3_story_map.json` with trigger/response, anchor, `term_refs`, and `evidence_chunk_ids` where stories are substantive. You will run `scripts/scanners/phase3_story_map_evidence.py` (same as `validate_phase3_story_map.py`). Details live in [terms-mechanisms](phases/terms-mechanisms.md) and [shaped-story-map](phases/shaped-story-map.md).

You do **not** put types in `concepts[]` yet.

### What you produce

- Shared **vocabulary** and **mechanism** artifacts tied to the corpus.
- A **candidate queue** for types (still not promoted).
- A **story map JSON** that reads as **capabilities and anchors**, not a type checklist.

### How you know you succeeded

Your Phase 2 artifacts trace back to `chunk_id`s. Your story map reads as **interaction capability**, not a list aligned to a future type catalog. Substantive stories tie to evidence where it matters. **Promotion** to domain types waits for Stage 3.


| #   | Phase                             | Actor   | Script                                          | Ref                                            | Outputs (fixture)                                                                | Summary                                                                                                                                                                                                                                                                    |
| --- | --------------------------------- | ------- | ----------------------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2   | Terms & mechanisms (layers 1 & 2) | AI-led  | `scripts/build_phase2_artifacts.py`             | [terms-mechanisms](phases/terms-mechanisms.md) | `phase2/mm3_terms_layer.json`, `mm3_mechanisms.json`, `mm3_candidate_queue.json` | `**build_phase2_artifacts.py`** emits **empty** schema shells; agent authors populate terms, mechanisms, and the candidate queue from context chunks with mandatory `chunk_id` citations per the contract. **Nothing** is promoted to `concepts[]` here. |
| 3   | Shaped story map                  | AI-led  | `scripts/scanners/phase3_story_map_evidence.py` | [shaped-story-map](phases/shaped-story-map.md) | `phase3/mm3_story_map.json`                                                      | Agent authors shaped story map (trigger/response, anchors, evidence links); validator checks phase rules. Outcome: JSON map of capabilities and interactions, not a type catalog.                                            |


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
| 4   | Domain types (`concepts[]`) | AI-led  | —      | [domain-types](phases/domain-types.md)                     | Sparse types + rationale                 | Promote a minimal set of concepts from the candidate queue with per-type rationale and explicit rejections. Outcome: `concepts[]` only where behavior justifies a distinct contract, not a large upfront ontology. |
| 5   | Variant classification      | AI-led  | —      | [variant-classification](phases/variant-classification.md) | Written variant decisions per family     | Decide how each variation family is represented before bulk property assignment. Outcome: written variant decisions per family so structure stays stable through deepen.                                      |
| 6   | Deepen                      | AI-led  | —      | [deepen](phases/deepen.md)                                 | Responsibilities, evidence, `depends_on` | Attach responsibilities, cross-type dependencies, and evidence to types in scope, citing chunks where claims matter. Outcome: an arguable model traceable to the corpus.                           |


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
| 7   | Integrate         | AI-led    | —                                                        | [integrate](phases/integrate.md)             | Drained candidate queue → `map-model-spec` | Merge synonyms, align references, combine story map with types and terms; close or defer every remaining candidate with rationale. Outcome: one coherent map-model-spec narrative, or a documented deliberate split.                                                                                                          |
| 8   | Validate & render | Code-led  | scanners, reports, `scripts/generate_context_bundle_manifest.py`, `scripts/build.py` | [validate-render](phases/validate-render.md) | CI checks, rendered reports, manifest      | `**build.py`** runs scanners, `**generate_context_bundle_manifest.py`**, and rule-example checks; wire CI in your host when you want automated runs. Outcome: reproducible validation and visible proof of quality for the scope you wire. |


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

Long-form contracts and narrative live under **`content/parts/library/`**. **`docs/README.md`** is an index that links into that folder (the `docs/` tree does not duplicate those files). Normative process lives in this file and in `phases/`. **Phase-specific narrative** (how to execute that phase end-to-end) belongs in **`phases/<slug>.md`**—e.g. **Phase 0** (AI-led spec + human review) in [`context-chunking-approach.md`](phases/context-chunking-approach.md); **Phase 1** build, coherence, and validation in [`canonical-context.md`](phases/canonical-context.md). **Shared** contracts (referenced by several phases or by validators) stay in the table below. Cross-cutting docs state rules and order without copying every phase. When you change a stage or phase, you update this file and the phase files, and you align [`principles-and-rules.md`](library/principles-and-rules.md) and [`execution-and-success.md`](library/execution-and-success.md).


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


