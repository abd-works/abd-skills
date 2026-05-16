# Initial information architecture — {{SCOPE}}

> **Companion to** `docs/ux/initial-ia.tldr` / `initial-ia.svg`. This markdown is the structured spec for the canvas. Author or update **this file first**, then drive the canvas from it. After the canvas is updated, sync any change back into this file so the two never diverge.

## Metadata

| Field | Value |
| --- | --- |
| Scope | {{SCOPE}} (e.g. `Increment 1`, `Crowd Manager Epic`, `Sprint 4`) |
| Story map | {{STORY_MAP_PATH}} |
| Ubiquitous language | {{UBIQUITOUS_LANGUAGE_PATH}} |
| Canvas (`.tldr`) | `docs/ux/initial-ia.tldr` |
| Canvas (`.svg`) | `docs/ux/initial-ia.svg` |
| Last canvas update | {{ISO_DATE}} |

## Description

{{ONE_PARAGRAPH_DESCRIPTION}}

One paragraph: what the IA covers, what conversation it supports, who reads it.

---

## Navigation

### Site map — screens

One block per user-visible screen. Names use UX terms for structural pieces and domain term names (linked) for subject matter. System stories do not get their own block — they appear inside the screen that surfaces them, under "Groups system stories".

Transitions are recorded inside each screen block as **From** (incoming) and **To** (outgoing) lists. Triggers use a UX term when structural, or a domain concept name (linked) when domain-specific. Every outgoing entry on one screen has a matching incoming entry on the destination screen.

Content lives **inside** the screen block when it is specific to that one screen. When the same content type appears on more than one screen, factor it out into [Content types (shared across screens)](#content-types-shared-across-screens) below and reference it from each screen.

#### {{SCREEN_NAME}}

- **Description:** {{ONE_LINE_DESCRIPTION}}
- **Source:** [{{DOMAIN_OR_STORY_NAME}}]({{LINK_TO_SOURCE}})
- **Layout** — the standard template the screen follows in conventional layout terms. Examples: `header + body + footer (single column)`; `header + left panel + body (2-column)`; `header + 3-column body (left nav | content | detail panel)`; `header + body grid (2 columns × 2 rows)`; `modal dialog (centered, single column)`. Name the regions in the next bullet against the slots in this layout.
  - {{LAYOUT_DESCRIPTOR}}
- **From (incoming transitions):**
  - from {{SOURCE_SCREEN}} — trigger: {{TRIGGER}}
- **To (outgoing transitions):**
  - to {{DESTINATION_SCREEN}} — trigger: {{TRIGGER}}
- **Regions and content** — for each region (UX term), say which **slot** of the layout above it occupies, name the content type that lives in it (with link), the relationship shown, and either inline content-type detail (if specific to this screen) or a reference to the shared block. Every slot in the layout is filled by exactly one region; every region maps to exactly one slot.

  **If a region has tabs, modes, or sub-screens:** decompose it fully — do NOT write "tabs: X, Y, Z" and stop. Each tab state is a named sub-region block with its own data shown, key actions, domain terms, and stories. Use the sub-region block pattern below.

  - **{{REGION_1}}** — slot: `{{LAYOUT_SLOT}}` (e.g. `header`, `left panel`, `body`, `body row 1`, `footer`) — [{{CONTENT_TYPE_NAME}}]({{LINK}}) — relationship: {{HIERARCHY / COLLECTION / NAVIGATION}}
    - *Specific to this screen* — data shown: {{...}}; key actions: {{...}}
    - *Shared* — see [Content types (shared) → {{CONTENT_TYPE_NAME}}](#content-types-shared-across-screens)

  - **{{TABBED_REGION}} — tab: {{TAB_NAME_1}}** — slot: `body (tab: {{TAB_NAME_1}})` — [{{CONTENT_TYPE}}]({{LINK}}) — relationship: {{...}}
    - Sub-regions:
      - **{{SUB_REGION_A}}** — data shown: {{...}}; key actions: {{...}}
      - **{{SUB_REGION_B}}** — data shown: {{...}}; key actions: {{...}}
    - Domain terms: {{TERM_1}}, {{TERM_2}}, …
    - Stories: {{STORY_NAME_1}}, {{STORY_NAME_2}}, …

  - **{{TABBED_REGION}} — tab: {{TAB_NAME_2}}** — slot: `body (tab: {{TAB_NAME_2}})` — …
    - Sub-regions: …
    - Domain terms: …
    - Stories: …

  <!-- repeat the tab block for every tab state; never collapse multiple tabs into one block -->

  - **{{REGION_N}}** — slot: `{{LAYOUT_SLOT}}` — …
- **In-scope user stories (names + links):**
  - [{{USER_STORY_TITLE}}]({{LINK}})
- **Groups system stories (names + links):**
  - [{{SYSTEM_STORY_TITLE}}]({{LINK}})

<!-- duplicate the #### block for each screen -->

### Navigational components

Persistent surfaces that carry navigation across screens (menus, primary navigation, sidebars, headers, footers, breadcrumbs, link groups). Named in UX terms, with the screens or content types they link to.

#### {{COMPONENT_NAME}} ({{UX_TYPE}})

- **Appears on:** {{SCREEN_NAMES}}
- **Links to:** {{SCREEN_OR_CONTENT_TYPE_NAMES_WITH_LINKS}}
- **Notes:** {{ONE_LINE}}

<!-- duplicate the #### block for each component -->

---

## Content types (shared across screens)

Only content types referenced by **more than one** screen are described here. Single-screen content types stay inline inside their screen block under "Regions and content".

#### {{CONTENT_TYPE_NAME}}

- **Source:** [{{DOMAIN_TERM}}]({{LINK_TO_UL}})
- **Used on:** {{SCREEN_NAME_1}}, {{SCREEN_NAME_2}}
- **Hierarchy / collections:** {{e.g. character belongs to crowd; crowd is a collection of character}}
- **Preliminary labels and tags:** {{LABELS}}
- **Key actions:** {{ACTION_1}}, {{ACTION_2}}, {{ACTION_3}}

<!-- duplicate the #### block for each shared content type -->

---

## Change log

Append a row whenever the canvas changes, in either direction (canvas → md or md → canvas).

| Date | Direction | Summary |
| --- | --- | --- |
| {{ISO_DATE}} | initial | First draft. |
