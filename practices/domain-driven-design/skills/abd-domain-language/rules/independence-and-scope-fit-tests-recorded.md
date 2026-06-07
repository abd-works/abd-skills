# Rule: Independence and scope-fit tests recorded in Decisions made

**Scanner:** Manual review

Every term placement decision — keep under a KA, move to boundary, or move out — must be recorded in the KA's `### Decisions made` block. The two tests are the **independence test** (does this concept have meaning on its own?) and the **scope-fit test** (does this concept fundamentally connect to the core purpose of the scope being modeled?). Decisions are gathered once per KA after all concept blocks. Passing means a reviewer can read the KA's `### Decisions made` and find every typing call and placement call. Failing means placements are silent, or decisions repeat per-concept instead of gathering per-KA.

## DO

- Record the independence test result for any term where the call mattered.

  **Example (pass):**
  ```
  ### Decisions made
  - *Degree of success* stays under *Check* — it has no meaning outside a *check* (independence test).
  ```

- Record the scope-fit test result for terms placed in the Boundary Domain or moved out.

  **Example (pass):**
  ```
  ### Decisions made
  - *Power effect* is owned by the *Power* module — it has broad meaning outside this scope (scope-fit test).
  ```

- Record typing decisions (concept vs property vs subtype vs instance) in the same block.

  **Example (pass):** `- *d20* is the instrument a *check* rolls — a property, not a concept.`

## DO NOT

- Place a term without any record of the decision.

  **Example (fail):** `### degree of success` appears under `## Check` with no `### Decisions made` anywhere explaining why it is there instead of its own KA.

- Repeat `### Decisions made` after each individual concept instead of collecting them per-KA.

  **Example (fail):**
  ```
  ### check
  - …
  ### Decisions made    ← per-concept; wrong for this skill
  - *d20* is a property.
  ### difficulty class
  - …
  ### Decisions made    ← repeated per-concept
  ```

**Source:** Inherited from abd-domain-language; scope-fit replaces module-fit to allow multi-module scope.
