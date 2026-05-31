# ADR-006: StripeWave behind payment port

> **Status:** Accepted
> **Date:** 2026-05-31
> **Deciders:** Engineer (discovery)

## Context

Guest checkout processes card payment via StripeWave (fixture vendor name). Outline principle: payments cross one seam; domain must not import Stripe SDK types. OrderService needs a stable interface for authorization and capture results.

## Decision

We will wrap StripeWave behind **`IPaymentProvider`** implemented by `PaymentGatewayAdapter`. OrderService depends on the interface only; vendor SDK types stay in the adapter package.

## Options considered

| Option | Pros | Cons | Why rejected (or chosen) |
|---|---|---|---|
| **Payment port + StripeWave adapter (chosen)** | Testable with fakes; swappable provider | Extra interface layer | **Chosen** — matches blueprint extension seam |
| Stripe SDK in OrderService | Fewer files | Domain coupled to vendor; hard to test | Rejected — violates outline payment principle |
| Mock payment only (no real adapter) | Simplest fixture | No integration path to real sandbox | Rejected — increment 2 needs sandbox verification |

## Consequences

**Positive:**
- Order domain tests use `FakePaymentProvider` without network I/O.
- New processors register at composition root without changing OrderService.

**Negative / trade-offs:**
- Adapter must map vendor errors to domain payment failures explicitly.

**Neutral:**
- Refund flows deferred until post-mini scope.

## Compliance / verification

- Static review or import-linter blocks StripeWave imports outside `PaymentGatewayAdapter`.
- Integration tests use StripeWave sandbox or recorded fixtures.

## Notes

- Extension & Evolution section in blueprint documents this as the sole plug-in seam for mini scope.
