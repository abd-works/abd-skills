# Rule: Every concept from Ubiquitous Language has a CRC block

**Scanner:** Manual review

After CRC enrichment, every concept and subtype represented in **`### Ubiquitous Language`** must have a corresponding CRC block in **`### Class Responsibility Collaborator`**. No concept may be silently dropped. Passing means every concept is accounted for. Failing means a concept exists in the Ubiquitous Language but has no CRC block.

## DO

- Create a CRC block for each `#### **ConceptName**` heading under `### Ubiquitous Language`.

  **Example (pass):** Ubiquitous Language lists `#### **Check**`, `#### **Difficulty Class**`, `#### **Trait`** — CRC section has blocks for `Check`, `Difficulty Class`, and `Trait`.

- Create a CRC block for each subtype the sketch records (however phrased — e.g. bullets or wording that establishes *is a type of* / specialization), using `#### **ChildConcept : ParentConcept**` in the CRC section.

  **Example (pass):** Ubiquitous Language establishes that Saving Throw is a kind of Check — CRC has `#### **Saving Throw : Check**` with delta responsibilities only.

## DO NOT

- Drop a concept without creating a CRC block for it.

  **Example (fail):** `#### **Trait**` appears under `### Ubiquitous Language` but no CRC block addresses `Trait`.

- Introduce a CRC block that has no corresponding concept in the Ubiquitous Language.

  **Example (fail):** A CRC block for `Resolution Engine` appears but no concept in the Ubiquitous Language supports it.

**Source:** Engagement convention (class-responsibility-collaborator skill).
