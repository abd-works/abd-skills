# Terms & mechanisms (layers A & B)



**Goal:** Glossary and **named processes** exist **before** sparse `concepts[]`.



**Normative for Phase 2:** this document. [`process.md`](../process.md) is pipeline **summary** only (table row)—not the procedure.



## Actor



**Code** runs `scripts/build_phase2_artifacts.py`, which writes **empty** `terms[]`, `mechanisms[]`, and `candidates[]` JSON files (schema shells only). **Human / AI** author all substantive content and cite evidence per the contract.



## What this phase produces



- **Terms** — surface vocabulary + chunk links; not classes.

- **Mechanisms** — workflows/lifecycles with steps + evidence.

- **Candidate queue** — “possible type” with rationale; **not** in `concepts[]` yet.



## Exit



Promotion rule written: **candidate → concept** only through the **domain-types** gate (Phase 4)—not by renaming a mention or string co-occurrence.



**Outputs:** `<workspace>/<output_dir>/phase2/terms_layer.json`, `mechanisms.json`, `candidate_queue.json`.



**Implementation notes:** [`terms-mechanisms-contract.md`](../library/terms-mechanisms-contract.md) (includes **inputs** and **`chunk_id` citation** rules for Phase 2).


