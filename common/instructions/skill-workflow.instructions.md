---
description: Shared execution workflow for all practice skills — output path resolution, read-gates, validation, diagram delegation, and correction loop.
alwaysApply: false
---

# Skill Workflow

Apply this when executing any practice skill. It governs how you resolve output paths, gate on rules, validate, and correct.

---

## Output path resolution

When a skill asks you to write deliverables, resolve `<deliverables-folder>` in this order (first match wins):

1. **The path the user told you.** If the user names a file or folder, use it exactly.
2. **`cdd-context-index.md` at the workspace root.** If this file exists and lists a path for this artifact, use that path and update the row if it changes.
3. **Where prior phase output already lives.** If earlier phases already wrote into a folder, put new output next to them in the same folder.
4. **Canonical scaffold path.** Use the path for this skill from `common/folder-conventions.md`.
5. **Workspace root.** Last resort only.

---

## Read-gates (hard gate — no exceptions)

Before authoring any artifact, read in this order:

1. **`rules/`** — every file for the active skill.
2. **`reference/`** — concepts, examples, teaching (**not** `input-traps.md` or `diagram-workflow.md` yet).
3. **`reference/input-traps.md`** — check each trap against available input.
4. **Practice family `reference/`** — any shared files linked from `SKILL.md` or `reference/concepts.md`.
5. **Grill mode only** — if invocation includes **"grill me"**, read `common/grill-me-with-practice-skill.md`.

Do not rely on memory or the SKILL body alone. Steps 1–4 always; step 5 when grill mode is active.

---

## Validate output

After generating, do both passes.

**A — Per-rule verdict:** Re-read `rules/`. Emit PASS/FAIL per rule. Apply practice-family `validate-checklist.md` when linked.

**B — Scanner pass:**

```bash
python <common_root>/scripts/run_scanners.py --skill-root <path-to-skill> --workspace <path-to-output>
```

---

## Diagram workflow (non-blocking)

After the scanner pass, if the active skill has **`reference/diagram-workflow.md`**, launch a **background sub-agent** with that file's contents. Do not wait for the sub-agent before returning to the user.

---

## Correction process

When something is wrong: identify → log → re-generate → iterate until correct, then optionally improve the source skill. See `skill-helpers/instructions/log-and-fix-skill-errors` for the full loop.
