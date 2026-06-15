---
description: Run scanners against the most recent skill output
---

Run the scanners for the skill that produced the current output. Do not do an AI rule review — just execute the scanner pass.

1. Identify the **target skill** (from conversation context or the user's mention).
2. Identify the **workspace** (the folder containing the output to scan).
3. Run: `python skills/execute-skill-using-skills-rules/scripts/run_scanners.py --skill-root <skill> --workspace <abs-path>`
4. Report results. If any scanner fails, fix the violations and re-run until clean.
