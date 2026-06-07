# Rule: Collaborators before invariants

**Scanner:** Manual review

A passing model lists collaborators before invariants when both appear under a method. Both are tab-indented. A failing model places invariants before collaborators or mixes the ordering inconsistently.

## DO

```markdown
----
advance(Stage): Ticket
	StageBucketLayout
	WipPolicy
	Invariant: cannot advance past final stage
	Invariant: WIP limit must not be exceeded
```

Collaborators (`StageBucketLayout`, `WipPolicy`) appear first. Invariants follow.

## DO NOT

```markdown
----
advance(Stage): Ticket
	Invariant: cannot advance past final stage
	StageBucketLayout
	Invariant: WIP limit must not be exceeded
	WipPolicy
```

Invariants and collaborators are interleaved. Collaborators must come before invariants, as a group.

```markdown
----
advance(Stage): Ticket
	Invariant: cannot advance past final stage
	Invariant: WIP limit must not be exceeded
	StageBucketLayout
	WipPolicy
```

All invariants before all collaborators — also wrong. Collaborators first.

**Source:** Engagement convention (domain-model skill).
