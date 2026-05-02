# Rule: Every concept from object sketch has a CRC block

**Scanner:** Manual review

After CRC enrichment, every concept and subtype heading from the Object Sketch section must have a corresponding CRC block in the CRC section. No concept may be silently dropped. Passing means every concept is accounted for. Failing means a concept exists in the Object Sketch but has no CRC block.

## DO

- Create a CRC block for each `### Concept` heading in the Object Sketch.

  **Example (pass):** Object Sketch has `### Check`, `### Difficulty Class`, `### Trait` — CRC section has blocks named `Check`, `Difficulty Class`, `Trait`.

- Create a CRC block for each `### Subtype *is a type of* Base` heading in the Object Sketch.

  **Example (pass):** Object Sketch has `### Saving Throw *is a type of* Check` — CRC section has a block `Saving Throw : Check`.

## DO NOT

- Drop a concept without creating a CRC block for it.

  **Example (fail):** `### Trait` exists in the Object Sketch but no CRC block mentions Trait — it simply vanished.

- Introduce a CRC block that has no corresponding concept in the Object Sketch.

  **Example (fail):** A CRC block for "Resolution Engine" appears but no concept heading in the sketch supports it.

**Source:** Engagement convention (class-responsibility-collaborator skill).
