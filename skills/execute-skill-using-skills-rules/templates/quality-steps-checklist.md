# Quality steps — checklist

Use **before** you do the skill’s main work: Step 1 is the **rules-first** gate; use the rest before you call the work **done**. Narrative: [**SKILL.md**](../SKILL.md) (section **Quality workflow**).

---

## Step 1 — Rules before real work (read first, then generate / edit)

- [ ] The agent **read through** that skill’s rules (**`rules/*.md`** + **Bundled rules** in **`SKILL.md`**) with the intent to **run the skill according to those rules**, not to skim or ignore them.
- [ ] Applicable **`rules/*.md`** were **read** (or inlined) **before** substantive work on the deliverable — not only after.
- [ ] The **Bundled rules** section of that skill’s **`SKILL.md`** was included if you rely on it (run **`bundle_rules_into_skill_md.py`** so it is current).
- [ ] **DO / DON'T** and examples in those rules were treated as the **shape contract**, not only CI.
- [ ] No claim that a rule “passed” if it was never applied to the artifact.

---

## Step 2 — Mechanical checks (scanners)

- [ ] Scanners run against the **generated output** (workspace / **`--workspace`** as documented for the skill).
- [ ] **Scanner report** saved under **`scanner-report/`** in **`active_skill_workspace`** (or the repo’s agreed path there).
- [ ] **Clear** violations fixed from the report; scanners re-run until clean or only **uncertain** items remain.
- [ ] **Uncertain** or **high-stakes** violations **shown to the user** with the report — not silently “fixed.”

---

## Step 3 — Adversarial pass (intent)

- [ ] Each applicable rule passes **by intent**, not only because tools are green.
- [ ] No **drift** a reviewer would catch between **`SKILL.md`** and what the skill actually does.

---

## Step 4 — Corrections log

- [ ] Problems found in review are logged under **`active_skill_workspace`** (see [**corrections-log.md**](./corrections-log.md)).
- [ ] **Item 4 — fix the output** completed for the entry (wrong → regenerate → **Example (correct)** filled) before editing skill sources for that issue.
- [ ] **DO / DO NOT** (and any promoted **rules** / **SKILL.md** edits) state **altered behavior** — not a long negation of the prior mistake; see [**corrections-log.md**](./corrections-log.md) **Phrasing**.

---

## Remember

Scanners are **necessary** for what they implement; they are **not sufficient** for semantic quality.
