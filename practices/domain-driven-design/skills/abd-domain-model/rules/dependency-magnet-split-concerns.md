# Rule: Dependency magnet — split concerns

**Scanner:** Manual review

A passing model keeps each class focused, with no more than 5–7 distinct collaborator types across its methods. A failing model has a class that collaborates with too many types — a dependency magnet signaling mixed concerns that should be split into focused classes.

## DO

Split a bloated class into focused ones:

```markdown
### **TicketRouter**

----
route(Ticket, Stage): Stage
	StageBucketLayout
	WipPolicy

### **TicketAssigner**

----
assign(Ticket, Agent): Assignment
	AgentCapability
	Skill

### **TicketTracker**

----
track(Ticket): TicketHistory
	TicketEvent
```

Each class has 2–3 collaborators and one clear concern.

## DO NOT

```markdown
### **BoardManager**

----
route(Ticket, Stage): Stage
	StageBucketLayout
	WipPolicy
assign(Ticket, Agent): Assignment
	AgentCapability
	Skill
track(Ticket): TicketHistory
	TicketEvent
notify(Agent): Notification
	NotificationChannel
	Template
validate(Ticket): ValidationResult
	Rule
	RuleSet
```

Eight distinct collaborator types. This class is a dependency magnet — it routes, assigns, tracks, notifies, and validates. Split into focused classes.

**Source:** Engagement convention (domain-model skill).
