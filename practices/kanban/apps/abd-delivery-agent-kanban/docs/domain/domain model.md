---
state: domain-model
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
- team member
- agent session
- agent definition
- bootstrap prompt
- agent output stream
- agent stream panel

**Key Abstractions (term grouping)**:
- **Kanban Board**: kanban board, stage, board position, stage work required, team, ticket, skill progress
- **Agent and Skills**: agent, skill, heartbeat, kanban lead, team member, agent session, agent definition, bootstrap prompt, agent output stream, agent stream panel

---

# Core Domain

## **Kanban Board**

### **KanbanBoard**

KanbanBoard(Stage, FilePath, Team)
------
savedAt: Timestamp
workspacePath: FilePath
stages: Stage
	Invariant: single source of truth for which skills each stage requires — each Stage carries its own StageWorkRequired; tickets never duplicate that list
team: Team
----
defineStageOrder(Stage): void
recordSaveTimestamp(): void
ticketsInFlow(): Ticket
	Stage
	Invariant: every ticket occupies exactly one stage at any given time
stageFor(Ticket): Stage
nextStageFor(Ticket): Stage
	Invariant: returns the stage immediately after the ticket's current boardPosition in the ordered stages list
advanceCompletedTickets(): void
	Stage, Ticket
	Invariant: for each ticket in any stage's done bucket whose skills are all done — scatter into child tickets if next stage is finer scope, otherwise advance to next stage
staleAgents(): TeamMember
	Team, AgentSession
	Invariant: returns TeamMembers whose AgentSession has not produced output within the expected heartbeat window

### **Ticket**

Ticket(Identifier, Ticket, ScopeLevel, Integer)
------
id: Identifier
lineage: Ticket
boardPosition: Stage
	Invariant: scopeLevel must match the scope declared by the current stage
scopeLevel: ScopeLevel
priority: Integer
skillProgress: SkillProgress
	Invariant: kanban board is single source of truth for which skills a stage requires — ticket never duplicates that list
notes: FreeText
stageTimestamps: StageTimestamp
isBlocked: Boolean
----
waitInStageDone(Stage): void
advanceToNextStage(Stage, Team): void
	StageTimestamp
	Invariant: a ticket never advances to the next stage automatically — a team member must initiate advancement
scatterIntoChildTickets(Stage): Ticket
	Invariant: scatter only occurs when the next stage's scope level is finer than the current stage's scope level
skillsDoneFor(StageWorkRequired): Boolean
	SkillProgress
	Invariant: true only when every skill in stageWorkRequired has a SkillProgress entry with executionStatus DONE and reviewStatus DONE
- isScopeFinerThan(ScopeLevel, ScopeLevel): Boolean
	Invariant: returns true when nextScopeLevel represents a narrower granularity than currentScopeLevel in the board's declared scope progression

### **BoardPosition**

BoardPosition(Stage, SubState)
------
currentStage: Stage
subState: SubState
	Invariant: a ticket never advances to the next stage automatically — readiness is signalled, not acted upon automatically
isReadyToAdvance: Boolean
	Invariant: true only when subState is DONE — all required skills have execution done and review done

### **SkillProgress**

SkillProgress(Skill, DeliveryRole, DeliveryRole)
------
skillName: Skill
executionStatus: ExecutionStatus
reviewStatus: ReviewStatus
executingAgentRole: DeliveryRole
reviewingAgentRole: DeliveryRole
executionStartedAt: Timestamp
executionCompletedAt: Timestamp
reviewStartedAt: Timestamp
reviewCompletedAt: Timestamp
----
startExecution(Agent): void
	Invariant: transitions executionStatus to IN_PROGRESS; records executionStartedAt
completeExecution(): void
	Invariant: transitions executionStatus to DONE; records executionCompletedAt; execution must reach DONE before review status can leave NOT_STARTED
startReview(Agent): void
	Invariant: may only be called when executionStatus is DONE; transitions reviewStatus to IN_PROGRESS; records reviewStartedAt
completeReview(): void
	Invariant: transitions reviewStatus to DONE; records reviewCompletedAt
failReview(): void
	Invariant: transitions reviewStatus to FAILED
isDone(): Boolean
	Invariant: true only when executionStatus is DONE and reviewStatus is DONE

### **Stage**

Stage(StageName, ScopeLevel, StageWorkRequired)
------
name: StageName
scopeLevel: ScopeLevel
workRequired: StageWorkRequired
queue: Ticket
inProgress: Ticket
done: Ticket
----
enqueue(Ticket): void
	Invariant: a ticket cannot skip a stage or move backward — ticket must have been in done of the prior stage before being enqueued here
moveToInProgress(Ticket): void
moveToDone(Ticket): void
allTickets(): Ticket
contains(Ticket): Boolean

### **StageWorkRequired**

StageWorkRequired(Skill, DeliveryRole)
------
orderedSkills: Skill
agentRoles: DeliveryRole
	Invariant: every skill in orderedSkills has an entry in agentRoles mapping to a delivery role
----
roleFor(Skill): DeliveryRole

### **StageTimestamp**

StageTimestamp(Stage)
------
enteredAt: Timestamp
completedAt: Timestamp

### **Team**

Team(TeamMembership)
------
memberships: TeamMembership
	Invariant: one TeamMembership per delivery role
----
incrementPairCount(DeliveryRole): void
	TeamMembership
decrementPairCount(DeliveryRole): void
	TeamMembership
	Invariant: result must remain non-negative

### **TeamMembership**

TeamMembership(DeliveryRole, Integer)
------
role: DeliveryRole
pairCount: Integer
	Invariant: must be non-negative; defaults to 1 when not explicitly configured
pairs: TeamMemberPair
----
incrementPairCount(): void
	TeamMemberPair
	Invariant: adds one new unfilled TeamMemberPair to pairs
decrementPairCount(): void
	TeamMemberPair
	Invariant: pairCount must remain non-negative; removes the last unfilled pair
unstaffedPairs(): TeamMemberPair
	Invariant: returns pairs where isFullyStaffed() is false — KanbanLead uses this to know which pairs need agents spawned

### **TeamMemberPair**

TeamMemberPair(DeliveryRole)
------
role: DeliveryRole
executor: TeamMember
reviewer: TeamMember
----
isFullyStaffed(): Boolean
	Invariant: true when both executor and reviewer hold live TeamMember agent references

### references

**Ref — Domain Language: Kanban Board KA**
Source: docs/domain/domain-language.md
Locator: lines 31–130
Extract: whole

**Ref — abd-kanban concepts**
Source: practices/kanban/skills/abd-kanban/reference/concepts.md
Locator: Kanban model, System of work, Tickets, Skill status flow, Scattering sections
Extract: whole

### decisions made

- *KanbanBoard* receives workspacePath as a constructor property because BootstrapPrompt requires it at session creation time and the domain model declares it as coming from board config.
- *StageWorkRequired* is owned by Stage, not by KanbanBoard — work required changes per column (stage), so it belongs on the thing that changes with it.
- *Team* lifecycle is fully contained within a board configuration; it has no standalone existence independent of the board that owns it.
- *StageTimestamp* is a typed pair extracted from the Ticket's "stage timestamps" domain model responsibility; it carries both enteredAt and completedAt as a named unit.
- *StageName* values are CONTEXT, SHAPING, DISCOVERY, EXPLORATION, SPECIFICATION, ENGINEERING.
- *ScopeLevel* values are INITIATIVE, PARTITION, INCREMENT, SPRINT, STORY, SCENARIO — ordered coarse to fine.
- *SubState* values are IN_PROGRESS and DONE; *ExecutionStatus* values are NOT_STARTED, IN_PROGRESS, DONE; *ReviewStatus* values are NOT_STARTED, IN_PROGRESS, DONE, FAILED; *WorkRole* values are EXECUTOR and REVIEWER.
- *Team* is an indirect collaborator in Ticket.advanceToNextStage (from domain model); KanbanLead extracts the relevant team configuration before calling this operation. Team is in the signature to honour the domain model declaration.
- *BoardPosition* is computed on demand from the Ticket's boardPosition (Stage) and the aggregate state of its SkillProgress entries. TeamMember creates a BoardPosition when it advances a ticket to in-progress.
- *Scatter* produces child Ticket instances whose lineage includes the parent's id; the KanbanLead triggers the operation.

---

## **Agent and Skills**

### **Agent**

Agent(DeliveryRole, WorkRole, AgentDefinition)
------
deliveryRole: DeliveryRole
workRole: WorkRole
agentDefinition: AgentDefinition
----
readAgentDefinition(AgentDefinition): void
createAgentSession(BootstrapPrompt): AgentSession
	Invariant: agent lifecycle managed by Cursor SDK sessions, not file-based heartbeats
startWorkOnSkill(Skill, Ticket): SkillProgress
	Invariant: agent may only start work on skills that require its delivery role
driveSkillToDone(SkillProgress): void
writeHeartbeat(): Heartbeat

### **TeamMember : Agent**

TeamMember(DeliveryRole, WorkRole, AgentDefinition)
------
----
advanceTicketToInProgress(Ticket): BoardPosition
	SkillProgress
	Invariant: only triggers on the first skill start — no-op when any SkillProgress entry is already IN_PROGRESS or DONE
persistSkillCompletion(KanbanBoard, SkillProgress): void
	Invariant: writes updated skillProgress state to the kanban board's persistent store
completeTicket(Ticket, Stage): void
	Invariant: a team member agent only executes skills that match its delivery role; ticket is moved to stage.done when all skills are done

### **KanbanLead : Agent**

KanbanLead(DeliveryRole, WorkRole, AgentDefinition)
------
----
monitorHeartbeats(Agent): Heartbeat
assignNextEligibleSkill(Board, AgentRole): SkillAssignment
startTeamMemberAgent(TeamMemberPair, WorkRole): AgentSession
stopTeamMemberAgent(AgentSession): void
restartStaleAgent(TeamMember): AgentSession
	Invariant: stale session is stopped before a new session is created for the same pair
dispatchSkillToIdleTeamMember(TeamMember, Ticket, Skill): void
runScanCycle(KanbanBoard): void
	TeamMemberPair, TeamMember
	Invariant: one pass — board advances or scatters completed tickets; lead staffs empty pairs and restarts stale agents

### **Skill**

------
name: SkillName
performedByRole: DeliveryRole

### **Heartbeat**

------
session: AgentSession
poolAvatarState: AvatarState
	Invariant: pool avatar inactive only when session is not running and agent role has zero board engagement
----
determineLiveness(Agent, Ticket): Boolean
- agentRoleHasBoardEngagement(Agent, Ticket): Boolean
	Invariant: true when any active ticket has a SkillProgress entry with the agent's deliveryRole in a non-DONE execution state

### **RoleEngagement**

------
role: DeliveryRole
engagedTicketCount: Integer
	Invariant: derived from live work or display focus, not stored independently
----
countEngagedTickets(Ticket, Agent): Integer

### **AgentSession**

AgentSession(SessionId, DeliveryRole)
------
sessionId: SessionId
agentRole: DeliveryRole
lifecycleState: SessionLifecycleState
	Invariant: one active session per agent slot at any time — a role with two executor slots and one reviewer slot may have at most three concurrent sessions
outputStream: AgentOutputStream
----
isRunning(): Boolean
	Invariant: true only when lifecycleState is RUNNING
agentIsLive(): Boolean
	Invariant: true only when lifecycleState is RUNNING

### **AgentDefinition**

------
role: DeliveryRole
rootFilePath: FilePath
	Invariant: every agent role has exactly one AGENT.md root file at agents/{role}/AGENT.md
sharedWorkflowFiles: FilePath
rolePlaybookPath: FilePath
	Invariant: skills each role can execute come from kanban.json stage work required, not from this definition

### **BootstrapPrompt**

------
workspacePath: FilePath
	Invariant: workspace path injected from KanbanBoard by KanbanLead, never sourced from AgentDefinition
roleIdentity: DeliveryRole
promptContent: PromptText
	Invariant: must contain workspace and role identity before being passed to createAgentSession
----
assembleFrom(AgentDefinition, FilePath): BootstrapPrompt
	Invariant: KanbanLead is the exclusive caller; it extracts workspacePath from KanbanBoard before passing it here

### **AgentOutputStream**

AgentOutputStream(SessionId)
------
sessionId: SessionId
messages: Message
----
deliverMessage(Message): void
messageHistory(): Message

### references

**Ref — Domain Language: Agent and Skills KA**
Source: docs/domain/domain-language.md
Locator: lines 132–194
Extract: whole

**Ref — abd-kanban concepts — Role agents**
Source: practices/kanban/skills/abd-kanban/reference/concepts.md
Locator: Role agents section
Extract: whole

### decisions made

- *Agent* is a base class — it is never instantiated directly; all concrete agents are either a TeamMember or a KanbanLead. writeHeartbeat() remains on Agent base because both subtypes report liveness.
- *TeamMember* constructor mirrors Agent's constructor — no additional properties at initialisation; the subtype adds only operational delta.
- *KanbanLead* constructor mirrors Agent's constructor; its orchestration operations are all deltas on top of the base agent lifecycle.
- *Skill* uses pre-defined instances from kanban.json stage work required — skills are loaded, not created by callers.
- *DeliveryRole* values are PRODUCT_OWNER, BUSINESS_EXPERT, UX_DESIGNER, ENGINEER.
- *SessionLifecycleState* values are CREATED, RUNNING, COMPLETED, FAILED; *AvatarState* values are ACTIVE and INACTIVE.
- *KanbanLead* and *KanbanBoard* are excluded as parameters from BootstrapPrompt.assembleFrom; they are caller-side collaborators declared in the domain model to establish where workspace path comes from.
- *AgentDefinition*, *BootstrapPrompt*, and *AgentOutputStream* are separated because each has a distinct lifecycle: definition is static per role, prompt is assembled once per session creation, and stream is continuous during a running session.
- isRunning() and agentIsLive() return the same predicate at this fidelity level — they are kept separate because they answer different questions for different callers; specialised rules may diverge in implementation.
- *RoleEngagement* is computed from live board state; engagedTicketCount is recomputed on each call.

---

# Boundary Domain

### **AgentStreamPanel**

------
outputStream: AgentOutputStream
anchoredStage: Stage
teamMember: TeamMember
isExpanded: Boolean
	Invariant: panel height matches the stage column height when expanded
----
anchor(TeamMember, Stage): void
expand(): void
collapse(): void

### references

**Ref — Domain Language: Agent and Skills KA**
Source: docs/domain/domain-language.md
Locator: Agent Stream Panel section
Extract: whole

### decisions made

- *AgentStreamPanel* is a UI display component — it has no domain behaviour beyond surfacing agent output beside its stage column; it does not participate in board flow or skill execution.
- The anchor(teamMember, stage) operation is placed here rather than on TeamMember or Stage because the panel is the actor that establishes its own layout position.
- Panels stacking side-by-side when multiple are open is a layout constraint enforced by the host UI container, not by the panel itself.

---
