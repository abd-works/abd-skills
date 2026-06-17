---
catalog_garden_tier: practice
catalog_garden_order: 10
name: abd-information-architecture
description: >-
  Produce a first-pass information architecture for a solution scope — a site
  map of screens and transitions, the navigational components that connect
  them, and a content model (types, hierarchy, labels, tags, key actions) for
  what lives on each screen — saved as a structured markdown spec and a draw.io
  diagram.
---
# abd-information-architecture

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

**Story budget signal:** a screen should carry ~4 user stories. Consistently more than ~4 almost always means a tab state, a detail/edit screen, or a mode has not been separated out. Each story on a screen must be directly and visibly satisfied by a region or action on that screen — not by a region on a sibling or ancestor screen.

### Transition

A **transition** is a directed move from one screen to another. Its label names the **trigger** — the user action or system event that causes the move — using a UX term when the trigger is structural (e.g. *opens primary nav*) or a domain concept name when the trigger is domain-specific (e.g. *submits valid path*), with a link to the source story or term.

### Layout

The **layout** of a screen is the standard template it follows. Use one of the named templates below — the CLI enforces the slot geometry. Layout is captured per screen as a template name; precise dimensions, spacing, and visual styling belong in `abd-lo-fi` and `abd-hi-fi`.

#### Layout templates

Use `node $DUXCLI templates` to print the full list with ASCII diagrams. Available templates and their slots:

```
stack        — single column                          slot: body
               +----------+
               |   body   |
               +----------+

modal        — centered overlay dialog (rounded)      slot: body
               +--[MODAL]---------+
               |      body        |
               +------------------+

form         — single-column form (stacked inputs)    slot: body
               +------------------+
               | [field]          |
               | [field]  [submit]|
               +------------------+

sidebar      — left panel + right workspace           slots: panel | body
               +--------+----------+
               | panel  |  body    |
               +--------+----------+

split-screen — two equal columns                      slots: left | right
               +----------+----------+
               |  left    |  right   |
               +----------+----------+

flyout       — main content + contextual side panel   slots: body | panel
               +---------------+------+
               |  body         |panel |
               +---------------+------+

holy-grail   — header + nav + body + aside + footer   slots: header, nav, body, aside, footer
               +---------------------+
               |      header         |
               +-----+--------+------+
               | nav |  body  |aside |
               +-----+--------+------+
               |      footer         |
               +---------------------+
```

`header` and `footer` slots always render as full-width bands above and below the column section, regardless of template. Any region assigned an unknown slot falls through to `body` (or the first defined column).

### Navigational component

A **navigational component** is a persistent surface that carries navigation across screens — menus, primary navigation, sidebars, headers, footers, breadcrumbs, link groups. Components are listed and named in UX terms, with the screens or content types they link to. They are not styled and they do not name controls.

### Canvas layout convention

The diagram uses a **column × row grid**. Every screen gets a `--col` (horizontal) and `--row` (vertical) when added. **Both are required — never rely on insertion order.**

```
screen ──► screen ──► screen          ← linear path: col increases, row = 0
                │
                ▼
           option 1 ──► detail        ← option: same col, row increments; detail goes right (col+) at same row
                ▼
           option 2 ──► detail
                ▼
           option 3
```

#### Decision rule — linear vs option (be aggressive)

Ask one question per screen: **"Can the user skip this and still complete the primary flow?"**

- **No — always visited:** linear. Put it in row 0, increment col.
- **Yes — sometimes visited:** option. Keep col the same as its trigger, increment row.

If in doubt, call it an option. Placing an optional screen in the linear row causes its column to push everything right, creating overlapping connections. The cost of calling it an option is zero — it just goes below.

**Common examples:**
| Screen | Linear or option? | Why |
|---|---|---|
| Game dir prompt → crowd manager | Linear | Always happens on first run |
| Crowd manager → desktop | Linear | Always happens to start a session |
| Desktop → attack config | Linear | Always happens when attacking |
| Crowd manager → model browser | **Option** | Only if building a crowd from a model list |
| Crowd manager abilities → ability editor | **Option** | Only when editing an ability |
| Tab siblings (identities / abilities / movements) | **Options** | User picks one; stack in same col |

#### Placing screens

```powershell
# Linear flow — row 0, cols 0 → N
node $DUXCLI add-screen "game directory prompt"      --layout modal        --col 0 --row 0
node $DUXCLI add-screen "crowd manager — identities" --layout sidebar      --col 1 --row 0
node $DUXCLI add-screen "desktop"                    --layout split-screen --col 2 --row 0
node $DUXCLI add-screen "attack configuration"       --layout flyout       --col 3 --row 0

# Options off crowd manager col 1 — same col, rows 1+
node $DUXCLI add-screen "crowd manager — abilities"  --layout sidebar --col 1 --row 1
node $DUXCLI add-screen "crowd manager — movements"  --layout sidebar --col 1 --row 2
node $DUXCLI add-screen "model browser"              --layout modal   --col 1 --row 3

# Detail screens for options — right of their parent option, same row
node $DUXCLI add-screen "ability editor"             --layout form    --col 2 --row 1
```

#### Connection routing

- **Cross-column connections** (different col): mxGraph routes automatically — clean horizontal arrows.
- **Same-column connections** (same col, different row): the CLI auto-routes these along the **left edge** of the column so they never cut through screen boxes. No manual intervention needed.

### Tab state

A **panel with N tabs generates N separate screens on the site map.** Each tab state is a full screen node — named `{{parent screen}} — {{tab label}}` (e.g. `crowd manager — identities`, `crowd manager — abilities`). The inactive tabs are shown as greyed labels in the tab bar of each sibling screen. The transition between tab states is an arrow labeled "selects {{tab}} tab".

The outer chrome of a multi-tab screen (toolbar, side panel, status bar, etc.) is shared across all tab-state screens. On the canvas this chrome is drawn once on each sibling screen box but described only in the primary screen block in the spec — sibling blocks note `chrome: same as {{parent screen}}`.

On the diagram, sibling-screen chrome is drawn with `add-chrome --dimmed`, which fills it with light grey (`#f5f5f5`). **Grey is used only for this purpose** — to de-emphasise chrome that repeats unchanged across sibling tab screens. Data rows and form fields are never grey.

**Red flag:** treating a tabbed panel as one screen with sub-regions is wrong. If you find yourself writing "character detail panel — tab: Identities … tab: Abilities … tab: Movements" inside one screen block, stop — each tab is a separate screen.

### Content type

A **content type** is a kind of thing a user interacts with — typically a domain concept the user reads, edits, or acts on. Each content type carries a hierarchy, collections, labels and tags, and a small set of key actions.

### User story

A **user story** is a story with a user-visible interaction. Each in-scope user story lives on at least one screen and contributes affordances and actions to that screen; the events in a user story drive transitions to or from the screen. On the IA a user story appears by **name** with a **link** to its full source — never by full text or acceptance criteria. The mapping from user stories to screens, transitions, and content actions is what makes the IA traceable back to scope.

### System story

A **system story** has no user-visible interaction of its own. It does not get its own screen — it is grouped (by name, with a link) with the closest user-visible screen whose interaction surfaces it.

### Domain term / concept / class

A **domain term**, **concept**, or **class** comes from the ubiquitous language, conceptual model, or class model of the solution and names something the team and its users care about. On the IA it appears by **name** with a **link** to its definition.

**Visible-only rule:** a domain term belongs on a screen only if it names something the user can see or directly interact with on that screen — a data field label, a list row type name, a region name, or a screen name. Internal model concepts that do not appear as visible text or a distinct UI element are excluded. The full sub-concept hierarchy of a KA is never listed wholesale; list only the sub-concepts that appear as named items in the UI.

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

The reference pattern — each tab state is its own screen, list regions show representative rows, actions are a verb row, chrome is named but not described, and each screen carries ~4 stories.

```
[ game directory prompt ]                          modal dialog
  ┌─────────────────────────────┐
  │ COH game directory          │  — label only
  │ directory path · browse     │  — field labels only
  │ validation feedback         │  — conditional region label
  │ continue                    │  — action gate
  └─────────────────────────────┘
  Stories (~2): Validate Game Directory · Prompt if Invalid
  Domain terms: COH game directory

       │ submits valid path
       ▼

[ crowd manager — identities ]                     left panel + body
  ┌────────────────┬────────────────────────────┐
  │ crowd tree     │ [ Identities ] Abilities   │  ← inactive tabs greyed; crowd tree
  │ (chrome,       │   Movements                │    uses --slot panel in sidebar layout
  │ --slot panel)  ├────────────────────────────┤    so it renders beside body, not above
  │                │ identity row: name · type  │  ← representative row 1
  │                │   active / default         │
  │                │ identity row: name · type  │  ← representative row 2
  │                │   active / default         │
  │                │ add · remove · set default │  ← verb row (light fill, black border)
  │                │   set active · reorder     │
  └────────────────┴────────────────────────────┘
  Stories (~4): Add Identity · Set Default Identity · Set Active Identity · Remove Identity
  Domain terms: identity · model identity · costume identity · active identity · default identity

  ↓ selects Abilities tab                ↓ selects Movements tab

[ crowd manager — abilities ]           [ crowd manager — movements ]
  ┌────────────────┬──────────────────┐   ┌────────────────┬──────────────────┐
  │ crowd tree     │ Identities       │   │ crowd tree     │ Identities       │
  │ (--panel left, │ [Abilities]      │   │ (--panel left, │ Abilities        │
  │  --dimmed)     │ Movements        │   │  --dimmed)     │ [Movements]      │
  │                ├──────────────────┤   │                ├──────────────────┤
  │                │ ability row      │   │                │ movement row     │
  │                │ ability row      │   │                │ movement row     │
  │                │ create · delete  │   │                │ add · remove     │
  │                │ play · stop      │   │                │ set default      │
  │                │ set key · edit   │   │                │ set key · edit   │
  └────────────────┴──────────────────┘   └────────────────┴──────────────────┘
  crowd tree dimmed (--dimmed) = grey fill    crowd tree dimmed (--dimmed) = grey fill
  signals "same chrome as primary screen"     signals "same chrome as primary screen"

  edit──► [ ability editor screen ]
  Stories (~4): Create Animated Ability       Stories (~3): Add Movement
    Delete · Set Key · Toggle Persistence       Edit Movement Parameters
  Domain terms: animated ability              Domain terms: character movement
```

No screen carries toolbar actions, navigation content, acceptance criteria, controls, copy, or wireframe-level detail. If a screen has more than ~4 user stories, a tab state or edit screen is missing.

---

## Build

**Goal:** Read the story map and ubiquitous language for a scope, identify the screens, transitions, navigational components, content types, per-screen content layouts, labels, and key actions, and save the result as `initial-ia.md` (structured spec) and `initial-ia.drawio` (diagram) in the engagement's `docs/ux/` folder.

1. **Resolve inputs.** Confirm three inputs are available: a path to `story-map.md`, a scope filter (increment number, epic name, sprint, or other), and a path to the ubiquitous-language file for that scope. If any is missing, ask the user.

2. **Filter the story map by scope.** Read `story-map.md` and keep only stories inside the scope filter.

3. **Read the ubiquitous language.** Read every term and definition in the supplied UL file. Domain concepts that appear on the canvas appear as **names with a link**; full definitions stay in the UL file.

4. **Identify screens by tab state, not by feature.** For each in-scope story, decide which user-visible state it belongs to. A panel with N tabs produces N screens — name them `{{parent}} — {{tab label}}`. Group system stories with the closest user-visible screen. Check the story budget: if any screen accumulates more than ~4 user stories, look for a missed tab, a missing detail/edit screen, or a mode that should be separated. Fix before continuing.

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

8. **Lay out content per screen — rows, not prose.** For each screen, list its regions. Follow these rules without exception:
   - **Chrome regions** (toolbar, sidebar, header, footer, crowd tree) — named boxes only. Do not list actions or data inside them.
   - **Left-panel chrome** (`--slot panel` in a `sidebar` or `flyout` layout) — when a screen's layout places a tree or sidebar panel *beside* the content area (not above it), assign the chrome to `--slot panel`. This renders the panel as a left column alongside the body (list/form) regions. Never stack a panel region above list regions when the actual UI places them side by side.
   - **Empty chrome** — only add a chrome region if it has visible content at IA level (named items, labelled structure). Omit any toolbar, footer, or sidebar box that has nothing to show. A named empty box adds noise and signals an incomplete layout.
   - **Grey = de-emphasis for repeated sibling chrome only** — use `add-chrome --dimmed` for chrome that appears unchanged on every sibling tab screen. This fills it with light grey (`#f5f5f5`) to signal repetition. Never apply grey to data rows or form fields.
   - **List/collection regions** — show 2–3 representative item rows. Each row contains only the visible field names (e.g. `name · activation key · flags`). Below the rows, add a single verb row of actions (e.g. `create · remove · play · stop · edit · reorder`). Never write "per item: …" prose.
   - **Edit/configure actions** — if the verb row includes "edit" or "configure", create a new named detail screen for the editor and add a transition arrow labeled "opens {{name}} editor". The detail screen is a full site-map node.
   - **Domain terms per screen** — list only terms that name a visible field, row type, or region on this screen. Do not list internal model terms or the full KA hierarchy.

9. **Draft preliminary labels and tags.** Where elements need identification on the canvas, choose labels in UX terms for structural pieces and domain term names (linked) for subject matter.

10. **Author or update `docs/ux/initial-ia.md` first.** Copy `templates/initial-ia.md` into the engagement's `docs/ux/` folder (or open the existing one) and fill in: scope, source paths (story map, UL), description, screens (regions, content types, actions, in-scope story names with links, grouped system story names with links), transitions, navigational components, and content-type details. This markdown is the structured spec the canvas is drawn from; the canvas is never authored without it.

10a. **Run the completeness test before touching the canvas.** Walk the checklist in `rules/tab-states-and-domain-traceability.md`:
  - Every tab/mode state fully decomposed in the spec.
  - Every in-scope domain term visible as a region, sub-region, content type, or action label — not only in the annotation.
  - Every in-scope domain concept's typed sub-concepts listed as separate items where users interact with them.
  - Every in-scope user story maps to a key action or transition trigger — no orphaned stories.
  Only proceed to the canvas when all items pass. Fix gaps in `initial-ia.md` first.

11. **Choose output mode.** After `initial-ia.md` passes the completeness check, produce `initial-ia.drawio` using one of two modes — ask the user if not already specified:

    **Mode A — Internal (agent uses the `drawio-ux` CLI):**
    Use `scripts/drawio-ux.mjs` — a Node.js CLI included in this skill — to build the diagram from a sequence of commands. No dependencies required; it generates mxGraph XML directly. The CLI enforces the style contract (white fill, black stroke, italic chrome, orthogonal edges) so the agent never touches raw XML.

    Resolve the CLI path:
    - From the agilebydesign-skills repo: `node skills/user-experience-design/abd-information-architecture/scripts/drawio-ux.mjs`
    - From a deployed project junction: `node .cursor/skills/abd-information-architecture/scripts/drawio-ux.mjs`

    Use this alias in the steps below: `DUXCLI=<resolved path>`

    Run these commands in sequence from the engagement root:

    ```powershell
    # 1 — point at the output file
    node $DUXCLI open docs/ux/initial-ia.drawio

    # 2 — start fresh
    node $DUXCLI clear

    # 3 — add screens with named layout templates
    node $DUXCLI add-screen "game directory prompt"      --layout modal
    node $DUXCLI add-screen "crowd manager — identities" --layout sidebar
    node $DUXCLI add-screen "crowd manager — abilities"  --layout sidebar --tab-of "crowd manager — identities"
    node $DUXCLI add-screen "crowd manager — movements"  --layout sidebar --tab-of "crowd manager — identities"
    # ... one add-screen per screen in initial-ia.md

    # 4 — add regions using --slot to place them in the correct template slot
    #
    # modal: single 'body' slot
    node $DUXCLI add-form "game directory prompt" "directory entry form" \
      --slot body --fields "COH game directory · directory path · browse · validation feedback · continue"

    # sidebar: crowd tree in 'panel', content list in 'body'
    node $DUXCLI add-chrome "crowd manager — identities" "crowd tree" --slot panel
    node $DUXCLI add-list   "crowd manager — identities" "identity list" \
      --slot body --fields  "name · type · active · default" \
                 --actions "add · remove · set-default · set-active"

    # Sibling screens: repeated chrome uses --dimmed (grey fill).
    # Grey signals "same chrome as primary screen" — ONLY valid use of grey.
    node $DUXCLI add-chrome "crowd manager — abilities" "crowd tree" --slot panel --dimmed
    node $DUXCLI add-list   "crowd manager — abilities" "ability list" \
      --slot body --fields  "name · activation key · persistent · attack flag" \
                 --actions "create · delete · set-key · toggle-persistence · play · stop · edit"

    node $DUXCLI add-chrome "crowd manager — movements" "crowd tree" --slot panel --dimmed
    node $DUXCLI add-list   "crowd manager — movements" "movement list" \
      --slot body --fields  "name · activation key · default · type" \
                 --actions "add · remove · set-default · set-key · edit"

    # 5 — add transitions
    node $DUXCLI connect "game directory prompt" "crowd manager — identities" \
      --label "submits valid path"
    node $DUXCLI connect "crowd manager — identities" "crowd manager — abilities" \
      --label "selects Abilities tab" --dashed
    node $DUXCLI connect "crowd manager — identities" "crowd manager — movements" \
      --label "selects Movements tab" --dashed

    # 6 — add callouts (stories + domain terms)
    node $DUXCLI add-callout "crowd manager — identities" \
      --stories "Add Identity · Set Default Identity · Set Active Identity · Remove Identity" \
      --terms   "identity · active identity · default identity · model identity"

    # 7 — generate the file
    node $DUXCLI save
    ```

    Check the current build state at any point with `node $DUXCLI status`.
    Overwrite `docs/ux/initial-ia.drawio` on every run — git carries the history.

    **Mode B — External (output a filled prompt for use anywhere):**
    Fill the slots in `templates/initial-ia-prompt.md` from `docs/ux/initial-ia.md` and **output the filled prompt to the user in chat**. The user pastes it into any AI chat (ChatGPT, Claude.ai, Copilot, Cursor, etc.) and asks the AI to return draw.io XML. The prompt instructs the AI to follow the same style contract as Mode A (white boxes, black outlines) and return only raw mxGraph XML. Save the returned XML to `docs/ux/initial-ia.drawio`.

12. **Sync diagram changes back into `initial-ia.md`.** If the diagram was edited directly in draw.io or via the drawio-ai plugin and structural changes were made (screens renamed, regions added/removed, transitions changed), update `docs/ux/initial-ia.md` to match. Append a row to the change log with date, direction (`drawio → md`), and a one-line summary.

13. **Apply the rules, then review like a peer.** Walk every file under `rules/` against the drawn canvas, the saved files, and the markdown spec. Fix every violation.

14. **Keep the bundled rules block honest.** Whenever you change a file under `rules/`, re-run the bundler so the rule prose inlined at the end of this `SKILL.md` matches what is on disk:

```bash
python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/user-experience-design/abd-information-architecture
```

- **Outputs:** `docs/ux/initial-ia.md` (structured spec) and `docs/ux/initial-ia.drawio` (diagram) — two artifacts in the engagement's deliverables folder, kept in sync.
- **Per format:** `.md` is the structured spec — created first, updated after diagram changes. `.drawio` is the visual diagram opened and edited in draw.io (VS Code draw.io extension or desktop app).
- **While writing:** UX terms for structural pieces, domain term names (linked) for subject matter. No invented vocabulary. No acceptance criteria. No controls. No wireframe detail.

---

## Validate

**Goal:** Read the saved IA as reviewers, not a second authoring pass.

- **Who is checking:** the product owner verifies that every in-scope story is referenceable from the IA (as part of a screen or as a transition trigger); a domain expert verifies that every domain concept appearing on the canvas is named and linked correctly; a UX practitioner verifies that the structural language is in UX terms and that the IA reads as navigation + content with no controls smuggled in.
- **Cross-artifact parity:** `initial-ia.md` and `initial-ia.drawio` describe the same IA — the same screens, transitions, navigational components, content types, and actions.

Walk the canvas and confirm:

- Every screen carries a name and a link to its source (domain concept or story).
- Every transition has a labeled trigger and a clear direction.
- Every navigational component is named in UX terms and lists what it links to.
- Every content type carries a name (linked), a hierarchy or collection, and a key-actions list.
- Every region label uses UX terms; every subject-matter label uses a domain term name with a link.
- No system story has its own screen; each is grouped with a user-visible screen.
- No screen carries acceptance criteria, controls, copy, or wireframe-level detail.
- `docs/ux/initial-ia.md` and `docs/ux/initial-ia.drawio` both exist and are in sync.
- **Each tab state is a separate screen node** — no tab state is described as a sub-region of another screen.
- **Chrome regions (toolbar, nav, sidebar, header, footer) are named only** — they carry no action lists in the layout. Chrome with no visible content at IA level is omitted entirely (no empty named boxes).
- **Left-panel chrome renders beside the body** — crowd tree, sidebar, and nav panels that the real UI places side-by-side with the content region use `--slot panel` in a `sidebar` or `flyout` layout, not stacked above list regions.
- **Grey = repeated sibling chrome only** — `--dimmed` (grey fill `#f5f5f5`) is used exclusively on chrome that repeats unchanged across sibling tab screens. Data rows and form fields carry no grey style.
- **List regions show representative rows** — no "per item: …" prose; actions appear as a verb row below the list.
- **Every "edit" action connects to a named detail screen** via a transition arrow.
- **Domain terms per screen are visible-only** — no internal model terms, no wholesale KA hierarchy dumps.
- **Every screen has ~4 user stories** — more than ~4 is a decomposition signal that was not resolved.

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
| `ide-files/abd-information-architecture.mdc` | `.cursor/rules/` (Cursor always-on rule) |
| `ide-files/abd-information-architecture.instructions.md` | `.github/` when `-ide vscode` is used (VS Code — same body as `.mdc` after frontmatter) |
| `ide-files/abd-information-architecture.prompt.md` | `.cursor/commands/` (Cursor slash command); also `.github/prompts/` under VS Code |

---

<!-- execute_rules:bundle_rules:begin -->
<!-- Rule prose is generated from rules/*.md — edit rules, then run:
     python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/user-experience-design/abd-information-architecture
-->
<!-- execute_rules:bundle_rules:end -->
