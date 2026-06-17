# Rule: State marker is crc

**Scanner:** Manual review

After this skill runs, the module file's YAML front matter must contain `state: crc`. Passing means the marker is present and correct. Failing means the marker is missing, still shows a previous state, or has a typo.

## DO

- Set the front matter to exactly `state: crc`.

  **Example (pass):**
  ```
  ---
  state: crc
  ---
  ```

## DO NOT

- Leave the state at `ubiquitous-language` (the previous step).

  **Example (fail):**
  ```
  ---
  state: ubiquitous-language
  ---
  ```

- Omit the front matter entirely.

  **Example (fail):** File starts with `## Module:` and has no YAML front matter.

**Source:** Engagement convention (class-responsibility-collaborator skill).
