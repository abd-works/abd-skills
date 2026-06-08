# Rule: Invariants from business logic

**Scanner:** Manual review

A passing model states invariants that express business rules — constraints that a domain expert would recognize and validate. A failing model states implementation invariants — null checks, type guards, or technical constraints that belong in code, not in the domain model.

## DO

```markdown
------
balance: Money
	Invariant: balance must not go negative
----
withdraw(Money): Account
	Invariant: withdrawal cannot exceed available balance
advance(Stage): Ticket
	Invariant: cannot advance past final stage
assign(Agent): Assignment
	Invariant: agent must hold required skill
```

Each invariant is a business rule a domain expert would state.

## DO NOT

```markdown
------
name: TicketTitle
	Invariant: must not be null
	Invariant: must be a valid string
----
advance(Stage): Ticket
	Invariant: stage parameter must not be undefined
	Invariant: must be called on an initialized instance
```

"Must not be null," "must be a valid string," and "must not be undefined" are implementation checks. They tell you nothing about the business domain.

**Source:** Engagement convention (domain-model skill).
