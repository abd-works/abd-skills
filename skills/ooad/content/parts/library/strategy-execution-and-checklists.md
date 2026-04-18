# Strategy execution and checklists (abd-ooad)

**Canonical doc** for: (1) **strategy** vs **live ticks**, (2) **where** those ticks live under **`progress/`**, (3) **stages** and **revisits** on one run sheet. For **command-line options** and **exactly when** files are created on disk, see **`scripts/base/generate.py`**. This doc does not replace **[process.md](../process.md)** (pipeline stages, `generate` / `build`) or **[skill-structure-and-concepts.md](../base/skill-structure-and-concepts.md)** (repo layout).

Only **`strategy.md`** defines **scope** and **which phase-ids (or stages) in what order**; checklists are where you **tick** progress.

---

## Workflow

1. **Domain scan** — produce scan artifacts (see **`strategy-led-generation`**). Phase-id: **`domain-scan`**.
2. **Strategy** — fill **`strategy.md`** from **`templates/strategy.md`**:
   - **Modeling scope** — corpus or product boundary; **source type** (book vs repo vs mixed).
   - **§1 Source slices** — ordered table: **Goal**, **Source** (chapters, files, modules, APIs — whatever locates work), **Coverage** (depth this pass), **Importance**; stable **slice IDs** reused everywhere (same strings as **`--slice`** on **`generate.py`**).
   - **§2 Slice plan** — per slice: **goal restated**, **unit kind**, **phase-ids** (or **stages**) you will run, produces, depends-on.
   - **Coverage across steps** — matrix: every slice → which **execution plan** phase-ids touch it → **depth** → deferrals.
   - **Cross-slice integration** — cross-boundary types and ordering (From → To + narrative).
   - **Anchor and subdomain elaboration** (when anchors have attached types) — map subdomains to slices and execution phase-ids.
   - **Execution plan (normative)** — ordered **phase-id** strings; **each line cites slice IDs** (mirror **`strategy-run-checklist.md`**). You may group work by **stage A–F** (see **`process.md` → Stage map**).
   - **Stage completion (after each stage)** — what completed; tensions; **new checklist lines** for revisits (below); **audit** — append dated line under *Ongoing strategic decisions*.
   - **Approach going forward** + **Ongoing strategic decisions** — short narrative and dated pivots.
3. **Align live checklists** — keep **`strategy-run-checklist.md`** in sync with the execution plan (same order and scope). On first run, **`generate.py`** seeds **`progress/README.md`** from **`templates/progress-README.md`**, and **`strategy-run-checklist.md`** from **`templates/strategy-run-checklist.md`**, when those templates exist in the skill.
4. **Run phases** — **`python scripts/base/generate.py --phase <phase-id> --slice <slice-id>`** (default slice **`main`**) for one step, or **`python scripts/base/generate.py --stage <A|B|…|F> --slice <slice-id>`** for a full stage (same order as **`process.md`** / **`skill-config.json` → `process_stages`**). Tick **`strategy-run-checklist.md`** when a phase (or stage slice) is **done** for its declared scope; tick **`progress/slices/<slice-id>/<phase-id>-checklist.md`** for **steps inside** that phase for that slice.

---

## Revisits and disruption (same checklist)

A **revisit** is **not** a separate rerun workflow. While executing (including late **stage F**), if work must **go back** to an earlier **stage** or **phase-id**, **add a new row** to **`strategy-run-checklist.md`** — e.g. `- [ ] Revisit stage B — <short reason>` or `- [ ] Re-run nouns-verbs-rules-and-states — slice S1 — reconcile new anchor` — at the **bottom** or **inserted** where it fits the agreed order. The checklist is the single source of truth for **forward** work plus **backward** revisits.

**Audit:** When you add a revisit row, append a dated line under **`strategy.md` → Ongoing strategic decisions**; never delete prior pivots.

### Hint table (non-prescriptive)

| You are here | Often need to touch |
|--------------|---------------------|
| Stage F | Stage E, D, or C (naming / validation feedback) |
| Stage E | Stage C (scenarios expose structure gaps) |
| Stage D | Stage C (splitting responsibilities) |

Use this as a **prompt**, not a rule.

---

## Strategy file, run sheet, and phase ticks (what lives where)

**1. Plan in prose — `strategy.md`**

- **Location:** your workspace (same tree as **`progress/`**), usually next to other engagement files. Start from **`templates/strategy.md`**.
- **Content:** scope, slices, and the **execution plan** in words — **no** `- [ ]` boxes.
- **Role:** the agreement on **what** you will run and **in what order**.

**2. Run sheet — `progress/strategy-run-checklist.md`**

- **Location:** `<active_skill_workspace>/<skill_name>/progress/strategy-run-checklist.md` — see **[base/workspace-and-config.md](base/workspace-and-config.md)** for how those path parts are chosen.
- **Content:** one tickable row per planned phase (and **revisit** rows when needed), aligned with **`strategy.md`** execution plan.
- **Source:** **you** maintain it. The first time the file is missing, **`python scripts/base/generate.py --phase …`** may copy **`templates/strategy-run-checklist.md`** into **`progress/`**; after that, edits are yours.

**3. Progress tree index — `progress/README.md`**

- **Location:** same **`progress/`** folder.
- **Content:** explains **`strategy-run-checklist.md`**, **`slices/<slice-id>/`**, and **`process-checklist.md`**.
- **Source:** first run copies **`templates/progress-README.md`** when that file is missing.

**4. Phase steps — `progress/slices/<slice-id>/<phase-id>-checklist.md`**

- **Location:** under **`progress/slices/`**, one folder per **slice ID** from **strategy.md** §1 (default CLI slice **`main`** for a single-slice engagement).
- **Content:** the **same steps** as **`content/parts/phases/<phase-id>.md` → ## Action Checklist** (or `- [ ]` task lines in that phase file if the section is absent).
- **Source:** the normative steps always live in **`content/parts/phases/<phase-id>.md`** in the skill. **`generate.py`** writes the workspace copy the first time it is missing when you run **`--phase <phase-id> --slice <slice-id>`**, so you tick in the workspace without editing the skill repo.

**Summary**

| You read or edit | It contains |
| --- | --- |
| **`strategy.md`** | Execution plan in prose (normative for **what** to run). |
| **`progress/strategy-run-checklist.md`** | Ticks for **which phases you ran**, in order, with scope (mirrors the plan). |
| **`progress/README.md`** | What each file under **`progress/`** is for. |
| **`content/parts/phases/<phase-id>.md`** | Phase instructions and **## Action Checklist** (normative for **how** the phase works). |
| **`progress/slices/<slice-id>/<phase-id>-checklist.md`** | Ticks for **steps inside** that phase for that **slice** (working copy of the action list). |

**`generate.py`** prints phase instructions and may create missing files under **`progress/`** as described above; options and edge cases are in **`scripts/base/generate.py`**.

---

## Keeping plan, skill docs, and ticks aligned

- **`strategy.md`** carries the **execution plan as text**; **`progress/strategy-run-checklist.md`** carries the **matching ticks**. Update both when the plan changes, and add a dated line under *Ongoing strategic decisions* in **`strategy.md`** when you pivot.
- **`content/parts/process.md`** and **`content/parts/phases/*.md`** in the skill stay **reference** instructions for everyone; your **session** ticks for a phase belong in **`progress/slices/<slice-id>/<phase-id>-checklist.md`**.

---

## Phase IDs

Use exact **phase-id** strings from **`skill-config.json` → `phase_files`** (e.g. `nouns-verbs-rules-and-states`, `domain-scan`). Labels for humans are in **`phase_section_headings`**. **Stages** **A–F** map to ordered phase-id lists in **`process_stages`** — see **`process.md`**.

---

## References

- **`base/workspace-and-config.md`** — **`skill_name`**, **`active_skill_workspace`**, where **`progress/`** lives
- **`strategy-led-generation.md`** — artifact roles, **`strategy.md`** vs **`domain-scan-results.md`**
- **`templates/strategy.md`**, **`templates/progress-README.md`**, **`templates/strategy-run-checklist.md`**
- **`scripts/base/generate.py`** — when it writes **`progress/`** files, CLI flags, order of operations
