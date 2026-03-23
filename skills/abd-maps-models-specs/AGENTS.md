# AGENTS — abd-maps-models-specs

## Process — abd-maps-models-specs

**Pipeline (navigation spine):** Set workspace → Context markdown → Context chunking approach → Canonical context → Terms & mechanisms → Story map → Domain types → Variants → Deepen → Integrate → Validate & render

### Generate prompt — required before every phase (0–10)

From the **skill package root** (the directory that contains `scripts/` and `conf/`):

1. **Before** doing work for **any** phase in the tables below, run **`python scripts/generate_prompt.py --phase <slug>`** and treat **stdout** as the binding procedure (role, phase body, library slices, inlined **rules**, and the **exact** commands for code-led steps). **AI-led** and **code-led** alike: the emitted bundle is normative; do not skip it in favor of only skimming this file.
2. **`<slug>`** is the `skill-config.json` → `phase_files` name: `set-workspace`, `context-markdown`, `context-chunking-approach`, `canonical-context`, `terms-mechanisms`, `shaped-story-map`, `domain-types`, `variant-classification`, `deepen`, `integrate`, `validate-render`.
3. **Static vs dynamic assembly** is configured in **`skill-config.json`**, not on the CLI: **`generate_prompt.assembly_mode`** is **`static`** (default for this skill) or **`dynamic`**. If that key is omitted, **`delivery.mode`** applies: **`static_built`** → prefer **`content/built/phases/<slug>.md`** when present; **`runtime_injection`** → always assemble from sources. If a built file is missing under static, the tool still assembles from sources (same as before).
4. If you expect a **pre-merged** bundle and **`content/built/phases/<slug>.md`** is missing, run **`python scripts/build.py --merge-only`** from the skill root, then run **`generate_prompt`** again.

Script path: `python` [`scripts/generate_prompt.py`](scripts/generate_prompt.py).

---

## Stage 1 — Context & evidence

### Your role

During this stage you will establish a **defensible evidence**, and an **evidence layout**

### What you must do

- **Set workspace** — Choose the active skill workspace, land `**solution.conf`** with `**context_path`**, chunking-spec pointer, and room for `**manifest_sources[]`** ([set-workspace](content/parts/phases/set-workspace.md)). Evidence **file paths** are finalized in context markdown, not here.
- **Convert** sources to **canonical markdown** where needed ([context-markdown](content/parts/phases/context-markdown.md)); record `**manifest_sources[]`** there.
- Create a **chunking spec** (AI draft + human-reviewed) aligned to how the sources are structured, when context-chunking-approach work is needed.
- **Chunk files** on disk match the index and the chunking spec.
- Assemble a **context package** (`chunks/*.md` + `context_index.json` + manifest) that downstream work treats as **the** evidence layer, without ad hoc files or mystery sources.

**Important**: You do **not** introduce classes, properties,  inheritance or `interactions`here. You only **package and pin** evidence the later stages will cite by `chunk_id`. Until above are true, you **do not** start Stage 2. 


| #   | Phase                     | Summary                                                                                                                                                                     | Actor    | Phase automation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Outputs                                                                                  | Ref                                                                                          |
| --- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 0   | Set workspace             | Active skill workspace + `solution.conf` with `context_path`, `context_chunking_spec` pointer, and `manifest_sources[]` slot; evidence paths finalized in context markdown. | Human    | **1.** `python` [`scripts/generate_prompt.py`](scripts/generate_prompt.py) `--phase set-workspace` **2.** `python` [`scripts/set_workspace.py`](scripts/set_workspace.py) — no args prints current; `<path>` sets `active_skill_workspace` in `conf/abd-config.json` ([set-workspace](content/parts/phases/set-workspace.md))                                                                                                                                                         | `**solution.conf`** landed; workspace root known to `**scripts/_config.py`**             | [set-workspace](content/parts/phases/set-workspace.md)                                                     |
| 1   | Context markdown          | Convert non-Markdown sources to canonical `.md`; record corpus in `manifest_sources[]` (`.md` paths + roles).                                                               | Code     | **1.** `python` [`scripts/generate_prompt.py`](scripts/generate_prompt.py) `--phase context-markdown` **2.** `python` [`scripts/convert_sources_to_markdown.py`](scripts/convert_sources_to_markdown.py) — `--file` or `--manifest` ([context-markdown](content/parts/phases/context-markdown.md))                                                                                                                                                                                    | Canonical `**.md`** beside sources (or documented equivalent) + `**manifest_sources[]`** | [context-markdown](content/parts/phases/context-markdown.md)                                               |
| 2   | Context chunking approach | Read `manifest_sources`, structural inventory, draft `context_chunking_spec`, disclose assumptions/gaps; human reviews spec before canonical context.                       | AI-led   | **1.** `python` [`scripts/generate_prompt.py`](scripts/generate_prompt.py) `--phase context-chunking-approach` **2.** Follow the emitted bundle (land `context_chunking_spec` YAML per [context-chunking-approach](content/parts/phases/context-chunking-approach.md); human review before canonical context).                                                                                                                                                                                  | `**context_chunking_spec`** (reviewed)                                                   | [context-chunking-approach](content/parts/phases/context-chunking-approach.md)                             |
| 3   | Canonical Context         | Chunks files, tag evidence type and modelling kind                                                                                                                          | Code-led | **1.** `python` [`scripts/generate_prompt.py`](scripts/generate_prompt.py) `--phase canonical-context` **2.** `python` [`scripts/build_context.py`](scripts/build_context.py) ([canonical-context](content/parts/phases/canonical-context.md)); then contract scan / validate per bundle                                                                                                                                                                                                | `context/chunks/*.md` + `context/context_index.json` / **v1** context package            | [canonical-context](content/parts/phases/canonical-context.md), [context-spec.md](library/context-spec.md) |


---

## Stage 2 — Vocabulary & behavior

### Your role

You separate **language** and **observable behavior** from **domain types**. You ground terms and mechanisms in **context chunks** (indexed by `context_index.json`). You write a **shaped** story map (who does what to which state) **before** you lock a sparse type system. Evidence and stories must lead type choices, not the reverse.

### What you must do

- **Terms & mechanisms.** You will consume `**context_index.json`** and context chunks. You will emit **terms**, **mechanisms**, and a **candidate queue** (possible types with rationale, still not promoted). `**scripts/build_phase2_artifacts.py`** writes **empty** JSON scaffolds (`terms[]`, `mechanisms[]`, `candidates[]`) under `phase2/`; it does **not** read chunks or fill vocabulary. **Authors** (human or AI) edit those files and **must** cite `chunk_id` on substantive rows per [terms-mechanisms-contract.md](library/terms-mechanisms-contract.md).
- **Shaped story map.** You will author `shaped_story_map.json` (under `phase3/`) with trigger/response, anchor, `term_refs`, and `evidence_chunk_ids` where stories are substantive. Satisfy [shaped-story-shape](../../rules/shaped-story-shape.md) (automated check is **rule-bound** — see [Rules and automated checks](#rules-and-automated-checks) below). Details live in [terms-mechanisms](content/parts/phases/terms-mechanisms.md) and [shaped-story-map](content/parts/phases/shaped-story-map.md).

You do **not** put types in `concepts[]` yet.

### What you produce

- Shared **vocabulary** and **mechanism** artifacts tied to the corpus.
- A **candidate queue** for types (still not promoted).
- A **story map JSON** that reads as **capabilities and anchors**, not a type checklist.

### How you know you succeeded

Your terms-and-mechanisms artifacts trace back to `chunk_id`s. Your story map reads as **interaction capability**, not a list aligned to a future type catalog. Substantive stories tie to evidence where it matters. **Promotion** to domain types waits for Stage 3.


| #   | Phase                             | Summary                                                                                                                                                                                                                                                  | Actor  | Phase automation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Outputs                                                                          | Ref                                            |
| --- | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------- |
| 4   | Terms & mechanisms (layers 1 & 2) | `**build_phase2_artifacts.py`** emits **empty** schema shells; agent authors populate terms, mechanisms, and the candidate queue from context chunks with mandatory `chunk_id` citations per the contract. **Nothing** is promoted to `concepts[]` here. | AI-led | **1.** `python` [`scripts/generate_prompt.py`](scripts/generate_prompt.py) `--phase terms-mechanisms` **2.** `python` [`scripts/build_phase2_artifacts.py`](scripts/build_phase2_artifacts.py) (also via `build.py`); then author JSON per bundle                                                                                                                                                                                                                      | `phase2/terms_layer.json`, `mechanisms.json`, `candidate_queue.json` | [terms-mechanisms](content/parts/phases/terms-mechanisms.md) |
| 5   | Shaped story map                  | Agent authors shaped story map (trigger/response, anchors, evidence links). Outcome: JSON map of capabilities and interactions, not a type catalog.                                                                                                      | AI-led | **1.** `python` [`scripts/generate_prompt.py`](scripts/generate_prompt.py) `--phase shaped-story-map` **2.** Author `phase3/shaped_story_map.json` per emitted bundle and [shaped-story-map](content/parts/phases/shaped-story-map.md)                                                                                                                                                                                                                                                         | `phase3/shaped_story_map.json`                                                      | [shaped-story-map](content/parts/phases/shaped-story-map.md) |


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
| 6   | Domain types (`concepts[]`) | Promote a minimal set of concepts from the candidate queue with per-type rationale and explicit rejections. Outcome: `concepts[]` only where behavior justifies a distinct contract, not a large upfront ontology. | AI-led | `python` [`scripts/generate_prompt.py`](scripts/generate_prompt.py) `--phase domain-types`; then promote per bundle and [domain-types](content/parts/phases/domain-types.md)                                                                                      | Sparse types + rationale                 | [domain-types](content/parts/phases/domain-types.md)                     |
| 7   | Variant classification      | Decide how each variation family is represented before bulk property assignment. Outcome: written variant decisions per family so structure stays stable through deepen.                                           | AI-led | `python` [`scripts/generate_prompt.py`](scripts/generate_prompt.py) `--phase variant-classification`; then record decisions per bundle and [variant-classification](content/parts/phases/variant-classification.md)                                               | Written variant decisions per family     | [variant-classification](content/parts/phases/variant-classification.md) |
| 8   | Deepen                      | Attach responsibilities, cross-type dependencies, and evidence to types in scope, citing chunks where claims matter. Outcome: an arguable model traceable to the corpus.                                           | AI-led | `python` [`scripts/generate_prompt.py`](scripts/generate_prompt.py) `--phase deepen`; then deepen per bundle and [deepen](content/parts/phases/deepen.md)                                                                                                         | Responsibilities, evidence, `depends_on` | [deepen](content/parts/phases/deepen.md)                                 |


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
| 9   | Integrate         | Merge synonyms, align references, combine story map with types and terms; close or defer every remaining candidate with rationale. Outcome: one coherent map-model-spec narrative, or a documented deliberate split. | AI-led   | `python` [`scripts/generate_prompt.py`](scripts/generate_prompt.py) `--phase integrate`; then integrate per bundle and [integrate](content/parts/phases/integrate.md)                                                                                                                                                                                                                                         | Drained candidate queue → `map-model-spec` | [integrate](content/parts/phases/integrate.md)             |
| 10  | Validate & render | Reproducible validation and reporting: full `**build.py`** pipeline (see below), bundle manifest, rule-example lint; wire CI in your host when you want automated runs.                                              | Code-led | **1.** `python` [`scripts/generate_prompt.py`](scripts/generate_prompt.py) `--phase validate-render` **2.** `python` [`scripts/build.py`](scripts/build.py) (full pipeline); includes `scripts/generate_context_bundle_manifest.py` per [validate-render](content/parts/phases/validate-render.md)                                                                                                   | CI checks, rendered reports, manifest      | [validate-render](content/parts/phases/validate-render.md) |


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

1. `**MapsContentAssembler`** — merges this file and `phases/*.md` into `**content/built/agents-staged.md`** and `**AGENTS.md`**; writes `**content/built/phases/<slug>.md**` (and `**content/built/README.md**`). See [built/phases/README.md](content/built/phases/README.md) and [content/built/README.md](content/built/README.md).
2. Remaining entries in `**build_pipeline**` — typically: context index contract (rule **stage-1-context-decisions**), Phase 2 artifact emit, pipeline-output presence check, shaped story map evidence (rule **shaped-story-shape**), map-model-spec chunk citations (rule **evidence-citations-required**), bundle manifest, `**test_rule_examples.py`**.

**Authors** produce `chunks/` and `context_index.json` outside this script (canonical context). When those files exist, the pipeline's context-index step enforces [context-spec.md](library/context-spec.md) per **stage-1-context-decisions**.

---

## Documentation library (`content/parts/library/`)

Long-form contracts and narrative live under `**content/parts/library/`**. `**docs/README.md`** is an index that links into that folder (the `docs/` tree does not duplicate those files). Normative process lives in this file and in `phases/`. Phase-specific narrative belongs in `**phases/<slug>.md**`—e.g. `[set-workspace.md](content/parts/phases/set-workspace.md)`; `[context-markdown.md](content/parts/phases/context-markdown.md)`; chunking spec in `[context-chunking-approach.md](content/parts/phases/context-chunking-approach.md)`; build, coherence, and validation in `[canonical-context.md](content/parts/phases/canonical-context.md)`. **Shared** contracts (referenced by several process rows or by validators) stay in the table below. **Checkable** expectations (DO/DON'T, scanners) live only in `**rules/*.md`**, which `build.py` inlines into each phase bundle under **Rules**—not in the principles library file. When you change a stage or row, you update this file and the phase files, and you align `[principles.md](library/principles.md)` with the process table.


| Document                                                             | Role                                                                                                                                 |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| [principles.md](library/principles.md)                               | Principles table only (why we work this way); checkable rules stay in `rules/`                                                       |
| [context-spec.md](library/context-spec.md)                           | **Contract:** `chunks/`, `context_index.json`, manifest, chunking spec shapes (process: phase files + `phases/canonical-context.md`) |
| [terms-mechanisms-contract.md](library/terms-mechanisms-contract.md) | Terms & mechanisms row — artifacts + automation                                                                                      |
| [shaped-story-map.md](library/shaped-story-map.md)                   | Shaped story map row — JSON, validation, rationale                                                                                   |
| [domain-model.md](library/domain-model.md)                           | Modules, concepts, `map-model-spec` scaffold                                                                                         |
| [story-map.md](library/story-map.md)                                 | Full interaction-tree story map (prose)                                                                                              |
| [README.md](library/README.md)                                       | Index of this library                                                                                                                |


---

## Set workspace

**You will** decide **where** the solution lives on disk and land **`solution.conf`** so every later step resolves paths the same way.

**You must not** finalize the full list of evidence files here—that happens when you finish **context markdown** and record `**manifest_sources[]`** there (see [context-markdown.md](content/parts/phases/context-markdown.md)).

**You will:**

1. **Choose the active skill workspace** — One folder that will contain `**solution.conf**`. The skill package points at it with `**conf/abd-config.json**` → `**active_skill_workspace**` (or the deprecated aliases documented in `scripts/_config.py`). **You must** treat that folder as the root for every relative path in `**solution.conf**`.
2. **Create or edit `solution.conf` in that workspace.** **You must** wire at minimum:
   - `**context_path**` and output conventions (where context artifacts like chunks and the index will live).
   - `**context_chunking_spec**` — pointer to the chunking YAML (default basename `**context_chunking_spec.yaml**` beside `**solution.conf**`). The YAML **contents** are drafted and reviewed in [context-chunking-approach.md](content/parts/phases/context-chunking-approach.md); in this phase **you should** only ensure the **pointer** exists so tooling knows where to read it.
   - `**manifest_sources[]`** — **You may** start **empty** or as a stub. The **authoritative list of which Markdown files are your corpus** (and each `**role**`) is finalized when you complete **context markdown**: that is where **you will** record **where** sources came from and **where** canonical `**.md**` landed (see end of [context-markdown.md](content/parts/phases/context-markdown.md)).

**Command line:** From the **skill package root** (the folder that contains `**scripts/**` and `**conf/**`):

- `python scripts/set_workspace.py` — **You will** use this to print the configured workspace path string (first non-empty among `**active_skill_workspace**`, then deprecated `**solution_workspace**` / `**skill_space_path**`).
- `python scripts/set_workspace.py <path>` — **You will** use this to set `**active_skill_workspace**` in `**conf/abd-config.json**` to `**<path>**` (resolved; stored **relative to the skill package** when that keeps the value portable, otherwise absolute). The script also writes the same string to `**solution_workspace**` for tools that still read the legacy key. **You must** pass an existing directory for `**<path>**` (the folder that will contain or already contains `**solution.conf**`).

This entry point matches the idea of `**skills/abd-solution-modeler/scripts/workspace.py**`; there is no separate “storage synchronizer” script in this repository.

**You should** treat **`scripts/_config.py`** (skill package root — the directory that contains `**scripts/**` and `**conf/**`) as how emitters and validators resolve paths consistently. [canonical-context.md](content/parts/phases/canonical-context.md) assumes this workspace and `**solution.conf**` already exist.

## See also

- **[context-markdown.md](content/parts/phases/context-markdown.md)** — Conversion and `**manifest_sources**` (evidence locations).
- **[context-chunking-approach.md](content/parts/phases/context-chunking-approach.md)** — Structural inventory and `**context_chunking_spec**` contents.
- **[canonical-context.md](content/parts/phases/canonical-context.md)** — Context package (chunks, index, validate).


---

## Context markdown

Produce **canonical Markdown** for each evidence source that is not already Markdown, then list those `.md` paths in `manifest_sources`. **Canonical context** assumes **Markdown** on disk.

**You will:**

1. Produce **canonical Markdown** for each source that is not already Markdown (fix encoding, strip or tag conversion artifacts you already know about, and land paths you can list in `manifest_sources`).
2. Keep conversion **repeatable**: use the same **Python** entry points below whenever you convert (dependency versions are fixed by a proper skill install). Run commands from the **abd-maps-models-specs skill package root** (the directory that contains `scripts/` and `conf/`). Paths you pass to `--file`, and paths in `manifest_sources[]`, are relative to the **skill workspace** (folder that contains `solution.conf`, from `conf/abd-config.json` → `active_skill_workspace`).

**Why two commands:** `--manifest` only works off a list that already exists in `solution.conf`. The **first** time you wire a workspace, that list is usually empty or not written yet—so you convert **named files** with `--file`, then **author** `manifest_sources[]` to point at the resulting `.md` files (and any sources that were already Markdown). Later, when the manifest is the source of truth and you add or swap non-Markdown paths there, `**--manifest`** is the point: one run converts every supported non-`.md` entry the manifest names (skips missing paths, already-`.md`, and unsupported extensions) without typing each path again.

**Exact commands (repeatable)**

Working directory: `skills/abd-maps-models-specs/` (repository path may vary; this folder must be current when you invoke Python).

**A — Greenfield or “not in the manifest yet”**  
**Point:** Convert a file you have on disk **before** `manifest_sources[]` describes it (or when you are landing files and will write the manifest afterward).

`python scripts/convert_sources_to_markdown.py --file <path>`

`<path>` is relative to the skill workspace unless it is absolute. Example: `python scripts/convert_sources_to_markdown.py --file docs/handbook.pdf`

Repeat for each non-Markdown source as needed. Then edit `solution.conf` and set `manifest_sources[]` to the **Markdown** paths canonical context should read.

**B — Manifest already lists the corpus**  
**Point:** Refresh conversion for **everything the manifest already points at**—typical after you add new `.pdf` / `.docx` / … paths to `manifest_sources[]` or re-run after upstream edits.

`python scripts/convert_sources_to_markdown.py --manifest`

Still **update** any `path` values to the `.md` files after conversion; the script does **not** rewrite `solution.conf`.

**Behavior:** writes `<stem>.md` beside each converted source and prefixes output with `<!-- Source: … -->` for provenance.

For SharePoint / OneDrive fetch, chunk-to-memory layout, or vector RAG, use **abd-context-to-memory** instead and record **its** exact commands the same way.

**What goes in `manifest_sources[]`:** After conversion (and for any sources that were already Markdown), **`solution.conf` → `manifest_sources[]`** is where you **record the corpus for downstream work**: each entry’s **`path`** is the **Markdown** file path (relative to the skill workspace—see [set-workspace.md](content/parts/phases/set-workspace.md)), and **`role`** is your provenance anchor for that source. That list is what **chunking** and **canonical context** read as “these are the files we cover”; it is the durable answer to **where** context came from and **where** canonical **`.md`** lives on disk.

## See also

- **[set-workspace.md](content/parts/phases/set-workspace.md)** — Skill workspace and **`solution.conf`** wiring (before you finalize paths here).
- **[context-chunking-approach.md](content/parts/phases/context-chunking-approach.md)** — Chunking spec after Markdown and **`manifest_sources`** exist.
- **[canonical-context.md](content/parts/phases/canonical-context.md)** — Context package (chunks, index, validate).


---

## Context chunking approach


**You will** read every file listed in **`manifest_sources`**, perform structural inventory, **draft** the YAML per [context-spec.md](content/parts/library/context-spec.md) chunking spec, and **disclose** what **you** did—assumptions, uncertainties, and anything **you** could not infer from structure alone.

**You will not skip this:** After **your** draft, you will present results to the user to spot‑check against the real Markdown, correct wrong patterns, tighten taxonomy, and **accept** the spec before **canonical context** runs.

**If the spec already fits the sources,** **you will** **not** re-run a full inventory—only revisit when layout or **`manifest_sources`** change materially.

---

## 1. Structural scan (inventory you will encode)

**You will** model the manuscript’s real shape before YAML is finalized. **You are going to** deliver **(a)** a short **structural report** (what **you** observed, risks, open questions) and **(b)** the **draft `context_chunking_spec`**. This is not a pass/fail score. If **your** inventory is shallow, canonical-context tooling will split mid-table or treat boilerplate as rules—and coherence **still needs the source** to catch drift; neither pass can fix a wrong **split policy** without updating the spec or the emitter.

### 1.1 Outline and navigation

**You will** examine and record:

- **Heading ladder** — Which `#` … `######` levels mean part, chapter, section, subsection? Are levels consistent?
- **Numbering** — Do `1.`, `1.2.3`, or appendix letters align with headings, or do lists float without a heading boundary?
- **Navigation chrome** — ToCs, “in this section,” breadcrumbs: **content** to chunk, or **noise** to exclude or tag per [context-spec.md](content/parts/library/context-spec.md)?

### 1.2 Dense and atomic regions

**You will** apply these constraints when **you** encode rules:

- **Tables** — Never split **through** a row; split above/below the table block.
- **Lists and definition lists** — A rule plus its bullets is often **one** unit.
- **Stat blocks, callouts, boxed examples** — Note delimiters. Repeated shapes → **pattern rules** in YAML, not one-off IDs.
- **Code fences** — Often stay with the prose that introduces them.

### 1.3 Noise vs signal

**You will** classify:

- **Export junk** — Running headers, page numbers, license blobs, conversion artifacts.
- **Policy** — Exclude (and use `**excluded[]`** where the contract allows), or **include and tag** (`metadata_noise`, `noise`, `structural_only`). Field meanings: [context-spec.md](content/parts/library/context-spec.md).

### 1.4 Repeated templates

**You will** encode the **pattern** in `**section_boundaries`** / splitting rules and set `**defaults**` + `**taxonomy**` for that pattern.

### 1.5 Capture sheet (you fill; human verifies)


| You will determine…                    | So the spec can encode…                                                                                        |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| What **starts** a new major unit?      | `chapter_break_regex` / `section_break_regex` ([context-spec.md](content/parts/library/context-spec.md) § Chunking spec). |
| What must **never** be split inside?   | `**splitting`** (e.g. keep tables intact).                                                                     |
| When tiny bits **merge**?              | `**min_chunk_chars`**, merge rules.                                                                            |
| What is **out of scope** for modeling? | `**modeling_kind`** defaults, exclusions.                                                                      |
| Which **taxonomy** values apply?       | Closed-world enums aligned with [context-spec.md](content/parts/library/context-spec.md).                                 |


---

## 2. Produce and land `context_chunking_spec`

1. **You will** write the YAML at `**solution.conf` → `context_chunking_spec`** (default basename `context_chunking_spec.yaml` beside `solution.conf`). **Fields and examples:** [context-spec.md](content/parts/library/context-spec.md) § Chunking spec. **Minimum areas:** `**section_boundaries`**, `**splitting`**, `**defaults**`, `**taxonomy**`.
2. **You will** disclose in the same turn or an accompanying note: **sources read**, **assumptions**, **low-confidence rules**, and **gaps** (e.g. “could not infer appendix boundary pattern”). **Human (solution analyst)** **will** use this during review.
3. **Human (solution analyst):** **You will** run a secondary pass on the manuscript vs draft YAML: fix wrong headings/tables/noise calls, tighten taxonomy, and ensure the spec is **valid** per [context-spec.md](content/parts/library/context-spec.md). The landed file is **owned** by the workspace; the AI draft is not sufficient without this review.

The list of **`manifest_sources`** **`path`** values is the corpus this spec **must** cover. Path resolution for **`solution.conf`**, chunking YAML, **`context_path`**, and outputs follows **`scripts/_config.py`** (same skill workspace as [set-workspace.md](content/parts/phases/set-workspace.md)).

---

## 3. If `chunks/` and an index already exist

**You will** feed learning back into the spec when asked—often **you** run another full chunking pass (structural report + draft YAML) and **Human (solution analyst)** **will** review again: coverage, misfiring defaults, new section shapes. That is **spec maintenance** for this phase—not canonical context’s contract validator.

---

## See also

- **[set-workspace.md](content/parts/phases/set-workspace.md)** — Workspace root and **`solution.conf`** wiring.
- **[context-markdown.md](content/parts/phases/context-markdown.md)** — **`manifest_sources`** and canonical **`.md`**.
- **[canonical-context.md](content/parts/phases/canonical-context.md)** — Context package (chunks, index, validate).
- **[context-spec.md](content/parts/library/context-spec.md)** — Normative chunk/index/manifest shapes and checklist.


---

## Canonical context — build and validate the package

**You will** produce a **single, versioned** context package with manifest provenance so later work cites well-structured, well-understood context from a modeling perspective.

**You will** turn **canonical Markdown** into a **validated** context package:

- **You must** ensure later work can cite `**chunk_id`** rows that exist on disk and in the index.
- **You must not** invent files or leave mystery sources

**Skill workspace:** **You will** treat the folder that contains `**solution.conf`** (selected by `**conf/abd-config.json` → `active_skill_workspace`**) as the root for every path in `**solution.conf`**—the same rules `**scripts/_config.py**` uses.

---

## Phase automation (emit)

All paths are under the **abd-maps-models-specs** skill package (the folder that contains `scripts/` and `conf/`).


| Script                                | Purpose                                                                                         |
| ------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `**python scripts/build_context.py`** | Emit `chunks/*.md` and `context_index.json`. Optional: `--dry-run`, `--config <solution.conf>`. |


Segmentation matches `**skills/abd-context-to-memory/scripts/chunk_markdown.py**`; implementation lives in `**scripts/context_chunk_from_memory.py**`. **Full schema** (front matter, index, manifest): [context-spec.md](content/parts/library/context-spec.md).

---

## Order of work

Work happens **in this order**: **code** (emit) → **AI** (coherence) → **code** (validate). Rationale: cut the corpus deterministically first, then judge whether cuts and labels match the manuscript, then check structure mechanically.

---

### 1. Emit the package (**code**)

**Actor:** Code (`build_context.py`).

**Inputs (read for you by `_config.py`):**

- `**conf/abd-config.json`** → workspace root.
- `**solution.conf`** → `manifest_sources[]`, `context_path`, `context_chunking_spec`.
- Each file listed in `**manifest_sources[]**` that ends in `**.md**`.
- `**context_chunking_spec**` — at minimum, `**defaults**` supply `**evidence_type**` and `**modeling_kind**` for new chunks until you change them in coherence.

**Outputs (under `<workspace>/<context_path>/`):**

- `**chunks/{chunk_id}.md`** — one file per chunk; YAML front matter + body per [context-spec.md](content/parts/library/context-spec.md).
- `**context_index.json`** — `spec_version`, `**manifest**` (sources + hashes + generator id), `**blocks[]**` aligned to those files.

**What the code does *not* do:** It does not decide whether a split is *wise* for your domain

---

### 2. Coherence pass (**AI or human**)

**Actor:** You (LLM session), **not** the emit script and **not** the contract scanner.

The **rule-bound** automated check (see [stage-1-context-decisions](../../rules/stage-1-context-decisions.md) and [scanners.json](../../rules/scanners.json)) verifies **shape** (files, ids, required fields). It does **not** read the whole handbook and ask “should this block be labeled `rule`?” — that is **your** job here.

**Inputs you use:**

- The **original** canonical Markdown at the paths in `**manifest_sources[]`** (ground truth).
- The emitted `**chunks/*.md`** and `**context_index.json**`.

**What you do:**

1. **Splits** — Walk the source and the chunks. Do boundaries follow the chunking **intent** (e.g. no half-table, no orphan heading, no merged topics that should be separate)? If not, adjust **chunk bodies** and/or **index** so they still obey [context-spec.md](content/parts/library/context-spec.md), or go back and fix `**context_chunking_spec`** / re-emit if the problem is structural.
2. **Labels** — Within **taxonomy** allowed by the chunking spec, set `**evidence_type`** and `**modeling_kind`** in front matter **and** matching `**blocks[]`** rows so they match **what the chunk text actually is** (form vs modeling stance — see context-spec). Fix `**preview`** text so it reflects the body, not a generic stub.
3. **Consistency** — Front matter, index row, and chunk body must **agree** (same `chunk_id`, same anchors, no contradictions).

**Rules:**

- Only edit fields the **schema allows**; do not invent free-form “evidence” without a `**chunk_id`**.
- **Do not** promote to terms, mechanisms, types, or `concepts[]` here — this phase **packages** evidence only.
- After you change chunks or the index, run **`python scripts/build.py`** (or the same pipeline your CI uses) so the **stage-1-context-decisions** check runs again.

---

### 3. Validate (**code**)

**Actor:** Automation for rule **stage-1-context-decisions** (scanner path in [scanners.json](../../rules/scanners.json)); executed from **`python scripts/build.py`** via **`operator.build_pipeline`**.

**Inputs:** Existing `**context_index.json`** and `**chunks/*.md`** (and workspace paths from config). If there is **no** index yet, the check exits success (greenfield).

**Outcome:** Exit **0** means the contract in [context-spec.md](content/parts/library/context-spec.md) is satisfied (e.g. every `blocks[]` row has a file, every chunk file is indexed or `**excluded`**, `chunk_id` in front matter matches filename, manifest/source checks as implemented). Exit **non-zero** means fix the artifacts and re-run **`build.py`**.

Treat this as a **hard gate** before later stages cite `**chunk_id`**.

---

## Other notes

- Rule ↔ scanner bindings: [scanners.json](../../rules/scanners.json) (`rule_scanner_bindings`).

---

## Related documents


| Topic                                  | Document                                                                                   |
| -------------------------------------- | ------------------------------------------------------------------------------------------ |
| Workspace + `solution.conf`            | [set-workspace.md](content/parts/phases/set-workspace.md)                                                       |
| Canonical `.md` + `manifest_sources[]` | [context-markdown.md](content/parts/phases/context-markdown.md)                                                 |
| Draft/review chunking YAML             | [context-chunking-approach.md](content/parts/phases/context-chunking-approach.md)                               |
| Schema and contract detail             | [context-spec.md](content/parts/library/context-spec.md)                                              |
| Pipeline overview                      | [process.md](content/parts/process.md), [principles.md](content/parts/library/principles.md) |


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



**Outputs:** `<workspace>/<output_dir>/phase2/terms_layer.json`, `mechanisms.json`, `candidate_queue.json`.



**Implementation notes:** [`terms-mechanisms-contract.md`](content/parts/library/terms-mechanisms-contract.md) (includes **inputs** and **`chunk_id` citation** rules for Phase 2).


---

## Shaped story map



**Goal:** Epics/stories that satisfy **actor → behavior → anchor** (domain state **read** and/or **write**); alignment allows **term** references without minting types.



**Normative for Phase 3:** this document. [`process.md`](content/parts/process.md) is pipeline **summary** only (table row)—not the procedure.



## Actor



**Automated enforcement** is **rule-bound** ([shaped-story-shape](../../rules/shaped-story-shape.md), [scanners.json](../../rules/scanners.json)); it runs as part of **`python scripts/build.py`**. **Human / AI** maintain `shaped_story_map.json`.



## Requirements



- Every story has a **clear** behavioral reading and **traceability** to concepts.

- No story exists solely to **match strings** in the type list.

- Every story states its **anchor** (read path, write path, or both)—not every story requires **mutation** of the core write model.

- **Query/read/forward** stories are as valid as **mutating** stories when the anchor is explicit.

- Substantive stories carry **`evidence_chunk_ids[]`** referencing **`context_index.json`** / `chunks/` ([`shaped-story-map.md`](content/parts/library/shaped-story-map.md)); `phase3_story_map_evidence.py` extends to enforce this when authored.



## Exit



Story map validated; **domain types** (`concepts[]`) follow after the shaped story map is sound.



**Output:** `phase3/shaped_story_map.json` under the workspace output root (when present).



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



Type count and rationale remain reviewable for the chosen workspace depth.


---

## Variant classification



**Goal:** Per family: **enum vs `extends`** **before** property churn.



**Normative for Phase 5:** this document. [`process.md`](content/parts/process.md) is pipeline **summary** only (table row)—not the procedure.



## Steps



1. For each variant family, record the **decision**: enum vs subtypes vs other **before** bulk property assignment.

2. Align with **Explicit variant representation** in [`principles.md`](content/parts/library/principles.md) / plan principles table.



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



**Goal:** Automated checks (scanners, schema) + **rendered** reports; CI on your configured workspace; optional **critic** checklist against the **principles table** in [`principles.md`](content/parts/library/principles.md) and applicable **`rules/`** for the scope.



**Normative for Phase 8:** this document. [`process.md`](content/parts/process.md) is pipeline **summary** only (table row)—not the procedure.



## Actor



**Code** — `skill-config` scanners, `scripts/generate_context_bundle_manifest.py` (invoked from `scripts/build.py`). **Human / AI** — review reports.



## Steps



1. Run structural / schema scanners defined for the skill.

2. Render reports as configured (paths under fixture output root).

3. Optional: critique pass against [`principles.md`](content/parts/library/principles.md) and phase **Rules** / `rules/` (external expert or checklist).



## Exit



Reproducible validation + manifest; CI green for the chosen workspace at the chosen scope.
