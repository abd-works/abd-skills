# Skill Workflow

Read this file when any practice skill tells you to. It defines the shared workflow for executing any skill using its rules.

---

## Output file resolution (deliverables)

**Where to write deliverables (`<deliverables-folder>` resolution):**

1. **The path the user told you to use.** If the user names a file or folder, use exactly that.
2. **`cdd-context-index.md` at the workspace root.** If this file exists and lists a non-standard path for this artifact, use that path. Update the row if the path changes.
3. **Where the engagement already keeps deliverables.** Look at the workspace; if previous phase output already lives in a folder, write next to them in the **same** folder.
4. **Canonical scaffold path.** If none of the above applies, use the path for this skill from [`common/folder-conventions.md`](./folder-conventions.md). The scaffold tree there defines the default `docs/` subtree for every skill family.
5. **The workspace root.** Last resort only.

---

## Read-gates

Before authoring any artifact — **hard gate, no exceptions:**

- Read every file in **`rules/`** for the active skill.
- Read every file in **`reference/`** for the active skill. Treat each DO / DO NOT as a hard contract, not a suggestion.

Do not rely on memory or the SKILL body alone. No main task starts until this gate is done.

---

## Validate output (AI pass + scanner pass)

After generating, do **both**. Together they are the answer to "does this match the rules?"

**A — Per-rule verdict (AI pass):** Re-read every file in **`rules/`**. For **each rule**, emit:

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

After the scanner pass, re-read the active skill's `SKILL.md` and check whether it contains a `## Diagram workflow` section. If it does, launch a **background sub-agent** (Task tool, `run_in_background: true`) with the diagram workflow section contents and enough context (deliverables folder, output paths) for it to execute the CLI command independently. Do not wait for the sub-agent before returning to the user.

---

## Correction process

When something is wrong: identify → log → re-generate → iterate on the output until correct, then optionally improve the source skill. See `skill-helpers/instructions/log-and-fix-skill-errors` for the full loop. Put the log under the engagement tree — not inside the skill package.
