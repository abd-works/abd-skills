# Lo-fi — Find Store — Map

> **Companion to** `find-store-map.drawio`. Author or update **this file first**, then regenerate the wireframe from the state file.

## Metadata

| Field | Value |
| --- | --- |
| Scope | Find Store — Map — store discovery via map |
| Initial IA | `docs/end-to-end/discovery/ux/information-architecture.md` |
| AC source | `docs/increments/1-walk-in-driver/exploration/stories/acceptance-criteria.md` |
| Domain terms | `docs/increments/1-walk-in-driver/exploration/domain/ubiquitous-language.md` |
| State file | `find-store-map-state.json` |
| Wireframe | `find-store-map.drawio` |
| Last updated | 2026-05-30 |

## Description

Customer opens *store map* to view every *store* as a selectable location, optionally shares location for *distance to store* ranking, and selects a *store* to set *selected store* before browsing *catalog*. Per-store *stock availability* is not shown on this screen.

---

## Design reference

| Design image | Panel/Region | UX element type | Key observations |
| --- | --- | --- | --- |
| IA spec | store map | listbox | Map pins rendered as selectable list items with store identity |
| IA spec | Find Store tab bar | nav-tabs | Map active; List inactive (greyed in hi-fi) |

---

## Screens

### Find Store — Map

**Layout:** stack  
**AC stories:** View Store Map · Calculate Distance to Store

| Region | Slot | Type | Controls | Interaction decisions |
| --- | --- | --- | --- | --- |
| site header · Find Store · catalog | header | chrome | Find Store · catalog nav links | No cart link — Increment 1 excludes cart |
| Find Store tab bar | body | nav-tabs | Map (active) · List | List tab switches to Find Store — List without losing discovery context |
| store map | body | listbox | store pin rows with address; distance to store when location shared | All stores visible without search/filter; selection highlights chosen store |
| store map actions | body | toolbar | use my location · select store | use my location triggers distance recalculation; select store sets selected store (primary path) |

**Conditional states:**
- No location shared: store map rows omit distance to store values (AC Calculate Distance #2)
- Store selected: one listbox item shows selected state before select store confirmation

---

## Affordance trace

| Affordance | AC story | AC clause |
| --- | --- | --- |
| store map (listbox) | View Store Map | AC 1 — displays every store as selectable location |
| store map (selection) | View Store Map | AC 2 — sets selected store on selection |
| store map (all stores visible) | View Store Map | AC 3 — all stores browsable; no stock availability before selected store |
| store map (no filter) | View Store Map | AC 4 — all locations together without search/filter |
| use my location | Calculate Distance to Store | AC 1 — calculates distance to store and nearest-first ranking |
| store map (no distance) | Calculate Distance to Store | AC 2 — stores shown but no distance until location shared |
| store map (distance shown) | Calculate Distance to Store | AC 3 — proximity alongside each store |
| use my location (recalc) | Calculate Distance to Store | AC 4 — recalculates on location change |
| select store | View Store Map | AC 2 — proceed to catalog after selected store set |

---

## CLI

```powershell
node "C:\dev\agilebydesign-skills\practices\user-experience-design\skills\abd-ux-mockup\scripts\drawio-mockup.mjs" `
  save `
  --state "docs/increments/1-walk-in-driver/exploration/ux/find-store-map-state.json" `
  --out   "docs/increments/1-walk-in-driver/exploration/ux/find-store-map.drawio"
```

---

## Change log

| Date | Direction | Summary |
| --- | --- | --- |
| 2026-05-30 | initial | First draft — store map discovery screen |
