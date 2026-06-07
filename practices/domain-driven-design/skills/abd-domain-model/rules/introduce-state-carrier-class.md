# Rule: Introduce state-carrier class

**Scanner:** Manual review

A passing model introduces a separate state-carrier class when applying a concept to an entity requires per-application state. The concept stays clean, the entity stays clean, and the relationship state lives on the carrier. A failing model adds per-application state to either the concept or the entity.

## DO

An Agent applies a Skill to a Ticket. The application has per-instance state (progress, started time, outcome):

```markdown
### **SkillExecution**

SkillExecution(Agent, Skill, Ticket)
------
agent: Agent
skill: Skill
ticket: Ticket
progress: ExecutionProgress
	Invariant: progress only moves forward
----
complete(Outcome): SkillExecution
	Invariant: cannot complete an already-completed execution
```

The per-application state lives on `SkillExecution`, not on `Agent`, `Skill`, or `Ticket`.

## DO NOT

Adding per-application state to the concept:

```markdown
### **Skill**

------
currentAgent: Agent          ← per-application state polluting the concept
currentProgress: Progress    ← per-application state polluting the concept
```

Or to the entity:

```markdown
### **Agent**

------
currentSkillProgress: Progress   ← per-application state polluting the entity
activeTicket: Ticket             ← per-application state polluting the entity
```

**Source:** Engagement convention (domain-model skill).
