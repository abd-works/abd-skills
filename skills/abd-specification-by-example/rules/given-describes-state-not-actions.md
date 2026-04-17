# Rule: Given describes state, not actions

**Given** steps state **what is true before** the behavior under test: preconditions and persisted state. The **first** thing that **happens**—a user gesture, system event, or command—belongs in **When**. **Then** captures observable outcomes (including errors). Do not hide the behavior under test inside **Given**.

## DO

- Phrase **Given** as state: “**{User}** is logged in”, “**{Character}** exists”, “workflow state is persisted”.
- Move verbs like *clicks*, *invokes*, *submits*, *calls* to **When**.
- When you need prior actions, express the **resulting state**, not the past action (“**{WirePayment}** creation is in progress”, not “user has clicked Continue”).

```gherkin
Given {Agent} is initialized
And {Project} is finished initializing
When {Tool} invokes load_project
Then {Project} loads configuration
```

## DON'T

- Use **Given** for UI navigation position (“user is on Payment Details step”) when you can state **domain** state (“**{PaymentDetails}** requires **{Account}** selection”).
- Put past-tense **actions** in **Given** (“Tool has invoked method”, “user has clicked”).
- Describe the functionality you are trying to prove inside **Given** instead of **Then**.

```gherkin
# WRONG
Given user clicks Pay
When payment succeeds

# BETTER
Given {Payment} is ready to authorize
When user authorizes {Payment}
Then {Payment} status is Authorized
```
