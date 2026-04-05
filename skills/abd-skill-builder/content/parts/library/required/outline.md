## Introduction
This skill builds other skills with the layout and capability outlined below; including merge pipeline, checklists, rules, and scripts. Links point at **this** repo’s `[content/parts/](../content/parts/)`, [`skill-config.json`](../skill-config.json), `[scripts/](../scripts/)`, etc., as concrete examples.

---

## Capability Summary
Skills built with the skill builderwill be able to solve the following problems with the following caabilities.

```
skill-root
Entry point — agent discovery (SKILL.md) and assembled agent instructions (AGENTS.md)
│
│   working in the wrong area; reads and writes wrong files.
├── ┌─────────────────────────────────────────────────────┐
│   │  skill-config.json → workspace                      │
│   │  Single manifest: routing + merge + build           │
│   └─────────────────────────────────────────────────────┘
│
│   guidance gets lost for multi step, more complex skills
├── ┌─────────────────────────────────────────────────────┐
│   │  Phases and process files                           │
│   │  process.md + phases/<phase>.md;                    │
│   └─────────────────────────────────────────────────────┘
│
│   losing track of progress, steps skipped, wrong order
├── ┌─────────────────────────────────────────────────────┐
│   │  Activity checklists                                │
│   │  Pipeline + per-phase checklist pieces              │
│   └─────────────────────────────────────────────────────┘
│
│   to many concepts creates confusion, for one file to contain
├── ┌─────────────────────────────────────────────────────┐
│   │  Build from parts                                   │
│   │  Library, phases, rules → assemble AGENTS.md        │
│   └─────────────────────────────────────────────────────┘
│
│   instructions are missed, guidance ignored
├── ┌─────────────────────────────────────────────────────┐
│   │  Phase-scoped prompts                               │
│   │  generate.py — one phase bundle per session         │
│   └─────────────────────────────────────────────────────┘
│
│   stubbornly makes the same mistakes despite the best prompting
├── ┌─────────────────────────────────────────────────────┐
│   │  Rules and scanners                                 │
│   │  Normative prose plus machine-checkable gates       │
│   └─────────────────────────────────────────────────────┘
│
│   AI output structure varies every run; downstream cannot rely on layout.
├── ┌─────────────────────────────────────────────────────┐
│   │  Templates                                          │
│   │  Structure format of all output                     │
│   └─────────────────────────────────────────────────────┘
│
│   Skill or scanner changes break behaviour without automated proof.
└── ┌─────────────────────────────────────────────────────┐
    │  Tests│
    │  Fixtures, and automated test suites for scripts    │
    └─────────────────────────────────────────────────────┘
```

---

## Capability Description

Sections follow the **How to read this** order above. Unless stated otherwise, “the skill” means **the skill built by the skill builder** (the repo that contains `**SKILL.md`**, `**content/parts/`**, `**scripts/base/build.py**`, etc.), not the skill-builder itself. Headings name the capability; paths link to this repo’s trees (**[content/parts/](../content/parts/)**, **[skill-config.json](../skill-config.json)**, **[scripts/](../scripts/)**, …) as working examples.

### Workspace and configuration

**Problem — Wrong tree**
A **skill** reads or writes the wrong project, or paths are ambiguous between **that skill’s install directory** and the **workspace tree** where engagement work should live.

**Solution**
In **each skill**, store `**active_skill_workspace`** (and optional `**known_skill_workspaces`**, `**context_paths**`) under `**skill-config.json**` → `**workspace**`. Phases, library slices, `**build_strategy**`, and **`build`** (compile paths, pipeline, scanners) live in the **same** file. Use `**scripts/base/set_workspace.py`** to print or set the pointer. Example in this repo: `[skill-config.json](../skill-config.json)`.

**What “workspace” means here** — That pointer chooses the **project root** for everything the skill produces or updates **outside** its own package: plans, pipeline checklists, generated docs, deliverables, and other engagement artifacts. Those paths resolve under **that** tree, not under the skill install (where `**SKILL.md`**, `**scripts/`**, and `**content/**` live). The pointer tells every script and instruction **which** tree is live.

```
        Skill package (install)                   Workspace (project tree)
        read/write: the skill’s own files         read/write: engagement artifacts
┌─────────────────────────────────────┐     ┌─────────────────────────────────────┐
│ Installed package — SKILL.md,       │     │ Project tree — plans, pipeline      │
│ scripts/, content/, rules/, tests…  │ ──► │ checklists, generated docs,         │
│                                     │     │ deliverables, runtime state, etc.   │
└─────────────────────────────────────┘     └─────────────────────────────────────┘
                      skill-config.json → workspace.active_skill_workspace
```

---

### Phases and process Files

**Problem — No map through the workflow**
It is unclear what happens in what order; people cannot jump to the right detail.

**Solution — File structure and links** (in **each skill**)

- `**content/parts/process.md`** — Defines the **ordered pipeline** and a **table of contents** with **one row per phase**. Each row links to the matching `**content/parts/phases/<phase>.md`** and declares **who runs that phase**: **AI** (work driven in the model/chat) or **code** (scripts, build steps, or other automation carrying the task)—so the kind of execution is visible **to the AI chat**.
- `**content/parts/phases/<phase>.md`** — One file per phase: inputs, outputs, procedure. Link out to `**content/parts/library/`** for norms and long-form detail where needed.

**Reference files (same layout as a typical skill)** — `[content/parts/process.md](../content/parts/process.md)`, `[content/parts/phases/](../content/parts/phases/)`, `[content/parts/library/](../content/parts/library/)`.

```
┌─────────────┐   defines   ┌────────────────────────────────────┐
│ process.md  │ ──────────► │  Phase 1 → Phase 2 → Phase 3 → …   │
└─────────────┘             └────────────────────────────────────┘
                                      │ each phase
                                      ▼
                              ┌──────────────────────┐
                              │  phases/<phase>.md   │
                              │  I/O, procedure,     │
                              │  TOC: AI vs code     │
                              └──────────────────────┘
```

---

### Activity Checklists

**Problem — No shared place to track “where we are”**
Workflow position and steps are easy to lose across or even during sessions.

**Solution — maps in the skill package; live checklists in the workspace**

**Each skill** using this layout defines the pipeline **in the install**, and tracks **checked** progress **under `active_skill_workspace`** — not by adding a `**library/process-checklist.md**` file to the repo (scaffold **does not** ship that path).

1. **Overall workflow (which phase are we in?)** — `**content/parts/process.md`** defines phase order; `**skill-config.json` → `phase_files`** lists the slugs that drive generation. The **live** pipeline checklist is **`process-checklist.md`**, **created** under `**<active_skill_workspace>/<skill_name>/progress/`** on first `**python scripts/base/generate.py --phase <slug>`** (when that file is missing). It has one row per phase (`**- [ ]` / `- [x]`**). Normative explanation of how these files are created: **`content/parts/library/base/checklist.md`** in **abd-skill-builder** (this repo).

2. **Per-phase steps (what to do inside this phase)** — Each `**content/parts/phases/<phase>.md`** may define **`## Action Checklist`** with `**- [ ]` / `- [x]`** steps. The **live** copy for tracking is **`<phase-slug>-checklist.md`** in the same **`progress/`** folder (generated from that section; not a file under **`library/`**). **Resume** = first unchecked step in the workspace copy.

**Stable reference:** **`content/parts/library/base/checklist.md`** (same in every scaffolded skill; see **[How checklists are created](base/checklist.md)**) documents **how** pipeline and phase checklists work. That is separate from the **workspace `progress/`** live checklists above.

```
  SKILL REPO (install — no ticked pipeline file in library/)     WORKSPACE (live — generated)
  content/parts/                                               <active_skill_workspace>/

  ┌─ Map: which phase exists, in what order ─┐   ┌─ Pipeline position (generated file) ─────┐
  │ process.md  →  TOC / links               │   │ progress/process-checklist.md           │
  │ skill-config → phase_files (slugs)       │   │ - [x] workspace-and-config                │
  │                                          │   │ - [ ] plan-script-build  ← you are here │
  │ (no library/process-checklist.md template)│   │ - [ ] …                                   │
  └──────────────────────────────────────────┘   └───────────────────────────────────────────┘

  ┌─ Per phase: ## Action Checklist in phase file ─┐   ┌─ Steps for current phase (generated) ─┐
  │ phases/shape.md                                │   │ progress/shape-checklist.md           │
  │ ## Action Checklist                            │   │ - [x] step one                        │
  │ - [ ] step one                                 │   │ - [ ] step two  (first unchecked = …) │
  └────────────────────────────────────────────────┘   └───────────────────────────────────────┘
         ▲                                                        ▲
         │  generate.py + workspace_checklists.py create missing │
         │  files under progress/; do not tick the repo copies   │
         └────────────────────────────────────────────────────────┘
```

---

### Build from parts

**Problem — Monolithic instructions**
A single giant instruction file is hard to maintain, impossible to version by topic, and the model loses focus.

**Solution — Merge parts into the full bundle**
Authors maintain skill content under `**content/parts/`** (**process.md**, **library/**, **phases/**) and `**rules/`**. Parts are assembled into a Agent.MD file.

The individual **phase instructions files** from `**phases/<phase>.md`** are merged with  **pieces the phase needs** from `**library/`** and  `**rules/`**. 

`**skill-config.json**` tells `**build.py**`  what phases use what library parts and what rules. The result is **per-phase built files**  under `content/parts/phases/built/`.

**Full bundle** — Everything rolls up into `**AGENTS.md`** at the repo root (the agent’s single merged view). 

Reference: `[scripts/base/build.py](../scripts/base/build.py)`, `[skill-config.json](../skill-config.json)`, `[scripts/base/generate.py](../scripts/base/generate.py)`, `[scripts/base/set_workspace.py](../scripts/base/set_workspace.py)`.

```
  content/parts/                    rules/
      process.md                        *.md  ──┐
      library/  (shared norms, shards)          ├──►  phases/built/<phase>.md
      phases/<phase>.md  (phase body)      ─────┘     (phase =phase + library + rules)
                                                         │
                                                         ▼
  build.py  ──────────────────────────────────────►  AGENTS.md
```

---

### Rules and scanners

**Problem — Silent violations**
Output looks correct but breaks structure or naming. Manual review is slow; without machine-checkable checks, standards drift.

**Solution**
In **each skill**, `**rules/*.md`** holds normative prose the model follows; `**rules/scanners.json`** binds optional **scanner** scripts to rules. `**build.py`** runs `**build.build_pipeline`**; `**build.scanners**` aligns local runs with CI the same way. Example tree: `**[rules/](../rules/)**` in this repo.

```
┌──────────────┐   read at prompt time   ┌──────────────────┐
│  rules/*.md  │ ─────────────────────►  │  AI follows      │
│  (prose)     │                         │  rule text       │
└──────────────┘                         └──────────────────┘

┌──────────────┐   run after merge       ┌──────────────────┐
│ scanners.json│ ─────────────────────►  │  Automated check │
│  (bindings)  │                         │  flags violation │
└──────────────┘                         └──────────────────┘
```

---

### Correction approach

The feedback loop after **rules** (and scanners) when something still slips through.

**Problem — Problems that slip through**
Something is wrong in the output — missed constraint, ambiguous prompt, or no rule/scanner would have caught it. Without a record, the same issues recur.

**Solution**
Log what failed, whether a rule or scanner should have applied (or none exists yet), and the proposed fix. Feed that into an **improvement backlog**: new or updated rules, scanners, or prompts.

```
┌──────────────────────┐     user spots problem     ┌─────────────────────────┐
│  AI output           │ ─────────────────────────► │  Problem log entry      │
│  (has a mistake)     │                            │  - what went wrong      │
└──────────────────────┘                            │  - rule/scanner missed? │
                                                    │  - suggested fix        │
                                                    └────────────┬────────────┘
                                                                 ▼
                                                    ┌─────────────────────────┐
                                                    │  Improvement backlog    │
                                                    └─────────────────────────┘
```

---

### Instruction Generation & Injection

**Problem — Command drift / wrong focus**
Dumping the **entire skill instruction bundle** into one prompt causes drift; the model invokes the wrong slice of the workflow or drops context.

**Solution**
In **each skill**, `**generate.py`** takes a **phase** and assembles **only** the bundle for that AI-chat session (from `**content/parts/phases/`**, `**library/`**, inlined rules per **skill-config**). The model gets what it needs for **that** phase, not the whole repo at once. See `[scripts/base/generate.py](../scripts/base/generate.py)` in this repo.

```
┌──────────┐     phase      ┌──────────────┐   assembled prompt   ┌──────────┐
│   User   │ ─────────────► │ generate.py  │ ────────────────────► │  AI Chat │
│  / Agent │                │              │                       │          │
└──────────┘                └──────────────┘                       └──────────┘
                                    │
                                    ▼
                        ┌──────────────────────┐
                        │  content/parts/       │
                        │  phases/  library/    │
                        └──────────────────────┘
```

---

### Templates

**Problem — Inconsistent output structure**
Without a fixed shape, the AI invents a format every time; downstream tools and humans cannot rely on layout.

**Solution**
**Each skill** may include `**templates/`** (or `**.template`** files) that define the structure the AI must fill in so artifact shape stays stable. Example: `[templates/](../templates/)` in this repo.

```
┌─────────────────────┐   structure contract   ┌──────────────────────┐
│  templates/…        │ ─────────────────────► │  AI fills output     │
│  (output shape)     │                        │  matching template   │
└─────────────────────┘                        └──────────────────────┘
```

---

### Tests

**Problem — Unverified changes**
Layout, merge output, or scanner behaviour in a **skill** can regress without automated proof.

**Solution**
`**test/`** holds fixtures, suites, and optional workspace snapshots under `**test/<workspace>/`**. Run them locally or in CI alongside `**build.compileall_paths`**, `**build.py**`, and `**build.scanners**`. Build from parts and Phase-scoped prompts (`**generate.py**`) are covered above; `**test/`** is **assertions on that skill’s own repo**.

```
┌──────────────────────────────────────┐   verifies   ┌─────────────────────────────┐
│  test/                               │ ───────────► │  Structure, merge output,   │
│  fixtures · pytest · snapshots       │              │  scanner behaviour          │
└──────────────────────────────────────┘              └─────────────────────────────┘
```

---

