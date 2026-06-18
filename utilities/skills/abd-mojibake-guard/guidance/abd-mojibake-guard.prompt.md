---
description: Scan and remove mojibake / encoding corruption before commit
mode: agent
---

Remove mojibake and encoding issues from this repo using **abd-mojibake-guard**.

Follow **`utilities/skills/abd-mojibake-guard/guidance/abd-mojibake-guard.instructions.md`** and every file in **`utilities/skills/abd-mojibake-guard/rules/`**.

## Steps

1. **Scan** — from abd-skills repo root:

   ```bash
   python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py scan
   ```

2. **If issues found** — auto-fix, then scan again:

   ```bash
   python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py fix
   python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py scan
   ```

3. **Review** — open any file that still fails; replace remaining garbled sequences with the intended Unicode character (smart quotes, em-dashes, bullets, accented letters). Re-run scan until clean or only documented skip paths remain.

4. **Before commit** — verify staged files:

   ```bash
   python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py check-staged
   ```

5. **Report** — list files fixed, issues remaining (if any), and confirm staged check passes.

If the repo has no guard yet, offer to run:

```bash
python utilities/skills/abd-mojibake-guard/scripts/run_encoding_guard.py install-guard
```
