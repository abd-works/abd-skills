# Strategy execution and checklists (abd-ooad)

OOAD uses **three** checklist layers under **`<workspace>/abd-ooad/progress/`**. Only **`strategy.md`** defines **scope** and **which phases in what order**; checklists are where you **tick** progress.

---

## Workflow

1. **Domain scan** — produce scan artifacts (see **`scan-artifacts-and-strategy`**).
2. **Strategy** — fill **`strategy.md`** from **`templates/strategy.md`**:
   - **Modeling scope** — chapters, anchors, files, in/out of scope.
   - **Execution plan (normative)** — ordered list of phase **slugs** (from **`skill-config.json` → `phase_files`**) plus **scope per step** (e.g. “nouns-verbs on Chapter 5 only”).
   - **Approach going forward** + **Ongoing strategic decisions** — short narrative and dated pivots.
3. **Align live checklists** — keep **`strategy-run-checklist.md`** in sync with the execution plan (same order and scope). Seed file: **`templates/strategy-run-checklist.md`** (created under **`progress/`** on first **`generate.py`** when missing).
4. **Run phases** — for the **current** phase: `python scripts/base/generate.py --phase <slug>`. Tick **`strategy-run-checklist.md`** when a phase is **done** for its declared scope; tick **`<slug>-checklist.md`** for **steps inside** that phase.

---

## Three layers

| Layer | File | What you tick |
| --- | --- | --- |
| **Strategy execution** | **`progress/strategy-run-checklist.md`** | **Which phases** you will run, **in order**, each with **scope** (matches **`strategy.md` → Execution plan**). Use this for “next three steps per chapter” or “whole pipeline on anchor X.” |
| **Full pipeline (reference)** | **`progress/process-checklist.md`** | **Every** phase in **`phase_files`** — useful as a map; optional if you rely only on strategy-run. |
| **Phase steps** | **`progress/<phase>-checklist.md`** | **Action checklist** copied from **`content/parts/phases/<phase>.md` → ## Action Checklist**. |

**Normative rules** for pipeline + phase checklists: **`library/base/checklist.md`**. **Implementation:** **`scripts/base/workspace_checklists.py`**.

---

## What not to do

- Do not put **checkboxes** in **`strategy.md`** — keep execution plan as **normative numbered/bulleted text**; ticks live under **`progress/`**.
- Do not let **`strategy-run-checklist.md`** drift from **`strategy.md`** — after a pivot, update both and append a line under *Ongoing strategic decisions*.

---

## Phase slugs

Use exact slugs from **`skill-config.json` → `phase_files`** (e.g. `nouns-verbs-rules-and-states`, `domain-scan`). Labels for humans are in **`phase_section_headings`**.
