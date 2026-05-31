# Lo-fi — Shopping Cart

> **Companion to** `shopping-cart.drawio`.

## Metadata

| Field | Value |
| --- | --- |
| Scope | Shopping Cart — manage lines before guest checkout |
| Initial IA | `docs/end-to-end/discovery/ux/information-architecture.md` |
| AC source | `docs/increments/2-click-and-collect/exploration/stories/acceptance-criteria.md` |
| Domain terms | `docs/increments/2-click-and-collect/exploration/domain/ubiquitous-language.md` |
| State file | `shopping-cart-state.json` |
| Wireframe | `shopping-cart.drawio` |
| Last updated | 2026-05-31 |

## Description

*Customer* reviews *shopping cart* lines, adjusts *cart quantity*, *remove product from cart*, and proceeds to *guest checkout* when at least one line exists. Empty cart shows browse path without checkout.

---

## Design reference

| Design image | Panel/Region | UX element type | Key observations |
| --- | --- | --- | --- |
| IA spec | cart lines | list | Columns: product, cart quantity, line total |
| IA spec | cart lines actions | list actions | update quantity · remove · checkout |

---

## Screens

### Shopping Cart

**Layout:** stack  
**AC stories:** Add Product to Cart · Update Cart Quantity · Remove Product from Cart

| Region | Slot | Type | Controls | Interaction decisions |
| --- | --- | --- | --- | --- |
| site header · Find Store · catalog · Cart | header | chrome | Find Store · catalog · Cart | Customer navigation; Cart active |
| cart lines | body | list | product · cart quantity · line total | cart quantity editable inline per line; line total recalculates on update |
| cart lines actions | body | list actions | update quantity · remove · continue shopping · checkout | remove is distinct from zero quantity; checkout primary when lines exist |
| empty cart message | body | chrome | browse catalog prompt | Shown when no lines; checkout hidden |

**Conditional states:**
- Non-empty cart: checkout enabled; lines show product identity and cart quantity
- Empty cart: checkout disabled; continue shopping to catalog
- Zero-quantity attempt: validation message directs to remove instead of update

---

## Affordance trace

| Affordance | AC story | AC clause |
| --- | --- | --- |
| cart lines (new line) | Add Product to Cart | AC 1 — product placed into shopping cart with cart quantity |
| cart lines (merge) | Add Product to Cart | AC 2 — increases cart quantity; no duplicate line |
| cart lines (unavailable) | Add Product to Cart | AC 3 — prevents add or warns before unavailable product |
| cart lines (visible after add) | Add Product to Cart | AC 4 — open cart shows product identity and cart quantity |
| checkout (disabled empty) | Add Product to Cart | AC 5 — guest checkout not offered until at least one line |
| cart quantity (editable) | Update Cart Quantity | AC 1 — each line cart quantity editable |
| cart quantity (increase) | Update Cart Quantity | AC 2 — higher count saved; line total reflects quantity |
| cart quantity (decrease positive) | Update Cart Quantity | AC 3 — lower positive count saved; line remains |
| cart quantity (zero rejected) | Update Cart Quantity | AC 4 — rejects zero; directs to remove product from cart |
| cart lines (persist) | Update Cart Quantity | AC 5 — counts retained until checkout or remove |
| remove | Remove Product from Cart | AC 1 — distinct from setting cart quantity to zero |
| remove (confirm) | Remove Product from Cart | AC 2 — deletes product line from shopping cart |
| checkout (disabled last removed) | Remove Product from Cart | AC 3 — empty cart; guest checkout unavailable |
| cart lines (partial remove) | Remove Product from Cart | AC 4 — remaining lines unchanged |
| continue shopping | Remove Product from Cart | AC 5 — return to catalog; removed line not restored |

---

## CLI

```powershell
node "C:\dev\agilebydesign-skills\practices\user-experience-design\skills\abd-ux-mockup\scripts\drawio-mockup.mjs" `
  save `
  --state "docs/increments/2-click-and-collect/exploration/ux/shopping-cart-state.json" `
  --out   "docs/increments/2-click-and-collect/exploration/ux/shopping-cart.drawio"
```

---

## Change log

| Date | Direction | Summary |
| --- | --- | --- |
| 2026-05-31 | initial | First draft — shopping cart line management |
