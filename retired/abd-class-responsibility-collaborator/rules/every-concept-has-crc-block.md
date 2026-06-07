# Rule: Every concept from Domain Language has a domain model block

**Scanner:** Manual review

After CRC enrichment, every concept and subtype represented in **`### Domain Language`** must have a corresponding CRC block in **`### Class Responsibility Collaborator`**. No concept may be silently dropped. Passing means every concept is accounted for. Failing means a concept exists in the Domain Language but has no CRC block.

## DO

- Create a domain model block for each `#### **ConceptName**` heading under `### Domain Language`.

  **Example (pass):** Domain Language lists `#### **Check**`, `#### **Difficulty Class**`, `#### **Trait`** — CRC section has blocks for `Check`, `Difficulty Class`, and `Trait`.

- Create a domain model block for each subtype the sketch records (however phrased — e.g. bullets or wording that establishes *is a type of* / specialization), using `#### **ChildConcept : ParentConcept**` in the domain model section.

  **Example (pass):** Domain Language establishes that Saving Throw is a kind of Check — CRC has `#### **Saving Throw : Check**` with delta responsibilities only.

## DO NOT

- Drop a concept without creating a domain model block for it.

  **Example (fail):** `#### **Trait**` appears under `### Domain Language` but no CRC block addresses `Trait`.

- Introduce a domain model block that has no corresponding concept in the Domain Language.

  **Example (fail):** a domain model block for `Resolution Engine` appears but no concept in the Domain Language supports it.

**Source:** Engagement convention (class-responsibility-collaborator skill).
