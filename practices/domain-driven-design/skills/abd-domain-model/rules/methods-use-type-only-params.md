# Rule: Methods use type-only params

**Scanner:** Manual review

A passing model uses types only in method parameter lists: `methodName(Type, Type): ReturnType`. No parameter names appear. The property name on the type's own class communicates the role. A failing model includes parameter names in method signatures.

## DO

```markdown
----
assign(Ticket, Agent): Assignment
advance(Stage): Ticket
score(Evidence): Score
create(TicketTitle, Stage): Ticket
```

Types only. The role is understood from context and from the type's own properties.

## DO NOT

```markdown
----
assign(ticket: Ticket, agent: Agent): Assignment
advance(targetStage: Stage): Ticket
score(submittedEvidence: Evidence): Score
create(title: TicketTitle, initialStage: Stage): Ticket
```

Parameter names (`ticket:`, `agent:`, `targetStage:`, `submittedEvidence:`, `title:`, `initialStage:`) add noise. The domain-model format is type-only.

**Source:** Engagement convention (domain-model skill).
