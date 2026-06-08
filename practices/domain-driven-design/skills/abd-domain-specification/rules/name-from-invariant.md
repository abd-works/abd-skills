# Rule: Name operations after their invariant

**Scanner:** Manual review

When the right name for an operation is unclear, name it after the invariant. The invariant is already the correct domain statement of what the operation does — the name should match it directly rather than inventing a separate abstract label.

## DO NOT

Invent a name that describes *how* the operation works or uses vague process words.

```
- applySupersession(...)
- handleSameSourceConflict(...)
- incomingIsBlocked(...)
```

These names either describe internal mechanics or encode the answer from the wrong perspective. A reader cannot tell what the operation asserts.

## DO

Read the invariant and use its subject-verb as the name.

Invariant: *"if incoming supersedes existing — remove existing, return true"*

```
- incomingSupersedes(existing: ImposedCondition, incoming: Condition): Boolean
	Invariant: if incoming supersedes existing — remove existing, return true; if existing supersedes incoming — return false
```

The name *is* the invariant's claim. The invariant then fills in the detail.

## Guidance

- This applies especially to private Boolean helpers — they answer a yes/no question about a domain rule. Name the question from the domain, not from the implementation.
- The invariant should not repeat the name verbatim — it adds precision (edge cases, side effects, return value meaning).
- If the invariant is still hard to summarise in a name, that is a signal the invariant itself needs to be sharpened first.
