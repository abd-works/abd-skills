# Architecture Outline — Examples

## Typical outline for a web-plus-API SaaS

```
{SystemName} — Architecture Outline
├── 1. Platform diagram          ← React SPA + Node API + Postgres + Redis
├── 2. Layered architecture      ← Presentation / Application / Domain / Infra
├── 3. System context            ← actors + 3 external systems
├── 4. Deployment topology       ← AWS: CloudFront → ALB → ECS → RDS
├── 5. Guiding principles        ← "Domain never imports infrastructure", etc.
├── 6. Technology stack          ← runtime + framework + library + tool per layer
├── 7. Major systems catalogue   ← 5 named subsystems, 1 line each
└── 8. Decision records          ← 3 ADRs (platform, style, deployment)
```

---

## The shape of a good outline

```
{Title} — Architecture Outline

1. Platform Diagram
   {diagram}
   {≤2 sentence caption}

2. Layered Architecture
   {diagram}
   {≤3 sentence caption naming dependency direction}

3. System Context
   {diagram}
   {≤2 sentence caption naming actors and external systems}

4. Deployment Topology
   {diagram}
   {≤3 sentence caption naming environments and hosts}

5. Guiding Principles
   - {Principle 1, one sentence, decidable}
   - {Principle 2, one sentence, decidable}
   - ... (5–10 total)

6. Technology Stack
   | Layer | Technology | Version | Purpose |
   |---|---|---|---|
   | ... |

7. Major Systems
   | System | One-line description | Primary owner / module |
   |---|---|---|
   | ... |

8. Decision Records
   - ADR-001: {chosen platform} — {one-line consequence}
   - ADR-002: {chosen architectural style}
   - ADR-003: {chosen deployment model}
   (each ADR is a separate file under docs/architecture/decisions/)
```
