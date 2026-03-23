---
rule_id: shaped-story-shape
---

## Shaped story map: stories are observable, not labels

**Artifact:** `phase3/shaped_story_map.json` (paths per [`shaped-story-map.md`](../content/parts/library/shaped-story-map.md)).

Each **story** must have a clear **anchor**: what state or projection is read, written, forwarded, or queried—**silence is not allowed** for substantive stories. In JSON, **trigger** and **response** are each `{ "actor", "behavior" }` only—no separate Triggering-State / Resulting-State fields; state belongs in **behavior** text and **Examples** tables. Where the story is substantive, **`evidence_chunk_ids[]`** is non-empty and validates against the Phase 1 index.

Where your narrative uses **Trigger** / **Response** (or When/Then on steps), they must describe **observable** interaction—not implementation trivia. This skill does **not** require a legacy DrawIO export; it requires **JSON + validation** that matches the **shaped story map** contract.

An **epic** without **stories** is incomplete for this phase—epics exist to group **confirming stories** for the shaped map, not to park vague themes.

**DO**

- Name stories as **observable behavior**; tie substantive claims to **`evidence_chunk_ids[]`** that resolve in **`context_index.json`**.
- Keep **trigger** / **response** at the **interaction** level (actor + behavior each), not internal method names.

```json
{
  "name": "Customer submits order",
  "anchor": "Order aggregate persisted and acknowledged",
  "trigger": {
    "actor": "Customer",
    "behavior": "Confirms checkout"
  },
  "response": {
    "actor": "System",
    "behavior": "Records order and returns confirmation id"
  },
  "evidence_chunk_ids": ["chunk-orders-04"]
}
```

**DON'T**

- Use placeholder story names with no actor, no anchor, and empty evidence while claiming domain truth.

```json
{
  "name": "Data layer",
  "evidence_chunk_ids": []
}
```

“Data layer” is a label, not a story in the shaped map—**violation** when the story is treated as substantive.
