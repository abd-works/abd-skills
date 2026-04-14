# Builder architecture — agent, skills, capabilities (source of truth)

This document is the **intended shape** for **abd-skill-builder**: what the **agent** is, which **operations** it exposes, where **agents** vs **standalone skills** live, and how **capabilities** are packaged. Implementation in this repo should **converge** here over time; older phase names and paths remain until migrated.

---

## 1. The agent is abd-skill-builder

**abd-skill-builder** is the **agent**: it orchestrates creating and extending other agents and skills. It is not only a bag of library markdown—it **scaffolds trees**, **merges** `AGENTS.md`, and **adds capabilities** using shared **capability packs** under **`skills/capabilities/`** in this repo.

---

## 2. Three primary operations (builder “skills”)

These are the user-facing operations (CLI, `SKILL.md` triggers, or phased workflow—**one surface** should win; today some of this maps to `process.md` phases).

### 2.1 `build_agent`

Scaffolds an **agent** repository with at least:

| Area | Contents |
| --- | --- |
| **`content/`** | `outline.md`, `principles.md`, `purpose.md`, `role.md` |
| **`scripts/`** | `build.py` — merges agent context into **`AGENTS.md`** (flat section list / manifest, per agent convention) |
| **`skills/`** | Includes a **workspace** skill: markdown + scripts to **set** and **get** the workspace so all skill output goes to the correct tree |
| **`AGENTS.md`** | Assembled from context; not hand-maintained as the only source of truth |

**Interaction contract:** Prefer **context** (repo, chat, existing files). **Verify** assumptions with the user. If **phase**, **process**, **purpose**, or **principles** cannot be inferred, **ask** before writing.

---

### 2.2 `scaffold_skill`

Creates a **skill** either **under an agent** or **standalone**.

| Target | Layout |
| --- | --- |
| **Agent + skills** | `<agent>/skills/<skill_name>/` — after walking **agent** steps and deciding what is a separate skill |
| **Standalone** | `<root>/skills/<skill_name>/` |

**Modes (conceptual):**

- **Build agent with skills** — run agent scaffolding first; place skills under the agent’s `skills/` folder.
- **Build skill only** — emit under `<root>/skills/` (or a path the user supplies).

**Skill tree (each `<skill_name>`):**

```text
<skill_name>/
  SKILL.md
  content/
  scripts/
  rules/
  templates/
```

**Interaction contract:** Derive **rules**, **inputs**, **outputs**, **purpose**, and **steps** from context; **verify** with the user or **ask** when missing.

---

### 2.3 `add_capability`

Adds a **named capability** to a **target agent** or **target skill** (`<param>` selects the capability **kind**).

| Capability kind | What it does |
| --- | --- |
| **Activity checklists** | When the target **agent** or **skill** runs, **checklists** track progress through steps (pipeline + per-phase where applicable). |
| **Rules or scanner** | **Rules** ship **inside** the target skill (or agent rules area); merged in **build**; **not** modeled as a separate installable skill. Scanners bind to those rules. |
| **Corrections** | When the user fixes bad output, **log** what changed, keep **final** result, and support **improvement** feedback over time (corrections log under workspace). |
| **Templates** | Outputs are **rendered through templates**; render logic **looks in** the skill’s `templates/` (or agent template root) **before** falling back to defaults. |

All of these **exist in the current codebase** in some form; the move is to implement them through **`add_capability`** + **`skills/capabilities/<Capability>/`** instead of one-off copies.

---

## 3. Capability packs (`skills/capabilities/` in abd-skill-builder)

Each capability that can be **added** to a target is defined as a **pack** in this repo:

```text
skills/capabilities/
  <CapabilityName>/
    agent/
      PART.md              # Boilerplate merged into target AGENTS.md (section contract TBD: prepend / append / named section)
      *.py                 # Optional: copied into target agent’s script area (e.g. scripts/)
    SKILL/
      SKILL.md             # What gets merged or copied for target agent’s skills/<capability>/SKILL.md (when capability is skill-scoped)
      scripts/
        *.py               # Copied to target skills/<capability>/scripts/ (or the skill’s scripts/ layout)
```

**Rules of thumb:**

- **Agent-only** capabilities: use `agent/PART.md` (+ agent scripts).
- **Skill-only** capabilities: use `SKILL/SKILL.md` + `SKILL/scripts/`.
- **Both**: provide both trees; `add_capability` picks by target type.

Exact **merge rules** and **filenames** per capability are defined beside each pack (see `skills/capabilities/README.md`).

---

## 4. Mapping from today’s repo

| Today | Direction |
| --- | --- |
| `content/parts/process.md` + phases | Still valid for **this** repo’s authoring; user-facing operations should **read** as **build_agent** / **scaffold_skill** / **add_capability** |
| `skills/build_skill/templates/skill-scaffold/` | Feeds **scaffold_skill** (owned by **build_skill** leaf) |
| `skills/build_agent/templates/` | **build_agent** copies **`build.py`**, **`workspace_skill/`** into new orchestrators |
| `content/parts/library/base/checklist.md`, rules, corrections, templates docs | **Sources of truth** for behavior; **packs** under `skills/capabilities/` should **reference** or **embed** those patterns |
| `scripts/scaffold_skill.py` | Evolves into or wraps **scaffold_skill** + **build_agent** flags |

---

## 5. Alignment (“vote”) — open decisions

Record decisions here or in PR discussion; update this file when settled.

- [ ] Single CLI entry vs three commands vs phase-only UX
- [ ] Default path for **workspace** skill name under `skills/`
- [ ] `PART.md` merge semantics into `AGENTS.md` (stable section anchors)
- [ ] Whether **capabilities** are versioned with the builder semver or independently

---

## See also

- **[outline.md](outline.md)** — capability-oriented outline (being aligned with this doc)
- **[skills/capabilities/README.md](../skills/capabilities/README.md)** — pack directory index
- **[parts/library/base/agent-skill-model.md](parts/library/base/agent-skill-model.md)** — agent vs leaf skill roles
- **[parts/library/base/process-phases.md](parts/library/base/process-phases.md)** — agent stages / one skill per phase (orchestration vocabulary)
