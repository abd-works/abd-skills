# Rule: Every behavior has a backing method

**Scanner:** Manual review

A passing model maps every behavior bullet from the Domain Language to at least one property or method. Noun phrases become properties; verb phrases become methods. A failing model leaves UL behaviors unrepresented — no property, no method, no trace.

## DO

UL behavior bullets for `Board`:
- "holds tickets in stages"
- "advances a ticket to the next stage"
- "current stage layout"

```markdown
### **Board**

Board(StageBucketLayout)
------
stageLayout: StageBucketLayout
----
advance(Ticket): Ticket
	Stage
```

- "holds tickets in stages" → property `stageLayout`
- "advances a ticket" → method `advance`
- "current stage layout" → property `stageLayout`

## DO NOT

Leaving a behavior unmapped:

UL says `Board` "rejects tickets that violate WIP limits" but the model shows:

```markdown
### **Board**

Board(StageBucketLayout)
------
stageLayout: StageBucketLayout
----
advance(Ticket): Ticket
```

No method or invariant captures "rejects tickets that violate WIP limits." The behavior is lost.

**Source:** Engagement convention (domain-model skill).
