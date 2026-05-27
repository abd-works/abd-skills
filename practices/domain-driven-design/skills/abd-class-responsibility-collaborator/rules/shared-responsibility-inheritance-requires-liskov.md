# Rule: Shared responsibility and inheritance require Liskov substitution

**Scanner:** Manual review

When the **same domain responsibility** (same behavioral contract in domain terms, not merely the same English label) appears on multiple concepts, that is a **signal to investigate** shared abstraction — often a base class with subtypes. Inheritance is appropriate **only if the Liskov substitution principle holds**: code written against the base concept must work correctly for **any** subtype without branching on which subtype it is. If a subtype would need to weaken a precondition, strengthen a postcondition, throw in cases the base promises not to, or otherwise change the contract, **inheritance is the wrong tool** — prefer a shared collaborator, a role interface at the point of use, composition, or two parallel concepts.

This rule supplements **Subtype uses child : parent** — it is the gate for *when* to introduce that hierarchy.

## DO

- Before adding `#### **Child : Parent**`, ask: *Could every responsibility inherited or lifted to the parent be fulfilled by every subtype with the same expectations?*

  **Example (pass):** `StandardCheck` and `OpposedCheck` both "resolve" with the same caller expectations (input concepts, outcome shape); differences are *how* total or DC is formed — delta responsibilities stay on subtypes; shared resolution contract stays on `Check`.

- When contracts genuinely align, extract the common responsibility to the parent and keep only deltas on subtypes.

## DO NOT

- Introduce a base class because two concepts share a noun in a responsibility name when their rules or collaborations differ incompatibly.

  **Example (fail):** `SavingsAccount` and `TradingAccount` both have "post transaction" but one forbids negative balance and the other allows margin — a single `Account.postTransaction` contract cannot serve both without subtype-specific checks that violate substitutability.

- Use inheritance to deduplicate implementation detail when the domain types are not substitutable for callers.

  **Example (fail):** Base `Bird` with `fly()` and subtype `Penguin : Bird` that cannot fly — same label, incompatible contract; use composition or separate roles instead.

**Source:** Engagement convention (class-responsibility-collaborator skill).
