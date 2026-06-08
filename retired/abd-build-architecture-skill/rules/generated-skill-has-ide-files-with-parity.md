### Rule: Generated skill ships ide-files with .mdc and .instructions.md body parity

Every generated implementation skill must ship an `ide-files/` folder containing **three** files: `<skill-name>.mdc`, `<skill-name>.instructions.md`, and `<skill-name>.prompt.md`. The `.mdc` and `.instructions.md` files must have **byte-equivalent bodies after normalization** — same headings, same bullets, same paths — because they are deployed to Cursor (`.mdc`) and VS Code (`.instructions.md`) and must teach the same agent the same way. The `.prompt.md` file is intentionally a different, short "run this skill" invocation, not the rule body. Passing means the three files exist, the `.mdc` and `.instructions.md` bodies match, and the `mdc-instructions-parity` scanner reports PASS on the generated skill. Failing means one of the three is missing, the bodies have drifted, or `.prompt.md` has been confused with the `.mdc`.

#### DO

- Create `ide-files/<skill-name>.mdc` with YAML frontmatter (`description:` plus `alwaysApply: true`) and an instruction body that names the skill and points at `SKILL.md`.

  **Example (pass):**
  ```markdown
  ---
  description: Generate <arch> modules from the reference document
  alwaysApply: true
  ---

  # Run <arch>-technical-architecture

  Read `architecture-centric-engineering/skills/<arch>-technical-architecture/SKILL.md`...
  ```

- Create `ide-files/<skill-name>.instructions.md` whose entire content is the body of the `.mdc` after the frontmatter, byte-identical after newline normalization.

  **Example (pass):** Diffing the two files after stripping the `.mdc` YAML header yields zero differences.

- Create `ide-files/<skill-name>.prompt.md` as a separate, short slash-command invocation with its own frontmatter (`description:` only).

  **Example (pass):**
  ```markdown
  ---
  description: Run <arch>-technical-architecture to generate a module
  ---

  Read **`architecture-centric-engineering/skills/<arch>-technical-architecture/SKILL.md`** and follow the Build steps.
  ```

- After generating the three files, run the parity scanner:

  ```bash
  python skill-helpers/skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
    --skill-root skill-builder/skills/abd-author-practice-skill \
    --workspace C:/absolute/path/to/architecture-centric-engineering/skills/<arch>-technical-architecture
  ```

  Confirm it reports PASS for `mdc-instructions-parity`.

#### DO NOT

- Ship only `.mdc` and `.prompt.md` and skip `.instructions.md` because "VS Code is not used here".

  **Example (fail):** `ide-files/` contains `<skill-name>.mdc` and `<skill-name>.prompt.md` only. The parity scanner reports MISSING `.instructions.md` and the skill cannot deploy to VS Code.

- Treat `.prompt.md` as the twin of `.mdc` and skip `.instructions.md`.

  **Example (fail):** The body of `.prompt.md` is the full instruction set and `.instructions.md` is empty. The Cursor command becomes a wall of text and VS Code parity is missing.

- Edit `.mdc` and forget to update `.instructions.md`.

  **Example (fail):** A new bullet "After scanners pass, run vitest" is added to `.mdc`; `.instructions.md` still has the previous three bullets. The parity scanner reports MISMATCH.

**Source:** Practice-skill authoring convention (abd-build-architecture-skill); enforces the same parity rule bundled in `abd-author-practice-skill` (mdc-instructions-parity).
