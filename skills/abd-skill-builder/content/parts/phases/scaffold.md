# Phase: Scaffold

For an **existing** skill tree (not greenfield): **[`plan-migrate.md`](plan-migrate.md)** (**1b**) — **delta** + user selection; then **[`migrate.md`](migrate.md)** — **execute** moves. Do **not** use **`scaffold_skill.py`** on an existing tree.

**Greenfield:** Pipeline order is **[`process.md`](../process.md)**. Complete **[plan-script-build](plan-script-build.md)** (library norms + **`content/parts/library/base/checklist.md`**) before you run this scaffold sequence—**or** accept that **scaffold** will copy **`library/base/`** (including **`checklist.md`**) from **abd-skill-builder** for you.

---

## Base scripts from abd-skill-builder (what scaffold emits)

**`scripts/scaffold_skill.py`** in **abd-skill-builder** builds a new skill under **`--out`** by:

1. Copying **`templates/skill-scaffold/`** (content, rules, tests, **`scripts/scanners/`**, **`scripts/<skill_name>/`**, etc.) with **`{{…}}` substitutions**.
2. Copying the **`scripts/base/`** package from **abd-skill-builder** — **`build.py`**, **`generate.py`**, **`set_workspace.py`**, **`Skill.load()`**, **`Instructions`**, **`workspace_checklists`**, **`skill_root`**, etc. Run from skill root: **`python scripts/base/build.py`**, **`python scripts/base/generate.py`**, **`python scripts/base/set_workspace.py`**.

So **greenfield skills** get the same checklist automation and **`generate.py`** behaviour as **abd-skill-builder** in **one** scaffold step; there is no second, divergent **`generate.py`** under **`templates/`**. After scaffold, you **extend** merge lists and phase slugs to match your **`parts/phases/*.md`** and **`parts/library/`**.

| Piece | Source | Role | What you extend |
| --- | --- | --- | --- |
| **`scripts/base/generate.py`** | **abd-skill-builder** **`scripts/base/generate.py`** (copied) | Phase bundle for AI chat; **`ensure_workspace_checklists`** when workspace is set. Imports **`Skill`** and helpers from **`scripts/base/`**. | Rarely—upgrade by re-copying from builder or cherry-picking **`scripts/base/`**. |
| **`scripts/base/set_workspace.py`** | **abd-skill-builder** **`scripts/base/set_workspace.py`** (copied) | Prints or sets **`active_skill_workspace`** in **`skill-config.json`** → **`workspace`**. | Same as above. |
| **`scripts/base/build.py`** | **abd-skill-builder** **`scripts/base/build.py`** (copied) | Merges **`process.md`** + **`library/*.md`** + **`phases/*.md`** → **`AGENTS.md`** (+ **`content/built/`**); then **`build.build_pipeline`** when wired (see **[`../library/rules-and-scanners.md`](../library/rules-and-scanners.md)**). Uses **`scripts/base/instructions.py`** and related modules. | **`LIBRARY_FILES`** / **`PHASE_FILES`**; link rewrites; custom steps in **`scripts/base/build.py`** (or shared helpers under **`scripts/base/`**) if needed. |
| **`scripts/scanners/scanner_<rule>.py`** | **`templates/skill-scaffold/scripts/scanners/`** (templated) | Example scanner stub; wire in **`rules/scanners.json`**. | Replace with real checks. |

**Structural validation** expects **`skill-config.json`** to list **`build.build_script`** (typically **`python scripts/base/build.py`**) and **`build.compileall_paths`**. **`generate.py`** is not part of that gate—it is for **human/AI sessions** running a phase prompt.

---

## Other scaffolded paths (brief)

| Path | Notes |
| --- | --- |
| **`skill-config.json`** | From **`templates/skill-scaffold/`** — includes **`workspace`**, **`build`**, **`delivery`**, and optional **`build_strategy`** (purpose / outline keys used by **`build.py`** / **`instructions.py`**) in one manifest. |
| **`parts/process.md`** or **`content/parts/process.md`** | Copied from **`templates/skill-scaffold/content/parts/process.md`** — enrich and run phases per **[`process-phases.md`](../library/process-phases.md)** and **[Skill structure and concepts — rich process table](../library/skill-structure-and-concepts.md#rich-process-table-team-plate)**. |
| **`content/parts/library/base/checklist.md`** | Copied with **`library/base/`** from **abd-skill-builder** by **`scaffold_skill.py`** — see **[How checklists are created](../library/base/checklist.md)** and **[Plan Script Build](plan-script-build.md)**. |
| **`phases/workspace-and-config.md`** | **Not** always emitted by minimal scaffold—**add** **`workspace-and-config.md`** under **`parts/phases/`** (copy from **abd-skill-builder** or follow **`process-phases.md`**) so **Phase 0** / **Workspace and config** exists. Wire it **first** in **`build.py`** **`PHASE_FILES`** and add a process table row with **`#`** **`0`**. |

If **`skill-scaffold/`** is missing from your **abd-skill-builder** checkout, scaffold cannot run — use a complete repo tree.

---

## Steps (greenfield)

1. **Checklist rules + plan:** Read **[how checklists are created](../library/base/checklist.md)** and **[skill-structure-and-concepts.md](../library/skill-structure-and-concepts.md#authoring-checklist--injector-body)**; **`scaffold_skill.py`** copies **`content/parts/library/base/`** (including **`checklist.md`**) into the new skill. Align **build intent**, rules/scanners, **`library/`**, **`delivery.mode`**, then release sign-off with the user.
2. Choose a **skill id** (directory name; kebab-case recommended).
3. Run `python scripts/scaffold_skill.py --name <id> --out <parent>/<id>` (from **abd-skill-builder** or your packaged builder).
4. Edit **`skill-config.json`** → **`build_strategy`** — set **`skill_purpose`** (short headline of what the skill does). Align **`content/parts/library/outline.md`** if your build uses it for the AGENTS outline.
5. **Wire scripts:** Extend **`scripts/base/build.py`** / **`scripts/base/generate.py`** as needed; add **`parts/phases/workspace-and-config.md`** and process row if the minimal tree omitted them.
6. Flesh out **`content/parts/process.md`** and phase files. For a **rich** process doc, follow **[Skill structure and concepts — rich process table](../library/skill-structure-and-concepts.md#rich-process-table-team-plate)**; follow **`process-phases.md`** for columns and workspace phase. Use **[process-phases.md](../library/process-phases.md)** for **`generate.py`** / **`build.py`**. Add rules and scanners as needed.
7. Add tests under **`test/`** (scaffold emits **`test/README.md`**); put fixtures in **`test/fixture/…`** and any **`active_skill_workspace`** under **`test/<name>/`** per **[skill-structure-and-concepts.md](../library/skill-structure-and-concepts.md)** (test layout norms).
8. Run `python scripts/base/build.py` (and any CI/scanner checks your repo uses).
9. **Fill the scaffold (content):** Use **[`fill-scaffold-parts.md`](fill-scaffold-parts.md)** (**process** phase **2c**) — AI + user **author** **`library/`**, **`rules/`**, and richer **process**/**phases** from **`SKILL.md`** and agreed scope. Emit the phase prompt with `python scripts/base/generate.py --phase fill-scaffold-parts`.

## Anchor

This phase **writes** the skill tree and **establishes** the build and delivery contract — no domain modeling yet.
