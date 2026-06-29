# Cross-Layer Domain Alignment — Invocation Order

Each row reads left-to-right in call order. Six layers:

**domain specification → Shared → Client (JS) → Page (app-client) → Route / Controller → Server**

---

## Template Rules

### Class names

```
domain specification:   {ClassName}
Shared:         {ClassName}
Server:         {ClassName}  extends  shared/{ClassName}
Client (JS):    {ClassName}  extends  shared/{ClassName}
Page:           {ClassName}View
Controller:     {ClassName}Controller
Route:          {ClassName}Routes
```

Examples: `KanbanBoard` → `KanbanBoard` → `KanbanBoard` → `KanbanBoardView` → `KanbanBoardController`

---

### Property names

```
domain specification:   {propertyName}: {Type}
Shared:         {propertyName}: {type}          (camelCase, same word)
Raw JSON:       {property_name}                 (snake_case)
Route body:     req.body.{property_name}        (snake_case)
```

Examples:

| domain specification         | Shared                 | Raw JSON           | Route body            |
|---|---|---|---|
| `scopeLevel: String` | `scopeLevel: string`   | `scope_level`      | —                     |
| `boardMode`          | `boardMode: BoardMode` | `board_mode`       | `req.body.board_mode` |
| `executionStatus`    | `executionStatus`      | `execution_status` | —                     |


---

### Method names

```
domain specification:   {verbNoun}({domainArg}: {DomainType})
Shared:         {verbNoun}({domainArg}: {domainType})        same names, TypeScript types
Client (JS):    static async {verbNoun}({domainArg}: {type}) domain types → HTTP body
Route:          POST /api/board/{resource}/{verb-noun}  body: { {arg_name}: {value} }  (snake_case)
Controller:     async {verbNoun}(body: {VerbNoun}Body)        body typed, extracts args by name
Server:         async {verbNoun}AndPersist({domainArg}: {type}) same arg names as Shared
```

Args transform across layers — domain objects narrow to their identity as they cross the wire:

| domain specification arg      | Shared arg           | Route body field | Controller extract | Server arg           | Why it narrows                                                             |
|---|---|---|---|---|---|
| `nextStage: Stage`    | `nextStage: StageId` | `next_stage`     | `body.next_stage`  | `nextStage: StageId` | Stage object narrows to its string ID; name stays the same |
| `delta: Integer`      | `delta: number`      | `delta`          | `body.delta`       | `delta: number`      | Primitive; passes unchanged |
| `skill: Skill`        | `skill: string`      | `skill`          | `body.skill`       | `skill: string`      | Skill identity is its name string |


Examples:


| domain specification                      | Client (JS)                                      | Route                    | Controller              | Server                                  |
|---|---|---|---|---|
| `toggleMode()`                    | `KanbanBoard.toggleMode()`                       | `POST .../mode`          | `toggleMode(body)`      | `toggleModeAndPersist()`                |
| `moveToStage(ticket, stage)`      | `Ticket.moveToStage(id, stage, placement)`       | `POST .../move-to-stage` | `moveToStage(body)`     | `moveToStageAndPersist(id, stage)`      |
| `updatePairCount(role, delta)`    | `TeamMembership.updatePairCount(role, delta)`    | `POST .../team`          | `updatePairCount(body)` | `updatePairCountAndPersist(role, delta)`|


---

### Layer responsibilities

```
Shared:         domain logic only — no I/O, no HTTP, no React
Server:         extends Shared — adds async file I/O and persist()
Client (JS):    extends Shared — adds static HTTP helpers and hooks
Page:           React only — receives snapshot props, calls Client methods on user action
Controller:     validates req body → calls Server method → returns KanbanBoardSnapshot
Route:          parses req → calls Controller or Server → res.json(snapshot)
```

---

### Every mutating route returns the same shape

```
POST /api/board/**  →  KanbanBoardSnapshot
```

---

## Drift and Violations

Where the current implementation has strayed from the domain specification or the template rules above.


| Class               | Property / Method                                     | Layer           | Violation                                                                                                                                                                              |
| ------------------- | ----------------------------------------------------- | --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `KanbanBoard`       | `workspacePath` / `planningRoot`                      | Client → Server | Board-selection state belongs on the server — user picks a board once and the server remembers it. Instead, every client method re-passes the board file path as `planningRoot` on every call. Infrastructure concern leaking into every method signature. Fix: server stores the active board; client methods take domain args only |
| `KanbanBoard`       | `savedAt`                                             | Shared          | Renamed to `syncedAt` — domain specification says `savedAt` |
| `KanbanBoard`       | `advanceCompletedTickets()`                           | All             | Method lives on `KanbanBoard` in the model; in code the caller (controller/route) triggers it by calling `moveToStageAndPersist` — no explicit `advanceCompletedTickets` method exists |
| `KanbanBoard`       | `moveToStage()` controller                            | Controller      | Controller method is `moveTicket()` — should be `moveToStage(body)` to match the template |
| `KanbanBoard`       | `staleAgents()`                                       | Server/Shared   | Fully absent from TypeScript — delegated entirely to Python CLI `lead tick`; no TS representation                                                                                      |
| `KanbanBoard`       | `defineStageOrder()`                                  | All             | Not a method — stage order is a static constant `Stage.ORDER`; no runtime call                                                                                                         |
| `Ticket`            | `id`                                                  | Shared → Raw    | **Name drift** — three names: `id` (model) → `ticketId` (shared TS) → `ticket_id` (JSON). The name should stay `id` / `ticket_id`; adding the `ticket` prefix in TS is redundant |
| `Ticket`            | `boardPosition: Stage`                                | Shared          | **Name drift** — `Stage` object narrowing to `StageId` string is expected; renaming `boardPosition` to `stage` is drift |
| `Ticket`            | `waitInStageDone(stage)` — `placement` arg            | Shared          | **Name drift** — `SubState` renamed to `MoveTicketPlacement`; values `IN_PROGRESS`/`DONE` renamed to `'in_progress'`/`'stage_done'` |
| `Stage`             | `enqueue()` / `moveToInProgress()` / `moveToDone()`   | Shared          | No `Stage` class with mutable buckets — replaced by `StageBucketLayout.build()` which computes buckets from snapshot data                                                              |
| `SkillProgress`     | `startReview()` / `completeReview()` / `failReview()` | All             | Absent from TypeScript entirely — only Python CLI writes these transitions                                                                                                             |
| `SkillProgress`     | `executionStatus`                                     | Shared → Raw    | Three names: `executionStatus` (model/shared TS) → `execution_status` (JSON)                                                                                                           |
| `SkillProgress`     | `reviewStatus`                                        | Shared          | Exists only in schema (raw JSON) — not surfaced as a typed property on the shared `SkillProgress` class                                                                                |
| `Team`              | —                                                     | Shared          | `Team` is not a class in shared — it is a plain `Record<AgentRole, number>` type alias                                                                                                 |
| `Team`              | `incrementPairCount()` / `decrementPairCount()`       | Client          | Client uses `Heartbeat.adjustTeam(root, role, +1/-1)` — verb `adjust` instead of `updatePairCount`; class is `Heartbeat` instead of `TeamMembership` |
| `TeamMemberPair`    | `executor`, `reviewer`                                | All             | Not materialized as a class at any layer — pair concept collapsed to a slot count integer                                                                                              |
| `TeamMembership`    | `unstaffedPairs()`                                    | Server/TS       | Not implemented in TypeScript — detected by Python CLI `lead tick` only                                                                                                                |
| `KanbanLead`        | `Agent` base class                                    | Server          | `KanbanLead` and `TeamMember` are independent classes in TS — no shared `Agent` base class                                                                                             |
| `KanbanLead`        | `writeHeartbeat()`                                    | All             | Removed entirely — replaced by SDK session liveness (`AgentSession.status`)                                                                                                            |
| `KanbanLead`        | `runScanCycle()`                                      | Server          | Not a TS method — implemented as a Python CLI call via `execFileAsync` in the route                                                                                                    |
| `KanbanLead`        | `deliveryRole`                                        | Server          | domain specification property — actual server class exposes `workspace` instead; role is implicit                                                                                              |
| `AgentDefinition`   | `rootFilePath`                                        | Server          | Renamed to `path`                                                                                                                                                                      |
| `AgentDefinition`   | `sharedWorkflowFiles`                                 | Server          | Accessible only via `resolveEligibleSkills().referencedFiles` — not a direct property                                                                                                  |
| `BootstrapPrompt`   | `roleIdentity`                                        | Shared          | Renamed to `role`                                                                                                                                                                      |
| `BootstrapPrompt`   | `promptContent`                                       | Shared          | Renamed to `agentDefinition` (holds the file path, not assembled content)                                                                                                              |
| `AgentOutputStream` | `messages: List<String>`                              | Server          | `AgentOutputStream` holds a single event, not a message list — accumulation happens in the SSE client hook                                                                             |
| `Heartbeat`         | —                                                     | All             | Not a domain entity in TS — split across `Heartbeat` (client display helpers) and `KanbanLead.getPoolAvatarState()` (server state)                                                     |
| `BoardPosition`     | —                                                     | All             | Not materialized as a class — computed inline from `stage` + `holdInProgress` + `completedStage` flags on `Ticket`                                                                     |


---

### planningRoot threading (design debt)

The user selects a board on the website; the server should own and remember that selection. Instead, every client method re-passes the board's file path as `planningRoot` on every call — an infrastructure concern leaking into every method signature.

**What should happen:** User selects a board → server stores the active board → all subsequent calls act on it with no path arg.

**What currently happens:**

| Layer | Workaround |
|---|---|
| Client (JS) | Takes `planningRoot` as first arg and puts it in every request body |
| Route | Reads `req.body.planningRoot` or `req.query.planningRoot` |
| Controller | Passes it to `board.setPlanningRoot()` before calling any method |
| Server | Accepts `planningRoot?` as last arg; falls back to `cachedRoot` if omitted |
| Shared | `KanbanBoard.resolvePlanningPaths(planningRoot)` derives all file paths from the root |

New routes must follow the current pattern only because the server infrastructure requires it — not because it is correct.

---

## Class Mappings

Each class from the domain specification traced through all six layers.

---

## KanbanBoard


| domain specification                          | Shared                                                     | Client (JS)                                      | Page (app-client)                        | Route/Controller                          | Server                                          |
| ------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------ | ---------------------------------------- | ----------------------------------------- | ----------------------------------------------- |
| **KanbanBoard**                       | **KanbanBoard**                                            | **KanbanBoard**                                  | **KanbanBoardView**                      | **KanbanBoardController**                 | **KanbanBoard**                                 |
| `stages: List<Stage>`                 | `Stage.ORDER: StageId[]`                                   | —                                                | `visibleStages`                          | —                                         | —                                               |
| `workspacePath: String`               | `resolvePlanningPaths(root)`                               | `resolvePlanningRoot()`                          | `snapshot.planningRoot`                  | `req.body.planningRoot`                   | `cachedRoot`                                    |
| `team: Team`                          | `get team(): Team`                                         | `snapshot.team`                                  | `<TeamView team={snapshot.team}/>`       | —                                         | `this.data.team`                                |
| `savedAt: String`                     | `get syncedAt(): string`                                   | `snapshot.syncedAt`                              | —                                        | —                                         | `this.data.synced_at`                           |
| `boardMode`                           | `get boardMode(): BoardMode`                               | `snapshot.board_mode`                            | `boardMode` state + toggle buttons       | —                                         | `this.data.board_mode`                          |
| `ticketsInFlow()`                     | `columnViews(): KanbanColumnView[]`                        | `KanbanBoard.fromSnapshot(json)`                 | `snapshot.columnViews` → stage buckets   | `GET /api/board` → `getSnapshot()`        | `loadSnapshot()`                                |
| `stageFor(ticket)`                    | `findRawTicket(id).stage`                                  | —                                                | —                                        | —                                         | `findRawTicket(id)`                             |
| `advanceCompletedTickets()`           | `moveToStage(id, target, config, def, opts)`               | `Ticket.moveToStage(root, id, stage, placement)` | `handleMoveTicket(id, stage, placement)` | `POST .../move-to-stage` → `moveTicket()` | `moveToStageAndPersist()`                       |
| `advanceCompletedTickets()` (scatter) | `scatterAndAdvance(parent, target, children, config, def)` | (same — server resolves)                         | (same handler)                           | (same route)                              | `moveToStageAndPersist()` → `scatterAndAdvance` |
| `defineStageOrder()`                  | `Stage.ORDER` (static)                                     | —                                                | —                                        | —                                         | —                                               |
| `staleAgents()`                       | —                                                          | —                                                | —                                        | —                                         | Python CLI `lead tick`                          |


---

## Ticket


| domain specification                     | Shared                            | Client (JS)                                      | Page (app-client)                        | Route/Controller                          | Server                                   |
| -------------------------------- | --------------------------------- | ------------------------------------------------ | ---------------------------------------- | ----------------------------------------- | ---------------------------------------- |
| **Ticket**                       | **Ticket**                        | **Ticket**                                       | **TicketView**                           | —                                         | **Ticket** (scatter)                     |
| `id: String`                     | `ticketId: string`                | `ticket.ticketId`                                | `data-ticket={ticket.ticketId}`          | `req.body.ticket_id`                      | `ticket.ticket_id`                       |
| `lineage: List<String>`          | `lineage: string[]`               | `ticket.lineage`                                 | `title={ticket.lineage.join(' > ')}`     | —                                         | raw `.lineage`                           |
| `boardPosition: Stage`           | `stage: StageId`                  | `ticket.stage`                                   | bucket placement via `StageBucketLayout` | `req.body.target_stage`                   | raw `.stage`                             |
| `scopeLevel: String`             | `scopeLevel: string`              | `ticket.scopeLevel`                              | `data-scope={ticket.scopeLevel}`         | —                                         | raw `.scope_level`                       |
| `priority: Integer`              | `priority: number`                | `ticket.priority`                                | sort order in bucket                     | —                                         | raw `.priority`                          |
| `skillProgress: Dict`            | `skillProgress: SkillProgressMap` | `.doneSkillIds`, `.executingSkillIds`            | skill rows in expanded view              | —                                         | raw `.skill_progress`                    |
| `notes: String`                  | `notes: string`                   | `ticket.notes`                                   | —                                        | —                                         | raw `.notes`                             |
| `stageTimestamps: Dict`          | `enteredStage`, `completedStage`  | —                                                | —                                        | —                                         | raw `.entered_stage`, `.stage_history[]` |
| `advanceToNextStage(next, team)` | `moveToStage()` on KanbanBoard    | `Ticket.moveToStage(root, id, stage, placement)` | `handleMoveTicket()`                     | `POST .../move-to-stage` → `moveTicket()` | `moveToStageAndPersist()`                |
| `waitInStageDone(stage)`         | placement=`stage_done`            | `Ticket.moveToStage(…, 'stage_done')`            | `commitTicketDrop(…, 'stage_done')`      | same route                                | `moveToStageAndPersist(…, 'stage_done')` |
| `scatterIntoChildTickets(next)`  | `scatterAndAdvance(…)`            | (server resolves)                                | (same handler)                           | same route                                | `Ticket.tryResolveScatterChildren()`     |
| `skillsDoneFor(workReq)`         | `isStageSkillsComplete(ids)`      | `ticket.isStageSkillsComplete(ids)`              | bucket done vs ip decision               | —                                         | —                                        |
| `isBlocked()`                    | `notes.includes('blocked')`       | `ticket.statusCssClass()`                        | CSS class `kb-ticket--blocked`           | —                                         | —                                        |


---

## Stage


| domain specification                      | Shared                               | Client (JS)                  | Page (app-client)                                      | Route/Controller        | Server                    |
| --------------------------------- | ------------------------------------ | ---------------------------- | ------------------------------------------------------ | ----------------------- | ------------------------- |
| **Stage**                         | **Stage**                            | — (uses shared)              | **StageGroupView**                                     | —                       | — (uses shared)           |
| `name: String`                    | `StageId` type                       | `stage` prop                 | `Stage.LABELS[stage]` in header                        | `req.body.target_stage` | `Stage.ORDER[i]`          |
| `scopeLevel: String`              | `StageDefinition.scope`              | —                            | —                                                      | —                       | config `.stages[].scope`  |
| `workRequired: StageWorkRequired` | `StageSkillRail { stage, skills[] }` | `snapshot.stageSkillRails`   | skill chips: `skills.map(s => <span>{s.label}</span>)` | —                       | `buildSkillRails(config)` |
| `queue: List<Ticket>`             | `StageBucket.feedsNext`              | `bucket.feedsNext`           | `<StageDoneView feedsNextTickets={…}/>`                | —                       | —                         |
| `inProgress: List<Ticket>`        | `StageBucket.ip`                     | `bucket.ip`                  | `<StageInProgressView tickets={…}/>`                   | —                       | —                         |
| `done: List<Ticket>`              | `StageBucket.done`                   | `bucket.done`                | `<StageDoneView doneTickets={…}/>`                     | —                       | —                         |
| `enqueue(ticket)`                 | `StageBucketLayout.build()`          | `StageBucketLayout.build(…)` | layout derivation in `useMemo`                         | —                       | —                         |
| `moveToInProgress(ticket)`        | bucket.ip in build                   | same                         | same                                                   | —                       | —                         |
| `moveToDone(ticket)`              | bucket.done in build                 | same                         | same                                                   | —                       | —                         |
| `allTickets()`                    | `get(stage): StageBucket`            | `stageBuckets.get(stage)`    | `bucket` prop on `StageGroupView`                      | —                       | —                         |


---

## SkillProgress


| domain specification            | Shared                                   | Client (JS)                                     | Page (app-client)                      | Route/Controller                                 | Server                               |
| ----------------------- | ---------------------------------------- | ----------------------------------------------- | -------------------------------------- | ------------------------------------------------ | ------------------------------------ |
| **SkillProgress**       | **SkillProgress**                        | — (queries via Ticket)                          | **TicketView** (expanded rows)         | —                                                | raw `.skill_progress[skill]`         |
| `skillName: String`     | `skillName: string`                      | `ticket.activeSkillId`                          | `stageSkills.map(s => …)`              | `req.body.skill`                                 | raw key                              |
| `executionStatus`       | `SkillExecutionStatus`                   | `.executingSkillIds`, `.doneSkillIds`           | `skillRowDisplayState(id, focus)`      | —                                                | raw `.execution_status`              |
| `reviewStatus`          | (schema)                                 | `.reviewingSkillIds`, `.awaitingReviewSkillIds` | `row.isUnderReview`, `row.showMagnify` | —                                                | raw `.review_status`                 |
| `executingAgentRole`    | (schema: `agent`)                        | `ticket.activeAgent`                            | live skill icon coloring               | `req.body.agent_role`                            | raw `.agent`                         |
| `reviewingAgentRole`    | (schema: `reviewer`)                     | `ticket.reviewAgent`                            | review icon                            | —                                                | raw `.reviewer`                      |
| `startExecution(agent)` | `SkillProgress.create(…, 'in_progress')` | `Ticket.postActionIntent(…)`                    | `commitDrop(e)` → postActionIntent     | `POST .../action-intent` → `writeActionIntent()` | `board.writeActionIntent(intent)`    |
| `completeExecution()`   | `markDone()`                             | —                                               | —                                      | —                                                | `KanbanLead.handleSkillCompletion()` |
| `startReview(agent)`    | —                                        | —                                               | —                                      | —                                                | Python CLI                           |
| `completeReview()`      | —                                        | —                                               | —                                      | —                                                | Python CLI                           |
| `failReview()`          | —                                        | —                                               | —                                      | —                                                | Python CLI                           |
| `isDone()`              | `isComplete()`                           | `ticket.doneSkillIds.includes(id)`              | `row.isDone` → DoneIcon                | —                                                | `exec=done && review=done`           |


---

## Team


| domain specification                                      | Shared                              | Client (JS)                            | Page (app-client)                               | Route/Controller                        | Server                           |
| ------------------------------------------------- | ----------------------------------- | -------------------------------------- | ----------------------------------------------- | --------------------------------------- | -------------------------------- |
| **Team**                                          | `Record<AgentRole, number>` (type)  | —                                      | **TeamView**                                    | —                                       | —                                |
| `memberships: Dict<DeliveryRole, TeamMembership>` | `counts: Record<AgentRole, number>` | `snapshot.team`                        | `AGENT_ROLES.map(role => <TeamRoleView …/>)`    | —                                       | `data.team`                      |
| `incrementPairCount(role)`                        | —                                   | `Heartbeat.adjustTeam(root, role, +1)` | `<button onClick={() => adjust(1)}>+</button>`  | `POST /api/board/team` → `updateTeam()` | `updateTeamAndPersist(role, +1)` |
| `decrementPairCount(role)`                        | —                                   | `Heartbeat.adjustTeam(root, role, -1)` | `<button onClick={() => adjust(-1)}>−</button>` | `POST /api/board/team` → `updateTeam()` | `updateTeamAndPersist(role, -1)` |


---

## TeamMembership


| domain specification                  | Shared                                     | Client (JS)  | Page (app-client)                        | Route/Controller | Server                 |
| ----------------------------- | ------------------------------------------ | ------------ | ---------------------------------------- | ---------------- | ---------------------- |
| **TeamMembership**            | **TeamMembership**                         | —            | **TeamRoleView**                         | —                | **TeamMembership**     |
| `role: DeliveryRole`          | `AgentRole` key                            | —            | `role` prop                              | `req.body.role`  | `.role`                |
| `pairCount: Integer`          | `count(role): number`                      | `team[role]` | `total={pairCount}` + avatar slots       | `req.body.delta` | config `.team[role]`   |
| `pairs: List<TeamMemberPair>` | (not materialized — count only)            | —            | slot array `Array.from({length: slots})` | —                | —                      |
| `incrementPairCount()`        | `incrementPairCount(role): TeamMembership` | —            | —                                        | —                | `adjust(role, +1)`     |
| `decrementPairCount()`        | `decrementPairCount(role): TeamMembership` | —            | —                                        | —                | `adjust(role, -1)`     |
| `unstaffedPairs()`            | —                                          | —            | `spawnNeeded` badge                      | —                | Python CLI `lead tick` |


---

## KanbanLead


| domain specification                           | Shared                                                 | Client (JS)                  | Page (app-client)                        | Route/Controller                    | Server                                   |
| -------------------------------------- | ------------------------------------------------------ | ---------------------------- | ---------------------------------------- | ----------------------------------- | ---------------------------------------- |
| **KanbanLead : Agent**                 | —                                                      | — (via Heartbeat)            | **TeamView** (lead avatar)               | **KanbanBoardController**           | **KanbanLead**                           |
| `deliveryRole`                         | —                                                      | `'kanban-lead'`              | `<TeamMemberView role="kanban-lead" …/>` | —                                   | `KanbanLead.workspace`                   |
| `startTeamMemberAgent(pair, workRole)` | `BootstrapPrompt` interface                            | —                            | —                                        | `POST .../agent/start`              | `SdkSessionRegistry.start(role, root)`   |
| `stopTeamMemberAgent(session)`         | —                                                      | —                            | —                                        | `POST .../agent/stop`               | `SdkSessionRegistry.stop(role)`          |
| `restartStaleAgent(member)`            | —                                                      | —                            | —                                        | —                                   | `detectStaleAndRestart(staleSession)`    |
| `runScanCycle(board)`                  | —                                                      | `Heartbeat.leadScan(root)`   | `wakeLeadScan()` onClick                 | `POST .../lead-scan` → `leadScan()` | Python CLI `lead tick`                   |
| `monitorHeartbeats(agents)`            | —                                                      | `snapshot.agentSessions`     | avatar states in `TeamRoleView`          | `GET /api/board` (sessions)         | `SdkSessionRegistry.statusMap()`         |
| `dispatchSkillToIdleTeamMember(…)`     | —                                                      | `Ticket.postActionIntent(…)` | `commitDrop(e)` in TicketView            | `POST .../action-intent`            | `board.writeActionIntent()`              |
| `createAgentSession(prompt)`           | `BootstrapPrompt { workspace, role, agentDefinition }` | —                            | —                                        | `POST .../agent/start`              | `KanbanLead.createAgentSession(def, ws)` |


---

## TeamMember


| domain specification                        | Shared                    | Client (JS)                            | Page (app-client)                         | Route/Controller         | Server                                    |
| ----------------------------------- | ------------------------- | -------------------------------------- | ----------------------------------------- | ------------------------ | ----------------------------------------- |
| **TeamMember : Agent**              | `AgentRole` type          | —                                      | **TeamMemberView**                        | —                        | **TeamMember**                            |
| `deliveryRole`                      | `AgentRole`               | —                                      | `role` prop + `Heartbeat.roleLabel(role)` | `req.body.role`          | `TeamMember.role`                         |
| `workRole`                          | —                         | —                                      | —                                         | —                        | `TeamMember.slotType`                     |
| `agentDefinition`                   | —                         | —                                      | —                                         | —                        | `TeamMember.definition`                   |
| `advanceTicketToInProgress(ticket)` | placement `'in_progress'` | `Ticket.moveToStage(…, 'in_progress')` | `handleMoveTicket()`                      | `POST .../move-to-stage` | `moveToStageAndPersist(…, 'in_progress')` |
| `persistSkillCompletion(board, sp)` | —                         | —                                      | —                                         | —                        | `KanbanLead.handleSkillCompletion()`      |
| `completeTicket(ticket, stage)`     | placement `'stage_done'`  | `Ticket.moveToStage(…, 'stage_done')`  | `commitTicketDrop(…, 'stage_done')`       | same route               | `moveToStageAndPersist(…, 'stage_done')`  |


---

## AgentSession


| domain specification        | Shared | Client (JS)                          | Page (app-client)               | Route/Controller                   | Server                     |
| ------------------- | ------ | ------------------------------------ | ------------------------------- | ---------------------------------- | -------------------------- |
| **AgentSession**    | —      | `useAgentStream(role)`               | **AgentStreamPanel**            | —                                  | **AgentSession**           |
| `sessionId: String` | —      | —                                    | —                               | —                                  | Map key                    |
| `agentRole: String` | —      | —                                    | `role` prop                     | `req.params.role`                  | `AgentSession.role`        |
| `lifecycleState`    | —      | `snapshot.agentSessions[role].state` | status banner (complete/failed) | —                                  | `AgentSession.status`      |
| `outputStream`      | —      | `useAgentStream(role)` → messages    | message bubbles + thinking dots | `GET .../agent/:role/stream` (SSE) | `AgentSession.emit(event)` |
| `isRunning()`       | —      | `session.state === 'running'`        | —                               | `GET .../agent/:role/status`       | `.status === 'running'`    |


---

## AgentDefinition


| domain specification           | Shared | Client (JS) | Page (app-client) | Route/Controller | Server                                     |
| ---------------------- | ------ | ----------- | ----------------- | ---------------- | ------------------------------------------ |
| **AgentDefinition**    | —      | —           | —                 | —                | **AgentDefinition**                        |
| `role: String`         | —      | —           | —                 | —                | `.role`                                    |
| `rootFilePath: String` | —      | —           | —                 | —                | `.path`                                    |
| `sharedWorkflowFiles`  | —      | —           | —                 | —                | `.resolveEligibleSkills().referencedFiles` |


---

## BootstrapPrompt


| domain specification            | Shared                          | Client (JS) | Page (app-client) | Route/Controller | Server                              |
| ----------------------- | ------------------------------- | ----------- | ----------------- | ---------------- | ----------------------------------- |
| **BootstrapPrompt**     | **BootstrapPrompt** (interface) | —           | —                 | —                | assembled in `createAgentSession()` |
| `workspacePath: String` | `.workspace`                    | —           | —                 | —                | from board config                   |
| `roleIdentity: String`  | `.role`                         | —           | —                 | —                | `definition.role`                   |
| `promptContent: String` | `.agentDefinition`              | —           | —                 | —                | `definition.path`                   |


---

## AgentOutputStream


| domain specification             | Shared | Client (JS)            | Page (app-client)                   | Route/Controller             | Server                         |
| ------------------------ | ------ | ---------------------- | ----------------------------------- | ---------------------------- | ------------------------------ |
| **AgentOutputStream**    | —      | `useAgentStream(role)` | **AgentStreamPanel**                | SSE relay                    | **AgentOutputStream**          |
| `messages: List<String>` | —      | `messages[]`           | `messages.map(msg => <div>…</div>)` | `GET .../agent/:role/stream` | `emit({type:'text', content})` |
| `deliverMessage(msg)`    | —      | auto via SSE           | auto render                         | SSE `data:` frame            | `AgentSession.emit(event)`     |


---

## Heartbeat / RoleEngagement (derived)


| domain specification                          | Shared                                 | Client (JS)                   | Page (app-client)                     | Route/Controller            | Server                           |
| ------------------------------------- | -------------------------------------- | ----------------------------- | ------------------------------------- | --------------------------- | -------------------------------- |
| **Heartbeat** / **RoleEngagement**    | —                                      | **Heartbeat** class           | **TeamMemberView** / **TeamRoleView** | —                           | `getPoolAvatarState()`           |
| `poolAvatarState`                     | —                                      | `'working'|'idle'|'inactive'` | CSS `kb-agent-avatar--{state}`        | —                           | `getPoolAvatarState(role)`       |
| `determineLiveness(agent, ticket)`    | —                                      | `resolveSlotState(…)`         | slot rendering                        | `GET /api/board` (sessions) | `SdkSessionRegistry.statusMap()` |
| `countEngagedTickets(tickets, agent)` | `Ticket.countRoleEngagement(colViews)` | `useMemo(…)`                  | `engagedCount` prop on TeamRoleView   | —                           | —                                |
| `formatAge(seconds)`                  | —                                      | `Heartbeat.formatAge(sec)`    | avatar tooltip                        | —                           | —                                |


---

## SkillCatalog (supporting)


| domain specification              | Shared                        | Client (JS)              | Page (app-client)              | Route/Controller | Server                           |
| ------------------------- | ----------------------------- | ------------------------ | ------------------------------ | ---------------- | -------------------------------- |
| **Skill**                 | **SkillCatalog**              | — (uses shared)          | **StageGroupView**             | —                | — (uses shared)                  |
| `name: String`            | `SkillCatalog.label(id)`      | —                        | `<span>{s.label}</span>` chips | —                | `buildSkillRails()`              |
| `performedByRole: String` | `StageWorkRequiredEntry.role` | `StageSkill.role`        | —                              | —                | config `.stages[].skills[].role` |
| family                    | `SkillCatalog.familyFor(id)`  | `familyCssClass(family)` | CSS class on skill chip        | —                | —                                |


