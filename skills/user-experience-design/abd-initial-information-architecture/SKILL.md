---
name: abd-initial-information-architecture
description: >-
  Produce a first-pass information architecture for a solution scope — a site
  map of screens and transitions, the navigational components that connect
  them, and a content model (types, hierarchy, labels, tags, key actions) for
  what lives on each screen — drawn on an abd-canvas whiteboard and saved as a
  versioned artifact.
---
# abd-initial-information-architecture

## Purpose

The purpose of this skill is to produce the **initial information architecture** for a solution scope.

**Information architecture (IA)** is the practice of structuring, organizing, and labeling the surfaces and content of a solution so users can find what they need and understand where they are. It covers two dimensions — **navigation** (how a user moves through the solution and the components that carry that movement) and **content** (what lives on each surface, how it is grouped, what it is called, and what users can do with it).

A **site map** — the inventory of screens and the directed transitions between them — is one component of the IA: the navigation backbone. This skill produces it alongside the rest of the IA in a single low-fidelity pass.

Doing this work early, before detailed design or development, flushes out gaps in functional and domain understanding, surfaces disagreements about scope, naming, and navigation when they are cheap to resolve, and gives the team a concrete picture to challenge and confirm before committing to wireframes or implementation. Functional requirements and stories written against a named screen inventory and content model become more precise: they reference agreed surfaces by name, missing coverage shows up as absent nodes, and edge-case states are identified before anyone has built against the wrong assumption.

---

## When to use this skill

Use this skill when **any** of the following apply:

- You are starting work that involves a change in user behavior or user interaction with the solution.
- The team is not aligned on how users engage and interact with the solution — different people describe it differently, and there is no single agreed picture to point at.
- You want an initial view of interaction flow, navigation, and screen layout to complement your early understanding of the solution — without committing to any detail.
- You want to identify gaps, redundancies, or missing states in the solution before anyone invests time designing or building them.
- You need to scope and estimate the work — a named screen inventory and content model make it possible to reason about effort, coverage, and complexity before wireframes or stories exist.
- A previous IA no longer reflects how the team understands the solution, and you need to re-establish a clean structural baseline.

---

## Core outputs

The IA is captured on a single canvas covering two dimensions.

### Navigation

- **Site map** — screens as named boxes, with directed transitions between them showing how users flow from one screen to the next. There should be a simple, obvious mapping from stories to this layer: in-scope stories live on screens, and the events in those stories drive the transitions.
- **Per-screen layout** — for each screen, the standard layout template it follows in conventional terms (e.g. `header + body + footer`, `header + left panel + body (2-column)`, `header + 3-column body`, `header + body grid (2 columns × 2 rows)`, `modal dialog`). The layout names the slots; the regions (next bullet) name what fills each slot.
- **Navigational components** — each screen has an initial description and approximate layout of the persistent surfaces that carry navigation: menus, primary navigation, sidebars, headers, footers, breadcrumbs, link groups. Named regions only, no controls, no styling.

### Content

- **Content types** — the kinds of things users read, create, or act on; where the context provides domain terms, concepts, or classes, a content type is typically one of those. Capture the hierarchy of each content type and any collections it belongs to.
- **Per-screen content layout** — for each screen, a categorized layout of what content lives there, visually depicting high-level relationships (hierarchy, collection) and the key navigation between content.
- **Labels and tags** — preliminary labels and tags needed to identify content elements on the canvas.
- **Key actions per content type** — the headline things a user can do with each content type (browse, create, edit, archive, share, …). There should be a simple, obvious mapping from stories to actions: each in-scope story that acts on a content type contributes an action to that type. No controls, no copy.

---

## Stories and domain as sources

The story map and the ubiquitous language are **sources** for this skill, not its subjects. They feed the IA but are not what it speaks in.

- Use **UX terms** on UX output — *screen*, *region*, *navigation*, *sidebar*, *header*, *footer*, *content type*, *action*, *label*, *tag*.
- When a story or a domain concept appears on the canvas, include only its **name** — the story title or the domain term — and a link to the full source. No acceptance criteria, no full definitions, no behavioral detail on the IA artifact.
- Stories and domain concepts in scope must be **referenceable** from the IA: every in-scope *user* story is reachable from a screen (as a story name listed on it, or as a transition trigger); every in-scope domain concept that the user perceives appears as a screen, content type, label, or action.

---

## Core concepts

### Scope

The slice of the solution this IA covers — typically one **increment**, one **epic**, or one **sprint**. Only stories and domain concepts inside the scope contribute screens, navigation, content types, and labels.

### Screen

A **screen** is a distinct user-visible state — what the user sees and acts on when one set of stories is active. Two states that differ only in transient data are the same screen; states that differ in which regions exist, which navigational components are present, or which actions are available are different screens.

### Transition

A **transition** is a directed move from one screen to another. Its label names the **trigger** — the user action or system event that causes the move — using a UX term when the trigger is structural (e.g. *opens primary nav*) or a domain concept name when the trigger is domain-specific (e.g. *submits valid path*), with a link to the source story or term.

### Layout

The **layout** of a screen is the standard template it follows in conventional UX terms — `header + body + footer`, `header + left panel + body (2-column)`, `header + 3-column body`, `header + body grid (2 columns × 2 rows)`, `modal dialog`, and so on. The layout names the slots; the regions name what fills each slot. Layout is captured per screen in plain language; precise dimensions, spacing, and visual styling belong in `abd-lo-fi` and `abd-hi-fi`.

### Navigational component

A **navigational component** is a persistent surface that carries navigation across screens — menus, primary navigation, sidebars, headers, footers, breadcrumbs, link groups. Components are listed and named in UX terms, with the screens or content types they link to. They are not styled and they do not name controls.

### Tab state / multi-state region

A **region that presents content through tabs, segmented controls, or mode-switches is not one region — each tab state is a distinct user-visible state** and must be decomposed fully. Each state gets its own name, sub-regions (with data shown and key actions), linked domain terms, and linked stories.

On the canvas, each tab state appears as a separate labeled box associated with the containing screen — not a single panel with tab names mentioned in passing.

**Red flag:** if a region description ends with "tabs: X, Y, Z" with no further decomposition, it is incomplete. Every tab must be documented to the same depth as any other region: what data is shown, what actions are available, which domain terms appear, which stories target it.

**Sub-concept traceability:** when a domain concept inside a tab state has its own typed sub-concepts (e.g. an option group with multiple element types), each sub-type that a user interacts with individually must appear as a separate item — not collapsed into one undifferentiated "element" entry. If a story targets a sub-type, the sub-type must be visible as a named item with actions.

### Content type

A **content type** is a kind of thing a user interacts with — typically a domain concept the user reads, edits, or acts on. Each content type carries a hierarchy, collections, labels and tags, and a small set of key actions.

### User story

A **user story** is a story with a user-visible interaction. Each in-scope user story lives on at least one screen and contributes affordances and actions to that screen; the events in a user story drive transitions to or from the screen. On the IA a user story appears by **name** with a **link** to its full source — never by full text or acceptance criteria. The mapping from user stories to screens, transitions, and content actions is what makes the IA traceable back to scope.

### System story

A **system story** has no user-visible interaction of its own. It does not get its own screen — it is grouped (by name, with a link) with the closest user-visible screen whose interaction surfaces it.

### Domain term / concept / class

A **domain term**, **concept**, or **class** comes from the ubiquitous language, conceptual model, or class model of the solution and names something the team and its users care about. On the IA it provides the vocabulary for **content types**, **labels and tags**, **screen subjects**, and **trigger names** — appearing by **name** with a **link** to its definition. The IA does not embed full definitions, attributes, methods, or behavioral detail; those stay in the source.

### Mental model alignment

Screen names, content type names, navigational component names, and the IA as a whole reflect the user's mental model of the solution rather than the technical decomposition. In practice this means:

- When naming a screen, content type, or component, prefer the term the product owner, domain expert, or user uses unprompted in conversation. If you are reaching for a system or framework name (`MainShellViewModel`, `SettingsRoute`), stop and pick a domain or UX term instead.
- When deciding whether two states are one screen or two, ask "does the user think of these as the same place?" Same place → same screen.
- When grouping content into a region or assigning content to a navigational component, ask "does the user perceive these as belonging together?" If they do, the grouping is right.
- When the IA is drafted, read it back to a domain expert or product owner without translating. If they recognise what each screen, region, content type, and action refers to without explanation, alignment is good. If they need translation, the names are wrong — fix them before moving on.

### Card sorting (informally)

Before drawing per-screen content layouts and per-component link groupings, candidate labels are grouped by affinity — what reads as one surface or one cluster to a user. The resulting groups become the named regions, content groupings, and component link sets.

### Rules

`rules/*.md` validate the output (the named artifacts on the canvas and the saved `.md` spec, `.tldr`, and `.svg`). Build steps live in **Build**.

---

## The shape of a good initial IA

```
[ game directory prompt ]
  Regions: prompt panel | path input area | error message area | continue area
  Content: game directory (link)
  Actions: select directory, continue

      |  submits valid path  →
      v

[ crowd manager ]
  Regions: header | primary nav (sidebar) | crowd tree panel | toolbar | filter bar | content area | status bar
  Content types: crowd (collection of character), character
  Actions on crowd: create, rename, archive, browse
  Actions on character: select, edit, move
  Groups system stories: Load Prism Shell and Module · Open Character Crowd Main Workspace
```

The drawing on the canvas mirrors this shape using `abd-canvas` shapes and arrows. Screen boxes are large enough to hold their regions, content types, and actions visibly. Transitions are directed and labeled. Navigational components are shown as named regions, with the screens they link to. No screen carries acceptance criteria, controls, copy, or wireframe-level detail.

---

## Build

**Goal:** Read the story map and ubiquitous language for a scope, identify the screens, transitions, navigational components, content types, per-screen content layouts, labels, and key actions, and save the result as `initial-ia.md` (structured spec), `initial-ia.tldr` (canvas), and `initial-ia.svg` (flat export) in the engagement's `docs/ux/` folder.

1. **Resolve inputs.** Confirm three inputs are available: a path to `story-map.md`, a scope filter (increment number, epic name, sprint, or other), and a path to the ubiquitous-language file for that scope. If any is missing, ask the user.

2. **Filter the story map by scope.** Read `story-map.md` and keep only stories inside the scope filter.

3. **Read the ubiquitous language.** Read every term and definition in the supplied UL file. Domain concepts that appear on the canvas appear as **names with a link**; full definitions stay in the UL file.

4. **Identify screens.** For each in-scope story, decide whether it introduces a new user-visible state. Group stories that share a screen. Group system stories with the closest user-visible screen that surfaces them.

4a. **Walk every story — produce a story trace table.** Before assigning screens, create a table with one row per in-scope story: `| story title | screen | region | key action or transition trigger |`. Fill every cell. Any row where the region or action column cannot be filled means either (a) a region is missing from a screen, (b) an action is missing from a region, or (c) a screen is missing entirely. Do not proceed past this step until every GM story has a non-empty region and action/trigger. System stories need only a screen and a "grouped" note.

    This is the primary completeness gate. The most common failures are:
    - A tabbed panel where only one tab's stories appear (the other tabs' stories have no home)
    - A contextual panel (attack configuration, modal, overlay) that was never added as a region
    - A roster or list panel that is implied by add/remove/activate stories but never drawn
    - Individual element-add stories (Add FX Element, Add MOV Element, …) that get collapsed into one "add element" action and effectively disappear

4b. **Walk every in-scope domain term — produce a domain term trace table.** Create a table: `| domain term | appears as | on screen | in region |`. "Appears as" is one of: screen name, region name, sub-region name, content type name, label, key action, or annotation only. A term marked "annotation only" is incomplete — trace it to a visible element or explain why it is purely metadata. Terms with typed sub-concepts (option groups, collection members, element types) require one row per sub-type if users interact with each type individually.

5. **Identify transitions.** For each pair of adjacent screens, find the user action or system event in the stories that moves the user between them. Label the arrow with that trigger.

6. **Identify navigational components.** From the screens and the stories, extract the persistent navigation surfaces (menus, primary navigation, sidebars, headers, footers, breadcrumbs). Name each in UX terms and list the screens or content types it links to.

7. **Identify content types and their structure.** For each in-scope domain concept the user perceives, decide whether it is a content type. For each content type, capture its hierarchy, the collections it belongs to, and a small set of key actions a user can perform on it.

8. **Lay out content per screen.** For each screen, list the regions and what content lives in each region. Identify every region that has tabs, modes, or sub-screens — do not treat these as a single region. Decompose each tab/mode state into its own named sub-region block with: (a) data shown, (b) key actions, (c) linked domain terms, (d) linked stories. For any domain concept inside a tab state that has typed sub-concepts (e.g. an option group with multiple element types), list each sub-type as a separate item with its own data and actions. A region description that ends with "tabs: X, Y, Z" without decomposing each tab is incomplete and must not proceed to the canvas.

9. **Draft preliminary labels and tags.** Where elements need identification on the canvas, choose labels in UX terms for structural pieces and domain term names (linked) for subject matter.

10. **Author or update `docs/ux/initial-ia.md` first.** Copy `templates/initial-ia.md` into the engagement's `docs/ux/` folder (or open the existing one) and fill in: scope, source paths (story map, UL), description, screens (regions, content types, actions, in-scope story names with links, grouped system story names with links), transitions, navigational components, and content-type details. This markdown is the structured spec the canvas is drawn from; the canvas is never authored without it.

10a. **Run the completeness test before touching the canvas.** Walk the checklist in `rules/tab-states-and-domain-traceability.md`:
  - Every tab/mode state fully decomposed in the spec.
  - Every in-scope domain term visible as a region, sub-region, content type, or action label — not only in the annotation.
  - Every in-scope domain concept's typed sub-concepts listed as separate items where users interact with them.
  - Every in-scope user story maps to a key action or transition trigger — no orphaned stories.
  Only proceed to the canvas when all items pass. Fix gaps in `initial-ia.md` first.

11. **Resolve the abd-canvas location.** Look up `$env:ABD_CANVAS_PATH`. If unset, default to `C:\dev\abd-canvas`. If the folder does not exist, stop and tell the user to clone the canvas from `https://github.com/agilebydesign/abd-canvas` into that path (or set `$env:ABD_CANVAS_PATH` to wherever it lives locally).

12. **Launch abd-canvas.** Run `node C:\dev\abd-canvas\scripts\start-canvas.js` (or `npm run dev` in the canvas folder) and wait for `http://localhost:5173` to be reachable. Open that URL in the browser.

13. **Fill and deliver the canvas prompt.** Fill the slots in `templates/initial-ia-prompt.md` from `docs/ux/initial-ia.md` (the structured spec is the single source of truth) and **output the filled prompt to the user in the chat** so they can paste it directly into the canvas chat panel. Do not attempt to type it into the canvas via browser automation — paste-by-user is the reliable path. Wait for the user to confirm the agent has finished drawing before proceeding.

    **Critical canvas instructions:** The prompt must tell the agent to draw **visual boxes and arrows**, not text descriptions of layout. Every screen is a rectangle; every region is a subdivided rectangle inside the screen box; every transition is a directed labeled arrow; content types are boxes with hierarchy lines. Never describe layout in words on the canvas — draw it.

    **Required per-screen content in the prompt:** Every screen block must include:
    - Region boxes with labels and the actions/data shown in each region
    - A **Stories** note per screen listing every in-scope user story name (title only — no AC)
    - A **Domain terms** note per screen listing every domain concept name that appears on that screen
    These must appear as readable text on the canvas — not omitted because "they are in the spec".

14. **Save canvas outputs.** When the agent finishes, click the `Save .tldr` button in the canvas helper-button row and write to `<engagement>/docs/ux/initial-ia.tldr`. Then export an SVG of the same canvas to `<engagement>/docs/ux/initial-ia.svg`. Overwrite both files on every run — git carries the history.

15. **Sync canvas changes back into `initial-ia.md`.** Read the updated canvas. If the agent renamed regions, added or removed transitions, regrouped components, added content types or actions, or otherwise changed the structure, update `docs/ux/initial-ia.md` to match. Append a row to the change log with date, direction (`canvas → md`), and a one-line summary.

16. **Apply the rules, then review like a peer.** Walk every file under `rules/` against the drawn canvas, the saved files, and the markdown spec. Fix every violation.

17. **Keep the bundled rules block honest.** Whenever you change a file under `rules/`, re-run the bundler so the rule prose inlined at the end of this `SKILL.md` matches what is on disk:

```bash
python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/user-experience-design/abd-initial-information-architecture
```

- **Outputs:** `docs/ux/initial-ia.md` (structured spec), `docs/ux/initial-ia.tldr` (canvas), `docs/ux/initial-ia.svg` (flat export) — three artifacts in the engagement's deliverables folder, kept in sync.
- **Per format:** `.md` is the structured spec — created first, updated after canvas changes. `.tldr` is the round-tripable canvas (re-openable via the canvas `Load .tldr` button). `.svg` is the flat artifact for documentation and reviews.
- **While writing:** UX terms for structural pieces, domain term names (linked) for subject matter. No invented vocabulary. No acceptance criteria. No controls. No wireframe detail.

---

## Validate

**Goal:** Read the saved IA as reviewers, not a second authoring pass.

- **Who is checking:** the product owner verifies that every in-scope story is referenceable from the IA (as part of a screen or as a transition trigger); a domain expert verifies that every domain concept appearing on the canvas is named and linked correctly; a UX practitioner verifies that the structural language is in UX terms and that the IA reads as navigation + content with no controls smuggled in.
- **Cross-artifact parity:** the `.md`, `.tldr`, and `.svg` describe the same IA — the same screens, transitions, navigational components, content types, and actions.

Walk the canvas and confirm:

- Every screen carries a name and a link to its source (domain concept or story).
- Every transition has a labeled trigger and a clear direction.
- Every navigational component is named in UX terms and lists what it links to.
- Every content type carries a name (linked), a hierarchy or collection, and a key-actions list.
- Every region label uses UX terms; every subject-matter label uses a domain term name with a link.
- No system story has its own screen; each is grouped with a user-visible screen.
- No screen carries acceptance criteria, controls, copy, or wireframe-level detail.
- `docs/ux/initial-ia.md`, `docs/ux/initial-ia.tldr`, and `docs/ux/initial-ia.svg` all exist and are in sync.
- **Every region with tabs or modes is decomposed into per-state sub-regions** — no "tabs: X, Y, Z" shorthand without full decomposition.
- **Every in-scope domain term appears as a named element** (region, sub-region, content type, label, or action) — not only in the per-screen annotation.
- **Every in-scope domain concept with typed sub-concepts** has those sub-types listed individually where users interact with them.
- **Every in-scope user story maps to a visible key action or transition trigger** — walk each story and confirm it resolves; if it does not, a screen, region, or action is missing.

---

## Deploy

This skill ships IDE-deployable files under `ide-files/`. Deploy them from the repo root using the standard repo-level script:

```powershell
cd C:\dev\agilebydesign-skills
.\scripts\deploy-skills.ps1 -ide cursor -Force
```

`deploy-skills.ps1` auto-discovers every skill under `skills/` with a `SKILL.md` and links its `ide-files/*.mdc` into `<deploy-root>/.cursor/rules/` and `ide-files/*.prompt.md` into `<deploy-root>/.cursor/commands/`. The deploy root is resolved from `skill-config.json`.

| File | Deploy target |
| --- | --- |
| `ide-files/abd-initial-information-architecture.mdc` | `.cursor/rules/` (Cursor always-on rule) |
| `ide-files/abd-initial-information-architecture.instructions.md` | `.github/` when `-ide vscode` is used (VS Code — same body as `.mdc` after frontmatter) |
| `ide-files/abd-initial-information-architecture.prompt.md` | `.cursor/commands/` (Cursor slash command); also `.github/prompts/` under VS Code |

---

<!-- execute_rules:bundle_rules:begin -->
<!-- Rule prose is generated from rules/*.md — edit rules, then run:
     python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/user-experience-design/abd-initial-information-architecture
-->
<!-- execute_rules:bundle_rules:end -->
