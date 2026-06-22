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

## Output file

**Deliverables folder:** see `../common/skill-rule-workflow.md` — Output file resolution.

**File name:** `story-map.md`. Add a `<name>-` prefix only when disambiguation is needed.

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these common input traps:

- **Hidden actors** — who actually uses this — is "the user" hiding three different people with different goals, or is there a system actor nobody mentioned?
- **Behaviors vs. tasks** — are these outcomes people care about, or build tasks disguised as stories? "Implement payment gateway" is a task; "Process customer payment" is a behavior. Which are we looking at?
- **Missing triggers** — are there background processes, scheduled jobs, or external systems that kick off behaviors nobody has surfaced yet? They always show up later as gaps.
- **Scope bleeding** — where does this product's responsibility end and another system's begin? If that boundary isn't drawn, stories will leak across it.
- **Depth agreement** — does everyone expect the same level of detail from this map — an outline to frame conversations, or a full breakdown to plan work? Mismatched expectations waste everyone's time.

---

## Agent Instructions

Follow `../common/skill-rule-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what story maps are, actors, personas, epics, stories, story types, pitfalls, gap recording, and depth levels.
- **`reference/examples.md`** — a worked example of a story map showing epics, sub-epics, and stories.

### 2. Generate

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/story-map.md` | The epic/sub-epic/story tree using that layout. Optional title or short context above the tree is fine. **Do not** paste the template's notation / `## Instructions` section into generated project files. |

**New files under `templates/` later** → one deliverable per file.

**Depth:** Respect the depth level the user asks for (see `reference/concepts.md` **Depth levels**). At **Story Map Outline**, produce epics with confirming stories; do not apply the full rule set. At **Level 2+**, apply the full hierarchy and rules. Default to Level 2 when the user does not specify.

**Consistency:** Connectors (`or`, `opt`), nested `(AC)` lines, and actor/story lines must be complete and consistent throughout the `.md` artifact. Generated artifacts contain **only** the map; notation rules stay in this skill and in `templates/story-map.md`.

**Quality bar:** Match the naming and layout expectations in `reference/concepts.md` (verb-noun, actor in `story_type` not in name, stories are behaviors not tasks).

**Where it lives:** Write `story-map.md` alongside the other engagement deliverables for this scope.


### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/skill-rule-workflow.md` § Validate output.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Hierarchy** — epics → sub-epics → stories; **verb—noun** names; actors only in `story_type`, not in titles.
- **Story size** — one observable behavior per story; flows grouped in sub-epics.
- **Intent** — outcomes and behaviors, not implementation tasks or internal structure.
- **Context gaps** — gaps recorded inline or in `## Context Gaps` section where context was absent.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
