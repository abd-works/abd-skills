# Lo-fi — Order Confirmation

> **Companion to** `order-confirmation.drawio`.

## Metadata

| Field | Value |
| --- | --- |
| Scope | Order Confirmation — post-payment summary and pickup location |
| Initial IA | `docs/end-to-end/discovery/ux/information-architecture.md` |
| AC source | `docs/increments/2-click-and-collect/exploration/stories/acceptance-criteria.md` |
| Domain terms | `docs/increments/2-click-and-collect/exploration/domain/ubiquitous-language.md` |
| State file | `order-confirmation-state.json` |
| Wireframe | `order-confirmation.drawio` |
| Last updated | 2026-05-31 |

## Description

After *StripeWave* payment success, *customer* sees placed *click-and-collect order* summary with pickup *click-and-collect store*, total, and *order confirmation* email notice. System stories handle payment and email; screen shows outcome only.

---

## Design reference

| Design image | Panel/Region | UX element type | Key observations |
| --- | --- | --- | --- |
| IA spec | order summary | form | order id · click-and-collect store · total · confirmation email |

---

## Screens

### Order Confirmation

**Layout:** stack  
**AC stories:** Confirm Order and Send Confirmation Email (system) · Process Card Payment via StripeWave (system)

| Region | Slot | Type | Controls | Interaction decisions |
| --- | --- | --- | --- | --- |
| site header · Find Store · catalog · Cart | header | chrome | Find Store · catalog · Cart | Customer navigation |
| order summary | body | form | order id · click-and-collect store · total · order confirmation | Read-only summary after payment success |
| order summary actions | body | form button | continue shopping | Returns to catalog; placed order not editable via cart |

**Conditional states:**
- Payment success: full summary visible; confirmation sent indicator
- No payment success: customer not routed here (checkout or error surfaces)

---

## Affordance trace

| Affordance | AC story | AC clause |
| --- | --- | --- |
| order confirmation (email) | Confirm Order and Send Confirmation Email | AC 1 — email sent with order and click-and-collect store |
| order summary | Confirm Order and Send Confirmation Email | AC 2 — order id, click-and-collect store, total on screen |
| order summary (no premature) | Confirm Order and Send Confirmation Email | AC 3 — not shown until payment succeeds |
| order summary (queue visibility) | Confirm Order and Send Confirmation Email | AC 4 — order visible to store employees in fulfillment queue |
| continue shopping | Confirm Order and Send Confirmation Email | AC 5 — return to catalog; order committed |
| order summary (entry) | Process Card Payment via StripeWave | AC 2 — reached only after StripeWave success |

---

## CLI

```powershell
node "C:\dev\agilebydesign-skills\practices\user-experience-design\skills\abd-ux-mockup\scripts\drawio-mockup.mjs" `
  save `
  --state "docs/increments/2-click-and-collect/exploration/ux/order-confirmation-state.json" `
  --out   "docs/increments/2-click-and-collect/exploration/ux/order-confirmation.drawio"
```

---

## Change log

| Date | Direction | Summary |
| --- | --- | --- |
| 2026-05-31 | initial | First draft — post-checkout pickup confirmation |
