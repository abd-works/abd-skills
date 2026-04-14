# Phase — Plan Script Build

This is **phase 1a** in [`../process.md`](../process.md) (**Stage 1 — Plan**). Read **library/** norms and **[how checklists are created](../library/base/checklist.md)** (stable under **`library/base/`**) together with **[skill-structure-and-concepts.md](../library/skill-structure-and-concepts.md#authoring-checklist--injector-body)** before **scaffold** or heavy edits. For **existing** skills, **migration planning** (inventory + **standards delta**) is **[`plan-migrate.md`](plan-migrate.md)** (**1b**), not this file.

**Checklists:** The **normative** description of checklist mechanics is **`content/parts/library/base/checklist.md`** (copied with **`library/base/`** when you scaffold). **Live** session progress is tracked under **`<active_skill_workspace>/<skill_name>/progress/`** by **`generate.py`** — see **`base/checklist.md`** and **`workspace_checklists.py`**.

**Workspace, `skill-config.json`, `active_skill_workspace`:** **[Workspace and config](workspace-and-config.md)** — full terms and keys under **[Skill path, skill workspace, and configuration](workspace-and-config.md#skill-path-skill-workspace-and-configuration)**. Do **not** re-derive routing here.

## Purpose

Load the **standards in `library/`** so **scaffold** (and, for existing skills, **plan-migrate** + **migrate**) work targets the same rules (§3, **`build.*`**, **`delivery.mode`**, **`test/`** expectations). Capture agreements on phases, delivery, and workspace in **`content/parts/process.md`** (and session notes if needed)—**not** a separate plan file under **`docs/`**.

## AI-chat phases: generate (what to read in the AI session)

For any phase that you run as an **AI-chat** step (see **[Skill structure and concepts — §3](../library/skill-structure-and-concepts.md#skill-structure-sec3)** and **[agent-skill-model.md](../library/base/agent-skill-model.md)**), you **call the generator** with the **phase slug**, then **read the printed text** as the instructions for that session—not improvised prose.

From the **skill root** (where **`scripts/`** lives):

```bash
python scripts/base/generate.py --phase <phase_slug>
```

- **`<phase_slug>`** — filename of the phase markdown under **`parts/phases/`** (or **`content/parts/phases/`**), **without** `.md`. Example: this file is **`plan-script-build.md`** → `--phase plan-script-build`.
- **`--mode dynamic`** (default) — reads **`phases/<slug>.md`** from source.
- **`--mode static`** — reads **`phases/built/<slug>.md`** after **`build.py`** has materialized it (if your skill uses built phase blobs).

**Scripts:** **[`generate.py`](../../scripts/base/generate.py)** (entry point) and **[`generate_prompt.py`](../../scripts/generate_prompt.py)** (same CLI). **`build.py`** assembles **AGENTS.md** / bundles; **`generate`** only answers “what instruction block for **this** AI phase?”—orthogonal jobs.

## What you produce

- Shared understanding of **library/** norms (including **`library/base/checklist.md`**), **delivery mode**, **phase order**, and **components** (reflected in **`content/parts/process.md`** and **`skill-config.json`**).

## How you know you succeeded

**`content/parts/process.md`** and **`skill-config.json`** reflect agreed pipeline and workspace; **`library/base/checklist.md`** is present (greenfield: copied with **`library/base/`** from **abd-skill-builder** via **`scaffold_skill.py`**). You know how **workspace `progress/`** checklists relate to **`generate.py`** (see **`base/checklist.md`**).

## Input / output / scripts (summary)

**Inputs:** **library/** norms; target workspace. **`skill-config.json`** / **`active_skill_workspace`** are covered in **[Workspace and config](workspace-and-config.md)**.

| | |
| --- | --- |
| **Input** | **library/** norms; workspace where the skill package will live. |
| **Output** | Process alignment in **`content/parts/process.md`** / **`skill-config.json`**; clarity on **`library/base/`** checklist norms and **`progress/`** checklists. |
| **Scripts / templates** | **`scaffold_skill.py`** copies **`content/parts/library/base/`** from **abd-skill-builder**. For **AI-chat** phases: **`python scripts/base/generate.py --phase <slug>`** — see **[AI-chat phases: generate](#ai-chat-phases-generate-what-to-read-in-the-ai-session)** above. Planning does **not** require **build**. |

## Steps

1. Open **[skill-structure-and-concepts.md](../library/skill-structure-and-concepts.md)** (repo layout, `skill-config.json` roles, **[authoring checklist — injector body](../library/skill-structure-and-concepts.md#authoring-checklist--injector-body)**) and **[checklist.md](../library/base/checklist.md)**.
2. Ensure **`content/parts/library/base/checklist.md`** exists (greenfield: **scaffold** copies **`library/base/`**; existing skill: copy **`base/`** from **abd-skill-builder** or merge **`checklist.md`** only).
3. Work through agreed process rows; leave the next scaffold/migrate steps visible until Stage 2.
