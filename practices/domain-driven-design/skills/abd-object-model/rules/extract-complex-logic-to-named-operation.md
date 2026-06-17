# Rule: Extract complex sub-logic to a named operation

**Scanner:** Manual review

An `Interaction:` block traces the key collaborations of an operation — it is not pseudocode. When a branch or calculation inside an interaction is non-trivial, extract it into a named operation with an invariant describing the rule. Call that operation from the interaction instead of expanding every line inline.

## DO NOT

Spell out multi-step branching logic inside an interaction block.

```
+ resolve(): CheckResult
	Interaction:
		...
		if activeResult.margin != 0: return activeResult
		// exact tie: higher rank bonus wins
		if trait.rank.value > opposingTrait.rank.value: return activeResult
		if opposingTrait.rank.value > trait.rank.value: return opposingResult
		// rank tie: d20 decides (1–10 active wins, 11–20 opposing wins)
		tieBreak: Integer = new D20().roll()
		activeWins: Boolean = tieBreak <= 10
		return activeWins ? activeResult : opposingResult
```

The tie-breaking procedure is a domain rule in its own right. Burying it inside the interaction makes both operations harder to read and obscures the rule.

## DO

Give the sub-logic a domain name, extract it as a separate operation, and describe the rule as its invariant. Call it from the interaction.

```
+ resolve(): CheckResult
	Interaction:
		...
		if activeResult.margin != 0: return activeResult
		return resolveTie(activeResult: activeResult, opposingResult: opposingResult)
- resolveTie(activeResult: CheckResult, opposingResult: CheckResult): CheckResult
	Invariant: higher rank bonus wins; if ranks are equal, d20 decides (1–10 active wins, 11–20 opposing wins)
```

The interaction stays high-level. The tie-breaking rule is declared precisely where it lives and is independently readable.

## Guidance

- If you find yourself writing more than two or three conditional branches inside a single `Interaction:` block, that is a signal to extract.
- The extracted operation's invariant replaces the inline comments — it is the authoritative statement of the rule.
- The name of the extracted operation should come from domain language, not from implementation vocabulary (`resolveTie`, not `handleTieCase` or `processTieBreaker`).
