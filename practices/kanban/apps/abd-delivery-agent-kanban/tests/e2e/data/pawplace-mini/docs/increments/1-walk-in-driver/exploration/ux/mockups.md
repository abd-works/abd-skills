# Lo-fi mockups — Increment 1: Walk-in driver (store locator + stock)

> **Scope:** Find Store — Map, Find Store — List, Product Details, Update Stock. Companion flow diagram: `walk-in-flow.drawio`.

## Metadata

| Field | Value |
| --- | --- |
| Scope | Increment 1 walk-in driver — store discovery and stock visibility |
| Initial IA | `docs/end-to-end/discovery/ux/information-architecture.md` |
| AC source | `docs/increments/1-walk-in-driver/exploration/stories/acceptance-criteria.md` |
| Domain terms | `docs/increments/1-walk-in-driver/exploration/domain/ubiquitous-language.md` |
| Output folder | `docs/increments/1-walk-in-driver/exploration/ux/` |
| Last updated | 2026-05-30 |

## Description

Lo-fi wireframes for the walk-in driver increment: *customer* discovers a *store* via *store map* or *store list*, chooses a *selected store*, reads *product* detail with *real-time stock* and *stock availability*, while *store employee* maintains *product stock levels*. No shopping cart or checkout controls appear (Increment 1 scope).

## Screen index

| Screen | State file | Wireframe | Spec |
| --- | --- | --- | --- |
| Find Store — Map | `find-store-map-state.json` | `find-store-map.drawio` | `find-store-map.md` |
| Find Store — List | `find-store-list-state.json` | `find-store-list.drawio` | `find-store-list.md` |
| Product Details | `product-details-state.json` | `product-details.drawio` | `product-details.md` |
| Update Stock | `update-stock-state.json` | `update-stock.drawio` | `update-stock.md` |
| Flow (combined) | `walk-in-flow-state.json` | `walk-in-flow.drawio` | — |

## Design reference

No production design images in workspace. Layout and regions follow discovery IA (`information-architecture.md`) and increment UL verbatim labels.

| Source | Panel/Region | UX element type | Key observations |
| --- | --- | --- | --- |
| IA — Find Store — Map | store map | listbox | Selectable store pins with identity + distance when location shared |
| IA — Find Store — List | store list | list | Tabular rows: store, address, distance to store; nearest first when ranked |
| IA — Product Details | product summary | form | Read-only product fields; stock availability + real-time stock |
| IA — Update Stock | stock list | list | Editable product stock levels per product; save levels primary action |

## Change log

| Date | Direction | Summary |
| --- | --- | --- |
| 2026-05-30 | initial | Store locator + stock screens for Increment 1 exploration |
