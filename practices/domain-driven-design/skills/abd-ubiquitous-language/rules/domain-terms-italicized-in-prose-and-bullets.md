# Rule: Domain terms italicized in prose and bullets; every term has a concept block

**Scanner:** Python — `domain-terms-coverage-scanner.py`

Every domain term in a behavior bullet, invariant, or KA intro paragraph must be italicized using `*term*`. Passing means every occurrence of every domain term is italicized consistently throughout the file. Failing means some occurrences are plain text, or non-domain words are italicized.

Every term listed in the **Terms** header must have a corresponding concept block (or subtype/property stub) in the body — no term is listed and then silently absent from Core Domain. Failing means a term appears in the Terms list but has no `### term` heading anywhere under `# Core Domain`.

## DO

- Italicize every domain term in behavior bullets, invariants, and KA intro paragraphs.

  **Example (pass):**
  ```
  - is resolved by *rolling* a *d20*, adding the *trait rank* and the *circumstance modifier*,
    comparing the *roll total* to the *difficulty class*, producing a *check result*
  ```

- Italicize terms consistently — if `*check*` is italicized in one bullet, italicize it everywhere.

  **Example (pass):** `*check*` appears 15 times in the file, italicized every time.

## DO NOT

- Leave domain terms as plain text in behavior bullets.

  **Example (fail):**
  ```
  - is made using the trait of a character
  ```

- Italicize only some occurrences of a domain term.

  **Example (fail):** `*check*` italicized in the first bullet, plain `check` three bullets later.

- Italicize non-domain words (articles, prepositions, connectives).

  **Example (fail):** `- *is* *made* *using* *the* *trait*`

## DO (terms coverage)

- Give every term in the **Terms** list a `### term` concept block, subtype heading, or property stub under `# Core Domain`.

  **Example (pass):** `**Terms**` lists *rank*; `### rank` appears under `## Trait` in Core Domain.

## DO NOT (terms coverage)

- List a term in **Terms** and have no heading for it anywhere in Core Domain.

  **Example (fail):** `**Terms**` lists *degree of success*; no `### degree of success` heading exists anywhere under `# Core Domain`.

**Source:** Inherited from abd-ubiquitous-language — check-resolution engagement adopted as standard.
