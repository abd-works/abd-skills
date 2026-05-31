---
catalog_garden_tier: practice
catalog_garden_order: 20
name: abd-ux-mockup
catalogue_one_liner: >-
  Lo-fi wireframes — exact controls, interactions, and states drawn in Draw.io from IA screens.
description: >-
  Precision pass after the initial IA — specify exact controls, interactions,
  and states for any scope (full site, flow, epic, story), drawn in Draw.io
  as a lo-fi wireframe and saved as a versioned .drawio artifact.
  Use when deciding which control renders each field, which button is primary,
  what conditional states exist, or reviewing a screen at the interaction level
  against its acceptance criteria.
---
# abd-ux-mockup

## Purpose

The initial IA established the screen inventory, regions, and story coverage. The lo-fi mockup is the next precision pass: it locks down **exactly which control renders each field**, **exactly what interactions are available in each state**, and **exactly what the user sees and does** — without yet committing to visual design. Every input becomes a specific control type (text field, dropdown, checkbox). Every action becomes a positioned button with a primary/secondary weight. Every conditional state (validation error, empty list, disabled control) is explicitly placed. This skill packages that pass: take one IA screen, resolve its AC and domain terms, build a `drawio-mockup.mjs` state file, generate the `.drawio` wireframe, and save it — so interaction decisions are made deliberately and traceable, not invented during implementation.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File names:** `<screen-slug>-state.json` (state source of truth), `<screen-slug>.drawio` (generated wireframe), `<screen-slug>.md` (structured spec). Output to `docs/ux/lo-fi/`.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — what a lo-fi mockup is, source IA, design image reference, UI element types and state formats, field input types, domain terms and AC verbatim rules, the shape of a good state file, rendering approach (CLI vs AI-crafted XML), mxGraph XML patterns, and CLI reference.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

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

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-ux-mockup \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

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
