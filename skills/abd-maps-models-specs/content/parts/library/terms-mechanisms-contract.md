# Terms & mechanisms contract

**Goal (Phase 2):** Glossary and **named processes** exist **before** sparse `concepts[]` (see [`content/parts/process.md`](../content/parts/process.md)).

## Artifacts (under `test/mm3/abd-maps-models-specs/phase2/`)

| File | Role |
|------|------|
| `mm3_terms_layer.json` | **Terms** — surface vocabulary + links to chunk IDs; not classes. |
| `mm3_mechanisms.json` | **Mechanisms** — named workflows/lifecycles with steps + evidence. |
| `mm3_candidate_queue.json` | **Candidate queue** — possible types with rationale; **not** in `concepts[]` until Phase 4 gate. |

## Exit criterion

Promotion rule is explicit: **candidate → concept** only through the **Phase 4** gate, not by renaming a mention.

## Automation

`scripts/build_phase2_artifacts.py` initializes or refreshes these files (reads Phase 0 metrics when present; populates layers when Phase 1 contract exists).

---

## Normative automation (Phase 2)

**Inputs:** Frozen **`context_index.json`** + **`chunks/`** from Phase 1 ([`context-package.md`](context-package.md)).

**Implementation expectations:**

- **Code** reads chunks + index; builds term list and mechanism sketches with **`chunk_id` refs on every extracted item**.
- **Optional:** LLM pass with a **checked-in** prompt template (e.g. `docs/prompts/phase2_terms.md`) for disambiguation; **must** output JSON that validates against **`phase2/v1`** and preserves/extends **`evidence_chunk_ids[]`**—not replace with prose.
- **Implementation:** Phase 2 logic lives in **`build_phase2_artifacts.py`**; emitted JSON validates against **`phase2/v1`** and preserves **`evidence_chunk_ids[]`** on every extracted item.

Schema: **`phase2/v1`** as emitted by current `build_phase2_artifacts.py` (extend in place when implementing).
