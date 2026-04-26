# Rule: Validate section is inspection not rewrite

**Scanner:** Manual review

The **target** **`SKILL.md`** **Validate** section should read like a **critic checklist**: each line can be checked against **`SKILL.md`**, **`rules/`**, **`templates/`**, and **`inputs/`** as the skill actually promises. You close gaps and fix drift; you do not treat **Validate** as the place to rip up **Build** and re-sequence the whole method unless new evidence demands it. Failure is generic **Validate** bullets that ignore promised templates and scanners, or using the pass mainly to redesign workflow, or leaving hub claims in **`SKILL.md`** that contradict **`inputs/abd-answers-retrieval.md`** with no fix and no **Deferred** note.

## DO

- Read **`SKILL.md`** and **`rules/*.md`** **as a critic**: each rule’s **DO** / **DO NOT** / examples should let you mark a concrete artifact pass or fail.

  **Example (pass):** Open **`rules/naming.md`**, pick **`story-map.md`** from **`templates/`**, verify titles match **DO** / **DO NOT**.

- Walk the **target** **Validate** section line by line; add missing checks when **`SKILL.md`** promises templates, markers, or citations **Validate** never mentions.

  **Example (pass):** Skill promises four **`templates/`** files; **Validate** lists all four plus “each has filled example” if that is required.

- Confirm **no** leftover **`{{PLACEHOLDER}}`** unless **`SKILL.md`** explicitly defers that slice.

  **Example (pass):** Grep **`{{PLACEHOLDER}}`** on target **`SKILL.md`**; only absent or explained in a **Deferred** note.

- Confirm **at least one** **`rules/*.md`** when **`SKILL.md`** has **`execute_rules:bundle_rules`** markers.

  **Example (pass):** Bundle markers present; **`rules/`** has **`naming.md`** (or another normative file).

## DO NOT

- Treat **Validate** as optional boilerplate that does not match shipped templates, **scanner:** hooks, or retrieval claims.

  **Example (fail):** **Validate** says “check quality” while the skill promises **`scanners/`** and four templates — list does not mention them.

- Use the inspection pass mainly to **re-sequence** work; **Build** owns order.

  **Example (fail):** Rewriting **Build** steps 1–7 during **Validate** without a retrieval or scope change driving it.

- Leave **hub-backed** **`SKILL.md`** claims that contradict **`inputs/abd-answers-retrieval.md`** with no fix and no **Deferred** note.

  **Example (fail):** **Purpose** cites a method the hub chunks do not describe; no gap logged.

**Source:** Practice-skill authoring convention (abd-practice-skill-builder).
