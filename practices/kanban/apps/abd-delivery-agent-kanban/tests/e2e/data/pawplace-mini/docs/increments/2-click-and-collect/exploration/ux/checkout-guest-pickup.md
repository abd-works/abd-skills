# Lo-fi — Checkout — Guest & pickup

> **Companion to** `checkout-guest-pickup.drawio`.

## Metadata

| Field | Value |
| --- | --- |
| Scope | Checkout — Guest & pickup — store selection, billing, payment |
| Initial IA | `docs/end-to-end/discovery/ux/information-architecture.md` |
| AC source | `docs/increments/2-click-and-collect/exploration/stories/acceptance-criteria.md` |
| Domain terms | `docs/increments/2-click-and-collect/exploration/domain/ubiquitous-language.md` |
| State file | `checkout-guest-pickup-state.json` |
| Wireframe | `checkout-guest-pickup.drawio` |
| Last updated | 2026-05-31 |

## Description

*Customer* completes *guest checkout* from a non-empty *shopping cart*: selects *click-and-collect store*, enters contact and *billing address*, chooses card *payment method* via *StripeWave*, and submits *place order*. Store-first ordering; payment blocked until pickup store chosen.

---

## Design reference

| Design image | Panel/Region | UX element type | Key observations |
| --- | --- | --- | --- |
| IA spec | pickup store | listbox | Selectable click-and-collect store with address |
| IA spec | guest checkout | form | email · phone; guest-only label |
| IA spec | billing address | form | name · street · city · postal code · country |
| IA spec | payment method | form | card · StripeWave; place order primary |

---

## Screens

### Checkout — Guest & pickup

**Layout:** form  
**AC stories:** Select Click-and-Collect Store · Check Out as Guest · Enter Billing Address · Select Payment Method · Process Card Payment via StripeWave (system)

| Region | Slot | Type | Controls | Interaction decisions |
| --- | --- | --- | --- | --- |
| site header · Find Store · catalog · Cart | header | chrome | Find Store · catalog · Cart | Customer navigation |
| pickup store | body | listbox | click-and-collect store · store address | Single selection; shows identity and address for confirmation |
| pickup store actions | body | toolbar | change store | Updates checkout binding; only one store selected |
| guest checkout | body | form | email · phone | Guest-only; no login or registration |
| billing address | body | form | name · street · city · postal code · country | Field-level validation before payment step |
| payment method | body | form | payment method · StripeWave | Card only; place order invokes StripeWave |
| payment method actions | body | form buttons | back to cart · place order | place order primary; disabled until store and billing valid |
| validation error area | body | chrome | field-level messages | Shown on invalid billing or missing store |

**Conditional states:**
- No click-and-collect store: place order disabled; billing may be visible but payment blocked
- Invalid billing address: field errors; StripeWave not invoked
- Processing payment: place order disabled; processing indicator until StripeWave responds
- Payment failure: error message; cart recoverable via back to cart

---

## Affordance trace

| Affordance | AC story | AC clause |
| --- | --- | --- |
| pickup store (list) | Select Click-and-Collect Store | AC 1 — eligible stores selectable for pickup |
| pickup store (binding) | Select Click-and-Collect Store | AC 2 — binds store; shows identity and address |
| place order (blocked no store) | Select Click-and-Collect Store | AC 3 — blocks payment without click-and-collect store |
| change store | Select Click-and-Collect Store | AC 4 — updates binding; one store at a time |
| pickup store (attach on pay) | Select Click-and-Collect Store | AC 5 — chosen store attaches to placed order |
| guest checkout (no sign-in) | Check Out as Guest | AC 1 — guest checkout without account |
| guest checkout (email) | Check Out as Guest | AC 2 — contact for order confirmation; no registration |
| back to cart (empty blocked) | Check Out as Guest | AC 3 — blocks checkout from empty cart |
| checkout sections (order) | Check Out as Guest | AC 4 — store → billing → payment sequence |
| guest checkout (no account) | Check Out as Guest | AC 5 — click-and-collect order without customer account |
| billing address (fields) | Enter Billing Address | AC 1 — name, street, city, postal code, country |
| billing address (valid submit) | Enter Billing Address | AC 2 — saves on session; continue to payment |
| validation error area | Enter Billing Address | AC 3 — rejects incomplete; no StripeWave |
| billing address (revise) | Enter Billing Address | AC 4 — replaces prior values before payment |
| billing address (on success) | Enter Billing Address | AC 5 — attaches to placed order |
| payment method (card only) | Select Payment Method | AC 1 — card via StripeWave only option |
| place order | Select Payment Method | AC 2 — enables StripeWave; records payment method |
| place order (blocked no method) | Select Payment Method | AC 3 — blocks StripeWave without payment method |
| payment method (no alternatives) | Select Payment Method | AC 4 — only card via StripeWave supported |
| place order (invoke) | Select Payment Method | AC 5 — passes details to StripeWave |
| place order (process) | Process Card Payment via StripeWave | AC 1 — invokes StripeWave; waits for response |
| place order (success path) | Process Card Payment via StripeWave | AC 2 — creates paid order; clears cart |
| validation error area (failure) | Process Card Payment via StripeWave | AC 3 — failure message; no order or confirmation |
| place order (duplicate block) | Process Card Payment via StripeWave | AC 4 — prevents duplicate submit while processing |
| back to cart (retry) | Process Card Payment via StripeWave | AC 5 — cart recoverable on payment failure |

---

## CLI

```powershell
node "C:\dev\agilebydesign-skills\practices\user-experience-design\skills\abd-ux-mockup\scripts\drawio-mockup.mjs" `
  save `
  --state "docs/increments/2-click-and-collect/exploration/ux/checkout-guest-pickup-state.json" `
  --out   "docs/increments/2-click-and-collect/exploration/ux/checkout-guest-pickup.drawio"
```

---

## Change log

| Date | Direction | Summary |
| --- | --- | --- |
| 2026-05-31 | initial | First draft — guest checkout with pickup store selection |
