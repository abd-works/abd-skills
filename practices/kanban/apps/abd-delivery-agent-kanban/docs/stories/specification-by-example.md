# Specification by Example — Delivery Agent Kanban

**Sources / context:** `docs/domain/domain-language.md`, `docs/domain/domain model.md`, `docs/acceptance-criteria.md`

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
  | abd-domain-language   | business-expert  |
  | abd-domain-sketch         | business-expert  |
When the board renders
Then the "discovery" *Stage* shows a skill rail beneath it
  And the rail contains chips labelled "abd-domain-language" and "abd-domain-sketch"

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

Given *Ticket* **#101** has *Skill Progress* for "abd-domain-language" with *Execution Status* "in progress"
  And the executing *Agent* role is "business-expert"
When the board renders
Then *Ticket* **#101** shows a bot icon color-coded by the skill's discipline
  And a "business-expert" avatar appears on the card

### Scenario 2: Focus skill shown between executions

Given *Ticket* **inc-sprint-2** is in the board active array at *Stage* "specification" → "In Progress"
  And *Skill Progress* for "abd-domain-model" is complete
  And no *Skill* has *Execution Status* or *Review Status* in progress
When the board renders
Then the *Focus Skill* is "abd-story-specification"
  And **inc-sprint-2** shows a bot icon on the card face
  And expanding shows a bot beside "Spec by Example" and a checkmark beside "domain model"

### Scenario 3: Bot icon visible without agent avatar

Given *Ticket* **inc-sprint-2** has a *Focus Skill* but no assigned *Agent*
When the board renders
Then **inc-sprint-2** shows the bot icon
  But no agent avatar appears

### Scenario 4: Reviewing agent replaces executor

Given *Ticket* **#101** has *Skill Progress* for "abd-domain-language" with *Review Status* "in progress"
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

### Scenario 4: Agent-avatar drop records intent without moving ticket stage

Given the *Kanban Board* is in manual mode
  And *Ticket* **#501** is in "discovery" → "In Progress"
When the user drags a "business-expert" *Team Member Agent* avatar onto **#501**
Then the app records an action intent for the next eligible *Skill*
  And **#501** remains in "discovery" → "In Progress"
  But the drop is not interpreted as a ticket stage-move

---

## Story: Show Skill Execution and Completion Indicators

**Story type:** system

**Sources / context:** Inspect Skill Progress — bot, magnifying glass, checkmark per skill row

---

## Scenarios

### Scenario 1: Completed skill shows checkmark in expanded list

Given *Ticket* **#101** has *Skill Progress* for "abd-domain-model" with execution and review done
When the Delivery Lead expands **#101**
Then the "domain model" row shows a checkmark icon beside the skill label

### Scenario 2: Executing skill shows bot icon on that row only

Given *Ticket* **#101** has *Skill Progress* for "abd-story-specification" with *Execution Status* "in progress"
When the Delivery Lead expands **#101**
Then only the "Spec by Example" row shows a bot icon

### Scenario 3: Skill under review shows magnifying glass on that row only

Given *Ticket* **#101** has *Skill Progress* for "abd-story-specification" with *Review Status* "in progress"
When the Delivery Lead expands **#101**
Then only the "Spec by Example" row shows a magnifying-glass icon
  And no other row shows a bot icon

### Scenario 4: Pending skill shows no icon

Given *Ticket* **#101** has not started "abd-domain-walk"
  And "abd-domain-walk" is not the *Focus Skill*
When the Delivery Lead expands **#101**
Then the "Scenario Walkthrough" row has no icon and is styled as pending

### Scenario 5: Focus skill shows bot between executions

Given *Ticket* **inc-sprint-2** is active in "specification" → "In Progress"
  And "abd-domain-model" is complete
  And "abd-story-specification" has not started
When the Delivery Lead expands **inc-sprint-2**
Then the "Spec by Example" row shows a bot icon
  And the "domain model" row shows a checkmark

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

### Scenario 4: Skill state transitions refresh UI with unchanged ticket/stage counts

Given *Ticket* **project-all** has one *Skill Progress* entry with *Execution Status* "in_progress" and *Review Status* null
When backend stub processing updates that same *Skill Progress* entry to *Execution Status* "done" and *Review Status* "in_progress"
  And ticket IDs and stage counts remain unchanged
Then the polling ETag changes
  And the UI refreshes to show review-in-progress state rather than the prior executing state

---

# Board Flow Logic (Kanban Lead, Agent, and Skill Orchestration)

## Story: Promote Backlog Ticket on Skill Claim

**Story type:** system

**Sources / context:** Kanban Board KA — kanban board, ticket, stage; Agent and Skills KA — team member agent, downstream-first pull

---

## Scenarios

### Scenario 1: Backlog ticket promoted to active when a team member claims its skill

Given a *Kanban Board* with no active *Tickets*
  And the backlog contains *Ticket* **1-external-protocol-integration** at *Stage* "discovery" with *Scope Level* "partition" and *Priority* 1
  And the backlog contains *Ticket* **2-dual-persistence** at *Stage* "discovery" with *Scope Level* "partition" and *Priority* 2
  And a "business-expert" *Team Member Agent* is available
When the scan cycle assigns eligible work
Then *Ticket* **1-external-protocol-integration** moves from backlog to active at *Stage* "discovery"
  And the "business-expert" *Agent* claims the first eligible *Skill* on that *Ticket*
  Because the highest-priority backlog *Ticket* is promoted when claimed

### Scenario 2: Active downstream ticket is preferred over upstream backlog ticket

Given a *Kanban Board* with *Ticket* **1-inc-1** active at *Stage* "exploration" with eligible work for "business-expert"
  And the backlog contains *Ticket* **2-inc-2** at *Stage* "discovery" with eligible work for "business-expert"
  And a "business-expert" *Team Member Agent* is available
When the scan cycle assigns eligible work
Then the "business-expert" *Agent* claims work on **1-inc-1** at *Stage* "exploration"
  And *Ticket* **2-inc-2** remains in the backlog
  Because downstream stages (exploration) are prioritized over upstream stages (discovery)

### Scenario 3: Backlog ticket promoted only when no downstream work exists

Given a *Kanban Board* with no active *Tickets* needing "product-owner"
  And the backlog contains *Ticket* **3-inc-3** at *Stage* "discovery" with eligible work for "product-owner"
  And a "product-owner" *Team Member Agent* is available
When the scan cycle assigns eligible work
Then *Ticket* **3-inc-3** moves from backlog to active
  And the "product-owner" *Agent* claims the first eligible *Skill* on that *Ticket*

---

## Story: Detect Stage Completion on a Ticket

**Story type:** system

**Sources / context:** Kanban Board KA — ticket, skill progress, stage work required

---

## Scenarios

### Scenario 1: Stage complete when all required skills are done

Given *Ticket* **1-external-protocol-integration** is active at *Stage* "discovery"
  And "discovery" *Stage Work Required* includes required *Skills*:
  | skill_name                | role             |
  | abd-domain-terms          | business-expert  |
  | abd-story-mapping         | product-owner    |
  | abd-thin-slicing          | product-owner    |
  | abd-architecture-blueprint| engineer         |
  And *Skill Progress* for all four *Skills* has *Execution Status* "done" and *Review Status* "done"
When the *Kanban Board* checks stage completion for **1-external-protocol-integration**
Then the *Stage* "discovery" is complete for **1-external-protocol-integration**
  And the *Ticket* is eligible to move to done

### Scenario 2: Stage not complete when a required skill has review pending

Given *Ticket* **1-external-protocol-integration** is active at *Stage* "discovery"
  And *Skill Progress* for "abd-domain-terms" has *Execution Status* "done" and *Review Status* "done"
  And *Skill Progress* for "abd-story-mapping" has *Execution Status* "done" and *Review Status* "not started"
When the *Kanban Board* checks stage completion for **1-external-protocol-integration**
Then the *Stage* "discovery" is not complete
  Because *Skill Progress* for "abd-story-mapping" has *Review Status* "not started"

### Scenario 3: Optional skill does not block stage completion

Given *Ticket* **1-inc-1-operator-signon** is active at *Stage* "exploration"
  And "exploration" *Stage Work Required* includes:
  | skill_name                   | role            | optional |
  | abd-domain-language      | business-expert | false    |
  | abd-story-acceptance-criteria      | product-owner   | false    |
  | abd-ux-mockup                | ux-designer     | true     |
  | abd-architecture-specification   | engineer        | false    |
  And *Skill Progress* for "abd-domain-language", "abd-story-acceptance-criteria", and "abd-architecture-specification" all have *Execution Status* "done" and *Review Status* "done"
  And no *Skill Progress* exists for "abd-ux-mockup"
When the *Kanban Board* checks stage completion for **1-inc-1-operator-signon**
Then the *Stage* "exploration" is complete
  Because "abd-ux-mockup" is optional and does not block completion

---

## Story: Scatter Ticket at Scope Boundary

**Story type:** system

**Sources / context:** Kanban Board KA — ticket (scatter into child tickets); Agent and Skills KA — kanban lead (trigger scatter)

---

## Scenarios

### Scenario 1: Completed partition scatters into increment children

Given *Ticket* **1-external-protocol-integration** has completed *Stage* "discovery" at *Scope Level* "partition"
  And the next *Stage* "exploration" has *Scope Level* "increment"
  And thin-slicing defines 4 increments for module 1:
  | child_id                                             | name                    | priority |
  | 1-external-protocol-integration-inc-1-operator-signon| Operator Signon         | 1        |
  | 1-external-protocol-integration-inc-2-message-routing| Message Routing         | 2        |
  | 1-external-protocol-integration-inc-3-session-mgmt   | Session Management      | 3        |
  | 1-external-protocol-integration-inc-4-error-handling  | Error Handling          | 4        |
When the *Kanban Lead* triggers scatter on **1-external-protocol-integration**
Then 4 child *Tickets* are created in the backlog at *Stage* "exploration" with *Scope Level* "increment"
  And each child *Ticket's* *Lineage* extends the parent's *Lineage* with the increment name
  And **1-external-protocol-integration** is archived with *scatter_to* listing all 4 child IDs
  And a "scatter" event is recorded in the metrics log

### Scenario 2: Scatter does not fire when next stage has same scope

Given *Ticket* **1-inc-1-operator-signon** has completed *Stage* "exploration" at *Scope Level* "increment"
  And the next *Stage* "specification" has *Scope Level* "sprint"
When the *Kanban Lead* checks for scatter eligibility on **1-inc-1-operator-signon**
Then **1-inc-1-operator-signon** is eligible for scatter
  Because *Scope Level* "sprint" is finer than "increment"

### Scenario 3: Already-scattered ticket is not scattered again

Given *Ticket* **1-external-protocol-integration** is in done with *scatter_to* ["1-epi-inc-1", "1-epi-inc-2"]
When the *Kanban Lead* checks for scatter eligibility
Then **1-external-protocol-integration** is not eligible for scatter
  Because it already has children recorded in *scatter_to*

### Scenario 4: Child ticket IDs include parent context to prevent collisions

Given *Ticket* **1-external-protocol-integration** scatters at *Stage* "discovery"
  And *Ticket* **2-dual-persistence** also scatters at *Stage* "discovery"
  And both modules define an increment named "Error Handling"
When the *Kanban Lead* generates child IDs
Then **1-external-protocol-integration**'s child is "1-external-protocol-integration-inc-4-error-handling"
  And **2-dual-persistence**'s child is "2-dual-persistence-inc-4-error-handling"
  And no two child *Tickets* share the same *ticket_id*

---

## Story: Advance Ticket to Next Stage (Same Scope)

**Story type:** system

**Sources / context:** Kanban Board KA — ticket (advance to next stage), stage

---

## Scenarios

### Scenario 1: Ticket advances when stage complete and next stage has same scope

Given *Ticket* **1-inc-1-sprint-a** has completed *Stage* "specification" at *Scope Level* "sprint"
  And the next *Stage* "engineering" has *Scope Level* "sprint"
When the *Kanban Board* advances **1-inc-1-sprint-a**
Then **1-inc-1-sprint-a** moves to *Stage* "engineering"
  And *Skill Progress* is cleared for the new stage
  And stage history records "specification" with entered and completed timestamps

### Scenario 2: Ticket does not advance automatically

Given *Ticket* **1-inc-1-sprint-a** has completed all *Skills* at *Stage* "specification"
When no *Agent* or *Kanban Lead* explicitly advances the *Ticket*
Then **1-inc-1-sprint-a** remains in *Stage* "specification" done sub-state
  Because a *Ticket* never advances to the next stage automatically — an actor must pick it up

### Scenario 3: Ticket cannot skip a stage

Given *Ticket* **1-inc-1-sprint-a** is at *Stage* "exploration"
  And the *Kanban Board* defines stages: "exploration", "specification", "engineering"
When an attempt is made to advance **1-inc-1-sprint-a** to "engineering"
Then the advance is rejected
  Because a *Ticket* cannot skip *Stage* "specification"

---

## Story: Agent Claims Next Eligible Skill (Downstream-First Pull)

**Story type:** system

**Sources / context:** Agent and Skills KA — agent (start work on skill), skill; Kanban Board KA — stage work required

---

## Scenarios

### Scenario 1: Agent claims first eligible skill in rail order

Given *Ticket* **1-inc-1-sprint-a** is active at *Stage* "specification"
  And "specification" *Stage Work Required* lists *Skills* in rail order:
  | skill_name                               | role             |
  | abd-domain-model     | business-expert  |
  | abd-story-specification              | product-owner    |
  | abd-architecture-specification                 | engineer         |
  | abd-story-acceptance-test    | engineer         |
  And no *Skill Progress* entries exist yet
When an *Agent* with role "business-expert" looks for eligible work
Then the *Agent* claims "abd-domain-model" on **1-inc-1-sprint-a**
  Because it is the first required *Skill* matching the *Agent's* role

### Scenario 2: Agent skips skills that require prior skills incomplete

Given *Ticket* **1-inc-1-sprint-a** is active at *Stage* "specification"
  And "abd-domain-model" *Skill Progress* has *Execution Status* "not started"
  And "abd-story-specification" is second in the rail and requires "abd-domain-model" done first
When an *Agent* with role "product-owner" looks for eligible work
Then no *Skill* is available for the "product-owner" *Agent*
  Because the prior *Skill* "abd-domain-model" is not done

### Scenario 3: Agent pulls from rightmost stage first (downstream-first)

Given 2 active *Tickets*:
  | ticket_id          | stage          |
  | 1-inc-1-sprint-a   | specification  |
  | 1-inc-2-sprint-b   | exploration    |
  And both have eligible work for role "business-expert"
When the *Agent* with role "business-expert" looks for eligible work
Then the *Agent* claims work on **1-inc-1-sprint-a** at *Stage* "specification"
  Because "specification" is downstream of "exploration" — later stages are prioritized

### Scenario 4: Agent does not claim skill already in progress

Given *Ticket* **1-inc-1-sprint-a** is active at *Stage* "specification"
  And *Skill Progress* for "abd-domain-model" has *Execution Status* "in_progress" with *Agent* "business-expert"
When a second *Agent* with role "business-expert" looks for eligible work
Then "abd-domain-model" on **1-inc-1-sprint-a** is not claimable
  Because a *Skill* with *Execution Status* "in_progress" cannot be claimed by another *Agent*

### Scenario 5: Agent claims review after execution done

Given *Ticket* **1-inc-1-sprint-a** is active at *Stage* "specification"
  And *Skill Progress* for "abd-domain-model" has *Execution Status* "done" and *Review Status* "not started"
When an *Agent* with role "business-expert" looks for eligible review work
Then the *Agent* can claim review of "abd-domain-model" on **1-inc-1-sprint-a**
  Because execution must reach done before review can leave not started

---

## Story: Architecture Reference and Template Run Once per Mechanism

**Story type:** system

**Sources / context:** Agent and Skills KA — skill (conditional execution); Kanban Board KA — stage work required

---

## Scenarios

### Scenario 1: Architecture reference creates registry on first increment

Given *Ticket* **1-inc-1-operator-signon** is the first active increment at *Stage* "exploration"
  And no architecture mechanism registry exists
  And "abd-architecture-specification" is in the *Stage Work Required*
When an *Agent* with role "engineer" claims "abd-architecture-specification"
Then the *Agent* creates the mechanism registry and runs architecture reference
  And *Skill Progress* for "abd-architecture-specification" records *Execution Status* "done"

### Scenario 2: Architecture reference quick pass on subsequent increments

Given *Ticket* **1-inc-2-message-routing** is active at *Stage* "exploration"
  And an architecture mechanism registry already exists from **1-inc-1-operator-signon**
  And all mechanisms in **1-inc-2-message-routing** are already covered by the registry
When an *Agent* with role "engineer" claims "abd-architecture-specification"
Then the *Agent* runs a quick pass and writes `architecture-reference-assignment.md` with assign-only rows
  And *Skill Progress* for "abd-architecture-specification" records *Execution Status* "done" and *Review Status* "done"
  And the *Agent* proceeds to the next eligible *Skill*

### Scenario 3: Architecture template creates for new mechanism only

Given *Ticket* **1-inc-2-sprint-b** is active at *Stage* "specification"
  And the mechanism registry shows "error-handling" already has a template
  And **1-inc-2-sprint-b** introduces a new mechanism "caching"
When an *Agent* with role "engineer" claims "abd-architecture-specification"
Then the *Agent* creates a template only for "caching"
  And "error-handling" is not re-created

---

# Manage Agent Lifecycle via Cursor SDK

## Story: Resolve Agent Definition from Role

**Story type:** system

**Sources / context:** Agent and Skills KA — agent role, agent definition; story-map.md consolidation notes — "Resolve Agent Definition from Role"

---

## Scenarios

### Scenario 1: Role "engineer" resolves to its agent definition

Given the *Kanban Board* workspace root is "C:\dev\project"
  And the agent definitions directory is `practices/kanban/agents/`
  And a file exists at `practices/kanban/agents/engineer/AGENT.md`
When the system resolves the *Agent Definition* for role "engineer"
Then the resolved path is `practices/kanban/agents/engineer/AGENT.md`
  And the definition content is loaded for parsing

### Scenario 2: Role "kanban-lead" resolves to its agent definition

Given the *Kanban Board* workspace root is "C:\dev\project"
  And a file exists at `practices/kanban/agents/kanban-lead/AGENT.md`
When the system resolves the *Agent Definition* for role "kanban-lead"
Then the resolved path is `practices/kanban/agents/kanban-lead/AGENT.md`
  And the definition content is loaded for parsing

### Scenario 3: Unknown role returns error

Given the *Kanban Board* workspace root is "C:\dev\project"
  And no file exists at `practices/kanban/agents/ux-designer/AGENT.md`
When the system resolves the *Agent Definition* for role "ux-designer"
Then the resolution fails with error "Agent definition not found for role: ux-designer"
  And no *Agent Session* is created

---

## Story: Parse Skills from Agent Definition

**Story type:** system

**Sources / context:** Agent and Skills KA — agent definition, skill; story-map.md consolidation notes — "Parse Skills from Agent Definition"

---

## Scenarios

### Scenario 1: Engineer role's eligible skills come from kanban.json stage work required

Given the *Agent Definition* for role "engineer" has been loaded
  And `kanban.json` *Stage Work Required* assigns the following *Skills* to role "engineer":
  | skill_name                            | stage          |
  | abd-architecture-specification            | specification  |
  | abd-architecture-specification             | specification  |
  | abd-story-acceptance-test| specification  |
  And the *Agent Definition* declares one conditional *Skill*: "abd-clean-code"
When the system resolves eligible *Skills* for role "engineer"
Then the resolved skill list contains 3 entries from *Stage Work Required* and 1 conditional
  And the conditional *Skill* is declared in the `AGENT.md`, not in `kanban.json`

### Scenario 2: Business Expert AGENT.md references executor-workflow.md and shared reference files

Given the *Agent Definition* for role "business-expert" has been loaded
  And the `AGENT.md` references `executor-workflow.md` for execution orchestration
  And the `AGENT.md` references `session-bootstrap.md`, `pull-model.md`, and `work-queue.md`
When the system parses the "business-expert" *Agent Definition*
Then the parsed result includes the workflow reference "executor-workflow.md"
  And eligible *Skills* for the role come from `kanban.json` *Stage Work Required*, not from the `AGENT.md`

### Scenario 3: Kanban Lead AGENT.md lists orchestration skills

Given the *Agent Definition* for role "kanban-lead" has been loaded
  And the definition contains orchestration *Skills*:
  | skill_name           |
  | abd-kanban-planning  |
  | abd-kanban           |
When the system parses *Skills* from the "kanban-lead" *Agent Definition*
Then the parsed skill list contains "abd-kanban-planning" and "abd-kanban"
  And the skills are marked as orchestration (not stage work required)

---

## Story: Create Agent Session via Cursor SDK

**Story type:** system

**Sources / context:** Agent and Skills KA — agent, agent session; story-map.md consolidation notes — "Create Agent Session via Cursor SDK"

---

## Scenarios

### Scenario 1: KanbanLead creates TeamMember session with bootstrap prompt

Given the *Kanban Lead* needs to start a *Team Member* with role "engineer"
  And the *Agent Definition* for "engineer" has been resolved and parsed
  And the *Kanban Board* workspace root is "C:\dev\project"
When the *Kanban Lead* creates an *Agent Session* via the Cursor SDK
Then a new *Agent Session* is created with a *Bootstrap Prompt* containing:
  | field          | value                        |
  | workspace      | C:\dev\project               |
  | role           | engineer                     |
  | agent_definition| practices/kanban/agents/engineer/AGENT.md |
  And the workspace path was injected by the *Kanban Lead* from the *Kanban Board* config
  And the session enters "running" state

### Scenario 2: Session creation fails — KanbanLead logs error and retries

Given the *Kanban Lead* attempts to create an *Agent Session* for role "engineer"
  And the Cursor SDK returns a connection error
When the *Agent Session* creation fails
Then the *Kanban Lead* logs error "Agent session creation failed for role: engineer"
  And the *Kanban Lead* retries session creation on the next scan cycle
  But no *Agent Session* is recorded for the role

### Scenario 3: Agent session created with MCP server configuration

Given the *Kanban Lead* creates an *Agent Session* for role "business-expert"
  And the board configuration specifies MCP servers for "business-expert":
  | mcp_server          |
  | user-story_bot      |
  | plugin-granola      |
When the *Agent Session* is created via the Cursor SDK
Then the session includes MCP server configuration for "user-story_bot" and "plugin-granola"
  And the *Agent* can invoke tools from those MCP servers during execution

---

## Story: Start Team Member Agent

**Story type:** system

**Sources / context:** Agent and Skills KA — kanban lead (start team member), team member; story-map.md — "Start Team Member Agent"

---

## Scenarios

### Scenario 1: Kanban Lead starts engineer for eligible skill — session moves to running

Given the *Kanban Lead* is running a scan cycle
  And *Ticket* **1-inc-1-sprint-a** is active at *Stage* "specification" with eligible *Skill* "abd-architecture-specification" for role "engineer"
  And no *Agent Session* for "engineer" is currently running
When the *Kanban Lead* starts a *Team Member* *Agent* for role "engineer"
Then a new *Agent Session* is created and enters "running" state
  And the *Agent* begins executing "abd-architecture-specification" on **1-inc-1-sprint-a**
  And the *Agent Pool* shows the "engineer" avatar as "working"

### Scenario 2: Kanban Lead starts business-expert for first skill in rail order — agent pulls downstream first

Given the *Kanban Lead* is running a scan cycle
  And 2 active *Tickets* have eligible work for role "business-expert":
  | ticket_id          | stage          | skill_name                            |
  | 1-inc-1-sprint-a   | specification  | abd-domain-model |
  | 1-inc-2-sprint-b   | exploration    | abd-domain-language               |
When the *Kanban Lead* starts a *Team Member* *Agent* for role "business-expert"
Then the *Agent* claims "abd-domain-model" on **1-inc-1-sprint-a**
  Because "specification" is downstream of "exploration" — later stages are prioritized

---

## Story: Stop Team Member Agent

**Story type:** system

**Sources / context:** Agent and Skills KA — kanban lead (stop team member), agent session

---

## Scenarios

### Scenario 1: Kanban Lead stops idle team member — session terminates cleanly

Given a *Team Member* *Agent* with role "engineer" has an active *Agent Session*
  And the *Agent* is idle (no *Skill* currently executing)
When the *Kanban Lead* stops the "engineer" *Team Member*
Then the *Agent Session* terminates with status "completed"
  And the *Agent Pool* shows the "engineer" avatar as "idle"
  And no *Skill Progress* entries are modified

### Scenario 2: Stop agent that has in-progress skill — skill progress preserved before termination

Given a *Team Member* *Agent* with role "business-expert" has an active *Agent Session*
  And the *Agent* is executing *Skill* "abd-domain-language" on *Ticket* **1-inc-1-sprint-a**
  And *Skill Progress* has *Execution Status* "in_progress"
When the *Kanban Lead* stops the "business-expert" *Team Member*
Then the *Skill Progress* for "abd-domain-language" retains *Execution Status* "in_progress"
  And the *Agent Session* terminates
  But the skill is not marked as "done" or rolled back
  And the *Kanban Lead* can assign a new *Agent* to resume the skill on the next cycle

---

## Story: Report Agent Session Status via SDK

**Story type:** system

**Sources / context:** Agent and Skills KA — agent session, agent liveness; story-map.md — "Report Agent Session Status via SDK"

---

## Scenarios

### Scenario 1: Running session reports "running" with message count and last activity

Given a *Team Member* *Agent* with role "engineer" has an active *Agent Session*
  And the session has emitted 42 messages
  And the last message was emitted 15 seconds ago
When the system queries *Agent Session* status for "engineer"
Then the status reports:
  | field               | value     |
  | state               | running   |
  | message_count       | 42        |
  | last_activity_sec   | 15        |

### Scenario 2: Completed session reports "completed" with final message

Given a *Team Member* *Agent* with role "business-expert" had an *Agent Session*
  And the session completed after executing "abd-domain-language"
When the system queries *Agent Session* status for "business-expert"
Then the status reports:
  | field          | value                                      |
  | state          | completed                                  |
  | final_message  | Completed abd-domain-language execution |

### Scenario 3: Failed session reports "failed" with error detail

Given a *Team Member* *Agent* with role "engineer" had an *Agent Session*
  And the session failed with a runtime error
When the system queries *Agent Session* status for "engineer"
Then the status reports:
  | field        | value                                    |
  | state        | failed                                   |
  | error_detail | Agent session terminated unexpectedly    |

---

## Story: Restart Stale Agent

**Story type:** system

**Sources / context:** Agent and Skills KA — agent session, agent liveness, kanban lead (restart)

---

## Scenarios

### Scenario 1: Agent session stale — KanbanLead stops and creates new session

Given a *Team Member* *Agent* with role "engineer" has an active *Agent Session*
  And the session has not emitted any output for 120 seconds
  And the *Agent* has *Skill Progress* "in_progress" for "abd-architecture-specification" on *Ticket* **1-inc-1-sprint-a**
When the *Kanban Lead* detects the "engineer" session is stale
Then the *Kanban Lead* stops the stale *Agent Session*
  And the *Kanban Lead* creates a new *Agent Session* for role "engineer"
  And the new *Agent* resumes eligible work on **1-inc-1-sprint-a**

### Scenario 2: Agent session completed but eligible work remains — KanbanLead creates new session

Given a *Team Member* *Agent* with role "business-expert" had an *Agent Session* that completed
  And *Ticket* **1-inc-2-sprint-b** is active at *Stage* "exploration" with eligible *Skill* "abd-domain-terms" for role "business-expert"
When the *Kanban Lead* detects that the "business-expert" session has ended with remaining eligible work
Then the *Kanban Lead* creates a new *Agent Session* for role "business-expert"
  And the new *Agent* claims "abd-domain-terms" on **1-inc-2-sprint-b**

---

## Story: Detect Agent Completion via SDK

**Story type:** system

**Sources / context:** Agent and Skills KA — agent session, skill progress, stage completion

---

## Scenarios

### Scenario 1: Agent completes skill — session emits completion, KanbanLead updates skill progress

Given a *Team Member* *Agent* with role "engineer" is executing *Skill* "abd-architecture-specification" on *Ticket* **1-inc-1-sprint-a**
  And the *Agent Session* is in "running" state
When the *Agent* finishes executing "abd-architecture-specification"
  And the *Agent Session* emits a completion signal
Then the *Kanban Lead* updates *Skill Progress* for "abd-architecture-specification" to *Execution Status* "done"
  And the *Kanban Lead* checks whether the *Agent* has additional eligible *Skills* on the ticket

### Scenario 2: Agent completes all skills on ticket — KanbanLead marks ticket stage complete

Given a *Team Member* *Agent* with role "business-expert" is executing the final required *Skill* "abd-story-specification" on *Ticket* **1-inc-1-sprint-a** at *Stage* "specification"
  And all other *Skills* in the *Stage Work Required* have *Execution Status* "done" and *Review Status* "done"
When the *Agent* finishes executing "abd-story-specification"
Then the *Kanban Lead* updates *Skill Progress* for "abd-story-specification" to *Execution Status* "done"
  And the *Kanban Lead* detects that all required *Skills* for *Stage* "specification" are complete
  And *Ticket* **1-inc-1-sprint-a** moves to the "Done" sub-column of "specification"

---

## Story: Stream Agent Messages via SDK

**Story type:** system

**Sources / context:** Agent and Skills KA — agent session, message stream; story-map.md consolidation notes — "Stream Agent Messages via SDK"

---

## Scenarios

### Scenario 1: Running agent emits message — server receives it in real time

Given a *Team Member* *Agent* with role "engineer" has an active *Agent Session*
  And the session is connected via Cursor SDK streaming
When the *Agent* emits a text message "Creating architecture template for caching mechanism"
Then the server receives the message within the SDK stream
  And the message is available to connected clients via the board API
  And the *Agent Session* last activity timestamp is updated

### Scenario 2: Agent emits thinking indicator — server relays to connected clients

Given a *Team Member* *Agent* with role "business-expert" has an active *Agent Session*
  And the session is connected via Cursor SDK streaming
When the *Agent* emits a thinking indicator (model is processing)
Then the server receives the thinking event
  And connected clients are notified of the "thinking" state for "business-expert"
  And the *Agent Pool* avatar for "business-expert" reflects the "working" state

---

## Story: Derive Agent Liveness from SDK Session State

**Story type:** system

**Sources / context:** Agent and Skills KA — agent liveness, agent session; replaces heartbeat-file liveness

---

## Scenarios

### Scenario 1: Session "running" with recent activity — agent is alive

Given a *Team Member* *Agent* with role "engineer" has an active *Agent Session* in "running" state
  And the last message was emitted 30 seconds ago
When the system derives *Agent Liveness* for "engineer"
Then the "engineer" *Agent* is considered alive
  And the *Agent Pool* avatar displays as "working" if a *Ticket* engages the role, or "idle" otherwise

### Scenario 2: Session "running" but no activity for 120+ seconds — agent is stale

Given a *Team Member* *Agent* with role "engineer" has an active *Agent Session* in "running" state
  And no messages have been emitted for 125 seconds
When the system derives *Agent Liveness* for "engineer"
Then the "engineer" *Agent* is considered stale
  And the *Agent Pool* avatar displays as "inactive"
  And the *Kanban Lead* is eligible to restart the session

### Scenario 3: No session exists for role — pool avatar "idle"

Given no *Agent Session* exists for role "ux-designer"
  And no active *Ticket* engages "ux-designer"
When the system derives *Agent Liveness* for "ux-designer"
Then the "ux-designer" *Agent* is considered idle
  And the *Agent Pool* avatar displays as "idle" (lit)
  But the avatar does not display as "inactive"

---

## Story: Preserve Board Mode on Ticket Move

**Story type:** system

**Sources / context:** Operate Board in Manual Mode — "Persist Board Mode Setting", "Move Ticket to In Progress on Agent Advance"

---

## Scenarios

### Scenario 1: Ticket move in manual mode does not reset board mode

Given the *Kanban Board* persisted *Board Mode* is "manual"
  And the server has a previously loaded in-memory board instance with stale *Board Mode* "automatic"
  And *Ticket* **project-all** is active at *Stage* "shaping"
When the app persists a ticket move for **project-all** to *Stage* "discovery"
Then the persisted board still has *Board Mode* "manual"
  And **project-all** persists at *Stage* "discovery"
  But no write path changes *Board Mode* back to "automatic"

### Scenario 2: Manual drag to done remains in done after refresh

Given the *Kanban Board* is in manual mode
  And *Ticket* **project-all** is active at *Stage* "shaping"
When the user drags **project-all** to "shaping" → "Done"
  And the board refreshes from persisted data
Then **project-all** remains in "shaping" → "Done"
  But it is not reclassified back to "shaping" → "In Progress" due only to incomplete stage skills

---

# Display Agent Output Stream

## Story: Expand Agent Stream by Clicking Team Member Avatar

**Story type:** user

**Sources / context:** Display Agent Output Stream — open agent stream panel; story-map.md consolidation notes — "Display Agent Output Stream"

---

## Scenarios

### Scenario 1: User clicks engineer avatar with active ticket — stream panel opens beside stage column

Given the *Agent Pool* shows an "engineer" avatar in "working" state
  And the "engineer" *Agent* is executing a *Skill* on *Ticket* **1-inc-1-sprint-a** at *Stage* "specification"
When the Delivery Lead clicks the "engineer" avatar
Then a *Stream Panel* opens beside the "specification" *Stage* column
  And the panel displays the live message stream from the "engineer" *Agent Session*
  And the panel height matches the "specification" column height

### Scenario 2: User clicks avatar with no active session — panel shows "No active session"

Given the *Agent Pool* shows a "business-expert" avatar in "idle" state
  And no *Agent Session* exists for "business-expert"
When the Delivery Lead clicks the "business-expert" avatar
Then a *Stream Panel* opens
  And the panel displays "No active session" message
  But no message stream is rendered

---

## Story: Anchor Stream Panel beside Active Ticket Stage Column

**Story type:** system

**Sources / context:** Display Agent Output Stream — panel anchoring by ticket stage

---

## Scenarios

### Scenario 1: Engineer working on ticket at "exploration" — panel anchored to right of exploration column

Given the "engineer" *Agent* is executing a *Skill* on *Ticket* **1-inc-2-sprint-b** at *Stage* "exploration"
  And a *Stream Panel* is open for "engineer"
When the board renders
Then the *Stream Panel* is anchored to the right edge of the "exploration" *Stage* column
  And the panel scrolls horizontally with the board

### Scenario 2: Agent moves ticket from "exploration" to "specification" — panel follows

Given the "engineer" *Agent* completed all *Skills* at *Stage* "exploration" on *Ticket* **1-inc-2-sprint-b**
  And *Ticket* **1-inc-2-sprint-b** advances to *Stage* "specification"
  And a *Stream Panel* is open for "engineer"
When the *Agent* begins executing a *Skill* at *Stage* "specification"
Then the *Stream Panel* repositions beside the "specification" *Stage* column
  And the panel content continues to stream without interruption

---

## Story: Open Second Agent Stream While First Is Open

**Story type:** user

**Sources / context:** Display Agent Output Stream — view multiple agent streams

---

## Scenarios

### Scenario 1: Business-expert panel open, user clicks engineer — both panels visible

Given a *Stream Panel* is open for "business-expert" anchored beside the "discovery" *Stage* column
  And the "engineer" *Agent* is executing a *Skill* at *Stage* "specification"
When the Delivery Lead clicks the "engineer" avatar
Then a second *Stream Panel* opens beside the "specification" *Stage* column
  And both the "business-expert" and "engineer" panels are visible side by side
  And each panel streams its respective *Agent Session* independently

### Scenario 2: Three panels open — all three stack horizontally

Given *Stream Panels* are open for "business-expert" and "engineer"
  And the "product-owner" *Agent* is executing a *Skill* at *Stage* "exploration"
When the Delivery Lead clicks the "product-owner" avatar
Then a third *Stream Panel* opens beside the "exploration" *Stage* column
  And all three panels are visible and stacked horizontally across the board
  And each panel is independently scrollable

---

## Story: Stream Agent Messages to Panel Like IDE Chat

**Story type:** system

**Sources / context:** Display Agent Output Stream — real-time agent output rendering

---

## Scenarios

### Scenario 1: Agent sends text response — appears as message bubble in panel

Given a *Stream Panel* is open for the "engineer" *Agent*
  And the *Agent Session* is in "running" state
When the *Agent* emits a text message "Generating acceptance tests for operator signon"
Then the message appears as a chat bubble in the *Stream Panel*
  And the bubble is styled as an agent response (not a user message)
  And the panel auto-scrolls to show the latest message

### Scenario 2: Agent is thinking — thinking indicator animates in panel

Given a *Stream Panel* is open for the "business-expert" *Agent*
  And the *Agent Session* is in "running" state
When the *Agent* enters a thinking state (model is processing)
Then a thinking indicator animates at the bottom of the *Stream Panel*
  And the indicator disappears when the *Agent* emits the next text message

### Scenario 3: Agent completes skill — completion status shown in panel

Given a *Stream Panel* is open for the "engineer" *Agent*
  And the *Agent* is executing *Skill* "abd-story-acceptance-test" on *Ticket* **1-inc-1-sprint-a**
When the *Agent* completes "abd-story-acceptance-test"
Then the *Stream Panel* displays a completion status indicator
  And the status shows "abd-story-acceptance-test — complete"
  And the panel remains open for subsequent *Skill* output or manual close

---
