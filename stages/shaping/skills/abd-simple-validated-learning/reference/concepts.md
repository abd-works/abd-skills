# Simple Validated Learning — Concepts

## What "simple" means here

- **Simple** = **small** batch of tests, **clear** pass/fail or strong signal, **named** owners — not a full research programme.
- This skill is **not** a substitute for **legal sign-off**, **formal** market research, or **production** analytics ownership; it **aligns** the team on what to **try next** to reduce uncertainty.
- **Discovery-first:** Prefer **weeks** (or **days**) of **targeted** learning over **quarters** of build before the **first** risky belief is checked.

---

## The method

### 1. Mine assumptions

The source artefact may already have explicit assumptions listed; if so, start there. If not, read the artefact for claims about customers, value, feasibility, and economics that have not been verified and extract them. Flag **high-risk** assumptions — those the whole case depends on — for priority attention.

### 2. Convert to hypotheses

For each item: *We believe …* → **We expect** that … **We will be wrong if** … (observable, **falsifiable**). One hypothesis can map to more than one test; merge duplicates.

### 3. Backlog prioritise

Order by **magnitude of uncertainty** and **impact of being wrong** vs **effort to test** (cheapest high-risk first when sensible). Mark **MUST learn before build** vs **can learn as part of build**.

### 4. Plan / Validate / Learn

For each **prioritised** item, define all of the following:

- **Belief** — what assumption are we testing, stated as something that could be wrong?
- **Hypothesis** — *We expect that … We will be wrong if …* (observable, falsifiable).
- **Plan** — what is the smallest activity that could change our mind? Include method (research, SME session, interview, prototype, pilot), timebox, and cohort or data source.
- **Validate** — what evidence will you collect, from whom or where, and what counts as a pass or fail signal?
- **Owner and date** — who is accountable and by when?
- **Learn** — what decision or model update follows: refine, pivot, kill, or proceed to a larger experiment?

### 5. Checklist pass

Skim the **multi-area** risk questions to ensure you did not only test the obvious area: cover problem/solution fit, capability/market, technology, delivery, and other feasibility areas.

---

## Input sources

Assumptions can come from anywhere — an opportunity canvas, an impact map, a cost-of-delay estimate, a journey map, a business case, or a workshop. This skill does not care about the source artefact; it cares about the assumptions themselves and whether the team is testing the right ones before committing to build.

First, check whether the source is **assumption-aware**: does it already have assumptions listed explicitly, or does it include an approach or framework for mining them (e.g. explicitly named assumptions, risk checklists, hypothesis sections)? If yes, start from what is already named. If not, treat the whole artefact as raw material and mine it for unverified claims.

---

## Discovery emphasis

This skill emphasises **up-front discovery and validation**: research, analysis, assessing current and target state (e.g. operations, finances, systems), validation with SMEs, deep dives, quick prototypes, cohort tests, and other relatively cheap validation activities. A longer build–measure–learn loop belongs in delivery practices once the team is shipping increments.
