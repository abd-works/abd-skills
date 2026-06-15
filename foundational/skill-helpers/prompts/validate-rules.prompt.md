---
description: Validate output against rules (AI per-rule verdict + scanner pass)
---

Validate the most recent skill output using both an AI rule review and the automated scanners.

1. Identify the **target skill** and the **workspace** containing the output.
2. **Read all rules** — open every file in the target skill's `rules/*.md`.
3. **AI per-rule verdict** — review the output against each rule and produce a table:

   | Rule | Verdict | Notes |
   |------|---------|-------|
   | rule-name | PASS / FAIL | brief justification |

4. **Scanner pass** — run: `python skills/execute-skill-using-skills-rules/scripts/run_scanners.py --skill-root <skill> --workspace <abs-path>`
5. If any rule or scanner fails, fix the violations, then re-run both checks until everything passes.
