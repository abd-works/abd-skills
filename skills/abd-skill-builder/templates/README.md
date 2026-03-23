# Templates (`templates/`)

**Purpose:** Scaffold emits a new skill tree from these files. Some templates are **only** for **`docs/`** planning artifacts (non-runtime per §3).

| File | Use |
|------|-----|
| **`process-team.md.template`** | **Team process plate** — **Phase 0 (Workspace and config)** is **hard-coded** (same for every skill). Other sections use **`{{parameter}}`** placeholders (see the **PARAMETER MANIFEST** in the file). A **filled** example is **`parts/process.md`** in **abd-skill-builder** (same shape, real prose). Pair with **`parts/library/process-table-standards.md`** for table columns. |
| **`skill-plan.md.template`** | **Stage 1 plan** — copied to **`docs/skill-plan.md`** by **`scaffold_skill.py`**, including **## Authoring checklist** (body injected from **`parts/library/authoring-checklist.md`**). Fill during Plan: delivery mode, stages/phases, rules/scanners, library components, role, operator/workspace/delivery, then track **`- [ ]`** in the checklist section. |
| **`abd-config.json.template`** | **Workspace routing** — scaffold writes **`conf/abd-config.json`** from this file. It is **minimal JSON** (two keys), not an empty file: **`active_skill_workspace`** and **`known_skill_workspaces`**. See **`abd-config.json.template.md`** for a short explanation. Normative semantics: **`parts/phases/plan-script-build.md`** (**Skill path, skill workspace, and configuration**). |
| **`concepts.md.template`** | **Concepts / domain model** — lightweight **`parts/library/`** doc: purpose, high-level shape, format, detail, examples, validation checklist. Optional **`<!-- abd:begin <phase-slug> -->`** / **`<!-- abd:end <phase-slug> -->`** pairs match **`phase_files`** so **`generate_prompt`** / **`build.py`** include only the right fragments per phase (see **`parts/library/process-approach.md`**). |

**Scaffold:** `scripts/scaffold_skill.py` emits **`process.md`** from **`process.md.template`**, **`conf/abd-config.json`** from **`abd-config.json.template`**, and **`docs/skill-plan.md`** (from **`skill-plan.md.template`**, with the authoring checklist section filled from **`parts/library/authoring-checklist.md`**). Replace or enrich **`process.md`** with the team plate when you need a richer pipeline doc.
