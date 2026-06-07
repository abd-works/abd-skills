# Rule: Slash terms resolved before CRC

**Scanner:** Manual review

Any concept named `A / B` in the Domain Language must be resolved to one canonical name before writing CRC blocks. Slash terms are acceptable in Domain Language headers as working hedges, but must not appear in CRC headings or responsibility names.

## DO

- Choose one canonical name and use it consistently throughout the domain model section.

  **Example (pass):** Domain Language has `#### **Check Result / Graded Check Result**` → CRC uses `#### **Check Result**` throughout; "graded" behavior is expressed via invariants.

- Note the resolution in the Decisions section if the choice is non-obvious.

  **Example (pass):** "Decisions: Check Result / Graded Check Result resolved to Check Result — graded behavior is an invariant, not a separate concept."

## DO NOT

- Use slash notation in any CRC heading or block.

  **Example (fail):** `#### **Check Result / Graded Check Result**` appears in the domain model section.

- Use one name in the heading and the other in collaborator columns.

  **Example (fail):** Heading is `#### **Check Result**` but collaborator column references `Graded Check Result` elsewhere.

**Source:** Engagement convention (class-responsibility-collaborator skill).
