---
name: abd-story-mapping
catalog_garden_tier: practice
catalog_garden_order: 10
catalogue_one_liner: >-
  Patton-style story maps (epics, stories, verb-noun naming); writes story-map templates from sources.
description: >-
  Produces Patton-style story maps — epics, sub-epics, stories, verb—noun naming, and actors.
  Use when structuring product discovery, decomposing user journeys, identifying epics and flows,
  story mapping, organizing requirements into a hierarchical map, or when the user mentions
  story maps, epics, sub-epics, or Jeff Patton—style backlog structure.
---
# abd-story-mapping

## Purpose

Build a **Patton-style story map** per scope from source material — a **single shared picture** of the product as epics (broad capability areas), sub-epics (flows or feature areas), and stories (one observable user or system interaction each). Decompose requirements into **outcomes and behaviors**, not build tasks or source dumps, so product, delivery, and domain people share one structure. Name every epic, sub-epic, and story **verb—noun**; carry **who** acts in `story_type`, not in the title. Record context gaps inline where source material is thin.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** `story-map.md`. Add a `<name>-` prefix only when disambiguation is needed.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what story maps are, actors, personas, epics, stories, story types, pitfalls, gap recording, and depth levels.
- **`reference/examples.md`** — a worked example of a story map showing epics, sub-epics, and stories.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

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

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-story-mapping \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Hierarchy** — epics → sub-epics → stories; **verb—noun** names; actors only in `story_type`, not in titles.
- **Story size** — one observable behavior per story; flows grouped in sub-epics.
- **Intent** — outcomes and behaviors, not implementation tasks or internal structure.
- **Context gaps** — gaps recorded inline or in `## Context Gaps` section where context was absent.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
