# Scenario Outline (specification by example)

A **Scenario Outline** is a scenario whose steps are **parameterized**: every varying value is replaced with a `<column_name>` token, and the actual values are supplied in an **Examples** table below. Each row in that table produces one concrete test run, so one outline with four rows gives you four scenarios without writing the steps four times. Use an outline when the **same** flow applies across multiple data variations—different payment instruments, boundary amounts, user roles, and so on—and the difference is purely **which data** runs through the same logic.

Example tables for an outline follow the same placement rules as regular scenario tables: precondition tables (rows needed by **Given**) go **above** the outline; outcome tables (first introduced in **When** / **Then**) go **below**. The **Examples** block itself is always kept with the outline, and its headers must match the `<column_name>` tokens in the steps exactly.

Provide **multiple rows** in every example table so readers can see the real variation the outline is testing.

---

## Template

## Story: `<Verb–Noun Title>`

**Story type:** user | system | technical

**Sources / context:** _(pointer to source or conversation / workshop date)_

---
## Examples

### `<Domain ConceptA>`:

| <scenario_name>       | <field_2> | <field_3> |
|-----------------------|-----------|-----------|
| <Scenario A>          | <value>   | <value>   |
| <Scenario B>          | <value>   | <value>   |
| <Scenario C>          | <value>   | <value>   |

### `<Domain ConceptB>`:

| <scenario_name> | <field_1> | <field_2> |
|-----------------|-----------|-----------|
| <Scenario A>    | <value>   | <value>   |
| <Scenario B>    | <value>   | <value>   |

### `<Domain ConceptC>`:

| <scenario_name> | <field_1> | <field_2> | <field_3> | <field_4> |
|-----------------|-----------|-----------|-----------|-----------|
| <Scenario A>    | <value>   | <value>   | <value>   | <value>   |
| <Scenario B>    | <value>   | <value>   | <value>   | <value>   |
| <Scenario C>    | <value>   | <value>   | <value>   | <value>   |

## Background

Given <Precondition statement with *Domain ConceptA*> {<field_1>}
  And <Precondition statement with *Domain ConceptA*> {<field_2>}
  And <Precondition statement with *Domain ConceptB*> {<field_1>}
---

## Scenarios

### Scenario 1: `<outcome-oriented name>`

### `<Domain ConceptD>`:

| <scenario_name> | <field_1> | <field_2> | <field_3> | <field_4> | <field_5> |
|-----------------|-----------|-----------|-----------|-----------|-----------|
| <Scenario A>    | <value>   | <value>   | <value>   | <value>   | <value>   |
| <Scenario B>    | <value>   | <value>   | <value>   | <value>   | <value>   |
| <Scenario C>    | <value>   | <value>   | <value>   | <value>   | <value>   |

### Steps
Given <Precondition statement with *Domain ConceptC*> {field_1}
When <action using *ConceptD* <{field_1}>
  And <action using *ConceptD* <{field_2}>
  And <action using *ConceptD* <{field_3}>
Then <outcome marked as *ConceptD* <{field_4}>
  And <ConceptD secondary outcome with <{field_5}>

---



---

<!-- Template reference only — do not copy this section into generated project files. -->
# Scenario Outline example

## Examples:

### Account:

| scenario      | enterprise_name | account_name       | activation_status |
|--------------|-----------------|--------------------|-------------------|
| Scenario 1   | Acme Corp       | Acme Operating     | Active            |
| Scenario 2   | Acme Corp       | Acme Payroll       | Active            |
| Scenario 3   | Beta LLC        | Beta Main Account  | Active            |

### Transactional Limit:

| scenario      | limit_name  | max_amount   | currency |
|--------------|-------------|--------------|----------|
| Scenario 1   | daily_wire  | 500000.00    | USD      |
| Scenario 2   | weekly_wire | 2000000.00   | USD      |

### Background
  Given a **User** *{user_name}* is logged into ChannelOne 2.0
  And that **User** *{user_name}* is representing **Enterprise** *{enterprise_name}* with **Role** *{user_role}*
  And that **Enterprise** *{enterprise_name}* has **Payment Service** *{payment_service}* enabled
  And that **User** *{user_name}* has **Entitlement** *{entitlement_name}* with **Entitlement Status** *{entitlement_status}*

## Scenarios:

### Scenario 1: Submit Payment and Validate Against Account Limit

### Wire Payment:

  | scenario      | amount      | currency | formatted_display | validation_status |
  |--------------|-------------|----------|-------------------|-------------------|
  | Scenario 1   | 10000.00    | USD      | $10,000.00        | successful        |
  | Scenario 2   | 500000.00   | USD      | $500,000.00       | successful        |
  | Scenario 3   | 500000.01   | USD      | $500,000.01       | rejected          |
  | Scenario 4   | 0.00        | USD      | $0.00             | rejected          |

  Given an **Account** *{account_name}* owned by **Enterprise** *{enterprise_name}* with **Activation Status** *{activation_status}* is selected
    And the daily **Transactional Limit** for that Account is *{max_amount} {currency}*
  When the **User** *{user_name}* enters a **Payment Amount** of *{amount} {currency}*
    Then the **Wire Payment** is marked as *{validation_status}*
    And a **Report** is sent with formatted display *{formatted_display}*

## Instructions
- Keep `<column_name>` tokens in steps spelled exactly like the **Examples** header row.
- Every `<column_name>` in the steps must appear as an **Examples** header; every **Examples** header must appear in at least one step.
- Provide **multiple rows** — an outline with one row should be a plain **Scenario** instead.
- Do not use an outline when rows need materially different **Given** setup; write separate scenarios instead.
- Concept tables that feed **Given** go **above** the outline; tables for **When**/**Then** outcomes go **below**.


