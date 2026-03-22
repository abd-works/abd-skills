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

# Terms & mechanisms (layers A & B)



**Goal:** Glossary and **named processes** exist **before** sparse `concepts[]`.



**Authoritative context:** Phase 2 row in [`content/parts/process.md`](../process.md); this file expands that row.



## Actor



**Code** runs `scripts/build_phase2_artifacts.py`. **Human / AI** curate terms and mechanisms.



## What this phase produces



- **Terms** — surface vocabulary + chunk links; not classes.

- **Mechanisms** — workflows/lifecycles with steps + evidence.

- **Candidate queue** — “possible type” with rationale; **not** in `concepts[]` yet.



## Exit



Promotion rule written: **candidate → concept** only through the **domain-types** gate (Phase 4)—not by renaming a mention or string co-occurrence.



**Outputs:** `test/mm3/abd-maps-models-specs/phase2/mm3_terms_layer.json`, `mm3_mechanisms.json`, `mm3_candidate_queue.json`.



**Implementation notes:** [`docs/terms-mechanisms-contract.md`](../../../docs/terms-mechanisms-contract.md) (includes **inputs** and **`chunk_id` citation** rules for Phase 2).


