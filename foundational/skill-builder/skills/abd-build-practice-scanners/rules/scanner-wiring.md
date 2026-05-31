# Rule: Scanner wiring

**Scanner:** Manual review

Each **`scanner:`** in rule frontmatter must have a matching **`scanners/<stem>-scanner.py`** on disk. The stem in the YAML field and the Python filename must be identical. Rules live only in **`rules/*.md`** — there is no bundled block to sync after scanner changes.

## DO

- **Implement first, then tag** — **`scanners/<stem>-scanner.py`** exists and runs before **`scanner: <stem>`** appears in **`rules/<stem>.md`**.

  **Example (pass):** `rules/titles.md` has `scanner: titles` and `scanners/titles-scanner.py` is present and executable.

- Keep scanner stem and rule filename aligned — one rule file, one scanner script.

  **Example (pass):** `rules/story-title-shape.md` with `scanner: story-title-shape` and `scanners/story-title-shape-scanner.py`.

## DO NOT

- Add **`scanner:`** to sell rigor when the script is missing or stub-only.

  **Example (fail):** `rules/layout.md` has `scanner: layout` but `scanners/layout-scanner.py` does not exist.

- Use this pass to **rewrite** rule meaning — fix scanners or rule text in **small**, reviewable steps.

  **Example (fail):** Changing the DO/DO NOT prose of a rule during the scanner-wiring pass — that belongs in the abd-author-practice-skill pass.

**Source:** Practice-skill builder convention (abd-build-practice-scanners).
