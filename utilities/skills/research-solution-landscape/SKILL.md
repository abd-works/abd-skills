---
name: research-solution-landscape
description: >-
  Map the landscape of competing solutions for a validated problem. Searches
  online and model knowledge for categories of approaches, key tools and
  frameworks, trade-offs, and which segments each solution targets. Use when
  the user wants to know how others are solving a problem, what the major
  approaches are, or needs a solution taxonomy before choosing a direction.
---
# research-solution-landscape

## Purpose

Given a validated problem, map **how people are actually solving it** — the
categories of solutions, concrete tools and practices, and how they differ.

## Knowledge sources — strict priority

1. **Web search** — current tools, frameworks, open-source projects, SaaS products, published architectures, case studies.
2. **Model knowledge** — well-known patterns, industry-standard approaches, published comparisons.
3. **NEVER** the user's own codebase or solutions as a source of "how to do it." Only reference user's work when explicitly asked, and then only as one data point alongside external approaches.

## Instructions

### Input

A validated problem statement (output from **research-problem-validation**) or
a problem the user states directly.

### Research steps

1. **Solution category scan**
   - Identify the **major categories** of approaches. Not individual tools — categories of thinking.
   - Example: for "agentic vs orchestration" the categories might be: multi-agent frameworks, workflow orchestration engines, fine-grained skill/tool composition, monolithic prompt chains.
   - Name each category clearly. Use the terminology the community uses, not invented labels.

2. **Key players per category**
   - For each category, list concrete tools, frameworks, or projects.
   - Note adoption signals: GitHub stars, commercial backing, conference mentions, community size.
   - Capture recency — is this actively maintained or abandoned?

3. **Trade-off analysis**
   - For each category, identify:
     - **Strengths** — what it does well, what problems it solves cleanly.
     - **Weaknesses** — where it breaks down, what it forces you to handle.
     - **Assumptions** — what it assumes about your environment, team, scale.
   - Be specific. "It's flexible" is not a trade-off. "It requires you to define explicit state transitions for every agent handoff" is.

4. **Segment fit**
   - Which categories serve which types of users?
   - Solo developer vs. team? Startup vs. enterprise? Experimental vs. production?
   - What's the typical adoption path — do people start with one category and migrate to another?

5. **Momentum and direction**
   - Which categories are gaining traction? Which are losing?
   - Are there convergence patterns (e.g., orchestration tools adding agent capabilities)?
   - What does the trajectory suggest for the next 6-12 months?

### Output

Produce a structured section for the research report:

```
## Solution Landscape: [problem in ~10 words]

### Categories

#### [Category Name]
- **Approach:** [1-2 sentence description]
- **Key players:** [tools/frameworks with links]
- **Strengths:** [specific advantages]
- **Weaknesses:** [specific disadvantages]
- **Best for:** [segment / use case fit]
- **Momentum:** [Rising | Stable | Declining]

[Repeat per category]

### Convergence patterns
- [Where categories are blurring or merging]

### Adoption paths
- [Typical journey: start here → migrate to here as needs grow]
```

### Stance

- **Breadth before depth.** Map the full landscape before drilling into any one solution.
- **Cite sources.** Tools, repos, articles, talks — every claim needs a reference.
- **No favorites.** Present trade-offs neutrally. The user decides, not the advisor.
- **Name the elephants.** If one category dominates and the user's approach doesn't fit it, say so.
