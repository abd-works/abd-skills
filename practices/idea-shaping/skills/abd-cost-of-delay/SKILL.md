---
name: abd-cost-of-delay
catalog_garden_tier: practice
catalog_garden_order: 21
catalogue_one_liner: >-
  Quantify urgency × value for backlog items; score CD3 and rank to prioritize by economic impact of delay.
description: >-
  Estimate Cost of Delay for features or initiatives, classify value type and urgency profile,
  calculate CD3 (Cost of Delay divided by Duration), and rank items to prioritize by economic
  impact. Use when ordering a backlog by value, comparing initiatives, or making trade-off
  decisions about what to build next.
---
# abd-cost-of-delay

**Manual:** `./manual/index.html`

## Purpose

Teams routinely prioritize work by gut feel, stakeholder loudness, or first-in-first-out — all of which ignore how much value decays while items wait to be delivered. Cost of Delay puts a price tag on time so teams can make scheduling decisions based on economics rather than politics. 

This skill packages that method, it classifies the value type and urgency of each feature or initiative in context, then builds a simple value model that makes assumptions explicit, calculatse Cost of Delay per time period (month / week), and divides value by time by duration to get Cost of Delay Divided By Duration (CD3), and rank so the highest-value shortest-duration work goes first.

## When to use this skill

Load this skill when **any** of the following apply:

- You have a backlog of features, epics, or initiatives and need to **order them by economic value** rather than opinion or arrival order.
- You want to make a **trade-off decision** between competing items — what is the cost of doing A before B?
- You need a **collaborative, assumption-explicit** value estimate that a cross-functional group can produce in a time-boxed session.
- You already have lead time and delay time estimates and want to **score and rank** items using CD3.
- You want to compare items already scored with CD3 against a new candidate.

---

## Core concepts

### Cost of Delay

The value an organisation does **not** receive for every time period an item is not yet in market. Expressed as dollars (or equivalent) per month or per week. It reframes prioritization from "how much does this cost to build?" to "how much does it cost us to **wait to build it**?"

### Value Type

Every item generates value through one of four mechanisms. The type shapes the formula you use to estimate Cost of Delay:

| Value Type | What it means | Formula pattern |
| --- | --- | --- |
| **Increase Revenue** | New or expanded sales | Market size × transaction value × likelihood × volume |
| **Protect Revenue** | Sustain current revenue against threats | Likelihood of threat × events/month × cost per event |
| **Reduce Cost** | Lower costs we are currently incurring | Cost reduction/event × events × likelihood of benefit |
| **Avoid Cost** | Prevent costs we do not yet incur but may | Cost avoidance/event × events |

### Urgency Profile

How fast value decays over time — the shape of the curve:

| Profile | Characteristic | Example |
| --- | --- | --- |
| **Expedite** | High and immediate impact; major loss if not addressed now | "Customer data is exposed until we fix this" |
| **Fixed Date** | Value drops to zero past a specific date | "Campaign must launch before Black Friday" |
| **Standard** | Shallow but immediate; incremental value over time | "More paying customers if they can subscribe online" |
| **Intangible** | No immediate impact; builds future capability | "Local delivery capability gives us autonomy to move at market speed" |

### CD3 — Cost of Delay Divided by Duration

The scheduling decision formula:

```
CD3 = Cost of Delay (per period) / Duration (lead time to deliver)
```

Rank by **highest CD3 first**. This maximises total value delivered for a given time window with fixed resources, and naturally encourages breaking work into smaller batches (smaller duration → higher CD3).

### Why CD3 beats FIFO

| Feature | CoD ($/week) | Duration (weeks) | CD3 |
| --- | --- | --- | --- |
| A | $1 | 5 | 0.2 |
| B | $4 | 1 | 4.0 |
| C | $5 | 2 | 2.5 |

**FIFO order (A → B → C):**

| Week | Working on | A earning | B earning | C earning | Revenue gained | Opportunity cost |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | A | $0 | $0 | $0 | $0 | $10 |
| 2 | A | $0 | $0 | $0 | $0 | $10 |
| 3 | A | $0 | $0 | $0 | $0 | $10 |
| 4 | A | $0 | $0 | $0 | $0 | $10 |
| 5 | A | $0 | $0 | $0 | $0 | $10 |
| 6 | B | $1 | $0 | $0 | $1 | $9 |
| 7 | C | $1 | $4 | $0 | $5 | $5 |
| 8 | C | $1 | $4 | $0 | $5 | $5 |
| **Total** | | | | | **$11** | **$69** |

**CD3 order (B → C → A):**

| Week | Working on | A earning | B earning | C earning | Revenue gained | Opportunity cost |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | B | $0 | $0 | $0 | $0 | $10 |
| 2 | C | $0 | $4 | $0 | $4 | $6 |
| 3 | C | $0 | $4 | $0 | $4 | $6 |
| 4 | A | $0 | $4 | $5 | $9 | $1 |
| 5 | A | $0 | $4 | $5 | $9 | $1 |
| 6 | A | $0 | $4 | $5 | $9 | $1 |
| 7 | A | $0 | $4 | $5 | $9 | $1 |
| 8 | A | $0 | $4 | $5 | $9 | $1 |
| **Total** | | | | | **$53** | **$27** |

**Result:** Same 8 weeks, same three features. CD3 ordering delivers **$53 revenue** vs FIFO's **$11** (nearly 5× more), and incurs only **$27 opportunity cost** vs **$69** — a **61% reduction** in total delay cost.

---

## Do the work

**Inputs required:** Each candidate item needs a **lead time estimate** (how long to deliver to market) and optionally a **delay time estimate** (how much of that lead time is waiting, not working). These come from outside this skill — from team knowledge, flow metrics, or a delivery planning practice.

1. **Scan context for items and isolate each one.** Read the supplied context (backlog, story map, canvas, brief, conversation) and identify every distinct feature, epic, or initiative. When there is more than one item, treat each independently — do not blend assumptions across items. List what you found and cite where in context each item came from.

2. **Check for lead time.** Each item needs a lead time (duration) estimate. If the context supplies it, cite where. If not, **ask the user** — do not invent a duration. You cannot calculate CD3 without it.

3. **Classify value type and urgency profile per item.** For each item independently, select one value type (Increase Revenue / Protect Revenue / Reduce Cost / Avoid Cost) and one urgency profile (Expedite / Fixed Date / Standard / Intangible). Cite which part of the context led to the classification — quote the phrase, metric, or constraint that justifies it.

4. **Build a value model and estimate Cost of Delay per item.** For each item independently, mine the context for numbers, constraints, and claims that feed the formula. Every assumption must cite its source: quote from context if available, mark as "team estimate" or "SWAG" if not. Use Reach × Frequency × Likelihood × Unit Value or the formula matching the value type. Express CoD as **$ per period** (month or week — be consistent across items). Document each assumption with factor, unit, confidence, and source citation.

5. **Calculate CD3 per item.** CD3 = Cost of Delay / Duration. Show the arithmetic.

6. **Rank by CD3 and produce the revenue vs opportunity-cost table.** Order all items highest CD3 first. Run the calculation script to generate the table:

   ```bash
   python skills/abd-cost-of-delay/scripts/cd3_table.py \
     --items "Name1:CoD1:Dur1, Name2:CoD2:Dur2, ..." \
     --period-label "Week"
   ```

   The script outputs a markdown table showing per-period revenue earned and opportunity cost. Do **not** hand-compute this table — always use the script for predictability.

7. **Answer "what if we reorder?"** When the user asks (or when items are close in CD3), use the script's `--compare` flag to show both orderings side by side:

   ```bash
   python skills/abd-cost-of-delay/scripts/cd3_table.py \
     --items "Name1:CoD1:Dur1, Name2:CoD2:Dur2, ..." \
     --compare "A,B,C" "B,C,A" \
     --period-label "Week"
   ```

   The output includes a comparison summary showing total revenue, total opportunity cost, and the saving vs the worst order.

---

## Agent Instructions

| Step | What to do |
| --- | --- |
| Isolate items | Scan context; list each distinct feature/epic/initiative separately; cite where each came from |
| Check lead time | If duration is in context, cite it. If missing, **ask the user** — never invent it |
| Classify | Per item independently: assign value type + urgency profile; **cite the context phrase** that justifies each |
| Value model | Per item independently: mine context for numbers; build assumption table (factor, unit, confidence, **source citation**); compute CoD |
| CD3 | Per item: CD3 = CoD / Duration; show arithmetic |
| Rank + table | Order by highest CD3; run `scripts/cd3_table.py --items "..." --period-label "Week"` — never hand-compute the table |
| What-if | Run `scripts/cd3_table.py --compare "order1" "order2"` to show both orderings side by side with comparison summary |
| Templates | Fill **both** `templates/cost-of-delay-canvas.md` and `templates/cd3-ranking.md` |

**Templates:**

| Template | What to produce |
| --- | --- |
| `templates/cost-of-delay-canvas.md` | One canvas per item: value type, urgency profile, assumptions table, CoD calculation, CD3 score |
| `templates/cd3-ranking.md` | Ranked list of all scored items with CoD, duration, CD3, and ordering rationale |

**Parity:** Items that appear in the ranking must have a canvas (or reference one from prior work). CoD and CD3 values must match across both files.

**Neighbours:** `abd-thin-slicing` handles increment ordering after items are scored; `abd-delivery-planning` provides the pipeline context where this skill fits as stage 5 (Value Estimation); `abd-simple-validated-learning` turns assumptions flagged here into a prioritised validation backlog with hypothesis format, owners, and Plan / Validate / Learn.

**Assumptions and validation:** Every CoD canvas labels assumptions with confidence (Strong / Reasonable / Uncertain). Assumptions marked **Uncertain** are candidates for validation — beliefs that could be wrong and would change the CoD materially if they are. This skill does **not** mine for assumptions (they emerge naturally from the value model) and does **not** run the validation workflow. It surfaces them with confidence labels so the team can decide what to test. Use **abd-simple-validated-learning** to take Uncertain assumptions through Plan / Validate / Learn — same language as `abd-opportunity-canvas` and `abd-impact-mapping`.

---

## Build

1. **Produce outputs from every template.** Generate content using **both** files in `templates/`. Unless the user explicitly asks for one format only, emit both the canvas and the ranking.

2. **Apply the rules, then review like a peer.** Follow the normative `rules/` prose bundled at the end of this file. After generating, act as a peer reviewer: walk each rule's DO and DO NOT and look for violations.

3. **Keep the bundled rules block honest.** Whenever you change a file under `rules/`, run:

```bash
python skills/execute_using_rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/abd-cost-of-delay
```

---

## Validate

**Goal:** Inspect what was built as a reviewer.

- **Assumptions explicit** — Every CoD estimate traces to named assumptions with factors, units, and confidence. No "we think it's worth $X" without showing the model.
- **Value type and urgency assigned** — Each item has exactly one value type and one urgency profile, with rationale.
- **CD3 arithmetic** — CoD / Duration = CD3; check the maths.
- **Ranking is by CD3** — Items ordered highest-first; any deviation from pure CD3 order has stated rationale.
- **Cross-template parity** — Canvas CoD and CD3 match the ranking table values.
- **No invented precision** — Estimates reflect stated confidence; uncertain assumptions are flagged, not hidden behind false precision.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Assumptions explicit with confidence

Every Cost of Delay estimate must trace to a set of named assumptions — each with a factor, unit, and confidence level — so the team can see what drives the number and where uncertainty lives. A canvas passes when a reviewer can reconstruct the CoD calculation from the assumptions table without needing to ask "where did that number come from?" It fails when a CoD figure appears with no supporting model, or when assumptions are listed without confidence ratings that would let a team know what to validate.

#### DO

- List every assumption that feeds the CoD formula as a row with **factor** (what you are estimating), **unit** (people/month, $/hour, %, events/month), and **confidence** (Strong / Reasonable / Uncertain).

  **Example (pass):**
  ```
  | Assumption | Factor | Unit | Confidence |
  | Customers travelling abroad/month | 500,000 | people/month | Strong |
  | Likelihood card is flagged | 30% | — | Strong |
  | Avg call duration | 0.25 | hours | Reasonable |
  | Hourly call center rate | $50 | $/hour | Strong |
  | % who would use self-service | 40% | — | Uncertain |
  ```

- Show the CoD formula as a product of the factors so arithmetic is transparent.

  **Example (pass):** `CoD = 500,000 × 0.30 × 0.25 × $50 × 0.40 = $750,000/month`

- Flag **Uncertain** assumptions as candidates for validated learning before committing to build.

  **Example (pass):** "% adoption (40%) is Uncertain — recommend quick survey or A/B before locking scope."

#### DO NOT

- Present a CoD number with no underlying factors or formula.

  **Example (fail):** "Cost of Delay: $750,000/month" with no assumptions table and no formula — the reviewer cannot verify or challenge the estimate.

- List assumptions without confidence levels, treating all factors as equally certain.

  **Example (fail):** Five assumption rows, all blank in the Confidence column — hides which parts of the estimate are guesses.

- Use false precision (e.g. $748,213.47/month) when inputs are uncertain — round to appropriate significant figures.

  **Example (fail):** "CoD = $748,213.47/month" when the adoption rate is a SWAG at 40% — implies precision the model does not support.

**Source:** Kept chunks #6, #8, #11 in `inputs/abd-answers-retrieval.md` — "The process of surfacing our assumptions about value are more useful than the numbers we come up with!"

### Rule: CD3 ranking by highest first

When multiple items have been scored, the ranking orders them by highest CD3 first — this is the scheduling decision that minimises total delay cost across the set. A ranking passes when items are ordered by CD3 descending, arithmetic is correct (CoD / Duration = CD3), and any deviation from pure CD3 order has explicit stated rationale. It fails when items are ordered by CoD alone (ignoring duration), by arrival order, or by unstated preference with no economic justification.

#### DO

- Order items by **highest CD3 first** (descending).

  **Example (pass):**
  ```
  | Rank | Item | CoD ($/month) | Duration (months) | CD3 |
  | 1 | Feature B | $4,000 | 1 | 4,000 |
  | 2 | Feature C | $5,000 | 2 | 2,500 |
  | 3 | Feature A | $1,000 | 5 | 200 |
  ```

- Verify arithmetic: CD3 = CoD / Duration for every row.

  **Example (pass):** Feature C: $5,000 / 2 = 2,500. Checks out.

- When deviating from pure CD3 order (e.g. for dependencies, fixed dates, or expedite items), state the rationale explicitly.

  **Example (pass):**
  ```
  | Rank | Item | CD3 | Override rationale |
  | 1 | Compliance fix | 800 | Expedite: regulatory deadline Nov 1 — must go first regardless of CD3 |
  | 2 | Feature B | 4,000 | — |
  ```

#### DO NOT

- Order by Cost of Delay alone without dividing by duration.

  **Example (fail):** Feature C ($5,000 CoD) ranked above Feature B ($4,000 CoD) even though B has CD3 of 4,000 vs C's 2,500 — duration was ignored.

- Use arrival order (FIFO) or stakeholder preference as the default without stating why CD3 was overridden.

  **Example (fail):** "Feature A first because the VP asked for it" with no CD3 comparison or economic justification.

- Present CD3 scores with incorrect arithmetic.

  **Example (fail):** CoD = $5,000, Duration = 2, CD3 shown as 5,000 — division was not performed.

**Source:** Kept chunks #7, #8, #12 in `inputs/abd-answers-retrieval.md` — FIFO ($69 delay cost) vs CD3 ordering ($27 delay cost), 61% reduction.

### Rule: Value type and urgency assigned

Every item scored in this skill must have exactly one value type and one urgency profile selected, with enough rationale that a reviewer can see why that classification was chosen. A canvas passes when value type picks the right formula pattern and urgency profile matches the decay shape. It fails when classifications are missing, when both are left as "Standard" by default without reasoning, or when the selected value type contradicts the formula used.

#### DO

- Assign exactly **one** value type per item: Increase Revenue, Protect Revenue, Reduce Cost, or Avoid Cost.

  **Example (pass):**
  ```
  Value Type: Reduce Cost
  Rationale: Customers currently call in to reactivate blocked cards; this reduces call volume.
  ```

- Assign exactly **one** urgency profile per item: Expedite, Fixed Date, Standard, or Intangible.

  **Example (pass):**
  ```
  Urgency Profile: Standard
  Rationale: Shallow but immediate cost saving; value accrues incrementally from day one with no hard deadline.
  ```

- Use a formula pattern that matches the selected value type (see Core concepts table in SKILL.md).

  **Example (pass):** Value type is "Reduce Cost" → formula uses `cost reduction/event × events × likelihood`.

#### DO NOT

- Leave value type or urgency profile blank or unselected on a scored item.

  **Example (fail):** Canvas has CoD = $200,000/month but the Value Type row says "TBD" — classification was skipped.

- Default both to "Standard / Standard" without stated reasoning.

  **Example (fail):** Three items all marked Standard/Standard with no rationale — suggests the team skipped the conversation.

- Select a value type that contradicts the formula used.

  **Example (fail):** Value Type says "Increase Revenue" but the formula calculates `cost avoidance/event × events` — mismatch between classification and model.

**Source:** Kept chunks #4, #9 in `inputs/abd-answers-retrieval.md` — value type / urgency profile matrix with four types and four profiles.
<!-- execute_rules:bundle_rules:end -->
