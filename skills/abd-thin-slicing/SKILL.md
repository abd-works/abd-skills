---
name: abd-thin-slicing
description: >-
  Teaches thin slicing and incremental prioritization: vertical MVIs, spine vs optional
  paths, quality trade-offs, marketable increment names, and early architectural risk
  validation. When prioritizing from a story map, output **all** template artifacts in
  `templates/` (currently `thin-slicing.md` and `thin-slicing.txt`) with the same
  increments and story coverage. Use when planning releases, MVIs, delivery increments,
  backlog ordering from a map, or when the user mentions thin slices, vertical slices,
  or prioritization after story mapping. Conventions align with agile_bots story_bot
  `behaviors/prioritization`.
---
# abd-thin-slicing

## Purpose

Describe what good **thin slicing** and **incremental prioritization** *are* (vertical value, spine vs optional, trade-offs, risk, naming). **How** to run the Agile Bot, workspace setup, and CLI belong in the agent and other skills—not here.

## When to use this skill

Load this skill when **any** of the following apply:

- You have a **story map** (see **`abd-story-mapping`**) and need **delivery increments** / MVIs / release slices.
- You must separate **mandatory spine** work from **optional** alternates, enhancements, or deep error paths before sequencing.
- You are **prioritizing for learning** (integration, deployment, performance, user impact) as much as for feature count.
- An agent is asked to “thin slice,” “define increments,” “order the backlog,” or “what ships first?”
- You are aligning narrative backlog docs with **`story-graph.json`** **`increments`** (or equivalent) where your pipeline stores them.

---

## Agent Instructions

1. **Templates**

Generate content using **every** template file in this skill’s `templates/` folder. **Do not** emit only Markdown or only plain text unless the user **explicitly** asks for a single format.

**Use every template file (required)**

When you **define or revise** increments from a map and context, you **must** deliver **one output artifact per file** in `templates/`.

| Template | What to produce |
| --- | --- |
| `templates/thin-slicing.md` | **Increments** with **marketable names**, **outcome** line, optional **slicing notes**, and **ordered story list** per increment (verb–noun stories, *italic* domain terms in prose). Optional product/context at the top. **Do not** paste the template’s `## Instructions` section into generated project files—that block is for skill maintainers. |
| `templates/thin-slicing.txt` | The **same** increment and story coverage as **plain text** only—structure matching the `.txt` template. |

**Consistency:** Increment names, ordering, story membership, and outcomes must match between `.md` and `.txt`. Optional **slicing notes** should match when present.

**If new files are added** under `templates/` later, produce a corresponding artifact for **each** new template the same way.

**Depth:** Stay at **increment + story list** level; do not duplicate full epic trees unless the user asks—point to **`story-map.md`** / graph for structure.

**Quality bar:** **Vertical** slices, **marketable** names, **spine-first** sequencing, **risk** addressed early, **trade-offs** visible—see **Core concepts** and bundled rules.

**Relationship:** **`abd-story-mapping`** supplies the map and naming; **`abd-thin-slicing`** orders **stories into shippable slices**. **`abd-acceptance-criteria`** and **`abd-specification-by-example`** deepen individual stories after priorities exist.

2. **Rules**

- Generate content following the rules attached to this skill (listed below, assembled from **`rules/*.md`**).
- After content exists, act as a *peer reviewer*: walk each rule’s constraints, DO/DON’T sections, and examples; be helpful but critical when comparing the deliverable to each rule.

- **Who is checking:** A **product owner** (value and order), a **tech lead** (risk and feasibility of slices), and a **domain expert** (whether the spine matches real workflow).
- **Cross-artifact parity:** `.md` and `.txt` must list the **same** stories under each increment.

3. **Mechanical checks (execute_rules)**

This skill ships **rules only** for now (no `scanners/*-scanner.py` under this folder). You can still run **`bundle_rules_into_skill_md.py`** to refresh bundled prose. If scanners are added later, run:

```text
python skills/execute_using_rules/scripts/run_scanners.py --skill-root skills/abd-thin-slicing --workspace <path-to-project>
```

4. **Assembling this skill**

This **`SKILL.md`** is assembled from **`rules/*.md`** into the bundled block below. Use **`bundle_rules_into_skill_md.py`** from **`skills/execute_using_rules/scripts/`** whenever **`rules/*.md`** changes:

---

## What is thin slicing?

**Thin slicing** (here) means ordering work into **small, vertical increments**: each increment delivers a **coherent, end-to-end** outcome users or the business can **see or use**, even if implementation is **minimal** (manual steps, stubs, thin UX). Slices **cut across** parts of the map needed for that journey—not “complete subsystem A, then subsystem B” horizontal layers.

**Spine** stories are the **mandatory sequence** for core value; **optional** stories are alternates, enhancements, or depth that should not block the **first marketable** slice.

---

## Core concepts

### Vertical vs horizontal

| Approach | Meaning |
| --- | --- |
| **Vertical slice** | Partial features, **full journey** (input → outcome) each increment. |
| **Horizontal layer** | Finish one epic/layer before integrating; **late** end-to-end validation. |

### Marketable increment

An increment has a **name** and **outcome** a stakeholder recognizes (**capability**, not “sprint” or “API milestone”).

### Quality ramp

Early increments **trade quality** (automation, validation, NFRs) for **speed of learning**; later increments **restore** quality with clear naming.

### Risk and uncertainty

**Integration, deployment, performance, and adoption** risks deserve **early** slices that **touch reality**—not endless local-only polish.

### Where it lives

Projects often mirror increments in **`story-graph.json`** (`increments` array with stories and priorities) and in docs like **`thin-slicing.md`**; keep **narrative** and **graph** aligned.

---

## Example (shape only)

```text
Increment 1: Manual checkout proof — clerk confirms payment; order saved to file; customer sees confirmation id.
  Stories: Place order, Record payment (manual), Save order file, Send confirmation email

Increment 2: Automated payment — same journey with payment gateway and database.
```

---

## The shape of good thin-slicing artifacts

```
Product (optional)
Spine vs optional reminder
For each increment:
  Marketable name
  Outcome (one line)
  Slicing notes (optional)
  Ordered list of stories (verb–noun)
```

**Bad shape:** Phase numbers without outcomes; horizontal “all UI then all API”; spine crowded with optional auth methods sequenced as 2,3,4.

---

## Build

**Goal:** Turn a **story map** and prioritization context into **both** template artifacts.

- **Outputs:** `thin-slicing.md` and `thin-slicing.txt` with **matching** increment/story content.
- **Per format:** Markdown may use *italics* for domain terms; plain text does not.
- **While writing:** Prefer **vertical** demonstration; **name** increments for **value**; **document** trade-offs in slicing notes when non-obvious.

---

## Validate

**Goal:** PO + tech + domain agree the **first increment** is **shippable/demoable** and **risk-aware**.

- **Vertical:** Each increment traces a **journey**, not a single layer.
- **Spine:** Mandatory flow is **lean**; optional work is **labeled**, not smuggled into spine order.
- **Names:** **Business** language dominates increment titles.
- **Risk:** Scary dependencies appear in **early** slices with **real** enough exercise.
- **Parity:** `.md` and `.txt` lists **match**.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Apply quality trade-offs for a minimal spine

The **first** thin slices deliberately trade away polish so the **spine** stays small and **end-to-end**. Document what is manual, stubbed, hard-coded, or unvalidated in early increments; add automation, dynamic data, validation, and richer UX in **later** increments with **clear names** (e.g. “Manual …” → “Automated …”).

#### DO

- Start with **manual** ops, **stubbed** integrations, or **hard-coded** data when that keeps a **full journey** testable sooner.
- Use **bare-bones** forms or flows in increment 1; add validation and UX depth later.
- Name increments so **quality level** is obvious—not “Phase 1 / Phase 2” or “Basic / Advanced” without saying *what* got better.

```text
Increment 1: Manual order confirmation — clerk records payment in spreadsheet; customer sees email from template.
Increment 2: Automated payment — same journey; gateway charges card; clerk step removed.
```

#### DON'T

- Put **full** automation, dynamic pricing, validation, error handling, and polished UX all in the **first** increment “because we’re agile.”
- Organize increments as **horizontal layers** (all of “order entry,” then all of “payment”)—that delays end-to-end learning.
- Leave trade-offs **unspoken**—reviewers should see why the slice is thin.

### Rule: Decision prompts for increments

Before locking increments, answer **why this order** and **what you are optimizing**. Use the prompts below (from prioritization guardrails) as a checklist; capture conclusions in **slicing notes** or team docs.

#### Questions to settle

- Which map areas carry the most **business or delivery risk**?
- Which areas deliver the most **value if shipped early**?
- Which are **complex relative to value**?
- Should thin slices be as **end-to-end** as possible? (Default for this skill: **yes**, unless constraints say otherwise.)
- What must be **reused** across many stories—validate that **early**?
- What **program constraints** (compliance, date, dependency) force order?
- Which **users or segments** must go first so others can follow?

#### Thin-slicing dimensions (how you make a slice thinner)

Pick explicitly when useful: **users** (role/context first); **workflow** (simple path before variants); **interfaces** (one channel first); **data variations** (one type first); **environment** (one deployment context); **business rules** (subset of rules first); **subjective quality** (lower NFR bar for early adopters); **spike** (throwaway learning).

#### How increments are grouped (strategy options)

Examples: **end-to-end journey**; **validate impact / feasibility**; **maximize earned value**; **increase reuse / reduce dependency risk**; **quick win**; **validate impact** with users (Wizard of Oz, landing page, stubs, etc.).

#### What value this increment optimizes

Examples: **end-to-end journey**; **earned value for a bounded capability**; **quick win**; **stakeholder validation**.

#### Earliest uncertainty to validate

Examples: **architecture / reuse**; **impact** (do users care?); **operations** (deploy, monitor, support); **system integration** (external APIs, partners).

#### DO

- Tie **Increment 1** to the **riskiest** or **most informative** uncertainty you can address in a **short vertical** slice.
- State **which dimension** you sliced on when it helps stakeholders reason about scope.

#### DON'T

- Sequence increments only by **component build order** with no **outcome** or **learning** rationale.
- Skip **stakeholder-visible** naming—prompts should surface in **increment titles** and **outcomes**, not stay in a private worksheet only.

### Rule: Design vertical-slice increments

Each increment is a **vertical slice**: a **working** path from **input → processing → persistence → visible outcome**, pulling **partial** depth from **multiple** epics or features as needed. Avoid **horizontal** plans that finish one epic before the next—those delay end-to-end validation.

#### DO

- Include the **smallest** set of behaviors that still **demonstrates** the journey, across whatever parts of the map touch that journey.
- Show **integration points** early—even if crudely (manual handoff, file store, simple UI).
- Make **partial completion** visible per epic when helpful (e.g. “Invoice epic2/5 in this increment”) so progress is honest.

```text
Increment 1: Place order → manual payment recording → save to file → confirmation email (stub).
Increment 2: Same flow → real gateway → database → richer confirmation.
```

#### DON'T

- Plan “Increment 1 = all of character creation, Increment 2 = all of storage” with **no** playable journey until late.
- Ship an increment that stops mid-air (**no** persistence, **no** visible result) and call it “done.”
- Optimize for **component completeness** over **journey demonstrability**.

### Rule: Identify marketable increments

**Increments** are named and ordered for **stakeholders**: business outcomes and user capabilities they can **recognize**. Names should **sell** the next slice of value, not describe your tech stack.

#### DO

- Use titles like *Basic phone activation*, *Self-service order portal*, *Automated invoicing*—outcomes people can demo or buy.
- Align story lists under each increment to that **one** headline outcome.

#### DON'T

- Name increments *API endpoints*, *Database schema*, *React components*, or *Sprint 3* without a **capability** story.
- Hide value behind **internal** milestones when an **external** outcome is understandable.

```text
Wrong: MVI 1 — Postgres migration
Right: MVI 1 — Customers can complete checkout and see order status
```

### Rule: Map sequential spine vs optional paths

The **spine** is the **minimum mandatory sequence** that delivers core value. **Optional** items are alternates (only one auth method needed), **enhancements** (customization after baseline works), and **non–happy-path** depth that can follow once the spine is marketable. Thin slicing **pulls from the spine first**; optional work lands in **later** increments or parallel tracks with clear markers.

#### DO

- Sequence **mandatory** steps in order; mark **alternates** (e.g. OAuth vs password) as optional so you do not serialize independent choices.
- Treat **dashboard customization**, **sharing**, **extra reports** as enhancements **after** “user sees default dashboard” works.
- Treat **deep error/retry** paths as optional **relative to** the first marketable happy path—still implement them, but not always in increment 1.

#### DON'T

- List **three login methods** as three sequential spine steps when **one** suffices for the slice.
- Elevate **nice-to-haves** to the same **mandatory** rank as “user can complete core task.”
- Forget **markers** (optional, alternate, enhancement) on the map or in metadata—reviewers cannot slice what they cannot distinguish.

```text
Spine: Enter credentials → Authenticate (one method) → View dashboard.
Optional: Social login, layout customization, export to PDF.
```

### Rule: Prioritize architectural risk validation

**Early** increments should **prove** the scary parts: real **integrations**, **performance** with realistic load, **deployment** and ops, **unfamiliar** frameworks—inside a **short end-to-end** flow. Deferring risk behind mocks or “local only” builds invites late rework.

#### DO

- Pull the **riskiest integration** into **Increment 1** with the **simplest** journey that still hits the real system (auth, response shape, limits).
- Deploy **something** real to the target environment early; validate connectivity, config, and observability.
- Size performance or data-volume tests to **match** early concerns (e.g. report with 10k rows if that is the fear).

#### DON'T

- Spend increments 1–2 on **perfect UI** while **payment**, **identity**, or **hosting** stays mocked or unspecified.
- Assume **infrastructure** “will be fine”—prove it with a **thin** feature on **real** infra.
- Treat **“we’ll swap the mock later”** as risk reduction without a dated, vertical slice that uses the real dependency.

```text
Good: Increment 1 — place order → **real** gateway (happy path only) → DB row → confirmation page.
Weak: Increment 1 — full cart UX; payment stub; “real payment in increment 4.”
```
<!-- execute_rules:bundle_rules:end -->
