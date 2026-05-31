---
ticket: 1-walk-in-driver-sprint-1
skill: abd-architecture-reference
scope: Increment 1 Sprint 1 — Find a store
---

# Architecture Reference Assignment — Increment 1 Sprint 1 (Find a store)

**Ticket:** `1-walk-in-driver-sprint-1`  
**Mode:** Docs-only E2E fixture — assign-only; no `architecture-reference.md` or `src/` generation at specification.

## Mechanisms in scope

| Mechanism / component | In sprint scope |
| --- | --- |
| Store discovery (StoreService, StoreApi, StoreRepository) | Yes |
| App Shell (AppClientShell store map/list views) | Yes — presentation only |
| Security | Yes — guest transport and edge validation |
| Error Handling & Resilience | Yes |
| Validation | Yes |
| Persistence (`store_*`) | Yes |
| Communication (REST `/api/v1`) | Yes |
| Configuration | Yes |
| Logging & Observability | Yes |
| Catalog, Cart, Order, Payment | No — later sprints / increments |

## Assignment table

| Mechanism | Reference | Code | Paths |
| --- | --- | --- | --- |
| Store discovery | **assign** | **n/a** | [`docs/end-to-end/discovery/architecture/architecture-blueprint.md`](../../../end-to-end/discovery/architecture/architecture-blueprint.md) § 2.2 Store components |
| Security | **assign** | **n/a** | Blueprint § 3.1 Security |
| Error Handling & Resilience | **assign** | **n/a** | Blueprint § 3.2 |
| Validation | **assign** | **n/a** | Blueprint § 3.4 |
| Persistence | **assign** | **n/a** | Blueprint § 3.6; data ownership § 4.2 (`Store`) |
| Communication | **assign** | **n/a** | Blueprint § 3.7 |
| Configuration | **assign** | **n/a** | Blueprint § 3.5 |
| Logging & Observability | **assign** | **n/a** | Blueprint § 3.3 |

### Exploration & specification context (assign)

- CRC: [`crc.md`](./crc.md)
- Spec by example: [`specification-by-example.md`](./specification-by-example.md)
- Interface design: [`interface-design.md`](./interface-design.md)
- Ubiquitous language: [`../exploration/domain/ubiquitous-language.md`](../exploration/domain/ubiquitous-language.md)
- Acceptance criteria: [`../exploration/stories/acceptance-criteria.md`](../exploration/stories/acceptance-criteria.md)
- UX mockups: [`../exploration/ux/mockups.md`](../exploration/ux/mockups.md)

**Deferred to engineering:** Runnable reference sections (`architecture-reference.md`), File Structure, and production code under `src/` — created by `abd-object-model`, `abd-acceptance-test-driven-development`, and `abd-clean-code` on the engineering ticket.

---

---
ticket: 1-walk-in-driver-sprint-2
skill: abd-architecture-reference
scope: Increment 1 Sprint 2 — Stock visibility
---

# Architecture Reference Assignment — Increment 1 Sprint 2 (Stock visibility)

**Ticket:** `1-walk-in-driver-sprint-2`  
**Mode:** Docs-only E2E fixture — assign-only; no `architecture-reference.md` or `src/` generation at specification.

## Mechanisms in scope

| Mechanism / component | In sprint scope |
| --- | --- |
| Catalog (CatalogService, CatalogApi, CatalogRepository) | Yes |
| Selected store context (read from Store module) | Yes — scope gate only |
| App Shell (AppClientShell catalog + stock views) | Yes — presentation only |
| Security | Yes — guest browse + staff token on stock-update routes |
| Error Handling & Resilience | Yes |
| Validation | Yes |
| Persistence (`catalog_*`) | Yes |
| Communication (REST `/api/v1`) | Yes |
| Configuration | Yes |
| Logging & Observability | Yes |
| Cart, Order, Payment | No — Increment 2 / later sprints |

## Assignment table

| Mechanism | Reference | Code | Paths |
| --- | --- | --- | --- |
| Catalog browse, detail, stock read/update | **assign** | **n/a** | [`docs/end-to-end/discovery/architecture/architecture-blueprint.md`](../../../end-to-end/discovery/architecture/architecture-blueprint.md) § 2.3 Catalog components |
| Store context (selected store) | **assign** | **n/a** | Blueprint § 2.2 Store components (read path for catalog scope) |
| Security | **assign** | **n/a** | Blueprint § 3.1 Security (guest + staff stock routes) |
| Error Handling & Resilience | **assign** | **n/a** | Blueprint § 3.2 |
| Validation | **assign** | **n/a** | Blueprint § 3.4 |
| Persistence | **assign** | **n/a** | Blueprint § 3.6; data ownership § 4.2 (`Product`, stock by store) |
| Communication | **assign** | **n/a** | Blueprint § 3.7 |
| Configuration | **assign** | **n/a** | Blueprint § 3.5 |
| Logging & Observability | **assign** | **n/a** | Blueprint § 3.3 |

### Exploration & specification context (assign)

- CRC (Sprint 2): [`crc.md`](./crc.md) — Increment 1 — Sprint 2: Stock visibility
- Spec by example (Sprint 2): [`specification-by-example.md`](./specification-by-example.md)
- Interface design (Sprint 2): [`interface-design.md`](./interface-design.md) — Browse Catalog, Product Details, Update Stock
- Ubiquitous language: [`../exploration/domain/ubiquitous-language.md`](../exploration/domain/ubiquitous-language.md)
- Acceptance criteria: [`../exploration/stories/acceptance-criteria.md`](../exploration/stories/acceptance-criteria.md)
- UX mockups: [`../exploration/ux/product-details.md`](../exploration/ux/product-details.md), [`../exploration/ux/update-stock.md`](../exploration/ux/update-stock.md)

**Deferred to engineering:** Runnable reference sections (`architecture-reference.md`), File Structure, and production code under `packages/` — created by `abd-object-model`, `abd-acceptance-test-driven-development`, and `abd-clean-code` on the engineering ticket.
