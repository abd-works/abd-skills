# AGENTS — abd-skill-builder

## Process

# Process — abd-skill-builder

**In order:** Standards & checklist → **Scaffold or migrate** → **Operator** (automated checks)

## Outcome of this process

You finish with a **skill** where the instructions you give the model **match what the skill actually says**, so work does not drift off-script. **Stages and phases** break the work into clear chunks; **steps** sit in phase files; **checklists** help you pick up after a break or a handoff. **Rules** say what must stay true; **scanners** and the other **automated checks** (Python validity on the paths you configured, **build**, scripts listed in config) **catch** when the **files in the repo** no longer match those rules. *Inputs, scripts, templates, and “done” outputs are spelled out in the **phase tables** below—not in a separate inventory.*

## High-level principles

- **Instructions match the skill:** Build prompts and injected text from what the skill already wrote in **library/**, **phases/**, and **rules/**—not off-the-cuff chat.
- **Stages, phases, and checklists:** The process **table** is the map; **steps** live inside phase files. **Checklists** (including the authoring checklist) keep long or stop-and-start work ordered so you can resume.
- **Quality process (rules → scan → assess → fix):** Keep must-holds in **rules/**, and **bring those rules into what the model sees**—prompt or injected sections—so work is **guided**, not guessed. Then **run scans** (small scripts or checklists). Then **check** the result against the rules (by eye or with automation). Then **fix** and **log** corrections so the next pass improves. Before you **commit**, the **Operator** checks still run: **Python files** in the folders listed in `**skill-config.json`** must **compile** (syntax/validity), then `**build.py`**, then **scanners**. *Same idea at full depth (iterate with corrections):* [abd-shaping](../../../../backup/abd-shaping/SKILL.md).
- **Assemble from parts:** You author a skill as **parts**—process, **library/**, phase files, **rules/**—and **build** stitches them into the **whole** the tools load (**AGENTS.md**, and—when you choose **static** delivery—checked-in slices under **content/built/**). **Dynamic** delivery still uses the same parts; the executor **combines them at run time** instead of reading a pre-merged file. Either way the **parts** are the source of truth; the **whole** must not drift. **Scaffold** (**scaffold_skill.py**) vs **migrate** (**phases/migrate.md**) is only how you **create or fix** the folder; phase order stays in this file’s **#** column and **build.py**’s lists—not in filenames. *Details:* [delivery-modes](library/delivery-modes.md).

## Stage 1 — Plan

### Purpose

Load the **standards in `library/`** and the **authoring checklist** so scaffold/migrate work targets the same rules (§3, operator, `**delivery.mode`**, `**test/**` expectations). If the skill resolves paths outside its install folder, set `**conf/abd-config.json**` → `**active_skill_workspace**` (customer or solution tree).

### What you produce

- Confirmed understanding of **§3** directory rules and **process table** semantics.
- A tracked checklist (copy `**library/authoring-checklist.md`** to `**<skill>/docs/authoring-checklist.md`** in the skill you are editing) with `**- [ ]` / `- [x]**` progress.

### How you know you succeeded

You can say where the **authoritative** text lives (**library/** vs **docs/**), and you have a **first unchecked** checklist item to pick up next time if work pauses.


| #   | Phase                                | Description                                                                                                                               | Actor      | Input                                                                                                                                                                                                                                                                            | Output                                                       | Scripts | Ref                                                                                                                               |
| --- | ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Read standards & authoring checklist | You open the index and full §3, then work the checklist (ask / AI-suggest / track). This grounds every later file move in the same norms. | Human / AI | **library/** files: [index](library/skill-repo-standards.md), [§3](library/skill-standards-section-3.md), [checklist](library/authoring-checklist.md); optional copy of checklist under **your skill** **docs/**; **workspace** routing via **conf/abd-config.json** when needed | Updated checklist boxes; clear picture of checks vs delivery | —       | [index](library/skill-repo-standards.md), [§3](library/skill-standards-section-3.md), [checklist](library/authoring-checklist.md) |


---

## Stage 2 — Create or fix the skill

### Purpose

Either **emit** a new compliant **skill** (**greenfield**) or **align** an existing one (**migrate**) without silent wholesale rewrites.

### What you produce

- **Greenfield:** New directory with scaffolded `**SKILL.md`**, `**skill-config.json`**, `**conf/**`, `**content/parts/**`, `**scripts/**`, `**rules/**`, `**test/**`.
- **Migrate:** Delta report (gaps vs standards) and **only** user-approved edits.

### How you know you succeeded

- Greenfield: `**python scripts/build.py`** runs in the new skill; Operator can run against it.
- Migrate: Delta rows are **fixed**, **deferred**, or **accepted risk** with rationale.


| #   | Phase                        | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Actor      | Input                                                                  | Output                                                                                                           | Scripts                                                                                     | Ref                            |
| --- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------ |
| 2a  | Scaffold new skill directory | You choose a **kebab-case** skill id and run the scaffold. It copies from **templates/** at the skill root (`SKILL.md.template`, `process.md.template`, `child_build.py.template`, …), creates **conf/**, **content/parts/**, **scripts/**, **rules/**, **test/**, and copies **authoring-checklist.md** into the new skill **docs/**. You get a minimal **process.md**; replace or enrich it with the **team process plate** (**content/parts/templates/process-team.md.template**; see **content/parts/templates/README.md**) when you need stages, inputs/outputs, and a full phase table. Then run `**python scripts/build.py`** in the new skill so **AGENTS.md** and **content/built/** (if static) match **content/parts/**. Heavier skills may add **scripts/generate_prompt.py** (optional phase prompt helper). | Code       | `**--name`**, `**--out**` (empty or non-existent path); **templates/** | **New skill** tree; **docs/authoring-checklist.md**; built **AGENTS.md** + **content/built/** after **build.py** | `**python scripts/scaffold_skill.py`**; then `**python scripts/build.py**` in the new skill | [scaffold](phases/scaffold.md) |
| 2b  | Migrate existing skill       | You inventory the skill on disk (**SKILL.md**, **skill-config.json**, **scripts/build.py**, **content/parts/**), compare to standards, write a **delta** table (e.g. **docs/standards-delta.md** pattern), and fix **only** what the user selects—no silent full rewrites.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Human / AI | Path to existing skill                                                 | Delta markdown; targeted patches; user-approved edits only                                                       | — (optional helper scripts per skill)                                                       | [migrate](phases/migrate.md)   |


---

## Stage 3 — Structural validation (Operator)

### Purpose

Show the **skill** **passes automated checks**: Python files under the configured folders compile (syntax check), **build** finishes, scanners return success. For a minimal valid layout reference, see **agentic-skill-builder**’s **test/fixture/toy-polite-dialogue/** (not a product deliverable).

### What you produce

- Exit code **0** from `**operator.run_operator()`** (or the same steps by hand: **Python compile check** on configured paths, `**python scripts/build.py`**, then **scanners**).
- **AGENTS.md** and **content/built/AGENTS.md** byte-match when static delivery; both reflect the latest **content/parts/**.

### How you know you succeeded

CI or local check run succeeds; `**skill-config.json`** paths match files on disk.


| #   | Phase        | Description                                                                                                                                                                                                                                                                                                                                                                                                                  | Actor | Input                                      | Output                                                                            | Scripts                                                                                                         | Ref                                                                         |
| --- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- | ------------------------------------------ | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| 3   | Run Operator | You run the structural gate: **Python compile check** on the paths in **skill-config.json**, then `**python scripts/build.py`**, then each **scanner** listed there (this repo includes `**scripts/scanner_skill_builder_layout.py`** for layout sanity). Fix failures in the source files—not by editing **AGENTS.md** by hand when **build** owns it. The **skill** should match §3; **build** exit **0**; scanners **0**. | Code  | The skill directory; **skill-config.json** | Exit **0**; **AGENTS.md** + **content/built/** consistent with **content/parts/** | **agentic-skill-builder** **operator** (or same steps manually); `**python scripts/build.py`**; listed scanners | [agentic-skill-builder README](../../../../agentic-skill-builder/README.md) |


---

## Team process plate (other skills)

To author a **maps-models-specs–style** `**process.md`** (outcome, principles, inputs/outputs, per-stage tables), start from `**content/parts/templates/process-team.md.template`** and `**content/parts/templates/README.md**`.
## Library (merged standards)

### Library: documentation-standards.md

# Skill documentation standards

**Canonical:** `skills/abd-skill-builder/content/parts/library/documentation-standards.md` (merged into **`AGENTS.md`**).

Use these rules when you author or refactor **process**, **phase docs**, optional **`docs/`** reference, staged **`content/built/`** output, and **AGENTS.md** for any Open Agent Skill. They prevent tangled cross-cutting docs and unreadable process prose.

## Delivery mode (`static_built` vs `runtime_injection`)

Declare **`delivery.mode`** in **`skill-config.json`** (default **`static_built`**). That flag answers whether the agent relies on **checked-in** **`content/built/`** + **`AGENTS.md`** or on **runtime** assembly from **`rules/`**, library fragments, and phase manifests. Normative definitions, when each applies, and how the two stay in sync are in **`delivery-modes.md`**.

## Workspace configuration

Every ace-skill declares **`active_skill_workspace`** (mandatory) in **`conf/abd-config.json`** at **`skill_path`**, plus optional **`known_skill_workspaces`**. The install folder does **not** hold the customer project—only pointers. Workspace-local parameters live under **`skill_workspace/conf/`** per skill docs. See **`workspace-config.md`** for **`skill_path`**, **`skill_workspace`**, and deprecated keys. Do not leave “where we run” only in prose unless the skill documents overrides.

## Agent-facing vs reference (read this first)

**If text is merged into `AGENTS.md`, injected into prompts, or otherwise part of the agent bundle, it belongs under `content/parts/`** (e.g. `process.md`, `phases/<phase>.md`, shared fragments). It does **not** live “only in `docs/`” with the expectation that the agent will see it unless your build copies it in.

**Staged build (`content/built/`):** When a complete file is **assembled** from pieces—e.g. a **base** plus **rules** plus **operator/story roles**—write the **intermediate, fully expanded** markdown under **`content/built/`** (or `content/parts/built/` / `phases/built/` if the skill already uses that layout). Then the final step generates the **complete** artifact (`AGENTS.md`, a single phase handoff, etc.). Do not skip the staged output if you need to diff or review what rules were baked in. (Example pattern: `abd-solution-modeler` uses `phases/built/` for phase specs.)

**`docs/`:** Use for **long-form reference** that operators (or tools) open beside the skill—principles, execution order, invariants, **and** standalone construct write-ups (schemas, package layout) **when** those are **not** duplicated as the sole copy of agent instructions. Phase tables and “what you must do” for the agent still live in **`content/parts/`**; `docs/` may **link** to the same ideas or hold deeper detail. If a norm must be in the agent’s context, mirror or generate it from `content/parts/`, not only from `docs/`.

## Voice and role

Write for the **operator** in **second person** (you, your). Frame the work clearly:

- **Your role** — What you are responsible for in this stage or skill (one or two sentences).
- **What you must do** — Imperatives and phase order (use bullets for several short obligations).
- **What you produce** / **How you know you succeeded** — Outcomes and done criteria.

Prefer **you must**, **you will**, and **then you** (sequence) over passive voice (“the pipeline establishes,” “artifacts are emitted”). Say who runs a script or makes a decision.

## Where content belongs

| Kind | Put it here | Do not |
| --- | --- | --- |
| **Process spine** — stages, phase numbers, tables, links to phase files | `content/parts/process.md` (or skill’s `content/process.md`) | Paste the entire phase table again as a second narrative. |
| **Phase behavior** — steps, checklists, file paths for that phase only | `content/parts/phases/<phase>.md` | Split one phase across three cross-cutting docs. |
| **Baked agent instructions** — bases + rules + roles merged before `AGENTS.md` | Source fragments under `content/parts/`; **output of merge** under `content/built/` (or `phases/built/`) **before** final generation | Edit only the final `AGENTS.md` by hand when a build step should own the merge. |
| **Standalone construct reference** — one artifact contract (schema, validators, chunk layout), diagrams, deep dives | `docs/<descriptive-name>.md` | Treat `docs/` as the **only** place agent-facing norms live; duplicate the “must do” into `content/parts/` or generate into `content/built/`. |
| **Cross-cutting** — principles, execution order, invariants that apply across phases | Usually `docs/` (`principles-and-rules.md`, `execution-and-success.md`, `pipeline_invariants.md`); **link** from `content/parts/` where needed | Restate every phase inside them; **link** to the process table instead. |

**Reference-doc filenames:** Do **not** prefix `docs/` filenames with phase numbers (e.g. avoid `phase2_terms.md`). Use **descriptive kebab-case** slugs (`terms-mechanisms-contract.md`, `behavioral-story-map.md`). Phase order belongs in `process.md` and `content/parts/phases/`, not in filenames.

**Cross-cutting** is for rules and order that are **not** naturally owned by a single phase. If the text is really about one phase only, prefer that phase’s file in `content/parts/phases/` plus a thin pointer from `docs/` if you keep a global index there.

## Prose style

- Several **short** points → **bullets**.
- One developed idea → **sentences** in a **paragraph**.
- Avoid long **semicolon chains** pretending to be one sentence.
- Avoid narrating **migration** from an old doc or old skill (“formerly §2.6”). Describe **this** skill only.

## Process tables

Keep the **stage narrative** at **intent and outcome**. The **table** holds actors, scripts, refs, and fixture paths.

You may add a **Summary** column to each phase row: **two or three sentences** on what you **do** in that phase and what **outcome** you get, without copying the phase file or listing every script again.

## When you edit

1. Update the **smallest** place: phase file or construct doc first.
2. If you are repeating script names and outputs that are **already** in the table, **delete** the repetition and keep purpose or pointer to `phases/`.
3. Regenerate **AGENTS.md** after changing `content/` so agents see the update.

### Library: workspace-config.md

# Skill path, skill workspace, and configuration (normative)

## Terms (do not conflate)

| Term | Meaning |
| --- | --- |
| **`skill_path`** | The directory where the **skill package is installed** (`SKILL.md`, `rules/`, `scripts/`, install-time `conf/`). Almost nothing here is **about** a customer corpus or generated artifacts. What **must** live here for workspace routing is **`conf/abd-config.json`**: which **skill workspace** is active, and optionally which workspaces you have used before, so you can **switch** without hunting paths in prose. |
| **`skill_workspace`** | The **root of the project or solution** you are working on right now (e.g. MM3, a customer repo). This is the **mandatory “where am I running?”** location. Context defaults (e.g. `context/`) are under this root unless you pass paths explicitly. **Anything generated, created, or rendered by the skill** goes under **`skill_workspace/<skill_directory_name>/`** unless the skill’s workspace config overrides the output folder. |
| **Solution workspace** | Same **root** as **`skill_workspace`** in this pipeline: the solution/project tree—not the skill install folder. |

## Two levels of `conf/`

### 1. Install: `<skill_path>/conf/abd-config.json` (mandatory)

**Required**

| Key | Meaning |
| --- | --- |
| **`active_skill_workspace`** | Path to the **`skill_workspace`** root (absolute preferred). You **cannot** run the skill in a meaningful way without this. Relative paths are resolved from **`skill_path`**. |

**Optional**

| Key | Meaning |
| --- | --- |
| **`known_skill_workspaces`** | Array of paths (strings) for **other** workspaces this skill has worked on, so tooling or operators can **pick** or **add** a workspace without editing unrelated files. |

**Deprecated (still read by older scripts):** `solution_workspace`, `skill_space_path` — same role as **`active_skill_workspace`**; migrate to **`active_skill_workspace`**.

The install folder does **not** hold customer data or large generated trees—only the skill package and this routing config.

### 2. Workspace: `<skill_workspace>/conf/` (per workspace)

Each **`skill_workspace`** should have a **`conf/`** directory for **parameters that are unique to that workspace** (and optionally per-skill files inside it). Examples:

- **`solution.conf`** at the workspace root (some skills) or under **`conf/`** as the skill evolves.
- **`conf/abd-config.json`** inside the workspace (e.g. story-synthesizer) for **context paths** and other **workspace-local** settings.

Skills document the exact filenames and precedence.

## Overrides

Environment variables may override for CI or local runs; each skill’s **`README`** or **`scripts/_config.py`** states precedence. Default: set **`active_skill_workspace`** in **`conf/abd-config.json`** first.

## Scaffold guarantee

**`abd-skill-builder`** scaffold (**`scaffold_skill.py`**) creates **`conf/abd-config.json`** and **`conf/README.md`** with **`active_skill_workspace`** and **`known_skill_workspaces`**. Replace **`active_skill_workspace`** with a real **`skill_workspace`** root before running pipelines.

### Library: delivery-modes.md

# Agent delivery modes (static build vs runtime injection)

Skills can hand instructions to an **agent** or **executor** (including an EA / orchestrator) in two ways. **Do not mix them in one session without an explicit choice** — same requirement as §3.3 *Assembly model* in [`skill-standards-section-3.md`](skill-standards-section-3.md) (static vs dynamic).

## `AGENTS.md` — always (skill-wide orientation)

**`AGENTS.md`** is the **assembled agent bundle**: how the skill is structured, how phases/steps relate, and how to work with it in general. It should be **assembled for every skill** (typically generated by **`scripts/build.py`**), regardless of **`delivery.mode`**. It is *not* what the mode flag switches on or off.

**What `delivery.mode` actually changes** is how a **single operation** (or phase/step run) gets its **process slice**: either from **pre-generated built output** or from **runtime injection** of sources — see below.

## Flag (system-wide convention)

Declare the mode in **`skill-config.json`** so tools, CI, and humans agree:

```json
"delivery": {
  "mode": "static_built"
}
```

| `delivery.mode` | Meaning |
| --- | --- |
| **`static_built`** | **Default.** When you **run an operation**, the executor uses **process content that has already been merged into `content/built/`** (and similar per-skill layouts): each slice includes the **process part** plus its **library** and **rules** components as produced by the build. **`AGENTS.md`** is still checked in as the skill-wide bundle; **built** trees are the canonical **operation-time** artifacts. Operators run **`python scripts/build.py`** after changing sources; commits include regenerated files. |
| **`runtime_injection`** | When you **run an operation**, the executor **injects** the **process part** and, in documented order, **all** of its **library** and **rules** components from source paths — **without** requiring that slice to exist as a pre-built file under **`content/built/`**. **`AGENTS.md`** is still assembled for orientation; only the **operation-time** merge strategy differs. |

**Default for new skills:** `static_built`. Use **`runtime_injection`** when you want runtime resolution; use **`static_built`** when you want checked-in slices — **both** require the same **documented injection map** (see below).

## Injection map — document regardless of mode

**`delivery.mode` does not decide whether you document injection.** It only decides **pre-generate** (build + commit **`content/built/`**) vs **inject at run time** after each operation. In **both** cases:

1. **Which** source paths (process slice, **`library/`**, **`rules/`**, …) apply **per operation** (phase/step).
2. **In what order** they are merged / concatenated / injected.
3. **How** that matches the **static** merge (same semantics as **`build.py`**, or **deliberate differences** called out).

Keep this in a **single lookup** place — e.g. skill **`README.md`**, a manifest in **`build.py`**, or a **generated manifest** checked in next to **`built/`** — so someone can **change `delivery.mode` later** without re-deriving paths from scattered files. The only thing that changes is **when** material is materialized (build vs runtime), not **what** the skill is allowed to omit from documentation.

## Mode (a) — `static_built`

- **What is delivered:** Generated markdown under **`content/built/`** (and/or `phases/built/`, `content/parts/steps/built/` per skill layout) plus the top-level **`AGENTS.md`** when the build emits it.
- **Operation-time behavior:** Use the **built** slices (process + library + rules already merged for that slice).
- **When it applies:** CI, reviewable diffs, reproducible runs, “what the agent saw” is literally in git.
- **Operator obligation:** After editing **`content/parts/`**, **`rules/`**, or merge inputs, run **`build.py`** and commit outputs.

## Mode (b) — `runtime_injection`

- **What is delivered:** For **operations**, not a single pre-expanded tree under **`built/`**; the **executor** resolves **phase** (or step) → **files** (`rules/…`, `content/parts/library/…`, process slice, etc.) and **injects** them into context in a documented order (full **process part + library + rules** for that operation).
- **`AGENTS.md`:** Still assembled so the agent understands the skill in general; only **per-operation** content is resolved at runtime.
- **When it applies:** Interactive orchestration, rapid iteration without running the full static pipeline each time, or environments where checking in large built blobs is undesirable (still document the tradeoff).
- **Operator / implementer obligation:** Same as **static** mode for the **injection map** — resolution order, equivalence vs static merge, validation — **not** optional just because execution is dynamic. Runtime mode adds: executor must follow the **same** documented map (or list exceptions).

## Staying in sync between modes

1. **Single source of truth** for *meaning* stays in **unbuilt** inputs: **`content/parts/`**, **`rules/`**, **`docs/`** (reference), not in hand-edited **`AGENTS.md`** when a build owns the merge.
2. **`static_built`** outputs are **derivatives**: regenerating must be repeatable from the same inputs + **`scripts/build.py`** (and any merge manifest the skill defines).
3. **`runtime_injection`** must **not drift silently**: if both modes are supported, the skill should state whether runtime is a *shortcut to the same merge* (ideal) or a *lighter subset* (then list gaps).
4. **Changing sources:** Under **`static_built`**, CI or pre-commit should run **`build.py`** and fail if **`content/built/`** / **`AGENTS.md`** are stale (exact hook is repo-specific).
5. **Switching modes:** The **injection map** (paths + order + equivalence) is what lets you move from **`static_built`** to **`runtime_injection`** or back — update **`delivery.mode`** and keep the **same** map unless you intentionally change behavior.

## Relation to `build.py` flags

Per §3.3, a skill may expose **`--assembly static|dynamic`** (or equivalent) **inside** `build.py` for *how* static snapshots are produced. That is **orthogonal** to **`delivery.mode`**: `delivery.mode` answers whether the **operator/agent relies on checked-in built files** vs **runtime resolution**. A skill can use `runtime_injection` at execution time while still using `build.py --assembly static` to produce reference snapshots for tests.

### Library: process-approach.md

# Process approach — IDE, `process.md`, code phases vs AI-chat phases

**Audience:** Authors and tooling. This is the **default mental model** for how a skill is **used** (Cursor, VS Code, Claude Desktop, similar) and how **phases** are executed.

## Who consumes what


| Artifact                                                               | Who uses it                                     | How                                                                                                                                                                                                                                                                                                                      |
| ---------------------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `**AGENTS.md`** (skill root)                                           | **IDE / assistant**                             | Loaded **automatically** by many tools as context for the repo. It orients the model: pipeline, links, where `process.md` lives. **No one “opens `built/` by hand” as the primary workflow** — the chat does not browse the tree to find instructions; **you tell it what to do** using `**process.md`** and phase docs. |
| `**content/parts/process.md**` (or `pieces/process.md` in some skills) | **Human + chat**                                | **Map of phases**: table rows are **phases**, **Ref** links to phase files. The skill should tell users to **read / `@`-reference** this file to know **how to execute** a given phase (order, actor, script). Example pattern: `@agilebydesign-skills/skills/<skill-id>/content/parts/process.md`.                      |
| **Built phase text** (`phases/built/`, `content/built/`, …)            | **Build pipeline + optional `generate_prompt`** | **Generated** outputs — **not** “what autonomous agents read first.” They exist so you can **materialize** a full instruction block for an AI phase (static mode) or **diff in git** under `static_built` delivery.                                                                                                      |


## Phase kinds (two execution styles)

### 1. Code-driven phases (human or CI runs the script)

- **You run** the Python/shell entry point **normally** (terminal, task, CI).
- **Await** exit code and artifacts the phase defines.
- The **phase markdown** (source) describes **how to invoke** the script, **arguments**, **outputs**, and **what “done” means** — not a prompt to paste unless the phase is hybrid.

### 2. AI-chat–driven phases (instructions for the model)

- The **instruction body** the chat must follow is produced by **prompt generation** — short name: **generate prompt** (implementation often `scripts/generate_prompt.py` per skill; names may vary).
- **CLI shape (contract):** support a **phase selector**, e.g. `python scripts/generate_prompt.py --phase <phase_slug>` (some teams use `phase:<name>` as a single token; equivalent intent).
- **Two modes** (both end with “text the user pastes or tool injects into chat”):


| Mode        | What it does                                                                                                                                                                                                                                                            | When to use                                                                |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Dynamic** | Builds one **string** by **collecting every section** required for that phase (source phase markdown, `library/` fragments, applicable `rules/`, manifest order in `skill-config.json` / `build.py`).                                                                   | Fast iteration; single source of truth; no checked-in blob for that phase. |
| **Static**  | Uses **pre-generated** phase text already written under the skill’s **built tree** (convention: `content/parts/phases/built/<phase_slug>.md` or `phases/built/<phase_slug>.md` — **document the path in the skill**). **Grab the whole file** as the instruction block. | Reproducible snapshots, CI, “exactly what shipped last release.”           |


In **either** mode, the **outcome** is: **the IDE chat has the right block of instructions** to follow for that phase — not “the agent navigates to `built/` like a filesystem API.”

## What `build.py` is for

- `**scripts/build.py`** merges **process + library + phases (+ rules where applicable)** into `**AGENTS.md`** and any `**content/built/**` slices per `**delivery.mode**`.
- It is the **authoritative** driver for **this** skill repo. `**generate_prompt`** is **orthogonal**: it answers “what text do I put in chat **for this AI phase**?” while `**build.py`** answers “what ships in **AGENTS.md** / static bundles?”

## Relation to §3

- **Stages / phases / steps** table semantics: `[skill-standards-section-3.md](skill-standards-section-3.md)`.
- **Rule file naming, assembly flags:** same §3 doc.
- **Delivery modes (`static_built` vs `runtime_injection`):** `[delivery-modes.md](delivery-modes.md)`.

## Team process plate (rich `process.md`)

For skills that need the same **shape** as **abd-maps-models-specs** — **outcome**, **principles**, **inputs / outputs**, **stages**, and a **wide phase table** (Description, Actor, Input, Output, Scripts) — start from the **team template**:

- **`content/parts/templates/process-team.md.template`** (in **abd-skill-builder**)
- **`content/parts/templates/README.md`** — how it relates to scaffold’s minimal **`templates/process.md.template`**

Copy the plate into **your** skill as **`content/parts/process.md`**, replace `{{skill_name}}`, add phases and **Ref** links, then run **`python scripts/build.py`**. The **abd-skill-builder** **`process.md`** demonstrates the same structure at production quality.

## Extending a new skill

1. Add `**content/parts/process.md`** with phase rows and **Ref**s (or start from **`process-team.md.template`** above).
2. For each **code phase**, document script + I/O in the phase file.
3. For each **AI-chat phase**, either wire `**generate_prompt`** (dynamic/static) or document a manual copy-paste path until scripted.
4. Run `**python scripts/build.py**` so `**AGENTS.md**` stays the IDE-facing bundle.
5. Keep `**process-approach.md**` behaviors in `**README.md**` in one paragraph so consumers know how your skill expects IDE + chat to work.


### Library: authoring-checklist.md

# Skill authoring checklist (human + AI)

**Purpose:** Trackable **`- [ ]` / `- [x]`** tasks for building or evolving a skill. **Copy this file into the skill you are working on** and check items off as you go — if you stop, the next session continues from the **first unchecked** box.

**Canonical source:** `skills/abd-skill-builder/content/parts/library/authoring-checklist.md` — merge updates from here when standards change.

| Role | What to do |
|------|------------|
| **A — Ask** | Use the **Ask:** lines under each section when you need input. |
| **B — Answer / suggest** | As **AI**, fill proposals; human confirms. |
| **C — Track** | Turn `- [ ]` into `- [x]` only when the item is **done**. |

**Normative layout/operator rules** stay in **`skill-repo-standards.md`** and **`skill-standards-section-3.md`** (under **`content/parts/library/`** in **abd-skill-builder**). **How the IDE uses the skill** (AGENTS.md, `process.md`, code vs AI-chat phases, `generate_prompt`): **`process-approach.md`**.

**Runtime vs `docs/`:** All markdown (and other content) that **pertains to how the skill is used at operation time** — merged or injected by **`build.py`**, read as phase bodies, or otherwise part of the **runnable** package — lives under **`content/parts/`** (and **`library/`**, **`rules/`**, etc. per norms). **`docs/`** is **only** for **non-runtime** material: user manuals, plans, architecture, optional authoring-checklist copies, standards deltas. **Do not** stash mergeable instruction content in **`docs/`**. (**abd-skill-builder** itself only keeps **`docs/standards-delta.md`**; copy this checklist to **`<your-skill>/docs/authoring-checklist.md`** when you track work.)

---

## Before you start (every session)

- [ ] **Working copy:** Copy **`content/parts/library/authoring-checklist.md`** (from **abd-skill-builder**) to **`docs/authoring-checklist.md`** inside **the skill you are building** (under **`active_skill_workspace`** / your project). **abd-skill-builder** does not maintain its own **`docs/authoring-checklist.md`**.
- [ ] **Resume:** Find the **first unchecked** `- [ ]` below and continue from there.
- [ ] **Optional:** Note the date and “stopped at §…” in **Gaps / follow-ups** at the bottom when pausing.
- [ ] **`docs/` vs `content/parts/`:** No **runtime** markdown under **`docs/`** — phases, library bodies, and anything **`build.py`** merges/injects stay in **`parts/`**. **`docs/`** = manuals, architecture, migration notes, **authoring-checklist** only.

---

## Greenfield vs existing skill

- [ ] **New skill:** Ran **`scaffold_skill.py`** (or equivalent) so the base tree exists.
- [ ] **Existing skill:** Ran **[migrate.md](content/parts/phases/migrate.md)** (inventory + delta report + user chose fixes) **before** bulk edits — **or** consciously skipped with a note in **Gaps / follow-ups**.

---

## Skill identity (what this skill does — not delta to other work)

Normative row: **Documentation focus** in **`skill-repo-standards.md`**.

- [ ] **Process, rules, and docs** describe **what this skill does** and how to run it — **this package**, on its own terms.
- [ ] They do **not** rely on “vs another skill” or “we don’t do X because Y” — that stays out of durable spec.
- [ ] **Dependencies** (other skills, repos, tools, versions) recorded explicitly (**Dependencies** / `README` / `conf/build-strategy.json`) — separate from the main narrative.

**AI should:** Strip migration chatter; put relationships in a **Dependencies** list.

**Ask:** “If this skill vanished, could someone run it from **this repo alone**?”

---

## Base scaffold: what you copy and extend

**Source:** **`skills/abd-skill-builder/scripts/scaffold_skill.py`** + **`skills/abd-skill-builder/templates/*`** — extend these files; don’t invent a parallel layout.

### Scaffold files present and reviewed (check each)

- [ ] **`SKILL.md`** — frontmatter + description make sense.
- [ ] **`skill-config.json`** — `operator.*`, `delivery.mode` match intent.
- [ ] **`conf/build-strategy.json`** — `skill_purpose` and siblings filled per Strategizer.
- [ ] **`conf/abd-config.json`** — **`active_skill_workspace`** set (under **`test/`** when using a workspace).
- [ ] **`conf/README.md`** — conf usage clear.
- [ ] **`content/parts/process.md`** — pipeline table matches real phases.
- [ ] **`content/parts/phases/`** — one file per row in **`process.md`** (add/rename beyond **`author.md`** as needed).
- [ ] **`content/parts/phases/built/`** — present when you use **static** AI-chat prompts; populate via **`build.py`**; see **`process-approach.md`**.
- [ ] **`scripts/generate_prompt.py`** — present for AI-chat phases; **`--mode dynamic`** vs **`static`** documented; extend per skill.
- [ ] **`scripts/build.py`** — merge/injection driver present (see non-negotiables below).
- [ ] **`scripts/scanner_smoke.py`** — replaced or supplemented with real scanners if needed.
- [ ] **`rules/README.md`** + **`rules/scanners.json`** — wired when rules exist.
- [ ] **`test/README.md`** — explains layout; workspace path if used.
- [ ] **`content/parts/library/`** — created when cross-cutting chunks exist; wired in **`build.py`** (e.g. **`PHASE_LIBRARY`**) per §3.

### Non-negotiables

- [ ] **`scripts/build.py`** is the **merge / injection driver** (writes at least **`AGENTS.md`** from process + phases).
- [ ] **`process.md`** order matches **`phases/`** and **`build.py`** (if order ≠ lexicographic sort of filenames, **`build.py`** uses an **explicit ordered list**, not **`sorted(glob)`**).
- [ ] **Process → operation injection** documented in/near **`build.py`** + human-readable place for §4.

### Reference templates read (when extending)

- [ ] Opened **`abd-skill-builder/templates/child_build.py.template`** (minimal merge).
- [ ] If per-operation bundles / library injection: reviewed **`abd-maps-models-specs/scripts/build.py`** (`PHASE_FILES`, `PHASE_LIBRARY`, built phases).

### Extension work (after §§0–4 answers)

- [ ] **One** **`build.py`** — no second hidden merge pipeline.
- [ ] **`process.md`**, **`phases/*.md`**, **`build.py`** updated **together** when adding/changing a phase.
- [ ] **`content/parts/library/`** chunks added and wired in **`build.py`** where needed.
- [ ] **Injection map** in **`build.py` docstring** and/or skill **`README.md`** (aligns with §4).
- [ ] **`python scripts/build.py`** run after structural edits; **`AGENTS.md`** / **`content/built/`** committed if **`static_built`**.

**Ask:** “Which files do we **edit** vs **add**? Where is the **ordered phase list** in **`build.py`**?”

---

## 0. Build intent (`conf/build-strategy.json`)

- [ ] **`conf/build-strategy.json`** complete per **`agentic-skill-builder`** (template + Strategizer).

**Ask:** “What must this skill accomplish end-to-end? Who runs it? What is out of scope?”

---

## 1. Process & phases

- [ ] **`content/parts/process.md`** lists the real pipeline (ordered phases).
- [ ] Phase files use **descriptive slugs**; order matches **`process.md`** and **`build.py`** (explicit order if not sort order).
- [ ] **`build.py`** phase list / merge keys updated when **`process.md`** changes.

**Ask:** “Phases in order?”

---

## 2. Rules (optional) & scanners

- [ ] Decided if **`rules/`** is needed.
- [ ] Listed planned **`rules/*.md`** files (one concern per file where possible).
- [ ] Decided scanner vs doc-only for each rule cluster.
- [ ] **`rules/scanners.json`** + **`skill-config.json`** `operator.scanners` aligned if scanners exist.

**Ask:** “Machine-checked vs human-reviewed? What would each scanner inspect?”

---

## 3. Library — cross-cutting concepts (`content/parts/library/`)

- [ ] Cross-cutting content in **`library/<slug>.md`** (or skill-specific equivalent).
- [ ] **`build.py`** merge order matches how phases reuse library.
- [ ] Optional **index** (short links only: **`README`**, **`conf/build-strategy.json` notes**, or a **`docs/*` index** if non-runtime) — **not** a second home for bodies; full cross-cutting copy stays in **`library/`** (see **`docs/` vs parts** in **`skill-repo-standards.md`**).
- [ ] Same concept **names** across phases.

**Ask:** “What repeats across phases → **library**?”

---

## 4. Agent delivery mode (`skill-config.json` → `delivery.mode`)

See **`abd-skill-builder`** [`delivery-modes.md`](content/parts/library/delivery-modes.md) (canonical: `skills/abd-skill-builder/content/parts/library/delivery-modes.md`).

- [ ] **`AGENTS.md`** assembled (both modes).
- [ ] **Injection / merge map** documented (paths per operation, order, equivalence to static) — **`README`**, **`build.py`**, or manifest — so mode can change later (narrative-only; sources remain under **`content/parts/`**).
- [ ] **`delivery.mode`** set: **`static_built`** or **`runtime_injection`**.
- [ ] If **`static_built`**: **`build.py`** run; **`content/built/`** (and peers) committed; traceable to map.
- [ ] If **`runtime_injection`**: runtime follows documented map (or deltas documented).

**Ask:** “Per operation: which files, which order, where is the lookup?”

---

## 5. `test/` — script tests & fixtures

- [ ] Chose: pytest **yes** or **no** (if no, skip pytest bullets; may still use **`test/`** for fixtures).
- [ ] If pytest **yes**: dev deps + **`pip install`** documented (**`requirements-dev.txt`** or **`pyproject.toml`**).
- [ ] **Run command** documented (e.g. **`python -m pytest test/`**).
- [ ] **CI** runs tests (optional).
- [ ] Tests live under **`test/`**; **`test/fixture/`** if needed.
- [ ] **`active_skill_workspace`** path under **`test/<name>/`** documented if set.

**Ask:** “What must stay green? Best fixture?”

---

## 6. Operator contract — “built the skill”

- [ ] **`SKILL.md`** + frontmatter.
- [ ] **`skill-config.json`** paths match disk.
- [ ] **`python scripts/build.py`** exits **0**.
- [ ] **Python compile check** on **`operator.compileall_paths`** passes (Operator uses Python’s **`compileall`** under the hood).
- [ ] **Scanner** scripts exit **0** (if any).

**Ask:** “Operator green?”

**Final:**

- [ ] **Attest** structurally built — **or** list gaps below.

---

## Gaps / follow-ups (free text)

Use for **resume notes** (date, last § completed, blockers):

```text


```

---

## How to use this file

1. **Copy** into **your skill** (or workspace) as **`docs/authoring-checklist.md`** before deep work — from **`abd-skill-builder`** **`content/parts/library/authoring-checklist.md`**.
2. Check **`- [x]`** only when done; **first unchecked** = resume point.
3. Pull updates from **`abd-skill-builder`** canonical copy when standards change.

### Library: skill-repo-standards.md

# Skill repository standards (index + extras)

**Process approach (IDE, `process.md`, code vs AI phases, `generate_prompt`):** [`process-approach.md`](process-approach.md) — **start here** for how skills are **used** in Cursor / similar: **`AGENTS.md`** auto-loaded, **`@…/process.md`** for phase map, **code phases** vs **AI-chat phases**, **dynamic vs static** prompt generation.

**Full normative §3 (all subsections):** [`skill-standards-section-3.md`](skill-standards-section-3.md) — directory and content conventions (**§3.1**), rule naming (**§3.2**), assembly (**§3.3**), reference notes (**§3.4**): stages/phases/steps, process tables, optional domain+story-map pattern, `AGENTS.md` / `content/built/`.

**Builder vs Operator (summary):** [`builder-vs-operator.md`](builder-vs-operator.md) — **scaffold / generation** path vs **`operator.run_operator()`** validation today.

**Authoring checklist (human + AI):** [`authoring-checklist.md`](authoring-checklist.md) — **copy into the skill or workspace** you are editing as **`docs/authoring-checklist.md`** (not stored in **abd-skill-builder**’s **`docs/`**); work through **`- [ ]` / `- [x]`** items so work can **resume after interruption** (first unchecked box = continue here). Covers scaffold verification, rules/scanners, **library**, **`delivery.mode`**, **`test/`**, operator.

**Migrating an existing skill:** [`../phases/migrate.md`](../phases/migrate.md) — inventory → compare to standards → **delta report** → **user chooses which gaps to fix** (no silent full rewrites).

**Example delta (this repo):** [`../../docs/standards-delta.md`](../../docs/standards-delta.md) — `abd-skill-builder` inventory vs §3 (delivery, `content/built/`, docs, tests/fixture notes).

---

## Quick layout reminder (before reading the full §3)

| Area | Convention |
|------|------------|
| **Entry** | `SKILL.md` at skill root (frontmatter: `name`, `description`). |
| **Operator config** | `skill-config.json` — `operator.compileall_paths`, `operator.build_script`, `operator.scanners`. |
| **Agent delivery** | `skill-config.json` — `delivery.mode`: **`static_built`** (pre-generate per-operation slices into **`content/built/`**) or **`runtime_injection`** (resolve the **same** sources at run time). **Only** that choice differs — always document **which paths** feed each operation, **merge order**, and **equivalence** to static output, in a **lookup** place (skill **`README.md`**, **`build.py`** manifest, or emitted manifest) so the team can switch modes later. **`AGENTS.md`** in **both** modes. See **`abd-skill-builder`** [`delivery-modes.md`](delivery-modes.md) (canonical: **`content/parts/library/delivery-modes.md`**). |
| **Authoring prose (normative for writers)** | [`documentation-standards.md`](documentation-standards.md) — voice, where content belongs, process tables; complements **`docs/` vs `content/parts/`** rule. |
| **Workspace routing** | [`workspace-config.md`](workspace-config.md) — **`skill_path`**, **`skill_workspace`**, **`conf/abd-config.json`** keys. |
| **Build intent** | `conf/build-strategy.json` — strategize loads this **whole JSON**; **`skill_purpose`** must be non-empty for **`strategy_complete`** (minimum to finish strategize). Other keys are **siblings** that enrich **`strategy`** / **`builder_manifest`** — they are **not** part of the **`skill_purpose`** text. See **`agentic-skill-builder/README.md`** (Strategizer). |
| **Normative content** | `content/parts/` — process table rows are **phases**; **steps** inside phase files. Phase markdown files use **descriptive slugs** (`terms-mechanisms.md`, …) — **not** `phase-NN-…` or phase numbers in **H1** titles; pipeline order is **only** in `process.md` (# column) + `build.py` merge list (see **`skill-standards-section-3.md`**). |
| **docs/ (non-runtime only)** | **`docs/`** is for material **not** consumed as merged/injected skill payload at operation time: **user manuals**, **migration/planning notes**, **architecture**, optional **authoring-checklist** copies, **standards deltas**. In **abd-skill-builder**, **`docs/`** is only **`standards-delta.md`** — delivery merge order lives in **`README.md`**. **Do not** put markdown (or other assets) in **`docs/`** that **`build.py` merges**, **injects**, or **ships** as the runnable instruction body for phases/operations — that belongs under **`content/parts/`** (including **`library/`**, **`phases/`**, **`process.md`**, **`rules/`** as applicable). |
| **Library** | `content/parts/library/` — **cross-cutting** material reused across more than one phase: definitions, tables, glossaries, named concepts. The library **is** the home for cross-cutting content; do not maintain a parallel “cross-cutting” layer elsewhere. **`docs/`** may hold a **short index** pointing into **`library/`**; **bodies** live in **`library/`**; merge order lives in **`build.py`**. |
| **Rules** | `rules/*.md` or `content/parts/rules/*.md`; optional `rules/scanners.json`. |
| **Scripts** | `scripts/build.py` (**required** — merge/injection driver; scaffold template is minimal; extend with explicit phase order + per-operation bundles as in **`abd-maps-models-specs`** when needed), scanners, optional `_config.py`. See **`authoring-checklist.md`** → *Base scaffold*. |
| **Tests & fixtures** | **`test/`** — all automated tests for the skill (pytest, smoke scripts, etc.) that exercise **`scripts/`**; optional **`test/fixture/<scenario>/`** for frozen inputs/snapshots; optional **`test/<workspace>/`** dirs when **`conf/abd-config.json`** uses **`active_skill_workspace`** (path relative to skill root). Example: **`abd-maps-models-specs/test/`** — workspace **`test/mm3`**, fixture **`test/fixture/mm3/`**. **`abd-skill-builder`** itself **does include** **`test/`** (see **`test/README.md`** + **`test/fixture/toy-polite-dialogue/`**) even though **pytest `test_*.py` files** are still optional follow-ups — do not read “pytest wiring pending” as “no **`test/`** folder.” **Operator today** only runs a **Python compile check** on **`operator.compileall_paths`** (usually **`["scripts"]`**; implemented with **`compileall`**) — it does **not** install or run **pytest**. If automated tests are **in scope**, add the **wiring** below. |
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
5. Each listed **scanner** exits 0.
6. **`rule_scanner_bindings`**: each `rule` and `scanner` path exists.

---

## What greenfield scaffold should emit

**`scripts/scaffold_skill.py`** (and equivalent generators) should produce a **complete, runnable skeleton**: file tree, `skill-config.json`, phase markdown stubs, `rules/` / `conf/` as needed, runnable **`build.py`**, optional scanner stubs — **without** baking in customer-specific “gold” domain solutions (those belong in the target workspace, not the template).

This **`abd-skill-builder`** skill ships **templates + `scaffold_skill.py`** as the supported way to create that tree. **`operator.run_operator()`** then validates what is on disk; it does not scaffold new skills by itself.

### Library: skill-standards-section-3.md

# §3 Skill package layout and content standards

**What this is:** Normative rules for how a **skill repository** is shaped — where **runtime** content lives (`content/parts/`, `rules/`, `build.py`), how **stages / phases / steps** relate, how **process tables** and **Refs** work, optional patterns (e.g. domain + story map), **rule file naming**, and **static vs dynamic** assembly of instructions. **How skills are used in the IDE** (AGENTS.md, `process.md`, code vs AI-chat phases, `generate_prompt`) is defined in [`process-approach.md`](process-approach.md) — read that first.

**How to use it:** Implement **§3.1–§3.4** when authoring or reviewing a skill. Tools and humans use the same rules; nothing here depends on any external “origin” document.

**Scope boundary — skills stay simple:** A **skill package** should express a **linear** pipeline: **stage → phase → (steps inside phase docs)**. The **process table** rows are **phases**, not steps. Keep skills deliberately sequential.

## 3.1 Directory and content conventions

**Hierarchy in the repo:** **Stages** group **phases**. Each **phase** has normative markdown (one file or section per phase, per skill); **steps** live **inside** that phase’s markdown — they are **not** separate rows in the master process table. See **Stages, phases, and steps** below.


| Area                            | Convention                                                                                                        | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Normative content**           | Under /`content/parts/`                                                                                           | Plans, operations, domain narrative — **not** dumped only in chat.                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `**docs/` (non-runtime)**       | /`docs/` at skill root                                                                                            | **User manuals**, **migration/planning notes**, **architecture**, **authoring checklists**, and **narrative** descriptions of delivery. **Do not** put markdown here that `build.py` **merges**, **injects**, or **ships** as the runnable phase/operation body — that belongs under `**content/parts/`** (including `**library/`**, `**phases/`**, `**process.md**`, `**rules/**`).                                                                                                                                   |
| **Phase markdown (source)**     | e.g. /`content/parts/phases/<descriptive-slug>.md`, or one doc per phase with step sections — paths vary by skill | **One row in the process table = one phase.** **Steps** (numbered sub-procedures, “Step 1…”, checklists) are written **inside** this markdown as **normative content of the phase**, not as their own table rows. **Do not** encode execution order in filenames or H1 titles (`phase-02-foo.md`, `# Phase 2 — …`): order belongs in `**process.md`** (the `#` column) and in `**scripts/build.py`**’s explicit file list. Use **stable descriptive** kebab-case slugs so renumbering the plan does not force renames. |
| **Built phase markdown**        | `content/parts/phases/built/<descriptive-slug>.md` and/or `content/built/…` per skill layout | **Generated** from source phase bodies + rules via `scripts/build.py`. **Authors do not hand-edit `built/`.** These files are **materialized instruction blobs** for **static** AI-chat phases and for **`static_built`** delivery — consumed by **`generate_prompt`** (or pasted into chat), **not** by “agents browsing the repo” as the primary UX. IDEs load **`AGENTS.md`**; see [`process-approach.md`](process-approach.md). Folder layout (`phases/built` vs `content/built`) is per skill; document it in **`README.md`**.                                                                                                                                                                                                            |
| **Atomic rules**                | `content/parts/rules/*.md` (or top-level `rules/` in simpler skills)                                              | One concern per file where possible; **names** should encode **phase** and/or **domain concept** + rule name (see §3.2).                                                                                                                                                                                                                                                                                                                                                                                               |
| **Roles**                       | `roles/*-role.md`                                                                                                 | One file per **user/agent role** the skill assumes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Process**                     | `content/parts/process.md` or staged process docs                                                                 | **Summary table: each row is a phase** (linked by **Ref** to phase markdown). Stages group those rows. **Steps** appear only **inside** the linked phase files.                                                                                                                                                                                                                                                                                                                                                        |
| **Repo-facing built artifacts** | `AGENTS.md`, `SKILL.md`, sometimes `README.md`                                                                    | Frequently produced by `scripts/build.py` (merge order per skill). **`AGENTS.md`** is what **IDEs and assistants typically load automatically** for the skill repo.                                                                                                                                                                                                                                                                                                                                                                |
| **Config**                      | `skill-config.json`                                                                                               | Name, version, paths — skill-specific knobs.                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Scripts**                     | `scripts/`                                                                                                        | Operational entry points; may share `_config.py` patterns.                                                                                                                                                                                                                                                                                                                                                                                                                                                             |


### Stages, phases, and steps (how they relate)

**Order is always:** **Stage → Phase → Step** (coarse → mid → finest) — but **only the first two appear as rows** in the master process table. **Steps** are **inside** the phase markdown.


| Term      | Typical meaning                                                                                                                                                                                                                                                                                                                      | Example                                                                                  |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **Stage** | **Coarse pipeline slice** — groups many **phases**; may span days or sessions. Often a heading or section in `process.md` or a staged doc.                                                                                                                                                                                           | **Stage 1 — Extract Context**; **Stage 2 — Map and Model**; **Stage 3 — Specification**. |
| **Phase** | **One row** in the process summary table — the unit of “what we do next” with a **driver**: **human** or **AI actor**. The **Ref** column links to **phase** markdown. Phases answer “are we allowed to proceed?” and **contain** the detailed steps as normative body copy.                                                         | “Corpus audit — Phase 0”; **Initiator / Actor** column = human vs AI.                    |
| **Step**  | **Sub-structure inside the phase’s markdown** — numbered instructions, checklists, “Step 1 / Step 2”, optional **suffix letters** (`5a`, `7a`) for companion script runs **within the same phase**. **Not** a row in the process table. Machine state (if any) may still reference `workflow_step` as a **sub-id** inside the phase. | Inside `modules-epics-scaffold-breadth.md`: “1. … 2. … 3a. rebuild index …”              |


**AI-driven phases — how the operation is delivered:** See **[`process-approach.md`](process-approach.md)**. In short: **code-driven** phases = run scripts as documented in the phase file; **AI-chat** phases = produce the instruction block via **`generate_prompt`**-style tooling in **dynamic** (assemble sections) or **static** (use pre-built phase markdown under `phases/built/` or equivalent). The **chat** follows that text; **`built/`** is not “the agent’s filesystem API.”

**Ordering (linear, inside the skill):** Stages order **major outcomes**. **Phases** run in **process table order** (each row = one phase). **Steps** follow the order **written inside** each phase document. **Parallel batches, fan-out, or merge** are **not** modeled as extra table rows; if needed, handle that **outside** the skill package (host app, orchestration, or scripts). **Phases** may **block** a later stage until accepted (e.g. “Phase 0 says rebuild chunks — do not start Stage 2 until accepted”).

**“Process” one-liner:** `content/parts/process.md` (or `parts/process.md`) often opens with a **single pipeline string** (e.g. Context → Foundational spine → …). That line is the **navigation spine**; the **table lists phases** (by stage); **authoritative step detail** lives inside each **Ref**’d phase file.

### Process tables, hyperlinks, and naming in the Ref column

**How the table is built**

- **Rows are phases**, not steps. Columns typically include: `#`, **Phase** (title — sometimes labeled “Step” in legacy tables; **semantically it is the phase**), **Initiator / Actor** (Human→Code, AI, Code), **Script** (if any), **What it does**, **Coverage**, **Ref**, **Inputs**, **Outputs**.
- **Ref** is the **hyperlink hub**: each row points to the **normative markdown for that phase**. **Steps** (numbered sub-procedures) live **inside** that file — not in separate table rows. Python entry points stay in **Script**, not **Ref**.
- **Two-tier phase files:**
  - **Source:** phase markdown authors edit (e.g. `content/parts/phases/<name>.md`, or `parts/steps/<name>.md` when the filename is the **phase** slug — naming varies by skill).
  - **Built:** `content/parts/phases/built/<name>.md` or `content/built/<name>.md` — **rules baked in** from `parts/rules/*.md` via `scripts/build.py`. **Steps remain inside** the built document. Used for **static** prompt generation and **`static_built`** slices — not hand-edited. See [`process-approach.md`](process-approach.md).
- **Cross-links inside the table:** The **Ref** column uses relative markdown links to the **phase** doc, e.g. `[context](parts/context.md)`, `[modules-epics-scaffold-breadth (built)](content/parts/steps/built/modules-epics-scaffold-breadth.md)` (paths vary by skill; **from the skill root** per `AGENTS.md`).

**Naming conventions visible in the table**

- **Phase titles** in the table read like **milestones or operations** (“Parse, curate, chunk, index”, “Integrate and Harmonize”) — stable labels for **phase** / workflow fields. **Finer labels** for **steps inside the phase file** may appear in JSON as `workflow_step` or similar.
- **Phase file names and H1 headings** must **not** duplicate pipeline indices (`phase-00-`, `Phase 3 —` in the title). Those numbers **change** when the plan evolves; **brittle** names churn git history and links. The **Ref** column and `build.py` define order; phase files stay **semantically** named (`story-map.md`, `canonical-context.md`).
- **Letter suffixes** (`5a`, `7a`) describe **sub-steps inside a phase** (e.g. companion script after a numbered step) — **inside the phase markdown**, not extra table rows.

### Concepts and cross-cutting artifacts (generic — all skills)

**This section is the generic rule.** A **skill** packages **concepts** (ideas, definitions, invariants, roles) and **artifacts** (outputs, schemas, manifests) that the workflow references across **multiple stages or phases**. Anything that would be **repeated** if pasted into every phase file should instead live in **its own file** (usually markdown under `content/parts/`, sometimes JSON alongside) so there is a **single source of truth**.


| Guideline           | Meaning                                                                                                                                                                                                         |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **When to extract** | If a concept or artifact **spans** more than one phase (or stage), give it a **dedicated** doc (or structured file) and **link** from phase bodies — do not duplicate long definitions in each phase.           |
| **Naming**          | Conventional filenames (`glossary.md`, `concepts.md`, `artifacts.md`, `roles/`*, etc.) vary by skill; **discover** and **validate** presence from templates and this skill’s `build.py`, not one global layout. |
| **Not every skill** | A minimal skill might only have `SKILL.md`, `content/parts/process.md`, and phase files — **no** separate “domain” or “story map” layer. That is valid.                                                         |


### Optional pattern — domain narrative + interaction tree (maps-models–class skills only)

Some skills (notably **abd-maps-models-specs** and similar) **choose** to separate **two parallel artifacts** that must stay in sync. **Do not** treat this table as the default for **all** skills — only for skills that explicitly adopt this shape.


| Piece                            | Role                                                                                                                                                                                                    | Typical location (example skill)                                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Domain narrative**             | **State and structure** — modules, **domain concepts** (CRC-style: owns, properties, operations, `extends`, invariants), evidence hooks. Answers **what things are** and **what owns which rules**.     | e.g. `parts/domain.md` + evolving `map-model-spec.json` (`modules_and_epics`, `concepts[]`, chunk citations). |
| **Story map / interaction tree** | **Behavior** — epics, sub-epics, stories, scenarios; **Trigger / Response**; **Pre-Condition**; **Given/When/Then** where required. Answers **who does what** and how behavior references domain state. | e.g. `parts/story-map.md` + nested JSON under epics (`stories`, `sub_epics`, etc.).                           |


**When this pattern applies**

- **Same vocabulary:** Domain concept names (`concepts[].name`) and story references can be held to **one namespace** — scanners may enforce **exact string match** where the skill defines that rule.
- **Evidence ladder / paired edits:** Concepts may carry `evidence_stage`; **domain** vs **journey** edits are **paired** in skills that implement both files.
- Skills **without** this split still use the **generic** rule above: cross-cutting concepts → **their own** markdown (whatever the skill calls them), not repeated per phase.

## 3.2 Rule file naming (heuristic standard)

Target pattern (flexible regex for validation):

```text
{phase-or-stage}__{domain-concept-or-scope}__{short-rule-name}.md
```

Examples mirror **story synchronizer / maps-models** style: scanners and rules tied to **phase** and **concept** (e.g. `chunks_must_be_referenced`, `concept-layering-scaffold`). **Propose** names from the **phase** + concept + verb (and step text inside the phase doc if needed), then **check uniqueness** under `parts/rules/`.

## 3.3 Assembly model (static vs dynamic)

**Two different “static vs dynamic” pairs** — do not conflate:

1. **`build.py` assembly** (repo artifacts): Each skill ships `scripts/build.py`. It merges **process + library + phases (+ rules)** into **`AGENTS.md`** and optional **`content/built/`**. Flags like `--assembly static|snapshot` are **per skill** when present.

2. **AI-chat prompt generation** (`generate_prompt`): For **AI-driven** phases only — **dynamic** = assemble instruction string from sections; **static** = emit text from **pre-built** phase file under `phases/built/` (or documented path). See [`process-approach.md`](process-approach.md).

**Per skill:** `build.py` is the **authoritative** merge driver for **this** repo; scaffolding **emit or check** trees — they do **not** replace `build.py`.

**Flag on `build.py`:** The skill’s `build.py` may expose **CLI flags** for snapshot vs interactive merge; exact names are per skill. For **prompt** modes, document **`generate_prompt`** (or equivalent) next to **`build.py`** in **`README`** / **`AGENTS.md`**.


| Mode (merge / delivery) | Mechanism                                                                               | When                                                               |
| ----------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Static (merge)**      | `build.py` merges **built-phase** fragments into `AGENTS.md` / `SKILL.md` (and related) | Release, reproducible snapshot; CI; “what ships”.                  |
| **Dynamic (merge)**     | Runtime concatenation by **phase** / **operation** from `skill-config.json` + manifest  | Interactive sessions, partial rebuild, IDE-driven iteration. |


A **host** (CI, IDE, or orchestrator) may emit an **internal** manifest (JSON or YAML) for a **given generation run**, listing which fragments form which artifact for both modes; the skill’s `build.py` **may read** that manifest (or embedded config) when implementing **static** merges and documents how **dynamic** mode resolves fragments at runtime. That manifest is **optional** and **not** a standard every skill must carry — only **documented** `build.py` behavior is.

## 3.4 Reference skills (illustrative)

Other skills in the monorepo **illustrate** patterns (long `AGENTS.md`, phased pipelines, rules + scanners). They are **examples**, not extra requirements. **Operator** checks and layout rules are grounded in **abd-skill-builder** library files and each skill’s **`skill-config.json`** — not in a separate “corpus” file unless your team adds one.
### Library: builder-vs-operator.md

# Builder vs Operator (today)

**Generation / scaffold (“builder” in the loose sense):** Anything that **emits** a new skill tree — typically **`abd-skill-builder`’s `scripts/scaffold_skill.py`** plus templates — producing `SKILL.md`, `skill-config.json`, phase markdown, `rules/` stubs, `scripts/build.py`, optional scanners. Output should match **§3** layout and avoid embedding customer “gold” solutions in the template.

**Operator (structural gate):** **`agentic-skill-builder`** **`operator.run_operator()`** — validates `skill-config.json`, runs a **Python compile check** on the paths in **`operator.compileall_paths`** (the implementation uses Python’s **`compileall`** module), runs **`operator.build_script`** (typically `python scripts/build.py`), runs **scanners** from **`skill-config.json`**. It does **not** create greenfield skills; that is **`scaffold_skill.py`** and authoring.

**This skill’s role:** Ship **standards** under **`content/parts/library/`**, **process + phases**, **`scaffold_skill.py`**, and **templates** so authors get a compliant tree first, then Operator keeps it green.


## Phase: scaffold

# Phase: Scaffold

For an **existing** skill tree (not greenfield), use **[`migrate.md`](migrate.md)** instead: produce a **delta report**, then **only fix** what the user selects.

## Steps (greenfield)

1. **Authoring checklist:** Open **[`../library/authoring-checklist.md`](../library/authoring-checklist.md)** (in **abd-skill-builder**; copy into **your new skill** as `docs/authoring-checklist.md` — scaffold does this). Work **A → B → C** (ask questions, AI suggestions, check boxes) for build intent, rules/scanners, library, cross-cutting concepts, **`delivery.mode`**, then operator sign-off.
2. Choose a **skill id** (directory name; kebab-case recommended).
3. Run `python scripts/scaffold_skill.py --name <id> --out <parent>/<id>`.
4. Edit `conf/build-strategy.json` — set **`skill_purpose`** (required for `strategy_complete` in the delivery graph). Add other keys from the template as needed; they are **separate fields**, not part of the **`skill_purpose`** string.
5. Flesh out **`content/parts/process.md`** and phase files. For a **rich** process doc (outcome, principles, inputs/outputs, staged tables like **abd-maps-models-specs**), copy/adapt **`content/parts/templates/process-team.md.template`** (team process plate) from **abd-skill-builder**; see **`library/process-approach.md`** → *Team process plate*. Add rules and scanners as needed (see checklist §2–5).
6. Add tests under **`test/`** (scaffold emits **`test/README.md`**); put fixtures in **`test/fixture/…`** and any **`active_skill_workspace`** under **`test/<name>/`** per **[`../library/skill-repo-standards.md`](../library/skill-repo-standards.md)**.
7. Run `python scripts/build.py`, then `agentic-skill-builder run --skill-path <path>` or equivalent Operator checks.

## Anchor

This phase **writes** the skill tree and **establishes** the operator contract — no domain modeling yet.

## Phase: migrate

# Migrate an existing skill to repository standards

Use this when the skill **already exists** and you need to **align** it with **[`skill-repo-standards.md`](../library/skill-repo-standards.md)**, **[`skill-standards-section-3.md`](../library/skill-standards-section-3.md)**, and (where relevant) the **[authoring checklist](../library/authoring-checklist.md)** — not when you are **scaffolding from zero** (`scaffold_skill.py`).

## Outcome

1. A **delta report**: what differs from the standards, **where**, and **why it matters**.
2. A **user choice**: which deltas to fix now, later, or **won’t fix** (with rationale).

The abd-skill-builder agent (or a human) **does not** silently rewrite the whole tree; it **surfaces gaps** and applies fixes **only for items the user selects**.

---

## Process (human + AI)

### 1. Inventory

Walk the skill root and note:

| Area | Look at |
|------|---------|
| **Entry** | `SKILL.md` frontmatter, description |
| **Authoring checklist** | In **each skill** (or workspace): **`docs/authoring-checklist.md`** — copy from [`../library/authoring-checklist.md`](../library/authoring-checklist.md) in **abd-skill-builder** if missing; check off **`- [ ]` → `- [x]`** as you go (resume from first unchecked). **abd-skill-builder** does not keep a checklist under its own **`docs/`**. |
| **docs/ vs parts** | **`docs/`** — non-runtime only (manuals, plans, architecture, optional checklist copies, **`standards-delta.md`** in **abd-skill-builder** only). **Mergeable / operation-time** markdown lives under **`content/parts/`** (and **`library/`**, **`rules/`**). If **`docs/`** holds instruction bodies that should merge, **move** them into **`parts/`** and leave **`docs/`** as index or narrative only (see **`skill-repo-standards.md`**) |
| **Operator** | `skill-config.json` → `operator.*`, paths on disk |
| **Delivery** | `delivery.mode`, `AGENTS.md`, `content/built/` if `static_built` |
| **Content** | `content/parts/process.md`, phase slugs, `build.py` merge order |
| **Library** | `content/parts/library/` — cross-cutting concepts (definitions, tables, glossaries) reused across phases; merge order in `build.py`; no second home for cross-cutting material outside **`library/`** |
| **Rules / scanners** | `rules/`, `rules/scanners.json`, bindings |
| **Scripts** | `scripts/build.py`, scanners, `compileall_paths` |
| **Tests** | `test/` per **Tests & fixtures** in [`../library/skill-repo-standards.md`](../library/skill-repo-standards.md); pytest wiring if tests exist |
| **ABD / workspace** | `conf/abd-config.json`, `active_skill_workspace` |
| **Narrative / identity** | Phases, rules, `SKILL.md` describe **this skill’s** behavior — not chronic “vs other skill” or “we skip X because Y” stories (see **Documentation focus** in [`../library/skill-repo-standards.md`](../library/skill-repo-standards.md)). Dependencies listed **explicitly** where needed. |

### 2. Compare to standards

For each row in **`skill-repo-standards.md`** (quick layout table) and the **§3** tables where applicable, mark:

- **Compliant** — matches normative text.
- **Partial** — close but missing rename, doc, or wiring.
- **Gap** — missing file, wrong shape, or contradicts standards.

### 3. Delta report (written artifact)

Produce a **single markdown or table** the user can keep in the skill (e.g. **`docs/standards-delta.md`**) with **one row per gap**:

| ID | Area | Current state | Expected (standard) | Severity (high/med/low) | Suggested fix |
|----|------|----------------|---------------------|-------------------------|---------------|
| D1 | … | … | … | … | … |

Optional: group by **Operator** vs **content** vs **tests** so fixes can be batched.

### 4. Ask the user what to fix

**Prompt (use verbatim spirit):**

> Here are the gaps between this skill and the repository standards (**N** items).  
> Which **IDs** should we fix in this session? You can choose **all**, **none** (document deferrals only), or a **subset**. For any item you **won’t** fix, say **defer** or **won’t fix** and a one-line reason.

Then:

- Apply **only** agreed fixes (edits, new files, `skill-config.json` updates).
- Re-run **operator** checks (Python compile check, `build.py`, scanners) after substantive changes.
- Update the delta report: mark rows **fixed**, **deferred**, or **accepted risk**.

---

## AI behavior

- **Be specific:** cite paths and standard sections (e.g. “§3.1 phase slugs”).
- **Don’t** treat every cosmetic difference as high severity.
- **Do** call out **operator** failures and **security**-sensitive paths (secrets, arbitrary paths) as **high**.
- If **`pytest`** was requested but missing: reference **When automated tests are asked for** in **[`../library/skill-repo-standards.md`](../library/skill-repo-standards.md)**.

---

## Related

- **[`../library/authoring-checklist.md`](../library/authoring-checklist.md)** — full checklist for **after** migration (or in parallel for deep refactors).
- **[`../library/skill-repo-standards.md`](../library/skill-repo-standards.md)** — index of conventions.
- **[agentic-skill-builder README](../../../agentic-skill-builder/README.md)** — strategize / delivery graph (for `conf/build-strategy.json`).
