# Rule: Rules open with plain pass-and-fail prose

**Scanner:** Manual review

A normative rule should stand on its own: right after the scanner line, use **ordinary prose** (one or two short paragraphs) to say **what passing looks like** and **what failing looks like** for a **named artifact**, without separate **Valid:** / **Invalid:** headings. Then **`## DO`** holds at least one checkable **pass** condition and **`## DO NOT`** at least one **fail** condition; more bullets are fine. The file must not be only a pointer to another rule for those conditions. If the opening is all “see elsewhere” or the bullets need workshop memory instead of file text, the rule fails.

## DO

- Open with prose paragraphs that state pass and fail in plain language so a reviewer knows the bar before **`## DO`**.

  **Example (pass):** First paragraph: “After a rule edit, **`SKILL.md`**’s bundle block matches **`rules/*.md` on disk.” Second paragraph: “Failure is an inlined rule that still shows old wording, or a **`scanner:`** with no script.”

- Give **at least one** **`## DO`** bullet with a checkable condition (file, section, marker, pattern).

  **Example (pass):** “**DO** run **`bundle_rules_into_skill_md.py`** on the skill root after any change under **`rules/`**.”

- Give **at least one** **`## DO NOT`** bullet with a concrete failure mode.

  **Example (pass):** “**DO NOT** set **`scanner: foo`** when **`scanners/foo-scanner.py`** does not exist.”

## DO NOT

- Replace the whole rule with cross-references so nobody can pass/fail from **this** file alone.

  **Example (fail):** “Mechanics for **`common`**: filenames, bundling, **`scanner:`**. For **DO**, **DO NOT**, **Examples**, see **Target rule files are checkable specs for named artifacts**.” — no local conditions in **this** file.

- Write **DO** bullets that need workshop context or memory — not decidable from the artifact.

  **Example (fail):** “**DO** ensure the team agreed in the room” — not checkable on a saved file.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).
