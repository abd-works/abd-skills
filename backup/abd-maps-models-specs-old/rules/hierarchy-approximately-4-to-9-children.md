---
rule_id: hierarchy-approximately-4-to-9-children
phases: [step1]
order: 30
scanner: scripts/scanners/hierarchy_sizing.py
impact: MEDIUM
---

## Epic tree sizing (4–9 children per level)

The story map should be navigable: neither a flat pile nor an over-nested hairball. Target roughly **4–9** children at each level (`epic.sub_epics`, `sub_epic.stories`, or `epic.stories` when there are no sub-epics).

The scanner (`scripts/scanners/hierarchy_sizing.py`) warns when a node has fewer than 4 or more than 9 children. It does not block the pipeline — judgment belongs to assessment.

**DO** group related stories under sub-epics so each level stays in range.

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Retail", "concepts": [] },
      "epic": {
        "name": "Retail checkout",
        "sub_epics": [
          {
            "name": "Cart and pricing",
            "stories": [
              { "name": "Add line", "trigger": "…", "response": "…" },
              { "name": "Apply promo", "trigger": "…", "response": "…" },
              { "name": "Recalculate tax", "trigger": "…", "response": "…" },
              { "name": "Hold for manager", "trigger": "…", "response": "…" }
            ]
          },
          {
            "name": "Payment capture",
            "stories": [
              { "name": "Card auth", "trigger": "…", "response": "…" },
              { "name": "Partial auth", "trigger": "…", "response": "…" },
              { "name": "Decline path", "trigger": "…", "response": "…" },
              { "name": "Receipt", "trigger": "…", "response": "…" }
            ]
          }
        ]
      }
    }
  ]
}
```

**DO NOT** put twenty-five sibling stories directly under one epic with no sub-epics.

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Fulfillment", "concepts": [] },
      "epic": {
        "name": "Order fulfillment",
        "stories": [
          { "name": "Story 01", "trigger": "…", "response": "…" },
          { "name": "Story 02", "trigger": "…", "response": "…" },
          { "name": "Story 03", "trigger": "…", "response": "…" },
          { "name": "Story 04", "trigger": "…", "response": "…" },
          { "name": "Story 05", "trigger": "…", "response": "…" },
          { "name": "Story 06", "trigger": "…", "response": "…" },
          { "name": "Story 07", "trigger": "…", "response": "…" },
          { "name": "Story 08", "trigger": "…", "response": "…" },
          { "name": "Story 09", "trigger": "…", "response": "…" },
          { "name": "Story 10", "trigger": "…", "response": "…" },
          { "name": "Story 11", "trigger": "…", "response": "…" },
          { "name": "Story 12", "trigger": "…", "response": "…" }
        ]
      }
    }
  ]
}
```

Twelve direct children — scanner warns (too wide).

**DO NOT** nest single-child chains (`A → B → C` each with one child) unless the corpus truly decomposes that way — flatten or merge.

```json
{
  "modules_and_epics": [
    {
      "module": { "name": "Example", "concepts": [] },
      "epic": {
        "name": "Level A",
        "sub_epics": [
          {
            "name": "Level B",
            "sub_epics": [
              {
                "name": "Level C",
                "stories": [{ "name": "Only story", "trigger": "…", "response": "…" }]
              }
            ]
          }
        ]
      }
    }
  ]
}
```

Deep single-child chain — scanner warns.
