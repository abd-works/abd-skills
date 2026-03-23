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
