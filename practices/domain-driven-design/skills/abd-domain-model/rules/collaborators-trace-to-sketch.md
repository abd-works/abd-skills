# Rule: Collaborators trace to sketch

**Scanner:** Manual review

A passing model only lists collaborators that trace to concepts in the Domain Language's behavior bullets or subtype edges. Domain-named types with distinct values are modeled as named classes, not reduced to primitives. A failing model invents collaborators with no UL backing or collapses domain types to primitives.

## DO

UL behavior for `KanbanLead`: "assigns agents to tickets based on skill match"

```markdown
### **KanbanLead**

----
assign(Ticket, Agent): Assignment
	Skill
```

`Skill` appears as a collaborator because the UL behavior mentions "skill match." Every collaborator traces to the UL.

## DO NOT

Inventing a collaborator:

```markdown
### **KanbanLead**

----
assign(Ticket, Agent): Assignment
	SkillMatcher         ← not in UL
	DatabaseConnection   ← infrastructure, not in UL
```

Reducing a domain type to a primitive:

```markdown
------
stageName: String    ← should be StageName
ticketId: String     ← should be TicketIdentifier
```

If `StageName` has distinct domain meaning, it must be a named type.

**Source:** Engagement convention (domain-model skill).
