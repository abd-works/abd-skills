# Skill Workflow

Read this file when any practice skill tells you to. It defines the shared workflow for executing any skill using its rules.

---

## Output file resolution (deliverables)

**Where to write** — resolve `<deliverables-folder>` in this order:

1. **The path the user told you to use.** If the user names a file or folder, use exactly that.
2. **`cdd-context-index.md` at the workspace root.** If this file lists a path for this artifact, use that path. Update the row if it changes.
3. **Where the engagement already keeps deliverables.** Write next to existing phase output in the **same** folder.
4. **Canonical scaffold path** from [`folder-conventions.md`](./folder-conventions.md) for the active skill.
5. **The workspace root.** Last resort only.

**File name** — after the folder is resolved:

1. If the active skill has **`reference/output.md`**, read it for file name, naming pattern, or non-`docs/` rules (e.g. project test folder).
2. Otherwise use the file name in [`folder-conventions.md`](./folder-conventions.md) for this skill (typically `<artifact-stem>.md`).
3. Add a `<name>-` prefix only when disambiguation is needed.

Most skills need no `reference/output.md` — `folder-conventions.md` is enough. Add `reference/output.md` only when the skill breaks the default (tests in project tree, multiple named outputs, non-`.md` deliverable).

---

## Read-gates

Before authoring any artifact — **hard gate, no exceptions.** Read in this order:

1. **`rules/`** — every file for the active skill.
2. **`reference/`** — concepts, examples, and other teaching files (**not** `input-traps.md`, `diagram-workflow.md`, or `output.md` yet).
3. **`reference/input-traps.md`** — check each trap against available input; flag gaps; do not assume away ambiguities this skill names.
4. **Practice family `reference/`** — read any shared files linked from the active skill's `SKILL.md` or `reference/concepts.md` (e.g. `handling-incomplete-context.md`, `diagram-workflow.md`, `domain-input-priority.md` at practice level).
5. **Grill mode only** — if the invocation includes **"grill me"**, read [`grill-me-with-practice-skill.md`](./grill-me-with-practice-skill.md) and work through unresolved traps as questions (one at a time) before generating.

Do not rely on memory or the SKILL body alone. No main task starts until steps 1–4 are done (and step 5 when grill mode is active).

---

## Validate output (AI pass + scanner pass)

After generating, do **both**. Together they are the answer to "does this match the rules?"

**A — Per-rule verdict (AI pass):** Re-read every file in **`rules/`**. For **each rule**, emit:

```
Rule: <rule-filename>  ->  PASS
Rule: <rule-filename>  ->  FAIL  <offending line or reason>
```

No rule may be silently skipped. Fix every FAIL before calling the work done.

When the active skill links to a practice-family **`validate-checklist.md`**, apply those shared items in addition to skill-specific `## Validate` bullets.

**B — Scanner pass:**

```bash
python <common_root>/scripts/run_scanners.py --skill-root <path-to-skill> --workspace <path-to-output>
```

Add `--language <lang>` (e.g. `python`, `javascript`) when scanners live in `scanners/<lang>/`. Save the report to `scanner-report/` in the workspace. Fix all violations and re-run.

---

## Diagram workflow (non-blocking)

After the scanner pass, check whether the active skill has **`reference/diagram-workflow.md`**. If it does, launch a **background sub-agent** (Task tool, `run_in_background: true`) with that file's contents and enough context (deliverables folder, output paths) for it to execute the CLI command independently. Do not wait for the sub-agent before returning to the user.

---

## Correction process

When something is wrong: identify → log → re-generate → iterate on the output until correct, then optionally improve the source skill. See `skill-helpers/instructions/log-and-fix-skill-errors` for the full loop. Put the log under the engagement tree — not inside the skill package.
