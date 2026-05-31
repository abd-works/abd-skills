# ADR-001: SPA plus REST API

> **Status:** Accepted  
> **Date:** 2026-05-31  
> **Deciders:** Engineer (shaping)  
> **Consulted:** Product, UX  
> **Informed:** Delivery team  

## Context

PawPlace mini delivers customer and store-employee flows in the browser across two increments (walk-in stock visibility and guest click-and-collect). The team needs a simple deployable shape for E2E kanban without server-rendered pages.

## Decision

We will ship a React SPA that talks to a Node/Express REST API. All business rules execute on the API; the SPA handles presentation and client-side navigation only.

## Consequences

**Positive:** Clear boundary for tests and module ownership.  
**Negative:** SEO and first paint are not goals for this slice.  
**Neutral:** API versioning starts at `/api/v1` for future clients.

## Compliance / verification

- New UI features must not embed business rules that skip the API.  
- API contract changes require an OpenAPI or shared-types check in CI (when introduced).
