---
state: domain-language
---

# Module: [Delivery Agent Kanban]

_Concept sketch for the real-time Kanban board that drives an agentic agile delivery pipeline — tickets flow through stages, agents start work on skills for tickets._

Scope: How delivery work is modeled and tracked: the kanban board with its ordered stages and skills, tickets flowing through stages, skill progress determining board position, and agent roles pulling skill work.

**Terms**:
- **Kanban Board**
  - *kanban board* — the blueprint of ordered stages, scope levels, and skills that governs ticket flow — live with tickets flowing through stages
  - *team* — the collection executor/reviewer pairs and their counts per agent role configured on the board
  - *ticket* — a unit of work at the scope level its current stage requires, carrying lineage, priority, and skill progress entries created as work starts
  - *board position* — the stage a ticket currently occupies
  - *skill progress* — the per-skill execution and review state created on a ticket when an agent starts work
  - *stage* — a named phase of delivery work: context, shaping, discovery, exploration, specification, or engineering; a column on the board holding a queue, in-progress, and done tickets
  - *stage work required* — the ordered list of skills required by a stage
  - *board mode* — a setting on the kanban board that determines whether the kanban lead acts automatically or waits for user-directed action intents (manual mode)
  - *action intent* — a record written to the action state file by the app when the Delivery Lead assigns a team member agent to a ticket in manual mode
  - *action state file* — the file the app writes action intents to and the kanban lead watches for changes; lives alongside board.json in the kanban directory
- **Agent and Skills**
  - *skill* — a named practice method (e.g. abd-domain-language, abd-clean-code) that an agent executes on a ticket at a stage
  - *agent* — an autonomous worker with a delivery role and a work role (executor or reviewer) that starts work on skills for active tickets; base class extended by kanban lead and team member; reads its agent definition to know its role, skills, and workflow; lifecycle managed via Cursor SDK agent sessions
  - *agent definition* — the AGENT.md file for a role that defines identity, skills, workflow, and bootstrap instructions; located at practices/kanban/agents/{role}/AGENT.md
  - *agent session* — a running Cursor SDK session representing an active agent; replaces heartbeat files for tracking liveness
  - *bootstrap prompt* — the prompt assembled from the agent definition, workspace path, and role that initializes an agent session via the Cursor SDK
  - *agent output stream* — the real-time message stream from a running agent session, delivered via the Cursor SDK
  - *agent stream panel* — a UI panel beside a stage column that displays an agent's output stream; opened by clicking a team member avatar
  - *heartbeat* — an agent liveness indicator now derived from agent session state rather than file timestamps; age determines pool avatar state
  - *team member agent* — an agent operating in one of the four delivery roles that the kanban lead delegates skill execution to; distinguished from the kanban lead which orchestrates but does not execute skills

---

_The *kanban board* defines ordered *stages* — each with a *scope level* and *skills* — and runs them live with *tickets* flowing through *stages*. A *ticket* has a *board position* — the *stage* it occupies. When all skill work at a stage is done a ticket waits in stage done; a team member with the first skill of the next stage picks it up to advance it — or it scatters into child tickets if the next stage has finer scope. *Agent roles* pull skill work from tickets. The board is acted upon by a *team*. Each *agent* reads its *agent definition* and is launched as an *agent session* via the Cursor SDK; the *agent output stream* from each session is visible in real time through an *agent stream panel*. *Heartbeats* track whether each *agent role* is alive — now derived from *agent session* state. The board has a *board mode* — automatic or manual — that determines whether the *kanban lead* acts autonomously or waits for *action intents* written to the *action state file* by the *app* when the Delivery Lead assigns a *team member agent* to a *ticket*._

---

# Core Domain

## Kanban Board

The *kanban board* defines an ordered set of *stages* — each with a *scope level* and *skills* — and runs them live with *tickets* flowing through *stages*, each holding its tickets in-progress and done. A *ticket's* *board position* — which *stage* and whether in progress or done — is derived from its *skill progress*. When a *ticket* completes a *stage* it waits in the stage-done state. A *team* member who possesses the first *skill* of the next *stage* then picks it up, advancing the *ticket* to that *stage*; if the next *stage* has a finer *scope level* the *ticket* *scatters* into child *tickets*, each entering the backlog and waiting to be picked up. The board is acted upon by a *team* — the number of executor/reviewer pairs per *agent role*. The board carries a *board mode* — automatic or manual. In *manual mode* the *kanban lead* suppresses automatic pull, scatter, and advance actions and instead watches the *action state file* for *action intents* that direct it to delegate *skill* execution to a specific *team member agent*.

### kanban board

- defines an ordered set of *stages*, each with a *scope level* and an ordered list of *skills*
- is the single source of truth for which *skills* each *stage* requires — *skill progress* entries on a *ticket* are populated from it when work starts, never duplicated
- *tickets* flow through its *stages*; *skills* act on each *ticket* at its current *stage*
- is acted upon by a *team* — the number of executor/reviewer pairs per *agent role*
- records a timestamp each time it is saved

- **Invariant:** every *ticket* occupies exactly one *stage* at any given time


### ticket

- carries a unique identifier and a *lineage* tracing its ancestry from project through finer *scope levels*
- has a *board position* — either backlog, the *stage* it currently occupies, or complete
- holds a *scope level* matching its current *stage's* scope in the *kanban board*
- maintains a *priority* determining its ordering within the backlog, derived from the story map and thin-slicing
- tracks *skill progress* for each *skill* an *agent* starts work on — entries are created when work starts
- waits in **stage done** after all *skills* complete — does not advance automatically; a *team* member with the first *skill* of the next *stage* picks it up
- when picked up from *stage* done, either advances to the next same-scope *stage* or **scatters** — stays visible in done with a *scatter_to* reference and creates child *tickets* at the finer *scope level*, each entering backlog
- scattered child *tickets* carry a reference to their parent *ticket* and a priority from the story map
- records timestamps for when it entered and completed each *stage*
- carries free-text *notes* that may signal blocked status
- **Invariant:** the *kanban board* is the single source of truth for which *skills* a *stage* requires — the *ticket* never duplicates that list, only tracks what has been started
- **Invariant:** a *ticket's* *scope level* must match the scope declared by its current *stage* in the *kanban board*
- **Invariant:** scatter only occurs when the next *stage's* *scope level* is finer than the current

### board position

- is the *stage* a *ticket* currently occupies on the *kanban board*
- a *ticket* with no *stage* yet is in backlog; a *ticket* that has passed all *stages* is complete
- **Invariant:** a *ticket* never advances to the next *stage* automatically — a *team* member must pick it up from the *stage*'s done queue

### skill progress

- is created by the *stage* on the *ticket* when an *agent* starts work on a *skill* — not before
- tracks *execution status* through not started → in progress → done
- tracks *review status* through not started → in progress → done (or failed, triggering rework)
- records the *agent role* performing execution and the *agent role* performing review, plus start and end timestamps for both
- **Invariant:** *execution status* must reach done before *review status* can transition from not started to in progress
- **Invariant:** a *stage* is complete only when every *skill* defined in the *kanban board* for that *stage* has a *skill progress* entry with *execution status* done and *review status* done

### focus skill

- is the *skill* the board highlights on a *ticket* card and expanded skill list
- when a *skill* is under review, the *focus skill* is that reviewing *skill*
- when a *skill* is executing, the *focus skill* is that executing *skill*
- when an active *ticket* sits in **in progress** at a *stage* with no skill currently executing or under review, the *focus skill* is the first incomplete *skill* in *stage work required* order
- drives the bot or magnifying-glass icon on the ticket card face and the active row in the expanded skill list

### display focus

- is the *focus skill* shown on a *ticket* after per-role WIP from *team* capacity is applied
- when multiple active *tickets* at the same *stage* compete for the same *agent role*, only the highest-priority *tickets* up to the role's executor count receive *display focus* for idle next-*skill* highlighting
- live execution or review always receives *display focus* regardless of WIP rank

### role engagement

- is the count of active *tickets* where an *agent role* is currently engaged
- a *ticket* engages a role when an *agent* of that role is executing or reviewing a *skill*, or when the *ticket* holds *display focus* on a *skill* that requires that role
- drives how many agent-pool avatar slots display as "working" for each *agent role*

### pool avatar state

- is the visual liveness of an avatar in the agent pool: **working**, **idle**, or **inactive**
- **working** — role is engaged on the board (lit with role-color ring)
- **idle** — role is available (lit, no ring)
- **inactive** — role is stale: *heartbeat* age exceeds the threshold and the role has zero board engagement (dim)

### stage

- is a named phase of delivery work: context, shaping, discovery, exploration, specification, or engineering — always in that order
- is a column on the *kanban board*; each *ticket* occupies exactly one *stage*
- carries a *scope level* defined by the *kanban board*
- has a **queue** — *tickets* from the previous *stage*'s done waiting to be picked up; a *team* member with the first required *skill* can take a *ticket* from the queue
- has **in progress** — *tickets* at this *stage* where *skill* work is underway
- has **done** — *tickets* at this *stage* where all *skills* are complete, waiting for pickup to the next *stage*
- **Invariant:** a *ticket* cannot skip a *stage* or move backward
- **Invariant:** a *ticket* in the queue of *stage* N was in the done state of *stage* N-1

### stage work required

- is the ordered list of *skills* required by a *stage*
- each *skill* is performed by an *agent role*
- describes what work a *ticket* at each *stage* requires

### team

- is the executor/reviewer pair counts per *agent role* configured on the board
- holds a count per *agent role* that can be incremented or decremented
- **Invariant:** pair counts must be non-negative integers
- **Invariant:** defaults to one executor and one reviewer per *agent role* when not explicitly configured

### board mode

- is a setting on the *kanban board* that determines whether the *kanban lead* acts automatically or waits for user-directed *action intents*
- defaults to automatic — the *kanban lead* pulls, scatters, and advances *tickets* without intervention
- when set to manual, suppresses all automatic *kanban lead* actions — pull, scatter, and advance wait for explicit *action intents*
- persists as part of the *kanban board* configuration alongside *stages* and *team*
- **Invariant:** the *kanban board* is always in exactly one *board mode* — automatic or manual — never both or neither

### action intent

- is a record written to the *action state file* by the *app* when the Delivery Lead assigns a *team member agent* to a *ticket* in *manual mode*
- specifies which *skill* to execute on which *ticket* and which *team member agent* should perform the work
- is consumed by the *kanban lead* when it detects a change in the *action state file*
- triggers the *kanban lead* to delegate *skill* execution to the named *team member agent*
- **Invariant:** an *action intent* is only written when the *kanban board* is in *manual mode*
- **Invariant:** the specified *skill* must be one required by the *ticket's* current *stage*

### action state file

- is the file the *app* writes *action intents* to and the *kanban lead* watches for changes
- lives alongside board.json in the kanban directory
- is the communication channel between the *app* (writing) and the *kanban lead* (reading)
- is watched by the *kanban lead* for changes that signal new *action intents* to process
- **Invariant:** only the *app* writes to the *action state file*; only the *kanban lead* reads from it

#### Decisions made

- *Stage*, *ticket*, *board position*, *skill progress*, *stage work required*, and *team* all belong here — none has meaning outside the *kanban board* (independence test).
- *Scatter* is an operation on *ticket*, not a standalone concept — its mechanics and invariant live on the *ticket* block (typing call).
- Individual stage names are instances of *stage*, not subtypes (typing call).
- *Board mode*, *action intent*, and *action state file* belong here — they govern how the *kanban board* operates and have no meaning outside it (independence test).
- *Board mode* is a setting on the *kanban board*, not a separate concept or subtype — automatic and manual are values, not types (typing call).

#### References

**Ref — kanbanBoard.ts core types, Ticket, SkillProgress, and team schema**
Source: packages/delivery-board/shared/kanbanBoard.ts
Locator: lines 1–141
Extract: whole

**Ref — parseSystemOfWork.ts types and builder**
Source: packages/delivery-board/shared/parseSystemOfWork.ts
Locator: lines 1–78
Extract: whole

**Ref — abd-kanban concepts — Kanban model, System of work, Tickets, Skill status flow, Scattering**
Source: practices/kanban/skills/abd-kanban/reference/concepts.md
Locator: Kanban model table, System of work, Tickets, Skill status flow, Scattering sections
Extract: whole

**Ref — delivery_model.py Ticket, SkillProgress, and SystemOfWork dataclasses**
Source: practices/kanban/skills/abd-kanban/scripts/delivery_model.py
Locator: lines 26–148
Extract: whole

---

## Agent and Skills

*A skill* is a named practice method (e.g. `abd-domain-language`, `abd-clean-code`) that an *agent* executes on a *ticket* at a *stage*. An *agent* is a base class extended by *kanban lead* and *team member agent*; it reads its *agent definition* to know its role, skills, and workflow. Every *agent* operates under an *agent role* — one of four delivery roles — which determines which *skills* it can start work on. *Agents* are created, started, stopped, and monitored via the Cursor SDK as *agent sessions*; Each running *agent session* provides an *agent output stream* — real-time messages visible through an *agent stream panel* in the UI. *Heartbeats* remain as a display concept for *pool avatar state* but are now derived from *agent session* liveness rather than file timestamps. A *team member agent* is an *agent* operating in one of the four delivery roles that the *kanban lead* delegates *skill* execution to; distinguished from the *kanban lead* which orchestrates but does not execute *skills*.

### skill

- is a named practice method an *agent* executes on a *ticket* — e.g. `abd-domain-language`, `abd-story-acceptance-criteria`, `abd-clean-code`
- is required by a *stage* through *stage work required*
- is performed by an *agent role*

### agent

- is the base class extended by *kanban lead* and *team member agent*
- reads its *agent definition* to know its identity, delivery role, available *skills*, and workflow
- starts work on *skills* for active *tickets* and drives them to done
- has a **work role** — either executor or reviewer
- as executor: does the *skill* work on the *ticket*
- as reviewer: checks the *skill* work on the *ticket*
- operates under one of four named delivery roles — product-owner, business-expert, ux-designer, or engineer — which determines which *skills* it can start work on
- is constrained by its role's *team* count — the number of executors and reviewers that may work concurrently
- lifecycle managed via Cursor SDK *agent sessions* — created, started, stopped, and monitored through the SDK
- reports liveness through its *agent session* state; *heartbeat* is derived from session liveness
- **Invariant:** an *agent* may only start work on *skills* that require its role
- **Invariant:** the *kanban lead* is a separate orchestrating role, not a delivery *agent*
- **Invariant:** an *agent* cannot run without a valid *agent definition*

### agent definition

- is a set of agent markdown files that collectively configure an *agent's* identity, workflow, and behavior
- the root file is `AGENT.md` at `practices/kanban/agents/{role}/AGENT.md` — declares fixed identity (role name, slot type, playbook reference)
- references shared workflow files that complete the definition:
  - `reference/agent-workflow/executor-workflow.md` — the execute-and-review workflow every team member follows
  - `reference/session-bootstrap.md` — bootstrap protocol (resolve workspace, arm pull loop, write heartbeat)
  - `reference/pull-model.md` — how agents pull eligible *skills* from active *tickets*
  - `reference/work-queue.md` — claiming rules, *skill* order, rail priority
  - `reference/roles/{role}.md` — the role's playbook (behavioral guidance specific to the delivery role)
- the *skills* each role can execute are defined by `kanban.json` *stage work required*, not by the `AGENT.md` itself — the agent reads the board to discover its eligible work
- is read directly by the *agent* at startup — all files are plain markdown, no intermediate parsing layer
- **Invariant:** every *agent* role has exactly one `AGENT.md` root file
- **Invariant:** `AGENT.md` must reference a valid workflow file

### agent session

- is a running Cursor SDK session representing an active *agent*
- has a lifecycle: created → running → completed/failed
- is created by assembling a *bootstrap prompt* from the *agent definition* and invoking the Cursor SDK
- provides an *agent output stream* of real-time messages while running
- determines *heartbeat* state — a running session means alive; a completed/failed session means stale
- **Invariant:** each *agent* slot (executor or reviewer instance within a *team membership*) has at most one active *agent session* — a role with two executor slots and one reviewer slot can have up to three concurrent sessions
- **Invariant:** an *agent session* must be in exactly one lifecycle state at any given moment

### bootstrap prompt

- is the prompt assembled from the *agent definition* and role that initializes an *agent session* via the Cursor SDK
- workspace path is injected by the *kanban lead* at creation time — the lead reads it from the *kanban board's* configured workspace, not from the *agent definition*
- combines identity, workflow instructions, and workspace context into a single initialization payload
- is constructed by the *kanban lead* when creating an *agent session* — never hand-written at runtime
- **Invariant:** a *bootstrap prompt* must reference a valid *agent definition*
- **Invariant:** workspace path must come from the *kanban board*, not be hardcoded in the prompt

### agent output stream

- is the real-time message stream from a running *agent session*, delivered via the Cursor SDK
- contains the agent's reasoning, tool calls, and status updates as they occur
- is consumed by the UI to populate *agent stream panels*
- streams only while the *agent session* is in the running state
- **Invariant:** an *agent output stream* exists only for an *agent session* in the running state

### agent stream panel

- is a UI panel beside a stage column that displays an *agent's* *agent output stream*
- opens when a user clicks a *team member agent* avatar in the pool or on a *ticket*
- shows messages in chat-like format as they arrive from the *agent output stream*
- multiple panels can be open side by side for different *agents*
- closes or goes inactive when the *agent session* completes or fails
- **Invariant:** an *agent stream panel* is always bound to exactly one *agent session*

### heartbeat

- is an *agent* liveness indicator derived from *agent session* state
- age is determined by how long since the *agent session* last emitted activity, rather than a file timestamp
- determines *agent* liveness together with board engagement: stale *heartbeat* dims avatars only when the role has zero board engagement
- remains the concept that drives *pool avatar state* transitions (working, idle, inactive)
- **Invariant:** an *agent* pool avatar is **inactive** only when *heartbeat* age exceeds the staleness threshold **and** the role has zero *role engagement* on active *tickets*

### kanban lead

- is the *agent* subclass that manages the *kanban board* — the single orchestrating role above the four delivery roles
- reads its *agent definition* from `practices/kanban/agents/kanban-lead/AGENT.md`
- is launched as an *agent session* via the Cursor SDK
- detects when a *stage* is complete and triggers *scatter* when needed
- monitors *agent sessions* to determine which *agents* are alive
- assigns eligible *skills* to available *team members* across all columns (active, done, backlog) — downstream *stages* first; promotes backlog *tickets* to active on claim
- reads *board mode* setting before acting — in *manual mode*, suppresses automatic pull, scatter, and advance actions
- watches the *action state file* for changes written by the *app*
- delegates *skill* execution to the appropriate *team member agent* based on *action intents*

### team member agent

- is the *agent* subclass operating in one of the four delivery roles (product-owner, business-expert, ux-designer, engineer) that the *kanban lead* delegates *skill* execution to
- reads its *agent definition* from `practices/kanban/agents/{role}/AGENT.md`
- is launched as an *agent session* via the Cursor SDK when the *kanban lead* assigns it work
- executes a single assigned *skill* on a *ticket* when directed by the *kanban lead* via an *action intent*
- advances the *ticket* to in progress when it starts executing its first *skill*
- persists *skill* completion to the board state upon finishing execution
- completes the *ticket* when all *skills* at its current *stage* are finished
- provides an *agent output stream* visible in an *agent stream panel*
- is distinguished from the *kanban lead* which orchestrates but does not execute *skills*
- **Invariant:** a *team member agent* only executes *skills* that match its delivery role

#### Decisions made

- *Skill* and *agent* are the core concepts — role, executor/reviewer variant, and *team* constraint are properties of the *agent*, not separate concepts (independence test).
- *Agent* is a base class with *kanban lead* and *team member agent* as subclasses — each extends the base with role-specific orchestration or execution behavior (typing call).
- *Heartbeat* remains as a display concept for *pool avatar state* but is now derived from *agent session* liveness rather than file timestamps (mechanism change, not a new concept).
- *Agent session* belongs here — it is the SDK-managed lifecycle that replaces file-based heartbeat polling and has no meaning outside *agent* monitoring (independence test).
- *Agent definition* belongs here — it is the declarative identity file that an *agent* reads at startup; without it the *agent* cannot initialize (independence test).
- *Bootstrap prompt* belongs here — it is constructed from the *agent definition* to create an *agent session* and has no standalone meaning (independence test).
- *Agent output stream* and *agent stream panel* belong here — the stream is a property of the running *agent session* and the panel is its UI projection (independence test).
- Individual role names remain instances of the role property on *agent*, not subtypes (typing call).
- *Kanban lead* orchestrates the board but its full behavior belongs to the Kanban Lead module (scope-fit test).

#### References

**Ref — kanbanBoard.ts AGENT_ROLES and HeartbeatAges**
Source: packages/delivery-board/shared/kanbanBoard.ts
Locator: lines 121–122, 192
Extract: whole

**Ref — kanbanBoard.service.ts heartbeat reading**
Source: packages/delivery-board/server/kanbanBoard.service.ts
Locator: lines 60–79
Extract: whole

**Ref — abd-kanban concepts — Role agents**
Source: practices/kanban/skills/abd-kanban/reference/concepts.md
Locator: Role agents section
Extract: whole

**Ref — Agent class hierarchy and AGENT.md structure**
Source: practices/kanban/agents/
Locator: {role}/AGENT.md files
Extract: identity, skills, workflow sections

**Ref — Cursor SDK agent lifecycle**
Source: @cursor/sdk
Locator: Agent.create, Agent.prompt, run.stream API surface
Extract: session lifecycle and streaming interface

---
