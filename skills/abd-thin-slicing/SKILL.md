---
name: abd-thin-slicing
description: >-
  **Produce** thin-sliced delivery increments: vertical MVIs, spine vs optional paths,
  quality trade-offs, marketable increment names, and early risk validation. From a story
  map, **write** all template artifacts in `templates/` (`thin-slicing.md` and
  `thin-slicing.txt`) with identical increment and story coverage. Use when planning
  releases, MVIs, backlog order, or thin/vertical slices after mapping.
---
# abd-thin-slicing

## Purpose

**Ship prioritized increments.** Turn a **story map** (and any notes on risk, constraints, or learning goals) into **`thin-slicing.md`** and **`thin-slicing.txt`**: marketable increment names, one-line outcomes, optional slicing notes, and **ordered story lists** per increment. Tooling and workspace setup live elsewhere; this skill is **authoring + review**.

## When to use this skill

Use it when **any** of these are true:

- You have a map (**`abd-story-mapping`**) and need **increments** / MVIs / “what ships first.”
- You must **split spine vs optional** before sequencing.
- You are ordering for **learning** (integration, deploy, performance, adoption), not only feature count.
- Someone asks for thin slices, backlog order, or alignment with **`story-graph.json`** **`increments`**.

---

## Core concepts

Short definitions (aligned with prioritization / vertical-slice guidance in **`backup/abd-shaping/docs/ace-shaping-strategy.md`** and **`backup/abd-maps-models-specs/abd-story-synthesizer/rules/interaction-ensure-vertical-slices.md`**):

### What is a **delivery increment**?

An increment is a **named, ordered slice** of the story map you plan to **ship or learn from before** the next slice. It groups **existing stories** (verb–noun, flow order) under one increment: a **sequenced backlog chunk**, not a new epic. In tooling terms it matches **`story-graph.json`** **`increments`** when your project uses that structure. *Prioritization* turns a shaped map into a map **with delivery increments**—this skill is that step in prose and templates.

### What is **thin slicing**?

**Thin slicing** means choosing the **smallest** increment that still **finishes a meaningful journey** (value, demo, or learning)—often by taking **partial** depth in several areas instead of **full** depth in one area first. Early increments may trade polish (manual steps, stubs, one data path) for **speed to end-to-end feedback**; later increments **raise quality** with clear names (for example “Manual …” then “Automated …”). Same user journey, richer implementation each time.

### **Vertical** vs **horizontal** slices

- **Vertical (preferred):** The increment cuts **across** epics/features: a little of order entry, payment, storage, confirmation—enough to go **end-to-end** (input → processing → persistence/feedback → visible outcome) in one slice.
- **Horizontal (avoid):** Finish **all** of Epic A, then **all** of Epic B—layers that **cannot** be exercised end-to-end until late increments.

---

## Do the work (required)

1. **Read inputs** — story map / graph, PO or tech notes, known risks and dependencies.
2. **Mark spine vs optional** — mandatory core sequence vs alternates, enhancements, deep error paths (see bundled rules).
3. **Cut vertical slices** — each increment is an **end-to-end** demonstrable path (even if manual/stubbed); avoid horizontal “finish epic A, then epic B.”
4. **Name for value** — increment titles = stakeholder-visible **capability**, not phase or stack labels.
5. **Pull stories** — under each increment, list **verb–noun** stories in **flow order**; don’t paste the whole map unless asked.
6. **Write both files** — fill **`templates/thin-slicing.md`** and **`templates/thin-slicing.txt`** with the **same** increments and stories (`.md` may use *italics* on domain terms).
7. **Omit maintainer noise** — do **not** copy the template’s **`## Instructions`** block into project deliverables.
8. **Review** — walk every bundled rule; fix violations before you call it done.

---

## Agent Instructions

1. **Templates**

Use **every** file under `templates/`. Unless the user **explicitly** wants one format only, emit **both** `.md` and `.txt`.

| Template | Produce |
| --- | --- |
| `templates/thin-slicing.md` | Increments: **name**, **outcome**, optional **slicing notes**, ordered **story** bullets (*italic* domain terms where helpful). Optional product/context at top. No template `## Instructions` in the deliverable. |
| `templates/thin-slicing.txt` | **Same** increments and stories, plain text layout per the `.txt` template. |

**Parity:** Names, order, story membership, and outcomes must match across `.md` and `.txt`. New files under `templates/` later → one deliverable per file.

**Pointers:** Depth stays at **increment + story list**; point to **`story-map.md`** / graph for full hierarchy.

**Neighbors:** **`abd-story-mapping`** = map structure; **`abd-thin-slicing`** = **order into slices**; **`abd-acceptance-criteria`** / **`abd-specification-by-example`** = story detail **after** priorities.

2. **Rules**

- Apply all prose in the bundled block below (from **`rules/*.md`**).
- Then **review as peer**: each rule’s DO/DON’T and examples—be critical.

**Reviewers:** product owner (value/order), tech lead (risk/feasibility), domain expert (spine matches reality).

3. **Mechanical checks (execute_rules)**

Rules only today (no `scanners/*-scanner.py` here). Refresh the bundle with **`bundle_rules_into_skill_md.py`** after editing **`rules/`**. If scanners are added later:

```text
python skills/execute_using_rules/scripts/run_scanners.py --skill-root skills/abd-thin-slicing --workspace <path-to-project>
```

4. **Assembling this skill**

After changing **`rules/*.md`**:

```text
python skills/execute_using_rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/abd-thin-slicing
```

---

## Constraints (apply while you work)

| Check | Pass means |
| --- | --- |
| **Vertical** | Each increment shows input → processing → persistence/feedback → visible outcome (minimal is OK). |
| **Horizontal** | **Reject** plans that complete one layer/epic with no journey until the end. |
| **Marketable title** | Stakeholder recognizes the **capability**—not “Sprint 3” or “API layer.” |
| **Quality ramp** | Early slice may be manual/stub/low NFR; later slices **add** quality with **clear** names. |
| **Risk** | Scary integration/deploy/perf tackled in **early** increments with **real enough** exercise. |
| **Spine** | Lean mandatory path; optional work **labeled**, not sequenced as if mandatory. |
| **Artifacts** | `thin-slicing.md` + `thin-slicing.txt` stay in sync; mirror **`story-graph.json`** **`increments`** if your project uses them. |

---

## Example output shape

```text
Increment 1: Manual checkout proof — clerk confirms payment; order saved to file; customer sees confirmation id.
  Stories: Place order, Record payment (manual), Save order file, Send confirmation email

Increment 2: Automated payment — same journey with payment gateway and database.
```

**Weak patterns to fix:** phase numbers with no outcome; “all UI then all API”; three auth methods as spine steps 2–4 when one suffices.

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
