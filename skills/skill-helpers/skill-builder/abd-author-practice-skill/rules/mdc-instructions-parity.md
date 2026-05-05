---
scanner: mdc-instructions-parity
---

# Rule: `.mdc` body matches `.instructions.md` (VS Code parity)

On the **target** skill package, every **Cursor rule** ( **`*.mdc`** ) lives under **`ide-files/`** next to **`SKILL.md`** (legacy: skill root only if **`ide-files/`** is absent). Each **`.mdc`** must have a **paired** **`<same-stem>.instructions.md`** in the **same folder** so VS Code gets the **same** always-on text. The **markdown body** of the **`.mdc`** (everything **after** the YAML frontmatter block) must be **byte-for-byte the same** as the **entire** **`.instructions.md`** file after **normalization** (line endings → LF, trim trailing spaces per line, trim leading/trailing blank lines). The **`.prompt.md`** slash-command file is **deliberately different** — it is a short invocation, not the rule body — and is **not** compared to the **`.mdc`**. Failure is a missing pair, or mismatched bodies between **`.mdc`** and **`.instructions.md`**.

## DO

- Keep **`<stem>.instructions.md`** as the **exact same prose** as **`<stem>.mdc`** without the `---` … `---` header (same headings, bullets, and paths). Edit one, then mirror the other, or edit **`.mdc`** and copy the body to **`.instructions.md`**.

  **Example (pass):** **`foo.mdc`** has frontmatter plus “# Run foo …” and three bullets; **`foo.instructions.md`** is only “# Run foo …” and those three bullets — identical after normalization.

- Run **`mdc-instructions-parity-scanner`** on the **target** skill root when validating ( **`--skill-root`** = **abd-author-practice-skill**, **`--workspace`** = **`skills/<target>/`** ).

  **Example (pass):** `python skills/execute-skill-using-skills-rules/scripts/run_scanners.py --skill-root skills/abd-practice-skill-builder/abd-author-practice-skill --workspace C:/dev/agilebydesign-skills/skills/correct_output` reports **PASS** for **mdc-instructions-parity**.

  **Example (fail):** `...\run_scanners.py ... --workspace skills/correct_output` from a shell whose cwd is not the repo root — the path resolves under the authoring skill and is wrong; use an **absolute** `--workspace`.

## DO NOT

- Change **`.mdc`** body text without updating **`.instructions.md`** to match (or the reverse).

  **Example (fail):** **`correct-output.mdc`** adds a fourth bullet; **`correct-output.instructions.md`** still has three bullets — scanner reports mismatch.

- Treat **`.prompt.md`** as the rule twin of **`.mdc`** — it is the **command** payload, not the always-on instruction file.

  **Example (fail):** Deleting **`.instructions.md`** because “**`.prompt.md`** is enough” — VS Code always-on parity is missing.

**Source:** deployable IDE file convention (abd-author-practice-skill **Build** step 8–9).
