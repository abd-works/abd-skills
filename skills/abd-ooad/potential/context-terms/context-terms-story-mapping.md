## Stage 1 — Context & evidence

### Your role

During this stage you will establish a **defensible evidence**, and an **evidence layout**

### What you must do

- **Set workspace** — Choose the active skill workspace, land `**solution.conf`** with `**context_path`**, chunking-spec pointer, and room for `**manifest_sources[]`** ([set-workspace](phases/set-workspace.md)). Evidence **file paths** are finalized in context markdown, not here.
- **Convert** sources to **canonical markdown** where needed ([context-markdown](phases/context-markdown.md)); record `**manifest_sources[]`** there.
- Create a **chunking spec** (AI draft + human-reviewed) aligned to how the sources are structured, when context-chunking-approach work is needed.
- **Chunk files** on disk match the index and the chunking spec.
- Assemble a **context package** (`context/*.md` chunk files + `context_index.json` + manifest; flat folder, no `chunks/` subfolder) that downstream work treats as **the** evidence layer, without ad hoc files or mystery sources.

**Important**: You do **not** introduce classes, properties,  inheritance or `interactions`here. You only **package and pin** evidence the later stages will cite by `chunk_id`. Until above are true, you **do not** start Stage 2. 


| #   | Phase                     | Summary                                                                                                                                                                     | Actor    | Phase automation                                                                                                                                                                                                                                                                                                            | Outputs                                                                                  | Ref                                                                                          |
| --- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 0   | Set workspace             | Active skill workspace + `solution.conf` with `context_path`, `context_chunking_spec` pointer, and `manifest_sources[]` slot; evidence paths finalized in context markdown. | Human    | **1.** `python` `[scripts/generate_prompt.py](../../scripts/generate_prompt.py)` `--phase set-workspace` **2.** `python` `[scripts/set_workspace.py](../../scripts/set_workspace.py)` — no args prints current; `<path>` sets `active_skill_workspace` in `skill-config.json` ([set-workspace](phases/set-workspace.md)) | `**solution.conf`** landed; workspace root known to `**scripts/_config.py`**             | [set-workspace](phases/set-workspace.md)                                                     |
| 1   | Context markdown          | Convert non-Markdown sources to canonical `.md`; record corpus in `manifest_sources[]` (`.md` paths + roles).                                                               | Code     | **1.** `python` `[scripts/generate_prompt.py](../../scripts/generate_prompt.py)` `--phase context-markdown` **2.** `python` `[scripts/convert_sources_to_markdown.py](../../scripts/convert_sources_to_markdown.py)` — `--file` or `--manifest` ([context-markdown](phases/context-markdown.md))                            | Canonical `**.md`** beside sources (or documented equivalent) + `**manifest_sources[]`** | [context-markdown](phases/context-markdown.md)                                               |
| 2   | Context chunking approach | Read `manifest_sources`, structural inventory, draft `context_chunking_spec`, disclose assumptions/gaps; human reviews spec before canonical context.                       | AI-led   | **1.** `python` `[scripts/generate_prompt.py](../../scripts/generate_prompt.py)` `--phase context-chunking-approach` **2.** Follow the emitted bundle (land `context_chunking_spec` YAML per [context-chunking-approach](phases/context-chunking-approach.md); human review before canonical context).                      | `**context_chunking_spec`** (reviewed)                                                   | [context-chunking-approach](phases/context-chunking-approach.md)                             |
| 3   | Canonical Context         | Chunks files, tag evidence type and modelling kind                                                                                                                          | Code-led | **1.** `python` `[scripts/generate_prompt.py](../../scripts/generate_prompt.py)` `--phase canonical-context` **2.** `python` `[scripts/build_context.py](../../scripts/build_context.py)` ([canonical-context](phases/canonical-context.md)); then contract scan / validate per bundle                                      | `context/*.md` + `context/context_index.json` / **v1** context package                   | [canonical-context](phases/canonical-context.md), [context-spec.md](library/context-spec.md) |


---

## Stage 2 — Vocabulary & behavior

### Your role

You separate **language** and **observable behavior** from **domain types**. You ground terms and mechanisms in **context chunks** (indexed by `context_index.json`). You write a **shaped** story map (who does what to which state) **before** you lock a sparse type system. Evidence and stories must lead type choices, not the reverse.

### What you must do

- **Terms & mechanisms.** You will consume `**context_index.json`** and context chunks. You will emit **terms**, **mechanisms**, and a **candidate queue** (possible types with rationale, still not promoted). `**scripts/build_terms_mechanisms_scaffold.py`** writes **empty** JSON scaffolds (`terms[]`, `mechanisms[]`, `candidates[]`) at the root of `**output_dir`** (e.g. `spec/`); it does **not** read chunks or fill vocabulary. **Authors** (human or AI) edit those files and **must** cite `chunk_id` on substantive rows per [terms-mechanisms-contract.md](library/terms-mechanisms-contract.md). **Mechanisms** use `**realized_by`** to point at **shaped story map** paths; **procedural `steps[]`** belong on **stories** in `shaped_story_map.json`, not duplicated inside `mechanisms.json`.
- **Shaped story map.** You will author `**phase3/shaped_story_map.json`** at the root of `**output_dir**` (see [shaped-story-map](phases/shaped-story-map.md)). Include trigger/response, anchor, `term_refs`, and `evidence_chunk_ids` where stories are substantive. Where a story **realizes** a named mechanism from Phase 2, add optional `**steps[]`**, `**realizes_mechanism**`, and `**mechanism_flow_order**` / `**mechanism_story**` per [shaped-story-map](library/shaped-story-map.md). Satisfy [shaped-story-shape](../../rules/shaped-story-shape.md) (automated check is **rule-bound** — see [Rules and automated checks](#rules-and-automated-checks) below). Details live in [terms-mechanisms](phases/terms-mechanisms.md) and [shaped-story-map](phases/shaped-story-map.md).

You do **not** put types in `concepts[]` yet.

### What you produce

- Shared **vocabulary** and **mechanism** artifacts tied to the corpus.
- A **candidate queue** for types (still not promoted).
- A **story map JSON** that reads as **capabilities and anchors**, not a type checklist.

### How you know you succeeded

Your terms-and-mechanisms artifacts trace back to `chunk_id`s. Your story map reads as **interaction capability**, not a list aligned to a future type catalog. Substantive stories tie to evidence where it matters. **Promotion** to domain types waits for Stage 3.


| #   | Phase                             | Summary                                                                                                                                                                                                                                                           | Actor  | Phase automation                                                                                                                                                                                                                                                                | Outputs                                                                    | Ref                                            |
| --- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------- |
| 4   | Terms & mechanisms (layers 1 & 2) | `**build_terms_mechanisms_scaffold.py`** emits **empty** schema shells; agent authors populate terms, mechanisms, and the candidate queue from context chunks with mandatory `chunk_id` citations per the contract. **Nothing** is promoted to `concepts[]` here. | AI-led | **1.** `python` `[scripts/generate_prompt.py](../../scripts/generate_prompt.py)` `--phase terms-mechanisms` **2.** `python` `[scripts/build_terms_mechanisms_scaffold.py](../../scripts/build_terms_mechanisms_scaffold.py)` (also via `build.py`); then author JSON per bundle | `<output_dir>/terms_layer.json`, `mechanisms.json`, `candidate_queue.json` | [terms-mechanisms](phases/terms-mechanisms.md) |
| 5   | Shaped story map                  | Agent authors shaped stories (trigger/response, anchors, evidence links). Outcome: JSON map of capabilities and interactions, not a type catalog.                                                                                                                 | AI-led | **1.** `python` `[scripts/generate_prompt.py](../../scripts/generate_prompt.py)` `--phase shaped-story-map` **2.** Author `shaped_story_map.json` under `**output_dir`** per [shaped-story-map](phases/shaped-story-map.md)                                                     | `shaped_story_map.json` (under `**output_dir**`, e.g. `spec/`)             | [shaped-story-map](phases/shaped-story-map.md) |


**Class diagram:** Phases **4–9** ship the [class-diagram-from-spec.md](library/class-diagram-from-spec.md) slice in `**generate_prompt`**. `**python scripts/build.py**` runs `**scripts/render_map_model_class_diagram.py**` after map-model relationship checks, writing `**<output_dir>/map-model-class-diagram.drawio**` next to `**map-model-spec.json**` (**mxfile** / **mxCell**; vendored `**scripts/map_model_spec_drawio.py`**). Optional `**class-diagram-layout-plan.json**` under `**output_dir**` drives logical cluster layout (see library slice). You can also run `**python scripts/render_map_model_class_diagram.py**` alone with `**--spec**` / `**--out**`. Open in diagrams.net / VS Code for human review—**Phase 10** validation remains the full `**build.py`** pipeline.

---
