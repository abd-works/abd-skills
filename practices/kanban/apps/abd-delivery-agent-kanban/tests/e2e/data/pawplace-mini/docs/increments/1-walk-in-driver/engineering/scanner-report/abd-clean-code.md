# Scanner report — abd-clean-code

**Ticket:** 1-walk-in-driver-sprint-2  
**Workspace:** packages/catalog/, packages/inventory/client/  
**Run:** 2026-05-31T20:15:00+00:00

## Verdict summary

| Rule area | Verdict | Evidence |
| --- | --- | --- |
| Domain language | PASS | Classes: WalkInCustomer, StoreEmployee, ProductStockLevels, RealTimeStock, CatalogStockAvailability |
| Single responsibility | PASS | Catalog orchestrates browse/detail; ProductStockLevels owns level persistence; CatalogApi handles HTTP only |
| Explicit dependencies | PASS | CatalogService receives CatalogRepository + StoreRepository via constructor |
| Guard clauses | PASS | Unset selected store, invalid quantities, missing staff token rejected early |
| Functions under 20 lines | PASS | Domain and service methods stay short |
| Encapsulation | PASS | ProductStockLevels uses private maps; ProductStoreKey centralizes composite key |
| Eliminate duplication | PASS | ProductStoreKey.toStorageKey(); RealTimeStock.reflectLatest delegates to showOnHandQuantityAtStore |
| No Manager/Handler naming | PASS | CatalogApi used for HTTP boundary only |

## Automated scanners

`run_scanners.py` — no embedded scanners in abd-clean-code rules for this fixture (INFO exit 0).

## Tests

| Suite | Status | Count |
| --- | --- | --- |
| stock-visibility_domain.test.ts | GREEN | 8/8 |
| stock-visibility_server.test.ts | GREEN | 15/15 |
| stock-visibility_client.test.tsx | GREEN | 15/15 |

## Remainder (ticket notes)

- No Playwright E2E for stock visibility in this sprint scope
- Full app-shell browser flows deferred to integration pass
