---
scanner: state-marker-correct
---

# Rule: State marker is key-abstractions

After this skill runs, the module file's YAML front matter must contain `state: key-abstractions`. Passing means the marker is present and correct. Failing means the marker is missing, still shows a previous state, or has a typo.

## DO

- Set the front matter to exactly `state: key-abstractions`.

  **Example (pass):**
  ```
  ---
  state: key-abstractions
  ---
  ```

## DO NOT

- Leave the state at `domain-language` (the previous step).

  **Example (fail):**
  ```
  ---
  state: domain-language
  ---
  ```

- Omit the front matter entirely.

  **Example (fail):** File starts with `## Module:` and has no YAML front matter.

- Use a different field name or value.

  **Example (fail):** `stage: key-abstractions` or `state: ka` or `state: key_abstractions`.
