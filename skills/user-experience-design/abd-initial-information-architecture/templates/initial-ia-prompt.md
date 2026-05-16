# initial-ia prompt template

Fill the slots between `{{` and `}}` from `docs/ux/initial-ia.md`, then paste the filled prompt into the abd-canvas chat panel.

---

```
Clear the canvas. Draw the initial information architecture for {{SCOPE}}.

Each screen is a large rectangle with its name as a bold title at the top.
Inside each screen, draw subdivided rectangles for each layout region — like a wireframe skeleton.
No bullet lists. No prose descriptions of layout. Just boxes with short labels.

WHITESPACE RULES (apply everywhere)
- 100px gap between screen boxes
- 14px internal padding inside every region band so labels never touch a border
- 8px gap between stacked horizontal bands inside a screen
- Arrow labels float above or below the arrow line with clear space around them
- Nothing packed tight — every element breathes

---

SCREENS

{{SCREEN_BLOCKS}}

Each screen block follows this pattern:

  SCREEN: [name]
  Size hint: [rough px dimensions]
  Layout: [layout descriptor, e.g. "header + left panel + body (2-column) + footer"]

  Draw subdivided bands/columns inside the screen box matching the layout.
  Label each band/column with its region name.
  Do not write "region:" or "slot:" — just the label inside the box.

---

CANVAS LAYOUT — SITE MAP CONVENTION
- Primary / straight-through flow: arrange screens LEFT TO RIGHT across the canvas, in the order a user moves through them on the main path.
- Optional flows, branch screens, and sub-screens: arrange ABOVE OR BELOW the main left-to-right row, like a classic site map tree. A screen that branches off the main flow sits directly above or below the screen it branches from, connected by a vertical or diagonal arrow.
- Never place an optional or branch screen to the right of the screen it branches from — that implies it is the next step in the primary flow when it is not.

TRANSITIONS
- Primary (left-to-right) arrows: straight horizontal arrows pointing right.
- Optional / branch arrows: vertical or diagonal arrows pointing up or down to the branch screen.
- Return / back transitions: curved arrows that arc back over the main row.
- Every arrow carries a short trigger label.

{{TRANSITIONS}}

---

NAVIGATIONAL COMPONENTS
Draw as a small separate panel beside the screens.

{{NAVIGATIONAL_COMPONENTS}}

---

CONTENT TYPES
Draw as a separate panel — one box per content type, with labeled hierarchy lines between them.
Inside each box show the key actions as a short verb list.

{{CONTENT_TYPES_WITH_ACTIONS}}

---

GROUPED SYSTEM STORIES
Inside each affected screen box, add a small note area at the bottom labeled "system stories:" with the story names.

{{GROUPED_SYSTEM_STORIES}}

---

DRAW THIS NOW
- Every screen is a drawn rectangle subdivided into region bands/columns
- Every transition is a directed labeled arrow
- Every content type is a box with hierarchy lines and a verb list
- Primary flow screens left to right; optional/branch screens above or below
- UX terms on structure; domain term names on subject matter
- No controls. No copy. No acceptance criteria.
```

---

## Slot reference

| Slot | Source | Notes |
| --- | --- | --- |
| `{{SCOPE}}` | user-supplied | e.g. `Full Application`, `Increment 1`, `Crowd Manager Epic`. |
| `{{SCREEN_BLOCKS}}` | `initial-ia.md` Navigation → screens | One block per screen: name, size hint (modal ~400×500, app window ~1200×700, full-screen ~1400×800), layout descriptor, and region list. **Placement:** primary-flow screens left to right; branch/optional screens above or below the screen they branch from. |
| `{{TRANSITIONS}}` | `initial-ia.md` Navigation → screens → From/To lists | Lines like `screen-a ──► screen-b  label: "trigger"`. Primary-flow arrows horizontal/right. Branch arrows vertical/diagonal. Return/back transitions as curved arcs. Fill from outgoing entries only to avoid duplicates. |
| `{{NAVIGATIONAL_COMPONENTS}}` | `initial-ia.md` Navigation → Navigational components | One entry per component: name, appears on (screen), links to (screens or regions). |
| `{{CONTENT_TYPES_WITH_ACTIONS}}` | `initial-ia.md` Content types (shared) + inline screen content | One block per type: name, hierarchy/collection relationships (as labeled lines), key actions (verb list inside the box). |
| `{{GROUPED_SYSTEM_STORIES}}` | `initial-ia.md` screens → Groups system stories | One line per screen: `screen-name: story-title · story-title · …` |
