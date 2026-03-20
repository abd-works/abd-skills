---
title: Hierarchy — Approximately 4 to 9 Children
impact: MEDIUM
tags: [step2, step3, step5, step6, hierarchy, epic, story]
scanner: scanners/hierarchy_sizing.py
---

## Keep Child Count in 4–9 Range

Any node (epic, sub-epic, story) has approximately 4–9 children. Does not apply to steps. For stories, count **steps** as children (not scenarios).

**DO** keep child count in the 4–9 range for manageable granularity.
- Epic: ~4–9 sub-epics or stories.
- Sub-epic: ~4–9 stories.
- Story: ~4–9 steps (total across scenarios).

**DO NOT** create nodes with many more than 9 children — split or regroup.
- Wrong: Epic with 15 stories (split into sub-epics).
- Wrong: Story with 12 steps (consider splitting story or grouping steps into scenarios).

Note: At Step 2, we allow 2–3 children for epics that are still being built out. Flag only when count exceeds 9.
