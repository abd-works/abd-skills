---
catalog_garden_tier: practice
catalog_garden_order: 20
name: abd-ux-mockup
catalogue_one_liner: >-
  Lock down every control and interaction before visual design — so nothing is invented during build.
description: >-
  Specify exact controls, interactions, and states for IA screens as lo-fi Draw.io wireframes. Use when locking down interaction decisions before visual design or implementation.
context-perspective: ux
context-fidelity:
  - level: exploration
    mode: ux-mockup
---
# abd-ux-mockup

## Purpose

Lock down every control and interaction before visual design — so nothing is invented during build.

---

## Output file

**Deliverables folder:** see `../common/skill-rule-workflow.md` — Output file resolution.

**File names:** `<screen-slug>-state.json` (state source of truth), `<screen-slug>.drawio` (generated wireframe), `<screen-slug>.md` (structured spec). Output to `docs/ux/lo-fi/`.

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these common input traps:

- **Who decides and why** — who actually uses this control and what are they deciding — or are we picking a dropdown because it seems standard without knowing the decision being made?
- **Conditional states** — what happens when things go wrong — empty lists, validation failures, permission denials, partial data — have we decided what the user sees in each case?
- **Interaction weight** — which action on this screen is the one that matters most — and does our control hierarchy (primary, secondary, tertiary) reflect the user's actual priority?
- **Control choice rationale** — why this control type and not another — is a dropdown right when there are only two options, or a text field right when there are 200 valid values?
- **Selection consequences** — what happens immediately after the user acts — does selecting an item open a detail, update a list, enable actions — and is that feedback visible in the wireframe?

---

## Agent Instructions

Follow `../common/skill-rule-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what a lo-fi mockup is, source IA, design image reference, UI element types and state formats, field input types, domain terms and AC verbatim rules, the shape of a good state file, rendering approach (CLI vs AI-crafted XML), mxGraph XML patterns, and CLI reference.

### 2. Generate

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/lo-fi.md` | Structured spec: screen name, source paths, layout, design reference catalog, regions with affordance traces, in-scope stories, domain terms (verbatim), and AC (verbatim) |

**Generation flow:**

1. **Agree scope** — which screens, stories, or epics are in scope.
2. **Resolve inputs** — path to `docs/ux/initial-ia.md`, UL file, AC file, agreed screens/stories.
3. **Reference design images** — read ALL design images in `Design/` folders; catalog UX elements per screen.
4. **Read in-scope screens from the initial IA** — layout, regions, stories, domain terms.
5. **Collect in-scope stories and AC.**
6. **Build the state JSON** — map each IA region to the correct element type matching the design image.
7. **Generate the wireframe** via `scripts/drawio-mockup.mjs`.
8. **Write `lo-fi.md` alongside the wireframe.**
9. **Add story and domain term annotations** to the drawio.

**CLI invocation:**

```powershell
node "<skill-root>/scripts/drawio-mockup.mjs" `
  save `
  --state "docs/ux/lo-fi/<screen-slug>-state.json" `
  --out   "docs/ux/lo-fi/<screen-slug>.drawio"
```

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/skill-rule-workflow.md` § Validate output.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Region fidelity** — every wireframe region matches a region from the initial IA for this screen.
- **Labels verbatim** — every label is a UL term verbatim or copy from an AC clause.
- **AC verbatim** — every acceptance criterion for in-scope stories is present in `lo-fi.md`, character-for-character.
- **Screen-scoped** — no story or domain term from another screen appears.
- **Affordance traceability** — every affordance traces to an AC clause or a UL term.
- **State sync** — `<screen-slug>-state.json` and `<screen-slug>.drawio` are in sync.
- **Trees are trees** — hierarchical data uses `type: "tree"`, not `type: "list"`.
- **Listboxes are listboxes** — selectable item lists use `type: "listbox"`, not `type: "form"`.
- **Icon toolbars are icon toolbars** — icon button rows use `type: "toolbar-icons"`, not `type: "toolbar"`.
- **Context menus match the design** — grouped actions with shortcuts, not flattened button bars.
- **Story and domain term annotations present** — yellow stories box and green domain terms box beside each screen.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
