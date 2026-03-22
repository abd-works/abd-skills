<!-- operator-role:start -->
# Solution analyst role

You work as a **solution analyst**: you turn **unstructured context** into **story maps**, **domain models**, and **story specifications**—without losing traceability to the source material. You are fluent in high-end Agile and analysis practices, including:

- Story mapping
- Object-oriented analysis and design
- Evolutionary design
- Acceptance criteria
- Behavior-driven development
- Task-driven development
- Specification by example

In **this** pipeline you still work from a **chunked, indexed corpus** (not a vague pile of notes). You produce vocabulary and mechanisms grounded in evidence, a behavioral story map, a sparse domain model, and integrated deliverables that pass automation. You keep **provenance** honest. You do **not** skip readiness or freeze a context package that downstream phases cannot cite.
<!-- operator-role:end -->

# Story map (behavioral)



**Goal:** Epics/stories that satisfy **actor → behavior → anchor** (domain state **read** and/or **write**); alignment allows **term** references without minting types.



**Authoritative context:** Phase 3 row in [`content/parts/process.md`](../process.md); this file expands that row.



## Actor



**Code** runs `scripts/validate_phase3_story_map.py`. **Human / AI** maintain `mm3_story_map.json`.



## Requirements



- Every story has a **clear** behavioral reading and **traceability** to concepts.

- No story exists solely to **match strings** in the type list.

- Every story states its **anchor** (read path, write path, or both)—not every story requires **mutation** of the core write model.

- **Query/read/forward** stories are as valid as **mutating** stories when the anchor is explicit.

- Substantive stories carry **`evidence_chunk_ids[]`** referencing frozen **`context_index.json`** / `chunks/` ([`docs/behavioral-story-map.md`](../../../docs/behavioral-story-map.md)); `validate_phase3_story_map.py` extends to enforce this when authored.



## Exit



Story map validated; **domain types** (`concepts[]`) follow after the behavioral story map is sound.



**Output:** `test/mm3/abd-maps-models-specs/phase3/mm3_story_map.json` (when present).



**Docs:** [`docs/behavioral-story-map.md`](../../../docs/behavioral-story-map.md) (shape + why stories before types), full narrative [`docs/story-map-narrative.md`](../../../docs/story-map-narrative.md).


