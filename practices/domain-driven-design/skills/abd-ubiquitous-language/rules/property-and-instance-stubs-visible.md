# Rule: Property and instance stubs visible — no silently dropped terms

**Scanner:** AI review

Terms classified as properties, instances, or type properties get a stub heading (`### term_name`) with a brief classification bullet. This makes visible that the term was considered, rather than silently dropped. Passing means every term from the Terms list either gets its own concept block or a stub heading. Failing means a term appears in the Terms list or KA grouping but has no heading anywhere in the body.

## DO

- Give property and instance terms a stub heading with a one-line classification note.

  **Example (pass):**
  ```
  ### d20
  - is the instrument a *check* rolls — a property of *check*, not a separate concept
  ```

## DO NOT

- Silently drop terms without a stub heading.

  **Example (fail):** `*d20*` is in the Terms list and KA grouping but has no `### d20` heading anywhere in the body.

- Use a stub heading without a classification note.

  **Example (fail):**
  ```
  ### d20
  - rolls 1–20                          ← reads like behavior; classification missing
  ```

**Source:** Inherited from abd-ubiquitous-language — property and instance stubs visible.
