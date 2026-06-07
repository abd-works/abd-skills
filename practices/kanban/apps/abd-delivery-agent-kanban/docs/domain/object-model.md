---
state: domain-model
---

# Module: [Delivery Agent Kanban]

Scope: How delivery work is modeled and tracked: the kanban board with its ordered stages and skills, tickets flowing through stages, skill progress determining board position, and agent roles pulling skill work.

---

# Core Domain

## **Kanban Board**

The Kanban Board owns the single source of truth for stage order, work required per stage, team configuration, and all tickets currently in flow. BoardPosition and SkillProgress are derived types that live here because they only have meaning relative to a ticket on the board.

### **KanbanBoard** << Entity >>

+ KanbanBoard(stages: List<Stage>, workspacePath: String, team: Team)
------
+ savedAt: String
+ workspacePath: String
+ << composition >> stages: List<Stage>
	Invariant: single source of truth for which skills each stage requires — each Stage carries its own StageWorkRequired; tickets never duplicate that list
+ << composition >> team: Team
----
+ defineStageOrder(orderedStageNames: List<String>): void
+ recordSaveTimestamp(): void
+ ticketsInFlow(): List<Ticket>
	Invariant: every ticket occupies exactly one stage at any given time
	Interaction:
		allTickets: List<Ticket> = stages.flatMap(stage: Stage => stage.allTickets())
		return allTickets
+ stageFor(ticket: Ticket): Stage
	Interaction:
		matchingStage: Stage = stages.first(stage: Stage => stage.contains(ticket: ticket))
		return matchingStage
+ nextStageFor(ticket: Ticket): Stage
	Invariant: returns the stage immediately after the ticket's current boardPosition in the ordered stages list
+ advanceCompletedTickets(): void
	Invariant: for each ticket in any stage's done bucket whose skills are all done — scatter into child tickets if next stage is finer scope, otherwise advance to next stage
	Interaction:
		for each stage in stages:
			for each ticket in stage.done where ticket.skillsDoneFor(stage.workRequired):
				nextStage: Stage = nextStageFor(ticket: ticket)
				childTickets: List<Ticket> = ticket.scatterIntoChildTickets(nextStage: nextStage)
				if childTickets is not empty: nextStage.enqueue each childTicket
				else: ticket.advanceToNextStage(nextStage: nextStage, team: team)
+ staleAgents(): List<TeamMember>
	Invariant: returns TeamMembers across all team memberships whose AgentSession has not produced output within the expected heartbeat window
	Interaction:
		allMembers: List<TeamMember> = team.memberships.values().flatMap(m: TeamMembership => m.pairs).flatMap(p: TeamMemberPair => [p.executor, p.reviewer])
		return allMembers.filter(tm: TeamMember => tm not null and not tm.currentSession.isRunning())

### **Ticket** << Entity >>

+ Ticket(id: String, lineage: List<String>, scopeLevel: String, priority: Integer)
------
+ id: String
+ lineage: List<String>
+ boardPosition: Stage
	Invariant: scopeLevel must match the scope declared by the current stage
+ scopeLevel: String
+ priority: Integer
+ << composition >> skillProgress: Dictionary<String, SkillProgress>
	Invariant: kanban board is single source of truth for which skills a stage requires — ticket never duplicates that list
+ notes: String
+ << composition >> stageTimestamps: Dictionary<String, StageTimestamp>
----
+ waitInStageDone(stage: Stage): void
	Interaction:
		stage.moveToDone(ticket: this)
+ advanceToNextStage(nextStage: Stage, team: Team): void
	Invariant: a ticket never advances to the next stage automatically — a team member must initiate advancement
	Interaction:
		nextStage.enqueue(ticket: this)
		enteredTimestamp: StageTimestamp = new StageTimestamp(enteredAt: currentIsoTimestamp())
		stageTimestamps.put(key: nextStage.name, value: enteredTimestamp)
		boardPosition = nextStage
+ scatterIntoChildTickets(nextStage: Stage): List<Ticket>
	Invariant: scatter only occurs when the next stage's scope level is finer than the current stage's scope level
	Interaction:
		scopeFiner: Boolean = isScopeFinerThan(nextScopeLevel: nextStage.scopeLevel, currentScopeLevel: this.scopeLevel)
		if not scopeFiner: return empty list
		childLineage: List<String> = lineage + [this.id]
		childTickets: List<Ticket> = new Ticket instances with lineage: childLineage and scopeLevel: nextStage.scopeLevel
		return childTickets
+ isBlocked(): Boolean
+ skillsDoneFor(stageWorkRequired: StageWorkRequired): Boolean
	Invariant: true only when every skill in stageWorkRequired has a SkillProgress entry with executionStatus DONE and reviewStatus DONE
	Interaction:
		requiredSkillNames: List<String> = stageWorkRequired.orderedSkills.map(skill: Skill => skill.name)
		allDone: Boolean = requiredSkillNames.all(name: String => skillProgress.get(name).isDone())
		return allDone
- isScopeFinerThan(nextScopeLevel: String, currentScopeLevel: String): Boolean
	Invariant: returns true when nextScopeLevel represents a narrower granularity than currentScopeLevel in the board's declared scope progression

### **BoardPosition** << ValueObject >>

Derived snapshot of a ticket's stage placement and work sub-state. Computed from the ticket's current stage and the aggregate execution state of its SkillProgress entries.

+ BoardPosition(currentStage: Stage, subState: SubState)
------
+ currentStage: Stage
+ subState: SubState
	Invariant: a ticket never advances to the next stage automatically — readiness is signalled, not acted upon automatically
----
+ isReadyToAdvance(): Boolean
	Invariant: true only when subState is DONE — all required skills have execution done and review done

### **SkillProgress** << Entity >>

Tracks the execution and review lifecycle of one skill on one ticket. Identity is meaningful — a specific agent is working a specific skill on a specific ticket.

+ SkillProgress(skillName: String, executingAgentRole: String, reviewingAgentRole: String)
------
+ skillName: String
+ executionStatus: ExecutionStatus
+ reviewStatus: ReviewStatus
+ executingAgentRole: String
+ reviewingAgentRole: String
+ executionStartedAt: String
+ executionCompletedAt: String
+ reviewStartedAt: String
+ reviewCompletedAt: String
----
+ startExecution(agent: Agent): void
	Invariant: transitions executionStatus to IN_PROGRESS; records executionStartedAt
+ completeExecution(): void
	Invariant: transitions executionStatus to DONE; records executionCompletedAt; execution must reach DONE before review status can leave NOT_STARTED
+ startReview(agent: Agent): void
	Invariant: may only be called when executionStatus is DONE; transitions reviewStatus to IN_PROGRESS; records reviewStartedAt
+ completeReview(): void
	Invariant: transitions reviewStatus to DONE; records reviewCompletedAt
+ failReview(): void
	Invariant: transitions reviewStatus to FAILED
+ isDone(): Boolean
	Invariant: true only when executionStatus is DONE and reviewStatus is DONE

### **Stage** << Entity >>

+ Stage(name: String, scopeLevel: String, workRequired: StageWorkRequired)
------
+ name: String
+ scopeLevel: String
+ << composition >> workRequired: StageWorkRequired
+ << aggregation >> queue: List<Ticket>
+ << aggregation >> inProgress: List<Ticket>
+ << aggregation >> done: List<Ticket>
----
+ enqueue(ticket: Ticket): void
	Invariant: a ticket cannot skip a stage or move backward — ticket must have been in done of the prior stage before being enqueued here
+ moveToInProgress(ticket: Ticket): void
+ moveToDone(ticket: Ticket): void
+ allTickets(): List<Ticket>
	Interaction:
		return queue + inProgress + done
+ contains(ticket: Ticket): Boolean

### **StageWorkRequired** << ValueObject >>

+ StageWorkRequired(orderedSkills: List<Skill>, agentRoles: Dictionary<String, String>)
------
+ << composition >> orderedSkills: List<Skill>
+ agentRoles: Dictionary<String, String>
	Invariant: every skill in orderedSkills has an entry in agentRoles mapping to a delivery role
----
+ roleFor(skill: Skill): String
	Invariant: returns the delivery role assigned to perform the given skill at this stage

### **StageTimestamp** << ValueObject >>

Immutable record of when a ticket entered and completed a stage. Extracted from the Ticket's "stage timestamps" responsibility to carry both timestamps as a typed pair.

+ StageTimestamp(enteredAt: String)
------
+ enteredAt: String
+ completedAt: String

### **Team** << Entity >>

+ Team(memberships: Dictionary<DeliveryRole, TeamMembership>)
------
+ << composition >> memberships: Dictionary<DeliveryRole, TeamMembership>
	Invariant: one TeamMembership per delivery role
----
+ incrementPairCount(role: DeliveryRole): void
	Interaction:
		membership: TeamMembership = memberships.get(role)
		membership.incrementPairCount()
+ decrementPairCount(role: DeliveryRole): void
	Invariant: result must remain non-negative
	Interaction:
		membership: TeamMembership = memberships.get(role)
		membership.decrementPairCount()

### **TeamMembership** << Entity >>

The configured collection of executor+reviewer pairs for one delivery role. Each pair is one executor slot and one reviewer slot of the same role. KanbanLead instantiates TeamMember agents to fill unfilled pairs.

+ TeamMembership(role: DeliveryRole, pairCount: Integer)
------
+ role: DeliveryRole
+ pairCount: Integer
	Invariant: must be non-negative; defaults to 1 when not explicitly configured
+ << composition >> pairs: List<TeamMemberPair>
----
+ incrementPairCount(): void
	Invariant: adds one new unfilled TeamMemberPair to pairs
+ decrementPairCount(): void
	Invariant: pairCount must remain non-negative; removes the last unfilled pair
+ unstaffedPairs(): List<TeamMemberPair>
	Invariant: returns pairs where isFullyStaffed() is false — KanbanLead uses this to know which pairs need agents spawned

### **TeamMemberPair** << Entity >>

An executor TeamMember and a reviewer TeamMember of the same delivery role, held together as a pair.

+ TeamMemberPair(role: DeliveryRole)
------
+ role: DeliveryRole
+ executor: TeamMember
+ reviewer: TeamMember
----
+ isFullyStaffed(): Boolean
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

- *KanbanBoard* receives `workspacePath` as a constructor property because `BootstrapPrompt` requires it at session creation time and the domain model declares it as coming from board config; it has no separate domain model responsibility line but is a necessary typed surface for the `KanbanLead` → `BootstrapPrompt` collaboration.
- *StageWorkRequired* is owned by `Stage`, not by `KanbanBoard` — work required changes per column (stage), so it belongs on the thing that changes with it. The board is still the single source of truth because it owns the stages; tickets navigate to work required through their current stage.
- *Team* is a composition on KanbanBoard — Team's lifecycle is fully contained within a board configuration; it has no standalone existence independent of the board that owns it.
- *StageTimestamp* is a typed pair extracted from the Ticket's "stage timestamps" domain model responsibility; it carries no domain model card of its own but earns a class because both enteredAt and completedAt must travel together as a named unit.
- *SubState* values are `IN_PROGRESS` and `DONE`; *ExecutionStatus* values are `NOT_STARTED`, `IN_PROGRESS`, `DONE`; *ReviewStatus* values are `NOT_STARTED`, `IN_PROGRESS`, `DONE`, `FAILED`; *WorkRole* values are `EXECUTOR` and `REVIEWER` — all are constrained enumerations on their owning classes.
- *Team* is an indirect collaborator in `Ticket.advanceToNextStage` (from domain model); KanbanLead extracts the relevant team configuration before calling this operation and passes Team as the authoritative configuration context. Team is not directly queried inside the Ticket — it is in the signature to honour the domain model declaration.
- *BoardPosition* is a ValueObject and not a property stored on Ticket — it is computed on demand from the Ticket's boardPosition (Stage) and the aggregate state of its SkillProgress entries. TeamMember creates a BoardPosition when it advances a ticket to in-progress.
- *Scatter* produces child Ticket instances whose lineage includes the parent's id; the KanbanLead triggers the operation.

---

# Core Domain

## **Agent and Skills**

Agent is the base class for all role agents. KanbanLead and TeamMember extend it with their specific orchestration and execution responsibilities respectively.

### **Agent** << Entity >>

+ Agent(deliveryRole: DeliveryRole, workRole: WorkRole, agentDefinition: AgentDefinition)
------
+ deliveryRole: DeliveryRole
+ workRole: WorkRole
+ agentDefinition: AgentDefinition
----
+ readAgentDefinition(agentDefinition: AgentDefinition): void
+ createAgentSession(bootstrapPrompt: BootstrapPrompt): AgentSession
	Invariant: agent lifecycle managed by Cursor SDK sessions, not file-based heartbeats
+ startWorkOnSkill(skill: Skill, ticket: Ticket): SkillProgress
	Invariant: agent may only start work on skills that require its delivery role
+ driveSkillToDone(skillProgress: SkillProgress): void
+ writeHeartbeat(): Heartbeat

### **TeamMember : Agent** << Entity >>

+ TeamMember(deliveryRole: DeliveryRole, workRole: WorkRole, agentDefinition: AgentDefinition)
------
----
+ advanceTicketToInProgress(ticket: Ticket): BoardPosition
	Invariant: only triggers on the first skill start — no-op when any SkillProgress entry is already IN_PROGRESS or DONE
	Interaction:
		firstStart: Boolean = ticket.skillProgress.values().all(sp: SkillProgress => sp.executionStatus == NOT_STARTED)
		if not firstStart: return existing boardPosition
		boardPosition: BoardPosition = new BoardPosition(currentStage: ticket.boardPosition, subState: IN_PROGRESS)
		return boardPosition
+ persistSkillCompletion(kanbanBoard: KanbanBoard, skillProgress: SkillProgress): void
	Invariant: writes updated skillProgress state to the kanban board's persistent store
+ completeTicket(ticket: Ticket, stage: Stage): void
	Invariant: a team member agent only executes skills that match its delivery role; ticket is moved to stage.done when all skills are done

### **KanbanLead : Agent** << Entity >>

+ KanbanLead(deliveryRole: DeliveryRole, workRole: WorkRole, agentDefinition: AgentDefinition)
------
----
+ monitorHeartbeats(agents: List<Agent>): List<Heartbeat>
+ pullTicketsFromBacklog(stage: Stage): List<Ticket>
+ startTeamMemberAgent(pair: TeamMemberPair, workRole: WorkRole): AgentSession
+ stopTeamMemberAgent(session: AgentSession): void
+ restartStaleAgent(teamMember: TeamMember): AgentSession
	Invariant: stale session is stopped before a new session is created for the same pair
	Interaction:
		stopTeamMemberAgent(session: teamMember.currentSession)
		newSession: AgentSession = startTeamMemberAgent(pair: teamMember.pair, workRole: teamMember.workRole)
		return newSession
+ dispatchSkillToIdleTeamMember(teamMember: TeamMember, ticket: Ticket, skill: Skill): void
+ runScanCycle(kanbanBoard: KanbanBoard): void
	Invariant: one pass — board advances or scatters completed tickets; lead staffs empty pairs and restarts stale agents
	Interaction:
		kanbanBoard.advanceCompletedTickets()
		unstaffedPairs: List<TeamMemberPair> = kanbanBoard.team.memberships.values().flatMap(m => m.unstaffedPairs())
		for each pair in unstaffedPairs: startTeamMemberAgent(pair: pair, workRole: next unstaffed workRole)
		staleMembers: List<TeamMember> = kanbanBoard.staleAgents()
		for each teamMember in staleMembers: restartStaleAgent(teamMember: teamMember)

### **Skill** << ValueObject >>

Initialisation: pre-defined instances created from kanban.json stage work required; not constructed at runtime.
------
+ name: String
+ performedByRole: String

### **Heartbeat** << ValueObject >>

Initialisation: derived on demand from an AgentSession's lifecycle state; not stored independently.
------
+ session: AgentSession
+ poolAvatarState: AvatarState
	Invariant: pool avatar inactive only when session is not running and agent role has zero board engagement
----
+ determineLiveness(agent: Agent, ticket: Ticket): Boolean
	Interaction:
		sessionLive: Boolean = session.isRunning()
		boardEngaged: Boolean = agentRoleHasBoardEngagement(agent: agent, ticket: ticket)
		liveness: Boolean = sessionLive || boardEngaged
		return liveness
- agentRoleHasBoardEngagement(agent: Agent, ticket: Ticket): Boolean
	Invariant: true when any active ticket has a SkillProgress entry with the agent's deliveryRole as executingAgentRole or reviewingAgentRole in a non-DONE execution state

### **RoleEngagement** << ValueObject >>

Initialisation: computed from live work or display focus; not stored independently.
------
+ role: String
+ engagedTicketCount: Integer
	Invariant: derived from live work or display focus, not stored independently
----
+ countEngagedTickets(tickets: List<Ticket>, agent: Agent): Integer
	Interaction:
		engagedTickets: List<Ticket> = tickets filtered to those with a SkillProgress entry where executingAgentRole or reviewingAgentRole matches agent.deliveryRole and executionStatus is not DONE
		engagedTicketCount = engagedTickets.size()
		return engagedTicketCount

### **AgentSession** << Entity >>

+ AgentSession(sessionId: String, agentRole: String)
------
+ sessionId: String
+ agentRole: String
+ lifecycleState: SessionLifecycleState
	Invariant: one active session per agent slot at any time — a role with two executor slots and one reviewer slot may have at most three concurrent sessions
+ << composition >> outputStream: AgentOutputStream
----
+ isRunning(): Boolean
	Invariant: true only when lifecycleState is RUNNING
+ agentIsLive(): Boolean
	Invariant: true only when lifecycleState is RUNNING

### **AgentDefinition** << ValueObject >>

Initialisation: loaded from file system at agents/{role}/AGENT.md; one definition per delivery role.
------
+ role: String
+ rootFilePath: String
	Invariant: every agent role has exactly one AGENT.md root file at agents/{role}/AGENT.md
+ sharedWorkflowFiles: List<String>
+ rolePlaybookPath: String
	Invariant: skills each role can execute come from kanban.json stage work required, not from this definition

### **BootstrapPrompt** << ValueObject >>

Initialisation: assembled via the assembleFrom factory method by KanbanLead at session creation time.
------
+ workspacePath: String
	Invariant: workspace path injected from KanbanBoard by KanbanLead, never sourced from AgentDefinition
+ roleIdentity: String
+ promptContent: String
	Invariant: must contain workspace and role identity before being passed to createAgentSession
----
+ assembleFrom(agentDefinition: AgentDefinition, workspacePath: String): BootstrapPrompt
	Invariant: KanbanLead is the exclusive caller; it extracts workspacePath from KanbanBoard before passing it here — KanbanBoard and KanbanLead are caller-side collaborators, not parameters
	Interaction:
		roleIdentity: String = agentDefinition.role
		promptContent: String = agentDefinition.rootFilePath + roleIdentity + workspacePath assembled into initialization prompt
		bootstrapPrompt: BootstrapPrompt = new BootstrapPrompt(workspacePath: workspacePath, roleIdentity: roleIdentity, promptContent: promptContent)
		return bootstrapPrompt

### **AgentOutputStream** << Entity >>

+ AgentOutputStream(sessionId: String)
------
+ sessionId: String
+ << composition >> messages: List<String>
----
+ deliverMessage(message: String): void
+ messageHistory(): List<String>

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

- *Agent* is an abstract base class — it is never instantiated directly; all concrete agents are either a TeamMember or a KanbanLead. `writeHeartbeat()` remains on Agent base because both subtypes report liveness, though the implementation derives from AgentSession state not files.
- *TeamMember* constructor mirrors Agent's constructor — no additional properties are introduced at initialisation; the subtype adds only operational delta.
- *KanbanLead* constructor mirrors Agent's constructor; its orchestration operations are all deltas on top of the base agent lifecycle.
- *Skill* uses pre-defined instances rather than runtime construction — skills are defined in kanban.json stage work required and loaded, not created by callers.
- *DeliveryRole* values are `PRODUCT_OWNER`, `BUSINESS_EXPERT`, `UX_DESIGNER`, `ENGINEER` — used as the key type on `Team.memberships` and as the typed identity of every agent.
- *SessionLifecycleState* values are `CREATED`, `RUNNING`, `COMPLETED`, `FAILED`; *AvatarState* values are `ACTIVE` and `INACTIVE`.
- *KanbanLead* and *KanbanBoard* are excluded as parameters from `BootstrapPrompt.assembleFrom`; they are caller-side collaborators declared in the domain model to establish where workspace path comes from — the typed model reflects this by declaring the invariant rather than coupling BootstrapPrompt to the KanbanLead/Board types.
- *AgentDefinition*, *BootstrapPrompt*, and *AgentOutputStream* are separated because each has a distinct lifecycle: definition is static per role, prompt is assembled once per session creation, and stream is continuous during a running session.
- `isRunning()` and `agentIsLive()` return the same predicate at this fidelity level — they are kept separate because they answer different questions for different callers (heartbeat vs. lead monitoring); specialised rules may diverge in implementation.
- *RoleEngagement* is computed from live board state and display focus; `engagedTicketCount` is not stored between calls — each call to `countEngagedTickets` recomputes it.

---

# Boundary Domain

### **AgentStreamPanel** << Boundary >>

Initialisation: created by the UI when a TeamMember avatar is clicked; layout is determined by the count of currently open panels.
------
+ outputStream: AgentOutputStream
+ anchoredStage: Stage
+ teamMember: TeamMember
+ isExpanded: Boolean
	Invariant: panel height matches the stage column height when expanded
----
+ anchor(teamMember: TeamMember, stage: Stage): void
+ expand(): void
+ collapse(): void

### references

**Ref — Domain Language: Agent and Skills KA**
Source: docs/domain/domain-language.md
Locator: Agent Stream Panel section
Extract: whole

### decisions made

- *AgentStreamPanel* is placed in the Boundary Domain because it is a UI display component — it has no domain behaviour beyond surfacing agent output beside its stage column; it does not participate in board flow or skill execution.
- The `anchor(teamMember, stage)` operation is placed here rather than on TeamMember or Stage because the panel is the actor that establishes its own layout position — consistent with the receiver-not-responsible-for-receiving rule.
- Panels stacking side-by-side when multiple are open is a layout constraint enforced by the host UI container, not by the panel itself; it is captured as an invariant on `isExpanded` rather than as an operation.
