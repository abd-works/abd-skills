# Rule: Invariants present for lifecycle

**Scanner:** Manual review

A passing model declares at least one invariant for every concept that has lifecycle state transitions. The invariant constrains which transitions are valid. A failing model has state-changing methods with no invariants — allowing unconstrained state changes.

## DO

```markdown
### **Ticket**

Ticket(TicketTitle, Stage)
------
currentStage: Stage
	Invariant: stage transitions follow stage order
----
advance(Stage): Ticket
	Invariant: cannot advance past final stage
block(BlockReason): Ticket
	Invariant: blocked ticket cannot advance
unblock(): Ticket
	Invariant: only blocked tickets can be unblocked
```

Every state-changing method has at least one invariant constraining the transition.

## DO NOT

```markdown
### **Ticket**

Ticket(TicketTitle, Stage)
------
currentStage: Stage
----
advance(Stage): Ticket
block(BlockReason): Ticket
unblock(): Ticket
```

Three state-changing methods and zero invariants. Can a blocked ticket advance? Can you unblock a ticket that is not blocked? Can you advance past the final stage? The model does not say.

**Source:** Engagement convention (domain-model skill).
