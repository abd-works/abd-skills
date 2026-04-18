# Rule: Given describes state, not actions

**Given** steps state what is true **before** the behavior under test: preconditions and persisted state. The first thing that **happens** — a user gesture, system event, or command — belongs in **When**. **Then** captures observable outcomes (including errors). Do not hide the behavior under test inside **Given**.

## DO

- Phrase **Given** as state: the **User** is logged in, the **Account** is active, the **Entitlement** is granted.
- Move verbs like *clicks*, *invokes*, *submits* to **When**.
- When you need prior actions, express the **resulting state**, not the past action.

Plain example:
``Given the **User** *Jane Doe* is logged into ChannelOne 2.0
  And **Account** *Acme Operating* is *Active*
When the **User** *Jane Doe* submits a **Wire Payment**
Then the **Wire Payment** is marked as *successful*
``
## DON'T

- Use **Given** for UI navigation ("user is on Payment Details step") when you can state domain state.
- Put past-tense actions in **Given** ("user has clicked Continue").
- Describe the functionality you are trying to prove inside **Given** instead of **Then**.

``# WRONG
Given user clicks Pay
When payment succeeds

# BETTER
Given the **Wire Payment** is ready to authorize
When the **User** authorizes the **Wire Payment**
Then the **Wire Payment** status is *Authorized*
``