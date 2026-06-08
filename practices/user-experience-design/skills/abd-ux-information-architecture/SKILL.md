---
catalog_garden_tier: practice
catalog_garden_order: 10
name: abd-information-architecture
description: >-
  Produce a first-pass information architecture for a solution scope — a site
  map of screens and transitions, the navigational components that connect
  them, and a content model (types, hierarchy, labels, tags, key actions) for
  what lives on each screen — saved as a structured markdown spec and a draw.io
  diagram. Use when starting work that involves user interaction changes, when
  the team needs a shared picture of screens and navigation, or when scoping
  effort before wireframes or stories exist.
---
# abd-information-architecture

## Purpose

Doing IA work early — before detailed design or development — flushes out gaps in functional and domain understanding, surfaces disagreements about scope, naming, and navigation when they are cheap to resolve, and gives the team a concrete picture to challenge and confirm before committing to wireframes or implementation. Functional requirements and stories written against a named screen inventory and content model become more precise: they reference agreed surfaces by name, missing coverage shows up as absent nodes, and edge-case states are identified before anyone has built against the wrong assumption.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File names:** `initial-ia.md` (structured spec) and `initial-ia.drawio` (diagram), typically in `docs/ux/`.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — core IA dimensions (navigation + content), screen/transition/layout/tab-state definitions, content types, story and domain term traceability rules, mental model alignment, canvas layout convention, and CLI layout templates.
- **`reference/examples.md`** — worked example of a good initial IA showing tab-state decomposition, representative rows, verb rows, chrome conventions, and story budget.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/initial-ia.md` | Structured spec: scope, source paths, screens (regions, content types, actions, stories, domain terms), transitions, navigational components, content-type details. |

**Method (13-step build):**

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
11. Author `docs/ux/initial-ia.md` from the template.
12. Run the completeness test from `rules/tab-states-and-domain-traceability.md` — fix gaps before touching the canvas.
13. Choose output mode (Mode A: `drawio-ux` CLI; Mode B: filled prompt for external AI) and produce `initial-ia.drawio`.

**CLI (Mode A — from skill's scripts/):**

```bash
node scripts/drawio-ux.mjs open docs/ux/initial-ia.drawio
node scripts/drawio-ux.mjs add-screen "screen name" --layout sidebar --col 0 --row 0
node scripts/drawio-ux.mjs add-list "screen name" "region" --slot body --fields "..." --actions "..."
node scripts/drawio-ux.mjs connect "source" "target" --label "trigger"
node scripts/drawio-ux.mjs save
```

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-information-architecture \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Read the saved IA as reviewers, not a second authoring pass.

- **Cross-artifact parity** — `initial-ia.md` and `initial-ia.drawio` describe the same IA — same screens, transitions, components, content types, and actions.
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
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
