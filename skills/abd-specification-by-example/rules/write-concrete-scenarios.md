# Rule: Write concrete, parameterized scenarios

Steps should read as **examples**, not abstracts: use **{Concept}** for domain objects and **{Concept.property}** for salient attributes. **Mention the domain concept in prose beside each placeholder** (e.g. `the User {User}`) so steps read naturally and still map to tables — see **Mention the domain concept beside the placeholder**. Every placeholder must appear in an **example table**; tables use domain column names. Work **backward** from the outcome to the base data the world needs (enterprise, user, entitlements, accounts). Relate concepts with collaboration language (“the **Wire Payment {WirePayment}** holds the **Payment Amount {PaymentAmount}**”), not jammed placeholders.

## DO

- Replace vague actors with **{User}**, **{Enterprise}**, **{PaymentAmount}**, each backed by a table, and label each brace with the matching domain term in the same step.
- Trace dependencies: e.g. payment needs account, account needs enterprise, user needs entitlements—show those tables.
- Prefer domain collaboration verbs from the model (holds, belongs to, validates against).

```gherkin
Given the User {User} is logged into ChannelOne 2.0
And the User {User} is entitled to the Entitlement {Entitlement}
When the User {User} enters a Payment Amount {PaymentAmount}
Then the Wire Payment {WirePayment} holds the Payment Amount {PaymentAmount}
```

```text
PaymentAmount:
| amount   | currency | formatted_display |
| 10000.00 | USD      | $10,000.00        |
```

## DON'T

- Hard-code literals in steps when the scenario system expects **{Concept}** + tables (“User Jane Doe…” without a **User** table).
- Invent generic placeholders (`<the_user>`, `{some_value}`) instead of type names from the domain.
- Stuff two unrelated placeholders next to each other without an English relation (“**{Enterprise}** **{User}** is logged in”).
- Describe **UI state** as **Given** when **data state** suffices (“on Payment Details step” vs “**{PaymentDetails}** awaits **{Account}**”).
- Use calculated fields (counts only) to stand in for the **records** that produce them when this scenario is the one doing the calculation.

```gherkin
# WRONG — no parameterization / tables
Given user enters $10,000.00

# BETTER
Given the User {User} enters a Payment Amount {PaymentAmount}
```
