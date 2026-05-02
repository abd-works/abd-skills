# Rule: All typing decisions grounded in source and pass the decision checks

**Scanner:** AI review

Every modeling classification (concept, subtype, type property, instance, property, invariant, relationship, role exclusion) must be grounded in the source material for that specific term. Passing means a reviewer can trace the classification to source evidence. Failing means a term was classified based on surface similarity, assumption, or pattern-matching without reading what the source says about that term's behavior.

## DO

- Read the source material for a term before classifying it.

  **Example (pass):** Classified *ability*, *defense*, *skill*, *power*, *advantage* as subtypes of *Trait* after reading that each is defined in its own module with distinct behavior — abilities set base scores, defenses derive from abilities and supply resistance DCs, powers have effect ranks and extras.

- Record the classification rationale in `#### Decisions made`.

  **Example (pass):** "Ability, defense, skill, power, advantage are subtypes of Trait with distinct behavior — each is owned by its own module."

## DO NOT

- Classify based on surface similarity without reading the source.

  **Example (fail):** "They all have ranks, so they're a type property on Trait" — without checking whether abilities, powers, and skills actually behave differently.

- Promote every term to a concept heading without checking whether it has distinct identity, state, behavior, structure, or interactions.

  **Example (fail):** Twenty Key Abstraction terms produce twenty `### Concept` headings — flat inventory, no modeling.

**Source:** Correction 21 (mm3e-online-holistic engagement).
