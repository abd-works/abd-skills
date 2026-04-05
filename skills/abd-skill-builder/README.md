# abd-skill-builder

Standalone skill for **repo layout standards**, **scaffolding new skills**, and **AGENTS.md assembly** — use it from any editor or assistant without depending on a specific host app.

**Flow:** copy the scaffold to a new directory (`scaffold_skill.py`), then **author the skill** with a human or AI using the phase docs and **`python scripts/base/build.py`** for merge + checks. There is **no** separate orchestration package in this repo.

**Normative bodies** live under **`parts/library/`** (or **`content/parts/library/`**) and **`parts/phases/`**. In **this** repo, **`docs/`** holds only **`standards-delta.md`** (inventory vs §3). **How checklists are created** is **[`content/parts/library/base/checklist.md`](content/parts/library/base/checklist.md)** (stable **`library/base/`**); injector notes are in **`content/parts/library/skill-structure-and-concepts.md`** (section **## Authoring checklist — injector body**). In **your** skill, use the same **`library/base/checklist.md`** after scaffold, and track live session work in workspace **`progress/`** checklists from **`generate.py`**. Placement, voice, and library vs phase: **§3**.

**Delivery:** **`skill-config.json`** → **`delivery.mode`**: **`static_built`**. Pre-merged outputs: root **`AGENTS.md`** and **`content/built/AGENTS.md`** (identical). Merge order and commit policy: **see [Delivery & merge order](#delivery--merge-order) below**. **Commit policy:** this repo commits **`content/built/*`** after meaningful part/build changes; teams may instead regenerate in CI and omit commits (document in your fork).

## Quick start

- **Workspace and config (`skill_path`, `skill-config.json` → `workspace`, `active_skill_workspace`):** `parts/phases/workspace-and-config.md` (phase document — same folder as the other phase files)
- **§3 layout & content (normative tables) + repo map:** `content/parts/library/skill-structure-and-concepts.md` (§3 and related tables live in the same file)
- **Layout & scaffold:** [`content/parts/library/skill-structure-and-concepts.md`](content/parts/library/skill-structure-and-concepts.md) (repository table, **`library/base/`** vs **`library/required/`**) and [`templates/skill-scaffold/`](templates/skill-scaffold/) — emitted by **`scripts/scaffold_skill.py`**
- **Build vs validation:** `content/parts/library/skill-structure-and-concepts.md` (layout, pipeline) and `content/parts/library/rules-and-scanners.md` (merge, scanners)
- **How checklists work (normative):** [`base/checklist.md`](content/parts/library/base/checklist.md) + **`skill-structure-and-concepts.md`** (**## Authoring checklist — injector body**)
- **Plan migration (existing skill — inventory + standards delta):** `content/parts/phases/plan-migrate.md` (**1b**)
- **Migrate existing skill (execute 1b plan):** `content/parts/phases/migrate.md` (**2b**)
- **Scaffold a new skill:**  
  `python scripts/scaffold_skill.py --name my-skill --out ../my-skill --purpose "…"`
- **Build AGENTS.md (this skill):**  
  `python scripts/base/build.py`
- **Minimal valid skill example (polite dialogue phases):** `test/fixture/toy-polite-dialogue/` — canonical layout for standards and tests in this repo.

## What this repo is

- **Standards** under **`content/parts/library/`**, **`templates/skill-scaffold/`**, and **`scripts/scaffold_skill.py`** to **create** compliant trees.
- **Validation** on a skill directory: **`python scripts/base/build.py`** (merge + scanners) plus **compile** paths from **`skill-config.json`**.
- **Stage 1** plan + checklist: **`content/parts/phases/plan-script-build.md`** — templates live under **`content/parts/library/`** (merged into **AGENTS.md** / phase bundles).

## Deploy to Cursor skills (junction)

Cursor loads installable skills from **`%USERPROFILE%\.cursor\skills\`** (each skill is a folder with `SKILL.md` at the root). To keep a **single source of truth** in this repo, use a **directory junction** on Windows:

```bat
cmd /c mklink /J "%USERPROFILE%\.cursor\skills\abd-skill-builder" "c:\dev\agilebydesign-skills\skills\abd-skill-builder"
```

- If `abd-skill-builder` already exists there, remove it first (only if it is not the junction you want): `rmdir "%USERPROFILE%\.cursor\skills\abd-skill-builder"` — **do not** use `rmdir` on the repo side; junction removal only deletes the link.
- After linking, the skill appears alongside e.g. `.cursor\skills\content-memory`.

## Delivery & merge order

**`skill-config.json`** declares **`delivery.mode`**: **`static_built`** (this repo). Optional alternate: **`runtime_injection`** (merge at load time in the host). Normative definitions: **`parts/library/delivery-modes.md`**.

### What gets built

| Output | Role |
| --- | --- |
| **`AGENTS.md`** (repo root) | Primary merged agent instructions for this skill. |
| **`content/built/AGENTS.md`** | Same bytes as root **`AGENTS.md`** — packaged slice for **`static_built`** installs / mirrors. |
| **`content/built/README.md`** | Short manifest; regenerated by **`scripts/base/build.py`**. |

### Merge order (`scripts/base/build.py`)

1. **`parts/process.md`** — under section **Process** (this repo uses **`parts/`**; scaffolded skills may use **`content/parts/`** instead).
2. **Per-phase bundles** (see **`skill-config.json`** → **`library_files`**, **`every_phase_rules`**, **`phase_bundle`**): library shards under **## Library**; optional rule stems (**`rules/<stem>.md`**) under **## Rules** when **`every_phase_rules`** / **`phase_rules`** list them. Workspace routing lives under **[Workspace and config](parts/phases/workspace-and-config.md)** (merged **`workspace-and-config`** body in **`AGENTS.md`**).
3. **Phases** (in order): **`workspace-and-config.md`**, **`plan-script-build.md`**, **`plan-migrate.md`**, **`scaffold.md`**, **`migrate.md`**, **`fill-scaffold-parts.md`** — in **`parts/phases/`** here (**`content/parts/phases/`** is the alternate layout some skills use).

Equivalence: **`runtime_injection`** would apply the same sequence when assembling the same bodies; only packaging differs.

### Regenerate

```bash
python scripts/base/build.py
```

### Commit policy for `content/built/`

This repo **commits** **`content/built/AGENTS.md`** and **`content/built/README.md`** after meaningful changes to **`parts/`** (or **`content/parts/`** if you use that layout) or **`scripts/base/build.py`**, so clones and **`static_built`** consumers see a consistent bundle without running the build first.

Teams may choose to git-ignore built files and run **`build.py`** in CI instead — if so, document that in the fork’s **`README.md`** and stop committing **`content/built/*`**.
