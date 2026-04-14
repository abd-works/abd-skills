# `scripts/base/` — skill package tooling (assignment)

Everything here is designed for a **skill package** layout: repo root holds `skill-config.json`, `content/parts/`, `rules/`, and this `scripts/base/` tree (`skill_root.py` assumes **`…/scripts/base/<script>.py`** → root is **two levels up**).

It is **not** the thin **multi-skill agent** merge used by orchestrators such as **`agents/abd-context-to-memory`** (those use a **separate** `scripts/build.py` at the **agent** root that only concatenates **`content/*.md`** slices into **`AGENTS.md`**).

**This repo** (`agents/abd-skill-builder`) is a **skill package** that also happens to live under `agents/`; the scripts below apply to **it** and to any skill emitted by **`build_skill`**.

**Rules, bundled `SKILL.md` updates, scanner listing, and running scanners** for any target skill are **not** here — they live under **`skills/execute_rules/scripts/`** in this repo. See **`content/parts/library/base/rules-and-scanners.md`**.

---

## Vocabulary

| Term | Meaning here |
| --- | --- |
| **Skill package** | Single Open Agent Skill: `SKILL.md`, `skill-config.json`, `content/parts/`, `scripts/base/*`, optional `skills/` only if you split leaf skills later. |
| **Multi-skill agent** | Orchestrator folder: root **`AGENTS.md`** from **`content/*.md`** via agent-level **`scripts/build.py`**; stage work delegated to **`skills/<name>/SKILL.md`**. Does **not** use this merge stack unless you copy a full skill package inside it. |
| **Library module** | Imported only; not the primary CLI entry for authors. |

---

## Assignment table

| File | Assignment | Role |
| --- | --- | --- |
| **`skill_root.py`** | Skill package · library | Resolves **`SKILL_ROOT`** (two parents up from `base/`). |
| **`config.py`** | Skill package · library | Loads normalised **`skill-config.json`** fragments for tooling. |
| **`skill.py`** | Skill package · library | Build-time skill model / merge context (`_BuildTimeContext`, etc.). |
| **`instructions.py`** | Skill package · library | Assembles merge slices: library shards, phase body, rules, markers (used by **`build.py`**). |
| **`rules.py`** | Skill package · library | Rule file resolution for bundles. |
| **`markers.py`** | Skill package · library | Section markers for merged markdown. |
| **`workspace_checklists.py`** | Skill package · library | Ensures **`progress/`** pipeline checklists under **`active_skill_workspace`**. |
| **`build.py`** | Skill package · **CLI** | Batch merge **`content/parts/`** → root **`AGENTS.md`** (+ optional **`content/built/`**, **`phases/built/`**); runs post-merge pipeline / scanners (scanner path logic inlined — same behavior as **`skills/execute_rules/scripts/scanner_paths.py`**). |
| **`set_workspace.py`** | Skill package · **CLI** | Read/write **`workspace.active_skill_workspace`** in **`skill-config.json`**. |

---

## What multi-skill agents use instead

For **orchestrator-only** repos (no `content/parts/` merge stack):

- Put **`agents/<agent>/content/*.md`** narrative slices there.
- Use **`agents/<agent>/scripts/build.py`** + **`skill-config.json` → `agents_md.sections`** (see **`agents/abd-context-to-memory`**) to build **`AGENTS.md`**.
- Per-stage procedures stay in **`agents/<agent>/skills/<skill>/SKILL.md`**.

Do **not** copy **`scripts/base/build.py`** from here expecting it to work without **`content/parts/`** and the full **`skill-config.json`** pipeline — unless that agent folder **is** (or embeds) a complete skill package.

---

## See also

- **`content/parts/library/base/rules-and-scanners.md`** — **`execute_rules`** CLIs vs **`scripts/base/`**.
- **`content/parts/library/base/skill-structure-and-concepts.md`** — repo map and **`scripts/base/`** role in scaffolds.
- **`content/parts/library/base/agent-skill-model.md`** — **`SKILL.md`** vs **`AGENTS.md`**, agents vs leaf skills.
- **`content/builder-architecture.md`** — planned **`build_agent`** / **`scaffold_skill`** / **`add_capability`** (high level).
