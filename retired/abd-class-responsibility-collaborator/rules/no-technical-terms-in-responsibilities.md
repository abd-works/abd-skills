# Rule: No technical terms in responsibility names

**Scanner:** Manual review (grammar/vocabulary spot-check)

Responsibility names — both property names and operation names — must use domain language vocabulary. Technical implementation terms are forbidden.

## Forbidden terms (and their replacements)

- `flag` → use a domain state phrase: `is ongoing`, `is routine`
- `boolean`, `bool` → use the domain state name
- `list`, `array`, `collection` → introduce a named collection class instead
- `type` as a bare noun → use a qualified domain noun
- `status` as a bare noun → qualify it from the behavior: `active status`, `activation status`
- `own` as a prefix → use descriptive qualifiers from the behavior language; `own` conveys nothing

## DO

- Derive the noun or verb from the behavior bullet that inspired the responsibility.

  **Example (pass):** Behavior says "penalizes a suffering character according to a game modifier" → property is `game modifier`, not `modifier` or `penalty flag`.

  **Example (pass):** Behavior says "may be ongoing for a target character" → property is `is ongoing`, not `ongoing flag` or `ongoing boolean`.

  **Example (pass):** Behavior says "is the power effect and attacker that imposed a condition" → property is `imposing source`, not `source` or `own source`.

## DO NOT

- Use bare nouns when a qualifier is available from the behavior.

  **Example (fail):** `source | Condition Source` when the behavior says "the imposing source" — use `imposing source`.

- Use technical implementation words.

  **Example (fail):** `ongoing flag | (true or false)`, `condition list | Condition`

**Source:** Engagement convention (class-responsibility-collaborator skill).
