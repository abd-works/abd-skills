# PawPlace — Architecture Outline (stub)

## Platform

MERN — MongoDB, Express, React, Node.js. Single deployable web app.

## Layering

| Layer | Responsibility |
| --- | --- |
| Presentation | React views — store locator, catalog, product detail |
| Domain | Product catalog, stock availability, store |
| Integration | MongoDB persistence, REST API |

## Major systems

- **App Shell** — routing, layout, API host
- **Product Catalog** — browse, search, stock read/write
- **Store Locator** — map and list of stores

## Guiding principles

Domain-first modules; real-time stock; no checkout in Increment 1.
