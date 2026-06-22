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

### kanban supporting practice *is a type of* supporting skill

- belongs to the *kanban* delivery-system practice (`abd-kanban`, `abd-kanban-planning`, `abd-kanban-repo`, `kanban-estimation`, `abd-kanban-handoff`)
- never appears as a ticket in a *stage* column on the board grid
- always appears in the *Supporting Section* crosscut row for *kanban*
- **Invariant:** the *kanban* crosscut row remains visible even when another *skill family* filter is *active*

### other skill *is a type of* skill

- belongs to no *skill family*; has a *stage* and appears in the board under the "other" row
- follows the same expand/collapse visibility rules as *stage skill*

### skill navigated to *is a type of* skill

- the specific *skill* whose detail page is currently open
- causes its *skill family* to be set as *active* when the *kanban* loads on that detail page

### skill family

- groups one or more *practice skills* (both *stage skills* and *supporting skills*)
- is *active* when ticked by the user; is *inactive* when unticked
- **Invariant:** a *skill family* header chip in the *Practice Rail* is visible when *Skills Toggle* is expanded, or when collapsed with that family *active* (ticked)

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
- **context** is a special *stage* — a cross-cutting column for context-to-memory skills; its *stage skills* (convert-to-markdown, chunk-markdown, embed-vectors, search-memory, semantic-context-chunker) appear at the **top of the family row band** (grid-row 2), parallel to the first row of any other *skill family*, not below the four practice-family rows

### kanban

- organises all *skills* by *skill family* row and *stage* column
- shows all *skill family* rows when no *skill family* is *active*; filters to *active* families when one or more are ticked
- shows all *stage* columns when no *stage* is *focused*; filters to the *focused stage* column when the user clicks a *stage column head*
- **Invariant:** all *skill family* header chips in the *Practice Rail* are visible when *Skills Toggle* is expanded; when collapsed, chips follow *Idle State* / *Filter Active State* rules (hidden when idle, ticked-only when filter active)

### stage focus

- is a property of *stage* — the column the user has clicked to filter the board vertically
- is independent of *active*/*inactive* *skill family* state; both filters may apply at once
- clears when the user clicks the same *stage column head* again

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
- *Idle State* — no family filter active; when expanded, all rows visible; when collapsed, no families or skill tickets shown
- *Other Practices Chip* — filter chip at the bottom of the *Practice Rail* for foundational / cross-family skills

### Acceptance criteria

1. **WHEN** the *Kanban Surface* loads on the hub index with no saved filter and *Skills Toggle* is collapsed (default)
   **THEN** no *Family Toggle* buttons appear in the *Practice Rail* — only the *Skills Toggle* is visible
   **AND** no *Board Rows* or skill tickets are visible in the *Stage Columns*
   **AND** the surface is in *Idle State*
   **Evidence:** stated requirement — hub first load hides practice families until skills expanded

1b. **WHEN** the *Kanban Surface* is expanded with no family filter active
   **THEN** all *Family Toggle* buttons appear in the *Practice Rail*
   **AND** all four practice-family *Board Rows* are visible across all *Stage Columns*
   **AND** *other practices* stage-folder skills are hidden until the *Other Practices Chip* is ticked
   **Evidence:** stated requirement — expanded idle shows all practice families; other rows on demand only

1c. **WHEN** the *Kanban Surface* is expanded
   **THEN** context-to-memory skill tickets in the *Context Stage Column* appear at the **same vertical band** as the first practice-family row (story-driven-delivery row) in adjacent stage columns
   **AND** context-to-memory skill tickets are **not** rendered below the four practice-family row slots
   **Evidence:** CSS override — `.kb-col[data-stage="context"] > .aad-skill-row[data-family="context-to-memory"] { grid-row: 2 }` places CTX at the top of the family row band, parallel to other practice families

2. **WHEN** *Skills Toggle* is collapsed and a family filter is active
   **THEN** only *Ticked Families* show individual skill tickets in the *Stage Columns*
   **AND** *Non-matching Board Rows* are hidden
   **AND** only *Ticked Families* remain visible in the *Practice Rail*; inactive families collapse to zero-height tracks
   **AND** visible *Family Header Chips* stay within the practice column width (no horizontal blowout)
   **Evidence:** stated requirement — collapsed focus mode; observed defect — inactive chips stretched column width

3. **WHEN** *Skills Toggle* is collapsed and no family filter is active
   **THEN** no individual skill tickets are visible in the *Stage Columns*
   **AND** no *Family Toggle* buttons are visible in the *Practice Rail*
   **AND** the *Stage Questions Row* (column footer bullet overviews) remains visible under each *Stage Column*
   **Evidence:** collapsed idle state — no families or tickets; stage footers always shown

4. **WHEN** *Skills Toggle* is expanded
   **THEN** ALL *Family Toggle* header chips are visible in the board area regardless of filter state
   **AND** individual skill tickets appear inside each visible *Board Row*
   **Evidence:** stated requirement — "expanded we always see all family chips selected or not"

5. **WHEN** the *Practice Rail* is visible
   **THEN** the *Other Practices Chip* shares the same left edge and width as the four practice-family chips above it
   **AND** the user can click it to tick or untick the *other* family filter
   **Evidence:** observed defect — other practices chip was left-shifted and hard to click

6. **WHEN** the user deactivates the *Other Practices Chip* while a *practice family* filter remains active
   **THEN** the board collapses the stage-other row tracks (gap + extra other rows) to zero height
   **AND** the *Other Practices Chip* remains visible in the *Practice Rail*
   **BUT** no empty vertical space is reserved below the visible board rows
   **Evidence:** observed defect — deactivating other left collapsed empty row tracks

7. **WHEN** the *Kanban Surface* is expanded with no family filter active
   **THEN** the *Other Practices Chip* sits directly below the four practice-family chips with no empty row gap
   **AND** ticking *Other Practices Chip* expands the other stage tracks and reveals stage-folder skills
   **AND** hub and skill pages use the same board grid and filter logic
   **Evidence:** observed defect — idle hub reserved other row tracks; hub/skill page HTML diverged

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
   **THEN** only *Ticked Families* show individual skill tickets in the *Stage Columns*
   **AND** *Non-matching Board Rows* are hidden
   **AND** only *Ticked Families* remain visible in the *Practice Rail*
   **Evidence:** stated requirement — collapsed focus mode shows only ticked family skills

4. **WHEN** a family is ticked and the surface is in *Filter Active State*
   **AND** *Skills Toggle* is expanded
   **THEN** ALL *Family Header Chips* remain visible in the *Practice Rail*
   **AND** only *Filtered Board Rows* show their individual skill tickets
   **AND** *Non-matching Board Rows* are hidden from the stage columns
   **AND** visible tickets for the selected family align on one horizontal band across all *Stage Columns*
   **AND** a single selected family's tickets stay on that family's *Practice Rail* row (not snapped to the story-driven-delivery row)
   **Evidence:** stated requirement — "expanded we always see all family chips selected or not"; observed defect — non-SDD single filter snapped to top row

5. **WHEN** a family is ticked
   **THEN** the matching *Crosscut Row* in the *Supporting Section* is shown *Auto-expanded*
   **BUT** the *Crosscut Row Header Chip* for any non-ticked family is never shown — regardless of whether *Skills Toggle* is expanded or collapsed
   **Evidence:** stated requirement — supporting section family visibility is controlled by tick state only, not by expand/collapse

6. **WHEN** the user ticks a second *Family Header Chip* while one is already ticked
   **THEN** both families' *Board Rows* become visible
   **AND** both families' *Crosscut Rows* appear in the *Supporting Section*
   **Evidence:** multi-select tick behavior

7. **WHEN** a *Stage Column Filter* is active
   **THEN** the *practice family* filter state is unchanged
   **AND** clearing the *Stage Column Filter* does not clear any *Ticked Family*
   **Evidence:** stated requirement — practice and stage filters are independent

---

## Story: Select Stage Column Filter

**Story type:** user

### Domain terms

- *Stage Column Head* — clickable header at the top of each *Stage Column* (Shaping, Discovery, etc.)
- *Stage Column Filter* — user toggles one or more *Stage Column Heads*; all five columns stay visible but non-selected columns show no skill tickets
- *Stage Filter Active State* — one stage selected; surface has `foundry-stage-filter-active` class
- *Stage Filter Idle State* — no stage selected; all five *Stage Columns* visible
- *Stage Questions Cell* — outcome bullets below the board aligned under each *Stage Column*
- *Focused Stage* — a *Stage Column* currently toggled on by the *Stage Column Filter*

### Acceptance criteria

1. **WHEN** the user clicks an untoggled *Stage Column Head*
   **THEN** all five *Stage Columns* remain visible on the board
   **BUT** only toggled-on stage columns show skill tickets; other columns are empty
   **AND** the *Stage Column Head* shows selected state (`is-selected`, `aria-pressed="true"`, tick indicator) like a *Family Header Chip*
   **AND** the matching *Stage Questions Cell* receives the `is-active` class
   **Evidence:** stated requirement — stage filters toggle like row filters; columns stay visible

2. **WHEN** the user clicks a toggled-on *Stage Column Head* again
   **THEN** that stage is removed from the filter
   **AND** when no stages remain toggled on, the surface returns to *Stage Filter Idle State* with all columns repopulated
   **AND** the *Stage Column Head* clears selected/current state and the questions cell loses `is-active`
   **Evidence:** stated requirement — toggle off restores tickets; observed defect — filter cleared but head stayed current

3. **WHEN** the user toggles multiple *Stage Column Heads* on
   **THEN** each toggled column shows skill tickets and each untoggled column is empty
   **Evidence:** stated requirement — stage filters behave like multi-select family chips

4. **WHEN** a *Stage Column Filter* is active
   **THEN** all *Family Header Chips* remain visible in the *Practice Rail*
   **BUT** no *Family Header Chip* is hidden or collapsed because of the stage filter
   **Evidence:** stated requirement — stage filter is vertical only; practice rail unchanged

5. **WHEN** both a *practice family* filter and a *Stage Column Filter* are active
   **THEN** only *Board Rows* for *Ticked Families* appear in the *Focused Stage* column
   **AND** non-matching families remain hidden in that column
   **AND** toggling the stage filter off restores all columns while the family filter stays active
   **Evidence:** stated requirement — orthogonal row and column filters

6. **WHEN** the user clicks a *Family Header Chip* or navigates to a skill via a ticket link
   **THEN** the *Stage Column Filter* does not activate
   **AND** all five *Stage Columns* remain visible with tickets in every column (subject to family filter only)
   **BUT** the current skill's stage may be highlighted (`kb-col-head--current`) without emptying other columns
   **Evidence:** stated requirement — highlight is not filter; only *Stage Column Head* clicks toggle the filter

---

## Story: Expand and Collapse Practice Skills

**Story type:** user

### Domain terms

- *Skills Toggle Button* — the `–` / `+` control in the top-left of the *Kanban Surface*
- *Expanded State* — individual skill tickets visible in each *Board Row*; `foundry-skills-expanded` class on surface
- *Collapsed State* — family header chips hidden in the *Practice Rail* when idle; skill tickets hidden unless a family filter is active; `foundry-skills-collapsed` class on surface
- *Skills Expanded Preference* — persisted `sessionStorage` value per surface type (hub index vs skill page) remembering the last toggle state

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
   **THEN** individual skill tickets are hidden in *Board Rows* unless a family filter is active
   **AND** when a family filter is active, only *Ticked Families* show skill tickets in *Stage Columns*
   **AND** inactive *Family Header Chips* are hidden from the *Practice Rail* and their grid tracks collapse
   **AND** the *Stage Questions Row* (column footer bullet overviews) remains visible under each *Stage Column*
   **AND** supporting *Crosscut Rows* and skill chips are hidden
   **BUT** the *Supporting Section* shell may keep its section label visible
   **Evidence:** stated requirement — collapse hides skill tickets, not stage column footers

4. **WHEN** the user reloads or navigates back to the *Kanban Surface*
   **THEN** the surface restores the *Skills Expanded Preference* for that surface type (hub index or skill page) from the last session
   **Evidence:** `sessionStorage` persistence via `readSkillsExpandedPref()` with separate hub/skill-page keys

---

## Story: View Supporting Section Crosscut Skills

**Story type:** user

### Domain terms

- *Crosscut Skill Chip* — individual skill chip inside a *Crosscut Row*; white text, family-colored left border
- *Crosscut Row Header* — the family label chip at the start of a *Crosscut Row*; family-colored text, family-colored left border
- *Foundational Section* — a second crosscut area for skills that apply across all families; header is muted grey, chips are white

### Acceptance criteria

1. **WHEN** the *Supporting Section* is visible and no filter is active
   **THEN** all supporting *Crosscut Rows* are shown (kanban, domain-driven-design, story-driven-delivery), each with its *Crosscut Row Header* and *Crosscut Skill Chips* inline (wrapping left to right)
   **Evidence:** stated requirement — no filter shows all supporting crosscut rows

2. **WHEN** a family filter is active and the *Supporting Section* is visible
   **THEN** the *Crosscut Row* for the *Selected Family* is shown
   **AND** its *Crosscut Skill Chips* are displayed inline and auto-expanded without a manual toggle
   **AND** the *kanban* *Crosscut Row* is always shown (kanban is supporting-only — not filtered by practice-family selection)
   **BUT** *Crosscut Rows* for other non-selected families are hidden
   **Evidence:** stated requirement — "supporting only [selected family] and the skills left to right"; kanban always in supporting area

3. **WHEN** the *Kanban Surface* is visible
   **THEN** no *kanban supporting practice* skill ticket appears in any *Stage Column* on the board grid
   **AND** every *kanban supporting practice* skill appears only under the *kanban* row in the *Supporting Section*
   **Evidence:** stated requirement — kanban skills are supporting-only

4. **WHEN** the *Foundational Section* is visible
   **THEN** its header chip uses muted grey text
   **AND** its individual *Crosscut Skill Chips* use white text
   **Evidence:** stated requirement — "header grey, skills white"

5. **WHEN** the *Supporting Section* is visible on a *Skill Page*
   **THEN** each *Crosscut Row* matches the hub layout: *Crosscut Row Header* link and *Crosscut Skill Chips* inline in one horizontal row (wrapping left to right)
   **AND** no manual crosscut-row toggle is required to reveal chips
   **Evidence:** stated requirement — skill page supporting section identical to hub

---

## Story: Navigate From Kanban to Skill Page

**Story type:** user

### Domain terms

- *Skill Page* — a detail page for one practice skill; also has a *Kanban Surface* (same markup as the hub)
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

4. **WHEN** the user clicks a skill ticket link that opens another catalog page (hub → skill or skill → skill)
   **THEN** the destination page restores the *Kanban Surface* to the same viewport offset it had before navigation
   **AND** the page does not jump to `scrollY = 0`
   **Evidence:** stated requirement — compare downstream skills without losing board context; `kanbanScroll` query param on click, restored after board layout

---

## Story: Skill Page Install and View Source

**Story type:** user

### Domain terms

- *Install Block* — the `install-block` section on a *Skill Page* with the `npx skills add` command
- *View Source Link* — link directly under the install snippet; opens the skill package folder on GitHub
- *Skill Package Path* — repo-relative path to the skill folder (e.g. `practices/story-driven-delivery/skills/abd-story-mapping`)

### Acceptance criteria

1. **WHEN** a *Skill Page* loads
   **THEN** an *Install Block* appears below the hero with heading "Install with npx"
   **AND** a copy-paste `npx skills add abd-works/abd-skills@<skill-name> -y` command
   **Evidence:** `_npx_skills_install_block` in `generate_abd_catalog.py`

2. **WHEN** the *Install Block* is rendered
   **THEN** a *View Source Link* labeled "View source" appears directly under the install snippet
   **AND** the link target is `https://github.com/abd-works/abd-skills/tree/main/<Skill Package Path>/`
   **AND** the *Skill Package Path* is shown beside the link in monospace
   **AND** the link opens in a new tab
   **Evidence:** `_repo_href(GITHUB_TREE_MAIN, pkg_rel_posix)`; `_REPO_LINK_NEW_TAB`

3. **WHEN** an agent or plugin detail page loads
   **THEN** no *Install Block* or *View Source Link* is shown
   **Evidence:** agent pages set `{{INSTALL_BLOCK}}` to empty

---

## Story: CDD Overview Tour (Travel Ring)

**Story type:** user

### Domain terms

- *CDD Toggle Button* — the "Click for overview" control above the *Kanban Surface*; advances the guided tour one step per click
- *Guide Panel* — the expanding copy block (`foundry-cdd-panel`) that reveals tour text for each step
- *Travel Ring* — the single orange bordered highlight (`#travel-ring`) that flies from the *CDD Toggle Button* onto tour targets
- *Tour Step* — one advance of the tour: Context scope → Context perspectives → Executable context → Change implications → reset
- *Tour Target* — the element or group the *Travel Ring* frames (column heads, perspective labels, or a stage column)
- *Landed Ring* — *Travel Ring* resting on *Tour Targets* after a flight completes

### Acceptance criteria

1. **WHEN** the user clicks the *CDD Toggle Button* to enter or advance a *Tour Step*
   **THEN** the *Guide Panel* reveals copy for that step
   **AND** after the copy finishes expanding, the *Travel Ring* flies from the *CDD Toggle Button* onto the step's *Tour Targets*
   **Evidence:** `catalog-foundry-tour.js` — `revealGuideText` then `flyRingToTargets`

2. **WHEN** a new *Tour Step* begins before the previous step's ring has been dismissed
   **THEN** the previous *Travel Ring* disappears immediately — no stale orange frame remains at prior *Tour Targets*
   **AND** at most one *Travel Ring* is visible on screen at any time
   **Evidence:** observed defect — stale ring lingered during guide-panel resize; fixed by clearing `lastRingTargets` and hiding ring on step transition

3. **WHEN** the *Guide Panel* resizes during copy reveal between *Tour Steps*
   **THEN** the *Travel Ring* is not re-shown at the previous step's *Tour Targets*
   **BUT** after a flight completes, layout changes may re-sync the *Landed Ring* to the current step's targets only
   **Evidence:** `ResizeObserver` + `syncRingToTargets`; must not sync while `ringIsAnimating()` or when `lastRingTargets` is cleared

4. **WHEN** a *Travel Ring* flight is in progress
   **THEN** layout or resize handlers must not restore a second ring or jump the ring to the destination before the animation finishes
   **Evidence:** `ringIsAnimating()` guard on `syncRingToTargets`

5. **WHEN** the user reaches the *Change implications* *Tour Step* (after Executable context)
   **THEN** the *Guide Panel* shows color-coded bullets for Story-driven delivery, Domain-driven design, User experience, Architecture, and The team
   **AND** no *Travel Ring* is shown — the ring is hidden for this step
   **Evidence:** `animateChangeImplications()` — `hideRing()`, `skipRingPause: true`

6. **WHEN** the user completes the final *Tour Step* and clicks the *CDD Toggle Button* again
   **THEN** the tour resets to idle, the *Travel Ring* is hidden, and the *Guide Panel* returns to its default prompt
   **Evidence:** `resetTour()` — `hideRing()`, `lastRingTargets = null`

---

## Story: Return to Catalog Hub via Forge Nav

### Domain terms

- *Forge Nav Link* — the single Foundry section item in the top navigation; label `Forge`; returns to the catalog hub (`index.html`)

### Acceptance criteria

1. **WHEN** any catalog page loads
   **THEN** the top navigation shows exactly one Foundry item labeled *Forge Nav Link*
   **AND** links for Complete, Skills, Agents, Instructions, and Delivery kanban are not shown
   **Evidence:** `foundryLinks()` in `catalog-nav.js`

2. **WHEN** the user is on the catalog hub (`index.html`)
   **THEN** *Forge Nav Link* has `aria-current="page"`
   **Evidence:** `linkHTML()` current-page logic for `forge` + `data-nav-current="hub"`

3. **WHEN** the user is on a skill or other catalog sub-page
   **THEN** *Forge Nav Link* is visible and its `href` resolves to the catalog hub
   **AND** it is not marked as the current page
   **Evidence:** skill pages set `data-nav-current="skills"`; forge href is `index.html`

---

## Story: Collapse and Expand Stage Column

**Story type:** user

### Domain terms

- *Stage Column* — a vertical column for a delivery stage (e.g. Shaping, Discovery, Exploration, Specification, Engineering, Context); identified by `.kb-col[data-stage]`
- *Collapse Button* — a small toggle button (`.kb-col-collapse-btn`) rendered at the top-right of each *Stage Column*; collapses or expands that column
- *Collapsed Column* — a *Stage Column* carrying the `.kb-col--collapsed` class; shows only a vertical stage label and the *Collapse Button*; its allocated grid width is narrowed to 28 px
- *Expanded Column* — default state; full-width; tickets and skill rows visible
- *Vertical Stage Label* — the stage name rendered rotated 90° inside a *Collapsed Column* (`.kb-col-collapsed-label`); read-only, not interactive

### Acceptance criteria

1. **WHEN** the *Kanban Surface* loads
   **THEN** each *Stage Column* has a *Collapse Button* visible at its top-right
   **AND** all columns start in the *Expanded Column* state unless a prior collapsed preference was saved in sessionStorage
   **Evidence:** `injectCollapseButtons()` in `catalog-foundry-skill-nav.js`; `readCollapsedColsPref()` restores state on load

2. **WHEN** the user clicks the *Collapse Button* on an *Expanded Column*
   **THEN** that column becomes a *Collapsed Column*
   **AND** its allocated grid width narrows to 28 px, giving horizontal space to remaining expanded columns
   **AND** skill tickets, skill rows, and the column definition area are hidden
   **AND** the *Vertical Stage Label* becomes visible inside the narrowed column
   **AND** the *Collapse Button* changes its `aria-label` to "Expand column" and `aria-expanded` to "false"
   **Evidence:** `setColCollapsed()` toggles `.kb-col--collapsed` and calls `updateGridColumns()`

3. **WHEN** the user clicks the *Collapse Button* on a *Collapsed Column*
   **THEN** that column returns to *Expanded Column* state
   **AND** its grid width is restored to `minmax(0, 1fr)`
   **AND** skill tickets and rows reappear
   **AND** the *Collapse Button* `aria-label` returns to "Collapse column" and `aria-expanded` to "true"
   **Evidence:** `toggleColCollapse()` calls `setColCollapsed(stage, false)`

4. **WHEN** a column is collapsed or expanded
   **THEN** the collapsed set is persisted to sessionStorage under key `abd-foundry-skill-nav-col-collapsed`
   **AND** on the next page load the same columns are restored to their collapsed state
   **Evidence:** `saveCollapsedColsPref()` and `readCollapsedColsPref()` in `catalog-foundry-skill-nav.js`

5. **WHEN** a *Stage Column* is *Collapsed*
   **THEN** collapsing it does not affect the family filter, stage focus filter, or skills expand/collapse state
   **AND** other columns continue to respond to filter changes normally
   **Evidence:** column collapse is a separate visual state independent of `selectedStages`, `selectedFamilies`, and `skillsExpanded`

---

## Source evidence table

| Story | AC # | Source |
|---|---|---|
| View Kanban With No Filter Selected | 1–3, 1b, 1c | Hub collapsed default; stage footers when collapsed; CTX skills at family-row band top; working session Jun 11 2026 |
| Select Practice Family Filter | 1 | Stated requirement: "ALL skills header chips should show" |
| Select Practice Family Filter | 2–3 | Stated requirement: board rows filter to selected family |
| Select Practice Family Filter | 4 | Stated requirement: "supporting only [family] and the skills left to right" |
| Select Practice Family Filter | 5 | Multi-select Set logic; inferred from implementation |
| Select Practice Family Filter | 7 | Stated requirement: practice and stage filters are independent |
| Select Stage Column Filter | 1–6 | Stated requirement: stage columns toggle like family chips; multi-select supported |
| Deselect Practice Family Filter | 1–2 | Stated requirement: "click again they all disappear/reappear" |
| Expand and Collapse Practice Skills | 1–4 | Hub expand/collapse; stage footers when collapsed; separate hub/skill sessionStorage keys |
| CDD Overview Tour (Travel Ring) | 1–6 | Tour ring animation; change-implications step; stale ring fix |
| View Supporting Section Crosscut Skills | 1–5 | Stated requirements: crosscut layout, foundational colors, skill-page parity |
| Navigate From Kanban to Skill Page | 1–4 | `data-initial-family`; sessionStorage FILTER_KEY; `kanbanScroll` restore |
| Skill Page Install and View Source | 1–3 | npx install block; GitHub tree link via `pkg_rel_posix` |
| Return to Catalog Hub via Forge Nav | 1–3 | Stated requirement: single forge link to catalog main page |
| Collapse and Expand Stage Column | 1–5 | `injectCollapseButtons`, `setColCollapsed`, `updateGridColumns`, `readCollapsedColsPref`, `saveCollapsedColsPref` in `catalog-foundry-skill-nav.js` |
