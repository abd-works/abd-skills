# Rule: Templates include ideal filled examples for the audience

**Scanner:** Manual review

Each **target** **`templates/`** file that **`SKILL.md`** promises should ship **at least one** worked example — a filled block, rows, or mini-sample — with enough **tone and depth** for **who reads that output** (sponsor, team session, ticket tool, as the practice says). Drill-only or stub templates must be **called out** in **`SKILL.md`**. You fail when a promised template is only headings and **`{{PLACEHOLDER}}`**, or when **`SKILL.md`** talks about quality but the template never shows a finished-looking fragment of that format.

## DO

- For each promised **`templates/`** file, include **at least one** filled example that matches the **audience** for that deliverable.

  **Example (pass):** **`templates/impact-map-hypotheses.md`** ends with an **Example** section: full hypothesis lines with realistic metrics, not only `{{impact_1_metric}}`.

- Say in **Instructions** or **`SKILL.md`** **who the example is for** when that is not obvious.

  **Example (pass):** “**Example** (sponsor readout): …” at the top of the example block.

- If a template is **drill-only** or **stubbed**, state that in **`SKILL.md`** like any other deferral.

  **Example (pass):** “**templates/drill-blank.md** is intentionally empty for classroom use; not used for delivery packages.”

## DO NOT

- Ship a promised template whose body is **only** scaffolding: headings, blank tables, placeholders, **no** completed sample.

  **Example (fail):** **`templates/bar.md`** is **## Fields** plus twenty `{{FIELD_N}}` lines and zero filled rows.

- Rely on **`SKILL.md`** alone for quality bar when the template never shows a **finished** fragment of that format.

  **Example (fail):** **`SKILL.md`** says “write clear hypotheses” but **`templates/hypotheses.md`** has no example paragraph a reader could mirror.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder); theme **G** in **`progress/corrections-log.md`**.
