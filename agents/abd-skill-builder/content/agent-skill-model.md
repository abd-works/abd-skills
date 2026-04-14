# Agent vs skill (Open Agent Skills)

This shard is **normative** for anything **abd-skill-builder** scaffolds or audits. It aligns with **Open Agent Skills**: one discoverable **`SKILL.md`**; **`AGENTS.md`** is the **assembled agent/IDE** view when a package **chooses** to ship a full merge (**`build.py`**), not a requirement for every leaf skill’s daily workflow.

---

## Roles

| Artifact | Role |
| -------- | ---- |
| **`SKILL.md`** | **Discovery + procedure** — description, when to use, and **enough instruction to run the skill** in one file **until** it gets long. Cursor and agents load this first. **Default:** put the full runnable guidance here; **only** move overflow to **`references/`** / **`docs/`** when **`SKILL.md`** would be hard to scan (see **[skill-structure-and-concepts.md](parts/library/base/skill-structure-and-concepts.md)** → *SKILL.md — default one file*). The **phase pipeline** (tables, long steps) still lives in **`content/parts/phases/`** — that is not “overflow”; it is the normative process tree. |
| **`AGENTS.md`** | **Orchestration / IDE context** — produced by a **batch merge** (**`scripts/base/build.py`** in skill packages; an agent’s own **`scripts/build.py`** in agent repos). **Skills:** merge is **optional** for day-to-day work (**`generate.py`** per phase is enough); run **`build.py`** when you **ship** refreshed **`AGENTS.md`** or **`static_built`** slices. **Agents:** merged from a **flat `content/*.md`** list (e.g. purpose, outline, workspace, role, checklist, process) via **`skill-config.json` → `agents_md.sections`** — no **`content/parts/library`** tree. |
| **`skill-config.json`** | **Manifest** — **Skills:** `workspace`, `library_files`, `phase_files`, `build` / scanners, `phase_rules`. **Agents:** e.g. `agents_md.sections` + `build.output`; keep orchestration config separate from leaf-skill **`phase_files`**. |

---

## Orchestrators are agents, not skills

If work **coordinates several phases**, **calls other tools**, or **owns a corpus path** (e.g. convert → chunk → index), package it as an **agent** (folder with **`AGENTS.md`**, **`conf/`**, scripts), not as a **second** “orchestrator” **`SKILL.md`** next to a leaf skill.

- **Skill package** = one **`SKILL.md`** + **`content/parts/`** + rules; **`scripts/base/build.py`** is **for assembling `AGENTS.md`** (and built slices), not something most docs or procedures should treat as mandatory on every edit.
- **Agent package** = workflow-first **`AGENTS.md`** (merge is the main story), optional small **`SKILL.md`** only if you still want Cursor discovery pointing at the same repo (the **workflow** stays in **`AGENTS.md`**).

Downstream **stage `SKILL.md`** files (in an agent repo) should **point authors at **`AGENTS.md`**** and any **`config.md` / `conf/`** story so runtime behavior matches the agent, not a stale skim of **`SKILL.md`** alone.

---

## Workspace: config first

**Skill workspace** (where engagement artifacts go) is **`skill-config.json` → `workspace.active_skill_workspace`** — see **[workspace-config.md](workspace-config.md)**. Paths for plans, checklists, and generated output resolve under that tree, not under the skill install directory.

For **agent** repos that mirror this pattern, **topic / corpus roots** should also be **config-driven** (e.g. **`conf/.secrets`** or **`.env`** with keys like **`CONTENT_MEMORY_ROOT`**), not “remember to export in the shell” as the primary story. Same *idea* as **`active_skill_workspace`**: one file the agent and skills agree on.

---

## Skill-internal phases vs agent phases

**Inside one skill package**, **phases** are rows in that skill’s **`process.md`** and files under **`content/parts/phases/`**, listed in **`skill-config.json` → `phase_files`**. Do not spawn a **separate skill repository** per *internal* phase; that fractures discovery and validation. If a slice is truly independent and reusable, it can be its **own** skill with its **own** **`SKILL.md`** — **product** decision, not the default way to model **steps** inside one capability (those stay inside phase markdown — see **[skill-structure-and-concepts.md §3](skill-structure-and-concepts.md#skill-structure-sec3)**).

**At the agent level**, **stages** and **phases** describe the workflow that **calls** one or more skills; **each phase typically maps to one skill**. That orchestration story is **[process-phases.md](process-phases.md)** — not duplicated in every leaf **`SKILL.md`**.

---

## Validation and the corrections log (skill builder scope)

Quality is **layered** — see **[critical-quality-steps.md](../skills/execute_rules/critical-quality-steps.md)** and **[rules-and-scanners.md](../skills/execute_rules/rules-and-scanners.md)** (bundled with the **execute-rules** skill; copies under **`content/parts/library/base/`** exist for **`build.py`** merge into phase docs):

1. **Rules** — normative prose under **`rules/`** (and library); **`phase_rules`** / **`every_phase_rules`**; rule order table via **`skills/execute_rules/scripts/rule_inventory.py --by-order`**.
2. **Mechanical checks** — **`scripts/base/build.py`** (merge then **`build.build_pipeline`** or merged scanner set), **`skills/execute_rules/scripts/run_scanners.py`**, **`rules/scanners.json`** bindings — see **rules-and-scanners** for merge order.
3. **Corrections log** — during review, log issues **against generated output first** (Loop 1); only then fix **`content/parts/`** (Loop 2).

**Where to put the log:** under **`active_skill_workspace`** (the project / engagement tree), not inside the skill install. Example paths: **`docs/corrections-log.md`** or **`.skill-builder/corrections-log.md`**. The log tracks **skill-output** quality for that engagement.

**If the skill ships no `rules/`** (minimal package): there is no second mechanical pass from rule prose — keep a **corrections log** anyway and let the **agent** decide what failed; still follow Loop 1 → Loop 2 so sources are not edited mid-review.

---

## Summary one-liner

**`SKILL.md`** = front door; **`AGENTS.md`** = how to run the whole thing; **orchestration** = agent layout; **workspace** = config; **validation** = rules + mechanical checks (**`build.py`** / **execute_rules** **`run_scanners.py`**) + corrections log under **`active_skill_workspace`**.
