# Process outline — capabilities and problems

**Companion to:** [`content/parts/process.md`](../content/parts/process.md) (authoritative process spine in the skill package).

This page is a **reader-facing outline**: what the abd-skill-builder **process is for**, which **capabilities** it provides, and which **problems** each principle addresses. Use it when onboarding or when you need a short “why this shape” without duplicating the full stage tables in **`process.md`**.

---

## What the process delivers (capabilities)

| Capability | What it is | Where it lives |
| --- | --- | --- |
| **Single-source instructions** | Prompts and agent bundles built from **`content/parts/`** (process, phases, library), **`rules/`**, and scripts — not one-off chat prose. | [`process.md`](../content/parts/process.md) § High-level principles; [`library/process-phases.md`](../content/parts/library/process-phases.md) |
| **Navigable pipeline** | Ordered phases with a **process table** (seven columns), **`phase_files`** in **`skill-config.json`**, and one file per slug under **`content/parts/phases/<slug>.md`**. | [`process.md`](../content/parts/process.md) stage tables; [`library/process-phases.md`](../content/parts/library/process-phases.md) |
| **Structural truth** | **`skill-scaffold/`** as the folder blueprint; **`scaffold_skill.py`** for greenfield trees. | [`plan-script-build.md`](../content/parts/phases/plan-script-build.md) (Stage 1 norms + **`library/base/checklist.md`**); repo **`skill-scaffold/`** |
| **Quality gate** | Rules → scanners → fix → **`python scripts/base/build.py`**; edit **sources**, not hand-tuned **`AGENTS.md`**. | [`library/rules-and-scanners.md`](../content/parts/library/rules-and-scanners.md) |
| **Governed change** | Analyze and confirm components before heavy authoring; checklists per **[how checklists are created](../content/parts/library/base/checklist.md)** (stable **`library/base/`** and workspace **`progress/`**). | [`base/checklist.md`](../content/parts/library/base/checklist.md); [`Skill structure and concepts.md`](../content/parts/library/skill-structure-and-concepts.md#authoring-checklist--injector-body) |

---

## Principles → problems solved

| Principle | Problem without it | Outcome |
| --- | --- | --- |
| **Author prompts from parts** | Instructions diverge from the repo; every session reinvents wording; no diffable source of truth. | One merge path into **`AGENTS.md`** / built slices; **`skill-scaffold/`** keeps new skills aligned. |
| **Process table is the map** | Phases missing, mis-ordered, or renamed in only one place; **`generate_prompt`** and **`build.py`** disagree. | **`skill-config.json` → `phase_files`**, **`process.md`** rows, and **`phases/*.md`** stay in lockstep; Phase **0** is always **Workspace and config**. |
| **Quality and validation** | “Green” **`AGENTS.md`** that still violates rules; manual patches hide regressions. | Scanners and **`build.py`** fail fast; fixes go to **`content/parts/`**, **`rules/`**, **`scripts/`**. |
| **Confirm before you lock** | Large mistaken edits; user sees finished work only after it is wrong. | Short proposals per component (1–2 sentences); explicit confirmation between **analyze**, **process & phases**, **rules**, **library**, **scripts**. |
