# Shaped story map



**Goal:** Epics/stories that satisfy **actor → behavior → anchor** (domain state **read** and/or **write**); alignment allows **term** references without minting types.



**Normative for Phase 3:** this document. [`process.md`](../process.md) is pipeline **summary** only (table row)—not the procedure.



## Actor



**Automated enforcement** is **rule-bound** ([shaped-story-shape](../../rules/shaped-story-shape.md), [scanners.json](../../rules/scanners.json)); it runs as part of **`python scripts/build.py`**. **Human / AI** maintain **`shaped_story_map.json`** at the root of **`output_dir`** (see [domain-model.md](../library/domain-model.md) → **`map-model-spec.json`** scaffold extensions).



## Requirements



- Every story has a **clear** behavioral reading and **traceability** to concepts.

- No story exists solely to **match strings** in the type list.

- Every story states its **anchor** (read path, write path, or both)—not every story requires **mutation** of the core write model.

- **Query/read/forward** stories are as valid as **mutating** stories when the anchor is explicit.

- Substantive stories carry **`evidence_chunk_ids[]`** referencing **`context_index.json`** and chunk `*.md` in **context_path** ([`shaped-story-map.md`](../library/shaped-story-map.md)); `phase3_story_map_evidence.py` enforces this for **`shaped_story_map.json`** when authored.

- When **mechanisms** exist in Phase 2, stories may **realize** them: optional **`steps[]`**, **`realizes_mechanism`**, **`mechanism_flow_order`**, **`mechanism_story`** ([`shaped-story-map.md`](../library/shaped-story-map.md)); **`mechanisms.json`** lists **`realized_by`** paths — no duplicate **`steps`** on mechanism rows.



## Exit



Story map validated; **domain types** (`concepts[]`) follow after the shaped story map is sound.



**Output:** `shaped_story_map.json` at the root of **`output_dir`** (e.g. `spec/shaped_story_map.json`).



**Docs:** [`shaped-story-map.md`](../library/shaped-story-map.md) (Phase 3 JSON shape + validators), [`story-map.md`](../library/story-map.md) (interaction tree prose + [why story mapping before domain types](../library/story-map.md#why-story-mapping-before-domain-types)).


