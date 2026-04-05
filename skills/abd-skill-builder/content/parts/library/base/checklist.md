# How checklists are created

This file documents **only** where checklist files come from and what creates them. It does **not** replace **[process-phases.md](../process-phases.md)** (process tables, `generate` / `build`), **[skill-structure-and-concepts.md](../skill-structure-and-concepts.md)** (repo layout), or individual **phase** files under **`content/parts/phases/`**.

**Stable norm:** This file lives at **`content/parts/library/base/checklist.md`**. It is **shared across all skills** built from **abd-skill-builder**: **`scaffold_skill.py`** copies the entire **`content/parts/library/base/`** directory from the builder. When these rules change, update **`checklist.md`** in **abd-skill-builder** and refresh **`library/base/`** in downstream skills (copy the folder or re-run scaffold patterns you use).

---

## Kinds (normative doc vs workspace progress)

| Kind | What it tracks | Where it lives | How it gets there |
| --- | --- | --- | --- |
| **Normative reference** | Rules for **how** pipeline and phase checklists work (this document) | **`content/parts/library/base/checklist.md`** | Copied with **`library/base/`** at scaffold; **not** created by **`generate.py`**. |
| **Pipeline position** | Which **phase** of the pipeline you are in | **`<active_skill_workspace>/<skill_name>/progress/process-checklist.md`** | **Created** on first **`python scripts/base/generate.py --phase <slug>`** when that file is **missing**, if **`skill-config.json` → `workspace.active_skill_workspace`** is set. One `- [ ]` line per slug in **`phase_files`** (labels from **`phase_section_headings`** when present). **Does not overwrite** an existing file. |
| **Phase action steps** | **Steps inside** the current phase | **`<active_skill_workspace>/<skill_name>/progress/<phase-slug>-checklist.md`** | **Created** in the **same** `generate.py` run when that file is **missing**. Steps are taken from **`## Action Checklist`** in **`content/parts/phases/<phase-slug>.md`**, or from task lines (`- [ ]` / `- [x]`) in that file if the section is absent. **Does not overwrite** an existing file. |

**Implementation:** **`scripts/base/workspace_checklists.py`**. Docstring and helpers there are the source of truth for paths and behavior.

---

## Names and workspace

- **`skill_name`** — **`skill-config.json` → `name`** (fallback: skill directory name). Used in **`…/<skill_name>/progress/`**.
- **`active_skill_workspace`** — Must point at the **project / engagement tree** where **`progress/`** checklists belong, **not** the skill install folder. See **`skill-config.json` → `workspace`** and **[workspace-and-config.md](../phases/workspace-and-config.md)**.

---

## What not to do

- **Do not** record pipeline or phase **session** progress by ticking boxes in **`content/parts/process.md`** or **`content/parts/phases/*.md`** — those stay **normative**; live ticks go **only** under **`…/progress/`**.

---

## Flags and skipping generation

- **`python scripts/base/generate.py --phase <slug> --no-ensure-checklists`** — run the phase prompt **without** creating missing **`progress/`** checklist files (see **`workspace_checklists.py`**).
