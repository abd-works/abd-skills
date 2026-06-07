# Rule: Explicit chain of responsibility

**Scanner:** Manual review

A passing model makes every actor in a behavioral chain visible — as a method parameter, return type, or indented collaborator. A failing model implies actors that never appear in the method signature or collaborator list, leaving responsibility gaps.

## DO

Behavior: "The lead assigns a ticket to an agent who then picks up work using a skill."

```markdown
### **KanbanLead**

----
assign(Ticket, Agent): Assignment
	Agent
	Ticket
```

```markdown
### **Agent**

----
pickUp(Assignment): WorkItem
	Skill
```

Every actor in the chain (KanbanLead, Agent, Ticket, Skill) is visible somewhere.

## DO NOT

```markdown
### **KanbanLead**

----
assign(Ticket): Assignment
```

Where is the Agent? The chain says "assigns to an agent" but Agent never appears as a parameter, return type, or collaborator. The actor is left implicit.

**Source:** Engagement convention (domain-model skill).
