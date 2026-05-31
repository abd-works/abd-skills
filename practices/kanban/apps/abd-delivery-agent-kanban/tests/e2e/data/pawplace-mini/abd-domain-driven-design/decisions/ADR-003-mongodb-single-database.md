# ADR-003: MongoDB single database

> **Status:** Accepted  
> **Date:** 2026-05-31  
> **Deciders:** Engineer (shaping)  
> **Consulted:** Engineer  
> **Informed:** Kanban lead  

## Context

Mini scope needs one persistence tier for catalog, per-store stock, carts, and orders without operating multiple data stores in the fixture.

## Decision

We will use one MongoDB database with collections owned by each module team (naming convention: `store_*`, `catalog_*`, `cart_*`, `order_*`).

## Consequences

**Positive:** Fast local and CI setup for E2E.  
**Negative:** Blast radius if credentials leak — mitigated by least-privilege app user per environment.  
**Neutral:** Split databases deferred until scale or compliance requires it.

## Compliance / verification

- Migrations/scripts document collection ownership in module README or blueprint.
