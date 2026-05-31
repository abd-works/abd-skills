---
state: crc
---

# Module: [Delivery Agent Kanban]

Scope: How delivery work is modeled and tracked: the kanban board with its ordered stages and skills, tickets flowing through stages, skill progress determining board position, and agent roles pulling skill work.

**Core terms**:
- kanban board
- ticket
- stage
- board position
- skill progress
- skill
- agent
- heartbeat
- team
- stage work required
- kanban lead

**Key Abstractions (term grouping)**:
- **Kanban Board**: kanban board, stage, board position, stage work required, team, ticket, skill progress
- **Agent and Skills**: agent, skill, heartbeat, kanban lead

---

# Core Domain

## **Kanban Board**

### **Kanban Board**
ordered stages                          | Stage
active stage flow                       | Stage
team configuration                      | Team
tickets in flow                         | Ticket
saved-at timestamp                      | (ISO timestamp)
define stage order                      | Stage
record save timestamp                   | (writes current time on each persist)
                                        |   invariant: every ticket occupies exactly one stage at any given time

### **Ticket**
unique identifier                       | (string)
lineage                                 | (ordered ancestry from project through scope levels)
board position                          | Stage
scope level                             | (matches current stage's scope in the kanban board)
priority                                | (numeric ordering from story map and thin-slicing)
skill progress entries                  | Skill Progress
notes                                   | (free-text; "blocked" signals blocked status)
stage timestamps                        | (entered-at, completed-at per stage)
wait in stage done                      | Stage
advance to next stage                   | Stage, Team
scatter into child tickets              | Ticket
                                        |   invariant: kanban board is single source of truth for which skills a stage requires — ticket never duplicates that list
                                        |   invariant: scope level must match the scope declared by its current stage
                                        |   invariant: scatter only occurs when the next stage's scope level is finer than the current

### **Board Position**
current stage                           | Stage
in-progress or done sub-state           | (derived from skill progress)
                                        |   invariant: a ticket never advances to the next stage automatically — a team member must pick it up

### **Skill Progress**
execution status                        | (not started, in progress, done)
review status                           | (not started, in progress, done, failed)
executing agent role                    | Agent
reviewing agent role                    | Agent
execution start and end timestamps      | (ISO timestamps)
review start and end timestamps         | (ISO timestamps)
                                        |   invariant: execution status must reach done before review status can leave not started
                                        |   invariant: a stage is complete only when every skill in the kanban board for that stage has execution done and review done

### **Stage**
stage name                              | (context, shaping, discovery, exploration, specification, engineering)
scope level                             | (defined by kanban board)
queue of tickets                        | Ticket
in-progress tickets                     | Ticket
done tickets                            | Ticket
                                        |   invariant: a ticket cannot skip a stage or move backward
                                        |   invariant: a ticket in the queue of stage N was in done of stage N-1

### **Stage Work Required**
ordered skills                          | Skill
agent role per skill                    | Agent
                                        |   invariant: describes what work a ticket at each stage requires

### **Team**
executor and reviewer pair counts       | Agent
increment pair count                    | Agent
decrement pair count                    | Agent
                                        |   invariant: pair counts must be non-negative integers
                                        |   invariant: defaults to one executor and one reviewer per agent role when not explicitly configured

### references

**Ref — Ubiquitous Language: Kanban Board KA**
Source: docs/domain/ubiquitous-language.md
Locator: lines 31–130
Extract: whole

**Ref — abd-kanban concepts**
Source: practices/kanban/skills/abd-kanban/reference/concepts.md
Locator: Kanban model, System of work, Tickets, Skill status flow, Scattering sections
Extract: whole

### decisions made

- *Board Position* is a value derived from a ticket's skill progress and current stage — it is not a standalone entity with independent lifecycle; it belongs on the Kanban Board KA because it only has meaning in the context of a ticket on a board.
- *Scatter* is an operation on Ticket, not a standalone concept — its mechanics and invariant live on the Ticket block.
- Individual stage names (context, shaping, etc.) are instances of Stage, not subtypes — they share identical behavior.
- *Stage Work Required* is a separate concept from Stage because it carries the ordered list of skills and role assignments; Stage carries positional state (queue, in-progress, done).

---

## **Agent and Skills**

### **Agent**
delivery role                           | (product-owner, business-expert, ux-designer, engineer)
work role                               | (executor or reviewer)
start work on skill                     | Skill, Ticket, Skill Progress
drive skill to done                     | Skill Progress
write heartbeat                         | Heartbeat
                                        |   invariant: an agent may only start work on skills that require its role
                                        |   invariant: the kanban lead is a separate orchestrating role, not an agent

### **Skill**
skill name                              | (e.g. abd-ubiquitous-language, abd-clean-code)
required by stage                       | Stage Work Required
performed by agent role                 | Agent

### **Heartbeat**
timestamp of last activity              | (ISO timestamp)
age in seconds                          | (elapsed since last written)
determine liveness                      | Agent, Ticket
                                        |   invariant: pool avatar inactive only when heartbeat stale and role has zero board engagement

### **Role Engagement**
count engaged tickets per role          | Ticket, Agent, Display Focus
derive from live work or display focus  | Focus Skill, Team

### **Kanban Lead**
manage kanban board                     | Kanban Board
detect stage completion                 | Stage, Ticket
trigger scatter                         | Ticket
monitor heartbeats                      | Heartbeat, Agent
pull tickets from backlog               | Ticket, Stage

### references

**Ref — Ubiquitous Language: Agent and Skills KA**
Source: docs/domain/ubiquitous-language.md
Locator: lines 132–194
Extract: whole

**Ref — abd-kanban concepts — Role agents**
Source: practices/kanban/skills/abd-kanban/reference/concepts.md
Locator: Role agents section
Extract: whole

### decisions made

- *Skill* and *Agent* are the core concepts — role, executor/reviewer variant, and team constraint are properties of the agent, not separate concepts.
- *Heartbeat* belongs here because it exists to report agent liveness and has no meaning outside agent monitoring. Age and liveness determination are properties of the heartbeat.
- Individual role names are instances of the role property on Agent, not subtypes.
- *Kanban Lead* orchestrates the board; its full behavior belongs to a Kanban Lead module but its core interactions with agents and the board are captured here.

---
