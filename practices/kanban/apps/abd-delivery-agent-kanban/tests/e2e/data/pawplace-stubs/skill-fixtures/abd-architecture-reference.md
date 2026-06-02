# Architecture Reference — Increment 1 (stub)

> Trimmed from abd-pet-store-demo Increment 1 mechanisms.

## Overview

MERN domain-first modules: `@pawplace/product-catalog-shared`, server, client.

## Mechanism: Persistence

MongoDB — `products`, `stock_availability`, `stores` collections.

## Mechanism: Validation

Express middleware validates request bodies; domain guards stock ≥ 0.

## Mechanism: Error handling

`DomainError` → 400; unexpected → 500 with logged correlation id.

Implementation paths: `packages/product-catalog-server`, `packages/app-client`.
