# Quality steps — checklist  

Use **before** you do the skill's main work: Step 1 is the **rules-first** gate; use the rest before you call the work **done**. Narrative: [**SKILL.md**](../SKILL.md) (section **Quality workflow**).  

---  

## Step 1 — Rules before real work (read first, then generate / edit)  

- [ ] Every file in **`rules/`** for the target skill was read before substantive work — not only skimmed.  
- [ ] Every file in **`reference/`** (if present) was read before authoring.  
- [ ] **DO / DON'T** and examples in those rules were treated as the **shape contract**, not only CI.  
- [ ] No claim that a rule "passed" if it was never applied to the artifact.  

---  

## Step 2 — Mechanical checks (scanners)  

- [ ] Scanners run against the **generated output** (workspace / **`--workspace`** as documented for the skill).  
- [ ] **Scanner report** saved under **`scanner-report/`** in **`active_skill_workspace`** (or the repo's agreed path there).  
- [ ] **Clear** violations fixed from the report; scanners re-run until clean or only **uncertain** items remain.  
- [ ] **Uncertain** or **high-stakes** violations **shown to the user** with the report — not silently "fixed."  

---  

## Step 3 — Per-rule verdict (AI pass)  

- [ ] For every file in **`rules/`**, a verdict was emitted: `Rule: <name>  -> PASS` or `Rule: <name>  -> FAIL  <offending line or reason>`.  
- [ ] No rule was silently skipped — every rule appears in the output.  
- [ ] FAIL verdicts were fixed and the rule re-checked before calling the work done.  

---  

## Step 4 — Adversarial pass (intent)  

- [ ] Each applicable rule passes **by intent**, not only because tools are green.  
- [ ] No **drift** a reviewer would catch between **`SKILL.md`** and what the skill actually does.  

---  

## Remember  

Scanners are **necessary** for what they implement; they are **not sufficient** for semantic quality.  
