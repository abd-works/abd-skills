# Rule: Shared responsibility inheritance requires Liskov

**Scanner:** Manual review

A passing model only uses inheritance (`Child : Parent`) when the child can be substituted wherever the parent is used without violating the parent's contract. A failing model uses inheritance for convenience when the subtype breaks the base contract — requiring composition or a sibling type instead.

## DO

`ScoringStrategy` defines `score(Evidence): Score`. Both `WeightedScoring` and `SimpleScoring` honor that contract — any caller expecting a `ScoringStrategy` can use either subtype:

```markdown
### **ScoringStrategy**

ScoringStrategy(StrategyName)
------
name: StrategyName
----
score(Evidence): Score

### **WeightedScoring : ScoringStrategy**

WeightedScoring(StrategyName, Weight)
------
weight: Weight
----
score(Evidence): Score
	Criterion
```

`WeightedScoring` substitutes cleanly for `ScoringStrategy` everywhere.

## DO NOT

A subtype that violates the base contract:

```markdown
### **ReadOnlyBoard : Board**

------
----
advance(Ticket): Ticket
	Invariant: always throws — read-only boards cannot advance
```

If `Board` promises `advance` works and `ReadOnlyBoard` always rejects it, substitution fails. This is not a true subtype. Use composition or a sibling type (`BoardSnapshot`) instead.

**Source:** Engagement convention (domain-model skill).
