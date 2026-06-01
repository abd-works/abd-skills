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

# Board Flow Logic (Kanban Lead, Agent, and Skill Orchestration)

## Story: Pull Backlog Tickets to Active per Stage WIP

**Story type:** system

**Sources / context:** Kanban Board KA — kanban board, ticket, stage; Agent and Skills KA — kanban lead

---

## Scenarios

### Scenario 1: Kanban Lead pulls partition tickets up to WIP limit

Given a *Kanban Board* "bess28-mern-spec" with *Stage* "discovery" at *Scope Level* "partition"
  And the *Kanban Board* has *partition_wip_limit* 1
  And the backlog contains *Ticket* **1-external-protocol-integration** at *Stage* "discovery" with *Scope Level* "partition" and *Priority* 1
  And the backlog contains *Ticket* **2-dual-persistence** at *Stage* "discovery" with *Scope Level* "partition" and *Priority* 2
  And no *Tickets* are active at *Stage* "discovery"
When the *Kanban Lead* runs a pull cycle
Then *Ticket* **1-external-protocol-integration** moves from backlog to active at *Stage* "discovery"
  And *Ticket* **2-dual-persistence** remains in the backlog
  And the *Kanban Board* records a "ticket_pulled" event in the metrics log

### Scenario 2: Kanban Lead does not pull when WIP is full

Given a *Kanban Board* "bess28-mern-spec" with *Stage* "discovery" at *Scope Level* "partition"
  And the *Kanban Board* has *partition_wip_limit* 1
  And *Ticket* **1-external-protocol-integration** is active at *Stage* "discovery"
  And the backlog contains *Ticket* **2-dual-persistence** at *Stage* "discovery" with *Scope Level* "partition" and *Priority* 2
When the *Kanban Lead* runs a pull cycle
Then no *Tickets* move from backlog to active for *Stage* "discovery"
  And *Ticket* **2-dual-persistence** remains in the backlog

### Scenario 3: Kanban Lead pulls for each stage independently

Given a *Kanban Board* "bess28-mern-spec" with *Stages*:
  | stage_name    | scope_level |
  | discovery     | partition   |
  | exploration   | increment   |
  And the backlog contains *Ticket* **3-batch-eod** at *Stage* "discovery" with *Scope Level* "partition"
  And the backlog contains *Ticket* **1-inc-1-operator-signon** at *Stage* "exploration" with *Scope Level* "increment"
  And both stages have available WIP capacity
When the *Kanban Lead* runs a pull cycle
Then *Ticket* **3-batch-eod** moves to active at *Stage* "discovery"
  And *Ticket* **1-inc-1-operator-signon** moves to active at *Stage* "exploration"

### Scenario 4: WIP limit derived from Team capacity when not explicit

Given a *Kanban Board* "bess28-mern-spec" with *Stage* "exploration" at *Scope Level* "increment"
  And the *Stage Work Required* first required *Skill* is "abd-ubiquitous-language" with *Agent* role "business-expert"
  And the *Team* has 3 executors for "business-expert"
  And no explicit *increment_wip_limit* is set on the board
When the *Kanban Lead* calculates the WIP limit for "exploration"
Then the WIP limit is 3 — derived from the *Team* capacity for "business-expert"

### Scenario 5: Rolling pull when first skill is done on active tickets

Given a *Kanban Board* with *Stage* "exploration" at *Scope Level* "increment" and WIP limit 3
  And 2 active *Tickets* at *Stage* "exploration" have *Skill Progress* for "abd-ubiquitous-language" with *Execution Status* "done" and *Review Status* "done"
  And the backlog contains *Ticket* **1-inc-3-payment-processing** at *Stage* "exploration"
When the *Kanban Lead* runs a pull cycle
Then *Ticket* **1-inc-3-payment-processing** moves from backlog to active at *Stage* "exploration"
  Because the 2 active *Tickets* with their first *Skill* done do not count against the WIP limit for new work

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
  | abd-ubiquitous-language      | business-expert | false    |
  | abd-acceptance-criteria      | product-owner   | false    |
  | abd-ux-mockup                | ux-designer     | true     |
  | abd-architecture-reference   | engineer        | false    |
  And *Skill Progress* for "abd-ubiquitous-language", "abd-acceptance-criteria", and "abd-architecture-reference" all have *Execution Status* "done" and *Review Status* "done"
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
  | abd-class-responsibility-collaborator     | business-expert  |
  | abd-specification-by-example              | product-owner    |
  | abd-architecture-template                 | engineer         |
  | abd-acceptance-test-driven-development    | engineer         |
  And no *Skill Progress* entries exist yet
When an *Agent* with role "business-expert" looks for eligible work
Then the *Agent* claims "abd-class-responsibility-collaborator" on **1-inc-1-sprint-a**
  Because it is the first required *Skill* matching the *Agent's* role

### Scenario 2: Agent skips skills that require prior skills incomplete

Given *Ticket* **1-inc-1-sprint-a** is active at *Stage* "specification"
  And "abd-class-responsibility-collaborator" *Skill Progress* has *Execution Status* "not started"
  And "abd-specification-by-example" is second in the rail and requires "abd-class-responsibility-collaborator" done first
When an *Agent* with role "product-owner" looks for eligible work
Then no *Skill* is available for the "product-owner" *Agent*
  Because the prior *Skill* "abd-class-responsibility-collaborator" is not done

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
  And *Skill Progress* for "abd-class-responsibility-collaborator" has *Execution Status* "in_progress" with *Agent* "business-expert"
When a second *Agent* with role "business-expert" looks for eligible work
Then "abd-class-responsibility-collaborator" on **1-inc-1-sprint-a** is not claimable
  Because a *Skill* with *Execution Status* "in_progress" cannot be claimed by another *Agent*

### Scenario 5: Agent claims review after execution done

Given *Ticket* **1-inc-1-sprint-a** is active at *Stage* "specification"
  And *Skill Progress* for "abd-class-responsibility-collaborator" has *Execution Status* "done" and *Review Status* "not started"
When an *Agent* with role "business-expert" looks for eligible review work
Then the *Agent* can claim review of "abd-class-responsibility-collaborator" on **1-inc-1-sprint-a**
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
  And "abd-architecture-reference" is in the *Stage Work Required*
When an *Agent* with role "engineer" claims "abd-architecture-reference"
Then the *Agent* creates the mechanism registry and runs architecture reference
  And *Skill Progress* for "abd-architecture-reference" records *Execution Status* "done"

### Scenario 2: Architecture reference quick pass on subsequent increments

Given *Ticket* **1-inc-2-message-routing** is active at *Stage* "exploration"
  And an architecture mechanism registry already exists from **1-inc-1-operator-signon**
  And all mechanisms in **1-inc-2-message-routing** are already covered by the registry
When an *Agent* with role "engineer" claims "abd-architecture-reference"
Then the *Agent* runs a quick pass and writes `architecture-reference-assignment.md` with assign-only rows
  And *Skill Progress* for "abd-architecture-reference" records *Execution Status* "done" and *Review Status* "done"
  And the *Agent* proceeds to the next eligible *Skill*

### Scenario 3: Architecture template creates for new mechanism only

Given *Ticket* **1-inc-2-sprint-b** is active at *Stage* "specification"
  And the mechanism registry shows "error-handling" already has a template
  And **1-inc-2-sprint-b** introduces a new mechanism "caching"
When an *Agent* with role "engineer" claims "abd-architecture-template"
Then the *Agent* creates a template only for "caching"
  And "error-handling" is not re-created

---
