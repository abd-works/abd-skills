# Specification by example (BDD scenarios)

<!-- Conventions aligned with agile_bots story_bot `behaviors/scenarios`. -->

For a **story**, define a linear set of steps using GIVEN/WHEN/THEN/BUT. Where it makes sense groups steps in **scenarios**, with a minimum of one scenaario per story (eg: Main Flow). Scenario steps must be associated with one or more **Examples**.  **Examples** may apply to one or more steps, scenarios, or even stories. Place examples at the appropriate level based on scope. 

Senarios may use a common **Background**, and/or **Scenario Outline** sections when data variations matter.

**Sources:** When working with  stories that already have **acceptance criteria** start by taking a subset of the acceptance criteria that represent the main flow,  add *Given* statements and *Examples* as necessary to make it a full scenario, then incorporate remaining acceptance criteria in additional scenarios. (eg failure cases, edge cases, diffrent flows). you will not always get a 1-1 mapping between *acceptance criteria* statements and *spec-by-example* scenario statements, but the relationship should be obvious.

## Story: `Verb–Noun Title`

**Story type:** user | system | technical

**Sources / context:** _(e.g. pointer to original context, chpater, page, para number, from conversation / general understanding”)_

---

## Background

_Use only when **three or more** scenarios share the same setup. **Given** and **And** only — no **When** / **Then**. Use **{Concept}** placeholders that tie to example tables (not hard-coded actors or values in the step text)._

```gherkin
Background:
  Given a User {user_name} is logged into ChannelOne 2.0
  And that User {user_namr} is representing an Enterprise {Enterprise} with the role {user_role}
  And that Enterprise {enterprise_name} has the {payment_service} enabled
  And that User is entitled to the Entitlement {entitlement_name} with a status of {entitlement_status}

```

---

## Example tables

_For every **{Concept}** in Background/steps (and in any **Scenario Outline** that uses **{Concept}** placeholders), provide a table whose **name** is the domain concept. In step prose, **put that concept’s words beside the brace** (e.g. `the User {User}`, `the Entitlement {Entitlement}`) so examples read naturally and still map to tables. Columns are **domain attributes** (not UI widgets, not arbitrary `<column>` placeholders in step prose). Prefer **{Concept.property}** in steps when a specific attribute is under test. Omit implementation-only ID columns unless a technical story requires them. Order tables so dependencies read naturally (e.g. *Enterprise* before *Account* it owns)._

**Enterprise:**

| enterprise_name | payment_service      |
|-----------------|----------------------|
| Acme Corp       | wire                 |

**User:**

| user_name | user_role     |
|-----------|---------------|
| Jane Doe  | Wire Operator |

**Entitlement (assigned entitlements for wire functions):**

| entitlement_name   | entitlement_status |
|--------------------|----------------------|
| WirePayment.Create | Granted              |

**Account (owned by enterprise):**

| enterprise_name | account_name | activation_status |
|-----------------|------------------|-------------------|
| Acme Corp       | Acme Operating   | Active            |

**PaymentAmount:**

| amount   | currency | formatted_display |
|----------|----------|-------------------|
| 10000.00 | USD      | $10,000.00        |

**WirePayment (outcome state asserted in Then):**

| status |
|---------|
| pending |

**TransactionalLimit:**

| limit_name | max_amount | currency |
|------------|------------|----------|
| daily_wire | 500000.00  | USD      |

**PaymentInstrument (Scenario Outline data — same rows as the outline’s Examples):**

| instrument    | fee_rate |
|-----------------|----------|
| credit_card     | 2.9%     |
| bank_transfer   | 0.5%     |

---

## Scenarios

### Scenario: `Short outcome-oriented name`

```gherkin
Given the Account {Account} with activation status {Account.activation_status} is selected
When the User {User} enters a Payment Amount {PaymentAmount}
Then the Wire Payment {WirePayment} holds the Payment Amount {PaymentAmount}
And the Payment Amount {PaymentAmount} is validated against the Transactional Limit {TransactionalLimit}
```

### Scenario Outline: `Same behavior, varying data` _(only when outline is warranted)_

_Use a **Scenario Outline** when the **same** steps apply across multiple rows (calculations, boundary checks, or named entity variations). Do **not** use an outline for a single row or for materially different business setups — use separate **Scenario**s instead._

```gherkin
Scenario Outline: Fees depend on payment instrument
  Given the Payment Instrument {PaymentInstrument} is "<instrument>"
  When fee schedule is applied
  Then fee rate is "<fee_rate>"

  Examples:
    | instrument    | fee_rate |
    | credit_card   | 2.9%     |
    | bank_transfer | 0.5%     |
```

---

<!-- Notation below is for skill/template maintainers. Agents MUST NOT copy this section into generated project files. -->

## Instructions (template reference only — omit from generated files)

- **Given** = **state / preconditions** only; the **first action** is **When**. **Then** asserts observable outcomes (domain effects, not green checkmarks unless literal UI copy is the contract).
- **Language:** domain nouns and collaboration verbs from the model — not “the user clicks the dropdown”.
- **Domain emphasis (Markdown):** in `.md` outputs, wrap domain-significant terms in *italics* with *Title Case* for multi-word concepts — same convention as **abd-acceptance-criteria** (and **emphasize-domain-significant-terms-scenarios** in this skill). Plain `.txt` artifacts omit markdown; keep wording domain-precise anyway.
- **Concrete examples:** every **{parameter}** appears in an example table; tables match steps **both ways** (no orphan tables, no `{Concept}` without a table). **Label each placeholder** with the domain concept in the same step (`the User {User}`, `Payment Amount {PaymentAmount}`).
- **Coverage:** at least one happy path, edge/boundary where the story or notes imply it, and explicit error/failure paths when failure behavior matters — trace back **base data** so the scenario is possible.
- **Persistence:** when using the Agile Bot **story-graph**, scenarios belong in **`story-graph.json`** (`scenarios` / `scenario_outlines`); do not invent parallel “feature specification” markdown trees outside the project’s agreed doc layout.
