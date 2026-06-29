# Rule: State marker is domain-specification

After this skill runs, the module file's YAML front matter must contain `state: domain-specification`. Passing means the marker is present and correct. Failing means the marker is missing, still shows a previous state, or has a typo.

## DO

- Set the front matter to exactly `state: domain-specification`.

  **Example (pass):**
  ```
  ---
  state: domain-specification
  ---
  ```

## DO NOT

- Leave the state at `domain-model` (the previous step).

  **Example (fail):**
  ```
  ---
  state: domain-model
  ---
  ```

- Omit the front matter entirely.

  **Example (fail):** File starts with `## Module:` and has no YAML front matter.
