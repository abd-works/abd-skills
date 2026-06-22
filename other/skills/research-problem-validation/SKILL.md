---
name: research-problem-validation
description: >-
  Research whether a stated problem is real and worth solving. Searches online
  and model knowledge for who is talking about the problem, who says it is NOT
  a problem, competing problems in the same space, and the maturity of
  discourse. Use when validating a hypothesis, checking if a problem is
  well-established, or when the user asks "is anyone else seeing this?"
---
# research-problem-validation

## Purpose

Given a problem statement (usually extracted from a hypothesis), determine
whether the problem is **real, recognized, and worth solving** — using
external evidence only.

## Knowledge sources — strict priority

1. **Web search** — current articles, blog posts, conference talks, research papers, tool docs, community discussions.
2. **Model knowledge** — training data on industry practices, published frameworks, well-known tooling.
3. **NEVER** the user's own codebase, skills, or prior solutions — unless the user explicitly asks you to reference their work for comparison (and even then, treat it as "what they are doing," not "what is correct").

## Instructions

### Input

A **problem statement** in plain language. Usually the Y in "I believe X will solve Y for Z."

### Research steps

1. **Problem signal scan**
   - Search for the problem using multiple phrasings (technical, business, community).
   - Identify **who** is discussing it: companies, practitioners, researchers, open-source communities.
   - Capture volume and recency — is this a 2024-2026 conversation or a 2018 blog post?

2. **Counter-signal scan**
   - Actively search for people who say this is **not** a problem, or that it is overstated.
   - Capture their reasoning. If the counter-argument is strong, surface it prominently.
   - Note if the "problem" is actually a symptom of a different root problem.

3. **Competing problems**
   - In the same domain, what **other** problems are people prioritizing?
   - Is the stated problem competing for attention with adjacent or overlapping concerns?
   - Are people grouping it under a larger umbrella problem?

4. **Maturity assessment**
   - Is this an emerging concern (few voices, mostly opinion) or a mature, widely-acknowledged challenge (industry reports, tooling built around it)?
   - Rate maturity: **Emerging** / **Growing** / **Established** / **Commoditized**.

### Output

Produce a structured section for the research report:

```
## Problem Validation: [problem in ~10 words]

### Signal
- [Who is talking about it, with citations]
- [Volume / recency of discussion]

### Counter-signal
- [Who disagrees or deprioritizes, with citations]
- [Strength of counter-argument: weak / moderate / strong]

### Competing problems
- [Adjacent problems people prioritize instead]
- [Overlap or umbrella relationships]

### Maturity: [Emerging | Growing | Established | Commoditized]
[Brief justification]
```

### Stance

- **Cite sources.** Every claim about what "others are doing" must link to a real article, repo, talk, or tool.
- **Do not flatter.** If the problem is niche or contested, say so plainly.
- **Do not assume the user's framing is correct.** If the real problem is different from what they stated, say that.
