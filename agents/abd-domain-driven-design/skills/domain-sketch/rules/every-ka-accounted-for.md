# Rule: Every Key Abstraction accounted for in a concept

**Scanner:** Manual review

After domain-sketch enrichment, every Key Abstraction from the `## Key Abstractions` section must appear in at least one `### Concept` block — either directly, merged with another, split into multiple, or renamed. No Key Abstraction may be silently dropped. Passing means every KA has a traceable concept. Failing means a KA exists in the Key Abstractions section but has no corresponding concept.

## DO

- Create at least one `### Concept` block for each Key Abstraction.

  **Example (pass):** KA `### Check` becomes `### Check` concept block with intent, behaviors, collaborations.

- When merging or splitting KAs, note the mapping so a reviewer can trace it.

  **Example (pass):** "Combines KA Check and KA Difficulty Class into a single Check concept" noted in the intent paragraph.

## DO NOT

- Drop a Key Abstraction without creating a concept for it.

  **Example (fail):** `### Trait` exists as a Key Abstraction but no concept block mentions Trait — it simply vanished.

- Create a concept that does not trace back to any Key Abstraction or source material.

  **Example (fail):** A concept block for "Resolution Engine" appears but no KA or source passage supports it.

**Source:** Engagement convention (domain-sketch skill).
