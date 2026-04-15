# Shaped story map



**Goal:** Epics/stories that satisfy **actor → behavior → anchor** (domain state **read** and/or **write**); alignment allows **term** references without minting types.



**Normative for Phase 3:** this document. [`process.md`](../process.md) is pipeline **summary** only (table row)—not the procedure.



## Actor



**Automated enforcement** is **rule-bound** ([shaped-story-shape](../../rules/shaped-story-shape.md), [scanners.json](../../rules/scanners.json)); it runs as part of **`python scripts/build.py`**. **Human / AI** maintain `shaped_story_map.json`.



## Requirements



- Every story has a **clear** behavioral reading and **traceability** to concepts.

- No story exists solely to **match strings** in the type list.

- Every story states its **anchor** (read path, write path, or both)—not every story requires **mutation** of the core write model.

- **Query/read/forward** stories are as valid as **mutating** stories when the anchor is explicit.

- Substantive stories carry **`evidence_chunk_ids[]`** referencing **`context_index.json`** and chunk `*.md` in **context_path** ([`shaped-story-map.md`](../library/shaped-story-map.md)); `phase3_story_map_evidence.py` extends to enforce this when authored.



## Exit



Story map validated; **domain types** (`concepts[]`) follow after the shaped story map is sound.



**Output:** `phase3/shaped_story_map.json` under the workspace output root (when present).



**Docs:** [`shaped-story-map.md`](../library/shaped-story-map.md) (Phase 3 JSON shape + validators), [`story-map.md`](../library/story-map.md) (interaction tree prose + [why story mapping before domain types](../library/story-map.md#why-story-mapping-before-domain-types)).


