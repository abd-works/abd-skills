# Specification by Example — `<Module Name>`

**Sources / context:** `<source files used>`

**Domain outline:** `docs/domain/domain-model.md` (default) · `docs/domain/domain-specification.md` (if present)

---

<!--
  Default input: domain model outline — read it before writing any scenario.
  Concept names, relationships, and invariants come from there verbatim.

  DEFAULT NOTATION: Scenario Outline.
  Every story with more than one scenario uses Scenario Outline with normalised Examples tables.
  Plain Scenario is the exception — only for single-path stories with no data variation.

  Stories are the organizing unit. All scenarios live in this single file.
-->

## Story: `<Verb–Noun Title>`

**Story type:** user | system | technical

**Sources / context:** _(pointer to AC file and domain model outline — e.g. `domain-model.md` § Campaign)_

Given a **`<Concept>`** *`<value>`* with a **`<Concept>`** *`<value>`*  
When **`<Concept>`** *`<value>`* does **`<action>`** with **`<Concept>`** *`<value>`*  
Then **`<Concept>`** is marked as *`<outcome>`*  

---

## Story: `<Verb–Noun Title>`

**Story type:** user | system | technical

**Sources / context:** _(pointer to AC file and domain model outline — e.g. `domain-model.md` § Campaign)_

---

## Examples

### `<Domain ConceptA>`:

| scenario      | `<field_1>` | `<field_2>` |
|---------------|-------------|-------------|
| `<Scenario A>` | `<value>`  | `<value>`   |
| `<Scenario B>` | `<value>`  | `<value>`   |

### `<Domain ConceptB>`:

| scenario      | `<concept_a_fk>` | `<field_1>` | `<field_2>` |
|---------------|-------------------|-------------|-------------|
| `<Scenario A>` | `<fk_value>`     | `<value>`   | `<value>`   |
| `<Scenario B>` | `<fk_value>`     | `<value>`   | `<value>`   |

---

## Background

Given a **`<ConceptA>`** {field_1} with **`<ConceptA>`** {field_2}
  And a **`<ConceptB>`** {field_1} linked to **`<ConceptA>`** {concept_a_fk}

---

## Scenarios

### Scenario Outline 1: `<outcome-oriented name>`

### Steps

When **`<action>`** using **`<ConceptA>`** {field_1}
Then **`<outcome>`** is {field_2}

---

## Example (plain scenario)

## Story: Apply For a Payment Product Agreement

**Story type:** user

**Sources / context:** _(Payments Domain — domain specification: Payment Product, Customer, Account, Owner, Payment Product Agreement · `domain-model.md` § Customer, Account)_

---

## Scenarios

### Scenario 1: Agreement submitted with valid DDA Account and Owner

Given a **Customer** *Jane Doe* exists  
  And that **Customer** *Jane Doe* has a valid **DDA Account** *DDA-001*  
When the **Customer** *Jane Doe* applies for a **Payment Product Agreement**  
    using **DDA Account** *DDA-001*  
    with **Owner** *John Doe*  
      that has **Contact Details** *john@acme.com*  
Then the **Payment Product Agreement** is submitted for review  
  And the **Owner** *John Doe* is notified at *john@acme.com*  

### Scenario 2: Agreement rejected when DDA Account is invalid

Given a **Customer** *Jane Doe* exists  
  And that **Customer** *Jane Doe* has **DDA Account** *DDA-999* with status *Invalid*  
When the **Customer** *Jane Doe* applies for a **Payment Product Agreement**  
    using **DDA Account** *DDA-999*  
Then the **Payment Product Agreement** is *rejected*  
  And **Customer** *Jane Doe* is notified that the **DDA Account** is *not eligible*  

---

## Example (scenario outline with normalized tables)

## Story: Submit Payment and Validate Against Account Limit

**Story type:** user

**Sources / context:** _(Payments Domain — domain specification: Account, Transactional Limit, Wire Payment)_

---

## Examples

### Account:

| scenario      | enterprise_name | account_name       | activation_status |
|---------------|-----------------|--------------------|-------------------|
| Scenario 1    | Acme Corp       | Acme Operating     | Active            |
| Scenario 2    | Acme Corp       | Acme Payroll       | Active            |

### Transactional Limit:

| scenario      | account_name       | limit_name  | max_amount   | currency |
|---------------|--------------------|-------------|--------------|----------|
| Scenario 1    | Acme Operating     | daily_wire  | 500000.00    | USD      |
| Scenario 2    | Acme Payroll       | weekly_wire | 2000000.00   | USD      |

### Wire Payment:

| scenario      | amount      | currency | formatted_display | validation_status |
|---------------|-------------|----------|-------------------|-------------------|
| Scenario 1    | 10000.00    | USD      | $10,000.00        | successful        |
| Scenario 2    | 500000.01   | USD      | $500,000.01       | rejected          |

---

## Background

Given a **User** {user_name} is logged into ChannelOne 2.0  
  And that **User** {user_name} is representing **Enterprise** {enterprise_name}  

---

## Scenarios

### Scenario Outline 1: Submit Payment and Validate Against Account Limit

### Steps

Given an **Account** {account_name} with **Activation Status** {activation_status}  
  And the **Transactional Limit** for that **Account** is {max_amount} {currency}  
When the **User** enters a **Payment Amount** of {amount} {currency}  
Then the **Wire Payment** is marked as {validation_status}  
  And a **Report** is sent with formatted display {formatted_display}  

---

<!-- Template reference only — do not copy this section into generated project files. -->

## Instructions

- **Default notation: Scenario Outline.** Every multi-scenario story uses Scenario Outline with Examples tables. Plain Scenario only for single-path stories with no data variation.
- **Plain scenarios:** Given = state; When = action; Then = observable outcome. Use **bold** for domain concepts, *italics* for values.
- **Scenario outlines:** Use `{column_name}` tokens in steps matching example table headers exactly. Provide multiple rows.
- **Example tables:** One table per domain concept. Link related tables with foreign-key columns. Never denormalize multiple concepts into a single flat table.
- Cover at least one happy path, one failure or rejection, and edge cases where the story implies them.
