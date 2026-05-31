# abd-kanban-planning — Concepts

**Shared kanban concepts** (ticket model, board lists, stages, scattering, skill progress, agents): [../../../reference/kanban-board.md](../../../reference/kanban-board.md) · [../../../reference/agents-and-skills.md](../../../reference/agents-and-skills.md)

## Why delivery planning

Agents benefit from an explicit delivery lifecycle: not just *what* to do next, but **when scope changes**, **when to scatter**, **how to group work**, and **when to stop for feedback**. The strategy + kanban board provide the spine without pre-planning every assignment.

- **Uncertainty is real** — keep the strategy living; update when corrections accumulate.
- **Risk before volume** — order increments so the hardest unknowns fail early.
- **JIT over pre-plan** — decompose only when needed, not everything upfront.
- **Humans in the loop** — checkpoint policy makes confirmation predictable.

---

## Strategy

A **strategy** defines how work flows through the kanban board:

- **Scope progression** — which scope levels apply at each stage (may differ from default)
- **Scatter rules** — when and how to decompose tickets at scope boundaries
- **Sprint grouping** — how to group stories into sprints (default 3–4, adjustable)
- **JIT policy** — how far ahead to scatter (next 1–2 items by default)
- **Checkpoint policy** — where to stop for feedback (per skill, per stage, per increment)
- **Risk classification** — which risks are present and how they affect ordering

---

## Risk classification

Classify risks to inform strategy selection:

- **Value risk** — building the wrong thing. Signals: vague briefs, no research, conflicting goals.
- **Technical risk** — wrong tech, infra, or architecture. Signals: proprietary APIs, unfamiliar stacks, scale unknowns.
- **Delivery risk** — miss schedule or quality bar. Signals: large scope, dependencies, deadlines.
- **Domain risk** — misunderstand business rules. Signals: regulatory regimes, complex rules, jargon.
- **Integration risk** — external systems constrain design. Signals: legacy, quirky APIs, backward compat.
- **AI-model risk** — agent likely to hallucinate. Signals: no training data, undocumented APIs.

Risk types drive strategy selection and checkpoint tightness.

---

## Strategy selection procedure

### Step 1 — Context analysis

Read all context. Identify:

1. **Known domains** — strong training data, documented APIs.
2. **Risky domains** — proprietary, internal, novel logic.
3. **Integration points** — external systems, dependencies.
4. **Complexity drivers** — regulatory, multi-actor, concurrency.
5. **Existing assets** — prior story graphs, specs, tests, code.

### Step 2 — Select strategy

1. Open `strategies/` in this skill folder.
2. Read each strategy's **When to use** section.
3. Match context and risks to a strategy (or blend multiple).
4. If no strategy fits, design custom — offer to save later.

### Step 3 — Configure kanban board stages

From the selected strategy, write `kanban.json` (the kanban board stage configuration):

- Which stages are active
- Scope level per stage
- Ordered stage work required per stage with delivery role assignments
- Any optional skills (marked in strategy)

### Step 4 — Define scatter and decomposition rules

Write the `strategy` section in `kanban.json` with:

- **Scatter rules**: which scope transitions scatter vs advance, sprint grouping (default 3–4), JIT policy
- **Ordering**: priority source (story map, user override, risk-first)
- **Checkpoint policy**: per-skill, per-stage, or per-increment
- **Autonomy**: tight, moderate, or full

### Step 5 — Present and confirm

Present to user:

1. Context assessment and classified risks.
2. Selected strategy (name, from which file, adaptations).
3. Kanban board stage configuration (stages, scope, skills).
4. Scatter rules and checkpoint policy.

**CHECKPOINT.** Wait for user confirm before setup.

---

## Stage 0: Context (optional)

The context stage prepares source material for agent consumption. It is **optional** — skip when:

- Context is already small and readable (a few markdown files, a short brief)
- The team already has domain knowledge loaded
- The project is a bug fix or small story with no external documents

**Include when:**

- Source material is in office formats (PDF, PPTX, DOCX, XLSX) that agents cannot read directly
- There are many files that need indexing for semantic search
- The domain is complex and agents need RAG-backed retrieval during later stages
- Prior engagement material exists that should be searchable

**Skills (ordered, conditional):**

- **abd-convert-to-markdown** — include when source files are PDF, PPTX, DOCX, XLSX, or other non-markdown formats
- **abd-semantic-context-chunker** — include when multiple source types need classifying before chunking
- **abd-chunk-markdown** — include when large converted files need splitting for retrieval
- **abd-embed-vectors** — include when semantic search (RAG) is needed during later stages

The kanban lead assesses source material at strategy selection and decides which context skills are needed (or skips the stage entirely).

---

## Exploration: architecture template (conditional)

`abd-architecture-template` is **on the exploration rail** for every increment ticket, but the engineer runs it **only when the increment needs mechanism template sections that do not yet exist**.

**Run when:** AC and blueprint name cross-cutting mechanisms missing a complete section under `docs/increments/<n>-<slug>/exploration/architecture/architecture-template.md`.

**Skip when:** All increment mechanisms are already documented — engineer assigns existing sections, marks skill done with skip notes, and exploration continues.

This mirrors the skill's assign-vs-create workflow; the kanban stage lists the skill so downstream skills stay ordered, not so every increment rewrites the same mechanisms.

Stage definitions: [`../../reference/stages/README.md`](../../reference/stages/README.md)

---

## Checkpoint granularity

- **Per skill** — after each skill completes on a ticket; use for high uncertainty, early work
- **Per stage** — after all skills complete (stage exit gate); use for normal flow
- **Per increment** — after increment tickets complete; use for multi-increment review

Default: start granular (per-skill), relax as confidence builds.

---

## Scatter rules (configurable per strategy)

### Default scatter heuristics

- **all → increment** — one ticket per increment from thin-slicing; scatter all
- **increment → sprint** — group 3–4 stories per sprint; scatter next 1–2 increments JIT
- **sprint → story** — rare; only if strategy requires per-story tickets

### User overrides

Users can specify:
- "Divide increment 1 into 3 sprints, increment 2 into 5 sprints"
- "Scatter all increments now"
- "Only scatter next 2"
- "Leave later increments until we know more"
- "Increment 1 sprint 1: story 1 then 2 then 3" (specific ordering)

### AI error rate adjustment

When AI output error rate is high (>10%):
- **Shrink scope**: move from increment-level to sprint-level or story-level
- Tighten checkpoints to per-skill
- After error rate drops, expand back

When error rate is low (<5%):
- **Expand scope**: move from sprint to increment across flows
- Relax checkpoints to per-stage

---

## Strategy file structure

Each strategy file in `strategies/` defines:

- **When to use** — context signals and risk types that match this strategy
- **Typical scope** — what boundary or area this applies to
- **Kanban board stages** — stages, scope per stage, skills per stage (or reference to default)
- **Scatter rules** — how tickets decompose at scope boundaries
- **Sprint grouping** — stories per sprint, grouping heuristics
- **JIT policy** — how far ahead to decompose
- **Checkpoint policy** — where to stop for feedback
- **Key constraints** — non-negotiable rules for this strategy

## Strategy catalog

- **[new-user-story.md](../strategies/new-user-story.md)** — 1–3 stories on existing solution
- **[new-thin-slice.md](../strategies/new-thin-slice.md)** — vertical slice (~5–15 stories)
- **[new-initiative-no-documented-architecture.md](../strategies/new-initiative-no-documented-architecture.md)** — greenfield; no architecture
- **[new-initiative-proprietary-technology-risk.md](../strategies/new-initiative-proprietary-technology-risk.md)** — proprietary/undocumented systems
- **[new-initiative-business-user-experience-risk.md](../strategies/new-initiative-business-user-experience-risk.md)** — UX/domain risk dominant
- **[brownfield-current-state.md](../strategies/brownfield-current-state.md)** — map and test existing system
- **[legacy-migration.md](../strategies/legacy-migration.md)** — replace system; legacy is truth
- **[regulatory-compliance-heavy.md](../strategies/regulatory-compliance-heavy.md)** — regulation/compliance dominates
- **[bug-fix.md](../strategies/bug-fix.md)** — defect or regression
- **[spike-proof-of-concept.md](../strategies/spike-proof-of-concept.md)** — answer one question before delivery

## Adding a strategy

After a custom engagement, save a new `<slug>.md` in `strategies/` with the same sections. Reference bootcamp stages and scope levels. Include scatter rules and sprint grouping heuristics.

## Adapting a strategy

When selecting a strategy, adapt it:

1. **Add/remove stages** — bug fix skips shaping; spike skips engineering.
2. **Add/remove skills** — brownfield adds module partition; UX-heavy adds IA.
3. **Change scope levels** — if stories are huge, add sub-story scope.
4. **Override sprint grouping** — "2 stories per sprint for this complex area."
5. **Change JIT policy** — "scatter all increments now, we know the domain."
6. **Adjust checkpoints** — "per-skill for increment 1, per-stage after."
