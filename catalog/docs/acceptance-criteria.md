# Domain Language — ABD Foundry Catalog Kanban

_Shared vocabulary for the kanban filtering and navigation behavior._

Scope: The interactive kanban surface — family filter, skills expand/collapse, supporting section, and skill page navigation.

**Terms**:
- **Skill**
  - **skill** — a practice capability a team can apply; the base concept for all skill types
  - **practice skill** — a *skill* that belongs to a *skill family*; either staged or supporting
  - **stage skill** — a *practice skill* that has a *stage*; appears in the board columns
  - **supporting skill** — a *practice skill* with no *stage*; appears in the supporting section
  - **other skill** — a *skill* with no *skill family* but with a *stage*; appears under the "other" row
  - **skill navigated to** — the *skill* whose detail page is currently open
  - **skill family** — a named grouping of *practice skills* (e.g. story-driven-delivery); either *active* or *inactive*
  - **active** — a *skill family* the user has ticked; its *stage skills* and *supporting skill* header chip are shown
  - **inactive** — a *skill family* that is unticked; its *stage skills* are hidden and its *supporting skill* header chip is never shown
  - **stage** — a named delivery phase (Shaping, Discovery, Exploration, Specification, Engineering); organises *stage skills* into columns
  - **kanban** — the board surface that organises all *skills* by *skill family* and *stage*

---

# Core Domain

## Skill

*Skill* is a practice capability a team can apply at a point in delivery. Every *skill* is either a *practice skill* (owned by a *skill family*) or an *other skill* (no family, but still placed in a *stage*). A *skill family* groups its *practice skills* and is either *active* or *inactive* on the *kanban* — that state controls which *skills* are visible and where.

### skill

- is the base concept for *practice skill*, *other skill*, and *skill navigated to*
- belongs to one *kanban*; is placed in a position determined by its type, *skill family*, and *stage*
- carries a link to its detail page; becomes the *skill navigated to* when that page is open

### practice skill *is a type of* skill

- belongs to exactly one *skill family*
- is either a *stage skill* (has a *stage*) or a *supporting skill* (has no *stage*)

### stage skill *is a type of* practice skill

- belongs to one *stage*; appears as a ticket in that *stage* column under its *skill family* row on the *kanban*
- is visible when its *skill family* is *active* and the *kanban* is expanded
- shows as a header chip only (no ticket body) when the *kanban* is expanded and its *skill family* is *inactive*

### supporting skill *is a type of* practice skill

- has no *stage*; lives in the supporting section below the *kanban* board
- its header chip is visible only when its *skill family* is *active*
- **Invariant:** *supporting skill* header chip visibility is controlled by *active*/*inactive* state only — expand/collapse has no effect

### other skill *is a type of* skill

- belongs to no *skill family*; has a *stage* and appears in the board under the "other" row
- follows the same expand/collapse visibility rules as *stage skill*

### skill navigated to *is a type of* skill

- the specific *skill* whose detail page is currently open
- causes its *skill family* to be set as *active* when the *kanban* loads on that detail page

### skill family

- groups one or more *practice skills* (both *stage skills* and *supporting skills*)
- is *active* when ticked by the user; is *inactive* when unticked
- **Invariant:** a *skill family* header chip in the practice rail is always visible whether *active* or *inactive*

### active

- is a property of *skill family* — the ticked state
- causes *stage skills* to appear in the board and the *supporting skill* header chip to appear in the supporting section

### inactive

- is a property of *skill family* — the unticked state
- hides *stage skills* from the board when collapsed; shows them as header chips only when expanded
- hides *supporting skill* header chip unconditionally regardless of expand/collapse

### stage

- names a phase of the delivery lifecycle; organises *stage skills* and *other skills* into columns on the *kanban*
- intersects with *skill family* — every *stage* column holds the *stage skills* for every *skill family*

### kanban

- organises all *skills* by *skill family* row and *stage* column
- shows all *skill family* rows when no *skill family* is *active*; filters to *active* families when one or more are ticked
- **Invariant:** all *skill family* header chips in the practice rail are always visible regardless of active/inactive or expand/collapse state

#### Decisions made

- *Skill* is the single KA — the domain is small; *kanban*, *skill family*, and *stage* are all subordinate concepts that only make sense in relation to *skill*.
- *Supporting skill* earns its own concept block for its distinct invariant (expand/collapse independence).
- *Active* and *inactive* are properties of *skill family*, not subtypes — they differ by boolean state only.
- *Other skill* is a direct subtype of *skill*, not *practice skill* — it has no *skill family*.

#### References

**Ref — working session**
Source: catalog/acceptance-criteria.md
Locator: working session Jun 11 2026
Extract: whole

---

# Acceptance Criteria — ABD Foundry Catalog Kanban

Source: observed behavior, stated requirements, and working session — Jun 11 2026.

---

## Story: View Kanban With No Filter Selected

**Story type:** user

### Domain terms

- *Kanban Surface* — the `.foundry-kanban-surface` element; the container for the full kanban UI (hub or skill page)
- *Practice Rail* — left column listing all *Family Header Chips*
- *Family Header Chip* — clickable chip for a practice family (e.g. story-driven-delivery); ticked or unticked to filter
- *Board Row* — a horizontal row of skill tickets for one practice family across all stage columns
- *Stage Column* — a vertical column for a delivery stage (Shaping, Discovery, Exploration, Specification, Engineering)
- *Skills Toggle* — button that expands or collapses individual skill rows in the board
- *Idle State* — no family filter active; all rows visible

### Acceptance criteria

1. **WHEN** the *Kanban Surface* loads with no saved filter
   **THEN** all *Family Toggle* buttons appear in the *Practice Rail*
   **AND** all *Board Rows* are visible across all *Stage Columns*
   **AND** the surface is in *Idle State*
   **Evidence:** stated requirement — hub default shows all families

2. **WHEN** *Skills Toggle* is collapsed and a family filter is active
   **THEN** only the *Selected Family* header chips are visible in the board area
   **AND** non-selected family rows are hidden
   **Evidence:** stated requirement — collapsed shows only selected family chips

3. **WHEN** *Skills Toggle* is collapsed and no family filter is active
   **THEN** no *Board Rows* are visible in the board area
   **Evidence:** collapsed idle state — nothing selected, nothing shown

4. **WHEN** *Skills Toggle* is expanded
   **THEN** ALL *Family Toggle* header chips are visible in the board area regardless of filter state
   **AND** individual skill tickets appear inside each visible *Board Row*
   **Evidence:** stated requirement — "expanded we always see all family chips selected or not"

---

## Story: Select Practice Family Filter

**Story type:** user

### Domain terms

- *Family Header Chip* — the clickable chip in the *Practice Rail* labelled with a family name (e.g. story-driven-delivery); ticked or unticked
- *Ticked Family* — a *Family Header Chip* the user has clicked to select; shows a selection indicator
- *Unticked Family* — a *Family Header Chip* that is not selected
- *Filter Active State* — one or more families ticked; surface has `foundry-skill-filter-active` class
- *Filtered Board Row* — a *Board Row* whose family matches a *Ticked Family*
- *Non-matching Board Row* — a *Board Row* whose family is not ticked; hidden when filter active
- *Supporting Section* — crosscut area below the board showing skills that support multiple families
- *Crosscut Row* — one family's row within the *Supporting Section*, with a header chip and skill chips
- *Crosscut Row Header Chip* — the family label chip at the start of a *Crosscut Row* in the *Supporting Section*; visibility is controlled exclusively by tick state
- *Auto-expanded Crosscut Row* — *Crosscut Row* whose skills are shown without a manual toggle click

### Acceptance criteria

1. **WHEN** the user clicks an *Unticked Family* header chip
   **THEN** that chip becomes a *Ticked Family* with a visible selection indicator
   **AND** all other *Family Header Chips* remain visible in the *Practice Rail*
   **BUT** no other *Family Header Chip* is hidden or collapsed
   **Evidence:** stated requirement — "ALL skills header chips should show"

2. **WHEN** the user clicks an already *Ticked Family* header chip
   **THEN** that chip becomes *Unticked*
   **AND** if no family remains ticked, the surface returns to *Idle State* and all *Board Rows* reappear
   **Evidence:** stated requirement — tick/untick toggles on and off

3. **WHEN** a family is ticked, the surface is in *Filter Active State*, and *Skills Toggle* is **collapsed**
   **THEN** only the *Ticked Family* header chip is visible in the board area
   **AND** *Non-matching Board Row* header chips are hidden
   **Evidence:** stated requirement — collapsed shows only ticked family chips

4. **WHEN** a family is ticked and the surface is in *Filter Active State*
   **AND** *Skills Toggle* is expanded
   **THEN** ALL *Family Header Chips* remain visible as row headers in the board area
   **AND** only the *Filtered Board Row* shows its individual skill tickets
   **AND** *Non-matching Board Rows* show their header chip but no skill tickets
   **Evidence:** stated requirement — "expanded we always see all family chips selected or not"

5. **WHEN** a family is ticked
   **THEN** the matching *Crosscut Row* in the *Supporting Section* is shown *Auto-expanded*
   **BUT** the *Crosscut Row Header Chip* for any non-ticked family is never shown — regardless of whether *Skills Toggle* is expanded or collapsed
   **Evidence:** stated requirement — supporting section family visibility is controlled by tick state only, not by expand/collapse

6. **WHEN** the user ticks a second *Family Header Chip* while one is already ticked
   **THEN** both families' *Board Rows* become visible
   **AND** both families' *Crosscut Rows* appear in the *Supporting Section*
   **Evidence:** multi-select tick behavior

---

---

## Story: Expand and Collapse Practice Skills

**Story type:** user

### Domain terms

- *Skills Toggle Button* — the `–` / `+` control in the top-left of the *Kanban Surface*
- *Expanded State* — individual skill tickets visible in each *Board Row*; `foundry-skills-expanded` class on surface
- *Collapsed State* — only family header chips visible in the board; `foundry-skills-collapsed` class on surface
- *Skills Expanded Preference* — persisted `sessionStorage` value remembering the last toggle state

### Acceptance criteria

1. **WHEN** the user clicks the *Skills Toggle Button*
   **THEN** the surface toggles between *Expanded State* and *Collapsed State*
   **AND** the *Skills Toggle Button* label and `aria-expanded` reflect the new state
   **Evidence:** existing hub expand/collapse behavior; tour step 2 animation

2. **WHEN** the surface enters *Expanded State*
   **THEN** skill tickets appear inside every visible *Board Row*
   **AND** the *Supporting Section* becomes visible with its *Crosscut Rows*
   **Evidence:** stated requirement — supporting section only shown when skills expanded

3. **WHEN** the surface enters *Collapsed State*
   **THEN** individual skill tickets are hidden in *Board Rows*
   **AND** the *Supporting Section* is hidden
   **Evidence:** stated requirement — collapse hides supporting section too

4. **WHEN** the user reloads or navigates back to the *Kanban Surface*
   **THEN** the surface restores the *Skills Expanded Preference* from the last session
   **Evidence:** `sessionStorage` persistence, `readSkillsExpandedPref()`

---

## Story: View Supporting Section Crosscut Skills

**Story type:** user

### Domain terms

- *Crosscut Skill Chip* — individual skill chip inside a *Crosscut Row*; white text, family-colored left border
- *Crosscut Row Header* — the family label chip at the start of a *Crosscut Row*; family-colored text, family-colored left border
- *Foundational Section* — a second crosscut area for skills that apply across all families; header is muted grey, chips are white

### Acceptance criteria

1. **WHEN** the *Supporting Section* is visible and no filter is active
   **THEN** all *Crosscut Rows* are shown, each with its *Crosscut Row Header* and *Crosscut Skill Chips* inline (wrapping left to right)
   **Evidence:** stated requirement — no filter shows all crosscut rows

2. **WHEN** a family filter is active and the *Supporting Section* is visible
   **THEN** only the *Crosscut Row* for the *Selected Family* is shown
   **AND** its *Crosscut Skill Chips* are displayed inline and auto-expanded without a manual toggle
   **BUT** *Crosscut Rows* for non-selected families are hidden
   **Evidence:** stated requirement — "supporting only [selected family] and the skills left to right"

3. **WHEN** the *Foundational Section* is visible
   **THEN** its header chip uses muted grey text
   **AND** its individual *Crosscut Skill Chips* use white text
   **Evidence:** stated requirement — "header grey, skills white"

---

## Story: Navigate From Kanban to Skill Page

**Story type:** user

### Domain terms

- *Skill Page* — a detail page for one practice skill; also has a *Kanban Surface* (`foundry-kanban-surface--skill-page`)
- *Initial Family* — the family that owns the skill being viewed; set on the surface as `data-initial-family`
- *Persisted Filter* — family selection saved to `sessionStorage` before navigation and restored on load

### Acceptance criteria

1. **WHEN** the user clicks a skill ticket on the hub kanban
   **THEN** the *Skill Page* loads with the ticket's family pre-selected as the *Initial Family*
   **AND** the board on the *Skill Page* shows only that family's rows
   **AND** all *Family Header Chips* remain visible in the *Practice Rail*
   **Evidence:** `data-initial-family` attribute; stated requirement — skill page filters to its family

2. **WHEN** the user clicks a different *Family Header Chip* on the *Skill Page*
   **THEN** the board adds that family's rows to the visible set
   **AND** the *Supporting Section* shows crosscut rows for all currently selected families
   **Evidence:** multi-select toggle behavior

3. **WHEN** the user navigates from the *Skill Page* back to the hub
   **THEN** the hub restores the *Persisted Filter* that was active before navigation
   **Evidence:** `sessionStorage` FILTER_KEY save-on-click behavior

---

## Source evidence table

| Story | AC # | Source |
|---|---|---|
| View Kanban With No Filter Selected | 1–3 | Hub default behavior; working session Jun 11 2026 |
| Select Practice Family Filter | 1 | Stated requirement: "ALL skills header chips should show" |
| Select Practice Family Filter | 2–3 | Stated requirement: board rows filter to selected family |
| Select Practice Family Filter | 4 | Stated requirement: "supporting only [family] and the skills left to right" |
| Select Practice Family Filter | 5 | Multi-select Set logic; inferred from implementation |
| Deselect Practice Family Filter | 1–2 | Stated requirement: "click again they all disappear/reappear" |
| Expand and Collapse Practice Skills | 1–4 | Hub expand/collapse; sessionStorage persistence |
| View Supporting Section Crosscut Skills | 1–3 | Stated requirements: crosscut layout, foundational colors |
| Navigate From Kanban to Skill Page | 1–3 | `data-initial-family`; sessionStorage FILTER_KEY |
