# Process — abd-skill-builder

**In order:** Standards & checklist → **Scaffold or migrate** → **Operator** (automated checks)

## Outcome of this process

You finish with a **skill** where the instructions you give the model **match what the skill actually says**, so work does not drift off-script. **Stages and phases** break the work into clear chunks; **steps** sit in phase files; **checklists** help you pick up after a break or a handoff. **Rules** say what must stay true; **scanners** and the other **automated checks** (Python validity on the paths you configured, **build**, scripts listed in config) **catch** when the **files in the repo** no longer match those rules. *Inputs, scripts, templates, and “done” outputs are spelled out in the **phase tables** below—not in a separate inventory.*

## High-level principles

- **Instructions match the skill:** Build prompts and injected text from what the skill already wrote in **library/**, **phases/**, and **rules/**—not off-the-cuff chat.
- **Stages, phases, and checklists:** The process **table** is the map; **steps** live inside phase files. **Checklists** (including the authoring checklist) keep long or stop-and-start work ordered so you can resume.
- **Quality process (rules → scan → assess → fix):** Keep must-holds in **rules/**, and **bring those rules into what the model sees**—prompt or injected sections—so work is **guided**, not guessed. Then **run scans** (small scripts or checklists). Then **check** the result against the rules (by eye or with automation). Then **fix** and **log** corrections so the next pass improves. Before you **commit**, the **Operator** checks still run: **Python files** in the folders listed in `**skill-config.json`** must **compile** (syntax/validity), then `**build.py`**, then **scanners**. *Same idea at full depth (iterate with corrections):* [abd-shaping](../../../../backup/abd-shaping/SKILL.md).
- **Assemble from parts:** You author a skill as **parts**—process, **library/**, phase files, **rules/**—and **build** stitches them into the **whole** the tools load (**AGENTS.md**, and—when you choose **static** delivery—checked-in slices under **content/built/**). **Dynamic** delivery still uses the same parts; the executor **combines them at run time** instead of reading a pre-merged file. Either way the **parts** are the source of truth; the **whole** must not drift. **Scaffold** (**scaffold_skill.py**) vs **migrate** (**phases/migrate.md**) is only how you **create or fix** the folder; phase order stays in this file’s **#** column and **build.py**’s lists—not in filenames. *Details:* [delivery-modes](library/delivery-modes.md).

## Stage 1 — Plan

### Purpose

Load the **standards in `library/`** and the **authoring checklist** so scaffold/migrate work targets the same rules (§3, operator, `**delivery.mode`**, `**test/**` expectations). If the skill resolves paths outside its install folder, set `**conf/abd-config.json**` → `**active_skill_workspace**` (customer or solution tree).

### What you produce

- Confirmed understanding of **§3** directory rules and **process table** semantics.
- A tracked checklist (copy `**library/authoring-checklist.md`** to `**<skill>/docs/authoring-checklist.md`** in the skill you are editing) with `**- [ ]` / `- [x]**` progress.

### How you know you succeeded

You can say where the **authoritative** text lives (**library/** vs **docs/**), and you have a **first unchecked** checklist item to pick up next time if work pauses.


| #   | Phase                                | Description                                                                                                                               | Actor      | Input                                                                                                                                                                                                                                                                            | Output                                                       | Scripts | Ref                                                                                                                               |
| --- | ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Read standards & authoring checklist | You open the index and full §3, then work the checklist (ask / AI-suggest / track). This grounds every later file move in the same norms. | Human / AI | **library/** files: [index](library/skill-repo-standards.md), [§3](library/skill-standards-section-3.md), [checklist](library/authoring-checklist.md); optional copy of checklist under **your skill** **docs/**; **workspace** routing via **conf/abd-config.json** when needed | Updated checklist boxes; clear picture of checks vs delivery | —       | [index](library/skill-repo-standards.md), [§3](library/skill-standards-section-3.md), [checklist](library/authoring-checklist.md) |


---

## Stage 2 — Create or fix the skill

### Purpose

Either **emit** a new compliant **skill** (**greenfield**) or **align** an existing one (**migrate**) without silent wholesale rewrites.

### What you produce

- **Greenfield:** New directory with scaffolded `**SKILL.md`**, `**skill-config.json`**, `**conf/**`, `**content/parts/**`, `**scripts/**`, `**rules/**`, `**test/**`.
- **Migrate:** Delta report (gaps vs standards) and **only** user-approved edits.

### How you know you succeeded

- Greenfield: `**python scripts/build.py`** runs in the new skill; Operator can run against it.
- Migrate: Delta rows are **fixed**, **deferred**, or **accepted risk** with rationale.


| #   | Phase                        | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Actor      | Input                                                                  | Output                                                                                                           | Scripts                                                                                     | Ref                            |
| --- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------ |
| 2a  | Scaffold new skill directory | You choose a **kebab-case** skill id and run the scaffold. It copies from **templates/** at the skill root (`SKILL.md.template`, `process.md.template`, `child_build.py.template`, …), creates **conf/**, **content/parts/**, **scripts/**, **rules/**, **test/**, and copies **authoring-checklist.md** into the new skill **docs/**. You get a minimal **process.md**; replace or enrich it with the **team process plate** (**content/parts/templates/process-team.md.template**; see **content/parts/templates/README.md**) when you need stages, inputs/outputs, and a full phase table. Then run `**python scripts/build.py`** in the new skill so **AGENTS.md** and **content/built/** (if static) match **content/parts/**. Heavier skills may add **scripts/generate_prompt.py** (optional phase prompt helper). | Code       | `**--name`**, `**--out**` (empty or non-existent path); **templates/** | **New skill** tree; **docs/authoring-checklist.md**; built **AGENTS.md** + **content/built/** after **build.py** | `**python scripts/scaffold_skill.py`**; then `**python scripts/build.py**` in the new skill | [scaffold](phases/scaffold.md) |
| 2b  | Migrate existing skill       | You inventory the skill on disk (**SKILL.md**, **skill-config.json**, **scripts/build.py**, **content/parts/**), compare to standards, write a **delta** table (e.g. **docs/standards-delta.md** pattern), and fix **only** what the user selects—no silent full rewrites.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Human / AI | Path to existing skill                                                 | Delta markdown; targeted patches; user-approved edits only                                                       | — (optional helper scripts per skill)                                                       | [migrate](phases/migrate.md)   |


---

## Stage 3 — Structural validation (Operator)

### Purpose

Show the **skill** **passes automated checks**: Python files under the configured folders compile (syntax check), **build** finishes, scanners return success. For a minimal valid layout reference, see **agentic-skill-builder**’s **test/fixture/toy-polite-dialogue/** (not a product deliverable).

### What you produce

- Exit code **0** from `**operator.run_operator()`** (or the same steps by hand: **Python compile check** on configured paths, `**python scripts/build.py`**, then **scanners**).
- **AGENTS.md** and **content/built/AGENTS.md** byte-match when static delivery; both reflect the latest **content/parts/**.

### How you know you succeeded

CI or local check run succeeds; `**skill-config.json`** paths match files on disk.


| #   | Phase        | Description                                                                                                                                                                                                                                                                                                                                                                                                                  | Actor | Input                                      | Output                                                                            | Scripts                                                                                                         | Ref                                                                         |
| --- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- | ------------------------------------------ | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| 3   | Run Operator | You run the structural gate: **Python compile check** on the paths in **skill-config.json**, then `**python scripts/build.py`**, then each **scanner** listed there (this repo includes `**scripts/scanner_skill_builder_layout.py`** for layout sanity). Fix failures in the source files—not by editing **AGENTS.md** by hand when **build** owns it. The **skill** should match §3; **build** exit **0**; scanners **0**. | Code  | The skill directory; **skill-config.json** | Exit **0**; **AGENTS.md** + **content/built/** consistent with **content/parts/** | **agentic-skill-builder** **operator** (or same steps manually); `**python scripts/build.py`**; listed scanners | [agentic-skill-builder README](../../../../agentic-skill-builder/README.md) |


---

## Team process plate (other skills)

To author a **maps-models-specs–style** `**process.md`** (outcome, principles, inputs/outputs, per-stage tables), start from `**content/parts/templates/process-team.md.template`** and `**content/parts/templates/README.md**`.