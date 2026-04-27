---
name: abd-simple-validated-learning
catalog_garden_tier: practice
catalog_garden_order: 17
catalogue_one_liner: >-
  Turn surfaced assumptions into hypotheses, prioritise small tests, and run Plan / Validate / Learn before full build.
description: >-
  Turn surfaced assumptions into falsifiable hypotheses, prioritise small tests, and work each one through Plan, Validate, and Learn before committing to full build.
---
# abd-simple-validated-learning

## Purpose

Opportunities, ideas, and initiatives often carry many unverified assumptions — about customers, value, feasibility, and economics — that the organisation has not yet checked. This skill is for **surfacing those assumptions explicitly** and **working through them** iteratively before the organisation treats them as fact or commits to a full build. The agent (or facilitator) **mines** the supplied context for **assumptions**, rewrites them as **falsifiable hypotheses**, **prioritises** them into a **validation backlog**, and structures each item to move through **Plan → Validate → Learn**.

The skill emphasises **up-front discovery and validation**:research, analysis, assessing current and target state (eg operations, finances, systems) validation with SMEs, deep dives, quick prototypes, cohort tests, and other relatively cheap validation activities. A longer build–measure–learn loop belongs in delivery practices once the team is shipping increments.

Assumptions can come from anywhere — an opportunity canvas, an impact map, a cost of delay estimate, a journey map, a business case, or a workshop. This skill does not care about the source artefact; it cares about the assumptions themselves and whether the team is testing the right ones before committing to build.

## When to use this skill

Load this skill when any of the following apply:

- You have (or are finishing) an **opportunity canvas**, **impact map with hypotheses**, or other model that lists **assumptions** and you need a **prioritised** set of **validation experiments** with owners and dates.
- You want to move from “we believe …” to **I/we expect that …, and we will be wrong if …**, with a **smallest** experiment that could reduce uncertainty.
- You need a **Validated Learning** working pattern (**Plan** / **Validate** / **Learn** or **Plan** / **Build** a *thin* test / **Measure** / **Learn**) aimed at **reducing uncertainty**, not a full product release train.
- The team uses or wants a **Validated Learning Kanban**-style board and a **multi-area** risk pass (problem/solution fit, capability/market, technology, delivery, regulatory/commercial, etc.).
- The user references an **experimentation canvas** (or lean experiment one-pager): use it as a **single-experiment** or **per-hypothesis** view alongside the **backlog** template in this skill.

## Agent instructions

1. **Inputs**
   - Accept whatever context the user provides — a canvas, impact map, cost of delay estimate, journey map, business case, workshop notes, or anything else that describes an opportunity or initiative.
   - First, check whether the source is **assumption-aware**: does it already have assumptions listed explicitly, or does it include an approach or framework for mining them (e.g. explicitly named assumptions, risk checklists, hypothesis sections)? If yes, start from what is already named. If not, treat the whole artefact as raw material and mine it for unverified claims about customers, value, feasibility, and economics.

2. **Build (sequence)**

   1. **Mine assumptions** — The source artefact may already have explicit assumptions listed; if so, start there. If not, read the artefact for claims about customers, value, feasibility, and economics that have not been verified and extract them. Flag **high-risk** assumptions — those the whole case depends on — for priority attention.
   2. **Convert to hypotheses** — For each item: *We believe …* → **We expect** that … **We will be wrong if** … (observable, **falsifiable**). One hypothesis can map to more than one test; merge duplicates.
   3. **Backlog prioritise** — Order by **magnitude of uncertainty** and **impact of being wrong** vs **effort to test** (cheapest high-risk first when sensible). Mark **MUST learn before build** vs **can learn as part of build**.
   4. **Plan / Validate / Learn** — For each **prioritised** item, define all of the following:
      - **Belief** — what assumption are we testing, stated as something that could be wrong?
      - **Hypothesis** — *We expect that … We will be wrong if …* (observable, falsifiable).
      - **Plan** — what is the smallest activity that could change our mind? Include method (research, SME session, interview, prototype, pilot), timebox, and cohort or data source.
      - **Validate** — what evidence will you collect, from whom or where, and what counts as a pass or fail signal?
      - **Owner and date** — who is accountable and by when?
      - **Learn** — what decision or model update follows: refine, pivot, kill, or proceed to a larger experiment?
   5. **Checklist pass** — Skim the **multi-area** risk questions to ensure you did not only test the obvious area: cover problem/solution fit, capability/market, technology, delivery, and other feasibility areas.

3. **Templates**

   | Template | What to produce |
   | -------- | ---------------- |
   | `templates/validated-learning-backlog.md` | Prioritised list + **Plan / Validate / Learn** table (Kanban-style columns in one view). |
   | `templates/experimentation-canvas.md` | One **experiment** per block: belief, method, **success/fail** signal, owner, **by when** — for workshops or a single high-stakes test. |

   Keep **template parity** in spirit: the same experiments appear in the backlog; the **experimentation canvas** can zoom **one** experiment.

4. **Rules**

   After generating, review bundled **`rules/*.md`** (when present) against the outputs. If no rules yet, use **Build** and **Validate** in this file as the bar.

---

## What “simple” means here

- **Simple** = **small** batch of tests, **clear** pass/fail or strong signal, **named** owners — not a full research programme.
- This skill is **not** a substitute for **legal sign-off**, **formal** market research, or **production** analytics ownership; it **aligns** the team on what to **try next** to reduce uncertainty.
- **Discovery-first:** Prefer **weeks** (or **days**) of **targeted** learning over **quarters** of build before the **first** risky belief is checked.

---

## Build

1. Ingest the user’s context (pasted files, path to canvas outputs, or prior chat summary).
2. Produce **validated-learning-backlog** from the sequence in **Agent instructions**; add **experimentation-canvas** only when a **single** experiment needs a full canvas treatment.
3. If the user names **RAG** or **abd-answers**, use **query-pinecone** and fold in only **relevant** chunks; cite per your workspace norm.

---

## Validate

- **Traceability** — Every backlog item ties to a **source** line or section in the input context.
- **Falsifiability** — Each hypothesis can **fail** on evidence; “success” is **learning**, not only green lights.
- **Accountability** — **Owner** and **date** on each active item, or an explicit **TBD** with **who** picks it up.
- **Scope honesty** — Do not imply this skill **runs** the team’s stand-up or their physical board; you **document** the rhythm they can follow.
- **Honest bar** — For **build–measure–learn** in **shipped** product, point to **delivery** / product practices; keep this skill in **pre-build discovery** unless the test **is** a thin release.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Each backlog item has an owner and a plan

**Scanner:** Manual review

A validated learning backlog item passes when it names who owns the test and what action they will take — the Plan step identifies the method (research, conversation, prototype, pilot, etc.) and scope. Failing means a backlog item exists with no named owner or no stated method, leaving the experiment undeclared and unscheduled.

#### DO

- Assign an owner and describe the planned method for every active backlog item.

  **Example (pass):** `Owner: Sarah (product). Plan: 30-minute interview with 5 dealer coordinators using a Figma prototype of the bay calendar — week of Jan 13.`

#### DO NOT

- Leave a backlog item with no owner or a vague "team" as the owner.

  **Example (fail):** `Owner: TBD` with no stated method — this item is not actionable and will not move.

- Describe the plan as the hypothesis itself with no distinct method or timebox.

  **Example (fail):** `Plan: validate that coordinators adopt the flow.` — this repeats the hypothesis; it is not a method the team could execute.

**Source:** Agile by Design validated learning practices — Plan / Validate / Learn accountability.

### Rule: Each hypothesis is falsifiable with a stated failure condition

**Scanner:** Manual review

A hypothesis in the validated learning backlog passes when it is stated as a belief that could turn out to be wrong, with an explicit condition that would count as failure — not as a plan, a goal, or a certainty. Passing means a reviewer can read the hypothesis and identify what evidence would refute it. Failing means the statement is directional optimism with no failure condition, or it describes a delivery action rather than a belief about the world.

#### DO

- State each hypothesis with a "we expect" belief and an explicit "we will be wrong if" failure condition.

  **Example (pass):** `We expect that dealer coordinators will switch to the self-service reschedule flow within two weeks of go-live. We will be wrong if fewer than 30% of reschedule events use the new flow after the pilot period.`

#### DO NOT

- Write a hypothesis as a plan or a task with no belief that could be falsified.

  **Example (fail):** `We will run a pilot with three dealers and measure adoption.` — this is a method, not a hypothesis; there is no belief stated and no failure condition.

- Write a directional statement with no threshold or signal that would count as failure.

  **Example (fail):** `We believe users will prefer the new flow.` — no failure condition, no observable signal, not testable.

**Source:** Agile by Design validated learning practices — hypothesis format.
<!-- execute_rules:bundle_rules:end -->
