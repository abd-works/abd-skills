---
name: abd-thin-slicing
catalog_garden_tier: practice
catalog_garden_order: 20
catalogue_one_liner: >-
  Decide what to deliver first and why — so the team ships value in the smallest useful increments.
description: >-
  Produce thin-sliced delivery increments with priority order, outcomes, and story groupings. Use when planning releases or deciding what to deliver first after story mapping.
context-perspective: stories
context-role: support
context-fidelity:
  - level: discovery
    mode: slice-ordering
---
# abd-thin-slicing

## Purpose

Decide what to deliver first and why — so the team ships value in the smallest useful increments.

---

## Agent Instructions

Follow `common/skill-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — definitions of increments, thin slicing, and vertical vs horizontal slices.
- **`reference/examples.md`** — output shape examples and weak patterns to avoid.

### 2. Generate

**Produce the template:**

| Template | Produce |
| --- | --- |
| `templates/thin-slicing.md` | Increments: **name**, **outcome**, optional **slicing notes**, ordered **story** bullets (*italic* domain terms where helpful). Optional product/context at top. No template `## Instructions` in the deliverable. |

**New files under `templates/` later** → one deliverable per file.

**Workflow steps:**

1. **Read inputs** — story map / graph, PO or tech notes, known risks and dependencies.
2. **Mark spine vs optional** — mandatory core sequence vs alternates, enhancements, deep error paths (see `rules/map-sequential-spine-vs-optional-paths.md`).
3. **Cut vertical slices** — each increment is an **end-to-end** demonstrable path (even if manual/stubbed); avoid horizontal "finish epic A, then epic B."
4. **Name for value** — increment titles = stakeholder-visible **capability**, not phase or stack labels.
5. **Pull stories** — under each increment, list **verb-noun** stories in **flow order**; don't paste the whole map unless asked.

   > **Story names MUST be copied verbatim from `story-map.md` / `story-graph.json` — character-for-character, including every parenthetical qualifier.**
   > - `- Load FX Resource Catalog (FxRepo.data)` (correct — exact)
   > - `- Load FX Resource Catalog` (WRONG — trimmed; creates an orphan; scanner will catch this)
   > - `- System --> Load Crowd from Repository` (WRONG — actor prefix; parser stores "System" as the name)

6. **Write the template file** — fill **`templates/thin-slicing.md`** with the increments and stories (*italics* on domain terms where helpful).
7. **Omit maintainer noise** — do **not** copy the template's `## Instructions` block into project deliverables.

**Before:** `abd-story-mapping` — produces the story map this skill slices.
**After:** `abd-story-acceptance-criteria`, `abd-story-specification` — add story detail once priorities are set.

### 3. Validate

Run the story-name exact-match scanner first:

```bash
python skills/abd-thin-slicing/scanners/story-name-exact-match-scanner.py --workspace <path-to-project>
```

Exit code 1 means story name mismatches — **do not proceed until it passes**.

Run scanners and emit per-rule verdicts — see `common/skill-workflow.md` § Validate output and [`../../../reference/validate-checklist.md`](../../../reference/validate-checklist.md).

---

## Validate

Also apply [`../../../reference/validate-checklist.md`](../../../reference/validate-checklist.md).

- Each increment shows a vertical path (input → processing → outcome), not a layer.
- Increment names are stakeholder-visible capabilities, not internal milestones.
- Quality trade-offs are named ("Manual…" → "Automated…"), not hidden.
- Story names in `thin-slicing.md` are character-for-character identical to the source story map.

---
