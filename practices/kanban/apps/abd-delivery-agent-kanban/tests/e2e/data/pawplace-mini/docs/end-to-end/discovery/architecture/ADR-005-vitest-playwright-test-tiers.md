# ADR-005: Vitest and Playwright test tiers

> **Status:** Accepted
> **Date:** 2026-05-31
> **Deciders:** Engineer (discovery)

## Context

PawPlace mini needs fast feedback on domain rules (stock, cart, checkout) and confidence on the browser checkout spine. The blueprint names four test tiers; the team must pick concrete runners before specification and engineering.

## Decision

We will use **Vitest** for Domain, Application, and Integration tiers and **Playwright** for E2E browser tests against the dev stack.

## Options considered

| Option | Pros | Cons | Why rejected (or chosen) |
|---|---|---|---|
| **Vitest + Playwright (chosen)** | Fast unit loop; real browser for checkout | Two runners to maintain | **Chosen** — aligns with TypeScript MERN stack |
| Jest + Cypress | Familiar to many teams | Slower unit defaults; Cypress less suited to API-heavy flows | Rejected — Vitest speed matters for domain-heavy modules |
| E2E-only | Simple pipeline | Slow feedback; domain bugs found late | Rejected — violates guiding principle for fast domain tests |

## Consequences

**Positive:**
- Domain tests run without MongoDB or StripeWave using fakes.
- Playwright covers find-store → browse → cart → pay → confirm path.

**Negative / trade-offs:**
- CI must provision MongoDB (container) for integration tier.

**Neutral:**
- E2E runs against staging or local compose; not every PR need run full Playwright if integration covers module contracts.

## Compliance / verification

- Each module ships at least one domain test file before first merge to main.
- Playwright smoke covers increment 2 checkout happy path when UI exists.

## Notes

- Mechanism-specific test examples defer to `architecture-reference.md`.
