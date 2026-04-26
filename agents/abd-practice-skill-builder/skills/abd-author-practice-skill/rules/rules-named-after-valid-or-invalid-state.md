# Rule: Rules named after valid or invalid state

**Scanner:** Manual review

Each normative check lives in its **own file** under **`rules/`**, and that file’s **name** is the **`*.md` basename** in **kebab-case** (everything before **`.md`**). That **filename** must read like the **outcome or state** you guard — what “good” means or what bad state you forbid — so someone can guess the check before opening the file. This rule is **about those rule markdown filenames**, not about prose inside **`SKILL.md`**. Naming fails when the basename is a vague quality label with **no** object (**`skill-valid-grammar`**), or when it names **only** a tool or folder (**`rules-files-and-bundle`**, **`execute-rules-steps`**) instead of the **verified outcome**.

## DO

- Name **`rules/<basename>.md`** after the **valid state** you want (or the **invalid** one you forbid), so **`basename`** reads like **`clear-english-on-every-skill-section`** — **what** must hold.

  **Example (pass):** **`rules/clear-english-throughout-skill-page.md`** — the pass condition is in the **filename**.

- Make **`# Rule:`** in that **`.md`** file match the same idea in normal English (title aligns with **`basename`**).

  **Example (pass):** File **`rules/templates-include-ideal-filled-examples-for-audience.md`**, title **`# Rule: Templates include ideal filled examples for the audience`**.

## DO NOT

- Use **`rules/<basename>.md`** names like **`skill-valid-grammar`** or **`valid-structure`** where **grammar** / **structure** has **no scope** (which artifact).

  **Example (fail):** **`rules/skill-valid-grammar.md`** — valid grammar **on what file or section**?

- Use a **basename** that only names plumbing (**`rules-and-bundle`**, **`files-and-bundle`**, **`misc-wiring`**) when the rule is really about a **checkable outcome** (then the **`.md`** name should say that outcome).

  **Example (fail):** **`rules/rules-files-and-bundle.md`** for “inlined **SKILL.md** matches **`rules/*.md`** and **`scanner:`** matches **`scanners/<stem>-scanner.py`**” — the **filename** should say **that**, e.g. **`skill-md-bundle-matches-rules-md-files-scanner-stem-matches-py-filename.md`**.

- Name the file after **only** a script or CLI when the rule is about an **artifact condition**; the **`rules/*.md`** name should describe the **pass/fail on disk**, not the command you ran.

  **Example (fail):** **`rules/run-bundle-script.md`** when the real check is **bundle content matches **`rules/naming.md`**, etc.**

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).
