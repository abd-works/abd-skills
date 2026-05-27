# Execute skills using their rules (always-on)

Triggers: you are about to **run, generate from, or edit output of** any skill whose package contains a **`rules/`** or **`scanners/`** directory.

**Authoritative steps** live in **`skills/execute-skill-using-skills-rules/SKILL.md`** (or **`~/.cursor/skills/execute-skill-using-skills-rules/SKILL.md`**).

**Non-negotiable:**

1. **Before generating** — read the target skill's **`rules/*.md`** first and align what you create with each rule's **DO** / **DO NOT**. No skipping, no working from memory.
2. **After generating** — second pass: re-check the output against those rules (AI pass) **and** run the scanners (`python skills/execute-skill-using-skills-rules/scripts/run_scanners.py --skill-root <skill> --workspace <abs-path-to-output>`). Fix anything that fails before declaring done.
3. **After a user correction or fix** — repeat step 2 on the edited artifact in the same turn. A user-flagged problem is not resolved until the rules pass and the scanners pass.
4. If a rule or scanner fails, follow **`skill-helpers/instructions/log-and-fix-skill-errors`** to log and re-generate.
