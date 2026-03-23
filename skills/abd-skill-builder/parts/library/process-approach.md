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

### Library shards with phase markers (`abd:begin` / `abd:end`)

A **`library/*.md`** file may wrap fragments in **`<!-- abd:begin <phase-slug> -->`** … **`<!-- abd:end <phase-slug> -->`** (same slug on both lines). When **`Instructions.assemble_prompt(<phase-slug>)`** runs (used by **`generate_prompt.py`** and **`build.py`** for **`phases/built/<slug>.md`**), the reader sees **all lines outside** those pairs **plus** only the **pair whose slug matches** the current phase. Slugs match **`phase_files`** in **`skill-config.json`** (e.g. **`plan-script-build`**). Files **without** markers are included in full whenever **`PHASE_LIBRARY_SLICES`** lists them for that phase. Authoring template: **`templates/concepts.md.template`**.

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

