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
