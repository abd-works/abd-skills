# Process — abd-maps-models-specs

**Pipeline (navigation spine):** Set workspace → Context markdown → Context chunking approach → Canonical context → Terms & mechanisms → Story map → Domain types → Variants → Deepen → Integrate → Validate & render

### Generate prompt — required before every phase (0–10)

From the **skill package root** (the directory that contains `scripts/` and `conf/`):

1. **Before** doing work for **any** phase in the tables below, run **`python scripts/generate_prompt.py --phase <slug>`** and treat **stdout** as the binding procedure (role, phase body, library slices, inlined **rules**, and the **exact** commands for code-led steps). **AI-led** and **code-led** alike: the emitted bundle is normative; do not skip it in favor of only skimming this file.
2. **`<slug>`** is the `skill-config.json` → `phase_files` name: `set-workspace`, `context-markdown`, `context-chunking-approach`, `canonical-context`, `terms-mechanisms`, `shaped-story-map`, `domain-types`, `variant-classification`, `deepen`, `integrate`, `validate-render`.
3. **Static vs dynamic assembly** is configured in **`skill-config.json`**, not on the CLI: **`generate_prompt.assembly_mode`** is **`static`** (default for this skill) or **`dynamic`**. If that key is omitted, **`delivery.mode`** applies: **`static_built`** → prefer **`content/built/phases/<slug>.md`** when present; **`runtime_injection`** → always assemble from sources. If a built file is missing under static, the tool still assembles from sources (same as before).
4. If you expect a **pre-merged** bundle and **`content/built/phases/<slug>.md`** is missing, run **`python scripts/build.py --merge-only`** from the skill root, then run **`generate_prompt`** again.

Script path: `python` [`scripts/generate_prompt.py`](../../scripts/generate_prompt.py).

---

## Stage 1 — Context & evidence

### Your role

During this stage you will establish a **defensible evidence**, and an **evidence layout**

### What you must do

- **Set workspace** — Choose the active skill workspace, land `**solution.conf`** with `**context_path`**, chunking-spec pointer, and room for `**manifest_sources[]`** ([set-workspace](phases/set-workspace.md)). Evidence **file paths** are finalized in context markdown, not here.
- **Convert** sources to **canonical markdown** where needed ([context-markdown](phases/context-markdown.md)); record `**manifest_sources[]`** there.
- Create a **chunking spec** (AI draft + human-reviewed) aligned to how the sources are structured, when context-chunking-approach work is needed.
- **Chunk files** on disk match the index and the chunking spec.
- Assemble a **context package** (`chunks/*.md` + `context_index.json` + manifest) that downstream work treats as **the** evidence layer, without ad hoc files or mystery sources.

**Important**: You do **not** introduce classes, properties,  inheritance or `interactions`here. You only **package and pin** evidence the later stages will cite by `chunk_id`. Until above are true, you **do not** start Stage 2. 


| #   | Phase                     | Summary                                                                                                                                                                     | Actor    | Phase automation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Outputs                                                                                  | Ref                                                                                          |
| --- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 0   | Set workspace             | Active skill workspace + `solution.conf` with `context_path`, `context_chunking_spec` pointer, and `manifest_sources[]` slot; evidence paths finalized in context markdown. | Human    | **1.** `python` [`scripts/generate_prompt.py`](../../scripts/generate_prompt.py) `--phase set-workspace` **2.** `python` [`scripts/set_workspace.py`](../../scripts/set_workspace.py) — no args prints current; `<path>` sets `active_skill_workspace` in `conf/abd-config.json` ([set-workspace](phases/set-workspace.md))                                                                                                                                                         | `**solution.conf`** landed; workspace root known to `**scripts/_config.py`**             | [set-workspace](phases/set-workspace.md)                                                     |
| 1   | Context markdown          | Convert non-Markdown sources to canonical `.md`; record corpus in `manifest_sources[]` (`.md` paths + roles).                                                               | Code     | **1.** `python` [`scripts/generate_prompt.py`](../../scripts/generate_prompt.py) `--phase context-markdown` **2.** `python` [`scripts/convert_sources_to_markdown.py`](../../scripts/convert_sources_to_markdown.py) — `--file` or `--manifest` ([context-markdown](phases/context-markdown.md))                                                                                                                                                                                    | Canonical `**.md`** beside sources (or documented equivalent) + `**manifest_sources[]`** | [context-markdown](phases/context-markdown.md)                                               |
| 2   | Context chunking approach | Read `manifest_sources`, structural inventory, draft `context_chunking_spec`, disclose assumptions/gaps; human reviews spec before canonical context.                       | AI-led   | **1.** `python` [`scripts/generate_prompt.py`](../../scripts/generate_prompt.py) `--phase context-chunking-approach` **2.** Follow the emitted bundle (land `context_chunking_spec` YAML per [context-chunking-approach](phases/context-chunking-approach.md); human review before canonical context).                                                                                                                                                                                  | `**context_chunking_spec`** (reviewed)                                                   | [context-chunking-approach](phases/context-chunking-approach.md)                             |
| 3   | Canonical Context         | Chunks files, tag evidence type and modelling kind                                                                                                                          | Code-led | **1.** `python` [`scripts/generate_prompt.py`](../../scripts/generate_prompt.py) `--phase canonical-context` **2.** `python` [`scripts/build_context.py`](../../scripts/build_context.py) ([canonical-context](phases/canonical-context.md)); then contract scan / validate per bundle                                                                                                                                                                                                | `context/chunks/*.md` + `context/context_index.json` / **v1** context package            | [canonical-context](phases/canonical-context.md), [context-spec.md](library/context-spec.md) |


---

## Stage 2 — Vocabulary & behavior

### Your role

You separate **language** and **observable behavior** from **domain types**. You ground terms and mechanisms in **context chunks** (indexed by `context_index.json`). You write a **shaped** story map (who does what to which state) **before** you lock a sparse type system. Evidence and stories must lead type choices, not the reverse.

### What you must do

- **Terms & mechanisms.** You will consume `**context_index.json`** and context chunks. You will emit **terms**, **mechanisms**, and a **candidate queue** (possible types with rationale, still not promoted). `**scripts/build_phase2_artifacts.py`** writes **empty** JSON scaffolds (`terms[]`, `mechanisms[]`, `candidates[]`) under `phase2/`; it does **not** read chunks or fill vocabulary. **Authors** (human or AI) edit those files and **must** cite `chunk_id` on substantive rows per [terms-mechanisms-contract.md](library/terms-mechanisms-contract.md).
- **Shaped story map.** You will author `shaped_story_map.json` (under `phase3/`) with trigger/response, anchor, `term_refs`, and `evidence_chunk_ids` where stories are substantive. Satisfy [shaped-story-shape](../../rules/shaped-story-shape.md) (automated check is **rule-bound** — see [Rules and automated checks](#rules-and-automated-checks) below). Details live in [terms-mechanisms](phases/terms-mechanisms.md) and [shaped-story-map](phases/shaped-story-map.md).

You do **not** put types in `concepts[]` yet.

### What you produce

- Shared **vocabulary** and **mechanism** artifacts tied to the corpus.
- A **candidate queue** for types (still not promoted).
- A **story map JSON** that reads as **capabilities and anchors**, not a type checklist.

### How you know you succeeded

Your terms-and-mechanisms artifacts trace back to `chunk_id`s. Your story map reads as **interaction capability**, not a list aligned to a future type catalog. Substantive stories tie to evidence where it matters. **Promotion** to domain types waits for Stage 3.


| #   | Phase                             | Summary                                                                                                                                                                                                                                                  | Actor  | Phase automation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Outputs                                                                          | Ref                                            |
| --- | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------- |
| 4   | Terms & mechanisms (layers 1 & 2) | `**build_phase2_artifacts.py`** emits **empty** schema shells; agent authors populate terms, mechanisms, and the candidate queue from context chunks with mandatory `chunk_id` citations per the contract. **Nothing** is promoted to `concepts[]` here. | AI-led | **1.** `python` [`scripts/generate_prompt.py`](../../scripts/generate_prompt.py) `--phase terms-mechanisms` **2.** `python` [`scripts/build_phase2_artifacts.py`](../../scripts/build_phase2_artifacts.py) (also via `build.py`); then author JSON per bundle                                                                                                                                                                                                                      | `phase2/terms_layer.json`, `mechanisms.json`, `candidate_queue.json` | [terms-mechanisms](phases/terms-mechanisms.md) |
| 5   | Shaped story map                  | Agent authors shaped story map (trigger/response, anchors, evidence links). Outcome: JSON map of capabilities and interactions, not a type catalog.                                                                                                      | AI-led | **1.** `python` [`scripts/generate_prompt.py`](../../scripts/generate_prompt.py) `--phase shaped-story-map` **2.** Author `phase3/shaped_story_map.json` per emitted bundle and [shaped-story-map](phases/shaped-story-map.md)                                                                                                                                                                                                                                                         | `phase3/shaped_story_map.json`                                                      | [shaped-story-map](phases/shaped-story-map.md) |


---

## Stage 3 — Domain modeling

### Your role

You add `concepts[]` only where stories and evidence justify **distinct** behavioral contracts. You avoid a large upfront ontology. You decide **variant shape** (enum versus subtypes versus other) **before** you spread properties across types. You deepen approved types with responsibilities, dependencies, and citations so the model is **arguable**.

### What you must do

- **Domain types.** You will run the **promotion gate**: candidate to **concept** with per-type rationale and explicit rejections (for example, “just a property on X”).
- **Variant classification.** You will write **variant decisions** per family (format is yours to standardize).
- **Deepen.** You will attach responsibilities, cross-type dependencies, and evidence to types in scope. Every substantive claim you add in AI-assisted passes **must** respect `chunk_id` discipline per the contract.

### What you produce

- A **small promoted set** with clear accept and reject rationale.
- **Per-family variant rules** before you churn structure.
- **Deepen** artifacts: responsibilities, `depends_on`, and evidence links for types in scope.

### How you know you succeeded

Your types are explainable at the depth you chose. Variant rules are stable before rework. Every promoted type has evidence. You use `extends` only where real substitution behavior requires it.


| #   | Phase                       | Summary                                                                                                                                                                                                            | Actor  | Phase automation                                                                                                                                                                                                                                                        | Outputs                                  | Ref                                                        |
| --- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- | ---------------------------------------------------------- |
| 6   | Domain types (`concepts[]`) | Promote a minimal set of concepts from the candidate queue with per-type rationale and explicit rejections. Outcome: `concepts[]` only where behavior justifies a distinct contract, not a large upfront ontology. | AI-led | `python` [`scripts/generate_prompt.py`](../../scripts/generate_prompt.py) `--phase domain-types`; then promote per bundle and [domain-types](phases/domain-types.md)                                                                                      | Sparse types + rationale                 | [domain-types](phases/domain-types.md)                     |
| 7   | Variant classification      | Decide how each variation family is represented before bulk property assignment. Outcome: written variant decisions per family so structure stays stable through deepen.                                           | AI-led | `python` [`scripts/generate_prompt.py`](../../scripts/generate_prompt.py) `--phase variant-classification`; then record decisions per bundle and [variant-classification](phases/variant-classification.md)                                               | Written variant decisions per family     | [variant-classification](phases/variant-classification.md) |
| 8   | Deepen                      | Attach responsibilities, cross-type dependencies, and evidence to types in scope, citing chunks where claims matter. Outcome: an arguable model traceable to the corpus.                                           | AI-led | `python` [`scripts/generate_prompt.py`](../../scripts/generate_prompt.py) `--phase deepen`; then deepen per bundle and [deepen](phases/deepen.md)                                                                                                         | Responsibilities, evidence, `depends_on` | [deepen](phases/deepen.md)                                 |


---

## Stage 4 — Integration & delivery

### Your role

You merge parallel work into **one coherent** map, model, and spec (or a deliberate split). You **drain** the candidate queue with explicit decisions. You **prove** quality with automation and visible outputs so reviewers get something **repeatable**, not a one-off edit.

### What you must do

- **Integrate.** You will integrate synonyms, repoint references, and merge the story map with types and terms. You will **close** or **defer** remaining candidates with rationale.
- **Validate & render.** You will run `**python scripts/build.py`** (which executes the [configured pipeline](#what-buildpy-does-for-you) including **rule-bound** automated checks), **render** reports, and run a critic pass against the **principles table** in [principles.md](library/principles.md) (and the phase **Rules** section / `rules/` where relevant) when you add that step to your workflow. You will wire **CI** on your chosen workspace (for example the bundled `test/sample-workspace`) for the scope you care about.

### What you produce

- An integrated **map-model-spec** narrative (or an intentional split).
- A **candidate queue** brought to explicit decisions.
- **Validation and reporting** output plus a bundle manifest that ties back to **principles** and **rules** used in the pipeline.

### How you know you succeeded

Your checks and manifest reproduce for the chosen scope. Your **CI** passes where you wired it. You can **explain** deliverables using provenance, the shaped story map, sparse types, and explicit variants without hand-waving.


| #   | Phase             | Summary                                                                                                                                                                                                              | Actor    | Phase automation                                                                                                                                                                                                                                                                                                                                                                                                    | Outputs                                    | Ref                                          |
| --- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | -------------------------------------------- |
| 9   | Integrate         | Merge synonyms, align references, combine story map with types and terms; close or defer every remaining candidate with rationale. Outcome: one coherent map-model-spec narrative, or a documented deliberate split. | AI-led   | `python` [`scripts/generate_prompt.py`](../../scripts/generate_prompt.py) `--phase integrate`; then integrate per bundle and [integrate](phases/integrate.md)                                                                                                                                                                                                                                         | Drained candidate queue → `map-model-spec` | [integrate](phases/integrate.md)             |
| 10  | Validate & render | Reproducible validation and reporting: full `**build.py`** pipeline (see below), bundle manifest, rule-example lint; wire CI in your host when you want automated runs.                                              | Code-led | **1.** `python` [`scripts/generate_prompt.py`](../../scripts/generate_prompt.py) `--phase validate-render` **2.** `python` [`scripts/build.py`](../../scripts/build.py) (full pipeline); includes `scripts/generate_context_bundle_manifest.py` per [validate-render](phases/validate-render.md)                                                                                                   | CI checks, rendered reports, manifest      | [validate-render](phases/validate-render.md) |


**Bundle manifest (cross-phase):** `scripts/generate_context_bundle_manifest.py` records hashes for sources and phase outputs. `scripts/build.py` invokes it as one step in `**operator.build_pipeline`**.

### Rules and automated checks

Same idea as **abd-story-synthesizer** ("validation uses **rules**; automation backs rules where implemented"): **phases** are not the home for scanner names.

- `**rules/*.md`** — normative **DO** / **DON'T** guidance. `**skill-config.json`** → `**phase_rules`** / `**every_phase_rules`** decides which rules are **inlined** into each built phase bundle (so agents see obligations **with** the phase).
- `**rules/scanners.json`** → `**rule_scanner_bindings`** — maps `**rule_id`** → **scanner script** for the checks we have automated. Add or change a binding when a new rule gets a script.
- **Phase automation** column: **every** row starts with **`generate_prompt`** (see [Generate prompt — required before every phase](#generate-prompt--required-before-every-phase-010)); additional lines are phase-specific commands. Assembly mode is **`skill-config.json`** → **`generate_prompt.assembly_mode`** (or **`delivery.mode`**). **Cross-phase** scanners and emitters still run when you execute **`python scripts/build.py`** (full pipeline) after artifact changes.

### What `build.py` does for you

`build.py` does **not** run set workspace or context markdown. It does **not** generate `chunks/` or `context_index.json`; that is the **canonical context** pipeline per [context-spec.md](library/context-spec.md).

`**python scripts/build.py --merge-only`** runs step **1** only (AGENTS + built phase bundles). **Skips** the post-merge pipeline.

`**python scripts/build.py`** (full pipeline) runs **1** then the ordered list in `**skill-config.json`** → `**operator.build_pipeline`** (default matches this skill's standard emitters, **rule-bound** scanners from [scanners.json](../../rules/scanners.json), manifest, rule-example lint):

1. `**MapsContentAssembler`** — merges this file and `phases/*.md` into `**content/built/agents-staged.md`** and `**AGENTS.md`**; writes `**content/built/phases/<slug>.md**` (and `**content/built/README.md**`). See [built/phases/README.md](../built/phases/README.md) and [content/built/README.md](../built/README.md).
2. Remaining entries in `**build_pipeline**` — typically: context index contract (rule **stage-1-context-decisions**), Phase 2 artifact emit, pipeline-output presence check, shaped story map evidence (rule **shaped-story-shape**), map-model-spec chunk citations (rule **evidence-citations-required**), bundle manifest, `**test_rule_examples.py`**.

**Authors** produce `chunks/` and `context_index.json` outside this script (canonical context). When those files exist, the pipeline's context-index step enforces [context-spec.md](library/context-spec.md) per **stage-1-context-decisions**.

---

## Documentation library (`content/parts/library/`)

Long-form contracts and narrative live under `**content/parts/library/`**. `**docs/README.md`** is an index that links into that folder (the `docs/` tree does not duplicate those files). Normative process lives in this file and in `phases/`. Phase-specific narrative belongs in `**phases/<slug>.md**`—e.g. `[set-workspace.md](phases/set-workspace.md)`; `[context-markdown.md](phases/context-markdown.md)`; chunking spec in `[context-chunking-approach.md](phases/context-chunking-approach.md)`; build, coherence, and validation in `[canonical-context.md](phases/canonical-context.md)`. **Shared** contracts (referenced by several process rows or by validators) stay in the table below. **Checkable** expectations (DO/DON'T, scanners) live only in `**rules/*.md`**, which `build.py` inlines into each phase bundle under **Rules**—not in the principles library file. When you change a stage or row, you update this file and the phase files, and you align `[principles.md](library/principles.md)` with the process table.


| Document                                                             | Role                                                                                                                                 |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| [principles.md](library/principles.md)                               | Principles table only (why we work this way); checkable rules stay in `rules/`                                                       |
| [context-spec.md](library/context-spec.md)                           | **Contract:** `chunks/`, `context_index.json`, manifest, chunking spec shapes (process: phase files + `phases/canonical-context.md`) |
| [terms-mechanisms-contract.md](library/terms-mechanisms-contract.md) | Terms & mechanisms row — artifacts + automation                                                                                      |
| [shaped-story-map.md](library/shaped-story-map.md)                   | Shaped story map row — JSON, validation, rationale                                                                                   |
| [domain-model.md](library/domain-model.md)                           | Modules, concepts, `map-model-spec` scaffold                                                                                         |
| [story-map.md](library/story-map.md)                                 | Full interaction-tree story map (prose)                                                                                              |
| [README.md](library/README.md)                                       | Index of this library                                                                                                                |


