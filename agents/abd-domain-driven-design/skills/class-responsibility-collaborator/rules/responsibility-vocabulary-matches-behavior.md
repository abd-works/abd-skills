# Rule: Responsibility vocabulary matches inspiring behavior

**Scanner:** Manual review (grammar/vocabulary spot-check)

Each responsibility name must use vocabulary that is tight to the domain sketch behavior bullet that inspired it. The match need not be word-for-word, but the key domain terms must be recognizable. A reader who sees the responsibility name and the behavior bullet should be able to connect them without explanation.

## DO

- Use the key noun or verb from the behavior bullet.

  **Example (pass):** Behavior: "carries *imposed conditions* via its *Imposed Conditions* collection" → responsibility: `imposed conditions | Imposed Conditions`.

  **Example (pass):** Behavior: "is removed when its *condition source* ends" → operation: `end | Imposed Conditions`.

  **Example (pass):** Behavior: "penalizes a *suffering character* according to a *game modifier*" → property: `game modifier | (penalty value or restriction description)`.

## DO NOT

- Use a generic name that could apply to any concept.

  **Example (fail):** Behavior says "enforces penalties and restrictions only when active" but responsibility is named `apply` — too vague; use `enforce | Character, Check`.

- Rename a domain term to a technical synonym or generic substitute.

  **Example (fail):** Behavior says "imposing source" but responsibility is named `origin` or `cause`.

- Use vocabulary from a different concept's behavior.

  **Example (fail):** `Condition` has a responsibility named `roll` — that term comes from `Check`, not from any `Condition` behavior.

**Source:** Engagement convention (class-responsibility-collaborator skill).
