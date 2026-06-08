# Selecting a strategy

See **[strategy.md](strategy.md)** for what a strategy is and **[strategy-catalog.md](strategy-catalog.md)** for available options.

---

## Step 1 â€” Context analysis

Read all context. Identify:

1. **Known domains** â€” strong training data, documented APIs.
2. **Risky domains** â€” proprietary, internal, novel logic.
3. **Integration points** â€” external systems, dependencies.
4. **Complexity drivers** â€” regulatory, multi-actor, concurrency.
5. **Existing assets** â€” prior story graphs, specs, tests, code.

## Step 2 â€” Select strategy

1. Open `reference/strategies/` in this skill folder.
2. Read each strategy's **When to use** section.
3. Match context and risks to a strategy (or blend multiple).
4. If no strategy fits, design custom â€” offer to save later.

## Step 3 â€” Configure kanban board stages

From the selected strategy, write `kanban.json` (the kanban board stage configuration):

- Which stages are active
- Scope level per stage
- Ordered stage work required per stage with delivery role assignments
- Any optional skills (marked in strategy)

## Step 4 â€” Define scatter and decomposition rules

Write the `strategy` section in `kanban.json` with:

- **Scatter rules**: which scope transitions scatter vs advance, sprint grouping (default 3â€“4), JIT policy
- **Ordering**: priority source (story map, user override, risk-first)
- **Checkpoint policy**: per-skill, per-stage, or per-increment
- **Autonomy**: tight, moderate, or full

## Step 5 â€” Present and confirm

Present to user:

1. Context assessment and classified risks.
2. Selected strategy (name, from which file, adaptations).
3. Kanban board stage configuration (stages, scope, skills).
4. Scatter rules and checkpoint policy.

**CHECKPOINT.** Wait for user confirm before setup.
