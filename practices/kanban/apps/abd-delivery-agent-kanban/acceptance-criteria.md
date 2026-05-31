# Acceptance Criteria — Delivery Agent Kanban

---

# Visualize Delivery Board

## Display Board Layout

### Story: Organize Tickets into Stage Groups by Delivery Phase

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Kanban Board* — the live board defining ordered stages and governing ticket flow
- *Ticket* — a unit of work at the scope level its current stage requires
- *Stage* — a named phase of delivery work (context, shaping, discovery, exploration, specification, engineering)
- *Board Position* — the stage a ticket currently occupies on the kanban board

1. **WHEN** the *Kanban Board* has *Tickets* flowing through active *Stages*
   **THEN** each *Ticket* is grouped under its assigned *Stage*
   **AND** *Stages* are arranged left to right in the canonical order defined by the *Kanban Board*
   **Evidence:** `kanbanBoard.ts` — `buildStageBuckets`, `STAGE_ORDER`; `DeliveryKanbanBoard.tsx` — `StageGroup`

2. **WHEN** a *Stage* column renders
   **THEN** it displays three sub-columns labelled "Queue", "In Progress", and "Done"
   **Evidence:** `DeliveryKanbanBoard.tsx` — `StageGroup` / `SubColumn`, queue · ip · done

3. **WHEN** a *Ticket* lives in the board `backlog` array and has a *Stage* assigned
   **THEN** it appears in that *Stage*'s "Queue" sub-column
   **AND** it does not appear in the global Backlog column
   **Evidence:** `kanbanBoard.ts` — `buildStageBuckets` (backlog → queue), `buildGlobalBacklogTickets`

4. **WHEN** a *Ticket* lives in the board `active` array
   **THEN** it appears in that *Stage*'s "In Progress" sub-column while stage skills remain incomplete
   **OR** in that *Stage*'s "Done" sub-column when every *Stage Work Required* skill is complete (execution and review done)
   **Evidence:** `kanbanBoard.ts` — `isStageSkillsComplete`, `buildStageBuckets`

5. **WHEN** an archived *Ticket* completed a *Stage* (scattered or final completion)
   **THEN** it appears in that *Stage*'s "Done" sub-column
   **AND** it is excluded from the far-right Archived column when already shown in stage Done
   **Evidence:** `kanbanBoard.ts` — `resolveArchivedStageDone`, `buildArchivedColumnTickets`

6. **WHEN** no *Tickets* occupy a *Stage* in the *active* flow
   **THEN** the *Stage* column still renders in the board layout
   **BUT** the *Stage* is visually distinguished from *Stages* that contain work
   **Evidence:** `DeliveryKanbanBoard.tsx` — `StageGroup` `hasWork` guard

7. **WHEN** the *Kanban Board* configuration limits the active *Stages*
   **THEN** only *Stages* present in the active stage flow are displayed
   **BUT** *Stages* outside the flow do not appear in the board layout
   **Evidence:** `DeliveryKanbanBoard.tsx` — `visibleStages`

---

### Story: Show Assigned Skills per Stage

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Stage* — a named phase of delivery work
- *Stage Work Required* — the ordered list of skills required by a stage on the kanban board
- *Skill* — a named practice method assigned to a stage, performed by an agent role

1. **WHEN** a *Stage* has *Skills* defined in *Stage Work Required*
   **THEN** the skill rail renders beneath the *Stage* column
   **AND** each *Skill* displays its label as a chip
   **Evidence:** `DeliveryKanbanBoard.tsx` — `StageGroup` skill chips, lines 253–261

2. **WHEN** the skill rail renders *Skills*
   **THEN** each skill chip is color-coded by its discipline family
   **Evidence:** `DeliveryKanbanBoard.tsx` — `familyCssClass(skillFamilyFor(...))`, line 256

3. **WHEN** a *Stage* has no *Skills* in *Stage Work Required*
   **THEN** no skill rail appears beneath the *Stage* column
   **BUT** the *Stage* column itself still renders
   **Evidence:** `DeliveryKanbanBoard.tsx` — `skills.length > 0` guard, line 253

---

### Story: Display Backlog Tickets

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Ticket* — a unit of work carrying lineage and priority
- *Board Position* — backlog is the pre-stage waiting position on the kanban board
- *Lineage* — ordered ancestry of a ticket from project down through scope levels
- *Priority* — numeric ordering determining backlog position

1. **WHEN** *Tickets* exist in the global backlog *Board Position* (no *Stage* assigned yet)
   **THEN** the Backlog column renders each *Ticket* showing its abbreviated ID and display name
   **AND** *Tickets* appear in *Priority* order
   **Evidence:** `kanbanBoard.ts` — `buildGlobalBacklogTickets`; `DeliveryKanbanBoard.tsx` — `EndColumn`

2. **WHEN** a *Ticket* has a *Stage* but lives in the board `backlog` array (stage queue)
   **THEN** it appears only in that *Stage*'s "Queue" sub-column
   **AND** it does not appear in the global Backlog column
   **Evidence:** `kanbanBoard.ts` — `buildStageBuckets`, `buildGlobalBacklogTickets`

3. **WHEN** a backlog *Ticket* card is hovered
   **THEN** the tooltip displays the full *Lineage* path (project > increment > sprint > story)
   **Evidence:** `DeliveryKanbanBoard.tsx` — `TicketCard` title attribute

4. **WHEN** the global backlog *Board Position* is empty
   **THEN** the Backlog column renders with heading but no ticket cards
   **Evidence:** `DeliveryKanbanBoard.tsx` — `EndColumn` renders empty ticket array

5. **WHEN** a global backlog *Ticket* is displayed
   **THEN** no skill indicators or agent avatars appear on the card
   **BUT** the card still shows the abbreviated ID and display name
   **Evidence:** `DeliveryKanbanBoard.tsx` — `TicketCard`; `kanbanBoard.ts` — `ticketCanExpand` returns false for backlog column

---

### Story: Display Archived Tickets

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Ticket* — a unit of work
- *Board Position* — archived is the permanently finished position on the kanban board

1. **WHEN** *Tickets* exist in the archived *Board Position* and are not shown in a *Stage* "Done" sub-column
   **THEN** the Archived column renders at the far right of the board
   **AND** each *Ticket* displays its abbreviated ID and display name
   **Evidence:** `kanbanBoard.ts` — `buildArchivedColumnTickets`; `DeliveryKanbanBoard.tsx` — `EndColumn`

2. **WHEN** an archived *Ticket* is already displayed in a *Stage* "Done" sub-column
   **THEN** it does not also appear in the Archived column
   **Evidence:** `kanbanBoard.ts` — `buildArchivedColumnTickets`

3. **WHEN** no *Tickets* remain for the Archived column after stage Done deduplication
   **THEN** the Archived column does not render at all
   **Evidence:** `DeliveryKanbanBoard.tsx` — conditional `archivedColumnTickets.length > 0`

4. **WHEN** the board state is assembled
   **THEN** archived *Tickets* are built separately from the active stage views
   **BUT** stage-complete archived *Tickets* are merged into stage Done buckets for display
   **Evidence:** `kanbanBoard.ts` — `buildArchivedViews`, `buildStageBuckets`, `resolveArchivedStageDone`

---

### Story: Derive Board Title from Ticket Lineage

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Kanban Board* — the persistent root holding all delivery state
- *Ticket* — a unit of work carrying lineage
- *Lineage* — ordered ancestry from project down through scope levels

1. **WHEN** the *Kanban Board* contains *Tickets* with non-empty *Lineage*
   **THEN** the board derives its title from the first element of the first qualifying *Ticket's* *Lineage*
   **AND** the title displays in the board header beside "Kanban Board —"
   **Evidence:** `KanbanBoardLoader.ts` — `deriveBoardTitle`, lines 54–59; `App.tsx` — header, lines 49–51

2. **WHEN** the *Kanban Board* has no *Tickets*
   **THEN** the board title defaults to "Kanban Board"
   **Evidence:** `KanbanBoardLoader.ts` — `deriveBoardTitle` empty-board fallback, line 56

3. **WHEN** all *Tickets* have empty *Lineage* arrays
   **THEN** the board title falls back to "Kanban Board"
   **BUT** no error is raised
   **Evidence:** `KanbanBoardLoader.ts` — `topLevel?.lineage[0]` nullish fallback, line 58

---

### Story: Show Last Sync Timestamp

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Kanban Board* — the persistent root of all delivery state; records a timestamp each time it is saved

1. **WHEN** the *Kanban Board* has a saved-at timestamp
   **THEN** the board header displays the timestamp formatted as "board.json YYYY-MM-DD HH:MM:SSZ"
   **AND** the timestamp is right-aligned in the header alongside the theme controls
   **Evidence:** `App.tsx` — syncedAt display, lines 58–60

2. **WHEN** the saved-at timestamp has sub-second precision
   **THEN** the display shows only date and time to the second
   **AND** the format is human-readable (e.g. "2025-01-15 10:30:00")
   **Evidence:** `App.tsx` — timestamp formatting, line 59

3. **WHEN** the *Kanban Board* has no saved-at timestamp
   **THEN** no timestamp text appears in the board header
   **BUT** the header layout remains intact
   **Evidence:** `App.tsx` — conditional rendering on `snapshot?.syncedAt`, line 58

---

### Story: Switch Display Theme

**Story type:** user

**Domain terms** (vocabulary for this story's AC):

- *Kanban Board* — the board state being rendered (unaffected by theme choice)

1. **WHEN** the Delivery Lead clicks the "Executive" button in the display mode toggle
   **THEN** the board applies the executive theme via `data-theme="executive"` on the root element
   **AND** the selection persists to `localStorage` under key `theme`
   **Evidence:** `App.tsx` — `toggleTheme`, lines 21–25; mode toggle buttons, lines 54–57

2. **WHEN** the Delivery Lead clicks the "Engineering" button
   **THEN** the board switches to the engineering theme
   **AND** the active button is visually highlighted with `is-active`
   **Evidence:** `App.tsx` — `toggleTheme`, lines 21–25; class toggle, lines 55–56

3. **WHEN** the board loads on a fresh session
   **THEN** the theme defaults to "engineering" unless `localStorage` holds a prior selection
   **BUT** the *Kanban Board* data is not affected by the theme choice
   **Evidence:** `App.tsx` — theme state initializer, lines 16–18

---

## Display Ticket Cards

### Story: Render Ticket with Chip Label and Display Name

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Ticket* — a unit of work with a unique identifier and lineage
- *Lineage* — ordered ancestry array on a ticket, from project down through scope levels

1. **WHEN** a *Ticket* renders on the board
   **THEN** the card shows an abbreviated ID chip and a display name derived from *Lineage*
   **AND** hovering the card reveals the full *Lineage* path as a tooltip
   **Evidence:** `DeliveryKanbanBoard.tsx` — `TicketCard`, lines 125–141; title attribute, line 123

2. **WHEN** the *Ticket's* ticket_id is eight characters or fewer
   **THEN** the *Chip Label* is the full ticket_id
   **Evidence:** `kanbanBoard.ts` — `ticketChipLabel`, lines 244–249

3. **WHEN** the *Ticket's* ticket_id is longer than eight characters and ends with digits
   **THEN** the *Chip Label* shows the numeric suffix prefixed with `#`
   **Evidence:** `kanbanBoard.ts` — `ticketChipLabel` regex match, lines 247–248

4. **WHEN** the *Ticket* has a non-empty *Lineage*
   **THEN** the display name is the last element of the *Lineage* array
   **BUT** when *Lineage* is empty, the display name falls back to the raw ticket identifier
   **Evidence:** `kanbanBoard.ts` — `ticketDisplayLabel`, lines 239–242

---

### Story: Show Active Skill and Agent on Ticket

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Ticket* — a unit of work tracking skill progress entries
- *Skill Progress* — per-skill execution and review state on a ticket
- *Execution Status* — skill work state: not started, in progress, or done
- *Agent* — the autonomous worker with a delivery role performing execution of a skill
- *Skill* — named practice method whose discipline determines color-coding
- *Focus Skill* — the skill highlighted on a ticket: under review, executing, or the next incomplete stage skill when the ticket is active in In Progress

1. **WHEN** an active *Ticket* has a *Skill Progress* entry with *Execution Status* in progress
   **THEN** the ticket card displays a bot icon color-coded by the *Focus Skill* discipline
   **AND** the executing *Agent* role avatar appears on the card
   **Evidence:** `kanbanBoard.ts` — `deriveActiveSkill`, `resolveWorkingAgent`; `DeliveryKanbanBoard.tsx` — `ChatbotIcon`, `AgentAvatar`

2. **WHEN** an active *Ticket* has a *Skill Progress* entry with *Review Status* in progress
   **THEN** the reviewing *Agent* avatar appears on the card
   **AND** a magnifying-glass icon replaces the bot icon
   **Evidence:** `kanbanBoard.ts` — `resolveWorkingAgent`; `DeliveryKanbanBoard.tsx` — `MagnifyIcon`

3. **WHEN** the *Focus Skill* is set but no skill has *Execution Status* or *Review Status* in progress
   **THEN** the bot or magnifying-glass skill icon may still appear
   **BUT** no *Agent* avatar renders
   **Evidence:** `kanbanBoard.ts` — `resolveWorkingAgent` returns null; `DeliveryKanbanBoard.tsx` — avatar guard

4. **WHEN** all *Stage Work Required* skills are complete and the ticket sits in stage Done
   **THEN** no *Focus Skill* is resolved and no bot icon appears on the card face
   **Evidence:** `kanbanBoard.ts` — `resolveFocusSkillId` returns null for done sub-column with all skills complete

5. **WHEN** multiple *Skill Progress* entries have *Execution Status* in progress
   **THEN** the first encountered entry is the *Focus Skill*
   **BUT** only one skill icon appears per ticket card
   **Evidence:** `kanbanBoard.ts` — `deriveActiveSkill` first-match logic

---

### Story: Show Review Status on Ticket

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Ticket* — a unit of work tracking skill progress entries
- *Skill Progress* — per-skill execution and review state
- *Review Status* — review cycle state: not started, in progress, done, or failed
- *Agent* — the autonomous worker performing review of a skill

1. **WHEN** a *Ticket* has a *Skill Progress* entry with *Review Status* in progress
   **THEN** a review status dot appears beside the ticket identifier
   **AND** the ticket card displays a magnifying-glass icon color-coded by the *Skill* discipline
   **Evidence:** `DeliveryKanbanBoard.tsx` — review dot, lines 127–129; `MagnifyIcon`, lines 155–156

2. **WHEN** a *Ticket* is under review
   **THEN** the reviewing *Agent* avatar replaces the executing *Agent* avatar on the card
   **Evidence:** `DeliveryKanbanBoard.tsx` — `reviewAgent ?? activeAgent` priority, lines 144–148

3. **WHEN** no *Skill Progress* entry has *Review Status* in progress
   **THEN** no review dot or magnifying-glass icon appears on the card
   **BUT** the executor skill icon (if any) still displays
   **Evidence:** `DeliveryKanbanBoard.tsx` — `isReviewing` guard, lines 111, 127

---

### Story: Highlight Blocked Ticket

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Ticket* — a unit of work carrying free-text notes
- *Notes* — free-text annotation on a ticket; "blocked" signals a blocked status

1. **WHEN** a *Ticket's* *Notes* contain the word "blocked" (case-insensitive)
   **THEN** the ticket card receives the `kb-ticket--blocked` CSS class
   **AND** the card is visually distinguished from non-blocked tickets
   **Evidence:** `DeliveryKanbanBoard.tsx` — `ticketStatusClass`, lines 90–93

2. **WHEN** a *Ticket's* *Notes* do not contain "blocked"
   **THEN** no blocked styling is applied to the card
   **Evidence:** `DeliveryKanbanBoard.tsx` — `ticketStatusClass` returns empty string, line 93

3. **WHEN** a *Ticket's* *Notes* contain "Blocked" or "BLOCKED" (any casing)
   **THEN** the blocked highlight still applies
   **BUT** the raw *Notes* text is not displayed on the card face
   **Evidence:** `DeliveryKanbanBoard.tsx` — `toLowerCase().includes('blocked')`, line 91

---

### Story: Animate Ticket on Position Change

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Ticket* — a unit of work that moves between stages on the kanban board
- *Board Position* — the stage a ticket currently occupies; changes between polls reveal movement

1. **WHEN** a *Ticket* changes *Board Position* between successive polls (stage, sub-state, or active skill change)
   **THEN** the ticket card receives an animation class triggering a movement animation
   **Evidence:** `useDeliveryBoardPoll.ts` — position comparison, lines 48–63; `DeliveryKanbanBoard.tsx` — moved class, line 121

2. **WHEN** a *Ticket's* *Board Position* is encoded as stage, sub-state, and active skill
   **THEN** any change in that composite key between polls marks the ticket as moved
   **AND** the previous position map is updated for the next comparison
   **Evidence:** `useDeliveryBoardPoll.ts` — `ticketPosition` function, lines 5–15; map update, line 61

3. **WHEN** a *Ticket* appears for the first time (no prior *Board Position* recorded)
   **THEN** the ticket is not marked as moved
   **BUT** its position is recorded for future comparison
   **Evidence:** `useDeliveryBoardPoll.ts` — `prev && prev !== pos` guard, line 60

---

## Inspect Skill Progress

### Story: Expand Ticket Skill List

**Story type:** user

**Domain terms** (vocabulary for this story's AC):

- *Ticket* — a unit of work tracking skill progress entries
- *Stage Work Required* — the ordered list of skills required by the ticket's current stage
- *Skill Progress* — per-skill execution and review state on a ticket
- *Board Position* — expansion is available for active and stage-complete tickets, not stage queue

1. **WHEN** the Delivery Lead clicks the expand button (+) on an eligible *Ticket* card
   **THEN** the card expands to show the full *Stage Work Required* for that *Ticket's* *Stage*
   **AND** each *Skill* row shows its label
   **Evidence:** `DeliveryKanbanBoard.tsx` — expand toggle and `kb-ticket-skills-expand`

2. **WHEN** the skill list is expanded
   **THEN** clicking the button again (−) collapses the list
   **Evidence:** `DeliveryKanbanBoard.tsx` — `setExpanded` toggle

3. **WHEN** the *Ticket* is in a *Stage* "Queue" sub-column or the global Backlog column
   **THEN** no expand button appears on the card
   **BUT** the abbreviated ID and display name still render
   **Evidence:** `kanbanBoard.ts` — `ticketCanExpand` (queue / backlog column guard)

4. **WHEN** the *Ticket* is in the board `active` array at a *Stage*
   **THEN** the expand button appears regardless of In Progress or Done sub-column placement
   **Evidence:** `kanbanBoard.ts` — `ticketCanExpand` (active column)

5. **WHEN** an archived *Ticket* with *Skill Progress* appears in a *Stage* "Done" sub-column
   **THEN** the expand button appears so the Delivery Lead can inspect completed skills
   **Evidence:** `kanbanBoard.ts` — `ticketCanExpand` (archived + `hasSkillProgress`)

---

### Story: Show Skill Execution and Completion Indicators

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Skill Progress* — per-skill execution and review state on a ticket
- *Execution Status* — skill progress state: not started, in progress, or done
- *Review Status* — review cycle state: not started, in progress, done, or failed
- *Skill* — named practice method shown in the expanded skill list

1. **WHEN** the expanded skill list shows a *Skill* with both *Execution Status* and *Review Status* done
   **THEN** a checkmark icon appears beside the skill label
   **AND** the row is styled as completed
   **Evidence:** `DeliveryKanbanBoard.tsx` — `DoneIcon` and `is-done` class

2. **WHEN** a *Skill* is the currently executing skill (*Execution Status* in progress)
   **THEN** a bot icon appears beside that skill's label only
   **AND** the row is styled as active
   **Evidence:** `DeliveryKanbanBoard.tsx` — `isExecuting` guard and `ChatbotIcon`

3. **WHEN** a *Skill* is under review (*Review Status* in progress, or execution done awaiting review)
   **THEN** a magnifying-glass icon appears beside that skill's label only
   **AND** the bot icon does not appear on other skill rows
   **Evidence:** `DeliveryKanbanBoard.tsx` — `isUnderReview` guard and `MagnifyIcon`

4. **WHEN** a *Skill* has not yet started and is not the *Focus Skill*
   **THEN** no icon appears beside the skill label
   **AND** the row is styled as pending
   **Evidence:** `kanbanBoard.ts` — `skillRowDisplayState` pending branch

5. **WHEN** a *Skill* is the *Focus Skill* between executions (not yet started, ticket in In Progress)
   **THEN** a bot icon appears beside that skill's label in the expanded list
   **AND** the row is styled as active
   **Evidence:** `kanbanBoard.ts` — `skillRowDisplayState` focus branch

6. **WHEN** a bot or magnifying-glass skill icon renders on the dark ticket theme
   **THEN** the icon uses `currentColor` from its discipline family class
   **AND** the icon remains visible against the ticket and expand-panel background
   **Evidence:** `DeliveryKanbanBoard.tsx` — `ChatbotIcon`, `MagnifyIcon`; `kanban.css` — `.kb-skill-icon--bot`, `.kb-skill-icon--review`

---

### Story: Color-Code Skills by Family

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Skill* — a named practice method, visually grouped by discipline family
- *Stage Work Required* — the ordered list of skills shown as chips beneath each stage

1. **WHEN** a *Skill* chip or expanded skill row renders
   **THEN** the element receives a CSS class derived from the *Skill* discipline family
   **AND** the color distinguishes the discipline visually
   **Evidence:** `DeliveryKanbanBoard.tsx` — `familyCssClass` calls, lines 109, 167, 256

2. **WHEN** the active skill icon appears on a *Ticket* card
   **THEN** the icon inherits the color class of the active *Skill's* discipline family
   **Evidence:** `DeliveryKanbanBoard.tsx` — `famClass` applied to bot/magnify icon, lines 153–158

3. **WHEN** a *Skill* identifier is resolved via the skill registry
   **THEN** the registry returns the discipline family and display label
   **BUT** unknown skill identifiers fall back to a default discipline classification
   **Evidence:** `kanbanBoard.ts` — `SkillFamily` type, lines 53–60; `DeliveryKanbanBoard.tsx` — `skillFamilyFor`, line 109

---

# Assemble Board for Display

### Story: Show Ticket Skill Activity on Load

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Ticket* — a unit of work carrying skill progress entries written by agents
- *Skill Progress* — per-skill execution and review state on a ticket
- *Skill* — named practice method an agent is executing or has completed

1. **WHEN** the *Kanban Board* is loaded and a *Ticket* has *Skill Progress* entries
   **THEN** the board shows which *Skill* is currently being executed (first in-progress entry)
   **AND** which *Skill* is being reviewed (first in-progress review)
   **AND** which *Skills* are done (all completed entries)
   **Evidence:** `kanbanBoard.ts` — `deriveActiveSkill`, lines 252–280

2. **WHEN** a *Ticket* has no *Skill Progress* entries
   **THEN** the *Ticket* displays with no skill indicators and no agent avatars
   **BUT** the *Ticket* card is still renderable with its name and identifier
   **Evidence:** `kanbanBoard.ts` — nulls for empty progress, lines 259–263

3. **WHEN** the *Kanban Board* is loaded with a corrupt or invalid board file
   **THEN** the Delivery Lead sees an error — no partial or misleading board is shown
   **Evidence:** `kanbanBoard.ts` — `KanbanBoardSchema.parse`, line 140

---

### Story: Resolve Stage Skills from Board Configuration

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Kanban Board* — defines ordered stages and the skills required at each
- *Stage Work Required* — the ordered skills required by a stage
- *Stage* — a named phase of delivery work

1. **WHEN** the *Kanban Board* is loaded
   **THEN** each *Stage* shows which *Skills* are required (the *Stage Work Required*)
   **AND** each *Skill* displays its label and is color-coded by discipline
   **Evidence:** `KanbanBoardLoader.ts` — `buildStageSkillRails`, line 28

2. **WHEN** the *Kanban Board* specifies a named stage configuration
   **THEN** that configuration determines which *Stages* are active and what *Skills* each requires
   **BUT** when no configuration is named, the default is used
   **Evidence:** `KanbanBoardLoader.ts` — `defName`, lines 27–28

3. **WHEN** the active stage configuration omits stages
   **THEN** only the configured *Stages* appear on the board
   **BUT** when no active stages are defined, all stages except "context" are shown
   **Evidence:** `KanbanBoardLoader.ts` — `stageFlow` fallback, lines 31–33

---

### Story: Determine Agent Liveness on Load

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Agent* — autonomous worker (product-owner, business-expert, ux-designer, engineer)
- *Kanban Lead* — the orchestrating role
- *Heartbeat* — timestamp each agent writes to signal it is alive

1. **WHEN** the *Kanban Board* is loaded
   **THEN** the application checks each *Agent's* and the *Kanban Lead's* last *Heartbeat*
   **AND** computes how many seconds have elapsed since each last reported activity
   **Evidence:** `kanbanBoard.service.ts` — heartbeat reading, lines 60–79

2. **WHEN** an *Agent* has no *Heartbeat* file
   **THEN** that *Agent* role appears as inactive on the board
   **BUT** the rest of the board loads normally
   **Evidence:** `kanbanBoard.service.ts` — null fallback, lines 72–76

---

## Serve Board State

### Story: Deliver Board State to the Display

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Kanban Board* — the live board the Delivery Lead views
- *Ticket* — units of work flowing through stages

1. **WHEN** the board display requests the current *Kanban Board* state
   **THEN** the application reads the board and its stage configuration from the planning folder
   **AND** delivers the assembled state to the display for rendering
   **Evidence:** `kanbanBoard.service.ts` — `loadSnapshot`, lines 34–58

2. **WHEN** the *Kanban Board* has not changed since the last delivery
   **THEN** the application signals "no change" and the display retains its current view
   **BUT** no redundant data is transmitted
   **Evidence:** `kanbanBoard.routes.ts` — ETag comparison, lines 39–42

3. **WHEN** the planning folder is not configured
   **THEN** the application reports "Planning root not configured" to the Delivery Lead
   **BUT** no board loading is attempted
   **Evidence:** `kanbanBoard.routes.ts` — missing planningRoot guard, lines 32–35

---

### Story: Report Missing Board to Delivery Lead

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Kanban Board* — the persistent board file required before display
- *Kanban Lead* — the orchestrating role that initializes the board

1. **WHEN** the planning folder exists but the *Kanban Board* has not been initialized
   **THEN** the application displays: "board.json missing. Initialize with kanban-lead setup."
   **Evidence:** `kanbanBoard.service.ts` — board file check, lines 44–49

2. **WHEN** the planning folder itself does not exist
   **THEN** the application displays: "Planning folder not found: {path}"
   **BUT** no further file reads are attempted
   **Evidence:** `kanbanBoard.service.ts` — planning root existence check, lines 39–42

3. **WHEN** the planning folder and *Kanban Board* file both exist
   **THEN** the board loads and displays normally
   **Evidence:** `kanbanBoard.service.ts` — successful path, lines 51–83

---

# Keep Board Live

### Story: Keep Board Display Current

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Kanban Board* — the live board with tickets flowing through stages
- *Ticket* — a unit of work whose movement the Delivery Lead observes in real time

1. **WHEN** the Delivery Lead opens the board
   **THEN** the application immediately fetches and displays the current *Kanban Board* state
   **AND** continues refreshing at a regular interval so the Delivery Lead sees *Agent* activity as it happens
   **Evidence:** `useDeliveryBoardPoll.ts` — initial poll and interval, lines 40–46

2. **WHEN** the *Kanban Board* has not changed since the last refresh
   **THEN** the display holds steady — no flicker, no redundant re-render
   **Evidence:** `deliveryBoard.api.ts` — 304 handling, line 15

3. **WHEN** an *Agent* moves a *Ticket* between refreshes
   **THEN** the Delivery Lead sees the *Ticket* card animate to its new *Stage*
   **AND** the *Ticket's* prior position is forgotten for the next comparison
   **Evidence:** `useDeliveryBoardPoll.ts` — position comparison, lines 56–61

4. **WHEN** the Delivery Lead switches to a different planning folder
   **THEN** the previous board state is cleared and a fresh load begins immediately
   **Evidence:** `useDeliveryBoardPoll.ts` — effect cleanup, lines 40–46

---

### Story: Show Board Loading and Error State

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Kanban Board* — the board state being fetched or that failed to load

1. **WHEN** the board is loading
   **THEN** the Delivery Lead sees "Loading…" in the status bar
   **Evidence:** `App.tsx` — loading indicator, line 74

2. **WHEN** the board loads successfully
   **THEN** the status bar shows the time of the last successful refresh
   **Evidence:** `App.tsx` — polled time, line 74

3. **WHEN** the board fails to load
   **THEN** the Delivery Lead sees a red error banner with a meaningful message
   **BUT** the last successful board view remains displayed
   **Evidence:** `App.tsx` — error banner, line 78

4. **WHEN** the next refresh succeeds after an error
   **THEN** the error banner disappears and the board updates
   **Evidence:** `useDeliveryBoardPoll.ts` — error cleared on success, line 31

---

# Manage Agent Pool

## Display Agent Pool

### Story: Render Agent Avatars by Role

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Agent* — autonomous worker with a delivery role (product-owner, business-expert, ux-designer, engineer)
- *Team* — executor and reviewer pair counts per agent role configured on the kanban board

1. **WHEN** the agent pool bar renders
   **THEN** each *Agent* role displays a group with the role's full name (Product Owner, Business Expert, UX Designer, Engineer)
   **AND** the number of avatar circles matches the executor count from the *Team* configuration
   **Evidence:** `DeliveryKanbanBoard.tsx` — `AgentPoolGroup`, lines 356–395; `AgentPoolBar`, lines 397–456

2. **WHEN** an *Agent* role's executor count is zero
   **THEN** one avatar still renders but in the inactive state
   **Evidence:** `DeliveryKanbanBoard.tsx` — `Math.max(total, 1)` minimum, line 376; inactive state for total=0, line 383

3. **WHEN** active *Tickets* engage an *Agent* role
   **THEN** the engaged count for that role is derived from active board state — live execution or review plus *display focus* on the next incomplete *skill*
   **AND** avatars up to the engaged count display as "working" with a role-color ring; remaining avatars display as "idle"
   **Evidence:** `kanbanBoard.ts` — `countRoleEngagement`, `resolveDisplayFocusSkillId`; `DeliveryKanbanBoard.tsx` — `AgentPoolBar` engagedCounts memo; `kanban.css` — `.kb-agent-avatar--working`

---

### Story: Show Role Engagement in Agent Pool

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Role engagement* — count of active *tickets* where an *agent role* is executing, reviewing, or holds *display focus*
- *Display focus* — *focus skill* after per-role WIP from *team* capacity is applied
- *Pool avatar state* — working, idle, or inactive appearance of an avatar in the agent pool

1. **WHEN** an *Agent* role has live execution or review on an active *Ticket*
   **THEN** that role's engaged count includes that *Ticket*
   **AND** at least one avatar for the role displays as "working"
   **Evidence:** `kanbanBoard.ts` — `countRoleEngagement` live branch; `resolveWorkingAgent`

2. **WHEN** an active *Ticket* in **in progress** has *display focus* on a *skill* requiring an *Agent* role
   **THEN** that role's engaged count includes the *Ticket* even if no *heartbeat* file exists
   **AND** the first avatar slot for the role displays as "working"
   **Evidence:** `kanbanBoard.ts` — `countRoleEngagement` focus branch; `board_snapshot_server.test.ts` — engagement without heartbeat

3. **WHEN** an *Agent* role has zero engagement and no fresh *Heartbeat*
   **THEN** unoccupied avatar slots display as "idle" if no *heartbeat* file exists
   **BUT** display as "inactive" (dim) only when a *heartbeat* file exists and age is 120 seconds or more
   **Evidence:** `kanbanBoard.ts` — `resolvePoolAvatarState`; `skill_focus_server.test.ts` — pool avatar state scenarios

---

### Story: Indicate Agent Liveness from Heartbeat

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Heartbeat* — per-role timestamp recording last activity
- *Agent* — delivery role whose liveness is assessed

1. **WHEN** a *Heartbeat* age is less than 120 seconds
   **THEN** the *Agent* role is considered alive
   **AND** its avatars display as "idle" or "working" based on current assignments
   **Evidence:** `kanbanBoard.ts` — `HEARTBEAT_STALE_SECS`, `resolvePoolAvatarState`

2. **WHEN** a *Heartbeat* age is 120 seconds or more
   **THEN** the *Agent* role is considered stale
   **AND** all avatars for that role display in the "inactive" state
   **BUT** avatars up to the engaged count still display as "working" when the role has board engagement
   **Evidence:** `kanbanBoard.ts` — `resolvePoolAvatarState`; `HEARTBEAT_STALE_SECS`

3. **WHEN** a *Heartbeat* age is null (no heartbeat file found)
   **THEN** unengaged avatar slots display as "idle" (lit), not "inactive"
   **Evidence:** `kanbanBoard.ts` — `resolvePoolAvatarState`; `skill_focus_server.test.ts` — no heartbeat idle scenario

---

### Story: Display Kanban Lead Status

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Kanban Lead* — orchestrating role that manages the kanban board
- *Heartbeat* — timestamp recording last kanban lead activity

1. **WHEN** the agent pool bar renders
   **THEN** the *Kanban Lead* displays as a separate group labelled "Kanban Lead" with a single avatar
   **AND** the group appears before the agent role groups, separated by a divider
   **Evidence:** `DeliveryKanbanBoard.tsx` — kanban-lead group, lines 429–434; divider, line 436

2. **WHEN** the *Kanban Lead's* *Heartbeat* age is under 120 seconds
   **THEN** the avatar displays in the "idle" state
   **Evidence:** `DeliveryKanbanBoard.tsx` — `klAlive` check, lines 424–425; avatar state, line 432

3. **WHEN** the *Kanban Lead's* *Heartbeat* age is 120 seconds or more
   **THEN** the avatar displays in the "inactive" state with tooltip "no thread"
   **BUT** when the *Heartbeat* file is missing the avatar displays as "idle"
   **Evidence:** `DeliveryKanbanBoard.tsx` — kanban lead avatar state; `AgentAvatar` tooltip

---

## Adjust Team Size

### Story: Scale Agent Pool Up or Down

**Story type:** user

**Domain terms** (vocabulary for this story's AC):

- *Agent* — autonomous worker with a delivery role
- *Team* — executor and reviewer pair counts per agent role on the kanban board

1. **WHEN** the Delivery Lead clicks "+" on an *Agent* role's pool group
   **THEN** the *Team* gains one more executor for that role
   **AND** the board immediately reflects the new avatar count
   **Evidence:** `DeliveryKanbanBoard.tsx` — adjust handler, lines 371–374

2. **WHEN** the Delivery Lead clicks "−" on an *Agent* role's pool group
   **THEN** the *Team* loses one executor for that role
   **AND** the board immediately reflects the reduced avatar count
   **Evidence:** `DeliveryKanbanBoard.tsx` — adjust(-1), line 390

3. **WHEN** the *Agent* role's executor count is already zero
   **THEN** the "−" button is disabled
   **BUT** the "+" button remains available
   **Evidence:** `DeliveryKanbanBoard.tsx` — disabled guard, line 390

4. **WHEN** the *Team* adjustment cannot be saved
   **THEN** the board remains unchanged — no partial state is shown
   **Evidence:** `DeliveryKanbanBoard.tsx` — null check, line 373

5. **WHEN** a *Team* size change is saved
   **THEN** the *Kanban Board* persists the new count
   **AND** the count can never go below zero regardless of how many times "−" is attempted
   **Evidence:** `kanbanBoard.service.ts` — `Math.max(0, ...)`, line 100

---

# Configure Planning Folder

### Story: Connect Board to a Planning Folder

**Story type:** user

**Domain terms** (vocabulary for this story's AC):

- *Kanban Board* — the live board loaded from the planning folder
- *Kanban Lead* — the orchestrating role that initializes boards in a planning folder

1. **WHEN** the Delivery Lead enters a planning folder path and clicks "Connect"
   **THEN** the application loads the *Kanban Board* from that folder
   **AND** the board display populates with *Tickets* and *Stages*
   **AND** the Delivery Lead sees "Planning folder connected."
   **Evidence:** `App.tsx` — `applyPlanningRoot`, lines 27–37

2. **WHEN** the Delivery Lead returns in a later session
   **THEN** the board remembers the last connected folder and loads it automatically
   **Evidence:** `App.tsx` — localStorage init, line 13

3. **WHEN** the folder path is invalid or the *Kanban Board* has not been initialized
   **THEN** the Delivery Lead sees an error message explaining what is wrong
   **BUT** the previously connected folder is not lost
   **Evidence:** `App.tsx` — error catch, lines 34–36

4. **WHEN** the Delivery Lead provides an empty path
   **THEN** the application rejects it with "planningRoot required"
   **Evidence:** `kanbanBoard.routes.ts` — empty guard, lines 17–20

---

### Story: Refresh Board from Disk

**Story type:** user

**Domain terms** (vocabulary for this story's AC):

- *Kanban Board* — the live board whose on-disk state may have changed externally

1. **WHEN** the Delivery Lead clicks "Refresh"
   **THEN** the application re-reads the *Kanban Board* from disk
   **AND** the display updates with the latest state
   **AND** the Delivery Lead sees "Re-read board.json from disk."
   **Evidence:** `App.tsx` — `handleRefresh`, lines 39–42

2. **WHEN** the refresh fails
   **THEN** the error is shown to the Delivery Lead
   **BUT** the last successful board view remains visible
   **Evidence:** `useDeliveryBoardPoll.ts` — error handling, lines 33–34

---

# React to Agent Activity

### Story: Board Reflects Agent Changes Automatically

**Story type:** system

**Domain terms** (vocabulary for this story's AC):

- *Kanban Board* — the live board that agents write to as they work
- *Agent* — autonomous worker whose actions change the board on disk
- *Heartbeat* — timestamp each agent writes to signal liveness

1. **WHEN** an *Agent* writes to the *Kanban Board* (moves a *Ticket*, updates *Skill Progress*, writes a *Heartbeat*)
   **THEN** the application detects the on-disk change
   **AND** the Delivery Lead's display refreshes on its next poll cycle — no manual refresh needed
   **Evidence:** `warRoomWatcher.ts` — watch method, lines 17–40

2. **WHEN** multiple *Agents* write in rapid succession
   **THEN** the application coalesces the changes into a single refresh
   **BUT** no update is lost — the refresh always reads the latest state
   **Evidence:** `warRoomWatcher.ts` — debounce, lines 49–54

3. **WHEN** an *Agent* writes a file that is not part of the *Kanban Board* (e.g. strategy documents)
   **THEN** no board refresh is triggered
   **Evidence:** `warRoomWatcher.ts` — pattern guard, line 28

4. **WHEN** the Delivery Lead switches planning folders
   **THEN** the application stops watching the old folder and begins watching the new one
   **Evidence:** `warRoomWatcher.ts` — stop and restart, lines 18–24

---
