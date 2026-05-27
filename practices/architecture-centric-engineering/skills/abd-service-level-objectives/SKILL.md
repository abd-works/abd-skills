---
name: abd-service-level-objectives
description: >-
  Capture the non-functional requirements (NFRs) of a system as concrete
  Service Level Indicators, Objectives, and Agreements (SLI/SLO/SLA) tied
  to a specific scope — a story, an epic, a parent epic, or the whole
  system. NFRs are organised into six categories (Performance &
  Scalability, Availability & Reliability, Security & Compliance, Usability
  & Accessibility, Maintainability & Supportability, Interoperability &
  Compatibility). Every objective states a target at a volume at a
  percentage so it can be measured, alerted on, and refused.
---
# abd-service-level-objectives

## Purpose

A non-functional requirement that cannot be measured is a wish. Teams that ship without measurable NFRs discover the truth in production — too late, too expensive, sometimes too public. This skill turns each NFR into a concrete **Service Level Indicator** (what is measured), **Service Level Objective** (the target on that indicator), and where a customer-facing commitment exists, a **Service Level Agreement**. Critically, each objective is scoped to the **functional area** it applies to: a single user story, an epic, a parent epic, or the system as a whole. Read-mostly catalogue browsing does not need the durability guarantee of order-placement, and treating them the same wastes money on the former and risks failure on the latter.

## When to use this skill

Load this skill when **any** of the following apply:

- An architecture **outline and blueprint** exist and the team needs to commit to **measurable non-functional targets** before further build-out.
- A **story or epic** has been described and someone in the room is asking "how fast?", "how many users?", "what happens when it fails?" — those questions deserve numbers, not gut feels.
- An **incident review** revealed that the team never had a target for the failing dimension; setting one prevents the next repeat.
- A **customer or compliance commitment** is being drafted (SLA) and the engineering team needs to translate it into internal SLOs and SLIs.
- The product is being **classified by criticality** — mission-critical writes vs. high-volume reads vs. background reporting — and each class needs its own target set.

## What is a Service Level Indicator / Objective / Agreement?

| Term | Definition | Example |
|---|---|---|
| **SLI** (Indicator) | The *thing being measured*. Always a ratio or a quantity over a time window. | "p99 response time for `POST /orders`" |
| **SLO** (Objective) | The *internal target* on the SLI, expressed as **a target value at a volume at a percentage**. | "< 300 ms p99 on `POST /orders`, sustained over 10 000 requests / day, met 99.9% of the time over a 28-day window" |
| **SLA** (Agreement) | The *external commitment* (usually contractual), looser than the SLO so internal teams have headroom. | "99.5% monthly availability on the Orders API, with credits below threshold" |

The discipline of this skill is: every NFR you commit to becomes one row of the SLO matrix with **target × volume × percentage**, scoped to a clearly named **functional area** so the right level of investment goes to the right operations.

---

## Core concepts

### Six NFR categories

NFRs span six categories. Every SLI/SLO row in this skill's templates picks one category so the matrix is browsable by concern. The categories are:

| Category | What it covers |
|---|---|
| **Performance & Scalability** | Speed, throughput, capacity, growth headroom. Examples: page load, API latency, requests per second, concurrent users. |
| **Availability & Reliability** | Uptime, fault tolerance, mean time between failures, recovery objectives. Examples: monthly uptime %, RPO (data loss target), RTO (recovery time target). |
| **Security & Compliance** | Data protection, authorization correctness, encryption at rest/in transit, regulatory adherence. Examples: time-to-revoke a stolen token, % of records encrypted, compliance audit pass. |
| **Usability & Accessibility** | UX quality, accessibility standards, learnability. Examples: WCAG 2.1 AA conformance, task-completion rate on key flows. |
| **Maintainability & Supportability** | Ease of change, debuggability, deployment without downtime, MTTR for production issues. Examples: deployment frequency, mean time to recover, change-failure rate. |
| **Interoperability & Compatibility** | Integration with external systems, browser/device compatibility, API contract stability. Examples: % of supported browsers passing E2E, breaking changes per quarter. |

### Scope: where the SLO lives in the story map

An NFR is rarely a property of "the whole system". The same system can be **mission-critical** for one path (order placement: durable, no errors, audited) and **best-effort** for another (recommendations: high volume, eventual consistency, occasional misses acceptable). This skill places each SLO at the right **scope** in the story map (or feature tree):

| Scope | When to set NFRs here |
|---|---|
| **System** | An NFR that genuinely applies to the whole product (auth correctness, encryption, top-level uptime). |
| **Parent epic** | An NFR that applies to a coherent group of features (all order-related flows, all reporting flows). |
| **Epic** | An NFR that applies to one epic but not its siblings (live editing within an epic where most of the epic is offline). |
| **Story** | An NFR specific to a single user-visible scenario (a "place order" story that is the highest-criticality write in the system). |

If you do not have a story map, the **system** and **parent epic** scopes are usually enough. The richer the map, the more precisely you can target investment.

### The target-volume-percentage shape

Every well-formed SLO has three numbers:

```
{target value}  at  {volume}  at  {percentage}
```

- **Target value** — the threshold being met (e.g. 300 ms, 99.9% uptime, zero data loss).
- **Volume** — *the conditions under which the target is claimed*. Without volume, a number is meaningless. (e.g. "at 10 000 requests/day", "during business hours", "across both regions concurrently").
- **Percentage** — *how often the target must be met over the measurement window* (e.g. "99.9% of the time over a 28-day window"). A 100% claim is almost always wrong — leave headroom for incidents.

Examples:
- "**p99 < 300 ms** on `POST /orders` at **10 000 req/day** **99.9% of the time over 28 days**." (Performance & Scalability)
- "**Zero data loss** on order writes at **all volumes** **100% of the time within the durability window**." (Availability & Reliability — durability)
- "**< 5 minutes time-to-revoke** a leaked token at **any volume** **99% of the time**." (Security & Compliance)

### Error budgets and burn rates

Every SLO with a percentage less than 100% has an **error budget** equal to `1 − target`. Burning the budget tells the team when to slow down feature work and shore up reliability — and conversely, an under-spent budget gives permission to take risk. The skill's template ships a small section for error-budget policy: what the team does when the budget is at 50% remaining, 25%, 0%.

---

## Example

A mid-size SaaS application's SLO matrix typically has 10–20 rows across the six categories, distributed across one system-level set, three parent-epic sets, and a handful of story-specific rows for the highest-criticality scenarios.

```
docs/architecture/service-level-objectives.md
├── 1. Scope and how to read this document
├── 2. Criticality classification          ← which features are mission-critical vs. best-effort
├── 3. System-level SLOs                   ← applies everywhere
├── 4. Parent-epic SLOs                    ← per-area (Orders, Catalogue, etc.)
├── 5. Story-level SLOs                    ← specific high-criticality scenarios
├── 6. Error-budget policy                 ← when to slow feature work
└── 7. SLA section                         ← contractual commitments (if any)
```

## The shape of a good SLO matrix

```
Each SLO row uses this skeleton:

| Scope | Category | SLI (what we measure) | SLO (target × volume × percentage) | Measurement | Owner |
|---|---|---|---|---|---|

Example:
| System | Availability & Reliability | API uptime | 99.9% uptime over 28-day rolling window, at all production traffic | CloudWatch synthetic + 5xx ratio | Platform team |
| Parent epic: Orders | Performance & Scalability | p99 latency `POST /orders` | < 300 ms at 10 000 req/day at 99.9% | Datadog APM | Orders team |
| Story: Place high-value order | Availability & Reliability | Order durability | Zero loss at any volume at 100% within commit window | Outbox replay audit | Orders team |
| System | Security & Compliance | Time to revoke leaked token | < 5 min at any volume at 99% | Auth0 audit log + sec tooling | Security team |
| System | Maintainability & Supportability | MTTR for sev-1 incidents | < 1 hour at all incidents at 95% | Incident-management tool | On-call rotation |
| Parent epic: Storefront | Usability & Accessibility | WCAG 2.1 AA conformance | 100% of public-facing pages at 100% | axe-core CI checks | Frontend team |
```

---

## Build

**Goal:** Produce `docs/architecture/service-level-objectives.md` mapping each functional area to its SLI/SLO/SLA across the six NFR categories.

1. **Establish scope vocabulary.** If a story map exists (`docs/stories/story-map.md` or similar), use its hierarchy (system → parent epic → epic → story) as the scoping vocabulary. If not, fall back to system + parent epic only.

2. **Classify features by criticality.** Walk the story map and tag each parent epic / epic / story as **mission-critical**, **business-important**, or **best-effort**. Criticality drives how aggressive the SLOs need to be and where the team should invest. Capture the classification as section 2 of the output.

3. **Set system-level SLOs.** Start with NFRs that apply to the whole product: top-level availability, security (auth, encryption, audit), maintainability (MTTR, deployment frequency, change-failure rate). One row per concern, every row in target-volume-percentage shape.

4. **Set parent-epic SLOs.** For each parent epic, walk the six categories and ask "does this parent epic have a target distinct from the system default?" If yes, add a row. Common cases: Orders need tighter latency than Reporting; Catalogue needs higher cache-hit-rate than Identity.

5. **Set story-level SLOs only for high-criticality stories.** Most stories inherit their parent epic's SLOs. Add a story-level row only for the highest-criticality writes or the highest-volume reads where the parent-epic target is materially wrong.

6. **Define the error-budget policy.** State explicitly what the team does at each burn threshold (50%, 25%, 0% of budget remaining). Without a policy, an error budget is a thermometer with nobody acting on the reading.

7. **List SLAs separately.** If the product has contractual commitments to customers, list them in a final section. Each SLA should be **looser than the internal SLO** that supports it (typical pattern: SLO 99.9%, SLA 99.5%).

8. **Validate against the rules** bundled at the end of this `SKILL.md`.

9. **Bundle this skill's rules into `SKILL.md`** when you have edited any `rules/*.md`:

   ```bash
   python skill-builder/skills/abd-author-practice-skill/scripts/bundle_rules_into_skill_md.py --skill-root architecture-centric-engineering/skills/abd-service-level-objectives
   ```

---

## Validate

**Goal:** Inspect the produced SLO matrix the way an SRE / architect / product owner would inspect any non-functional document.

- **Who is checking:** SRE / Platform (are the SLIs actually measurable today?), Product Owner (does the criticality classification match how the business sees the features?), Security/Compliance (are the security objectives consistent with the regulatory framework?).
- **Cross-artifact parity:** Every parent epic in the story map either appears in the SLO matrix or is explicitly noted as inheriting system defaults. Every scope referenced in a row exists in the story map (no orphan epic names).

Checklist for the **produced matrix**:

- **Every SLO has target × volume × percentage** — no bare "fast", "highly available", "secure"; no target without a volume condition; no percentage of 100% on availability claims.
- **Every row picks one of the six NFR categories** — Performance & Scalability, Availability & Reliability, Security & Compliance, Usability & Accessibility, Maintainability & Supportability, Interoperability & Compatibility.
- **Every row has a named scope** — system, parent epic, epic, or story — and that scope exists in the story map (or there is an explicit "no story map; system+parent-epic only" statement).
- **Every SLI is measurable today** — names a real tool (Datadog APM, CloudWatch, axe-core CI, an audit log) or a planned tool with an owner who will land it.
- **Error-budget policy is concrete** — actions tied to thresholds (50% / 25% / 0% remaining), not "review periodically".
- **SLAs (if any) are looser than the SLOs that support them** — never the same number; the internal target has headroom over the external commitment.
- **Criticality classification is explicit** — section 2 marks each parent epic / story as mission-critical / business-important / best-effort.

---

## Deploy

This skill ships IDE-deployable files under `ide-files/`. Deploy them to any project:

```powershell
.\skills\skill-builder\abd-author-practice-skill\scripts\Deploy-SkillOutputs.ps1 -SkillPath skills/architecture-centric-engineering/abd-service-level-objectives -ProjectRoot <target-project> -Force
```

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Error-budget policy states concrete actions at named thresholds

Every SLO matrix with rows whose percentage is less than 100% has an **error-budget policy section** stating concrete actions the team takes at named burn thresholds. A thermometer is useless if nobody acts on the reading; the policy turns the burn rate into operational decisions. Standard thresholds are **50%**, **25%**, and **0%** remaining over the measurement window. Failing means a policy with no thresholds, thresholds with no actions ("review periodically"), or a matrix that has error budgets but no policy section at all.

#### DO

- Include a policy table with one row per named threshold and a concrete action in plain language.

  **Example (pass):**

  | Budget remaining | Action |
  |---|---|
  | > 50% | Normal feature work; experiment with riskier changes if budget supports it. |
  | 25–50% | Caution. Pause large migrations and new infrastructure introductions for affected service. |
  | < 25% | Reliability work prioritised next sprint; feature work only on low-risk paths. |
  | 0% | Feature freeze on the affected scope until budget recovers above 25%. |

- State who owns each action and how the burn rate is calculated and reviewed.

  **Example (pass):** "Burn rate is calculated weekly on a 28-day rolling window. The on-call SRE reports it in the engineering operations review. Feature-freeze decisions at 0% are made by the engineering manager + product owner together."

- For SLOs without an error budget (100% targets like zero data loss, encryption coverage), state explicitly that the absolute-target nature means there is no budget — any miss is an incident.

  **Example (pass):** "Targets at 100% (durability, encryption coverage) have no error budget. Any miss is a sev-1 incident with full post-mortem."

#### DO NOT

- Ship the matrix with error budgets implicit in the percentages but no policy section.

  **Example (fail):** Section 5 of the matrix has 12 rows with percentages from 95% to 99.95%. There is no section 6 describing what happens when those budgets burn down. The numbers are reporting, not engineering policy.

- Use vague verbs in the actions column.

  **Example (fail):** Threshold "< 25% remaining" → action "Review and consider reliability work." (What is reviewed? By whom? What triggers actual work?)

- State a policy that no team actually applies.

  **Example (fail):** "Feature freeze at 0% budget" written down, but in practice the team has continued shipping new features through three consecutive budget exhaustions with no freeze. Either bring the team into compliance with the policy or rewrite the policy to match reality and call out the gap.

**Source:** Practice-skill authoring convention (abd-service-level-objectives); SLOs without policy are surveillance, not engineering.

### Rule: SLA is looser than the supporting SLO

When the product has external commitments (SLAs), each SLA must be **looser** than the internal SLO that supports it — never the same number, never tighter. The internal team needs operational headroom to act on the SLO before the SLA is breached. Standard pattern: SLO 99.9%, SLA 99.5% — the 0.4% margin is what gives the team room to detect and respond to incidents before customers can claim a breach. Failing means publishing an SLA equal to or tighter than the SLO, citing the SLO directly in customer contracts, or having an SLA with no internal SLO behind it at all.

#### DO

- For each SLA row, name the supporting internal SLO row and confirm the SLA threshold is strictly looser.

  **Example (pass):** SLA "99.5% monthly availability on Orders API" supported by internal SLO "API uptime 99.9% over a 28-day window". The 0.4% gap is the team's operational headroom.

- When negotiating a new SLA, set the SLO first and the SLA at least one tier looser (e.g. 99.99% SLO → 99.9% SLA, or 99.9% SLO → 99.5% SLA).

  **Example (pass):** New enterprise contract proposes 99.95% availability. The team confirms an internal SLO of 99.99% is achievable; the SLA is set at 99.95%.

- State the supporting SLO explicitly in the SLA section so the relationship is visible to both engineering and legal/sales.

  **Example (pass):** SLA table includes a column "Supporting internal SLO" linking back to the row in section 3 or 4.

#### DO NOT

- Publish an SLA equal to the supporting SLO.

  **Example (fail):** Internal SLO 99.9% availability; SLA in customer contract: 99.9% availability. The first incident that burns half the error budget puts the team at imminent SLA breach with no headroom.

- Publish an SLA tighter than the internal SLO.

  **Example (fail):** Internal SLO 99.5%, SLA promises 99.9%. Engineering has no way to detect breach before customers experience it.

- Ship the matrix with SLAs but no named supporting SLO rows.

  **Example (fail):** Section 7 lists customer SLAs (99.5% Orders, 99.9% Enterprise) but the matrix has no internal SLO rows for those endpoints. Engineering has no way to know whether the team is on or off the SLA at any given moment.

**Source:** Practice-skill authoring convention (abd-service-level-objectives); the SLO–SLA gap is the engineering team's operational headroom.

### Rule: Every SLO row has a named scope and one NFR category

Every row in the SLO matrix must name its **scope** (system, parent epic, epic, or story) and pick exactly one of the six **NFR categories** (Performance & Scalability, Availability & Reliability, Security & Compliance, Usability & Accessibility, Maintainability & Supportability, Interoperability & Compatibility). Scope is what makes the right level of investment go to the right operations: read-mostly catalogue browsing does not need order-placement durability, and the matrix should make that distinction visible. Failing means a row with no scope, a row scoped to "the system" when it really applies to one epic, a row that picks two categories, or a row that picks a category outside the six.

#### DO

- Name the scope in the row's Scope column using one of: `system`, `parent epic: {name}`, `epic: {name}`, `story: {name}`.

  **Example (pass):** Scope cell reads `parent epic: Orders` — the row applies to every story under the Orders parent epic but does not impose itself on Catalogue or Reporting.

- When a parent-epic-level target genuinely overrides the system default, write the row at parent-epic scope and let the matrix make the override visible.

  **Example (pass):** System availability SLO = 99.9%. Orders parent-epic availability SLO = 99.95% (tighter). Both rows present; readers see Orders is intentionally tighter.

- Pick exactly one NFR category from the canonical six. If a target genuinely spans two categories, split it into two rows.

  **Example (pass):** "Time-to-revoke a leaked token" is **Security & Compliance**. The fact that fast revocation is also a *performance* concern does not change the category — the SLI is a security indicator.

#### DO NOT

- Omit the scope column or leave it blank.

  **Example (fail):** A row with SLI "Catalogue cache hit rate" but no Scope cell — readers cannot tell whether this applies to the whole system or just one epic.

- Scope every row to "system" because "everything matters to everyone".

  **Example (fail):** Order durability, catalogue cache hit rate, and reporting job throughput all scoped to `system`. The matrix becomes a list of generic numbers and loses the criticality signal.

- Pick a category outside the canonical six ("Performance and Security", "Other", "Cross-cutting").

  **Example (fail):** Category column reads "Performance & Security" — pick one. The architecture mechanism that *implements* the target may span both, but the SLI itself measures one.

- Scope a row to a story when its parent epic's SLO already covers it.

  **Example (fail):** Twenty stories each get their own story-scoped latency row that is identical to the parent epic's row. The matrix bloats; readers cannot find the genuinely story-specific targets. Story-scoped rows exist only when the target differs materially from the parent epic.

**Source:** Practice-skill authoring convention (abd-service-level-objectives); scope and category are how the matrix stays browsable and actionable.

### Rule: Every SLO row has target × volume × percentage

Every Service Level Objective in the matrix must specify three numbers: a **target value** (the threshold being met), a **volume** (the conditions under which the target is claimed), and a **percentage** (how often the target must be met over a measurement window). Without all three, the row is a wish, not an objective — a "fast API" can be made true or false by the next reader, but "p99 < 300 ms at 10 000 req/day at 99.9% over 28 days" cannot. Failing means a row missing the volume condition, a percentage of 100% on an availability claim where incidents are inevitable, or a target stated only in adjectives ("highly available", "fast", "secure").

#### DO

- Write every SLO as `{target value} at {volume} at {percentage}` (or as three filled cells in a table that compose to the same shape).

  **Example (pass):** "p99 < 300 ms on `POST /orders` at 10 000 req/day at 99.9% over a 28-day rolling window."

- Choose a percentage less than 100% for anything subject to real-world failure (availability, latency, success rate). 100% is appropriate only for absolute requirements (zero data loss, zero unauthorized writes, encryption coverage).

  **Example (pass):** "Order durability: zero data loss at any volume at 100% within the commit window" — correct because data loss is a hard requirement.

  **Example (pass):** "API uptime: < 0.1% error rate at production traffic at 99.9% over 28 days" — correct because perfect availability is impossible and 99.9% has a real error budget.

- Make the volume realistic and named. "Peak hour", "10 000 req/day", "during business hours", "across both regions concurrently" all qualify.

  **Example (pass):** "Cache hit rate ≥ 95% at all reads at 99% over a 24-hour window." (Volume = "all reads", time window stated.)

#### DO NOT

- Ship a row with no volume condition.

  **Example (fail):** "API latency < 300 ms at 99.9%." — at what request rate? Cold start? Peak load? The row is unmeasurable in practice.

- Claim 100% on a probabilistic dimension.

  **Example (fail):** "API uptime 100% over a 28-day window." — incidents are inevitable; the team will burn out chasing a target it cannot hit, or pretend the target was met when it was not.

- State an objective in adjectives.

  **Example (fail):** "The system must be highly available, performant, and secure." — none of the three is decidable.

- Use a SLI that is not actually being measured today, without naming the planned tool and owner.

  **Example (fail):** SLI column reads "user-perceived latency" with no measurement column entry. If the tool does not exist yet, the row should name the tool that will measure it and the owner who will land it; otherwise the objective is unsupported.

**Source:** Practice-skill authoring convention (abd-service-level-objectives); the target-volume-percentage shape is the central discipline of this skill.
<!-- execute_rules:bundle_rules:end -->
