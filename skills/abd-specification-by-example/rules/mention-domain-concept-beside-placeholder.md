# Rule: Mention the domain concept beside the placeholder

In **Background** and **scenario** steps, put the **readable domain concept name** (the word or phrase stakeholders use) **next to** each **`{Concept}`** or **`{Concept.property}`** placeholder. Readers should see *what* the brace refers to without decoding braces alone; the placeholder still ties the line to the **example table** for that concept.

## DO

- Use a short English cue before or after the brace: e.g. `the User {User}`, `the Entitlement {Entitlement}`, `the Enterprise {Enterprise}`, `activation status {Account.activation_status}`, `Payment Amount {PaymentAmount}`.
- Keep **one** `{Concept}` per table-backed object in that clause; the prose name should match the **table title** / domain type (singular or phrasing your team uses consistently).
- Apply the same pattern in **Background** (Given/And only) and in **scenario** steps (Given/When/Then/And).

```gherkin
Background:
  Given the User {User} is logged into ChannelOne 2.0
  And the User {User} is entitled to the Entitlement {Entitlement} for the Enterprise {Enterprise}
  And the Enterprise {Enterprise} has wire service enabled

Scenario: Wire capture
  Given the Account {Account} with activation status {Account.activation_status} is selected
  When the User {User} enters a Payment Amount {PaymentAmount}
  Then the Wire Payment {WirePayment} holds the Payment Amount {PaymentAmount}
```

## DON'T

- Use **only** `{User}` with no surrounding domain words — unless your pipeline forbids extra words (default: prefer the paired pattern above).
- Repeat the brace twice in a clumsy way (`{User} User …`) — use **one** natural phrase: `the User {User}` or `User {User}`, not both duplicated back-to-back.
- Replace `{Concept}` with **only** the English name and drop the placeholder — you still need the brace for table mapping unless your tool explicitly uses another convention.
