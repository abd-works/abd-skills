---
catalog_garden_tier: practice
catalog_garden_order: 20
name: abd-ux-mockup
catalogue_one_liner: >-
  Lock down every control and interaction before visual design — so nothing is invented during build.
description: >-
  Specify exact controls, interactions, and states for IA screens as Draw.io wireframes. Use when locking down interaction decisions before visual design or implementation.
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

**Deliverables folder:** see `../common/reference/skill-workflow.md` — Output file resolution.

**File names:** `<screen-slug>.aria.yaml` (detailed ARIA spec), `<screen-slug>-state.json` (state source of truth), `<screen-slug>.drawio` (generated wireframe), `<screen-slug>.md` (structured spec). Output to `docs/ux/mockup/screens/`; shared state in `docs/ux/mockup/state.json`. See [`common/reference/folder-conventions.md`](../../../../common/reference/folder-conventions.md).

---

## Grill prompts

Read `common/reference/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these common input traps:

- **Who decides and why** — who actually uses this control and what are they deciding — or are we picking a dropdown because it seems standard without knowing the decision being made?
- **Conditional states** — what happens when things go wrong — empty lists, validation failures, permission denials, partial data — have we decided what the user sees in each case?
- **Interaction weight** — which action on this screen is the one that matters most — and does our control hierarchy (primary, secondary, tertiary) reflect the user's actual priority?
- **Control choice rationale** — why this control type and not another — is a dropdown right when there are only two options, or a text field right when there are 200 valid values?
- **Selection consequences** — what happens immediately after the user acts — does selecting an item open a detail, update a list, enable actions — and is that feedback visible in the wireframe?

---

## Diagram workflow

Produces `docs/ux/mockups/<screen-slug>.drawio` from the state JSON. Must exist on disk before the cell is marked done.

```powershell
node "<skill-root>/scripts/drawio-mockup.mjs" `
  save `
  --state "docs/ux/mockups/<screen-slug>-state.json" `
  --out   "docs/ux/mockups/<screen-slug>.drawio"
```

Run once per screen in scope after `<screen-slug>-state.json` is written. To regenerate, re-run the same command — the state JSON is the source of truth.

---

## Agent Instructions

Follow `../common/reference/skill-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files in full before generating. Do not skip any file.

- **`reference/concepts.md`** — what a mockup is, source IA, design image reference, UI element types and state formats, field input types, domain terms and AC verbatim rules, the shape of a good state file, rendering approach (CLI vs AI-crafted XML), mxGraph XML patterns, and CLI reference.
- **`reference/aria-pipeline.md`** — ARIA fidelity model, input resolution (IA → mockup), promotion rules (structural → detailed), `aria.yaml` output format, and two-pass rendering protocol.

### 2. Generate

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/ux-mockup.md` | Structured spec: screen name, source paths, layout, design reference catalog, regions with affordance traces, in-scope stories, domain terms (verbatim), and AC (verbatim) |

**Generation flow:**

**Input resolution (before step 1):** Check whether `docs/ux/ia/<screen-slug>.aria.yaml` exists for the in-scope screen. If found, use as the structural base and promote to detailed fidelity per `reference/aria-pipeline.md`. If not, construct the detailed tree from `initial-ia.md` and the design image catalog.

1. **Agree scope** — which screens, stories, or epics are in scope.
2. **Resolve inputs** — path to `docs/ux/initial-ia.md`, UL file, AC file, agreed screens/stories.
3. **Reference design images** — read ALL design images in `Design/` folders; catalog UX elements per screen.
4. **Read in-scope screens from the initial IA** — layout, regions, stories, domain terms.
5. **Collect in-scope stories and AC.**
6. **Write `docs/ux/mockups/<screen-slug>.aria.yaml`** — promote the structural ARIA tree (or construct from IA) to detailed fidelity using the promotion rules in `reference/aria-pipeline.md`. Every control must have exact type, all live states, and required relationship attributes.
7. **Build the state JSON** — derive `<screen-slug>-state.json` from the detailed `aria.yaml`, mapping each ARIA node to the correct element type matching the design image.
8. **Pass 1 — Render wireframe:** Generate the wireframe via `scripts/drawio-mockup.mjs` driven from the state JSON. Save.
9. **Write `mockup.md` alongside the wireframe** — under each screen heading list:
   - **Stories:** every in-scope user and system story for that screen, verbatim from the story map (`(U)` / `(S)` prefix · Epic → Story title)
   - **Domain terms:** every domain term visible on that screen, verbatim from the Domain Language file, as a `·`-separated inline list
   - **AC:** every acceptance criterion for in-scope stories, verbatim.
10. **Pass 2 — Annotate:** Add yellow stories box and green domain terms box beside each screen in the drawio. No wireframe layout changes in this pass. Save.

**CLI invocation:**

```powershell
node "<skill-root>/scripts/drawio-mockup.mjs" `
  save `
  --state "docs/ux/mockups/<screen-slug>-state.json" `
  --out   "docs/ux/mockups/<screen-slug>.drawio"
```

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/reference/skill-workflow.md` § Validate output.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **Diagram exists** — `<screen-slug>.drawio` is on disk before the cell is marked done. The markdown spec alone is not a complete deliverable. (`rules/diagram-is-required-deliverable.md`)
- **Region fidelity** — every wireframe region matches a region from the initial IA for this screen.
- **Labels verbatim** — every label is a UL term verbatim or copy from an AC clause.
- **AC verbatim** — every acceptance criterion for in-scope stories is present in `mockup.md`, character-for-character.
- **Screen-scoped** — no story or domain term from another screen appears.
- **Affordance traceability** — every affordance traces to an AC clause or a UL term.
- **State sync** — `<screen-slug>-state.json` and `<screen-slug>.drawio` are in sync.
- **Trees are trees** — hierarchical data uses `type: "tree"`, not `type: "list"`.
- **Listboxes are listboxes** — selectable item lists use `type: "listbox"`, not `type: "form"`.
- **Icon toolbars are icon toolbars** — icon button rows use `type: "toolbar-icons"`, not `type: "toolbar"`.
- **Context menus match the design** — grouped actions with shortcuts, not flattened button bars.
- **ARIA file present** — `docs/ux/mockups/<screen-slug>.aria.yaml` exists for every in-scope screen; each file contains detailed-fidelity nodes (exact control types, all live states, relationship attributes, grid/table structure, toolbar composition, complete dialog contents).
- **Story and domain term annotations present** — yellow stories box and green domain terms box beside each screen.
- **Stories listed under each screen** — every `### Screen` block lists `**Stories:**` verbatim from story map and `**Domain terms:**` verbatim from Domain Language, matching the annotation boxes.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
