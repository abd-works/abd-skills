# Rule: Map table columns to scenario parameters

Every **{Concept}** in Background and scenario steps must have a matching **example table**, and every example table must appear as **{Concept}** (or **{Concept.property}**) in the steps. In prose, put the **domain concept name beside** each placeholder (e.g. `the Entitlement {Entitlement}`) so the tie to the table is obvious in human-readable specs — see **Mention the domain concept beside the placeholder**. Verification columns belong in **Then** via **{Concept.property}** or explicit domain outcomes—keep **Given** tables aligned with preconditions only.

## DO

- Work **both directions**: step placeholder ↔ table name ↔ columns ↔ readable label next to the brace.
- Use **{Concept.property}** when a column is specifically asserted (e.g. `{Recipient.status}` is Active).
- Keep tables **minimal**: only concepts and attributes the scenario actually needs.

```gherkin
Given the User {User} is entitled to the Entitlement {Entitlement}
```

```text
User:
| user_name | user_role     |
| Jane Doe  | Wire Operator |

Entitlement:
| entitlement_name   | entitlement_status |
| WirePayment.Create | Granted              |
```

## DON'T

- Use angle-bracket **`<column_name>`** placeholders in prose instead of **{Concept}**.
- Leave **orphan** tables (no **{Concept}** in steps) or **{Concept}** placeholders with no table.
- Dump raw column names into a step without tying them to a concept (“User `<user_name>`”).

```gherkin
# WRONG
Given User <user_name> is logged in

# CORRECT
Given the User {User} is logged in
```
