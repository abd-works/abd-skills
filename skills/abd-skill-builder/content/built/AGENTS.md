# AGENTS — abd-skill-builder

## Process

# Process — abd-skill-builder

**In order:** **[Critical quality / Principles](library/critical-quality-steps.md)** (read first in every AI-chat phase bundle) → Standards & checklist → **Phase 0 — [Workspace and config](phases/workspace-and-config.md)** → **Plan (1a or 1b)** → **Scaffold or migrate** → **Fill library and rules (AI + user)** → **Operator** (automated checks)

## Outcome of this process

You finish with a **skill** where the instructions you give the model **match what the skill actually says**, so work does not drift off-script. **Stages and phases** break the work into clear chunks; **steps** sit in phase files; **checklists** help you pick up after a break or a handoff. **Rules** say what must stay true; **scanners** and the other **automated checks** (Python validity on the paths you configured, **build**, scripts listed in config) **catch** when the **files in the repo** no longer match those rules. *Each phase row lists **Input**, **Output**, and **Scripts**. **[Workspace and config](phases/workspace-and-config.md)** covers `**skill_path`**, `**conf/abd-config.json`**, `**active_skill_workspace**`. **Plan** has **1a** — **[Plan Script Build](phases/plan-script-build.md)** (new skill); **1b** — **[Plan skill migration](phases/plan-migrate.md)** (existing skill: **delta** vs standards, user choice). `**docs/skill-plan.md`** holds the plan and the **Authoring checklist** section.*

## High-level principles

- **Critical quality first:** For any **`python scripts/generate.py --phase …`** session, the emitted bundle leads with **`## Principles`** ([**critical-quality-steps.md**](library/critical-quality-steps.md)) — rules + scanners + review **before** role, phase body, library shards, and rules text.
- **Instructions match the skill:** Build prompts and injected text from what the skill already wrote in **library/**, **phases/**, and **rules/**—not off-the-cuff chat.
- **Stages, phases, and checklists:** The process **table** is the map; **steps** live inside phase files. **Checklists** (including the authoring checklist) keep long or stop-and-start work ordered so you can resume.
- **Quality process (rules → scan → assess → fix):** Put must-holds in **rules/** and reflect them in prompts/injections so work is guided. Scan, check against rules, fix, log. Before commit, **Operator** runs: Python on paths in **skill-config.json** compiles, then `**python scripts/build.py`** (merge + `**operator.build_pipeline**` steps when configured), then `**operator.scanners**`. If your workflow needs a longer **refine / shape** loop after that, document it in **library/** or **phases/**—not here as a hard dependency.
- **Assemble from parts:** Author **parts** (process, **library/**, **phases/**, **rules/**); **build** produces **AGENTS.md** and (if **static**) **content/built/**; **dynamic** merges the same parts at run time. Parts stay the source of truth. **Scaffold** vs **migrate** only affects how you create or fix the tree—phase order is this table’s **#** and **build.py** lists, not filenames. [delivery-modes](library/delivery-modes.md).

### Rules and automated checks (all skills)

**Default framework:** `**[library/rules-and-automated-checks.md](library/rules-and-automated-checks.md)`** — bind scanners to **rules** in `**rules/scanners.json`**, run ordered post-merge steps from `**skill-config.json` → `operator.build_pipeline**` inside `**python scripts/build.py**`, and keep `**operator.scanners**` aligned for **Operator**. **Process** tables stay about **phases** and **merge/emit** CLIs, not a laundry list of validators per row.

## Stage 0 — Workspace and config

**Doc:** **[Workspace and config](phases/workspace-and-config.md)** — `**skill_path`**, `**skill_workspace`**, `**conf/abd-config.json**`, `**active_skill_workspace**`, two levels of `**conf/**` (not duplicated in later phases).


| #   | Phase                                                  | Description                                                                                                                                                                                                                                                                                                    | Actor      | Input                                             | Output                                                                                                  | Scripts                                                                                                                                                                                                                                                                                                                    |
| --- | ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0   | [Workspace and config](phases/workspace-and-config.md) | You nail **where the skill runs**: `**skill_path`** vs `**skill_workspace`**, install `**conf/abd-config.json**` (see `**[conf/abd-config.json](conf/abd-config.json)**`), **set `active_skill_workspace`**, optional `**known_skill_workspaces**`, overrides, scaffold adding `**conf/**` when greenfield. | Human / AI | Skill directory; customer/project tree you target | `**conf/abd-config.json**` correct for this skill; terms unambiguous for **1a**/**1b** and **Operator** | `python` `[scripts/set_workspace.py](scripts/set_workspace.py)` — no args prints current; `<path>` sets `active_skill_workspace` in `conf/abd-config.json` ([workspace-and-config](phases/workspace-and-config.md)) · [generate.py](scripts/generate.py) — `python scripts/generate.py --phase workspace-and-config` |


---

## Stage 1 — Plan

**Phase docs:** **[Plan Script Build](phases/plan-script-build.md)** (**1a**, new skill) · **[Plan skill migration](phases/plan-migrate.md)** (**1b**, existing skill — **inventory**, **standards delta**, **user selection** before any moves).


| #   | Phase                                            | Description                                                                                                                                                                                                                                                                                                                                                                                                             | Actor | Input                                                                                                           | Output                                                                                                                                                                                             | Scripts                                                                                        |
| --- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- | --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| 1a  | [Plan Script Build](phases/plan-script-build.md) | You read `**library/`** so you know what “compliant” means for this skill, then you decide how *this* skill will actually be built—delivery, phases, operator chain, workspace—so Stage 2 is not improvised. You write that down as one `**docs/skill-plan.md*`* (plan + **Authoring checklist** section) and only then proceed. Routing: **[Workspace and config](phases/workspace-and-config.md)**—not repeated here. | AI    | **library/** norms internalized; **workspace** (or target repo) where `**docs/skill-plan.md`** will be authored | `**docs/skill-plan.md`** — plan + **## Authoring checklist** (norms aligned with `**library/authoring-checklist.md`**; shape from **[skill-plan template](templates/skill-plan.md.template)**). | [generate.py](scripts/generate.py) — `python scripts/generate.py --phase plan-script-build` |
| 1b  | [Plan skill migration](phases/plan-migrate.md)   | You **inventory** the existing skill on disk (**SKILL.md**, **skill-config.json**, **scripts/build.py**, **content/parts/**), **compare** to **library/** standards, **write** a **[standards-delta](docs/standards-delta.md)**-style table, and **record** which gap **IDs** the user will fix—**planning only**, no bulk moves yet. Routing: **[Workspace and config](phases/workspace-and-config.md)**.           | AI    | Path to existing skill                                                                                          | **[standards-delta](docs/standards-delta.md)**-style delta; **selected** IDs for **[migrate](phases/migrate.md)**                                                                               | [generate.py](scripts/generate.py) — `python scripts/generate.py --phase plan-migrate`      |


---

## Stage 2 — Create or fix the skill

### Purpose

Either **emit** a new compliant **skill** (**greenfield**) or **align** an existing one (**migrate**) without silent wholesale rewrites—then **author** the **instructional** content (`**library/`**, `**rules/`**, richer **process** and **phases**) so the scaffold is **filled**, not just created.

### What you produce

- **Greenfield:** New directory with scaffolded `**SKILL.md`**, `**skill-config.json`**, `**conf/**`, `**content/parts/**`, `**scripts/**`, `**rules/**`, `**test/**`.
- **Migrate:** **Straight execution** of **1b**—**move** files into the right **places**, **patch** only **selected** delta **IDs**; update the delta as **fixed** / deferred.
- **After the tree exists:** `**library/`** and `**rules/`** (and **phase** bodies as needed) that match `**SKILL.md`** purpose, `**docs/skill-plan.md`**, and your **process**—**not** empty placeholders.

### How you know you succeeded

- Greenfield: `**python scripts/build.py`** runs in the new skill; Operator can run against it.
- Migrate: Agreed **IDs** from **1b** are **implemented**; delta rows **fixed**, **deferred**, or **accepted risk** with rationale.
- **Fill parts:** `**build.py`** merges real **library** and **rules** content; **AGENTS.md** reflects the skill’s intent.


| #   | Phase                                                              | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Actor      | Input                                                                                                                                                               | Output                                                                                                                                                                                                                                                                       | Scripts                                                                                                                                                                       |
| --- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2a  | [Scaffold new skill directory](phases/scaffold.md)                 | You choose a **kebab-case** skill id and run the scaffold. It copies from **templates/** at the skill root, creates **conf/**, **content/parts/**, **scripts/**, **rules/**, **test/**, and writes `**docs/skill-plan.md`** from the skill-plan template (checklist from **library**). You get a minimal **process.md**; swap in the **team process plate** when you need a full table. Then `**python scripts/build.py`** in the new skill so **AGENTS.md** and **content/built/** match **parts/**. | Code       | **CLI:** `**--name`**, `**--out`** (empty or non-existent path); **templates/** at skill root                                                                       | **Scaffolded skill directory** at `**--out`**: `**SKILL.md`**, `**skill-config.json**`, `**conf/**`, `**content/parts/**`, `**scripts/**`, `**rules/**`, `**test/**`, `**docs/skill-plan.md**` (from template); `**AGENTS.md**` + `**content/built/**` after `**build.py**`. | [scaffold_skill.py](scripts/scaffold_skill.py) — `python scripts/scaffold_skill.py --name <id> --out <path>` · [build.py](scripts/build.py) — `python scripts/build.py` |
| 2b  | [Migrate existing skill](phases/migrate.md)                        | You **apply** the **1b** plan: **move** and **rename** into the **layout** §3 expects, **patch** only **IDs** the user already selected—**straight delta**, not a second inventory.                                                                                                                                                                                                                                                                                                                   | Human / AI | **Skill path**; **delta** from **1b** with agreed **IDs**                                                                                                           | **Tree** aligned for agreed items; **delta** updated **fixed**/deferred                                                                                                                                                                                                      | [migrate](phases/migrate.md) — procedure only (no single script)                                                                                                              |
| 2c  | [Fill scaffold — library and rules](phases/fill-scaffold-parts.md) | The AI reads **purpose** (**SKILL.md**), **process** outline, `**docs/skill-plan.md`** (phases, suggested rules), and **skill-config** hints, then **authors** `**content/parts/library/`** and `**rules/`** with the user—definitions, must-holds, cross-cutting chunks—not just empty folders. **Content** work after the scaffold **script**, not a second scaffold.                                                                                                                               | Human / AI | **Skill tree** at `**skill_path`** (after **2a** or **2b**); `**docs/skill-plan.md`**; `**SKILL.md`**; `**content/parts/process.md**`; user direction and approvals | `**library/**` and `**rules/**` filled; **process**/**phases** updated when gaps surface; `**build.py`** merges honest **AGENTS.md**                                                                                                                                         | [generate.py](scripts/generate.py) — `python scripts/generate.py --phase fill-scaffold-parts`                                                                              |


---

## Stage 3 — Structural validation (Operator)

### Purpose

Show the **skill** **passes automated checks**: Python files under the configured folders compile (syntax check), **build** finishes, scanners return success. Optionally keep a **test/fixture/** sample in this repo that demonstrates a minimal valid tree (not a product deliverable).

### What you produce

- Exit code **0** from your **Operator** run (or the same steps by hand: **Python compile check** on configured paths, `**python scripts/build.py`**, then **scanners**).
- **AGENTS.md** and **content/built/AGENTS.md** byte-match when static delivery; both reflect the latest **content/parts/**.

### How you know you succeeded

CI or local check run succeeds; `**skill-config.json`** paths match files on disk.


| #   | Phase        | Description                                                                                                                                                                                                                                                                                                                                                                             | Actor | Input                                    | Output                                                                            | Scripts                                                                                                                  |
| --- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- | ---------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| 3   | Run Operator | You run the structural gate: **Python compile check** on paths in `**skill-config.json`**, then `**python scripts/build.py`** (merge + `**operator.build_pipeline**` if present), then `**operator.scanners**`. Fix **source** files—not **AGENTS.md** by hand. Exits **0**. **Rule-bound checks:** **[library/rules-and-automated-checks.md](library/rules-and-automated-checks.md)**. | Code  | Skill directory; `**skill-config.json`** | Exit **0**; **AGENTS.md** + **content/built/** consistent with **content/parts/** | [build.py](scripts/build.py) — `python scripts/build.py` · *(paths in `**operator.scanners`** / `**build_pipeline***` |


---

## Team process plate (other skills)

To author a **rich** `**process.md`** (outcome, principles, per-stage tables), start from **[templates/process-team.md.template](templates/process-team.md.template)** and **[templates/README.md](templates/README.md)**.

## Workspace and config

## Principles

**AI quality — normative rules, scanners, and review.** This shard is injected under **`## Principles`** in phase bundles; the heading above is added by the assembler.

**Scope:** In **abd-skill-builder**, this file is injected as **`## Principles`** and is the **first** section in each AI-chat phase bundle (`python scripts/generate.py --phase <slug>` and `content/parts/phases/built/<slug>.md`). Read it **before** Role, Phase body, Library shards, and Rules for that phase.

---

**Every rule in `rules/` is two things at once:** (1) **Normative advice** — prose the model follows while authoring **`content/parts/`**, **`rules/`**, **`skill-config.json`**, and other skill artifacts. (2) **Checkable expectations** — where this repo ships a **scanner** under **`scripts/`**, it catches common layout or config misses; where it does not, **you** still review against the rule text.

**Example (wrong):** Treating a green **`python scripts/build.py`** as enough while **`AGENTS.md`** still disagrees with **`content/parts/`** or **`phase_rules`** omits a rule you claimed to enforce.

**Example (correct):** Read the **Rules** section in this bundle, align files with **`library/`** norms, run **`python scripts/build.py`** (and **`operator.scanners`** when configured), then **re-read** outputs against each applicable rule.

---

## Layer 1 — Generate with rules

While generating or editing skill artifacts:

- Apply **`rules/*.md`** inlined into this bundle (and related **`library/`** docs).
- Prefer **DO / DON’T** and **good vs bad** fragments inside each rule — they are the contract for *shape*, not only for CI.

---

## Layer 2 — Mechanical checks (this skill)

After you have files on disk, the pipeline can run:

| Mechanism | What it does |
| --------- | ------------ |
| **`python scripts/build.py`** | Merges **process** + per-phase bundles into **`AGENTS.md`** and **`content/built/`**, then runs **`operator.build_pipeline`** (e.g. **`scripts/scanner_skill_builder_layout.py`**) when configured. |
| **`rules/scanners.json`** | Declares **rule → scanner** bindings when your skill uses them; align with **`operator.scanners`**. |

**Example (wrong):** Hand-editing **`AGENTS.md`** while **`build.py`** is supposed to own the merge.

**Example (wrong):** Adding a scanner only in prose — no **`rule_scanner_bindings`** or **`build_pipeline`** step.

**Example (correct):** Fix issues reported by scanners, re-run **build**, keep **`skill-config.json`** paths honest.

Scanners are **necessary** for what they implement; they are **not sufficient** for semantic quality (e.g. a valid tree that still mis-describes what the skill does).

---

## Layer 3 — Adversarial pass (human or AI)

With clean tool output, still ask:

- Does each **rule** that applies to this phase pass **by intent**, not only by letter?
- Would a reviewer see **drift** between **`SKILL.md`**, **`process.md`**, and **`phases/`** even when the tree validates?

Use the **Corrections format** below when fixing issues.

---

## Corrections format

When recording or fixing a problem:

| Field | Content |
| ----- | ------- |
| **Rule** | Rule id or `rules/<file>.md` name |
| **Example (wrong)** | What was done incorrectly |
| **Example (correct)** | What it should be |
| **Scanner or validator** | If applicable — see **`rules/scanners.json`** and **`operator.build_pipeline`** |
| **Likely source** | One of: prompt gap · rule not read · edge case · automation gap |

---

## Do not bypass the documented pipeline

**AI phases** mean: read inputs, reason, update the **source** files this skill owns under **`content/parts/`**, **`rules/`**, and config — not one-off scripts that rewrite merged outputs **instead** of fixing sources. Automation that ships with the skill lives under **`scripts/`** and is wired through **`skill-config.json`** (**`build.py`**, **`build_pipeline`**, **`operator.scanners`**) as documented in **`library/rules-and-automated-checks.md`**.

**Example (wrong):** Patching **`AGENTS.md`** directly to “pass” review while **`process.md`** is unchanged.

**Example (correct):** Edit **`content/parts/`** (or **`rules/`**), run **`python scripts/build.py`**, commit regenerated **`AGENTS.md`** / **`content/built/`** when using **`static_built`**.


---

## Phase

# Workspace and config

This doc is **Workspace and config** in [`../process.md`](../process.md). **All** workspace routing, **`conf/abd-config.json`**, **`active_skill_workspace`**, and related **config** norms live **here**—not scattered through **Plan Script Build** or other phases. Do **Workspace and config** (or read this doc) before you rely on **where the skill runs**.

Emit for an AI session:

```bash
python scripts/generate.py --phase workspace-and-config
```

**Command line (workspace pointer):** From the **skill package root** (the folder that contains **`scripts/`** and **`conf/`**), same as **abd-maps-models-specs** **Set workspace** / **`scripts/set_workspace.py`**:

- `python scripts/set_workspace.py` — prints the configured workspace path string (first non-empty among **`active_skill_workspace`**, then deprecated **`solution_workspace`** / **`skill_space_path`**).
- `python scripts/set_workspace.py <path>` — sets **`active_skill_workspace`** in **`conf/abd-config.json`** to **`<path>`** (resolved; stored **relative to the skill package** when that keeps the value portable, otherwise absolute). Also writes the same string to **`solution_workspace`** for tools that still read the legacy key. **`<path>`** must be an existing directory (the **skill workspace** root — project or solution tree you run against).

Scaffold copies **`scripts/set_workspace.py`** from **abd-skill-builder** into every new skill.

---

## Purpose

Make  **`skill_workspace`**, and **`conf/abd-config.json`** unambiguous for **this** skill. **[`conf/abd-config.json`](../../conf/abd-config.json)** in **abd-skill-builder** (`skills/abd-skill-builder/conf/abd-config.json`) is the **reference file**: same JSON shape for any skill—**create it at your skill root if missing**, then **set `active_skill_workspace`**.

---

## Skill path, skill workspace, and configuration

### Terms (do not conflate)

| Term | Meaning |
| --- | --- |
| **`skill_path`** | The directory where this  **skill package is installed** (`SKILL.md`, `rules/`, `scripts/`, install-time **`conf/`**). **Workspace routing** (when used) reads **`conf/abd-config.json`** at **`skill_path`**: which **skill workspace** is active, and optionally **`known_skill_workspaces`**, so you can **switch** without hunting paths in prose. |
| **`skill_workspace`** | The **root of the project or solution** you are working on right now (e.g. a customer repo). This is the **mandatory “where am I running?”** location. Context defaults (e.g. `context/`) are under this root unless you pass paths explicitly. **Anything generated, created, or rendered by the skill** goes under **`skill_workspace/<skill_directory_name>/`** unless the skill’s workspace config overrides the output folder. |
| **Solution workspace** | Same **root** as **`skill_workspace`** in this pipeline: the solution/project tree—not the skill install folder. |

### Two levels of `conf/`

#### 1. Install: `<skill_path>/conf/abd-config.json`

Canonical example in **abd-skill-builder**: **[`skills/abd-skill-builder/conf/abd-config.json`](../../conf/abd-config.json)**. Same path on disk as **`conf/abd-config.json`** at the **skill root**—**that JSON file** is what you edit.

**If your skill has no `conf/` yet:** create **`conf/abd-config.json`** with the same keys (**`active_skill_workspace`**, **`known_skill_workspaces`**) as the builder skill’s file, then **set `active_skill_workspace`** to your workspace root (absolute preferred). **`.`** means the skill install directory **is** the workspace.

**Required** (when this file is used for routing)

| Key | Meaning |
| --- | --- |
| **`active_skill_workspace`** | Path to the **`skill_workspace`** root (absolute preferred). Skills that **route** through this file need a real value **before** meaningful runs against a customer tree; until then, **`.`** is fine. Relative paths resolve from **`skill_path`** (the skill install directory), not the shell cwd. |

**Optional**

| Key | Meaning |
| --- | --- |
| **`known_skill_workspaces`** | Array of paths (strings) for **other** workspaces this skill has worked on, so tooling or operators can **pick** or **add** a workspace without editing unrelated files. |

**Deprecated (still read by older scripts):** `solution_workspace`, `skill_space_path` — same role as **`active_skill_workspace`**; migrate to **`active_skill_workspace`**.

The install folder does **not** hold customer data or large generated trees—only the skill package and this routing config.

#### 2. Workspace: `<skill_workspace>/conf/` (per workspace)

Each **`skill_workspace`** should have a **`conf/`** directory for **parameters that are unique to that workspace** (and optionally per-skill files inside it). Examples:

- **`solution.conf`** at the workspace root (some skills) or under **`conf/`** as the skill evolves.
- **`conf/abd-config.json`** inside the workspace (e.g. story-synthesizer) for **context paths** and other **workspace-local** settings.

Skills document the exact filenames and precedence.

### Overrides

Environment variables may override for CI or local runs; each skill’s **`README`** or **`scripts/_config.py`** states precedence. Prefer editing **`active_skill_workspace`** in **`conf/abd-config.json`** when you need a stable default.

### New skill from scaffold

When **`scaffold_skill.py`** creates a **new** tree, it may **add** **`conf/abd-config.json`** (and **`conf/README.md`**) if missing—**same shape** as **[`../../conf/abd-config.json`](../../conf/abd-config.json)** in **abd-skill-builder**. **Then** (or any time): **set `active_skill_workspace`**.

---

## Related

- **[`plan-script-build.md`](plan-script-build.md)** — **`docs/skill-plan.md`**; assumes workspace terms are clear after **Workspace and config**.
- **[`conf/README.md`](../../conf/README.md)** — short pointer at **`conf/`** in this repo.


---

## Library



---

### `documentation-standards.md`

# Skill documentation standards

**Canonical:** `skills/abd-skill-builder/content/parts/library/documentation-standards.md` (merged into **`AGENTS.md`**).

Use these rules when you author or refactor **process**, **phase docs**, optional **`docs/`** reference, staged **`content/built/`** output, and **AGENTS.md** for any Open Agent Skill. They prevent tangled cross-cutting docs and unreadable process prose.

## Delivery mode (`static_built` vs `runtime_injection`)

Declare **`delivery.mode`** in **`skill-config.json`** (default **`static_built`**). That flag answers whether the agent relies on **checked-in** **`content/built/`** + **`AGENTS.md`** or on **runtime** assembly from **`rules/`**, library fragments, and phase manifests. Normative definitions, when each applies, and how the two stay in sync are in **`delivery-modes.md`**.

## Workspace configuration

Skills that **route** to a customer tree keep **`conf/abd-config.json`** at **`skill_path`** with **`active_skill_workspace`** (and optional **`known_skill_workspaces`**). The file is **part of the repo**—**edit `active_skill_workspace`** to point at the workspace root (see **[workspace-and-config — Skill path, skill workspace, and configuration](../phases/workspace-and-config.md#skill-path-skill-workspace-and-configuration)**). A host (e.g. SkillField) may override. The install folder does **not** hold the customer project—only pointers. Workspace-local parameters live under **`skill_workspace/conf/`** per skill docs. Do not leave “where we run” only in prose unless the skill documents overrides.

## Agent-facing vs reference (read this first)

**If text is merged into `AGENTS.md`, injected into prompts, or otherwise part of the agent bundle, it belongs under `content/parts/`** (e.g. `process.md`, `phases/<phase>.md`, shared fragments). It does **not** live “only in `docs/`” with the expectation that the agent will see it unless your build copies it in.

**Staged build (`content/built/`):** When a complete file is **assembled** from pieces—e.g. a **base** plus **rules** plus **operator/story roles**—write the **intermediate, fully expanded** markdown under **`content/built/`** (or `content/parts/built/` / `phases/built/` if the skill already uses that layout). Then the final step generates the **complete** artifact (`AGENTS.md`, a single phase handoff, etc.). Do not skip the staged output if you need to diff or review what rules were baked in. (Example pattern: `abd-solution-modeler` uses `phases/built/` for phase specs.)

**`docs/`:** Use for **long-form reference** that operators (or tools) open beside the skill—principles, execution order, invariants, **and** standalone construct write-ups (schemas, package layout) **when** those are **not** duplicated as the sole copy of agent instructions. Phase tables and “what you must do” for the agent still live in **`content/parts/`**; `docs/` may **link** to the same ideas or hold deeper detail. If a norm must be in the agent’s context, mirror or generate it from `content/parts/`, not only from `docs/`.

## Voice and role

Write for the **operator** in **second person** (you, your). Frame the work clearly:

- **Your role** — What you are responsible for in this stage or skill (one or two sentences).
- **What you must do** — Imperatives and phase order (use bullets for several short obligations).
- **What you produce** / **How you know you succeeded** — Outcomes and done criteria.

Prefer **you must**, **you will**, and **then you** (sequence) over passive voice (“the pipeline establishes,” “artifacts are emitted”). Say who runs a script or makes a decision.

## Where content belongs

| Kind | Put it here | Do not |
| --- | --- | --- |
| **Process spine** — stages, phase numbers, tables, links to phase files | `content/parts/process.md` (or skill’s `content/process.md`) | Paste the entire phase table again as a second narrative. |
| **Phase behavior** — steps, checklists, **script invocations**, file paths for **this phase only** | `content/parts/phases/<phase>.md` | Split one phase across three cross-cutting docs; **duplicate** long cross-phase definitions—**link** to **`library/`** instead. |
| **Library shards** — definitions, glossaries, artifact shapes, naming, invariants for ideas that **span multiple phases** | `content/parts/library/<topic>.md` | Phase-local procedures, numbered runbooks, pipeline order, or “run `python scripts/…`” blocks that belong in **`phases/`**. |
| **Baked agent instructions** — bases + rules + roles merged before `AGENTS.md` | Source fragments under `content/parts/`; **output of merge** under `content/built/` (or `phases/built/`) **before** final generation | Edit only the final `AGENTS.md` by hand when a build step should own the merge. |
| **Standalone construct reference** — one artifact contract (schema, validators, chunk layout), diagrams, deep dives | `docs/<descriptive-name>.md` | Treat `docs/` as the **only** place agent-facing norms live; duplicate the “must do” into `content/parts/` or generate into `content/built/`. |
| **Cross-cutting** — principles, execution order, invariants that apply across phases | Usually `docs/` or `content/parts/library/` (e.g. principles prose); **governance rules** that vary by phase: **`skill-config.json`** → **`phase_rules`** / **`every_phase_rules`** + `rules/*.md` (see **`process-approach.md`**). **Link** from `content/parts/` where needed | Restate every phase inside cross-cutting docs; **link** to the process table instead. |

**Reference-doc filenames:** Do **not** prefix `docs/` filenames with phase numbers (e.g. avoid `phase2_terms.md`). Use **descriptive kebab-case** slugs (`terms-mechanisms-contract.md`, `behavioral-story-map.md`). Phase order belongs in `process.md` and `content/parts/phases/`, not in filenames.

**Cross-cutting** is for rules and order that are **not** naturally owned by a single phase. If the text is really about one phase only, prefer that phase’s file in `content/parts/phases/` plus a thin pointer from `docs/` if you keep a global index there.

## Library vs phase documents (split responsibility)

Use this split in **every** skill that has both **`library/`** and **`phases/`**:

- **`library/`** = **structure and meaning** shared across phases (what a thing *is*, how it is named, what fields exist, how it relates to other ideas). Think **reference** and **single source of truth** for multi-phase concepts.
- **`phases/*.md`** = **execution** for one pipeline step (what *you* do next, in order, including **commands** and **done checks**). Think **operator procedure** for *this* phase only.

**Hard bars**

| Layer | Must include | Must not be (move or trim) |
| --- | --- | --- |
| **`library/`** | Stable definitions, tables, schemas, cross-phase vocabulary | Long “how to run this phase” sections; **step sequences**; **script/CLI** runbooks; **phase ordering** or “after phase X…” workflow story |
| **`phases/`** | Short purpose, I/O, **steps**, script lines, checklists, **links** to **`library/`** for deep defs | Entire glossaries or artifact specs duplicated from **`library/`**; normative essays that belong in **`library/`** because **other phases** need the same text |

If a paragraph would still make sense **after renumbering or reordering phases**, it probably belongs in **`library/`** or **`rules/`**, not inside a single **`phases/<slug>.md`**.

**Governance rule in this repo:** [`rules/content-placement.md`](../../rules/content-placement.md).

## Prose style

- Several **short** points → **bullets**.
- One developed idea → **sentences** in a **paragraph**.
- Avoid long **semicolon chains** pretending to be one sentence.
- Avoid narrating **migration** from an old doc or old skill (“formerly §2.6”). Describe **this** skill only.

## Process tables

Keep the **stage narrative** at **intent and outcome**. The **table** holds actors, scripts, refs, and deliverable paths.

Normative column meanings, the required **workspace** phase (**Phase 0** informally), **`Input`/`Output` rules**, and **`build.py`/`generate.py` alignment** are in **[`process-table-standards.md`](process-table-standards.md)**. Use that doc whenever you create or refactor **`process.md`** in another skill.

Optional: an extra **Summary** column per row (**two or three sentences**) is allowed if you keep the abd-skill-builder **seven-column** shape as the default—do not drop **Input** / **Output** / **Scripts** in favor of summary-only rows. For the **maps-models-specs**-style table (**`Script`**, **`Outputs`**, **`Ref`**), put **`Summary`** in the **third** column (after **`#`**, **Phase**) and **`Ref`** **last**—see **`process-table-standards.md`** § Maps / models / specs pipeline table.

## When you edit

1. Update the **smallest** place: phase file or construct doc first.
2. If you are repeating script names and outputs that are **already** in the table, **delete** the repetition and keep purpose or pointer to `phases/`.
3. Regenerate **AGENTS.md** after changing `content/` so agents see the update.


---

### `process-table-standards.md`

# Process table standards (for `process.md`)

**Use this** whenever you author or refactor **`parts/process.md`** (or **`content/parts/process.md`**) so skills stay consistent with **abd-skill-builder** and Operator expectations. Pair with **`skill-standards-section-3.md`** (stages / phases / steps) and **`documentation-standards.md`** (voice, where content lives).

---

## Workspace phase (“Phase 0”) — required for every skill

Every skill that can target a **project tree** or needs unambiguous **where am I running?** semantics must include a **workspace** phase:

| Item | Rule |
| --- | --- |
| **Phase file** | **`parts/phases/workspace-and-config.md`** (or under **`content/parts/phases/`** if your skill uses that layout). Slug: **`workspace-and-config`**. |
| **Process row** | First process-table row **after** any “standards / checklist” preamble; **#** column **`0`** (Phase 0 — workspace first in the pipeline). **Team process plate** (`process-team.md.template`) hard-codes this row; **do not** rename the **Phase** link text to **`Phase 0 — …`** inside the table cell—keep the stable slug title **Workspace and config**. |
| **Heading & name** | Phase document **H1** and links: **Workspace and config** (not **Phase 0 — …** in the phase file’s **H1**). In **`parts/process.md`**, the **section** heading **Phase 0 — Workspace and config** is OK; the **process table** still uses the stable **Phase** column title above. |
| **Config** | **`conf/abd-config.json`** at **`skill_path`** with **`active_skill_workspace`** (and optional **`known_skill_workspaces`**). Same **JSON shape** across skills; see **abd-skill-builder** reference **`conf/abd-config.json`**. |
| **Merge / generate** | **`build.py`** should list **`workspace-and-config`** **first** in the phase merge list when that file exists; **`generate.py --phase workspace-and-config`** must resolve for AI-chat steps. |
| **CLI — `active_skill_workspace`** | Every scaffolded skill includes **`scripts/set_workspace.py`** (copied from **abd-skill-builder**). **Process** row **0** **Scripts** cell must include the same wording as **abd-maps-models-specs** phase **Set workspace**: `` `python` [`scripts/set_workspace.py`](…) — no args prints current; `<path>` sets `active_skill_workspace` in `conf/abd-config.json` ([workspace-and-config](phases/workspace-and-config.md)) `` — then **`·`** and **`generate.py`** for the AI-chat phase when both apply. |

Routing details are **not** duplicated inside **Plan** or **Scaffold** phase bodies—**link** to **`workspace-and-config.md`**.

---

## Process table columns (abd-skill-builder shape)

Use this **seven-column** header (exact labels help readers and tooling):

| Column | Meaning |
| --- | --- |
| **`#`** | **Phase id** in the pipeline: **`0`** for workspace (Phase 0); **`1a` / `1b`** for plan variants; **`2a` / `2b` / `2c`** for create/fix/fill; **`3`** for operator; or your skill’s own scheme. **Order** is this column + stage sections—not filenames. |
| **Phase** | **Linked title** to **`phases/<slug>.md`**. Stable, descriptive name (not `phase-02-foo.md` in the link text). |
| **Description** | **What happens** in this phase: decisions, constraints, pointers to other phase docs for cross-cutting topics. **Not** a second copy of the whole phase file—enough to choose the right doc. |
| **Actor** | **Who runs it:** Human / AI, Code, Human / AI + Code, etc. |
| **Input** | **What you must have** to start: paths, prior artifacts, CLI flags, **not** the phase’s primary deliverable if that deliverable is produced **in** this phase (avoid listing **`docs/skill-plan.md`** as **Input** for **1a** when **1a** creates that file—use *library norms + target workspace* instead). |
| **Output** | **Concrete artifacts** when the phase is done: files, directories, exit criteria. For **scaffold (2a)**, lead with the **scaffolded skill tree** ( **`SKILL.md`**, **`skill-config.json`**, **`conf/`**, **`content/parts/`** or **`parts/`**, **`scripts/`**, **`rules/`**, **`test/`**, **`docs/skill-plan.md`** ), then **`AGENTS.md` / `content/built/`** after **`build.py`**—not only the skill-plan template. |
| **Scripts** | **Commands** with **entry script names**: `python scripts/generate.py --phase <slug>`, `python scripts/build.py`, **`scaffold_skill.py`**. **Do not** pack **rule-bound scanners** here—those are skill-wide; document them under **Rules and automated checks** (see **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**) and run them via **`build.py`** / **`operator.build_pipeline`**. One cell; use **`·`** between multiple commands. |

**Do not** use a vague **Output** that only points at a **template file** when the real outcome is a **written document** or **directory tree**—say the **path** under the skill (e.g. **`docs/skill-plan.md`**).

### Maps / models / specs pipeline table (seven columns, `Script` + `Outputs` variant)

Skills such as **abd-maps-models-specs** use the **same seven-column count** with different labels: **`#`**, **Phase**, **Summary**, **Actor**, **Script**, **Outputs**, **`Ref`**.

- **`Summary`** is the **third** column (after **`#`** and **Phase**) so wide prose sits early in the row and previews well in Markdown renderers.
- **`Ref`** is the **last** column (phase doc links stay the right-hand anchor).

Keep **exact header labels** (**`Outputs`** for concrete artifacts and paths) so tables stay consistent across stages.

---

## Stages vs tables

- **Stage** sections (**`## Stage N — …`**) carry **narrative**: purpose, what you produce, how you know you succeeded.
- **Tables** carry **rows = phases**: Ref, Actor, Input, Output, Scripts. **Steps** stay **inside** phase markdown files, not extra table rows (per §3).

---

## Language

- **Second person** for operator-facing prose in phase files (**you**, **your**); see **`documentation-standards.md`**.
- **Process one-liner** at the top of **`process.md`**: pipeline string with **linked phase names** (e.g. **Workspace and config** → **Plan** → …).
- **Routing** cells: short **“Routing: [Workspace and config](…)—not repeated here.”** instead of repeating **`conf/`** keys.

---

## `build.py` and `generate.py` alignment

When you add or rename a phase:

1. **`parts/phases/<slug>.md`** exists.
2. **`process.md`** has a row with that **Phase** link and **`#`** id.
3. **`scripts/build.py`** — **`PHASE_FILES`** (or equivalent) lists **`slug`** in merge order; **`LIBRARY_FILES`** lists library shards in order.
4. **`scripts/generate_prompt.py`** — resolves **`parts/phases/<slug>.md`** (or **`content/parts/phases/`**); **`generate.py`** stays the thin CLI that delegates to it.
5. Regenerate **`AGENTS.md`** / **`content/built/`** after edits.

---

## Reference

- **Worked example:** **`parts/process.md`** in **abd-skill-builder**.
- **Rich pipeline doc:** **`templates/process-team.md.template`** (team process plate).
- **Workspace normative body:** **`parts/phases/workspace-and-config.md`**.


---

### `delivery-modes.md`

# Agent delivery modes (static build vs runtime injection)

Skills can hand instructions to an **agent** or **executor** (including an EA / orchestrator) in two ways. **Do not mix them in one session without an explicit choice** — same requirement as §3.3 *Assembly model* in [`skill-standards-section-3.md`](skill-standards-section-3.md) (static vs dynamic).

## `AGENTS.md` — always (skill-wide orientation)

**`AGENTS.md`** is the **assembled agent bundle**: how the skill is structured, how phases/steps relate, and how to work with it in general. It should be **assembled for every skill** (typically generated by **`scripts/build.py`**), regardless of **`delivery.mode`**. It is *not* what the mode flag switches on or off.

**What `delivery.mode` actually changes** is how a **single operation** (or phase/step run) gets its **process slice**: either from **pre-generated built output** or from **runtime injection** of sources — see below.

## Flag (system-wide convention)

Declare the mode in **`skill-config.json`** so tools, CI, and humans agree:

```json
"delivery": {
  "mode": "static_built"
}
```

| `delivery.mode` | Meaning |
| --- | --- |
| **`static_built`** | **Default.** When you **run an operation**, the executor uses **process content that has already been merged into `content/built/`** (and similar per-skill layouts): each slice includes the **process part** plus its **library** and **rules** components as produced by the build. **`AGENTS.md`** is still checked in as the skill-wide bundle; **built** trees are the canonical **operation-time** artifacts. Operators run **`python scripts/build.py`** after changing sources; commits include regenerated files. |
| **`runtime_injection`** | When you **run an operation**, the executor **injects** the **process part** and, in documented order, **all** of its **library** and **rules** components from source paths — **without** requiring that slice to exist as a pre-built file under **`content/built/`**. **`AGENTS.md`** is still assembled for orientation; only the **operation-time** merge strategy differs. |

**Default for new skills:** `static_built`. Use **`runtime_injection`** when you want runtime resolution; use **`static_built`** when you want checked-in slices — **both** require the same **documented injection map** (see below).

## Injection map — document regardless of mode

**`delivery.mode` does not decide whether you document injection.** It only decides **pre-generate** (build + commit **`content/built/`**) vs **inject at run time** after each operation. In **both** cases:

1. **Which** source paths (process slice, **`library/`**, **`rules/`**, …) apply **per operation** (phase/step).
2. **In what order** they are merged / concatenated / injected.
3. **How** that matches the **static** merge (same semantics as **`build.py`**, or **deliberate differences** called out).

Keep this in a **single lookup** place — e.g. skill **`README.md`**, a manifest in **`build.py`**, or a **generated manifest** checked in next to **`built/`** — so someone can **change `delivery.mode` later** without re-deriving paths from scattered files. The only thing that changes is **when** material is materialized (build vs runtime), not **what** the skill is allowed to omit from documentation.

## Mode (a) — `static_built`

- **What is delivered:** Generated markdown under **`content/built/`** (and/or `phases/built/`, `content/parts/steps/built/` per skill layout) plus the top-level **`AGENTS.md`** when the build emits it.
- **Operation-time behavior:** Use the **built** slices (process + library + rules already merged for that slice).
- **When it applies:** CI, reviewable diffs, reproducible runs, “what the agent saw” is literally in git.
- **Operator obligation:** After editing **`content/parts/`**, **`rules/`**, or merge inputs, run **`build.py`** and commit outputs.

## Mode (b) — `runtime_injection`

- **What is delivered:** For **operations**, not a single pre-expanded tree under **`built/`**; the **executor** resolves **phase** (or step) → **files** (`rules/…`, `content/parts/library/…`, process slice, etc.) and **injects** them into context in a documented order (full **process part + library + rules** for that operation).
- **`AGENTS.md`:** Still assembled so the agent understands the skill in general; only **per-operation** content is resolved at runtime.
- **When it applies:** Interactive orchestration, rapid iteration without running the full static pipeline each time, or environments where checking in large built blobs is undesirable (still document the tradeoff).
- **Operator / implementer obligation:** Same as **static** mode for the **injection map** — resolution order, equivalence vs static merge, validation — **not** optional just because execution is dynamic. Runtime mode adds: executor must follow the **same** documented map (or list exceptions).

## Staying in sync between modes

1. **Single source of truth** for *meaning* stays in **unbuilt** inputs: **`content/parts/`**, **`rules/`**, **`docs/`** (reference), not in hand-edited **`AGENTS.md`** when a build owns the merge.
2. **`static_built`** outputs are **derivatives**: regenerating must be repeatable from the same inputs + **`scripts/build.py`** (and any merge manifest the skill defines).
3. **`runtime_injection`** must **not drift silently**: if both modes are supported, the skill should state whether runtime is a *shortcut to the same merge* (ideal) or a *lighter subset* (then list gaps).
4. **Changing sources:** Under **`static_built`**, CI or pre-commit should run **`build.py`** and fail if **`content/built/`** / **`AGENTS.md`** are stale (exact hook is repo-specific).
5. **Switching modes:** The **injection map** (paths + order + equivalence) is what lets you move from **`static_built`** to **`runtime_injection`** or back — update **`delivery.mode`** and keep the **same** map unless you intentionally change behavior.

## Relation to `build.py` flags

Per §3.3, a skill may expose **`--assembly static|dynamic`** (or equivalent) **inside** `build.py` for *how* static snapshots are produced. That is **orthogonal** to **`delivery.mode`**: `delivery.mode` answers whether the **operator/agent relies on checked-in built files** vs **runtime resolution**. A skill can use `runtime_injection` at execution time while still using `build.py --assembly static` to produce reference snapshots for tests.


---

### `process-approach.md`

# Process approach — IDE, `process.md`, code phases vs AI-chat phases

**Audience:** Authors and tooling. This is the **default mental model** for how a skill is **used** (Cursor, VS Code, Claude Desktop, similar) and how **phases** are executed.

## Who consumes what


| Artifact                                                               | Who uses it                                     | How                                                                                                                                                                                                                                                                                                                      |
| ---------------------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `**AGENTS.md`** (skill root)                                           | **IDE / assistant**                             | Loaded **automatically** by many tools as context for the repo. It orients the model: pipeline, links, where `process.md` lives. **No one “opens `built/` by hand” as the primary workflow** — the chat does not browse the tree to find instructions; **you tell it what to do** using `**process.md`** and phase docs. |
| `**content/parts/process.md**` (or `pieces/process.md` in some skills) | **Human + chat**                                | **Map of phases**: table rows are **phases**, **Ref** links to phase files. The skill should tell users to **read / `@`-reference** this file to know **how to execute** a given phase (order, actor, script). Example pattern: `@agilebydesign-skills/skills/<skill-id>/content/parts/process.md`.                      |
| **Built phase text** (`phases/built/`, `content/built/`, …)            | **Build pipeline + optional `generate_prompt`** | **Generated** outputs — **not** “what autonomous agents read first.” They exist so you can **materialize** a full instruction block for an AI phase (static mode) or **diff in git** under `static_built` delivery.                                                                                                      |


## Phase kinds (two execution styles)

### 1. Code-driven phases (human or CI runs the script)

- **You run** the Python/shell entry point **normally** (terminal, task, CI).
- **Await** exit code and artifacts the phase defines.
- The **phase markdown** (source) describes **how to invoke** the script, **arguments**, **outputs**, and **what “done” means** — not a prompt to paste unless the phase is hybrid.

### 2. AI-chat–driven phases (instructions for the model)

- The **instruction body** the chat must follow is produced by **prompt generation** — short name: **generate prompt** (implementation often `scripts/generate_prompt.py` per skill; names may vary).
- **CLI shape (contract):** support a **phase selector**, e.g. `python scripts/generate_prompt.py --phase <phase_slug>` (some teams use `phase:<name>` as a single token; equivalent intent).
- **Two modes** (both end with “text the user pastes or tool injects into chat”):


| Mode        | What it does                                                                                                                                                                                                                                                            | When to use                                                                |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Dynamic** | Builds one **string** by **collecting every section** required for that phase (source phase markdown, `library/` fragments, applicable `rules/`, manifest order in `skill-config.json` / `build.py`).                                                                   | Fast iteration; single source of truth; no checked-in blob for that phase. |
| **Static**  | Uses **pre-generated** phase text already written under the skill’s **built tree** (convention: `content/parts/phases/built/<phase_slug>.md` or `phases/built/<phase_slug>.md` — **document the path in the skill**). **Grab the whole file** as the instruction block. | Reproducible snapshots, CI, “exactly what shipped last release.”           |


In **either** mode, the **outcome** is: **the IDE chat has the right block of instructions** to follow for that phase — not “the agent navigates to `built/` like a filesystem API.”

### Default `phase_bundle` order (`skill-config.json`)

**abd-skill-builder** `Instructions` (used by `scripts/generate_prompt.py` and typical `scripts/build.py` merges) follows **`phase_bundle.order`** — an array of section tokens — unless `operation_sections` overrides the slug. **Default in this repo and scaffold template:** **`["principles", "role", "phase", "library", "rules"]`** so **`critical-quality-steps.md`** ( **`## Principles`** ) leads every AI-chat bundle. Other skills may reorder (e.g. **`principles`** last) or omit tokens; missing optional files (**`role`**, **`principles`**) are skipped.

Section tokens (each included only if listed in **`order`**):

- **`principles`** — optional: file under `content/parts/library/` (default `critical-quality-steps.md`), heading **`principles_heading`**. **Omitted** if the file is missing.
- **`role`** — optional: file under `content/parts/` (default basename `solution-analyst-role.md`). **Omitted** if the file is missing.
- **`phase`** — `content/parts/phases/<slug>.md` (or `parts/phases/`), with heading **`## Phase`** when `phase_bundle.phase_heading` is set.
- **`library`** — shards from **`PHASE_LIBRARY_SLICES`** for that slug, or all of **`library_files`** when the slice is absent; one **`## Library`** heading, then **`### \`file.md\``** per shard (with `abd:begin` / `abd:end` filtering). **Empty slice** → placeholder body under **`## Library`**.
- **`rules`** — **normative:** governance markdown inlined from **`rules/<stem>.md`** in manifest order. Stems come only from **`skill-config.json`**:
   - **`every_phase_rules`** — array of stems (no `.md`) prepended for **every** phase, **deduplicated** in order (listed once even if also under a phase).
   - **`phase_rules`** — object: keys are **phase slugs** (same strings as **`phase_files`**); values are ordered arrays of stems. Example: `"shaped-story-map": ["evidence-citations-required", "shaped-story-shape"]`.
   **No stems** for a phase → placeholder body under **`## Rules`** (points authors to this doc). Rule files may keep optional YAML frontmatter (e.g. **`rule_id:`**); **`Instructions`** strips it before inlining so bundles stay readable. **Do not** use per-rule **`phase_files:`** frontmatter as the source of truth for which phase gets which rule — that duplicates the manifest and drifts; **abd-maps-models-specs** and **abd-skill-builder** both standardize on **`phase_rules` / `every_phase_rules`**.

Configure (or copy defaults) via **`phase_bundle`** in **`skill-config.json`**: keys include **`order`**, **`role_file`**, **`principles_file`**, and optional **`role_heading`**, **`phase_heading`**, **`library_heading`**, **`rules_heading`**, **`principles_heading`**. **abd-skill-builder** ships the full default object so scaffolded skills inherit the same contract; **abd-maps-models-specs** uses **`MapsInstructions`**, which follows the same **`phase_rules` / `every_phase_rules`** contract (plus maps-only critical-quality notes).

### Library shards with phase markers (`abd:begin` / `abd:end`)

A **`library/*.md`** file may wrap fragments in **`<!-- abd:begin <phase-slug> -->`** … **`<!-- abd:end <phase-slug> -->`** (same slug on both lines). When **`Instructions.assemble_prompt(<phase-slug>)`** runs (used by **`generate_prompt.py`** and **`build.py`** for **`phases/built/<slug>.md`**), the reader sees **all lines outside** those pairs **plus** only the **pair whose slug matches** the current phase. Slugs match **`phase_files`** in **`skill-config.json`** (e.g. **`plan-script-build`**). Files **without** markers are included in full whenever **`PHASE_LIBRARY_SLICES`** lists them for that phase. Authoring template: **`templates/concepts.md.template`**.

## What `build.py` is for

- `**scripts/build.py`** merges **process + library + phases (+ rules where applicable)** into `**AGENTS.md`** and any `**content/built/**` slices per `**delivery.mode**`.
- It is the **authoritative** driver for **this** skill repo. `**generate_prompt`** is **orthogonal**: it answers “what text do I put in chat **for this AI phase**?” while `**build.py`** answers “what ships in **AGENTS.md** / static bundles?”

## Relation to §3

- **Stages / phases / steps** table semantics: `[skill-standards-section-3.md](skill-standards-section-3.md)`.
- **Rule file naming, assembly flags:** same §3 doc.
- **Delivery modes (`static_built` vs `runtime_injection`):** `[delivery-modes.md](delivery-modes.md)`.

## Team process plate (rich `process.md`)

For skills that need the same **shape** as **abd-maps-models-specs** — **outcome**, **principles**, **inputs / outputs**, **stages**, and a **wide phase table** (Description, Actor, Input, Output, Scripts) — start from the **team template**:

- **`content/parts/templates/process-team.md.template`** (in **abd-skill-builder**)
- **`content/parts/templates/README.md`** — how it relates to scaffold’s minimal **`templates/process.md.template`**

Copy the plate into **your** skill as **`content/parts/process.md`**, replace `{{skill_name}}`, add phases and **Ref** links, then run **`python scripts/build.py`**. The **abd-skill-builder** **`process.md`** demonstrates the same structure at production quality.

## Extending a new skill

1. Add `**content/parts/process.md`** with phase rows and **Ref**s (or start from **`process-team.md.template`** above).
2. For each **code phase**, document script + I/O in the phase file.
3. For each **AI-chat phase**, either wire `**generate_prompt`** (dynamic/static) or document a manual copy-paste path until scripted.
4. Run `**python scripts/build.py**` so `**AGENTS.md**` stays the IDE-facing bundle.
5. Keep `**process-approach.md**` behaviors in `**README.md**` in one paragraph so consumers know how your skill expects IDE + chat to work.


---

### `authoring-checklist.md`

# Skill authoring checklist (human + AI)

**Purpose:** Trackable **`- [ ]` / `- [x]`** tasks for building or evolving a skill. **Workspace convention:** keep this content in **`docs/skill-plan.md`** under the **## Authoring checklist** section (one document with the plan). **Scaffold** injects this file there; by hand, paste from here. If you stop mid-work, the next session continues from the **first unchecked** box in that section.

**Canonical source:** `skills/abd-skill-builder/content/parts/library/authoring-checklist.md` — merge updates from here when standards change.

| Role | What to do |
|------|------------|
| **A — Ask** | Use the **Ask:** lines under each section when you need input. |
| **B — Answer / suggest** | As **AI**, fill proposals; human confirms. |
| **C — Track** | Turn `- [ ]` into `- [x]` only when the item is **done**. |

**Normative layout/operator rules** stay in **`skill-repo-standards.md`** and **`skill-standards-section-3.md`** (under **`content/parts/library/`** in **abd-skill-builder**). **How the IDE uses the skill** (AGENTS.md, `process.md`, code vs AI-chat phases, `generate_prompt`): **`process-approach.md`**.

**Runtime vs `docs/`:** All markdown (and other content) that **pertains to how the skill is used at operation time** — merged or injected by **`build.py`**, read as phase bodies, or otherwise part of the **runnable** package — lives under **`content/parts/`** (and **`library/`**, **`rules/`**, etc. per norms). **`docs/`** is **only** for **non-runtime** material: user manuals, **skill plans** (including the checklist section), architecture, standards deltas. **Do not** stash mergeable instruction content in **`docs/`**. (**abd-skill-builder** itself only keeps **`docs/standards-delta.md`**.)

---

## Before you start (every session)

- [ ] **Working copy:** **`docs/skill-plan.md`** includes an **## Authoring checklist** section (scaffold injects this file there; by hand, paste from **`library/authoring-checklist.md`** into that section).
- [ ] **Resume:** Find the **first unchecked** `- [ ]` in the checklist section and continue from there.
- [ ] **Optional:** Note the date and “stopped at §…” in **Gaps / follow-ups** at the bottom when pausing.
- [ ] **`docs/` vs `content/parts/`:** No **runtime** markdown under **`docs/`** — phases, library bodies, and anything **`build.py`** merges/injects stay in **`parts/`**. **`docs/`** = manuals, **skill plan** (with checklist section), architecture, migration notes only.

---

## Greenfield vs existing skill

- [ ] **New skill:** Ran **`scaffold_skill.py`** (or equivalent) so the base tree exists.
- [ ] **Existing skill:** Ran **[plan-migrate.md](../phases/plan-migrate.md)** (**1b**: inventory + **standards-delta** + user chose **IDs**), then **[migrate.md](../phases/migrate.md)** (**2b**: execute moves) **before** bulk edits — **or** consciously skipped with a note in **Gaps / follow-ups**.

---

## Skill identity (what this skill does — not delta to other work)

Normative row: **Documentation focus** in **`skill-repo-standards.md`**.

- [ ] **Process, rules, and docs** describe **what this skill does** and how to run it — **this package**, on its own terms.
- [ ] They do **not** rely on “vs another skill” or “we don’t do X because Y” — that stays out of durable spec.
- [ ] **Dependencies** (other skills, repos, tools, versions) recorded explicitly (**Dependencies** / `README` / `conf/build-strategy.json`) — separate from the main narrative.

**AI should:** Strip migration chatter; put relationships in a **Dependencies** list.

**Ask:** “If this skill vanished, could someone run it from **this repo alone**?”

---

## Base scaffold: what you copy and extend

**Source:** **`skills/abd-skill-builder/scripts/scaffold_skill.py`** + **`skills/abd-skill-builder/templates/*`** — extend these files; don’t invent a parallel layout.

### Scaffold files present and reviewed (check each)

- [ ] **`SKILL.md`** — frontmatter + description make sense.
- [ ] **`skill-config.json`** — `operator.*`, `delivery.mode` match intent; if **`rules/*.md`** back AI-chat phases, **`phase_rules`** / **`every_phase_rules`** list every rule stem for the right **phase slug** (**[`process-approach.md`](process-approach.md)** — *rules* in the default **`phase_bundle`**).
- [ ] **`conf/build-strategy.json`** — `skill_purpose` and siblings filled per Strategizer.
- [ ] **`conf/abd-config.json`** — **`active_skill_workspace`** set (under **`test/`** when using a workspace); optional CLI: **`python scripts/set_workspace.py <path>`**.
- [ ] **`scripts/set_workspace.py`** — present (scaffold copies from **abd-skill-builder**).
- [ ] **`conf/README.md`** — conf usage clear.
- [ ] **`content/parts/process.md`** — pipeline table matches real phases.
- [ ] **`content/parts/phases/`** — one file per row in **`process.md`** (add/rename beyond **`author.md`** as needed).
- [ ] **`content/parts/phases/built/`** — present when you use **static** AI-chat prompts; populate via **`build.py`**; see **`process-approach.md`**.
- [ ] **`scripts/generate_prompt.py`** — present for AI-chat phases; **`--mode dynamic`** vs **`static`** documented; extend per skill.
- [ ] **`scripts/build.py`** — merge/injection driver present (see non-negotiables below).
- [ ] **`scripts/scanner_smoke.py`** — replaced or supplemented with real scanners if needed.
- [ ] **`rules/README.md`** + **`rules/scanners.json`** — wired when rules exist.
- [ ] **`test/README.md`** — explains layout; workspace path if used.
- [ ] **`content/parts/library/`** — created when cross-cutting chunks exist; wired in **`build.py`** (e.g. **`PHASE_LIBRARY`**) per §3.

### Non-negotiables

- [ ] **`scripts/build.py`** is the **merge / injection driver** (writes at least **`AGENTS.md`** from process + phases).
- [ ] **`process.md`** order matches **`phases/`** and **`build.py`** (if order ≠ lexicographic sort of filenames, **`build.py`** uses an **explicit ordered list**, not **`sorted(glob)`**).
- [ ] **Process → operation injection** documented in/near **`build.py`** + human-readable place for §4.

### Reference templates read (when extending)

- [ ] Read **`abd-skill-builder/parts/library/process-table-standards.md`** — process **`#`**, **Phase**, **Description**, **Actor**, **Input**, **Output**, **Scripts**; **workspace** phase (**Phase 0**) required.
- [ ] Opened **`abd-skill-builder/templates/child_build.py.template`** (minimal merge).
- [ ] If per-operation bundles / library injection: reviewed **`abd-maps-models-specs/scripts/build.py`** (`PHASE_FILES`, `PHASE_LIBRARY`, built phases).

### Extension work (after §§0–4 answers)

- [ ] **One** **`build.py`** — no second hidden merge pipeline.
- [ ] **`process.md`**, **`phases/*.md`**, **`build.py`** updated **together** when adding/changing a phase.
- [ ] **`content/parts/library/`** chunks added and wired in **`build.py`** where needed.
- [ ] **Injection map** in **`build.py` docstring** and/or skill **`README.md`** (aligns with §4).
- [ ] **`python scripts/build.py`** run after structural edits; **`AGENTS.md`** / **`content/built/`** committed if **`static_built`**.

**Ask:** “Which files do we **edit** vs **add**? Where is the **ordered phase list** in **`build.py`**?”

---

## 0. Build intent (`conf/build-strategy.json`)

- [ ] **`conf/build-strategy.json`** complete per **`agentic-skill-builder`** (template + Strategizer).

**Ask:** “What must this skill accomplish end-to-end? Who runs it? What is out of scope?”

---

## 1. Process & phases

- [ ] **`parts/process.md`** (or **`content/parts/process.md`**) lists the real pipeline (ordered phases) and follows **[`process-table-standards.md`](process-table-standards.md)** — column meanings, **Input**/**Output** semantics, **Scripts** cell.
- [ ] **Workspace phase (Phase 0):** **`parts/phases/workspace-and-config.md`** exists; **`conf/abd-config.json`** + **`active_skill_workspace`** documented; first process row uses **`0`** in **`#`** and the phase name **Workspace and config** (see standards doc).
- [ ] Phase files use **descriptive slugs**; order matches **`process.md`** and **`build.py`** (explicit order if not sort order).
- [ ] **`build.py`** phase list / merge keys updated when **`process.md`** changes.
- [ ] **Phase vs library:** Each **`phases/<slug>.md`** is **procedure** for that phase (steps, scripts, checklists)—**not** a dump of cross-phase definitions (**[`documentation-standards.md`](documentation-standards.md)** → *Library vs phase documents*; **[`rules/content-placement.md`](../../rules/content-placement.md)**).

**Ask:** “Phases in order?”

---

## 2. Rules (optional) & scanners

- [ ] Decided if **`rules/`** is needed.
- [ ] Listed planned **`rules/*.md`** files (one concern per file where possible).
- [ ] Decided scanner vs doc-only for each rule cluster.
- [ ] **Base framework** (when checks exist): read **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** — **`rules/scanners.json`** **`rule_scanner_bindings`** for each machine-checked rule; **`skill-config.json`** **`operator.build_pipeline`** lists ordered post-merge steps for **`build.py`**; **`operator.scanners`** lists the same scanner paths (or a superset) for **Operator** / CI.
- [ ] **`process.md`** does **not** treat scanners as phase-local “script column” noise; skill-level **Rules and automated checks** (or link to **`rules-and-automated-checks.md`**) instead.

**Ask:** “Machine-checked vs human-reviewed? What would each scanner inspect?”

---

## 3. Library — cross-cutting concepts (`content/parts/library/`)

- [ ] Cross-cutting content in **`library/<slug>.md`** (or skill-specific equivalent).
- [ ] **`build.py`** merge order matches how phases reuse library.
- [ ] Optional **index** (short links only: **`README`**, **`conf/build-strategy.json` notes**, or a **`docs/*` index** if non-runtime) — **not** a second home for bodies; full cross-cutting copy stays in **`library/`** (see **`docs/` vs parts** in **`skill-repo-standards.md`**).
- [ ] Same concept **names** across phases.
- [ ] **Library stays non-procedural:** **no** numbered “how to run a phase” sequences, **no** phase ordering story, **no** phase-specific **`python scripts/…`** runbooks—those stay in **`phases/`** and **`process.md`** (**[`rules/content-placement.md`](../../rules/content-placement.md)**).

**Ask:** “What repeats across phases → **library**?”

---

## 4. Agent delivery mode (`skill-config.json` → `delivery.mode`)

See **`abd-skill-builder`** [`delivery-modes.md`](content/parts/library/delivery-modes.md) (canonical: `skills/abd-skill-builder/content/parts/library/delivery-modes.md`).

- [ ] **`AGENTS.md`** assembled (both modes).
- [ ] **Injection / merge map** documented (paths per operation, order, equivalence to static) — **`README`**, **`build.py`**, or manifest — so mode can change later (narrative-only; sources remain under **`content/parts/`**).
- [ ] **`delivery.mode`** set: **`static_built`** or **`runtime_injection`**.
- [ ] If **`static_built`**: **`build.py`** run; **`content/built/`** (and peers) committed; traceable to map.
- [ ] If **`runtime_injection`**: runtime follows documented map (or deltas documented).

**Ask:** “Per operation: which files, which order, where is the lookup?”

---

## 5. `test/` — script tests & fixtures

- [ ] Chose: pytest **yes** or **no** (if no, skip pytest bullets; may still use **`test/`** for fixtures).
- [ ] If pytest **yes**: dev deps + **`pip install`** documented (**`requirements-dev.txt`** or **`pyproject.toml`**).
- [ ] **Run command** documented (e.g. **`python -m pytest test/`**).
- [ ] **CI** runs tests (optional).
- [ ] Tests live under **`test/`**; **`test/fixture/`** if needed.
- [ ] **`active_skill_workspace`** path under **`test/<name>/`** documented if set.

**Ask:** “What must stay green? Best fixture?”

---

## 6. Operator contract — “built the skill”

- [ ] **`SKILL.md`** + frontmatter.
- [ ] **`skill-config.json`** paths match disk.
- [ ] **`python scripts/build.py`** exits **0**.
- [ ] **Python compile check** on **`operator.compileall_paths`** passes (Operator uses Python’s **`compileall`** under the hood).
- [ ] **Scanner** scripts exit **0** (if any).

**Ask:** “Operator green?”

**Final:**

- [ ] **Attest** structurally built — **or** list gaps below.

---

## Gaps / follow-ups (free text)

Use for **resume notes** (date, last § completed, blockers):

```text


```

---

## How to use this file

1. **Ensure** **`docs/skill-plan.md`** has an **## Authoring checklist** section (scaffold injects from **`abd-skill-builder`** **`content/parts/library/authoring-checklist.md`**) before deep work.
2. Check **`- [x]`** only when done; **first unchecked** = resume point.
3. Pull updates from **`abd-skill-builder`** canonical copy when standards change.


---

### `skill-repo-standards.md`

# Skill repository standards (index + extras)

**Process approach (IDE, `process.md`, code vs AI phases, `generate_prompt`):** [`process-approach.md`](process-approach.md) — **start here** for how skills are **used** in Cursor / similar: **`AGENTS.md`** auto-loaded, **`@…/process.md`** for phase map, **code phases** vs **AI-chat phases**, **dynamic vs static** prompt generation.

**Full normative §3 (all subsections):** [`skill-standards-section-3.md`](skill-standards-section-3.md) — directory and content conventions (**§3.1**), rule naming (**§3.2**), assembly (**§3.3**), reference notes (**§3.4**): stages/phases/steps, process tables, optional domain+story-map pattern, `AGENTS.md` / `content/built/`.

**Rules + scanners + build pipeline (base framework):** [`rules-and-automated-checks.md`](rules-and-automated-checks.md) — **default** wiring: **`rules/scanners.json`** bindings, **`operator.build_pipeline`** for **`build.py`**, **`operator.scanners`** for Operator; **do not** hang scanners off individual **process** phases.

**Builder vs Operator (summary):** [`builder-vs-operator.md`](builder-vs-operator.md) — **scaffold / generation** path vs **`operator.run_operator()`** validation today.

**Authoring checklist (human + AI):** [`authoring-checklist.md`](authoring-checklist.md) — normative body merged into **AGENTS.md**; in each skill, work the **## Authoring checklist** section inside **`docs/skill-plan.md`** (scaffold injects this file there). **`- [ ]` / `- [x]`** so work can **resume after interruption** (first unchecked box = continue here). Covers scaffold verification, rules/scanners, **library**, **`delivery.mode`**, **`test/`**, operator.

**Migrating an existing skill:** [`../phases/plan-migrate.md`](../phases/plan-migrate.md) (**1b**) — inventory → compare to standards → **delta report** → **user chooses which gap IDs to fix**; then [`../phases/migrate.md`](../phases/migrate.md) (**2b**) — **execute** moves and patches for those IDs only (no silent full rewrites).

**Example delta (this repo):** [`../../docs/standards-delta.md`](../../docs/standards-delta.md) — `abd-skill-builder` inventory vs §3 (delivery, `content/built/`, docs, tests/fixture notes).

---

## Quick layout reminder (before reading the full §3)

| Area | Convention |
|------|------------|
| **Entry** | `SKILL.md` at skill root (frontmatter: `name`, `description`). |
| **Operator config** | `skill-config.json` — `operator.compileall_paths`, `operator.build_script`, **`operator.build_pipeline`** (post-merge steps for **`build.py`**), **`operator.scanners`** (Operator; align paths with rule-bound scanners). See **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**. |
| **Agent delivery** | `skill-config.json` — `delivery.mode`: **`static_built`** (pre-generate per-operation slices into **`content/built/`**) or **`runtime_injection`** (resolve the **same** sources at run time). **Only** that choice differs — always document **which paths** feed each operation, **merge order**, and **equivalence** to static output, in a **lookup** place (skill **`README.md`**, **`build.py`** manifest, or emitted manifest) so the team can switch modes later. **`AGENTS.md`** in **both** modes. See **`abd-skill-builder`** [`delivery-modes.md`](delivery-modes.md) (canonical: **`content/parts/library/delivery-modes.md`**). |
| **Authoring prose (normative for writers)** | [`documentation-standards.md`](documentation-standards.md) — voice, where content belongs, process tables; complements **`docs/` vs `content/parts/`** rule. |
| **Workspace routing** | **[workspace-and-config](../phases/workspace-and-config.md#skill-path-skill-workspace-and-configuration)** — **`skill_path`**, **`skill_workspace`**, **`conf/abd-config.json`** keys (**Workspace and config**). |
| **Build intent** | `conf/build-strategy.json` — strategize loads this **whole JSON**; **`skill_purpose`** must be non-empty for **`strategy_complete`** (minimum to finish strategize). Other keys are **siblings** that enrich **`strategy`** / **`builder_manifest`** — they are **not** part of the **`skill_purpose`** text. See **`agentic-skill-builder/README.md`** (Strategizer). |
| **Normative content** | `content/parts/` — process table rows are **phases**; **steps** inside phase files. Phase markdown files use **descriptive slugs** (`terms-mechanisms.md`, …) — **not** `phase-NN-…` or phase numbers in **H1** titles; pipeline order is **only** in `process.md` (# column) + `build.py` merge list (see **`skill-standards-section-3.md`**). **Column definitions** and required **workspace** row: **`process-table-standards.md`**. |
| **docs/ (non-runtime only)** | **`docs/`** is for material **not** consumed as merged/injected skill payload at operation time: **user manuals**, **migration/planning notes**, **architecture**, **`docs/skill-plan.md`** (plan + **Authoring checklist** section), **standards deltas**. In **abd-skill-builder**, **`docs/`** is only **`standards-delta.md`** — delivery merge order lives in **`README.md`**. **Do not** put markdown (or other assets) in **`docs/`** that **`build.py` merges**, **injects**, or **ships** as the runnable instruction body for phases/operations — that belongs under **`content/parts/`** (including **`library/`**, **`phases/`**, **`process.md`**, **`rules/`** as applicable). |
| **Library** | `content/parts/library/` — **cross-cutting meaning** reused across more than one phase: definitions, tables, glossaries, named concepts, artifact shapes. **Not** phase procedures, **not** step-by-step runbooks, **not** CLI blocks for a single phase, **not** pipeline order (that is **`process.md`** + **`phases/`**). The library **is** the home for that shared meaning; do not maintain a parallel “cross-cutting” layer elsewhere. **`docs/`** may hold a **short index** pointing into **`library/`**; **bodies** live in **`library/`**; merge order lives in **`build.py`**. See **`documentation-standards.md`** → *Library vs phase documents*. |
| **Phases** | `content/parts/phases/<slug>.md` — **person-to-process** instructions for **one** process-table row: I/O, **steps**, scripts, done criteria. **Link** to **`library/`** for deep definitions; avoid duplicating large normative blocks that belong in **`library/`** because multiple phases need them. |
| **Rules** | `rules/*.md` or `content/parts/rules/*.md`; optional `rules/scanners.json`. |
| **Scripts** | `scripts/build.py` (**required** — merge/injection driver; scaffold template is minimal; extend with explicit phase order + per-operation bundles as in **`abd-maps-models-specs`** when needed), scanners, optional `_config.py`. See **`authoring-checklist.md`** → *Base scaffold*. |
| **Tests & fixtures** | **`test/`** — all automated tests for the skill (pytest, smoke scripts, etc.) that exercise **`scripts/`**; optional **`test/fixture/<scenario>/`** for frozen inputs/snapshots; optional **`test/<workspace>/`** dirs when **`conf/abd-config.json`** uses **`active_skill_workspace`** (path relative to skill root). Example: **`abd-maps-models-specs/test/`** — workspace **`test/sample-workspace`**, optional fixture **`test/fixture/<scenario>/`**. **`abd-skill-builder`** itself **does include** **`test/`** (see **`test/README.md`** + **`test/fixture/toy-polite-dialogue/`**) even though **pytest `test_*.py` files** are still optional follow-ups — do not read “pytest wiring pending” as “no **`test/`** folder.” **Operator today** only runs a **Python compile check** on **`operator.compileall_paths`** (usually **`["scripts"]`**; implemented with **`compileall`**) — it does **not** install or run **pytest**. If automated tests are **in scope**, add the **wiring** below. |
| **Agent bundle (always)** | `AGENTS.md` — assembled agent bundle (skill-wide “how it works”); typically generated by `build.py`; **not** gated on `delivery.mode`. |
| **Built slices (operation-time, static mode)** | `content/built/` — pre-merged process + library + rules per skill layout when `delivery.mode` is **`static_built`**. |
| **Documentation focus (this skill only)** | Process plans, **rules**, and **docs** describe **what this skill does** — in positive, runnable terms for **this** package. **Do not** use them as a running commentary on how this skill **differs** from another skill, or why it **doesn’t** do something “because another skill does.” That is **local context in time**, not part of the durable skill. **Dependencies** (other skills, tools, repos, contracts) are **explicit** — names, links, versions — in a **Dependencies** section, `README`, or build-strategy notes. That is **not** the same as narrating deltas to sibling work. |

**Minimal valid skill:** `SKILL.md` + `scripts/build.py` + `skill-config.json` with operator block — see **`test/fixture/toy-polite-dialogue/`** in this skill (**`abd-skill-builder`**).

---

## When automated tests are asked for (pytest wiring)

If the skill should run **pytest** (or similar) under **`test/`**, do **not** assume it is already installed or wired into **`operator`** — add it explicitly:

| Step | What to do |
|------|------------|
| **Dependency** | Add **`pytest`** (and dev-only plugins if needed) to a **`requirements-dev.txt`**, **`pyproject.toml`** `[project.optional-dependencies] dev`, or the skill’s documented venv install step — **commit** the file so others can `pip install -r …`. |
| **Layout** | Tests live under **`test/`** (e.g. **`test/test_*.py`** or **`test/<suite>/`**); shared fixtures in **`test/fixture/`** or **`conftest.py`** as usual for pytest. |
| **Run command** | Document in skill **`README.md`** or **`test/README.md`**: e.g. `python -m pytest test/` from skill root (with venv activated). |
| **CI (optional)** | Add a workflow or monorepo job that installs dev deps and runs the same command. |
| **Operator** | **`operator.run_operator()`** does **not** run pytest by default. To gate releases on tests, extend **CI** or a **wrapper script**; only add **`test`** to **`compileall_paths`** if you intentionally want bytecode checks on test modules (unusual). |

---

## Operator checklist (machine-runnable)

1. `SKILL.md` present.
2. `skill-config.json` parses; `operator` block consistent with files on disk.
3. Python files on declared paths pass a **compile check** (Operator uses **`compileall`**).
4. `python scripts/build.py` exits 0.
5. Each listed **scanner** in **`operator.scanners`** exits **0** (and any step in **`operator.build_pipeline`** that **`build.py`** runs also exits **0** when you rely on **`build.py`** as the full local gate).
6. **`rule_scanner_bindings`** (in **`rules/scanners.json`** when used): each **`rule_file`** and **`scanner`** path exists.

---

## What greenfield scaffold should emit

**`scripts/scaffold_skill.py`** (and equivalent generators) should produce a **complete, runnable skeleton**: file tree, `skill-config.json`, phase markdown stubs, `rules/` / `conf/` as needed, runnable **`build.py`**, optional scanner stubs — **without** baking in customer-specific “gold” domain solutions (those belong in the target workspace, not the template).

This **`abd-skill-builder`** skill ships **templates + `scaffold_skill.py`** as the supported way to create that tree. **`operator.run_operator()`** then validates what is on disk; it does not scaffold new skills by itself.


---

### `skill-standards-section-3.md`

# §3 Skill package layout and content standards

**What this is:** Normative rules for how a **skill repository** is shaped — where **runtime** content lives (`content/parts/`, `rules/`, `build.py`), how **stages / phases / steps** relate, how **process tables** and **Refs** work, optional patterns (e.g. domain + story map), **rule file naming**, and **static vs dynamic** assembly of instructions. **How skills are used in the IDE** (AGENTS.md, `process.md`, code vs AI-chat phases, `generate_prompt`) is defined in [`process-approach.md`](process-approach.md) — read that first.

**How to use it:** Implement **§3.1–§3.4** when authoring or reviewing a skill. Tools and humans use the same rules; nothing here depends on any external “origin” document.

**Scope boundary — skills stay simple:** A **skill package** should express a **linear** pipeline: **stage → phase → (steps inside phase docs)**. The **process table** rows are **phases**, not steps. Keep skills deliberately sequential.

## 3.1 Directory and content conventions

**Hierarchy in the repo:** **Stages** group **phases**. Each **phase** has normative markdown (one file or section per phase, per skill); **steps** live **inside** that phase’s markdown — they are **not** separate rows in the master process table. See **Stages, phases, and steps** below.


| Area                            | Convention                                                                                                        | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Normative content**           | Under /`content/parts/`                                                                                           | Plans, operations, domain narrative — **not** dumped only in chat.                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `**docs/` (non-runtime)**       | /`docs/` at skill root                                                                                            | **User manuals**, **migration/planning notes**, **architecture**, **authoring checklists**, and **narrative** descriptions of delivery. **Do not** put markdown here that `build.py` **merges**, **injects**, or **ships** as the runnable phase/operation body — that belongs under `**content/parts/`** (including `**library/`**, `**phases/`**, `**process.md**`, `**rules/**`).                                                                                                                                   |
| **Phase markdown (source)**     | e.g. /`content/parts/phases/<descriptive-slug>.md`, or one doc per phase with step sections — paths vary by skill | **One row in the process table = one phase.** **Steps** (numbered sub-procedures, “Step 1…”, checklists) are written **inside** this markdown as **normative content of the phase**, not as their own table rows. **Do not** encode execution order in filenames or H1 titles (`phase-02-foo.md`, `# Phase 2 — …`): order belongs in `**process.md`** (the `#` column) and in `**scripts/build.py`**’s explicit file list. Use **stable descriptive** kebab-case slugs so renumbering the plan does not force renames. |
| **Built phase markdown**        | `content/parts/phases/built/<descriptive-slug>.md` and/or `content/built/…` per skill layout | **Generated** from source phase bodies + rules via `scripts/build.py`. **Authors do not hand-edit `built/`.** These files are **materialized instruction blobs** for **static** AI-chat phases and for **`static_built`** delivery — consumed by **`generate_prompt`** (or pasted into chat), **not** by “agents browsing the repo” as the primary UX. IDEs load **`AGENTS.md`**; see [`process-approach.md`](process-approach.md). Folder layout (`phases/built` vs `content/built`) is per skill; document it in **`README.md`**.                                                                                                                                                                                                            |
| **Atomic rules**                | `content/parts/rules/*.md` (or top-level `rules/` in simpler skills)                                              | One concern per file where possible; **names** should encode **phase** and/or **domain concept** + rule name (see §3.2). **Which phase inlines which rule** is declared in **`skill-config.json`** (`phase_rules`, `every_phase_rules`), not scattered in per-rule frontmatter lists.                                                                                                                                                                                                                                                                                                                                                                                               |
| **Roles**                       | `roles/*-role.md`                                                                                                 | One file per **user/agent role** the skill assumes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Process**                     | `content/parts/process.md` or staged process docs                                                                 | **Summary table: each row is a phase** (linked by **Ref** to phase markdown). Stages group those rows. **Steps** appear only **inside** the linked phase files.                                                                                                                                                                                                                                                                                                                                                        |
| **Library markdown**            | `content/parts/library/*.md` (or `parts/library/`)                                                                | **Cross-phase structure and meaning**: definitions, glossaries, artifact shapes, naming, invariants. **Not** phase-local procedures, pipeline ordering, or CLI runbooks—those live in **`process.md`** / **`phases/`** (see **Library vs phase documents** below).                                                                                                                                                                                                                                                     |
| **Repo-facing built artifacts** | `AGENTS.md`, `SKILL.md`, sometimes `README.md`                                                                    | Frequently produced by `scripts/build.py` (merge order per skill). **`AGENTS.md`** is what **IDEs and assistants typically load automatically** for the skill repo.                                                                                                                                                                                                                                                                                                                                                                |
| **Config**                      | `skill-config.json`                                                                                               | Name, version, **`phase_files`**, **`PHASE_LIBRARY_SLICES`**, **`phase_rules`** / **`every_phase_rules`** (ordered rule **stems** inlined per phase bundle — see [`process-approach.md`](process-approach.md)), **`phase_bundle`**, **`operator.compileall_paths`**, **`operator.build_script`**, **`operator.build_pipeline`** (post-merge steps for **`build.py`**), **`operator.scanners`** (Operator gate; align with rule-bound scanners) — skill-specific knobs. See **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** (base framework).                                                                                                                                                                                                                                               |
| **Scripts**                     | `scripts/`                                                                                                        | Operational entry points; may share `_config.py` patterns.                                                                                                                                                                                                                                                                                                                                                                                                                                                             |


### Stages, phases, and steps (how they relate)

**Order is always:** **Stage → Phase → Step** (coarse → mid → finest) — but **only the first two appear as rows** in the master process table. **Steps** are **inside** the phase markdown.


| Term      | Typical meaning                                                                                                                                                                                                                                                                                                                      | Example                                                                                  |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **Stage** | **Coarse pipeline slice** — groups many **phases**; may span days or sessions. Often a heading or section in `process.md` or a staged doc.                                                                                                                                                                                           | **Stage 1 — Extract Context**; **Stage 2 — Map and Model**; **Stage 3 — Specification**. |
| **Phase** | **One row** in the process summary table — the unit of “what we do next” with a **driver**: **human** or **AI actor**. The **Ref** column links to **phase** markdown. Phases answer “are we allowed to proceed?” and **contain** the detailed steps as normative body copy.                                                         | “Corpus audit — Phase N”; **Initiator / Actor** column = human vs AI.                    |
| **Step**  | **Sub-structure inside the phase’s markdown** — numbered instructions, checklists, “Step 1 / Step 2”, optional **suffix letters** (`5a`, `7a`) for companion script runs **within the same phase**. **Not** a row in the process table. Machine state (if any) may still reference `workflow_step` as a **sub-id** inside the phase. | Inside `modules-epics-scaffold-breadth.md`: “1. … 2. … 3a. rebuild index …”              |


**AI-driven phases — how the operation is delivered:** See **[`process-approach.md`](process-approach.md)**. In short: **code-driven** phases = run scripts as documented in the phase file; **AI-chat** phases = produce the instruction block via **`generate_prompt`**-style tooling in **dynamic** (assemble sections) or **static** (use pre-built phase markdown under `phases/built/` or equivalent). The **chat** follows that text; **`built/`** is not “the agent’s filesystem API.”

**Ordering (linear, inside the skill):** Stages order **major outcomes**. **Phases** run in **process table order** (each row = one phase). **Steps** follow the order **written inside** each phase document. **Parallel batches, fan-out, or merge** are **not** modeled as extra table rows; if needed, handle that **outside** the skill package (host app, orchestration, or scripts). **Phases** may **block** a later stage until accepted (e.g. “the indexer phase says rebuild chunks — do not start Stage 2 until accepted”).

**“Process” one-liner:** `content/parts/process.md` (or `parts/process.md`) often opens with a **single pipeline string** (e.g. Context → Foundational spine → …). That line is the **navigation spine**; the **table lists phases** (by stage); **authoritative step detail** lives inside each **Ref**’d phase file.

### Process tables, hyperlinks, and naming in the Ref column

**How the table is built**

- **Rows are phases**, not steps. Columns typically include: `#`, **Phase** (title — sometimes labeled “Step” in legacy tables; **semantically it is the phase**), **Initiator / Actor** (Human→Code, AI, Code), **Script** (if any), **What it does**, **Coverage**, **Ref**, **Inputs**, **Outputs**.
- **Ref** is the **hyperlink hub**: each row points to the **normative markdown for that phase**. **Steps** (numbered sub-procedures) live **inside** that file — not in separate table rows. Python entry points stay in **Script**, not **Ref**.
- **Two-tier phase files:**
  - **Source:** phase markdown authors edit (e.g. `content/parts/phases/<name>.md`, or `parts/steps/<name>.md` when the filename is the **phase** slug — naming varies by skill).
  - **Built:** `content/parts/phases/built/<name>.md` or `content/built/<name>.md` — **rules baked in** from `parts/rules/*.md` via `scripts/build.py`. **Steps remain inside** the built document. Used for **static** prompt generation and **`static_built`** slices — not hand-edited. See [`process-approach.md`](process-approach.md).
- **Cross-links inside the table:** The **Ref** column uses relative markdown links to the **phase** doc, e.g. `[context](parts/context.md)`, `[modules-epics-scaffold-breadth (built)](content/parts/steps/built/modules-epics-scaffold-breadth.md)` (paths vary by skill; **from the skill root** per `AGENTS.md`).

**Naming conventions visible in the table**

- **Phase titles** in the table read like **milestones or operations** (“Parse, curate, chunk, index”, “Integrate and Harmonize”) — stable labels for **phase** / workflow fields. **Finer labels** for **steps inside the phase file** may appear in JSON as `workflow_step` or similar.
- **Phase file names and H1 headings** must **not** duplicate pipeline indices (`phase-00-`, `Phase 3 —` in the title). Those numbers **change** when the plan evolves; **brittle** names churn git history and links. The **Ref** column and `build.py` define order; phase files stay **semantically** named (`story-map.md`, `canonical-context.md`).
- **Letter suffixes** (`5a`, `7a`) describe **sub-steps inside a phase** (e.g. companion script after a numbered step) — **inside the phase markdown**, not extra table rows.

### Concepts and cross-cutting artifacts (generic — all skills)

**This section is the generic rule.** A **skill** packages **concepts** (ideas, definitions, invariants, roles) and **artifacts** (outputs, schemas, manifests) that the workflow references across **multiple stages or phases**. Anything that would be **repeated** if pasted into every phase file should instead live in **its own file** (usually markdown under `content/parts/`, sometimes JSON alongside) so there is a **single source of truth**.


| Guideline           | Meaning                                                                                                                                                                                                         |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **When to extract** | If a concept or artifact **spans** more than one phase (or stage), give it a **dedicated** doc (or structured file) and **link** from phase bodies — do not duplicate long definitions in each phase.           |
| **Naming**          | Conventional filenames (`glossary.md`, `concepts.md`, `artifacts.md`, `roles/`*, etc.) vary by skill; **discover** and **validate** presence from templates and this skill’s `build.py`, not one global layout. |
| **Not every skill** | A minimal skill might only have `SKILL.md`, `content/parts/process.md`, and phase files — **no** separate “domain” or “story map” layer. That is valid.                                                         |


### Library vs phase documents (authoring split)

**`library/`** answers **what** (stable meaning for ideas and artifacts that **more than one** phase touches). **`phases/<slug>.md`** answers **how for this step** (operator procedure: inputs, outputs, ordered steps, **commands**, done checks).

| In **`library/`** | In **`phases/`** (not a second copy of the whole library) |
| --- | --- |
| Definitions, tables, schemas, vocabulary used across phases | Purpose of **this** phase, **steps**, checklists, **script/CLI** lines |
| Single source of truth for a construct that spans the pipeline | **Links** into the right **`library/`** shard for depth |
| Optional injection slices (`abd:begin` / `abd:end`) | **No** long normative essays that other phases would repeat verbatim |

**Do not** put **numbered phase procedures**, **order-of-operations** for the skill, or **phase-to-phase sequencing narrative** in **`library/`**—that belongs in **`process.md`** and the relevant **`phases/`** files. **Do not** park **large** reusable specs only inside one phase file if another phase needs the same text—extract to **`library/`** and link.

Normative detail for writers: [`documentation-standards.md`](documentation-standards.md) and [`../../rules/content-placement.md`](../../rules/content-placement.md).

### Optional pattern — domain narrative + interaction tree (maps-models–class skills only)

Some skills (notably **abd-maps-models-specs** and similar) **choose** to separate **two parallel artifacts** that must stay in sync. **Do not** treat this table as the default for **all** skills — only for skills that explicitly adopt this shape.


| Piece                            | Role                                                                                                                                                                                                    | Typical location (example skill)                                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Domain narrative**             | **State and structure** — modules, **domain concepts** (CRC-style: owns, properties, operations, `extends`, invariants), evidence hooks. Answers **what things are** and **what owns which rules**.     | e.g. `parts/domain.md` + evolving `map-model-spec.json` (`modules_and_epics`, `concepts[]`, chunk citations). |
| **Story map / interaction tree** | **Behavior** — epics, sub-epics, stories, scenarios; **Trigger / Response**; **Pre-Condition**; **Given/When/Then** where required. Answers **who does what** and how behavior references domain state. | e.g. `parts/story-map.md` + nested JSON under epics (`stories`, `sub_epics`, etc.).                           |


**When this pattern applies**

- **Same vocabulary:** Domain concept names (`concepts[].name`) and story references can be held to **one namespace** — scanners may enforce **exact string match** where the skill defines that rule.
- **Evidence ladder / paired edits:** Concepts may carry `evidence_stage`; **domain** vs **journey** edits are **paired** in skills that implement both files.
- Skills **without** this split still use the **generic** rule above: cross-cutting concepts → **their own** markdown (whatever the skill calls them), not repeated per phase.

### Rules and automated checks (default wiring)

For **machine-enforceable** rules, use the **base framework** in **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**:

- Declare **rule → scanner** bindings in **`rules/scanners.json`** (`rule_scanner_bindings`).
- List **ordered post-merge steps** under **`skill-config.json` → `operator.build_pipeline`**; **`scripts/build.py`** runs them after merges (same pattern as **`abd-maps-models-specs`**).
- Keep **`operator.scanners`** consistent with those scripts for **`operator.run_operator()`** / CI.

**Process tables** should **not** enumerate every scanner as if it belonged to a single phase; document automation at the skill level and link **`rules/scanners.json`** + **`build.py`** / **`build_pipeline`**.

## 3.2 Rule file naming (heuristic standard)

Target pattern (flexible regex for validation):

```text
{phase-or-stage}__{domain-concept-or-scope}__{short-rule-name}.md
```

Examples mirror **story synchronizer / maps-models** style: scanners and rules tied to **phase** and **concept** (e.g. `chunks_must_be_referenced`, `concept-layering-scaffold`). **Propose** names from the **phase** + concept + verb (and step text inside the phase doc if needed), then **check uniqueness** under `parts/rules/`.

## 3.3 Assembly model (static vs dynamic)

**Two different “static vs dynamic” pairs** — do not conflate:

1. **`build.py` assembly** (repo artifacts): Each skill ships `scripts/build.py`. It merges **process + library + phases (+ rules)** into **`AGENTS.md`** and optional **`content/built/`**. Flags like `--assembly static|snapshot` are **per skill** when present.

2. **AI-chat prompt generation** (`generate_prompt`): For **AI-driven** phases only — **dynamic** = assemble instruction string from sections; **static** = emit text from **pre-built** phase file under `phases/built/` (or documented path). See [`process-approach.md`](process-approach.md).

**Per skill:** `build.py` is the **authoritative** merge driver for **this** repo; scaffolding **emit or check** trees — they do **not** replace `build.py`.

**Flag on `build.py`:** The skill’s `build.py` may expose **CLI flags** for snapshot vs interactive merge; exact names are per skill. For **prompt** modes, document **`generate_prompt`** (or equivalent) next to **`build.py`** in **`README`** / **`AGENTS.md`**.


| Mode (merge / delivery) | Mechanism                                                                               | When                                                               |
| ----------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Static (merge)**      | `build.py` merges **built-phase** fragments into `AGENTS.md` / `SKILL.md` (and related) | Release, reproducible snapshot; CI; “what ships”.                  |
| **Dynamic (merge)**     | Runtime concatenation by **phase** / **operation** from `skill-config.json` + manifest  | Interactive sessions, partial rebuild, IDE-driven iteration. |


A **host** (CI, IDE, or orchestrator) may emit an **internal** manifest (JSON or YAML) for a **given generation run**, listing which fragments form which artifact for both modes; the skill’s `build.py` **may read** that manifest (or embedded config) when implementing **static** merges and documents how **dynamic** mode resolves fragments at runtime. That manifest is **optional** and **not** a standard every skill must carry — only **documented** `build.py` behavior is.

## 3.4 Reference skills (illustrative)

Other skills in the monorepo **illustrate** patterns (long `AGENTS.md`, phased pipelines, rules + scanners). They are **examples**, not extra requirements. **Operator** checks and layout rules are grounded in **abd-skill-builder** library files and each skill’s **`skill-config.json`** — not in a separate “corpus” file unless your team adds one.


---

### `builder-vs-operator.md`

# Builder vs Operator (today)

**Generation / scaffold (“builder” in the loose sense):** Anything that **emits** a new skill tree — typically **`abd-skill-builder`’s `scripts/scaffold_skill.py`** plus templates — producing `SKILL.md`, `skill-config.json`, phase markdown, `rules/` stubs, `scripts/build.py`, optional scanners. Output should match **§3** layout and avoid embedding customer “gold” solutions in the template.

**Operator (structural gate):** **`agentic-skill-builder`** **`operator.run_operator()`** — validates `skill-config.json`, runs a **Python compile check** on the paths in **`operator.compileall_paths`** (the implementation uses Python’s **`compileall`** module), runs **`operator.build_script`** (typically `python scripts/build.py`), then runs **scanner scripts** listed under **`operator.scanners`**. A normative skill also declares **`operator.build_pipeline`**: the **ordered post-merge steps** that **`build.py`** runs after writing **`AGENTS.md`** / built slices (rule-bound scanners, emitters, manifest, lint—**per skill**). **Rule → scanner** bindings live in **`rules/scanners.json`**; see **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** (base framework for all skills). Operator does **not** create greenfield skills; that is **`scaffold_skill.py`** and authoring.

**This skill’s role:** Ship **standards** under **`content/parts/library/`**, **process + phases**, **`scaffold_skill.py`**, and **templates** so authors get a compliant tree first, then Operator keeps it green.


---

### `rules-and-automated-checks.md`

# Rules and automated checks (base framework for every skill)

**Status:** **Normative default** for Open Agent Skills in this repo. When a skill defines **governance rules** (`rules/*.md`) and wants **machine enforcement**, wire checks this way—not as one-off phase script call-outs.

## What owns what

| Layer | Owns |
| --- | --- |
| **`rules/<stem>.md`** | The **human-readable rule**: scope, must/should, examples, done criteria. |
| **`rules/scanners.json`** | **Which script enforces which rule** — `rule_scanner_bindings[]` maps `rule_id` + `rule_file` → `scanner` path (relative to skill root). Optional top-level **`scanners`** lists scanner scripts for tooling that expects a flat array. |
| **`skill-config.json` → `operator.build_pipeline`** | **Ordered post-merge steps** that **`scripts/build.py`** runs after it writes **`AGENTS.md`** / **`content/built/`** (or your skill’s equivalent). Entries are typically **`scripts/...py`** paths: rule-bound scanners, emitters, manifest generators, rule-example linters, etc. **Empty or omitted** means “merge only” (skills with no automated checks yet). |
| **`skill-config.json` → `operator.scanners`** | **Operator / CI gate** — paths **`agentic-skill-builder`** **`operator.run_operator()`** runs **after** **`operator.build_script`**. **Keep these paths aligned** with the scanner steps you care about (usually the same modules listed in **`build_pipeline`** and/or **`rules/scanners.json`**), so “green build” and “green operator” mean the same checks. |

## What you do not do

- **Do not** treat **scanners** as **phase-owned scripts** in **`process.md`** process tables. Phase rows are for **human/AI procedure** and **merge / emit** entry points (e.g. `python scripts/build.py`), not for listing every validator. If readers need detail, add a short **“Rules and automated checks”** subsection in **`process.md`** that points here and to **`rules/scanners.json`**.
- **Do not** bind scanners only in prose. If a rule is machine-checked, add a **`rule_scanner_bindings`** row and a **`build_pipeline`** step (and **`operator.scanners`** / Operator docs as required by your host).

## Execution flow (mental model)

1. Author edits **`content/parts/`**, **`rules/`**, **`skill-config.json`**.
2. **`python scripts/build.py`** merges instruction bundles, then runs **`operator.build_pipeline`** in order (if present).
3. **Operator** (or CI) runs compile check → **`build.py`** again → **`operator.scanners`** (when configured).

**Reference implementation:** **`abd-maps-models-specs`** — `rules/scanners.json`, **`operator.build_pipeline`** in **`skill-config.json`**, and **`scripts/build.py`** driving the pipeline after merge.

## Scaffolded skills

Greenfield trees from **`scaffold_skill.py`** should ship **`rules/scanners.json`** (even if bindings start empty) and a **`skill-config.json`** fragment that includes **`operator.build_pipeline`** alongside **`operator.scanners`**, so authors extend **one** pattern instead of inventing ad hoc wrappers.

See also: **[`skill-standards-section-3.md`](skill-standards-section-3.md)** (§3.1 config row), **[`builder-vs-operator.md`](builder-vs-operator.md)**, **`rules/README.md`** at the skill root.


---

## Rules

*No rules for this phase. List rule stems (filename without `.md`) under `skill-config.json` → `phase_rules` for this phase slug, and optionally `every_phase_rules` for rules that apply to every phase. See `parts/library/process-approach.md` § Phase bundle — rules.*


---

## Phase: plan-script-build

## Principles

**AI quality — normative rules, scanners, and review.** This shard is injected under **`## Principles`** in phase bundles; the heading above is added by the assembler.

**Scope:** In **abd-skill-builder**, this file is injected as **`## Principles`** and is the **first** section in each AI-chat phase bundle (`python scripts/generate.py --phase <slug>` and `content/parts/phases/built/<slug>.md`). Read it **before** Role, Phase body, Library shards, and Rules for that phase.

---

**Every rule in `rules/` is two things at once:** (1) **Normative advice** — prose the model follows while authoring **`content/parts/`**, **`rules/`**, **`skill-config.json`**, and other skill artifacts. (2) **Checkable expectations** — where this repo ships a **scanner** under **`scripts/`**, it catches common layout or config misses; where it does not, **you** still review against the rule text.

**Example (wrong):** Treating a green **`python scripts/build.py`** as enough while **`AGENTS.md`** still disagrees with **`content/parts/`** or **`phase_rules`** omits a rule you claimed to enforce.

**Example (correct):** Read the **Rules** section in this bundle, align files with **`library/`** norms, run **`python scripts/build.py`** (and **`operator.scanners`** when configured), then **re-read** outputs against each applicable rule.

---

## Layer 1 — Generate with rules

While generating or editing skill artifacts:

- Apply **`rules/*.md`** inlined into this bundle (and related **`library/`** docs).
- Prefer **DO / DON’T** and **good vs bad** fragments inside each rule — they are the contract for *shape*, not only for CI.

---

## Layer 2 — Mechanical checks (this skill)

After you have files on disk, the pipeline can run:

| Mechanism | What it does |
| --------- | ------------ |
| **`python scripts/build.py`** | Merges **process** + per-phase bundles into **`AGENTS.md`** and **`content/built/`**, then runs **`operator.build_pipeline`** (e.g. **`scripts/scanner_skill_builder_layout.py`**) when configured. |
| **`rules/scanners.json`** | Declares **rule → scanner** bindings when your skill uses them; align with **`operator.scanners`**. |

**Example (wrong):** Hand-editing **`AGENTS.md`** while **`build.py`** is supposed to own the merge.

**Example (wrong):** Adding a scanner only in prose — no **`rule_scanner_bindings`** or **`build_pipeline`** step.

**Example (correct):** Fix issues reported by scanners, re-run **build**, keep **`skill-config.json`** paths honest.

Scanners are **necessary** for what they implement; they are **not sufficient** for semantic quality (e.g. a valid tree that still mis-describes what the skill does).

---

## Layer 3 — Adversarial pass (human or AI)

With clean tool output, still ask:

- Does each **rule** that applies to this phase pass **by intent**, not only by letter?
- Would a reviewer see **drift** between **`SKILL.md`**, **`process.md`**, and **`phases/`** even when the tree validates?

Use the **Corrections format** below when fixing issues.

---

## Corrections format

When recording or fixing a problem:

| Field | Content |
| ----- | ------- |
| **Rule** | Rule id or `rules/<file>.md` name |
| **Example (wrong)** | What was done incorrectly |
| **Example (correct)** | What it should be |
| **Scanner or validator** | If applicable — see **`rules/scanners.json`** and **`operator.build_pipeline`** |
| **Likely source** | One of: prompt gap · rule not read · edge case · automation gap |

---

## Do not bypass the documented pipeline

**AI phases** mean: read inputs, reason, update the **source** files this skill owns under **`content/parts/`**, **`rules/`**, and config — not one-off scripts that rewrite merged outputs **instead** of fixing sources. Automation that ships with the skill lives under **`scripts/`** and is wired through **`skill-config.json`** (**`build.py`**, **`build_pipeline`**, **`operator.scanners`**) as documented in **`library/rules-and-automated-checks.md`**.

**Example (wrong):** Patching **`AGENTS.md`** directly to “pass” review while **`process.md`** is unchanged.

**Example (correct):** Edit **`content/parts/`** (or **`rules/`**), run **`python scripts/build.py`**, commit regenerated **`AGENTS.md`** / **`content/built/`** when using **`static_built`**.


---

## Phase

# Phase — Plan Script Build

This is **phase 1a** in [`../process.md`](../process.md) (**Stage 1 — Plan**). Read **library/** norms and produce **`docs/skill-plan.md`** in the skill workspace before scaffold. For **existing** skills, **migration planning** (inventory + **standards delta**) is **[`plan-migrate.md`](plan-migrate.md)** (**1b**), not this file. The **authoring checklist** is a **section inside** that file (not a second document); **scaffold** injects **[library/authoring-checklist.md](../library/authoring-checklist.md)** into the skill-plan template.

**Workspace, `conf/abd-config.json`, `active_skill_workspace`:** **[Workspace and config](workspace-and-config.md)** — full terms and keys under **[Skill path, skill workspace, and configuration](workspace-and-config.md#skill-path-skill-workspace-and-configuration)**. Do **not** re-derive routing here.

## Purpose

Load the **standards in `library/`** so **scaffold** (and, for existing skills, **plan-migrate** + **migrate**) work targets the same rules (§3, operator, **`delivery.mode`**, **`test/`** expectations). Capture the plan and trackable **`- [ ]` / `- [x]`** work in **one** workspace doc: **`docs/skill-plan.md`**, including the **## Authoring checklist** section (normative text from **library/authoring-checklist.md**).

## AI-chat phases: generate (what to read in the AI session)

For any phase that you run as an **AI-chat** step (see **[`process-approach.md`](../library/process-approach.md)**), you **call the generator** with the **phase slug**, then **read the printed text** as the instructions for that session—not improvised prose.

From the **skill root** (where **`scripts/`** lives):

```bash
python scripts/generate.py --phase <phase_slug>
```

- **`<phase_slug>`** — filename of the phase markdown under **`parts/phases/`** (or **`content/parts/phases/`**), **without** `.md`. Example: this file is **`plan-script-build.md`** → `--phase plan-script-build`.
- **`--mode dynamic`** (default) — reads **`phases/<slug>.md`** from source.
- **`--mode static`** — reads **`phases/built/<slug>.md`** after **`build.py`** has materialized it (if your skill uses built phase blobs).

**Scripts:** **[`generate.py`](../../scripts/generate.py)** (entry point) and **[`generate_prompt.py`](../../scripts/generate_prompt.py)** (same CLI). **`build.py`** assembles **AGENTS.md** / bundles; **`generate`** only answers “what instruction block for **this** AI phase?”—orthogonal jobs.

## What you produce

- **`docs/skill-plan.md`** — from [skill-plan.md.template](../../templates/skill-plan.md.template): plan sections **and** the **Authoring checklist** section (paste or merge from **library/authoring-checklist.md** if you are not using scaffold).

## How you know you succeeded

**docs/skill-plan.md** exists under the workspace **docs/**; it reads like a coherent build plan with a working checklist section (first unchecked box = resume)—and you can point to **authoritative** norms in **library/** for anything you asserted.

## Input / output / scripts (summary)

**Inputs:** **`docs/skill-plan.md`** (plan + checklist). **`conf/`** / **`active_skill_workspace`** are covered in **[Workspace and config](workspace-and-config.md)**.

| | |
| --- | --- |
| **Input** | **`docs/skill-plan.md`** workspace (plan + **## Authoring checklist**). |
| **Output** | **`docs/skill-plan.md`** — plan + **## Authoring checklist** (normative body from **library/authoring-checklist.md**). |
| **Scripts / templates** | [skill-plan.md.template](../../templates/skill-plan.md.template) → `docs/skill-plan.md` (checklist injected at scaffold). For **AI-chat** phases: **`python scripts/generate.py --phase <slug>`** — see **[AI-chat phases: generate](#ai-chat-phases-generate-what-to-read-in-the-ai-session)** above. Planning does **not** require **build**. |

## Steps

1. Open [skill-repo-standards](../library/skill-repo-standards.md), [skill-standards-section-3](../library/skill-standards-section-3.md), and [authoring-checklist](../library/authoring-checklist.md) (same content will live under **## Authoring checklist** in **`docs/skill-plan.md`**).
2. Create **`docs/skill-plan.md`** from the skill-plan template (with checklist section filled—scaffold does this in one step when you scaffold a new skill).
3. Work the checklist section and the rest of the plan; leave the next scaffold/migrate steps visible as unchecked until Stage 2.


---

## Library



---

### `documentation-standards.md`

# Skill documentation standards

**Canonical:** `skills/abd-skill-builder/content/parts/library/documentation-standards.md` (merged into **`AGENTS.md`**).

Use these rules when you author or refactor **process**, **phase docs**, optional **`docs/`** reference, staged **`content/built/`** output, and **AGENTS.md** for any Open Agent Skill. They prevent tangled cross-cutting docs and unreadable process prose.

## Delivery mode (`static_built` vs `runtime_injection`)

Declare **`delivery.mode`** in **`skill-config.json`** (default **`static_built`**). That flag answers whether the agent relies on **checked-in** **`content/built/`** + **`AGENTS.md`** or on **runtime** assembly from **`rules/`**, library fragments, and phase manifests. Normative definitions, when each applies, and how the two stay in sync are in **`delivery-modes.md`**.

## Workspace configuration

Skills that **route** to a customer tree keep **`conf/abd-config.json`** at **`skill_path`** with **`active_skill_workspace`** (and optional **`known_skill_workspaces`**). The file is **part of the repo**—**edit `active_skill_workspace`** to point at the workspace root (see **[workspace-and-config — Skill path, skill workspace, and configuration](../phases/workspace-and-config.md#skill-path-skill-workspace-and-configuration)**). A host (e.g. SkillField) may override. The install folder does **not** hold the customer project—only pointers. Workspace-local parameters live under **`skill_workspace/conf/`** per skill docs. Do not leave “where we run” only in prose unless the skill documents overrides.

## Agent-facing vs reference (read this first)

**If text is merged into `AGENTS.md`, injected into prompts, or otherwise part of the agent bundle, it belongs under `content/parts/`** (e.g. `process.md`, `phases/<phase>.md`, shared fragments). It does **not** live “only in `docs/`” with the expectation that the agent will see it unless your build copies it in.

**Staged build (`content/built/`):** When a complete file is **assembled** from pieces—e.g. a **base** plus **rules** plus **operator/story roles**—write the **intermediate, fully expanded** markdown under **`content/built/`** (or `content/parts/built/` / `phases/built/` if the skill already uses that layout). Then the final step generates the **complete** artifact (`AGENTS.md`, a single phase handoff, etc.). Do not skip the staged output if you need to diff or review what rules were baked in. (Example pattern: `abd-solution-modeler` uses `phases/built/` for phase specs.)

**`docs/`:** Use for **long-form reference** that operators (or tools) open beside the skill—principles, execution order, invariants, **and** standalone construct write-ups (schemas, package layout) **when** those are **not** duplicated as the sole copy of agent instructions. Phase tables and “what you must do” for the agent still live in **`content/parts/`**; `docs/` may **link** to the same ideas or hold deeper detail. If a norm must be in the agent’s context, mirror or generate it from `content/parts/`, not only from `docs/`.

## Voice and role

Write for the **operator** in **second person** (you, your). Frame the work clearly:

- **Your role** — What you are responsible for in this stage or skill (one or two sentences).
- **What you must do** — Imperatives and phase order (use bullets for several short obligations).
- **What you produce** / **How you know you succeeded** — Outcomes and done criteria.

Prefer **you must**, **you will**, and **then you** (sequence) over passive voice (“the pipeline establishes,” “artifacts are emitted”). Say who runs a script or makes a decision.

## Where content belongs

| Kind | Put it here | Do not |
| --- | --- | --- |
| **Process spine** — stages, phase numbers, tables, links to phase files | `content/parts/process.md` (or skill’s `content/process.md`) | Paste the entire phase table again as a second narrative. |
| **Phase behavior** — steps, checklists, **script invocations**, file paths for **this phase only** | `content/parts/phases/<phase>.md` | Split one phase across three cross-cutting docs; **duplicate** long cross-phase definitions—**link** to **`library/`** instead. |
| **Library shards** — definitions, glossaries, artifact shapes, naming, invariants for ideas that **span multiple phases** | `content/parts/library/<topic>.md` | Phase-local procedures, numbered runbooks, pipeline order, or “run `python scripts/…`” blocks that belong in **`phases/`**. |
| **Baked agent instructions** — bases + rules + roles merged before `AGENTS.md` | Source fragments under `content/parts/`; **output of merge** under `content/built/` (or `phases/built/`) **before** final generation | Edit only the final `AGENTS.md` by hand when a build step should own the merge. |
| **Standalone construct reference** — one artifact contract (schema, validators, chunk layout), diagrams, deep dives | `docs/<descriptive-name>.md` | Treat `docs/` as the **only** place agent-facing norms live; duplicate the “must do” into `content/parts/` or generate into `content/built/`. |
| **Cross-cutting** — principles, execution order, invariants that apply across phases | Usually `docs/` or `content/parts/library/` (e.g. principles prose); **governance rules** that vary by phase: **`skill-config.json`** → **`phase_rules`** / **`every_phase_rules`** + `rules/*.md` (see **`process-approach.md`**). **Link** from `content/parts/` where needed | Restate every phase inside cross-cutting docs; **link** to the process table instead. |

**Reference-doc filenames:** Do **not** prefix `docs/` filenames with phase numbers (e.g. avoid `phase2_terms.md`). Use **descriptive kebab-case** slugs (`terms-mechanisms-contract.md`, `behavioral-story-map.md`). Phase order belongs in `process.md` and `content/parts/phases/`, not in filenames.

**Cross-cutting** is for rules and order that are **not** naturally owned by a single phase. If the text is really about one phase only, prefer that phase’s file in `content/parts/phases/` plus a thin pointer from `docs/` if you keep a global index there.

## Library vs phase documents (split responsibility)

Use this split in **every** skill that has both **`library/`** and **`phases/`**:

- **`library/`** = **structure and meaning** shared across phases (what a thing *is*, how it is named, what fields exist, how it relates to other ideas). Think **reference** and **single source of truth** for multi-phase concepts.
- **`phases/*.md`** = **execution** for one pipeline step (what *you* do next, in order, including **commands** and **done checks**). Think **operator procedure** for *this* phase only.

**Hard bars**

| Layer | Must include | Must not be (move or trim) |
| --- | --- | --- |
| **`library/`** | Stable definitions, tables, schemas, cross-phase vocabulary | Long “how to run this phase” sections; **step sequences**; **script/CLI** runbooks; **phase ordering** or “after phase X…” workflow story |
| **`phases/`** | Short purpose, I/O, **steps**, script lines, checklists, **links** to **`library/`** for deep defs | Entire glossaries or artifact specs duplicated from **`library/`**; normative essays that belong in **`library/`** because **other phases** need the same text |

If a paragraph would still make sense **after renumbering or reordering phases**, it probably belongs in **`library/`** or **`rules/`**, not inside a single **`phases/<slug>.md`**.

**Governance rule in this repo:** [`rules/content-placement.md`](../../rules/content-placement.md).

## Prose style

- Several **short** points → **bullets**.
- One developed idea → **sentences** in a **paragraph**.
- Avoid long **semicolon chains** pretending to be one sentence.
- Avoid narrating **migration** from an old doc or old skill (“formerly §2.6”). Describe **this** skill only.

## Process tables

Keep the **stage narrative** at **intent and outcome**. The **table** holds actors, scripts, refs, and deliverable paths.

Normative column meanings, the required **workspace** phase (**Phase 0** informally), **`Input`/`Output` rules**, and **`build.py`/`generate.py` alignment** are in **[`process-table-standards.md`](process-table-standards.md)**. Use that doc whenever you create or refactor **`process.md`** in another skill.

Optional: an extra **Summary** column per row (**two or three sentences**) is allowed if you keep the abd-skill-builder **seven-column** shape as the default—do not drop **Input** / **Output** / **Scripts** in favor of summary-only rows. For the **maps-models-specs**-style table (**`Script`**, **`Outputs`**, **`Ref`**), put **`Summary`** in the **third** column (after **`#`**, **Phase**) and **`Ref`** **last**—see **`process-table-standards.md`** § Maps / models / specs pipeline table.

## When you edit

1. Update the **smallest** place: phase file or construct doc first.
2. If you are repeating script names and outputs that are **already** in the table, **delete** the repetition and keep purpose or pointer to `phases/`.
3. Regenerate **AGENTS.md** after changing `content/` so agents see the update.


---

### `process-table-standards.md`

# Process table standards (for `process.md`)

**Use this** whenever you author or refactor **`parts/process.md`** (or **`content/parts/process.md`**) so skills stay consistent with **abd-skill-builder** and Operator expectations. Pair with **`skill-standards-section-3.md`** (stages / phases / steps) and **`documentation-standards.md`** (voice, where content lives).

---

## Workspace phase (“Phase 0”) — required for every skill

Every skill that can target a **project tree** or needs unambiguous **where am I running?** semantics must include a **workspace** phase:

| Item | Rule |
| --- | --- |
| **Phase file** | **`parts/phases/workspace-and-config.md`** (or under **`content/parts/phases/`** if your skill uses that layout). Slug: **`workspace-and-config`**. |
| **Process row** | First process-table row **after** any “standards / checklist” preamble; **#** column **`0`** (Phase 0 — workspace first in the pipeline). **Team process plate** (`process-team.md.template`) hard-codes this row; **do not** rename the **Phase** link text to **`Phase 0 — …`** inside the table cell—keep the stable slug title **Workspace and config**. |
| **Heading & name** | Phase document **H1** and links: **Workspace and config** (not **Phase 0 — …** in the phase file’s **H1**). In **`parts/process.md`**, the **section** heading **Phase 0 — Workspace and config** is OK; the **process table** still uses the stable **Phase** column title above. |
| **Config** | **`conf/abd-config.json`** at **`skill_path`** with **`active_skill_workspace`** (and optional **`known_skill_workspaces`**). Same **JSON shape** across skills; see **abd-skill-builder** reference **`conf/abd-config.json`**. |
| **Merge / generate** | **`build.py`** should list **`workspace-and-config`** **first** in the phase merge list when that file exists; **`generate.py --phase workspace-and-config`** must resolve for AI-chat steps. |
| **CLI — `active_skill_workspace`** | Every scaffolded skill includes **`scripts/set_workspace.py`** (copied from **abd-skill-builder**). **Process** row **0** **Scripts** cell must include the same wording as **abd-maps-models-specs** phase **Set workspace**: `` `python` [`scripts/set_workspace.py`](…) — no args prints current; `<path>` sets `active_skill_workspace` in `conf/abd-config.json` ([workspace-and-config](phases/workspace-and-config.md)) `` — then **`·`** and **`generate.py`** for the AI-chat phase when both apply. |

Routing details are **not** duplicated inside **Plan** or **Scaffold** phase bodies—**link** to **`workspace-and-config.md`**.

---

## Process table columns (abd-skill-builder shape)

Use this **seven-column** header (exact labels help readers and tooling):

| Column | Meaning |
| --- | --- |
| **`#`** | **Phase id** in the pipeline: **`0`** for workspace (Phase 0); **`1a` / `1b`** for plan variants; **`2a` / `2b` / `2c`** for create/fix/fill; **`3`** for operator; or your skill’s own scheme. **Order** is this column + stage sections—not filenames. |
| **Phase** | **Linked title** to **`phases/<slug>.md`**. Stable, descriptive name (not `phase-02-foo.md` in the link text). |
| **Description** | **What happens** in this phase: decisions, constraints, pointers to other phase docs for cross-cutting topics. **Not** a second copy of the whole phase file—enough to choose the right doc. |
| **Actor** | **Who runs it:** Human / AI, Code, Human / AI + Code, etc. |
| **Input** | **What you must have** to start: paths, prior artifacts, CLI flags, **not** the phase’s primary deliverable if that deliverable is produced **in** this phase (avoid listing **`docs/skill-plan.md`** as **Input** for **1a** when **1a** creates that file—use *library norms + target workspace* instead). |
| **Output** | **Concrete artifacts** when the phase is done: files, directories, exit criteria. For **scaffold (2a)**, lead with the **scaffolded skill tree** ( **`SKILL.md`**, **`skill-config.json`**, **`conf/`**, **`content/parts/`** or **`parts/`**, **`scripts/`**, **`rules/`**, **`test/`**, **`docs/skill-plan.md`** ), then **`AGENTS.md` / `content/built/`** after **`build.py`**—not only the skill-plan template. |
| **Scripts** | **Commands** with **entry script names**: `python scripts/generate.py --phase <slug>`, `python scripts/build.py`, **`scaffold_skill.py`**. **Do not** pack **rule-bound scanners** here—those are skill-wide; document them under **Rules and automated checks** (see **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**) and run them via **`build.py`** / **`operator.build_pipeline`**. One cell; use **`·`** between multiple commands. |

**Do not** use a vague **Output** that only points at a **template file** when the real outcome is a **written document** or **directory tree**—say the **path** under the skill (e.g. **`docs/skill-plan.md`**).

### Maps / models / specs pipeline table (seven columns, `Script` + `Outputs` variant)

Skills such as **abd-maps-models-specs** use the **same seven-column count** with different labels: **`#`**, **Phase**, **Summary**, **Actor**, **Script**, **Outputs**, **`Ref`**.

- **`Summary`** is the **third** column (after **`#`** and **Phase**) so wide prose sits early in the row and previews well in Markdown renderers.
- **`Ref`** is the **last** column (phase doc links stay the right-hand anchor).

Keep **exact header labels** (**`Outputs`** for concrete artifacts and paths) so tables stay consistent across stages.

---

## Stages vs tables

- **Stage** sections (**`## Stage N — …`**) carry **narrative**: purpose, what you produce, how you know you succeeded.
- **Tables** carry **rows = phases**: Ref, Actor, Input, Output, Scripts. **Steps** stay **inside** phase markdown files, not extra table rows (per §3).

---

## Language

- **Second person** for operator-facing prose in phase files (**you**, **your**); see **`documentation-standards.md`**.
- **Process one-liner** at the top of **`process.md`**: pipeline string with **linked phase names** (e.g. **Workspace and config** → **Plan** → …).
- **Routing** cells: short **“Routing: [Workspace and config](…)—not repeated here.”** instead of repeating **`conf/`** keys.

---

## `build.py` and `generate.py` alignment

When you add or rename a phase:

1. **`parts/phases/<slug>.md`** exists.
2. **`process.md`** has a row with that **Phase** link and **`#`** id.
3. **`scripts/build.py`** — **`PHASE_FILES`** (or equivalent) lists **`slug`** in merge order; **`LIBRARY_FILES`** lists library shards in order.
4. **`scripts/generate_prompt.py`** — resolves **`parts/phases/<slug>.md`** (or **`content/parts/phases/`**); **`generate.py`** stays the thin CLI that delegates to it.
5. Regenerate **`AGENTS.md`** / **`content/built/`** after edits.

---

## Reference

- **Worked example:** **`parts/process.md`** in **abd-skill-builder**.
- **Rich pipeline doc:** **`templates/process-team.md.template`** (team process plate).
- **Workspace normative body:** **`parts/phases/workspace-and-config.md`**.


---

### `delivery-modes.md`

# Agent delivery modes (static build vs runtime injection)

Skills can hand instructions to an **agent** or **executor** (including an EA / orchestrator) in two ways. **Do not mix them in one session without an explicit choice** — same requirement as §3.3 *Assembly model* in [`skill-standards-section-3.md`](skill-standards-section-3.md) (static vs dynamic).

## `AGENTS.md` — always (skill-wide orientation)

**`AGENTS.md`** is the **assembled agent bundle**: how the skill is structured, how phases/steps relate, and how to work with it in general. It should be **assembled for every skill** (typically generated by **`scripts/build.py`**), regardless of **`delivery.mode`**. It is *not* what the mode flag switches on or off.

**What `delivery.mode` actually changes** is how a **single operation** (or phase/step run) gets its **process slice**: either from **pre-generated built output** or from **runtime injection** of sources — see below.

## Flag (system-wide convention)

Declare the mode in **`skill-config.json`** so tools, CI, and humans agree:

```json
"delivery": {
  "mode": "static_built"
}
```

| `delivery.mode` | Meaning |
| --- | --- |
| **`static_built`** | **Default.** When you **run an operation**, the executor uses **process content that has already been merged into `content/built/`** (and similar per-skill layouts): each slice includes the **process part** plus its **library** and **rules** components as produced by the build. **`AGENTS.md`** is still checked in as the skill-wide bundle; **built** trees are the canonical **operation-time** artifacts. Operators run **`python scripts/build.py`** after changing sources; commits include regenerated files. |
| **`runtime_injection`** | When you **run an operation**, the executor **injects** the **process part** and, in documented order, **all** of its **library** and **rules** components from source paths — **without** requiring that slice to exist as a pre-built file under **`content/built/`**. **`AGENTS.md`** is still assembled for orientation; only the **operation-time** merge strategy differs. |

**Default for new skills:** `static_built`. Use **`runtime_injection`** when you want runtime resolution; use **`static_built`** when you want checked-in slices — **both** require the same **documented injection map** (see below).

## Injection map — document regardless of mode

**`delivery.mode` does not decide whether you document injection.** It only decides **pre-generate** (build + commit **`content/built/`**) vs **inject at run time** after each operation. In **both** cases:

1. **Which** source paths (process slice, **`library/`**, **`rules/`**, …) apply **per operation** (phase/step).
2. **In what order** they are merged / concatenated / injected.
3. **How** that matches the **static** merge (same semantics as **`build.py`**, or **deliberate differences** called out).

Keep this in a **single lookup** place — e.g. skill **`README.md`**, a manifest in **`build.py`**, or a **generated manifest** checked in next to **`built/`** — so someone can **change `delivery.mode` later** without re-deriving paths from scattered files. The only thing that changes is **when** material is materialized (build vs runtime), not **what** the skill is allowed to omit from documentation.

## Mode (a) — `static_built`

- **What is delivered:** Generated markdown under **`content/built/`** (and/or `phases/built/`, `content/parts/steps/built/` per skill layout) plus the top-level **`AGENTS.md`** when the build emits it.
- **Operation-time behavior:** Use the **built** slices (process + library + rules already merged for that slice).
- **When it applies:** CI, reviewable diffs, reproducible runs, “what the agent saw” is literally in git.
- **Operator obligation:** After editing **`content/parts/`**, **`rules/`**, or merge inputs, run **`build.py`** and commit outputs.

## Mode (b) — `runtime_injection`

- **What is delivered:** For **operations**, not a single pre-expanded tree under **`built/`**; the **executor** resolves **phase** (or step) → **files** (`rules/…`, `content/parts/library/…`, process slice, etc.) and **injects** them into context in a documented order (full **process part + library + rules** for that operation).
- **`AGENTS.md`:** Still assembled so the agent understands the skill in general; only **per-operation** content is resolved at runtime.
- **When it applies:** Interactive orchestration, rapid iteration without running the full static pipeline each time, or environments where checking in large built blobs is undesirable (still document the tradeoff).
- **Operator / implementer obligation:** Same as **static** mode for the **injection map** — resolution order, equivalence vs static merge, validation — **not** optional just because execution is dynamic. Runtime mode adds: executor must follow the **same** documented map (or list exceptions).

## Staying in sync between modes

1. **Single source of truth** for *meaning* stays in **unbuilt** inputs: **`content/parts/`**, **`rules/`**, **`docs/`** (reference), not in hand-edited **`AGENTS.md`** when a build owns the merge.
2. **`static_built`** outputs are **derivatives**: regenerating must be repeatable from the same inputs + **`scripts/build.py`** (and any merge manifest the skill defines).
3. **`runtime_injection`** must **not drift silently**: if both modes are supported, the skill should state whether runtime is a *shortcut to the same merge* (ideal) or a *lighter subset* (then list gaps).
4. **Changing sources:** Under **`static_built`**, CI or pre-commit should run **`build.py`** and fail if **`content/built/`** / **`AGENTS.md`** are stale (exact hook is repo-specific).
5. **Switching modes:** The **injection map** (paths + order + equivalence) is what lets you move from **`static_built`** to **`runtime_injection`** or back — update **`delivery.mode`** and keep the **same** map unless you intentionally change behavior.

## Relation to `build.py` flags

Per §3.3, a skill may expose **`--assembly static|dynamic`** (or equivalent) **inside** `build.py` for *how* static snapshots are produced. That is **orthogonal** to **`delivery.mode`**: `delivery.mode` answers whether the **operator/agent relies on checked-in built files** vs **runtime resolution**. A skill can use `runtime_injection` at execution time while still using `build.py --assembly static` to produce reference snapshots for tests.


---

### `process-approach.md`

# Process approach — IDE, `process.md`, code phases vs AI-chat phases

**Audience:** Authors and tooling. This is the **default mental model** for how a skill is **used** (Cursor, VS Code, Claude Desktop, similar) and how **phases** are executed.

## Who consumes what


| Artifact                                                               | Who uses it                                     | How                                                                                                                                                                                                                                                                                                                      |
| ---------------------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `**AGENTS.md`** (skill root)                                           | **IDE / assistant**                             | Loaded **automatically** by many tools as context for the repo. It orients the model: pipeline, links, where `process.md` lives. **No one “opens `built/` by hand” as the primary workflow** — the chat does not browse the tree to find instructions; **you tell it what to do** using `**process.md`** and phase docs. |
| `**content/parts/process.md**` (or `pieces/process.md` in some skills) | **Human + chat**                                | **Map of phases**: table rows are **phases**, **Ref** links to phase files. The skill should tell users to **read / `@`-reference** this file to know **how to execute** a given phase (order, actor, script). Example pattern: `@agilebydesign-skills/skills/<skill-id>/content/parts/process.md`.                      |
| **Built phase text** (`phases/built/`, `content/built/`, …)            | **Build pipeline + optional `generate_prompt`** | **Generated** outputs — **not** “what autonomous agents read first.” They exist so you can **materialize** a full instruction block for an AI phase (static mode) or **diff in git** under `static_built` delivery.                                                                                                      |


## Phase kinds (two execution styles)

### 1. Code-driven phases (human or CI runs the script)

- **You run** the Python/shell entry point **normally** (terminal, task, CI).
- **Await** exit code and artifacts the phase defines.
- The **phase markdown** (source) describes **how to invoke** the script, **arguments**, **outputs**, and **what “done” means** — not a prompt to paste unless the phase is hybrid.

### 2. AI-chat–driven phases (instructions for the model)

- The **instruction body** the chat must follow is produced by **prompt generation** — short name: **generate prompt** (implementation often `scripts/generate_prompt.py` per skill; names may vary).
- **CLI shape (contract):** support a **phase selector**, e.g. `python scripts/generate_prompt.py --phase <phase_slug>` (some teams use `phase:<name>` as a single token; equivalent intent).
- **Two modes** (both end with “text the user pastes or tool injects into chat”):


| Mode        | What it does                                                                                                                                                                                                                                                            | When to use                                                                |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Dynamic** | Builds one **string** by **collecting every section** required for that phase (source phase markdown, `library/` fragments, applicable `rules/`, manifest order in `skill-config.json` / `build.py`).                                                                   | Fast iteration; single source of truth; no checked-in blob for that phase. |
| **Static**  | Uses **pre-generated** phase text already written under the skill’s **built tree** (convention: `content/parts/phases/built/<phase_slug>.md` or `phases/built/<phase_slug>.md` — **document the path in the skill**). **Grab the whole file** as the instruction block. | Reproducible snapshots, CI, “exactly what shipped last release.”           |


In **either** mode, the **outcome** is: **the IDE chat has the right block of instructions** to follow for that phase — not “the agent navigates to `built/` like a filesystem API.”

### Default `phase_bundle` order (`skill-config.json`)

**abd-skill-builder** `Instructions` (used by `scripts/generate_prompt.py` and typical `scripts/build.py` merges) follows **`phase_bundle.order`** — an array of section tokens — unless `operation_sections` overrides the slug. **Default in this repo and scaffold template:** **`["principles", "role", "phase", "library", "rules"]`** so **`critical-quality-steps.md`** ( **`## Principles`** ) leads every AI-chat bundle. Other skills may reorder (e.g. **`principles`** last) or omit tokens; missing optional files (**`role`**, **`principles`**) are skipped.

Section tokens (each included only if listed in **`order`**):

- **`principles`** — optional: file under `content/parts/library/` (default `critical-quality-steps.md`), heading **`principles_heading`**. **Omitted** if the file is missing.
- **`role`** — optional: file under `content/parts/` (default basename `solution-analyst-role.md`). **Omitted** if the file is missing.
- **`phase`** — `content/parts/phases/<slug>.md` (or `parts/phases/`), with heading **`## Phase`** when `phase_bundle.phase_heading` is set.
- **`library`** — shards from **`PHASE_LIBRARY_SLICES`** for that slug, or all of **`library_files`** when the slice is absent; one **`## Library`** heading, then **`### \`file.md\``** per shard (with `abd:begin` / `abd:end` filtering). **Empty slice** → placeholder body under **`## Library`**.
- **`rules`** — **normative:** governance markdown inlined from **`rules/<stem>.md`** in manifest order. Stems come only from **`skill-config.json`**:
   - **`every_phase_rules`** — array of stems (no `.md`) prepended for **every** phase, **deduplicated** in order (listed once even if also under a phase).
   - **`phase_rules`** — object: keys are **phase slugs** (same strings as **`phase_files`**); values are ordered arrays of stems. Example: `"shaped-story-map": ["evidence-citations-required", "shaped-story-shape"]`.
   **No stems** for a phase → placeholder body under **`## Rules`** (points authors to this doc). Rule files may keep optional YAML frontmatter (e.g. **`rule_id:`**); **`Instructions`** strips it before inlining so bundles stay readable. **Do not** use per-rule **`phase_files:`** frontmatter as the source of truth for which phase gets which rule — that duplicates the manifest and drifts; **abd-maps-models-specs** and **abd-skill-builder** both standardize on **`phase_rules` / `every_phase_rules`**.

Configure (or copy defaults) via **`phase_bundle`** in **`skill-config.json`**: keys include **`order`**, **`role_file`**, **`principles_file`**, and optional **`role_heading`**, **`phase_heading`**, **`library_heading`**, **`rules_heading`**, **`principles_heading`**. **abd-skill-builder** ships the full default object so scaffolded skills inherit the same contract; **abd-maps-models-specs** uses **`MapsInstructions`**, which follows the same **`phase_rules` / `every_phase_rules`** contract (plus maps-only critical-quality notes).

### Library shards with phase markers (`abd:begin` / `abd:end`)

A **`library/*.md`** file may wrap fragments in **`<!-- abd:begin <phase-slug> -->`** … **`<!-- abd:end <phase-slug> -->`** (same slug on both lines). When **`Instructions.assemble_prompt(<phase-slug>)`** runs (used by **`generate_prompt.py`** and **`build.py`** for **`phases/built/<slug>.md`**), the reader sees **all lines outside** those pairs **plus** only the **pair whose slug matches** the current phase. Slugs match **`phase_files`** in **`skill-config.json`** (e.g. **`plan-script-build`**). Files **without** markers are included in full whenever **`PHASE_LIBRARY_SLICES`** lists them for that phase. Authoring template: **`templates/concepts.md.template`**.

## What `build.py` is for

- `**scripts/build.py`** merges **process + library + phases (+ rules where applicable)** into `**AGENTS.md`** and any `**content/built/**` slices per `**delivery.mode**`.
- It is the **authoritative** driver for **this** skill repo. `**generate_prompt`** is **orthogonal**: it answers “what text do I put in chat **for this AI phase**?” while `**build.py`** answers “what ships in **AGENTS.md** / static bundles?”

## Relation to §3

- **Stages / phases / steps** table semantics: `[skill-standards-section-3.md](skill-standards-section-3.md)`.
- **Rule file naming, assembly flags:** same §3 doc.
- **Delivery modes (`static_built` vs `runtime_injection`):** `[delivery-modes.md](delivery-modes.md)`.

## Team process plate (rich `process.md`)

For skills that need the same **shape** as **abd-maps-models-specs** — **outcome**, **principles**, **inputs / outputs**, **stages**, and a **wide phase table** (Description, Actor, Input, Output, Scripts) — start from the **team template**:

- **`content/parts/templates/process-team.md.template`** (in **abd-skill-builder**)
- **`content/parts/templates/README.md`** — how it relates to scaffold’s minimal **`templates/process.md.template`**

Copy the plate into **your** skill as **`content/parts/process.md`**, replace `{{skill_name}}`, add phases and **Ref** links, then run **`python scripts/build.py`**. The **abd-skill-builder** **`process.md`** demonstrates the same structure at production quality.

## Extending a new skill

1. Add `**content/parts/process.md`** with phase rows and **Ref**s (or start from **`process-team.md.template`** above).
2. For each **code phase**, document script + I/O in the phase file.
3. For each **AI-chat phase**, either wire `**generate_prompt`** (dynamic/static) or document a manual copy-paste path until scripted.
4. Run `**python scripts/build.py**` so `**AGENTS.md**` stays the IDE-facing bundle.
5. Keep `**process-approach.md**` behaviors in `**README.md**` in one paragraph so consumers know how your skill expects IDE + chat to work.


---

### `authoring-checklist.md`

# Skill authoring checklist (human + AI)

**Purpose:** Trackable **`- [ ]` / `- [x]`** tasks for building or evolving a skill. **Workspace convention:** keep this content in **`docs/skill-plan.md`** under the **## Authoring checklist** section (one document with the plan). **Scaffold** injects this file there; by hand, paste from here. If you stop mid-work, the next session continues from the **first unchecked** box in that section.

**Canonical source:** `skills/abd-skill-builder/content/parts/library/authoring-checklist.md` — merge updates from here when standards change.

| Role | What to do |
|------|------------|
| **A — Ask** | Use the **Ask:** lines under each section when you need input. |
| **B — Answer / suggest** | As **AI**, fill proposals; human confirms. |
| **C — Track** | Turn `- [ ]` into `- [x]` only when the item is **done**. |

**Normative layout/operator rules** stay in **`skill-repo-standards.md`** and **`skill-standards-section-3.md`** (under **`content/parts/library/`** in **abd-skill-builder**). **How the IDE uses the skill** (AGENTS.md, `process.md`, code vs AI-chat phases, `generate_prompt`): **`process-approach.md`**.

**Runtime vs `docs/`:** All markdown (and other content) that **pertains to how the skill is used at operation time** — merged or injected by **`build.py`**, read as phase bodies, or otherwise part of the **runnable** package — lives under **`content/parts/`** (and **`library/`**, **`rules/`**, etc. per norms). **`docs/`** is **only** for **non-runtime** material: user manuals, **skill plans** (including the checklist section), architecture, standards deltas. **Do not** stash mergeable instruction content in **`docs/`**. (**abd-skill-builder** itself only keeps **`docs/standards-delta.md`**.)

---

## Before you start (every session)

- [ ] **Working copy:** **`docs/skill-plan.md`** includes an **## Authoring checklist** section (scaffold injects this file there; by hand, paste from **`library/authoring-checklist.md`** into that section).
- [ ] **Resume:** Find the **first unchecked** `- [ ]` in the checklist section and continue from there.
- [ ] **Optional:** Note the date and “stopped at §…” in **Gaps / follow-ups** at the bottom when pausing.
- [ ] **`docs/` vs `content/parts/`:** No **runtime** markdown under **`docs/`** — phases, library bodies, and anything **`build.py`** merges/injects stay in **`parts/`**. **`docs/`** = manuals, **skill plan** (with checklist section), architecture, migration notes only.

---

## Greenfield vs existing skill

- [ ] **New skill:** Ran **`scaffold_skill.py`** (or equivalent) so the base tree exists.
- [ ] **Existing skill:** Ran **[plan-migrate.md](../phases/plan-migrate.md)** (**1b**: inventory + **standards-delta** + user chose **IDs**), then **[migrate.md](../phases/migrate.md)** (**2b**: execute moves) **before** bulk edits — **or** consciously skipped with a note in **Gaps / follow-ups**.

---

## Skill identity (what this skill does — not delta to other work)

Normative row: **Documentation focus** in **`skill-repo-standards.md`**.

- [ ] **Process, rules, and docs** describe **what this skill does** and how to run it — **this package**, on its own terms.
- [ ] They do **not** rely on “vs another skill” or “we don’t do X because Y” — that stays out of durable spec.
- [ ] **Dependencies** (other skills, repos, tools, versions) recorded explicitly (**Dependencies** / `README` / `conf/build-strategy.json`) — separate from the main narrative.

**AI should:** Strip migration chatter; put relationships in a **Dependencies** list.

**Ask:** “If this skill vanished, could someone run it from **this repo alone**?”

---

## Base scaffold: what you copy and extend

**Source:** **`skills/abd-skill-builder/scripts/scaffold_skill.py`** + **`skills/abd-skill-builder/templates/*`** — extend these files; don’t invent a parallel layout.

### Scaffold files present and reviewed (check each)

- [ ] **`SKILL.md`** — frontmatter + description make sense.
- [ ] **`skill-config.json`** — `operator.*`, `delivery.mode` match intent; if **`rules/*.md`** back AI-chat phases, **`phase_rules`** / **`every_phase_rules`** list every rule stem for the right **phase slug** (**[`process-approach.md`](process-approach.md)** — *rules* in the default **`phase_bundle`**).
- [ ] **`conf/build-strategy.json`** — `skill_purpose` and siblings filled per Strategizer.
- [ ] **`conf/abd-config.json`** — **`active_skill_workspace`** set (under **`test/`** when using a workspace); optional CLI: **`python scripts/set_workspace.py <path>`**.
- [ ] **`scripts/set_workspace.py`** — present (scaffold copies from **abd-skill-builder**).
- [ ] **`conf/README.md`** — conf usage clear.
- [ ] **`content/parts/process.md`** — pipeline table matches real phases.
- [ ] **`content/parts/phases/`** — one file per row in **`process.md`** (add/rename beyond **`author.md`** as needed).
- [ ] **`content/parts/phases/built/`** — present when you use **static** AI-chat prompts; populate via **`build.py`**; see **`process-approach.md`**.
- [ ] **`scripts/generate_prompt.py`** — present for AI-chat phases; **`--mode dynamic`** vs **`static`** documented; extend per skill.
- [ ] **`scripts/build.py`** — merge/injection driver present (see non-negotiables below).
- [ ] **`scripts/scanner_smoke.py`** — replaced or supplemented with real scanners if needed.
- [ ] **`rules/README.md`** + **`rules/scanners.json`** — wired when rules exist.
- [ ] **`test/README.md`** — explains layout; workspace path if used.
- [ ] **`content/parts/library/`** — created when cross-cutting chunks exist; wired in **`build.py`** (e.g. **`PHASE_LIBRARY`**) per §3.

### Non-negotiables

- [ ] **`scripts/build.py`** is the **merge / injection driver** (writes at least **`AGENTS.md`** from process + phases).
- [ ] **`process.md`** order matches **`phases/`** and **`build.py`** (if order ≠ lexicographic sort of filenames, **`build.py`** uses an **explicit ordered list**, not **`sorted(glob)`**).
- [ ] **Process → operation injection** documented in/near **`build.py`** + human-readable place for §4.

### Reference templates read (when extending)

- [ ] Read **`abd-skill-builder/parts/library/process-table-standards.md`** — process **`#`**, **Phase**, **Description**, **Actor**, **Input**, **Output**, **Scripts**; **workspace** phase (**Phase 0**) required.
- [ ] Opened **`abd-skill-builder/templates/child_build.py.template`** (minimal merge).
- [ ] If per-operation bundles / library injection: reviewed **`abd-maps-models-specs/scripts/build.py`** (`PHASE_FILES`, `PHASE_LIBRARY`, built phases).

### Extension work (after §§0–4 answers)

- [ ] **One** **`build.py`** — no second hidden merge pipeline.
- [ ] **`process.md`**, **`phases/*.md`**, **`build.py`** updated **together** when adding/changing a phase.
- [ ] **`content/parts/library/`** chunks added and wired in **`build.py`** where needed.
- [ ] **Injection map** in **`build.py` docstring** and/or skill **`README.md`** (aligns with §4).
- [ ] **`python scripts/build.py`** run after structural edits; **`AGENTS.md`** / **`content/built/`** committed if **`static_built`**.

**Ask:** “Which files do we **edit** vs **add**? Where is the **ordered phase list** in **`build.py`**?”

---

## 0. Build intent (`conf/build-strategy.json`)

- [ ] **`conf/build-strategy.json`** complete per **`agentic-skill-builder`** (template + Strategizer).

**Ask:** “What must this skill accomplish end-to-end? Who runs it? What is out of scope?”

---

## 1. Process & phases

- [ ] **`parts/process.md`** (or **`content/parts/process.md`**) lists the real pipeline (ordered phases) and follows **[`process-table-standards.md`](process-table-standards.md)** — column meanings, **Input**/**Output** semantics, **Scripts** cell.
- [ ] **Workspace phase (Phase 0):** **`parts/phases/workspace-and-config.md`** exists; **`conf/abd-config.json`** + **`active_skill_workspace`** documented; first process row uses **`0`** in **`#`** and the phase name **Workspace and config** (see standards doc).
- [ ] Phase files use **descriptive slugs**; order matches **`process.md`** and **`build.py`** (explicit order if not sort order).
- [ ] **`build.py`** phase list / merge keys updated when **`process.md`** changes.
- [ ] **Phase vs library:** Each **`phases/<slug>.md`** is **procedure** for that phase (steps, scripts, checklists)—**not** a dump of cross-phase definitions (**[`documentation-standards.md`](documentation-standards.md)** → *Library vs phase documents*; **[`rules/content-placement.md`](../../rules/content-placement.md)**).

**Ask:** “Phases in order?”

---

## 2. Rules (optional) & scanners

- [ ] Decided if **`rules/`** is needed.
- [ ] Listed planned **`rules/*.md`** files (one concern per file where possible).
- [ ] Decided scanner vs doc-only for each rule cluster.
- [ ] **Base framework** (when checks exist): read **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** — **`rules/scanners.json`** **`rule_scanner_bindings`** for each machine-checked rule; **`skill-config.json`** **`operator.build_pipeline`** lists ordered post-merge steps for **`build.py`**; **`operator.scanners`** lists the same scanner paths (or a superset) for **Operator** / CI.
- [ ] **`process.md`** does **not** treat scanners as phase-local “script column” noise; skill-level **Rules and automated checks** (or link to **`rules-and-automated-checks.md`**) instead.

**Ask:** “Machine-checked vs human-reviewed? What would each scanner inspect?”

---

## 3. Library — cross-cutting concepts (`content/parts/library/`)

- [ ] Cross-cutting content in **`library/<slug>.md`** (or skill-specific equivalent).
- [ ] **`build.py`** merge order matches how phases reuse library.
- [ ] Optional **index** (short links only: **`README`**, **`conf/build-strategy.json` notes**, or a **`docs/*` index** if non-runtime) — **not** a second home for bodies; full cross-cutting copy stays in **`library/`** (see **`docs/` vs parts** in **`skill-repo-standards.md`**).
- [ ] Same concept **names** across phases.
- [ ] **Library stays non-procedural:** **no** numbered “how to run a phase” sequences, **no** phase ordering story, **no** phase-specific **`python scripts/…`** runbooks—those stay in **`phases/`** and **`process.md`** (**[`rules/content-placement.md`](../../rules/content-placement.md)**).

**Ask:** “What repeats across phases → **library**?”

---

## 4. Agent delivery mode (`skill-config.json` → `delivery.mode`)

See **`abd-skill-builder`** [`delivery-modes.md`](content/parts/library/delivery-modes.md) (canonical: `skills/abd-skill-builder/content/parts/library/delivery-modes.md`).

- [ ] **`AGENTS.md`** assembled (both modes).
- [ ] **Injection / merge map** documented (paths per operation, order, equivalence to static) — **`README`**, **`build.py`**, or manifest — so mode can change later (narrative-only; sources remain under **`content/parts/`**).
- [ ] **`delivery.mode`** set: **`static_built`** or **`runtime_injection`**.
- [ ] If **`static_built`**: **`build.py`** run; **`content/built/`** (and peers) committed; traceable to map.
- [ ] If **`runtime_injection`**: runtime follows documented map (or deltas documented).

**Ask:** “Per operation: which files, which order, where is the lookup?”

---

## 5. `test/` — script tests & fixtures

- [ ] Chose: pytest **yes** or **no** (if no, skip pytest bullets; may still use **`test/`** for fixtures).
- [ ] If pytest **yes**: dev deps + **`pip install`** documented (**`requirements-dev.txt`** or **`pyproject.toml`**).
- [ ] **Run command** documented (e.g. **`python -m pytest test/`**).
- [ ] **CI** runs tests (optional).
- [ ] Tests live under **`test/`**; **`test/fixture/`** if needed.
- [ ] **`active_skill_workspace`** path under **`test/<name>/`** documented if set.

**Ask:** “What must stay green? Best fixture?”

---

## 6. Operator contract — “built the skill”

- [ ] **`SKILL.md`** + frontmatter.
- [ ] **`skill-config.json`** paths match disk.
- [ ] **`python scripts/build.py`** exits **0**.
- [ ] **Python compile check** on **`operator.compileall_paths`** passes (Operator uses Python’s **`compileall`** under the hood).
- [ ] **Scanner** scripts exit **0** (if any).

**Ask:** “Operator green?”

**Final:**

- [ ] **Attest** structurally built — **or** list gaps below.

---

## Gaps / follow-ups (free text)

Use for **resume notes** (date, last § completed, blockers):

```text


```

---

## How to use this file

1. **Ensure** **`docs/skill-plan.md`** has an **## Authoring checklist** section (scaffold injects from **`abd-skill-builder`** **`content/parts/library/authoring-checklist.md`**) before deep work.
2. Check **`- [x]`** only when done; **first unchecked** = resume point.
3. Pull updates from **`abd-skill-builder`** canonical copy when standards change.


---

### `skill-repo-standards.md`

# Skill repository standards (index + extras)

**Process approach (IDE, `process.md`, code vs AI phases, `generate_prompt`):** [`process-approach.md`](process-approach.md) — **start here** for how skills are **used** in Cursor / similar: **`AGENTS.md`** auto-loaded, **`@…/process.md`** for phase map, **code phases** vs **AI-chat phases**, **dynamic vs static** prompt generation.

**Full normative §3 (all subsections):** [`skill-standards-section-3.md`](skill-standards-section-3.md) — directory and content conventions (**§3.1**), rule naming (**§3.2**), assembly (**§3.3**), reference notes (**§3.4**): stages/phases/steps, process tables, optional domain+story-map pattern, `AGENTS.md` / `content/built/`.

**Rules + scanners + build pipeline (base framework):** [`rules-and-automated-checks.md`](rules-and-automated-checks.md) — **default** wiring: **`rules/scanners.json`** bindings, **`operator.build_pipeline`** for **`build.py`**, **`operator.scanners`** for Operator; **do not** hang scanners off individual **process** phases.

**Builder vs Operator (summary):** [`builder-vs-operator.md`](builder-vs-operator.md) — **scaffold / generation** path vs **`operator.run_operator()`** validation today.

**Authoring checklist (human + AI):** [`authoring-checklist.md`](authoring-checklist.md) — normative body merged into **AGENTS.md**; in each skill, work the **## Authoring checklist** section inside **`docs/skill-plan.md`** (scaffold injects this file there). **`- [ ]` / `- [x]`** so work can **resume after interruption** (first unchecked box = continue here). Covers scaffold verification, rules/scanners, **library**, **`delivery.mode`**, **`test/`**, operator.

**Migrating an existing skill:** [`../phases/plan-migrate.md`](../phases/plan-migrate.md) (**1b**) — inventory → compare to standards → **delta report** → **user chooses which gap IDs to fix**; then [`../phases/migrate.md`](../phases/migrate.md) (**2b**) — **execute** moves and patches for those IDs only (no silent full rewrites).

**Example delta (this repo):** [`../../docs/standards-delta.md`](../../docs/standards-delta.md) — `abd-skill-builder` inventory vs §3 (delivery, `content/built/`, docs, tests/fixture notes).

---

## Quick layout reminder (before reading the full §3)

| Area | Convention |
|------|------------|
| **Entry** | `SKILL.md` at skill root (frontmatter: `name`, `description`). |
| **Operator config** | `skill-config.json` — `operator.compileall_paths`, `operator.build_script`, **`operator.build_pipeline`** (post-merge steps for **`build.py`**), **`operator.scanners`** (Operator; align paths with rule-bound scanners). See **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**. |
| **Agent delivery** | `skill-config.json` — `delivery.mode`: **`static_built`** (pre-generate per-operation slices into **`content/built/`**) or **`runtime_injection`** (resolve the **same** sources at run time). **Only** that choice differs — always document **which paths** feed each operation, **merge order**, and **equivalence** to static output, in a **lookup** place (skill **`README.md`**, **`build.py`** manifest, or emitted manifest) so the team can switch modes later. **`AGENTS.md`** in **both** modes. See **`abd-skill-builder`** [`delivery-modes.md`](delivery-modes.md) (canonical: **`content/parts/library/delivery-modes.md`**). |
| **Authoring prose (normative for writers)** | [`documentation-standards.md`](documentation-standards.md) — voice, where content belongs, process tables; complements **`docs/` vs `content/parts/`** rule. |
| **Workspace routing** | **[workspace-and-config](../phases/workspace-and-config.md#skill-path-skill-workspace-and-configuration)** — **`skill_path`**, **`skill_workspace`**, **`conf/abd-config.json`** keys (**Workspace and config**). |
| **Build intent** | `conf/build-strategy.json` — strategize loads this **whole JSON**; **`skill_purpose`** must be non-empty for **`strategy_complete`** (minimum to finish strategize). Other keys are **siblings** that enrich **`strategy`** / **`builder_manifest`** — they are **not** part of the **`skill_purpose`** text. See **`agentic-skill-builder/README.md`** (Strategizer). |
| **Normative content** | `content/parts/` — process table rows are **phases**; **steps** inside phase files. Phase markdown files use **descriptive slugs** (`terms-mechanisms.md`, …) — **not** `phase-NN-…` or phase numbers in **H1** titles; pipeline order is **only** in `process.md` (# column) + `build.py` merge list (see **`skill-standards-section-3.md`**). **Column definitions** and required **workspace** row: **`process-table-standards.md`**. |
| **docs/ (non-runtime only)** | **`docs/`** is for material **not** consumed as merged/injected skill payload at operation time: **user manuals**, **migration/planning notes**, **architecture**, **`docs/skill-plan.md`** (plan + **Authoring checklist** section), **standards deltas**. In **abd-skill-builder**, **`docs/`** is only **`standards-delta.md`** — delivery merge order lives in **`README.md`**. **Do not** put markdown (or other assets) in **`docs/`** that **`build.py` merges**, **injects**, or **ships** as the runnable instruction body for phases/operations — that belongs under **`content/parts/`** (including **`library/`**, **`phases/`**, **`process.md`**, **`rules/`** as applicable). |
| **Library** | `content/parts/library/` — **cross-cutting meaning** reused across more than one phase: definitions, tables, glossaries, named concepts, artifact shapes. **Not** phase procedures, **not** step-by-step runbooks, **not** CLI blocks for a single phase, **not** pipeline order (that is **`process.md`** + **`phases/`**). The library **is** the home for that shared meaning; do not maintain a parallel “cross-cutting” layer elsewhere. **`docs/`** may hold a **short index** pointing into **`library/`**; **bodies** live in **`library/`**; merge order lives in **`build.py`**. See **`documentation-standards.md`** → *Library vs phase documents*. |
| **Phases** | `content/parts/phases/<slug>.md` — **person-to-process** instructions for **one** process-table row: I/O, **steps**, scripts, done criteria. **Link** to **`library/`** for deep definitions; avoid duplicating large normative blocks that belong in **`library/`** because multiple phases need them. |
| **Rules** | `rules/*.md` or `content/parts/rules/*.md`; optional `rules/scanners.json`. |
| **Scripts** | `scripts/build.py` (**required** — merge/injection driver; scaffold template is minimal; extend with explicit phase order + per-operation bundles as in **`abd-maps-models-specs`** when needed), scanners, optional `_config.py`. See **`authoring-checklist.md`** → *Base scaffold*. |
| **Tests & fixtures** | **`test/`** — all automated tests for the skill (pytest, smoke scripts, etc.) that exercise **`scripts/`**; optional **`test/fixture/<scenario>/`** for frozen inputs/snapshots; optional **`test/<workspace>/`** dirs when **`conf/abd-config.json`** uses **`active_skill_workspace`** (path relative to skill root). Example: **`abd-maps-models-specs/test/`** — workspace **`test/sample-workspace`**, optional fixture **`test/fixture/<scenario>/`**. **`abd-skill-builder`** itself **does include** **`test/`** (see **`test/README.md`** + **`test/fixture/toy-polite-dialogue/`**) even though **pytest `test_*.py` files** are still optional follow-ups — do not read “pytest wiring pending” as “no **`test/`** folder.” **Operator today** only runs a **Python compile check** on **`operator.compileall_paths`** (usually **`["scripts"]`**; implemented with **`compileall`**) — it does **not** install or run **pytest**. If automated tests are **in scope**, add the **wiring** below. |
| **Agent bundle (always)** | `AGENTS.md` — assembled agent bundle (skill-wide “how it works”); typically generated by `build.py`; **not** gated on `delivery.mode`. |
| **Built slices (operation-time, static mode)** | `content/built/` — pre-merged process + library + rules per skill layout when `delivery.mode` is **`static_built`**. |
| **Documentation focus (this skill only)** | Process plans, **rules**, and **docs** describe **what this skill does** — in positive, runnable terms for **this** package. **Do not** use them as a running commentary on how this skill **differs** from another skill, or why it **doesn’t** do something “because another skill does.” That is **local context in time**, not part of the durable skill. **Dependencies** (other skills, tools, repos, contracts) are **explicit** — names, links, versions — in a **Dependencies** section, `README`, or build-strategy notes. That is **not** the same as narrating deltas to sibling work. |

**Minimal valid skill:** `SKILL.md` + `scripts/build.py` + `skill-config.json` with operator block — see **`test/fixture/toy-polite-dialogue/`** in this skill (**`abd-skill-builder`**).

---

## When automated tests are asked for (pytest wiring)

If the skill should run **pytest** (or similar) under **`test/`**, do **not** assume it is already installed or wired into **`operator`** — add it explicitly:

| Step | What to do |
|------|------------|
| **Dependency** | Add **`pytest`** (and dev-only plugins if needed) to a **`requirements-dev.txt`**, **`pyproject.toml`** `[project.optional-dependencies] dev`, or the skill’s documented venv install step — **commit** the file so others can `pip install -r …`. |
| **Layout** | Tests live under **`test/`** (e.g. **`test/test_*.py`** or **`test/<suite>/`**); shared fixtures in **`test/fixture/`** or **`conftest.py`** as usual for pytest. |
| **Run command** | Document in skill **`README.md`** or **`test/README.md`**: e.g. `python -m pytest test/` from skill root (with venv activated). |
| **CI (optional)** | Add a workflow or monorepo job that installs dev deps and runs the same command. |
| **Operator** | **`operator.run_operator()`** does **not** run pytest by default. To gate releases on tests, extend **CI** or a **wrapper script**; only add **`test`** to **`compileall_paths`** if you intentionally want bytecode checks on test modules (unusual). |

---

## Operator checklist (machine-runnable)

1. `SKILL.md` present.
2. `skill-config.json` parses; `operator` block consistent with files on disk.
3. Python files on declared paths pass a **compile check** (Operator uses **`compileall`**).
4. `python scripts/build.py` exits 0.
5. Each listed **scanner** in **`operator.scanners`** exits **0** (and any step in **`operator.build_pipeline`** that **`build.py`** runs also exits **0** when you rely on **`build.py`** as the full local gate).
6. **`rule_scanner_bindings`** (in **`rules/scanners.json`** when used): each **`rule_file`** and **`scanner`** path exists.

---

## What greenfield scaffold should emit

**`scripts/scaffold_skill.py`** (and equivalent generators) should produce a **complete, runnable skeleton**: file tree, `skill-config.json`, phase markdown stubs, `rules/` / `conf/` as needed, runnable **`build.py`**, optional scanner stubs — **without** baking in customer-specific “gold” domain solutions (those belong in the target workspace, not the template).

This **`abd-skill-builder`** skill ships **templates + `scaffold_skill.py`** as the supported way to create that tree. **`operator.run_operator()`** then validates what is on disk; it does not scaffold new skills by itself.


---

### `skill-standards-section-3.md`

# §3 Skill package layout and content standards

**What this is:** Normative rules for how a **skill repository** is shaped — where **runtime** content lives (`content/parts/`, `rules/`, `build.py`), how **stages / phases / steps** relate, how **process tables** and **Refs** work, optional patterns (e.g. domain + story map), **rule file naming**, and **static vs dynamic** assembly of instructions. **How skills are used in the IDE** (AGENTS.md, `process.md`, code vs AI-chat phases, `generate_prompt`) is defined in [`process-approach.md`](process-approach.md) — read that first.

**How to use it:** Implement **§3.1–§3.4** when authoring or reviewing a skill. Tools and humans use the same rules; nothing here depends on any external “origin” document.

**Scope boundary — skills stay simple:** A **skill package** should express a **linear** pipeline: **stage → phase → (steps inside phase docs)**. The **process table** rows are **phases**, not steps. Keep skills deliberately sequential.

## 3.1 Directory and content conventions

**Hierarchy in the repo:** **Stages** group **phases**. Each **phase** has normative markdown (one file or section per phase, per skill); **steps** live **inside** that phase’s markdown — they are **not** separate rows in the master process table. See **Stages, phases, and steps** below.


| Area                            | Convention                                                                                                        | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Normative content**           | Under /`content/parts/`                                                                                           | Plans, operations, domain narrative — **not** dumped only in chat.                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `**docs/` (non-runtime)**       | /`docs/` at skill root                                                                                            | **User manuals**, **migration/planning notes**, **architecture**, **authoring checklists**, and **narrative** descriptions of delivery. **Do not** put markdown here that `build.py` **merges**, **injects**, or **ships** as the runnable phase/operation body — that belongs under `**content/parts/`** (including `**library/`**, `**phases/`**, `**process.md**`, `**rules/**`).                                                                                                                                   |
| **Phase markdown (source)**     | e.g. /`content/parts/phases/<descriptive-slug>.md`, or one doc per phase with step sections — paths vary by skill | **One row in the process table = one phase.** **Steps** (numbered sub-procedures, “Step 1…”, checklists) are written **inside** this markdown as **normative content of the phase**, not as their own table rows. **Do not** encode execution order in filenames or H1 titles (`phase-02-foo.md`, `# Phase 2 — …`): order belongs in `**process.md`** (the `#` column) and in `**scripts/build.py`**’s explicit file list. Use **stable descriptive** kebab-case slugs so renumbering the plan does not force renames. |
| **Built phase markdown**        | `content/parts/phases/built/<descriptive-slug>.md` and/or `content/built/…` per skill layout | **Generated** from source phase bodies + rules via `scripts/build.py`. **Authors do not hand-edit `built/`.** These files are **materialized instruction blobs** for **static** AI-chat phases and for **`static_built`** delivery — consumed by **`generate_prompt`** (or pasted into chat), **not** by “agents browsing the repo” as the primary UX. IDEs load **`AGENTS.md`**; see [`process-approach.md`](process-approach.md). Folder layout (`phases/built` vs `content/built`) is per skill; document it in **`README.md`**.                                                                                                                                                                                                            |
| **Atomic rules**                | `content/parts/rules/*.md` (or top-level `rules/` in simpler skills)                                              | One concern per file where possible; **names** should encode **phase** and/or **domain concept** + rule name (see §3.2). **Which phase inlines which rule** is declared in **`skill-config.json`** (`phase_rules`, `every_phase_rules`), not scattered in per-rule frontmatter lists.                                                                                                                                                                                                                                                                                                                                                                                               |
| **Roles**                       | `roles/*-role.md`                                                                                                 | One file per **user/agent role** the skill assumes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Process**                     | `content/parts/process.md` or staged process docs                                                                 | **Summary table: each row is a phase** (linked by **Ref** to phase markdown). Stages group those rows. **Steps** appear only **inside** the linked phase files.                                                                                                                                                                                                                                                                                                                                                        |
| **Library markdown**            | `content/parts/library/*.md` (or `parts/library/`)                                                                | **Cross-phase structure and meaning**: definitions, glossaries, artifact shapes, naming, invariants. **Not** phase-local procedures, pipeline ordering, or CLI runbooks—those live in **`process.md`** / **`phases/`** (see **Library vs phase documents** below).                                                                                                                                                                                                                                                     |
| **Repo-facing built artifacts** | `AGENTS.md`, `SKILL.md`, sometimes `README.md`                                                                    | Frequently produced by `scripts/build.py` (merge order per skill). **`AGENTS.md`** is what **IDEs and assistants typically load automatically** for the skill repo.                                                                                                                                                                                                                                                                                                                                                                |
| **Config**                      | `skill-config.json`                                                                                               | Name, version, **`phase_files`**, **`PHASE_LIBRARY_SLICES`**, **`phase_rules`** / **`every_phase_rules`** (ordered rule **stems** inlined per phase bundle — see [`process-approach.md`](process-approach.md)), **`phase_bundle`**, **`operator.compileall_paths`**, **`operator.build_script`**, **`operator.build_pipeline`** (post-merge steps for **`build.py`**), **`operator.scanners`** (Operator gate; align with rule-bound scanners) — skill-specific knobs. See **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** (base framework).                                                                                                                                                                                                                                               |
| **Scripts**                     | `scripts/`                                                                                                        | Operational entry points; may share `_config.py` patterns.                                                                                                                                                                                                                                                                                                                                                                                                                                                             |


### Stages, phases, and steps (how they relate)

**Order is always:** **Stage → Phase → Step** (coarse → mid → finest) — but **only the first two appear as rows** in the master process table. **Steps** are **inside** the phase markdown.


| Term      | Typical meaning                                                                                                                                                                                                                                                                                                                      | Example                                                                                  |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **Stage** | **Coarse pipeline slice** — groups many **phases**; may span days or sessions. Often a heading or section in `process.md` or a staged doc.                                                                                                                                                                                           | **Stage 1 — Extract Context**; **Stage 2 — Map and Model**; **Stage 3 — Specification**. |
| **Phase** | **One row** in the process summary table — the unit of “what we do next” with a **driver**: **human** or **AI actor**. The **Ref** column links to **phase** markdown. Phases answer “are we allowed to proceed?” and **contain** the detailed steps as normative body copy.                                                         | “Corpus audit — Phase N”; **Initiator / Actor** column = human vs AI.                    |
| **Step**  | **Sub-structure inside the phase’s markdown** — numbered instructions, checklists, “Step 1 / Step 2”, optional **suffix letters** (`5a`, `7a`) for companion script runs **within the same phase**. **Not** a row in the process table. Machine state (if any) may still reference `workflow_step` as a **sub-id** inside the phase. | Inside `modules-epics-scaffold-breadth.md`: “1. … 2. … 3a. rebuild index …”              |


**AI-driven phases — how the operation is delivered:** See **[`process-approach.md`](process-approach.md)**. In short: **code-driven** phases = run scripts as documented in the phase file; **AI-chat** phases = produce the instruction block via **`generate_prompt`**-style tooling in **dynamic** (assemble sections) or **static** (use pre-built phase markdown under `phases/built/` or equivalent). The **chat** follows that text; **`built/`** is not “the agent’s filesystem API.”

**Ordering (linear, inside the skill):** Stages order **major outcomes**. **Phases** run in **process table order** (each row = one phase). **Steps** follow the order **written inside** each phase document. **Parallel batches, fan-out, or merge** are **not** modeled as extra table rows; if needed, handle that **outside** the skill package (host app, orchestration, or scripts). **Phases** may **block** a later stage until accepted (e.g. “the indexer phase says rebuild chunks — do not start Stage 2 until accepted”).

**“Process” one-liner:** `content/parts/process.md` (or `parts/process.md`) often opens with a **single pipeline string** (e.g. Context → Foundational spine → …). That line is the **navigation spine**; the **table lists phases** (by stage); **authoritative step detail** lives inside each **Ref**’d phase file.

### Process tables, hyperlinks, and naming in the Ref column

**How the table is built**

- **Rows are phases**, not steps. Columns typically include: `#`, **Phase** (title — sometimes labeled “Step” in legacy tables; **semantically it is the phase**), **Initiator / Actor** (Human→Code, AI, Code), **Script** (if any), **What it does**, **Coverage**, **Ref**, **Inputs**, **Outputs**.
- **Ref** is the **hyperlink hub**: each row points to the **normative markdown for that phase**. **Steps** (numbered sub-procedures) live **inside** that file — not in separate table rows. Python entry points stay in **Script**, not **Ref**.
- **Two-tier phase files:**
  - **Source:** phase markdown authors edit (e.g. `content/parts/phases/<name>.md`, or `parts/steps/<name>.md` when the filename is the **phase** slug — naming varies by skill).
  - **Built:** `content/parts/phases/built/<name>.md` or `content/built/<name>.md` — **rules baked in** from `parts/rules/*.md` via `scripts/build.py`. **Steps remain inside** the built document. Used for **static** prompt generation and **`static_built`** slices — not hand-edited. See [`process-approach.md`](process-approach.md).
- **Cross-links inside the table:** The **Ref** column uses relative markdown links to the **phase** doc, e.g. `[context](parts/context.md)`, `[modules-epics-scaffold-breadth (built)](content/parts/steps/built/modules-epics-scaffold-breadth.md)` (paths vary by skill; **from the skill root** per `AGENTS.md`).

**Naming conventions visible in the table**

- **Phase titles** in the table read like **milestones or operations** (“Parse, curate, chunk, index”, “Integrate and Harmonize”) — stable labels for **phase** / workflow fields. **Finer labels** for **steps inside the phase file** may appear in JSON as `workflow_step` or similar.
- **Phase file names and H1 headings** must **not** duplicate pipeline indices (`phase-00-`, `Phase 3 —` in the title). Those numbers **change** when the plan evolves; **brittle** names churn git history and links. The **Ref** column and `build.py` define order; phase files stay **semantically** named (`story-map.md`, `canonical-context.md`).
- **Letter suffixes** (`5a`, `7a`) describe **sub-steps inside a phase** (e.g. companion script after a numbered step) — **inside the phase markdown**, not extra table rows.

### Concepts and cross-cutting artifacts (generic — all skills)

**This section is the generic rule.** A **skill** packages **concepts** (ideas, definitions, invariants, roles) and **artifacts** (outputs, schemas, manifests) that the workflow references across **multiple stages or phases**. Anything that would be **repeated** if pasted into every phase file should instead live in **its own file** (usually markdown under `content/parts/`, sometimes JSON alongside) so there is a **single source of truth**.


| Guideline           | Meaning                                                                                                                                                                                                         |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **When to extract** | If a concept or artifact **spans** more than one phase (or stage), give it a **dedicated** doc (or structured file) and **link** from phase bodies — do not duplicate long definitions in each phase.           |
| **Naming**          | Conventional filenames (`glossary.md`, `concepts.md`, `artifacts.md`, `roles/`*, etc.) vary by skill; **discover** and **validate** presence from templates and this skill’s `build.py`, not one global layout. |
| **Not every skill** | A minimal skill might only have `SKILL.md`, `content/parts/process.md`, and phase files — **no** separate “domain” or “story map” layer. That is valid.                                                         |


### Library vs phase documents (authoring split)

**`library/`** answers **what** (stable meaning for ideas and artifacts that **more than one** phase touches). **`phases/<slug>.md`** answers **how for this step** (operator procedure: inputs, outputs, ordered steps, **commands**, done checks).

| In **`library/`** | In **`phases/`** (not a second copy of the whole library) |
| --- | --- |
| Definitions, tables, schemas, vocabulary used across phases | Purpose of **this** phase, **steps**, checklists, **script/CLI** lines |
| Single source of truth for a construct that spans the pipeline | **Links** into the right **`library/`** shard for depth |
| Optional injection slices (`abd:begin` / `abd:end`) | **No** long normative essays that other phases would repeat verbatim |

**Do not** put **numbered phase procedures**, **order-of-operations** for the skill, or **phase-to-phase sequencing narrative** in **`library/`**—that belongs in **`process.md`** and the relevant **`phases/`** files. **Do not** park **large** reusable specs only inside one phase file if another phase needs the same text—extract to **`library/`** and link.

Normative detail for writers: [`documentation-standards.md`](documentation-standards.md) and [`../../rules/content-placement.md`](../../rules/content-placement.md).

### Optional pattern — domain narrative + interaction tree (maps-models–class skills only)

Some skills (notably **abd-maps-models-specs** and similar) **choose** to separate **two parallel artifacts** that must stay in sync. **Do not** treat this table as the default for **all** skills — only for skills that explicitly adopt this shape.


| Piece                            | Role                                                                                                                                                                                                    | Typical location (example skill)                                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Domain narrative**             | **State and structure** — modules, **domain concepts** (CRC-style: owns, properties, operations, `extends`, invariants), evidence hooks. Answers **what things are** and **what owns which rules**.     | e.g. `parts/domain.md` + evolving `map-model-spec.json` (`modules_and_epics`, `concepts[]`, chunk citations). |
| **Story map / interaction tree** | **Behavior** — epics, sub-epics, stories, scenarios; **Trigger / Response**; **Pre-Condition**; **Given/When/Then** where required. Answers **who does what** and how behavior references domain state. | e.g. `parts/story-map.md` + nested JSON under epics (`stories`, `sub_epics`, etc.).                           |


**When this pattern applies**

- **Same vocabulary:** Domain concept names (`concepts[].name`) and story references can be held to **one namespace** — scanners may enforce **exact string match** where the skill defines that rule.
- **Evidence ladder / paired edits:** Concepts may carry `evidence_stage`; **domain** vs **journey** edits are **paired** in skills that implement both files.
- Skills **without** this split still use the **generic** rule above: cross-cutting concepts → **their own** markdown (whatever the skill calls them), not repeated per phase.

### Rules and automated checks (default wiring)

For **machine-enforceable** rules, use the **base framework** in **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**:

- Declare **rule → scanner** bindings in **`rules/scanners.json`** (`rule_scanner_bindings`).
- List **ordered post-merge steps** under **`skill-config.json` → `operator.build_pipeline`**; **`scripts/build.py`** runs them after merges (same pattern as **`abd-maps-models-specs`**).
- Keep **`operator.scanners`** consistent with those scripts for **`operator.run_operator()`** / CI.

**Process tables** should **not** enumerate every scanner as if it belonged to a single phase; document automation at the skill level and link **`rules/scanners.json`** + **`build.py`** / **`build_pipeline`**.

## 3.2 Rule file naming (heuristic standard)

Target pattern (flexible regex for validation):

```text
{phase-or-stage}__{domain-concept-or-scope}__{short-rule-name}.md
```

Examples mirror **story synchronizer / maps-models** style: scanners and rules tied to **phase** and **concept** (e.g. `chunks_must_be_referenced`, `concept-layering-scaffold`). **Propose** names from the **phase** + concept + verb (and step text inside the phase doc if needed), then **check uniqueness** under `parts/rules/`.

## 3.3 Assembly model (static vs dynamic)

**Two different “static vs dynamic” pairs** — do not conflate:

1. **`build.py` assembly** (repo artifacts): Each skill ships `scripts/build.py`. It merges **process + library + phases (+ rules)** into **`AGENTS.md`** and optional **`content/built/`**. Flags like `--assembly static|snapshot` are **per skill** when present.

2. **AI-chat prompt generation** (`generate_prompt`): For **AI-driven** phases only — **dynamic** = assemble instruction string from sections; **static** = emit text from **pre-built** phase file under `phases/built/` (or documented path). See [`process-approach.md`](process-approach.md).

**Per skill:** `build.py` is the **authoritative** merge driver for **this** repo; scaffolding **emit or check** trees — they do **not** replace `build.py`.

**Flag on `build.py`:** The skill’s `build.py` may expose **CLI flags** for snapshot vs interactive merge; exact names are per skill. For **prompt** modes, document **`generate_prompt`** (or equivalent) next to **`build.py`** in **`README`** / **`AGENTS.md`**.


| Mode (merge / delivery) | Mechanism                                                                               | When                                                               |
| ----------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Static (merge)**      | `build.py` merges **built-phase** fragments into `AGENTS.md` / `SKILL.md` (and related) | Release, reproducible snapshot; CI; “what ships”.                  |
| **Dynamic (merge)**     | Runtime concatenation by **phase** / **operation** from `skill-config.json` + manifest  | Interactive sessions, partial rebuild, IDE-driven iteration. |


A **host** (CI, IDE, or orchestrator) may emit an **internal** manifest (JSON or YAML) for a **given generation run**, listing which fragments form which artifact for both modes; the skill’s `build.py` **may read** that manifest (or embedded config) when implementing **static** merges and documents how **dynamic** mode resolves fragments at runtime. That manifest is **optional** and **not** a standard every skill must carry — only **documented** `build.py` behavior is.

## 3.4 Reference skills (illustrative)

Other skills in the monorepo **illustrate** patterns (long `AGENTS.md`, phased pipelines, rules + scanners). They are **examples**, not extra requirements. **Operator** checks and layout rules are grounded in **abd-skill-builder** library files and each skill’s **`skill-config.json`** — not in a separate “corpus” file unless your team adds one.


---

### `builder-vs-operator.md`

# Builder vs Operator (today)

**Generation / scaffold (“builder” in the loose sense):** Anything that **emits** a new skill tree — typically **`abd-skill-builder`’s `scripts/scaffold_skill.py`** plus templates — producing `SKILL.md`, `skill-config.json`, phase markdown, `rules/` stubs, `scripts/build.py`, optional scanners. Output should match **§3** layout and avoid embedding customer “gold” solutions in the template.

**Operator (structural gate):** **`agentic-skill-builder`** **`operator.run_operator()`** — validates `skill-config.json`, runs a **Python compile check** on the paths in **`operator.compileall_paths`** (the implementation uses Python’s **`compileall`** module), runs **`operator.build_script`** (typically `python scripts/build.py`), then runs **scanner scripts** listed under **`operator.scanners`**. A normative skill also declares **`operator.build_pipeline`**: the **ordered post-merge steps** that **`build.py`** runs after writing **`AGENTS.md`** / built slices (rule-bound scanners, emitters, manifest, lint—**per skill**). **Rule → scanner** bindings live in **`rules/scanners.json`**; see **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** (base framework for all skills). Operator does **not** create greenfield skills; that is **`scaffold_skill.py`** and authoring.

**This skill’s role:** Ship **standards** under **`content/parts/library/`**, **process + phases**, **`scaffold_skill.py`**, and **templates** so authors get a compliant tree first, then Operator keeps it green.


---

### `rules-and-automated-checks.md`

# Rules and automated checks (base framework for every skill)

**Status:** **Normative default** for Open Agent Skills in this repo. When a skill defines **governance rules** (`rules/*.md`) and wants **machine enforcement**, wire checks this way—not as one-off phase script call-outs.

## What owns what

| Layer | Owns |
| --- | --- |
| **`rules/<stem>.md`** | The **human-readable rule**: scope, must/should, examples, done criteria. |
| **`rules/scanners.json`** | **Which script enforces which rule** — `rule_scanner_bindings[]` maps `rule_id` + `rule_file` → `scanner` path (relative to skill root). Optional top-level **`scanners`** lists scanner scripts for tooling that expects a flat array. |
| **`skill-config.json` → `operator.build_pipeline`** | **Ordered post-merge steps** that **`scripts/build.py`** runs after it writes **`AGENTS.md`** / **`content/built/`** (or your skill’s equivalent). Entries are typically **`scripts/...py`** paths: rule-bound scanners, emitters, manifest generators, rule-example linters, etc. **Empty or omitted** means “merge only” (skills with no automated checks yet). |
| **`skill-config.json` → `operator.scanners`** | **Operator / CI gate** — paths **`agentic-skill-builder`** **`operator.run_operator()`** runs **after** **`operator.build_script`**. **Keep these paths aligned** with the scanner steps you care about (usually the same modules listed in **`build_pipeline`** and/or **`rules/scanners.json`**), so “green build” and “green operator” mean the same checks. |

## What you do not do

- **Do not** treat **scanners** as **phase-owned scripts** in **`process.md`** process tables. Phase rows are for **human/AI procedure** and **merge / emit** entry points (e.g. `python scripts/build.py`), not for listing every validator. If readers need detail, add a short **“Rules and automated checks”** subsection in **`process.md`** that points here and to **`rules/scanners.json`**.
- **Do not** bind scanners only in prose. If a rule is machine-checked, add a **`rule_scanner_bindings`** row and a **`build_pipeline`** step (and **`operator.scanners`** / Operator docs as required by your host).

## Execution flow (mental model)

1. Author edits **`content/parts/`**, **`rules/`**, **`skill-config.json`**.
2. **`python scripts/build.py`** merges instruction bundles, then runs **`operator.build_pipeline`** in order (if present).
3. **Operator** (or CI) runs compile check → **`build.py`** again → **`operator.scanners`** (when configured).

**Reference implementation:** **`abd-maps-models-specs`** — `rules/scanners.json`, **`operator.build_pipeline`** in **`skill-config.json`**, and **`scripts/build.py`** driving the pipeline after merge.

## Scaffolded skills

Greenfield trees from **`scaffold_skill.py`** should ship **`rules/scanners.json`** (even if bindings start empty) and a **`skill-config.json`** fragment that includes **`operator.build_pipeline`** alongside **`operator.scanners`**, so authors extend **one** pattern instead of inventing ad hoc wrappers.

See also: **[`skill-standards-section-3.md`](skill-standards-section-3.md)** (§3.1 config row), **[`builder-vs-operator.md`](builder-vs-operator.md)**, **`rules/README.md`** at the skill root.


---

## Rules

*No rules for this phase. List rule stems (filename without `.md`) under `skill-config.json` → `phase_rules` for this phase slug, and optionally `every_phase_rules` for rules that apply to every phase. See `parts/library/process-approach.md` § Phase bundle — rules.*


---

## Phase: plan-migrate

## Principles

**AI quality — normative rules, scanners, and review.** This shard is injected under **`## Principles`** in phase bundles; the heading above is added by the assembler.

**Scope:** In **abd-skill-builder**, this file is injected as **`## Principles`** and is the **first** section in each AI-chat phase bundle (`python scripts/generate.py --phase <slug>` and `content/parts/phases/built/<slug>.md`). Read it **before** Role, Phase body, Library shards, and Rules for that phase.

---

**Every rule in `rules/` is two things at once:** (1) **Normative advice** — prose the model follows while authoring **`content/parts/`**, **`rules/`**, **`skill-config.json`**, and other skill artifacts. (2) **Checkable expectations** — where this repo ships a **scanner** under **`scripts/`**, it catches common layout or config misses; where it does not, **you** still review against the rule text.

**Example (wrong):** Treating a green **`python scripts/build.py`** as enough while **`AGENTS.md`** still disagrees with **`content/parts/`** or **`phase_rules`** omits a rule you claimed to enforce.

**Example (correct):** Read the **Rules** section in this bundle, align files with **`library/`** norms, run **`python scripts/build.py`** (and **`operator.scanners`** when configured), then **re-read** outputs against each applicable rule.

---

## Layer 1 — Generate with rules

While generating or editing skill artifacts:

- Apply **`rules/*.md`** inlined into this bundle (and related **`library/`** docs).
- Prefer **DO / DON’T** and **good vs bad** fragments inside each rule — they are the contract for *shape*, not only for CI.

---

## Layer 2 — Mechanical checks (this skill)

After you have files on disk, the pipeline can run:

| Mechanism | What it does |
| --------- | ------------ |
| **`python scripts/build.py`** | Merges **process** + per-phase bundles into **`AGENTS.md`** and **`content/built/`**, then runs **`operator.build_pipeline`** (e.g. **`scripts/scanner_skill_builder_layout.py`**) when configured. |
| **`rules/scanners.json`** | Declares **rule → scanner** bindings when your skill uses them; align with **`operator.scanners`**. |

**Example (wrong):** Hand-editing **`AGENTS.md`** while **`build.py`** is supposed to own the merge.

**Example (wrong):** Adding a scanner only in prose — no **`rule_scanner_bindings`** or **`build_pipeline`** step.

**Example (correct):** Fix issues reported by scanners, re-run **build**, keep **`skill-config.json`** paths honest.

Scanners are **necessary** for what they implement; they are **not sufficient** for semantic quality (e.g. a valid tree that still mis-describes what the skill does).

---

## Layer 3 — Adversarial pass (human or AI)

With clean tool output, still ask:

- Does each **rule** that applies to this phase pass **by intent**, not only by letter?
- Would a reviewer see **drift** between **`SKILL.md`**, **`process.md`**, and **`phases/`** even when the tree validates?

Use the **Corrections format** below when fixing issues.

---

## Corrections format

When recording or fixing a problem:

| Field | Content |
| ----- | ------- |
| **Rule** | Rule id or `rules/<file>.md` name |
| **Example (wrong)** | What was done incorrectly |
| **Example (correct)** | What it should be |
| **Scanner or validator** | If applicable — see **`rules/scanners.json`** and **`operator.build_pipeline`** |
| **Likely source** | One of: prompt gap · rule not read · edge case · automation gap |

---

## Do not bypass the documented pipeline

**AI phases** mean: read inputs, reason, update the **source** files this skill owns under **`content/parts/`**, **`rules/`**, and config — not one-off scripts that rewrite merged outputs **instead** of fixing sources. Automation that ships with the skill lives under **`scripts/`** and is wired through **`skill-config.json`** (**`build.py`**, **`build_pipeline`**, **`operator.scanners`**) as documented in **`library/rules-and-automated-checks.md`**.

**Example (wrong):** Patching **`AGENTS.md`** directly to “pass” review while **`process.md`** is unchanged.

**Example (correct):** Edit **`content/parts/`** (or **`rules/`**), run **`python scripts/build.py`**, commit regenerated **`AGENTS.md`** / **`content/built/`** when using **`static_built`**.


---

## Phase

# Phase — Plan skill migration

This is **phase 1b** in [`../process.md`](../process.md) (**Stage 1 — Plan**). Use it when the skill **already exists** and you need a **written plan** before **moving** anything: inventory, **compare to standards**, **delta table**, user **selection** of what to fix. **Execution** (moves, patches) is **[`migrate.md`](migrate.md)** (**Stage 2b**) — not here.

For **greenfield** planning (new skill, no tree yet), use **[`plan-script-build.md`](plan-script-build.md)** (**1a**).

Emit this file for an AI session with:

```bash
python scripts/generate.py --phase plan-migrate
```

---

## Outcome

1. A **delta report**: what differs from the standards, **where**, and **why it matters**.
2. A **user choice**: which deltas to fix in the **migrate** phase (now, later, or **won’t fix** with rationale).

The agent (or a human) **does not** apply bulk rewrites in this phase—it **surfaces gaps** and **records** the plan.

---

## Process (human + AI)

### 1. Inventory

Walk the skill root and note:

| Area | Look at |
|------|---------|
| **Entry** | `SKILL.md` frontmatter, description |
| **Authoring checklist** | In **each skill** (or workspace): **`docs/skill-plan.md`** → **## Authoring checklist** section (norms from [`../library/authoring-checklist.md`](../library/authoring-checklist.md)); check off **`- [ ]` → `- [x]`** as you go (resume from first unchecked). **abd-skill-builder** does not keep a separate checklist under its own **`docs/`**. |
| **docs/ vs parts** | **`docs/`** — non-runtime only (manuals, plans, architecture, optional checklist copies, **`standards-delta.md`** in **abd-skill-builder** only). **Mergeable / operation-time** markdown lives under **`content/parts/`** (and **`library/`**, **`rules/`**). If **`docs/`** holds instruction bodies that should merge, **move** them into **`parts/`** and leave **`docs/`** as index or narrative only (see **`skill-repo-standards.md`**) |
| **Operator** | `skill-config.json` → `operator.*`, paths on disk |
| **Delivery** | `delivery.mode`, `AGENTS.md`, `content/built/` if `static_built` |
| **Content** | `content/parts/process.md`, phase slugs, `build.py` merge order |
| **Library** | `content/parts/library/` — cross-cutting concepts (definitions, tables, glossaries) reused across phases; merge order in `build.py`; no second home for cross-cutting material outside **`library/`** |
| **Rules / scanners** | `rules/`, `rules/scanners.json`, bindings |
| **Scripts** | `scripts/build.py`, scanners, `compileall_paths` |
| **Tests** | `test/` per **Tests & fixtures** in [`../library/skill-repo-standards.md`](../library/skill-repo-standards.md); pytest wiring if tests exist |
| **ABD / workspace** | `conf/abd-config.json`, `active_skill_workspace` |
| **Narrative / identity** | Phases, rules, `SKILL.md` describe **this skill’s** behavior — not chronic “vs other skill” or “we skip X because Y” stories (see **Documentation focus** in [`../library/skill-repo-standards.md`](../library/skill-repo-standards.md)). Dependencies listed **explicitly** where needed. |

### 2. Compare to standards

For each row in **`skill-repo-standards.md`** (quick layout table) and the **§3** tables where applicable, mark:

- **Compliant** — matches normative text.
- **Partial** — close but missing rename, doc, or wiring.
- **Gap** — missing file, wrong shape, or contradicts standards.

Use **[`skill-standards-section-3.md`](../library/skill-standards-section-3.md)** and **[`skill-repo-standards.md`](../library/skill-repo-standards.md)** as the bar.

### 3. Delta report (written artifact)

Produce a **single markdown or table** the user can keep in the skill (e.g. **`docs/standards-delta.md`**) with **one row per gap**:

| ID | Area | Current state | Expected (standard) | Severity (high/med/low) | Suggested fix |
|----|------|----------------|---------------------|-------------------------|---------------|
| D1 | … | … | … | … | … |

Optional: group by **Operator** vs **content** vs **tests** so **[`migrate.md`](migrate.md)** can batch fixes.

### 4. Ask the user what to fix (next phase)

**Prompt (use verbatim spirit):**

> Here are the gaps between this skill and the repository standards (**N** items).  
> Which **IDs** should we fix in the **migrate** phase? You can choose **all**, **none** (document deferrals only), or a **subset**. For any item you **won’t** fix, say **defer** or **won’t fix** and a one-line reason.

Record selections; **[`migrate.md`](migrate.md)** applies **only** those IDs.

---

## AI behavior

- **Be specific:** cite paths and standard sections (e.g. “§3.1 phase slugs”).
- **Don’t** treat every cosmetic difference as high severity.
- **Do** call out **operator** failures and **security**-sensitive paths (secrets, arbitrary paths) as **high**.
- If **`pytest`** was requested but missing: reference **When automated tests are asked for** in **[`../library/skill-repo-standards.md`](../library/skill-repo-standards.md)**.

---

## Related

- **[`plan-script-build.md`](plan-script-build.md)** — **1a** (plan a **new** skill).
- **[`migrate.md`](migrate.md)** — **2b** (execute moves and patches from this plan).
- **[`fill-scaffold-parts.md`](fill-scaffold-parts.md)** — **2c** (author **`library/`** and **`rules/`** after the tree is right).
- **[`../library/authoring-checklist.md`](../library/authoring-checklist.md)** — checklist norms in **`docs/skill-plan.md`**.
- **[`../library/skill-repo-standards.md`](../library/skill-repo-standards.md)** — index of conventions.


---

## Library



---

### `documentation-standards.md`

# Skill documentation standards

**Canonical:** `skills/abd-skill-builder/content/parts/library/documentation-standards.md` (merged into **`AGENTS.md`**).

Use these rules when you author or refactor **process**, **phase docs**, optional **`docs/`** reference, staged **`content/built/`** output, and **AGENTS.md** for any Open Agent Skill. They prevent tangled cross-cutting docs and unreadable process prose.

## Delivery mode (`static_built` vs `runtime_injection`)

Declare **`delivery.mode`** in **`skill-config.json`** (default **`static_built`**). That flag answers whether the agent relies on **checked-in** **`content/built/`** + **`AGENTS.md`** or on **runtime** assembly from **`rules/`**, library fragments, and phase manifests. Normative definitions, when each applies, and how the two stay in sync are in **`delivery-modes.md`**.

## Workspace configuration

Skills that **route** to a customer tree keep **`conf/abd-config.json`** at **`skill_path`** with **`active_skill_workspace`** (and optional **`known_skill_workspaces`**). The file is **part of the repo**—**edit `active_skill_workspace`** to point at the workspace root (see **[workspace-and-config — Skill path, skill workspace, and configuration](../phases/workspace-and-config.md#skill-path-skill-workspace-and-configuration)**). A host (e.g. SkillField) may override. The install folder does **not** hold the customer project—only pointers. Workspace-local parameters live under **`skill_workspace/conf/`** per skill docs. Do not leave “where we run” only in prose unless the skill documents overrides.

## Agent-facing vs reference (read this first)

**If text is merged into `AGENTS.md`, injected into prompts, or otherwise part of the agent bundle, it belongs under `content/parts/`** (e.g. `process.md`, `phases/<phase>.md`, shared fragments). It does **not** live “only in `docs/`” with the expectation that the agent will see it unless your build copies it in.

**Staged build (`content/built/`):** When a complete file is **assembled** from pieces—e.g. a **base** plus **rules** plus **operator/story roles**—write the **intermediate, fully expanded** markdown under **`content/built/`** (or `content/parts/built/` / `phases/built/` if the skill already uses that layout). Then the final step generates the **complete** artifact (`AGENTS.md`, a single phase handoff, etc.). Do not skip the staged output if you need to diff or review what rules were baked in. (Example pattern: `abd-solution-modeler` uses `phases/built/` for phase specs.)

**`docs/`:** Use for **long-form reference** that operators (or tools) open beside the skill—principles, execution order, invariants, **and** standalone construct write-ups (schemas, package layout) **when** those are **not** duplicated as the sole copy of agent instructions. Phase tables and “what you must do” for the agent still live in **`content/parts/`**; `docs/` may **link** to the same ideas or hold deeper detail. If a norm must be in the agent’s context, mirror or generate it from `content/parts/`, not only from `docs/`.

## Voice and role

Write for the **operator** in **second person** (you, your). Frame the work clearly:

- **Your role** — What you are responsible for in this stage or skill (one or two sentences).
- **What you must do** — Imperatives and phase order (use bullets for several short obligations).
- **What you produce** / **How you know you succeeded** — Outcomes and done criteria.

Prefer **you must**, **you will**, and **then you** (sequence) over passive voice (“the pipeline establishes,” “artifacts are emitted”). Say who runs a script or makes a decision.

## Where content belongs

| Kind | Put it here | Do not |
| --- | --- | --- |
| **Process spine** — stages, phase numbers, tables, links to phase files | `content/parts/process.md` (or skill’s `content/process.md`) | Paste the entire phase table again as a second narrative. |
| **Phase behavior** — steps, checklists, **script invocations**, file paths for **this phase only** | `content/parts/phases/<phase>.md` | Split one phase across three cross-cutting docs; **duplicate** long cross-phase definitions—**link** to **`library/`** instead. |
| **Library shards** — definitions, glossaries, artifact shapes, naming, invariants for ideas that **span multiple phases** | `content/parts/library/<topic>.md` | Phase-local procedures, numbered runbooks, pipeline order, or “run `python scripts/…`” blocks that belong in **`phases/`**. |
| **Baked agent instructions** — bases + rules + roles merged before `AGENTS.md` | Source fragments under `content/parts/`; **output of merge** under `content/built/` (or `phases/built/`) **before** final generation | Edit only the final `AGENTS.md` by hand when a build step should own the merge. |
| **Standalone construct reference** — one artifact contract (schema, validators, chunk layout), diagrams, deep dives | `docs/<descriptive-name>.md` | Treat `docs/` as the **only** place agent-facing norms live; duplicate the “must do” into `content/parts/` or generate into `content/built/`. |
| **Cross-cutting** — principles, execution order, invariants that apply across phases | Usually `docs/` or `content/parts/library/` (e.g. principles prose); **governance rules** that vary by phase: **`skill-config.json`** → **`phase_rules`** / **`every_phase_rules`** + `rules/*.md` (see **`process-approach.md`**). **Link** from `content/parts/` where needed | Restate every phase inside cross-cutting docs; **link** to the process table instead. |

**Reference-doc filenames:** Do **not** prefix `docs/` filenames with phase numbers (e.g. avoid `phase2_terms.md`). Use **descriptive kebab-case** slugs (`terms-mechanisms-contract.md`, `behavioral-story-map.md`). Phase order belongs in `process.md` and `content/parts/phases/`, not in filenames.

**Cross-cutting** is for rules and order that are **not** naturally owned by a single phase. If the text is really about one phase only, prefer that phase’s file in `content/parts/phases/` plus a thin pointer from `docs/` if you keep a global index there.

## Library vs phase documents (split responsibility)

Use this split in **every** skill that has both **`library/`** and **`phases/`**:

- **`library/`** = **structure and meaning** shared across phases (what a thing *is*, how it is named, what fields exist, how it relates to other ideas). Think **reference** and **single source of truth** for multi-phase concepts.
- **`phases/*.md`** = **execution** for one pipeline step (what *you* do next, in order, including **commands** and **done checks**). Think **operator procedure** for *this* phase only.

**Hard bars**

| Layer | Must include | Must not be (move or trim) |
| --- | --- | --- |
| **`library/`** | Stable definitions, tables, schemas, cross-phase vocabulary | Long “how to run this phase” sections; **step sequences**; **script/CLI** runbooks; **phase ordering** or “after phase X…” workflow story |
| **`phases/`** | Short purpose, I/O, **steps**, script lines, checklists, **links** to **`library/`** for deep defs | Entire glossaries or artifact specs duplicated from **`library/`**; normative essays that belong in **`library/`** because **other phases** need the same text |

If a paragraph would still make sense **after renumbering or reordering phases**, it probably belongs in **`library/`** or **`rules/`**, not inside a single **`phases/<slug>.md`**.

**Governance rule in this repo:** [`rules/content-placement.md`](../../rules/content-placement.md).

## Prose style

- Several **short** points → **bullets**.
- One developed idea → **sentences** in a **paragraph**.
- Avoid long **semicolon chains** pretending to be one sentence.
- Avoid narrating **migration** from an old doc or old skill (“formerly §2.6”). Describe **this** skill only.

## Process tables

Keep the **stage narrative** at **intent and outcome**. The **table** holds actors, scripts, refs, and deliverable paths.

Normative column meanings, the required **workspace** phase (**Phase 0** informally), **`Input`/`Output` rules**, and **`build.py`/`generate.py` alignment** are in **[`process-table-standards.md`](process-table-standards.md)**. Use that doc whenever you create or refactor **`process.md`** in another skill.

Optional: an extra **Summary** column per row (**two or three sentences**) is allowed if you keep the abd-skill-builder **seven-column** shape as the default—do not drop **Input** / **Output** / **Scripts** in favor of summary-only rows. For the **maps-models-specs**-style table (**`Script`**, **`Outputs`**, **`Ref`**), put **`Summary`** in the **third** column (after **`#`**, **Phase**) and **`Ref`** **last**—see **`process-table-standards.md`** § Maps / models / specs pipeline table.

## When you edit

1. Update the **smallest** place: phase file or construct doc first.
2. If you are repeating script names and outputs that are **already** in the table, **delete** the repetition and keep purpose or pointer to `phases/`.
3. Regenerate **AGENTS.md** after changing `content/` so agents see the update.


---

### `process-table-standards.md`

# Process table standards (for `process.md`)

**Use this** whenever you author or refactor **`parts/process.md`** (or **`content/parts/process.md`**) so skills stay consistent with **abd-skill-builder** and Operator expectations. Pair with **`skill-standards-section-3.md`** (stages / phases / steps) and **`documentation-standards.md`** (voice, where content lives).

---

## Workspace phase (“Phase 0”) — required for every skill

Every skill that can target a **project tree** or needs unambiguous **where am I running?** semantics must include a **workspace** phase:

| Item | Rule |
| --- | --- |
| **Phase file** | **`parts/phases/workspace-and-config.md`** (or under **`content/parts/phases/`** if your skill uses that layout). Slug: **`workspace-and-config`**. |
| **Process row** | First process-table row **after** any “standards / checklist” preamble; **#** column **`0`** (Phase 0 — workspace first in the pipeline). **Team process plate** (`process-team.md.template`) hard-codes this row; **do not** rename the **Phase** link text to **`Phase 0 — …`** inside the table cell—keep the stable slug title **Workspace and config**. |
| **Heading & name** | Phase document **H1** and links: **Workspace and config** (not **Phase 0 — …** in the phase file’s **H1**). In **`parts/process.md`**, the **section** heading **Phase 0 — Workspace and config** is OK; the **process table** still uses the stable **Phase** column title above. |
| **Config** | **`conf/abd-config.json`** at **`skill_path`** with **`active_skill_workspace`** (and optional **`known_skill_workspaces`**). Same **JSON shape** across skills; see **abd-skill-builder** reference **`conf/abd-config.json`**. |
| **Merge / generate** | **`build.py`** should list **`workspace-and-config`** **first** in the phase merge list when that file exists; **`generate.py --phase workspace-and-config`** must resolve for AI-chat steps. |
| **CLI — `active_skill_workspace`** | Every scaffolded skill includes **`scripts/set_workspace.py`** (copied from **abd-skill-builder**). **Process** row **0** **Scripts** cell must include the same wording as **abd-maps-models-specs** phase **Set workspace**: `` `python` [`scripts/set_workspace.py`](…) — no args prints current; `<path>` sets `active_skill_workspace` in `conf/abd-config.json` ([workspace-and-config](phases/workspace-and-config.md)) `` — then **`·`** and **`generate.py`** for the AI-chat phase when both apply. |

Routing details are **not** duplicated inside **Plan** or **Scaffold** phase bodies—**link** to **`workspace-and-config.md`**.

---

## Process table columns (abd-skill-builder shape)

Use this **seven-column** header (exact labels help readers and tooling):

| Column | Meaning |
| --- | --- |
| **`#`** | **Phase id** in the pipeline: **`0`** for workspace (Phase 0); **`1a` / `1b`** for plan variants; **`2a` / `2b` / `2c`** for create/fix/fill; **`3`** for operator; or your skill’s own scheme. **Order** is this column + stage sections—not filenames. |
| **Phase** | **Linked title** to **`phases/<slug>.md`**. Stable, descriptive name (not `phase-02-foo.md` in the link text). |
| **Description** | **What happens** in this phase: decisions, constraints, pointers to other phase docs for cross-cutting topics. **Not** a second copy of the whole phase file—enough to choose the right doc. |
| **Actor** | **Who runs it:** Human / AI, Code, Human / AI + Code, etc. |
| **Input** | **What you must have** to start: paths, prior artifacts, CLI flags, **not** the phase’s primary deliverable if that deliverable is produced **in** this phase (avoid listing **`docs/skill-plan.md`** as **Input** for **1a** when **1a** creates that file—use *library norms + target workspace* instead). |
| **Output** | **Concrete artifacts** when the phase is done: files, directories, exit criteria. For **scaffold (2a)**, lead with the **scaffolded skill tree** ( **`SKILL.md`**, **`skill-config.json`**, **`conf/`**, **`content/parts/`** or **`parts/`**, **`scripts/`**, **`rules/`**, **`test/`**, **`docs/skill-plan.md`** ), then **`AGENTS.md` / `content/built/`** after **`build.py`**—not only the skill-plan template. |
| **Scripts** | **Commands** with **entry script names**: `python scripts/generate.py --phase <slug>`, `python scripts/build.py`, **`scaffold_skill.py`**. **Do not** pack **rule-bound scanners** here—those are skill-wide; document them under **Rules and automated checks** (see **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**) and run them via **`build.py`** / **`operator.build_pipeline`**. One cell; use **`·`** between multiple commands. |

**Do not** use a vague **Output** that only points at a **template file** when the real outcome is a **written document** or **directory tree**—say the **path** under the skill (e.g. **`docs/skill-plan.md`**).

### Maps / models / specs pipeline table (seven columns, `Script` + `Outputs` variant)

Skills such as **abd-maps-models-specs** use the **same seven-column count** with different labels: **`#`**, **Phase**, **Summary**, **Actor**, **Script**, **Outputs**, **`Ref`**.

- **`Summary`** is the **third** column (after **`#`** and **Phase**) so wide prose sits early in the row and previews well in Markdown renderers.
- **`Ref`** is the **last** column (phase doc links stay the right-hand anchor).

Keep **exact header labels** (**`Outputs`** for concrete artifacts and paths) so tables stay consistent across stages.

---

## Stages vs tables

- **Stage** sections (**`## Stage N — …`**) carry **narrative**: purpose, what you produce, how you know you succeeded.
- **Tables** carry **rows = phases**: Ref, Actor, Input, Output, Scripts. **Steps** stay **inside** phase markdown files, not extra table rows (per §3).

---

## Language

- **Second person** for operator-facing prose in phase files (**you**, **your**); see **`documentation-standards.md`**.
- **Process one-liner** at the top of **`process.md`**: pipeline string with **linked phase names** (e.g. **Workspace and config** → **Plan** → …).
- **Routing** cells: short **“Routing: [Workspace and config](…)—not repeated here.”** instead of repeating **`conf/`** keys.

---

## `build.py` and `generate.py` alignment

When you add or rename a phase:

1. **`parts/phases/<slug>.md`** exists.
2. **`process.md`** has a row with that **Phase** link and **`#`** id.
3. **`scripts/build.py`** — **`PHASE_FILES`** (or equivalent) lists **`slug`** in merge order; **`LIBRARY_FILES`** lists library shards in order.
4. **`scripts/generate_prompt.py`** — resolves **`parts/phases/<slug>.md`** (or **`content/parts/phases/`**); **`generate.py`** stays the thin CLI that delegates to it.
5. Regenerate **`AGENTS.md`** / **`content/built/`** after edits.

---

## Reference

- **Worked example:** **`parts/process.md`** in **abd-skill-builder**.
- **Rich pipeline doc:** **`templates/process-team.md.template`** (team process plate).
- **Workspace normative body:** **`parts/phases/workspace-and-config.md`**.


---

### `delivery-modes.md`

# Agent delivery modes (static build vs runtime injection)

Skills can hand instructions to an **agent** or **executor** (including an EA / orchestrator) in two ways. **Do not mix them in one session without an explicit choice** — same requirement as §3.3 *Assembly model* in [`skill-standards-section-3.md`](skill-standards-section-3.md) (static vs dynamic).

## `AGENTS.md` — always (skill-wide orientation)

**`AGENTS.md`** is the **assembled agent bundle**: how the skill is structured, how phases/steps relate, and how to work with it in general. It should be **assembled for every skill** (typically generated by **`scripts/build.py`**), regardless of **`delivery.mode`**. It is *not* what the mode flag switches on or off.

**What `delivery.mode` actually changes** is how a **single operation** (or phase/step run) gets its **process slice**: either from **pre-generated built output** or from **runtime injection** of sources — see below.

## Flag (system-wide convention)

Declare the mode in **`skill-config.json`** so tools, CI, and humans agree:

```json
"delivery": {
  "mode": "static_built"
}
```

| `delivery.mode` | Meaning |
| --- | --- |
| **`static_built`** | **Default.** When you **run an operation**, the executor uses **process content that has already been merged into `content/built/`** (and similar per-skill layouts): each slice includes the **process part** plus its **library** and **rules** components as produced by the build. **`AGENTS.md`** is still checked in as the skill-wide bundle; **built** trees are the canonical **operation-time** artifacts. Operators run **`python scripts/build.py`** after changing sources; commits include regenerated files. |
| **`runtime_injection`** | When you **run an operation**, the executor **injects** the **process part** and, in documented order, **all** of its **library** and **rules** components from source paths — **without** requiring that slice to exist as a pre-built file under **`content/built/`**. **`AGENTS.md`** is still assembled for orientation; only the **operation-time** merge strategy differs. |

**Default for new skills:** `static_built`. Use **`runtime_injection`** when you want runtime resolution; use **`static_built`** when you want checked-in slices — **both** require the same **documented injection map** (see below).

## Injection map — document regardless of mode

**`delivery.mode` does not decide whether you document injection.** It only decides **pre-generate** (build + commit **`content/built/`**) vs **inject at run time** after each operation. In **both** cases:

1. **Which** source paths (process slice, **`library/`**, **`rules/`**, …) apply **per operation** (phase/step).
2. **In what order** they are merged / concatenated / injected.
3. **How** that matches the **static** merge (same semantics as **`build.py`**, or **deliberate differences** called out).

Keep this in a **single lookup** place — e.g. skill **`README.md`**, a manifest in **`build.py`**, or a **generated manifest** checked in next to **`built/`** — so someone can **change `delivery.mode` later** without re-deriving paths from scattered files. The only thing that changes is **when** material is materialized (build vs runtime), not **what** the skill is allowed to omit from documentation.

## Mode (a) — `static_built`

- **What is delivered:** Generated markdown under **`content/built/`** (and/or `phases/built/`, `content/parts/steps/built/` per skill layout) plus the top-level **`AGENTS.md`** when the build emits it.
- **Operation-time behavior:** Use the **built** slices (process + library + rules already merged for that slice).
- **When it applies:** CI, reviewable diffs, reproducible runs, “what the agent saw” is literally in git.
- **Operator obligation:** After editing **`content/parts/`**, **`rules/`**, or merge inputs, run **`build.py`** and commit outputs.

## Mode (b) — `runtime_injection`

- **What is delivered:** For **operations**, not a single pre-expanded tree under **`built/`**; the **executor** resolves **phase** (or step) → **files** (`rules/…`, `content/parts/library/…`, process slice, etc.) and **injects** them into context in a documented order (full **process part + library + rules** for that operation).
- **`AGENTS.md`:** Still assembled so the agent understands the skill in general; only **per-operation** content is resolved at runtime.
- **When it applies:** Interactive orchestration, rapid iteration without running the full static pipeline each time, or environments where checking in large built blobs is undesirable (still document the tradeoff).
- **Operator / implementer obligation:** Same as **static** mode for the **injection map** — resolution order, equivalence vs static merge, validation — **not** optional just because execution is dynamic. Runtime mode adds: executor must follow the **same** documented map (or list exceptions).

## Staying in sync between modes

1. **Single source of truth** for *meaning* stays in **unbuilt** inputs: **`content/parts/`**, **`rules/`**, **`docs/`** (reference), not in hand-edited **`AGENTS.md`** when a build owns the merge.
2. **`static_built`** outputs are **derivatives**: regenerating must be repeatable from the same inputs + **`scripts/build.py`** (and any merge manifest the skill defines).
3. **`runtime_injection`** must **not drift silently**: if both modes are supported, the skill should state whether runtime is a *shortcut to the same merge* (ideal) or a *lighter subset* (then list gaps).
4. **Changing sources:** Under **`static_built`**, CI or pre-commit should run **`build.py`** and fail if **`content/built/`** / **`AGENTS.md`** are stale (exact hook is repo-specific).
5. **Switching modes:** The **injection map** (paths + order + equivalence) is what lets you move from **`static_built`** to **`runtime_injection`** or back — update **`delivery.mode`** and keep the **same** map unless you intentionally change behavior.

## Relation to `build.py` flags

Per §3.3, a skill may expose **`--assembly static|dynamic`** (or equivalent) **inside** `build.py` for *how* static snapshots are produced. That is **orthogonal** to **`delivery.mode`**: `delivery.mode` answers whether the **operator/agent relies on checked-in built files** vs **runtime resolution**. A skill can use `runtime_injection` at execution time while still using `build.py --assembly static` to produce reference snapshots for tests.


---

### `process-approach.md`

# Process approach — IDE, `process.md`, code phases vs AI-chat phases

**Audience:** Authors and tooling. This is the **default mental model** for how a skill is **used** (Cursor, VS Code, Claude Desktop, similar) and how **phases** are executed.

## Who consumes what


| Artifact                                                               | Who uses it                                     | How                                                                                                                                                                                                                                                                                                                      |
| ---------------------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `**AGENTS.md`** (skill root)                                           | **IDE / assistant**                             | Loaded **automatically** by many tools as context for the repo. It orients the model: pipeline, links, where `process.md` lives. **No one “opens `built/` by hand” as the primary workflow** — the chat does not browse the tree to find instructions; **you tell it what to do** using `**process.md`** and phase docs. |
| `**content/parts/process.md**` (or `pieces/process.md` in some skills) | **Human + chat**                                | **Map of phases**: table rows are **phases**, **Ref** links to phase files. The skill should tell users to **read / `@`-reference** this file to know **how to execute** a given phase (order, actor, script). Example pattern: `@agilebydesign-skills/skills/<skill-id>/content/parts/process.md`.                      |
| **Built phase text** (`phases/built/`, `content/built/`, …)            | **Build pipeline + optional `generate_prompt`** | **Generated** outputs — **not** “what autonomous agents read first.” They exist so you can **materialize** a full instruction block for an AI phase (static mode) or **diff in git** under `static_built` delivery.                                                                                                      |


## Phase kinds (two execution styles)

### 1. Code-driven phases (human or CI runs the script)

- **You run** the Python/shell entry point **normally** (terminal, task, CI).
- **Await** exit code and artifacts the phase defines.
- The **phase markdown** (source) describes **how to invoke** the script, **arguments**, **outputs**, and **what “done” means** — not a prompt to paste unless the phase is hybrid.

### 2. AI-chat–driven phases (instructions for the model)

- The **instruction body** the chat must follow is produced by **prompt generation** — short name: **generate prompt** (implementation often `scripts/generate_prompt.py` per skill; names may vary).
- **CLI shape (contract):** support a **phase selector**, e.g. `python scripts/generate_prompt.py --phase <phase_slug>` (some teams use `phase:<name>` as a single token; equivalent intent).
- **Two modes** (both end with “text the user pastes or tool injects into chat”):


| Mode        | What it does                                                                                                                                                                                                                                                            | When to use                                                                |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Dynamic** | Builds one **string** by **collecting every section** required for that phase (source phase markdown, `library/` fragments, applicable `rules/`, manifest order in `skill-config.json` / `build.py`).                                                                   | Fast iteration; single source of truth; no checked-in blob for that phase. |
| **Static**  | Uses **pre-generated** phase text already written under the skill’s **built tree** (convention: `content/parts/phases/built/<phase_slug>.md` or `phases/built/<phase_slug>.md` — **document the path in the skill**). **Grab the whole file** as the instruction block. | Reproducible snapshots, CI, “exactly what shipped last release.”           |


In **either** mode, the **outcome** is: **the IDE chat has the right block of instructions** to follow for that phase — not “the agent navigates to `built/` like a filesystem API.”

### Default `phase_bundle` order (`skill-config.json`)

**abd-skill-builder** `Instructions` (used by `scripts/generate_prompt.py` and typical `scripts/build.py` merges) follows **`phase_bundle.order`** — an array of section tokens — unless `operation_sections` overrides the slug. **Default in this repo and scaffold template:** **`["principles", "role", "phase", "library", "rules"]`** so **`critical-quality-steps.md`** ( **`## Principles`** ) leads every AI-chat bundle. Other skills may reorder (e.g. **`principles`** last) or omit tokens; missing optional files (**`role`**, **`principles`**) are skipped.

Section tokens (each included only if listed in **`order`**):

- **`principles`** — optional: file under `content/parts/library/` (default `critical-quality-steps.md`), heading **`principles_heading`**. **Omitted** if the file is missing.
- **`role`** — optional: file under `content/parts/` (default basename `solution-analyst-role.md`). **Omitted** if the file is missing.
- **`phase`** — `content/parts/phases/<slug>.md` (or `parts/phases/`), with heading **`## Phase`** when `phase_bundle.phase_heading` is set.
- **`library`** — shards from **`PHASE_LIBRARY_SLICES`** for that slug, or all of **`library_files`** when the slice is absent; one **`## Library`** heading, then **`### \`file.md\``** per shard (with `abd:begin` / `abd:end` filtering). **Empty slice** → placeholder body under **`## Library`**.
- **`rules`** — **normative:** governance markdown inlined from **`rules/<stem>.md`** in manifest order. Stems come only from **`skill-config.json`**:
   - **`every_phase_rules`** — array of stems (no `.md`) prepended for **every** phase, **deduplicated** in order (listed once even if also under a phase).
   - **`phase_rules`** — object: keys are **phase slugs** (same strings as **`phase_files`**); values are ordered arrays of stems. Example: `"shaped-story-map": ["evidence-citations-required", "shaped-story-shape"]`.
   **No stems** for a phase → placeholder body under **`## Rules`** (points authors to this doc). Rule files may keep optional YAML frontmatter (e.g. **`rule_id:`**); **`Instructions`** strips it before inlining so bundles stay readable. **Do not** use per-rule **`phase_files:`** frontmatter as the source of truth for which phase gets which rule — that duplicates the manifest and drifts; **abd-maps-models-specs** and **abd-skill-builder** both standardize on **`phase_rules` / `every_phase_rules`**.

Configure (or copy defaults) via **`phase_bundle`** in **`skill-config.json`**: keys include **`order`**, **`role_file`**, **`principles_file`**, and optional **`role_heading`**, **`phase_heading`**, **`library_heading`**, **`rules_heading`**, **`principles_heading`**. **abd-skill-builder** ships the full default object so scaffolded skills inherit the same contract; **abd-maps-models-specs** uses **`MapsInstructions`**, which follows the same **`phase_rules` / `every_phase_rules`** contract (plus maps-only critical-quality notes).

### Library shards with phase markers (`abd:begin` / `abd:end`)

A **`library/*.md`** file may wrap fragments in **`<!-- abd:begin <phase-slug> -->`** … **`<!-- abd:end <phase-slug> -->`** (same slug on both lines). When **`Instructions.assemble_prompt(<phase-slug>)`** runs (used by **`generate_prompt.py`** and **`build.py`** for **`phases/built/<slug>.md`**), the reader sees **all lines outside** those pairs **plus** only the **pair whose slug matches** the current phase. Slugs match **`phase_files`** in **`skill-config.json`** (e.g. **`plan-script-build`**). Files **without** markers are included in full whenever **`PHASE_LIBRARY_SLICES`** lists them for that phase. Authoring template: **`templates/concepts.md.template`**.

## What `build.py` is for

- `**scripts/build.py`** merges **process + library + phases (+ rules where applicable)** into `**AGENTS.md`** and any `**content/built/**` slices per `**delivery.mode**`.
- It is the **authoritative** driver for **this** skill repo. `**generate_prompt`** is **orthogonal**: it answers “what text do I put in chat **for this AI phase**?” while `**build.py`** answers “what ships in **AGENTS.md** / static bundles?”

## Relation to §3

- **Stages / phases / steps** table semantics: `[skill-standards-section-3.md](skill-standards-section-3.md)`.
- **Rule file naming, assembly flags:** same §3 doc.
- **Delivery modes (`static_built` vs `runtime_injection`):** `[delivery-modes.md](delivery-modes.md)`.

## Team process plate (rich `process.md`)

For skills that need the same **shape** as **abd-maps-models-specs** — **outcome**, **principles**, **inputs / outputs**, **stages**, and a **wide phase table** (Description, Actor, Input, Output, Scripts) — start from the **team template**:

- **`content/parts/templates/process-team.md.template`** (in **abd-skill-builder**)
- **`content/parts/templates/README.md`** — how it relates to scaffold’s minimal **`templates/process.md.template`**

Copy the plate into **your** skill as **`content/parts/process.md`**, replace `{{skill_name}}`, add phases and **Ref** links, then run **`python scripts/build.py`**. The **abd-skill-builder** **`process.md`** demonstrates the same structure at production quality.

## Extending a new skill

1. Add `**content/parts/process.md`** with phase rows and **Ref**s (or start from **`process-team.md.template`** above).
2. For each **code phase**, document script + I/O in the phase file.
3. For each **AI-chat phase**, either wire `**generate_prompt`** (dynamic/static) or document a manual copy-paste path until scripted.
4. Run `**python scripts/build.py**` so `**AGENTS.md**` stays the IDE-facing bundle.
5. Keep `**process-approach.md**` behaviors in `**README.md**` in one paragraph so consumers know how your skill expects IDE + chat to work.


---

### `authoring-checklist.md`

# Skill authoring checklist (human + AI)

**Purpose:** Trackable **`- [ ]` / `- [x]`** tasks for building or evolving a skill. **Workspace convention:** keep this content in **`docs/skill-plan.md`** under the **## Authoring checklist** section (one document with the plan). **Scaffold** injects this file there; by hand, paste from here. If you stop mid-work, the next session continues from the **first unchecked** box in that section.

**Canonical source:** `skills/abd-skill-builder/content/parts/library/authoring-checklist.md` — merge updates from here when standards change.

| Role | What to do |
|------|------------|
| **A — Ask** | Use the **Ask:** lines under each section when you need input. |
| **B — Answer / suggest** | As **AI**, fill proposals; human confirms. |
| **C — Track** | Turn `- [ ]` into `- [x]` only when the item is **done**. |

**Normative layout/operator rules** stay in **`skill-repo-standards.md`** and **`skill-standards-section-3.md`** (under **`content/parts/library/`** in **abd-skill-builder**). **How the IDE uses the skill** (AGENTS.md, `process.md`, code vs AI-chat phases, `generate_prompt`): **`process-approach.md`**.

**Runtime vs `docs/`:** All markdown (and other content) that **pertains to how the skill is used at operation time** — merged or injected by **`build.py`**, read as phase bodies, or otherwise part of the **runnable** package — lives under **`content/parts/`** (and **`library/`**, **`rules/`**, etc. per norms). **`docs/`** is **only** for **non-runtime** material: user manuals, **skill plans** (including the checklist section), architecture, standards deltas. **Do not** stash mergeable instruction content in **`docs/`**. (**abd-skill-builder** itself only keeps **`docs/standards-delta.md`**.)

---

## Before you start (every session)

- [ ] **Working copy:** **`docs/skill-plan.md`** includes an **## Authoring checklist** section (scaffold injects this file there; by hand, paste from **`library/authoring-checklist.md`** into that section).
- [ ] **Resume:** Find the **first unchecked** `- [ ]` in the checklist section and continue from there.
- [ ] **Optional:** Note the date and “stopped at §…” in **Gaps / follow-ups** at the bottom when pausing.
- [ ] **`docs/` vs `content/parts/`:** No **runtime** markdown under **`docs/`** — phases, library bodies, and anything **`build.py`** merges/injects stay in **`parts/`**. **`docs/`** = manuals, **skill plan** (with checklist section), architecture, migration notes only.

---

## Greenfield vs existing skill

- [ ] **New skill:** Ran **`scaffold_skill.py`** (or equivalent) so the base tree exists.
- [ ] **Existing skill:** Ran **[plan-migrate.md](../phases/plan-migrate.md)** (**1b**: inventory + **standards-delta** + user chose **IDs**), then **[migrate.md](../phases/migrate.md)** (**2b**: execute moves) **before** bulk edits — **or** consciously skipped with a note in **Gaps / follow-ups**.

---

## Skill identity (what this skill does — not delta to other work)

Normative row: **Documentation focus** in **`skill-repo-standards.md`**.

- [ ] **Process, rules, and docs** describe **what this skill does** and how to run it — **this package**, on its own terms.
- [ ] They do **not** rely on “vs another skill” or “we don’t do X because Y” — that stays out of durable spec.
- [ ] **Dependencies** (other skills, repos, tools, versions) recorded explicitly (**Dependencies** / `README` / `conf/build-strategy.json`) — separate from the main narrative.

**AI should:** Strip migration chatter; put relationships in a **Dependencies** list.

**Ask:** “If this skill vanished, could someone run it from **this repo alone**?”

---

## Base scaffold: what you copy and extend

**Source:** **`skills/abd-skill-builder/scripts/scaffold_skill.py`** + **`skills/abd-skill-builder/templates/*`** — extend these files; don’t invent a parallel layout.

### Scaffold files present and reviewed (check each)

- [ ] **`SKILL.md`** — frontmatter + description make sense.
- [ ] **`skill-config.json`** — `operator.*`, `delivery.mode` match intent; if **`rules/*.md`** back AI-chat phases, **`phase_rules`** / **`every_phase_rules`** list every rule stem for the right **phase slug** (**[`process-approach.md`](process-approach.md)** — *rules* in the default **`phase_bundle`**).
- [ ] **`conf/build-strategy.json`** — `skill_purpose` and siblings filled per Strategizer.
- [ ] **`conf/abd-config.json`** — **`active_skill_workspace`** set (under **`test/`** when using a workspace); optional CLI: **`python scripts/set_workspace.py <path>`**.
- [ ] **`scripts/set_workspace.py`** — present (scaffold copies from **abd-skill-builder**).
- [ ] **`conf/README.md`** — conf usage clear.
- [ ] **`content/parts/process.md`** — pipeline table matches real phases.
- [ ] **`content/parts/phases/`** — one file per row in **`process.md`** (add/rename beyond **`author.md`** as needed).
- [ ] **`content/parts/phases/built/`** — present when you use **static** AI-chat prompts; populate via **`build.py`**; see **`process-approach.md`**.
- [ ] **`scripts/generate_prompt.py`** — present for AI-chat phases; **`--mode dynamic`** vs **`static`** documented; extend per skill.
- [ ] **`scripts/build.py`** — merge/injection driver present (see non-negotiables below).
- [ ] **`scripts/scanner_smoke.py`** — replaced or supplemented with real scanners if needed.
- [ ] **`rules/README.md`** + **`rules/scanners.json`** — wired when rules exist.
- [ ] **`test/README.md`** — explains layout; workspace path if used.
- [ ] **`content/parts/library/`** — created when cross-cutting chunks exist; wired in **`build.py`** (e.g. **`PHASE_LIBRARY`**) per §3.

### Non-negotiables

- [ ] **`scripts/build.py`** is the **merge / injection driver** (writes at least **`AGENTS.md`** from process + phases).
- [ ] **`process.md`** order matches **`phases/`** and **`build.py`** (if order ≠ lexicographic sort of filenames, **`build.py`** uses an **explicit ordered list**, not **`sorted(glob)`**).
- [ ] **Process → operation injection** documented in/near **`build.py`** + human-readable place for §4.

### Reference templates read (when extending)

- [ ] Read **`abd-skill-builder/parts/library/process-table-standards.md`** — process **`#`**, **Phase**, **Description**, **Actor**, **Input**, **Output**, **Scripts**; **workspace** phase (**Phase 0**) required.
- [ ] Opened **`abd-skill-builder/templates/child_build.py.template`** (minimal merge).
- [ ] If per-operation bundles / library injection: reviewed **`abd-maps-models-specs/scripts/build.py`** (`PHASE_FILES`, `PHASE_LIBRARY`, built phases).

### Extension work (after §§0–4 answers)

- [ ] **One** **`build.py`** — no second hidden merge pipeline.
- [ ] **`process.md`**, **`phases/*.md`**, **`build.py`** updated **together** when adding/changing a phase.
- [ ] **`content/parts/library/`** chunks added and wired in **`build.py`** where needed.
- [ ] **Injection map** in **`build.py` docstring** and/or skill **`README.md`** (aligns with §4).
- [ ] **`python scripts/build.py`** run after structural edits; **`AGENTS.md`** / **`content/built/`** committed if **`static_built`**.

**Ask:** “Which files do we **edit** vs **add**? Where is the **ordered phase list** in **`build.py`**?”

---

## 0. Build intent (`conf/build-strategy.json`)

- [ ] **`conf/build-strategy.json`** complete per **`agentic-skill-builder`** (template + Strategizer).

**Ask:** “What must this skill accomplish end-to-end? Who runs it? What is out of scope?”

---

## 1. Process & phases

- [ ] **`parts/process.md`** (or **`content/parts/process.md`**) lists the real pipeline (ordered phases) and follows **[`process-table-standards.md`](process-table-standards.md)** — column meanings, **Input**/**Output** semantics, **Scripts** cell.
- [ ] **Workspace phase (Phase 0):** **`parts/phases/workspace-and-config.md`** exists; **`conf/abd-config.json`** + **`active_skill_workspace`** documented; first process row uses **`0`** in **`#`** and the phase name **Workspace and config** (see standards doc).
- [ ] Phase files use **descriptive slugs**; order matches **`process.md`** and **`build.py`** (explicit order if not sort order).
- [ ] **`build.py`** phase list / merge keys updated when **`process.md`** changes.
- [ ] **Phase vs library:** Each **`phases/<slug>.md`** is **procedure** for that phase (steps, scripts, checklists)—**not** a dump of cross-phase definitions (**[`documentation-standards.md`](documentation-standards.md)** → *Library vs phase documents*; **[`rules/content-placement.md`](../../rules/content-placement.md)**).

**Ask:** “Phases in order?”

---

## 2. Rules (optional) & scanners

- [ ] Decided if **`rules/`** is needed.
- [ ] Listed planned **`rules/*.md`** files (one concern per file where possible).
- [ ] Decided scanner vs doc-only for each rule cluster.
- [ ] **Base framework** (when checks exist): read **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** — **`rules/scanners.json`** **`rule_scanner_bindings`** for each machine-checked rule; **`skill-config.json`** **`operator.build_pipeline`** lists ordered post-merge steps for **`build.py`**; **`operator.scanners`** lists the same scanner paths (or a superset) for **Operator** / CI.
- [ ] **`process.md`** does **not** treat scanners as phase-local “script column” noise; skill-level **Rules and automated checks** (or link to **`rules-and-automated-checks.md`**) instead.

**Ask:** “Machine-checked vs human-reviewed? What would each scanner inspect?”

---

## 3. Library — cross-cutting concepts (`content/parts/library/`)

- [ ] Cross-cutting content in **`library/<slug>.md`** (or skill-specific equivalent).
- [ ] **`build.py`** merge order matches how phases reuse library.
- [ ] Optional **index** (short links only: **`README`**, **`conf/build-strategy.json` notes**, or a **`docs/*` index** if non-runtime) — **not** a second home for bodies; full cross-cutting copy stays in **`library/`** (see **`docs/` vs parts** in **`skill-repo-standards.md`**).
- [ ] Same concept **names** across phases.
- [ ] **Library stays non-procedural:** **no** numbered “how to run a phase” sequences, **no** phase ordering story, **no** phase-specific **`python scripts/…`** runbooks—those stay in **`phases/`** and **`process.md`** (**[`rules/content-placement.md`](../../rules/content-placement.md)**).

**Ask:** “What repeats across phases → **library**?”

---

## 4. Agent delivery mode (`skill-config.json` → `delivery.mode`)

See **`abd-skill-builder`** [`delivery-modes.md`](content/parts/library/delivery-modes.md) (canonical: `skills/abd-skill-builder/content/parts/library/delivery-modes.md`).

- [ ] **`AGENTS.md`** assembled (both modes).
- [ ] **Injection / merge map** documented (paths per operation, order, equivalence to static) — **`README`**, **`build.py`**, or manifest — so mode can change later (narrative-only; sources remain under **`content/parts/`**).
- [ ] **`delivery.mode`** set: **`static_built`** or **`runtime_injection`**.
- [ ] If **`static_built`**: **`build.py`** run; **`content/built/`** (and peers) committed; traceable to map.
- [ ] If **`runtime_injection`**: runtime follows documented map (or deltas documented).

**Ask:** “Per operation: which files, which order, where is the lookup?”

---

## 5. `test/` — script tests & fixtures

- [ ] Chose: pytest **yes** or **no** (if no, skip pytest bullets; may still use **`test/`** for fixtures).
- [ ] If pytest **yes**: dev deps + **`pip install`** documented (**`requirements-dev.txt`** or **`pyproject.toml`**).
- [ ] **Run command** documented (e.g. **`python -m pytest test/`**).
- [ ] **CI** runs tests (optional).
- [ ] Tests live under **`test/`**; **`test/fixture/`** if needed.
- [ ] **`active_skill_workspace`** path under **`test/<name>/`** documented if set.

**Ask:** “What must stay green? Best fixture?”

---

## 6. Operator contract — “built the skill”

- [ ] **`SKILL.md`** + frontmatter.
- [ ] **`skill-config.json`** paths match disk.
- [ ] **`python scripts/build.py`** exits **0**.
- [ ] **Python compile check** on **`operator.compileall_paths`** passes (Operator uses Python’s **`compileall`** under the hood).
- [ ] **Scanner** scripts exit **0** (if any).

**Ask:** “Operator green?”

**Final:**

- [ ] **Attest** structurally built — **or** list gaps below.

---

## Gaps / follow-ups (free text)

Use for **resume notes** (date, last § completed, blockers):

```text


```

---

## How to use this file

1. **Ensure** **`docs/skill-plan.md`** has an **## Authoring checklist** section (scaffold injects from **`abd-skill-builder`** **`content/parts/library/authoring-checklist.md`**) before deep work.
2. Check **`- [x]`** only when done; **first unchecked** = resume point.
3. Pull updates from **`abd-skill-builder`** canonical copy when standards change.


---

### `skill-repo-standards.md`

# Skill repository standards (index + extras)

**Process approach (IDE, `process.md`, code vs AI phases, `generate_prompt`):** [`process-approach.md`](process-approach.md) — **start here** for how skills are **used** in Cursor / similar: **`AGENTS.md`** auto-loaded, **`@…/process.md`** for phase map, **code phases** vs **AI-chat phases**, **dynamic vs static** prompt generation.

**Full normative §3 (all subsections):** [`skill-standards-section-3.md`](skill-standards-section-3.md) — directory and content conventions (**§3.1**), rule naming (**§3.2**), assembly (**§3.3**), reference notes (**§3.4**): stages/phases/steps, process tables, optional domain+story-map pattern, `AGENTS.md` / `content/built/`.

**Rules + scanners + build pipeline (base framework):** [`rules-and-automated-checks.md`](rules-and-automated-checks.md) — **default** wiring: **`rules/scanners.json`** bindings, **`operator.build_pipeline`** for **`build.py`**, **`operator.scanners`** for Operator; **do not** hang scanners off individual **process** phases.

**Builder vs Operator (summary):** [`builder-vs-operator.md`](builder-vs-operator.md) — **scaffold / generation** path vs **`operator.run_operator()`** validation today.

**Authoring checklist (human + AI):** [`authoring-checklist.md`](authoring-checklist.md) — normative body merged into **AGENTS.md**; in each skill, work the **## Authoring checklist** section inside **`docs/skill-plan.md`** (scaffold injects this file there). **`- [ ]` / `- [x]`** so work can **resume after interruption** (first unchecked box = continue here). Covers scaffold verification, rules/scanners, **library**, **`delivery.mode`**, **`test/`**, operator.

**Migrating an existing skill:** [`../phases/plan-migrate.md`](../phases/plan-migrate.md) (**1b**) — inventory → compare to standards → **delta report** → **user chooses which gap IDs to fix**; then [`../phases/migrate.md`](../phases/migrate.md) (**2b**) — **execute** moves and patches for those IDs only (no silent full rewrites).

**Example delta (this repo):** [`../../docs/standards-delta.md`](../../docs/standards-delta.md) — `abd-skill-builder` inventory vs §3 (delivery, `content/built/`, docs, tests/fixture notes).

---

## Quick layout reminder (before reading the full §3)

| Area | Convention |
|------|------------|
| **Entry** | `SKILL.md` at skill root (frontmatter: `name`, `description`). |
| **Operator config** | `skill-config.json` — `operator.compileall_paths`, `operator.build_script`, **`operator.build_pipeline`** (post-merge steps for **`build.py`**), **`operator.scanners`** (Operator; align paths with rule-bound scanners). See **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**. |
| **Agent delivery** | `skill-config.json` — `delivery.mode`: **`static_built`** (pre-generate per-operation slices into **`content/built/`**) or **`runtime_injection`** (resolve the **same** sources at run time). **Only** that choice differs — always document **which paths** feed each operation, **merge order**, and **equivalence** to static output, in a **lookup** place (skill **`README.md`**, **`build.py`** manifest, or emitted manifest) so the team can switch modes later. **`AGENTS.md`** in **both** modes. See **`abd-skill-builder`** [`delivery-modes.md`](delivery-modes.md) (canonical: **`content/parts/library/delivery-modes.md`**). |
| **Authoring prose (normative for writers)** | [`documentation-standards.md`](documentation-standards.md) — voice, where content belongs, process tables; complements **`docs/` vs `content/parts/`** rule. |
| **Workspace routing** | **[workspace-and-config](../phases/workspace-and-config.md#skill-path-skill-workspace-and-configuration)** — **`skill_path`**, **`skill_workspace`**, **`conf/abd-config.json`** keys (**Workspace and config**). |
| **Build intent** | `conf/build-strategy.json` — strategize loads this **whole JSON**; **`skill_purpose`** must be non-empty for **`strategy_complete`** (minimum to finish strategize). Other keys are **siblings** that enrich **`strategy`** / **`builder_manifest`** — they are **not** part of the **`skill_purpose`** text. See **`agentic-skill-builder/README.md`** (Strategizer). |
| **Normative content** | `content/parts/` — process table rows are **phases**; **steps** inside phase files. Phase markdown files use **descriptive slugs** (`terms-mechanisms.md`, …) — **not** `phase-NN-…` or phase numbers in **H1** titles; pipeline order is **only** in `process.md` (# column) + `build.py` merge list (see **`skill-standards-section-3.md`**). **Column definitions** and required **workspace** row: **`process-table-standards.md`**. |
| **docs/ (non-runtime only)** | **`docs/`** is for material **not** consumed as merged/injected skill payload at operation time: **user manuals**, **migration/planning notes**, **architecture**, **`docs/skill-plan.md`** (plan + **Authoring checklist** section), **standards deltas**. In **abd-skill-builder**, **`docs/`** is only **`standards-delta.md`** — delivery merge order lives in **`README.md`**. **Do not** put markdown (or other assets) in **`docs/`** that **`build.py` merges**, **injects**, or **ships** as the runnable instruction body for phases/operations — that belongs under **`content/parts/`** (including **`library/`**, **`phases/`**, **`process.md`**, **`rules/`** as applicable). |
| **Library** | `content/parts/library/` — **cross-cutting meaning** reused across more than one phase: definitions, tables, glossaries, named concepts, artifact shapes. **Not** phase procedures, **not** step-by-step runbooks, **not** CLI blocks for a single phase, **not** pipeline order (that is **`process.md`** + **`phases/`**). The library **is** the home for that shared meaning; do not maintain a parallel “cross-cutting” layer elsewhere. **`docs/`** may hold a **short index** pointing into **`library/`**; **bodies** live in **`library/`**; merge order lives in **`build.py`**. See **`documentation-standards.md`** → *Library vs phase documents*. |
| **Phases** | `content/parts/phases/<slug>.md` — **person-to-process** instructions for **one** process-table row: I/O, **steps**, scripts, done criteria. **Link** to **`library/`** for deep definitions; avoid duplicating large normative blocks that belong in **`library/`** because multiple phases need them. |
| **Rules** | `rules/*.md` or `content/parts/rules/*.md`; optional `rules/scanners.json`. |
| **Scripts** | `scripts/build.py` (**required** — merge/injection driver; scaffold template is minimal; extend with explicit phase order + per-operation bundles as in **`abd-maps-models-specs`** when needed), scanners, optional `_config.py`. See **`authoring-checklist.md`** → *Base scaffold*. |
| **Tests & fixtures** | **`test/`** — all automated tests for the skill (pytest, smoke scripts, etc.) that exercise **`scripts/`**; optional **`test/fixture/<scenario>/`** for frozen inputs/snapshots; optional **`test/<workspace>/`** dirs when **`conf/abd-config.json`** uses **`active_skill_workspace`** (path relative to skill root). Example: **`abd-maps-models-specs/test/`** — workspace **`test/sample-workspace`**, optional fixture **`test/fixture/<scenario>/`**. **`abd-skill-builder`** itself **does include** **`test/`** (see **`test/README.md`** + **`test/fixture/toy-polite-dialogue/`**) even though **pytest `test_*.py` files** are still optional follow-ups — do not read “pytest wiring pending” as “no **`test/`** folder.” **Operator today** only runs a **Python compile check** on **`operator.compileall_paths`** (usually **`["scripts"]`**; implemented with **`compileall`**) — it does **not** install or run **pytest**. If automated tests are **in scope**, add the **wiring** below. |
| **Agent bundle (always)** | `AGENTS.md` — assembled agent bundle (skill-wide “how it works”); typically generated by `build.py`; **not** gated on `delivery.mode`. |
| **Built slices (operation-time, static mode)** | `content/built/` — pre-merged process + library + rules per skill layout when `delivery.mode` is **`static_built`**. |
| **Documentation focus (this skill only)** | Process plans, **rules**, and **docs** describe **what this skill does** — in positive, runnable terms for **this** package. **Do not** use them as a running commentary on how this skill **differs** from another skill, or why it **doesn’t** do something “because another skill does.” That is **local context in time**, not part of the durable skill. **Dependencies** (other skills, tools, repos, contracts) are **explicit** — names, links, versions — in a **Dependencies** section, `README`, or build-strategy notes. That is **not** the same as narrating deltas to sibling work. |

**Minimal valid skill:** `SKILL.md` + `scripts/build.py` + `skill-config.json` with operator block — see **`test/fixture/toy-polite-dialogue/`** in this skill (**`abd-skill-builder`**).

---

## When automated tests are asked for (pytest wiring)

If the skill should run **pytest** (or similar) under **`test/`**, do **not** assume it is already installed or wired into **`operator`** — add it explicitly:

| Step | What to do |
|------|------------|
| **Dependency** | Add **`pytest`** (and dev-only plugins if needed) to a **`requirements-dev.txt`**, **`pyproject.toml`** `[project.optional-dependencies] dev`, or the skill’s documented venv install step — **commit** the file so others can `pip install -r …`. |
| **Layout** | Tests live under **`test/`** (e.g. **`test/test_*.py`** or **`test/<suite>/`**); shared fixtures in **`test/fixture/`** or **`conftest.py`** as usual for pytest. |
| **Run command** | Document in skill **`README.md`** or **`test/README.md`**: e.g. `python -m pytest test/` from skill root (with venv activated). |
| **CI (optional)** | Add a workflow or monorepo job that installs dev deps and runs the same command. |
| **Operator** | **`operator.run_operator()`** does **not** run pytest by default. To gate releases on tests, extend **CI** or a **wrapper script**; only add **`test`** to **`compileall_paths`** if you intentionally want bytecode checks on test modules (unusual). |

---

## Operator checklist (machine-runnable)

1. `SKILL.md` present.
2. `skill-config.json` parses; `operator` block consistent with files on disk.
3. Python files on declared paths pass a **compile check** (Operator uses **`compileall`**).
4. `python scripts/build.py` exits 0.
5. Each listed **scanner** in **`operator.scanners`** exits **0** (and any step in **`operator.build_pipeline`** that **`build.py`** runs also exits **0** when you rely on **`build.py`** as the full local gate).
6. **`rule_scanner_bindings`** (in **`rules/scanners.json`** when used): each **`rule_file`** and **`scanner`** path exists.

---

## What greenfield scaffold should emit

**`scripts/scaffold_skill.py`** (and equivalent generators) should produce a **complete, runnable skeleton**: file tree, `skill-config.json`, phase markdown stubs, `rules/` / `conf/` as needed, runnable **`build.py`**, optional scanner stubs — **without** baking in customer-specific “gold” domain solutions (those belong in the target workspace, not the template).

This **`abd-skill-builder`** skill ships **templates + `scaffold_skill.py`** as the supported way to create that tree. **`operator.run_operator()`** then validates what is on disk; it does not scaffold new skills by itself.


---

### `skill-standards-section-3.md`

# §3 Skill package layout and content standards

**What this is:** Normative rules for how a **skill repository** is shaped — where **runtime** content lives (`content/parts/`, `rules/`, `build.py`), how **stages / phases / steps** relate, how **process tables** and **Refs** work, optional patterns (e.g. domain + story map), **rule file naming**, and **static vs dynamic** assembly of instructions. **How skills are used in the IDE** (AGENTS.md, `process.md`, code vs AI-chat phases, `generate_prompt`) is defined in [`process-approach.md`](process-approach.md) — read that first.

**How to use it:** Implement **§3.1–§3.4** when authoring or reviewing a skill. Tools and humans use the same rules; nothing here depends on any external “origin” document.

**Scope boundary — skills stay simple:** A **skill package** should express a **linear** pipeline: **stage → phase → (steps inside phase docs)**. The **process table** rows are **phases**, not steps. Keep skills deliberately sequential.

## 3.1 Directory and content conventions

**Hierarchy in the repo:** **Stages** group **phases**. Each **phase** has normative markdown (one file or section per phase, per skill); **steps** live **inside** that phase’s markdown — they are **not** separate rows in the master process table. See **Stages, phases, and steps** below.


| Area                            | Convention                                                                                                        | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Normative content**           | Under /`content/parts/`                                                                                           | Plans, operations, domain narrative — **not** dumped only in chat.                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `**docs/` (non-runtime)**       | /`docs/` at skill root                                                                                            | **User manuals**, **migration/planning notes**, **architecture**, **authoring checklists**, and **narrative** descriptions of delivery. **Do not** put markdown here that `build.py` **merges**, **injects**, or **ships** as the runnable phase/operation body — that belongs under `**content/parts/`** (including `**library/`**, `**phases/`**, `**process.md**`, `**rules/**`).                                                                                                                                   |
| **Phase markdown (source)**     | e.g. /`content/parts/phases/<descriptive-slug>.md`, or one doc per phase with step sections — paths vary by skill | **One row in the process table = one phase.** **Steps** (numbered sub-procedures, “Step 1…”, checklists) are written **inside** this markdown as **normative content of the phase**, not as their own table rows. **Do not** encode execution order in filenames or H1 titles (`phase-02-foo.md`, `# Phase 2 — …`): order belongs in `**process.md`** (the `#` column) and in `**scripts/build.py`**’s explicit file list. Use **stable descriptive** kebab-case slugs so renumbering the plan does not force renames. |
| **Built phase markdown**        | `content/parts/phases/built/<descriptive-slug>.md` and/or `content/built/…` per skill layout | **Generated** from source phase bodies + rules via `scripts/build.py`. **Authors do not hand-edit `built/`.** These files are **materialized instruction blobs** for **static** AI-chat phases and for **`static_built`** delivery — consumed by **`generate_prompt`** (or pasted into chat), **not** by “agents browsing the repo” as the primary UX. IDEs load **`AGENTS.md`**; see [`process-approach.md`](process-approach.md). Folder layout (`phases/built` vs `content/built`) is per skill; document it in **`README.md`**.                                                                                                                                                                                                            |
| **Atomic rules**                | `content/parts/rules/*.md` (or top-level `rules/` in simpler skills)                                              | One concern per file where possible; **names** should encode **phase** and/or **domain concept** + rule name (see §3.2). **Which phase inlines which rule** is declared in **`skill-config.json`** (`phase_rules`, `every_phase_rules`), not scattered in per-rule frontmatter lists.                                                                                                                                                                                                                                                                                                                                                                                               |
| **Roles**                       | `roles/*-role.md`                                                                                                 | One file per **user/agent role** the skill assumes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Process**                     | `content/parts/process.md` or staged process docs                                                                 | **Summary table: each row is a phase** (linked by **Ref** to phase markdown). Stages group those rows. **Steps** appear only **inside** the linked phase files.                                                                                                                                                                                                                                                                                                                                                        |
| **Library markdown**            | `content/parts/library/*.md` (or `parts/library/`)                                                                | **Cross-phase structure and meaning**: definitions, glossaries, artifact shapes, naming, invariants. **Not** phase-local procedures, pipeline ordering, or CLI runbooks—those live in **`process.md`** / **`phases/`** (see **Library vs phase documents** below).                                                                                                                                                                                                                                                     |
| **Repo-facing built artifacts** | `AGENTS.md`, `SKILL.md`, sometimes `README.md`                                                                    | Frequently produced by `scripts/build.py` (merge order per skill). **`AGENTS.md`** is what **IDEs and assistants typically load automatically** for the skill repo.                                                                                                                                                                                                                                                                                                                                                                |
| **Config**                      | `skill-config.json`                                                                                               | Name, version, **`phase_files`**, **`PHASE_LIBRARY_SLICES`**, **`phase_rules`** / **`every_phase_rules`** (ordered rule **stems** inlined per phase bundle — see [`process-approach.md`](process-approach.md)), **`phase_bundle`**, **`operator.compileall_paths`**, **`operator.build_script`**, **`operator.build_pipeline`** (post-merge steps for **`build.py`**), **`operator.scanners`** (Operator gate; align with rule-bound scanners) — skill-specific knobs. See **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** (base framework).                                                                                                                                                                                                                                               |
| **Scripts**                     | `scripts/`                                                                                                        | Operational entry points; may share `_config.py` patterns.                                                                                                                                                                                                                                                                                                                                                                                                                                                             |


### Stages, phases, and steps (how they relate)

**Order is always:** **Stage → Phase → Step** (coarse → mid → finest) — but **only the first two appear as rows** in the master process table. **Steps** are **inside** the phase markdown.


| Term      | Typical meaning                                                                                                                                                                                                                                                                                                                      | Example                                                                                  |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **Stage** | **Coarse pipeline slice** — groups many **phases**; may span days or sessions. Often a heading or section in `process.md` or a staged doc.                                                                                                                                                                                           | **Stage 1 — Extract Context**; **Stage 2 — Map and Model**; **Stage 3 — Specification**. |
| **Phase** | **One row** in the process summary table — the unit of “what we do next” with a **driver**: **human** or **AI actor**. The **Ref** column links to **phase** markdown. Phases answer “are we allowed to proceed?” and **contain** the detailed steps as normative body copy.                                                         | “Corpus audit — Phase N”; **Initiator / Actor** column = human vs AI.                    |
| **Step**  | **Sub-structure inside the phase’s markdown** — numbered instructions, checklists, “Step 1 / Step 2”, optional **suffix letters** (`5a`, `7a`) for companion script runs **within the same phase**. **Not** a row in the process table. Machine state (if any) may still reference `workflow_step` as a **sub-id** inside the phase. | Inside `modules-epics-scaffold-breadth.md`: “1. … 2. … 3a. rebuild index …”              |


**AI-driven phases — how the operation is delivered:** See **[`process-approach.md`](process-approach.md)**. In short: **code-driven** phases = run scripts as documented in the phase file; **AI-chat** phases = produce the instruction block via **`generate_prompt`**-style tooling in **dynamic** (assemble sections) or **static** (use pre-built phase markdown under `phases/built/` or equivalent). The **chat** follows that text; **`built/`** is not “the agent’s filesystem API.”

**Ordering (linear, inside the skill):** Stages order **major outcomes**. **Phases** run in **process table order** (each row = one phase). **Steps** follow the order **written inside** each phase document. **Parallel batches, fan-out, or merge** are **not** modeled as extra table rows; if needed, handle that **outside** the skill package (host app, orchestration, or scripts). **Phases** may **block** a later stage until accepted (e.g. “the indexer phase says rebuild chunks — do not start Stage 2 until accepted”).

**“Process” one-liner:** `content/parts/process.md` (or `parts/process.md`) often opens with a **single pipeline string** (e.g. Context → Foundational spine → …). That line is the **navigation spine**; the **table lists phases** (by stage); **authoritative step detail** lives inside each **Ref**’d phase file.

### Process tables, hyperlinks, and naming in the Ref column

**How the table is built**

- **Rows are phases**, not steps. Columns typically include: `#`, **Phase** (title — sometimes labeled “Step” in legacy tables; **semantically it is the phase**), **Initiator / Actor** (Human→Code, AI, Code), **Script** (if any), **What it does**, **Coverage**, **Ref**, **Inputs**, **Outputs**.
- **Ref** is the **hyperlink hub**: each row points to the **normative markdown for that phase**. **Steps** (numbered sub-procedures) live **inside** that file — not in separate table rows. Python entry points stay in **Script**, not **Ref**.
- **Two-tier phase files:**
  - **Source:** phase markdown authors edit (e.g. `content/parts/phases/<name>.md`, or `parts/steps/<name>.md` when the filename is the **phase** slug — naming varies by skill).
  - **Built:** `content/parts/phases/built/<name>.md` or `content/built/<name>.md` — **rules baked in** from `parts/rules/*.md` via `scripts/build.py`. **Steps remain inside** the built document. Used for **static** prompt generation and **`static_built`** slices — not hand-edited. See [`process-approach.md`](process-approach.md).
- **Cross-links inside the table:** The **Ref** column uses relative markdown links to the **phase** doc, e.g. `[context](parts/context.md)`, `[modules-epics-scaffold-breadth (built)](content/parts/steps/built/modules-epics-scaffold-breadth.md)` (paths vary by skill; **from the skill root** per `AGENTS.md`).

**Naming conventions visible in the table**

- **Phase titles** in the table read like **milestones or operations** (“Parse, curate, chunk, index”, “Integrate and Harmonize”) — stable labels for **phase** / workflow fields. **Finer labels** for **steps inside the phase file** may appear in JSON as `workflow_step` or similar.
- **Phase file names and H1 headings** must **not** duplicate pipeline indices (`phase-00-`, `Phase 3 —` in the title). Those numbers **change** when the plan evolves; **brittle** names churn git history and links. The **Ref** column and `build.py` define order; phase files stay **semantically** named (`story-map.md`, `canonical-context.md`).
- **Letter suffixes** (`5a`, `7a`) describe **sub-steps inside a phase** (e.g. companion script after a numbered step) — **inside the phase markdown**, not extra table rows.

### Concepts and cross-cutting artifacts (generic — all skills)

**This section is the generic rule.** A **skill** packages **concepts** (ideas, definitions, invariants, roles) and **artifacts** (outputs, schemas, manifests) that the workflow references across **multiple stages or phases**. Anything that would be **repeated** if pasted into every phase file should instead live in **its own file** (usually markdown under `content/parts/`, sometimes JSON alongside) so there is a **single source of truth**.


| Guideline           | Meaning                                                                                                                                                                                                         |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **When to extract** | If a concept or artifact **spans** more than one phase (or stage), give it a **dedicated** doc (or structured file) and **link** from phase bodies — do not duplicate long definitions in each phase.           |
| **Naming**          | Conventional filenames (`glossary.md`, `concepts.md`, `artifacts.md`, `roles/`*, etc.) vary by skill; **discover** and **validate** presence from templates and this skill’s `build.py`, not one global layout. |
| **Not every skill** | A minimal skill might only have `SKILL.md`, `content/parts/process.md`, and phase files — **no** separate “domain” or “story map” layer. That is valid.                                                         |


### Library vs phase documents (authoring split)

**`library/`** answers **what** (stable meaning for ideas and artifacts that **more than one** phase touches). **`phases/<slug>.md`** answers **how for this step** (operator procedure: inputs, outputs, ordered steps, **commands**, done checks).

| In **`library/`** | In **`phases/`** (not a second copy of the whole library) |
| --- | --- |
| Definitions, tables, schemas, vocabulary used across phases | Purpose of **this** phase, **steps**, checklists, **script/CLI** lines |
| Single source of truth for a construct that spans the pipeline | **Links** into the right **`library/`** shard for depth |
| Optional injection slices (`abd:begin` / `abd:end`) | **No** long normative essays that other phases would repeat verbatim |

**Do not** put **numbered phase procedures**, **order-of-operations** for the skill, or **phase-to-phase sequencing narrative** in **`library/`**—that belongs in **`process.md`** and the relevant **`phases/`** files. **Do not** park **large** reusable specs only inside one phase file if another phase needs the same text—extract to **`library/`** and link.

Normative detail for writers: [`documentation-standards.md`](documentation-standards.md) and [`../../rules/content-placement.md`](../../rules/content-placement.md).

### Optional pattern — domain narrative + interaction tree (maps-models–class skills only)

Some skills (notably **abd-maps-models-specs** and similar) **choose** to separate **two parallel artifacts** that must stay in sync. **Do not** treat this table as the default for **all** skills — only for skills that explicitly adopt this shape.


| Piece                            | Role                                                                                                                                                                                                    | Typical location (example skill)                                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Domain narrative**             | **State and structure** — modules, **domain concepts** (CRC-style: owns, properties, operations, `extends`, invariants), evidence hooks. Answers **what things are** and **what owns which rules**.     | e.g. `parts/domain.md` + evolving `map-model-spec.json` (`modules_and_epics`, `concepts[]`, chunk citations). |
| **Story map / interaction tree** | **Behavior** — epics, sub-epics, stories, scenarios; **Trigger / Response**; **Pre-Condition**; **Given/When/Then** where required. Answers **who does what** and how behavior references domain state. | e.g. `parts/story-map.md` + nested JSON under epics (`stories`, `sub_epics`, etc.).                           |


**When this pattern applies**

- **Same vocabulary:** Domain concept names (`concepts[].name`) and story references can be held to **one namespace** — scanners may enforce **exact string match** where the skill defines that rule.
- **Evidence ladder / paired edits:** Concepts may carry `evidence_stage`; **domain** vs **journey** edits are **paired** in skills that implement both files.
- Skills **without** this split still use the **generic** rule above: cross-cutting concepts → **their own** markdown (whatever the skill calls them), not repeated per phase.

### Rules and automated checks (default wiring)

For **machine-enforceable** rules, use the **base framework** in **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**:

- Declare **rule → scanner** bindings in **`rules/scanners.json`** (`rule_scanner_bindings`).
- List **ordered post-merge steps** under **`skill-config.json` → `operator.build_pipeline`**; **`scripts/build.py`** runs them after merges (same pattern as **`abd-maps-models-specs`**).
- Keep **`operator.scanners`** consistent with those scripts for **`operator.run_operator()`** / CI.

**Process tables** should **not** enumerate every scanner as if it belonged to a single phase; document automation at the skill level and link **`rules/scanners.json`** + **`build.py`** / **`build_pipeline`**.

## 3.2 Rule file naming (heuristic standard)

Target pattern (flexible regex for validation):

```text
{phase-or-stage}__{domain-concept-or-scope}__{short-rule-name}.md
```

Examples mirror **story synchronizer / maps-models** style: scanners and rules tied to **phase** and **concept** (e.g. `chunks_must_be_referenced`, `concept-layering-scaffold`). **Propose** names from the **phase** + concept + verb (and step text inside the phase doc if needed), then **check uniqueness** under `parts/rules/`.

## 3.3 Assembly model (static vs dynamic)

**Two different “static vs dynamic” pairs** — do not conflate:

1. **`build.py` assembly** (repo artifacts): Each skill ships `scripts/build.py`. It merges **process + library + phases (+ rules)** into **`AGENTS.md`** and optional **`content/built/`**. Flags like `--assembly static|snapshot` are **per skill** when present.

2. **AI-chat prompt generation** (`generate_prompt`): For **AI-driven** phases only — **dynamic** = assemble instruction string from sections; **static** = emit text from **pre-built** phase file under `phases/built/` (or documented path). See [`process-approach.md`](process-approach.md).

**Per skill:** `build.py` is the **authoritative** merge driver for **this** repo; scaffolding **emit or check** trees — they do **not** replace `build.py`.

**Flag on `build.py`:** The skill’s `build.py` may expose **CLI flags** for snapshot vs interactive merge; exact names are per skill. For **prompt** modes, document **`generate_prompt`** (or equivalent) next to **`build.py`** in **`README`** / **`AGENTS.md`**.


| Mode (merge / delivery) | Mechanism                                                                               | When                                                               |
| ----------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Static (merge)**      | `build.py` merges **built-phase** fragments into `AGENTS.md` / `SKILL.md` (and related) | Release, reproducible snapshot; CI; “what ships”.                  |
| **Dynamic (merge)**     | Runtime concatenation by **phase** / **operation** from `skill-config.json` + manifest  | Interactive sessions, partial rebuild, IDE-driven iteration. |


A **host** (CI, IDE, or orchestrator) may emit an **internal** manifest (JSON or YAML) for a **given generation run**, listing which fragments form which artifact for both modes; the skill’s `build.py` **may read** that manifest (or embedded config) when implementing **static** merges and documents how **dynamic** mode resolves fragments at runtime. That manifest is **optional** and **not** a standard every skill must carry — only **documented** `build.py` behavior is.

## 3.4 Reference skills (illustrative)

Other skills in the monorepo **illustrate** patterns (long `AGENTS.md`, phased pipelines, rules + scanners). They are **examples**, not extra requirements. **Operator** checks and layout rules are grounded in **abd-skill-builder** library files and each skill’s **`skill-config.json`** — not in a separate “corpus” file unless your team adds one.


---

### `builder-vs-operator.md`

# Builder vs Operator (today)

**Generation / scaffold (“builder” in the loose sense):** Anything that **emits** a new skill tree — typically **`abd-skill-builder`’s `scripts/scaffold_skill.py`** plus templates — producing `SKILL.md`, `skill-config.json`, phase markdown, `rules/` stubs, `scripts/build.py`, optional scanners. Output should match **§3** layout and avoid embedding customer “gold” solutions in the template.

**Operator (structural gate):** **`agentic-skill-builder`** **`operator.run_operator()`** — validates `skill-config.json`, runs a **Python compile check** on the paths in **`operator.compileall_paths`** (the implementation uses Python’s **`compileall`** module), runs **`operator.build_script`** (typically `python scripts/build.py`), then runs **scanner scripts** listed under **`operator.scanners`**. A normative skill also declares **`operator.build_pipeline`**: the **ordered post-merge steps** that **`build.py`** runs after writing **`AGENTS.md`** / built slices (rule-bound scanners, emitters, manifest, lint—**per skill**). **Rule → scanner** bindings live in **`rules/scanners.json`**; see **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** (base framework for all skills). Operator does **not** create greenfield skills; that is **`scaffold_skill.py`** and authoring.

**This skill’s role:** Ship **standards** under **`content/parts/library/`**, **process + phases**, **`scaffold_skill.py`**, and **templates** so authors get a compliant tree first, then Operator keeps it green.


---

### `rules-and-automated-checks.md`

# Rules and automated checks (base framework for every skill)

**Status:** **Normative default** for Open Agent Skills in this repo. When a skill defines **governance rules** (`rules/*.md`) and wants **machine enforcement**, wire checks this way—not as one-off phase script call-outs.

## What owns what

| Layer | Owns |
| --- | --- |
| **`rules/<stem>.md`** | The **human-readable rule**: scope, must/should, examples, done criteria. |
| **`rules/scanners.json`** | **Which script enforces which rule** — `rule_scanner_bindings[]` maps `rule_id` + `rule_file` → `scanner` path (relative to skill root). Optional top-level **`scanners`** lists scanner scripts for tooling that expects a flat array. |
| **`skill-config.json` → `operator.build_pipeline`** | **Ordered post-merge steps** that **`scripts/build.py`** runs after it writes **`AGENTS.md`** / **`content/built/`** (or your skill’s equivalent). Entries are typically **`scripts/...py`** paths: rule-bound scanners, emitters, manifest generators, rule-example linters, etc. **Empty or omitted** means “merge only” (skills with no automated checks yet). |
| **`skill-config.json` → `operator.scanners`** | **Operator / CI gate** — paths **`agentic-skill-builder`** **`operator.run_operator()`** runs **after** **`operator.build_script`**. **Keep these paths aligned** with the scanner steps you care about (usually the same modules listed in **`build_pipeline`** and/or **`rules/scanners.json`**), so “green build” and “green operator” mean the same checks. |

## What you do not do

- **Do not** treat **scanners** as **phase-owned scripts** in **`process.md`** process tables. Phase rows are for **human/AI procedure** and **merge / emit** entry points (e.g. `python scripts/build.py`), not for listing every validator. If readers need detail, add a short **“Rules and automated checks”** subsection in **`process.md`** that points here and to **`rules/scanners.json`**.
- **Do not** bind scanners only in prose. If a rule is machine-checked, add a **`rule_scanner_bindings`** row and a **`build_pipeline`** step (and **`operator.scanners`** / Operator docs as required by your host).

## Execution flow (mental model)

1. Author edits **`content/parts/`**, **`rules/`**, **`skill-config.json`**.
2. **`python scripts/build.py`** merges instruction bundles, then runs **`operator.build_pipeline`** in order (if present).
3. **Operator** (or CI) runs compile check → **`build.py`** again → **`operator.scanners`** (when configured).

**Reference implementation:** **`abd-maps-models-specs`** — `rules/scanners.json`, **`operator.build_pipeline`** in **`skill-config.json`**, and **`scripts/build.py`** driving the pipeline after merge.

## Scaffolded skills

Greenfield trees from **`scaffold_skill.py`** should ship **`rules/scanners.json`** (even if bindings start empty) and a **`skill-config.json`** fragment that includes **`operator.build_pipeline`** alongside **`operator.scanners`**, so authors extend **one** pattern instead of inventing ad hoc wrappers.

See also: **[`skill-standards-section-3.md`](skill-standards-section-3.md)** (§3.1 config row), **[`builder-vs-operator.md`](builder-vs-operator.md)**, **`rules/README.md`** at the skill root.


---

## Rules

*No rules for this phase. List rule stems (filename without `.md`) under `skill-config.json` → `phase_rules` for this phase slug, and optionally `every_phase_rules` for rules that apply to every phase. See `parts/library/process-approach.md` § Phase bundle — rules.*


---

## Phase: scaffold

## Principles

**AI quality — normative rules, scanners, and review.** This shard is injected under **`## Principles`** in phase bundles; the heading above is added by the assembler.

**Scope:** In **abd-skill-builder**, this file is injected as **`## Principles`** and is the **first** section in each AI-chat phase bundle (`python scripts/generate.py --phase <slug>` and `content/parts/phases/built/<slug>.md`). Read it **before** Role, Phase body, Library shards, and Rules for that phase.

---

**Every rule in `rules/` is two things at once:** (1) **Normative advice** — prose the model follows while authoring **`content/parts/`**, **`rules/`**, **`skill-config.json`**, and other skill artifacts. (2) **Checkable expectations** — where this repo ships a **scanner** under **`scripts/`**, it catches common layout or config misses; where it does not, **you** still review against the rule text.

**Example (wrong):** Treating a green **`python scripts/build.py`** as enough while **`AGENTS.md`** still disagrees with **`content/parts/`** or **`phase_rules`** omits a rule you claimed to enforce.

**Example (correct):** Read the **Rules** section in this bundle, align files with **`library/`** norms, run **`python scripts/build.py`** (and **`operator.scanners`** when configured), then **re-read** outputs against each applicable rule.

---

## Layer 1 — Generate with rules

While generating or editing skill artifacts:

- Apply **`rules/*.md`** inlined into this bundle (and related **`library/`** docs).
- Prefer **DO / DON’T** and **good vs bad** fragments inside each rule — they are the contract for *shape*, not only for CI.

---

## Layer 2 — Mechanical checks (this skill)

After you have files on disk, the pipeline can run:

| Mechanism | What it does |
| --------- | ------------ |
| **`python scripts/build.py`** | Merges **process** + per-phase bundles into **`AGENTS.md`** and **`content/built/`**, then runs **`operator.build_pipeline`** (e.g. **`scripts/scanner_skill_builder_layout.py`**) when configured. |
| **`rules/scanners.json`** | Declares **rule → scanner** bindings when your skill uses them; align with **`operator.scanners`**. |

**Example (wrong):** Hand-editing **`AGENTS.md`** while **`build.py`** is supposed to own the merge.

**Example (wrong):** Adding a scanner only in prose — no **`rule_scanner_bindings`** or **`build_pipeline`** step.

**Example (correct):** Fix issues reported by scanners, re-run **build**, keep **`skill-config.json`** paths honest.

Scanners are **necessary** for what they implement; they are **not sufficient** for semantic quality (e.g. a valid tree that still mis-describes what the skill does).

---

## Layer 3 — Adversarial pass (human or AI)

With clean tool output, still ask:

- Does each **rule** that applies to this phase pass **by intent**, not only by letter?
- Would a reviewer see **drift** between **`SKILL.md`**, **`process.md`**, and **`phases/`** even when the tree validates?

Use the **Corrections format** below when fixing issues.

---

## Corrections format

When recording or fixing a problem:

| Field | Content |
| ----- | ------- |
| **Rule** | Rule id or `rules/<file>.md` name |
| **Example (wrong)** | What was done incorrectly |
| **Example (correct)** | What it should be |
| **Scanner or validator** | If applicable — see **`rules/scanners.json`** and **`operator.build_pipeline`** |
| **Likely source** | One of: prompt gap · rule not read · edge case · automation gap |

---

## Do not bypass the documented pipeline

**AI phases** mean: read inputs, reason, update the **source** files this skill owns under **`content/parts/`**, **`rules/`**, and config — not one-off scripts that rewrite merged outputs **instead** of fixing sources. Automation that ships with the skill lives under **`scripts/`** and is wired through **`skill-config.json`** (**`build.py`**, **`build_pipeline`**, **`operator.scanners`**) as documented in **`library/rules-and-automated-checks.md`**.

**Example (wrong):** Patching **`AGENTS.md`** directly to “pass” review while **`process.md`** is unchanged.

**Example (correct):** Edit **`content/parts/`** (or **`rules/`**), run **`python scripts/build.py`**, commit regenerated **`AGENTS.md`** / **`content/built/`** when using **`static_built`**.


---

## Phase

# Phase: Scaffold

For an **existing** skill tree (not greenfield): **[`plan-migrate.md`](plan-migrate.md)** (**1b**) — **delta** + user selection; then **[`migrate.md`](migrate.md)** (**2b**) — **execute** moves. Do **not** use **`scaffold_skill.py`** on an existing tree.

**Greenfield:** Pipeline order is **[`process.md`](../process.md)**. Have **`docs/skill-plan.md`** from **[plan-script-build](plan-script-build.md)** (including the **Authoring checklist** section) before you run this scaffold sequence.

---

## Base scripts from abd-skill-builder (what scaffold emits)

**`scripts/scaffold_skill.py`** in **abd-skill-builder** builds a new skill under **`--out`**. It writes **`scripts/`** using templates from **`abd-skill-builder/templates/`** and **copies** **`generate.py`** and **`set_workspace.py`** verbatim from **abd-skill-builder** `scripts/`. After scaffold, you **extend** merge lists and phase slugs to match your **`parts/phases/*.md`** and **`parts/library/`**.

| Script | Source | Role | What you extend |
| --- | --- | --- | --- |
| **`generate.py`** | **Copied** from **abd-skill-builder** `scripts/generate.py` | Thin CLI: loads **`generate_prompt.py`** and runs **`main()`**. | Almost never—keep in sync with builder if the contract changes. |
| **`set_workspace.py`** | **Copied** from **abd-skill-builder** `scripts/set_workspace.py` | Prints or sets **`active_skill_workspace`** / legacy keys in **`conf/abd-config.json`** (same CLI as **abd-maps-models-specs**). | Almost never—keep in sync with builder. |
| **`generate_prompt.py`** | **Template** `generate_prompt.py.template` (or equivalent in **`templates/`**) | Resolves **`parts/`** vs **`content/parts/`**, loads **`phases/<slug>.md`**, optional **`phases/built/`** for **`--mode static`**. | **`PARTS`** path logic; **`PHASES`**, **`BUILT`**; add flags only if the skill needs them. Every AI-chat phase must be reachable via **`python scripts/generate.py --phase <slug>`**. |
| **`build.py`** | **Template** `child_build.py.template` | Merges **`process.md`** + **`library/*.md`** + **`phases/*.md`** → **`AGENTS.md`** (+ **`content/built/`**); then runs **`operator.build_pipeline`** from **`skill-config.json`** (rule-bound scanners, emitters—see **[`../library/rules-and-automated-checks.md`](../library/rules-and-automated-checks.md)**). | **`LIBRARY_FILES`** tuple (order); **`PHASE_FILES`** tuple (order—**must** start with **`workspace-and-config`** if that phase exists); **`PHASE_SECTION_HEADINGS`** for human **`##`** titles; **`_process_md_for_agents`** link rewrites for your paths; title **`# AGENTS — <skill>`**; extend **`build.py`** to run **`build_pipeline`** if the template is older. |
| **`scanner_smoke.py`** | **Template** `child_scanner_smoke.py.template` | Placeholder scanner exit **0**; Operator wiring via **`skill-config.json`**. | Replace or supplement with real scanners (e.g. layout, JSON schema); register in **`rules/scanners.json`**. |

**abd-skill-builder** also ships **`scanner_skill_builder_layout.py`** — **not** copied to child skills by default; child skills use their own scanners.

**Operator** (via **agentic-skill-builder**) expects **`skill-config.json`** to list **`operator.build_script`** (typically **`python scripts/build.py`**) and **`operator.compileall_paths`**. **`generate.py`** is not part of Operator—it is for **human/AI sessions** running a phase prompt.

---

## Other scaffolded paths (brief)

| Path | Notes |
| --- | --- |
| **`conf/abd-config.json`** | From **`abd-config.json.template`** — set **`active_skill_workspace`** (see **[Workspace and config](workspace-and-config.md)**). |
| **`parts/process.md`** or **`content/parts/process.md`** | From **`process.md.template`** — replace/enrich with **[`process-team.md.template`](../../templates/process-team.md.template)** and obey **[`process-table-standards.md`](../library/process-table-standards.md)**. |
| **`docs/skill-plan.md`** | From **`skill-plan.md.template`** + injected **Authoring checklist** body. |
| **`phases/workspace-and-config.md`** | **Not** always emitted by minimal scaffold—**add** **`workspace-and-config.md`** under **`parts/phases/`** (copy from **abd-skill-builder** or follow **`process-table-standards.md`**) so **Phase 0** / **Workspace and config** exists. Wire it **first** in **`build.py`** **`PHASE_FILES`** and add a process table row with **`#`** **`0`**. |

If your **`templates/`** folder is missing files **`scaffold_skill.py` references** (`process.md.template`, `child_build.py.template`, etc.), pull them from **abd-skill-builder** or run scaffold from a complete **abd-skill-builder** checkout.

---

## Steps (greenfield)

1. **Skill plan + checklist:** Open **[`../library/authoring-checklist.md`](../library/authoring-checklist.md)** for norms; **`docs/skill-plan.md`** holds the plan and **## Authoring checklist** (scaffold injects the library body into that section). Work **A → B → C** (ask questions, AI suggestions, check boxes) for build intent, rules/scanners, library, cross-cutting concepts, **`delivery.mode`**, then operator sign-off.
2. Choose a **skill id** (directory name; kebab-case recommended).
3. Run `python scripts/scaffold_skill.py --name <id> --out <parent>/<id>` (from **abd-skill-builder** or your packaged builder).
4. Edit `conf/build-strategy.json` — set **`skill_purpose`** (required for `strategy_complete` in the delivery graph). Add other keys from the template as needed; they are **separate fields**, not part of the **`skill_purpose`** string.
5. **Wire scripts:** Extend **`build.py`** and **`generate_prompt.py`** per the table above; add **`parts/phases/workspace-and-config.md`** and process row if the minimal tree omitted them.
6. Flesh out **`content/parts/process.md`** and phase files. For a **rich** process doc, copy/adapt **`templates/process-team.md.template`**; follow **`process-table-standards.md`** for columns and workspace phase. Add rules and scanners as needed (see checklist §2–5).
7. Add tests under **`test/`** (scaffold emits **`test/README.md`**); put fixtures in **`test/fixture/…`** and any **`active_skill_workspace`** under **`test/<name>/`** per **[`../library/skill-repo-standards.md`](../library/skill-repo-standards.md)**.
8. Run `python scripts/build.py`, then `agentic-skill-builder run --skill-path <path>` or equivalent Operator checks.
9. **Fill the scaffold (content):** Use **[`fill-scaffold-parts.md`](fill-scaffold-parts.md)** (**process** phase **2c**) — AI + user **author** **`library/`**, **`rules/`**, and richer **process**/**phases** from **`SKILL.md`**, **`docs/skill-plan.md`**, and the plan. Emit the phase prompt with `python scripts/generate.py --phase fill-scaffold-parts`.

## Anchor

This phase **writes** the skill tree and **establishes** the operator contract — no domain modeling yet.


---

## Library



---

### `documentation-standards.md`

# Skill documentation standards

**Canonical:** `skills/abd-skill-builder/content/parts/library/documentation-standards.md` (merged into **`AGENTS.md`**).

Use these rules when you author or refactor **process**, **phase docs**, optional **`docs/`** reference, staged **`content/built/`** output, and **AGENTS.md** for any Open Agent Skill. They prevent tangled cross-cutting docs and unreadable process prose.

## Delivery mode (`static_built` vs `runtime_injection`)

Declare **`delivery.mode`** in **`skill-config.json`** (default **`static_built`**). That flag answers whether the agent relies on **checked-in** **`content/built/`** + **`AGENTS.md`** or on **runtime** assembly from **`rules/`**, library fragments, and phase manifests. Normative definitions, when each applies, and how the two stay in sync are in **`delivery-modes.md`**.

## Workspace configuration

Skills that **route** to a customer tree keep **`conf/abd-config.json`** at **`skill_path`** with **`active_skill_workspace`** (and optional **`known_skill_workspaces`**). The file is **part of the repo**—**edit `active_skill_workspace`** to point at the workspace root (see **[workspace-and-config — Skill path, skill workspace, and configuration](../phases/workspace-and-config.md#skill-path-skill-workspace-and-configuration)**). A host (e.g. SkillField) may override. The install folder does **not** hold the customer project—only pointers. Workspace-local parameters live under **`skill_workspace/conf/`** per skill docs. Do not leave “where we run” only in prose unless the skill documents overrides.

## Agent-facing vs reference (read this first)

**If text is merged into `AGENTS.md`, injected into prompts, or otherwise part of the agent bundle, it belongs under `content/parts/`** (e.g. `process.md`, `phases/<phase>.md`, shared fragments). It does **not** live “only in `docs/`” with the expectation that the agent will see it unless your build copies it in.

**Staged build (`content/built/`):** When a complete file is **assembled** from pieces—e.g. a **base** plus **rules** plus **operator/story roles**—write the **intermediate, fully expanded** markdown under **`content/built/`** (or `content/parts/built/` / `phases/built/` if the skill already uses that layout). Then the final step generates the **complete** artifact (`AGENTS.md`, a single phase handoff, etc.). Do not skip the staged output if you need to diff or review what rules were baked in. (Example pattern: `abd-solution-modeler` uses `phases/built/` for phase specs.)

**`docs/`:** Use for **long-form reference** that operators (or tools) open beside the skill—principles, execution order, invariants, **and** standalone construct write-ups (schemas, package layout) **when** those are **not** duplicated as the sole copy of agent instructions. Phase tables and “what you must do” for the agent still live in **`content/parts/`**; `docs/` may **link** to the same ideas or hold deeper detail. If a norm must be in the agent’s context, mirror or generate it from `content/parts/`, not only from `docs/`.

## Voice and role

Write for the **operator** in **second person** (you, your). Frame the work clearly:

- **Your role** — What you are responsible for in this stage or skill (one or two sentences).
- **What you must do** — Imperatives and phase order (use bullets for several short obligations).
- **What you produce** / **How you know you succeeded** — Outcomes and done criteria.

Prefer **you must**, **you will**, and **then you** (sequence) over passive voice (“the pipeline establishes,” “artifacts are emitted”). Say who runs a script or makes a decision.

## Where content belongs

| Kind | Put it here | Do not |
| --- | --- | --- |
| **Process spine** — stages, phase numbers, tables, links to phase files | `content/parts/process.md` (or skill’s `content/process.md`) | Paste the entire phase table again as a second narrative. |
| **Phase behavior** — steps, checklists, **script invocations**, file paths for **this phase only** | `content/parts/phases/<phase>.md` | Split one phase across three cross-cutting docs; **duplicate** long cross-phase definitions—**link** to **`library/`** instead. |
| **Library shards** — definitions, glossaries, artifact shapes, naming, invariants for ideas that **span multiple phases** | `content/parts/library/<topic>.md` | Phase-local procedures, numbered runbooks, pipeline order, or “run `python scripts/…`” blocks that belong in **`phases/`**. |
| **Baked agent instructions** — bases + rules + roles merged before `AGENTS.md` | Source fragments under `content/parts/`; **output of merge** under `content/built/` (or `phases/built/`) **before** final generation | Edit only the final `AGENTS.md` by hand when a build step should own the merge. |
| **Standalone construct reference** — one artifact contract (schema, validators, chunk layout), diagrams, deep dives | `docs/<descriptive-name>.md` | Treat `docs/` as the **only** place agent-facing norms live; duplicate the “must do” into `content/parts/` or generate into `content/built/`. |
| **Cross-cutting** — principles, execution order, invariants that apply across phases | Usually `docs/` or `content/parts/library/` (e.g. principles prose); **governance rules** that vary by phase: **`skill-config.json`** → **`phase_rules`** / **`every_phase_rules`** + `rules/*.md` (see **`process-approach.md`**). **Link** from `content/parts/` where needed | Restate every phase inside cross-cutting docs; **link** to the process table instead. |

**Reference-doc filenames:** Do **not** prefix `docs/` filenames with phase numbers (e.g. avoid `phase2_terms.md`). Use **descriptive kebab-case** slugs (`terms-mechanisms-contract.md`, `behavioral-story-map.md`). Phase order belongs in `process.md` and `content/parts/phases/`, not in filenames.

**Cross-cutting** is for rules and order that are **not** naturally owned by a single phase. If the text is really about one phase only, prefer that phase’s file in `content/parts/phases/` plus a thin pointer from `docs/` if you keep a global index there.

## Library vs phase documents (split responsibility)

Use this split in **every** skill that has both **`library/`** and **`phases/`**:

- **`library/`** = **structure and meaning** shared across phases (what a thing *is*, how it is named, what fields exist, how it relates to other ideas). Think **reference** and **single source of truth** for multi-phase concepts.
- **`phases/*.md`** = **execution** for one pipeline step (what *you* do next, in order, including **commands** and **done checks**). Think **operator procedure** for *this* phase only.

**Hard bars**

| Layer | Must include | Must not be (move or trim) |
| --- | --- | --- |
| **`library/`** | Stable definitions, tables, schemas, cross-phase vocabulary | Long “how to run this phase” sections; **step sequences**; **script/CLI** runbooks; **phase ordering** or “after phase X…” workflow story |
| **`phases/`** | Short purpose, I/O, **steps**, script lines, checklists, **links** to **`library/`** for deep defs | Entire glossaries or artifact specs duplicated from **`library/`**; normative essays that belong in **`library/`** because **other phases** need the same text |

If a paragraph would still make sense **after renumbering or reordering phases**, it probably belongs in **`library/`** or **`rules/`**, not inside a single **`phases/<slug>.md`**.

**Governance rule in this repo:** [`rules/content-placement.md`](../../rules/content-placement.md).

## Prose style

- Several **short** points → **bullets**.
- One developed idea → **sentences** in a **paragraph**.
- Avoid long **semicolon chains** pretending to be one sentence.
- Avoid narrating **migration** from an old doc or old skill (“formerly §2.6”). Describe **this** skill only.

## Process tables

Keep the **stage narrative** at **intent and outcome**. The **table** holds actors, scripts, refs, and deliverable paths.

Normative column meanings, the required **workspace** phase (**Phase 0** informally), **`Input`/`Output` rules**, and **`build.py`/`generate.py` alignment** are in **[`process-table-standards.md`](process-table-standards.md)**. Use that doc whenever you create or refactor **`process.md`** in another skill.

Optional: an extra **Summary** column per row (**two or three sentences**) is allowed if you keep the abd-skill-builder **seven-column** shape as the default—do not drop **Input** / **Output** / **Scripts** in favor of summary-only rows. For the **maps-models-specs**-style table (**`Script`**, **`Outputs`**, **`Ref`**), put **`Summary`** in the **third** column (after **`#`**, **Phase**) and **`Ref`** **last**—see **`process-table-standards.md`** § Maps / models / specs pipeline table.

## When you edit

1. Update the **smallest** place: phase file or construct doc first.
2. If you are repeating script names and outputs that are **already** in the table, **delete** the repetition and keep purpose or pointer to `phases/`.
3. Regenerate **AGENTS.md** after changing `content/` so agents see the update.


---

### `process-table-standards.md`

# Process table standards (for `process.md`)

**Use this** whenever you author or refactor **`parts/process.md`** (or **`content/parts/process.md`**) so skills stay consistent with **abd-skill-builder** and Operator expectations. Pair with **`skill-standards-section-3.md`** (stages / phases / steps) and **`documentation-standards.md`** (voice, where content lives).

---

## Workspace phase (“Phase 0”) — required for every skill

Every skill that can target a **project tree** or needs unambiguous **where am I running?** semantics must include a **workspace** phase:

| Item | Rule |
| --- | --- |
| **Phase file** | **`parts/phases/workspace-and-config.md`** (or under **`content/parts/phases/`** if your skill uses that layout). Slug: **`workspace-and-config`**. |
| **Process row** | First process-table row **after** any “standards / checklist” preamble; **#** column **`0`** (Phase 0 — workspace first in the pipeline). **Team process plate** (`process-team.md.template`) hard-codes this row; **do not** rename the **Phase** link text to **`Phase 0 — …`** inside the table cell—keep the stable slug title **Workspace and config**. |
| **Heading & name** | Phase document **H1** and links: **Workspace and config** (not **Phase 0 — …** in the phase file’s **H1**). In **`parts/process.md`**, the **section** heading **Phase 0 — Workspace and config** is OK; the **process table** still uses the stable **Phase** column title above. |
| **Config** | **`conf/abd-config.json`** at **`skill_path`** with **`active_skill_workspace`** (and optional **`known_skill_workspaces`**). Same **JSON shape** across skills; see **abd-skill-builder** reference **`conf/abd-config.json`**. |
| **Merge / generate** | **`build.py`** should list **`workspace-and-config`** **first** in the phase merge list when that file exists; **`generate.py --phase workspace-and-config`** must resolve for AI-chat steps. |
| **CLI — `active_skill_workspace`** | Every scaffolded skill includes **`scripts/set_workspace.py`** (copied from **abd-skill-builder**). **Process** row **0** **Scripts** cell must include the same wording as **abd-maps-models-specs** phase **Set workspace**: `` `python` [`scripts/set_workspace.py`](…) — no args prints current; `<path>` sets `active_skill_workspace` in `conf/abd-config.json` ([workspace-and-config](phases/workspace-and-config.md)) `` — then **`·`** and **`generate.py`** for the AI-chat phase when both apply. |

Routing details are **not** duplicated inside **Plan** or **Scaffold** phase bodies—**link** to **`workspace-and-config.md`**.

---

## Process table columns (abd-skill-builder shape)

Use this **seven-column** header (exact labels help readers and tooling):

| Column | Meaning |
| --- | --- |
| **`#`** | **Phase id** in the pipeline: **`0`** for workspace (Phase 0); **`1a` / `1b`** for plan variants; **`2a` / `2b` / `2c`** for create/fix/fill; **`3`** for operator; or your skill’s own scheme. **Order** is this column + stage sections—not filenames. |
| **Phase** | **Linked title** to **`phases/<slug>.md`**. Stable, descriptive name (not `phase-02-foo.md` in the link text). |
| **Description** | **What happens** in this phase: decisions, constraints, pointers to other phase docs for cross-cutting topics. **Not** a second copy of the whole phase file—enough to choose the right doc. |
| **Actor** | **Who runs it:** Human / AI, Code, Human / AI + Code, etc. |
| **Input** | **What you must have** to start: paths, prior artifacts, CLI flags, **not** the phase’s primary deliverable if that deliverable is produced **in** this phase (avoid listing **`docs/skill-plan.md`** as **Input** for **1a** when **1a** creates that file—use *library norms + target workspace* instead). |
| **Output** | **Concrete artifacts** when the phase is done: files, directories, exit criteria. For **scaffold (2a)**, lead with the **scaffolded skill tree** ( **`SKILL.md`**, **`skill-config.json`**, **`conf/`**, **`content/parts/`** or **`parts/`**, **`scripts/`**, **`rules/`**, **`test/`**, **`docs/skill-plan.md`** ), then **`AGENTS.md` / `content/built/`** after **`build.py`**—not only the skill-plan template. |
| **Scripts** | **Commands** with **entry script names**: `python scripts/generate.py --phase <slug>`, `python scripts/build.py`, **`scaffold_skill.py`**. **Do not** pack **rule-bound scanners** here—those are skill-wide; document them under **Rules and automated checks** (see **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**) and run them via **`build.py`** / **`operator.build_pipeline`**. One cell; use **`·`** between multiple commands. |

**Do not** use a vague **Output** that only points at a **template file** when the real outcome is a **written document** or **directory tree**—say the **path** under the skill (e.g. **`docs/skill-plan.md`**).

### Maps / models / specs pipeline table (seven columns, `Script` + `Outputs` variant)

Skills such as **abd-maps-models-specs** use the **same seven-column count** with different labels: **`#`**, **Phase**, **Summary**, **Actor**, **Script**, **Outputs**, **`Ref`**.

- **`Summary`** is the **third** column (after **`#`** and **Phase**) so wide prose sits early in the row and previews well in Markdown renderers.
- **`Ref`** is the **last** column (phase doc links stay the right-hand anchor).

Keep **exact header labels** (**`Outputs`** for concrete artifacts and paths) so tables stay consistent across stages.

---

## Stages vs tables

- **Stage** sections (**`## Stage N — …`**) carry **narrative**: purpose, what you produce, how you know you succeeded.
- **Tables** carry **rows = phases**: Ref, Actor, Input, Output, Scripts. **Steps** stay **inside** phase markdown files, not extra table rows (per §3).

---

## Language

- **Second person** for operator-facing prose in phase files (**you**, **your**); see **`documentation-standards.md`**.
- **Process one-liner** at the top of **`process.md`**: pipeline string with **linked phase names** (e.g. **Workspace and config** → **Plan** → …).
- **Routing** cells: short **“Routing: [Workspace and config](…)—not repeated here.”** instead of repeating **`conf/`** keys.

---

## `build.py` and `generate.py` alignment

When you add or rename a phase:

1. **`parts/phases/<slug>.md`** exists.
2. **`process.md`** has a row with that **Phase** link and **`#`** id.
3. **`scripts/build.py`** — **`PHASE_FILES`** (or equivalent) lists **`slug`** in merge order; **`LIBRARY_FILES`** lists library shards in order.
4. **`scripts/generate_prompt.py`** — resolves **`parts/phases/<slug>.md`** (or **`content/parts/phases/`**); **`generate.py`** stays the thin CLI that delegates to it.
5. Regenerate **`AGENTS.md`** / **`content/built/`** after edits.

---

## Reference

- **Worked example:** **`parts/process.md`** in **abd-skill-builder**.
- **Rich pipeline doc:** **`templates/process-team.md.template`** (team process plate).
- **Workspace normative body:** **`parts/phases/workspace-and-config.md`**.


---

### `delivery-modes.md`

# Agent delivery modes (static build vs runtime injection)

Skills can hand instructions to an **agent** or **executor** (including an EA / orchestrator) in two ways. **Do not mix them in one session without an explicit choice** — same requirement as §3.3 *Assembly model* in [`skill-standards-section-3.md`](skill-standards-section-3.md) (static vs dynamic).

## `AGENTS.md` — always (skill-wide orientation)

**`AGENTS.md`** is the **assembled agent bundle**: how the skill is structured, how phases/steps relate, and how to work with it in general. It should be **assembled for every skill** (typically generated by **`scripts/build.py`**), regardless of **`delivery.mode`**. It is *not* what the mode flag switches on or off.

**What `delivery.mode` actually changes** is how a **single operation** (or phase/step run) gets its **process slice**: either from **pre-generated built output** or from **runtime injection** of sources — see below.

## Flag (system-wide convention)

Declare the mode in **`skill-config.json`** so tools, CI, and humans agree:

```json
"delivery": {
  "mode": "static_built"
}
```

| `delivery.mode` | Meaning |
| --- | --- |
| **`static_built`** | **Default.** When you **run an operation**, the executor uses **process content that has already been merged into `content/built/`** (and similar per-skill layouts): each slice includes the **process part** plus its **library** and **rules** components as produced by the build. **`AGENTS.md`** is still checked in as the skill-wide bundle; **built** trees are the canonical **operation-time** artifacts. Operators run **`python scripts/build.py`** after changing sources; commits include regenerated files. |
| **`runtime_injection`** | When you **run an operation**, the executor **injects** the **process part** and, in documented order, **all** of its **library** and **rules** components from source paths — **without** requiring that slice to exist as a pre-built file under **`content/built/`**. **`AGENTS.md`** is still assembled for orientation; only the **operation-time** merge strategy differs. |

**Default for new skills:** `static_built`. Use **`runtime_injection`** when you want runtime resolution; use **`static_built`** when you want checked-in slices — **both** require the same **documented injection map** (see below).

## Injection map — document regardless of mode

**`delivery.mode` does not decide whether you document injection.** It only decides **pre-generate** (build + commit **`content/built/`**) vs **inject at run time** after each operation. In **both** cases:

1. **Which** source paths (process slice, **`library/`**, **`rules/`**, …) apply **per operation** (phase/step).
2. **In what order** they are merged / concatenated / injected.
3. **How** that matches the **static** merge (same semantics as **`build.py`**, or **deliberate differences** called out).

Keep this in a **single lookup** place — e.g. skill **`README.md`**, a manifest in **`build.py`**, or a **generated manifest** checked in next to **`built/`** — so someone can **change `delivery.mode` later** without re-deriving paths from scattered files. The only thing that changes is **when** material is materialized (build vs runtime), not **what** the skill is allowed to omit from documentation.

## Mode (a) — `static_built`

- **What is delivered:** Generated markdown under **`content/built/`** (and/or `phases/built/`, `content/parts/steps/built/` per skill layout) plus the top-level **`AGENTS.md`** when the build emits it.
- **Operation-time behavior:** Use the **built** slices (process + library + rules already merged for that slice).
- **When it applies:** CI, reviewable diffs, reproducible runs, “what the agent saw” is literally in git.
- **Operator obligation:** After editing **`content/parts/`**, **`rules/`**, or merge inputs, run **`build.py`** and commit outputs.

## Mode (b) — `runtime_injection`

- **What is delivered:** For **operations**, not a single pre-expanded tree under **`built/`**; the **executor** resolves **phase** (or step) → **files** (`rules/…`, `content/parts/library/…`, process slice, etc.) and **injects** them into context in a documented order (full **process part + library + rules** for that operation).
- **`AGENTS.md`:** Still assembled so the agent understands the skill in general; only **per-operation** content is resolved at runtime.
- **When it applies:** Interactive orchestration, rapid iteration without running the full static pipeline each time, or environments where checking in large built blobs is undesirable (still document the tradeoff).
- **Operator / implementer obligation:** Same as **static** mode for the **injection map** — resolution order, equivalence vs static merge, validation — **not** optional just because execution is dynamic. Runtime mode adds: executor must follow the **same** documented map (or list exceptions).

## Staying in sync between modes

1. **Single source of truth** for *meaning* stays in **unbuilt** inputs: **`content/parts/`**, **`rules/`**, **`docs/`** (reference), not in hand-edited **`AGENTS.md`** when a build owns the merge.
2. **`static_built`** outputs are **derivatives**: regenerating must be repeatable from the same inputs + **`scripts/build.py`** (and any merge manifest the skill defines).
3. **`runtime_injection`** must **not drift silently**: if both modes are supported, the skill should state whether runtime is a *shortcut to the same merge* (ideal) or a *lighter subset* (then list gaps).
4. **Changing sources:** Under **`static_built`**, CI or pre-commit should run **`build.py`** and fail if **`content/built/`** / **`AGENTS.md`** are stale (exact hook is repo-specific).
5. **Switching modes:** The **injection map** (paths + order + equivalence) is what lets you move from **`static_built`** to **`runtime_injection`** or back — update **`delivery.mode`** and keep the **same** map unless you intentionally change behavior.

## Relation to `build.py` flags

Per §3.3, a skill may expose **`--assembly static|dynamic`** (or equivalent) **inside** `build.py` for *how* static snapshots are produced. That is **orthogonal** to **`delivery.mode`**: `delivery.mode` answers whether the **operator/agent relies on checked-in built files** vs **runtime resolution**. A skill can use `runtime_injection` at execution time while still using `build.py --assembly static` to produce reference snapshots for tests.


---

### `process-approach.md`

# Process approach — IDE, `process.md`, code phases vs AI-chat phases

**Audience:** Authors and tooling. This is the **default mental model** for how a skill is **used** (Cursor, VS Code, Claude Desktop, similar) and how **phases** are executed.

## Who consumes what


| Artifact                                                               | Who uses it                                     | How                                                                                                                                                                                                                                                                                                                      |
| ---------------------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `**AGENTS.md`** (skill root)                                           | **IDE / assistant**                             | Loaded **automatically** by many tools as context for the repo. It orients the model: pipeline, links, where `process.md` lives. **No one “opens `built/` by hand” as the primary workflow** — the chat does not browse the tree to find instructions; **you tell it what to do** using `**process.md`** and phase docs. |
| `**content/parts/process.md**` (or `pieces/process.md` in some skills) | **Human + chat**                                | **Map of phases**: table rows are **phases**, **Ref** links to phase files. The skill should tell users to **read / `@`-reference** this file to know **how to execute** a given phase (order, actor, script). Example pattern: `@agilebydesign-skills/skills/<skill-id>/content/parts/process.md`.                      |
| **Built phase text** (`phases/built/`, `content/built/`, …)            | **Build pipeline + optional `generate_prompt`** | **Generated** outputs — **not** “what autonomous agents read first.” They exist so you can **materialize** a full instruction block for an AI phase (static mode) or **diff in git** under `static_built` delivery.                                                                                                      |


## Phase kinds (two execution styles)

### 1. Code-driven phases (human or CI runs the script)

- **You run** the Python/shell entry point **normally** (terminal, task, CI).
- **Await** exit code and artifacts the phase defines.
- The **phase markdown** (source) describes **how to invoke** the script, **arguments**, **outputs**, and **what “done” means** — not a prompt to paste unless the phase is hybrid.

### 2. AI-chat–driven phases (instructions for the model)

- The **instruction body** the chat must follow is produced by **prompt generation** — short name: **generate prompt** (implementation often `scripts/generate_prompt.py` per skill; names may vary).
- **CLI shape (contract):** support a **phase selector**, e.g. `python scripts/generate_prompt.py --phase <phase_slug>` (some teams use `phase:<name>` as a single token; equivalent intent).
- **Two modes** (both end with “text the user pastes or tool injects into chat”):


| Mode        | What it does                                                                                                                                                                                                                                                            | When to use                                                                |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Dynamic** | Builds one **string** by **collecting every section** required for that phase (source phase markdown, `library/` fragments, applicable `rules/`, manifest order in `skill-config.json` / `build.py`).                                                                   | Fast iteration; single source of truth; no checked-in blob for that phase. |
| **Static**  | Uses **pre-generated** phase text already written under the skill’s **built tree** (convention: `content/parts/phases/built/<phase_slug>.md` or `phases/built/<phase_slug>.md` — **document the path in the skill**). **Grab the whole file** as the instruction block. | Reproducible snapshots, CI, “exactly what shipped last release.”           |


In **either** mode, the **outcome** is: **the IDE chat has the right block of instructions** to follow for that phase — not “the agent navigates to `built/` like a filesystem API.”

### Default `phase_bundle` order (`skill-config.json`)

**abd-skill-builder** `Instructions` (used by `scripts/generate_prompt.py` and typical `scripts/build.py` merges) follows **`phase_bundle.order`** — an array of section tokens — unless `operation_sections` overrides the slug. **Default in this repo and scaffold template:** **`["principles", "role", "phase", "library", "rules"]`** so **`critical-quality-steps.md`** ( **`## Principles`** ) leads every AI-chat bundle. Other skills may reorder (e.g. **`principles`** last) or omit tokens; missing optional files (**`role`**, **`principles`**) are skipped.

Section tokens (each included only if listed in **`order`**):

- **`principles`** — optional: file under `content/parts/library/` (default `critical-quality-steps.md`), heading **`principles_heading`**. **Omitted** if the file is missing.
- **`role`** — optional: file under `content/parts/` (default basename `solution-analyst-role.md`). **Omitted** if the file is missing.
- **`phase`** — `content/parts/phases/<slug>.md` (or `parts/phases/`), with heading **`## Phase`** when `phase_bundle.phase_heading` is set.
- **`library`** — shards from **`PHASE_LIBRARY_SLICES`** for that slug, or all of **`library_files`** when the slice is absent; one **`## Library`** heading, then **`### \`file.md\``** per shard (with `abd:begin` / `abd:end` filtering). **Empty slice** → placeholder body under **`## Library`**.
- **`rules`** — **normative:** governance markdown inlined from **`rules/<stem>.md`** in manifest order. Stems come only from **`skill-config.json`**:
   - **`every_phase_rules`** — array of stems (no `.md`) prepended for **every** phase, **deduplicated** in order (listed once even if also under a phase).
   - **`phase_rules`** — object: keys are **phase slugs** (same strings as **`phase_files`**); values are ordered arrays of stems. Example: `"shaped-story-map": ["evidence-citations-required", "shaped-story-shape"]`.
   **No stems** for a phase → placeholder body under **`## Rules`** (points authors to this doc). Rule files may keep optional YAML frontmatter (e.g. **`rule_id:`**); **`Instructions`** strips it before inlining so bundles stay readable. **Do not** use per-rule **`phase_files:`** frontmatter as the source of truth for which phase gets which rule — that duplicates the manifest and drifts; **abd-maps-models-specs** and **abd-skill-builder** both standardize on **`phase_rules` / `every_phase_rules`**.

Configure (or copy defaults) via **`phase_bundle`** in **`skill-config.json`**: keys include **`order`**, **`role_file`**, **`principles_file`**, and optional **`role_heading`**, **`phase_heading`**, **`library_heading`**, **`rules_heading`**, **`principles_heading`**. **abd-skill-builder** ships the full default object so scaffolded skills inherit the same contract; **abd-maps-models-specs** uses **`MapsInstructions`**, which follows the same **`phase_rules` / `every_phase_rules`** contract (plus maps-only critical-quality notes).

### Library shards with phase markers (`abd:begin` / `abd:end`)

A **`library/*.md`** file may wrap fragments in **`<!-- abd:begin <phase-slug> -->`** … **`<!-- abd:end <phase-slug> -->`** (same slug on both lines). When **`Instructions.assemble_prompt(<phase-slug>)`** runs (used by **`generate_prompt.py`** and **`build.py`** for **`phases/built/<slug>.md`**), the reader sees **all lines outside** those pairs **plus** only the **pair whose slug matches** the current phase. Slugs match **`phase_files`** in **`skill-config.json`** (e.g. **`plan-script-build`**). Files **without** markers are included in full whenever **`PHASE_LIBRARY_SLICES`** lists them for that phase. Authoring template: **`templates/concepts.md.template`**.

## What `build.py` is for

- `**scripts/build.py`** merges **process + library + phases (+ rules where applicable)** into `**AGENTS.md`** and any `**content/built/**` slices per `**delivery.mode**`.
- It is the **authoritative** driver for **this** skill repo. `**generate_prompt`** is **orthogonal**: it answers “what text do I put in chat **for this AI phase**?” while `**build.py`** answers “what ships in **AGENTS.md** / static bundles?”

## Relation to §3

- **Stages / phases / steps** table semantics: `[skill-standards-section-3.md](skill-standards-section-3.md)`.
- **Rule file naming, assembly flags:** same §3 doc.
- **Delivery modes (`static_built` vs `runtime_injection`):** `[delivery-modes.md](delivery-modes.md)`.

## Team process plate (rich `process.md`)

For skills that need the same **shape** as **abd-maps-models-specs** — **outcome**, **principles**, **inputs / outputs**, **stages**, and a **wide phase table** (Description, Actor, Input, Output, Scripts) — start from the **team template**:

- **`content/parts/templates/process-team.md.template`** (in **abd-skill-builder**)
- **`content/parts/templates/README.md`** — how it relates to scaffold’s minimal **`templates/process.md.template`**

Copy the plate into **your** skill as **`content/parts/process.md`**, replace `{{skill_name}}`, add phases and **Ref** links, then run **`python scripts/build.py`**. The **abd-skill-builder** **`process.md`** demonstrates the same structure at production quality.

## Extending a new skill

1. Add `**content/parts/process.md`** with phase rows and **Ref**s (or start from **`process-team.md.template`** above).
2. For each **code phase**, document script + I/O in the phase file.
3. For each **AI-chat phase**, either wire `**generate_prompt`** (dynamic/static) or document a manual copy-paste path until scripted.
4. Run `**python scripts/build.py**` so `**AGENTS.md**` stays the IDE-facing bundle.
5. Keep `**process-approach.md**` behaviors in `**README.md**` in one paragraph so consumers know how your skill expects IDE + chat to work.


---

### `authoring-checklist.md`

# Skill authoring checklist (human + AI)

**Purpose:** Trackable **`- [ ]` / `- [x]`** tasks for building or evolving a skill. **Workspace convention:** keep this content in **`docs/skill-plan.md`** under the **## Authoring checklist** section (one document with the plan). **Scaffold** injects this file there; by hand, paste from here. If you stop mid-work, the next session continues from the **first unchecked** box in that section.

**Canonical source:** `skills/abd-skill-builder/content/parts/library/authoring-checklist.md` — merge updates from here when standards change.

| Role | What to do |
|------|------------|
| **A — Ask** | Use the **Ask:** lines under each section when you need input. |
| **B — Answer / suggest** | As **AI**, fill proposals; human confirms. |
| **C — Track** | Turn `- [ ]` into `- [x]` only when the item is **done**. |

**Normative layout/operator rules** stay in **`skill-repo-standards.md`** and **`skill-standards-section-3.md`** (under **`content/parts/library/`** in **abd-skill-builder**). **How the IDE uses the skill** (AGENTS.md, `process.md`, code vs AI-chat phases, `generate_prompt`): **`process-approach.md`**.

**Runtime vs `docs/`:** All markdown (and other content) that **pertains to how the skill is used at operation time** — merged or injected by **`build.py`**, read as phase bodies, or otherwise part of the **runnable** package — lives under **`content/parts/`** (and **`library/`**, **`rules/`**, etc. per norms). **`docs/`** is **only** for **non-runtime** material: user manuals, **skill plans** (including the checklist section), architecture, standards deltas. **Do not** stash mergeable instruction content in **`docs/`**. (**abd-skill-builder** itself only keeps **`docs/standards-delta.md`**.)

---

## Before you start (every session)

- [ ] **Working copy:** **`docs/skill-plan.md`** includes an **## Authoring checklist** section (scaffold injects this file there; by hand, paste from **`library/authoring-checklist.md`** into that section).
- [ ] **Resume:** Find the **first unchecked** `- [ ]` in the checklist section and continue from there.
- [ ] **Optional:** Note the date and “stopped at §…” in **Gaps / follow-ups** at the bottom when pausing.
- [ ] **`docs/` vs `content/parts/`:** No **runtime** markdown under **`docs/`** — phases, library bodies, and anything **`build.py`** merges/injects stay in **`parts/`**. **`docs/`** = manuals, **skill plan** (with checklist section), architecture, migration notes only.

---

## Greenfield vs existing skill

- [ ] **New skill:** Ran **`scaffold_skill.py`** (or equivalent) so the base tree exists.
- [ ] **Existing skill:** Ran **[plan-migrate.md](../phases/plan-migrate.md)** (**1b**: inventory + **standards-delta** + user chose **IDs**), then **[migrate.md](../phases/migrate.md)** (**2b**: execute moves) **before** bulk edits — **or** consciously skipped with a note in **Gaps / follow-ups**.

---

## Skill identity (what this skill does — not delta to other work)

Normative row: **Documentation focus** in **`skill-repo-standards.md`**.

- [ ] **Process, rules, and docs** describe **what this skill does** and how to run it — **this package**, on its own terms.
- [ ] They do **not** rely on “vs another skill” or “we don’t do X because Y” — that stays out of durable spec.
- [ ] **Dependencies** (other skills, repos, tools, versions) recorded explicitly (**Dependencies** / `README` / `conf/build-strategy.json`) — separate from the main narrative.

**AI should:** Strip migration chatter; put relationships in a **Dependencies** list.

**Ask:** “If this skill vanished, could someone run it from **this repo alone**?”

---

## Base scaffold: what you copy and extend

**Source:** **`skills/abd-skill-builder/scripts/scaffold_skill.py`** + **`skills/abd-skill-builder/templates/*`** — extend these files; don’t invent a parallel layout.

### Scaffold files present and reviewed (check each)

- [ ] **`SKILL.md`** — frontmatter + description make sense.
- [ ] **`skill-config.json`** — `operator.*`, `delivery.mode` match intent; if **`rules/*.md`** back AI-chat phases, **`phase_rules`** / **`every_phase_rules`** list every rule stem for the right **phase slug** (**[`process-approach.md`](process-approach.md)** — *rules* in the default **`phase_bundle`**).
- [ ] **`conf/build-strategy.json`** — `skill_purpose` and siblings filled per Strategizer.
- [ ] **`conf/abd-config.json`** — **`active_skill_workspace`** set (under **`test/`** when using a workspace); optional CLI: **`python scripts/set_workspace.py <path>`**.
- [ ] **`scripts/set_workspace.py`** — present (scaffold copies from **abd-skill-builder**).
- [ ] **`conf/README.md`** — conf usage clear.
- [ ] **`content/parts/process.md`** — pipeline table matches real phases.
- [ ] **`content/parts/phases/`** — one file per row in **`process.md`** (add/rename beyond **`author.md`** as needed).
- [ ] **`content/parts/phases/built/`** — present when you use **static** AI-chat prompts; populate via **`build.py`**; see **`process-approach.md`**.
- [ ] **`scripts/generate_prompt.py`** — present for AI-chat phases; **`--mode dynamic`** vs **`static`** documented; extend per skill.
- [ ] **`scripts/build.py`** — merge/injection driver present (see non-negotiables below).
- [ ] **`scripts/scanner_smoke.py`** — replaced or supplemented with real scanners if needed.
- [ ] **`rules/README.md`** + **`rules/scanners.json`** — wired when rules exist.
- [ ] **`test/README.md`** — explains layout; workspace path if used.
- [ ] **`content/parts/library/`** — created when cross-cutting chunks exist; wired in **`build.py`** (e.g. **`PHASE_LIBRARY`**) per §3.

### Non-negotiables

- [ ] **`scripts/build.py`** is the **merge / injection driver** (writes at least **`AGENTS.md`** from process + phases).
- [ ] **`process.md`** order matches **`phases/`** and **`build.py`** (if order ≠ lexicographic sort of filenames, **`build.py`** uses an **explicit ordered list**, not **`sorted(glob)`**).
- [ ] **Process → operation injection** documented in/near **`build.py`** + human-readable place for §4.

### Reference templates read (when extending)

- [ ] Read **`abd-skill-builder/parts/library/process-table-standards.md`** — process **`#`**, **Phase**, **Description**, **Actor**, **Input**, **Output**, **Scripts**; **workspace** phase (**Phase 0**) required.
- [ ] Opened **`abd-skill-builder/templates/child_build.py.template`** (minimal merge).
- [ ] If per-operation bundles / library injection: reviewed **`abd-maps-models-specs/scripts/build.py`** (`PHASE_FILES`, `PHASE_LIBRARY`, built phases).

### Extension work (after §§0–4 answers)

- [ ] **One** **`build.py`** — no second hidden merge pipeline.
- [ ] **`process.md`**, **`phases/*.md`**, **`build.py`** updated **together** when adding/changing a phase.
- [ ] **`content/parts/library/`** chunks added and wired in **`build.py`** where needed.
- [ ] **Injection map** in **`build.py` docstring** and/or skill **`README.md`** (aligns with §4).
- [ ] **`python scripts/build.py`** run after structural edits; **`AGENTS.md`** / **`content/built/`** committed if **`static_built`**.

**Ask:** “Which files do we **edit** vs **add**? Where is the **ordered phase list** in **`build.py`**?”

---

## 0. Build intent (`conf/build-strategy.json`)

- [ ] **`conf/build-strategy.json`** complete per **`agentic-skill-builder`** (template + Strategizer).

**Ask:** “What must this skill accomplish end-to-end? Who runs it? What is out of scope?”

---

## 1. Process & phases

- [ ] **`parts/process.md`** (or **`content/parts/process.md`**) lists the real pipeline (ordered phases) and follows **[`process-table-standards.md`](process-table-standards.md)** — column meanings, **Input**/**Output** semantics, **Scripts** cell.
- [ ] **Workspace phase (Phase 0):** **`parts/phases/workspace-and-config.md`** exists; **`conf/abd-config.json`** + **`active_skill_workspace`** documented; first process row uses **`0`** in **`#`** and the phase name **Workspace and config** (see standards doc).
- [ ] Phase files use **descriptive slugs**; order matches **`process.md`** and **`build.py`** (explicit order if not sort order).
- [ ] **`build.py`** phase list / merge keys updated when **`process.md`** changes.
- [ ] **Phase vs library:** Each **`phases/<slug>.md`** is **procedure** for that phase (steps, scripts, checklists)—**not** a dump of cross-phase definitions (**[`documentation-standards.md`](documentation-standards.md)** → *Library vs phase documents*; **[`rules/content-placement.md`](../../rules/content-placement.md)**).

**Ask:** “Phases in order?”

---

## 2. Rules (optional) & scanners

- [ ] Decided if **`rules/`** is needed.
- [ ] Listed planned **`rules/*.md`** files (one concern per file where possible).
- [ ] Decided scanner vs doc-only for each rule cluster.
- [ ] **Base framework** (when checks exist): read **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** — **`rules/scanners.json`** **`rule_scanner_bindings`** for each machine-checked rule; **`skill-config.json`** **`operator.build_pipeline`** lists ordered post-merge steps for **`build.py`**; **`operator.scanners`** lists the same scanner paths (or a superset) for **Operator** / CI.
- [ ] **`process.md`** does **not** treat scanners as phase-local “script column” noise; skill-level **Rules and automated checks** (or link to **`rules-and-automated-checks.md`**) instead.

**Ask:** “Machine-checked vs human-reviewed? What would each scanner inspect?”

---

## 3. Library — cross-cutting concepts (`content/parts/library/`)

- [ ] Cross-cutting content in **`library/<slug>.md`** (or skill-specific equivalent).
- [ ] **`build.py`** merge order matches how phases reuse library.
- [ ] Optional **index** (short links only: **`README`**, **`conf/build-strategy.json` notes**, or a **`docs/*` index** if non-runtime) — **not** a second home for bodies; full cross-cutting copy stays in **`library/`** (see **`docs/` vs parts** in **`skill-repo-standards.md`**).
- [ ] Same concept **names** across phases.
- [ ] **Library stays non-procedural:** **no** numbered “how to run a phase” sequences, **no** phase ordering story, **no** phase-specific **`python scripts/…`** runbooks—those stay in **`phases/`** and **`process.md`** (**[`rules/content-placement.md`](../../rules/content-placement.md)**).

**Ask:** “What repeats across phases → **library**?”

---

## 4. Agent delivery mode (`skill-config.json` → `delivery.mode`)

See **`abd-skill-builder`** [`delivery-modes.md`](content/parts/library/delivery-modes.md) (canonical: `skills/abd-skill-builder/content/parts/library/delivery-modes.md`).

- [ ] **`AGENTS.md`** assembled (both modes).
- [ ] **Injection / merge map** documented (paths per operation, order, equivalence to static) — **`README`**, **`build.py`**, or manifest — so mode can change later (narrative-only; sources remain under **`content/parts/`**).
- [ ] **`delivery.mode`** set: **`static_built`** or **`runtime_injection`**.
- [ ] If **`static_built`**: **`build.py`** run; **`content/built/`** (and peers) committed; traceable to map.
- [ ] If **`runtime_injection`**: runtime follows documented map (or deltas documented).

**Ask:** “Per operation: which files, which order, where is the lookup?”

---

## 5. `test/` — script tests & fixtures

- [ ] Chose: pytest **yes** or **no** (if no, skip pytest bullets; may still use **`test/`** for fixtures).
- [ ] If pytest **yes**: dev deps + **`pip install`** documented (**`requirements-dev.txt`** or **`pyproject.toml`**).
- [ ] **Run command** documented (e.g. **`python -m pytest test/`**).
- [ ] **CI** runs tests (optional).
- [ ] Tests live under **`test/`**; **`test/fixture/`** if needed.
- [ ] **`active_skill_workspace`** path under **`test/<name>/`** documented if set.

**Ask:** “What must stay green? Best fixture?”

---

## 6. Operator contract — “built the skill”

- [ ] **`SKILL.md`** + frontmatter.
- [ ] **`skill-config.json`** paths match disk.
- [ ] **`python scripts/build.py`** exits **0**.
- [ ] **Python compile check** on **`operator.compileall_paths`** passes (Operator uses Python’s **`compileall`** under the hood).
- [ ] **Scanner** scripts exit **0** (if any).

**Ask:** “Operator green?”

**Final:**

- [ ] **Attest** structurally built — **or** list gaps below.

---

## Gaps / follow-ups (free text)

Use for **resume notes** (date, last § completed, blockers):

```text


```

---

## How to use this file

1. **Ensure** **`docs/skill-plan.md`** has an **## Authoring checklist** section (scaffold injects from **`abd-skill-builder`** **`content/parts/library/authoring-checklist.md`**) before deep work.
2. Check **`- [x]`** only when done; **first unchecked** = resume point.
3. Pull updates from **`abd-skill-builder`** canonical copy when standards change.


---

### `skill-repo-standards.md`

# Skill repository standards (index + extras)

**Process approach (IDE, `process.md`, code vs AI phases, `generate_prompt`):** [`process-approach.md`](process-approach.md) — **start here** for how skills are **used** in Cursor / similar: **`AGENTS.md`** auto-loaded, **`@…/process.md`** for phase map, **code phases** vs **AI-chat phases**, **dynamic vs static** prompt generation.

**Full normative §3 (all subsections):** [`skill-standards-section-3.md`](skill-standards-section-3.md) — directory and content conventions (**§3.1**), rule naming (**§3.2**), assembly (**§3.3**), reference notes (**§3.4**): stages/phases/steps, process tables, optional domain+story-map pattern, `AGENTS.md` / `content/built/`.

**Rules + scanners + build pipeline (base framework):** [`rules-and-automated-checks.md`](rules-and-automated-checks.md) — **default** wiring: **`rules/scanners.json`** bindings, **`operator.build_pipeline`** for **`build.py`**, **`operator.scanners`** for Operator; **do not** hang scanners off individual **process** phases.

**Builder vs Operator (summary):** [`builder-vs-operator.md`](builder-vs-operator.md) — **scaffold / generation** path vs **`operator.run_operator()`** validation today.

**Authoring checklist (human + AI):** [`authoring-checklist.md`](authoring-checklist.md) — normative body merged into **AGENTS.md**; in each skill, work the **## Authoring checklist** section inside **`docs/skill-plan.md`** (scaffold injects this file there). **`- [ ]` / `- [x]`** so work can **resume after interruption** (first unchecked box = continue here). Covers scaffold verification, rules/scanners, **library**, **`delivery.mode`**, **`test/`**, operator.

**Migrating an existing skill:** [`../phases/plan-migrate.md`](../phases/plan-migrate.md) (**1b**) — inventory → compare to standards → **delta report** → **user chooses which gap IDs to fix**; then [`../phases/migrate.md`](../phases/migrate.md) (**2b**) — **execute** moves and patches for those IDs only (no silent full rewrites).

**Example delta (this repo):** [`../../docs/standards-delta.md`](../../docs/standards-delta.md) — `abd-skill-builder` inventory vs §3 (delivery, `content/built/`, docs, tests/fixture notes).

---

## Quick layout reminder (before reading the full §3)

| Area | Convention |
|------|------------|
| **Entry** | `SKILL.md` at skill root (frontmatter: `name`, `description`). |
| **Operator config** | `skill-config.json` — `operator.compileall_paths`, `operator.build_script`, **`operator.build_pipeline`** (post-merge steps for **`build.py`**), **`operator.scanners`** (Operator; align paths with rule-bound scanners). See **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**. |
| **Agent delivery** | `skill-config.json` — `delivery.mode`: **`static_built`** (pre-generate per-operation slices into **`content/built/`**) or **`runtime_injection`** (resolve the **same** sources at run time). **Only** that choice differs — always document **which paths** feed each operation, **merge order**, and **equivalence** to static output, in a **lookup** place (skill **`README.md`**, **`build.py`** manifest, or emitted manifest) so the team can switch modes later. **`AGENTS.md`** in **both** modes. See **`abd-skill-builder`** [`delivery-modes.md`](delivery-modes.md) (canonical: **`content/parts/library/delivery-modes.md`**). |
| **Authoring prose (normative for writers)** | [`documentation-standards.md`](documentation-standards.md) — voice, where content belongs, process tables; complements **`docs/` vs `content/parts/`** rule. |
| **Workspace routing** | **[workspace-and-config](../phases/workspace-and-config.md#skill-path-skill-workspace-and-configuration)** — **`skill_path`**, **`skill_workspace`**, **`conf/abd-config.json`** keys (**Workspace and config**). |
| **Build intent** | `conf/build-strategy.json` — strategize loads this **whole JSON**; **`skill_purpose`** must be non-empty for **`strategy_complete`** (minimum to finish strategize). Other keys are **siblings** that enrich **`strategy`** / **`builder_manifest`** — they are **not** part of the **`skill_purpose`** text. See **`agentic-skill-builder/README.md`** (Strategizer). |
| **Normative content** | `content/parts/` — process table rows are **phases**; **steps** inside phase files. Phase markdown files use **descriptive slugs** (`terms-mechanisms.md`, …) — **not** `phase-NN-…` or phase numbers in **H1** titles; pipeline order is **only** in `process.md` (# column) + `build.py` merge list (see **`skill-standards-section-3.md`**). **Column definitions** and required **workspace** row: **`process-table-standards.md`**. |
| **docs/ (non-runtime only)** | **`docs/`** is for material **not** consumed as merged/injected skill payload at operation time: **user manuals**, **migration/planning notes**, **architecture**, **`docs/skill-plan.md`** (plan + **Authoring checklist** section), **standards deltas**. In **abd-skill-builder**, **`docs/`** is only **`standards-delta.md`** — delivery merge order lives in **`README.md`**. **Do not** put markdown (or other assets) in **`docs/`** that **`build.py` merges**, **injects**, or **ships** as the runnable instruction body for phases/operations — that belongs under **`content/parts/`** (including **`library/`**, **`phases/`**, **`process.md`**, **`rules/`** as applicable). |
| **Library** | `content/parts/library/` — **cross-cutting meaning** reused across more than one phase: definitions, tables, glossaries, named concepts, artifact shapes. **Not** phase procedures, **not** step-by-step runbooks, **not** CLI blocks for a single phase, **not** pipeline order (that is **`process.md`** + **`phases/`**). The library **is** the home for that shared meaning; do not maintain a parallel “cross-cutting” layer elsewhere. **`docs/`** may hold a **short index** pointing into **`library/`**; **bodies** live in **`library/`**; merge order lives in **`build.py`**. See **`documentation-standards.md`** → *Library vs phase documents*. |
| **Phases** | `content/parts/phases/<slug>.md` — **person-to-process** instructions for **one** process-table row: I/O, **steps**, scripts, done criteria. **Link** to **`library/`** for deep definitions; avoid duplicating large normative blocks that belong in **`library/`** because multiple phases need them. |
| **Rules** | `rules/*.md` or `content/parts/rules/*.md`; optional `rules/scanners.json`. |
| **Scripts** | `scripts/build.py` (**required** — merge/injection driver; scaffold template is minimal; extend with explicit phase order + per-operation bundles as in **`abd-maps-models-specs`** when needed), scanners, optional `_config.py`. See **`authoring-checklist.md`** → *Base scaffold*. |
| **Tests & fixtures** | **`test/`** — all automated tests for the skill (pytest, smoke scripts, etc.) that exercise **`scripts/`**; optional **`test/fixture/<scenario>/`** for frozen inputs/snapshots; optional **`test/<workspace>/`** dirs when **`conf/abd-config.json`** uses **`active_skill_workspace`** (path relative to skill root). Example: **`abd-maps-models-specs/test/`** — workspace **`test/sample-workspace`**, optional fixture **`test/fixture/<scenario>/`**. **`abd-skill-builder`** itself **does include** **`test/`** (see **`test/README.md`** + **`test/fixture/toy-polite-dialogue/`**) even though **pytest `test_*.py` files** are still optional follow-ups — do not read “pytest wiring pending” as “no **`test/`** folder.” **Operator today** only runs a **Python compile check** on **`operator.compileall_paths`** (usually **`["scripts"]`**; implemented with **`compileall`**) — it does **not** install or run **pytest**. If automated tests are **in scope**, add the **wiring** below. |
| **Agent bundle (always)** | `AGENTS.md` — assembled agent bundle (skill-wide “how it works”); typically generated by `build.py`; **not** gated on `delivery.mode`. |
| **Built slices (operation-time, static mode)** | `content/built/` — pre-merged process + library + rules per skill layout when `delivery.mode` is **`static_built`**. |
| **Documentation focus (this skill only)** | Process plans, **rules**, and **docs** describe **what this skill does** — in positive, runnable terms for **this** package. **Do not** use them as a running commentary on how this skill **differs** from another skill, or why it **doesn’t** do something “because another skill does.” That is **local context in time**, not part of the durable skill. **Dependencies** (other skills, tools, repos, contracts) are **explicit** — names, links, versions — in a **Dependencies** section, `README`, or build-strategy notes. That is **not** the same as narrating deltas to sibling work. |

**Minimal valid skill:** `SKILL.md` + `scripts/build.py` + `skill-config.json` with operator block — see **`test/fixture/toy-polite-dialogue/`** in this skill (**`abd-skill-builder`**).

---

## When automated tests are asked for (pytest wiring)

If the skill should run **pytest** (or similar) under **`test/`**, do **not** assume it is already installed or wired into **`operator`** — add it explicitly:

| Step | What to do |
|------|------------|
| **Dependency** | Add **`pytest`** (and dev-only plugins if needed) to a **`requirements-dev.txt`**, **`pyproject.toml`** `[project.optional-dependencies] dev`, or the skill’s documented venv install step — **commit** the file so others can `pip install -r …`. |
| **Layout** | Tests live under **`test/`** (e.g. **`test/test_*.py`** or **`test/<suite>/`**); shared fixtures in **`test/fixture/`** or **`conftest.py`** as usual for pytest. |
| **Run command** | Document in skill **`README.md`** or **`test/README.md`**: e.g. `python -m pytest test/` from skill root (with venv activated). |
| **CI (optional)** | Add a workflow or monorepo job that installs dev deps and runs the same command. |
| **Operator** | **`operator.run_operator()`** does **not** run pytest by default. To gate releases on tests, extend **CI** or a **wrapper script**; only add **`test`** to **`compileall_paths`** if you intentionally want bytecode checks on test modules (unusual). |

---

## Operator checklist (machine-runnable)

1. `SKILL.md` present.
2. `skill-config.json` parses; `operator` block consistent with files on disk.
3. Python files on declared paths pass a **compile check** (Operator uses **`compileall`**).
4. `python scripts/build.py` exits 0.
5. Each listed **scanner** in **`operator.scanners`** exits **0** (and any step in **`operator.build_pipeline`** that **`build.py`** runs also exits **0** when you rely on **`build.py`** as the full local gate).
6. **`rule_scanner_bindings`** (in **`rules/scanners.json`** when used): each **`rule_file`** and **`scanner`** path exists.

---

## What greenfield scaffold should emit

**`scripts/scaffold_skill.py`** (and equivalent generators) should produce a **complete, runnable skeleton**: file tree, `skill-config.json`, phase markdown stubs, `rules/` / `conf/` as needed, runnable **`build.py`**, optional scanner stubs — **without** baking in customer-specific “gold” domain solutions (those belong in the target workspace, not the template).

This **`abd-skill-builder`** skill ships **templates + `scaffold_skill.py`** as the supported way to create that tree. **`operator.run_operator()`** then validates what is on disk; it does not scaffold new skills by itself.


---

### `skill-standards-section-3.md`

# §3 Skill package layout and content standards

**What this is:** Normative rules for how a **skill repository** is shaped — where **runtime** content lives (`content/parts/`, `rules/`, `build.py`), how **stages / phases / steps** relate, how **process tables** and **Refs** work, optional patterns (e.g. domain + story map), **rule file naming**, and **static vs dynamic** assembly of instructions. **How skills are used in the IDE** (AGENTS.md, `process.md`, code vs AI-chat phases, `generate_prompt`) is defined in [`process-approach.md`](process-approach.md) — read that first.

**How to use it:** Implement **§3.1–§3.4** when authoring or reviewing a skill. Tools and humans use the same rules; nothing here depends on any external “origin” document.

**Scope boundary — skills stay simple:** A **skill package** should express a **linear** pipeline: **stage → phase → (steps inside phase docs)**. The **process table** rows are **phases**, not steps. Keep skills deliberately sequential.

## 3.1 Directory and content conventions

**Hierarchy in the repo:** **Stages** group **phases**. Each **phase** has normative markdown (one file or section per phase, per skill); **steps** live **inside** that phase’s markdown — they are **not** separate rows in the master process table. See **Stages, phases, and steps** below.


| Area                            | Convention                                                                                                        | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Normative content**           | Under /`content/parts/`                                                                                           | Plans, operations, domain narrative — **not** dumped only in chat.                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `**docs/` (non-runtime)**       | /`docs/` at skill root                                                                                            | **User manuals**, **migration/planning notes**, **architecture**, **authoring checklists**, and **narrative** descriptions of delivery. **Do not** put markdown here that `build.py` **merges**, **injects**, or **ships** as the runnable phase/operation body — that belongs under `**content/parts/`** (including `**library/`**, `**phases/`**, `**process.md**`, `**rules/**`).                                                                                                                                   |
| **Phase markdown (source)**     | e.g. /`content/parts/phases/<descriptive-slug>.md`, or one doc per phase with step sections — paths vary by skill | **One row in the process table = one phase.** **Steps** (numbered sub-procedures, “Step 1…”, checklists) are written **inside** this markdown as **normative content of the phase**, not as their own table rows. **Do not** encode execution order in filenames or H1 titles (`phase-02-foo.md`, `# Phase 2 — …`): order belongs in `**process.md`** (the `#` column) and in `**scripts/build.py`**’s explicit file list. Use **stable descriptive** kebab-case slugs so renumbering the plan does not force renames. |
| **Built phase markdown**        | `content/parts/phases/built/<descriptive-slug>.md` and/or `content/built/…` per skill layout | **Generated** from source phase bodies + rules via `scripts/build.py`. **Authors do not hand-edit `built/`.** These files are **materialized instruction blobs** for **static** AI-chat phases and for **`static_built`** delivery — consumed by **`generate_prompt`** (or pasted into chat), **not** by “agents browsing the repo” as the primary UX. IDEs load **`AGENTS.md`**; see [`process-approach.md`](process-approach.md). Folder layout (`phases/built` vs `content/built`) is per skill; document it in **`README.md`**.                                                                                                                                                                                                            |
| **Atomic rules**                | `content/parts/rules/*.md` (or top-level `rules/` in simpler skills)                                              | One concern per file where possible; **names** should encode **phase** and/or **domain concept** + rule name (see §3.2). **Which phase inlines which rule** is declared in **`skill-config.json`** (`phase_rules`, `every_phase_rules`), not scattered in per-rule frontmatter lists.                                                                                                                                                                                                                                                                                                                                                                                               |
| **Roles**                       | `roles/*-role.md`                                                                                                 | One file per **user/agent role** the skill assumes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Process**                     | `content/parts/process.md` or staged process docs                                                                 | **Summary table: each row is a phase** (linked by **Ref** to phase markdown). Stages group those rows. **Steps** appear only **inside** the linked phase files.                                                                                                                                                                                                                                                                                                                                                        |
| **Library markdown**            | `content/parts/library/*.md` (or `parts/library/`)                                                                | **Cross-phase structure and meaning**: definitions, glossaries, artifact shapes, naming, invariants. **Not** phase-local procedures, pipeline ordering, or CLI runbooks—those live in **`process.md`** / **`phases/`** (see **Library vs phase documents** below).                                                                                                                                                                                                                                                     |
| **Repo-facing built artifacts** | `AGENTS.md`, `SKILL.md`, sometimes `README.md`                                                                    | Frequently produced by `scripts/build.py` (merge order per skill). **`AGENTS.md`** is what **IDEs and assistants typically load automatically** for the skill repo.                                                                                                                                                                                                                                                                                                                                                                |
| **Config**                      | `skill-config.json`                                                                                               | Name, version, **`phase_files`**, **`PHASE_LIBRARY_SLICES`**, **`phase_rules`** / **`every_phase_rules`** (ordered rule **stems** inlined per phase bundle — see [`process-approach.md`](process-approach.md)), **`phase_bundle`**, **`operator.compileall_paths`**, **`operator.build_script`**, **`operator.build_pipeline`** (post-merge steps for **`build.py`**), **`operator.scanners`** (Operator gate; align with rule-bound scanners) — skill-specific knobs. See **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** (base framework).                                                                                                                                                                                                                                               |
| **Scripts**                     | `scripts/`                                                                                                        | Operational entry points; may share `_config.py` patterns.                                                                                                                                                                                                                                                                                                                                                                                                                                                             |


### Stages, phases, and steps (how they relate)

**Order is always:** **Stage → Phase → Step** (coarse → mid → finest) — but **only the first two appear as rows** in the master process table. **Steps** are **inside** the phase markdown.


| Term      | Typical meaning                                                                                                                                                                                                                                                                                                                      | Example                                                                                  |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **Stage** | **Coarse pipeline slice** — groups many **phases**; may span days or sessions. Often a heading or section in `process.md` or a staged doc.                                                                                                                                                                                           | **Stage 1 — Extract Context**; **Stage 2 — Map and Model**; **Stage 3 — Specification**. |
| **Phase** | **One row** in the process summary table — the unit of “what we do next” with a **driver**: **human** or **AI actor**. The **Ref** column links to **phase** markdown. Phases answer “are we allowed to proceed?” and **contain** the detailed steps as normative body copy.                                                         | “Corpus audit — Phase N”; **Initiator / Actor** column = human vs AI.                    |
| **Step**  | **Sub-structure inside the phase’s markdown** — numbered instructions, checklists, “Step 1 / Step 2”, optional **suffix letters** (`5a`, `7a`) for companion script runs **within the same phase**. **Not** a row in the process table. Machine state (if any) may still reference `workflow_step` as a **sub-id** inside the phase. | Inside `modules-epics-scaffold-breadth.md`: “1. … 2. … 3a. rebuild index …”              |


**AI-driven phases — how the operation is delivered:** See **[`process-approach.md`](process-approach.md)**. In short: **code-driven** phases = run scripts as documented in the phase file; **AI-chat** phases = produce the instruction block via **`generate_prompt`**-style tooling in **dynamic** (assemble sections) or **static** (use pre-built phase markdown under `phases/built/` or equivalent). The **chat** follows that text; **`built/`** is not “the agent’s filesystem API.”

**Ordering (linear, inside the skill):** Stages order **major outcomes**. **Phases** run in **process table order** (each row = one phase). **Steps** follow the order **written inside** each phase document. **Parallel batches, fan-out, or merge** are **not** modeled as extra table rows; if needed, handle that **outside** the skill package (host app, orchestration, or scripts). **Phases** may **block** a later stage until accepted (e.g. “the indexer phase says rebuild chunks — do not start Stage 2 until accepted”).

**“Process” one-liner:** `content/parts/process.md` (or `parts/process.md`) often opens with a **single pipeline string** (e.g. Context → Foundational spine → …). That line is the **navigation spine**; the **table lists phases** (by stage); **authoritative step detail** lives inside each **Ref**’d phase file.

### Process tables, hyperlinks, and naming in the Ref column

**How the table is built**

- **Rows are phases**, not steps. Columns typically include: `#`, **Phase** (title — sometimes labeled “Step” in legacy tables; **semantically it is the phase**), **Initiator / Actor** (Human→Code, AI, Code), **Script** (if any), **What it does**, **Coverage**, **Ref**, **Inputs**, **Outputs**.
- **Ref** is the **hyperlink hub**: each row points to the **normative markdown for that phase**. **Steps** (numbered sub-procedures) live **inside** that file — not in separate table rows. Python entry points stay in **Script**, not **Ref**.
- **Two-tier phase files:**
  - **Source:** phase markdown authors edit (e.g. `content/parts/phases/<name>.md`, or `parts/steps/<name>.md` when the filename is the **phase** slug — naming varies by skill).
  - **Built:** `content/parts/phases/built/<name>.md` or `content/built/<name>.md` — **rules baked in** from `parts/rules/*.md` via `scripts/build.py`. **Steps remain inside** the built document. Used for **static** prompt generation and **`static_built`** slices — not hand-edited. See [`process-approach.md`](process-approach.md).
- **Cross-links inside the table:** The **Ref** column uses relative markdown links to the **phase** doc, e.g. `[context](parts/context.md)`, `[modules-epics-scaffold-breadth (built)](content/parts/steps/built/modules-epics-scaffold-breadth.md)` (paths vary by skill; **from the skill root** per `AGENTS.md`).

**Naming conventions visible in the table**

- **Phase titles** in the table read like **milestones or operations** (“Parse, curate, chunk, index”, “Integrate and Harmonize”) — stable labels for **phase** / workflow fields. **Finer labels** for **steps inside the phase file** may appear in JSON as `workflow_step` or similar.
- **Phase file names and H1 headings** must **not** duplicate pipeline indices (`phase-00-`, `Phase 3 —` in the title). Those numbers **change** when the plan evolves; **brittle** names churn git history and links. The **Ref** column and `build.py` define order; phase files stay **semantically** named (`story-map.md`, `canonical-context.md`).
- **Letter suffixes** (`5a`, `7a`) describe **sub-steps inside a phase** (e.g. companion script after a numbered step) — **inside the phase markdown**, not extra table rows.

### Concepts and cross-cutting artifacts (generic — all skills)

**This section is the generic rule.** A **skill** packages **concepts** (ideas, definitions, invariants, roles) and **artifacts** (outputs, schemas, manifests) that the workflow references across **multiple stages or phases**. Anything that would be **repeated** if pasted into every phase file should instead live in **its own file** (usually markdown under `content/parts/`, sometimes JSON alongside) so there is a **single source of truth**.


| Guideline           | Meaning                                                                                                                                                                                                         |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **When to extract** | If a concept or artifact **spans** more than one phase (or stage), give it a **dedicated** doc (or structured file) and **link** from phase bodies — do not duplicate long definitions in each phase.           |
| **Naming**          | Conventional filenames (`glossary.md`, `concepts.md`, `artifacts.md`, `roles/`*, etc.) vary by skill; **discover** and **validate** presence from templates and this skill’s `build.py`, not one global layout. |
| **Not every skill** | A minimal skill might only have `SKILL.md`, `content/parts/process.md`, and phase files — **no** separate “domain” or “story map” layer. That is valid.                                                         |


### Library vs phase documents (authoring split)

**`library/`** answers **what** (stable meaning for ideas and artifacts that **more than one** phase touches). **`phases/<slug>.md`** answers **how for this step** (operator procedure: inputs, outputs, ordered steps, **commands**, done checks).

| In **`library/`** | In **`phases/`** (not a second copy of the whole library) |
| --- | --- |
| Definitions, tables, schemas, vocabulary used across phases | Purpose of **this** phase, **steps**, checklists, **script/CLI** lines |
| Single source of truth for a construct that spans the pipeline | **Links** into the right **`library/`** shard for depth |
| Optional injection slices (`abd:begin` / `abd:end`) | **No** long normative essays that other phases would repeat verbatim |

**Do not** put **numbered phase procedures**, **order-of-operations** for the skill, or **phase-to-phase sequencing narrative** in **`library/`**—that belongs in **`process.md`** and the relevant **`phases/`** files. **Do not** park **large** reusable specs only inside one phase file if another phase needs the same text—extract to **`library/`** and link.

Normative detail for writers: [`documentation-standards.md`](documentation-standards.md) and [`../../rules/content-placement.md`](../../rules/content-placement.md).

### Optional pattern — domain narrative + interaction tree (maps-models–class skills only)

Some skills (notably **abd-maps-models-specs** and similar) **choose** to separate **two parallel artifacts** that must stay in sync. **Do not** treat this table as the default for **all** skills — only for skills that explicitly adopt this shape.


| Piece                            | Role                                                                                                                                                                                                    | Typical location (example skill)                                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Domain narrative**             | **State and structure** — modules, **domain concepts** (CRC-style: owns, properties, operations, `extends`, invariants), evidence hooks. Answers **what things are** and **what owns which rules**.     | e.g. `parts/domain.md` + evolving `map-model-spec.json` (`modules_and_epics`, `concepts[]`, chunk citations). |
| **Story map / interaction tree** | **Behavior** — epics, sub-epics, stories, scenarios; **Trigger / Response**; **Pre-Condition**; **Given/When/Then** where required. Answers **who does what** and how behavior references domain state. | e.g. `parts/story-map.md` + nested JSON under epics (`stories`, `sub_epics`, etc.).                           |


**When this pattern applies**

- **Same vocabulary:** Domain concept names (`concepts[].name`) and story references can be held to **one namespace** — scanners may enforce **exact string match** where the skill defines that rule.
- **Evidence ladder / paired edits:** Concepts may carry `evidence_stage`; **domain** vs **journey** edits are **paired** in skills that implement both files.
- Skills **without** this split still use the **generic** rule above: cross-cutting concepts → **their own** markdown (whatever the skill calls them), not repeated per phase.

### Rules and automated checks (default wiring)

For **machine-enforceable** rules, use the **base framework** in **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**:

- Declare **rule → scanner** bindings in **`rules/scanners.json`** (`rule_scanner_bindings`).
- List **ordered post-merge steps** under **`skill-config.json` → `operator.build_pipeline`**; **`scripts/build.py`** runs them after merges (same pattern as **`abd-maps-models-specs`**).
- Keep **`operator.scanners`** consistent with those scripts for **`operator.run_operator()`** / CI.

**Process tables** should **not** enumerate every scanner as if it belonged to a single phase; document automation at the skill level and link **`rules/scanners.json`** + **`build.py`** / **`build_pipeline`**.

## 3.2 Rule file naming (heuristic standard)

Target pattern (flexible regex for validation):

```text
{phase-or-stage}__{domain-concept-or-scope}__{short-rule-name}.md
```

Examples mirror **story synchronizer / maps-models** style: scanners and rules tied to **phase** and **concept** (e.g. `chunks_must_be_referenced`, `concept-layering-scaffold`). **Propose** names from the **phase** + concept + verb (and step text inside the phase doc if needed), then **check uniqueness** under `parts/rules/`.

## 3.3 Assembly model (static vs dynamic)

**Two different “static vs dynamic” pairs** — do not conflate:

1. **`build.py` assembly** (repo artifacts): Each skill ships `scripts/build.py`. It merges **process + library + phases (+ rules)** into **`AGENTS.md`** and optional **`content/built/`**. Flags like `--assembly static|snapshot` are **per skill** when present.

2. **AI-chat prompt generation** (`generate_prompt`): For **AI-driven** phases only — **dynamic** = assemble instruction string from sections; **static** = emit text from **pre-built** phase file under `phases/built/` (or documented path). See [`process-approach.md`](process-approach.md).

**Per skill:** `build.py` is the **authoritative** merge driver for **this** repo; scaffolding **emit or check** trees — they do **not** replace `build.py`.

**Flag on `build.py`:** The skill’s `build.py` may expose **CLI flags** for snapshot vs interactive merge; exact names are per skill. For **prompt** modes, document **`generate_prompt`** (or equivalent) next to **`build.py`** in **`README`** / **`AGENTS.md`**.


| Mode (merge / delivery) | Mechanism                                                                               | When                                                               |
| ----------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Static (merge)**      | `build.py` merges **built-phase** fragments into `AGENTS.md` / `SKILL.md` (and related) | Release, reproducible snapshot; CI; “what ships”.                  |
| **Dynamic (merge)**     | Runtime concatenation by **phase** / **operation** from `skill-config.json` + manifest  | Interactive sessions, partial rebuild, IDE-driven iteration. |


A **host** (CI, IDE, or orchestrator) may emit an **internal** manifest (JSON or YAML) for a **given generation run**, listing which fragments form which artifact for both modes; the skill’s `build.py` **may read** that manifest (or embedded config) when implementing **static** merges and documents how **dynamic** mode resolves fragments at runtime. That manifest is **optional** and **not** a standard every skill must carry — only **documented** `build.py` behavior is.

## 3.4 Reference skills (illustrative)

Other skills in the monorepo **illustrate** patterns (long `AGENTS.md`, phased pipelines, rules + scanners). They are **examples**, not extra requirements. **Operator** checks and layout rules are grounded in **abd-skill-builder** library files and each skill’s **`skill-config.json`** — not in a separate “corpus” file unless your team adds one.


---

### `builder-vs-operator.md`

# Builder vs Operator (today)

**Generation / scaffold (“builder” in the loose sense):** Anything that **emits** a new skill tree — typically **`abd-skill-builder`’s `scripts/scaffold_skill.py`** plus templates — producing `SKILL.md`, `skill-config.json`, phase markdown, `rules/` stubs, `scripts/build.py`, optional scanners. Output should match **§3** layout and avoid embedding customer “gold” solutions in the template.

**Operator (structural gate):** **`agentic-skill-builder`** **`operator.run_operator()`** — validates `skill-config.json`, runs a **Python compile check** on the paths in **`operator.compileall_paths`** (the implementation uses Python’s **`compileall`** module), runs **`operator.build_script`** (typically `python scripts/build.py`), then runs **scanner scripts** listed under **`operator.scanners`**. A normative skill also declares **`operator.build_pipeline`**: the **ordered post-merge steps** that **`build.py`** runs after writing **`AGENTS.md`** / built slices (rule-bound scanners, emitters, manifest, lint—**per skill**). **Rule → scanner** bindings live in **`rules/scanners.json`**; see **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** (base framework for all skills). Operator does **not** create greenfield skills; that is **`scaffold_skill.py`** and authoring.

**This skill’s role:** Ship **standards** under **`content/parts/library/`**, **process + phases**, **`scaffold_skill.py`**, and **templates** so authors get a compliant tree first, then Operator keeps it green.


---

### `rules-and-automated-checks.md`

# Rules and automated checks (base framework for every skill)

**Status:** **Normative default** for Open Agent Skills in this repo. When a skill defines **governance rules** (`rules/*.md`) and wants **machine enforcement**, wire checks this way—not as one-off phase script call-outs.

## What owns what

| Layer | Owns |
| --- | --- |
| **`rules/<stem>.md`** | The **human-readable rule**: scope, must/should, examples, done criteria. |
| **`rules/scanners.json`** | **Which script enforces which rule** — `rule_scanner_bindings[]` maps `rule_id` + `rule_file` → `scanner` path (relative to skill root). Optional top-level **`scanners`** lists scanner scripts for tooling that expects a flat array. |
| **`skill-config.json` → `operator.build_pipeline`** | **Ordered post-merge steps** that **`scripts/build.py`** runs after it writes **`AGENTS.md`** / **`content/built/`** (or your skill’s equivalent). Entries are typically **`scripts/...py`** paths: rule-bound scanners, emitters, manifest generators, rule-example linters, etc. **Empty or omitted** means “merge only” (skills with no automated checks yet). |
| **`skill-config.json` → `operator.scanners`** | **Operator / CI gate** — paths **`agentic-skill-builder`** **`operator.run_operator()`** runs **after** **`operator.build_script`**. **Keep these paths aligned** with the scanner steps you care about (usually the same modules listed in **`build_pipeline`** and/or **`rules/scanners.json`**), so “green build” and “green operator” mean the same checks. |

## What you do not do

- **Do not** treat **scanners** as **phase-owned scripts** in **`process.md`** process tables. Phase rows are for **human/AI procedure** and **merge / emit** entry points (e.g. `python scripts/build.py`), not for listing every validator. If readers need detail, add a short **“Rules and automated checks”** subsection in **`process.md`** that points here and to **`rules/scanners.json`**.
- **Do not** bind scanners only in prose. If a rule is machine-checked, add a **`rule_scanner_bindings`** row and a **`build_pipeline`** step (and **`operator.scanners`** / Operator docs as required by your host).

## Execution flow (mental model)

1. Author edits **`content/parts/`**, **`rules/`**, **`skill-config.json`**.
2. **`python scripts/build.py`** merges instruction bundles, then runs **`operator.build_pipeline`** in order (if present).
3. **Operator** (or CI) runs compile check → **`build.py`** again → **`operator.scanners`** (when configured).

**Reference implementation:** **`abd-maps-models-specs`** — `rules/scanners.json`, **`operator.build_pipeline`** in **`skill-config.json`**, and **`scripts/build.py`** driving the pipeline after merge.

## Scaffolded skills

Greenfield trees from **`scaffold_skill.py`** should ship **`rules/scanners.json`** (even if bindings start empty) and a **`skill-config.json`** fragment that includes **`operator.build_pipeline`** alongside **`operator.scanners`**, so authors extend **one** pattern instead of inventing ad hoc wrappers.

See also: **[`skill-standards-section-3.md`](skill-standards-section-3.md)** (§3.1 config row), **[`builder-vs-operator.md`](builder-vs-operator.md)**, **`rules/README.md`** at the skill root.


---

## Rules

*No rules for this phase. List rule stems (filename without `.md`) under `skill-config.json` → `phase_rules` for this phase slug, and optionally `every_phase_rules` for rules that apply to every phase. See `parts/library/process-approach.md` § Phase bundle — rules.*


---

## Phase: migrate

## Principles

**AI quality — normative rules, scanners, and review.** This shard is injected under **`## Principles`** in phase bundles; the heading above is added by the assembler.

**Scope:** In **abd-skill-builder**, this file is injected as **`## Principles`** and is the **first** section in each AI-chat phase bundle (`python scripts/generate.py --phase <slug>` and `content/parts/phases/built/<slug>.md`). Read it **before** Role, Phase body, Library shards, and Rules for that phase.

---

**Every rule in `rules/` is two things at once:** (1) **Normative advice** — prose the model follows while authoring **`content/parts/`**, **`rules/`**, **`skill-config.json`**, and other skill artifacts. (2) **Checkable expectations** — where this repo ships a **scanner** under **`scripts/`**, it catches common layout or config misses; where it does not, **you** still review against the rule text.

**Example (wrong):** Treating a green **`python scripts/build.py`** as enough while **`AGENTS.md`** still disagrees with **`content/parts/`** or **`phase_rules`** omits a rule you claimed to enforce.

**Example (correct):** Read the **Rules** section in this bundle, align files with **`library/`** norms, run **`python scripts/build.py`** (and **`operator.scanners`** when configured), then **re-read** outputs against each applicable rule.

---

## Layer 1 — Generate with rules

While generating or editing skill artifacts:

- Apply **`rules/*.md`** inlined into this bundle (and related **`library/`** docs).
- Prefer **DO / DON’T** and **good vs bad** fragments inside each rule — they are the contract for *shape*, not only for CI.

---

## Layer 2 — Mechanical checks (this skill)

After you have files on disk, the pipeline can run:

| Mechanism | What it does |
| --------- | ------------ |
| **`python scripts/build.py`** | Merges **process** + per-phase bundles into **`AGENTS.md`** and **`content/built/`**, then runs **`operator.build_pipeline`** (e.g. **`scripts/scanner_skill_builder_layout.py`**) when configured. |
| **`rules/scanners.json`** | Declares **rule → scanner** bindings when your skill uses them; align with **`operator.scanners`**. |

**Example (wrong):** Hand-editing **`AGENTS.md`** while **`build.py`** is supposed to own the merge.

**Example (wrong):** Adding a scanner only in prose — no **`rule_scanner_bindings`** or **`build_pipeline`** step.

**Example (correct):** Fix issues reported by scanners, re-run **build**, keep **`skill-config.json`** paths honest.

Scanners are **necessary** for what they implement; they are **not sufficient** for semantic quality (e.g. a valid tree that still mis-describes what the skill does).

---

## Layer 3 — Adversarial pass (human or AI)

With clean tool output, still ask:

- Does each **rule** that applies to this phase pass **by intent**, not only by letter?
- Would a reviewer see **drift** between **`SKILL.md`**, **`process.md`**, and **`phases/`** even when the tree validates?

Use the **Corrections format** below when fixing issues.

---

## Corrections format

When recording or fixing a problem:

| Field | Content |
| ----- | ------- |
| **Rule** | Rule id or `rules/<file>.md` name |
| **Example (wrong)** | What was done incorrectly |
| **Example (correct)** | What it should be |
| **Scanner or validator** | If applicable — see **`rules/scanners.json`** and **`operator.build_pipeline`** |
| **Likely source** | One of: prompt gap · rule not read · edge case · automation gap |

---

## Do not bypass the documented pipeline

**AI phases** mean: read inputs, reason, update the **source** files this skill owns under **`content/parts/`**, **`rules/`**, and config — not one-off scripts that rewrite merged outputs **instead** of fixing sources. Automation that ships with the skill lives under **`scripts/`** and is wired through **`skill-config.json`** (**`build.py`**, **`build_pipeline`**, **`operator.scanners`**) as documented in **`library/rules-and-automated-checks.md`**.

**Example (wrong):** Patching **`AGENTS.md`** directly to “pass” review while **`process.md`** is unchanged.

**Example (correct):** Edit **`content/parts/`** (or **`rules/`**), run **`python scripts/build.py`**, commit regenerated **`AGENTS.md`** / **`content/built/`** when using **`static_built`**.


---

## Phase

# Phase — Migrate existing skill (execute)

Use this when the skill **already exists** and you are **applying** the plan from **[`plan-migrate.md`](plan-migrate.md)** (**Stage 1b**): **move** files into the **correct layout**, **rename**, **rewire** **`build.py`** / **`skill-config.json`**, and **patch** only what the user **already selected** in the **delta**—**straight execution**, not a second full standards inventory.

**Not here:** writing the **initial** **[`docs/standards-delta.md`](../../docs/standards-delta.md)** table or comparing every row to §3—that is **`plan-migrate.md`**.

**Not here:** **scaffolding from zero** — use **[`scaffold.md`](scaffold.md)** (**2a**).

---

## Prerequisites

- **[`plan-migrate.md`](plan-migrate.md)** completed: a **delta** artifact (e.g. **`docs/standards-delta.md`**) with **IDs**, and the user’s **choice** of which **IDs** to fix in this pass.

---

## Outcome

1. **Tree** changes that implement **only** agreed **IDs** (moves, new files, config updates).
2. **Delta** rows updated: **fixed**, **deferred**, or **accepted risk**.
3. **Operator** checks pass after substantive edits (**Python compile**, **`build.py`**, **scanners**).

---

## Process

1. **Re-read** the selected **IDs** from the delta—**no** scope creep.
2. **Apply** each fix: path moves, **`content/parts/`** layout, **`rules/`**, **`skill-config.json`**, **`build.py`** merge lists—whatever the **ID** requires.
3. Run **`python scripts/build.py`**; fix **sources**, not **AGENTS.md** by hand.
4. Re-run **operator** steps (compile paths, **build**, scanners).
5. **Update** the delta file: mark rows **fixed** / **deferred** / **accepted risk**.

---

## AI behavior

- **Straight delta:** implement **only** what **1b** and the user agreed—**no** silent full rewrites.
- **Be specific** in commits/edits: one **ID** per logical change when practical.
- After **migrate**, consider **[`fill-scaffold-parts.md`](fill-scaffold-parts.md)** (**2c**) if **`library/`** / **`rules/`** still need **authoring** beyond layout fixes.

---

## Related

- **[`plan-migrate.md`](plan-migrate.md)** — **1b** (inventory + delta + user selection).
- **[`plan-script-build.md`](plan-script-build.md)** — **1a** (new skill plan).
- **[`fill-scaffold-parts.md`](fill-scaffold-parts.md)** — **2c** (fill **library** / **rules**).
- **[`../library/skill-repo-standards.md`](../library/skill-repo-standards.md)** — standards index.
- **[agentic-skill-builder README](../../../agentic-skill-builder/README.md)** — operator / delivery graph.


---

## Library



---

### `documentation-standards.md`

# Skill documentation standards

**Canonical:** `skills/abd-skill-builder/content/parts/library/documentation-standards.md` (merged into **`AGENTS.md`**).

Use these rules when you author or refactor **process**, **phase docs**, optional **`docs/`** reference, staged **`content/built/`** output, and **AGENTS.md** for any Open Agent Skill. They prevent tangled cross-cutting docs and unreadable process prose.

## Delivery mode (`static_built` vs `runtime_injection`)

Declare **`delivery.mode`** in **`skill-config.json`** (default **`static_built`**). That flag answers whether the agent relies on **checked-in** **`content/built/`** + **`AGENTS.md`** or on **runtime** assembly from **`rules/`**, library fragments, and phase manifests. Normative definitions, when each applies, and how the two stay in sync are in **`delivery-modes.md`**.

## Workspace configuration

Skills that **route** to a customer tree keep **`conf/abd-config.json`** at **`skill_path`** with **`active_skill_workspace`** (and optional **`known_skill_workspaces`**). The file is **part of the repo**—**edit `active_skill_workspace`** to point at the workspace root (see **[workspace-and-config — Skill path, skill workspace, and configuration](../phases/workspace-and-config.md#skill-path-skill-workspace-and-configuration)**). A host (e.g. SkillField) may override. The install folder does **not** hold the customer project—only pointers. Workspace-local parameters live under **`skill_workspace/conf/`** per skill docs. Do not leave “where we run” only in prose unless the skill documents overrides.

## Agent-facing vs reference (read this first)

**If text is merged into `AGENTS.md`, injected into prompts, or otherwise part of the agent bundle, it belongs under `content/parts/`** (e.g. `process.md`, `phases/<phase>.md`, shared fragments). It does **not** live “only in `docs/`” with the expectation that the agent will see it unless your build copies it in.

**Staged build (`content/built/`):** When a complete file is **assembled** from pieces—e.g. a **base** plus **rules** plus **operator/story roles**—write the **intermediate, fully expanded** markdown under **`content/built/`** (or `content/parts/built/` / `phases/built/` if the skill already uses that layout). Then the final step generates the **complete** artifact (`AGENTS.md`, a single phase handoff, etc.). Do not skip the staged output if you need to diff or review what rules were baked in. (Example pattern: `abd-solution-modeler` uses `phases/built/` for phase specs.)

**`docs/`:** Use for **long-form reference** that operators (or tools) open beside the skill—principles, execution order, invariants, **and** standalone construct write-ups (schemas, package layout) **when** those are **not** duplicated as the sole copy of agent instructions. Phase tables and “what you must do” for the agent still live in **`content/parts/`**; `docs/` may **link** to the same ideas or hold deeper detail. If a norm must be in the agent’s context, mirror or generate it from `content/parts/`, not only from `docs/`.

## Voice and role

Write for the **operator** in **second person** (you, your). Frame the work clearly:

- **Your role** — What you are responsible for in this stage or skill (one or two sentences).
- **What you must do** — Imperatives and phase order (use bullets for several short obligations).
- **What you produce** / **How you know you succeeded** — Outcomes and done criteria.

Prefer **you must**, **you will**, and **then you** (sequence) over passive voice (“the pipeline establishes,” “artifacts are emitted”). Say who runs a script or makes a decision.

## Where content belongs

| Kind | Put it here | Do not |
| --- | --- | --- |
| **Process spine** — stages, phase numbers, tables, links to phase files | `content/parts/process.md` (or skill’s `content/process.md`) | Paste the entire phase table again as a second narrative. |
| **Phase behavior** — steps, checklists, **script invocations**, file paths for **this phase only** | `content/parts/phases/<phase>.md` | Split one phase across three cross-cutting docs; **duplicate** long cross-phase definitions—**link** to **`library/`** instead. |
| **Library shards** — definitions, glossaries, artifact shapes, naming, invariants for ideas that **span multiple phases** | `content/parts/library/<topic>.md` | Phase-local procedures, numbered runbooks, pipeline order, or “run `python scripts/…`” blocks that belong in **`phases/`**. |
| **Baked agent instructions** — bases + rules + roles merged before `AGENTS.md` | Source fragments under `content/parts/`; **output of merge** under `content/built/` (or `phases/built/`) **before** final generation | Edit only the final `AGENTS.md` by hand when a build step should own the merge. |
| **Standalone construct reference** — one artifact contract (schema, validators, chunk layout), diagrams, deep dives | `docs/<descriptive-name>.md` | Treat `docs/` as the **only** place agent-facing norms live; duplicate the “must do” into `content/parts/` or generate into `content/built/`. |
| **Cross-cutting** — principles, execution order, invariants that apply across phases | Usually `docs/` or `content/parts/library/` (e.g. principles prose); **governance rules** that vary by phase: **`skill-config.json`** → **`phase_rules`** / **`every_phase_rules`** + `rules/*.md` (see **`process-approach.md`**). **Link** from `content/parts/` where needed | Restate every phase inside cross-cutting docs; **link** to the process table instead. |

**Reference-doc filenames:** Do **not** prefix `docs/` filenames with phase numbers (e.g. avoid `phase2_terms.md`). Use **descriptive kebab-case** slugs (`terms-mechanisms-contract.md`, `behavioral-story-map.md`). Phase order belongs in `process.md` and `content/parts/phases/`, not in filenames.

**Cross-cutting** is for rules and order that are **not** naturally owned by a single phase. If the text is really about one phase only, prefer that phase’s file in `content/parts/phases/` plus a thin pointer from `docs/` if you keep a global index there.

## Library vs phase documents (split responsibility)

Use this split in **every** skill that has both **`library/`** and **`phases/`**:

- **`library/`** = **structure and meaning** shared across phases (what a thing *is*, how it is named, what fields exist, how it relates to other ideas). Think **reference** and **single source of truth** for multi-phase concepts.
- **`phases/*.md`** = **execution** for one pipeline step (what *you* do next, in order, including **commands** and **done checks**). Think **operator procedure** for *this* phase only.

**Hard bars**

| Layer | Must include | Must not be (move or trim) |
| --- | --- | --- |
| **`library/`** | Stable definitions, tables, schemas, cross-phase vocabulary | Long “how to run this phase” sections; **step sequences**; **script/CLI** runbooks; **phase ordering** or “after phase X…” workflow story |
| **`phases/`** | Short purpose, I/O, **steps**, script lines, checklists, **links** to **`library/`** for deep defs | Entire glossaries or artifact specs duplicated from **`library/`**; normative essays that belong in **`library/`** because **other phases** need the same text |

If a paragraph would still make sense **after renumbering or reordering phases**, it probably belongs in **`library/`** or **`rules/`**, not inside a single **`phases/<slug>.md`**.

**Governance rule in this repo:** [`rules/content-placement.md`](../../rules/content-placement.md).

## Prose style

- Several **short** points → **bullets**.
- One developed idea → **sentences** in a **paragraph**.
- Avoid long **semicolon chains** pretending to be one sentence.
- Avoid narrating **migration** from an old doc or old skill (“formerly §2.6”). Describe **this** skill only.

## Process tables

Keep the **stage narrative** at **intent and outcome**. The **table** holds actors, scripts, refs, and deliverable paths.

Normative column meanings, the required **workspace** phase (**Phase 0** informally), **`Input`/`Output` rules**, and **`build.py`/`generate.py` alignment** are in **[`process-table-standards.md`](process-table-standards.md)**. Use that doc whenever you create or refactor **`process.md`** in another skill.

Optional: an extra **Summary** column per row (**two or three sentences**) is allowed if you keep the abd-skill-builder **seven-column** shape as the default—do not drop **Input** / **Output** / **Scripts** in favor of summary-only rows. For the **maps-models-specs**-style table (**`Script`**, **`Outputs`**, **`Ref`**), put **`Summary`** in the **third** column (after **`#`**, **Phase**) and **`Ref`** **last**—see **`process-table-standards.md`** § Maps / models / specs pipeline table.

## When you edit

1. Update the **smallest** place: phase file or construct doc first.
2. If you are repeating script names and outputs that are **already** in the table, **delete** the repetition and keep purpose or pointer to `phases/`.
3. Regenerate **AGENTS.md** after changing `content/` so agents see the update.


---

### `process-table-standards.md`

# Process table standards (for `process.md`)

**Use this** whenever you author or refactor **`parts/process.md`** (or **`content/parts/process.md`**) so skills stay consistent with **abd-skill-builder** and Operator expectations. Pair with **`skill-standards-section-3.md`** (stages / phases / steps) and **`documentation-standards.md`** (voice, where content lives).

---

## Workspace phase (“Phase 0”) — required for every skill

Every skill that can target a **project tree** or needs unambiguous **where am I running?** semantics must include a **workspace** phase:

| Item | Rule |
| --- | --- |
| **Phase file** | **`parts/phases/workspace-and-config.md`** (or under **`content/parts/phases/`** if your skill uses that layout). Slug: **`workspace-and-config`**. |
| **Process row** | First process-table row **after** any “standards / checklist” preamble; **#** column **`0`** (Phase 0 — workspace first in the pipeline). **Team process plate** (`process-team.md.template`) hard-codes this row; **do not** rename the **Phase** link text to **`Phase 0 — …`** inside the table cell—keep the stable slug title **Workspace and config**. |
| **Heading & name** | Phase document **H1** and links: **Workspace and config** (not **Phase 0 — …** in the phase file’s **H1**). In **`parts/process.md`**, the **section** heading **Phase 0 — Workspace and config** is OK; the **process table** still uses the stable **Phase** column title above. |
| **Config** | **`conf/abd-config.json`** at **`skill_path`** with **`active_skill_workspace`** (and optional **`known_skill_workspaces`**). Same **JSON shape** across skills; see **abd-skill-builder** reference **`conf/abd-config.json`**. |
| **Merge / generate** | **`build.py`** should list **`workspace-and-config`** **first** in the phase merge list when that file exists; **`generate.py --phase workspace-and-config`** must resolve for AI-chat steps. |
| **CLI — `active_skill_workspace`** | Every scaffolded skill includes **`scripts/set_workspace.py`** (copied from **abd-skill-builder**). **Process** row **0** **Scripts** cell must include the same wording as **abd-maps-models-specs** phase **Set workspace**: `` `python` [`scripts/set_workspace.py`](…) — no args prints current; `<path>` sets `active_skill_workspace` in `conf/abd-config.json` ([workspace-and-config](phases/workspace-and-config.md)) `` — then **`·`** and **`generate.py`** for the AI-chat phase when both apply. |

Routing details are **not** duplicated inside **Plan** or **Scaffold** phase bodies—**link** to **`workspace-and-config.md`**.

---

## Process table columns (abd-skill-builder shape)

Use this **seven-column** header (exact labels help readers and tooling):

| Column | Meaning |
| --- | --- |
| **`#`** | **Phase id** in the pipeline: **`0`** for workspace (Phase 0); **`1a` / `1b`** for plan variants; **`2a` / `2b` / `2c`** for create/fix/fill; **`3`** for operator; or your skill’s own scheme. **Order** is this column + stage sections—not filenames. |
| **Phase** | **Linked title** to **`phases/<slug>.md`**. Stable, descriptive name (not `phase-02-foo.md` in the link text). |
| **Description** | **What happens** in this phase: decisions, constraints, pointers to other phase docs for cross-cutting topics. **Not** a second copy of the whole phase file—enough to choose the right doc. |
| **Actor** | **Who runs it:** Human / AI, Code, Human / AI + Code, etc. |
| **Input** | **What you must have** to start: paths, prior artifacts, CLI flags, **not** the phase’s primary deliverable if that deliverable is produced **in** this phase (avoid listing **`docs/skill-plan.md`** as **Input** for **1a** when **1a** creates that file—use *library norms + target workspace* instead). |
| **Output** | **Concrete artifacts** when the phase is done: files, directories, exit criteria. For **scaffold (2a)**, lead with the **scaffolded skill tree** ( **`SKILL.md`**, **`skill-config.json`**, **`conf/`**, **`content/parts/`** or **`parts/`**, **`scripts/`**, **`rules/`**, **`test/`**, **`docs/skill-plan.md`** ), then **`AGENTS.md` / `content/built/`** after **`build.py`**—not only the skill-plan template. |
| **Scripts** | **Commands** with **entry script names**: `python scripts/generate.py --phase <slug>`, `python scripts/build.py`, **`scaffold_skill.py`**. **Do not** pack **rule-bound scanners** here—those are skill-wide; document them under **Rules and automated checks** (see **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**) and run them via **`build.py`** / **`operator.build_pipeline`**. One cell; use **`·`** between multiple commands. |

**Do not** use a vague **Output** that only points at a **template file** when the real outcome is a **written document** or **directory tree**—say the **path** under the skill (e.g. **`docs/skill-plan.md`**).

### Maps / models / specs pipeline table (seven columns, `Script` + `Outputs` variant)

Skills such as **abd-maps-models-specs** use the **same seven-column count** with different labels: **`#`**, **Phase**, **Summary**, **Actor**, **Script**, **Outputs**, **`Ref`**.

- **`Summary`** is the **third** column (after **`#`** and **Phase**) so wide prose sits early in the row and previews well in Markdown renderers.
- **`Ref`** is the **last** column (phase doc links stay the right-hand anchor).

Keep **exact header labels** (**`Outputs`** for concrete artifacts and paths) so tables stay consistent across stages.

---

## Stages vs tables

- **Stage** sections (**`## Stage N — …`**) carry **narrative**: purpose, what you produce, how you know you succeeded.
- **Tables** carry **rows = phases**: Ref, Actor, Input, Output, Scripts. **Steps** stay **inside** phase markdown files, not extra table rows (per §3).

---

## Language

- **Second person** for operator-facing prose in phase files (**you**, **your**); see **`documentation-standards.md`**.
- **Process one-liner** at the top of **`process.md`**: pipeline string with **linked phase names** (e.g. **Workspace and config** → **Plan** → …).
- **Routing** cells: short **“Routing: [Workspace and config](…)—not repeated here.”** instead of repeating **`conf/`** keys.

---

## `build.py` and `generate.py` alignment

When you add or rename a phase:

1. **`parts/phases/<slug>.md`** exists.
2. **`process.md`** has a row with that **Phase** link and **`#`** id.
3. **`scripts/build.py`** — **`PHASE_FILES`** (or equivalent) lists **`slug`** in merge order; **`LIBRARY_FILES`** lists library shards in order.
4. **`scripts/generate_prompt.py`** — resolves **`parts/phases/<slug>.md`** (or **`content/parts/phases/`**); **`generate.py`** stays the thin CLI that delegates to it.
5. Regenerate **`AGENTS.md`** / **`content/built/`** after edits.

---

## Reference

- **Worked example:** **`parts/process.md`** in **abd-skill-builder**.
- **Rich pipeline doc:** **`templates/process-team.md.template`** (team process plate).
- **Workspace normative body:** **`parts/phases/workspace-and-config.md`**.


---

### `delivery-modes.md`

# Agent delivery modes (static build vs runtime injection)

Skills can hand instructions to an **agent** or **executor** (including an EA / orchestrator) in two ways. **Do not mix them in one session without an explicit choice** — same requirement as §3.3 *Assembly model* in [`skill-standards-section-3.md`](skill-standards-section-3.md) (static vs dynamic).

## `AGENTS.md` — always (skill-wide orientation)

**`AGENTS.md`** is the **assembled agent bundle**: how the skill is structured, how phases/steps relate, and how to work with it in general. It should be **assembled for every skill** (typically generated by **`scripts/build.py`**), regardless of **`delivery.mode`**. It is *not* what the mode flag switches on or off.

**What `delivery.mode` actually changes** is how a **single operation** (or phase/step run) gets its **process slice**: either from **pre-generated built output** or from **runtime injection** of sources — see below.

## Flag (system-wide convention)

Declare the mode in **`skill-config.json`** so tools, CI, and humans agree:

```json
"delivery": {
  "mode": "static_built"
}
```

| `delivery.mode` | Meaning |
| --- | --- |
| **`static_built`** | **Default.** When you **run an operation**, the executor uses **process content that has already been merged into `content/built/`** (and similar per-skill layouts): each slice includes the **process part** plus its **library** and **rules** components as produced by the build. **`AGENTS.md`** is still checked in as the skill-wide bundle; **built** trees are the canonical **operation-time** artifacts. Operators run **`python scripts/build.py`** after changing sources; commits include regenerated files. |
| **`runtime_injection`** | When you **run an operation**, the executor **injects** the **process part** and, in documented order, **all** of its **library** and **rules** components from source paths — **without** requiring that slice to exist as a pre-built file under **`content/built/`**. **`AGENTS.md`** is still assembled for orientation; only the **operation-time** merge strategy differs. |

**Default for new skills:** `static_built`. Use **`runtime_injection`** when you want runtime resolution; use **`static_built`** when you want checked-in slices — **both** require the same **documented injection map** (see below).

## Injection map — document regardless of mode

**`delivery.mode` does not decide whether you document injection.** It only decides **pre-generate** (build + commit **`content/built/`**) vs **inject at run time** after each operation. In **both** cases:

1. **Which** source paths (process slice, **`library/`**, **`rules/`**, …) apply **per operation** (phase/step).
2. **In what order** they are merged / concatenated / injected.
3. **How** that matches the **static** merge (same semantics as **`build.py`**, or **deliberate differences** called out).

Keep this in a **single lookup** place — e.g. skill **`README.md`**, a manifest in **`build.py`**, or a **generated manifest** checked in next to **`built/`** — so someone can **change `delivery.mode` later** without re-deriving paths from scattered files. The only thing that changes is **when** material is materialized (build vs runtime), not **what** the skill is allowed to omit from documentation.

## Mode (a) — `static_built`

- **What is delivered:** Generated markdown under **`content/built/`** (and/or `phases/built/`, `content/parts/steps/built/` per skill layout) plus the top-level **`AGENTS.md`** when the build emits it.
- **Operation-time behavior:** Use the **built** slices (process + library + rules already merged for that slice).
- **When it applies:** CI, reviewable diffs, reproducible runs, “what the agent saw” is literally in git.
- **Operator obligation:** After editing **`content/parts/`**, **`rules/`**, or merge inputs, run **`build.py`** and commit outputs.

## Mode (b) — `runtime_injection`

- **What is delivered:** For **operations**, not a single pre-expanded tree under **`built/`**; the **executor** resolves **phase** (or step) → **files** (`rules/…`, `content/parts/library/…`, process slice, etc.) and **injects** them into context in a documented order (full **process part + library + rules** for that operation).
- **`AGENTS.md`:** Still assembled so the agent understands the skill in general; only **per-operation** content is resolved at runtime.
- **When it applies:** Interactive orchestration, rapid iteration without running the full static pipeline each time, or environments where checking in large built blobs is undesirable (still document the tradeoff).
- **Operator / implementer obligation:** Same as **static** mode for the **injection map** — resolution order, equivalence vs static merge, validation — **not** optional just because execution is dynamic. Runtime mode adds: executor must follow the **same** documented map (or list exceptions).

## Staying in sync between modes

1. **Single source of truth** for *meaning* stays in **unbuilt** inputs: **`content/parts/`**, **`rules/`**, **`docs/`** (reference), not in hand-edited **`AGENTS.md`** when a build owns the merge.
2. **`static_built`** outputs are **derivatives**: regenerating must be repeatable from the same inputs + **`scripts/build.py`** (and any merge manifest the skill defines).
3. **`runtime_injection`** must **not drift silently**: if both modes are supported, the skill should state whether runtime is a *shortcut to the same merge* (ideal) or a *lighter subset* (then list gaps).
4. **Changing sources:** Under **`static_built`**, CI or pre-commit should run **`build.py`** and fail if **`content/built/`** / **`AGENTS.md`** are stale (exact hook is repo-specific).
5. **Switching modes:** The **injection map** (paths + order + equivalence) is what lets you move from **`static_built`** to **`runtime_injection`** or back — update **`delivery.mode`** and keep the **same** map unless you intentionally change behavior.

## Relation to `build.py` flags

Per §3.3, a skill may expose **`--assembly static|dynamic`** (or equivalent) **inside** `build.py` for *how* static snapshots are produced. That is **orthogonal** to **`delivery.mode`**: `delivery.mode` answers whether the **operator/agent relies on checked-in built files** vs **runtime resolution**. A skill can use `runtime_injection` at execution time while still using `build.py --assembly static` to produce reference snapshots for tests.


---

### `process-approach.md`

# Process approach — IDE, `process.md`, code phases vs AI-chat phases

**Audience:** Authors and tooling. This is the **default mental model** for how a skill is **used** (Cursor, VS Code, Claude Desktop, similar) and how **phases** are executed.

## Who consumes what


| Artifact                                                               | Who uses it                                     | How                                                                                                                                                                                                                                                                                                                      |
| ---------------------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `**AGENTS.md`** (skill root)                                           | **IDE / assistant**                             | Loaded **automatically** by many tools as context for the repo. It orients the model: pipeline, links, where `process.md` lives. **No one “opens `built/` by hand” as the primary workflow** — the chat does not browse the tree to find instructions; **you tell it what to do** using `**process.md`** and phase docs. |
| `**content/parts/process.md**` (or `pieces/process.md` in some skills) | **Human + chat**                                | **Map of phases**: table rows are **phases**, **Ref** links to phase files. The skill should tell users to **read / `@`-reference** this file to know **how to execute** a given phase (order, actor, script). Example pattern: `@agilebydesign-skills/skills/<skill-id>/content/parts/process.md`.                      |
| **Built phase text** (`phases/built/`, `content/built/`, …)            | **Build pipeline + optional `generate_prompt`** | **Generated** outputs — **not** “what autonomous agents read first.” They exist so you can **materialize** a full instruction block for an AI phase (static mode) or **diff in git** under `static_built` delivery.                                                                                                      |


## Phase kinds (two execution styles)

### 1. Code-driven phases (human or CI runs the script)

- **You run** the Python/shell entry point **normally** (terminal, task, CI).
- **Await** exit code and artifacts the phase defines.
- The **phase markdown** (source) describes **how to invoke** the script, **arguments**, **outputs**, and **what “done” means** — not a prompt to paste unless the phase is hybrid.

### 2. AI-chat–driven phases (instructions for the model)

- The **instruction body** the chat must follow is produced by **prompt generation** — short name: **generate prompt** (implementation often `scripts/generate_prompt.py` per skill; names may vary).
- **CLI shape (contract):** support a **phase selector**, e.g. `python scripts/generate_prompt.py --phase <phase_slug>` (some teams use `phase:<name>` as a single token; equivalent intent).
- **Two modes** (both end with “text the user pastes or tool injects into chat”):


| Mode        | What it does                                                                                                                                                                                                                                                            | When to use                                                                |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Dynamic** | Builds one **string** by **collecting every section** required for that phase (source phase markdown, `library/` fragments, applicable `rules/`, manifest order in `skill-config.json` / `build.py`).                                                                   | Fast iteration; single source of truth; no checked-in blob for that phase. |
| **Static**  | Uses **pre-generated** phase text already written under the skill’s **built tree** (convention: `content/parts/phases/built/<phase_slug>.md` or `phases/built/<phase_slug>.md` — **document the path in the skill**). **Grab the whole file** as the instruction block. | Reproducible snapshots, CI, “exactly what shipped last release.”           |


In **either** mode, the **outcome** is: **the IDE chat has the right block of instructions** to follow for that phase — not “the agent navigates to `built/` like a filesystem API.”

### Default `phase_bundle` order (`skill-config.json`)

**abd-skill-builder** `Instructions` (used by `scripts/generate_prompt.py` and typical `scripts/build.py` merges) follows **`phase_bundle.order`** — an array of section tokens — unless `operation_sections` overrides the slug. **Default in this repo and scaffold template:** **`["principles", "role", "phase", "library", "rules"]`** so **`critical-quality-steps.md`** ( **`## Principles`** ) leads every AI-chat bundle. Other skills may reorder (e.g. **`principles`** last) or omit tokens; missing optional files (**`role`**, **`principles`**) are skipped.

Section tokens (each included only if listed in **`order`**):

- **`principles`** — optional: file under `content/parts/library/` (default `critical-quality-steps.md`), heading **`principles_heading`**. **Omitted** if the file is missing.
- **`role`** — optional: file under `content/parts/` (default basename `solution-analyst-role.md`). **Omitted** if the file is missing.
- **`phase`** — `content/parts/phases/<slug>.md` (or `parts/phases/`), with heading **`## Phase`** when `phase_bundle.phase_heading` is set.
- **`library`** — shards from **`PHASE_LIBRARY_SLICES`** for that slug, or all of **`library_files`** when the slice is absent; one **`## Library`** heading, then **`### \`file.md\``** per shard (with `abd:begin` / `abd:end` filtering). **Empty slice** → placeholder body under **`## Library`**.
- **`rules`** — **normative:** governance markdown inlined from **`rules/<stem>.md`** in manifest order. Stems come only from **`skill-config.json`**:
   - **`every_phase_rules`** — array of stems (no `.md`) prepended for **every** phase, **deduplicated** in order (listed once even if also under a phase).
   - **`phase_rules`** — object: keys are **phase slugs** (same strings as **`phase_files`**); values are ordered arrays of stems. Example: `"shaped-story-map": ["evidence-citations-required", "shaped-story-shape"]`.
   **No stems** for a phase → placeholder body under **`## Rules`** (points authors to this doc). Rule files may keep optional YAML frontmatter (e.g. **`rule_id:`**); **`Instructions`** strips it before inlining so bundles stay readable. **Do not** use per-rule **`phase_files:`** frontmatter as the source of truth for which phase gets which rule — that duplicates the manifest and drifts; **abd-maps-models-specs** and **abd-skill-builder** both standardize on **`phase_rules` / `every_phase_rules`**.

Configure (or copy defaults) via **`phase_bundle`** in **`skill-config.json`**: keys include **`order`**, **`role_file`**, **`principles_file`**, and optional **`role_heading`**, **`phase_heading`**, **`library_heading`**, **`rules_heading`**, **`principles_heading`**. **abd-skill-builder** ships the full default object so scaffolded skills inherit the same contract; **abd-maps-models-specs** uses **`MapsInstructions`**, which follows the same **`phase_rules` / `every_phase_rules`** contract (plus maps-only critical-quality notes).

### Library shards with phase markers (`abd:begin` / `abd:end`)

A **`library/*.md`** file may wrap fragments in **`<!-- abd:begin <phase-slug> -->`** … **`<!-- abd:end <phase-slug> -->`** (same slug on both lines). When **`Instructions.assemble_prompt(<phase-slug>)`** runs (used by **`generate_prompt.py`** and **`build.py`** for **`phases/built/<slug>.md`**), the reader sees **all lines outside** those pairs **plus** only the **pair whose slug matches** the current phase. Slugs match **`phase_files`** in **`skill-config.json`** (e.g. **`plan-script-build`**). Files **without** markers are included in full whenever **`PHASE_LIBRARY_SLICES`** lists them for that phase. Authoring template: **`templates/concepts.md.template`**.

## What `build.py` is for

- `**scripts/build.py`** merges **process + library + phases (+ rules where applicable)** into `**AGENTS.md`** and any `**content/built/**` slices per `**delivery.mode**`.
- It is the **authoritative** driver for **this** skill repo. `**generate_prompt`** is **orthogonal**: it answers “what text do I put in chat **for this AI phase**?” while `**build.py`** answers “what ships in **AGENTS.md** / static bundles?”

## Relation to §3

- **Stages / phases / steps** table semantics: `[skill-standards-section-3.md](skill-standards-section-3.md)`.
- **Rule file naming, assembly flags:** same §3 doc.
- **Delivery modes (`static_built` vs `runtime_injection`):** `[delivery-modes.md](delivery-modes.md)`.

## Team process plate (rich `process.md`)

For skills that need the same **shape** as **abd-maps-models-specs** — **outcome**, **principles**, **inputs / outputs**, **stages**, and a **wide phase table** (Description, Actor, Input, Output, Scripts) — start from the **team template**:

- **`content/parts/templates/process-team.md.template`** (in **abd-skill-builder**)
- **`content/parts/templates/README.md`** — how it relates to scaffold’s minimal **`templates/process.md.template`**

Copy the plate into **your** skill as **`content/parts/process.md`**, replace `{{skill_name}}`, add phases and **Ref** links, then run **`python scripts/build.py`**. The **abd-skill-builder** **`process.md`** demonstrates the same structure at production quality.

## Extending a new skill

1. Add `**content/parts/process.md`** with phase rows and **Ref**s (or start from **`process-team.md.template`** above).
2. For each **code phase**, document script + I/O in the phase file.
3. For each **AI-chat phase**, either wire `**generate_prompt`** (dynamic/static) or document a manual copy-paste path until scripted.
4. Run `**python scripts/build.py**` so `**AGENTS.md**` stays the IDE-facing bundle.
5. Keep `**process-approach.md**` behaviors in `**README.md**` in one paragraph so consumers know how your skill expects IDE + chat to work.


---

### `authoring-checklist.md`

# Skill authoring checklist (human + AI)

**Purpose:** Trackable **`- [ ]` / `- [x]`** tasks for building or evolving a skill. **Workspace convention:** keep this content in **`docs/skill-plan.md`** under the **## Authoring checklist** section (one document with the plan). **Scaffold** injects this file there; by hand, paste from here. If you stop mid-work, the next session continues from the **first unchecked** box in that section.

**Canonical source:** `skills/abd-skill-builder/content/parts/library/authoring-checklist.md` — merge updates from here when standards change.

| Role | What to do |
|------|------------|
| **A — Ask** | Use the **Ask:** lines under each section when you need input. |
| **B — Answer / suggest** | As **AI**, fill proposals; human confirms. |
| **C — Track** | Turn `- [ ]` into `- [x]` only when the item is **done**. |

**Normative layout/operator rules** stay in **`skill-repo-standards.md`** and **`skill-standards-section-3.md`** (under **`content/parts/library/`** in **abd-skill-builder**). **How the IDE uses the skill** (AGENTS.md, `process.md`, code vs AI-chat phases, `generate_prompt`): **`process-approach.md`**.

**Runtime vs `docs/`:** All markdown (and other content) that **pertains to how the skill is used at operation time** — merged or injected by **`build.py`**, read as phase bodies, or otherwise part of the **runnable** package — lives under **`content/parts/`** (and **`library/`**, **`rules/`**, etc. per norms). **`docs/`** is **only** for **non-runtime** material: user manuals, **skill plans** (including the checklist section), architecture, standards deltas. **Do not** stash mergeable instruction content in **`docs/`**. (**abd-skill-builder** itself only keeps **`docs/standards-delta.md`**.)

---

## Before you start (every session)

- [ ] **Working copy:** **`docs/skill-plan.md`** includes an **## Authoring checklist** section (scaffold injects this file there; by hand, paste from **`library/authoring-checklist.md`** into that section).
- [ ] **Resume:** Find the **first unchecked** `- [ ]` in the checklist section and continue from there.
- [ ] **Optional:** Note the date and “stopped at §…” in **Gaps / follow-ups** at the bottom when pausing.
- [ ] **`docs/` vs `content/parts/`:** No **runtime** markdown under **`docs/`** — phases, library bodies, and anything **`build.py`** merges/injects stay in **`parts/`**. **`docs/`** = manuals, **skill plan** (with checklist section), architecture, migration notes only.

---

## Greenfield vs existing skill

- [ ] **New skill:** Ran **`scaffold_skill.py`** (or equivalent) so the base tree exists.
- [ ] **Existing skill:** Ran **[plan-migrate.md](../phases/plan-migrate.md)** (**1b**: inventory + **standards-delta** + user chose **IDs**), then **[migrate.md](../phases/migrate.md)** (**2b**: execute moves) **before** bulk edits — **or** consciously skipped with a note in **Gaps / follow-ups**.

---

## Skill identity (what this skill does — not delta to other work)

Normative row: **Documentation focus** in **`skill-repo-standards.md`**.

- [ ] **Process, rules, and docs** describe **what this skill does** and how to run it — **this package**, on its own terms.
- [ ] They do **not** rely on “vs another skill” or “we don’t do X because Y” — that stays out of durable spec.
- [ ] **Dependencies** (other skills, repos, tools, versions) recorded explicitly (**Dependencies** / `README` / `conf/build-strategy.json`) — separate from the main narrative.

**AI should:** Strip migration chatter; put relationships in a **Dependencies** list.

**Ask:** “If this skill vanished, could someone run it from **this repo alone**?”

---

## Base scaffold: what you copy and extend

**Source:** **`skills/abd-skill-builder/scripts/scaffold_skill.py`** + **`skills/abd-skill-builder/templates/*`** — extend these files; don’t invent a parallel layout.

### Scaffold files present and reviewed (check each)

- [ ] **`SKILL.md`** — frontmatter + description make sense.
- [ ] **`skill-config.json`** — `operator.*`, `delivery.mode` match intent; if **`rules/*.md`** back AI-chat phases, **`phase_rules`** / **`every_phase_rules`** list every rule stem for the right **phase slug** (**[`process-approach.md`](process-approach.md)** — *rules* in the default **`phase_bundle`**).
- [ ] **`conf/build-strategy.json`** — `skill_purpose` and siblings filled per Strategizer.
- [ ] **`conf/abd-config.json`** — **`active_skill_workspace`** set (under **`test/`** when using a workspace); optional CLI: **`python scripts/set_workspace.py <path>`**.
- [ ] **`scripts/set_workspace.py`** — present (scaffold copies from **abd-skill-builder**).
- [ ] **`conf/README.md`** — conf usage clear.
- [ ] **`content/parts/process.md`** — pipeline table matches real phases.
- [ ] **`content/parts/phases/`** — one file per row in **`process.md`** (add/rename beyond **`author.md`** as needed).
- [ ] **`content/parts/phases/built/`** — present when you use **static** AI-chat prompts; populate via **`build.py`**; see **`process-approach.md`**.
- [ ] **`scripts/generate_prompt.py`** — present for AI-chat phases; **`--mode dynamic`** vs **`static`** documented; extend per skill.
- [ ] **`scripts/build.py`** — merge/injection driver present (see non-negotiables below).
- [ ] **`scripts/scanner_smoke.py`** — replaced or supplemented with real scanners if needed.
- [ ] **`rules/README.md`** + **`rules/scanners.json`** — wired when rules exist.
- [ ] **`test/README.md`** — explains layout; workspace path if used.
- [ ] **`content/parts/library/`** — created when cross-cutting chunks exist; wired in **`build.py`** (e.g. **`PHASE_LIBRARY`**) per §3.

### Non-negotiables

- [ ] **`scripts/build.py`** is the **merge / injection driver** (writes at least **`AGENTS.md`** from process + phases).
- [ ] **`process.md`** order matches **`phases/`** and **`build.py`** (if order ≠ lexicographic sort of filenames, **`build.py`** uses an **explicit ordered list**, not **`sorted(glob)`**).
- [ ] **Process → operation injection** documented in/near **`build.py`** + human-readable place for §4.

### Reference templates read (when extending)

- [ ] Read **`abd-skill-builder/parts/library/process-table-standards.md`** — process **`#`**, **Phase**, **Description**, **Actor**, **Input**, **Output**, **Scripts**; **workspace** phase (**Phase 0**) required.
- [ ] Opened **`abd-skill-builder/templates/child_build.py.template`** (minimal merge).
- [ ] If per-operation bundles / library injection: reviewed **`abd-maps-models-specs/scripts/build.py`** (`PHASE_FILES`, `PHASE_LIBRARY`, built phases).

### Extension work (after §§0–4 answers)

- [ ] **One** **`build.py`** — no second hidden merge pipeline.
- [ ] **`process.md`**, **`phases/*.md`**, **`build.py`** updated **together** when adding/changing a phase.
- [ ] **`content/parts/library/`** chunks added and wired in **`build.py`** where needed.
- [ ] **Injection map** in **`build.py` docstring** and/or skill **`README.md`** (aligns with §4).
- [ ] **`python scripts/build.py`** run after structural edits; **`AGENTS.md`** / **`content/built/`** committed if **`static_built`**.

**Ask:** “Which files do we **edit** vs **add**? Where is the **ordered phase list** in **`build.py`**?”

---

## 0. Build intent (`conf/build-strategy.json`)

- [ ] **`conf/build-strategy.json`** complete per **`agentic-skill-builder`** (template + Strategizer).

**Ask:** “What must this skill accomplish end-to-end? Who runs it? What is out of scope?”

---

## 1. Process & phases

- [ ] **`parts/process.md`** (or **`content/parts/process.md`**) lists the real pipeline (ordered phases) and follows **[`process-table-standards.md`](process-table-standards.md)** — column meanings, **Input**/**Output** semantics, **Scripts** cell.
- [ ] **Workspace phase (Phase 0):** **`parts/phases/workspace-and-config.md`** exists; **`conf/abd-config.json`** + **`active_skill_workspace`** documented; first process row uses **`0`** in **`#`** and the phase name **Workspace and config** (see standards doc).
- [ ] Phase files use **descriptive slugs**; order matches **`process.md`** and **`build.py`** (explicit order if not sort order).
- [ ] **`build.py`** phase list / merge keys updated when **`process.md`** changes.
- [ ] **Phase vs library:** Each **`phases/<slug>.md`** is **procedure** for that phase (steps, scripts, checklists)—**not** a dump of cross-phase definitions (**[`documentation-standards.md`](documentation-standards.md)** → *Library vs phase documents*; **[`rules/content-placement.md`](../../rules/content-placement.md)**).

**Ask:** “Phases in order?”

---

## 2. Rules (optional) & scanners

- [ ] Decided if **`rules/`** is needed.
- [ ] Listed planned **`rules/*.md`** files (one concern per file where possible).
- [ ] Decided scanner vs doc-only for each rule cluster.
- [ ] **Base framework** (when checks exist): read **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** — **`rules/scanners.json`** **`rule_scanner_bindings`** for each machine-checked rule; **`skill-config.json`** **`operator.build_pipeline`** lists ordered post-merge steps for **`build.py`**; **`operator.scanners`** lists the same scanner paths (or a superset) for **Operator** / CI.
- [ ] **`process.md`** does **not** treat scanners as phase-local “script column” noise; skill-level **Rules and automated checks** (or link to **`rules-and-automated-checks.md`**) instead.

**Ask:** “Machine-checked vs human-reviewed? What would each scanner inspect?”

---

## 3. Library — cross-cutting concepts (`content/parts/library/`)

- [ ] Cross-cutting content in **`library/<slug>.md`** (or skill-specific equivalent).
- [ ] **`build.py`** merge order matches how phases reuse library.
- [ ] Optional **index** (short links only: **`README`**, **`conf/build-strategy.json` notes**, or a **`docs/*` index** if non-runtime) — **not** a second home for bodies; full cross-cutting copy stays in **`library/`** (see **`docs/` vs parts** in **`skill-repo-standards.md`**).
- [ ] Same concept **names** across phases.
- [ ] **Library stays non-procedural:** **no** numbered “how to run a phase” sequences, **no** phase ordering story, **no** phase-specific **`python scripts/…`** runbooks—those stay in **`phases/`** and **`process.md`** (**[`rules/content-placement.md`](../../rules/content-placement.md)**).

**Ask:** “What repeats across phases → **library**?”

---

## 4. Agent delivery mode (`skill-config.json` → `delivery.mode`)

See **`abd-skill-builder`** [`delivery-modes.md`](content/parts/library/delivery-modes.md) (canonical: `skills/abd-skill-builder/content/parts/library/delivery-modes.md`).

- [ ] **`AGENTS.md`** assembled (both modes).
- [ ] **Injection / merge map** documented (paths per operation, order, equivalence to static) — **`README`**, **`build.py`**, or manifest — so mode can change later (narrative-only; sources remain under **`content/parts/`**).
- [ ] **`delivery.mode`** set: **`static_built`** or **`runtime_injection`**.
- [ ] If **`static_built`**: **`build.py`** run; **`content/built/`** (and peers) committed; traceable to map.
- [ ] If **`runtime_injection`**: runtime follows documented map (or deltas documented).

**Ask:** “Per operation: which files, which order, where is the lookup?”

---

## 5. `test/` — script tests & fixtures

- [ ] Chose: pytest **yes** or **no** (if no, skip pytest bullets; may still use **`test/`** for fixtures).
- [ ] If pytest **yes**: dev deps + **`pip install`** documented (**`requirements-dev.txt`** or **`pyproject.toml`**).
- [ ] **Run command** documented (e.g. **`python -m pytest test/`**).
- [ ] **CI** runs tests (optional).
- [ ] Tests live under **`test/`**; **`test/fixture/`** if needed.
- [ ] **`active_skill_workspace`** path under **`test/<name>/`** documented if set.

**Ask:** “What must stay green? Best fixture?”

---

## 6. Operator contract — “built the skill”

- [ ] **`SKILL.md`** + frontmatter.
- [ ] **`skill-config.json`** paths match disk.
- [ ] **`python scripts/build.py`** exits **0**.
- [ ] **Python compile check** on **`operator.compileall_paths`** passes (Operator uses Python’s **`compileall`** under the hood).
- [ ] **Scanner** scripts exit **0** (if any).

**Ask:** “Operator green?”

**Final:**

- [ ] **Attest** structurally built — **or** list gaps below.

---

## Gaps / follow-ups (free text)

Use for **resume notes** (date, last § completed, blockers):

```text


```

---

## How to use this file

1. **Ensure** **`docs/skill-plan.md`** has an **## Authoring checklist** section (scaffold injects from **`abd-skill-builder`** **`content/parts/library/authoring-checklist.md`**) before deep work.
2. Check **`- [x]`** only when done; **first unchecked** = resume point.
3. Pull updates from **`abd-skill-builder`** canonical copy when standards change.


---

### `skill-repo-standards.md`

# Skill repository standards (index + extras)

**Process approach (IDE, `process.md`, code vs AI phases, `generate_prompt`):** [`process-approach.md`](process-approach.md) — **start here** for how skills are **used** in Cursor / similar: **`AGENTS.md`** auto-loaded, **`@…/process.md`** for phase map, **code phases** vs **AI-chat phases**, **dynamic vs static** prompt generation.

**Full normative §3 (all subsections):** [`skill-standards-section-3.md`](skill-standards-section-3.md) — directory and content conventions (**§3.1**), rule naming (**§3.2**), assembly (**§3.3**), reference notes (**§3.4**): stages/phases/steps, process tables, optional domain+story-map pattern, `AGENTS.md` / `content/built/`.

**Rules + scanners + build pipeline (base framework):** [`rules-and-automated-checks.md`](rules-and-automated-checks.md) — **default** wiring: **`rules/scanners.json`** bindings, **`operator.build_pipeline`** for **`build.py`**, **`operator.scanners`** for Operator; **do not** hang scanners off individual **process** phases.

**Builder vs Operator (summary):** [`builder-vs-operator.md`](builder-vs-operator.md) — **scaffold / generation** path vs **`operator.run_operator()`** validation today.

**Authoring checklist (human + AI):** [`authoring-checklist.md`](authoring-checklist.md) — normative body merged into **AGENTS.md**; in each skill, work the **## Authoring checklist** section inside **`docs/skill-plan.md`** (scaffold injects this file there). **`- [ ]` / `- [x]`** so work can **resume after interruption** (first unchecked box = continue here). Covers scaffold verification, rules/scanners, **library**, **`delivery.mode`**, **`test/`**, operator.

**Migrating an existing skill:** [`../phases/plan-migrate.md`](../phases/plan-migrate.md) (**1b**) — inventory → compare to standards → **delta report** → **user chooses which gap IDs to fix**; then [`../phases/migrate.md`](../phases/migrate.md) (**2b**) — **execute** moves and patches for those IDs only (no silent full rewrites).

**Example delta (this repo):** [`../../docs/standards-delta.md`](../../docs/standards-delta.md) — `abd-skill-builder` inventory vs §3 (delivery, `content/built/`, docs, tests/fixture notes).

---

## Quick layout reminder (before reading the full §3)

| Area | Convention |
|------|------------|
| **Entry** | `SKILL.md` at skill root (frontmatter: `name`, `description`). |
| **Operator config** | `skill-config.json` — `operator.compileall_paths`, `operator.build_script`, **`operator.build_pipeline`** (post-merge steps for **`build.py`**), **`operator.scanners`** (Operator; align paths with rule-bound scanners). See **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**. |
| **Agent delivery** | `skill-config.json` — `delivery.mode`: **`static_built`** (pre-generate per-operation slices into **`content/built/`**) or **`runtime_injection`** (resolve the **same** sources at run time). **Only** that choice differs — always document **which paths** feed each operation, **merge order**, and **equivalence** to static output, in a **lookup** place (skill **`README.md`**, **`build.py`** manifest, or emitted manifest) so the team can switch modes later. **`AGENTS.md`** in **both** modes. See **`abd-skill-builder`** [`delivery-modes.md`](delivery-modes.md) (canonical: **`content/parts/library/delivery-modes.md`**). |
| **Authoring prose (normative for writers)** | [`documentation-standards.md`](documentation-standards.md) — voice, where content belongs, process tables; complements **`docs/` vs `content/parts/`** rule. |
| **Workspace routing** | **[workspace-and-config](../phases/workspace-and-config.md#skill-path-skill-workspace-and-configuration)** — **`skill_path`**, **`skill_workspace`**, **`conf/abd-config.json`** keys (**Workspace and config**). |
| **Build intent** | `conf/build-strategy.json` — strategize loads this **whole JSON**; **`skill_purpose`** must be non-empty for **`strategy_complete`** (minimum to finish strategize). Other keys are **siblings** that enrich **`strategy`** / **`builder_manifest`** — they are **not** part of the **`skill_purpose`** text. See **`agentic-skill-builder/README.md`** (Strategizer). |
| **Normative content** | `content/parts/` — process table rows are **phases**; **steps** inside phase files. Phase markdown files use **descriptive slugs** (`terms-mechanisms.md`, …) — **not** `phase-NN-…` or phase numbers in **H1** titles; pipeline order is **only** in `process.md` (# column) + `build.py` merge list (see **`skill-standards-section-3.md`**). **Column definitions** and required **workspace** row: **`process-table-standards.md`**. |
| **docs/ (non-runtime only)** | **`docs/`** is for material **not** consumed as merged/injected skill payload at operation time: **user manuals**, **migration/planning notes**, **architecture**, **`docs/skill-plan.md`** (plan + **Authoring checklist** section), **standards deltas**. In **abd-skill-builder**, **`docs/`** is only **`standards-delta.md`** — delivery merge order lives in **`README.md`**. **Do not** put markdown (or other assets) in **`docs/`** that **`build.py` merges**, **injects**, or **ships** as the runnable instruction body for phases/operations — that belongs under **`content/parts/`** (including **`library/`**, **`phases/`**, **`process.md`**, **`rules/`** as applicable). |
| **Library** | `content/parts/library/` — **cross-cutting meaning** reused across more than one phase: definitions, tables, glossaries, named concepts, artifact shapes. **Not** phase procedures, **not** step-by-step runbooks, **not** CLI blocks for a single phase, **not** pipeline order (that is **`process.md`** + **`phases/`**). The library **is** the home for that shared meaning; do not maintain a parallel “cross-cutting” layer elsewhere. **`docs/`** may hold a **short index** pointing into **`library/`**; **bodies** live in **`library/`**; merge order lives in **`build.py`**. See **`documentation-standards.md`** → *Library vs phase documents*. |
| **Phases** | `content/parts/phases/<slug>.md` — **person-to-process** instructions for **one** process-table row: I/O, **steps**, scripts, done criteria. **Link** to **`library/`** for deep definitions; avoid duplicating large normative blocks that belong in **`library/`** because multiple phases need them. |
| **Rules** | `rules/*.md` or `content/parts/rules/*.md`; optional `rules/scanners.json`. |
| **Scripts** | `scripts/build.py` (**required** — merge/injection driver; scaffold template is minimal; extend with explicit phase order + per-operation bundles as in **`abd-maps-models-specs`** when needed), scanners, optional `_config.py`. See **`authoring-checklist.md`** → *Base scaffold*. |
| **Tests & fixtures** | **`test/`** — all automated tests for the skill (pytest, smoke scripts, etc.) that exercise **`scripts/`**; optional **`test/fixture/<scenario>/`** for frozen inputs/snapshots; optional **`test/<workspace>/`** dirs when **`conf/abd-config.json`** uses **`active_skill_workspace`** (path relative to skill root). Example: **`abd-maps-models-specs/test/`** — workspace **`test/sample-workspace`**, optional fixture **`test/fixture/<scenario>/`**. **`abd-skill-builder`** itself **does include** **`test/`** (see **`test/README.md`** + **`test/fixture/toy-polite-dialogue/`**) even though **pytest `test_*.py` files** are still optional follow-ups — do not read “pytest wiring pending” as “no **`test/`** folder.” **Operator today** only runs a **Python compile check** on **`operator.compileall_paths`** (usually **`["scripts"]`**; implemented with **`compileall`**) — it does **not** install or run **pytest**. If automated tests are **in scope**, add the **wiring** below. |
| **Agent bundle (always)** | `AGENTS.md` — assembled agent bundle (skill-wide “how it works”); typically generated by `build.py`; **not** gated on `delivery.mode`. |
| **Built slices (operation-time, static mode)** | `content/built/` — pre-merged process + library + rules per skill layout when `delivery.mode` is **`static_built`**. |
| **Documentation focus (this skill only)** | Process plans, **rules**, and **docs** describe **what this skill does** — in positive, runnable terms for **this** package. **Do not** use them as a running commentary on how this skill **differs** from another skill, or why it **doesn’t** do something “because another skill does.” That is **local context in time**, not part of the durable skill. **Dependencies** (other skills, tools, repos, contracts) are **explicit** — names, links, versions — in a **Dependencies** section, `README`, or build-strategy notes. That is **not** the same as narrating deltas to sibling work. |

**Minimal valid skill:** `SKILL.md` + `scripts/build.py` + `skill-config.json` with operator block — see **`test/fixture/toy-polite-dialogue/`** in this skill (**`abd-skill-builder`**).

---

## When automated tests are asked for (pytest wiring)

If the skill should run **pytest** (or similar) under **`test/`**, do **not** assume it is already installed or wired into **`operator`** — add it explicitly:

| Step | What to do |
|------|------------|
| **Dependency** | Add **`pytest`** (and dev-only plugins if needed) to a **`requirements-dev.txt`**, **`pyproject.toml`** `[project.optional-dependencies] dev`, or the skill’s documented venv install step — **commit** the file so others can `pip install -r …`. |
| **Layout** | Tests live under **`test/`** (e.g. **`test/test_*.py`** or **`test/<suite>/`**); shared fixtures in **`test/fixture/`** or **`conftest.py`** as usual for pytest. |
| **Run command** | Document in skill **`README.md`** or **`test/README.md`**: e.g. `python -m pytest test/` from skill root (with venv activated). |
| **CI (optional)** | Add a workflow or monorepo job that installs dev deps and runs the same command. |
| **Operator** | **`operator.run_operator()`** does **not** run pytest by default. To gate releases on tests, extend **CI** or a **wrapper script**; only add **`test`** to **`compileall_paths`** if you intentionally want bytecode checks on test modules (unusual). |

---

## Operator checklist (machine-runnable)

1. `SKILL.md` present.
2. `skill-config.json` parses; `operator` block consistent with files on disk.
3. Python files on declared paths pass a **compile check** (Operator uses **`compileall`**).
4. `python scripts/build.py` exits 0.
5. Each listed **scanner** in **`operator.scanners`** exits **0** (and any step in **`operator.build_pipeline`** that **`build.py`** runs also exits **0** when you rely on **`build.py`** as the full local gate).
6. **`rule_scanner_bindings`** (in **`rules/scanners.json`** when used): each **`rule_file`** and **`scanner`** path exists.

---

## What greenfield scaffold should emit

**`scripts/scaffold_skill.py`** (and equivalent generators) should produce a **complete, runnable skeleton**: file tree, `skill-config.json`, phase markdown stubs, `rules/` / `conf/` as needed, runnable **`build.py`**, optional scanner stubs — **without** baking in customer-specific “gold” domain solutions (those belong in the target workspace, not the template).

This **`abd-skill-builder`** skill ships **templates + `scaffold_skill.py`** as the supported way to create that tree. **`operator.run_operator()`** then validates what is on disk; it does not scaffold new skills by itself.


---

### `skill-standards-section-3.md`

# §3 Skill package layout and content standards

**What this is:** Normative rules for how a **skill repository** is shaped — where **runtime** content lives (`content/parts/`, `rules/`, `build.py`), how **stages / phases / steps** relate, how **process tables** and **Refs** work, optional patterns (e.g. domain + story map), **rule file naming**, and **static vs dynamic** assembly of instructions. **How skills are used in the IDE** (AGENTS.md, `process.md`, code vs AI-chat phases, `generate_prompt`) is defined in [`process-approach.md`](process-approach.md) — read that first.

**How to use it:** Implement **§3.1–§3.4** when authoring or reviewing a skill. Tools and humans use the same rules; nothing here depends on any external “origin” document.

**Scope boundary — skills stay simple:** A **skill package** should express a **linear** pipeline: **stage → phase → (steps inside phase docs)**. The **process table** rows are **phases**, not steps. Keep skills deliberately sequential.

## 3.1 Directory and content conventions

**Hierarchy in the repo:** **Stages** group **phases**. Each **phase** has normative markdown (one file or section per phase, per skill); **steps** live **inside** that phase’s markdown — they are **not** separate rows in the master process table. See **Stages, phases, and steps** below.


| Area                            | Convention                                                                                                        | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Normative content**           | Under /`content/parts/`                                                                                           | Plans, operations, domain narrative — **not** dumped only in chat.                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `**docs/` (non-runtime)**       | /`docs/` at skill root                                                                                            | **User manuals**, **migration/planning notes**, **architecture**, **authoring checklists**, and **narrative** descriptions of delivery. **Do not** put markdown here that `build.py` **merges**, **injects**, or **ships** as the runnable phase/operation body — that belongs under `**content/parts/`** (including `**library/`**, `**phases/`**, `**process.md**`, `**rules/**`).                                                                                                                                   |
| **Phase markdown (source)**     | e.g. /`content/parts/phases/<descriptive-slug>.md`, or one doc per phase with step sections — paths vary by skill | **One row in the process table = one phase.** **Steps** (numbered sub-procedures, “Step 1…”, checklists) are written **inside** this markdown as **normative content of the phase**, not as their own table rows. **Do not** encode execution order in filenames or H1 titles (`phase-02-foo.md`, `# Phase 2 — …`): order belongs in `**process.md`** (the `#` column) and in `**scripts/build.py`**’s explicit file list. Use **stable descriptive** kebab-case slugs so renumbering the plan does not force renames. |
| **Built phase markdown**        | `content/parts/phases/built/<descriptive-slug>.md` and/or `content/built/…` per skill layout | **Generated** from source phase bodies + rules via `scripts/build.py`. **Authors do not hand-edit `built/`.** These files are **materialized instruction blobs** for **static** AI-chat phases and for **`static_built`** delivery — consumed by **`generate_prompt`** (or pasted into chat), **not** by “agents browsing the repo” as the primary UX. IDEs load **`AGENTS.md`**; see [`process-approach.md`](process-approach.md). Folder layout (`phases/built` vs `content/built`) is per skill; document it in **`README.md`**.                                                                                                                                                                                                            |
| **Atomic rules**                | `content/parts/rules/*.md` (or top-level `rules/` in simpler skills)                                              | One concern per file where possible; **names** should encode **phase** and/or **domain concept** + rule name (see §3.2). **Which phase inlines which rule** is declared in **`skill-config.json`** (`phase_rules`, `every_phase_rules`), not scattered in per-rule frontmatter lists.                                                                                                                                                                                                                                                                                                                                                                                               |
| **Roles**                       | `roles/*-role.md`                                                                                                 | One file per **user/agent role** the skill assumes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Process**                     | `content/parts/process.md` or staged process docs                                                                 | **Summary table: each row is a phase** (linked by **Ref** to phase markdown). Stages group those rows. **Steps** appear only **inside** the linked phase files.                                                                                                                                                                                                                                                                                                                                                        |
| **Library markdown**            | `content/parts/library/*.md` (or `parts/library/`)                                                                | **Cross-phase structure and meaning**: definitions, glossaries, artifact shapes, naming, invariants. **Not** phase-local procedures, pipeline ordering, or CLI runbooks—those live in **`process.md`** / **`phases/`** (see **Library vs phase documents** below).                                                                                                                                                                                                                                                     |
| **Repo-facing built artifacts** | `AGENTS.md`, `SKILL.md`, sometimes `README.md`                                                                    | Frequently produced by `scripts/build.py` (merge order per skill). **`AGENTS.md`** is what **IDEs and assistants typically load automatically** for the skill repo.                                                                                                                                                                                                                                                                                                                                                                |
| **Config**                      | `skill-config.json`                                                                                               | Name, version, **`phase_files`**, **`PHASE_LIBRARY_SLICES`**, **`phase_rules`** / **`every_phase_rules`** (ordered rule **stems** inlined per phase bundle — see [`process-approach.md`](process-approach.md)), **`phase_bundle`**, **`operator.compileall_paths`**, **`operator.build_script`**, **`operator.build_pipeline`** (post-merge steps for **`build.py`**), **`operator.scanners`** (Operator gate; align with rule-bound scanners) — skill-specific knobs. See **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** (base framework).                                                                                                                                                                                                                                               |
| **Scripts**                     | `scripts/`                                                                                                        | Operational entry points; may share `_config.py` patterns.                                                                                                                                                                                                                                                                                                                                                                                                                                                             |


### Stages, phases, and steps (how they relate)

**Order is always:** **Stage → Phase → Step** (coarse → mid → finest) — but **only the first two appear as rows** in the master process table. **Steps** are **inside** the phase markdown.


| Term      | Typical meaning                                                                                                                                                                                                                                                                                                                      | Example                                                                                  |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **Stage** | **Coarse pipeline slice** — groups many **phases**; may span days or sessions. Often a heading or section in `process.md` or a staged doc.                                                                                                                                                                                           | **Stage 1 — Extract Context**; **Stage 2 — Map and Model**; **Stage 3 — Specification**. |
| **Phase** | **One row** in the process summary table — the unit of “what we do next” with a **driver**: **human** or **AI actor**. The **Ref** column links to **phase** markdown. Phases answer “are we allowed to proceed?” and **contain** the detailed steps as normative body copy.                                                         | “Corpus audit — Phase N”; **Initiator / Actor** column = human vs AI.                    |
| **Step**  | **Sub-structure inside the phase’s markdown** — numbered instructions, checklists, “Step 1 / Step 2”, optional **suffix letters** (`5a`, `7a`) for companion script runs **within the same phase**. **Not** a row in the process table. Machine state (if any) may still reference `workflow_step` as a **sub-id** inside the phase. | Inside `modules-epics-scaffold-breadth.md`: “1. … 2. … 3a. rebuild index …”              |


**AI-driven phases — how the operation is delivered:** See **[`process-approach.md`](process-approach.md)**. In short: **code-driven** phases = run scripts as documented in the phase file; **AI-chat** phases = produce the instruction block via **`generate_prompt`**-style tooling in **dynamic** (assemble sections) or **static** (use pre-built phase markdown under `phases/built/` or equivalent). The **chat** follows that text; **`built/`** is not “the agent’s filesystem API.”

**Ordering (linear, inside the skill):** Stages order **major outcomes**. **Phases** run in **process table order** (each row = one phase). **Steps** follow the order **written inside** each phase document. **Parallel batches, fan-out, or merge** are **not** modeled as extra table rows; if needed, handle that **outside** the skill package (host app, orchestration, or scripts). **Phases** may **block** a later stage until accepted (e.g. “the indexer phase says rebuild chunks — do not start Stage 2 until accepted”).

**“Process” one-liner:** `content/parts/process.md` (or `parts/process.md`) often opens with a **single pipeline string** (e.g. Context → Foundational spine → …). That line is the **navigation spine**; the **table lists phases** (by stage); **authoritative step detail** lives inside each **Ref**’d phase file.

### Process tables, hyperlinks, and naming in the Ref column

**How the table is built**

- **Rows are phases**, not steps. Columns typically include: `#`, **Phase** (title — sometimes labeled “Step” in legacy tables; **semantically it is the phase**), **Initiator / Actor** (Human→Code, AI, Code), **Script** (if any), **What it does**, **Coverage**, **Ref**, **Inputs**, **Outputs**.
- **Ref** is the **hyperlink hub**: each row points to the **normative markdown for that phase**. **Steps** (numbered sub-procedures) live **inside** that file — not in separate table rows. Python entry points stay in **Script**, not **Ref**.
- **Two-tier phase files:**
  - **Source:** phase markdown authors edit (e.g. `content/parts/phases/<name>.md`, or `parts/steps/<name>.md` when the filename is the **phase** slug — naming varies by skill).
  - **Built:** `content/parts/phases/built/<name>.md` or `content/built/<name>.md` — **rules baked in** from `parts/rules/*.md` via `scripts/build.py`. **Steps remain inside** the built document. Used for **static** prompt generation and **`static_built`** slices — not hand-edited. See [`process-approach.md`](process-approach.md).
- **Cross-links inside the table:** The **Ref** column uses relative markdown links to the **phase** doc, e.g. `[context](parts/context.md)`, `[modules-epics-scaffold-breadth (built)](content/parts/steps/built/modules-epics-scaffold-breadth.md)` (paths vary by skill; **from the skill root** per `AGENTS.md`).

**Naming conventions visible in the table**

- **Phase titles** in the table read like **milestones or operations** (“Parse, curate, chunk, index”, “Integrate and Harmonize”) — stable labels for **phase** / workflow fields. **Finer labels** for **steps inside the phase file** may appear in JSON as `workflow_step` or similar.
- **Phase file names and H1 headings** must **not** duplicate pipeline indices (`phase-00-`, `Phase 3 —` in the title). Those numbers **change** when the plan evolves; **brittle** names churn git history and links. The **Ref** column and `build.py` define order; phase files stay **semantically** named (`story-map.md`, `canonical-context.md`).
- **Letter suffixes** (`5a`, `7a`) describe **sub-steps inside a phase** (e.g. companion script after a numbered step) — **inside the phase markdown**, not extra table rows.

### Concepts and cross-cutting artifacts (generic — all skills)

**This section is the generic rule.** A **skill** packages **concepts** (ideas, definitions, invariants, roles) and **artifacts** (outputs, schemas, manifests) that the workflow references across **multiple stages or phases**. Anything that would be **repeated** if pasted into every phase file should instead live in **its own file** (usually markdown under `content/parts/`, sometimes JSON alongside) so there is a **single source of truth**.


| Guideline           | Meaning                                                                                                                                                                                                         |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **When to extract** | If a concept or artifact **spans** more than one phase (or stage), give it a **dedicated** doc (or structured file) and **link** from phase bodies — do not duplicate long definitions in each phase.           |
| **Naming**          | Conventional filenames (`glossary.md`, `concepts.md`, `artifacts.md`, `roles/`*, etc.) vary by skill; **discover** and **validate** presence from templates and this skill’s `build.py`, not one global layout. |
| **Not every skill** | A minimal skill might only have `SKILL.md`, `content/parts/process.md`, and phase files — **no** separate “domain” or “story map” layer. That is valid.                                                         |


### Library vs phase documents (authoring split)

**`library/`** answers **what** (stable meaning for ideas and artifacts that **more than one** phase touches). **`phases/<slug>.md`** answers **how for this step** (operator procedure: inputs, outputs, ordered steps, **commands**, done checks).

| In **`library/`** | In **`phases/`** (not a second copy of the whole library) |
| --- | --- |
| Definitions, tables, schemas, vocabulary used across phases | Purpose of **this** phase, **steps**, checklists, **script/CLI** lines |
| Single source of truth for a construct that spans the pipeline | **Links** into the right **`library/`** shard for depth |
| Optional injection slices (`abd:begin` / `abd:end`) | **No** long normative essays that other phases would repeat verbatim |

**Do not** put **numbered phase procedures**, **order-of-operations** for the skill, or **phase-to-phase sequencing narrative** in **`library/`**—that belongs in **`process.md`** and the relevant **`phases/`** files. **Do not** park **large** reusable specs only inside one phase file if another phase needs the same text—extract to **`library/`** and link.

Normative detail for writers: [`documentation-standards.md`](documentation-standards.md) and [`../../rules/content-placement.md`](../../rules/content-placement.md).

### Optional pattern — domain narrative + interaction tree (maps-models–class skills only)

Some skills (notably **abd-maps-models-specs** and similar) **choose** to separate **two parallel artifacts** that must stay in sync. **Do not** treat this table as the default for **all** skills — only for skills that explicitly adopt this shape.


| Piece                            | Role                                                                                                                                                                                                    | Typical location (example skill)                                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Domain narrative**             | **State and structure** — modules, **domain concepts** (CRC-style: owns, properties, operations, `extends`, invariants), evidence hooks. Answers **what things are** and **what owns which rules**.     | e.g. `parts/domain.md` + evolving `map-model-spec.json` (`modules_and_epics`, `concepts[]`, chunk citations). |
| **Story map / interaction tree** | **Behavior** — epics, sub-epics, stories, scenarios; **Trigger / Response**; **Pre-Condition**; **Given/When/Then** where required. Answers **who does what** and how behavior references domain state. | e.g. `parts/story-map.md` + nested JSON under epics (`stories`, `sub_epics`, etc.).                           |


**When this pattern applies**

- **Same vocabulary:** Domain concept names (`concepts[].name`) and story references can be held to **one namespace** — scanners may enforce **exact string match** where the skill defines that rule.
- **Evidence ladder / paired edits:** Concepts may carry `evidence_stage`; **domain** vs **journey** edits are **paired** in skills that implement both files.
- Skills **without** this split still use the **generic** rule above: cross-cutting concepts → **their own** markdown (whatever the skill calls them), not repeated per phase.

### Rules and automated checks (default wiring)

For **machine-enforceable** rules, use the **base framework** in **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**:

- Declare **rule → scanner** bindings in **`rules/scanners.json`** (`rule_scanner_bindings`).
- List **ordered post-merge steps** under **`skill-config.json` → `operator.build_pipeline`**; **`scripts/build.py`** runs them after merges (same pattern as **`abd-maps-models-specs`**).
- Keep **`operator.scanners`** consistent with those scripts for **`operator.run_operator()`** / CI.

**Process tables** should **not** enumerate every scanner as if it belonged to a single phase; document automation at the skill level and link **`rules/scanners.json`** + **`build.py`** / **`build_pipeline`**.

## 3.2 Rule file naming (heuristic standard)

Target pattern (flexible regex for validation):

```text
{phase-or-stage}__{domain-concept-or-scope}__{short-rule-name}.md
```

Examples mirror **story synchronizer / maps-models** style: scanners and rules tied to **phase** and **concept** (e.g. `chunks_must_be_referenced`, `concept-layering-scaffold`). **Propose** names from the **phase** + concept + verb (and step text inside the phase doc if needed), then **check uniqueness** under `parts/rules/`.

## 3.3 Assembly model (static vs dynamic)

**Two different “static vs dynamic” pairs** — do not conflate:

1. **`build.py` assembly** (repo artifacts): Each skill ships `scripts/build.py`. It merges **process + library + phases (+ rules)** into **`AGENTS.md`** and optional **`content/built/`**. Flags like `--assembly static|snapshot` are **per skill** when present.

2. **AI-chat prompt generation** (`generate_prompt`): For **AI-driven** phases only — **dynamic** = assemble instruction string from sections; **static** = emit text from **pre-built** phase file under `phases/built/` (or documented path). See [`process-approach.md`](process-approach.md).

**Per skill:** `build.py` is the **authoritative** merge driver for **this** repo; scaffolding **emit or check** trees — they do **not** replace `build.py`.

**Flag on `build.py`:** The skill’s `build.py` may expose **CLI flags** for snapshot vs interactive merge; exact names are per skill. For **prompt** modes, document **`generate_prompt`** (or equivalent) next to **`build.py`** in **`README`** / **`AGENTS.md`**.


| Mode (merge / delivery) | Mechanism                                                                               | When                                                               |
| ----------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Static (merge)**      | `build.py` merges **built-phase** fragments into `AGENTS.md` / `SKILL.md` (and related) | Release, reproducible snapshot; CI; “what ships”.                  |
| **Dynamic (merge)**     | Runtime concatenation by **phase** / **operation** from `skill-config.json` + manifest  | Interactive sessions, partial rebuild, IDE-driven iteration. |


A **host** (CI, IDE, or orchestrator) may emit an **internal** manifest (JSON or YAML) for a **given generation run**, listing which fragments form which artifact for both modes; the skill’s `build.py` **may read** that manifest (or embedded config) when implementing **static** merges and documents how **dynamic** mode resolves fragments at runtime. That manifest is **optional** and **not** a standard every skill must carry — only **documented** `build.py` behavior is.

## 3.4 Reference skills (illustrative)

Other skills in the monorepo **illustrate** patterns (long `AGENTS.md`, phased pipelines, rules + scanners). They are **examples**, not extra requirements. **Operator** checks and layout rules are grounded in **abd-skill-builder** library files and each skill’s **`skill-config.json`** — not in a separate “corpus” file unless your team adds one.


---

### `builder-vs-operator.md`

# Builder vs Operator (today)

**Generation / scaffold (“builder” in the loose sense):** Anything that **emits** a new skill tree — typically **`abd-skill-builder`’s `scripts/scaffold_skill.py`** plus templates — producing `SKILL.md`, `skill-config.json`, phase markdown, `rules/` stubs, `scripts/build.py`, optional scanners. Output should match **§3** layout and avoid embedding customer “gold” solutions in the template.

**Operator (structural gate):** **`agentic-skill-builder`** **`operator.run_operator()`** — validates `skill-config.json`, runs a **Python compile check** on the paths in **`operator.compileall_paths`** (the implementation uses Python’s **`compileall`** module), runs **`operator.build_script`** (typically `python scripts/build.py`), then runs **scanner scripts** listed under **`operator.scanners`**. A normative skill also declares **`operator.build_pipeline`**: the **ordered post-merge steps** that **`build.py`** runs after writing **`AGENTS.md`** / built slices (rule-bound scanners, emitters, manifest, lint—**per skill**). **Rule → scanner** bindings live in **`rules/scanners.json`**; see **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** (base framework for all skills). Operator does **not** create greenfield skills; that is **`scaffold_skill.py`** and authoring.

**This skill’s role:** Ship **standards** under **`content/parts/library/`**, **process + phases**, **`scaffold_skill.py`**, and **templates** so authors get a compliant tree first, then Operator keeps it green.


---

### `rules-and-automated-checks.md`

# Rules and automated checks (base framework for every skill)

**Status:** **Normative default** for Open Agent Skills in this repo. When a skill defines **governance rules** (`rules/*.md`) and wants **machine enforcement**, wire checks this way—not as one-off phase script call-outs.

## What owns what

| Layer | Owns |
| --- | --- |
| **`rules/<stem>.md`** | The **human-readable rule**: scope, must/should, examples, done criteria. |
| **`rules/scanners.json`** | **Which script enforces which rule** — `rule_scanner_bindings[]` maps `rule_id` + `rule_file` → `scanner` path (relative to skill root). Optional top-level **`scanners`** lists scanner scripts for tooling that expects a flat array. |
| **`skill-config.json` → `operator.build_pipeline`** | **Ordered post-merge steps** that **`scripts/build.py`** runs after it writes **`AGENTS.md`** / **`content/built/`** (or your skill’s equivalent). Entries are typically **`scripts/...py`** paths: rule-bound scanners, emitters, manifest generators, rule-example linters, etc. **Empty or omitted** means “merge only” (skills with no automated checks yet). |
| **`skill-config.json` → `operator.scanners`** | **Operator / CI gate** — paths **`agentic-skill-builder`** **`operator.run_operator()`** runs **after** **`operator.build_script`**. **Keep these paths aligned** with the scanner steps you care about (usually the same modules listed in **`build_pipeline`** and/or **`rules/scanners.json`**), so “green build” and “green operator” mean the same checks. |

## What you do not do

- **Do not** treat **scanners** as **phase-owned scripts** in **`process.md`** process tables. Phase rows are for **human/AI procedure** and **merge / emit** entry points (e.g. `python scripts/build.py`), not for listing every validator. If readers need detail, add a short **“Rules and automated checks”** subsection in **`process.md`** that points here and to **`rules/scanners.json`**.
- **Do not** bind scanners only in prose. If a rule is machine-checked, add a **`rule_scanner_bindings`** row and a **`build_pipeline`** step (and **`operator.scanners`** / Operator docs as required by your host).

## Execution flow (mental model)

1. Author edits **`content/parts/`**, **`rules/`**, **`skill-config.json`**.
2. **`python scripts/build.py`** merges instruction bundles, then runs **`operator.build_pipeline`** in order (if present).
3. **Operator** (or CI) runs compile check → **`build.py`** again → **`operator.scanners`** (when configured).

**Reference implementation:** **`abd-maps-models-specs`** — `rules/scanners.json`, **`operator.build_pipeline`** in **`skill-config.json`**, and **`scripts/build.py`** driving the pipeline after merge.

## Scaffolded skills

Greenfield trees from **`scaffold_skill.py`** should ship **`rules/scanners.json`** (even if bindings start empty) and a **`skill-config.json`** fragment that includes **`operator.build_pipeline`** alongside **`operator.scanners`**, so authors extend **one** pattern instead of inventing ad hoc wrappers.

See also: **[`skill-standards-section-3.md`](skill-standards-section-3.md)** (§3.1 config row), **[`builder-vs-operator.md`](builder-vs-operator.md)**, **`rules/README.md`** at the skill root.


---

## Rules

*No rules for this phase. List rule stems (filename without `.md`) under `skill-config.json` → `phase_rules` for this phase slug, and optionally `every_phase_rules` for rules that apply to every phase. See `parts/library/process-approach.md` § Phase bundle — rules.*


---

## Phase: fill-scaffold-parts

## Principles

**AI quality — normative rules, scanners, and review.** This shard is injected under **`## Principles`** in phase bundles; the heading above is added by the assembler.

**Scope:** In **abd-skill-builder**, this file is injected as **`## Principles`** and is the **first** section in each AI-chat phase bundle (`python scripts/generate.py --phase <slug>` and `content/parts/phases/built/<slug>.md`). Read it **before** Role, Phase body, Library shards, and Rules for that phase.

---

**Every rule in `rules/` is two things at once:** (1) **Normative advice** — prose the model follows while authoring **`content/parts/`**, **`rules/`**, **`skill-config.json`**, and other skill artifacts. (2) **Checkable expectations** — where this repo ships a **scanner** under **`scripts/`**, it catches common layout or config misses; where it does not, **you** still review against the rule text.

**Example (wrong):** Treating a green **`python scripts/build.py`** as enough while **`AGENTS.md`** still disagrees with **`content/parts/`** or **`phase_rules`** omits a rule you claimed to enforce.

**Example (correct):** Read the **Rules** section in this bundle, align files with **`library/`** norms, run **`python scripts/build.py`** (and **`operator.scanners`** when configured), then **re-read** outputs against each applicable rule.

---

## Layer 1 — Generate with rules

While generating or editing skill artifacts:

- Apply **`rules/*.md`** inlined into this bundle (and related **`library/`** docs).
- Prefer **DO / DON’T** and **good vs bad** fragments inside each rule — they are the contract for *shape*, not only for CI.

---

## Layer 2 — Mechanical checks (this skill)

After you have files on disk, the pipeline can run:

| Mechanism | What it does |
| --------- | ------------ |
| **`python scripts/build.py`** | Merges **process** + per-phase bundles into **`AGENTS.md`** and **`content/built/`**, then runs **`operator.build_pipeline`** (e.g. **`scripts/scanner_skill_builder_layout.py`**) when configured. |
| **`rules/scanners.json`** | Declares **rule → scanner** bindings when your skill uses them; align with **`operator.scanners`**. |

**Example (wrong):** Hand-editing **`AGENTS.md`** while **`build.py`** is supposed to own the merge.

**Example (wrong):** Adding a scanner only in prose — no **`rule_scanner_bindings`** or **`build_pipeline`** step.

**Example (correct):** Fix issues reported by scanners, re-run **build**, keep **`skill-config.json`** paths honest.

Scanners are **necessary** for what they implement; they are **not sufficient** for semantic quality (e.g. a valid tree that still mis-describes what the skill does).

---

## Layer 3 — Adversarial pass (human or AI)

With clean tool output, still ask:

- Does each **rule** that applies to this phase pass **by intent**, not only by letter?
- Would a reviewer see **drift** between **`SKILL.md`**, **`process.md`**, and **`phases/`** even when the tree validates?

Use the **Corrections format** below when fixing issues.

---

## Corrections format

When recording or fixing a problem:

| Field | Content |
| ----- | ------- |
| **Rule** | Rule id or `rules/<file>.md` name |
| **Example (wrong)** | What was done incorrectly |
| **Example (correct)** | What it should be |
| **Scanner or validator** | If applicable — see **`rules/scanners.json`** and **`operator.build_pipeline`** |
| **Likely source** | One of: prompt gap · rule not read · edge case · automation gap |

---

## Do not bypass the documented pipeline

**AI phases** mean: read inputs, reason, update the **source** files this skill owns under **`content/parts/`**, **`rules/`**, and config — not one-off scripts that rewrite merged outputs **instead** of fixing sources. Automation that ships with the skill lives under **`scripts/`** and is wired through **`skill-config.json`** (**`build.py`**, **`build_pipeline`**, **`operator.scanners`**) as documented in **`library/rules-and-automated-checks.md`**.

**Example (wrong):** Patching **`AGENTS.md`** directly to “pass” review while **`process.md`** is unchanged.

**Example (correct):** Edit **`content/parts/`** (or **`rules/`**), run **`python scripts/build.py`**, commit regenerated **`AGENTS.md`** / **`content/built/`** when using **`static_built`**.


---

## Phase

# Phase — Fill scaffold (library and rules)

This is **phase 2c** in [`../process.md`](../process.md) (**Stage 2 — Create or fix the skill**). It runs **after** **[scaffold](scaffold.md)** (**2a**) or **[migrate](migrate.md)** (**2b** — **execute** after **1b**) when a **tree** already exists. The scaffold **creates directories and templates**; this phase **fills them** with the **instructional content** the skill actually runs on: **`content/parts/library/**`**, **`rules/**`**, and—where needed—**richer `content/parts/process.md`** and **`phases/*.md`**.

**Not in scope:** running **`scaffold_skill.py`** again, or replacing **`scripts/build.py`**. **In scope:** collaborative **authoring** (human + AI) so **library** chunks and **rules** match **SKILL.md** purpose, **`docs/skill-plan.md`**, and the **process** you sketched.

Emit this file for an AI session with:

```bash
python scripts/generate.py --phase fill-scaffold-parts
```

(Or `python scripts/generate_prompt.py --phase fill-scaffold-parts`.)

---

## Purpose

Turn a **hollow** or **minimal** skill package into one whose **merged** agent bundle (**`AGENTS.md`**) and **built** slices honestly describe **how** the skill works. The AI **interprets** the skill’s **intent** (purpose, suggested phases, suggested rules, delivery hints) and **proposes concrete files**: definitions in **`library/`**, must-holds in **`rules/`**, and edits to **`process.md` / `phases/*.md`** where the scaffold left placeholders. The **user** confirms domain facts, rejects bad shortcuts, and owns final wording.

This is **not** “have the model freestyle in chat.” It is **structured authoring** against the same **norms** as any other skill: **[`../library/authoring-checklist.md`](../library/authoring-checklist.md)**, **[`../library/skill-repo-standards.md`](../library/skill-repo-standards.md)**, **[`../library/skill-standards-section-3.md`](../library/skill-standards-section-3.md)**.

---

## What to read first (in the skill under construction)

| Source | Why |
| --- | --- |
| **`SKILL.md`** | Declared purpose, frontmatter, what the skill *is for*. |
| **`docs/skill-plan.md`** | Plan, **Authoring checklist** progress, phases/rules you already named. |
| **`content/parts/process.md`** | Staged flow—even if minimal—defines **order** and **phase slugs**. |
| **`skill-config.json`** | **`delivery.mode`**, **`operator`**, paths **build** and scanners use. |
| **`conf/`** (as applicable) | **[Workspace and config](workspace-and-config.md)** — **`abd-config.json`**, **`active_skill_workspace`**. |
| **Existing `content/parts/phases/*.md`** | Skeleton or empty—**extend**, don’t duplicate the **process** table blindly. |

If **`library/`** or **`rules/`** already has files (e.g. after **migrate**), **revise** before adding parallel ad-hoc docs elsewhere.

---

## What to produce

| Area | Target |
| --- | --- |
| **`content/parts/library/*.md`** | Cross-cutting definitions, tables, glossaries, **delivery** notes—**one home** for concepts reused across phases (see **`skill-repo-standards`**). |
| **`rules/*.md`** (and **`rules/scanners.json`** if used) | Must-holds the agent and tooling should enforce; align with **`skill-config.json`** scanners when you add them. |
| **`content/parts/process.md` / `phases/*.md`** | Replace placeholders with **steps** that match the **#** column and **`build.py`** merge order (when the skill’s **`build.py`** lists phases explicitly). |

Everything you add must **merge** cleanly: no instruction bodies that belong in **`parts/`** stranded under **`docs/`** (except non-runtime docs like plans—already in **`docs/skill-plan.md`** per norms).

---

## Prompt contract — how the AI should work (follow in order)

1. **Restate the skill’s purpose** in one short paragraph (from **`SKILL.md`** + **`docs/skill-plan.md`**). If unclear, **ask** the user before inventing domain rules.

2. **Map process to files:** From **`process.md`**, list **phase slugs** and ensure each has a **`phases/<slug>.md`** (or a documented exception). Flag **gaps** between the **table** and **`phases/`** on disk.

3. **Design `library/`:** Propose **which** library files you need (names mirror **concepts**, not random `misc.md`). Each file should have a **single** role (definitions vs delivery vs checklist pointers). Pull **cross-cutting** text out of phase files into **`library/`** when two or more phases would repeat it. **`library/`** must stay **non-procedural**: definitions and structure only—**not** step-by-step phase execution, **not** CLI runbooks, **not** pipeline order (**[`documentation-standards.md`](../library/documentation-standards.md)** → *Library vs phase documents*).

4. **Design `rules/`:** Turn “suggested rules” from the plan into **actionable** rule files—**testable** where possible. Connect rules to **scanners** only when the skill **defines** those scanners; otherwise keep rules as **agent** constraints.

5. **Collaborate:** After each batch of proposed paths, **stop** for user confirmation on: domain terms, **must** vs **should**, and **out-of-scope** behavior.

6. **Run the merge check:** After edits, run **`python scripts/build.py`** in the **skill under construction** and fix **source** files until **build** succeeds—**never** hand-edit **`AGENTS.md`** if **build** owns it.

---

## Success criteria

- **`library/`** holds **shared meaning** (definitions, shapes, vocabulary) the phases **link** to; **`phases/`** holds **procedures** (steps, scripts, checks)—not duplicated long essays, and **not** the reverse (procedures hiding in **`library/`**).
- **`rules/`** reflects **must-holds** the user agreed to, consistent with **`skill-config.json`** where wired.
- **`process.md`** phase table and **`phases/*.md`** **agree** on slugs and order (and with **`build.py`** if the skill uses an explicit phase list).
- **`python scripts/build.py`** exits **0**; **`AGENTS.md`** reflects the new content.

---

## See also

- **[Workspace and config](workspace-and-config.md)** — **`skill_path`**, **`conf/abd-config.json`**, **`active_skill_workspace`**.
- **[Scaffold](scaffold.md)** — **2a** (tree creation).
- **[Migrate](migrate.md)** — **2b** (apply **1b** delta).
- **[Plan skill migration](plan-migrate.md)** — **1b** (inventory + **standards delta**).
- **[Plan Script Build](plan-script-build.md)** — **1a** (plan before scaffold).


---

## Library



---

### `documentation-standards.md`

# Skill documentation standards

**Canonical:** `skills/abd-skill-builder/content/parts/library/documentation-standards.md` (merged into **`AGENTS.md`**).

Use these rules when you author or refactor **process**, **phase docs**, optional **`docs/`** reference, staged **`content/built/`** output, and **AGENTS.md** for any Open Agent Skill. They prevent tangled cross-cutting docs and unreadable process prose.

## Delivery mode (`static_built` vs `runtime_injection`)

Declare **`delivery.mode`** in **`skill-config.json`** (default **`static_built`**). That flag answers whether the agent relies on **checked-in** **`content/built/`** + **`AGENTS.md`** or on **runtime** assembly from **`rules/`**, library fragments, and phase manifests. Normative definitions, when each applies, and how the two stay in sync are in **`delivery-modes.md`**.

## Workspace configuration

Skills that **route** to a customer tree keep **`conf/abd-config.json`** at **`skill_path`** with **`active_skill_workspace`** (and optional **`known_skill_workspaces`**). The file is **part of the repo**—**edit `active_skill_workspace`** to point at the workspace root (see **[workspace-and-config — Skill path, skill workspace, and configuration](../phases/workspace-and-config.md#skill-path-skill-workspace-and-configuration)**). A host (e.g. SkillField) may override. The install folder does **not** hold the customer project—only pointers. Workspace-local parameters live under **`skill_workspace/conf/`** per skill docs. Do not leave “where we run” only in prose unless the skill documents overrides.

## Agent-facing vs reference (read this first)

**If text is merged into `AGENTS.md`, injected into prompts, or otherwise part of the agent bundle, it belongs under `content/parts/`** (e.g. `process.md`, `phases/<phase>.md`, shared fragments). It does **not** live “only in `docs/`” with the expectation that the agent will see it unless your build copies it in.

**Staged build (`content/built/`):** When a complete file is **assembled** from pieces—e.g. a **base** plus **rules** plus **operator/story roles**—write the **intermediate, fully expanded** markdown under **`content/built/`** (or `content/parts/built/` / `phases/built/` if the skill already uses that layout). Then the final step generates the **complete** artifact (`AGENTS.md`, a single phase handoff, etc.). Do not skip the staged output if you need to diff or review what rules were baked in. (Example pattern: `abd-solution-modeler` uses `phases/built/` for phase specs.)

**`docs/`:** Use for **long-form reference** that operators (or tools) open beside the skill—principles, execution order, invariants, **and** standalone construct write-ups (schemas, package layout) **when** those are **not** duplicated as the sole copy of agent instructions. Phase tables and “what you must do” for the agent still live in **`content/parts/`**; `docs/` may **link** to the same ideas or hold deeper detail. If a norm must be in the agent’s context, mirror or generate it from `content/parts/`, not only from `docs/`.

## Voice and role

Write for the **operator** in **second person** (you, your). Frame the work clearly:

- **Your role** — What you are responsible for in this stage or skill (one or two sentences).
- **What you must do** — Imperatives and phase order (use bullets for several short obligations).
- **What you produce** / **How you know you succeeded** — Outcomes and done criteria.

Prefer **you must**, **you will**, and **then you** (sequence) over passive voice (“the pipeline establishes,” “artifacts are emitted”). Say who runs a script or makes a decision.

## Where content belongs

| Kind | Put it here | Do not |
| --- | --- | --- |
| **Process spine** — stages, phase numbers, tables, links to phase files | `content/parts/process.md` (or skill’s `content/process.md`) | Paste the entire phase table again as a second narrative. |
| **Phase behavior** — steps, checklists, **script invocations**, file paths for **this phase only** | `content/parts/phases/<phase>.md` | Split one phase across three cross-cutting docs; **duplicate** long cross-phase definitions—**link** to **`library/`** instead. |
| **Library shards** — definitions, glossaries, artifact shapes, naming, invariants for ideas that **span multiple phases** | `content/parts/library/<topic>.md` | Phase-local procedures, numbered runbooks, pipeline order, or “run `python scripts/…`” blocks that belong in **`phases/`**. |
| **Baked agent instructions** — bases + rules + roles merged before `AGENTS.md` | Source fragments under `content/parts/`; **output of merge** under `content/built/` (or `phases/built/`) **before** final generation | Edit only the final `AGENTS.md` by hand when a build step should own the merge. |
| **Standalone construct reference** — one artifact contract (schema, validators, chunk layout), diagrams, deep dives | `docs/<descriptive-name>.md` | Treat `docs/` as the **only** place agent-facing norms live; duplicate the “must do” into `content/parts/` or generate into `content/built/`. |
| **Cross-cutting** — principles, execution order, invariants that apply across phases | Usually `docs/` or `content/parts/library/` (e.g. principles prose); **governance rules** that vary by phase: **`skill-config.json`** → **`phase_rules`** / **`every_phase_rules`** + `rules/*.md` (see **`process-approach.md`**). **Link** from `content/parts/` where needed | Restate every phase inside cross-cutting docs; **link** to the process table instead. |

**Reference-doc filenames:** Do **not** prefix `docs/` filenames with phase numbers (e.g. avoid `phase2_terms.md`). Use **descriptive kebab-case** slugs (`terms-mechanisms-contract.md`, `behavioral-story-map.md`). Phase order belongs in `process.md` and `content/parts/phases/`, not in filenames.

**Cross-cutting** is for rules and order that are **not** naturally owned by a single phase. If the text is really about one phase only, prefer that phase’s file in `content/parts/phases/` plus a thin pointer from `docs/` if you keep a global index there.

## Library vs phase documents (split responsibility)

Use this split in **every** skill that has both **`library/`** and **`phases/`**:

- **`library/`** = **structure and meaning** shared across phases (what a thing *is*, how it is named, what fields exist, how it relates to other ideas). Think **reference** and **single source of truth** for multi-phase concepts.
- **`phases/*.md`** = **execution** for one pipeline step (what *you* do next, in order, including **commands** and **done checks**). Think **operator procedure** for *this* phase only.

**Hard bars**

| Layer | Must include | Must not be (move or trim) |
| --- | --- | --- |
| **`library/`** | Stable definitions, tables, schemas, cross-phase vocabulary | Long “how to run this phase” sections; **step sequences**; **script/CLI** runbooks; **phase ordering** or “after phase X…” workflow story |
| **`phases/`** | Short purpose, I/O, **steps**, script lines, checklists, **links** to **`library/`** for deep defs | Entire glossaries or artifact specs duplicated from **`library/`**; normative essays that belong in **`library/`** because **other phases** need the same text |

If a paragraph would still make sense **after renumbering or reordering phases**, it probably belongs in **`library/`** or **`rules/`**, not inside a single **`phases/<slug>.md`**.

**Governance rule in this repo:** [`rules/content-placement.md`](../../rules/content-placement.md).

## Prose style

- Several **short** points → **bullets**.
- One developed idea → **sentences** in a **paragraph**.
- Avoid long **semicolon chains** pretending to be one sentence.
- Avoid narrating **migration** from an old doc or old skill (“formerly §2.6”). Describe **this** skill only.

## Process tables

Keep the **stage narrative** at **intent and outcome**. The **table** holds actors, scripts, refs, and deliverable paths.

Normative column meanings, the required **workspace** phase (**Phase 0** informally), **`Input`/`Output` rules**, and **`build.py`/`generate.py` alignment** are in **[`process-table-standards.md`](process-table-standards.md)**. Use that doc whenever you create or refactor **`process.md`** in another skill.

Optional: an extra **Summary** column per row (**two or three sentences**) is allowed if you keep the abd-skill-builder **seven-column** shape as the default—do not drop **Input** / **Output** / **Scripts** in favor of summary-only rows. For the **maps-models-specs**-style table (**`Script`**, **`Outputs`**, **`Ref`**), put **`Summary`** in the **third** column (after **`#`**, **Phase**) and **`Ref`** **last**—see **`process-table-standards.md`** § Maps / models / specs pipeline table.

## When you edit

1. Update the **smallest** place: phase file or construct doc first.
2. If you are repeating script names and outputs that are **already** in the table, **delete** the repetition and keep purpose or pointer to `phases/`.
3. Regenerate **AGENTS.md** after changing `content/` so agents see the update.


---

### `process-table-standards.md`

# Process table standards (for `process.md`)

**Use this** whenever you author or refactor **`parts/process.md`** (or **`content/parts/process.md`**) so skills stay consistent with **abd-skill-builder** and Operator expectations. Pair with **`skill-standards-section-3.md`** (stages / phases / steps) and **`documentation-standards.md`** (voice, where content lives).

---

## Workspace phase (“Phase 0”) — required for every skill

Every skill that can target a **project tree** or needs unambiguous **where am I running?** semantics must include a **workspace** phase:

| Item | Rule |
| --- | --- |
| **Phase file** | **`parts/phases/workspace-and-config.md`** (or under **`content/parts/phases/`** if your skill uses that layout). Slug: **`workspace-and-config`**. |
| **Process row** | First process-table row **after** any “standards / checklist” preamble; **#** column **`0`** (Phase 0 — workspace first in the pipeline). **Team process plate** (`process-team.md.template`) hard-codes this row; **do not** rename the **Phase** link text to **`Phase 0 — …`** inside the table cell—keep the stable slug title **Workspace and config**. |
| **Heading & name** | Phase document **H1** and links: **Workspace and config** (not **Phase 0 — …** in the phase file’s **H1**). In **`parts/process.md`**, the **section** heading **Phase 0 — Workspace and config** is OK; the **process table** still uses the stable **Phase** column title above. |
| **Config** | **`conf/abd-config.json`** at **`skill_path`** with **`active_skill_workspace`** (and optional **`known_skill_workspaces`**). Same **JSON shape** across skills; see **abd-skill-builder** reference **`conf/abd-config.json`**. |
| **Merge / generate** | **`build.py`** should list **`workspace-and-config`** **first** in the phase merge list when that file exists; **`generate.py --phase workspace-and-config`** must resolve for AI-chat steps. |
| **CLI — `active_skill_workspace`** | Every scaffolded skill includes **`scripts/set_workspace.py`** (copied from **abd-skill-builder**). **Process** row **0** **Scripts** cell must include the same wording as **abd-maps-models-specs** phase **Set workspace**: `` `python` [`scripts/set_workspace.py`](…) — no args prints current; `<path>` sets `active_skill_workspace` in `conf/abd-config.json` ([workspace-and-config](phases/workspace-and-config.md)) `` — then **`·`** and **`generate.py`** for the AI-chat phase when both apply. |

Routing details are **not** duplicated inside **Plan** or **Scaffold** phase bodies—**link** to **`workspace-and-config.md`**.

---

## Process table columns (abd-skill-builder shape)

Use this **seven-column** header (exact labels help readers and tooling):

| Column | Meaning |
| --- | --- |
| **`#`** | **Phase id** in the pipeline: **`0`** for workspace (Phase 0); **`1a` / `1b`** for plan variants; **`2a` / `2b` / `2c`** for create/fix/fill; **`3`** for operator; or your skill’s own scheme. **Order** is this column + stage sections—not filenames. |
| **Phase** | **Linked title** to **`phases/<slug>.md`**. Stable, descriptive name (not `phase-02-foo.md` in the link text). |
| **Description** | **What happens** in this phase: decisions, constraints, pointers to other phase docs for cross-cutting topics. **Not** a second copy of the whole phase file—enough to choose the right doc. |
| **Actor** | **Who runs it:** Human / AI, Code, Human / AI + Code, etc. |
| **Input** | **What you must have** to start: paths, prior artifacts, CLI flags, **not** the phase’s primary deliverable if that deliverable is produced **in** this phase (avoid listing **`docs/skill-plan.md`** as **Input** for **1a** when **1a** creates that file—use *library norms + target workspace* instead). |
| **Output** | **Concrete artifacts** when the phase is done: files, directories, exit criteria. For **scaffold (2a)**, lead with the **scaffolded skill tree** ( **`SKILL.md`**, **`skill-config.json`**, **`conf/`**, **`content/parts/`** or **`parts/`**, **`scripts/`**, **`rules/`**, **`test/`**, **`docs/skill-plan.md`** ), then **`AGENTS.md` / `content/built/`** after **`build.py`**—not only the skill-plan template. |
| **Scripts** | **Commands** with **entry script names**: `python scripts/generate.py --phase <slug>`, `python scripts/build.py`, **`scaffold_skill.py`**. **Do not** pack **rule-bound scanners** here—those are skill-wide; document them under **Rules and automated checks** (see **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**) and run them via **`build.py`** / **`operator.build_pipeline`**. One cell; use **`·`** between multiple commands. |

**Do not** use a vague **Output** that only points at a **template file** when the real outcome is a **written document** or **directory tree**—say the **path** under the skill (e.g. **`docs/skill-plan.md`**).

### Maps / models / specs pipeline table (seven columns, `Script` + `Outputs` variant)

Skills such as **abd-maps-models-specs** use the **same seven-column count** with different labels: **`#`**, **Phase**, **Summary**, **Actor**, **Script**, **Outputs**, **`Ref`**.

- **`Summary`** is the **third** column (after **`#`** and **Phase**) so wide prose sits early in the row and previews well in Markdown renderers.
- **`Ref`** is the **last** column (phase doc links stay the right-hand anchor).

Keep **exact header labels** (**`Outputs`** for concrete artifacts and paths) so tables stay consistent across stages.

---

## Stages vs tables

- **Stage** sections (**`## Stage N — …`**) carry **narrative**: purpose, what you produce, how you know you succeeded.
- **Tables** carry **rows = phases**: Ref, Actor, Input, Output, Scripts. **Steps** stay **inside** phase markdown files, not extra table rows (per §3).

---

## Language

- **Second person** for operator-facing prose in phase files (**you**, **your**); see **`documentation-standards.md`**.
- **Process one-liner** at the top of **`process.md`**: pipeline string with **linked phase names** (e.g. **Workspace and config** → **Plan** → …).
- **Routing** cells: short **“Routing: [Workspace and config](…)—not repeated here.”** instead of repeating **`conf/`** keys.

---

## `build.py` and `generate.py` alignment

When you add or rename a phase:

1. **`parts/phases/<slug>.md`** exists.
2. **`process.md`** has a row with that **Phase** link and **`#`** id.
3. **`scripts/build.py`** — **`PHASE_FILES`** (or equivalent) lists **`slug`** in merge order; **`LIBRARY_FILES`** lists library shards in order.
4. **`scripts/generate_prompt.py`** — resolves **`parts/phases/<slug>.md`** (or **`content/parts/phases/`**); **`generate.py`** stays the thin CLI that delegates to it.
5. Regenerate **`AGENTS.md`** / **`content/built/`** after edits.

---

## Reference

- **Worked example:** **`parts/process.md`** in **abd-skill-builder**.
- **Rich pipeline doc:** **`templates/process-team.md.template`** (team process plate).
- **Workspace normative body:** **`parts/phases/workspace-and-config.md`**.


---

### `delivery-modes.md`

# Agent delivery modes (static build vs runtime injection)

Skills can hand instructions to an **agent** or **executor** (including an EA / orchestrator) in two ways. **Do not mix them in one session without an explicit choice** — same requirement as §3.3 *Assembly model* in [`skill-standards-section-3.md`](skill-standards-section-3.md) (static vs dynamic).

## `AGENTS.md` — always (skill-wide orientation)

**`AGENTS.md`** is the **assembled agent bundle**: how the skill is structured, how phases/steps relate, and how to work with it in general. It should be **assembled for every skill** (typically generated by **`scripts/build.py`**), regardless of **`delivery.mode`**. It is *not* what the mode flag switches on or off.

**What `delivery.mode` actually changes** is how a **single operation** (or phase/step run) gets its **process slice**: either from **pre-generated built output** or from **runtime injection** of sources — see below.

## Flag (system-wide convention)

Declare the mode in **`skill-config.json`** so tools, CI, and humans agree:

```json
"delivery": {
  "mode": "static_built"
}
```

| `delivery.mode` | Meaning |
| --- | --- |
| **`static_built`** | **Default.** When you **run an operation**, the executor uses **process content that has already been merged into `content/built/`** (and similar per-skill layouts): each slice includes the **process part** plus its **library** and **rules** components as produced by the build. **`AGENTS.md`** is still checked in as the skill-wide bundle; **built** trees are the canonical **operation-time** artifacts. Operators run **`python scripts/build.py`** after changing sources; commits include regenerated files. |
| **`runtime_injection`** | When you **run an operation**, the executor **injects** the **process part** and, in documented order, **all** of its **library** and **rules** components from source paths — **without** requiring that slice to exist as a pre-built file under **`content/built/`**. **`AGENTS.md`** is still assembled for orientation; only the **operation-time** merge strategy differs. |

**Default for new skills:** `static_built`. Use **`runtime_injection`** when you want runtime resolution; use **`static_built`** when you want checked-in slices — **both** require the same **documented injection map** (see below).

## Injection map — document regardless of mode

**`delivery.mode` does not decide whether you document injection.** It only decides **pre-generate** (build + commit **`content/built/`**) vs **inject at run time** after each operation. In **both** cases:

1. **Which** source paths (process slice, **`library/`**, **`rules/`**, …) apply **per operation** (phase/step).
2. **In what order** they are merged / concatenated / injected.
3. **How** that matches the **static** merge (same semantics as **`build.py`**, or **deliberate differences** called out).

Keep this in a **single lookup** place — e.g. skill **`README.md`**, a manifest in **`build.py`**, or a **generated manifest** checked in next to **`built/`** — so someone can **change `delivery.mode` later** without re-deriving paths from scattered files. The only thing that changes is **when** material is materialized (build vs runtime), not **what** the skill is allowed to omit from documentation.

## Mode (a) — `static_built`

- **What is delivered:** Generated markdown under **`content/built/`** (and/or `phases/built/`, `content/parts/steps/built/` per skill layout) plus the top-level **`AGENTS.md`** when the build emits it.
- **Operation-time behavior:** Use the **built** slices (process + library + rules already merged for that slice).
- **When it applies:** CI, reviewable diffs, reproducible runs, “what the agent saw” is literally in git.
- **Operator obligation:** After editing **`content/parts/`**, **`rules/`**, or merge inputs, run **`build.py`** and commit outputs.

## Mode (b) — `runtime_injection`

- **What is delivered:** For **operations**, not a single pre-expanded tree under **`built/`**; the **executor** resolves **phase** (or step) → **files** (`rules/…`, `content/parts/library/…`, process slice, etc.) and **injects** them into context in a documented order (full **process part + library + rules** for that operation).
- **`AGENTS.md`:** Still assembled so the agent understands the skill in general; only **per-operation** content is resolved at runtime.
- **When it applies:** Interactive orchestration, rapid iteration without running the full static pipeline each time, or environments where checking in large built blobs is undesirable (still document the tradeoff).
- **Operator / implementer obligation:** Same as **static** mode for the **injection map** — resolution order, equivalence vs static merge, validation — **not** optional just because execution is dynamic. Runtime mode adds: executor must follow the **same** documented map (or list exceptions).

## Staying in sync between modes

1. **Single source of truth** for *meaning* stays in **unbuilt** inputs: **`content/parts/`**, **`rules/`**, **`docs/`** (reference), not in hand-edited **`AGENTS.md`** when a build owns the merge.
2. **`static_built`** outputs are **derivatives**: regenerating must be repeatable from the same inputs + **`scripts/build.py`** (and any merge manifest the skill defines).
3. **`runtime_injection`** must **not drift silently**: if both modes are supported, the skill should state whether runtime is a *shortcut to the same merge* (ideal) or a *lighter subset* (then list gaps).
4. **Changing sources:** Under **`static_built`**, CI or pre-commit should run **`build.py`** and fail if **`content/built/`** / **`AGENTS.md`** are stale (exact hook is repo-specific).
5. **Switching modes:** The **injection map** (paths + order + equivalence) is what lets you move from **`static_built`** to **`runtime_injection`** or back — update **`delivery.mode`** and keep the **same** map unless you intentionally change behavior.

## Relation to `build.py` flags

Per §3.3, a skill may expose **`--assembly static|dynamic`** (or equivalent) **inside** `build.py` for *how* static snapshots are produced. That is **orthogonal** to **`delivery.mode`**: `delivery.mode` answers whether the **operator/agent relies on checked-in built files** vs **runtime resolution**. A skill can use `runtime_injection` at execution time while still using `build.py --assembly static` to produce reference snapshots for tests.


---

### `process-approach.md`

# Process approach — IDE, `process.md`, code phases vs AI-chat phases

**Audience:** Authors and tooling. This is the **default mental model** for how a skill is **used** (Cursor, VS Code, Claude Desktop, similar) and how **phases** are executed.

## Who consumes what


| Artifact                                                               | Who uses it                                     | How                                                                                                                                                                                                                                                                                                                      |
| ---------------------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `**AGENTS.md`** (skill root)                                           | **IDE / assistant**                             | Loaded **automatically** by many tools as context for the repo. It orients the model: pipeline, links, where `process.md` lives. **No one “opens `built/` by hand” as the primary workflow** — the chat does not browse the tree to find instructions; **you tell it what to do** using `**process.md`** and phase docs. |
| `**content/parts/process.md**` (or `pieces/process.md` in some skills) | **Human + chat**                                | **Map of phases**: table rows are **phases**, **Ref** links to phase files. The skill should tell users to **read / `@`-reference** this file to know **how to execute** a given phase (order, actor, script). Example pattern: `@agilebydesign-skills/skills/<skill-id>/content/parts/process.md`.                      |
| **Built phase text** (`phases/built/`, `content/built/`, …)            | **Build pipeline + optional `generate_prompt`** | **Generated** outputs — **not** “what autonomous agents read first.” They exist so you can **materialize** a full instruction block for an AI phase (static mode) or **diff in git** under `static_built` delivery.                                                                                                      |


## Phase kinds (two execution styles)

### 1. Code-driven phases (human or CI runs the script)

- **You run** the Python/shell entry point **normally** (terminal, task, CI).
- **Await** exit code and artifacts the phase defines.
- The **phase markdown** (source) describes **how to invoke** the script, **arguments**, **outputs**, and **what “done” means** — not a prompt to paste unless the phase is hybrid.

### 2. AI-chat–driven phases (instructions for the model)

- The **instruction body** the chat must follow is produced by **prompt generation** — short name: **generate prompt** (implementation often `scripts/generate_prompt.py` per skill; names may vary).
- **CLI shape (contract):** support a **phase selector**, e.g. `python scripts/generate_prompt.py --phase <phase_slug>` (some teams use `phase:<name>` as a single token; equivalent intent).
- **Two modes** (both end with “text the user pastes or tool injects into chat”):


| Mode        | What it does                                                                                                                                                                                                                                                            | When to use                                                                |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Dynamic** | Builds one **string** by **collecting every section** required for that phase (source phase markdown, `library/` fragments, applicable `rules/`, manifest order in `skill-config.json` / `build.py`).                                                                   | Fast iteration; single source of truth; no checked-in blob for that phase. |
| **Static**  | Uses **pre-generated** phase text already written under the skill’s **built tree** (convention: `content/parts/phases/built/<phase_slug>.md` or `phases/built/<phase_slug>.md` — **document the path in the skill**). **Grab the whole file** as the instruction block. | Reproducible snapshots, CI, “exactly what shipped last release.”           |


In **either** mode, the **outcome** is: **the IDE chat has the right block of instructions** to follow for that phase — not “the agent navigates to `built/` like a filesystem API.”

### Default `phase_bundle` order (`skill-config.json`)

**abd-skill-builder** `Instructions` (used by `scripts/generate_prompt.py` and typical `scripts/build.py` merges) follows **`phase_bundle.order`** — an array of section tokens — unless `operation_sections` overrides the slug. **Default in this repo and scaffold template:** **`["principles", "role", "phase", "library", "rules"]`** so **`critical-quality-steps.md`** ( **`## Principles`** ) leads every AI-chat bundle. Other skills may reorder (e.g. **`principles`** last) or omit tokens; missing optional files (**`role`**, **`principles`**) are skipped.

Section tokens (each included only if listed in **`order`**):

- **`principles`** — optional: file under `content/parts/library/` (default `critical-quality-steps.md`), heading **`principles_heading`**. **Omitted** if the file is missing.
- **`role`** — optional: file under `content/parts/` (default basename `solution-analyst-role.md`). **Omitted** if the file is missing.
- **`phase`** — `content/parts/phases/<slug>.md` (or `parts/phases/`), with heading **`## Phase`** when `phase_bundle.phase_heading` is set.
- **`library`** — shards from **`PHASE_LIBRARY_SLICES`** for that slug, or all of **`library_files`** when the slice is absent; one **`## Library`** heading, then **`### \`file.md\``** per shard (with `abd:begin` / `abd:end` filtering). **Empty slice** → placeholder body under **`## Library`**.
- **`rules`** — **normative:** governance markdown inlined from **`rules/<stem>.md`** in manifest order. Stems come only from **`skill-config.json`**:
   - **`every_phase_rules`** — array of stems (no `.md`) prepended for **every** phase, **deduplicated** in order (listed once even if also under a phase).
   - **`phase_rules`** — object: keys are **phase slugs** (same strings as **`phase_files`**); values are ordered arrays of stems. Example: `"shaped-story-map": ["evidence-citations-required", "shaped-story-shape"]`.
   **No stems** for a phase → placeholder body under **`## Rules`** (points authors to this doc). Rule files may keep optional YAML frontmatter (e.g. **`rule_id:`**); **`Instructions`** strips it before inlining so bundles stay readable. **Do not** use per-rule **`phase_files:`** frontmatter as the source of truth for which phase gets which rule — that duplicates the manifest and drifts; **abd-maps-models-specs** and **abd-skill-builder** both standardize on **`phase_rules` / `every_phase_rules`**.

Configure (or copy defaults) via **`phase_bundle`** in **`skill-config.json`**: keys include **`order`**, **`role_file`**, **`principles_file`**, and optional **`role_heading`**, **`phase_heading`**, **`library_heading`**, **`rules_heading`**, **`principles_heading`**. **abd-skill-builder** ships the full default object so scaffolded skills inherit the same contract; **abd-maps-models-specs** uses **`MapsInstructions`**, which follows the same **`phase_rules` / `every_phase_rules`** contract (plus maps-only critical-quality notes).

### Library shards with phase markers (`abd:begin` / `abd:end`)

A **`library/*.md`** file may wrap fragments in **`<!-- abd:begin <phase-slug> -->`** … **`<!-- abd:end <phase-slug> -->`** (same slug on both lines). When **`Instructions.assemble_prompt(<phase-slug>)`** runs (used by **`generate_prompt.py`** and **`build.py`** for **`phases/built/<slug>.md`**), the reader sees **all lines outside** those pairs **plus** only the **pair whose slug matches** the current phase. Slugs match **`phase_files`** in **`skill-config.json`** (e.g. **`plan-script-build`**). Files **without** markers are included in full whenever **`PHASE_LIBRARY_SLICES`** lists them for that phase. Authoring template: **`templates/concepts.md.template`**.

## What `build.py` is for

- `**scripts/build.py`** merges **process + library + phases (+ rules where applicable)** into `**AGENTS.md`** and any `**content/built/**` slices per `**delivery.mode**`.
- It is the **authoritative** driver for **this** skill repo. `**generate_prompt`** is **orthogonal**: it answers “what text do I put in chat **for this AI phase**?” while `**build.py`** answers “what ships in **AGENTS.md** / static bundles?”

## Relation to §3

- **Stages / phases / steps** table semantics: `[skill-standards-section-3.md](skill-standards-section-3.md)`.
- **Rule file naming, assembly flags:** same §3 doc.
- **Delivery modes (`static_built` vs `runtime_injection`):** `[delivery-modes.md](delivery-modes.md)`.

## Team process plate (rich `process.md`)

For skills that need the same **shape** as **abd-maps-models-specs** — **outcome**, **principles**, **inputs / outputs**, **stages**, and a **wide phase table** (Description, Actor, Input, Output, Scripts) — start from the **team template**:

- **`content/parts/templates/process-team.md.template`** (in **abd-skill-builder**)
- **`content/parts/templates/README.md`** — how it relates to scaffold’s minimal **`templates/process.md.template`**

Copy the plate into **your** skill as **`content/parts/process.md`**, replace `{{skill_name}}`, add phases and **Ref** links, then run **`python scripts/build.py`**. The **abd-skill-builder** **`process.md`** demonstrates the same structure at production quality.

## Extending a new skill

1. Add `**content/parts/process.md`** with phase rows and **Ref**s (or start from **`process-team.md.template`** above).
2. For each **code phase**, document script + I/O in the phase file.
3. For each **AI-chat phase**, either wire `**generate_prompt`** (dynamic/static) or document a manual copy-paste path until scripted.
4. Run `**python scripts/build.py**` so `**AGENTS.md**` stays the IDE-facing bundle.
5. Keep `**process-approach.md**` behaviors in `**README.md**` in one paragraph so consumers know how your skill expects IDE + chat to work.


---

### `authoring-checklist.md`

# Skill authoring checklist (human + AI)

**Purpose:** Trackable **`- [ ]` / `- [x]`** tasks for building or evolving a skill. **Workspace convention:** keep this content in **`docs/skill-plan.md`** under the **## Authoring checklist** section (one document with the plan). **Scaffold** injects this file there; by hand, paste from here. If you stop mid-work, the next session continues from the **first unchecked** box in that section.

**Canonical source:** `skills/abd-skill-builder/content/parts/library/authoring-checklist.md` — merge updates from here when standards change.

| Role | What to do |
|------|------------|
| **A — Ask** | Use the **Ask:** lines under each section when you need input. |
| **B — Answer / suggest** | As **AI**, fill proposals; human confirms. |
| **C — Track** | Turn `- [ ]` into `- [x]` only when the item is **done**. |

**Normative layout/operator rules** stay in **`skill-repo-standards.md`** and **`skill-standards-section-3.md`** (under **`content/parts/library/`** in **abd-skill-builder**). **How the IDE uses the skill** (AGENTS.md, `process.md`, code vs AI-chat phases, `generate_prompt`): **`process-approach.md`**.

**Runtime vs `docs/`:** All markdown (and other content) that **pertains to how the skill is used at operation time** — merged or injected by **`build.py`**, read as phase bodies, or otherwise part of the **runnable** package — lives under **`content/parts/`** (and **`library/`**, **`rules/`**, etc. per norms). **`docs/`** is **only** for **non-runtime** material: user manuals, **skill plans** (including the checklist section), architecture, standards deltas. **Do not** stash mergeable instruction content in **`docs/`**. (**abd-skill-builder** itself only keeps **`docs/standards-delta.md`**.)

---

## Before you start (every session)

- [ ] **Working copy:** **`docs/skill-plan.md`** includes an **## Authoring checklist** section (scaffold injects this file there; by hand, paste from **`library/authoring-checklist.md`** into that section).
- [ ] **Resume:** Find the **first unchecked** `- [ ]` in the checklist section and continue from there.
- [ ] **Optional:** Note the date and “stopped at §…” in **Gaps / follow-ups** at the bottom when pausing.
- [ ] **`docs/` vs `content/parts/`:** No **runtime** markdown under **`docs/`** — phases, library bodies, and anything **`build.py`** merges/injects stay in **`parts/`**. **`docs/`** = manuals, **skill plan** (with checklist section), architecture, migration notes only.

---

## Greenfield vs existing skill

- [ ] **New skill:** Ran **`scaffold_skill.py`** (or equivalent) so the base tree exists.
- [ ] **Existing skill:** Ran **[plan-migrate.md](../phases/plan-migrate.md)** (**1b**: inventory + **standards-delta** + user chose **IDs**), then **[migrate.md](../phases/migrate.md)** (**2b**: execute moves) **before** bulk edits — **or** consciously skipped with a note in **Gaps / follow-ups**.

---

## Skill identity (what this skill does — not delta to other work)

Normative row: **Documentation focus** in **`skill-repo-standards.md`**.

- [ ] **Process, rules, and docs** describe **what this skill does** and how to run it — **this package**, on its own terms.
- [ ] They do **not** rely on “vs another skill” or “we don’t do X because Y” — that stays out of durable spec.
- [ ] **Dependencies** (other skills, repos, tools, versions) recorded explicitly (**Dependencies** / `README` / `conf/build-strategy.json`) — separate from the main narrative.

**AI should:** Strip migration chatter; put relationships in a **Dependencies** list.

**Ask:** “If this skill vanished, could someone run it from **this repo alone**?”

---

## Base scaffold: what you copy and extend

**Source:** **`skills/abd-skill-builder/scripts/scaffold_skill.py`** + **`skills/abd-skill-builder/templates/*`** — extend these files; don’t invent a parallel layout.

### Scaffold files present and reviewed (check each)

- [ ] **`SKILL.md`** — frontmatter + description make sense.
- [ ] **`skill-config.json`** — `operator.*`, `delivery.mode` match intent; if **`rules/*.md`** back AI-chat phases, **`phase_rules`** / **`every_phase_rules`** list every rule stem for the right **phase slug** (**[`process-approach.md`](process-approach.md)** — *rules* in the default **`phase_bundle`**).
- [ ] **`conf/build-strategy.json`** — `skill_purpose` and siblings filled per Strategizer.
- [ ] **`conf/abd-config.json`** — **`active_skill_workspace`** set (under **`test/`** when using a workspace); optional CLI: **`python scripts/set_workspace.py <path>`**.
- [ ] **`scripts/set_workspace.py`** — present (scaffold copies from **abd-skill-builder**).
- [ ] **`conf/README.md`** — conf usage clear.
- [ ] **`content/parts/process.md`** — pipeline table matches real phases.
- [ ] **`content/parts/phases/`** — one file per row in **`process.md`** (add/rename beyond **`author.md`** as needed).
- [ ] **`content/parts/phases/built/`** — present when you use **static** AI-chat prompts; populate via **`build.py`**; see **`process-approach.md`**.
- [ ] **`scripts/generate_prompt.py`** — present for AI-chat phases; **`--mode dynamic`** vs **`static`** documented; extend per skill.
- [ ] **`scripts/build.py`** — merge/injection driver present (see non-negotiables below).
- [ ] **`scripts/scanner_smoke.py`** — replaced or supplemented with real scanners if needed.
- [ ] **`rules/README.md`** + **`rules/scanners.json`** — wired when rules exist.
- [ ] **`test/README.md`** — explains layout; workspace path if used.
- [ ] **`content/parts/library/`** — created when cross-cutting chunks exist; wired in **`build.py`** (e.g. **`PHASE_LIBRARY`**) per §3.

### Non-negotiables

- [ ] **`scripts/build.py`** is the **merge / injection driver** (writes at least **`AGENTS.md`** from process + phases).
- [ ] **`process.md`** order matches **`phases/`** and **`build.py`** (if order ≠ lexicographic sort of filenames, **`build.py`** uses an **explicit ordered list**, not **`sorted(glob)`**).
- [ ] **Process → operation injection** documented in/near **`build.py`** + human-readable place for §4.

### Reference templates read (when extending)

- [ ] Read **`abd-skill-builder/parts/library/process-table-standards.md`** — process **`#`**, **Phase**, **Description**, **Actor**, **Input**, **Output**, **Scripts**; **workspace** phase (**Phase 0**) required.
- [ ] Opened **`abd-skill-builder/templates/child_build.py.template`** (minimal merge).
- [ ] If per-operation bundles / library injection: reviewed **`abd-maps-models-specs/scripts/build.py`** (`PHASE_FILES`, `PHASE_LIBRARY`, built phases).

### Extension work (after §§0–4 answers)

- [ ] **One** **`build.py`** — no second hidden merge pipeline.
- [ ] **`process.md`**, **`phases/*.md`**, **`build.py`** updated **together** when adding/changing a phase.
- [ ] **`content/parts/library/`** chunks added and wired in **`build.py`** where needed.
- [ ] **Injection map** in **`build.py` docstring** and/or skill **`README.md`** (aligns with §4).
- [ ] **`python scripts/build.py`** run after structural edits; **`AGENTS.md`** / **`content/built/`** committed if **`static_built`**.

**Ask:** “Which files do we **edit** vs **add**? Where is the **ordered phase list** in **`build.py`**?”

---

## 0. Build intent (`conf/build-strategy.json`)

- [ ] **`conf/build-strategy.json`** complete per **`agentic-skill-builder`** (template + Strategizer).

**Ask:** “What must this skill accomplish end-to-end? Who runs it? What is out of scope?”

---

## 1. Process & phases

- [ ] **`parts/process.md`** (or **`content/parts/process.md`**) lists the real pipeline (ordered phases) and follows **[`process-table-standards.md`](process-table-standards.md)** — column meanings, **Input**/**Output** semantics, **Scripts** cell.
- [ ] **Workspace phase (Phase 0):** **`parts/phases/workspace-and-config.md`** exists; **`conf/abd-config.json`** + **`active_skill_workspace`** documented; first process row uses **`0`** in **`#`** and the phase name **Workspace and config** (see standards doc).
- [ ] Phase files use **descriptive slugs**; order matches **`process.md`** and **`build.py`** (explicit order if not sort order).
- [ ] **`build.py`** phase list / merge keys updated when **`process.md`** changes.
- [ ] **Phase vs library:** Each **`phases/<slug>.md`** is **procedure** for that phase (steps, scripts, checklists)—**not** a dump of cross-phase definitions (**[`documentation-standards.md`](documentation-standards.md)** → *Library vs phase documents*; **[`rules/content-placement.md`](../../rules/content-placement.md)**).

**Ask:** “Phases in order?”

---

## 2. Rules (optional) & scanners

- [ ] Decided if **`rules/`** is needed.
- [ ] Listed planned **`rules/*.md`** files (one concern per file where possible).
- [ ] Decided scanner vs doc-only for each rule cluster.
- [ ] **Base framework** (when checks exist): read **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** — **`rules/scanners.json`** **`rule_scanner_bindings`** for each machine-checked rule; **`skill-config.json`** **`operator.build_pipeline`** lists ordered post-merge steps for **`build.py`**; **`operator.scanners`** lists the same scanner paths (or a superset) for **Operator** / CI.
- [ ] **`process.md`** does **not** treat scanners as phase-local “script column” noise; skill-level **Rules and automated checks** (or link to **`rules-and-automated-checks.md`**) instead.

**Ask:** “Machine-checked vs human-reviewed? What would each scanner inspect?”

---

## 3. Library — cross-cutting concepts (`content/parts/library/`)

- [ ] Cross-cutting content in **`library/<slug>.md`** (or skill-specific equivalent).
- [ ] **`build.py`** merge order matches how phases reuse library.
- [ ] Optional **index** (short links only: **`README`**, **`conf/build-strategy.json` notes**, or a **`docs/*` index** if non-runtime) — **not** a second home for bodies; full cross-cutting copy stays in **`library/`** (see **`docs/` vs parts** in **`skill-repo-standards.md`**).
- [ ] Same concept **names** across phases.
- [ ] **Library stays non-procedural:** **no** numbered “how to run a phase” sequences, **no** phase ordering story, **no** phase-specific **`python scripts/…`** runbooks—those stay in **`phases/`** and **`process.md`** (**[`rules/content-placement.md`](../../rules/content-placement.md)**).

**Ask:** “What repeats across phases → **library**?”

---

## 4. Agent delivery mode (`skill-config.json` → `delivery.mode`)

See **`abd-skill-builder`** [`delivery-modes.md`](content/parts/library/delivery-modes.md) (canonical: `skills/abd-skill-builder/content/parts/library/delivery-modes.md`).

- [ ] **`AGENTS.md`** assembled (both modes).
- [ ] **Injection / merge map** documented (paths per operation, order, equivalence to static) — **`README`**, **`build.py`**, or manifest — so mode can change later (narrative-only; sources remain under **`content/parts/`**).
- [ ] **`delivery.mode`** set: **`static_built`** or **`runtime_injection`**.
- [ ] If **`static_built`**: **`build.py`** run; **`content/built/`** (and peers) committed; traceable to map.
- [ ] If **`runtime_injection`**: runtime follows documented map (or deltas documented).

**Ask:** “Per operation: which files, which order, where is the lookup?”

---

## 5. `test/` — script tests & fixtures

- [ ] Chose: pytest **yes** or **no** (if no, skip pytest bullets; may still use **`test/`** for fixtures).
- [ ] If pytest **yes**: dev deps + **`pip install`** documented (**`requirements-dev.txt`** or **`pyproject.toml`**).
- [ ] **Run command** documented (e.g. **`python -m pytest test/`**).
- [ ] **CI** runs tests (optional).
- [ ] Tests live under **`test/`**; **`test/fixture/`** if needed.
- [ ] **`active_skill_workspace`** path under **`test/<name>/`** documented if set.

**Ask:** “What must stay green? Best fixture?”

---

## 6. Operator contract — “built the skill”

- [ ] **`SKILL.md`** + frontmatter.
- [ ] **`skill-config.json`** paths match disk.
- [ ] **`python scripts/build.py`** exits **0**.
- [ ] **Python compile check** on **`operator.compileall_paths`** passes (Operator uses Python’s **`compileall`** under the hood).
- [ ] **Scanner** scripts exit **0** (if any).

**Ask:** “Operator green?”

**Final:**

- [ ] **Attest** structurally built — **or** list gaps below.

---

## Gaps / follow-ups (free text)

Use for **resume notes** (date, last § completed, blockers):

```text


```

---

## How to use this file

1. **Ensure** **`docs/skill-plan.md`** has an **## Authoring checklist** section (scaffold injects from **`abd-skill-builder`** **`content/parts/library/authoring-checklist.md`**) before deep work.
2. Check **`- [x]`** only when done; **first unchecked** = resume point.
3. Pull updates from **`abd-skill-builder`** canonical copy when standards change.


---

### `skill-repo-standards.md`

# Skill repository standards (index + extras)

**Process approach (IDE, `process.md`, code vs AI phases, `generate_prompt`):** [`process-approach.md`](process-approach.md) — **start here** for how skills are **used** in Cursor / similar: **`AGENTS.md`** auto-loaded, **`@…/process.md`** for phase map, **code phases** vs **AI-chat phases**, **dynamic vs static** prompt generation.

**Full normative §3 (all subsections):** [`skill-standards-section-3.md`](skill-standards-section-3.md) — directory and content conventions (**§3.1**), rule naming (**§3.2**), assembly (**§3.3**), reference notes (**§3.4**): stages/phases/steps, process tables, optional domain+story-map pattern, `AGENTS.md` / `content/built/`.

**Rules + scanners + build pipeline (base framework):** [`rules-and-automated-checks.md`](rules-and-automated-checks.md) — **default** wiring: **`rules/scanners.json`** bindings, **`operator.build_pipeline`** for **`build.py`**, **`operator.scanners`** for Operator; **do not** hang scanners off individual **process** phases.

**Builder vs Operator (summary):** [`builder-vs-operator.md`](builder-vs-operator.md) — **scaffold / generation** path vs **`operator.run_operator()`** validation today.

**Authoring checklist (human + AI):** [`authoring-checklist.md`](authoring-checklist.md) — normative body merged into **AGENTS.md**; in each skill, work the **## Authoring checklist** section inside **`docs/skill-plan.md`** (scaffold injects this file there). **`- [ ]` / `- [x]`** so work can **resume after interruption** (first unchecked box = continue here). Covers scaffold verification, rules/scanners, **library**, **`delivery.mode`**, **`test/`**, operator.

**Migrating an existing skill:** [`../phases/plan-migrate.md`](../phases/plan-migrate.md) (**1b**) — inventory → compare to standards → **delta report** → **user chooses which gap IDs to fix**; then [`../phases/migrate.md`](../phases/migrate.md) (**2b**) — **execute** moves and patches for those IDs only (no silent full rewrites).

**Example delta (this repo):** [`../../docs/standards-delta.md`](../../docs/standards-delta.md) — `abd-skill-builder` inventory vs §3 (delivery, `content/built/`, docs, tests/fixture notes).

---

## Quick layout reminder (before reading the full §3)

| Area | Convention |
|------|------------|
| **Entry** | `SKILL.md` at skill root (frontmatter: `name`, `description`). |
| **Operator config** | `skill-config.json` — `operator.compileall_paths`, `operator.build_script`, **`operator.build_pipeline`** (post-merge steps for **`build.py`**), **`operator.scanners`** (Operator; align paths with rule-bound scanners). See **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**. |
| **Agent delivery** | `skill-config.json` — `delivery.mode`: **`static_built`** (pre-generate per-operation slices into **`content/built/`**) or **`runtime_injection`** (resolve the **same** sources at run time). **Only** that choice differs — always document **which paths** feed each operation, **merge order**, and **equivalence** to static output, in a **lookup** place (skill **`README.md`**, **`build.py`** manifest, or emitted manifest) so the team can switch modes later. **`AGENTS.md`** in **both** modes. See **`abd-skill-builder`** [`delivery-modes.md`](delivery-modes.md) (canonical: **`content/parts/library/delivery-modes.md`**). |
| **Authoring prose (normative for writers)** | [`documentation-standards.md`](documentation-standards.md) — voice, where content belongs, process tables; complements **`docs/` vs `content/parts/`** rule. |
| **Workspace routing** | **[workspace-and-config](../phases/workspace-and-config.md#skill-path-skill-workspace-and-configuration)** — **`skill_path`**, **`skill_workspace`**, **`conf/abd-config.json`** keys (**Workspace and config**). |
| **Build intent** | `conf/build-strategy.json` — strategize loads this **whole JSON**; **`skill_purpose`** must be non-empty for **`strategy_complete`** (minimum to finish strategize). Other keys are **siblings** that enrich **`strategy`** / **`builder_manifest`** — they are **not** part of the **`skill_purpose`** text. See **`agentic-skill-builder/README.md`** (Strategizer). |
| **Normative content** | `content/parts/` — process table rows are **phases**; **steps** inside phase files. Phase markdown files use **descriptive slugs** (`terms-mechanisms.md`, …) — **not** `phase-NN-…` or phase numbers in **H1** titles; pipeline order is **only** in `process.md` (# column) + `build.py` merge list (see **`skill-standards-section-3.md`**). **Column definitions** and required **workspace** row: **`process-table-standards.md`**. |
| **docs/ (non-runtime only)** | **`docs/`** is for material **not** consumed as merged/injected skill payload at operation time: **user manuals**, **migration/planning notes**, **architecture**, **`docs/skill-plan.md`** (plan + **Authoring checklist** section), **standards deltas**. In **abd-skill-builder**, **`docs/`** is only **`standards-delta.md`** — delivery merge order lives in **`README.md`**. **Do not** put markdown (or other assets) in **`docs/`** that **`build.py` merges**, **injects**, or **ships** as the runnable instruction body for phases/operations — that belongs under **`content/parts/`** (including **`library/`**, **`phases/`**, **`process.md`**, **`rules/`** as applicable). |
| **Library** | `content/parts/library/` — **cross-cutting meaning** reused across more than one phase: definitions, tables, glossaries, named concepts, artifact shapes. **Not** phase procedures, **not** step-by-step runbooks, **not** CLI blocks for a single phase, **not** pipeline order (that is **`process.md`** + **`phases/`**). The library **is** the home for that shared meaning; do not maintain a parallel “cross-cutting” layer elsewhere. **`docs/`** may hold a **short index** pointing into **`library/`**; **bodies** live in **`library/`**; merge order lives in **`build.py`**. See **`documentation-standards.md`** → *Library vs phase documents*. |
| **Phases** | `content/parts/phases/<slug>.md` — **person-to-process** instructions for **one** process-table row: I/O, **steps**, scripts, done criteria. **Link** to **`library/`** for deep definitions; avoid duplicating large normative blocks that belong in **`library/`** because multiple phases need them. |
| **Rules** | `rules/*.md` or `content/parts/rules/*.md`; optional `rules/scanners.json`. |
| **Scripts** | `scripts/build.py` (**required** — merge/injection driver; scaffold template is minimal; extend with explicit phase order + per-operation bundles as in **`abd-maps-models-specs`** when needed), scanners, optional `_config.py`. See **`authoring-checklist.md`** → *Base scaffold*. |
| **Tests & fixtures** | **`test/`** — all automated tests for the skill (pytest, smoke scripts, etc.) that exercise **`scripts/`**; optional **`test/fixture/<scenario>/`** for frozen inputs/snapshots; optional **`test/<workspace>/`** dirs when **`conf/abd-config.json`** uses **`active_skill_workspace`** (path relative to skill root). Example: **`abd-maps-models-specs/test/`** — workspace **`test/sample-workspace`**, optional fixture **`test/fixture/<scenario>/`**. **`abd-skill-builder`** itself **does include** **`test/`** (see **`test/README.md`** + **`test/fixture/toy-polite-dialogue/`**) even though **pytest `test_*.py` files** are still optional follow-ups — do not read “pytest wiring pending” as “no **`test/`** folder.” **Operator today** only runs a **Python compile check** on **`operator.compileall_paths`** (usually **`["scripts"]`**; implemented with **`compileall`**) — it does **not** install or run **pytest**. If automated tests are **in scope**, add the **wiring** below. |
| **Agent bundle (always)** | `AGENTS.md` — assembled agent bundle (skill-wide “how it works”); typically generated by `build.py`; **not** gated on `delivery.mode`. |
| **Built slices (operation-time, static mode)** | `content/built/` — pre-merged process + library + rules per skill layout when `delivery.mode` is **`static_built`**. |
| **Documentation focus (this skill only)** | Process plans, **rules**, and **docs** describe **what this skill does** — in positive, runnable terms for **this** package. **Do not** use them as a running commentary on how this skill **differs** from another skill, or why it **doesn’t** do something “because another skill does.” That is **local context in time**, not part of the durable skill. **Dependencies** (other skills, tools, repos, contracts) are **explicit** — names, links, versions — in a **Dependencies** section, `README`, or build-strategy notes. That is **not** the same as narrating deltas to sibling work. |

**Minimal valid skill:** `SKILL.md` + `scripts/build.py` + `skill-config.json` with operator block — see **`test/fixture/toy-polite-dialogue/`** in this skill (**`abd-skill-builder`**).

---

## When automated tests are asked for (pytest wiring)

If the skill should run **pytest** (or similar) under **`test/`**, do **not** assume it is already installed or wired into **`operator`** — add it explicitly:

| Step | What to do |
|------|------------|
| **Dependency** | Add **`pytest`** (and dev-only plugins if needed) to a **`requirements-dev.txt`**, **`pyproject.toml`** `[project.optional-dependencies] dev`, or the skill’s documented venv install step — **commit** the file so others can `pip install -r …`. |
| **Layout** | Tests live under **`test/`** (e.g. **`test/test_*.py`** or **`test/<suite>/`**); shared fixtures in **`test/fixture/`** or **`conftest.py`** as usual for pytest. |
| **Run command** | Document in skill **`README.md`** or **`test/README.md`**: e.g. `python -m pytest test/` from skill root (with venv activated). |
| **CI (optional)** | Add a workflow or monorepo job that installs dev deps and runs the same command. |
| **Operator** | **`operator.run_operator()`** does **not** run pytest by default. To gate releases on tests, extend **CI** or a **wrapper script**; only add **`test`** to **`compileall_paths`** if you intentionally want bytecode checks on test modules (unusual). |

---

## Operator checklist (machine-runnable)

1. `SKILL.md` present.
2. `skill-config.json` parses; `operator` block consistent with files on disk.
3. Python files on declared paths pass a **compile check** (Operator uses **`compileall`**).
4. `python scripts/build.py` exits 0.
5. Each listed **scanner** in **`operator.scanners`** exits **0** (and any step in **`operator.build_pipeline`** that **`build.py`** runs also exits **0** when you rely on **`build.py`** as the full local gate).
6. **`rule_scanner_bindings`** (in **`rules/scanners.json`** when used): each **`rule_file`** and **`scanner`** path exists.

---

## What greenfield scaffold should emit

**`scripts/scaffold_skill.py`** (and equivalent generators) should produce a **complete, runnable skeleton**: file tree, `skill-config.json`, phase markdown stubs, `rules/` / `conf/` as needed, runnable **`build.py`**, optional scanner stubs — **without** baking in customer-specific “gold” domain solutions (those belong in the target workspace, not the template).

This **`abd-skill-builder`** skill ships **templates + `scaffold_skill.py`** as the supported way to create that tree. **`operator.run_operator()`** then validates what is on disk; it does not scaffold new skills by itself.


---

### `skill-standards-section-3.md`

# §3 Skill package layout and content standards

**What this is:** Normative rules for how a **skill repository** is shaped — where **runtime** content lives (`content/parts/`, `rules/`, `build.py`), how **stages / phases / steps** relate, how **process tables** and **Refs** work, optional patterns (e.g. domain + story map), **rule file naming**, and **static vs dynamic** assembly of instructions. **How skills are used in the IDE** (AGENTS.md, `process.md`, code vs AI-chat phases, `generate_prompt`) is defined in [`process-approach.md`](process-approach.md) — read that first.

**How to use it:** Implement **§3.1–§3.4** when authoring or reviewing a skill. Tools and humans use the same rules; nothing here depends on any external “origin” document.

**Scope boundary — skills stay simple:** A **skill package** should express a **linear** pipeline: **stage → phase → (steps inside phase docs)**. The **process table** rows are **phases**, not steps. Keep skills deliberately sequential.

## 3.1 Directory and content conventions

**Hierarchy in the repo:** **Stages** group **phases**. Each **phase** has normative markdown (one file or section per phase, per skill); **steps** live **inside** that phase’s markdown — they are **not** separate rows in the master process table. See **Stages, phases, and steps** below.


| Area                            | Convention                                                                                                        | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Normative content**           | Under /`content/parts/`                                                                                           | Plans, operations, domain narrative — **not** dumped only in chat.                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `**docs/` (non-runtime)**       | /`docs/` at skill root                                                                                            | **User manuals**, **migration/planning notes**, **architecture**, **authoring checklists**, and **narrative** descriptions of delivery. **Do not** put markdown here that `build.py` **merges**, **injects**, or **ships** as the runnable phase/operation body — that belongs under `**content/parts/`** (including `**library/`**, `**phases/`**, `**process.md**`, `**rules/**`).                                                                                                                                   |
| **Phase markdown (source)**     | e.g. /`content/parts/phases/<descriptive-slug>.md`, or one doc per phase with step sections — paths vary by skill | **One row in the process table = one phase.** **Steps** (numbered sub-procedures, “Step 1…”, checklists) are written **inside** this markdown as **normative content of the phase**, not as their own table rows. **Do not** encode execution order in filenames or H1 titles (`phase-02-foo.md`, `# Phase 2 — …`): order belongs in `**process.md`** (the `#` column) and in `**scripts/build.py`**’s explicit file list. Use **stable descriptive** kebab-case slugs so renumbering the plan does not force renames. |
| **Built phase markdown**        | `content/parts/phases/built/<descriptive-slug>.md` and/or `content/built/…` per skill layout | **Generated** from source phase bodies + rules via `scripts/build.py`. **Authors do not hand-edit `built/`.** These files are **materialized instruction blobs** for **static** AI-chat phases and for **`static_built`** delivery — consumed by **`generate_prompt`** (or pasted into chat), **not** by “agents browsing the repo” as the primary UX. IDEs load **`AGENTS.md`**; see [`process-approach.md`](process-approach.md). Folder layout (`phases/built` vs `content/built`) is per skill; document it in **`README.md`**.                                                                                                                                                                                                            |
| **Atomic rules**                | `content/parts/rules/*.md` (or top-level `rules/` in simpler skills)                                              | One concern per file where possible; **names** should encode **phase** and/or **domain concept** + rule name (see §3.2). **Which phase inlines which rule** is declared in **`skill-config.json`** (`phase_rules`, `every_phase_rules`), not scattered in per-rule frontmatter lists.                                                                                                                                                                                                                                                                                                                                                                                               |
| **Roles**                       | `roles/*-role.md`                                                                                                 | One file per **user/agent role** the skill assumes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Process**                     | `content/parts/process.md` or staged process docs                                                                 | **Summary table: each row is a phase** (linked by **Ref** to phase markdown). Stages group those rows. **Steps** appear only **inside** the linked phase files.                                                                                                                                                                                                                                                                                                                                                        |
| **Library markdown**            | `content/parts/library/*.md` (or `parts/library/`)                                                                | **Cross-phase structure and meaning**: definitions, glossaries, artifact shapes, naming, invariants. **Not** phase-local procedures, pipeline ordering, or CLI runbooks—those live in **`process.md`** / **`phases/`** (see **Library vs phase documents** below).                                                                                                                                                                                                                                                     |
| **Repo-facing built artifacts** | `AGENTS.md`, `SKILL.md`, sometimes `README.md`                                                                    | Frequently produced by `scripts/build.py` (merge order per skill). **`AGENTS.md`** is what **IDEs and assistants typically load automatically** for the skill repo.                                                                                                                                                                                                                                                                                                                                                                |
| **Config**                      | `skill-config.json`                                                                                               | Name, version, **`phase_files`**, **`PHASE_LIBRARY_SLICES`**, **`phase_rules`** / **`every_phase_rules`** (ordered rule **stems** inlined per phase bundle — see [`process-approach.md`](process-approach.md)), **`phase_bundle`**, **`operator.compileall_paths`**, **`operator.build_script`**, **`operator.build_pipeline`** (post-merge steps for **`build.py`**), **`operator.scanners`** (Operator gate; align with rule-bound scanners) — skill-specific knobs. See **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** (base framework).                                                                                                                                                                                                                                               |
| **Scripts**                     | `scripts/`                                                                                                        | Operational entry points; may share `_config.py` patterns.                                                                                                                                                                                                                                                                                                                                                                                                                                                             |


### Stages, phases, and steps (how they relate)

**Order is always:** **Stage → Phase → Step** (coarse → mid → finest) — but **only the first two appear as rows** in the master process table. **Steps** are **inside** the phase markdown.


| Term      | Typical meaning                                                                                                                                                                                                                                                                                                                      | Example                                                                                  |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **Stage** | **Coarse pipeline slice** — groups many **phases**; may span days or sessions. Often a heading or section in `process.md` or a staged doc.                                                                                                                                                                                           | **Stage 1 — Extract Context**; **Stage 2 — Map and Model**; **Stage 3 — Specification**. |
| **Phase** | **One row** in the process summary table — the unit of “what we do next” with a **driver**: **human** or **AI actor**. The **Ref** column links to **phase** markdown. Phases answer “are we allowed to proceed?” and **contain** the detailed steps as normative body copy.                                                         | “Corpus audit — Phase N”; **Initiator / Actor** column = human vs AI.                    |
| **Step**  | **Sub-structure inside the phase’s markdown** — numbered instructions, checklists, “Step 1 / Step 2”, optional **suffix letters** (`5a`, `7a`) for companion script runs **within the same phase**. **Not** a row in the process table. Machine state (if any) may still reference `workflow_step` as a **sub-id** inside the phase. | Inside `modules-epics-scaffold-breadth.md`: “1. … 2. … 3a. rebuild index …”              |


**AI-driven phases — how the operation is delivered:** See **[`process-approach.md`](process-approach.md)**. In short: **code-driven** phases = run scripts as documented in the phase file; **AI-chat** phases = produce the instruction block via **`generate_prompt`**-style tooling in **dynamic** (assemble sections) or **static** (use pre-built phase markdown under `phases/built/` or equivalent). The **chat** follows that text; **`built/`** is not “the agent’s filesystem API.”

**Ordering (linear, inside the skill):** Stages order **major outcomes**. **Phases** run in **process table order** (each row = one phase). **Steps** follow the order **written inside** each phase document. **Parallel batches, fan-out, or merge** are **not** modeled as extra table rows; if needed, handle that **outside** the skill package (host app, orchestration, or scripts). **Phases** may **block** a later stage until accepted (e.g. “the indexer phase says rebuild chunks — do not start Stage 2 until accepted”).

**“Process” one-liner:** `content/parts/process.md` (or `parts/process.md`) often opens with a **single pipeline string** (e.g. Context → Foundational spine → …). That line is the **navigation spine**; the **table lists phases** (by stage); **authoritative step detail** lives inside each **Ref**’d phase file.

### Process tables, hyperlinks, and naming in the Ref column

**How the table is built**

- **Rows are phases**, not steps. Columns typically include: `#`, **Phase** (title — sometimes labeled “Step” in legacy tables; **semantically it is the phase**), **Initiator / Actor** (Human→Code, AI, Code), **Script** (if any), **What it does**, **Coverage**, **Ref**, **Inputs**, **Outputs**.
- **Ref** is the **hyperlink hub**: each row points to the **normative markdown for that phase**. **Steps** (numbered sub-procedures) live **inside** that file — not in separate table rows. Python entry points stay in **Script**, not **Ref**.
- **Two-tier phase files:**
  - **Source:** phase markdown authors edit (e.g. `content/parts/phases/<name>.md`, or `parts/steps/<name>.md` when the filename is the **phase** slug — naming varies by skill).
  - **Built:** `content/parts/phases/built/<name>.md` or `content/built/<name>.md` — **rules baked in** from `parts/rules/*.md` via `scripts/build.py`. **Steps remain inside** the built document. Used for **static** prompt generation and **`static_built`** slices — not hand-edited. See [`process-approach.md`](process-approach.md).
- **Cross-links inside the table:** The **Ref** column uses relative markdown links to the **phase** doc, e.g. `[context](parts/context.md)`, `[modules-epics-scaffold-breadth (built)](content/parts/steps/built/modules-epics-scaffold-breadth.md)` (paths vary by skill; **from the skill root** per `AGENTS.md`).

**Naming conventions visible in the table**

- **Phase titles** in the table read like **milestones or operations** (“Parse, curate, chunk, index”, “Integrate and Harmonize”) — stable labels for **phase** / workflow fields. **Finer labels** for **steps inside the phase file** may appear in JSON as `workflow_step` or similar.
- **Phase file names and H1 headings** must **not** duplicate pipeline indices (`phase-00-`, `Phase 3 —` in the title). Those numbers **change** when the plan evolves; **brittle** names churn git history and links. The **Ref** column and `build.py` define order; phase files stay **semantically** named (`story-map.md`, `canonical-context.md`).
- **Letter suffixes** (`5a`, `7a`) describe **sub-steps inside a phase** (e.g. companion script after a numbered step) — **inside the phase markdown**, not extra table rows.

### Concepts and cross-cutting artifacts (generic — all skills)

**This section is the generic rule.** A **skill** packages **concepts** (ideas, definitions, invariants, roles) and **artifacts** (outputs, schemas, manifests) that the workflow references across **multiple stages or phases**. Anything that would be **repeated** if pasted into every phase file should instead live in **its own file** (usually markdown under `content/parts/`, sometimes JSON alongside) so there is a **single source of truth**.


| Guideline           | Meaning                                                                                                                                                                                                         |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **When to extract** | If a concept or artifact **spans** more than one phase (or stage), give it a **dedicated** doc (or structured file) and **link** from phase bodies — do not duplicate long definitions in each phase.           |
| **Naming**          | Conventional filenames (`glossary.md`, `concepts.md`, `artifacts.md`, `roles/`*, etc.) vary by skill; **discover** and **validate** presence from templates and this skill’s `build.py`, not one global layout. |
| **Not every skill** | A minimal skill might only have `SKILL.md`, `content/parts/process.md`, and phase files — **no** separate “domain” or “story map” layer. That is valid.                                                         |


### Library vs phase documents (authoring split)

**`library/`** answers **what** (stable meaning for ideas and artifacts that **more than one** phase touches). **`phases/<slug>.md`** answers **how for this step** (operator procedure: inputs, outputs, ordered steps, **commands**, done checks).

| In **`library/`** | In **`phases/`** (not a second copy of the whole library) |
| --- | --- |
| Definitions, tables, schemas, vocabulary used across phases | Purpose of **this** phase, **steps**, checklists, **script/CLI** lines |
| Single source of truth for a construct that spans the pipeline | **Links** into the right **`library/`** shard for depth |
| Optional injection slices (`abd:begin` / `abd:end`) | **No** long normative essays that other phases would repeat verbatim |

**Do not** put **numbered phase procedures**, **order-of-operations** for the skill, or **phase-to-phase sequencing narrative** in **`library/`**—that belongs in **`process.md`** and the relevant **`phases/`** files. **Do not** park **large** reusable specs only inside one phase file if another phase needs the same text—extract to **`library/`** and link.

Normative detail for writers: [`documentation-standards.md`](documentation-standards.md) and [`../../rules/content-placement.md`](../../rules/content-placement.md).

### Optional pattern — domain narrative + interaction tree (maps-models–class skills only)

Some skills (notably **abd-maps-models-specs** and similar) **choose** to separate **two parallel artifacts** that must stay in sync. **Do not** treat this table as the default for **all** skills — only for skills that explicitly adopt this shape.


| Piece                            | Role                                                                                                                                                                                                    | Typical location (example skill)                                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Domain narrative**             | **State and structure** — modules, **domain concepts** (CRC-style: owns, properties, operations, `extends`, invariants), evidence hooks. Answers **what things are** and **what owns which rules**.     | e.g. `parts/domain.md` + evolving `map-model-spec.json` (`modules_and_epics`, `concepts[]`, chunk citations). |
| **Story map / interaction tree** | **Behavior** — epics, sub-epics, stories, scenarios; **Trigger / Response**; **Pre-Condition**; **Given/When/Then** where required. Answers **who does what** and how behavior references domain state. | e.g. `parts/story-map.md` + nested JSON under epics (`stories`, `sub_epics`, etc.).                           |


**When this pattern applies**

- **Same vocabulary:** Domain concept names (`concepts[].name`) and story references can be held to **one namespace** — scanners may enforce **exact string match** where the skill defines that rule.
- **Evidence ladder / paired edits:** Concepts may carry `evidence_stage`; **domain** vs **journey** edits are **paired** in skills that implement both files.
- Skills **without** this split still use the **generic** rule above: cross-cutting concepts → **their own** markdown (whatever the skill calls them), not repeated per phase.

### Rules and automated checks (default wiring)

For **machine-enforceable** rules, use the **base framework** in **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)**:

- Declare **rule → scanner** bindings in **`rules/scanners.json`** (`rule_scanner_bindings`).
- List **ordered post-merge steps** under **`skill-config.json` → `operator.build_pipeline`**; **`scripts/build.py`** runs them after merges (same pattern as **`abd-maps-models-specs`**).
- Keep **`operator.scanners`** consistent with those scripts for **`operator.run_operator()`** / CI.

**Process tables** should **not** enumerate every scanner as if it belonged to a single phase; document automation at the skill level and link **`rules/scanners.json`** + **`build.py`** / **`build_pipeline`**.

## 3.2 Rule file naming (heuristic standard)

Target pattern (flexible regex for validation):

```text
{phase-or-stage}__{domain-concept-or-scope}__{short-rule-name}.md
```

Examples mirror **story synchronizer / maps-models** style: scanners and rules tied to **phase** and **concept** (e.g. `chunks_must_be_referenced`, `concept-layering-scaffold`). **Propose** names from the **phase** + concept + verb (and step text inside the phase doc if needed), then **check uniqueness** under `parts/rules/`.

## 3.3 Assembly model (static vs dynamic)

**Two different “static vs dynamic” pairs** — do not conflate:

1. **`build.py` assembly** (repo artifacts): Each skill ships `scripts/build.py`. It merges **process + library + phases (+ rules)** into **`AGENTS.md`** and optional **`content/built/`**. Flags like `--assembly static|snapshot` are **per skill** when present.

2. **AI-chat prompt generation** (`generate_prompt`): For **AI-driven** phases only — **dynamic** = assemble instruction string from sections; **static** = emit text from **pre-built** phase file under `phases/built/` (or documented path). See [`process-approach.md`](process-approach.md).

**Per skill:** `build.py` is the **authoritative** merge driver for **this** repo; scaffolding **emit or check** trees — they do **not** replace `build.py`.

**Flag on `build.py`:** The skill’s `build.py` may expose **CLI flags** for snapshot vs interactive merge; exact names are per skill. For **prompt** modes, document **`generate_prompt`** (or equivalent) next to **`build.py`** in **`README`** / **`AGENTS.md`**.


| Mode (merge / delivery) | Mechanism                                                                               | When                                                               |
| ----------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Static (merge)**      | `build.py` merges **built-phase** fragments into `AGENTS.md` / `SKILL.md` (and related) | Release, reproducible snapshot; CI; “what ships”.                  |
| **Dynamic (merge)**     | Runtime concatenation by **phase** / **operation** from `skill-config.json` + manifest  | Interactive sessions, partial rebuild, IDE-driven iteration. |


A **host** (CI, IDE, or orchestrator) may emit an **internal** manifest (JSON or YAML) for a **given generation run**, listing which fragments form which artifact for both modes; the skill’s `build.py` **may read** that manifest (or embedded config) when implementing **static** merges and documents how **dynamic** mode resolves fragments at runtime. That manifest is **optional** and **not** a standard every skill must carry — only **documented** `build.py` behavior is.

## 3.4 Reference skills (illustrative)

Other skills in the monorepo **illustrate** patterns (long `AGENTS.md`, phased pipelines, rules + scanners). They are **examples**, not extra requirements. **Operator** checks and layout rules are grounded in **abd-skill-builder** library files and each skill’s **`skill-config.json`** — not in a separate “corpus” file unless your team adds one.


---

### `builder-vs-operator.md`

# Builder vs Operator (today)

**Generation / scaffold (“builder” in the loose sense):** Anything that **emits** a new skill tree — typically **`abd-skill-builder`’s `scripts/scaffold_skill.py`** plus templates — producing `SKILL.md`, `skill-config.json`, phase markdown, `rules/` stubs, `scripts/build.py`, optional scanners. Output should match **§3** layout and avoid embedding customer “gold” solutions in the template.

**Operator (structural gate):** **`agentic-skill-builder`** **`operator.run_operator()`** — validates `skill-config.json`, runs a **Python compile check** on the paths in **`operator.compileall_paths`** (the implementation uses Python’s **`compileall`** module), runs **`operator.build_script`** (typically `python scripts/build.py`), then runs **scanner scripts** listed under **`operator.scanners`**. A normative skill also declares **`operator.build_pipeline`**: the **ordered post-merge steps** that **`build.py`** runs after writing **`AGENTS.md`** / built slices (rule-bound scanners, emitters, manifest, lint—**per skill**). **Rule → scanner** bindings live in **`rules/scanners.json`**; see **[`rules-and-automated-checks.md`](rules-and-automated-checks.md)** (base framework for all skills). Operator does **not** create greenfield skills; that is **`scaffold_skill.py`** and authoring.

**This skill’s role:** Ship **standards** under **`content/parts/library/`**, **process + phases**, **`scaffold_skill.py`**, and **templates** so authors get a compliant tree first, then Operator keeps it green.


---

### `rules-and-automated-checks.md`

# Rules and automated checks (base framework for every skill)

**Status:** **Normative default** for Open Agent Skills in this repo. When a skill defines **governance rules** (`rules/*.md`) and wants **machine enforcement**, wire checks this way—not as one-off phase script call-outs.

## What owns what

| Layer | Owns |
| --- | --- |
| **`rules/<stem>.md`** | The **human-readable rule**: scope, must/should, examples, done criteria. |
| **`rules/scanners.json`** | **Which script enforces which rule** — `rule_scanner_bindings[]` maps `rule_id` + `rule_file` → `scanner` path (relative to skill root). Optional top-level **`scanners`** lists scanner scripts for tooling that expects a flat array. |
| **`skill-config.json` → `operator.build_pipeline`** | **Ordered post-merge steps** that **`scripts/build.py`** runs after it writes **`AGENTS.md`** / **`content/built/`** (or your skill’s equivalent). Entries are typically **`scripts/...py`** paths: rule-bound scanners, emitters, manifest generators, rule-example linters, etc. **Empty or omitted** means “merge only” (skills with no automated checks yet). |
| **`skill-config.json` → `operator.scanners`** | **Operator / CI gate** — paths **`agentic-skill-builder`** **`operator.run_operator()`** runs **after** **`operator.build_script`**. **Keep these paths aligned** with the scanner steps you care about (usually the same modules listed in **`build_pipeline`** and/or **`rules/scanners.json`**), so “green build” and “green operator” mean the same checks. |

## What you do not do

- **Do not** treat **scanners** as **phase-owned scripts** in **`process.md`** process tables. Phase rows are for **human/AI procedure** and **merge / emit** entry points (e.g. `python scripts/build.py`), not for listing every validator. If readers need detail, add a short **“Rules and automated checks”** subsection in **`process.md`** that points here and to **`rules/scanners.json`**.
- **Do not** bind scanners only in prose. If a rule is machine-checked, add a **`rule_scanner_bindings`** row and a **`build_pipeline`** step (and **`operator.scanners`** / Operator docs as required by your host).

## Execution flow (mental model)

1. Author edits **`content/parts/`**, **`rules/`**, **`skill-config.json`**.
2. **`python scripts/build.py`** merges instruction bundles, then runs **`operator.build_pipeline`** in order (if present).
3. **Operator** (or CI) runs compile check → **`build.py`** again → **`operator.scanners`** (when configured).

**Reference implementation:** **`abd-maps-models-specs`** — `rules/scanners.json`, **`operator.build_pipeline`** in **`skill-config.json`**, and **`scripts/build.py`** driving the pipeline after merge.

## Scaffolded skills

Greenfield trees from **`scaffold_skill.py`** should ship **`rules/scanners.json`** (even if bindings start empty) and a **`skill-config.json`** fragment that includes **`operator.build_pipeline`** alongside **`operator.scanners`**, so authors extend **one** pattern instead of inventing ad hoc wrappers.

See also: **[`skill-standards-section-3.md`](skill-standards-section-3.md)** (§3.1 config row), **[`builder-vs-operator.md`](builder-vs-operator.md)**, **`rules/README.md`** at the skill root.


---

## Rules

*No rules for this phase. List rule stems (filename without `.md`) under `skill-config.json` → `phase_rules` for this phase slug, and optionally `every_phase_rules` for rules that apply to every phase. See `parts/library/process-approach.md` § Phase bundle — rules.*


---
