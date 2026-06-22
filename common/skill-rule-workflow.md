# Skill Rule Workflow

Read this file when any practice skill tells you to. It defines the shared workflow for executing any skill using its rules.

---

## Output file resolution (deliverables)

**Where to write deliverables (`<deliverables-folder>` resolution):**

1. **The path the user told you to use.** If the user names a file or folder, use exactly that.
2. **Where the engagement already keeps deliverables.** Look at the workspace; if previous phase output already lives in a folder, write next to them in the **same** folder.
3. **The workspace root.** If neither applies, write to the workspace root.

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

## Correction process

When something is wrong: identify → log → re-generate → iterate on the output until correct, then optionally improve the source skill. See `skill-helpers/instructions/log-and-fix-skill-errors` for the full loop. Put the log under the engagement tree — not inside the skill package.
