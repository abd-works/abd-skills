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
