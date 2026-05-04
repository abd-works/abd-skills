# Rule: English prose only — no method signatures or typed notation

**Scanner:** Manual review

Responsibility names, collaborator names, and invariants must be written in plain domain language using the property/operation table format. No method signatures, typed parameters, return types, UML notation, cardinality markers, or code-level constructs are permitted anywhere.

## DO

- Write property names as noun phrases and operation names as verb phrases.

  **Example (pass):** `resolve | D20, Trait, Circumstance Modifier, Difficulty Class, Check Result`

- Write invariants as declarative English statements using `|   invariant:`.

  **Example (pass):** `|   invariant: only active conditions apply modifiers`

- Use parenthetical value descriptions for primitives and enums.

  **Example (pass):** `active status | (active or inactive)`

## DO NOT

- Include operation signatures with parameters or return types.

  **Example (fail):** `resolve(roll: int, dc: int) -> bool`

- Use typed property declarations.

  **Example (fail):** `stored result: CheckResult`

- Include UML or cardinality notation in collaborators.

  **Example (fail):** `DifficultyClass 1..1, Modifier 0..*`

- Use code-style boolean expressions in invariants.

  **Example (fail):** `invariant: damage >= threshold && !isImmune` — write "damage equals or exceeds the threshold and the character is not immune" instead.

**Source:** Engagement convention (class-responsibility-collaborator skill).
