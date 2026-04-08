# Strategy execution and checklists (abd-ooad)

**Canonical doc** for: (1) **strategy** vs **live ticks**, (2) **which files** hold checkboxes, (3) **how** `generate.py` creates workspace **`progress/`** files. Does **not** replace **[process.md](../process.md)** (process tables, `generate` / `build`) or **[skill-structure-and-concepts.md](../base/skill-structure-and-concepts.md)** (repo layout).

Only **`strategy.md`** defines **scope** and **which phases in what order**; checklists are where you **tick** progress.

---

## Workflow

1. **Domain scan** — produce scan artifacts (see **`strategy-led-generation`**).
2. **Strategy** — fill **`strategy.md`** from **`templates/strategy.md`**:
   - **Modeling scope** — corpus or product boundary; **source type** (book vs repo vs mixed).
   - **§1 Source slices** — ordered table: **Goal**, **Source** (chapters, files, modules, APIs — whatever locates work), **Coverage** (depth this pass), **Importance**; stable **slice IDs** reused everywhere.
   - **§2 Slice plan** — per slice: **goal restated**, **unit kind**, **phases** (execution step numbers / slugs), produces, depends-on.
   - **Coverage across steps** — matrix: every slice → which **execution plan** steps touch it → **depth** → deferrals.
   - **Cross-slice integration** — cross-boundary types and ordering (From → To + narrative).
   - **Anchor and subdomain elaboration** (when anchors have attached types) — map subdomains to slices and execution §.
   - **Execution plan (normative)** — ordered phase **slugs**; **each line cites slice IDs** (mirror **`strategy-run-checklist.md`**).
   - **Approach going forward** + **Ongoing strategic decisions** — short narrative and dated pivots.
3. **Align live checklists** — keep **`strategy-run-checklist.md`** in sync with the execution plan (same order and scope). Optional **`templates/strategy-run-checklist.md`** seed; optional **`templates/progress-README.md`** → **`progress/README.md`** for slice-specific files under **`progress/slices/`**.
4. **Run phases** — for the **current** phase: `python scripts/base/generate.py --phase <slug>`. Tick **`strategy-run-checklist.md`** when a phase is **done** for its declared scope; tick **`<slug>-checklist.md`** for **steps inside** that phase.

---

## Three layers (what you tick)

| Layer | File | What you tick |
| --- | --- | --- |
| **Strategy execution** | **`progress/strategy-run-checklist.md`** | **Which phases** you will run, **in order**, each with **scope** that **includes the same slice IDs** as **`strategy.md` → Execution plan**. Optional: **`progress/slices/<slice-id>-checklist.md`** per slice — see **`progress/README.md`** in the workspace (if present). |
| **Full pipeline (reference)** | **`progress/process-checklist.md`** | **Every** phase in **`phase_files`** — useful as a map; optional if you rely only on strategy-run. |
| **Phase steps** | **`progress/<phase>-checklist.md`** | **Action checklist** copied from **`content/parts/phases/<phase>.md` → ## Action Checklist**. |

**Implementation:** **`scripts/base/workspace_checklists.py`** (paths, behavior, `--no-ensure-checklists`).

---

## How workspace checklist files are created (mechanical)

| Kind | What it tracks | Where it lives | How it gets there |
| --- | --- | --- | --- |
| **Normative reference** | Rules in **this document** — strategy vs ticks, layers, `generate.py` behavior | **`content/parts/library/strategy-execution-and-checklists.md`** | Authored in the skill; **not** created by **`generate.py`**. |
| **Pipeline position** | Which **phase** of the pipeline you are in | **`<active_skill_workspace>/<skill_name>/progress/process-checklist.md`** | **Created** on first **`python scripts/base/generate.py --phase <slug>`** when that file is **missing**, if **`skill-config.json` → `workspace.active_skill_workspace`** is set. One `- [ ]` line per slug in **`phase_files`** (labels from **`phase_section_headings`** when present). **Does not overwrite** an existing file. |
| **Phase action steps** | **Steps inside** the current phase | **`<active_skill_workspace>/<skill_name>/progress/<phase-slug>-checklist.md`** | **Created** in the **same** `generate.py` run when that file is **missing**. Steps are taken from **`## Action Checklist`** in **`content/parts/phases/<phase-slug>.md`**, or from task lines (`- [ ]` / `- [x]`) in that file if the section is absent. **Does not overwrite** an existing file. |
| **Strategy execution** (workspace) | Ordered phases matching **`strategy.md`** | **`progress/strategy-run-checklist.md`** | Seeded from template when **`generate.py`** / workspace checklist logic creates it; **you** align it with **`strategy.md`**. |

### Names and workspace

- **`skill_name`** — **`skill-config.json` → `name`** (fallback: skill directory name). Used in **`…/<skill_name>/progress/`**.
- **`active_skill_workspace`** — Must point at the **project / engagement tree** where **`progress/`** checklists belong, **not** the skill install folder. See **`skill-config.json` → `workspace`** and **[workspace-and-config.md](phases/workspace-and-config.md)**.

### Flags

- **`python scripts/base/generate.py --phase <slug> --no-ensure-checklists`** — run the phase prompt **without** creating missing **`progress/`** checklist files (see **`workspace_checklists.py`**).

---

## What not to do

- Do not put **checkboxes** in **`strategy.md`** — keep execution plan as **normative numbered/bulleted text**; ticks live under **`progress/`**.
- Do not record pipeline or phase **session** progress by ticking boxes in **`content/parts/process.md`** or **`content/parts/phases/*.md`** — those stay **normative**; live ticks go **only** under **`…/progress/`**.
- Do not let **`strategy-run-checklist.md`** drift from **`strategy.md`** — after a pivot, update both and append a line under *Ongoing strategic decisions*.

---

## Phase slugs

Use exact slugs from **`skill-config.json` → `phase_files`** (e.g. `nouns-verbs-rules-and-states`, `domain-scan`). Labels for humans are in **`phase_section_headings`**.

---

## References

- **`strategy-led-generation.md`** — artifact roles, **`strategy.md`** vs **`domain-scan-results.md`**
- **`templates/strategy.md`**, **`templates/progress-README.md`**
- **`scripts/base/workspace_checklists.py`**
