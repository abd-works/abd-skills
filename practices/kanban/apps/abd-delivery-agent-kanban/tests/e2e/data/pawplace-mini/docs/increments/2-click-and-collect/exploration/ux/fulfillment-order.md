# Lo-fi — Fulfillment — Order

> **Companion to** `fulfillment-order.drawio`.

## Metadata

| Field | Value |
| --- | --- |
| Scope | Fulfillment — Order — pickup handoff detail |
| Initial IA | `docs/end-to-end/discovery/ux/information-architecture.md` |
| AC source | `docs/increments/2-click-and-collect/exploration/stories/acceptance-criteria.md` |
| Domain terms | `docs/increments/2-click-and-collect/exploration/domain/ubiquitous-language.md` |
| State file | `fulfillment-order-state.json` |
| Wireframe | `fulfillment-order.drawio` |
| Last updated | 2026-05-31 |

## Description

*Store employee* opens a prepared *click-and-collect order*, reviews lines and *click-and-collect store*, and confirms *fulfill click-and-collect order* to complete *order fulfillment* at pickup.

---

## Design reference

| Design image | Panel/Region | UX element type | Key observations |
| --- | --- | --- | --- |
| IA spec | order detail | form | order id · product lines · click-and-collect store · order fulfillment status |
| IA spec | order detail actions | form buttons | back to queue · fulfill click-and-collect order |

---

## Screens

### Fulfillment — Order

**Layout:** stack  
**AC stories:** Fulfill Click-and-Collect Order

| Region | Slot | Type | Controls | Interaction decisions |
| --- | --- | --- | --- | --- |
| employee header · store · Fulfillment · Sign out | header | chrome | store · Fulfillment · Sign out | Employee-only navigation |
| order detail | body | form | order id · product · click-and-collect store · order fulfillment | Shows lines and fulfillment status |
| order detail actions | body | form buttons | back to queue · fulfill click-and-collect order | fulfill primary when preparation complete; blocked if not prepared |

**Conditional states:**
- Prepared order: fulfill click-and-collect order enabled
- Not prepared: handoff blocked or warning shown
- After fulfill: order marked collected; removed from active queue

---

## Affordance trace

| Affordance | AC story | AC clause |
| --- | --- | --- |
| order detail | Fulfill Click-and-Collect Order | AC 1 — shows lines, click-and-collect store, status; offers fulfill when ready |
| fulfill click-and-collect order | Fulfill Click-and-Collect Order | AC 2 — marks order fulfillment complete; removes from queue |
| order detail (handoff) | Fulfill Click-and-Collect Order | AC 3 — employee matches order; customer receives products |
| fulfill click-and-collect order (not prepared) | Fulfill Click-and-Collect Order | AC 4 — blocks or warns if preparation incomplete |
| fulfill click-and-collect order (complete) | Fulfill Click-and-Collect Order | AC 5 — order collected or closed |
| back to queue | Fulfill Click-and-Collect Order | AC 1 — return to order queue without handoff |

---

## CLI

```powershell
node "C:\dev\agilebydesign-skills\practices\user-experience-design\skills\abd-ux-mockup\scripts\drawio-mockup.mjs" `
  save `
  --state "docs/increments/2-click-and-collect/exploration/ux/fulfillment-order-state.json" `
  --out   "docs/increments/2-click-and-collect/exploration/ux/fulfillment-order.drawio"
```

---

## Change log

| Date | Direction | Summary |
| --- | --- | --- |
| 2026-05-31 | initial | First draft — pickup handoff detail |
