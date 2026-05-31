# Lo-fi — Find Store — List

> **Companion to** `find-store-list.drawio`.

## Metadata

| Field | Value |
| --- | --- |
| Scope | Find Store — List — store discovery via list |
| Initial IA | `docs/end-to-end/discovery/ux/information-architecture.md` |
| AC source | `docs/increments/1-walk-in-driver/exploration/stories/acceptance-criteria.md` |
| Domain terms | `docs/increments/1-walk-in-driver/exploration/domain/ubiquitous-language.md` |
| State file | `find-store-list-state.json` |
| Wireframe | `find-store-list.drawio` |
| Last updated | 2026-05-30 |

## Description

Customer opens *store list* as an alternative to *store map*, compares *stores* in a readable list layout, optionally ranks by *distance to store*, and selects a *store* to set *selected store*.

---

## Design reference

| Design image | Panel/Region | UX element type | Key observations |
| --- | --- | --- | --- |
| IA spec | store list | list | Columns: store, address, distance to store |
| IA spec | Find Store tab bar | nav-tabs | List active; Map inactive |

---

## Screens

### Find Store — List

**Layout:** stack  
**AC stories:** View Store List · Calculate Distance to Store

| Region | Slot | Type | Controls | Interaction decisions |
| --- | --- | --- | --- | --- |
| site header · Find Store · catalog | header | chrome | Find Store · catalog | Same customer chrome as map screen |
| Find Store tab bar | body | nav-tabs | Map · List (active) | Map tab returns to store map without losing context |
| store list | body | list | store · address · distance to store columns; use my location · select store | Nearest-first sort when distance calculated; select store is primary action |

**Conditional states:**
- No location: distance to store column empty
- With location: rows sorted nearest first

---

## Affordance trace

| Affordance | AC story | AC clause |
| --- | --- | --- |
| store list | View Store List | AC 1 — store list alternative with store name and details |
| select store | View Store List | AC 2 — sets selected store; proceed to catalog |
| store list (readable rows) | View Store List | AC 3 — compare stores without map layout; tab switch preserves context |
| store list (no stock) | View Store List | AC 4 — lists every store; stock availability hidden until selected store |
| use my location | Calculate Distance to Store | AC 1 — distance to store calculated; nearest first |
| store list (no distance) | Calculate Distance to Store | AC 2 — stores shown without distance until location shared |
| distance to store column | Calculate Distance to Store | AC 3 — proximity in list presentation |
| use my location (recalc) | Calculate Distance to Store | AC 4 — recalculates sort on location change |

---

## CLI

```powershell
node "C:\dev\agilebydesign-skills\practices\user-experience-design\skills\abd-ux-mockup\scripts\drawio-mockup.mjs" `
  save `
  --state "docs/increments/1-walk-in-driver/exploration/ux/find-store-list-state.json" `
  --out   "docs/increments/1-walk-in-driver/exploration/ux/find-store-list.drawio"
```

---

## Change log

| Date | Direction | Summary |
| --- | --- | --- |
| 2026-05-30 | initial | First draft — store list discovery screen |
