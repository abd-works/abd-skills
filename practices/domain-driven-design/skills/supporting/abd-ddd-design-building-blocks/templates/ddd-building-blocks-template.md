# DDD Building Blocks — {{MODULE_NAME}}

**Source model:** {{SOURCE_ARTIFACT_PATH}}
**Module:** {{MODULE_NAME}}
**Date:** {{DATE}}

---

## How to read this document

This document **copies and extends** the existing domain model. Each concept from the source is preserved and annotated with DDD stereotype markers (`<<Entity>>`, `<<Value Object>>`, `<<Aggregate Root>>`, `<<Repository>>`, `<<Factory>>`, `<<Domain Event>>`). New concepts (Repositories, Factories, Events) are added where the building-block questions surface them.

Identity is marked with `*` on the properties that **uniquely identify** the concept. Invariants are added where consistency rules are discovered. Cross-aggregate references use `(by ID)`.

Heading level will vary by source fidelity — the structure below is one example.

---

## Template structure

```
# <<Aggregate>> ModuleName or Key ABsrtraction

## <<Aggregate Root>> ConceptName
<<identifier>> property            | (type)
<<identifier>> property            | (type)
responsibility                     | Collaborator
responsibility                     | Collaborator
                                   |   invariant: consistency rule that must always hold

### <<Entity>> ChildConceptName
<<identifier>> property            | (type)
responsibility                     | Collaborator

### <<Value Object>> ConceptName
property                           | (type or values)
property                           | (type or values)

### <<Repository>> ConceptNameRepository
add                                | AggregateRoot
remove                             | AggregateRoot
update                             | AggregateRoot
new                                | AggregateRoot (delegates to Factory or Specification as complexity requires)
find by [business search criteria] | (search parameters)
retire / archive                   | (retirement rules)
                                   |   note: abstracts persistence behind a collection-style interface;
                                   |   at class-model fidelity, implement as a collection type

### <<Factory>> ConceptNameFactory
assemble [concept] from [inputs]   | Collaborators
                                   |   invariant: new instance must be valid (what must be true at birth)

### <<Domain Event>> SomethingHappened
raised when                        | triggering state change
payload                            | (key data carried)

### <<Service>> ActionName
[domain operation]                 | Collaborators across entities
                                   |   stateless: coordinates work, holds nothing between calls
                                   |   rationale: no single concept owns this without distortion

### <<Specification>> RuleName
evaluate                           | (Concept to evaulate)
specify                            | (Concept to upgrade)
                                   |   satisfied when: business predicate expressed as a reusable object
                                   |   used for: querying, validating, or specifying
```

---

---

## Example — Pet Store Order module (from domain model input)

**Source model:** `docs/pet-store/pet-store-class-responsibility-collaborator.md`
**Module:** Order
**Date:** 2026-05-18

---

# <<Aggregate>> Order

## <<Aggregate Root>> Order
<<identifier>> ordering customer   | Customer (by ID)
<<identifier>> order date time     | DateTime
<<identifier>> order amount        | Money
order lines                        | OrderLine
place order                        | Customer (by ID), OrderLine
calculate total                    | OrderLine
                                   |   invariant: total = sum of line amounts
                                   |   invariant: status only advances (Draft → Confirmed → Fulfilled)
                                   |   invariant: cannot confirm with zero lines

### <<Value Object>> OrderLine
product reference                  | Product (by ID)
quantity                           | (integer)
unit price                         | Money
calculate line amount              | (quantity × unit price)

### <<Value Object>> Money
amount                             | (decimal)
currency                           | (ISO code)
                                   |   invariant: immutable — arithmetic returns new instances

## <<Repository>> OrderRepository
store and retrieve orders          | Order
find orders by customer            | Customer (by ID)
find orders by status and date     | (status, date range)
archive fulfilled orders older than | (retention period)

## <<Factory>> OrderFactory
assemble order with lines          | Customer (by ID), Product (by ID), Money
                                   |   invariant: new order always has at least one line and correct total

## <<Domain Event>> OrderConfirmed
raised when                        | Order status transitions to Confirmed after payment validates
payload                            | order ID, customer ID, line items, total, confirmed timestamp
consumers                          | Payment (process charge), Inventory (reserve pets), Notifications (send receipt)

## <<Domain Event>> OrderFulfilled
raised when                        | all items in the order are delivered/picked up
payload                            | order ID, customer ID, fulfillment timestamp
consumers                          | Reporting (revenue), Customer (satisfaction follow-up)

---

# <<Aggregate>> Customer

## <<Aggregate Root>> Customer
<<identifier>> email               | (string)
<<identifier>> phone number        | (string)
place orders                       | Order (by ID)
contact preferences                | ContactPreferences

### <<Value Object>> Address
street                             | (string)
city                               | (string)
province                           | (string)
postal code                        | (string)
                                   |   invariant: immutable — replaced when customer moves

### <<Value Object>> ContactPreferences
preferred channel                  | (email, phone, SMS)
opt-in marketing                   | (boolean)

## <<Repository>> CustomerRepository
store and retrieve customers       | Customer
find by email                      | (email)
find by phone                      | (phone number)
deactivate customer                | (deactivation reason, date)

---

# <<Aggregate>> Product

## <<Aggregate Root>> Product
<<identifier>> SKU                 | (string)
name                               | (string)
category                           | (string)
current price                      | Money

## <<Repository>> ProductRepository
store and retrieve products        | Product
find by category                   | (category)
find by price range                | (min, max Money)

## <<Domain Event>> PriceChanged
raised when                        | Product current price is updated
payload                            | product SKU, old price, new price, effective date
consumers                          | Order (in-flight orders: business decides — freeze at order time or update?)
                                   |   cross-aggregate question: "When price changes, what happens to open orders?"
                                   |   answer: "Orders lock price at time of line creation — price change does not propagate to existing orders"
