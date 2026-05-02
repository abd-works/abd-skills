---
---

# Rule: State marker is business-logic

After this skill runs, the module file's YAML front matter must contain `state: business-logic`. Passing means the marker is present and correct. Failing means the marker is missing, still shows a previous state, or has a typo.

## DO

- Set the front matter to exactly `state: business-logic`.

  **Example (pass):**
  ```
  ---
  state: business-logic
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
