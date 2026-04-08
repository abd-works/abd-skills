<!--
  Live strategy execution checklist — workspace file
  Copy / seed to: <workspace>/abd-ooad/progress/strategy-run-checklist.md
  Created on first `python scripts/base/generate.py --phase <phase-id>` when missing (if template present).
-->

# Strategy execution — {{project_name}}

**Purpose:** Tick **which phase-ids** (or **stages**) you will run, in **what order**, and with **what scope** — aligned with **`strategy.md` → Execution plan (normative)**. Resume at the **first unchecked** row.

**Normative plan (no ticks):** `strategy.md`  
**Full pipeline reference (all phase-ids):** `process-checklist.md`  
**Current phase steps:** `<phase-id>-checklist.md` (e.g. `nouns-verbs-rules-and-states-checklist.md`)

**Revisits:** Add **new rows** here when you must go **backward** (same file — not a separate rerun workflow). Example rows below.

Edit the rows below to match **`strategy.md` → Execution plan (normative)**. **Reuse slice IDs** from **`strategy.md` → §1** in each scope line (e.g. `slices: S6, S1 — Ch.6 Powers + Ch.1 glue`).

---

## Planned phases (in order)

- [ ] **`domain-scan`** — slices: {{S1…Sn \| all}} — {{short scope note}}
- [ ] **`nouns-verbs-rules-and-states`** — slices: {{e.g. S6, S1}} — {{what}}
- [ ] **`raw-candidate-list`** — slices: {{…}} — {{…}}
- [ ] *(add next phase-ids or delete unused rows)*

---

## Revisit rows (examples — add as needed)

- [ ] **Revisit stage B** — slices: {{S1}} — {{reason — e.g. new anchor from stakeholder}}
- [ ] **Re-run `thing-vs-data-about-a-thing`** — slices: {{S2}} — {{reason — boundary fix after validate-with-scenarios}}
- [ ] **Revisit stage D** — slices: {{all}} — {{reason — split bloated class}}

---

## Notes

*Optional: link to **term-registry** rows, **`terms.md`** paths, diagram paths, blockers, or **slice ID** renames after a pivot.*
