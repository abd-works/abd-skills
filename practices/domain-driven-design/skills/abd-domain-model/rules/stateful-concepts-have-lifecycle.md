# Rule: Stateful concepts have lifecycle

**Scanner:** Manual review

A passing model declares — for every concept with mutable state — how it is created (constructor), how its state changes (methods), and what constraints hold across transitions (invariants). A failing model has stateful concepts with no constructor, no mutation methods, or no invariants constraining transitions.

## DO

```markdown
### **Ticket**

Ticket(TicketTitle, Stage)
------
title: TicketTitle
currentStage: Stage
	Invariant: stage transitions follow stage order
----
advance(Stage): Ticket
	Invariant: cannot advance past final stage
block(BlockReason): Ticket
	Invariant: blocked ticket cannot advance
```

Creation (constructor), state change (advance, block), and constraints (stage order, cannot advance past final, blocked cannot advance) are all explicit.

## DO NOT

A stateful concept with no lifecycle declaration:

```markdown
### **Ticket**

------
title: TicketTitle
currentStage: Stage
----
getTitle(): TicketTitle
```

No constructor shows how it is born. No mutation method shows how state changes. No invariant constrains transitions. The lifecycle is invisible.

**Source:** Engagement convention (domain-model skill).
