# Strategy: Legacy Migration

**When to use:** Replacing or rewriting an existing system; **legacy behavior is truth**. Backward compatibility, data migration, phased cutover.

**Typical scope:** Grouped by existing boundaries (endpoints, modules, domains).


| Step | Stage | Intent | Scope | Checkpoint policy | Rationale |
| ---- | ----- | ------ | ----- | ----------------- | --------- |
| 1 | Discovery | **Anchor the map to reality:** epics and **thin slices last** from APIs, schema, manuals, existing tests — legacy **is** the spec | Per boundary (endpoint group, module) | **Per boundary**: confirm **contracts** before continuing | Wrong map means wrong migration |
| 2 | Exploration → Engineering | **Contract from legacy:** AC matches current behavior; **acceptance tests pass against the old system** before new implementation | First endpoint group or module | Per-AC / per-test | Safety net: tests encode legacy truth |
| 3 | Engineering | **First implementation** on the new stack so the **same** tests pass against the new system | First module/service | Per endpoint or service | Proves pattern for the rest |
| 4+ | Exploration → Engineering | **Repeat:** AC from legacy → tests → implement new — per module | Remaining modules | Per-module; review against earlier patterns | Systematic rollout |


**Key constraints:**

- Tests against the old system are mandatory before new behavior is trusted.
- Behavioral deltas vs legacy need explicit approval.
- Data migration is its own slice — do not mix casually with behavioral migration.
- No tests on legacy → first priority is characterizing behavior with tests, not shipping new code.
