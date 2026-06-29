I'm about to generate or edit output for a skill that has `rules/` or `scanners/`. Follow **`common/skill-workflow.md`**.

1. Read the target skill's **`rules/*.md`** before producing anything; align with each rule's **DO** / **DO NOT**.
2. After generating (or after any user-suggested fix), do a second pass: re-check the output against the rules and run the scanners — `python common/scripts/run_scanners.py --skill-root <skill> --workspace <abs-path>`. Fix anything that fails before declaring done.
3. **Diagram workflow (non-blocking):** After the scanner pass, check whether the active skill has `reference/diagram-workflow.md`. If it does, launch a **background sub-agent** (Task tool, `run_in_background: true`) with that file's contents and enough context (deliverables folder, output paths) for it to execute the CLI command independently. Do not wait for the sub-agent before returning to the user.
