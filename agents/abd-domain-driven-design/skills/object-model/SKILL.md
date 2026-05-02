---
name: object-model
description: >-
  Enrich each module file with a typed domain surface — properties, operation
  signatures, relationships with cardinality, and member-level invariants —
  bridging CRC modeling into implementation-ready design.
---
# object-model

## Purpose

Up to this point the model describes behavior in English: CRC says what each class is responsible for, who it collaborates with, how its lifecycle is structured, and what invariants must always hold. This skill **converts that English into a typed domain surface** — the bridge between behavioral modeling and implementation code. After this step every class exposes the properties it must hold, the operations it can perform (with parameter and return types), the relationships it maintains (with direction and cardinality), and the invariants that constrain individual members. The result is precise enough to drive production code yet still readable as a domain document.

## When to use

- The module file has reached `state: crc` and is ready for its typed surface.
- You need to move from English responsibilities to typed properties and method signatures.
- You want to make collaborator relationships explicit with composition, association, and cardinality.
- You need member-level invariant constraints derived from business-logic.

## Core concepts

### Properties

A property is **what an object must know** to fulfil its responsibility. Derive each property from the CRC "Responsible for" lines: if a class is responsible for tracking something, it needs a property to hold it. Type each property where the domain makes the type obvious (`String`, `Boolean`, `Money`, `List<Item>`, etc.); leave it untyped only when the domain is genuinely ambiguous. Typed constants and enum-like value sets (`UPPER_CASE` names) are grouped under a named constant block.

### Operations

An operation is a **typed method signature** — `methodName(param: Type): ReturnType` — derived from CRC responsibilities. Each "Responsible for" verb phrase becomes a candidate operation. Parameters come from the information the method needs but does not already hold as a property; the return type reflects what the caller expects back. Keep signatures at the domain level: no infrastructure, no UI, no framework types.

### Relationships

A relationship makes a **CRC collaborator** concrete. Two flavors matter:

- **Composition** — the parent owns the child's lifecycle (child cannot exist alone).
- **Association** — both sides have independent lifecycles.

Every relationship has **two ends** and **cardinality** (`1..1`, `0..1`, `1..*`, `0..*`). Derive direction and multiplicity from CRC collaborator lines and domain-logic statements. If the source is ambiguous, state the assumption.

### Invariant lines

An invariant is a **declarative constraint** — "must", "cannot", "only if" — that a property or operation must satisfy. Write it tab-indented directly under the member it constrains: `Invariant: ...`. Derive invariants from business-logic lifecycle guards and always-true rules. Keep each invariant short (one line); long lifecycle prose stays in the business-logic content above.

## Build

1. **Open the module file.** Confirm the YAML front-matter reads `state: crc`. If it does not, stop — the prerequisite skill has not run.
2. **Locate the CRC content** already in the file. For each CRC class (or subtype), derive a domain-model block.
3. **Derive properties.** Read each "Responsible for" line. Ask: *what must this class remember to do that?* List each answer as `+ propertyName: Type`. Group related properties into clusters separated by `----`.
4. **Derive operations.** Read each "Responsible for" verb phrase. Ask: *what action does the class expose, and what does it need and return?* Write `+ methodName(param: Type): ReturnType`. Place operations after their related properties inside the same cluster.
5. **Derive relationships.** Read each "Collaborators" entry. Ask: *does this class own the other (composition) or merely reference it (association)?* Write the relationship with cardinality on both ends. Place relationships in the cluster where they are most relevant.
6. **Add invariant lines.** Scan the CRC `invariants:` fields in the file for lifecycle guards and always-true rules that constrain a specific property or operation. Write each as a tab-indented `Invariant: ...` line directly under the member it constrains.
7. **Handle subtypes.** Use `ChildClass : ParentClass` on the heading line. The child block contains only delta properties, operations, and relationships — do not repeat the parent surface. Stereotypes (`<< Entity >>`, `<< ValueObject >>`) are optional.
8. **Format.** Use `----` to separate clusters within a class and `-----` to separate whole classes. Follow `templates/domain-model-scaffold.md` for placeholder shapes and heading conventions.
9. **Bump state.** Change the YAML front-matter from `state: crc` to `state: domain-model`.

## Templates

`templates/domain-model-scaffold.md`

## Validate

- Every CRC class that owns domain behavior has a domain-model block with at least one property justified by its "Responsible for" line.
- Every operation signature traces to a CRC responsibility verb phrase.
- Every relationship has two named ends and cardinality; direction matches the CRC collaborator that sourced it.
- Invariant lines reference CRC `invariants:` guards or always-true rules — none are invented.
- Walkthrough scenarios (if present) can still be stepped with the new typed names (spot-check at least one).
- The YAML front-matter reads `state: domain-model`.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Invariant lines trace to CRC invariants or always-true rules

Every `Invariant: ...` line under a member must be sourced from the CRC `invariants:` field of the corresponding concept. Passing means each invariant is short, tab-indented under the member it constrains, and traceable to the CRC block. Failing means an invariant is invented, placed outside a member context, or contradicts the CRC source.

#### DO

- Write each invariant as a single tab-indented line directly under the property or operation it constrains, sourced from the CRC `invariants:` field.

  **Example (pass):**
  ```
  + remainingBudget: Money
  	Invariant: remainingBudget ≥ 0 (from: "budget must never go negative")
  ```

- Keep invariants declarative — "must", "cannot", "only if" — matching the CRC phrasing.

  **Example (pass):**
  ```
  + ship(destination: Address): void
  	Invariant: cannot ship unless paymentCleared is true
  ```

#### DO NOT

- Invent an invariant that has no corresponding CRC `invariants:` line.

  **Example (fail):**
  ```
  + quantity: Integer
  	Invariant: quantity must be a prime number   ← no CRC source
  ```

- Place an invariant as a free-standing line outside any member context.

  **Example (fail):**
  ```
  Invariant: total must match sum of line items
  + totalPrice: Money                             ← invariant floats above, not under a member
  ```

- Write multi-line prose instead of a single declarative constraint.

  **Example (fail):**
  ```
  + status: OrderStatus
  	Invariant: When the order transitions from pending to confirmed
  	           the system must verify that all line items are in stock
  	           ← too long; split into atomic invariants or keep prose in CRC
  ```

### Rule: Operations use typed signatures tracing to CRC verbs

Every operation must be written as a typed method signature — `methodName(param: Type): ReturnType` — and must trace to a CRC responsibility verb phrase. Passing means the signature is complete and the source verb phrase is identifiable. Failing means the operation lacks types, uses prose instead of a signature, or has no CRC verb-phrase origin.

#### DO

- Write each operation as `+ methodName(param: Type): ReturnType`, derived from a CRC "Responsible for" verb phrase.

  **Example (pass):**
  ```
  CRC — Responsible for: calculating shipping cost based on weight and destination

  Domain-model block:
  + calculateShippingCost(weight: Weight, destination: Address): Money
  ```

- Omit the return type only when the operation is genuinely void (a command with no meaningful return).

  **Example (pass):**
  ```
  + cancelOrder(reason: String): void
  ```

#### DO NOT

- Write an operation as plain prose without a typed signature.

  **Example (fail):**
  ```
  + calculates the shipping cost     ← prose, not a signature
  ```

- Add an operation that does not trace to any CRC responsibility verb phrase.

  **Example (fail):**
  ```
  CRC — (no mention of "archiving")

  Domain-model block:
  + archiveRecord(id: RecordId): void   ← invented, no CRC source
  ```

- Leave parameters or return types untyped when the domain makes the type obvious.

  **Example (fail):**
  ```
  + calculateShippingCost(weight, destination)   ← missing types
  ```

### Rule: Every property traces to a CRC responsibility

Every property in a domain-model block must be justified by a "Responsible for" line in the corresponding CRC class. Passing means each property answers the question *what must this class remember to fulfil that responsibility?* Failing means a property appears with no CRC backing, or a CRC responsibility that implies stored state has no matching property.

#### DO

- Derive each property from a specific "Responsible for" line and type it where the domain makes the type obvious.

  **Example (pass):**
  ```
  CRC — Responsible for: tracking the total price of the order

  Domain-model block:
  + totalPrice: Money
  ```

- Include at least one property for every CRC class that owns domain behavior.

  **Example (pass):** A CRC class with three "Responsible for" lines produces a domain-model block with three or more properties, each traceable to one of those lines.

#### DO NOT

- Add a property that has no corresponding CRC responsibility.

  **Example (fail):**
  ```
  CRC — (no mention of "color")

  Domain-model block:
  + color: String       ← invented, not sourced from CRC
  ```

- Leave a CRC class that holds state without any domain-model properties.

  **Example (fail):** A CRC class is "Responsible for: maintaining the remaining budget" but its domain-model block has zero properties — the stored state was never surfaced.

### Rule: Relationships have two named ends and cardinality

Every relationship in a domain-model block must name both ends and state cardinality (`1..1`, `0..1`, `1..*`, `0..*`). Direction must match the CRC collaborator that sourced it. Passing means both ends, cardinality, and direction are present and traceable. Failing means an end is unnamed, cardinality is missing, or the direction contradicts the CRC collaborator line.

#### DO

- State both class names, the relationship kind (composition or association), and cardinality on both ends.

  **Example (pass):**
  ```
  Order *composes* OrderLine  [1..1 → 1..*]
  ```

- Derive direction from the CRC collaborator entry — the class that lists the collaborator is the navigating end.

  **Example (pass):**
  ```
  CRC — Order collaborates with OrderLine
  → Order navigates to OrderLine, not the reverse
  ```

#### DO NOT

- Write a relationship with only one end named.

  **Example (fail):**
  ```
  *composes* OrderLine  [1..*]    ← owning end missing
  ```

- Omit cardinality entirely.

  **Example (fail):**
  ```
  Order *associates* Customer     ← no cardinality on either end
  ```

- Reverse the direction from what the CRC collaborator line states.

  **Example (fail):**
  ```
  CRC — Order collaborates with Customer
  Relationship written as: Customer *associates* Order  ← direction flipped
  ```

### Rule: State marker is domain-model

After this skill runs, the module file's YAML front matter must contain `state: domain-model`. Passing means the marker is present and correct. Failing means the marker is missing, still shows a previous state, or has a typo.

#### DO

- Set the front matter to exactly `state: domain-model`.

  **Example (pass):**
  ```
  ---
  state: domain-model
  ---
  ```

#### DO NOT

- Leave the state at `crc` (the previous step).

  **Example (fail):**
  ```
  ---
  state: crc
  ---
  ```

- Omit the front matter entirely.

  **Example (fail):** File starts with `## Module:` and has no YAML front matter.
<!-- execute_rules:bundle_rules:end -->
