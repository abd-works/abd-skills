# Service Level Objectives — Examples

## Typical SLO matrix structure

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

---

## The shape of a good SLO matrix

Each SLO row uses this skeleton:

| Scope | Category | SLI (what we measure) | SLO (target × volume × percentage) | Measurement | Owner |
|---|---|---|---|---|---|

**Example rows:**

| System | Availability & Reliability | API uptime | 99.9% uptime over 28-day rolling window, at all production traffic | CloudWatch synthetic + 5xx ratio | Platform team |
| Parent epic: Orders | Performance & Scalability | p99 latency `POST /orders` | < 300 ms at 10 000 req/day at 99.9% | Datadog APM | Orders team |
| Story: Place high-value order | Availability & Reliability | Order durability | Zero loss at any volume at 100% within commit window | Outbox replay audit | Orders team |
| System | Security & Compliance | Time to revoke leaked token | < 5 min at any volume at 99% | Auth0 audit log + sec tooling | Security team |
| System | Maintainability & Supportability | MTTR for sev-1 incidents | < 1 hour at all incidents at 95% | Incident-management tool | On-call rotation |
