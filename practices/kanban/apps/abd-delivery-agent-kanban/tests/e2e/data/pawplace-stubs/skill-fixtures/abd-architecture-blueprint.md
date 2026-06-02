# PawPlace — Architecture Blueprint (stub)

## Scope

Increment 1 — catalog browse, search, per-store stock. MERN spike.

## Components

### AppServerHost

Express app mounting catalog and store API routes.

### AppClientShell

React shell with header search and route table.

### ProductCatalogService

Browse, search, stock read/update for staff.

## Mechanisms (catalogue)

| Mechanism | Intent |
| --- | --- |
| Persistence | MongoDB for products and stock |
| Validation | Guard stock quantity ≥ 0 |
| Error handling | API errors → user-visible messages |

Deep walkthroughs: `architecture-reference.md` (specification stage).
