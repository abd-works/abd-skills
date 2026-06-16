# Rule: All collaborators accounted for

**Scanner:** Manual review

A passing model accounts for every collaborator from the Domain Language — each appears as a method parameter, return type, property type, or indented collaborator under a method. If a collaborator is intentionally excluded, a decision record explains why. A failing model has UL collaborators that appear nowhere in the model with no recorded rationale.

## DO

UL says `Board` collaborates with: Stage, Ticket, StageBucketLayout, WipPolicy

```markdown
### **Board**

Board(StageBucketLayout)
------
layout: StageBucketLayout
----
advance(Ticket, Stage): Ticket
	WipPolicy
```

- `StageBucketLayout` → property type and constructor param
- `Ticket` → method parameter and return type
- `Stage` → method parameter
- `WipPolicy` → indented collaborator

All four accounted for.

## DO NOT

UL says `Board` collaborates with: Stage, Ticket, StageBucketLayout, WipPolicy

```markdown
### **Board**

Board(StageBucketLayout)
------
layout: StageBucketLayout
----
advance(Ticket): Ticket
```

Where is `Stage`? Where is `WipPolicy`? Two collaborators from the UL are missing with no decision record explaining the exclusion.

**Source:** Engagement convention (domain-model skill).
