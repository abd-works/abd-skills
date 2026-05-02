# Rule: English prose only — no method signatures or typed notation

**Scanner:** Manual review

The entire CRC section — responsibilities, rejections, collaborators, lifecycle transitions, and invariants — must be written in plain English. No method signatures, typed parameters, return types, UML notation, cardinality markers, or code-level constructs are permitted anywhere. Passing means every line reads as a natural-language sentence or phrase. Failing means design-level notation has leaked into any field.

## DO

- Write responsibilities, rejections, and collaborator descriptions in prose.

  **Example (pass):** `responsible: resolves whether an attempted action succeeds or fails against a target difficulty`

- Describe lifecycle transitions and constraints in natural English.

  **Example (pass):** `transitions: inactive → active (source effect imposed), active → resolved (source effect ends or resistance check succeeds)`

- Write invariants as declarative English statements.

  **Example (pass):** `- a condition already present in the supersession chain is overridden by the more severe one, never duplicated`

## DO NOT

- Include operation signatures with parameters or return types.

  **Example (fail):** `responsible: resolve(roll: int, dc: int) -> bool`

- Use typed property declarations.

  **Example (fail):** `responsible: stores result: CheckResult and modifiers: List<Modifier>`

- Include UML or cardinality notation in collaborators.

  **Example (fail):** `collaborators: DifficultyClass 1..1, Modifier 0..*`

- Use code-style boolean expressions in invariants.

  **Example (fail):** `invariants: damage >= threshold && !isImmune` — write "damage equals or exceeds the threshold and the character is not immune" instead.

**Source:** Engagement convention (class-responsibility-collaborator skill).
