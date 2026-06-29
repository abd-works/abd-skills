# Rule Checklist

**When:** After [`skill-workflow.md`](./skill-workflow.md) § Generate — before calling work done.

**Prerequisite:** § Read-gates completed (rules, reference, templates read in full). Do not start this checklist until generation is finished.

Together, these steps are the answer to "does this match the rules?" Scanners are **necessary** for what they implement; they are **not sufficient** for semantic quality.

When the practice family ships **`reference/validate-checklist.md`**, read it and apply those shared items during this checklist. Do **not** duplicate rule checks in `SKILL.md` — this checklist, per-rule verdicts, and scanners are sufficient.

---

## Step 1 — Scanner pass (mechanical checks)

- [ ] Scanners run against the **generated output** (`--workspace` as documented for the skill):

```bash
python <common_root>/scripts/run_scanners.py --skill-root <path-to-skill> --workspace <path-to-output>
```

Add `--language <lang>` (e.g. `python`, `javascript`) when scanners live in `scanners/<lang>/`.

- [ ] **Scanner report** saved under `scanner-report/` in the workspace.
- [ ] Clear violations fixed from the report; scanners re-run until clean or only **uncertain** items remain.
- [ ] **Uncertain** or **high-stakes** violations shown to the user — not silently "fixed."

---

## Step 2 — Per-rule verdict (AI pass)

Re-read every file in **`rules/`**. For **each rule**, emit:

```
Rule: <rule-filename>  ->  PASS
Rule: <rule-filename>  ->  FAIL  <offending line or reason>
```

- [ ] No rule was silently skipped — every rule appears in the output.
- [ ] FAIL verdicts were fixed and the rule re-checked before calling the work done.

---

## Step 3 — Adversarial pass (intent)

- [ ] Each applicable rule passes **by intent**, not only because tools are green.
- [ ] No drift a reviewer would catch between `SKILL.md` and what the skill actually does.
