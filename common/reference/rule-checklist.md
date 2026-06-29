# Rule Checklist

**When:** Run **Step 1** after [`skill-workflow.md`](./skill-workflow.md) § Read-gates and before substantive generation. Run **Steps 2–4** after generating, before calling work done.

Together, Steps 2–4 are the answer to "does this match the rules?" Scanners are **necessary** for what they implement; they are **not sufficient** for semantic quality.

When the practice family ships **`reference/validate-checklist.md`**, read it and apply those shared items during Steps 2–4. Do **not** duplicate rule checks in `SKILL.md` — this checklist, per-rule verdicts, and scanners are sufficient.

---

## Step 1 — Read rules before real work

Confirms § Read-gates in [`skill-workflow.md`](./skill-workflow.md) were completed — not a substitute for them.

- [ ] Every file in **`rules/`** for the target skill was read before substantive work — not only skimmed.
- [ ] Every file in **`reference/`** (if present) was read before authoring.
- [ ] DO / DO NOT and examples in those rules were treated as the **shape contract**, not only CI.
- [ ] No claim that a rule "passed" if it was never applied to the artifact.

---

## Step 2 — Scanner pass (mechanical checks)

- [ ] Scanners run against the **generated output** (`--workspace` as documented for the skill):

```bash
python <common_root>/scripts/run_scanners.py --skill-root <path-to-skill> --workspace <path-to-output>
```

Add `--language <lang>` (e.g. `python`, `javascript`) when scanners live in `scanners/<lang>/`.

- [ ] **Scanner report** saved under `scanner-report/` in the workspace.
- [ ] Clear violations fixed from the report; scanners re-run until clean or only **uncertain** items remain.
- [ ] **Uncertain** or **high-stakes** violations shown to the user — not silently "fixed."

---

## Step 3 — Per-rule verdict (AI pass)

Re-read every file in **`rules/`**. For **each rule**, emit:

```
Rule: <rule-filename>  ->  PASS
Rule: <rule-filename>  ->  FAIL  <offending line or reason>
```

- [ ] No rule was silently skipped — every rule appears in the output.
- [ ] FAIL verdicts were fixed and the rule re-checked before calling the work done.

---

## Step 4 — Adversarial pass (intent)

- [ ] Each applicable rule passes **by intent**, not only because tools are green.
- [ ] No drift a reviewer would catch between `SKILL.md` and what the skill actually does.
