# Rule: No raw String types

**Scanner:** Manual review

A passing model uses domain types, constrained enums, or typed primitives for every property and parameter. A failing model uses raw `String` (or `Number`, `Boolean`) where a named domain type should exist.

## DO

```markdown
------
name: AgentName
stage: StageName
scope: ScopeLevel
startedAt: Timestamp
path: FilePath
identifier: TicketIdentifier
description: FreeText
----
rename(AgentName): Agent
moveTo(StageName): Ticket
```

Every type communicates its domain meaning: `AgentName`, `StageName`, `ScopeLevel`, `Timestamp`, `FilePath`, `TicketIdentifier`, `FreeText`.

## DO NOT

```markdown
------
name: String
stage: String
scope: String
startedAt: String
path: String
identifier: String
description: String
----
rename(String): Agent
moveTo(String): Ticket
```

Seven properties and two parameters, all `String`. What kind of string? A name? A path? A timestamp? A scope level? The model communicates nothing about the domain.

**Source:** Engagement convention (domain-model skill).
