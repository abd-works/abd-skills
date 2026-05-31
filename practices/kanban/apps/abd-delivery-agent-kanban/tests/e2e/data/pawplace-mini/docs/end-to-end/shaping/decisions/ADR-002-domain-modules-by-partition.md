# ADR-002: Domain modules by partition

> **Status:** Accepted  
> **Date:** 2026-05-31  
> **Deciders:** Engineer (shaping)  
> **Consulted:** Business expert  
> **Informed:** Product owner  

## Context

Shaping partitioned PawPlace mini into Store, Catalog, Cart, and Order modules. Implementation must not collapse those boundaries before discovery CRC work.

## Decision

We will map each partition to a domain package (and matching application/infrastructure adapters). Cross-partition orchestration uses explicit application services, not shared “god” repositories.

## Consequences

**Positive:** Stories and tests align to module folders.  
**Negative:** Some flows (checkout) touch multiple packages.  
**Neutral:** Shared kernel types (money, address) live in a small `shared` package if needed.

## Compliance / verification

- Import-linter or manual review blocks `catalog` → `order` domain imports except via published application APIs.
