# Rule: Scenarios cover all cases implied by the story

A solid story has **happy path** scenarios plus **edge** and **error** cases that trace to **whatever specifies behavior**: formal acceptance criteria, story text, notes, or agreed rules. If validation, persistence, or error handling matters, scenarios should show those outcomes explicitly—not assume “we’ll handle errors somewhere.”

## DO

- Include at least one **success** path with realistic data.
- Add **boundary** or rule-adjacent cases when limits, optional fields, or transitions are stated (in AC, notes, or the story).
- Add **failure** paths with the observable error or prevention behavior (message, status, no persistence), using concrete example values.

```gherkin
Scenario: Valid payment amount is accepted
  When {User} enters {PaymentAmount}
  Then {WirePayment} holds {PaymentAmount}

Scenario: Negative amount is rejected
  When {User} enters {PaymentAmount}
  Then submission is blocked
  And {WirePayment} is not created
```

## DON'T

- Ship only “everything works” scenarios when negatives or edge rules are known from any source.
- Describe errors abstractly (“invalid data”) without the concrete violating example the table supplies.
