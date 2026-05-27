# Rule: Invariants without interactions

**Scanner:** Manual review

An operation that carries multiple invariants must also carry an `Interaction:` block. Invariants declare *what must be true* — they cannot replace the step-chain that *makes it true*. Several invariants are a reliable signal that the operation is performing real internal work; that work must be made explicit.

## DO NOT

Write multiple invariants with no interaction block.

```
+ resolve(): CheckResult
	Invariant: shape is always rollTotal vs dc.value
	Invariant: subtypes vary only how total or DC is produced
	Invariant: natural 20 always yields a critical success
```

These constraints hint at internal calculations (rolling a die, summing a total, comparing to DC) that are nowhere shown. A reader cannot tell how the result is produced.

## DO

Follow every multi-invariant operation with an `Interaction:` block that shows the steps that satisfy those invariants.

```
+ resolve(): CheckResult
	Invariant: shape is always rollTotal vs dc.value; subtypes vary only how total or DC is produced
	Interaction:
		roll: Integer = d20.roll()
		total: Integer = trait.rank + roll + circumstanceModifier.value
		success: Boolean = total >= dc.value
		margin: Integer = total - dc.value
		result: CheckResult = new CheckResult(rollTotal: total, dc: dc, isSuccess: success, margin: margin)
		return result
```

Now the invariants are backed by visible steps — the reader can see exactly how `rollTotal`, `dc`, and `isSuccess` are produced.

## Guidance

- A single invariant on a simple setter or guard is fine without an interaction block.
- Two or more invariants — especially ones describing how values are derived or compared — require an `Interaction:` block.
- When in doubt: if the invariants collectively describe a *process*, the process belongs in `Interaction:`.
