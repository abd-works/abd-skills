---
rule_id: integrate-coherence
phase_files:
  - integrate.md
---

## Integrate: one coherent map, model, and spec

**Phase 7** in [`content/parts/process.md`](../content/parts/process.md).

You merge parallel work so **terms**, **story map**, and **promoted types** **tell one story**. The candidate queue is **drained** with explicit **close** or **defer** decisions—no silent orphans.

“Cross-cutting” concerns (policies, shared mechanisms) must be **resolved** into owned homes—either a **concept**, an **explicit** policy attachment, or a **documented** deferral. Unowned cross-cutting text is **debt**, not integration.

Story map references to concepts (or your binding convention) must **resolve** to concepts that exist in the domain model for the integrated slice.

Older “cross-cutting resolved” rules assumed a different artifact layout. This rule states the **same intent** for **this** skill’s integrate phase only.

**DO**

- Close or defer every candidate-queue item in writing; align story map names to **`concepts[]`** after synonym merges.

```json
{
  "candidate_queue": [
    { "name": "OrderTotal", "decision": "merged", "into": "Pricing" }
  ],
  "story_map_references": ["Pricing"]
}
```

**DON'T**

- Leave story map references to concept names that were **deleted** from `concepts[]`, or keep **three synonyms** for the same capability with no merge decision.

```json
{
  "story": "Uses OrderTotal for display",
  "concepts": [{ "name": "Pricing" }]
}
```

`OrderTotal` missing from model after merge—**violation** (broken alignment).
