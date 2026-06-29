---
description: Shared execution workflow for all practice skills — output path resolution, read-gates, validation, diagram delegation, and correction loop.
alwaysApply: false
---

# Skill Workflow

**You were sent here from a practice skill's `SKILL.md`.** Read in full. Order: bootstrap → read-gates → generate → validate.

---

## Bootstrap (engagement context)

Before skill read-gates:

1. **`cdd-context-index.md`** at workspace root when present.
2. **Existing deliverables** for this scope (`common/skill-index.md` filenames).
3. **Decision records** — all relevant `DR-*.md` / `ADR-*.md` per `common/decision-record.md` (Accepted in full). Check `docs/decisions/` plus practice `decisions/` folders and session `decisions/` when applicable.

Write new DRs per `common/decision-record.md` when criteria are met.

---

## Output file resolution (deliverables)

**Where to write** — resolve `<deliverables-folder>` in this order:

1. **The path the user told you to use.** If the user names a file or folder, use exactly that.
2. **`cdd-context-index.md` at the workspace root.** If this file lists a path for this artifact, use that path. Update the row if it changes.
3. **Where the engagement already keeps deliverables.** Write next to existing phase output in the **same** folder.
4. **Canonical scaffold path** from `common/folder-conventions.md` for the active skill.
5. **The workspace root.** Last resort only.

**File name** — after the folder is resolved:

1. If the active skill has **`reference/output.md`**, read it for file name, naming pattern, or non-`docs/` rules (e.g. project test folder).
2. Otherwise use the file name in `common/folder-conventions.md` for this skill (typically `<artifact-stem>.md`).
3. Add a `<name>-` prefix only when disambiguation is needed.

Most skills need no `reference/output.md` — `folder-conventions.md` is enough.

---

## Read-gates (hard gate — no exceptions)

Before authoring any artifact, read in this order:

1. **`rules/`** — every file, **read in full**.
2. **`reference/`** — every file except `grill-me.md` (grill mode only — step 5), **read in full**.
3. **`templates/`** — every file in the skill's `templates/` folder, **read in full**.
4. **Practice `reference/`** — every file in `<family>-perspective.md` shared-reference table, plus every practice file linked from any file in this skill's `reference/` folder, **read in full**.
5. **Grill mode only** — read `common/grill-me-with-practice-skill.md` and the active skill's `reference/grill-me.md` in full; questions from `grill-me.md` only, not `input-traps.md`.

**Read each file in full** — no skimming or memory. Complete **Bootstrap** first, then steps 1–4 (and step 5 when grill mode is active).

---

## Generate

After read-gates: author to all `rules/`; one deliverable per `templates/` file; never copy template `## Instructions` into project files. Orchestration in `reference/generate.md` when present. Skill-specific steps are not in `SKILL.md`.

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
