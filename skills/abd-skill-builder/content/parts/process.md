# Process — abd-skill-builder

**Read first in every phase bundle:** **[Principles](library/principles.md)** (then **library** in the bundle, including **[critical quality steps](library/critical-quality-steps.md)**).

**Pipeline:** **[Principles](library/principles.md)** → **[Workspace and config](phases/workspace-and-config.md)** → **[Plan Script Build](phases/plan-script-build.md)** → **Stage 2 — build the skill** (phase **#2** scaffold through **#6** scripts — see one table below) → **Stage 3 — validation** (**`python scripts/base/build.py`** + **`build.scanners`**)

**Navigation spine:** **Standards** → **[Workspace and config](phases/workspace-and-config.md)** → **Analyze & confirm** → **Build the skill** (scaffold → process & phases → rules → library → scripts) → **Validation**

**Structural reference:** Copy layout and filenames from **`skill-scaffold/`** at the **abd-skill-builder** repo root — real directories, example files, comments. **Stage 1 plan** ( **`content/parts/library/base/checklist.md`** + **[Plan Script Build](phases/plan-script-build.md)** ). **Rich vs minimal `process.md` (team process plate):** **[Skill structure and concepts — rich process table](library/skill-structure-and-concepts.md#rich-process-table-team-plate)** and **[process-phases.md](library/process-phases.md)**. **Running phases / bundles:** **[process-phases.md](library/process-phases.md)**. Field-by-field authoring for scaffolded files is bundled under **Library** in phase prompts (**`scaffold_skill.py`** reads templates from **`content/parts/library/`** in **abd-skill-builder**). **`scaffold_skill.py`** copies from **`skill-scaffold/`**; the **`templates/`** folder is optional (codegen-only stubs not mirrored in **`skill-scaffold/`**).

---

## Outcome of this process

You finish with a **skill** where **instructions match the repo**: **`content/parts/process.md`** and **`phases/*.md`** align with **`skill-config.json`**; **`library/`**, **`rules/`**, and **`scripts/`** match **`SKILL.md`** and the agreed scope (see **`content/parts/library/base/checklist.md`** for how checklists are created and tracked). You **confirm with the user** after **analyze**, then at checkpoints **inside Stage 2** (scaffold, process & phases, rules, library, scripts — phase **#2** through **#6**) so work does not drift before **Stage 3** validation.

---

## High-level principles

**Outline (capabilities + problems solved):** the same structure is documented for readers under **`docs/`** — **[`docs/process-outline.md`](../../docs/process-outline.md)** — so onboarding can point at a short “why this shape” without duplicating stage tables.

### Capabilities (what this process enables)

| Capability | Problem it addresses |
| --- | --- |
| **Parts-based instructions** | Chat-only or ad-hoc prose drifts from the repo; nothing to diff or review. |
| **Process table ↔ `phase_files` ↔ `phases/*.md`** | Lost ordering, missing phases, or slugs that disagree with **`skill-config.json`** / **`generate_prompt`** / **`build.py`**. |
| **`skill-scaffold/` blueprint** | Invented folder layouts, broken greenfield skills, inconsistent **`SKILL.md`** / **`skill-config.json`** shape. |
| **Rules + scanners + `build.py`** | Violations that look “fine” in **`AGENTS.md`** until runtime; hand-edited merges hiding regressions. |
| **Staged confirmation** | Large wrong commits before the user can correct course. |

### Principles (normative)

1. **Author prompts from parts:** Build injected text from **`content/parts/library/`**, **`content/parts/phases/`**, **`rules/`**, and **`content/parts/process.md`** — not ad-hoc chat. Use **`skill-scaffold/`** as the folder blueprint.
2. **Process table is the map:** Every phase slug in **`skill-config.json` → `phase_files`** has a row below (seven columns per **[process-phases.md](library/process-phases.md)**) and a file at **`content/parts/phases/<slug>.md`**. Phase **0** is always **Workspace and config**; its row matches the scaffold contract.
3. **Quality and validation:** **Rules** → **scanners** → fix → **`python scripts/base/build.py`**. Fix **sources** under **`content/parts/`**, **`rules/`**, **`scripts/`** — not hand-edited **`AGENTS.md`**. See **[rules-and-scanners.md](library/rules-and-scanners.md)**.
4. **Confirm before you lock:** **Analyze** and propose components (1–2 sentences each); user corrects. **Stage 2** then runs phase **#2** through **#6** (scaffold through scripts); **confirm at natural breakpoints** inside that stage before **Stage 3** validation.

---

## Rules and automated checks (all skills)

**Default framework:** **[library/rules-and-scanners.md](library/rules-and-scanners.md)** — bind scanners to **`rules/`**, wire **`rules/scanners.json`**, align **`skill-config.json` → `build.build_pipeline`** and **`build.scanners`** with **`python scripts/base/build.py`**.

---

## Stage 0 — Workspace and config

### Purpose

Nail **where the skill runs**: **`skill_path`**, **`skill_workspace`**, **`skill-config.json`**, **`active_skill_workspace`**. Same semantics for every skill; routing detail lives only in **[Workspace and config](phases/workspace-and-config.md)**.

### What you produce

**`skill-config.json`** with correct **`active_skill_workspace`** for the project tree the skill reads and writes (pattern: **`skill-scaffold/skill-config.json`** at the skill root).

### How you know you succeeded

**`python scripts/base/set_workspace.py`** (no args) prints the expected workspace; paths resolve for **Plan** and **validation**.

### Phase table

| # | Phase | Description | Actor | Input | Output | Scripts |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | [Workspace and config](phases/workspace-and-config.md) | Set **`skill_path`** / **`skill_workspace`**; install **`skill-config.json`**; confirm **`active_skill_workspace`** matches the target tree. | Human / AI | Skill directory; target project tree | **`skill-config.json`** correct; terms unambiguous for later stages | `python` [`scripts/base/set_workspace.py`](../../scripts/base/set_workspace.py) — no args prints current; `<path>` sets **`active_skill_workspace`** in **`skill-config.json`** ([workspace-and-config](phases/workspace-and-config.md)) · `python scripts/base/generate.py --phase workspace-and-config` |

---

## Stage 1 — Analyze skill and confirm understanding

### Purpose

Before bulk authoring, **align with the user** on what the skill will contain. Review **`skill-scaffold/`** and propose **phases**, **library** shards, **rules**, **scanner** entries, and **scripts** — **one to two sentences per part**. User corrects; align **`content/parts/library/base/checklist.md`** (copied with **`library/base/`** at scaffold) with **[Plan Script Build](phases/plan-script-build.md)** and **[how checklists are created](library/base/checklist.md)**.

### What you produce

Shared understanding of delivery mode, phase order, and components; **`content/parts/library/base/checklist.md`** present (greenfield: from **`library/base/`** copy). No commitment to final **`library/`** / **`rules/`** text until Stage 1 is confirmed.

### How you know you succeeded

User explicitly confirms the **component list** and **phase slugs** before you run **scaffold** or heavy edits.

### Phase table

| # | Phase | Description | Actor | Input | Output | Scripts |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [Plan Script Build](phases/plan-script-build.md) | Internalize **library/** norms; decide delivery, phases, **build** / scanner chain, workspace; understand **`content/parts/library/base/checklist.md`** and **[how checklists are created](library/base/checklist.md)**. Use **`skill-scaffold/`** as the reference tree when naming parts. | AI (+ user) | **library/** norms; target workspace | Checklist norms + plan aligned; **`library/base/checklist.md`** in tree (scaffold) | `python scripts/base/generate.py --phase plan-script-build` |

---

## Stage 2 — Build the skill (phase #2 through phase #6)

**One process stage:** everything after **Stage 1 (analyze)** and before **Stage 3 (validation)**. The **numbered rows** below (**# 2 … 6**) are the **phase** order inside the skill package — not separate “stages” in this document.

### Purpose

- **#2 Scaffold:** **Greenfield:** emit a tree with **`scaffold_skill.py`**. **Existing tree:** skip **`scaffold_skill.py`** and start at **#3**. Follow **`skill-scaffold/`** and **[Scaffold](phases/scaffold.md)**.
- **#3 Process & phases:** Author **`content/parts/process.md`** and **`content/parts/phases/<slug>.md`** to match **`skill-config.json` → `phase_files`** and the **Pipeline** line above. See **[process-phases.md](library/process-phases.md)** and **[Skill structure and concepts — rich format](library/skill-structure-and-concepts.md#rich-process-table-team-plate)**.
- **#4–#6 [Fill scaffold parts](phases/fill-scaffold-parts.md):** **Rules & scanners** → **library** → **scripts** — same phase file, different focus per row; align **[rules-and-scanners.md](library/rules-and-scanners.md)**.

### What you produce

**`SKILL.md`**, **`skill-config.json`**, **`content/parts/`**, **`rules/`**, **`library/`**, **`scripts/`** as needed; **`build.py`** / **`phase_files`** aligned. **Confirm** with the user after **scaffold** (if greenfield), after **process/phases** are stable, and before treating **rules / library / scripts** as done.

### How you know you succeeded

**`python scripts/base/build.py`** runs through the work; **AGENTS.md** reflects **process**, **phases**, **rules**, **library**, and **scripts**; user has **confirmed** the main checkpoints inside this stage.

### Phase table (Stage 2 — all phases in one stage)

| # | Phase | Description | Actor | Input | Output | Scripts |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | [Scaffold](phases/scaffold.md) | **Greenfield:** **`scaffold_skill.py`** → scaffolded tree. Follow **`skill-scaffold/`**. | Code / Human | Stage 1 agreements; empty **`--out`** path | Scaffolded tree; **AGENTS.md** + **content/built/** after **`build.py`** | `python scripts/scaffold_skill.py --name <id> --out <path>` · `python scripts/base/build.py` |
| 3 | *(Authoring — see [process-phases.md](library/process-phases.md))* | **Process & phases:** edit **`content/parts/process.md`** and **`content/parts/phases/<slug>.md`**; keep slugs in sync with **`skill-config.json`**. | Human / AI | Tree from **#2** or existing skill | **Process** + **phases** honest and linked; user **confirmed** | `python scripts/base/build.py` · `python scripts/base/generate.py --phase <slug>` |
| 4 | [Fill scaffold parts](phases/fill-scaffold-parts.md) | **Rules & scanners:** **`rules/`**, **`rules/scanners.json`**, **`skill-config.json` → `build`**; align **[rules-and-scanners.md](library/rules-and-scanners.md)**. | Human / AI | **SKILL.md**; **`content/parts/process.md`**; plan | **`rules/`** + scanner wiring | `python scripts/base/generate.py --phase fill-scaffold-parts` · `python scripts/base/build.py` |
| 5 | [Fill scaffold parts](phases/fill-scaffold-parts.md) | **Library:** **`content/parts/library/*.md`** per **`library_files`** / **`phase_library`**; **`progress/`** checklists — **[checklist.md](library/base/checklist.md)**. | Human / AI | Rules baseline; **SKILL.md**; scope | **`library/`** complete; **AGENTS.md** reflects norms | `python scripts/base/generate.py --phase fill-scaffold-parts` · `python scripts/base/build.py` |
| 6 | [Fill scaffold parts](phases/fill-scaffold-parts.md) | **Scripts:** **`scripts/*.py`**, **`build.build_pipeline`**, **`build.scanners`**, **`compileall_paths`** as needed. | Human / Code | Plan; **validation** expectations | Scripts match **build** / **scan** contract | `python scripts/base/build.py` |

---

## Stage 3 — Structural validation

### Purpose

Prove **Python** compiles, **merge** succeeds, **scanners** pass. Exit **0** on the full chain.

### What you produce

Clean **validation** run; **`AGENTS.md`** and **`content/built/AGENTS.md`** consistent with **`content/parts/`** when using **`static_built`**.

### How you know you succeeded

**CI or local:** **`compileall`** on **`skill-config.json` → `build.compileall_paths`** → **`python scripts/base/build.py`** → **`build.scanners`**. Fix **sources**, not **AGENTS.md**.

### Phase table

| # | Phase | Description | Actor | Input | Output | Scripts |
| --- | --- | --- | --- | --- | --- | --- |
| 7 | *(validation)* | **Structural gate:** Python compile → **`build.py`** (merge + **`build.build_pipeline`**) → **`build.scanners`**. | Code | Skill root; **`skill-config.json`** | Exit **0**; built artifacts match **parts** | `python scripts/base/build.py` *(and scanners configured in **`skill-config.json`**)* |
