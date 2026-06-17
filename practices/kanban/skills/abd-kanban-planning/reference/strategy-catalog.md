# Strategy catalog

## Available strategies

- **[new-user-story.md](./strategies/new-user-story.md)** ” 1“3 stories on existing solution
- **[new-thin-slice.md](./strategies/new-thin-slice.md)** ” vertical slice (~5“15 stories)
- **[new-initiative-no-documented-architecture.md](./strategies/new-initiative-no-documented-architecture.md)** ” greenfield; no architecture
- **[new-initiative-proprietary-technology-risk.md](./strategies/new-initiative-proprietary-technology-risk.md)** ” proprietary/undocumented systems
- **[new-initiative-business-user-experience-risk.md](./strategies/new-initiative-business-user-experience-risk.md)** ” UX/domain risk dominant
- **[brownfield-current-state.md](./strategies/brownfield-current-state.md)** ” map and test existing system
- **[legacy-migration.md](./strategies/legacy-migration.md)** ” replace system; legacy is truth
- **[regulatory-compliance-heavy.md](./strategies/regulatory-compliance-heavy.md)** ” regulation/compliance dominates
- **[bug-fix.md](./strategies/bug-fix.md)** ” defect or regression
- **[spike-proof-of-concept.md](./strategies/spike-proof-of-concept.md)** ” answer one question before delivery

## Adding a strategy

After a custom engagement, save a new `<slug>.md` in `reference/strategies/` with the same sections. Reference bootcamp stages and scope levels. Include scatter rules and sprint grouping heuristics.

## Adapting a strategy

When selecting a strategy, adapt it:

1. **Add/remove stages** ” bug fix skips shaping; spike skips engineering.
2. **Add/remove skills** ” brownfield adds module partition; UX-heavy adds IA.
3. **Change scope levels** ” if stories are huge, add sub-story scope.
4. **Override sprint grouping** ” "2 stories per sprint for this complex area."
5. **Change JIT policy** ” "scatter all increments now, we know the domain."
6. **Adjust checkpoints** ” "per-skill for increment 1, per-stage after."
