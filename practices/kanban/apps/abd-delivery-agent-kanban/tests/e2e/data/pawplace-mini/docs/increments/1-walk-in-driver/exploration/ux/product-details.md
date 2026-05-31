# Lo-fi — Product Details

> **Companion to** `product-details.drawio`.

## Metadata

| Field | Value |
| --- | --- |
| Scope | Product Details — stock visibility at selected store |
| Initial IA | `docs/end-to-end/discovery/ux/information-architecture.md` |
| AC source | `docs/increments/1-walk-in-driver/exploration/stories/acceptance-criteria.md` |
| Domain terms | `docs/increments/1-walk-in-driver/exploration/domain/ubiquitous-language.md` |
| State file | `product-details-state.json` |
| Wireframe | `product-details.drawio` |
| Last updated | 2026-05-30 |

## Description

Customer with a *selected store* views *product* detail including *real-time stock* and *stock availability* to decide on a walk-in purchase. No cart, checkout, or payment actions (Increment 1).

---

## Design reference

| Design image | Panel/Region | UX element type | Key observations |
| --- | --- | --- | --- |
| IA spec | product summary | form | Read-only fields for product identity and stock |
| IA spec | selected store | chrome | Shows active store context on detail view |

---

## Screens

### Product Details

**Layout:** stack  
**AC stories:** View Product Details · Display Real-Time Stock Availability (system)

| Region | Slot | Type | Controls | Interaction decisions |
| --- | --- | --- | --- | --- |
| site header · Find Store · catalog | header | chrome | Find Store · catalog | Customer navigation |
| selected store | body | chrome | selected store name and address | Scopes detail to one store; no aggregate stock |
| product summary | body | form | product · price · description · real-time stock · stock availability | Read-only display; stock availability derived from real-time stock |
| product summary actions | body | form button | back to catalog | Returns to catalog without losing selected store |

**Conditional states:**
- stock availability available: positive real-time stock at selected store
- stock availability unavailable: zero real-time stock; no cart/backorder actions

---

## Affordance trace

| Affordance | AC story | AC clause |
| --- | --- | --- |
| product summary | View Product Details | AC 2 — product detail before visiting in person |
| selected store | View Product Details | AC 3 — scoped to selected store; no cart/checkout |
| real-time stock | Display Real-Time Stock Availability | AC 1 — displays real-time stock at selected store |
| stock availability | Display Real-Time Stock Availability | AC 2 — available now when sellable quantity |
| stock availability (zero) | Display Real-Time Stock Availability | AC 3 — unavailable; no online purchase actions |
| real-time stock (store scoped) | Display Real-Time Stock Availability | AC 5 — counts only for selected store |
| back to catalog | View Product Details | AC 5 — return to catalog without losing selected store |

---

## CLI

```powershell
node "C:\dev\agilebydesign-skills\practices\user-experience-design\skills\abd-ux-mockup\scripts\drawio-mockup.mjs" `
  save `
  --state "docs/increments/1-walk-in-driver/exploration/ux/product-details-state.json" `
  --out   "docs/increments/1-walk-in-driver/exploration/ux/product-details.drawio"
```

---

## Change log

| Date | Direction | Summary |
| --- | --- | --- |
| 2026-05-30 | initial | First draft — product detail with stock visibility |
