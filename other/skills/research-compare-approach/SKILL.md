---
name: research-compare-approach
description: >-
  Critically compare the user's approach against researched alternatives.
  Identifies strengths, weaknesses, trade-offs, and legitimate white space.
  Reads the user's codebase ONLY to understand what they built — never as a
  source of best practice. Use when the user wants to know how their solution
  stacks up, where they are strong, where they are exposed, or where there is
  genuine white space for their approach.
---
# research-compare-approach

## Purpose

Given a solution landscape (from **research-solution-landscape**) and the
user's own approach, produce a **critical, honest comparison** — not a
validation exercise.

## Knowledge sources — strict priority

1. **External research** — the solution landscape already gathered, plus any deeper dives needed.
2. **User's codebase / skills / agents** — read ONLY to understand **what the user built and how**. Treat this as the subject under review, never as the standard.
3. **Model knowledge** — industry norms, published architectures, known failure modes.

## Instructions

### Input

- The solution landscape (from **research-solution-landscape**).
- The user's approach — described by the user, or discovered by reading their codebase when they ask you to.
- Optionally: 1-2 specific external approaches the user wants to compare against.

### Analysis steps

1. **Classify the user's approach**
   - Which solution category (from the landscape) does it fit?
   - If it spans categories or doesn't fit cleanly, name that explicitly.
   - What assumptions does it make about environment, team, scale?

2. **Strengths — be specific, not generous**
   - What does the user's approach do that the alternatives don't?
   - Is the strength inherent to the design, or incidental?
   - Would an external reviewer recognize this as a genuine advantage?
   - Only count it as a strength if external evidence supports the value.

3. **Weaknesses — be direct, not diplomatic**
   - Where does the user's approach fall behind the established alternatives?
   - What risks does it carry that the alternatives have already solved?
   - What would break first at scale, in a team, or in production?
   - If the user has reinvented something that already exists (and the existing version is better), say so.

4. **Trade-off map**
   - For each dimension that matters (complexity, flexibility, maintenance, learning curve, community support, longevity), score the user's approach against 1-2 alternatives.
   - Use a simple scale: **Stronger / Comparable / Weaker** — with justification.

5. **White space analysis**
   - Is there legitimate white space — a real need that no existing solution covers well, where the user's approach genuinely adds value?
   - Distinguish between white space (unmet need) and gap (the user hasn't caught up yet).
   - If there is no white space, say so. Do not manufacture uniqueness.

6. **Recommendation**
   - Given the comparison, what should the user consider?
   - Options: double down on white space, adopt an existing approach, hybridize, or pivot.
   - Be honest about sunk cost — if the user has invested heavily in a direction that the landscape doesn't support, name it.

### Output

Produce a structured section for the research report:

```
## Approach Comparison: [user's approach] vs [alternative(s)]

### Classification
- **User's approach fits:** [category from landscape]
- **Key assumptions:** [what the approach depends on]

### Strengths
- [Strength with evidence]

### Weaknesses
- [Weakness with evidence]

### Trade-off map

| Dimension | User's approach | [Alternative A] | [Alternative B] |
|-----------|----------------|-----------------|-----------------|
| Complexity | ... | ... | ... |
| Flexibility | ... | ... | ... |
| Community/support | ... | ... | ... |
| Production-readiness | ... | ... | ... |

### White space
- [Genuine unmet need the user addresses — or "none identified"]

### Recommendation
[Direct, actionable guidance. Not flattery.]
```

### Stance

- **Your role is impartial advisor, not cheerleader.** The user explicitly asked you to be critical.
- **Cite external evidence** for every claim about what alternatives do better or worse.
- **Name sunk-cost risks.** If the user has gone deep in a direction that the market doesn't validate, say "the evidence suggests X" — don't soften it.
- **White space must be earned.** Only call something white space if you can show that no existing solution covers it AND there is demand for it.
- **Acknowledge what's good.** Being critical doesn't mean ignoring genuine strengths. But strengths need evidence too.
