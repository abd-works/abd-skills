# Rule: Introduce a state-carrier class when application requires unique state

**Scanner:** Manual review

When applying a concept to an entity requires state that is unique from the concept itself — state that varies per application, per entity, or over time — introduce a separate state-carrier class. Do not add that state to the original concept or to the entity.

## DO

- Introduce a state-carrier class when the applied state is distinct from the concept's definition.

  **Example (pass):** `Condition` holds its label, modifier, and supersession relationships — the same for every character. `Imposed Condition` holds the active/inactive status, suppressing condition, and source — state that is unique to each application on a specific character.

- Name the state-carrier after its role in the application.

  **Example (pass):** `Imposed Condition` — describes what it is: a condition that has been imposed. Not `ConditionState` or `AppliedCondition`.

## DO NOT

- Add per-application state to the value object concept.

  **Example (fail):** Adding `active status` and `suppressing condition` directly to `Condition` — these vary per character and per imposition, not per condition type.

- Add per-concept state to the entity that holds it.

  **Example (fail):** Adding `active status` directly to `Character` — the character may carry many conditions, each with its own status.

## Vocabulary note

Use the word *instance* only for values of a value object (e.g. *dazed* is an instance/value of `Condition`). Never use *instance* as a synonym for a state-carrier class — a state-carrier is a distinct domain class, not an instance of another.

**Source:** Engagement convention (class-responsibility-collaborator skill).
