# Scanner report — abd-acceptance-test-driven-development

**Ticket:** `2-click-and-collect-sprint-2`  
**Workspace:** `C:/dev/agilebydesign-skills/practices/kanban/apps/abd-delivery-agent-kanban/tests/e2e/data/pawplace-mini`  
**Scope:** Sprint 2 Checkout & pay — RED server/domain/e2e; client GREEN from prior interface-design

## Automated scanners

No rule scanners bundled with ATDD skill (`run_scanners.py` — no scanners found).

## Manual review (executor pass)

| Rule | Verdict | Evidence |
| --- | --- | --- |
| Class-based test organization | PASS | 6 story `describe` blocks in server; domain grouped by concept |
| Match specification scenarios | PASS | 30 server + 8 client scenarios map to spec-by-example Sprint 2 |
| Given/When/Then helpers | PASS | `Checkout{Server,Client,E2E}Helper` with `given_*`, `when_*`, `then_*` |
| Domain language | PASS | Guest Checkout, Click-and-collect Store, StripeWave, Order Confirmation |
| MERN test layout | PASS | `tests/shop-and-pay-online/checkout-and-pay/*_{server,client,e2e}.*` + domain under `packages/checkout/shared/tests/` |
| RED before GREEN | PASS | Server/domain/e2e `when_*` throws RED; client 8/8 GREEN (interface-design prior) |

## Test status

| Tier | File | Status |
| --- | --- | --- |
| Client | `checkout-and-pay_client.test.tsx` | **8/8 GREEN** |
| Server | `checkout-and-pay_server.test.ts` | **30/30 RED** |
| Domain | `checkout-and-pay_domain.test.ts` | **22/22 RED** |
| E2E | `checkout-and-pay_e2e.spec.ts` | **5 RED** (Playwright; excluded from vitest) |

## Artifacts

- `tests/shop-and-pay-online/checkout-and-pay/checkout-and-pay_client.test.tsx`
- `tests/shop-and-pay-online/checkout-and-pay/checkout-and-pay_server.test.ts`
- `tests/shop-and-pay-online/checkout-and-pay/checkout-and-pay_e2e.spec.ts`
- `tests/shop-and-pay-online/checkout-and-pay/helpers/checkout.{base,client,server,e2e}.ts`
- `packages/checkout/shared/tests/checkout-and-pay_domain.test.ts`
