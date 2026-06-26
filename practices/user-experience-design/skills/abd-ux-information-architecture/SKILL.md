---
catalog_garden_tier: practice
catalog_garden_order: 10
name: abd-information-architecture
description: >-
  Produce a first-pass information architecture — site map, navigation, and content model — saved as markdown and draw.io. Use when starting work that involves user interaction changes or aligning on screen structure.
context-perspective: ux
context-fidelity:
  - level: discovery
    mode: information-architecture
---
# abd-information-architecture

## Purpose

Define what screens exist and how users move between them — so missing coverage shows as absent nodes and scope disagreements surface before wireframes begin.

---

## Output file

**Deliverables folder:** see `../common/skill-rule-workflow.md` — Output file resolution.

**File names:** `information-architecture.md` (structured spec), `information-architecture.drawio` (diagram), and one `screens/<screen-slug>.aria.yaml` per screen — all in `docs/ux/information-architecture/`. See [`common/folder-conventions.md`](../../../../common/folder-conventions.md).

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these common input traps:

- **Who arrives at each screen** — who actually uses this screen and what are they trying to accomplish — or are we designing for a generic "user" that doesn't exist?
- **Screen boundaries** — where does one screen end and another begin — are we splitting by feature or by what the user perceives as a single "place" they're in?
- **Navigation mental model** — does the user think of this as a linear flow, a hub they explore from, or something else — and does our site map match that mental model?
- **Hidden screens** — what screens does the user need that nobody has mentioned yet — error recovery, first-time setup, empty-state guidance, admin overrides?
- **Content ownership** — which content types belong on which screen — or are we putting everything on a "dashboard" because nobody has decided where things live?
- **Transition triggers** — what actually causes the user to move between screens — a deliberate choice, an automatic redirect, or an error — and have we designed for each?

---

## Diagram workflow

Produces `docs/ux/initial-ia.drawio` — two pages: Page 1 (Detailed IA, full screen layouts) and Page 2 (Site Map, one box per screen with labeled arrows). Must exist on disk before the cell is marked done.

Build in two passes after `initial-ia.md` and all `aria.yaml` files are written:

**Pass 1 — Structure from ARIA (Mode A — CLI from skill's `scripts/`):**

```bash
node scripts/drawio-ux.mjs open docs/ux/initial-ia.drawio
node scripts/drawio-ux.mjs add-screen "<screen-name>" --layout sidebar --col <c> --row <r>
node scripts/drawio-ux.mjs add-list "<screen-name>" "<region>" --slot body --fields "..." --actions "..."
node scripts/drawio-ux.mjs connect "<source>" "<target>" --label "<trigger>"
node scripts/drawio-ux.mjs save
```

Repeat `add-screen`, `add-list`, and `connect` calls for every screen. `save` always writes both pages.

**Pass 2 — Annotate (no layout changes):** Add yellow stories boxes and green domain terms boxes alongside each screen in the drawio. Save.

**Mode B (no CLI available):** Pass the `aria.yaml` trees and the prompt template from `reference/concepts.md` to an external AI to generate the drawio XML directly.

---

## Agent Instructions

Follow `../common/skill-rule-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files in full before generating. Do not skip any file.

- **`reference/concepts.md`** — core IA dimensions (navigation + content), screen/transition/layout/tab-state definitions, content types, story and domain term traceability rules, mental model alignment, canvas layout convention, and CLI layout templates.
- **`reference/examples.md`** — worked example of a good initial IA showing tab-state decomposition, representative rows, verb rows, chrome conventions, and story budget.
- **`reference/aria-pipeline.md`** — ARIA fidelity model, input resolution (extractor → IA), structural fidelity rules, `aria.yaml` output format, and two-pass rendering protocol.

### 2. Generate

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/initial-ia.md` | Structured spec: scope, source paths, screen flow map, screens (regions, content types, actions, stories, domain terms), transitions, navigational components, content-type details. |

**Method (16-step build):**

**Input resolution (before step 1):** Check whether `docs/extracted-context/from-application/pages/<slug>/aria.yaml` exists for any in-scope screen. If found, use as structural seed per `reference/aria-pipeline.md`; otherwise construct from story map and domain language.

1. Resolve inputs: story map, scope filter, Domain Language file.
2. Filter story map by scope; read the Domain Language.
3. Identify screens by tab state (N tabs = N screens). Check ~4 story budget per screen.
4. Walk every story — produce a **story trace table** (story → screen → region → action/trigger). Every cell must be filled before proceeding.
5. Walk every in-scope domain term — produce a **domain term trace table** (term → appears as → on screen → in region).
6. Identify transitions with labeled triggers.
7. Identify navigational components in UX terms.
8. Identify content types with hierarchy, collections, key actions.
9. Lay out content per screen as rows (representative data rows + verb row), not prose.
10. Draft labels and tags.
11. **Write `docs/ux/ia/<screen-slug>.aria.yaml`** for each screen at structural fidelity. Use `reference/aria-pipeline.md` for the fidelity rules and output format. One file per screen slug.
12. Author the **Screen flow — complete connection map** section of `docs/ux/initial-ia.md`: one ASCII block showing navigation components (drawer nav, secondary nav, etc.) then each screen → [type] action → destination screen, using the format in `templates/initial-ia.md`.
13. Author the rest of `docs/ux/initial-ia.md` from the template.
14. Run the completeness test from `rules/tab-states-and-domain-traceability.md` — fix gaps before touching the canvas.
15. **Pass 1 — Structure from ARIA:** Choose output mode (Mode A: `drawio-ux` CLI; Mode B: filled prompt for external AI) and produce `initial-ia.drawio` driven from the `aria.yaml` trees. Map landmarks to layout regions, navigation links to site-map arrows, primary actions to verb rows. Save. The CLI `save` command always writes **two pages**: Page 1 — Detailed IA (full screen layouts); Page 2 — Site Map (one box per screen, arrows only).
16. **Pass 2 — Annotate:** Add yellow stories boxes and green domain terms boxes alongside each screen in the drawio. Update the story-trace and domain-term-trace tables in `initial-ia.md`. No layout changes in this pass. Save.

**CLI (Mode A — from skill's scripts/):**

```bash
node scripts/drawio-ux.mjs open docs/ux/initial-ia.drawio
node scripts/drawio-ux.mjs add-screen "screen name" --layout sidebar --col 0 --row 0
node scripts/drawio-ux.mjs add-list "screen name" "region" --slot body --fields "..." --actions "..."
node scripts/drawio-ux.mjs connect "source" "target" --label "trigger"
node scripts/drawio-ux.mjs save
# save always produces two diagram pages:
#   Page 1 — "Detailed IA"  (full screen layouts with regions and callouts)
#   Page 2 — "Site Map"     (one titled box per screen, labeled connector arrows)
```

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/skill-rule-workflow.md` § Validate output.

---

## Validate

**Goal:** Read the saved IA as reviewers, not a second authoring pass.

- **Cross-artifact parity** — `initial-ia.md` and `initial-ia.drawio` describe the same IA — same screens, transitions, components, content types, and actions. The drawio **Site Map page** matches the **Screen flow — complete connection map** section in `initial-ia.md` (same screens, same labeled arrows).
- **Every screen** has a name and linked source (domain concept or story).
- **Every transition** has a labeled trigger and clear direction.
- **Every navigational component** is named in UX terms with what it links to.
- **Every content type** carries a name (linked), hierarchy/collection, and key-actions list.
- **Tab states decomposed** — each tab is a separate screen node, not a sub-region.
- **Chrome regions** are named only — no action lists; empty chrome omitted.
- **Left-panel chrome** renders beside the body (`--slot panel`), not stacked above.
- **Grey = repeated sibling chrome only** — `--dimmed` used exclusively for tab-sibling chrome.
- **List regions** show representative rows; actions appear as a verb row below.
- **Every "edit" action** connects to a named detail screen via a transition arrow.
- **Domain terms per screen** are visible-only — no internal model terms, no wholesale KA hierarchy.
- **Story budget** — every screen has ~4 user stories; more signals missing decomposition.
- **No system story has its own screen** — each is grouped with a user-visible screen.
- **No acceptance criteria, controls, copy, or wireframe detail** on any screen.
- **ARIA files present** — `docs/ux/ia/<screen-slug>.aria.yaml` exists for every in-scope screen; each file contains only structural-fidelity nodes (landmarks, navigation links, primary actions, representative list row) — no form field detail, no relationship attributes.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
