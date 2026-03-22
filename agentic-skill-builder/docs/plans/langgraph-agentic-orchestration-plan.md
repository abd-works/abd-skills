# LangGraph agentic orchestration — agentic-skill-builder plan

**Status:** planning document (implementation lives in `agentic-skill-builder/src/` when built).  
**Audience:** you (product/architecture) + implementers.  
**Not normative for:** `abd-maps-models-specs` — treat that skill’s `plan/` and `scripts/orchestrator_loop.py` as **prior experiments**, not requirements.

**Canonical project name and path:** `**agentic-skill-builder`** — folder `agilebydesign-skills/agentic-skill-builder/`. Older notes may say `skills-delivery`; **ignore that** — there is **one** plan file: `docs/plans/langgraph-agentic-orchestration-plan.md` in this folder.

### Execution status — Slack disabled for now

**Slack is deferred:** there is **no** access to configure a Slack app / **Incoming Webhook** at **api.slack.com** (no Incoming Webhook URL on **hooks.slack.com**). **Do not** block LangGraph scaffolding, **§7.1** trivial skill, Builder / Operator / Expert, or **§1.2** gates on Slack.


| Rule                   | Meaning                                                                                                                                                                          |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **HITL without Slack** | Human-in-the-loop uses **LangGraph interrupts**, **checkpoints**, and **IDE / CLI resume** only.                                                                                 |
| **Graph**              | `**notify_hitl_slack`** (§5.2) is **optional** — implement as **no-op** or omit until Slack is re-enabled.                                                                       |
| **Code**               | `slack_notify.py`, `scripts/notify_slack.py`, and `**conf/.secrets.example`** stay in the repo for when webhook access exists; they are **not** part of the critical path today. |
| **Resume work**        | Start and continue implementation per **§7–§8** and **§1.2**; treat Slack as **off** until this note is removed or replaced.                                                     |


---

## 1. Purpose

Deliver a **repeatable pipeline** that:

1. **Builds** new or updated skills **to the same structural and authoring standards** as existing skills in `agilebydesign-skills/skills/*` (reverse-engineered into explicit rules).
2. **Operates** those skills as **structural tests** (syntax, runnable scripts, file layout, rule presence) — **not** outcome quality.
3. **Critiques** artifacts with **domain expertise** (principles, form, fitness to story) using **your** bodies of knowledge + **idealized references / rubrics**.
4. **Deploys** (optional) via git: branches, tags, parallel experiments, rollback story.

Orchestration is implemented with **LangGraph** (LangChain ecosystem) so we get **state**, **checkpoints**, **human-in-the-loop**, and **conditional routing** without ad-hoc shell loops.

### 1.1 Research-backed rationale: who may hold the “gold,” and why the Builder must not

**Verdict:** Reserving a **full reference artifact** (what “good” actually looks like) for the **orchestrator / Expert / human** — while the **Builder** only receives **principle-shaped, transferable** feedback — is **aligned with established patterns** in ML systems design, interactive learning, and template-based generation. It is **not** merely preference: several fields independently converged on **separating the evaluator’s privileged view from the generator’s training signal** to preserve **generalization** and avoid **demonstration bias**.

**Caveat:** Separation is necessary but not sufficient. RLHF-style pipelines document **reward–policy mismatch**, **reward hacking**, and **overoptimization** when the critic and actor drift apart; our mitigations are **structural Operator checks**, **rubric-grounded public critique**, **iteration caps**, and **HITL** when the critic’s signal is noisy.


| External pattern                                                                                                                             | What it says                                                                                                                                                                                                                      | How this plan maps it                                                                                                                                                                                      |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Actor–critic / decoupled representations**                                                                                                 | Policy (actor) and value/reward side (critic) **specialize**; shared weights can hurt **generalization**; critic explores different information than the actor.                                                                   | **Builder** ≈ actor: emits artifacts from **standards + brief**. **Expert** ≈ critic: scores against corpus + rubric + **private** gold **without** rewriting the Builder’s weights to memorize that gold. |
| **RLHF: reward model vs policy**                                                                                                             | Human preferences are distilled into a **reward model**; the policy optimizes **reward**, not **paste of human completions**. Leakage of “the answer” into the policy target causes **overfitting** to style of the labeling era. | **Private** channel holds the analog of **preference data / gold completion**; it **must not** become the Builder’s **few-shot exemplar of content** for every future skill.                               |
| **Self-Refine** (Madaan et al., NeurIPS 2023)                                                                                                | Iterative **FEEDBACK → REFINE** loops; feedback is **actionable** and **task-dependent** without requiring **gold answer disclosure** to the refiner.                                                                             | **Public** critique is the safe analog: “tighten structure here,” not “replace with paragraph 3 of the secret doc.”                                                                                        |
| **Interactive in-context learning from NL feedback** (e.g. *Improving Interactive In-Context Learning from Natural Language Feedback*, 2026) | **Teacher** with **privileged ground truth** gives **natural language feedback** to a **student** **without revealing the final answer**; **information asymmetry** is used for **didactic** improvement.                         | **Orchestrator / Expert** = teacher; **Builder** = student; **private** = ground truth + gap analysis **kept out of Builder context**.                                                                     |
| **Constitutional AI / critique–revise**                                                                                                      | Improvement driven by **principles** (“constitution”) and **critique–revise** loops, not by **one** labeled answer per task.                                                                                                      | **Public** feedback aligns with **principles + form**; **gold** is **not** the constitution.                                                                                                               |
| **Demonstration bias / overfitting to one scenario**                                                                                         | Agents and templates **overfit** to the **visible test case** or **single vendor template**, breaking **other** cases; **one-template-per-product** does not scale.                                                               | If the Builder is **prompted or tuned** toward **one** RFP response product, the **next** RFP skill **will** break; **gold** stays in **evaluation**, not in **scaffold DNA**.                             |


**Worked example — “proposal response” skill**

1. **Intent:** You want **agentic-skill-builder** to produce a **high-quality** skill for **RFP / proposal response** (memory, RAG, voice, workflow steps).
2. **You possess:** A **final** proposal response (and mental model of what “done” means) — the **gold**.
3. **Correct division of labor:**
  - **Orchestrator + Expert (and you):** Compare **built skill behavior** and **sample outputs** against the gold **off the Builder path** — e.g. HITL review, private scoring, gap notes (“missed executive summary hook,” “wrong evidence ladder”). Only here is **full** comparison to the gold legitimate.  
  - **Builder:** Consumes **only** **public** remediation — **repository standards**, **step structure**, **rule naming**, **process clarity**, **domain-neutral** coherence (“this skill doesn’t define a repeatable evidence→draft→review loop”).
4. **Why the Builder must not “know” the final product:** If the Builder **optimizes** toward **one** gold response (even implicitly via **few-shot** or **hidden** exemplar in prompts), the **scaffold** becomes **a forked template for that product**; the **next** proposal domain will **not** fit. **Only** the orchestration layer should **hold** “this is what winning looked like **for this** run” so you can **diagnose** from **first principles** and **without** poisoning the **general** builder.
5. **Optional nuance:** A **small** amount of **abstract** pattern (“responses must include a compliance matrix”) is **public**; **the actual matrix from your gold bid** is **private**.

**“Gentle” workflow (best practices in this family)**

- **Iterative refinement** with **bounded iterations** (not unbounded adversarial loops).  
- **Human-in-the-loop** at **interrupt** points (LangGraph pattern) — **review** before **deploy**, not **punishment**.  
- **Rubric-first** public feedback so the Builder **does** receive **signal** without **secret** **content**.  
- **Monitor** for **reward hacking** analogs: **Operator** passes while **Expert** fails → **do not** auto-ship; **escalate** to human.

### 1.2 Step-by-step execution with human gates (how we build *this* project)

**Until the scaffold is accepted, nothing runs “hands off.”** Implementation of **agentic-skill-builder** follows a **strict cadence**: **one thin slice at a time → stop → you review → either proceed, revise this plan, or redo the step** — repeat until the scaffold is real and you **explicitly** release the next phase to run without you.


| Rule                    | Meaning                                                                                                                                                                                                                                                                                                                                                         |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **One step, one stop**  | Each **increment** (e.g. “state object only”, “operator on fixture”, “builder stub”) ends in a **mandatory pause**: **human reviews** output + diff + behavior. **No** chaining “while we’re here” work into the same session without approval.                                                                                                                 |
| **Plan is live**        | If a step reveals a wrong assumption, **edit `langgraph-agentic-orchestration-plan.md`** (or tickets) **before** continuing. Retrying the **same** step with a **fixed** plan is normal; bulldozing forward is not.                                                                                                                                             |
| **Redo is allowed**     | A failed or rejected step **does not** advance the roadmap number — **redo** until the gate passes or the plan changes.                                                                                                                                                                                                                                         |
| **Autopilot is opt-in** | Longer **autonomous** runs (e.g. multi-iteration builder loops, unattended Expert passes) are **off** until you **sign off** that the **scaffold** is in place — i.e. you are satisfied that **Builder + Operator + Expert** behave on the **§7.1 trivial skill** and the **graph** matches what you want. Document that handoff in a ticket or commit message. |
| **LangGraph mapping**   | During bootstrap, configure `**interrupt_before`** (or equivalent) on **every** automated node so **no** node advances without resumption after review; relax only after opt-in (see §5.2 note).                                                                                                                                                                |


**Relationship to §7–§8:** Phases **7.1 / 8** are **product** milestones; **§1.2** is **process discipline** for **all** engineering work leading to them — including edits to this document.

### 1.3 Early runs: standards, critique, orchestration, and “dimensions of improvement”

The **first several** build–critique cycles should **assume** human review — not because the implementation is lazy, but because **repository standards** (what “good” scaffolding is) and **Expert critique** (rubric, retrieval, public/private split) **will not** land correctly on the **first** try. Plan for **iteration**, not **one-shot** correctness.


| Expectation                                   | Why                                                                                                                                                                                                                                                                                                                                                                                                               |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Standards take calibration**                | Encoded rules and templates are **hypotheses** until a human **confirms** they match how `skills/*` really work. Early **Builder** outputs are **fodder for review**, not final truth.                                                                                                                                                                                                                            |
| **Critique takes calibration**                | The **first** Expert pass on a real artifact is a **test of the critic** as much as of the skill: prompts, corpus slices, and scoring need **your** feedback. **Stop after the first critique** (and after the first **Operator** run on a new path) — **no** unattended second pass until you’ve reacted.                                                                                                        |
| **Orchestration is feedback, not only files** | Review is **not** limited to “this file is wrong.” Expect to comment on **how** work is split in **agentic-skill-builder** (LangGraph): **subgraphs**, **order of nodes**, **which agent owns which concern**, and **handoffs** between Builder, Operator, and Expert. **Skill repos** stay **linear** (§3); graph shape lives here. That feedback **updates this plan** and graph config, not only prompt text.  |
| **Manual runs before patterns**               | After **several** **manual** end-to-end runs (build → test → critique → review), you should not only have a **list of fixes** but a sense of **dimensions of improvement** — recurring axes of quality (e.g. “traceability of steps,” “critic overweights form vs principles,” “Operator too loose on X”). Those **dimensions** become **explicit** rubric rows, roadmap priorities, or Expert lens weights (§6). |


**Outcome:** Early HITL is **load-bearing**. Later, **autopilot** (§1.2) means “we’ve **compressed** repeated human judgment into **dimensions** and **gates** we trust” — not “we stopped caring.”

---

## 2. External best practices (LangGraph / agentic orchestration)

These are the patterns we intend to follow; pin library versions when coding starts.


| Practice                                            | Why it matters here                                                                                                                                                                                                                  |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Explicit graph state (Pydantic)**                 | Carries skill target path, build artifacts, operator logs, critic scores, deploy metadata, and **HITL** flags in one reducible structure.                                                                                            |
| **Checkpointers — default: SQLite**                 | **SqliteSaver** (file-backed, no server) for durable checkpoints; `**MemorySaver`** for quick runs/tests. **Postgres** only if we later need a shared DB across multiple app instances. Long runs can resume; supports review gates. |
| `**interrupt_before` / `interrupt_after` on nodes** | Human approval between “builder produced tree” and “operator runs”, or after critic before deploy. **Bootstrap:** interrupt **before every node** until human releases “autopilot” (§1.2).                                           |
| **Reducer fields for append-only logs**             | In the **orchestrator** graph, append-only fields avoid races if multiple branches write logs (skills themselves stay linear — §3 intro).                                                                                            |
| **Subgraphs**                                       | **Orchestrator only** — e.g. isolate “deployer” for dry-run. **Not** a pattern for complexity inside a single skill package.                                                                                                         |
| **Supervisor / router pattern**                     | A thin **orchestrator** node decides next step from state (re-plan, rebuild, re-run tests, request expert pass, abort).                                                                                                              |
| **Tool boundaries**                                 | Builder/operator call **filesystem + subprocess + JSON validators** as tools; LLM nodes only where judgment is required.                                                                                                             |
| **Separation of “verifier” vs “judge”**             | Structural checks = deterministic or lint-like; **expert critique** = LLM + rubric + retrieved corpora — mirrors your **Operator ≠ Expert** distinction.                                                                             |


**Cross-reference:** Critique–refine **roles**, **gold** placement, and **generalization** risks are grounded in **§1.1** (research-aligned); this section is **tooling** only.

**References (official / ecosystem):** LangGraph “Persistence”, “Human-in-the-loop”, “Subgraphs”, “StateGraph”; LangChain “structured output” for critic JSON when needed.

---

## 3. Reverse-engineered skill standards (what the Builder must know)

The following is distilled from recurring patterns across `abd-context-to-memory`, `abd-solution-modeler`, `abd-story-synthesizer`, `abd-maps-models-specs`, `abd-skill-builder`, etc. The **Builder** must encode **generic** rules (apply to any skill) as **machine-checkable** checks + **templates**; **family-specific** patterns (e.g. maps-models **domain + story-map** split) are **optional** and documented separately below — not every skill looks like `abd-maps-models-specs`.

**Scope boundary — skills stay simple:** A **skill package** should express a **linear** pipeline: **stage → phase → (steps inside phase docs)**. The **process table** rows are **phases**, not steps. It should **not** embed **parallel branches**, **multi-agent fan-out**, or **LangGraph-style routing** inside the skill repo. If work needs that complexity, it belongs in **agentic-skill-builder** orchestration (or we split/reshape skills). **Changing** that rule means **changing how we author skills**, so we keep skills deliberately small and sequential.

### 3.1 Directory and content conventions

**Hierarchy in the repo:** **Stages** group **phases**. Each **phase** has normative markdown (one file or section per phase, per skill); **steps** live **inside** that phase’s markdown — they are **not** separate rows in the master process table. See **Stages, phases, and steps** below.


| Area                            | Convention                                                                                            | Notes                                                                                                                                                                                                                                                                                                                             |
| ------------------------------- | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Normative content**           | Under `content/parts/` (or skill-specific `parts/` parallel to `content/`)                            | Plans, operations, domain narrative — **not** dumped only in chat.                                                                                                                                                                                                                                                                |
| **Phase markdown (source)**     | e.g. `content/parts/phases/<name>.md`, or one doc per stage with phase sections — paths vary by skill | **One row in the process table = one phase.** **Steps** (numbered sub-procedures, “Step 1…”, checklists) are written **inside** this markdown as **normative content of the phase**, not as their own table rows.                                                                                                                 |
| **Built phase markdown**        | `content/parts/steps/built/` and/or `**content/built/`** (generated)                                  | **Generated** from source phase bodies + rules via `scripts/build.py` (or `build_agents.py`). **Steps baked inside** the built file(s). **Agents read `built/`**; authors do not hand-edit `built/`. Folder name (`steps/built` vs `content/built`) is a skill convention; meaning is always **built normative text for phases**. |
| **Atomic rules**                | `content/parts/rules/*.md` (or top-level `rules/` in simpler skills)                                  | One concern per file where possible; **names** should encode **phase** and/or **domain concept** + rule name (see §3.2).                                                                                                                                                                                                          |
| **Roles**                       | `roles/*-role.md`                                                                                     | One file per **user/agent role** the skill assumes.                                                                                                                                                                                                                                                                               |
| **Process**                     | `content/parts/process.md` or staged process docs                                                     | **Summary table: each row is a phase** (linked by **Ref** to phase markdown). Stages group those rows. **Steps** appear only **inside** the linked phase files.                                                                                                                                                                   |
| **Repo-facing built artifacts** | `AGENTS.md`, `SKILL.md`, sometimes `README.md`                                                        | Frequently produced by `**scripts/build.py`** delegating to shared **ace-shaping** / **engine** (`build_skill(skill_dir, ...)`) or skill-local merge order.                                                                                                                                                                       |
| **Config**                      | `skill-config.json`                                                                                   | Name, version, paths — skill-specific knobs.                                                                                                                                                                                                                                                                                      |
| **Scripts**                     | `scripts/`                                                                                            | Operational entry points; may share `_config.py` patterns.                                                                                                                                                                                                                                                                        |


#### Stages, phases, and steps (how they relate)

**Order is always:** **Stage → Phase → Step** (coarse → mid → finest) — but **only the first two appear as rows** in the master process table. **Steps** are **inside** the phase markdown.


| Term      | Typical meaning                                                                                                                                                                                                                                                                                                                      | Example                                                                                  |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **Stage** | **Coarse pipeline slice** — groups many **phases**; may span days or sessions. Often a heading or section in `process.md` or a staged doc.                                                                                                                                                                                           | **Stage 1 — Extract Context**; **Stage 2 — Map and Model**; **Stage 3 — Specification**. |
| **Phase** | **One row** in the process summary table — the unit of “what we do next” with a **driver**: **human** or **AI actor**. The **Ref** column links to **phase** markdown. Phases answer “are we allowed to proceed?” and **contain** the detailed steps as normative body copy.                                                         | “Corpus audit — Phase 0”; **Initiator / Actor** column = human vs AI.                    |
| **Step**  | **Sub-structure inside the phase’s markdown** — numbered instructions, checklists, “Step 1 / Step 2”, optional **suffix letters** (`5a`, `7a`) for companion script runs **within the same phase**. **Not** a row in the process table. Machine state (if any) may still reference `workflow_step` as a **sub-id** inside the phase. | Inside `modules-epics-scaffold-breadth.md`: “1. … 2. … 3a. rebuild index …”              |


**AI-driven phases — how the operation is delivered:** The AI does **not** invent parallel workflows inside the skill. For an **AI actor** **phase**, the operation is conducted by either **(a)** loading a **generated markdown** file for that phase (typically under `**content/parts/steps/built/`** or `**content/built/`** — see directory table) and using it (including **steps embedded inside**) as the instruction body, or **(b)** **assembling** the prompt **dynamically** from **sections** (manifest / `skill-config`) and **injecting that assembled text into chat** for the model to follow. **Human-driven** phases use the same layout; the **human** is the driver (review, edit, trigger script).

**Ordering (linear, inside the skill):** Stages order **major outcomes**. **Phases** run in **process table order** (each row = one phase). **Steps** follow the order **written inside** each phase document. **Parallel batches, fan-out, or merge** are **not** modeled as extra table rows; if needed, implement in **agentic-skill-builder** orchestration (see scope boundary above). **Phases** may **block** a later stage until accepted (e.g. “Phase 0 says rebuild chunks — do not start Stage 2 until accepted”).

**“Process” one-liner:** `content/parts/process.md` (or `parts/process.md`) often opens with a **single pipeline string** (e.g. Context → Foundational spine → …). That line is the **navigation spine**; the **table lists phases** (by stage); **authoritative step detail** lives inside each **Ref**’d phase file.

#### Process tables, hyperlinks, and naming in the Ref column

**How the table is built**

- **Rows are phases**, not steps. Columns typically include: `**#`**, **Phase** (title — sometimes labeled “Step” in legacy tables; **semantically it is the phase**), **Initiator / Actor** (Human→Code, AI, Code), **Script** (if any), **What it does**, **Coverage**, **Ref**, **Inputs**, **Outputs**.
- **Ref** is the **hyperlink hub**: each row points to the **normative markdown for that phase**. **Steps** (numbered sub-procedures) live **inside** that file — not in separate table rows. Python entry points stay in **Script**, not **Ref**.
- **Two-tier phase files:**
  - **Source:** phase markdown authors edit (e.g. `content/parts/phases/<name>.md`, or `parts/steps/<name>.md` when the filename is the **phase** slug — naming varies by skill).
  - **Built:** `content/parts/steps/built/<name>.md` or `content/built/<name>.md` — **rules baked in** from `parts/rules/*.md` via `scripts/build.py` (or `build_agents.py`). **Steps remain inside** the built document. **Agents read `built/`**; they do not hand-edit `built/`.
- **Cross-links inside the table:** The **Ref** column uses relative markdown links to the **phase** doc, e.g. `[context](parts/context.md)`, `[modules-epics-scaffold-breadth (built)](content/parts/steps/built/modules-epics-scaffold-breadth.md)` (paths vary by skill; **from the skill root** per `AGENTS.md`).

**Naming conventions visible in the table**

- **Phase titles** in the table read like **milestones or operations** (“Parse, curate, chunk, index”, “Integrate and Harmonize”) — stable labels for `**phase`** / workflow fields. **Finer labels** for **steps inside the phase file** may appear in JSON as `workflow_step` or similar.
- **Letter suffixes** (`5a`, `7a`) describe **sub-steps inside a phase** (e.g. companion script after a numbered step) — **inside the phase markdown**, not extra table rows.

#### Concepts and cross-cutting artifacts (generic — all skills)

**This section is the generic rule.** A **skill** packages **concepts** (ideas, definitions, invariants, roles) and **artifacts** (outputs, schemas, manifests) that the workflow references across **multiple stages or phases**. Anything that would be **repeated** if pasted into every phase file should instead live in **its own file** (usually markdown under `content/parts/`, sometimes JSON alongside) so there is a **single source of truth**.


| Guideline           | Meaning                                                                                                                                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **When to extract** | If a concept or artifact **spans** more than one phase (or stage), give it a **dedicated** doc (or structured file) and **link** from phase bodies — do not duplicate long definitions in each phase.         |
| **Naming**          | Conventional filenames (`glossary.md`, `concepts.md`, `artifacts.md`, `roles/`*, etc.) vary by skill; the Builder should **discover** and **validate** presence from templates, not assume one global layout. |
| **Not every skill** | A minimal skill might only have `SKILL.md`, `content/parts/process.md`, and phase files — **no** separate “domain” or “story map” layer. That is valid.                                                       |


**Meta (out of scope for §3):** **agentic-skill-builder** may be **developed** using story maps, domain docs, and the same rigor as any other project — that work lives in **this repo’s** planning and story artifacts, **not** as a requirement that every skill under `skills/`* mirror `abd-maps-models-specs`.

#### Optional pattern — domain narrative + interaction tree (maps-models–class skills only)

Some skills (notably `**abd-maps-models-specs`** and similar) **choose** to separate **two parallel artifacts** that must stay in sync. **Do not** treat this table as the default for **all** skills — only for skills that explicitly adopt this shape.


| Piece                            | Role                                                                                                                                                                                                    | Typical location (example skill)                                                                              |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Domain narrative**             | **State and structure** — modules, **domain concepts** (CRC-style: owns, properties, operations, `extends`, invariants), evidence hooks. Answers **what things are** and **what owns which rules**.     | e.g. `parts/domain.md` + evolving `map-model-spec.json` (`modules_and_epics`, `concepts[]`, chunk citations). |
| **Story map / interaction tree** | **Behavior** — epics, sub-epics, stories, scenarios; **Trigger / Response**; **Pre-Condition**; **Given/When/Then** where required. Answers **who does what** and how behavior references domain state. | e.g. `parts/story-map.md` + nested JSON under epics (`stories`, `sub_epics`, etc.).                           |


**When this pattern applies**

- **Same vocabulary:** Domain concept names (`concepts[].name`) and story references can be held to **one namespace** — scanners may enforce **exact string match** where the skill defines that rule.
- **Evidence ladder / paired edits:** Concepts may carry `evidence_stage`; **domain** vs **journey** edits are **paired** in skills that implement both files.
- Skills **without** this split still use the **generic** rule above: cross-cutting concepts → **their own** markdown (whatever the skill calls them), not repeated per phase.

### 3.2 Rule file naming (heuristic standard)

Target pattern (flexible regex for validation):

```text
{phase-or-stage}__{domain-concept-or-scope}__{short-rule-name}.md
```

Examples mirror **story synchronizer / maps-models** style: scanners and rules tied to **phase** and **concept** (e.g. `chunks_must_be_referenced`, `concept-layering-scaffold`). The Builder should **propose** names from the **phase** + concept + verb (and step text inside the phase doc if needed), then **check uniqueness** under `parts/rules/`.

### 3.3 Assembly model (static vs dynamic)

**Per skill:** Each skill ships its own `**scripts/build.py`** (or equivalent entry point). The generic Builder does **not** replace that script; it **generates or validates** skill content according to the skill’s template, including how assembly works.

**Flag on `build.py`:** The skill’s `build.py` should expose an explicit **CLI flag** (or subcommand) to select assembly mode — e.g. `--assembly static|dynamic`, `--snapshot`, `--interactive`, or two clear options documented in the skill’s `README` / `AGENTS.md`. Exact names are per skill; the **requirement** is: **one reproducible path** (static snapshot) and **one session-oriented path** (dynamic) are **not** ambiguously mixed without the operator choosing.


| Mode        | Mechanism                                                                               | When                                                               |
| ----------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Static**  | `build.py` merges **built-phase** fragments into `AGENTS.md` / `SKILL.md` (and related) | Release, reproducible snapshot; CI; “what ships”.                  |
| **Dynamic** | Runtime concatenation by **phase** / **operation** from `skill-config.json` + manifest  | Interactive agent sessions, partial rebuild, IDE-driven iteration. |


The Builder (orchestration) may output an **internal** manifest (JSON or YAML) for a **given builder run**, listing which fragments form which artifact for both modes; the skill’s `**build.py` reads** that manifest (or embedded config) when implementing **static** merges and documents how **dynamic** mode resolves fragments at runtime. That manifest is **process state for skill generation** (see §9.3) — **not** a public standard every skill must carry.

### 3.4 “Standards corpus” for the Builder

Implementation should maintain `**docs/reference/skill-repo-profile.md`** (future) generated from:

- `skills/abd-skill-builder` (scaffold + merge order),
- `skills/abd-context-to-memory` (RAG + long `AGENTS.md`),
- `skills/abd-story-synthesizer` / `abd-solution-modeler` (phased pipelines),
- `skills/abd-maps-models-specs` (rules + scanners + orchestration experiment).

This file becomes the **non-LLM** ground truth for Operator checks.

---

## 4. Agents: responsibilities, inputs, outputs

### 4.1 Builder


| Field        | Content                                                                                                                                                                       |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Goal**     | Emit a **skill directory tree** + **manifest** that conforms to §3.                                                                                                           |
| **Inputs**   | Skill name, domain brief, chosen template (maps-model vs memory vs synthesizer-shaped), optional existing repo path to extend.                                                |
| **Outputs**  | File tree; `skill-config.json`; rule stubs; `parts/steps/*.md`; `roles/*.md`; runnable `build.py`; optional scanner stubs.                                                    |
| **Does not** | Prove semantic correctness of domain content; does not guarantee “good OO” or “good stories”; does **not** receive **private** critique or hidden-solution priors (see §4.3). |


**Constraints:** Must follow **rule naming**, **folder placement**, and **assembly contract**. Should call **scaffold** patterns from `abd-skill-builder` where applicable instead of inventing layout. **Design stance:** the Builder is **standards-only** — it must not be authored or prompted so that “the right answer” is smuggled in via domain knowledge the scaffold layer should not hold.

### 4.2 Operator (tester / runner)


| Field       | Content                                                                                                                                                                                                                                        |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Goal**    | Answer: **Did we build a skill that runs and complies with repo standards?**                                                                                                                                                                   |
| **Checks**  | `python -m compileall` or equivalent; `build.py` dry-run; required globs present; JSON schema for `skill-config.json`; optional markdown frontmatter; run **existing scanners** if the skill has them; **no** evaluation of business outcomes. |
| **Outputs** | Structured report: pass/fail per check, logs, artifact hashes.                                                                                                                                                                                 |


**Constraints:** Treat **Builder rules** as ORDERS; treat **skill domain** as opaque except where the skill exposes **machine-readable** tests.

### 4.3 Expert critique (domain)


| Field                      | Content                                                                                                                                                                                                                   |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Goal**                   | Answer three orchestration questions (see §6) from a **principal’s** perspective: principles, form, outcome fitness.                                                                                                      |
| **Inputs (two mandatory)** | (1) **Body of knowledge** — curated corpus pointers (paths, skills, `abd_content`, `agile_bots/bots` rules). (2) **Idealized reference** — rubric paragraph, gold example artifact, or `docs/reference/`* style exemplar. |
| **Outputs**                | Scored dimensions + actionable edits + **citations** into the corpus where possible.                                                                                                                                      |


**Public vs private (this is the point, not “NDA wording”):**


| Channel     | What it is                                                                                                                                                                                                                                                                                                                                                                                     | What may flow **to the Builder**                                                                                                                                                                                                                                                  |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Public**  | Feedback that **any** principled reviewer could give **without** knowing your hidden target: you are **not** following stated principles; the artifact does not reach a **sound structural** outcome; the design does not hang together from a **domain-neutral** perspective (clarity, coupling, traceability, scaffolding, vocabulary discipline — **not** “it should have been class Foo”). | **Yes** — this is the legitimate loop fuel: actionable, standards-shaped, **non-leaking**.                                                                                                                                                                                        |
| **Private** | The reviewer’s knowledge of **what the solution is actually supposed to look like**, including blunt gap analysis (“we blew it relative to that bar”). You may **never** disclose the real solution to the system; you may sometimes tell the Builder **that** the run missed an outcome (“did not reach X”) **without** teaching it **what X is in domain terms**.                            | **No** — **must not** be merged into Builder prompts, manifest priors, or “fix it like this” hints that encode the answer. The **Builder is built to have no domain knowledge of the solution**: it only **scaffolds skills to repository standards**, not to a secret blueprint. |


**Constraints:** Expert may use LLM + retrieval. **Graph routing:** only **public** critique updates feed `**builder`** replan paths; **private** notes are for humans (and optional non-Builder channels), never for baking solution-shaped knowledge into the Builder.

### 4.4 Deployer


| Field       | Content                                                                                       |
| ----------- | --------------------------------------------------------------------------------------------- |
| **Goal**    | Git lifecycle: branch naming, tags, parallel experiment branches, merge, rollback procedures. |
| **Inputs**  | Operator pass + optional human approval + version bump policy.                                |
| **Outputs** | Commit metadata, tag, changelog snippet.                                                      |


**Constraints:** No deploy without **explicit gate** in graph (HITL or CI policy).

---

## 5. LangGraph shape (implementation sketch)

### 5.1 State (conceptual)

```text
SkillDeliveryState:
  skill_id, skill_path
  builder_manifest: dict | None
  operator_report: dict | None
  expert_report: dict | None
  deploy_result: dict | None
  iteration: int
  gates: { builder_review: bool, expert_review: bool, deploy: bool }
  trace: list[str]   # append-only
  hitl_reason: str | None        # why we stopped (human-readable; Slack body when §5.4 enabled)
  slack_notify_ts: str | None    # optional Slack message ts — only if Slack on (§5.4); else None
```

### 5.2 Nodes (first cut)

1. `**ingest_request**` — Normalize inputs; resolve corpus paths; fail fast if required HITL inputs missing (§7).
2. `**builder**` — Template expansion + file writes + manifest.
3. `**operator**` — Structural validation suite.
4. `**route_after_operator**` — If fail → loop to `builder` with diff **or** stop; if pass → `expert_critique` **or** skip if configured.
5. `**expert_critique`** — Retrieval-augmented LLM or script-assisted review using §4.3 inputs.
6. `**orchestrator_decide`** — Supervisor: continue, iterate, or request human (interrupt).
7. `**deployer`** — Git operations (optional subgraph).
8. `**notify_hitl_slack`** (optional **hook** on interrupt) — POST to Slack when HITL fires (**§5.4**); **deferred / no-op** while Slack is off (see **Execution status — Slack** above). **Not** a substitute for `interrupt`, only a **ping** when enabled.

**Graph-level:** `**SqliteSaver`** (path under e.g. `log/` or project config) for normal work; `**MemorySaver`** when ephemeral state is enough; `interrupt_before` on `deployer` and optionally after `builder`.

**Bootstrap vs steady state:** During **initial implementation** (until you sign off per **§1.2**), prefer `**interrupt_before` on *each* node** (`ingest_request`, `builder`, `operator`, `expert_critique`, `orchestrator_decide`, …) so **every** transition is human-resumable. After scaffold acceptance, narrow interrupts to **deployer** and **high-risk** nodes only.

### 5.3 Mapping from abd-maps-models-specs experiment

That repo’s `docs/orchestrator.md` describes **Planner / Runner / Critic** with **public vs private** critic fields. We adopt the split as in **§4.3**: **public** = domain-neutral principles + structure + coherence; **private** = comparison to a **known target** the Builder must **never** ingest. Competitive/client sensitivity is a **subset**, not the definition.

- **Public / private split** for critique payloads — **Builder receives public only** (see §4.3 table).
- **Iteration cap** and **stop-on-score** analogs for Expert dimensions (not only numeric — could be rubric thresholds).

We do **not** assume the same scripts — **agentic-skill-builder** generalizes across skills.

### 5.4 Slack notifications for human-in-the-loop (HITL) — **optional / deferred**

**Status:** **Off** until **api.slack.com** access and an Incoming Webhook URL exist — see **Execution status — Slack** at the top of this document. Until then, **ignore** Slack for scheduling and delivery; HITL is **interrupt + checkpoint + IDE/CLI** only.

When the graph **requires human intervention** and Slack **is** enabled later — **LangGraph** `interrupt_before` / `interrupt_after`, **orchestrator_decide**, **deployer** gate, etc. — the implementation **may** **notify** via Slack so you are not relying on a terminal you are not watching. That layer is **additive**, not required for correctness.

**Scope when Slack returns:** **Outbound notifications only** — **Incoming Webhook** (or later `chat.postMessage`). **No** Slack Events API in v1 of this feature; **no** “reply in Slack to resume the graph” — **resume** via checkpoint / CLI / IDE. Two-way Slack is a **later** optional layer (see `conf/README.md`).


| Concern                     | Approach                                                                                                                                                                                                                                                                                                                                                       |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Your workspace (humans)** | When enabled: join / use the **Agile by Design** Slack workspace via `**agentic-skill-builder/conf/README.md`**.                                                                                                                                                                                                                                               |
| **Programmatic delivery**   | **Slack Incoming Webhook** (URL on **hooks.slack.com**, in gitignored `**conf/.secrets**`) — `**AGENTIC_SKILL_BUILDER_SLACK_WEBHOOK_URL`**; optional `**AGENTIC_SKILL_BUILDER_SLACK_NOTIFY_USER_ID=`** (member ID for **@jeff.anderson**). **Shared code:** `src/agentic_skill_builder/slack_notify.py`; **CLI:** `python scripts/notify_slack.py "…"`. |
| **Payload**                 | Short **title** (e.g. `HITL: expert_critique`), **node** name, `**hitl_reason`**, iteration, skill_path / run id, link or CLI hint to resume. Optional `**slack_notify_ts`** for threading when Slack is on.                                                                                                                                                   |
| **When to fire**            | On **every** interrupt that blocks progress (when Slack enabled). Optionally **debounce** rapid repeats — **never** silently skip the first HITL in a run.                                                                                                                                                                                                     |
| **While Slack is off**      | No script runs required; completion summaries stay in **Cursor / terminal / logs**.                                                                                                                                                                                                                                                                            |


**Human workspace link (when relevant):** [Slack — Agile by Design workspace (invite)](https://join.slack.com/share/enQtMTA3NDMxMDA3OTI1NzktOWJjMDA2MDhhNjdiNDkwOTE2YWVmYzk4NTAwOGRiZTQ2M2M3YzJmODBmNGNhN2FmY2U1M2RiMzY4NjBlMzRjYg)

---

## 6. Orchestrator validation angles (your three lenses)

Order can change; all three should appear in `**expert_critique`** configuration.


| Lens               | Question                                                                                                     | Typical signals                                                                                               |
| ------------------ | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| **A — Principles** | Are relationships and responsibilities sane (no inheritance explosion, no nonsense associations)?            | OO smoke tests, CRC alignment, DDD-lite heuristics **from your materials**, not generic textbook boilerplate. |
| **B — Form**       | Is textual / structural representation well-formed (Given/When/Then, headings, rule structure, JSON shapes)? | Lint, schema validation, narrative patterns from `agile_bots` story rules.                                    |
| **C — Outcome**    | Would this artifact plausibly **realize** the story for a downstream “solution + architecture” pass?         | Trace from story map to concepts; scenario coverage; gap list vs idealized exemplar.                          |


**Operator** covers a **subset** of B (machine checks). **A and C** are primarily Expert (with optional deterministic helpers).

**§1.3 note:** After several **manual** runs, **dimensions of improvement** you observe (e.g. critic **overweights B vs A**) should feed back as **weights**, **thresholds**, or **extra rubric rows** — not only one-off fixes.

---

## 7. Rollout strategy, defaults, and corpus configuration

**Process:** Follow **§1.2** (gates) and **§1.3** (early standards + critique calibration, orchestration feedback, dimensions of improvement).

Implementation should follow **phases** below. Do **not** jump straight to **maps / models / specs** — validate the **whole loop** on a **trivial** skill first. **Engineering** detail (toy-first, stop between slices, milestone table): **§8**.

### 7.1 Phased rollout (product sequence)


| Phase                           | Goal                                                                                                          | Success criterion                                                                                                                                                                                                       |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1 — Reference trivial skill** | Prove **Builder + Operator + Expert** end-to-end on something **small** and easy to reason about.             | A generated skill passes **Operator**; **Expert** produces a sensible **public** critique using a **tiny** corpus + rubric (politeness / dialogue quality). You can **read** the artifact and agree the **flow** works. |
| **2 — Architecture review**     | You inspect **graph shape**, **state**, **gates**, **where gold lives** (§4.3).                               | You **accept** or request changes **before** heavy templates ship.                                                                                                                                                      |
| **3 — Maps / models / specs**   | Point the same pipeline at **real** skill families (`abd-maps-models-specs`-shaped layouts, rules, scanners). | Same pipeline; **larger** corpora and stricter Expert rubrics — **no** rewrite of core orchestration if Phase 1 was honest.                                                                                             |


**Reference trivial skill (concrete spec for Phase 1)**

Purpose: **smallest** skill that still has **stages**, **normative steps**, and a **non-empty** Expert domain (“what good dialogue looks like”) **without** enterprise complexity.


| Aspect                         | Choice                                                                                                                                                                                                                                                                                                |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Working name**               | e.g. `abd-polite-dialogue` or `hello-conversation` (final name when scaffolded).                                                                                                                                                                                                                      |
| **User journey (four stages)** | (1) **Greet** — open with a clear, friendly greeting. (2) **Introduce** — short self/context so the user knows who they are talking to. (3) **Converse** — one or more turns that **keep the thread** (clarify, respond, don’t dead-end). (4) **Close** — say goodbye cleanly without abrupt cut-off. |
| **Expert role**                | Knows **principles**: politeness, turn-taking, clarity, appropriate length — **not** a secret script. Optional **private** gold: an example “perfect” transcript **only** for **human** or **orchestrator** comparison (§4.3); **Builder** never sees it.                                             |
| **Operator**                   | Same **structural** contract as any skill: `build.py`, layout, `skill-config.json`, required globs, `compileall`.                                                                                                                                                                                     |
| **Why this works**             | If the pipeline **cannot** produce this, it will **not** reliably produce **abd-maps-models-specs**. If it **can**, you have a **debuggable** baseline.                                                                                                                                               |


### 7.2 What “full authority” means here

You asked for a **right approach** without needing to pre-decide every knob. **Defaults below** are **implementation authority**: the repo can ship with these unless you **explicitly** override in `conf/` or tickets.

- **Orchestration first:** Prove **LangGraph state + checkpoints + routing** on Phase 1; **Deployer** and **best-of-N** are **later** extras.
- **Expert retrieval:** Start with **small, explicit** file lists for the trivial skill; **broad** `skills/`* glob search comes **after** Phase 1 works.
- **Gold / private critique:** For the hello skill, private gold is **optional**; for **maps/models/specs**, **assume** gold lives **outside** Builder prompts (§1.1, §4.3).

### 7.3 Corpus roots for Expert (default priority)

Use this order for **retrieval** and **citation** unless a run config overrides it:


| Priority | Path / scope                                                                                            | Role                                                                                                                     |
| -------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **1**    | `agilebydesign-skills/skills/abd-skill-builder`                                                         | **Scaffold contract** — how skills are **shaped** and **built**; primary **structural** reference for Builder alignment. |
| **2**    | `agilebydesign-skills/skills/`* (other production skills, **excluding** the skill under test if needed) | **Patterns** — `build.py`, `parts/`, rules, `AGENTS.md` assembly.                                                        |
| **3**    | `C:\dev\abd_content` (or workspace `abd_content` root)                                                  | **Voice / content** examples for Expert when the skill is **content-heavy**; omit for purely structural critique.        |
| **4**    | `agile_bots/bots` (story / CRC rules)                                                                   | **Form** — Given/When/Then, narrative structure, **B** lens (§6).                                                        |
| **5**    | `skills/abd-maps-models-specs-old` or legacy paths                                                      | **Only** when migrating or comparing to an **old** layout — **not** default for Phase 1 trivial skill.                   |


**Default exclusions:** No automatic ingestion of **client confidential** trees; `**.env`**, `**/.secrets`, and giant binary dirs should stay **out** of retrieval allowlists. **Size:** cap chunk counts per Expert call in implementation config.

### 7.4 Optional knobs (defaults)


| Topic                            | Default                                                                                                                                      |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Expert model**                 | One **API** model for **Expert** in v1; **routing** can stay **deterministic** (no second LLM) until needed.                                 |
| **Deployer**                     | **Local commit + branch only** — no `**git push`** until you add a **config flag**.                                                          |
| **Parallelism / best-of-N**      | **Off** until Phase 2+; serial **builder → operator → expert** loops first.                                                                  |
| **Maps/models/specs gold shape** | After Phase 2 approval: prefer **lighter** exemplars first (`docs/reference/`* **shape**), then **full** gold sidecars if Expert needs them. |


---

## 8. Phased implementation roadmap (engineering)

Aligned with **§7.1** (product sequence) and **§1.2** (gates). **Intent:** do **not** build the whole orchestrator in one push. **Stand up the smallest useful slice** from a **Builder** perspective, then **immediately** validate it with a **toy skill** — **not** maps/models/specs yet.

### 8.1 Toy skill first (always)

As soon as something **Builder-shaped** exists (even a stub that emits files), **exercise the full agent chain** on a **trivial** skill so you can see end-to-end behavior before complexity grows:

- **Toy examples:** polite dialogue, greetings, a simple counter, “hello conversation” — **anything minimal** with **stages/phases** and something for **Expert** to judge (§7.1 table).
- **Pass it through every agent:** **Builder** (produce/update the toy) → **Operator** (structural checks) → **Expert** (rubric critique). Confirm **routing, state, and interrupts** behave as intended.
- **If the toy path is wrong**, fix **orchestration** before investing in **abd-maps-models-specs**-shaped templates.

### 8.2 Stop at each engineering slice (not “ship P1 in one go”)

**P1–P5** below are **milestones**, each of which should be **cut into stages** with a **§1.2 stop** between them — e.g. state only → **review** → graph shell → **review** → Operator on a fixture → **review** → Builder emits toy → **review**. Same idea for **P2**, **P3**, etc.: **build stage one → stop → stage two → stop** — **no** implicit “finish the whole phase unattended.”

### 8.3 Maps / models / specs (later) — same HITL discipline

When you move the pipeline toward **real** `abd-maps-models-specs`-style skills (**P3** and **§7.1 phase 3**), **do not** skip human loops. For each increment: **build** (template or skill output) → **operate** (validators/scanners) → **expert** (critique) → **you review**. Expect **several manual runs** before the pipeline and rubrics are **calibrated**; **§1.3** applies — you **get feedback back** as **dimensions of improvement**, not only one-off file fixes. Autopilot stays **off** until you **explicitly** sign off (§1.2).

### 8.4 Milestone table

**P1–P3** are the **minimum** path to confidence; later rows are **stretch**. **Between every row** (and **between sub-deliverables** inside a row): **stop**, **human review**, **fix plan or redo** — no skipping gates until you **explicitly** allow hands-off runs.


| Phase  | Deliverable                                                                                                                                                                                                                                                                              |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **P0** | This plan + repo scaffold under `**agentic-skill-builder/`** (done).                                                                                                                                                                                                                     |
| **P1** | `**SkillDeliveryState`** + runnable graph + CLI; **Operator** on a **fixed path**; **Builder** emits the **§7.1 toy / trivial** skill (scaffold + generation). Exercise **full loop** on the toy (§8.1). **Optional:** `**notify_hitl_slack**` when Slack is enabled (§5.4).                 |
| **P2** | **Expert** node + **minimal** retrieval from **§7.3** priority **1–2** + rubric YAML; **public/private** routing per §4.3; **HITL interrupt** after Expert as needed. **Slack pings** only if webhook configured — otherwise IDE/CLI only (§5.4, Execution status).                        |
| **P3** | **You review** architecture (§7.1 phase 2); then **Builder templates** aligned to `**abd-maps-models-specs`** layout (rules, phase markdown, scanners). **HITL:** build → operate → expert → **human review**; **several runs** before treating behavior as stable (§8.3).                 |
| **P4** | Deployer subgraph + **optional** `git push` policy + reporting.                                                                                                                                                                                                                          |
| **P5** | Best-of-N builder (optional) + parallel experiment branches.                                                                                                                                                                                                                             |


**Sub-step example (inside P1):** (a) state type + empty graph → **review** → (b) Operator CLI on fixture → **review** → (c) Builder stub → **review** → (d) toy skill path → **review** → (e) run **Builder → Operator → Expert** on toy → **review**. Each letter is a **§1.2** gate; do **not** collapse into one undifferentiated “P1 done” without stops if you want this discipline.

---

## 9. Resolved defaults (was open questions)

### 9.1 Operator: what gets checked for a **skill**

**agentic-skill-builder** exists to **build** skills that match the **Open Agent Skills** shape — the same category as **[skills.sh](https://skills.sh)** (*The Agent Skills Directory* / open ecosystem) and the same kind of skill as the rest of this monorepo. There is **no** separate “agentic skill” product type and **no** requirement that a skill “plug into” this repo.

**Default for validating a skill directory:**

- **That skill’s** `build.py`, **native** scanners, and domain rules — **domain** validation stays **in the skill**.
- **Thin shared checks** (only where this repo provides them): e.g. `compileall`, required globs, “scanners declared in config ran” — **structural / mechanical**, not a second domain layer. These are **not** “integration with agentic-skill-builder”; they are **quality gates** on the **artifact** (a normal skill).

Skills **do not** carry an extra public contract because they were (or were not) produced by this builder.

### 9.2 Builder: code vs LLM content

**Default:** **Deterministic skeleton** + **LLM-authored** bodies under **`content/parts/`** (and similar), not free-form repo-wide generation without structure.

### 9.3 `builder_manifest` — **internal** to the builder, not a skill standard

**Role:** During a **builder orchestration run**, the pipeline may emit a **`builder_manifest`** (or equivalent) that records **fragment wiring**, **static vs dynamic** assembly intent, and **artifacts** the Builder run produced (see §3.3). That structure is **for the skill-building process** — it is **not** something every skill must satisfy, and **not** what makes a skill valid under **[skills.sh](https://skills.sh)**-style / Open Agent Skills packaging.

**JSON Schema (optional but useful):** A **versioned** JSON Schema (`$id`, semver or dated artifact) may be published **for this repository only** — to validate **builder-run outputs / internal state** in **CI** and to keep the orchestration code honest. That is **tooling for agentic-skill-builder**, **not** a third-party “plug-in” spec for skills.

**What third parties and hand-authored skills need:** Conformance to **skills as defined by the [skills.sh](https://skills.sh)** ecosystem (Open Agent Skills — `SKILL.md`, layout, procedural knowledge packaging) plus whatever **that skill’s** own README documents. **No** second standard from agentic-skill-builder on top of that.

---

## 10. References

### Inside this monorepo

- `agilebydesign-skills/skills/abd-skill-builder` — scaffold + build order.  
- `agilebydesign-skills/skills/abd-context-to-memory/scripts/build.py` — engine delegation pattern.  
- `agilebydesign-skills/skills/abd-maps-models-specs/docs/orchestrator.md` — planner/runner/critic split.  
- `agilebydesign-skills/skills/abd-maps-models-specs/plan/pipeline-deep-dive.md` — domain critique of pipeline incentives (inform Expert rubric, not Operator).  
- `agile_bots/bots` — story + CRC rules as **form** and **outcome** hints for Expert.

### External (skills ecosystem, critique, refinement)

- **[skills.sh](https://skills.sh)** — Open Agent Skills ecosystem and directory; definitional home for **skills** referenced in this plan.  
- Madaan et al., **Self-Refine: Iterative Refinement with Self-Feedback**, NeurIPS 2023 — [paper](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html)
- Anthropic, **Constitutional AI: Harmlessness from AI Feedback** — [research](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
- *Improving Interactive In-Context Learning from Natural Language Feedback* (2026) — teacher feedback with **privileged ground truth** **without** revealing the answer — [HF paper page](https://huggingface.co/papers/2602.16066)
- LTS Commerce, **The Overfitting Trap: When LLM Agents Fix One Thing and Break Everything Else** — [article](https://ltscommerce.dev/articles/llm-overfitting-trap.html) (demonstration bias / single-scenario fixes)
- **Reward model overoptimization / policy–reward mismatch** in iterated RLHF — e.g. [arXiv:2505.18126](https://arxiv.org/abs/2505.18126) (why **separation** needs **monitoring**)

---

*End of plan — defaults in §7–§9; override via `conf/` and product review at §7.1 phase 2. **Execution discipline:** §1.2 (stop every step until scaffold sign-off); §1.3 (first builds: standards + critique + orchestration feedback → dimensions of improvement).*