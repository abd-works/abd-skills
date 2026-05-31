---
state: ubiquitous-language
---

# Module: [Delivery Agent Kanban]

_Concept sketch for the real-time Kanban board that drives an agentic agile delivery pipeline — tickets flow through stages, agents start work on skills for tickets._

Scope: How delivery work is modeled and tracked: the kanban board with its ordered stages and skills, tickets flowing through stages, skill progress determining board position, and agent roles pulling skill work.

**Terms**:
- **Kanban Board**
  - **kanban board** — the blueprint of ordered stages, scope levels, and skills that governs ticket flow — live with tickets flowing through stages
  - **team** — the collection executor/reviewer pairs and their counts per agent role configured on the board
  - **ticket** — a unit of work at the scope level its current stage requires, carrying lineage, priority, and skill progress entries created as work starts
  - **board position** — the stage a ticket currently occupies
  - **skill progress** — the per-skill execution and review state created on a ticket when an agent starts work
  - **stage** — a named phase of delivery work: context, shaping, discovery, exploration, specification, or engineering; a column on the board holding a queue, in-progress, and done tickets
  - **stage work required** — the ordered list of skills required by a stage
- **Agent**
  - **skill** — a named practice method (e.g. abd-ubiquitous-language, abd-clean-code) that an agent executes on a ticket at a stage
  - **agent** — an autonomous worker with a delivery role and a work role (executor or reviewer) that starts work on skills for active tickets
  - **heartbeat** — a timestamp written by each agent recording last activity; age determines liveness

---

_The *kanban board* defines ordered *stages* — each with a *scope level* and *skills* — and runs them live with *tickets* flowing through *stages*. A *ticket* has a *board position* — the *stage* it occupies. When all skill work at a stage is done a ticket waits in stage done; a team member with the first skill of the next stage picks it up to advance it — or it scatters into child tickets if the next stage has finer scope. *Agent roles* pull skill work from tickets. The board is acted upon by a *team*. *Heartbeats* track whether each *agent role* is alive._

---

# Core Domain

## Kanban Board

The *kanban board* defines an ordered set of *stages* — each with a *scope level* and *skills* — and runs them live with *tickets* flowing through *stages*, each holding its tickets in-progress and done. A *ticket's* *board position* — which *stage* and whether in progress or done — is derived from its *skill progress*. When a *ticket* completes a *stage* it waits in the stage-done state. A *team* member who possesses the first *skill* of the next *stage* then picks it up, advancing the *ticket* to that *stage*; if the next *stage* has a finer *scope level* the *ticket* *scatters* into child *tickets*, each entering the backlog and waiting to be picked up. The board is acted upon by a *team* — the number of executor/reviewer pairs per *agent role*.

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
- when picked up from *stage* done, either advances to the next same-scope *stage* or **scatters** — archives itself and creates child *tickets* at the finer *scope level*, each entering backlog
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

#### Decisions made

- *Stage*, *ticket*, *board position*, *skill progress*, *stage work required*, and *team* all belong here — none has meaning outside the *kanban board* (independence test).
- *Scatter* is an operation on *ticket*, not a standalone concept — its mechanics and invariant live on the *ticket* block (typing call).
- Individual stage names are instances of *stage*, not subtypes (typing call).

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

*A skill* is a named practice method (e.g. `abd-ubiquitous-language`, `abd-clean-code`) that an *agent* executes on a *ticket* at a *stage*. An *agent* is an autonomous executor that can perform skills and drives them to done. Every *agent* operates under an *agent role* — one of four delivery roles — which determines which *skills* it can start work on. *Agents* report liveness via *heartbeats*; *heartbeat* age determines whether an *agent* is alive or stale.

### skill

- is a named practice method an *agent* executes on a *ticket* — e.g. `abd-ubiquitous-language`, `abd-acceptance-criteria`, `abd-clean-code`
- is required by a *stage* through *stage work required*
- is performed by an *agent role*

### agent

- is an autonomous worker that starts work on *skills* for active *tickets* and drives them to done
- has a **work role** — either executor or reviewer
- as executor: does the *skill* work on the *ticket*
- as reviewer: checks the *skill* work on the *ticket*
- operates under one of four named delivery roles — product-owner, business-expert, ux-designer, or engineer — which determines which *skills* it can start work on
- is constrained by its role's *team* count — the number of executors and reviewers that may work concurrently
- reports liveness by writing a *heartbeat*
- **Invariant:** an *agent* may only start work on *skills* that require its role
- **Invariant:** the *kanban lead* is a separate orchestrating role, not an *agent*

### heartbeat

- is a timestamp written by each *agent* and the *kanban lead* recording last activity
- age is the elapsed seconds since it was last written
- determines *agent* liveness together with board engagement: stale *heartbeat* dims avatars only when the role has zero board engagement
- **Invariant:** an *agent* pool avatar is **inactive** only when *heartbeat* age exceeds the staleness threshold **and** the role has zero *role engagement* on active *tickets*

### kanban lead

- manages the *kanban board* — the single orchestrating role above the four delivery roles
- detects when a *stage* is complete and triggers *scatter* when needed
- monitors *heartbeats* to determine which *agents* are alive
- pulls *tickets* from the backlog into the first *stage*

#### Decisions made

- *Skill* and *agent* are the core concepts — role, executor/reviewer variant, and *team* constraint are properties of the *agent*, not separate concepts (independence test).
- *Heartbeat* belongs here — it exists to report *agent* liveness and has no meaning outside *agent* monitoring (independence test). Age and liveness determination are properties of the *heartbeat*, not a separate concept.
- Individual role names are instances of the role property on *agent*, not subtypes (typing call).
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

---
