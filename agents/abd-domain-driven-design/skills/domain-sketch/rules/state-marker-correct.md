# Rule: State marker is domain-sketch

**Scanner:** Manual review

After this skill runs, the module file's YAML front matter must contain `state: domain-sketch`. Passing means the marker is present and correct. Failing means the marker is missing, still shows a previous state, or has a typo.

## DO

- Set the front matter to exactly `state: domain-sketch`.

  **Example (pass):**
  ```
  ---
  state: domain-sketch
  ---
  ```

## DO NOT

- Leave the state at `key-abstractions` (the previous step).

  **Example (fail):**
  ```
  ---
  state: key-abstractions
  ---
  ```

- Omit the front matter entirely.

  **Example (fail):** File starts with `## Module:` and has no YAML front matter.

**Source:** Engagement convention (domain-sketch skill).
