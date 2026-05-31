# Lo-fi — Update Stock

> **Companion to** `update-stock.drawio`.

## Metadata

| Field | Value |
| --- | --- |
| Scope | Update Stock — store employee stock maintenance |
| Initial IA | `docs/end-to-end/discovery/ux/information-architecture.md` |
| AC source | `docs/increments/1-walk-in-driver/exploration/stories/acceptance-criteria.md` |
| Domain terms | `docs/increments/1-walk-in-driver/exploration/domain/ubiquitous-language.md` |
| State file | `update-stock-state.json` |
| Wireframe | `update-stock.drawio` |
| Last updated | 2026-05-30 |

## Description

*Store employee* opens stock maintenance for a *store*, edits *product stock levels* per *product*, and saves so *real-time stock* and *stock availability* update for *customers* at that store only.

---

## Design reference

| Design image | Panel/Region | UX element type | Key observations |
| --- | --- | --- | --- |
| IA spec | stock list | list | product and product stock levels columns; edit level inline |
| IA spec | store panel | form | Active store context in sidebar |
| IA spec | employee header | chrome | Staff navigation separate from customer header |

---

## Screens

### Update Stock

**Layout:** sidebar  
**AC stories:** Update Product Stock Levels

| Region | Slot | Type | Controls | Interaction decisions |
| --- | --- | --- | --- | --- |
| employee header · store · Sign out | header | chrome | store name · staff nav | Customer stock maintenance view not available to customers |
| store | panel | form | store (read-only) | Scopes stock list to one store |
| stock list | body | list | product · product stock levels · edit level · save levels | edit level enables inline quantity edit; save levels persists all changes (primary) |
| validation error area | body | chrome | validation message when invalid quantity | Shown when negative or non-numeric quantity submitted |

**Conditional states:**
- Valid save: product stock levels updated; customer views reflect change
- Invalid quantity: validation error area shows message; previous levels unchanged

---

## Affordance trace

| Affordance | AC story | AC clause |
| --- | --- | --- |
| stock list | Update Product Stock Levels | AC 1 — lists products with editable product stock levels |
| save levels | Update Product Stock Levels | AC 2 — saves new levels; updates real-time stock for customers |
| validation error area | Update Product Stock Levels | AC 3 — rejects invalid quantity with clear message |
| stock list (store scoped) | Update Product Stock Levels | AC 4 — only that store's counts change |
| employee header (access) | Update Product Stock Levels | AC 5 — not available to customer; customer reads stock on product detail |

---

## CLI

```powershell
node "C:\dev\agilebydesign-skills\practices\user-experience-design\skills\abd-ux-mockup\scripts\drawio-mockup.mjs" `
  save `
  --state "docs/increments/1-walk-in-driver/exploration/ux/update-stock-state.json" `
  --out   "docs/increments/1-walk-in-driver/exploration/ux/update-stock.drawio"
```

---

## Change log

| Date | Direction | Summary |
| --- | --- | --- |
| 2026-05-30 | initial | First draft — store employee stock maintenance |
