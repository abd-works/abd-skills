# Rule: Extract complex logic to named operation

**Scanner:** Manual review

A passing model extracts complex internal logic into a separate named private method rather than leaving it implicit inside a public method. Each method does one clear thing. A failing model leaves multi-step logic buried inside a single method with no visible decomposition.

## DO

```markdown
### **StageBucketLayout**

----
advance(Ticket, Stage): Stage
	-validateStageOrder(Stage, Stage): Stage
	-enforceWipLimit(Stage): Stage
	Invariant: target stage must follow current stage
	Invariant: WIP limit must not be exceeded
-validateStageOrder(Stage, Stage): Stage
-enforceWipLimit(Stage): Stage
```

The complex logic of `advance` is decomposed into two named private operations. Each does one thing.

## DO NOT

```markdown
### **StageBucketLayout**

----
advance(Ticket, Stage): Stage
	Invariant: target stage must follow current stage
	Invariant: WIP limit must not be exceeded
	Invariant: stage must exist in layout
	Invariant: ticket must not be blocked
	Invariant: concurrent advances must be serialized
```

Five invariants on one method with no decomposition. The method is doing too much. Extract the distinct concerns into named operations.

**Source:** Engagement convention (domain-model skill).
