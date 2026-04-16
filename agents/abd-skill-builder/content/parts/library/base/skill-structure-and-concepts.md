# Skill structure and concepts

This is the **one** place for **what goes where** in a skill repo and **how it connects** to the capability story in **[outline.md](../../../outline.md)**. Everything else in `content/parts/library/` is detail: link out from here.

**Greenfield template:** **`skills/build_skill/scripts/build_skill.py`** copies **[skills/build_skill/templates/skill-scaffold/](../../../../skills/build_skill/templates/skill-scaffold/)** (paths below are relative to **`content/parts/library/`** unless noted).

---

## Repository shape (skill package root)

Typical tree after scaffold. **Purpose** = why it exists; **Template** = starting file under `skills/build_skill/templates/skill-scaffold/` when applicable.

| Path | Purpose | Template / note |
| --- | --- | --- |
| `SKILL.md` | Agent discovery: name, description | [`skills/build_skill/templates/skill-scaffold/SKILL.md`](../../../../skills/build_skill/templates/skill-scaffold/SKILL.md) |
| `AGENTS.md` | Optional merged IDE context (**`build.py`** batch output when the repo ships it) | Generated — do not hand-edit as source of truth; routine work edits **`SKILL.md`**, **`content/parts/`**, **`rules/`** |
| `skill-config.json` | **One manifest:** workspace routing, `phase_files`, library + rules shards, `delivery`, `build` | [`skills/build_skill/templates/skill-scaffold/skill-config.json`](../../../../skills/build_skill/templates/skill-scaffold/skill-config.json) |
| `content/parts/process.md` | **Pipeline:** one table row per **phase** (not per step) | [`skills/build_skill/templates/skill-scaffold/content/parts/process.md`](../../../../skills/build_skill/templates/skill-scaffold/content/parts/process.md) |
| `content/parts/phases/<slug>.md` | Procedure, steps, checklists **for that phase** | [`phase-template.md`](../../../../skills/build_skill/templates/skill-scaffold/content/parts/phases/phase-template.md), [`workspace-and-config.md`](../../../../skills/build_skill/templates/skill-scaffold/content/parts/phases/workspace-and-config.md) |
| `content/parts/phases/built/` | Generated phase bodies for static prompts | [`built/README.md`](../../../../skills/build_skill/templates/skill-scaffold/content/parts/phases/built/README.md) |
| `content/parts/library/base/*.md` | **Frozen** shared norms copied from **abd-skill-builder** (checklist, critical-quality-steps, …) — refresh from upstream, do not fork casually | Copied by **`build_skill.py`** |
| `content/*.md` | **Per-skill** narrative every scaffold creates (`purpose.md`, `outline.md`, `role.md`, `principles.md`) — authors extend these | [`skills/build_skill/templates/skill-scaffold/content/`](../../../../skills/build_skill/templates/skill-scaffold/content/) |
| `content/parts/library/*.md` | Optional **extra** shards (listed in `library_files`) — not in base/required | Skill-specific |
| `content/built/` | Optional built slices when `delivery.mode` is `static_built` | [`content/built/README.md`](../../../../skills/build_skill/templates/skill-scaffold/content/built/README.md) |
| `rules/*.md` | Normative constraints; stems wired in `skill-config.json` | [`rules/rule-template.md`](../../../../skills/build_skill/templates/skill-scaffold/rules/rule-template.md) |
| `rules/scanners.json` | Rule → scanner bindings | [`rules/scanners.json`](../../../../skills/build_skill/templates/skill-scaffold/rules/scanners.json) |
| `scripts/base/` | **`build.py`** (batch **`AGENTS.md`** / **`built/`**), **`set_workspace.py`**, shared modules (`instructions`, `skill`, …). | Copied from **abd-skill-builder** `scripts/base/` — assignment (**skill package** vs **multi-skill agent**): **[`scripts/base/README.md`](../../../../scripts/base/README.md)** |
| `scanners/` | Scanner modules + CLI `*-scanner.py` entrypoints | Template stub under `skills/build_skill/templates/skill-scaffold/scanners/` |
| `docs/` | **Non-runtime:** onboarding, manuals, architecture notes — **not** mergeable instruction bodies | [`docs/README.md`](../../../../skills/build_skill/templates/skill-scaffold/docs/README.md) |
| `docs/capability-registry.md` | **Metadata:** which abd-skill-builder capabilities this skill has adopted (✓ Fully Adopted, ⏹ Not Yet Adopted) | [`skills/build_skill/templates/skill-scaffold/docs/capability-registry.md`](../../../../skills/build_skill/templates/skill-scaffold/docs/capability-registry.md) |
| `test/` | Pytest + fixtures (optional) | [`test/README.md`](../../../../skills/build_skill/templates/skill-scaffold/test/README.md) |

**Stages → phases → steps (inside one skill):** **Stages** group work; **phases** are **rows** in that skill’s `process.md`; **steps** live **inside** each `phases/<slug>.md` only — never as extra process rows. For **agent** workflows that **invoke multiple skills** (outer stages/phases, typically **one skill per phase**), see **[process-phases.md](process-phases.md)**.

**`library/` vs `phases/`:** Library = **what** (shared definitions). Resolution order for a filename is **`library/<file>`** → **`content/<file>`** (next to `content/parts/`) → **`library/required/<file>`** (legacy) → **`library/base/<file>`** (see `scripts/base/instructions.py` → `_resolve_library_md`). Phases = **how** for that step (commands, ordered steps). **`docs/`** = human planning; runnable markdown stays under **`content/parts/`**.

**`docs/` vs mergeable markdown:** If **`docs/`** holds instruction bodies that should merge into **`build.py`** output, **move** them into **`content/parts/`** (`library/`, `phases/`) and keep **`docs/`** as index or narrative only.

---

## `skill-config.json` (two roles)

### Workspace (`workspace` in JSON)

| Key | Use |
| --- | --- |
| `active_skill_workspace` | Project tree the skill reads/writes (or `"."`). Set with `python scripts/base/set_workspace.py`. |
| `known_skill_workspaces` | Optional list of other roots. |
| `context_paths` | Extra context dirs for tooling. |

### Pipeline manifest (same file)

| Key | Use |
| --- | --- |
| `name`, `version` | Skill id and semver. |
| `library_files` | Filenames under `library/` merged into **every** phase section when **`build.py`** assembles output. |
| `phase_files` | Ordered phase slugs; each → `content/parts/phases/<slug>.md` (first is usually `workspace-and-config`). |
| `phase_library` | Optional: extra library shards per phase. |
| `every_phase_rules` / `phase_rules` | Rule stems from `rules/` per phase. |
| `phase_bundle` | Order of sections when **`build.py`** assembles merge output (`role`, `principles`, `phase`, `library`, `rules`). |
| `delivery.mode` | `static_built` vs `runtime_injection` — see [base/delivery-modes.md](base/delivery-modes.md). |
| `build` | `compileall_paths`, `build_script`, `build_pipeline`, `scanners`. |

Optional keys `agents_front`, `operation_sections`: see comments in scaffold `skill-config.json` and `scripts/base/build.py`.

---

## content/parts/process.md — minimal format

`process.md` defines the **phase pipeline** for the skill — what phases exist, what order they run, what each phase does, who runs it, and what scripts drive it.

The filled scaffold copy lives at [`skills/build_skill/templates/skill-scaffold/content/parts/process.md`](../../../../skills/build_skill/templates/skill-scaffold/content/parts/process.md).

### Minimal vs rich format

| Format | When to use |
| --- | --- |
| **Minimal** (single table) | Simple skills with 2–3 phases. One table covers all phases. |
| **Rich** (multi-stage) | Skills with distinct planning, build, and validation stages. See [Rich process table (team process plate)](#rich-process-table-team-plate) below. |

### Required sections (both formats)

#### H1 title

One clear title for the skill’s process doc.

#### Pipeline table(s)

One **row per phase** — not one row per step. Columns follow the **[rich process table](#rich-process-table-team-plate)** below (e.g. **#**, **Phase**, **Description**, **Actor**, **Input**, **Output**, **Scripts**). Include a **workspace / Phase 0** row when applicable.

---

## Rich process table (team process plate)

Use this when **`content/parts/process.md`** spans **multiple stages** (plan → build → validate) with separate tables or sections per stage. Norms:

- **Seven-column** tables (abd-skill-builder shape) — use this header set unless a sibling repo documents an alternate shape (e.g. abd-maps-models-specs):

| Column | Use |
| --- | --- |
| **`#`** | Order id: **`0`** = workspace first; **`1a`/`1b`**, **`2a`/`2b`**, … as needed. |
| **Phase** | Link text → **`phases/<slug>.md`**. Stable title, not `phase-02-foo` in the link. |
| **Description** | What this phase **does** — enough to pick the right doc. |
| **Actor** | Human / AI / Code / mixed. |
| **Input** | What you need **before** starting (paths, prior artifacts). |
| **Output** | Concrete **artifacts** when done (paths, tree, exit criteria). |
| **Scripts** | Commands authors run — e.g. **`python scripts/base/set_workspace.py`**, skill scripts under **`scripts/<skill>/`**, and **`python scripts/base/build.py`** when refreshing merged **`AGENTS.md`** / **`built/`** (release, CI). Separate **`·`** between commands. |

- **Stages** are narrative grouping; **phases** remain **rows** linked to **`content/parts/phases/<slug>.md`**.
- Routine work centers **`SKILL.md`** and **`content/parts/`**; **`build.py`** refreshes merged **`AGENTS.md`** / static slices when the package ships them — see **[agent-skill-model.md](base/agent-skill-model.md)**.

**Alternate shape (e.g. abd-maps-models-specs):** same idea (**one row per phase**) but headers like **`Summary`** + **`Script`** + **`Outputs`** + **`Ref`** — keep header labels consistent within a skill.

**Do not** write vague **Output** cells that only name a template — give the **real path** under the skill (e.g. **`content/parts/library/base/checklist.md`**).

### Adding or renaming a phase (skill package)

1. Add **`content/parts/phases/<slug>.md`**.
2. Add a **row** in **`process.md`** (and a **Stage** section if it starts a new stage).
3. Append **`slug`** to **`skill-config.json` → `phase_files`** in order.
4. If the skill uses **`library_files`** / **`phase_library`**, add shards as needed.
5. Wire **`phase_rules`** when new rules apply to that slug.
6. If the repo **commits** **`AGENTS.md`** or **`static_built`** outputs, run **`python scripts/base/build.py`** and fix links.

---

## Authoring checklist — injector body

The canonical file **[checklist.md](base/checklist.md)** in **abd-skill-builder** explains **how checklist files are created**: the stable **`library/base/`** reference, workspace **`progress/`** files, and **`workspace_checklists.py`**. It does **not** duplicate the full process story — skill-internal process tables and phases stay in **this file** (§3, [rich process table](#rich-process-table-team-plate)); **agent** stages/phases across skills stay in **[process-phases.md](process-phases.md)**; activity narrative in **[outline.md](../../../outline.md)** (*Activity checklists*).

**Convention:** **`skills/build_skill/scripts/build_skill.py`** copies **`content/parts/library/base/`** from the builder, including **`checklist.md`**. Refresh **`library/base/checklist.md`** from **abd-skill-builder** when checklist mechanics change.

---

## Skill identity

Phases, rules, and **`SKILL.md`** describe **this skill’s** behavior on its own terms — not chronic “vs another skill” or migration-only narrative. **Dependencies** (other repos, tools, versions) belong in **`README`**, **`skill-config.json`** → **`build_strategy`**, or an explicit **Dependencies** list — not mixed into the main story.

### SKILL.md — default one file; split only when long

**Default:** Keep agent-facing instructions in **`SKILL.md`** (YAML front matter + body) so discovery and procedure live in **one** place.

**Split only when long:** Add **`references/`**, extra **`docs/`**, or **`content/parts/library/`** shards **only** when **`SKILL.md`** would be hard to scan (rough guide: more than ~1–2 screens of dense procedure, or repeated appendices). From **`SKILL.md`**, link to those pieces **once** at the end.

**Avoid:** A stub **`SKILL.md`** that only points elsewhere for content that would still fit inline — that wastes the discovery surface.

Deep **phase** bodies always belong under **`content/parts/phases/`**; this rule is about **leaf / agent discovery** text, not replacing the phase pipeline.

---

## Validation and tests

- **`build.compileall_paths`** and **`build.build_script`** (often `python scripts/base/build.py` when the repo **commits** merged output) gate structure **if** you use the batch merge path.
- **`rules/scanners.json`**, optional **`workspace.scanners`**, and **`scanners/*-scanner.py`** (merge order in **rules-and-scanners.md**) align local checks with CI when wired.
- **`test/`** holds pytest suites and fixtures; layout norms match the **Repository shape** table above. See **`test/README.md`** in the scaffold and **[rules-and-scanners.md](rules-and-scanners.md)**.

---

<a id="skill-structure-sec3"></a>

## Skill package layout and content standards (§3)

**What this is:** Normative rules for how a **skill repository** is shaped — where **runtime** content lives (`content/parts/`, `rules/`), how **stages / phases / steps** relate **inside that skill**, how **process tables** and **Refs** work, optional patterns (e.g. domain + story map), **rule file naming**, and **static vs dynamic** assembly of instructions. Optional **`build.py`** batch merge produces **`AGENTS.md`** / **`built/`** when you ship full IDE context. **Agent orchestration** (outer stages and phases, typically **one skill per phase**) is **[process-phases.md](process-phases.md)** — read that when modeling multi-skill workflows; use **§3 below** for single-skill layout.

**How to use it:** Implement **§3.1–§3.4** when authoring or reviewing a skill. Tools and humans use the same rules; nothing here depends on any external “origin” document.

**Scope boundary — skills stay simple:** A **skill package** should express a **linear** pipeline: **stage → phase → (steps inside phase docs)**. The **process table** rows are **phases**, not steps. Keep skills deliberately sequential.

### 3.1 Directory and content conventions

**Hierarchy in the repo:** **Stages** group **phases**. Each **phase** has normative markdown (one file or section per phase, per skill); **steps** live **inside** that phase’s markdown — they are **not** separate rows in the master process table. See **Stages, phases, and steps** below.


| Area                            | Convention                                                                                                        | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Normative content**           | Under /`content/parts/`                                                                                           | Plans, operations, domain narrative — **not** dumped only in chat.                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `**docs/` (non-runtime)**       | /`docs/` at skill root                                                                                            | **User manuals**, **migration/planning notes**, **architecture**, **authoring checklists**, and **narrative** descriptions of delivery. **Do not** put markdown here that `build.py` **merges**, **injects**, or **ships** as the runnable phase/operation body — that belongs under `**content/parts/`** (including `**library/`**, `**phases/`**, `**process.md**`, `**rules/**`).                                                                                                                                   |
| **Phase markdown (source)**     | e.g. /`content/parts/phases/<descriptive-slug>.md`, or one doc per phase with step sections — paths vary by skill | **One row in the process table = one phase.** **Steps** (numbered sub-procedures, “Step 1…”, checklists) are written **inside** this markdown as **normative content of the phase**, not as their own table rows. **Do not** encode execution order in filenames or H1 titles (`phase-02-foo.md`, `# Phase 2 — …`): order belongs in `**process.md`** (the `#` column) and in `**scripts/base/build.py`**’s explicit file list. Use **stable descriptive** kebab-case slugs so renumbering the plan does not force renames. |
| **Built phase markdown**        | `content/parts/phases/built/<descriptive-slug>.md` and/or `content/built/…` per skill layout | **Generated** from source phase bodies + rules via `scripts/base/build.py`. **Authors do not hand-edit `built/`.** These files are **materialized instruction blobs** for **static** AI-chat phases and for **`static_built`** delivery — consumed by **`generate_prompt`** (or pasted into chat), **not** by “agents browsing the repo” as the primary UX. IDEs load **`AGENTS.md`** when the package ships it; see **[agent-skill-model.md](base/agent-skill-model.md)**. Folder layout (`phases/built` vs `content/built`) is per skill; document it in **`README.md`**.                                                                                                                                                                                                            |
| **Atomic rules**                | `content/parts/rules/*.md` (or top-level `rules/` in simpler skills)                                              | One concern per file where possible; **names** should encode **phase** and/or **domain concept** + rule name (see §3.2). **Which phase inlines which rule** is declared in **`skill-config.json`** (`phase_rules`, `every_phase_rules`), not scattered in per-rule frontmatter lists.                                                                                                                                                                                                                                                                                                                                                                                               |
| **Roles**                       | `roles/*-role.md`                                                                                                 | One file per **user/agent role** the skill assumes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Process**                     | `content/parts/process.md` or staged process docs                                                                 | **Summary table: each row is a phase** (linked by **Ref** to phase markdown). Stages group those rows. **Steps** appear only **inside** the linked phase files.                                                                                                                                                                                                                                                                                                                                                        |
| **Library markdown**            | `content/parts/library/*.md` (or `parts/library/`)                                                                | **Cross-phase structure and meaning**: definitions, glossaries, artifact shapes, naming, invariants. **Not** phase-local procedures, pipeline ordering, or CLI runbooks—those live in **`process.md`** / **`phases/`** (see **Library vs phase documents** below).                                                                                                                                                                                                                                                     |
| **Repo-facing built artifacts** | `AGENTS.md`, `SKILL.md`, sometimes `README.md`                                                                    | **`AGENTS.md`** — when present, produced by **`scripts/base/build.py`** (merge order per skill). **`SKILL.md`** + **`content/parts/`** are primary for authors; **`AGENTS.md`** is **packaged** IDE context when you ship it.                                                                                                                                                                                                                                                                                                                                                                |
| **Config**                      | `skill-config.json`                                                                                               | Name, version, **`phase_files`**, **`PHASE_LIBRARY_SLICES`**, **`phase_rules`** / **`every_phase_rules`** (ordered rule **stems** in merge wiring), **`phase_bundle`**, **`build.compileall_paths`**, **`build.build_pipeline`** (post-merge steps for **`build.py`**; if empty, merged scanners run), **`workspace.scanners`** — skill-specific knobs. Host CI may mirror these under **`operator.*`**. See **[`rules-and-scanners.md`](rules-and-scanners.md)**. |
| **Scripts**                     | `scripts/`                                                                                                        | Operational entry points; may share `_config.py` patterns.                                                                                                                                                                                                                                                                                                                                                                                                                                                             |


#### Stages, phases, and steps (how they relate)

**Order is always:** **Stage → Phase → Step** (coarse → mid → finest) — but **only the first two appear as rows** in the master process table. **Steps** are **inside** the phase markdown.


| Term      | Typical meaning                                                                                                                                                                                                                                                                                                                      | Example                                                                                  |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **Stage** | **Coarse pipeline slice** — groups many **phases**; may span days or sessions. Often a heading or section in `process.md` or a staged doc.                                                                                                                                                                                           | **Stage 1 — Extract Context**; **Stage 2 — Map and Model**; **Stage 3 — Specification**. |
| **Phase** | **One row** in the process summary table — the unit of “what we do next” with a **driver**: **human** or **AI actor**. The **Ref** column links to **phase** markdown. Phases answer “are we allowed to proceed?” and **contain** the detailed steps as normative body copy.                                                         | “Corpus audit — Phase N”; **Initiator / Actor** column = human vs AI.                    |
| **Step**  | **Sub-structure inside the phase’s markdown** — numbered instructions, checklists, “Step 1 / Step 2”, optional **suffix letters** (`5a`, `7a`) for companion script runs **within the same phase**. **Not** a row in the process table. Machine state (if any) may still reference `workflow_step` as a **sub-id** inside the phase. | Inside `modules-epics-scaffold-breadth.md`: “1. … 2. … 3a. rebuild index …”              |


**AI-driven phases — how the operation is delivered (inside this skill):** **code-driven** phases = run scripts as documented in the phase file; **AI-chat** phases = follow the phase markdown (and **`SKILL.md`**) with the skill attached — optional **static** bodies under `phases/built/` are produced by **`build.py`**, not a separate per-session bundler CLI. **Agent-level** phase sequencing across skills is **[process-phases.md](process-phases.md)**.

**Ordering (linear, inside the skill):** Stages order **major outcomes**. **Phases** run in **process table order** (each row = one phase). **Steps** follow the order **written inside** each phase document. **Parallel batches, fan-out, or merge** are **not** modeled as extra table rows; if needed, handle that **outside** the skill package (host app, orchestration, or scripts). **Phases** may **block** a later stage until accepted (e.g. “the indexer phase says rebuild chunks — do not start Stage 2 until accepted”).

**“Process” one-liner:** `content/parts/process.md` (or `parts/process.md`) often opens with a **single pipeline string** (e.g. Context → Foundational spine → …). That line is the **navigation spine**; the **table lists phases** (by stage); **authoritative step detail** lives inside each **Ref**’d phase file.

#### Process tables, hyperlinks, and naming in the Ref column

**How the table is built**

- **Rows are phases**, not steps. Columns typically include: `#`, **Phase** (title — sometimes labeled “Step” in legacy tables; **semantically it is the phase**), **Initiator / Actor** (Human→Code, AI, Code), **Script** (if any), **What it does**, **Coverage**, **Ref**, **Inputs**, **Outputs**.
- **Ref** is the **hyperlink hub**: each row points to the **normative markdown for that phase**. **Steps** (numbered sub-procedures) live **inside** that file — not in separate table rows. Python entry points stay in **Script**, not **Ref**.
- **Two-tier phase files:**
  - **Source:** phase markdown authors edit (e.g. `content/parts/phases/<name>.md`, or `parts/steps/<name>.md` when the filename is the **phase** slug — naming varies by skill).
  - **Built:** `content/parts/phases/built/<name>.md` or `content/built/<name>.md` — **rules baked in** from `parts/rules/*.md` via `scripts/base/build.py`. **Steps remain inside** the built document. Used for **static** prompt generation and **`static_built`** slices — not hand-edited. See **[agent-skill-model.md](base/agent-skill-model.md)** and **`scripts/base/build.py`**.
- **Cross-links inside the table:** The **Ref** column uses relative markdown links to the **phase** doc, e.g. `[context](parts/context.md)`, `[modules-epics-scaffold-breadth (built)](content/parts/steps/built/modules-epics-scaffold-breadth.md)` (paths vary by skill; **from the skill root** per `AGENTS.md`).

**Naming conventions visible in the table**

- **Phase titles** in the table read like **milestones or operations** (“Parse, curate, chunk, index”, “Integrate and Harmonize”) — stable labels for **phase** / workflow fields. **Finer labels** for **steps inside the phase file** may appear in JSON as `workflow_step` or similar.
- **Phase file names and H1 headings** must **not** duplicate pipeline indices (`phase-00-`, `Phase 3 —` in the title). Those numbers **change** when the plan evolves; **brittle** names churn git history and links. The **Ref** column and `build.py` define order; phase files stay **semantically** named (`story-map.md`, `canonical-context.md`).
- **Letter suffixes** (`5a`, `7a`) describe **sub-steps inside a phase** (e.g. companion script after a numbered step) — **inside the phase markdown**, not extra table rows.

#### Concepts and cross-cutting artifacts (generic — all skills)

**This section is the generic rule.** A **skill** packages **concepts** (ideas, definitions, invariants, roles) and **artifacts** (outputs, schemas, manifests) that the workflow references across **multiple stages or phases**. Anything that would be **repeated** if pasted into every phase file should instead live in **its own file** (usually markdown under `content/parts/`, sometimes JSON alongside) so there is a **single source of truth**.


| Guideline           | Meaning                                                                                                                                                                                                         |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **When to extract** | If a concept or artifact **spans** more than one phase (or stage), give it a **dedicated** doc (or structured file) and **link** from phase bodies — do not duplicate long definitions in each phase.           |
| **Naming**          | Conventional filenames (`glossary.md`, `concepts.md`, `artifacts.md`, `roles/`*, etc.) vary by skill; **discover** and **validate** presence from templates and this skill’s `build.py`, not one global layout. |
| **Not every skill** | A minimal skill might only have `SKILL.md`, `content/parts/process.md`, and phase files — **no** separate “domain” or “story map” layer. That is valid.                                                         |


#### Library vs phase documents (authoring split)

**`library/`** answers **what** (stable meaning for ideas and artifacts that **more than one** phase touches). **`phases/<slug>.md`** answers **how for this step** (operator procedure: inputs, outputs, ordered steps, **commands**, done checks).

| In **`library/`** | In **`phases/`** (not a second copy of the whole library) |
| --- | --- |
| Definitions, tables, schemas, vocabulary used across phases | Purpose of **this** phase, **steps**, checklists, **script/CLI** lines |
| Single source of truth for a construct that spans the pipeline | **Links** into the right **`library/`** shard for depth |
| Optional injection slices (`abd:begin` / `abd:end`) | **No** long normative essays that other phases would repeat verbatim |

**Do not** put **numbered phase procedures**, **order-of-operations** for the skill, or **phase-to-phase sequencing narrative** in **`library/`**—that belongs in **`process.md`** and the relevant **`phases/`** files. **Do not** park **large** reusable specs only inside one phase file if another phase needs the same text—extract to **`library/`** and link.

Normative detail for writers: [`documentation-standards.md`](documentation-standards.md) and [`Skill structure and concepts.md`](skill-structure-and-concepts.md#skill-structure-sec3) (§3).

#### Optional pattern — domain narrative + interaction tree (maps-models–class skills only)

Some skills (notably **abd-maps-models-specs** and similar) **choose** to separate **two parallel artifacts** that must stay in sync. **Do not** treat this table as the default for **all** skills — only for skills that explicitly adopt this shape.


| Piece                            | Role                                                                                                                                                                                                    | Typical location (example skill)                                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Domain narrative**             | **State and structure** — modules, **domain concepts** (CRC-style: owns, properties, operations, `extends`, invariants), evidence hooks. Answers **what things are** and **what owns which rules**.     | e.g. `parts/domain.md` + evolving `map-model-spec.json` (`modules_and_epics`, `concepts[]`, chunk citations). |
| **Story map / interaction tree** | **Behavior** — epics, sub-epics, stories, scenarios; **Trigger / Response**; **Pre-Condition**; **Given/When/Then** where required. Answers **who does what** and how behavior references domain state. | e.g. `parts/story-map.md` + nested JSON under epics (`stories`, `sub_epics`, etc.).                           |


**When this pattern applies**

- **Same vocabulary:** Domain concept names (`concepts[].name`) and story references can be held to **one namespace** — scanners may enforce **exact string match** where the skill defines that rule.
- **Evidence ladder / paired edits:** Concepts may carry `evidence_stage`; **domain** vs **journey** edits are **paired** in skills that implement both files.
- Skills **without** this split still use the **generic** rule above: cross-cutting concepts → **their own** markdown (whatever the skill calls them), not repeated per phase.

#### Rules and automated checks (default wiring)

For **machine-enforceable** rules, use **[`rules-and-scanners.md`](rules-and-scanners.md)**:

- **`rules/*.md`**, **`phase_rules`**, **`every_phase_rules`**; authoring order table: **`skills/execute_rules/scripts/rule_inventory.py --by-order`** (from **abd-skill-builder** root).
- **`rules/scanners.json`** (`rule_scanner_bindings`, optional **`scanners`** list).
- **`build.build_pipeline`**, discovered **`scanners/*-scanner.py`** — merge order and **`run_scanners.py`** (**execute_rules**) are documented in **`rules-and-scanners.md`**.

**Process tables** should **not** enumerate every scanner as phase rows; link **`rules/scanners.json`** and **`build.py`** at skill level.

### 3.2 Rule file naming (heuristic standard)

Target pattern (flexible regex for validation):

```text
{phase-or-stage}__{domain-concept-or-scope}__{short-rule-name}.md
```

Examples mirror **story synchronizer / maps-models** style: scanners and rules tied to **phase** and **concept** (e.g. `chunks_must_be_referenced`, `concept-layering-scaffold`). **Propose** names from the **phase** + concept + verb (and step text inside the phase doc if needed), then **check uniqueness** under `parts/rules/`.

<a id="assembly-model"></a>

### 3.3 Assembly model (static vs dynamic)

**Two different “static vs dynamic” pairs** — do not conflate:

1. **`build.py` assembly** (repo artifacts): Each skill ships `scripts/base/build.py`. It merges **process + library + phases (+ rules)** into **`AGENTS.md`** and optional **`content/built/`**. Flags like `--assembly static|snapshot` are **per skill** when present.

2. **AI-chat instruction shape:** For **AI-driven** phases, authors maintain **`content/parts/phases/<slug>.md`** (and **`SKILL.md`**). **`build.py`** can materialize **static** bodies under `phases/built/` when configured; there is **no** separate “phase bundle for chat” CLI in the author workflow.

**Per skill:** `build.py` is the **authoritative** merge driver for **this** repo; scaffolding **emit or check** trees — they do **not** replace `build.py`.

**Flag on `build.py`:** The skill’s `build.py` may expose **CLI flags** for snapshot vs interactive merge; exact names are per skill. Document merge and delivery behavior next to **`build.py`** in **`README`** / **`AGENTS.md`**.


| Mode (merge / delivery) | Mechanism                                                                               | When                                                               |
| ----------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Static (merge)**      | `build.py` merges **built-phase** fragments into `AGENTS.md` / `SKILL.md` (and related) | Release, reproducible snapshot; CI; “what ships”.                  |
| **Dynamic (merge)**     | Runtime concatenation by **phase** / **operation** from `skill-config.json` + manifest  | Interactive sessions, partial rebuild, IDE-driven iteration. |


A **host** (CI, IDE, or orchestrator) may emit an **internal** manifest (JSON or YAML) for a **given generation run**, listing which fragments form which artifact for both modes; the skill’s `build.py` **may read** that manifest (or embedded config) when implementing **static** merges and documents how **dynamic** mode resolves fragments at runtime. That manifest is **optional** and **not** a standard every skill must carry — only **documented** `build.py` behavior is.

### 3.4 Reference skills (illustrative)

Other skills in the monorepo **illustrate** patterns (long `AGENTS.md`, phased pipelines, rules + scanners). They are **examples**, not extra requirements. **Operator** checks and layout rules are grounded in **abd-skill-builder** library files and each skill’s **`skill-config.json`** — not in a separate “corpus” file unless your team adds one.
