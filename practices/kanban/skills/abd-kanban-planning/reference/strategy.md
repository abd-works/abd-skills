# Strategy

A **strategy** defines how work flows through the kanban board:

- **Scope progression** ” which scope levels apply at each stage (may differ from default)
- **Scatter rules** ” when and how to decompose tickets at scope boundaries
- **Sprint grouping** ” how to group stories into sprints (default 3“4, adjustable)
- **JIT policy** ” how far ahead to scatter (next 1“2 items by default)
- **Checkpoint policy** ” where to stop for feedback (per skill, per stage, per increment)
- **Risk classification** ” which risks are present and how they affect ordering

---

## Why Kanban Planning

Agents benefit from an explicit delivery lifecycle: not just *what* to do next, but **when scope changes**, **when to scatter**, **how to group work**, and **when to stop for feedback**. The strategy + kanban board provide the spine without pre-planning every assignment.

- **Uncertainty is real** ” keep the strategy living; update when corrections accumulate.
- **Risk before volume** ” order increments so the hardest unknowns fail early.
- **JIT over pre-plan** ” decompose only when needed, not everything upfront.
- **Humans in the loop** ” checkpoint policy makes confirmation predictable.

---

## Risk classification

Classify risks to inform strategy selection:

- **Value risk** ” building the wrong thing. Signals: vague briefs, no research, conflicting goals.
- **Technical risk** ” wrong tech, infra, or architecture. Signals: proprietary APIs, unfamiliar stacks, scale unknowns.
- **Delivery risk** ” miss schedule or quality bar. Signals: large scope, dependencies, deadlines.
- **Domain risk** ” misunderstand business rules. Signals: regulatory regimes, complex rules, jargon.
- **Integration risk** ” external systems constrain design. Signals: legacy, quirky APIs, backward compat.
- **AI-model risk** ” agent likely to hallucinate. Signals: no training data, undocumented APIs.

Risk types drive strategy selection and checkpoint tightness.

---

## Checkpoint granularity

Matches kanban scope levels ” pick the coarsest that still gives you confidence:

- **Per skill** ” after each skill completes on a ticket; finest; use for high uncertainty or early work
- **Per story** ” after all skills complete on a story-scope ticket
- **Per sprint** ” after all skills complete on a sprint-scope ticket (specification / engineering)
- **Per increment** ” after all skills complete on an increment-scope ticket (discovery / exploration)
- **Per stage** ” after the stage exit gate passes; use for well-understood, repeatable work

Default: start per-skill, relax as confidence builds.

---

## Scatter rules

### Default heuristics

- **all â†’ increment** ” one ticket per increment from thin-slicing; scatter all
- **increment â†’ sprint** ” group 3“4 stories per sprint; scatter next 1“2 increments JIT
- **sprint â†’ story** ” rare; only if strategy requires per-story tickets

### User overrides

- "Divide increment 1 into 3 sprints, increment 2 into 5 sprints"
- "Scatter all increments now"
- "Only scatter next 2"
- "Leave later increments until we know more"
- "Increment 1 sprint 1: story 1 then 2 then 3" (specific ordering)

### AI error rate adjustment

When AI output error rate is high (>10%):
- Shrink scope: move from increment-level to sprint-level or story-level
- Tighten checkpoints to per-skill

When error rate is low (<5%):
- Expand scope: move from sprint to increment across flows
- Relax checkpoints to per-stage

---

## Strategy file structure

Each strategy file in `reference/strategies/` defines:

- **When to use** ” context signals and risk types that match this strategy
- **Typical scope** ” what boundary or area this applies to
- **Kanban board stages** ” stages, scope per stage, skills per stage (or reference to default)
- **Scatter rules** ” how tickets decompose at scope boundaries
- **Sprint grouping** ” stories per sprint, grouping heuristics
- **JIT policy** ” how far ahead to decompose
- **Checkpoint policy** ” where to stop for feedback
- **Key constraints** ” non-negotiable rules for this strategy

See **[strategy-catalog.md](strategy-catalog.md)** for all available strategies.
