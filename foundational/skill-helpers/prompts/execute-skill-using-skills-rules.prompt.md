---
description: Read a skill's rules before generating, then run scanners after
---

I'm about to generate or edit output for a skill that has `rules/` or `scanners/`. Follow **`skills/execute-skill-using-skills-rules/SKILL.md`**.

1. Read the target skill's **`rules/*.md`** before producing anything; align with each rule's **DO** / **DO NOT**.
2. After generating (or after any user-suggested fix), do a second pass: re-check the output against the rules and run the scanners — `python skills/execute-skill-using-skills-rules/scripts/run_scanners.py --skill-root <skill> --workspace <abs-path>`. Fix anything that fails before declaring done.
---
description: Read a skill's rules before generating, then run scanners after
---

I'm about to generate or edit output for a skill that has `rules/` or `scanners/`. Follow **`skills/execute-skill-using-skills-rules/SKILL.md`**.

1. Read the target skill's **`rules/*.md`** before producing anything; align with each rule's **DO** / **DO NOT**.
2. After generating (or after any user-suggested fix), do a second pass: re-check the output against the rules and run the scanners — `python skills/execute-skill-using-skills-rules/scripts/run_scanners.py --skill-root <skill> --workspace <abs-path>`. Fix anything that fails before declaring done.
