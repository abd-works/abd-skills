# Process — {{skill_name}}

**Read first in every phase:** **[Principles](library/principles.md)** (then other **library** shards linked from the phase doc, including **[critical quality steps](library/critical-quality-steps.md)** when present).

**Pipeline:** **[Workspace and config](phases/workspace-and-config.md)** → **[{{phase_name}}](phases/{{phase_slug}}.md)** → **[{{code_phase_name}}](phases/{{code_phase_slug}}.md)** → **Stage 3 — validation** (**`python scripts/base/build.py`** and **`build.scanners`** when wired)

**Navigation spine:** **Standards** → **[Workspace and config](phases/workspace-and-config.md)** → **{{phase_name}}** → **{{code_phase_name}}** → **Validation**

**Structural reference:** Copy layout and filenames from **`skill-scaffold/`** in **abd-skill-builder** — real directories, example files, comments. **Rich vs minimal `process.md`:** **[Skill structure and concepts — rich process table](library/skill-structure-and-concepts.md#rich-process-table-team-plate)** and **[process-phases.md](library/process-phases.md)**. Field-by-field authoring for scaffolded files is described in **library** shards; align **`content/parts/process.md`** with **`skill-config.json` → `phase_files`**.

---

## Outcome of this process

You finish with a **skill** where **instructions match the repo**: **`content/parts/process.md`** and **`phases/*.md`** align with **`skill-config.json`**; **`library/`**, **`rules/`**, and **`scripts/`** match **`SKILL.md`** and the agreed scope (see **`content/parts/library/base/checklist.md`** for how checklists are created and tracked). **Confirm** scope after **Stage 1** before heavy **Stage 2** edits; run **Stage 3** before you treat the skill as done.

---

## High-level principles

### Capabilities (what this process enables)

| Capability | Problem it addresses |
| --- | --- |
| **Parts-based instructions** | Ad-hoc chat drifts from the repo; nothing to diff or review. |
| **Process table ↔ `phase_files` ↔ `phases/*.md`** | Lost ordering, missing phases, or slugs that disagree with **`skill-config.json`** / **`build.py`**. |
| **Rules + scanners + `build.py`** | Violations that look fine until runtime; hand-edited merges hiding regressions. |
| **Staged confirmation** | Large wrong commits before the user can correct course. |

### Principles (normative)

1. **Author prompts from parts:** Build injected text from **`content/parts/library/`**, **`content/parts/phases/`**, **`rules/`**, and **`content/parts/process.md`**. Use **`skill-scaffold/`** as the folder blueprint when extending layout.
2. **Process table is the map:** Every phase slug in **`skill-config.json` → `phase_files`** has a row in the tables below (seven columns per **[process-phases.md](library/process-phases.md)**) and a file at **`content/parts/phases/<slug>.md`**. Phase **0** is always **Workspace and config** when this skill routes workspace.
3. **Quality and validation:** **Rules** → **scanners** → fix → **`python scripts/base/build.py`**. Fix **sources** under **`content/parts/`**, **`rules/`**, **`scripts/`** — not hand-edited **`AGENTS.md`**. See **[rules-and-scanners.md](library/rules-and-scanners.md)**.
4. **Confirm before you lock:** Align on components after **Stage 1**; complete **Stage 2** with checkpoints before **Stage 3** validation.

---

## Rules and automated checks (all skills)

**Default framework:** **[library/rules-and-scanners.md](library/rules-and-scanners.md)** — bind scanners to **`rules/`**, wire **`rules/scanners.json`**, align **`skill-config.json` → `build.build_pipeline`** and **`build.scanners`** with **`python scripts/base/build.py`**.

---

## Stage 0 — Workspace and config

### Purpose

Nail **where the skill runs**: **`skill_path`**, **`skill_workspace`**, **`skill-config.json`**, **`active_skill_workspace`**. Routing detail lives in **[Workspace and config](phases/workspace-and-config.md)**.

### What you produce

**`skill-config.json`** with correct **`active_skill_workspace`** for the project tree the skill reads and writes.

### How you know you succeeded

**`python scripts/base/set_workspace.py`** (no args) prints the expected workspace; paths resolve for later phases and **validation**.

### Phase table

| # | Phase | Description | Actor | Input | Output | Scripts |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | [Workspace and config](phases/workspace-and-config.md) | Set workspace path; install **`skill-config.json`**; confirm skill and workspace roots. | Human / AI | Skill directory; target project tree | **`skill-config.json`** correct | `python scripts/base/set_workspace.py <path>` |

---

## Stage 1 — {{phase_name}}

### Purpose

**Primary skill work** for this scaffold: {{phase_description}} Align **`content/parts/process.md`** and **`skill-config.json` → `phase_files`** before you depend on merge output.

### What you produce

{{phase_output}} (see **[{{phase_slug}}](phases/{{phase_slug}}.md)**).

### How you know you succeeded

Inputs and outputs for this phase match **`phases/{{phase_slug}}.md`**; user has confirmed direction if the skill is collaborative.

### Phase table

| # | Phase | Description | Actor | Input | Output | Scripts |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [{{phase_name}}](phases/{{phase_slug}}.md) | {{phase_description}} | Human / AI | {{phase_input}} | {{phase_output}} | Follow **[{{phase_slug}}](phases/{{phase_slug}}.md)** with this skill attached |

---

## Stage 2 — {{code_phase_name}}

### Purpose

{{code_phase_description}} Wire automation under **`scripts/{{skill_name}}/`** and **`build`** as needed.

### What you produce

{{code_phase_output}}

### How you know you succeeded

Scripts and **`skill-config.json` → `build`** match the validation you intend; **`python scripts/base/build.py`** runs for merge checks.

### Phase table

| # | Phase | Description | Actor | Input | Output | Scripts |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | [{{code_phase_name}}](phases/{{code_phase_slug}}.md) | {{code_phase_description}} | Code | {{code_phase_input}} | {{code_phase_output}} | `python scripts/{{skill_name}}/{{code_phase_script}}` · `python scripts/base/build.py` |

---

## Stage 3 — Structural validation

### Purpose

Prove **Python** compiles (when **`build.compileall_paths`** is set), **merge** succeeds, **scanners** pass. Exit **0** on the full chain.

### What you produce

Clean **validation** run; **`AGENTS.md`** and optional **`content/built/`** consistent with **`content/parts/`** when using **`static_built`**.

### How you know you succeeded

**CI or local:** **`compileall`** on paths from **`skill-config.json`** → **`python scripts/base/build.py`** → **`build.scanners`**. Fix **sources**, not **AGENTS.md**.

### Phase table

| # | Phase | Description | Actor | Input | Output | Scripts |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | *(validation)* | **Structural gate:** compile (if configured) → **`build.py`** (merge + **`build.build_pipeline`**) → **`build.scanners`**. | Code | Skill root; **`skill-config.json`** | Exit **0**; built artifacts match **parts** | `python scripts/base/build.py` *(and scanners configured in **`skill-config.json`**)* |

---

## Scripts layout

**From the skill directory**, the usual commands are **`python scripts/base/build.py`** (merge + validation when configured) and **`python scripts/base/set_workspace.py …`**. Shared implementation lives under **`scripts/base/`** (merge into **`AGENTS.md`**, workspace, **`skill_root.py`**, **`skill.py`**, **`instructions.py`**, …). **Bundled rules**, rule tables, listing scanners, and **running scanners** use **`skills/execute_rules/scripts/`** in **abd-skill-builder** (`bundle_rules_into_skill_md.py`, **`rule_inventory.py`**, **`run_scanners.py`**). Optional scanner CLI scripts go under **`scanners/`** (e.g. **`*-scanner.py`** beside scanner modules), with **`scanner:`** in rule frontmatter as in **execute_using_rules**.

**Only in the abd-skill-builder repo:** **`scripts/scaffold_skill.py`** — create a new skill from **`skills/build_skill/templates/skill-scaffold/`** and copy **`scripts/base/`** from the builder.

Skill-specific scripts (owned by this skill):

```
scripts/{{skill_name}}/   Scripts specific to this skill
  {{code_phase_script}}   {{description}}
```

> **Convention:** all scripts you write for this skill go under `scripts/{{skill_name}}/`.
> Never add skill-specific logic directly to `scripts/base/`.
