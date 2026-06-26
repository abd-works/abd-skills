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

Before authoring any artifact:

- Read every file in **`rules/`** for the active skill.
- Read every file in **`reference/`** for the active skill. Treat every DO / DO NOT as a hard contract, not a suggestion.

Do not rely on memory or the SKILL body alone. The main task does not start until this gate is done.

---

## Validate output

After generating, do both passes. Together they answer "does this match the rules?"

**A — Per-rule verdict (AI pass):** Re-read every file in `rules/`. For **each rule** emit:

```
Rule: <rule-filename>  ->  PASS
Rule: <rule-filename>  ->  FAIL  <offending line or reason>
```

No rule may be silently skipped. Fix every FAIL before calling the work done.

**B — Scanner pass:**

```bash
python <common_root>/scripts/run_scanners.py --skill-root <path-to-skill> --workspace <path-to-output>
```

Add `--language <lang>` (e.g. `python`, `javascript`) when scanners live in `scanners/<lang>/`. Save the report to `scanner-report/` in the workspace. Fix all violations and re-run.

---

## Diagram workflow (non-blocking)

After the scanner pass, re-read the active skill's `SKILL.md` and check for a `## Diagram workflow` section. If present, launch a **background sub-agent** (`Task` tool, `run_in_background: true`) with the diagram workflow content and enough context (deliverables folder, output paths) for it to run the CLI command independently. Do not wait for the sub-agent before returning to the user.

---

## Correction process

When something is wrong: identify → log → re-generate → iterate until correct, then optionally improve the source skill. See `skill-helpers/instructions/log-and-fix-skill-errors` for the full loop. Put the log under the engagement tree — not inside the skill package.
