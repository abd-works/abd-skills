# Phase — Fill scaffold (library and rules)

In [`../process.md`](../process.md), **[Fill scaffold parts](fill-scaffold-parts.md)** appears as **phase #4, #5, and #6** — all inside **Stage 2** (one stage: phase **#2** scaffold through **#6** scripts). Focus **#4** rules & scanners, **#5** library, **#6** scripts. It runs **after** **phase #2** ([**scaffold**](scaffold.md)) and **phase #3** (process & phase files), or **after** **[migrate](migrate.md)** (execute a **plan-migrate** / **1b** plan) when you did not use greenfield scaffold. The scaffold **creates directories and templates**; this phase **fills them** with the **instructional content** the skill actually runs on: **`content/parts/library/**`**, **`rules/**`**, and—where needed—**richer `content/parts/process.md`** and **`phases/*.md`**.

**Not in scope:** running **`scaffold_skill.py`** again, or replacing **`scripts/base/build.py`**. **In scope:** collaborative **authoring** (human + AI) so **library** chunks and **rules** match **SKILL.md** purpose, **`content/parts/process.md`**, and the **process** you sketched.

Emit this file for an AI session with:

```bash
python scripts/base/generate.py --phase fill-scaffold-parts
```

(Or `python scripts/generate_prompt.py --phase fill-scaffold-parts`.)

---

## Purpose

Turn a **hollow** or **minimal** skill package into one whose **merged** agent bundle (**`AGENTS.md`**) and **built** slices honestly describe **how** the skill works. The AI **interprets** the skill’s **intent** (purpose, suggested phases, suggested rules, delivery hints) and **proposes concrete files**: definitions in **`library/`**, must-holds in **`rules/`**, and edits to **`process.md` / `phases/*.md`** where the scaffold left placeholders. The **user** confirms domain facts, rejects bad shortcuts, and owns final wording.

This is **not** “have the model freestyle in chat.” It is **structured authoring** against **[skill-structure-and-concepts.md](../library/skill-structure-and-concepts.md)** and **[how checklists are created](../library/base/checklist.md)** (stable **`library/base/`** reference vs workspace **`progress/`**). Each skill has **`content/parts/library/base/checklist.md`** after scaffold (copied with **`library/base/`** from **abd-skill-builder**).

---

## What to read first (in the skill under construction)

| Source | Why |
| --- | --- |
| **`SKILL.md`** | Declared purpose, frontmatter, what the skill *is for*. |
| **`content/parts/library/base/checklist.md`** | How checklists work in this layout (refresh from **abd-skill-builder** `library/base/` when needed). |
| **`content/parts/process.md`** | Staged flow—even if minimal—defines **order** and **phase slugs**. |
| **`skill-config.json`** | **`delivery.mode`**, **`build.*`** (compile paths, pipeline, scanners), workspace keys — see **[Workspace and config](workspace-and-config.md)** (**`active_skill_workspace`**). |
| **Existing `content/parts/phases/*.md`** | Skeleton or empty—**extend**, don’t duplicate the **process** table blindly. |

If **`library/`** or **`rules/`** already has files (e.g. after **migrate**), **revise** before adding parallel ad-hoc docs elsewhere.

---

## What to produce

| Area | Target |
| --- | --- |
| **`content/parts/library/*.md`** | Cross-cutting definitions, tables, glossaries, **delivery** notes—**one home** for concepts reused across phases (see **[skill-structure-and-concepts.md](../library/skill-structure-and-concepts.md)**). |
| **`rules/*.md`** (and **`rules/scanners.json`** if used) | Must-holds the agent and tooling should enforce; align with **`skill-config.json`** scanners when you add them. |
| **`content/parts/process.md` / `phases/*.md`** | Replace placeholders with **steps** that match the **#** column and **`build.py`** merge order (when the skill’s **`build.py`** lists phases explicitly). |

Everything you add must **merge** cleanly: no instruction bodies that belong in **`parts/`** stranded under **`docs/`** ( **`docs/`** is for onboarding / manuals — not mergeable phase bodies).

---

## Prompt contract — how the AI should work (follow in order)

1. **Restate the skill’s purpose** in one short paragraph (from **`SKILL.md`** and **`content/parts/process.md`**). If unclear, **ask** the user before inventing domain rules.

2. **Map process to files:** From **`process.md`**, list **phase slugs** and ensure each has a **`phases/<slug>.md`** (or a documented exception). Flag **gaps** between the **table** and **`phases/`** on disk.

3. **Design `library/`:** Propose **which** library files you need (names mirror **concepts**, not random `misc.md`). Each file should have a **single** role (definitions vs delivery vs checklist pointers). Pull **cross-cutting** text out of phase files into **`library/`** when two or more phases would repeat it. **`library/`** must stay **non-procedural**: definitions and structure only—**not** step-by-step phase execution, **not** CLI runbooks, **not** pipeline order (**[`Skill structure and concepts.md`](../library/skill-structure-and-concepts.md#skill-structure-sec3)** → *Library vs phase*).

4. **Design `rules/`:** Turn “suggested rules” from the plan into **actionable** rule files—**testable** where possible. Connect rules to **scanners** only when the skill **defines** those scanners; otherwise keep rules as **agent** constraints.

5. **Collaborate:** After each batch of proposed paths, **stop** for user confirmation on: domain terms, **must** vs **should**, and **out-of-scope** behavior.

6. **Run the merge check:** After edits, run **`python scripts/base/build.py`** in the **skill under construction** and fix **source** files until **build** succeeds—**never** hand-edit **`AGENTS.md`** if **build** owns it.

---

## Success criteria

- **`library/`** holds **shared meaning** (definitions, shapes, vocabulary) the phases **link** to; **`phases/`** holds **procedures** (steps, scripts, checks)—not duplicated long essays, and **not** the reverse (procedures hiding in **`library/`**).
- **`rules/`** reflects **must-holds** the user agreed to, consistent with **`skill-config.json`** where wired.
- **`process.md`** phase table and **`phases/*.md`** **agree** on slugs and order (and with **`build.py`** if the skill uses an explicit phase list).
- **`python scripts/base/build.py`** exits **0**; **`AGENTS.md`** reflects the new content.

---

## See also

- **[skill-structure-and-concepts.md](../library/skill-structure-and-concepts.md#skill-structure-sec3)** — placement, voice, **library/** vs **phases/** (§3).
- **[Workspace and config](workspace-and-config.md)** — **`skill_path`**, **`skill-config.json`**, **`active_skill_workspace`**.
- **[Scaffold](scaffold.md)** — greenfield tree (**phase #2** in **Stage 2** in **`process.md`**).
- **[Migrate](migrate.md)** — apply **1b** delta (brownfield).
- **[Plan skill migration](plan-migrate.md)** — **1b** (inventory + **standards delta**).
- **[Plan Script Build](plan-script-build.md)** — **Stage 1** (plan before scaffold).
