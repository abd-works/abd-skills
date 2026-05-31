# Scanner report — abd-clean-code

**Ticket:** 2-click-and-collect-sprint-1  
**Workspace:** packages/cart/  
**Run:** 2026-05-31T03:00:00+00:00

## Verdict summary

| Rule area | Verdict | Evidence |
| --- | --- | --- |
| Domain language | PASS | Classes: ShoppingCart, CartLines, AddProductToCart, CartQuantity |
| Single responsibility | PASS | Services delegate to CartLines collection; HTTP in CartApi only |
| Explicit dependencies | PASS | CartService receives CartRepository via constructor |
| Guard clauses | PASS | Zero/unavailable paths throw domain exceptions early |
| Functions under 20 lines | PASS | Mapper and repository methods stay short |
| Domain exceptions | PASS | UnavailableProductException, ZeroQuantityRejectedException |
| No Manager/Handler naming | PASS | CartApi used for HTTP boundary only |

## Automated scanners

`run_scanners.py` — no embedded scanners in abd-clean-code rules for this fixture (INFO exit 0).

## Tests

| Suite | Status | Count |
| --- | --- | --- |
| manage-cart_domain.test.ts | GREEN | 4/4 |
| manage-cart_server.test.ts | GREEN | 15/15 |
| manage-cart_client.test.tsx | GREEN | 6/6 |

## Remainder (ticket notes)

- `manage-cart_e2e.spec.ts` — Playwright E2E still RED (needs full app shell)
- `packages/cart/client` HTTP client wiring to live server — deferred; InMemoryCartApi used for ATDD
- Checkout / order modules — Sprint 2+
