# Rule: State marker is domain-model

After this skill runs, the module file's YAML front matter must contain `state: class-model`. Passing means the marker is present and correct. Failing means the marker is missing, still shows a previous state, or has a typo.

## DO

- Set the front matter to exactly `state: class-model`.

  **Example (pass):**
  ```
  ---
  state: class-model
  ---
  ```

## DO NOT

- Leave the state at `domain model` (the previous step).

  **Example (fail):**
  ```
  ---
  state: class-model
  ---
  ```

- Omit the front matter entirely.

  **Example (fail):** File starts with `## Module:` and has no YAML front matter.
