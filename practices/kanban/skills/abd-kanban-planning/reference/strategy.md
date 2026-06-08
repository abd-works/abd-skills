# Strategy

A **strategy** defines how work flows through the kanban board:

- **Scope progression** â€” which scope levels apply at each stage (may differ from default)
- **Scatter rules** â€” when and how to decompose tickets at scope boundaries
- **Sprint grouping** â€” how to group stories into sprints (default 3â€“4, adjustable)
- **JIT policy** â€” how far ahead to scatter (next 1â€“2 items by default)
- **Checkpoint policy** â€” where to stop for feedback (per skill, per stage, per increment)
- **Risk classification** â€” which risks are present and how they affect ordering

---

## Why Kanban Planning

Agents benefit from an explicit delivery lifecycle: not just *what* to do next, but **when scope changes**, **when to scatter**, **how to group work**, and **when to stop for feedback**. The strategy + kanban board provide the spine without pre-planning every assignment.

- **Uncertainty is real** â€” keep the strategy living; update when corrections accumulate.
- **Risk before volume** â€” order increments so the hardest unknowns fail early.
- **JIT over pre-plan** â€” decompose only when needed, not everything upfront.
- **Humans in the loop** â€” checkpoint policy makes confirmation predictable.

---

## Risk classification

Classify risks to inform strategy selection:

- **Value risk** â€” building the wrong thing. Signals: vague briefs, no research, conflicting goals.
- **Technical risk** â€” wrong tech, infra, or architecture. Signals: proprietary APIs, unfamiliar stacks, scale unknowns.
- **Delivery risk** â€” miss schedule or quality bar. Signals: large scope, dependencies, deadlines.
- **Domain risk** â€” misunderstand business rules. Signals: regulatory regimes, complex rules, jargon.
- **Integration risk** â€” external systems constrain design. Signals: legacy, quirky APIs, backward compat.
- **AI-model risk** â€” agent likely to hallucinate. Signals: no training data, undocumented APIs.

Risk types drive strategy selection and checkpoint tightness.

---

## Checkpoint granularity

Matches kanban scope levels â€” pick the coarsest that still gives you confidence:

- **Per skill** â€” after each skill completes on a ticket; finest; use for high uncertainty or early work
- **Per story** â€” after all skills complete on a story-scope ticket
- **Per sprint** â€” after all skills complete on a sprint-scope ticket (specification / engineering)
- **Per increment** â€” after all skills complete on an increment-scope ticket (discovery / exploration)
- **Per stage** â€” after the stage exit gate passes; use for well-understood, repeatable work

Default: start per-skill, relax as confidence builds.

---

## Scatter rules

### Default heuristics

- **all â†’ increment** â€” one ticket per increment from thin-slicing; scatter all
- **increment â†’ sprint** â€” group 3â€“4 stories per sprint; scatter next 1â€“2 increments JIT
- **sprint â†’ story** â€” rare; only if strategy requires per-story tickets

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

- **When to use** â€” context signals and risk types that match this strategy
- **Typical scope** â€” what boundary or area this applies to
- **Kanban board stages** â€” stages, scope per stage, skills per stage (or reference to default)
- **Scatter rules** â€” how tickets decompose at scope boundaries
- **Sprint grouping** â€” stories per sprint, grouping heuristics
- **JIT policy** â€” how far ahead to decompose
- **Checkpoint policy** â€” where to stop for feedback
- **Key constraints** â€” non-negotiable rules for this strategy

See **[strategy-catalog.md](strategy-catalog.md)** for all available strategies.
