# Rule: Every CRC block has at least one "not responsible for" rejection

**Scanner:** Manual review

Every CRC block must include a non-empty `not_responsible:` line that explicitly rejects at least one plausible misplaced concern. Passing means every block names something the concept must not own. Failing means the line is missing, empty, or contains only a placeholder.

## DO

- State a concrete behavior that someone might mistakenly assign to this concept, and reject it.

  **Example (pass):**
  ```
  Check
      responsible: resolves whether an attempted action succeeds or fails
      not_responsible: does not own the narrative consequence of failure — that belongs to the calling rule or encounter context
      collaborators: Difficulty Class, Modifier
  ```

- When possible, name where the rejected concern actually belongs.

  **Example (pass):** `not_responsible: does not determine the base DC — that is the Difficulty Class's responsibility`

## DO NOT

- Omit the `not_responsible:` line entirely.

  **Example (fail):**
  ```
  Check
      responsible: resolves whether an attempted action succeeds or fails
      collaborators: Difficulty Class, Modifier
  ```

- Use a generic placeholder that rejects nothing specific.

  **Example (fail):** `not_responsible: N/A` or `not_responsible: nothing to note`

**Source:** Engagement convention (class-responsibility-collaborator skill).
