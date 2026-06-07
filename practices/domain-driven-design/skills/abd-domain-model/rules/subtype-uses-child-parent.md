# Rule: Subtype uses Child : Parent notation

**Scanner:** Manual review

A passing subtype heading uses `### **ChildClass : ParentClass**` and lists only delta members — properties and methods that the child adds or overrides. A failing file repeats inherited members or uses any other notation for inheritance.

## DO

```markdown
### **WeightedScoring : ScoringStrategy**

WeightedScoring(Weight, Criterion)
------
weight: Weight
----
score(Evidence): Score
	Criterion
```

Only the new `weight` property and overridden `score` method appear. Members inherited from `ScoringStrategy` are omitted.

## DO NOT

```markdown
### **WeightedScoring**

WeightedScoring(Weight, Criterion)
------
name: StrategyName       ← inherited, should not appear
weight: Weight
----
evaluate(Evidence): Score   ← inherited, should not appear
score(Evidence): Score
```

Do not omit the parent from the heading:

```markdown
### **WeightedScoring**
```

Do not use UML-style markers for inheritance:

```markdown
### **WeightedScoring** << extends ScoringStrategy >>
```

**Source:** Engagement convention (domain-model skill).
