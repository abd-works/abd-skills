# Process — Maps-Models-Specs

Pipeline: Context → Foundational spine → Modules/epics scaffold (breadth) → Classify → Deepen → Integrate → Evidence → Structure → Finalize.

**Core principle:** Discover taxonomy layer by layer, top-down, with evidence indexed as you go. Each pipeline step is a separate AI or code pass. Scanners enforce structure mechanically. AI resolves violations — scanners never propose fixes.

**Prerequisites:** Stage 1 — source documents (PDF, DOCX, PPTX, etc.). Stage 2+ — `context_index.json` and `chunks/*.md` under **`context_path`** from `solution.conf` (default `<output_dir>/context`).

**Config:** `skill-config.json` must set **`solution_workspace`** (workspace root with **`solution.conf`**). In `solution.conf`, **`output_dir`** holds map-model-spec.\*, mms-chunk-index.json, evidence/, summary.md, relationships.md, generated/; **`context_path`** holds context_index.json and chunks/. See `conf/README.md`. Scripts fail if workspace is missing or invalid.

**Two parallel artifacts produced at every pipeline step:**

- **Domain model** — modules, concepts, properties, operations (what things are and own)
- **Story map** — epics, sub-epics, stories, acceptance criteria, specifications, examples (what actors do and what changes)

These are two views of the same coin and must be produced simultaneously. **Epics matter for scope and flow, but they are empty if they do not verify the domain** — every epic **`statement`** and **`confirming_stories`** name must **ground in `concepts[].name`** and **chunks**; otherwise the story map is labels without a model underneath.

**Output files (under `output_dir`; single evolving spec):**

- `map-model-spec.json` — forward index (foundational spine; modules/epics scaffold breadth; classify; deepen; integrate; evidence; structure and finalize — see Stage 2–3 tables below)
- `map-model-spec.md` — human-readable summary (**layout:** fill from JSON using **`parts/templates/map-model-spec.md.template.md`**)
- `mms-chunk-index.json` — reverse index (chunk_id → concepts, epics, stories, modules). **Code-only:** run `build_chunk_index.py` after **Modules and Epics**, **Concept Classes and Stories**, or **Integrate and Harmonize** — each has a **Build chunk index** row in the Stage 2 table (**5a**, **7a**, **8a**). AI steps do not run it.
- **Concept Classification (code)** (row **6a**) also writes **`summary.md`**, **`relationships.md`** (same directory as the spec, unless a script overrides).

**Step specs** (same pattern as solution modeler `pieces/phases/`): Clean instructions live in `parts/steps/<name>.md`. **Agents use the built files** in `parts/steps/built/<name>.md` (base + rules baked in). Do not edit `built/` by hand. After changing a step or any rule, run `python scripts/build.py` (or `build_agents.py`).

---

## Stage 1: Extract Context


| #   | Step        | Initiator    | Script                        | What it does                                                   | Coverage       | Ref                   | Inputs           | Outputs                         |
| --- | ----------- | ------------ | ----------------------------- | -------------------------------------------------------------- | -------------- | --------------------- | ---------------- | ------------------------------- |
| 1   | **Convert** | Human → Code | convert_to_markdown.py        | Source → markdown                                              | Creates corpus | [context](context.md) | Source folder    | markdown                        |
| 2   | **Analyze** | AI           | discover_context_structure.py | Analyze markdown → markers for headers, tables, sections, TOC, | —              | [context](context.md) | markdown         | solution.conf                   |
| 3   | **Parse, curate, chunk, index** | Code | parse_and_curate.py | Parse → **curate** (classify, exclude) → chunk → index          | —              | [context](context.md) | markdown         | chunks/*.md, context_index.json |

**Curate note:** Curate is **not** a separate script step. The script parse_and_curate.py does all of: parse markdown to blocks; **curate** (classify evidence_type, assign document_region, exclude noise and out-of-scope sections); purpose-built chunking and merge; write chunks and context_index.json. Excluded blocks are listed in context_index.json under `excluded` and are not written to chunks.


---

## Stage 2: Map and Model (rows 4–8)

Rows **4** and **5** are **two separate AI passes** (foundational spine vs. modules/epics scaffold breadth), not two halves of one pass.

| #   | Step                              | Actor | Script                                    | What it does                                                                                                                  | Coverage               | Ref                                                   | Inputs                                    | Outputs                                           |
| --- | --------------------------------- | ----- | ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------------- | ----------------------------------------- | ------------------------------------------------- |
| 4   | **Foundational mechanisms**       | AI    | —                                         | **Before** chunk-heavy scaffold work: from `context_index.json` + document headings/TOC, identify **3–7 foundational mechanisms**. **Spine = `concepts[]` per area** (named domain objects/mechanisms + citations), not module/epic labels alone; epics/`confirming_stories` ground in **`concepts[].name`**. Write **`modules_and_epics`** rows (`foundational`, `evidence_stage: hypothesis` on concepts); attach provisional citations; **human checkpoint** — then run **Modules and Epics** (row 5). | Skim / structure       | [modules-epics-foundational-spine (built)](steps/built/modules-epics-foundational-spine.md) | context (index + corpus skim)             | map-model-spec.json                               |
| 5   | **Modules and Epics**             | AI    | —                                         | **After** foundational spine gate: orientation pass; **full-read ~30%** of corpus (**K ≈ round(0.3N)** chunks, breadth); expand **`modules_and_epics`** with cited candidates, epics/stories, layering, per-module **`depends_on`**; scanners; hand off for review. Advance `evidence_stage` toward **`scaffolded`** where chunks substantiate. **`confirming_stories`:** add **as many** names as needed to validate foundational concepts — **not** a default of two. Use interactive AI (optionally **batches / sub-agents** per [modules-epics-scaffold-breadth](steps/built/modules-epics-scaffold-breadth.md)). | ~K full reads          | [modules-epics-scaffold-breadth (built)](steps/built/modules-epics-scaffold-breadth.md) | context/, map-model-spec.json             | map-model-spec.json, map-model-spec.md            |
| 5a  | **Build chunk index**             | Code  | build_chunk_index.py                      | Regenerate reverse index from map-model-spec.json                                                                             | —                      | —                                                     | map-model-spec.json                       | mms-chunk-index.json                              |
| 6   | **Concept Classification**        | AI    | classify_chunks.py (Pass 1)               | AI reads chunks (or configured %); extracts concepts and relationships                                                        | All chunks             | [concept-classification (built)](steps/built/concept-classification.md)   | map-model-spec.json, context/             | map-model-spec.json                               |
| 6a  | **Concept Classification (code)** | Code  | classify_chunks.py (Pass 2); summarize.py | Code scans chunks; extracts concepts and relationships, merges gaps with AI pass; summarize.py → summary.md, relationships.md | All chunks             | [concept-classification (built)](steps/built/concept-classification.md)   | map-model-spec.json                       | map-model-spec.json, summary.md, relationships.md |
| 7   | **Concept Classes and Stories**   | AI    | —                                         | Deepen classes/stories per module/epic; resolve [defer] tags                                                                  | Chunks per Module/Epic | [concept-classes-stories (built)](steps/built/concept-classes-stories.md) | map-model-spec.json, context/             | map-model-spec.json                               |
| 7a  | **Build chunk index**             | Code  | build_chunk_index.py                      | Regenerate reverse index from map-model-spec.json                                                                             | —                      | —                                                     | map-model-spec.json                       | mms-chunk-index.json                              |
| 8   | **Integrate and Harmonize**       | AI    | —                                         | Unify naming; wire cross-module; resolve [cross-cutting]; finalize subtypes                                                   | —                      | [integrate-harmonize (built)](steps/built/integrate-harmonize.md)         | map-model-spec.json, mms-chunk-index.json | map-model-spec.json                               |
| 8a  | **Build chunk index**             | Code  | build_chunk_index.py                      | Regenerate reverse index from map-model-spec.json                                                                             | —                      | —       