# Phase 8 — Behavior Model

**Actor:** AI | 
## Purpose

Assign operations to concepts based on interaction steps.


## Trigger

behavior model, assign operations, trigger response, pre-condition steps

## Inputs


## Outputs



---

## Domain Model Rules (7)

Apply these rules when producing the domain model output for this phase.

---
title: Domain Model — Atomic Operations
impact: HIGH
---

## One Operation = One Behavior

**DO** keep Operations atomic: one Operation = one behavior.

**DO** describe behavior (Acquires, Releases, Calculates, Validates), not outcome (Prevents, Issues).

**DO NOT** pack multiple conditions into one Operation (e.g. "Releases on unlock, redemption complete, or timeout" → split into separate Operations).

**DO NOT** use outcome phrasing (Prevents, Issues) when behavior phrasing is clearer (Acquires, Releases).


---

---
title: Behavior Owns Decision
impact: HIGH
---

# Behavior Owns Decision

Place behavior on the object that owns the data needed for the decision. The information expert should own the rule.

**DO:** Assign decisions, validation, and rule enforcement to the object that holds the state needed to make the decision. If an object has properties, it should also have operations that use those properties.

Example (correct):
```
Account
- Number balance
- can_debit(amount) → balance >= amount
- debit(amount) → enforces invariant, updates balance
```

**DO NOT:** Split data from the logic that operates on it. Objects with properties but no meaningful operations are anemic — the decisions are elsewhere, typically in a service or manager.

Example (wrong):
```
Account
- Number balance
(no operations — debit logic lives in AccountService.debit(account, amount))

AccountService
- debit(account, amount) → checks account.balance >= amount, sets account.balance -= amount
```


---

---
title: Domain Model — Code Representation
impact: MEDIUM
---

## Align to Implementation

**DO** use concise concept names that could exist as types (Order, Portfolio, LineItem).

**DO** use typed Properties and Operations — actual type names (Money, Symbol, Quantity), not prose descriptions.

**DO NOT** use long prose sentences as concept names (e.g. "Collection of customer investments that aggregates all holdings...").

**DO NOT** use prose descriptions for Property or Operation types — use actual type names (e.g. `RiskScore, RiskModel, Holding`, not "detailed object containing volatility calculations").


---

---
title: No Generic Resolvers
impact: HIGH
---

# No Generic Resolvers

Generic resolver, handler, manager, or processor classes that route all behavior through one point are a sign of missing domain abstractions.

**DO:** Create specific domain objects for specific behaviors. If multiple types share a pattern, use polymorphism — each type owns its own behavior.

Example (correct):
```
WireTransfer
- validate() → validates SWIFT code, multi-day settlement rules
- execute() → executes wire-specific settlement

ACHTransfer
- validate() → validates routing number, batch rules
- execute() → executes ACH-specific settlement
```

**DO NOT:** Use generic "resolver" or "handler" classes that route all behavior through one point. These centralize decisions that should be distributed to domain objects.

Example (wrong):
```
TransferResolver
- resolve(type, data) → if type == "wire": ... elif type == "ach": ... elif ...
```


---

---
title: Thin Orchestration
impact: HIGH
---

# Thin Orchestration

Orchestration layers coordinate — they do not decide. Business logic belongs to the object that owns the data needed for the decision.

**DO:** Keep orchestrators thin — they sequence calls, pass messages, and handle lifecycle. Decisions, validation, and rule enforcement live on domain objects.

Example (correct):
```
PaymentProcessor (orchestration)
- process(payment) → delegates to payment.validate(), account.debit(), settlement.execute()

Payment (domain object)
- validate() → owns validation rules
- apply_fees() → owns fee calculation
```

**DO NOT:** Put business logic in orchestrators, managers, or handlers. If an orchestrator is making decisions about domain state, the decision belongs on the domain object instead.

Example (wrong):
```
PaymentProcessor (orchestration)
- process(payment) → checks payment.amount > 0, checks account.balance >= amount, calculates fees, applies discount rules
```


---

---
title: Traverse From Root
impact: HIGH
---

## Traverse From Root

**DO** traverse from root. The source owns creation; the created object receives the source and derives the value internally. Do not pass raw derived values.

**DO NOT** pass raw values when the source object is available.

- Example (wrong): `validation.resolve(source.value)`
- Example (correct): `validation = source.create_validation(dc)` then `validation.resolve()` — validation gets value from source internally.


---

---
title: Derive from context
impact: HIGH
---

## Derive from context

**DO** derive concepts from the interactions you find in the context; focus on *who* exchanges *what* and *what must be true before and after*.
- Example (right): Context says "Customer adds to cart" → interaction: Add to Cart; concepts: Shopping Cart, LineItem. Context says "User selects country for payment" → interaction: Select Country; concepts: Country, PaymentType.

**DO NOT** invent workflows or mechanics not present in the context.
- Example (wrong): Story "Express checkout" or concept "LoyaltyPoints" when context never mentions them. Right: Omit; if needed, state assumption.


---

