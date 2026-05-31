# ADR-007: Idempotent order placement

> **Status:** Accepted
> **Date:** 2026-05-31
> **Deciders:** Engineer (discovery)

## Context

Guest checkout submit-payment may be retried on flaky networks or double-clicks. Without idempotency, retries could create duplicate charges or orders. Outline guiding principle commits to idempotent order placement at the HTTP boundary.

## Decision

We will require a **client idempotency key** on submit-payment requests. OrderService stores the key with the order aggregate; duplicate keys return the original outcome without re-invoking StripeWave.

## Options considered

| Option | Pros | Cons | Why rejected (or chosen) |
|---|---|---|---|
| **Client idempotency key (chosen)** | Standard HTTP pattern; safe retries | Clients must generate and persist key | **Chosen** — matches outline principle |
| Server-only dedupe by cart id | No client change | Race on concurrent submits from same cart | Rejected — weaker under parallel tabs |
| No idempotency (mini only) | Simplest code | Duplicate orders in E2E and production | Rejected — checkout is critical path |

## Consequences

**Positive:**
- Safe retries after 502/timeout without duplicate payment.
- E2E tests can assert replay behaviour.

**Negative / trade-offs:**
- Idempotency records need TTL or archival policy to avoid unbounded growth.

**Neutral:**
- Key scope is per guest session + checkout attempt; not global across customers.

## Compliance / verification

- OrderApi rejects or ignores duplicate processing when the same key returns a completed order.
- Integration test replays submit-payment with identical key and asserts single charge.

## Notes

- Persistence details for idempotency storage live with OrderRepository in architecture reference.
