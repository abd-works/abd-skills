# Rule: SKILL.md bundle matches rules/*.md files; scanner stem matches Python filename

**Scanner:** Manual review

On the **target** package, each **normative rule** is a **file** under **`rules/`** named **`something.md`**. After you edit any of those **`.md`** files, **`SKILL.md`** must be bundled so the inlined HTML block between **`execute_rules:bundle_rules`** markers contains the **same** text as the **`rules/<same-stem>.md`** file on disk — that is a **filename-to-content sync** check, not a vague “bundle” nod. In rule YAML, **`scanner: <stem>`** is allowed **only** if the **file** **`scanners/<stem>-scanner.py`** exists (same **stem** in both the field and the **Python filename**). Failure is stale inlined text, a **`scanner:`** stem with no matching **`.py`** file, or one **`scanner:`** stem pretending to cover unrelated **`rules/*.md`** topics.

## DO

- After you change any **`rules/<name>.md`** on the **target** package, run **`bundle_rules_into_skill_md.py`** with **`--skill-root`** set to that skill’s root so the **inlined** copy in **`SKILL.md`** matches that **`.md`** file’s current contents.

  **Example (pass):** You edit **`skills/foo/rules/naming.md`**, run `python skills/common/scripts/bundle_rules_into_skill_md.py --skill-root skills/foo`, open **`skills/foo/SKILL.md`**, search for the **### Rule** heading that corresponds to **`naming.md`**, the inlined **DO** text matches **`rules/naming.md`**.

- Set **`scanner: <stem>`** in the **rule file’s YAML** only when **`scanners/<stem>-scanner.py`** exists on that package (**stem** repeated exactly in the **scanner Python filename**).

  **Example (pass):** **`rules/titles.md`** has frontmatter **`scanner: titles`** and the file **`scanners/titles-scanner.py`** is present beside **`rules/`**.

- Keep **one** **`rules/<topic>.md`** per validation concern; when a scanner exists, align **`scanner:`** **stem** with the **topic** and the **`scanners/<stem>-scanner.py`** **filename**.

  **Example (pass):** **`rules/story-title-shape.md`** owns title-shape checks; **`scanner: story-title-shape`** and **`scanners/story-title-shape-scanner.py`** use the same stem.

## DO NOT

- Declare **`scanner: layout`** in **`rules/layout.md`** (or any rule) when **`scanners/layout-scanner.py`** is missing — the **YAML stem** must name a real **`.py`** file.

  **Example (fail):** **`rules/layout.md`** has **`scanner: layout`** but there is no **`layout-scanner.py`** under **`scanners/`**.

- Leave **`SKILL.md`** with an inlined rule that does not match the current **`rules/<stem>.md`** file after an edit (no re-bundle).

  **Example (fail):** **`rules/evidence.md`** on disk adds a **DO NOT** bullet, but **`SKILL.md`** still inlines the old text without that bullet.

**Source:** `skills/common` target layout convention.
