# Rule Checklist

Run **Step 1 before starting** the skill's main work. Run **Steps 2–4 before calling work done**.

---

## Step 1 — Read rules before real work

- [ ] Every file in **`rules/`** for the target skill was read before substantive work — not only skimmed.
- [ ] Every file in **`reference/`** (if present) was read before authoring.
- [ ] DO / DO NOT and examples in those rules were treated as the **shape contract**, not only CI.
- [ ] No claim that a rule "passed" if it was never applied to the artifact.

---

## Step 2 — Scanner pass (mechanical checks)

- [ ] Scanners run against the **generated output** (`--workspace` as documented for the skill).
- [ ] **Scanner report** saved under `scanner-report/` in the workspace.
- [ ] Clear violations fixed from the report; scanners re-run until clean or only **uncertain** items remain.
- [ ] **Uncertain** or **high-stakes** violations shown to the user — not silently "fixed."

---

## Step 3 — Per-rule verdict (AI pass)

- [ ] For every file in **`rules/`**, a verdict was emitted: `Rule: <name>  -> PASS` or `Rule: <name>  -> FAIL  <offending line or reason>`.
- [ ] No rule was silently skipped — every rule appears in the output.
- [ ] FAIL verdicts were fixed and the rule re-checked before calling the work done.

---

## Step 4 — Adversarial pass (intent)

- [ ] Each applicable rule passes **by intent**, not only because tools are green.
- [ ] No drift a reviewer would catch between `SKILL.md` and what the skill actually does.

---

Scanners are **necessary** for what they implement; they are **not sufficient** for semantic quality.
