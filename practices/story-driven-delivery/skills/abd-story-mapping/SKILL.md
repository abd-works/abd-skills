---
name: abd-story-mapping
catalog_garden_tier: practice
catalog_garden_order: 10
catalogue_one_liner: >-
  Give product, delivery, and domain people one shared picture of scope — outcomes and behaviors, not tasks.
description: >-
  Produce a Patton-style story map — epics, sub-epics, and stories named verb-noun. Use when decomposing user journeys into a hierarchical backlog structure.
context-perspective: stories
context-fidelity:
  - level: shaping
    mode: outline
  - level: discovery
    mode: full
---
# abd-story-mapping

## Purpose

Give product, delivery, and domain people one shared picture of scope — outcomes and behaviors, not tasks — so everyone argues from the same map.

---

## Agent Instructions

**MANDATORY:** Read **`common/skill-workflow.md` in its entirety** and complete § Read-gates before generating.

### 1. Generate

| Template | What to produce |
| --- | --- |
| `templates/story-map.md` | The epic/sub-epic/story tree using that layout. Optional title or short context above the tree is fine. |

**Depth:** Respect the depth level the user asks for (see `reference/concepts.md` **Depth levels**). At **Story Map Outline**, produce epics with confirming stories; do not apply the full rule set. At **Level 2+**, apply the full hierarchy and rules. Default to Level 2 when the user does not specify.

**Consistency:** Connectors (`or`, `opt`), nested `(AC)` lines, and actor/story lines must be complete and consistent throughout the `.md` artifact. Generated artifacts contain **only** the map; notation rules stay in this skill and in `templates/story-map.md`.

**Quality bar:** Match the naming and layout expectations in `reference/concepts.md` (verb-noun, actor in `story_type` not in name, stories are behaviors not tasks).

### 2. Validate

See `common/skill-workflow.md` § Validate output.

---

## Validate

- **Hierarchy** — epics → sub-epics → stories; **verb—noun** names; actors only in `story_type`, not in titles.
- **Story size** — one observable behavior per story; flows grouped in sub-epics.
- **Intent** — outcomes and behaviors, not implementation tasks or internal structure.
- **Context gaps** — gaps recorded inline or in `## Context Gaps` section where context was absent.

---
