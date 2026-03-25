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
