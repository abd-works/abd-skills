# ADR-004: Zod validation at the API boundary

> **Status:** Accepted
> **Date:** 2026-05-31
> **Deciders:** Engineer (discovery)

## Context

PawPlace mini exposes REST endpoints across four modules. Invalid payloads must fail before application services run so domain code receives typed DTOs only. The team needs a shared validation approach that works on the server and can align with client forms.

## Decision

We will validate every API request and response at the HTTP adapter edge using **Zod schemas** colocated in each module's shared package. Application services accept parsed DTOs; they do not parse raw JSON.

## Options considered

| Option | Pros | Cons | Why rejected (or chosen) |
|---|---|---|---|
| **Zod at API edge (chosen)** | Runtime + TypeScript inference; shareable with client | Schema drift if not co-located | **Chosen** — matches MERN conventions and blueprint mechanism catalogue |
| Manual validation in controllers | No extra dependency | Duplicated checks; easy to skip | Rejected — inconsistent across modules |
| OpenAPI-only validation | Good for external consumers | Does not give TS types in-process without codegen step | Rejected — overhead for mini fixture |

## Consequences

**Positive:**
- Invalid cart and checkout payloads return 400 before touching MongoDB or StripeWave.
- Client packages can import the same schemas for form validation.

**Negative / trade-offs:**
- Each new endpoint requires schema maintenance alongside route handlers.

**Neutral:**
- OpenAPI generation can be added later from Zod if external clients appear.

## Compliance / verification

- Code review rejects handlers that pass `req.body` directly into services without schema parse.
- Integration tests include at least one malformed-payload case per public write endpoint.

## Notes

- Outline ADR-001 establishes SPA + REST; this ADR covers request shape enforcement.
