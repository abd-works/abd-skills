# Rule: Collection class for managed groups

**Scanner:** Manual review

A passing model introduces a named collection class when a concept owns multiple related objects AND the collection has behavior beyond mere containment (ordering, filtering, capacity rules, invariants). A failing model embeds collection logic into the owning class or uses raw collection types.

## DO

A Board owns Stages in a defined order with WIP limits per stage:

```markdown
### **StageBucketLayout**

StageBucketLayout(Stage)
------
stages: Stage
	Invariant: stages are ordered and non-empty
----
stageAt(Position): Stage
advance(Ticket, Stage): Stage
	Invariant: target stage must follow current stage in order
```

The collection behavior (ordering, positional access, advancement rules) lives in `StageBucketLayout`, not in `Board`.

## DO NOT

Embedding collection logic in the owner:

```markdown
### **Board**

Board(Stage)
------
stages: Stage
----
getStageAt(Position): Stage
advanceTicket(Ticket, Stage): Stage
reorderStages(Stage): Board
validateWipLimit(Stage): Boolean
```

The Board is now doing collection management. These are stage-ordering concerns, not board concerns.

**Source:** Engagement convention (domain-model skill).
