# Specification by example (BDD scenarios)

<!-- Conventions aligned with agile_bots story_bot `behaviors/scenarios`. -->

Use this template when you want scenarios with inline values—no placeholders, no abstract tokens. Group scenarios under a common Background when three or more share the same starting state.

**Formatting convention:** use **bold** for domain concept names and *italics* for the actual values of those concepts (e.g. **User** *Jane Doe*, **Enterprise** *Acme Corp*, **Payment Amount** *$10,000.00 USD*).

---

## Template

## Story: `<Verb–Noun Title>`

**Story type:** user | system | technical

**Sources / context:** _(pointer to source or conversation / workshop date)_

---

## Background

Given a **<Concept>** *<value>*
  And that **<Concept>** *<value>* has **<Concept>** *<value>*
  And that **<Concept>** *<value>* is related to **<Concept>** *<value>* with **<Concept>** *<value>*

---

## Scenarios

### Scenario 1: `<outcome-oriented name>`

Given **<Concept>** *<value>* with **<Concept>** *<value>*
  And **<Concept>** *<value>* for that **<Concept>** is *<value>*
When **<Concept>** *<value>* does **<action>** with **<Concept>** *<value>*
Then **<Concept>** is marked as *<outcome>*
  And a **<Concept>** is sent to *<value>* showing *<value>*

### Scenario 2: `<outcome-oriented name>`

Given **<Concept>** *<value>* with **<Concept>** *<value>*
When **<Concept>** *<value>* does **<action>** with **<Concept>** *<value>*
Then **<Concept>** is *<outcome>*

---

## Example

## Story: Apply For a Payment Product Agreement

**Story type:** user

**Sources / context:** _(Payments Domain — object model: Payment Product, Customer, Account, Owner, Payment Product Agreement)_

---

## Background

Given the following **Payment Products** exist:
  And **Payment Product** *Savings Plus* specifies **Payment Channel** *Direct Deposit*
    And **Payment Product** *Savings Plus* supports **Payment Transactions**

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

<!-- Template reference only - do not copy this section into generated project files. -->

## Instructions

- Given = state / preconditions only; When = first action; Then = observable domain outcomes.
- Use exact real values inline in the steps - no tables, no placeholder tokens.
- **Domain concept names** in bold; *actual values* in italics.
- Cover at least one happy path, one failure or rejection, and edge cases where the story implies them.
