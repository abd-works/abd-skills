# Rule: State marker is domain-model

After this skill runs, the module file's YAML front matter must contain `state: domain-model`. Passing means the marker is present and correct. Failing means the marker is missing, still shows a previous state, or has a typo.

## DO

- Set the front matter to exactly `state: domain-model`.

  **Example (pass):**
  ```
  ---
  state: domain-model
  ---
  ```

## DO NOT

- Leave the state at `crc` (the previous step).

  **Example (fail):**
  ```
  ---
  state: crc
  ---
  ```

- Omit the front matter entirely.

  **Example (fail):** File starts with `## Module:` and has no YAML front matter.
