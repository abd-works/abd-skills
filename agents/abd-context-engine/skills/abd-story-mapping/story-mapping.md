# Story Map Format

## Hierarchy

Each node is an interaction. Epic → Sub-Epic (or Epic) → Story → Scenario → Step. Epics can nest (epic children = sub-epics).


| Node     | Meaning                                                                                                                                                                                                                       | Heading                                    |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| Epic     | Large domain capability — a major area of the system. Groups stories; statement = scope (broad flows), not a single interaction.                                                                                              | `# Epic: <name> (<statement>)`             |
| Sub-Epic | An epic whose parent is an epic; logical grouping of related stories — a feature area, not a behavior itself.                                                                                                                 | `## Epic: <name> (<statement>)`            |
| Story    | Smallest independently valuable behavior — has a triggering actor, a responding actor, and produces observable state change. If it has no actor and no state change, it is not a story. Statement = one trigger and response. | `### Story: <name> (<statement>)`          |
| Scenario | Condition-specific grouping of steps within a story (e.g. success path, failure path). Names describe conditions tested.                                                                                                      | `#### Scenario: <name>`                    |
| Step     | Atomic interaction — one action by one actor. When/Then: Trigger as When, Response as Then.                                                                                                                                   | `- Step N: <name> (When/Then <statement>)` |
