# Specification by Example — Delivery Agent Kanban

**Sources / context:** `docs/domain/ubiquitous-language.md`, `docs/domain/crc.md`, `docs/acceptance-criteria.md`

---

## Story: Organize Tickets into Stage Groups by Delivery Phase

**Story type:** system

**Sources / context:** Kanban Board KA — stages, tickets, board position

---

## Scenarios

### Scenario 1: Tickets grouped under their assigned stages

Given a *Kanban Board* with *Stages* "shaping", "discovery", "exploration"
  And a *Ticket* **#101** "Build Domain Model" at *Stage* "discovery"
  And a *Ticket* **#102** "Write Acceptance Tests" at *Stage* "exploration"
When the board renders
Then *Ticket* **#101** appears in the "discovery" *Stage* column
  And *Ticket* **#102** appears in the "exploration" *Stage* column
  And the *Stages* are arranged left to right: shaping, discovery, exploration

### Scenario 2: Stage shows Queue, In Progress, and Done sub-columns

Given a *Kanban Board* with *Stage* "specification"
  And *Ticket* **inc-sprint-a** is in the board backlog array at "specification" (stage queue)
  And *Ticket* **inc-sprint-b** is in the board active array at "specification" with a skill executing
  And *Ticket* **inc-sprint-c** is in the board active array at "specification" with all stage skills complete
When the board renders
Then the "specification" column shows sub-columns "Queue", "In Progress", and "Done"
  And **inc-sprint-a** appears under "Queue"
  And **inc-sprint-b** appears under "In Progress"
  And **inc-sprint-c** appears under "Done"

### Scenario 3: Stage queue tickets do not appear in global Backlog

Given *Ticket* **inc-sprint-a** is in the board backlog array with *Stage* "specification"
When the board renders
Then **inc-sprint-a** does not appear in the global Backlog column
  But **inc-sprint-a** appears in "specification" → "Queue"

### Scenario 4: Empty stage still renders

Given a *Kanban Board* with *Stages* "shaping", "discovery", "exploration"
  And no *Tickets* occupy "shaping"
When the board renders
Then the "shaping" *Stage* column is visible
  But it is visually distinguished as empty

---

## Story: Show Assigned Skills per Stage

**Story type:** system

**Sources / context:** Kanban Board KA — stage work required, skill

---

## Scenarios

### Scenario 1: Stage skill rail appears with skill chips

Given a *Kanban Board* where "discovery" *Stage Work Required* includes *Skills*:
  | skill_name                | delivery_role    |
  | abd-ubiquitous-language   | business-expert  |
  | abd-domain-sketch         | business-expert  |
When the board renders
Then the "discovery" *Stage* shows a skill rail beneath it
  And the rail contains chips labelled "abd-ubiquitous-language" and "abd-domain-sketch"

### Scenario 2: Stage with no skills shows no rail

Given a *Kanban Board* where "context" *Stage Work Required* is empty
When the board renders
Then no skill rail appears beneath the "context" *Stage*
  But the *Stage* column itself still renders

---

## Story: Display Backlog Tickets

**Story type:** system

**Sources / context:** Kanban Board KA — ticket, board position, lineage, priority

---

## Scenarios

### Scenario 1: Backlog tickets ordered by priority

Given a *Kanban Board* with backlog *Tickets*:
  | ticket_id | lineage                              | priority |
  | STORY-003 | ["PetStore", "Sprint 1", "Add Pet"]  | 1        |
  | STORY-007 | ["PetStore", "Sprint 1", "List Pets"]| 2        |
When the board renders the Backlog column
Then *Ticket* "STORY-003" appears above "STORY-007"
  And each card shows an abbreviated ID and a display name derived from the last *Lineage* element

### Scenario 2: Hovering backlog ticket shows full lineage

Given a *Ticket* **STORY-003** with *Lineage* ["PetStore", "Sprint 1", "Add Pet"]
When the Delivery Lead hovers the card
Then a tooltip shows "PetStore > Sprint 1 > Add Pet"

### Scenario 3: Empty backlog renders without cards

Given a *Kanban Board* with no *Tickets* in backlog
When the board renders
Then the Backlog column is visible with its heading
  But no ticket cards appear

---

## Story: Animate Ticket on Position Change

**Story type:** system

**Sources / context:** Kanban Board KA — ticket, board position, stage

---

## Scenarios

### Scenario 1: Ticket moves stage and animates

Given the *Kanban Board* was last seen with *Ticket* **#101** at *Stage* "discovery" in-progress
When an *Agent* advances **#101** to *Stage* "discovery" done
  And the board refreshes
Then *Ticket* **#101** card animates to the "Done" sub-column

### Scenario 2: New ticket does not animate

Given *Ticket* **#301** appears for the first time (no prior position)
When the board refreshes
Then *Ticket* **#301** renders without animation
  But its position is recorded for future comparison

---

## Story: Show Active Skill and Agent on Ticket

**Story type:** system

**Sources / context:** Agent and Skills KA — agent, skill progress

---

## Scenarios

### Scenario 1: Executing agent shown on ticket

Given *Ticket* **#101** has *Skill Progress* for "abd-ubiquitous-language" with *Execution Status* "in progress"
  And the executing *Agent* role is "business-expert"
When the board renders
Then *Ticket* **#101** shows a bot icon color-coded by the skill's discipline
  And a "business-expert" avatar appears on the card

### Scenario 2: Focus skill shown between executions

Given *Ticket* **inc-sprint-2** is in the board active array at *Stage* "specification" → "In Progress"
  And *Skill Progress* for "abd-class-responsibility-collaborator" is complete
  And no *Skill* has *Execution Status* or *Review Status* in progress
When the board renders
Then the *Focus Skill* is "abd-specification-by-example"
  And **inc-sprint-2** shows a bot icon on the card face
  And expanding shows a bot beside "Spec by Example" and a checkmark beside "CRC"

### Scenario 3: Bot icon visible without agent avatar

Given *Ticket* **inc-sprint-2** has a *Focus Skill* but no assigned *Agent*
When the board renders
Then **inc-sprint-2** shows the bot icon
  But no agent avatar appears

### Scenario 4: Reviewing agent replaces executor

Given *Ticket* **#101** has *Skill Progress* for "abd-ubiquitous-language" with *Review Status* "in progress"
  And the reviewing *Agent* role is "engineer"
When the board renders
Then *Ticket* **#101** shows a magnifying-glass icon
  And the "engineer" reviewer avatar replaces the executor avatar

---

## Story: Expand Ticket Skill List

**Story type:** user

**Sources / context:** Inspect Skill Progress — expand/collapse stage work required

---

## Scenarios

### Scenario 1: Delivery Lead expands active ticket skill list

Given *Ticket* **inc-sprint-1** is in the board active array at *Stage* "specification"
  And "specification" *Stage Work Required* lists five *Skills*
When the Delivery Lead clicks "+" on **inc-sprint-1**
Then the card expands to show all five *Skill* rows with labels

### Scenario 2: Stage queue ticket has no expand control

Given *Ticket* **inc-sprint-3** is in the board backlog array at *Stage* "specification"
When the board renders **inc-sprint-3** in "specification" → "Queue"
Then no expand button appears on the card

### Scenario 3: Archived stage-complete ticket expands in stage Done

Given archived *Ticket* **inc-8-marketing-engine** completed *Stage* "exploration" and scattered to sprints
When the board renders **inc-8-marketing-engine** in "exploration" → "Done"
Then the expand button appears
  And expanding shows checkmarks beside completed exploration *Skills*

---

## Story: Show Skill Execution and Completion Indicators

**Story type:** system

**Sources / context:** Inspect Skill Progress — bot, magnifying glass, checkmark per skill row

---

## Scenarios

### Scenario 1: Completed skill shows checkmark in expanded list

Given *Ticket* **#101** has *Skill Progress* for "abd-class-responsibility-collaborator" with execution and review done
When the Delivery Lead expands **#101**
Then the "CRC" row shows a checkmark icon beside the skill label

### Scenario 2: Executing skill shows bot icon on that row only

Given *Ticket* **#101** has *Skill Progress* for "abd-specification-by-example" with *Execution Status* "in progress"
When the Delivery Lead expands **#101**
Then only the "Spec by Example" row shows a bot icon

### Scenario 3: Skill under review shows magnifying glass on that row only

Given *Ticket* **#101** has *Skill Progress* for "abd-specification-by-example" with *Review Status* "in progress"
When the Delivery Lead expands **#101**
Then only the "Spec by Example" row shows a magnifying-glass icon
  And no other row shows a bot icon

### Scenario 4: Pending skill shows no icon

Given *Ticket* **#101** has not started "abd-scenario-walkthrough"
  And "abd-scenario-walkthrough" is not the *Focus Skill*
When the Delivery Lead expands **#101**
Then the "Scenario Walkthrough" row has no icon and is styled as pending

### Scenario 5: Focus skill shows bot between executions

Given *Ticket* **inc-sprint-2** is active in "specification" → "In Progress"
  And "abd-class-responsibility-collaborator" is complete
  And "abd-specification-by-example" has not started
When the Delivery Lead expands **inc-sprint-2**
Then the "Spec by Example" row shows a bot icon
  And the "CRC" row shows a checkmark

### Scenario 6: Skill icons use theme-visible colors

Given the board uses the engineering dark ticket theme
When a bot or magnifying-glass icon renders on a skill row
Then the icon stroke and fill inherit the discipline family color via `currentColor`
  And the icon is visible against the ticket background

---

## Story: Indicate Agent Liveness from Heartbeat

**Story type:** system

**Sources / context:** Agent and Skills KA — agent, heartbeat

---

## Scenarios

### Scenario 1: Agent alive — heartbeat recent

Given the *Agent* role "engineer" last wrote a *Heartbeat* 30 seconds ago
When the board renders the agent pool
Then the "engineer" avatars display as "idle" or "working"

### Scenario 2: Agent inactive — heartbeat stale with no board engagement

Given the *Agent* role "engineer" last wrote a *Heartbeat* 180 seconds ago
  And no active *Ticket* engages "engineer"
When the board renders the agent pool
Then all "engineer" avatars display in the "inactive" state

### Scenario 3: Agent idle — no heartbeat file

Given the *Agent* role "ux-designer" has no *Heartbeat* file
  And no active *Ticket* engages "ux-designer"
When the board renders the agent pool
Then the "ux-designer" avatars display as "idle" (lit), not "inactive"

### Scenario 4: Agent working — board engagement without heartbeat

Given the *Agent* role "product-owner" has no *Heartbeat* file
  And an active *Ticket* in **in progress** has *display focus* on a *skill* requiring "product-owner"
When the board renders the agent pool
Then the first "product-owner" avatar displays as "working"
  And the avatar is lit with a role-color ring

### Scenario 5: Agent working — stale heartbeat but board engagement

Given the *Agent* role "business-expert" last wrote a *Heartbeat* 180 seconds ago
  And an active *Ticket* engages "business-expert" via *display focus*
When the board renders the agent pool
Then the first "business-expert" avatar displays as "working"
  But unengaged slots for "business-expert" display as "inactive"

---

## Story: Show Role Engagement in Agent Pool

**Story type:** system

**Sources / context:** Agent and Skills KA — role engagement, display focus, pool avatar state

Scenarios 4–5 above exercise this story. Additional coverage: `skill_focus_server.test.ts` (`countRoleEngagement`), `board_snapshot_server.test.ts` (PawPlace board without heartbeat files).

---

## Story: Scale Agent Pool Up or Down

**Story type:** user

**Sources / context:** Kanban Board KA — team; Agent and Skills KA — agent

---

## Scenarios

### Scenario 1: Delivery Lead adds an executor

Given the *Team* has 2 executors for "engineer"
When the Delivery Lead clicks "+" on the "engineer" pool group
Then the *Team* shows 3 executors for "engineer"
  And the board displays 3 avatar circles for "engineer"

### Scenario 2: Delivery Lead removes an executor

Given the *Team* has 2 executors for "business-expert"
When the Delivery Lead clicks "−" on the "business-expert" pool group
Then the *Team* shows 1 executor for "business-expert"

### Scenario 3: Cannot reduce below zero

Given the *Team* has 0 executors for "ux-designer"
When the Delivery Lead views the "ux-designer" pool group
Then the "−" button is disabled
  But the "+" button remains available

---

## Story: Connect Board to a Planning Folder

**Story type:** user

**Sources / context:** Configure Planning Folder AC

---

## Scenarios

### Scenario 1: Successful connection loads the board

Given a valid planning folder at "C:\dev\project\kanban"
  And the folder contains an initialized *Kanban Board*
When the Delivery Lead enters "C:\dev\project\kanban" and clicks "Connect"
Then the board populates with *Tickets* and *Stages*
  And the Delivery Lead sees "Planning folder connected."

### Scenario 2: Invalid folder shows error

Given a planning folder path "C:\dev\nonexistent"
When the Delivery Lead enters the path and clicks "Connect"
Then the Delivery Lead sees "Planning folder not found: C:\dev\nonexistent"
  But the previously connected folder remains active

### Scenario 3: Missing board file shows initialization message

Given a valid planning folder at "C:\dev\project\kanban"
  And the folder has no board.json
When the Delivery Lead enters the path and clicks "Connect"
Then the Delivery Lead sees "board.json missing. Initialize with kanban-lead setup."

---

## Story: Board Reflects Agent Changes Automatically

**Story type:** system

**Sources / context:** React to Agent Activity AC

---

## Scenarios

### Scenario 1: Agent moves a ticket — board refreshes

Given the Delivery Lead is viewing the *Kanban Board*
  And *Ticket* **#101** is at *Stage* "discovery" in-progress
When an *Agent* completes the *Skill* work and advances **#101** to done
  And writes the updated board to disk
Then the Delivery Lead sees **#101** move to the "Done" sub-column on the next refresh
  But no manual refresh is needed

### Scenario 2: Agent writes heartbeat — liveness updates

Given the *Agent* "engineer" was previously inactive (no recent *Heartbeat*)
When the "engineer" *Agent* starts and writes a fresh *Heartbeat*
Then on the next refresh the "engineer" avatars change from "inactive" to "idle"

### Scenario 3: Non-board file changes do not trigger refresh

Given the Delivery Lead is viewing the *Kanban Board*
When an *Agent* writes a strategy.md file in the kanban directory
Then the board display does not refresh

---
