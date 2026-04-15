# Terms & mechanisms (layers A & B)

**Goal:** Glossary and **named processes** exist **before** sparse `concepts[]`.

**Normative for Phase 4:** this document. [`process.md`](../process.md) is pipeline **summary** only (table row)—not the procedure.

## Actor

**Code** runs `scripts/build_terms_mechanisms_scaffold.py`, which writes **empty** `terms[]`, `mechanisms[]`, and `candidates[]` JSON files (schema shells only). **Human / AI** author all substantive content and cite evidence per the contract.

## What this phase produces

- **Terms** — surface vocabulary + chunk links; not classes.

- **Mechanisms** — named workflows/lifecycles: **description**, **evidence**, and **`realized_by`** pointing at **shaped story map** paths. **Procedural `steps[]`** live on **stories** in `shaped_story_map.json`, not duplicated in `mechanisms.json` ([`terms-mechanisms-contract.md`](../library/terms-mechanisms-contract.md)).

- **Candidate queue** — "possible type" with rationale; **not** in `concepts[]` yet.

## Candidate extraction (mandatory)

After terms and mechanisms are authored, **sweep every evidence chunk** in `context_index.json` to populate `candidate_queue.json`. This is not optional — the candidate queue feeds the domain-types phase and must be comprehensive.

**Extraction procedure:**

1. For each chunk in `context_index.json`, read the chunk `.md` body text.

2. Extract every **noun that holds state, makes a decision, is acted upon, or owns a boundary** in the natural language of the evidence content. This is content-agnostic — chunks may be narrative, API spec, interview transcript, rules, definitions, or any other form.

3. Deduplicate against existing `terms_layer.json` entries and previously extracted candidates.

4. For each extracted entity, record in `candidate_queue.json`:
   - `name` — the entity name
   - `source_chunks[]` — all chunk IDs where this entity appears
   - `extraction_rationale` — why this entity might be a domain concept (what behavior or state it exhibits in the evidence)
   - `modeling_kind_composition` — the `modeling_kind` breakdown of its source chunks (e.g., `{"rule": 3, "example": 1}`)

5. Also extract candidates from `mechanisms.json` — every entity **named** in a mechanism description or `realized_by` path that is not yet a term or candidate.

6. Also extract candidates from `shaped_story_map.json` — every `anchor`, entity in `trigger`/`response`, or concept referenced in `steps[]` that is not yet a term or candidate.

**Completeness check:** No entity that appears in a mechanism description or shaped story map anchor should be absent from both `terms_layer.json` and `candidate_queue.json` after this step.

## Exit

Promotion rule written: **candidate → concept** only through the **domain-types** gate (Phase 6)—not by renaming a mention or string co-occurrence.

**Outputs:** `<workspace>/<output_dir>/terms_layer.json`, `mechanisms.json`, `candidate_queue.json`.

**Implementation notes:** [`terms-mechanisms-contract.md`](../library/terms-mechanisms-contract.md) (includes **inputs**, **`chunk_id` citation**, **mechanism ↔ story map** linkage, and **candidate queue population contract**).
