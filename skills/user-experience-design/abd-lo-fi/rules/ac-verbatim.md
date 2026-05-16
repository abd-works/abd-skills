# Rule: Acceptance criteria appear on the canvas verbatim

**Scanner:** AI review

Every acceptance criterion attached to the wireframe is copied character-for-character from the acceptance-criteria source file. Story headings, numbering, clause wording, and the `WHEN / THEN / AND / BUT` structure are preserved exactly. Reworded, merged, or shortened criteria are a fail.

## DO

- Copy each criterion exactly, including its number and any `WHEN / THEN / AND / BUT` keywords as the source writes them.

  **Example (pass):**
  ```
  Story: Validate City of Heroes Game Directory
  1. WHEN the application starts THEN the system checks that the stored
     COH game directory path exists on disk and contains the expected content
     AND proceeds to open the crowd manager if the check passes
  ```

- Preserve story headings as the source writes them.

  **Example (pass):** Source: `Story: Prompt for Game Directory if Invalid`. Canvas attaches: `Story: Prompt for Game Directory if Invalid` — same wording, same capitalisation.

## DO NOT

- Reword a criterion for "clarity".

  **Example (fail):** Source: `WHEN no COH game directory is stored THEN the check fails immediately AND the GM is prompted to supply a path before startup continues`. Canvas: `If no path is stored, prompt the user before continuing`. Reworded — fail.

- Merge two criteria into one.

  **Example (fail):** Source has criteria 1 and 2 as separate clauses. Canvas combines them into a single bullet.

- Drop a criterion because it is "the same as another" or "covered elsewhere".

  **Example (fail):** Canvas shows criterion 1 but skips criterion 3 because "they overlap". They are different clauses with different conditions; both belong on the canvas.

- Renumber, reorder, or restyle the criteria.

  **Example (fail):** Source numbers `1.`, `2.`, `3.`. Canvas uses bullets, or reorders, or relabels them `a.`, `b.`, `c.`.
