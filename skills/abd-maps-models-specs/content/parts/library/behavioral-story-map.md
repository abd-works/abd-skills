# Behavioral story map

**Goal:** Epics and stories satisfy **actor → behavior → anchor** (domain state read and/or write, or observable query/read path).

## Artifact

`test/mm3/abd-maps-models-specs/phase3/mm3_story_map.json`

## Shape (minimal contract)

- **`schema_version`**
- **`epics[]`** — each epic has a name and **`stories[]`**
- Each **story** includes at minimum:
  - **`name`**
  - **`anchor`** — what state/projection is read, passed, forwarded, written, or which constraint applies (no silent stories)
  - **`actor`** (primary) and optional **`behavior`** (operation language)
  - **`term_refs`** / evidence chunk IDs where applicable

Stories must **not** exist solely to match strings in a type list.

## Validation

```bash
python scripts/validate_phase3_story_map.py
```

## Why behavioral stories before domain types (Phase 3 before Phase 4)

This pipeline orders **behavioral** work (the story map) before **sparse domain types** (`concepts[]`).

**Reason:** If types land first, epics and stories get **pulled toward nouns that already exist in `concepts[]`**, and alignment rules reward **surface string match** between story text and type names. That **amplifies noun explosion** and confuses **documentation artifacts** with **stateful domain types**.

**Story-first** forces each slice of value to be stated as **actor → behavior → anchor** (what state is read, written, or queried). Types are then promoted only where the **story map and evidence** justify **distinct** behavioral contracts—not because a word appeared in a heading.

**Read vs write:** A story may be anchored on **observation** or **query** only; mutation is not required. That matches the **behavioral description of value** principle in [`principles-and-rules.md`](principles-and-rules.md).

See also: [`pipeline_invariants.md`](pipeline_invariants.md) (layers A–D).

---

## Normative automation (Phase 3)

**File:** `phase3/mm3_story_map.json` (under `OUT_ROOT / phase3/`).

**Validator:** Extend **`validate_phase3_story_map.py`** as needed.

**Normative fields:**

- Top-level `epics[]` with nested sub-epics / stories per project convention.
- Each **story** (where applicable):
  - `anchor` — behavioral anchor (read/write/query as per process).
  - `term_refs[]` — optional strings referencing Phase 2 terms.
  - `evidence_chunk_ids[]` — **required** for substantive stories (min one id that exists in the Phase 1 index).

Validator loads **`CONTEXT_INDEX`** and checks every `evidence_chunk_ids[]` exists in `blocks[]`.
