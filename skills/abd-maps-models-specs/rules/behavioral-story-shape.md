---
rule_id: behavioral-story-shape
phase_files:
  - story-map.md
---

## Stories are behavioral, not labels

**Artifact:** `phase3/mm3_story_map.json` (paths per [`behavioral-story-map.md`](../content/parts/library/behavioral-story-map.md)).

Each **story** must have a clear **anchor**: what state or projection is read, written, forwarded, or queried—**silence is not allowed** for substantive stories. **Actor** (primary) and **behavior** language match the pipeline’s **interaction** framing. Where the story is substantive, **`evidence_chunk_ids[]`** is non-empty and validates against the Phase 1 index.

Where your narrative uses **trigger** and **response** (or When/Then elsewhere), they must describe **observable** interaction—not implementation trivia. This skill does **not** require a legacy DrawIO export; it requires **JSON + validation** that matches the behavioral contract.

An **epic** without **stories** is incomplete for this phase—epics exist to group **confirming behavioral stories**, not to park vague themes.

**DO**

- Name stories as **observable behavior**; tie substantive claims to **`evidence_chunk_ids[]`** that resolve in the frozen index.
- Keep trigger/response (or equivalent) at the **interaction** level, not internal method names.

```json
{
  "name": "Customer submits order",
  "actor": "Customer",
  "anchor": "Order aggregate persisted and acknowledged",
  "evidence_chunk_ids": ["chunk-orders-04"],
  "trigger": "Customer confirms checkout",
  "response": "System records order and returns confirmation id"
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

“Data layer” is a label, not a behavioral story—violation when the story is treated as substantive.
