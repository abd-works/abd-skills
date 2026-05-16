# Rule: Collaborators trace to sketch collaborations and subtype edges

**Scanner:** Manual review

The collaborator column in each CRC block must list domain concepts that appear in the Ubiquitous Language's behavior bullets or subtype edges for that concept. No collaborator may be invented. An empty collaborator column must contain a value description in parentheses (for true primitives only) or name a domain class. Domain-named types with distinct values must be modeled as a named class, not reduced to a parenthetical.

## DO

- List collaborators that correspond to concepts named in the behavior bullet.

  **Example (pass):** Sketch says "supersedes a less severe condition from the same source"; CRC has `supersede | Condition`.

- Use a parenthetical only for true primitives — integer, boolean, string, or a two-state toggle with no domain name.

  **Example (pass):** `numeric value | (integer, can be negative)`

  **Example (pass):** `active status | (active or inactive)` — a boolean toggle with no domain identity of its own.

- Model any domain-named enumeration as a named class with its values listed as an invariant.

  **Example (pass):** `dimension type | Measurement Type` where `Measurement Type` is a concept with invariant `one of mass, time, distance, or volume`.

## DO NOT

- Use a parenthetical for a first-class domain type — a named enumeration whose values carry domain meaning.

  **Example (fail):** `dimension type | (mass, time, distance, or volume)` — these are domain concepts, not a primitive; they need a named class.

- Invent collaborators that have no basis in the Ubiquitous Language.

  **Example (fail):** CRC block lists `Logger, EventBus` but neither concept appears anywhere in the sketch.

- Leave the collaborator column blank without explanation.

  **Example (fail):** `supersede |` with nothing on the right.

**Source:** Engagement convention (class-responsibility-collaborator skill).
