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

**MANDATORY bootstrap — no generation until complete.**

1. Read **`common/skill-workflow.md` in its entirety** and complete every step in § Read-gates (all of `rules/`, all of `reference/` including `input-traps.md`, practice files linked from this skill, and `common/grill-me-with-practice-skill.md` when grill mode is active).
2. Read **every file linked in § 1 below in full** — do not skim, summarize from memory, or skip.

Output resolution, validation, and diagram delegation are defined in `common/skill-workflow.md`.

### 1. Read context (MANDATORY — every linked file in full)

Read these files:
- **`reference/concepts.md`** — what story maps are, actors, personas, epics, stories, story types, pitfalls, gap recording, and depth levels.
- **`reference/examples.md`** — a worked example of a story map showing epics, sub-epics, and stories.
- **[`../../../reference/handling-incomplete-context.md`](../../../reference/handling-incomplete-context.md)** and **[`../../../reference/new-vs-existing-system.md`](../../../reference/new-vs-existing-system.md)** — shared gap and system-mode discipline.

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

Run scanners and emit per-rule verdicts — see `common/skill-workflow.md` § Validate output and [`../../../reference/validate-checklist.md`](../../../reference/validate-checklist.md).

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers. Also apply [`../../../reference/validate-checklist.md`](../../../reference/validate-checklist.md).

- **Hierarchy** — epics → sub-epics → stories; **verb—noun** names; actors only in `story_type`, not in titles.
- **Story size** — one observable behavior per story; flows grouped in sub-epics.
- **Intent** — outcomes and behaviors, not implementation tasks or internal structure.
- **Context gaps** — gaps recorded inline or in `## Context Gaps` section where context was absent.

---
