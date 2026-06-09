# Corrections log

Project: story-graph-ops (nodes.py)
Source: story_graph_ops/nodes.py — SubEpic, StoryGroup, Story from_dict; Epic.from_dict sub_epic loop

---

## Entry: null sequential_order crashes from_dict

- **Status:** confirmed
- **Context:** `SubEpic.from_dict`, `StoryGroup.from_dict`, `Story.from_dict`, and the sub-epic loop in `Epic.from_dict`
- **DO / DO NOT:** DO treat an explicit JSON `null` for `sequential_order` as `0.0` in every `from_dict` that calls `float(sequential_order)`. Use `val = data.get('sequential_order'); if val is None: val = 0.0` instead of `data.get('sequential_order', 0)` (the default only fires when the key is absent, not when it is present and null).
- **Example (wrong):**
  `SubEpic.from_dict` called `float(None)` when a sub-epic carried `"sequential_order": null` in the JSON, raising `TypeError: float() argument must be a string or a real number, not 'NoneType'`.
- **Example (correct):**
  All four sites (`SubEpic.from_dict`, `StoryGroup.from_dict`, `Story.from_dict`, sub-epic loop in `Epic.from_dict`) now coerce `None → 0.0` before passing to `float()`. Render completes successfully.
- **Likely source:** edge case

---
