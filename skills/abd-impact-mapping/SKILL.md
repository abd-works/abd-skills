---
name: abd-impact-mapping
catalog_garden_tier: practice
catalog_garden_order: 15
catalogue_one_liner: >-
  Strategic impact maps: hierarchy view, ASCII wall map, and hypothesis sentences from discovery sources.
description: >-
  Teaches collaborative impact mapping: layered goals, actors, observable impacts, and deliverable options.
  Emits six template outputs (hierarchy, ASCII map, and BUILD/OUTCOME hypotheses, each in Markdown and plain text).
  Use when connecting organisational outcomes to scope, facilitating discovery, or replacing feature-first backlogs.
---
Manual: [Practice manual](./manual/index.html)

# abd-impact-mapping

## Purpose

Impact mapping is a strategic discovery technique that links broader goals to finer-grained goals, then to actors, their observable behaviour changes, and deliverable options (often epics or features) that could create those behaviours. It keeps discussion outcome-first: you see *why* an option might matter before debating build order.

The map answers four questions in order (see Core concepts): *Why are we doing this?* *Who can help or hinder?* *How should behaviour change?* *What could we do to support that change?* Good maps surface assumptions, limit scope creep by tying ideas to impacts, and support shared ownership when business and delivery build them together.

This skill defines the ideas behind a sound map, how to structure one, and what good looks like. Workspace layout, CLIs, and agent wiring belong in other skills.

## When to use this skill

Load this skill when any of the following apply:

- You have a defined business outcome and need scoped options that tie to behaviour change, not a raw feature dump.
- You are facilitating discovery and want a visible spine from goal to actors to impacts to deliverables.
- Stakeholders ask to align delivery with outcomes, reduce scope creep, or see who is involved beyond a single user persona.
- You are rewriting interview notes, strategy briefs, or roadmaps into a single impact map for prioritisation or story mapping downstream.

## Agent Instructions

1. Templates

Generate content using **every** template file in this skill's `templates/` folder (six files). Each file has a **Template** section with `{{placeholder}}` tokens and an **Example (reference)** below it: copy the shape from Template, replace every placeholder with engagement text, and do **not** paste Instructions or Example into stakeholder deliverables. For **hypotheses** templates, phrase lines in **natural English** while keeping all actors, impacts, impact metrics, goals, and goal metrics explicit (see the note at the top of the Template section). Do not emit only Markdown or only plain text unless the user explicitly asks for a single format.


| Template | What to produce |
| -------- | ---------------- |
| `templates/impact-map.md` | Hierarchy view: broader to finer `GOAL:` levels, then ACTOR / IMPACT / DELIVERABLE per Template placeholders; optional `METRIC:` under each `GOAL:` (lagging proof) and under each `IMPACT:` (behaviour proxy); optional phased table. |
| `templates/impact-map.txt` | Same hierarchy tree and phased TSV (if any) as plain text; same `{{placeholder}}` pattern as the `.md` Template. |
| `templates/impact-map-ascii.md` | **ASCII wall sketch** (training-style **four columns**): **OBJECTIVE (Why?) \| PERSONA (Who?) \| IMPACT (How?) \| INITIATIVE (What?)**, goal stack and **`#`** metrics in the objective column, one initiative row per **`DELIVERABLE:`** — same four questions as hub material (**`inputs/abd-answers-retrieval.md`** Kept chunks 1-3) and the same facts as **`impact-map.md`**. ASCII only (no Unicode box drawing). |
| `templates/impact-map-ascii.txt` | Same four-column table as plain text. |
| `templates/impact-map-hypotheses.md` | `### Outcome` + build bullets: same facts as the tree. `Then` clause: **we will** + goal as a **verb phrase** (e.g. *grow monthly active players*) + `with` + goal metric; avoid *achieve **Grow …***. **Phrase naturally**; optional **PHASE:**. |
| `templates/impact-map-hypotheses.txt` | Same placeholders and sentence shape as the `.md` template in plain text. |


Parity:

- Within each **pair** (hierarchy, ASCII, hypotheses), the `.md` and `.txt` versions match.
- Across **all six** files: same engagement — same goal stack, actors, impacts, deliverables, and phased items. Impacts stay behavioural; each deliverable supports one impact; hypothesis lines use the same names as the hierarchy view.

Quality bar: Match Core concepts and The shape of a good impact map for structure; use `rules/*.md` for generative wording (goal, impact, actor, deliverable, assumptions, phased backlog **Actor / impact** column) without duplicating this section.

1. Rules

After generating content, review against each bundled rule (DO, DO NOT, Examples).

1. Bundling

When `rules/*.md` changes, run `bundle_rules_into_skill_md.py` on this skill root (see Build).

---
## What is an impact map?

An impact map is a layered picture of cause and intent, read in a fixed order:

1. Goal — Broader organisational outcomes connect to finer-grained outcomes (why). You pick the level you are mapping in detail; actors and behaviour hang off that focus.
2. Actors — People, teams, or roles that can help or obstruct (who).
3. Impacts — Observable changes in behaviour for each actor (how behaviour should move).
4. Deliverables — Hypotheses about what we could build or do to enable those behaviours (what).

It is not a story map, a WBS, or a prioritised backlog by itself. It feeds those artifacts by clarifying how candidate scope links back to outcomes and behaviour. For delivery planning, you can add a phased backlog over named timeboxes (months, quarters, or another convention): each scheduled option still points at one behaviour path on the map so ordering stays tied to outcomes, not to a separate feature list.

### Why use it?

- Assumptions visible — Gaps and guesses show on the map instead of hiding in documents.
- Scope discipline — Orphan features are obvious when they are not tied to a behaviour you care about.
- Cross-functional alignment — Shared picture for product, delivery, and domain voices (when run collaboratively).

---

## Core concepts

### Goal

The goal is why you are doing the work: the business outcome the organisation wants — the stakes in play (market, revenue, risk, adoption, compliance, cost, reliability, and similar). Broader outcomes decompose into finer outcomes that roll up to them. The finest-grained outcome on the map is often workshop-sized (about a quarter or less when you timebox).

Phrase each level as an outcome in the world: direction and stakes in language about results (growth, reliability, risk posture, adoption, retention, margin), not shipping labels. Examples: *Grow monthly actives*; *Achieve reliable same-day completion for domestic orders*; *Grow net revenue retention in the enterprise segment*. Put numeric proof on `METRIC:` lines indented under that `GOAL:` (e.g. verified MAU lift), not in the `GOAL:` headline when using this skill's templates. Deliverables hold candidate things to build or ship once behaviour is clear under impacts.

Clear organisational outcomes are specific enough that the team can identify the actors that are necessary to achieving it. Who will help us achieve our outcome?; How should behaviour change?; What could we do to support that impact? 
Good goals are often nested, starting major (wide intent) narrowing to tactical. They stay customer- and stakeholder-driven toward outcomes in the world. Actors and impacts tie the mapped outcome to who and observable behaviour; deliverables carry what you might ship.

### Goal metrics (`METRIC:` under each `GOAL:`)

Lagging proof tied to outcomes: economic (revenue, margin, unit cost) or strategic (adoption, share, compliance, risk). Attach each at the goal level it measures — numeric bars, percent targets, thresholds, and counts that show the organisation moved.

Example: *Grow monthly actives* with proof on `METRIC:` *verified MAU +20% this quarter vs baseline*; *Achieve reliable same-day completion for domestic orders* with proof *ninety percent same-day*; *Grow net revenue retention in the enterprise segment* with proof *NRR above 110% this fiscal year*.

### Actors

An actor is someone who can help or block the outcome in the goal hierarchy: a person, team, or organisation. For each actor, be clear which people or teams you mean and what about their situation matters here (for example new versus returning, channel or market, a lifecycle stage, contract timing, or a stressful moment such as renewal or outage). Words like customer, operator, or partner are fine to start, but you need to make them more specific.

Never cast a product, service, system, or platform as an actor, even when a brief talks that way. Name who actually helps or blocks and put the system under deliverables.

If you only name a vague who (“all customers,” “partners,” one bucket of “users”) but the impacts you list are really about different groups or moments with different behaviour, you are mixing actors. Narrow the situation, name the moment, or split into separate actors so each who matches one coherent narrative.

Every actor on the map should have at least one impact — something you want that actor to do or stop doing. If there is nothing to say about behaviour for that who, merge them with another actor or stop treating them as separate.

### Impacts

An impact is the behaviour change you want from a given actor toward those outcomes: what they should start doing, do more of, do less of, or stop doing. It answers *how should this person or team behave differently?* — not *what are we building?* and not *what is the business outcome?* (that lives in the goal hierarchy above).

Good impacts are specific enough to recognise in the world. Someone could watch, read a transcript, pull a metric, or walk a journey and say whether it is happening. They usually lead with a verb the actor performs: completes, submits, shares, invites, triages, opts in, returns, finishes, escalates. In this skill's **shipped hierarchy templates**, keep each `IMPACT:` line to observable behaviour **without** embedded cadence targets, deadlines, SLA timing, or numeric bars — put those on `METRIC:` lines indented under that `IMPACT:` (and in hypotheses after `by` with the impact metric). In live facilitation you may still talk in tighter cadence; when writing the tree, move quotas to metric lines.

One impact is one movement of behaviour. If you mix two behaviours, split them. Do not treat a component, project name, epic title, or system as the impact — that belongs under deliverables (or under engineering planning), not as the behaviour itself. Do not stop at slogans like "better onboarding" with no observable picture.

Contrast: "Submits the order without calling support" describes behaviour; "New checkout microservice" describes a build. "Shares run highlights to social" is an impact headline; weekly share rate belongs on a `METRIC:` line under that impact; "Share sheet v2" is not an impact.


### Impact metrics (`METRIC:` under each `IMPACT:`)

Behaviour and usage proxies (e.g. weekly share rate, D7 retention, hours watched) that should move before goal-level `METRIC:` lines respond. They make each behaviour change testable on its own.

Example: *Shares run highlight to a social channel* with metric *share events per weekly active user*; *Finishes tutorial and first ranked match in the first session* with metrics *D1 ranked-match completion rate*; *Opens abuse report quickly* with metric *median hours to first moderator action*.

### Deliverables

Deliverables are candidate things to build, ship, or run that might help produce an impact. They are options and bets — useful for roadmap and prioritisation — not promises and not a substitute for naming behaviour. Phrase them at roadmap granularity: a capability, epic, experiment, or policy change someone could schedule, not a ten-year vision sentence.

Several deliverables under the same impact means different ways you might achieve that one behaviour change. Keep each option one clear idea; split merged features. A deliverable should not restate the goal, duplicate goal metric lines, or copy the impact sentence ("User posts weekly") — those stay where they belong.

Do not hide a grab-bag in one deliverable ("Everything for sharing"); do not use empty words like "Success" as if they were shippable work. If you cannot name a plausible thing to try, you probably need a sharper impact first.

Contrast: under an impact about sharing to social, "One-tap share sheet with clip" and "Seasonal badge asset pack" are deliverables — different bets on the same behaviour. "Grow monthly active players" is goal territory; share rate and cadence sit in metrics, not in the `IMPACT:` headline when using this skill's templates.



### Assumptions

An impact map carries two kinds of assumption, and both are already visible in the hypotheses templates:

- **Build assumption** — If we build this deliverable, the target actor will be impacted in a specific way (eg their behavior), measurable by the impact metric. This is a bet on delivery causing behaviour change.
- **Outcome assumption** — If the impact metric moves, the goal metric will follow. This is a bet on the behaviour change mattering to the outcome.

Teams use a validated learning approach to confirm or refute each belief and update the map as they learn — keeping evidence and learning visible:

- **Plan** — what to test, the smallest useful check, who owns it, and by when.
- **Validate** — run the check and collect evidence to confirm or refute the belief.
- **Learn** — what the team took away and how the bet, the map, or the next experiment updates.

The `templates/impact-map-hypotheses.md` (and `.txt`) already phrase both assumption types as testable sentences — they are the natural starting point. Use **abd-simple-validated-learning** to turn those sentences into a prioritised backlog of experiments with owners and explicit failure conditions when the team needs to validate before committing to build.

### Phased feature backlog

When delivery needs a time horizon, you extend the same map with a phased backlog: a sequence of timeboxes (months, quarters, or another convention you name once). Each phase holds scheduled options — concrete things you might ship or run. Every option stays tied to exactly one impact path on the map: the same actor and the same behaviour change that option is meant to support. That keeps sequencing honest: order is about *when* you might try something, not a separate story from *why* that something mattered. Orphan work shows up when an option does not link to a behaviour you care about.

---

## Example

Illustrative map (live-ops product): read as a **hierarchy**. Each `Goal` line carries its **goal metric** in angle brackets. Nested goals roll up. Under the finest goal, each `|- Actor` branch lists **impacts**; after `--`, **Q1 / Q2 / …** (or M1 / M2, quarters, months — name the convention once) are scheduled options for *that* impact only. Every feature still ties to one actor-and-behaviour path.

```text
Strengthen recurring revenue and engagement in the flagship title <net revenue retention; live-ops engagement targets for the title>
|- Grow monthly active players <verified MAU +20% vs baseline; week-over-week return among onboarded>
     |- Existing players (returning, past onboarding)
          Share run highlights to social <share attempts per weekly active player; target cadence at least weekly> -- Q1: One-tap share sheet with clip, Q2: Seasonal tournament badge, Q3: Friend-invite deep link from post-match
          Complete ranked matches regularly <ranked matches per active player per week; target at least three per week> -- Q1: Queue-time fairness pass, Q2: Streak bonus for consistent ranked play
     |- New players (first fourteen days after install)
          Finish onboarding and first ranked match in the first session <session-one ranked completion rate> -- Q1: Guided tutorial path with fewer dead ends, Q2: Optional skip for experienced players on a new device (abuse guardrails TBD)
```

Q1 / Q2 / Q3 here mean calendar quarters for the illustration; use whatever timeboxes the room agrees. Options on a line are different bets on the **same** impact, sequenced by timebox — not a second map.

## The shape of a good impact map

In substance: an outcome hierarchy (broad to the level you are mapping), then for that focus the actors who matter, the observable behaviour you want from each, and the deliverable options that might produce those behaviours. Optional goal metrics sit with the goal level they measure; optional behaviour proxies sit with the impacts (`METRIC:` under each **`IMPACT:`** on the prefix map). A phased backlog, when you need one, orders those deliverable options across timeboxes while preserving the same one-to-one link from each scheduled option to one impact path on the map.

---

## Build

Produce all six template outputs from the engagement sources; keep behaviour impacts honest; follow Core concepts (including the bullets under Goal).

1. Produce outputs from every template. Fill all files under `templates/` that define an output shape (`impact-map*.{md,txt}`). Strip maintainer Instructions blocks from stakeholder deliverables.
2. Apply the rules, then review like a peer. Use the bundled rules at the end of this file (they primarily reference the hierarchy `GOAL:` / `ACTOR:` / `IMPACT:` / `DELIVERABLE:` tree; ASCII and hypotheses must stay consistent with that tree).
3. Keep the bundled rules block honest. After editing `rules/*.md`:

- Outputs: One full map set per engagement (or version): hierarchy `.md` and `.txt`, ASCII `.md` and `.txt`, hypotheses `.md` and `.txt`, unless the user asked for a subset of formats.
- Hierarchy `.md` may include optional context before the tree; hierarchy `.txt` contains only tree lines and allowed optional labels (`NOTE:`, `ASSUMPTION:`, `METRIC:` under goals or impacts) plus an optional phased backlog table block.
- While writing: Use vocabulary from sources; keep verb-led impacts where natural.
- Persistence: *N/A* for this skill (file outputs only).

---

## Validate

Inspect the map as a product owner, developer, and facilitator would.

- Who is checking: Product owner (outcome and actor completeness); developer (clarity of behaviours and options); facilitator (collaboration and assumption coverage).
- Cross-artifact parity: hierarchy `.md` and `.txt` match; ASCII pair matches the same story; hypotheses pair matches the same story; all six align on goals, actors, impacts, and deliverables.

Checklist:

- Goal — Broader to finer `GOAL:` hierarchy; actors attach under the mapped `GOAL:`.
- Deliverables — Each deliverable sits under an impact it serves; phased backlog rows each name an impact on this map.
- Impacts — Observable behaviour for each actor.
- Actors — Situational who (segment, moment, context); everyone who can help or block the goal, scoped so labels match the behaviours underneath.
- Metrics — If used, `METRIC:` lines indented under a `GOAL:` record lagging proof for that level; keep each `GOAL:` a directional outcome headline. `METRIC:` lines indented under an `IMPACT:` hold usage or behaviour proxies.
- Rules pass — Generated maps meet each `rules/*.md` (goal outcome phrasing, observable impacts, goal-related situational actors, deliverable hypotheses, multi-actor assumptions or explicit none and same-file ancestry, phased backlog **Actor / impact** column).

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Multi-actor maps record assumptions or explicit none

**Scanner:** Manual review

For one engagement, **`impact-map.md`** and **`impact-map.txt`** (same tree) either make hidden dependencies visible or they fail a quick review. **Passing** means: when two or more distinct **`ACTOR:`** lines appear, the reader sees at least one **`ASSUMPTION:`** that could be tested, or an explicit **none** plus a one-line reason. Every **`DELIVERABLE:`** hangs under a full branch from **`GOAL:`** through **`ACTOR:`** and **`IMPACT:`** in that file. **Failing** means several actors and no **`ASSUMPTION:`** line at all, or **`DELIVERABLE:`** lines that are not anchored in the same tree.

#### DO

- When the tree has two or more distinct **`ACTOR:`** lines, include at least one **`ASSUMPTION:`** line that states a testable belief, dependency, or conflict across those branches.

  **Example (pass):** After four **`ACTOR:`** blocks, the file includes `ASSUMPTION: Moderator SLA holds if creator volume stays under X streams per week.`

- When no cross-branch assumption is needed, record that explicitly on one line.

  **Example (pass):** `ASSUMPTION: None identified - wholesale and retail tracks already use separate fulfillment with ops sign-off.`

#### DO NOT

- Omit **`ASSUMPTION:`** entirely when two or more **`ACTOR:`** lines appear in the same file.

  **Example (fail):** Five **`ACTOR:`** labels and zero **`ASSUMPTION:`** lines anywhere in the tree.

- Emit **`DELIVERABLE:`** lines that are not under a **`GOAL:`** with **`ACTOR:`** and **`IMPACT:`** ancestors in the same file.

  **Example (fail):** First substantive line is `DELIVERABLE: Mobile relaunch` with no **`GOAL:`** above it.

**Source:** Practice convention. Pair with **`rules/impact-map-phased-backlog-actor-impact.md`** for phased backlog **Actor / impact** cells.

### Rule: Deliverables are shippable options under impacts

**Scanner:** Manual review

This check applies to **`DELIVERABLE:`** lines under **`IMPACT:`** in **`impact-map.md`** / **`impact-map.txt`**. **Passing** means each line names a roadmap-sized bet (capability, epic, experiment, policy move) that could plausibly support the parent behaviour, one clear idea per line, with outcome and behaviour language kept in **`GOAL:`**, **`IMPACT:`**, and metrics where they belong. **Failing** means goal proof, vague bundles, non-shippable labels, or behaviour sentences parked under **`DELIVERABLE:`**.

#### DO

- Phrase each **`DELIVERABLE:`** as a roadmap-sized option that might create the parent impact.

  **Example (pass):** Under `IMPACT: Share run highlights to social` — `DELIVERABLE: One-tap share sheet with clip`.

- Use several **`DELIVERABLE:`** lines under one impact when they are different bets on the same behaviour.

  **Example (pass):** Same impact lists `DELIVERABLE: Native share extension` and `DELIVERABLE: Post-to-feed template`.

- Keep one shippable idea per line; split merged features.

  **Example (pass):** `DELIVERABLE: Seasonal badge asset pack` (single bet; not combined with unrelated UI work on the same line).

- Mirror the same deliverable names in hypotheses and ASCII outputs when those formats ship for the same engagement.

  **Example (pass):** Hierarchy shows `DELIVERABLE: Queue-time fairness pass`; hypotheses build bullet references the same wording for that feature.

#### DO NOT

- Put outcome language, behaviour sentences, or goal numeric proof in **`DELIVERABLE:`** that belong under **`GOAL:`**, **`IMPACT:`**, or on a **`METRIC:`** line under a **`GOAL:`**.

  **Example (fail):** `DELIVERABLE: Verified MAU +20% vs baseline` (that belongs on a **`METRIC:`** under the **`GOAL:`**, not as a shippable option).

- Use a vague grab-bag label instead of concrete options.

  **Example (fail):** `DELIVERABLE: Everything for sharing`.

- Use empty success labels as if they were work.

  **Example (fail):** `DELIVERABLE: Success`.

- Park observable behaviour under **`DELIVERABLE:`** instead of under **`IMPACT:`**.

  **Example (fail):** `DELIVERABLE: User posts weekly` (behaviour belongs under **`IMPACT:`**, not under **`DELIVERABLE:`**).

**Source:** `SKILL.md`, Core concepts / Deliverables.

### Rule: Goals read as business outcomes with METRIC lines for lagging proof

**Scanner:** Manual review

This check applies to **`GOAL:`** and **`METRIC:`** lines indented under those goals in **`impact-map.md`** / **`impact-map.txt`**. **Passing** means a credible hierarchy (broad to the level you are mapping), each **`GOAL:`** phrased as an outcome in the world, numeric proof on **`METRIC:`** under the level it measures, and headlines that stay directional rather than solution-led. **Failing** means launch-or-build language as the goal, or percent targets baked into the **`GOAL:`** headline when this skill expects them on **`METRIC:`** under that **`GOAL:`**.

#### DO

- Model goals as a hierarchy: broader organisational outcomes decompose into finer outcomes that roll up; use one **`GOAL:`** per level you need.

  **Example (pass):** `GOAL: Improve durable growth in the enterprise book` then nested `GOAL: Grow net revenue retention in the enterprise segment`.

- Keep the finest mapped **`GOAL:`** at a workshop-friendly horizon (often about a quarter or less when you timebox).

  **Example (pass):** Under a multi-year headline, the mapped focus is `GOAL: Grow monthly active players` for the next planning slice.

- Phrase each **`GOAL:`** as a business outcome (grow, reduce, achieve, strengthen) with clear object; put lagging proof on **`METRIC:`** under that level.

  **Example (pass):** `GOAL: Accomplish same-day checkout completion for domestic orders` with `METRIC: Same-day rate ninety percent plus (strategic)`.

- Keep each **`GOAL:`** line a directional headline at its altitude; express proof you moved on **`METRIC:`** where you measure.

  **Example (pass):** `GOAL: Grow monthly active players` with `METRIC: Verified MAU +20% vs baseline this quarter` on the lines below that goal.

- Anchor stakes readers recognise: revenue, adoption, risk, compliance, cost, market position, operational reliability.

  **Example (pass):** `GOAL: Reduce fraud loss in card-not-present checkout` under a revenue-and-risk story.

#### DO NOT

- Headline the **`GOAL:`** as build, ship, implement, or launch when the real measure is behaviour, revenue, or risk (put the build under **`DELIVERABLE:`**).

  **Example (fail):** `GOAL: Ship checkout v2`.

- Name an output or project as the goal when the goal is the outcome that output is meant to serve.

  **Example (fail):** `GOAL: Build moderation dashboard`.

- Use launch metaphors as the goal instead of the stakeholder outcome.

  **Example (fail):** `GOAL: Mobile app relaunch`.

- Put numeric bars in the **`GOAL:`** headline when this skill expects them on **`METRIC:`** under that outcome.

  **Example (fail):** `GOAL: Grow verified MAU by twenty percent this quarter` (split: short directional **`GOAL:`** plus **`METRIC:`** for the +20% bar).

**Source:** `SKILL.md`, Core concepts / Goal.

### Rule: Actors are situational people or organisations tied to the goal

**Scanner:** Manual review

This check applies to **`ACTOR:`** lines under the mapped **`GOAL:`** in **`impact-map.md`** / **`impact-map.txt`**. **Passing** means each label shows *who* in *what situation* can help or block that goal, split when behaviours differ, and never substitutes systems or products for people. **Failing** means bare categories, personified platforms, or one **`ACTOR:`** bucket hiding incompatible situations.

#### DO

- Name actors by situation: segment, lifecycle moment, channel, or context that matters for this goal, not the abstract category alone.

  **Example (pass):** `ACTOR: New mobile shoppers (first order within fourteen days)`.

- Make the situation visible in the label (cohort, geography, tenure, stress moment, contract window).

  **Example (pass):** `ACTOR: Tier-one support agents (queue A, business hours)`.

- Split when situations imply different behaviours under the same broad label.

  **Example (pass):** Separate `ACTOR: Day-one buyer` from `ACTOR: Renewal owner` when impacts differ.

- Keep labels short while still showing who and why the situation matters for the goal.

  **Example (pass):** `ACTOR: Payment acquirer partner (contract renewal window)`.

- Give every **`ACTOR:`** at least one **`IMPACT:`**; merge or drop actors with nothing behavioural to say.

  **Example (pass):** `ACTOR: Streamers in the spring campaign cohort` with at least one `IMPACT:` branch beneath it.

#### DO NOT

- Use bare categories with no situation when the map needs distinct behaviours.

  **Example (fail):** `ACTOR: Customers` with impacts that only apply to wholesale buyers, mobile guests, and admins (split or narrow).

- Cast a product, service, system, or platform as the actor.

  **Example (fail):** `ACTOR: The loyalty API` (put the system under **`DELIVERABLE:`**; name the person or team).

- Collapse incompatible situations into **`ACTOR: Users`** when impacts assume different groups or moments.

  **Example (fail):** One `ACTOR: Users` line with impacts that only make sense for parents, teens, and admins respectively.

- Use component names where a person or organisation is what helps or blocks.

  **Example (fail):** `ACTOR: The platform` instead of `ACTOR: Internal platform SRE rotation`.

**Source:** `SKILL.md`, Core concepts / Actors.

### Rule: Impact lines name observable behaviour for the actor

**Scanner:** Manual review

This check applies to **`IMPACT:`** lines under each **`ACTOR:`** in **`impact-map.md`** / **`impact-map.txt`**. **Passing** means each line answers how behaviour should change in a way someone could observe or measure, verb-led, one movement per line, with quotas and numeric bars on **`METRIC:`** lines indented under that **`IMPACT:`** instead of crammed into the headline. **Failing** means feature titles, components, or slogans with no observable picture.

#### DO

- Answer how this actor's behaviour should change in terms a reviewer could witness without opening a backlog tool.

  **Example (pass):** `IMPACT: Completes payment on mobile without switching to desktop when the bank supports in-app 3-D Secure.`

- Lead with a verb the actor performs (completes, submits, shares, invites, triages, opts in, returns, finishes).

  **Example (pass):** `IMPACT: Shares run highlights to social`.

- Keep the **`IMPACT:`** headline free of cadence quotas, day-N deadlines, SLA timing, and numeric bars; put those on **`METRIC:`** under that **`IMPACT:`**.

  **Example (pass):** `IMPACT: Opens every abuse report within one business day` with cadence detail moved to `METRIC: Median hours to first action; target under twelve`.

- State one behaviour movement per **`IMPACT:`**; split when two behaviours are mixed.

  **Example (pass):** Split `IMPACT: Finishes tutorial` and `IMPACT: Completes first ranked match` when they are two movements.

- Keep channel or qualitative guardrails in the impact phrase when they are not numeric bars (for example *without calling support*).

  **Example (pass):** `IMPACT: Submits the order without calling support`.

#### DO NOT

- Put system names, epic codes, or feature titles alone in **`IMPACT:`** with no behaviour clause.

  **Example (fail):** `IMPACT: New share sheet`.

- Use a component or tool name as if it were behaviour.

  **Example (fail):** `IMPACT: Moderation tool`.

- Ship slogans with no observable picture.

  **Example (fail):** `IMPACT: Better onboarding`.

- Mix two incompatible behaviours in one **`IMPACT:`** line.

  **Example (fail):** `IMPACT: Onboards faster and invites three friends in week one` (split if those are separate movements).

**Source:** `SKILL.md`, Core concepts / Impacts and Purpose (four questions).

### Rule: Phased backlog rows name the same actor and impact as the tree

**Scanner:** Manual review

This check applies to optional phased backlog tables in the same file as the **`GOAL:`** / **`ACTOR:`** / **`IMPACT:`** tree (**`impact-map.md`** / **`impact-map.txt`**). **Passing** means each row's **Actor / impact** cell repeats the **`ACTOR:`** label and **`IMPACT:`** line that branch already contains (same wording or obvious paraphrase), and the timebox convention is named once (for example in **`NOTE:`**). **Failing** means a scheduled feature paired with an actor/impact pair that does not appear in the tree, or silent mixing of timebox schemes.

#### DO

- For each phased row, fill the **Actor / impact** column so it matches one **`ACTOR:`** + **`IMPACT:`** path in that file.

  **Example (pass):** Tree contains `ACTOR: Existing players` and `IMPACT: Share run highlights to social`; backlog row `M1 | Share sheet with clip | Existing players / Share run highlights to social`.

- Use one timebox convention per file (for example M1..M4 or Q1..Q4) and record it in **`NOTE:`** once.

  **Example (pass):** `NOTE: M1-M4 below = calendar months in this example; use quarters if the brief says Q1-Q4.`

#### DO NOT

- List a feature whose **Actor / impact** cell does not match any actor-and-impact branch in the tree.

  **Example (fail):** Backlog cell `Streamers / Daily clip` when the tree only has `IMPACT: Broadcast this title during the campaign window`.

- Switch timebox schemes row by row without stating the convention.

  **Example (fail):** Mixing `M1`, `Q2`, `Sprint 4` in the same phased table with no **`NOTE:`** explaining the scheme.

**Source:** Practice convention.
<!-- execute_rules:bundle_rules:end -->
