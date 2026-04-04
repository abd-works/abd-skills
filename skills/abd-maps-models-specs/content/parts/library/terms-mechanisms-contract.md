# Terms & mechanisms contract

**Goal:** Glossary and **named processes** exist **before** sparse `concepts[]` (see [`content/parts/process.md`](../content/parts/process.md)).

## Artifacts (at `<workspace>/<output_dir>/` root, e.g. `spec/`)

| File | Role |
|------|------|
| `terms_layer.json` | **Terms** — surface vocabulary + links to chunk IDs; not classes. |
| `mechanisms.json` | **Mechanisms** — named workflows/lifecycles: **description**, **`evidence_chunk_ids[]`**, and **`realized_by`** pointing at **shaped story map** paths. **Do not** duplicate procedural **`steps[]` here** — those belong on **stories** in `shaped_story_map.json` (see below). |
| `candidate_queue.json` | **Candidate queue** — possible types with rationale; **not** in `concepts[]` until the domain-types promotion gate. |

## Mechanisms and the shaped story map (normative)

**Procedural steps** for a named process live on **stories**, not as a parallel list inside `mechanisms[]`.

1. **Author or refine** the **shaped story map** so observable stories exist for the capability (see [`shaped-story-map.md`](shaped-story-map.md): **`steps[]`**, **`realizes_mechanism`**, **`mechanism_flow_order`**, **`mechanism_story`**).
2. **Each mechanism row** in `mechanisms.json` includes:
   - **`name`**, **`description`**, **`evidence_chunk_ids[]`** (substantive claims cite the corpus).
   - **`realized_by`** — how this mechanism is realized in the map, for example:
     - **`kind`**: `"single_story"` | `"ordered_stories"`
     - **`paths`**: strings of the form `"<Epic> / <Sub-epic> / <Story name>"` (must match `shaped_story_map.json` hierarchy).
     - **`note`** (optional): related stories or ordering hints.

Automation and authors **must not** add a top-level **`steps`** array on mechanism objects in `mechanisms.json` for new work; use **`steps[]` on the realizing story or stories** in `shaped_story_map.json` instead.

## Exit criterion

Promotion rule is explicit: **candidate → concept** only through the **domain types** gate, not by renaming a mention.

## Automation

`scripts/build_terms_mechanisms_scaffold.py` writes **empty** scaffolds for the three files above. It does **not** read chunks or populate rows.

---

## Candidate queue population contract

After terms and mechanisms are authored, the candidate queue **must** be populated by sweeping all evidence. This is not optional — the candidate queue feeds Phase 6 (domain-types) and every entry will receive an explicit decision in the promotion ledger.

### What goes into the candidate queue

Every **noun that holds state, makes a decision, is acted upon, or owns a boundary** extracted from:

1. **`context_index.json` chunk bodies** — read the actual `.md` chunk text, not just metadata. Extract entities from the natural language regardless of chunk form (narrative, API spec, transcript, rules, definitions, etc.).
2. **`mechanisms.json`** — every entity **named** in a mechanism `description` or `realized_by` path that is not already a term or candidate.
3. **`shaped_story_map.json`** — every `anchor`, entity in `trigger`/`response`, or concept referenced in `steps[]` that is not already a term or candidate.

### Required fields per candidate

| Field | Description |
|-------|-------------|
| `name` | The entity name |
| `source_chunks[]` | All chunk IDs where this entity appears |
| `extraction_rationale` | Why this entity might be a domain concept (what behavior or state it exhibits) |
| `modeling_kind_composition` | Breakdown of `modeling_kind` values from its source chunks (e.g. `{"rule": 3, "example": 1}`) |

### Completeness check

No entity that appears in a mechanism description or shaped story map anchor may be absent from **both** `terms_layer.json` and `candidate_queue.json` after this step. The mechanism-concept-coverage scanner enforces this at validation time.

### Deduplication

Candidates are deduplicated against existing `terms_layer.json` entries and previously extracted candidates. A term that is already in the glossary does not need a candidate entry unless there is evidence it should be promoted to a concept (in which case it gets a candidate entry with rationale explaining the promotion case).

---

## Normative automation (full extraction)

**Inputs:** **`context_index.json`** + chunk **`*.md`** in **`context_path`** from the canonical-context stage ([`context-spec.md`](context-spec.md)).

**Implementation expectations:**

- **Code** reads chunks + index; builds term list and mechanism sketches with **`chunk_id` refs on every extracted item**.
- **Mechanism extraction** should emit **`realized_by`** (or leave mechanisms empty until the shaped map exists) and **`steps[]` on stories** when generating both layers — **not** `steps` arrays inside `mechanisms.json`.
- **Optional:** LLM pass with a **checked-in** prompt template (e.g. `docs/prompts/terms_mechanisms.md`) for disambiguation; **must** output JSON that validates against **`terms_mechanisms_queue/v1`** and preserves/extends **`evidence_chunk_ids[]`**—not replace with prose.
- **Implementation:** Terms/mechanisms/candidate logic lives in tooling you add alongside **`build_terms_mechanisms_scaffold.py`**; emitted JSON validates against **`terms_mechanisms_queue/v1`** and preserves **`evidence_chunk_ids[]`** on every extracted item.

Schema: **`terms_mechanisms_queue/v1`** as emitted by current **`build_terms_mechanisms_scaffold.py`** (empty arrays) and extended when you implement extraction (extend in place when implementing).
