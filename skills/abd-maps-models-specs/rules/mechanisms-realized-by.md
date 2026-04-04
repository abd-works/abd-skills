---
rule_id: mechanisms-realized-by
---

## Mechanisms use `realized_by`; procedural steps live on stories

**Applies** when `mechanisms.json` is present under the workspace `output_dir` (e.g. `spec/`).

**Automation:** `scripts/scanners/mechanisms_contract.py` (this skill’s `build_pipeline`). Validates structure of `mechanisms[]` and, when `shaped_story_map.json` exists, checks that each `realized_by.paths[]` entry matches a story path in the map.

**DO**

- Give each mechanism **`name`**, **`description`**, **`evidence_chunk_ids[]`**, and **`realized_by`** with **`kind`** (`single_story` or `ordered_stories`), non-empty **`paths[]`**, and optional **`note`**.
- Put procedural **`steps[]`** on the **story** rows in `shaped_story_map.json`, not on mechanism objects.

```json
{
  "name": "RAG chat turn",
  "description": "...",
  "evidence_chunk_ids": ["blk_abc"],
  "realized_by": {
    "kind": "ordered_stories",
    "paths": [
      "Epic / Sub-epic / First story",
      "Epic / Sub-epic / Second story"
    ]
  }
}
```

**DO NOT**

- Add a **`steps`** or **`interaction_steps`** array on mechanism rows (use **`steps[]`** on stories in the shaped story map).

```json
{
  "name": "Bad",
  "steps": ["do this", "then that"]
}
```

- Omit **`realized_by`** on mechanisms that are meant to be realized in the map once stories exist.
