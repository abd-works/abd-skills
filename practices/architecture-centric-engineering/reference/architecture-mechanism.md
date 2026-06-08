# Architecture Mechanism — Shared Concept

This is the family-level definition of an **architecture mechanism**. The
architecture skills (`abd-architecture-outline`, `abd-architecture-blueprint`,
`abd-architecture-specification`, `abd-architecture-specification`) all refer to it; each
skill adds its own *level of fidelity* on top of this single definition rather
than re-defining the term.

## What an architecture mechanism is

An **architecture mechanism** is the architecture's fixed answer to a
**cross-cutting concern** — a concern that shows up in many components rather
than belonging to one feature. It is the *verbed* concern: not "errors" but
*how the architecture handles errors*; not "data" but *how it persists*; not
"identity" but *how it authorizes*. A mechanism is a standardized, recurring
technical solution applied consistently across the system so that complexity
stays down, behaviour stays uniform, and proven solutions get reused instead of
reinvented.

The term comes from the Rational Unified Process, where mechanisms evolve
through three stages — analysis (the concern is named), design
(a technology-agnostic approach is chosen), implementation (a concrete
technology realizes it). Modern practice often calls the same idea an
architectural pattern, tactic, or architecturally significant requirement; in
this family we keep the single word **mechanism**. Background notes:
[`data.md`](data.md).

## Canonical mechanism categories

Adapt these to the project; they are the common starting set:

- **Security** — authentication, authorization, secret handling, identity propagation.
- **Error Handling & Resilience** — exception/Result conventions, retry, circuit breaker, fallback, error reporting.
- **Logging & Observability** — logging library, log shape, trace propagation, metric emission.
- **Validation** — input validation, business-rule validation, error reporting back to the caller.
- **Configuration** — config source, environment separation, secret management, feature flags.
- **Caching** — where caches sit, invalidation strategy, consistency model.
- **Communication** — sync vs async patterns, message bus, API versioning, service discovery.
- **Persistence** — repository pattern, transaction boundaries, migration strategy.

Less common but recurring: idempotency, transactions, rate limiting, messaging.

## How each skill uses this concept

- **`abd-architecture-outline`** — *names* the mechanisms in scope and explicitly defers their detail downward.
- **`abd-architecture-blueprint`** — describes each mechanism in 1–2 paragraphs: the concern it addresses, which components depend on it, how they interact with it.
- **`abd-architecture-specification`** — takes one mechanism at a time and goes deep using the five-part shape (principles & patterns, file structure, participants, flow, walkthrough).
- **`abd-architecture-specification`** — emits runnable code that implements one mechanism end-to-end.
