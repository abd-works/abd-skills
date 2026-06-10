# {ProductName} — Service Level Objectives

> **Status:** Draft / Approved
> **Owner:** {SRE / Platform team}
> **Last updated:** YYYY-MM-DD
>
> **Purpose.** Concrete, measurable non-functional targets for {ProductName}, scoped to the right functional area. Every objective uses the shape **target × volume × percentage**. Linked from the [architecture outline](./architecture-outline.md) and the [story map](../stories/story-map.md).

---

## 1. How to read this document

- **SLI** — Service Level Indicator: the thing being measured.
- **SLO** — Service Level Objective: the internal target, written as `{value} at {volume} at {percentage}`.
- **SLA** — Service Level Agreement: external (typically contractual) commitment; always looser than the supporting SLO.
- **Scope** — where the objective applies: `system`, `parent epic: {name}`, `epic: {name}`, or `story: {name}`.
- **Category** — one of the six NFR categories (Performance & Scalability, Availability & Reliability, Security & Compliance, Usability & Accessibility, Maintainability & Supportability, Interoperability & Compatibility).

---

## 2. Criticality classification

Walk the story map and tag each parent epic / epic / story by criticality. Investment in SLOs follows criticality.

| Scope | Criticality | Why |
|---|---|---|
| **System** | mission-critical | Auth, encryption, audit — failure has legal/financial consequences. |
| **Parent epic: Orders** | mission-critical | Revenue-bearing writes; durability is a hard requirement. |
| **Parent epic: Catalogue** | business-important | Read-mostly; cache staleness acceptable within bounds. |
| **Parent epic: Reporting** | best-effort | Analytical; delays of hours are tolerable. |
| **Story: Place order > $10 000** | mission-critical | High-value transaction; audit trail is non-negotiable. |
| **Story: Browse catalogue (anonymous)** | best-effort | Cached at edge; degraded experience acceptable during incidents. |

---

## 3. System-level SLOs

Apply across the whole product unless overridden by a more specific scope.

| Category | SLI | SLO (target × volume × percentage) | Measurement | Owner |
|---|---|---|---|---|
| Availability & Reliability | API uptime (5xx ratio) | < 0.1% errors at production traffic at 99.9% over a 28-day rolling window | CloudWatch + Datadog synthetic | Platform team |
| Availability & Reliability | RPO (data loss) | Zero loss on committed writes at any volume at 100% | Outbox replay audit + WAL backup verification | Platform team |
| Availability & Reliability | RTO (recovery time) | < 30 min to recover from region failover at any volume at 99% | DR drill quarterly | Platform team |
| Security & Compliance | Time-to-revoke leaked credential | < 5 min from incident detection at any volume at 99% | Auth0 audit log + sec tooling | Security team |
| Security & Compliance | Encryption-at-rest coverage | 100% of records at all data stores at 100% | Cloud provider compliance scan | Security team |
| Maintainability & Supportability | MTTR for sev-1 incidents | < 1 hour at all sev-1 occurrences at 95% over a quarter | Incident management tool | On-call rotation |
| Maintainability & Supportability | Deployment frequency | ≥ 5 production deploys per week at normal sprint cadence at 80% of weeks | CI/CD pipeline metrics | Engineering |
| Maintainability & Supportability | Change-failure rate | < 15% of deploys cause a rollback at all deploys at 90% over a quarter | CI/CD + incident log | Engineering |
| Interoperability & Compatibility | Browser compatibility | Chrome / Safari / Firefox / Edge — last 2 major versions at all release builds at 100% | Playwright cross-browser CI | Frontend team |

---

## 4. Parent-epic SLOs

Tighten or relax the system defaults per parent epic when needed.

### 4.1 Parent epic: Orders (mission-critical)

| Category | SLI | SLO | Measurement | Owner |
|---|---|---|---|---|
| Performance & Scalability | p99 latency `POST /orders` | < 300 ms at 10 000 req/day at 99.9% | Datadog APM | Orders team |
| Performance & Scalability | Throughput | ≥ 50 req/s sustained at peak hour at 99% | Datadog APM | Orders team |
| Availability & Reliability | Endpoint availability | < 0.05% errors at peak traffic at 99.95% (tighter than system) | Datadog APM | Orders team |
| Security & Compliance | PCI scope containment | Zero card data outside vault at all transactions at 100% | Static analysis + vault audit | Security + Orders |

### 4.2 Parent epic: Catalogue (business-important)

| Category | SLI | SLO | Measurement | Owner |
|---|---|---|---|---|
| Performance & Scalability | p99 latency `GET /products/:sku` | < 100 ms at 1 M req/day at 99% | Datadog APM | Catalogue team |
| Performance & Scalability | Cache hit rate | ≥ 95% at all reads at 99% over a 24-hour window | Redis metrics | Catalogue team |
| Availability & Reliability | Stale-but-serving on cache miss | Stale content acceptable < 24 h at any volume at 100% | Cache-control headers | Catalogue team |

### 4.3 Parent epic: Storefront (business-important)

| Category | SLI | SLO | Measurement | Owner |
|---|---|---|---|---|
| Performance & Scalability | First contentful paint | < 1.5 s at all production sessions at 75th percentile | RUM (real user monitoring) | Frontend team |
| Usability & Accessibility | WCAG 2.1 AA conformance | 100% of public pages at all release builds at 100% | axe-core CI | Frontend team |

### 4.4 Parent epic: Reporting (best-effort)

| Category | SLI | SLO | Measurement | Owner |
|---|---|---|---|---|
| Performance & Scalability | Report generation time | < 5 min for a 30-day report at 1 000 reports/day at 95% | Job queue metrics | Reporting team |
| Availability & Reliability | Job success rate | ≥ 98% at all queued jobs at 99% over a 28-day window | Job queue metrics | Reporting team |

---

## 5. Story-level SLOs

Add rows only for stories whose criticality differs materially from their parent epic.

| Scope | Category | SLI | SLO | Measurement | Owner |
|---|---|---|---|---|---|
| Story: Place order > $10 000 | Security & Compliance | Audit-trail completeness | 100% of transactions audited within 1 min at all transactions at 100% | Audit-log ingestion check | Compliance |
| Story: Cancel order within 5 min of placement | Availability & Reliability | Cancellation succeeds before fulfilment trigger | 100% at all orders < 5 min old at 100% | Outbox sequence ordering check | Orders team |
| Story: Bulk export reports | Performance & Scalability | Export completion time | < 15 min for ≤ 1 M rows at 50 exports/day at 95% | Job queue metrics | Reporting team |

---

## 6. Error-budget policy

Every SLO with a percentage less than 100% has an error budget = `1 − target`. The policy below states what the team does as the budget burns down.

| Budget remaining | Action |
|---|---|
| **> 50%** | Normal feature work. Continue planned development; experiment with riskier changes if the budget supports it. |
| **25–50%** | Caution. Pause non-essential risky changes (large migrations, new infrastructure introductions). Tighten code-review for the affected service. |
| **< 25%** | Reliability work prioritised. The next sprint focuses on reducing burn rate: load testing, dependency hardening, incident-cause fixes. Feature work continues only on low-risk paths. |
| **0% (budget exhausted)** | Feature freeze for the affected scope until the budget recovers above 25%. Customer comms drafted if external impact is likely. |

Burn rate is calculated weekly on a 28-day rolling window and reported in the engineering operations review.

---

## 7. Service Level Agreements (external commitments)

SLAs are looser than the internal SLOs that support them so the team has operational headroom. Each row links to the customer-facing contract.

| Customer / contract | Commitment | Supporting internal SLO | Penalty / credit |
|---|---|---|---|
| All paid plans (T&Cs section 7) | 99.5% monthly availability on the Orders API | System SLO row "API uptime" (99.9%) | Service credit per outage hour; capped at 30% of monthly fee |
| Enterprise plan (MSA Appendix B) | 99.9% monthly availability + 4-hour P1 response | System SLOs + MTTR row | Service credit per outage hour; uncapped within month |

---

## See also

- [`architecture-outline.md`](./architecture-outline.md) — the system at a glance.
- [`architecture-blueprint.md`](./architecture-blueprint.md) — components and mechanisms that bear these SLOs.
- [`architecture-reference.md`](./architecture-reference.md) — deep-dive on the mechanisms that implement availability, security, observability.
- [`../stories/story-map.md`](../stories/story-map.md) — story map providing the scope vocabulary used here.
