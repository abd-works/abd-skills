# Rule: Background vs scenario setup

**Background** is shared **precondition** text for **three or more** scenarios. It contains only **Given** / **And** lines (state), never **When** or **Then**. Steps use **{Concept}** (and **{Concept.property}** when a specific attribute matters) so each placeholder resolves to an example table. **Put the domain concept words beside each placeholder** (e.g. `the User {User}`) in Background and scenarios — see **Mention the domain concept beside the placeholder**. Do not repeat Background lines inside individual scenarios.

## DO

- Model shared state once in **Background** when many scenarios need the same starting world (e.g. logged-in **User {User}**, **Entitlement {Entitlement}**, **Enterprise {Enterprise}**).
- Use **{Concept.property}** when the scenario hinges on a particular field (e.g. `activation status {Account.activation_status}`).
- Keep Background free of actions; the **first** behavior under test belongs in **When** inside each scenario.

```gherkin
Background:
  Given the User {User} is logged into ChannelOne 2.0
  And the User {User} is entitled to the Entitlement {Entitlement} for the Enterprise {Enterprise}
  And the Enterprise {Enterprise} has wire service enabled
```

## DON'T

- Put **When** / **Then** in Background, or encode actions as “user logs in” inside Background **Given** lines.
- Hard-code identities or permissions inline when the scenario system expects **{Concept}** + tables (avoid “user is entitled to create wire payments” without **{Entitlement}**).
- Duplicate a Background **Given** inside a scenario’s steps.

```gherkin
# WRONG — action in Background
Background:
  When {User} logs in

# WRONG — repeats Background
Scenario: Pay wire
  Given {User} is logged into ChannelOne 2.0
  When ...
```
