# Process — Maps-Models-Specs

Pipeline: Context → Discover → Classify → Deepen → Canonicalize → Evidence → Structure → Finalize.

**Core principle:** Discover taxonomy layer by layer, top-down, with evidence indexed as you go. Each step is a separate AI or code pass. Scanners enforce structure mechanically. AI resolves violations — scanners never propose fixes.

**Prerequisites:** Stage 1 — source documents (PDF, DOCX, PPTX, etc.). Stage 2+ — `context/context_index.json` and `context/chunks/*.md` from Stage 1.

**Two parallel artifacts produced at every step:**

- **Domain model** — modules, concepts, properties, operations (what things are and own)
- **Story map** — epics, sub-epics, stories, acceptance criteria, specifications, examples (what actors do and what changes)

These are two views of the same coin and must be produced simultaneously.

**Output files (single evolving document):**

- `map-model-spec.json` — forward index (Step 4 creates; Steps 5/5a classify; Step 6 deepens; Step 7 canonicalizes; Step 9 structures; Step 10 finalizes)
- `map-model-spec.md` — human-readable summary
- `mms-chunk-index.json` — reverse index (chunk_id → concepts, epics, stories, modules). **Code-only:** `build_chunk_index.py` reads map-model-spec.json and produces this derived artifact. Steps 4a, 6a, 7a run it after 4, 6, 7 whenever the spec changes. The AI steps do not invoke it — it is a separate step.

---

## Stage 1: Extract Context


| #   | Step        | Initiator    | Script                        | What it does                                                   | Coverage       | Ref                   | Outputs                         |
| --- | ----------- | ------------ | ----------------------------- | -------------------------------------------------------------- | -------------- | --------------------- | ------------------------------- |
| 1   | **Convert** | Human → Code | convert_to_markdown.py        | Source → markdown                                              | Creates corpus | [context](context.md) | markdown                        |
| 2   | **Analyze** | AI           | discover_context_structure.py | Analyze markdown → markers for headers, tables, sections, TOC, | —              | [context](context.md) | solution.conf                   |
| 3   | **Parse, curate, chunk, index** | Code | parse_and_curate.py | Parse → **curate** (classify, exclude) → chunk → index          | —              | [context](context.md) | chunks/*.md, context_index.json |

**Step 3 — curate is not a separate step.** The script parse_and_curate.py does all of: parse markdown to blocks; **curate** (classify evidence_type, assign document_region, exclude noise and out-of-scope sections); purpose-built chunking and merge; write chunks and context_index.json. Excluded blocks are listed in context_index.json under `excluded` and are not written to chunks.


---

## Stage 2: Map and Model (Steps 4–7)


| #   | Step                              | Actor | Script                                    | What it does                                                                                                                  | Coverage               | Ref                                                   | Outputs                                           |
| --- | --------------------------------- | ----- | ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------------- | ------------------------------------------------- |
| 4   | **Modules and Epics**             | AI    | —                                         | Orient on context taxonomy; discover module/epic pairs; sketch modules and concept classes; 2–3 story names per epic          | 30% sampled            | [modules-epics](modules-epics.md)                     | map-model-spec.json, map-model-spec.md            |
| 4a  | **Build chunk index**             | Code  | build_chunk_index.py                      | Regenerate reverse index from map-model-spec.json                                                                             | —                      | —                                                     | mms-chunk-index.json                              |
| 5   | **Concept Classification**        | AI    | classify_chunks.py (Pass 1)               | AI reads chunks (or configured %); extracts concepts and relationships                                                        | All chunks             | [concept-classification](concept-classification.md)   | map-model-spec.json                               |
| 5a  | **Concept Classification (code)** | Code  | classify_chunks.py (Pass 2); summarize.py | Code scans chunks; extracts concepts and relationships, merges gaps with AI pass; summarize.py → summary.md, relationships.md | All chunks             | [concept-classification](concept-classification.md)   | map-model-spec.json, summary.md, relationships.md |
| 6   | **Concept Classes and Stories**   | AI    | —                                         | Deepen classes/stories per module/epic; resolve [defer] tags                                                                  | Chunks per Module/Epic | [concept-classes-stories](concept-classes-stories.md) | map-model-spec.json                               |
| 6a  | **Build chunk index**             | Code  | build_chunk_index.py                      | Regenerate reverse index from map-model-spec.json                                                                             | —                      | —                                                     | mms-chunk-index.json                              |
| 7   | **Integrate and Harmonize**       | AI    | —                                         | Unify naming; wire cross-module; resolve [cross-cutting]; finalize subtypes                                                   | —                      | [integrate-harmonize](integrate-harmonize.md)         | map-model-spec.json                               |
| 7a  | **Build chunk index**             | Code  | build_chunk_index.py                      | Regenerate reverse index from map-model-spec.json                                                                             | —                      | —                                                     | mms-chunk-index.json                              |


---

## Stage 3: Specification


| #   | Step          | Actor | Script                | What it does                                                                   | Coverage   | Ref                       | Outputs             |
| --- | ------------- | ----- | --------------------- | ------------------------------------------------------------------------------ | ---------- | ------------------------- | ------------------- |
| 8   | **Evidence**  | Code  | TBD (not implemented) | Mine complete context for actions, decisions, states, relationships            | All chunks | [evidence](evidence.md)   | evidence/*.json     |
| 9   | **Structure** | AI    | —                     | Finalize Map & model and build steps, scenarios, examples from evidence        | —          | [structure](structure.md) | map-model-spec.json |
| 10  | **Finalize**  | AI    | —                     | Assign operations; link behaviors; split by subtype; fix anti-patterns; assess | —          | [finalize](finalize.md)   | map-model-spec.json |


---

## Config (solution modeler pattern)

**Skill config** `conf/abd-config.json` — one key:

- `solution_workspace` — path to workspace root (e.g. `mm3`). When set, all paths resolve relative to workspace.

**Workspace config** `<workspace>/solution.conf` — paths relative to workspace root:

- `output_dir` — where map-model-spec.json, evidence/, mms-chunk-index.json live (default: `solution` or e.g. `maps-models-specs`)
- `context_path` — where chunks/ and context_index.json live (default: `output_dir/context`)

When no workspace is configured, scripts fall back to skill root (flat layout).

## Workspace Layout

**With workspace (e.g. mm3):**

```
mm3/
├── solution.conf          # output_dir, context_path
├── maps-models-specs/     # output_dir
│   ├── summary.md        # from summarize.py (Step 5a)
│   ├── relationships.md  # from summarize.py (Step 5a)
│   ├── context/          # chunks/*.md, context_index.json
│   ├── generated/        # junk_config.json
│   ├── evidence/         # actions.json, decisions.json, ...
│   ├── map-model-spec.json
│   ├── map-model-spec.md
│   └── mms-chunk-index.json
```

**Flat (no workspace):**

```
abd-maps-models-specs/
├── conf/abd-config.json   # optional: solution_workspace
├── parts/, rules/, scripts/
├── context/               # chunks/*.md (content), context_index.json (metadata + indexes)
├── evidence/
├── map-model-spec.json
├── map-model-spec.md
└── mms-chunk-index.json
```

---

## Operational flow

Per-step details: [context](context.md), [modules-epics](modules-epics.md), [concept-classification](concept-classification.md), [concept-classes-stories](concept-classes-stories.md), [integrate-harmonize](integrate-harmonize.md), [evidence](evidence.md), [structure](structure.md), [finalize](finalize.md).


| Step | Actor        | Script                                    | Inputs                                    | Outputs                                           |
| ---- | ------------ | ----------------------------------------- | ----------------------------------------- | ------------------------------------------------- |
| 1    | Human → Code | convert_to_markdown.py                    | Source folder                             | markdown                                          |
| 2    | AI           | discover_context_structure.py             | markdown                                  | solution.conf                                     |
| 3    | Code         | parse_and_curate.py                       | markdown                                  | chunks/*.md, context_index.json                   |
| 4    | AI           | —                                         | context/                                  | map-model-spec.json                               |
| 4a   | Code         | build_chunk_index.py                      | map-model-spec.json                       | mms-chunk-index.json                              |
| 5    | AI           | classify_chunks.py (Pass 1)               | map-model-spec.json, context/             | map-model-spec.json                               |
| 5a   | Code         | classify_chunks.py (Pass 2); summarize.py | map-model-spec.json                       | map-model-spec.json, summary.md, relationships.md |
| 6    | AI           | —                                         | map-model-spec.json, context/             | map-model-spec.json                               |
| 6a   | Code         | build_chunk_index.py                      | map-model-spec.json                       | mms-chunk-index.json                              |
| 7    | AI           | —                                         | map-model-spec.json, mms-chunk-index.json | map-model-spec.json                               |
| 7a   | Code         | build_chunk_index.py                      | map-model-spec.json                       | mms-chunk-index.json                              |
| 8    | Code         | TBD (not implemented)                     | map-model-spec.json, context/             | evidence/*.json                                   |
| 9    | AI           | —                                         | map-model-spec.json, evidence/            | map-model-spec.json                               |
| 10   | AI           | —                                         | map-model-spec.json                       | map-model-spec.json                               |


### File dependency graph

```
source docs
       │
       ▼
   STAGE 1 (Code) — Steps 1–3
   convert → [discover_context_structure] → parse_and_curate
       │
       ▼
context_index.json + chunks/*.md
       │
       ├──────────────────────────────────────────────────────────────────┐
       │                                                                   │
       ▼                                                                   ▼
   STEP 4 (AI)                                                    STEP 5 (AI)
   Shape modules/epics                                            classify_chunks Pass 1
   samples 30%                                                            │
       │                                                                   │
       ▼                                                                   ▼
map-model-spec.json ◄───────────────────────────────────────────── STEP 5a (Code)
       │                    (writes evidence directly)                    classify_chunks Pass 2 + summarize
       │                                                                   │
       ├──────────────────────────────────────────────────────────────────▼
       │                                              summary.md, relationships.md
       │                                                                   │
       ▼                                                                   ▼
                                                                    STEP 6 (AI)
                                                                    Concept classes and stories
       │                                                                   │
       │                                                                   ▼
       │                                              map-model-spec.json (deepened)
       │                                                                   │
       │                                                                   ▼
       │                                                      build_chunk_index.py
       │                                                                   │
       │                                                                   ▼
       │                                                      mms-chunk-index.json
       │                                                                   │
       │                                                                   ▼
       │                                                         STEP 7 (AI)
       │                                                         Integrate and harmonize
       │                                                                   │
       │                                                                   ▼
       │                                              map-model-spec.json (canonical)
       │                                                                   │
       │                                                                   ├─────────────────────┐
       │                                                                   │                     │
       │                                                                   ▼                     ▼
       │                                                         STEP 8 (Code)            build_chunk_index.py
       │                                                         evidence extraction            │
       │                                                                   │                     ▼
       │                                                                   ▼              mms-chunk-index.json
       │                                                                   │
       │                                                                   ▼
       │                                                         STEP 9 (AI)
       │                                                         Structure
       │                                                                   │
       │                                                                   ▼
       │                                                         STEP 10 (AI)
       │                                                         Finalize
       │                                                                   │
       │                                                                   ▼
       │                                              map-model-spec.json (final)
```

