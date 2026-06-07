# Rule: Name from invariant

**Scanner:** Manual review

A passing model names methods after the invariant they enforce when the right name is unclear. The invariant is the correct domain statement — the method name should match it directly. A failing model uses vague or technical names when a clear invariant exists to guide naming.

## DO

Invariant: "WIP limit must not be exceeded"

```markdown
----
enforceWipLimit(Stage, Ticket): Stage
	Invariant: WIP limit must not be exceeded
```

Invariant: "only qualified agents may be assigned"

```markdown
----
requireQualification(Agent, Skill): Agent
	Invariant: only qualified agents may be assigned
```

The method name mirrors the invariant it protects.

## DO NOT

```markdown
----
check(Stage, Ticket): Stage
	Invariant: WIP limit must not be exceeded
```

```markdown
----
process(Agent, Skill): Agent
	Invariant: only qualified agents may be assigned
```

`check` and `process` are meaningless. The invariant says exactly what the method does — use it as the name.

**Source:** Engagement convention (domain-model skill).
