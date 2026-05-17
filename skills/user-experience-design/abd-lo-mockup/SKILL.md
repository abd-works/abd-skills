---
name: abd-lo-mockup
description: >-
  Precision pass after the initial IA — specify exact controls, interactions,
  and states for any scope (full site, flow, epic, story), drawn in Draw.io
  as a lo-fi wireframe and saved as a versioned .drawio artifact.
---
# abd-lo-mockup

## Purpose

The initial IA established the screen inventory, regions, and story coverage. The lo-fi mockup is the next precision pass: it locks down **exactly which control renders each field**, **exactly what interactions are available in each state**, and **exactly what the user sees and does** — without yet committing to visual design. Every input becomes a specific control type (text field, dropdown, checkbox). Every action becomes a positioned button with a primary/secondary weight. Every conditional state (validation error, empty list, disabled control) is explicitly placed. This skill packages that pass: take one IA screen, resolve its AC and domain terms, build a `drawio-mockup.mjs` state file, generate the `.drawio` wireframe, and save it — so interaction decisions are made deliberately and traceable, not invented during implementation.

**Critical principle:** The lo-fi mockup must faithfully reproduce the production UI structure as shown in design images. Do NOT substitute tables for trees, do NOT use fields when a listbox is called for, do NOT flatten hierarchical views into flat lists. Match the design.

---

## When to use this skill

Load this skill when **any** of the following apply:

- You have a screen specification (regions, stories, domain terms) and you need to decide **exactly which control renders each field, which button is primary, and what conditional states exist**.
- You are about to hand a screen to a developer and the interaction model is still implicit — control types, validation behaviour, empty states, and button weights have not been made explicit.
- A built screen has interaction decisions that were never consciously made — you want to surface them, validate them against acceptance criteria, and lock them down.
- You want to review a screen layout against its acceptance criteria at the **interaction level** — missing error states, wrong control types, actions with no AC backing.

---

## What is a lo-fi mockup

A **lo-fi mockup** is a structural wireframe that makes interaction decisions explicit. Its scope is whatever the team needs to validate — the entire application, a section, a flow, an epic, or a single story. We tend to work in small increments (a story, a screen, a feature) not because the tool demands it but because we want to see and validate what we're building before committing further.

It shows:

- **IA regions** as containers — unchanged from the structural IA, not invented here.
- **Exact control types** for each field: tree view, listbox, text input, dropdown, checkbox, radio, textarea — not generic "field" boxes.
- **Exact button placement and weight**: primary vs secondary, icon buttons vs text buttons, which actions are available at rest vs after selection.
- **Conditional states**: validation error placeholders, empty list states, disabled controls, selection highlighting, clipboard states (ghost/dimmed for cut, chain icons for linked) — placed where they appear, labelled in domain terms.
- **Exact interactions implied by each action**: what triggers, what changes, what the user does next.
- **Hierarchical structure**: tree views rendered with proper indentation, expand/collapse chevrons, icons per node type — not flattened into tables.

It also shows, per screen:

- **In-scope user stories** — listed alongside or below the wireframe, matching the initial IA's per-screen story list.
- **Domain terms** — the UL terms visible on this screen, listed alongside or below the wireframe, matching the initial IA's per-screen domain term list.

These lists appear in the drawio diagram as annotation boxes beside each screen, so the wireframe is self-contained and reviewable without flipping to the companion `.md` file.

It does not show colour, typography, spacing, or brand polish. It does not implement code. It does not invent controls that no AC or story justifies.

---

## Core concepts

### Source: initial IA

The screen spec lives in `docs/ux/initial-ia.md`. Each screen section defines:
- **Layout** (`sidebar`, `form`, `split-screen`, `modal`, `flyout`) — maps directly to `drawio-mockup.mjs` `layout` field.
- **Regions** with `slot`, `type`, `fields`, and `actions` — map directly to state JSON regions.
- **Stories** and **domain terms** — determine which AC clauses and UL terms are in scope.

### Design image reference

Before building the state JSON, the agent MUST:
1. Read ALL design images for the relevant screens from `Design/` folders.
2. Catalog what UX elements are actually shown: tree views, listboxes, toolbars with icon buttons, context menus, filter bars, etc.
3. Note indentation levels, expand/collapse state, icon types, selection behaviour, and groupings.
4. The state JSON and wireframe MUST match these design images — no reinterpretation, no substituting simpler controls.

### UI element types

| State type | Renders as | State keys |
| --- | --- | --- |
| `tree` | hierarchical node list with indent, expand/collapse, icons | `nodes[].{label, indent, expanded, icon, selected}` |
| `listbox` | selectable item list (not a data grid) | `items[].{label, icon, selected, dimmed, badge}` |
| `context-menu` | right-click popup menu with grouped actions | `groups[].items[].{label, shortcut}` |
| `toolbar-icons` | horizontal row of icon-style square buttons | `buttons[].{icon, tooltip, active}` |
| `filter-bar` | text input with search/clear affordance | `placeholder`, `value` |
| `browse-panel` | grid of category icon buttons | `categories[].{label, icon}` |
| `form` | label-input pairs + button row | `fields[].input`, `buttons[]` |
| `list` | column headers + data rows + action buttons | `columns[]`, `rows`, `actions[]` |
| `nav-tabs` | horizontal tab strip | `tabs[].label`, `tabs[].active` |
| `toolbar` | horizontal text button row (header/footer) | `buttons[]` |
| `button-bar` | horizontal button row (inline) | `buttons[]` |
| `chrome` | plain labelled band (dimmed panels) | `name` |

### Tree state format

```json
{
  "type": "tree",
  "name": "character tree",
  "nodes": [
    { "label": "All Characters", "indent": 0, "expanded": true, "icon": "group" },
    { "label": "Crowd 1", "indent": 1, "expanded": true, "icon": "crowd" },
    { "label": "Character 1", "indent": 2, "icon": "character" },
    { "label": "Character 2", "indent": 2, "icon": "character", "selected": true },
    { "label": "Crowd 2", "indent": 1, "expanded": false, "icon": "crowd" }
  ]
}
```

**Icons:** `group` (all), `crowd` (multi-person), `character` (single person), `folder`, `file`, `ability`, `movement`, `power`, `fx`, `sound`, `sequence`
**Indent:** integer 0–N indicating nesting depth
**Expanded/collapsed:** `expanded: true` renders ▼, `expanded: false` renders ▶, omit for leaf nodes

### Listbox state format

```json
{
  "type": "listbox",
  "name": "active roster",
  "items": [
    { "label": "Character 1", "icon": "character" },
    { "label": "Character 2", "icon": "character", "selected": true },
    { "label": "Character 3", "icon": "character", "dimmed": true }
  ]
}
```

**Dimmed:** indicates cut-to-clipboard state (ghost). **Selected:** highlighted item.

### Context menu state format

```json
{
  "type": "context-menu",
  "name": "character actions",
  "groups": [
    { "items": [
      { "label": "New", "shortcut": "Ctrl+N" },
      { "label": "Edit", "shortcut": "Ctrl+E" },
      { "label": "Delete", "shortcut": "Del" },
      { "label": "Save", "shortcut": "Ctrl+S" }
    ]},
    { "items": [
      { "label": "Cut", "shortcut": "Ctrl+X" },
      { "label": "Clone", "shortcut": "Ctrl+C" },
      { "label": "Link", "shortcut": "Ctrl+L" },
      { "label": "Paste", "shortcut": "Ctrl+V" }
    ]},
    { "items": [
      { "label": "Spawn", "shortcut": "Alt+S" },
      { "label": "Place", "shortcut": "Alt+P" }
    ]}
  ]
}
```

Groups are separated by horizontal dividers.

### Toolbar-icons state format

```json
{
  "type": "toolbar-icons",
  "name": "explorer toolbar",
  "buttons": [
    { "icon": "new-file", "tooltip": "New" },
    { "icon": "cut", "tooltip": "Cut" },
    { "icon": "copy", "tooltip": "Copy" },
    { "icon": "paste", "tooltip": "Paste" },
    { "icon": "add-crowd", "tooltip": "Add Crowd", "active": true },
    { "icon": "edit", "tooltip": "Edit" }
  ]
}
```

Rendered as square icon buttons in a row — not pill-shaped text buttons.

### Filter-bar state format

```json
{
  "type": "filter-bar",
  "name": "character filter",
  "placeholder": "Search characters…",
  "value": "Spyder"
}
```

### Browse-panel state format

```json
{
  "type": "browse-panel",
  "name": "browse characters",
  "categories": [
    { "label": "All Characters", "icon": "group" },
    { "label": "Heroes", "icon": "hero" },
    { "label": "Villains", "icon": "villain" }
  ]
}
```

### Field input types

| Value | Renders as |
| --- | --- |
| `text` | empty bordered rectangle |
| `textarea` | taller bordered rectangle |
| `dropdown` | rectangle with ▾ suffix and first option |
| `checkbox` | `☐ Label` inline |
| `radio` | `○ Label` inline |

### Domain terms — verbatim, screen-scoped

Only terms whose stories appear on this screen may appear. Copy verbatim from the ubiquitous-language file.

### Acceptance criteria — verbatim

Placed beside the wireframe, character-for-character. No rewording, shortening, or paraphrasing.

---

## The shape of a good lo-fi state file

```json
{
  "target": "docs/ux/lo-fi/character-explorer.drawio",
  "screens": [{
    "name": "character explorer",
    "layout": "sidebar",
    "col": 0, "row": 0,
    "regions": [
      {
        "name": "explorer toolbar",
        "slot": "header",
        "type": "toolbar-icons",
        "buttons": [
          { "icon": "new-file", "tooltip": "New" },
          { "icon": "cut", "tooltip": "Cut" },
          { "icon": "copy", "tooltip": "Copy" },
          { "icon": "paste", "tooltip": "Paste" },
          { "icon": "add-crowd", "tooltip": "Add Crowd" },
          { "icon": "add-character", "tooltip": "Add Character" },
          { "icon": "edit", "tooltip": "Edit" }
        ]
      },
      {
        "name": "character filter",
        "slot": "panel",
        "type": "filter-bar",
        "placeholder": "Search characters…",
        "value": "Spyder"
      },
      {
        "name": "character tree",
        "slot": "panel",
        "type": "tree",
        "nodes": [
          { "label": "All Characters", "indent": 0, "expanded": true, "icon": "group" },
          { "label": "Crowd 1", "indent": 1, "expanded": true, "icon": "crowd" },
          { "label": "Character 1", "indent": 2, "icon": "character" },
          { "label": "Character 2", "indent": 2, "icon": "character" },
          { "label": "Crowd 2", "indent": 1, "expanded": false, "icon": "crowd" }
        ]
      },
      {
        "name": "tab bar",
        "slot": "body",
        "type": "nav-tabs",
        "tabs": [
          { "label": "Identities", "active": true },
          { "label": "Abilities" },
          { "label": "Movements" }
        ]
      },
      {
        "name": "identity list",
        "slot": "body",
        "type": "listbox",
        "items": [
          { "label": "Identity 1", "icon": "identity" },
          { "label": "Identity 2", "icon": "identity", "selected": true },
          { "label": "Identity 3", "icon": "identity" }
        ]
      }
    ]
  }],
  "connections": []
}
```

---

## Rendering approach: CLI vs AI-crafted XML

The skill supports two rendering paths. Choose based on screen complexity.

### CLI path (drawio-mockup.mjs)

Use the CLI when the screen contains **only** these element types:
- Forms, lists (tabular), nav-tabs, toolbars, button-bars, chrome
- AND the new types: tree, listbox, context-menu, toolbar-icons, filter-bar, browse-panel

The CLI generates correct drawio XML programmatically from the state JSON.

```powershell
node "C:\dev\agilebydesign-skills\skills\user-experience-design\abd-lo-mockup\scripts\drawio-mockup.mjs" `
  save `
  --state "docs/ux/lo-fi/<screen-slug>-state.json" `
  --out   "docs/ux/lo-fi/<screen-slug>.drawio"
```

### AI-crafted XML path

Use AI-crafted drawio XML when:
- The screen has complex compositions not expressible in state JSON (overlapping panels, drag handles, unusual nesting)
- The design image shows layouts that the CLI grid system cannot reproduce
- You need pixel-level fidelity to a specific design image

Process:
1. Start from a screen-template `.drawio` fragment (from `screen-templates/`)
2. Read the production design images to understand exact layout
3. Hand-craft mxGraph XML cells for each element
4. Use the mxGraph XML patterns documented below

### mxGraph XML patterns for UX elements

**Tree node (leaf):**
```xml
<mxCell value="    Character 1" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;spacingLeft=20;" vertex="1" parent="PARENT">
  <mxGeometry x="X" y="Y" width="W" height="22" as="geometry"/>
</mxCell>
```

**Tree node (expanded parent — ▼):**
```xml
<mxCell value="▼ Crowd 1" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;fontStyle=1;spacingLeft=INDENT;" vertex="1" parent="PARENT">
  <mxGeometry x="X" y="Y" width="W" height="22" as="geometry"/>
</mxCell>
```

**Tree node (collapsed — ▶):**
```xml
<mxCell value="▶ Crowd 2" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;fontStyle=1;spacingLeft=INDENT;" vertex="1" parent="PARENT">
  <mxGeometry x="X" y="Y" width="W" height="22" as="geometry"/>
</mxCell>
```

**Listbox item (normal):**
```xml
<mxCell value="Character 1" style="whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e0e0e0;fontSize=10;verticalAlign=middle;align=left;spacingLeft=8;" vertex="1" parent="PARENT">
  <mxGeometry x="X" y="Y" width="W" height="26" as="geometry"/>
</mxCell>
```

**Listbox item (selected):**
```xml
<mxCell value="Character 2" style="whiteSpace=wrap;html=1;fillColor=#c8e6c9;strokeColor=#4caf50;fontSize=10;fontStyle=1;verticalAlign=middle;align=left;spacingLeft=8;" vertex="1" parent="PARENT">
  <mxGeometry x="X" y="Y" width="W" height="26" as="geometry"/>
</mxCell>
```

**Context menu container:**
```xml
<mxCell value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="X" y="Y" width="180" height="H" as="geometry"/>
</mxCell>
```

**Context menu item:**
```xml
<mxCell value="Edit          Ctrl+E" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;fontFamily=monospace;" vertex="1" parent="PARENT">
  <mxGeometry x="X" y="Y" width="170" height="22" as="geometry"/>
</mxCell>
```

**Context menu separator:**
```xml
<mxCell value="" style="line;strokeWidth=1;strokeColor=#cccccc;fillColor=none;" vertex="1" parent="PARENT">
  <mxGeometry x="X" y="Y" width="170" height="1" as="geometry"/>
</mxCell>
```

**Story list annotation (placed below or beside the screen):**
```xml
<mxCell value="Stories&#xa;─────────────────&#xa;• Story Title 1&#xa;• Story Title 2&#xa;• Story Title 3" style="text;html=0;align=left;verticalAlign=top;fontSize=10;fontFamily=monospace;fillColor=#fffde7;strokeColor=#f9a825;rounded=1;arcSize=8;spacingLeft=6;spacingTop=4;spacingRight=6;spacingBottom=4;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="X" y="Y" width="260" height="H" as="geometry"/>
</mxCell>
```

**Domain terms annotation (placed below the story list):**
```xml
<mxCell value="Domain terms&#xa;─────────────────&#xa;• term 1&#xa;• term 2&#xa;• term 3" style="text;html=0;align=left;verticalAlign=top;fontSize=10;fontFamily=monospace;fillColor=#e8f5e9;strokeColor=#4caf50;rounded=1;arcSize=8;spacingLeft=6;spacingTop=4;spacingRight=6;spacingBottom=4;whiteSpace=wrap;" vertex="1" parent="1">
  <mxGeometry x="X" y="Y" width="260" height="H" as="geometry"/>
</mxCell>
```

Annotation boxes use light yellow (stories) and light green (domain terms) to distinguish them from the wireframe elements. Place them below or to the right of the screen they annotate.

**Icon toolbar button (square):**
```xml
<mxCell value="✂" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#999999;fontSize=14;verticalAlign=middle;align=center;" vertex="1" parent="PARENT">
  <mxGeometry x="X" y="Y" width="28" height="28" as="geometry"/>
</mxCell>
```

---

## Build

**Goal:** Agree scope, reference design images, map in-scope IA screens to a state JSON, run `drawio-mockup.mjs`, save the wireframe, and write a `lo-fi.md` spec alongside it.

1. **Agree scope.** Decide which screens, stories, or epics are in scope for this mockup pass — a single story, a flow across several screens, an epic, or the full application. Scope is a team decision, not a tool constraint. Small increments (a story, a feature) are preferred because they let the team see and react before committing further.

2. **Resolve inputs.** Confirm: path to `docs/ux/initial-ia.md`, path to the UL file, path to the AC file, and the agreed set of screens or stories in scope. Ask for any that are missing.

3. **Reference design images.** Before building any state, read ALL design images in `Design/` folders that relate to the screens in scope. For each screen, catalog:
   - What panels/regions are visible
   - What UX element type each region uses (tree, listbox, toolbar-icons, etc.)
   - Indentation levels in tree views
   - Icon types per node
   - Groupings in context menus
   - Selection/active/clipboard states shown
   
   Record this catalog in the "Design reference" section of `lo-fi.md`.

4. **Read the in-scope screens from the initial IA.** For each screen, read its layout, regions (slot, type, fields, actions), stories, and domain terms.

5. **Collect in-scope stories and AC.** From the story map and AC file, gather stories and criteria for the agreed scope only.

6. **Build the state JSON.** Map each IA region to a state JSON region using the correct element type — trees for hierarchical data, listboxes for selectable lists, toolbar-icons for icon button bars:
   - IA `layout` → state `layout`
   - IA `slot` → state `slot`
   - IA region `type` → state `type` — **choose the type that matches the design image**, NOT the simplest available
   - IA region `fields` → state `columns` (for list), `fields[].label` (for form), `nodes[]` (for tree), `items[]` (for listbox)
   - IA region `actions` → state `actions[].label` (for list), `buttons[].label` (for form), `groups[].items[]` (for context-menu)
   - IA `transitions out` → state `connections[]`

7. **Generate the wireframe.**

```powershell
node "C:\dev\agilebydesign-skills\skills\user-experience-design\abd-lo-mockup\scripts\drawio-mockup.mjs" `
  save `
  --state "docs/ux/lo-fi/<screen-slug>-state.json" `
  --out   "docs/ux/lo-fi/<screen-slug>.drawio"
```

8. **Write `lo-fi.md` alongside the wireframe.** The markdown spec contains: screen name, source paths, layout, design reference catalog, regions with affordance traces (each affordance → AC clause or domain term), in-scope stories, domain term excerpt (verbatim), and AC (verbatim). The `.drawio` is never authored without the `.md` spec.

9. **Add story and domain term annotations to the drawio.** For each screen in the drawio, add two annotation boxes positioned below or beside the screen:
   - **Stories box** (light yellow `#fffde7`): lists all in-scope user stories for that screen, one bullet per story, matching the initial IA's per-screen story list.
   - **Domain terms box** (light green `#e8f5e9`): lists all UL terms visible on that screen, one bullet per term, matching the initial IA's per-screen domain term list.
   These make the wireframe self-contained for review without cross-referencing the `.md` file.

10. **Validate.** Walk the wireframe and confirm every check below passes — with special attention to ensuring trees are trees (not tables), listboxes are listboxes (not forms), and icon toolbars are icon toolbars (not text button rows).

11. **Sync.** If the diagram was edited manually in Draw.io, update the state JSON and `lo-fi.md` to match. Append to the change log.

**Outputs:**
- `docs/ux/lo-fi/<screen-slug>-state.json` — source of truth for the wireframe
- `docs/ux/lo-fi/<screen-slug>.drawio` — the generated wireframe (open in VS Code Draw.io extension)
- `docs/ux/lo-fi/<screen-slug>.md` — structured spec with verbatim AC and domain terms

---

## CLI reference

```
drawio-mockup.mjs save --state <state.json> --out <file.drawio>
drawio-mockup.mjs init --out <state.json>
```

### Layouts

| Layout | Columns (slot → width) |
| --- | --- |
| `sidebar` | panel 33% · body 67% |
| `split-screen` | left 50% · right 50% |
| `form` | body 100% |
| `modal` | body 100% (rounded border) |
| `flyout` | body 65% · panel 35% |
| `stack` | body 100% |

### Grid positioning

Use `col` and `row` integers on each screen to arrange screens in a grid:
- **Linear flow** (user must pass through): increment `col` left to right.
- **Optional branch** (user may choose): increment `row` top to bottom within the same `col`.

This matches the convention established in `drawio-ux.mjs` (the IA diagram CLI).

---

## Validate

Walk the wireframe and confirm:

- Every region in the wireframe matches a region from the initial IA for this screen.
- Every label is a UL term verbatim or copy from an AC clause.
- Every acceptance criterion for an in-scope story is present in `lo-fi.md`, verbatim.
- No story or domain term from another screen appears.
- Every affordance traces to an AC clause or a UL term (documented in the `Trace` column of `lo-fi.md`).
- `<screen-slug>-state.json` and `<screen-slug>.drawio` are in sync (regenerating from state produces the same file).
- **Trees are trees** — hierarchical data uses `type: "tree"` with indent levels, NOT `type: "list"` with columns.
- **Listboxes are listboxes** — selectable item lists use `type: "listbox"`, NOT `type: "form"` with fields.
- **Icon toolbars are icon toolbars** — icon button rows use `type: "toolbar-icons"`, NOT `type: "toolbar"` with text labels.
- **Context menus match the design** — grouped actions with shortcuts, not flattened button bars.
- **Story and domain term annotations present** — every screen in the drawio has a yellow stories box and green domain terms box beside or below it, matching the initial IA's per-screen lists.

---

## Deploy

```powershell
cd C:\dev\agilebydesign-skills
.\scripts\deploy-skills.ps1 -ide cursor -Force
```

| File | Deploy target |
| --- | --- |
| `ide-files/abd-lo-mockup.mdc` | `.cursor/rules/` |
| `ide-files/abd-lo-mockup.prompt.md` | `.cursor/commands/` |

---

<!-- execute_rules:bundle_rules:begin -->
<!-- Rule prose is generated from rules/*.md — edit rules, then run:
     python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/user-experience-design/abd-lo-mockup
-->
<!-- execute_rules:bundle_rules:end -->
