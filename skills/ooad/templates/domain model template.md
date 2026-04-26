## Domain model 

One file per workspace. All phases write into this file. **Never delete old `note:` lines -- each phase appends.**

**Conventions (abd-ooad / properties-methods-and-relationships):**

- `## [Module: Name]` then a short paragraph for module scope.
- `ClassName << Entity | ValueObject | ... >>` when stereotypes help; one or two sentences on what the class owns.
- Group **related** properties and the methods that belong with them; use `----` between sub-clusters inside a class.
- **`-----`** between **classes** (full separator).
- **Relationships / cardinality** on properties: `+ name:Type [*..1]`, etc.
- **Typed constants / enums:** `NAME_IN_UPPER_SNAKE` for literals or enum-like sets; document values in a block under the type name.
- **Subtypes:** `ChildClass : ParentClass` on the class title line — make generalization explicit.
- **Invariants** (declarative): tab-indented under the **property or method** they guard, e.g. `Invariant: ...` (see example). For heavy lifecycle text, prefer **`business-logic.md`** and reference briefly here.

---

## [Module: {{Module}}]

{{Short paragraph describing module purpose / responsibility}}

{{ClassName}} : {{BaseType}}
{{1-2 sentences: why this class exists / what it owns}}
----------
+ {{property}}:{{Type}}
+ {{property}}:{{Type}}
+ {{method}}({{param}}:{{Type}}, ...): {{ReturnType}}
+ {{method}}({{param}}:{{Type}}, ...): {{ReturnType}}

-----

---

## Example

## [Module: Payments]

Owns all money movement and connector routing for a transaction.

Payment << Entity >>
Owns lifecycle and state transitions for a single money movement attempt.
+ id:UniqueID
+ uniqueSessionKey:String
----
+ currency:Currency [*..1]
+ region:Region [*..1]
+ rail:PaymentRail [*..1]
+ rail:connectToRail()
    Invariant: payment rail, currency, and region are immutable once set
-----
+ PAYMENT_STATE:PaymentState [*..1]
+ authorize(selectedPaymentRail:PaymentRail): AuthResult
    Invariant: PAYMENT_STATE must be PAYMENT_METHOD_SELECTED before authorize
+ submit():PaymentResult
    Invariant: state must be PAYMENT_READY before submit

PaymentRailConnector
The PaymentRail is determined by the currency+region pair that selects a connector.
+ determineRail(payment:Payment): PaymentRail

PAYMENT_STATE
Typed constants (UPPER_CASE):
    PAYMENT_AUTHORIZED = "PA"
    PAYMENT_READY = "PR"

WireTransfer : Payment

-----
