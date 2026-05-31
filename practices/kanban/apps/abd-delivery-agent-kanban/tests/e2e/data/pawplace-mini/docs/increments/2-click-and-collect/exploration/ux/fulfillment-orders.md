# Lo-fi — Fulfillment — Orders

> **Companion to** `fulfillment-orders.drawio`.

## Metadata

| Field | Value |
| --- | --- |
| Scope | Fulfillment — Orders — store employee preparation queue |
| Initial IA | `docs/end-to-end/discovery/ux/information-architecture.md` |
| AC source | `docs/increments/2-click-and-collect/exploration/stories/acceptance-criteria.md` |
| Domain terms | `docs/increments/2-click-and-collect/exploration/domain/ubiquitous-language.md` |
| State file | `fulfillment-orders-state.json` |
| Wireframe | `fulfillment-orders.drawio` |
| Last updated | 2026-05-31 |

## Description

*Store employee* opens the fulfillment queue for a *click-and-collect store*, views paid *click-and-collect orders* awaiting *prepare click-and-collect orders for pickup*, and marks orders preparing or opens order detail.

---

## Design reference

| Design image | Panel/Region | UX element type | Key observations |
| --- | --- | --- | --- |
| IA spec | order queue | list | order id · customer · status · pickup time |
| IA spec | employee header | chrome | store · Fulfillment · Sign out |

---

## Screens

### Fulfillment — Orders

**Layout:** stack  
**AC stories:** Prepare Click-and-Collect Orders for Pickup

| Region | Slot | Type | Controls | Interaction decisions |
| --- | --- | --- | --- | --- |
| employee header · store · Fulfillment · Sign out | header | chrome | store · Fulfillment · Sign out | Employee-only navigation |
| order queue | body | list | order id · customer · status · pickup time | Scoped to employee click-and-collect store only |
| order queue actions | body | list actions | open order · mark preparing | mark preparing primary; stages order for collection |

**Conditional states:**
- Paid confirmed orders only: unpaid sessions excluded from queue
- Store scoped: orders for other stores not shown
- Customer role: fulfillment queue unavailable

---

## Affordance trace

| Affordance | AC story | AC clause |
| --- | --- | --- |
| order queue | Prepare Click-and-Collect Orders for Pickup | AC 1 — lists paid click-and-collect orders awaiting preparation |
| mark preparing | Prepare Click-and-Collect Orders for Pickup | AC 2 — updates status to ready for collection |
| order queue (paid only) | Prepare Click-and-Collect Orders for Pickup | AC 3 — excludes unpaid or failed checkout |
| order queue (store scoped) | Prepare Click-and-Collect Orders for Pickup | AC 4 — only orders for employee click-and-collect store |
| employee header (access) | Prepare Click-and-Collect Orders for Pickup | AC 5 — unavailable to customer |
| open order | Prepare Click-and-Collect Orders for Pickup | AC 1 — navigate to order detail for handoff prep |

---

## CLI

```powershell
node "C:\dev\agilebydesign-skills\practices\user-experience-design\skills\abd-ux-mockup\scripts\drawio-mockup.mjs" `
  save `
  --state "docs/increments/2-click-and-collect/exploration/ux/fulfillment-orders-state.json" `
  --out   "docs/increments/2-click-and-collect/exploration/ux/fulfillment-orders.drawio"
```

---

## Change log

| Date | Direction | Summary |
| --- | --- | --- |
| 2026-05-31 | initial | First draft — fulfillment order queue |
