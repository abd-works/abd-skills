---
name: abd-delivery-planning
catalog_garden_tier: practice
catalog_garden_order: 70
catalogue_one_liner: >-
  Delivery plans only: context, risks, strategies, staged runs and checkpoints (not stories, tests, or code).
description: >-
  Build and revise agile delivery plans: context assessment, risk types, strategies
  (scan strategies/ for matching When to use), runs (stages, scope, checkpoints,
  rationale), and example plans. Planning only — not for producing story artifacts,
  tests, or code (those come from downstream practice work).
---

# abd-delivery-planning

## When to use this skill

- You want to **build, present, or revise** a delivery plan after reading context.
- You need to **classify risks**, **pick or adapt a strategy**, or **design runs** with explicit scope and checkpoint policy.
- After a custom engagement, you are **saving a new reusable strategy** — add a new **`.md`** file under **`strategies/`** in this skill folder (see **`strategies/README.md`**).

Do **not** use this skill as a substitute for the work that **produces** artifacts (maps, slices, acceptance criteria, scenarios, tests, code). This skill only plans *how* and *in what order* that work happens.

### Why agile delivery planning

Like people, **agents** infer from partial context. Getting the *right* context upfront—and how much to load in one shot—is hard; a single linear pass rarely suffices. Agents can **hallucinate**, **drift**, and **miss** important edges.

**Agents benefit from an explicit delivery lifecycle**—the same reason humans do: not just *what* to do next, but **when to stop**, **what to verify**, **when to revisit**, **replan**, **re-execute**, and **when to move on**. That lifecycle is how you **stop for feedback**, **correct course**, **revise scope**, and **refine how delivery runs** instead of hoping one long prompt “sticks.”

At those stops, the orchestrator and user surface the questions that matter: Do we **understand the outcome**? Is **scope** right? Will the **architecture** support the goals? Do we **understand the domain**? Can we **trace requirements into code** through the architecture and roles we chose? Delivery planning names **where** those questions get asked and **what** “good enough to continue” means.

- **Uncertainty is real** — keep the plan **living**: update it as artifacts land and corrections accumulate, not as a frozen script.
- **Orchestration needs a spine** — **runs** and **checkpoint policy** say what to delegate next, when to pause, and what “done” means before the next agent acts.
- **Risk before volume** — order work so the hardest unknowns fail early, before breadth.
- **Humans in the loop** — checkpoints make confirmation and correction **predictable**, not accidental.

Without delivery planning, you get one-off prompts and silent scope creep instead of a repeatable lifecycle across specialized agents.

---

## Agile delivery plan

An **agile delivery plan** determines what stages to run, for what scope, in what order, how many times stages run, and when to stop for feedback. **Build or update the plan as the first substantive step after reading context** — it is the most important planning output.

A plan is:

- A **sequence of runs**, ordered to manage risk, maximize learning, and build confidence incrementally.
- An **assessment** of the engagement landscape: what is known, what is risky, where the model is likely to struggle.
- A **living document** — revised after every run based on what was learned, corrections accumulated, and scope shifted.

The plan answers: *Given everything we know about this engagement, what is the smartest order to do the work, at what granularity, and where do we need to be most careful?*

### Plan structure

```
Plan
├── Context assessment (known domains, risky domains, integration points, complexity)
├── Context inventory (provided vs missing — see below)
├── Run 1: { stages, scope, checkpoint policy, rationale }
├── Run 2: { … }
├── ...
└── Run N: { … }
```

#### Context inventory (required)

Do **not** treat a named platform (Foundry, Salesforce, your monolith, etc.) as “understood” unless context was **actually supplied**. In every **saved** plan (`agile-delivery-plan.md`), include:

1. **Provided context** — concrete inputs you used: file paths, repo URLs, doc links, API refs, **versions** (runtime, module API level), existing story graph, prior corrections.
2. **Missing or assumed context** — explicit **flags** for what was **not** provided but is needed for honest planning or execution (e.g. no Foundry version, no module source, no hook list). Use neutral wording: *not yet provided* — not “TBD” buried in prose.
3. **Implications** — if critical context is missing, state what must happen before implementation runs (spike, doc pass, user drops links, clone repo). **AI-model and integration risk** spike when a **host product or integration surface** is named in the brief but undocumented in the engagement.

If you only have a short brief, the inventory should say so. **Outcome:** reviewers and the delivery lead see gaps immediately instead of inferring from chat.

#### Run rationale: say what you are actually trying to do

**Rationale** must name the **concrete outcome** of the run—what is **true**, **proven**, or **delivered** when the run completes—not only which risk types you are mitigating. Vague lines like *“mitigate technical risk”* without *what done looks like* are not enough.

When the work is constrained by a **specific product, runtime, or external system** (VTT, ERP, browser, engine, vendor API), **fold that into the same rationale**: name the constraint and what this run achieves **there**. When there is no such constraint, a plain product or engineering outcome is enough—**do not** add integration boilerplate.

Early runs whose main job is to **learn how something works in a host environment** (map the surface, spike, first vertical) should say that plainly in rationale, not only “deliver business value.”

Each run builds on the outcomes of the previous one. The plan is **front-loaded** — the first runs target the riskiest, least-understood areas. Later runs can move faster because the model (and the corrections log) have learned the domain, technology, and UX patterns.

**A plan is NOT "run all six stages start to finish."** That is the degenerate case for trivial engagements with no risk. Real plans decompose the work into targeted runs that flush out unknowns early.

After every run completes, **review** learnings, quality, and risk. **Revise** the plan when understanding warrants changing run order, scope, checkpoint policies, or which stages execute next.

### Where to save the plan (engagement workspace)

The delivery plan is a **living document** in the **engagement workspace**, not in the skill repo. Use one **fixed filename** so orchestration and humans always know where to look:

```text
<workspace>/agile-delivery-plan.md
```

- **`workspace`** is the engagement root (same root used for `story-graph.json`, `docs/corrections-log.md`, and **`track_task`** paths).
- **When to write:** After you **build**, **confirm**, or **revise** the plan (including after each run’s replan in Step 7 of the delivery lead). **Overwrite or patch** this file so it reflects the current context assessment, selected strategies, and full run sequence—do not leave the authoritative plan only in chat.
- **Companion file:** Checkbox execution lives in **`abd-delivery-lead/progress/delivery-plan-checklist.md`** (see **`track_task`**). The narrative plan and the checklist must stay **aligned** when either changes.

---

## What is a run

A **run** is one unit of planned work within the plan. Each run has four dimensions:


| Dimension             | What it defines                                                               | Example                                                                                              |
| --------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Stages**            | Which stages execute, start through end                                       | `discovery → exploration` or bug-fix: `acceptance-tests`, `engineering`, `story-definition`          |
| **Scope**             | What stories, thin slices, epics, or areas the run covers                     | "Stories that integrate the Acme SSO API" or "Thin slice 1: basic login"                             |
| **Checkpoint policy** | Where to stop and validate (after stage done, in-stage, after stages X and Y) | Checkpoints within team member workflow; or after each thin slice completes engineering              |
| **Rationale**         | Why this run; which **risk type(s)** it mitigates; **the concrete outcome** when the run completes (what is proven, decided, or shipped)—including **where** that outcome lives if a host system or integration matters | Mitigate *integration* + *AI-model* risk: **prove** one end-to-end path through the Acme SSO API and capture unknowns before mapping the rest of login |


Scope can be **qualitative** (e.g. "all stories touching payment processing") when the graph does not yet exist, or **exact** (story names, slice IDs, epic paths) once the graph exists.

### Checkpoint granularity levels


| Level                   | Scope                                                            | When to use                                       |
| ----------------------- | ---------------------------------------------------------------- | ------------------------------------------------- |
| **Within team member**  | After each story, AC, scenario, or test                          | High uncertainty, proprietary domains, early runs |
| **Across team members** | Between stages (e.g. after exploration, before story definition) | Normal flow, handoff validation                   |
| **Across runs**         | After a full run's scope before the next                         | Multi-run review, scope adjustment                |


**Default:** start granular (per-story within team member), relax as confidence builds. Tighten if the model errs; widen if flow is smooth.

---

## Delivery flow — stage sequence

This flow has **six ordered stages**. Per-stage **entry conditions**, **exit gates**, and **team role** are defined in **`stages/<stage>.md`** in your orchestration setup — not in this skill.


| #   | Stage            | Team Role     | Typical practice focus        | Stage file (convention) |
| --- | ---------------- | ------------- | ----------------------------- | ----------------------- |
| 1   | Discovery        | Product Owner | Story mapping                 | `discovery.md`          |
| 2   | Prioritization   | Product Owner | Thin slicing / ordering work  | `prioritization.md`     |
| 3   | Exploration      | Analyst       | Acceptance criteria           | `exploration.md`        |
| 4   | Story Definition | Analyst       | Specification by example      | `scenarios.md`          |
| 5   | Acceptance Tests | Engineer      | Acceptance-test-driven work   | `acceptance-tests.md`   |
| 6   | Engineering      | Engineer      | Clean implementation          | `engineering.md`        |


Stages are sequential by default. Parallel runs are allowed when outputs are independent (e.g. story definition for one slice while discovery continues for another).

---

## Step 2 — Build the plan (procedure)

Use this procedure when planning. The delivery lead executes it; this skill documents the rules.

### 2a — Context analysis

Read all context: documents, briefs, API references, prior material, existing code. Identify:

1. **Known domains** — strong training data (common frameworks, documented APIs).
2. **Risky domains** — proprietary APIs, internal systems, novel logic, no public examples.
3. **Integration points** — external systems, APIs, data sources, dependencies.
4. **Complexity drivers** — regulatory load, multi-actor workflows, concurrency, state.
5. **Existing assets** — prior story graphs, specs, tests, code.

Then **classify risks** using the table below. A successful delivery manages and mitigates risk systematically; wrong risk prioritization wastes effort.


| Risk type            | Meaning                                                                   | Signals in context                                                                  |
| -------------------- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **Value risk**       | We might build the wrong thing — need, solution, or customer fit unclear. | Vague briefs, no research, conflicting goals, untested assumptions.                 |
| **Technical risk**   | Wrong tech, infrastructure, skills, or architecture.                      | Proprietary APIs, unfamiliar stacks, novel algorithms, scale/perf unknowns.         |
| **Delivery risk**    | Miss schedule or quality bar.                                             | Large scope, dependencies, cross-team work, deadlines, immature pipelines.          |
| **Domain risk**      | Misunderstand business rules, regulations, or domain logic.               | Regulatory regimes, complex rules, jargon, ambiguous terms.                         |
| **Integration risk** | External systems behave unexpectedly or constrain design.                 | Legacy systems, quirky APIs, backward compatibility, migrations.                    |
| **AI-model risk**    | The agent is likely to hallucinate or produce wrong output.               | No training data for proprietary systems, undocumented APIs, unique internal logic. |


Tag each risk. Risk types drive strategy choice, run ordering, and checkpoint tightness.

### 2b — Select and adapt a strategy

1. Open **`strategies/`** in this skill folder (see **`strategies/README.md`** for conventions and the catalog table).
2. **Enumerate** strategy files — every **`.md`** in **`strategies/`** except **`README.md`** is one strategy.
3. For each candidate file, read at least **When to use** (and **Typical scope** if present). **Match** context and classified risks to **zero, one, or more** strategies. **Combine** or **blend** when multiple fit (cross-links in *New Initiative* strategies explain common pairings).
4. **Adapt** the chosen table(s): scope, checkpoints, runs, and stages to the engagement.

**If no strategy fits**, design a custom plan and propose saving it as a new **`<slug>.md`** under **`strategies/`** after the engagement (same six-column table shape as the others).

### 2c — Design the runs

Based on the strategy, propose a **sequence of runs**:

- **Front-load risk** — targeted early runs that exercise the hardest unknowns with minimal scope.
- **Order by learning value** — hardest integration, architecture, UX, or business logic first.
- **Match checkpoint granularity to uncertainty.**
- **Plan for re-planning** after each run.
- **Regressions and test-led fixes** — when the signal is a **failing test**, **wrong behavior**, or a **small defect**, plan **separate steps with distinct intents** (e.g. Exploration to **isolate** scope → Engineering (+ tests) to **prove** the fix → Exploration / Story Definition to **reverse-engineer** AC/spec from corrected behavior). Same stages can appear in multiple rows when scope differs; intent explains *why* each step exists — see **`strategies/bug-fix.md`**.

For **each run**, state:

1. **Stages** (start through end).
2. **Scope** — qualitative or exact.
3. **Checkpoint policy** at each level (within team member, across team members, across runs).
4. **Entry conditions** — include **context dependencies** (docs, repo access, versions). If something required is still in **Missing context**, **flag** it here or in **rationale**; do not assume it will appear.
5. **Expected outputs.**
6. **Rationale** — risk type(s) mitigated **and** the **concrete outcome** of the run (see **Run rationale** above). If missing context **blocks** the run, say so **in rationale or entry conditions**.

### 2d — Example plans (patterns)

Use these as patterns for how different context shapes different plans.

**Example A — Proprietary API integration platform**

Context: CRM, SSO, SOAP billing; React; three actors.


| Run | Stages                     | Scope                                          | Checkpoint Policy                         | Rationale                |
| --- | -------------------------- | ---------------------------------------------- | ----------------------------------------- | ------------------------ |
| 1   | Discovery → Prioritization | Only stories touching CRM, SSO, or billing     | Per-story                                 | Map integration surface  |
| 2   | Exploration → Engineering  | Thin slice 1: one story through all three APIs | Per-AC / per-test; cross-team after story | Prove hardest path       |
| 3   | Exploration → Engineering  | Thin slice 2: second actor path                | Per-story; cross-run vs run 2             | Second auth flow         |
| 4   | Discovery (remaining)      | Full map including pure UI                     | Per-epic                                  | Broaden once APIs proven |
| 5   | Prioritization             | Re-slice full map                              | Cross-team                                | Order by value           |
| 6+  | Exploration → Engineering  | Remaining slices                               | Per-slice                                 | Routine                  |


**Example B — Regulatory (FCA/HMRC) with public APIs**


| Run | Stages                         | Scope                                     | Checkpoint Policy           | Rationale                   |
| --- | ------------------------------ | ----------------------------------------- | --------------------------- | --------------------------- |
| 1   | Discovery → Prioritization     | Full map; slice by compliance surface     | Per-epic PO                 | Rules are the risk          |
| 2   | Exploration                    | Auditor / Finance slices — heaviest rules | Per-AC; regulatory accuracy | AC = compliance             |
| 3   | Story Definition               | Same slice; real VAT/retention values     | Per-scenario                | Concrete values expose gaps |
| 4   | Acceptance Tests → Engineering | Compliance slice end-to-end               | Per-test                    | Tests prove compliance      |
| 5+  | Exploration → Engineering      | Other slices                              | Per-slice                   | Lower risk                  |


**Example C — Greenfield, ambiguous domain**


| Run | Stages                         | Scope                             | Checkpoint Policy            | Rationale                           |
| --- | ------------------------------ | --------------------------------- | ---------------------------- | ----------------------------------- |
| 1   | Discovery only                 | Full map from brief + interviews  | Per-story PO                 | Extract domain language             |
| 2   | Discovery (refine)             | Vague terms (e.g. "optimization") | User validates definitions   | Cannot write AC without definitions |
| 3   | Prioritization                 | Simplest E2E slice first          | Per-slice PO                 | Prove domain model                  |
| 4   | Exploration → Engineering      | Basic lifecycle slice             | Per-story                    | Entities in code                    |
| 5   | Exploration → Story Definition | Hard algorithmic stories          | Per-AC + user vs transcripts | Validate before code                |
| 6+  | Acceptance Tests → Engineering | Algorithm stories then rest       | Per-test / per-slice         | Incremental                         |


**Example D — Legacy monolith migration**


| Run | Stages                     | Scope                          | Checkpoint Policy | Rationale         |
| --- | -------------------------- | ------------------------------ | ----------------- | ----------------- |
| 1   | Discovery → Prioritization | Map from existing API + manual | Per-endpoint PO   | Old system = spec |
| 2   | Exploration                | AC matches legacy behavior     | Per-AC vs PHP     | Contract          |
| 3   | Acceptance Tests           | Tests pass against **old** API | Per-test          | Safety net        |
| 4   | Engineering                | Implement first service        | Per-endpoint      | Prove pattern     |
| 5+  | Exploration → Engineering  | Remaining groups               | Per-group         | Repeat pattern    |


### Present the plan (checkpoint)

Present to the user:

1. Context assessment and classified risks.
2. **Context inventory** (**Provided** vs **Missing** — see **Context inventory (required)**).
3. Selected strategy or strategies (from **`strategies/`**, with file name(s)) and adaptations.
4. Sequence of runs; for **each run**, include the items from **§2c** (each **rationale** must state the **concrete outcome**, not only risks).

**Persist** the same content to **`<workspace>/agile-delivery-plan.md`** (see **Where to save the plan**) **before** you stop for confirmation, or immediately after the user confirms if you presented from a draft—so the delivery lead and other agents can **read the plan from disk** on the next session. The persisted file must include the **context inventory** so missing inputs are not lost between sessions.

Stop for confirmation. If no named strategy fits, explain why and present the custom plan; offer to save it as a new file under **`strategies/`** later.

---

## Files in this skill


| File / path                            | Purpose                                                                |
| -------------------------------------- | ---------------------------------------------------------------------- |
| `SKILL.md` (this file)                 | Concepts, procedure, risk types, stage table, example plans            |
| `strategies/README.md`                 | Strategy conventions, catalog, how to select a strategy                |
| `strategies/*.md`                      | One prepackaged strategy per file (excluding `README.md`)              |
| `rules/*.md`                           | Mechanical rules for plan quality (six rules, bound to one scanner)    |
| `scanners/plan-shape-scanner.py`       | Single scanner evaluating the six plan-shape rules against the saved plan |
| `scanners/tests/*.md`                  | Good / bad plan fixtures used to verify the scanner                    |

### Validating a saved plan

After writing or revising `<workspace>/agile-delivery-plan.md` (Step 2 or Step 7 of the delivery lead), run:

```
python skills/execute_using_rules/scripts/run_scanners.py \
    --skill-root skills/abd-delivery-planning \
    --workspace <workspace>
```

The runner discovers `scanners/plan-shape-scanner.py` from each rule's `scanner: plan-shape` frontmatter (deduplicated to a single invocation) and from flat discovery under `scanners/`. The scanner reads the plan at `<workspace>/agile-delivery-plan.md` and reports violations for any of the six rules; exit code 0 = clean, 1 = at least one violation, 2 = path resolution failure. When no plan exists yet the scanner exits 0 silently.

**Engagement workspace (not in this repo):** `agile-delivery-plan.md` (at workspace root) — canonical **saved** agile delivery plan for the engagement; see **Where to save the plan**.