# Rule: Collaborators trace to sketch collaborations and subtype edges

**Scanner:** Manual review

The `collaborators:` line in each CRC block must list domain concepts that appear in the Object Sketch's collaboration lines or subtype edges for that concept. Concepts with no sketch collaborations must say `(none)` explicitly. Passing means every listed collaborator is traceable and no-collaborator blocks are marked. Failing means collaborators are invented, omitted without explanation, or left blank.

## DO

- List collaborators that correspond to sketch collaboration lines or subtype relationships.

  **Example (pass):** Sketch says "Check — collaborates with → Difficulty Class, Modifier"; CRC block has `collaborators: Difficulty Class, Modifier`.

- Write `(none)` when a concept has no sketch collaborations.

  **Example (pass):**
  ```
  Modifier
      responsible: represents a single numeric adjustment to a check
      not_responsible: does not combine itself with other modifiers — stacking is the Check's job
      collaborators: (none)
  ```

## DO NOT

- Invent collaborators that have no basis in the Object Sketch.

  **Example (fail):** CRC block lists `collaborators: Logger, EventBus` but neither concept appears anywhere in the sketch.

- Leave the collaborators line blank or omit it entirely.

  **Example (fail):**
  ```
  Check
      responsible: resolves whether an attempted action succeeds or fails
      not_responsible: does not own narrative consequences
      collaborators:
  ```

**Source:** Engagement convention (class-responsibility-collaborator skill).
