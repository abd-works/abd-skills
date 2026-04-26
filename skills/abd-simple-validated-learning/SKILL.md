---
name: abd-simple-validated-learning
catalog_garden_tier: practice
catalog_garden_order: 17
catalogue_one_liner: >-
  Turn surfaced assumptions into hypotheses, prioritise small tests, and run Plan / Validate / Learn before full build.
description: >-
  Mine context for assumptions, convert them to testable hypotheses, prioritise a validation backlog, and work items
  through Plan, Validate, and Learn—with emphasis on discovery and cheap checks; pair with an opportunity or
  experimentation canvas. Use abd-answers (query-pinecone) for grounded phrasing. Full product build–measure–learn
  is a different cadence (solution delivery), not the primary focus here.
---

# abd-simple-validated-learning

## Purpose

Opportunity work, story maps, and similar artifacts **name beliefs**; this skill is for **working those beliefs off** in small, time-boxed **experiments** before the organisation treats them as fact or commits a full build. The agent (or facilitator) **mines** the supplied context for **assumptions**, rewrites them as **falsifiable hypotheses**, **prioritises** them into a **validation backlog**, and structures each item to move through **Plan → Validate → Learn**.

The skill emphasises **up-front discovery and validation**: desk research, conversations and **SME** deep dives, paper prototypes, **quick pilots**, cohort tests, and other **cheap** checks. A **longer** build–measure–learn loop in **live product delivery** is related but **not** the same rhythm—use delivery-oriented practices when the bet is a shipped increment, not a canvas row.

**abd-opportunity-canvas** (and similar) **surfaces** uncertainty; **this skill** helps the team **operate** a learning backlog and accountability (**who** / **what** / **by when**) to **confirm** or **refute** each hypothesis. The **Opportunity Canvas** training material describes a **Validated Learning Kanban** and an **assumption / risk checklist**; wording is in **`inputs/abd-answers-retrieval.md`** (sourced from ABD **abd-answers** content).

## When to use this skill

Load this skill when any of the following apply:

- You have (or are finishing) an **opportunity canvas**, **impact map with hypotheses**, or other model that lists **assumptions** and you need a **prioritised** set of **tests** with owners and dates.
- You want to move from “we believe …” to **I/we expect that …, and we will be wrong if …**, with a **smallest** experiment that could reduce uncertainty.
- You need a **Validated Learning** working pattern (**Plan** / **Validate** / **Learn** or **Plan** / **Build** a *thin* test / **Measure** / **Learn**) aimed at **discovery**, not a full product release train.
- The team uses or wants a **Validated Learning Kanban**-style board and a **multi-area** risk pass (problem/solution fit, capability/market, technology, delivery, regulatory/commercial, etc.) — see hub material in **`inputs/abd-answers-retrieval.md`**.
- The user references an **experimentation canvas** (or lean experiment one-pager): use it as a **single-experiment** or **per-hypothesis** view alongside the **backlog** template in this skill.

**Optional:** Load **query-pinecone** and search **abd-answers** (Agile Practices / training corpus) for phrases like *validated learning*, *opportunity canvas* assumptions, *uncertainty backlog*, to align language with in-house material.

## Agent instructions

1. **Inputs**
   - Accept **context** the user provides (canvas text, map, interview notes, deck bullets). If **abd-opportunity-canvas** outputs exist, treat **`ASSUMPTION:`** and **`validate by:`** lines as the primary mine.
   - For **grounding**, prefer **`inputs/abd-answers-retrieval.md`** in this skill; optionally run **abd-answers** RAG for additional phrasing and the checklist.

2. **Build (sequence)**

   1. **Mine assumptions** — Extract explicit and **implicit** beliefs from the context (link rows when possible: e.g. segment size ↔ Customer Problems, partner risk ↔ Key Partners). Flag **fragile** beliefs that the narrative depends on.
   2. **Convert to hypotheses** — For each item: *We believe …* → **We expect** that … **We will be wrong if** … (observable, **falsifiable**). One hypothesis can map to more than one test; merge duplicates.
   3. **Backlog prioritise** — Order by **risk to the bet** and **cost of being wrong** vs **cost to test** (cheapest high-risk first when sensible). Mark **MUST learn before build** vs **can learn in parallel**.
   4. **Plan / Validate / Learn** — For each **prioritised** item, define:
      - **Plan** — What will you do, with what **scope** and **timebox** (research, SME session, mock, pilot, etc.)?
      - **Validate** — What **evidence** will you collect, from **whom** or **where**?
      - **Learn** — What **decision** or **canvas update** follows (refine, kill, pivot, or proceed to a larger experiment)?
      - **Owner** and **date** (who does what by when).
   5. **Checklist pass** (from hub) — Skim the **multi-area** questions in **`inputs/abd-answers-retrieval.md`** to ensure you did not only test the “obvious” row (problem/solution fit, capability/market, technology, delivery, other feasibility).

3. **Templates**

   | Template | What to produce |
   | -------- | ---------------- |
   | `templates/validated-learning-backlog.md` | Prioritised list + **Plan / Validate / Learn** table (Kanban-style columns in one view). |
   | `templates/experimentation-canvas.md` | One **experiment** per block: belief, method, **success/fail** signal, owner, **by when** — for workshops or a single high-stakes test. |

   Keep **template parity** in spirit: the same experiments appear in the backlog; the **experimentation canvas** can zoom **one** row.

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

- **Traceability** — Every backlog row ties to a **source** line or section in the input context.
- **Falsifiability** — Each hypothesis can **fail** on evidence; “success” is **learning**, not only green lights.
- **Accountability** — **Owner** and **date** on each active item, or an explicit **TBD** with **who** picks it up.
- **Scope honesty** — Do not imply this skill **runs** the team’s stand-up or their physical board; you **document** the rhythm they can follow.
- **Honest bar** — For **build–measure–learn** in **shipped** product, point to **delivery** / product practices; keep this skill in **pre-build discovery** unless the test **is** a thin release.

---

<!-- execute_rules:bundle_rules:begin -->
<!-- execute_rules:bundle_rules:end -->
