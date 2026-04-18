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

## Story: Submit Wire Payment

**Story type:** user

**Sources / context:** _(Enterprise Payments Requirements v2, Ch. 3 pp. 12-14)_

---

## Background

Given a **User** *Jane Doe* is logged into ChannelOne 2.0
  And that **User** *Jane Doe* is representing **Enterprise** *Acme Corp* with **Role** *Wire Operator*
  And that **Enterprise** *Acme Corp* has **Payment Service** *wire* enabled
  And that **User** *Jane Doe* has **Entitlement** *WirePayment.Create* with **Entitlement Status** *Granted*

---

## Scenarios

### Scenario 1: Submit payment within limit - approved

Given **Account** *Acme Operating* owned by **Enterprise** *Acme Corp* with **Activation Status** *Active* is selected
  And the **Transactional Limit** *daily_wire* for that Account is *$500,000.00 USD*
When the **User** *Jane Doe* enters a **Payment Amount** of *$10,000.00 USD*
Then the **Payment Amount** *$10,000.00 USD* is validated against **Transactional Limit** *$500,000.00 USD*
  And the **Wire Payment** is marked as *successful*
  And a **Report** is sent to *Jane Doe* showing formatted display *$10,000.00*

### Scenario 2: Submit payment over limit - rejected

Given **Account** *Acme Operating* owned by **Enterprise** *Acme Corp* with **Activation Status** *Active* is selected
  And the **Transactional Limit** *daily_wire* for that Account is *$500,000.00 USD*
When the **User** *Jane Doe* enters a **Payment Amount** of *$500,000.01 USD*
Then the **Wire Payment** is *rejected*
  And a **Report** is sent to *Jane Doe* showing validation status *rejected*

---

<!-- Template reference only - do not copy this section into generated project files. -->

## Instructions

- Given = state / preconditions only; When = first action; Then = observable domain outcomes.
- Use exact real values inline in the steps - no tables, no placeholder tokens.
- **Domain concept names** in bold; *actual values* in italics.
- Cover at least one happy path, one failure or rejection, and edge cases where the story implies them.
