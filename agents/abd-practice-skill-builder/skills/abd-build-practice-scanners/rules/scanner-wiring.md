# Rule: Scanner wiring

**Scanner:** Manual review

## DO

- **Implement first, then tag** — **`scanners/<stem>-scanner.py`** exists and runs before **`scanner: <stem>`** appears in **`rules/<stem>.md`**.
- **Re-bundle** after any **`rules/*.md`** or scanner change so **SKILL.md** stays truthful.

## DO NOT

- Add **`scanner:`** to **sell** rigor when the script is missing or stub-only.
- Use this pass to **rewrite** rule meaning — fix scanners or rule text in **small**, reviewable steps.

**Source:** Practice-skill builder convention (abd-build-practice-scanners).
