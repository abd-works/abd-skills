---
state: ubiquitous-language
---

# Module: [PawPlace mini — Increment 1]

_Concept sketch for the walk-in driver increment: find a store, browse catalog, see per-store stock, buy in person — no cart or checkout in system._

Scope: Increment 1 (walk-in driver) — store discovery, catalog browsing, and real-time stock visibility at a chosen store. Excludes shopping cart, guest checkout, payment, and order fulfillment (Increment 2).

**Terms**:
- **Store**
  - **store** — a PawPlace retail location where customers shop in person
  - **store map** — map view of store locations for the customer to choose where to shop
  - **store list** — list view of store names and details as an alternative to the store map
  - **distance to store** — proximity ranking of stores relative to the customer
  - **selected store** — the store the customer chooses as context for catalog browsing and stock visibility
- **Catalog**
  - **catalog** — the browsable set of products available through PawPlace
  - **product** — an item in the catalog offered at a store
  - **real-time stock** — current on-hand quantity of a product at the selected store
  - **stock availability** — whether a product can be bought at the selected store now
  - **product stock levels** — on-hand counts a store employee maintains for each product at a store

_A *customer* discovers a *store* via *store map*, *store list*, or *distance to store*, then chooses a *selected store*. From that context the *customer* browses the *catalog*, views *product* details, and reads *real-time stock* and *stock availability* before walking in to buy. A *store employee* maintains *product stock levels* so stock views stay accurate. No online checkout appears in this increment._

---

# Core Domain

## Store

*Store* is the physical PawPlace retail location a *customer* discovers and selects before browsing *catalog* or reading *stock availability*. *Store* owns location identity, discovery views (*store map*, *store list*, *distance to store*), and the *selected store* that scopes catalog and stock for the walk-in journey.

### store

- is a PawPlace retail location where *customers* browse *catalog* and buy in person
- carries identity and location information surfaced on the *store map* and *store list*
- becomes the *selected store* when the *customer* chooses it as the shopping context
- **Invariant:** every *catalog* browse and *stock availability* view in this increment is scoped to exactly one *selected store*

### store map

- shows *store* locations so the *customer* can choose where to shop
- presents geographic placement of *stores* as an alternative to scanning the *store list*
- supports selecting a *store*, producing a *selected store* for downstream *catalog* views

### store list

- presents *store* names and details as an alternative to the *store map*
- lets the *customer* compare *stores* without a map-centric layout
- supports selecting a *store*, producing a *selected store* for downstream *catalog* views

### distance to store

- ranks *stores* by proximity to the *customer*
- helps the *customer* prioritize nearby *stores* when choosing a *selected store*
- may combine with *store map* or *store list* presentation without replacing either view

### selected store

- is the *store* the *customer* picks as active context for *catalog* browsing and *stock availability*
- scopes *real-time stock* and *product* detail views to one retail location
- **Invariant:** without a *selected store*, the system must not show per-store *stock availability*

### customer *(boundary)*

- discovers *stores* and chooses a *selected store*
- browses *catalog* and reads *stock availability* before visiting in person

#### Decisions made

- *Store* owns discovery and selection; *Catalog* depends on *selected store* but does not define store identity (independence test).
- *Selected store* is a concept, not a property of *store* — it carries session context and invariants for stock scoping (typing call).
- *Click-and-collect store* from discovery vocabulary is out of scope for Increment 1 — deferred to Increment 2 checkout (scope-fit test).

#### References

**Ref — Find a Store epic**
Source: docs/end-to-end/discovery/stories/story-map.md
Locator: lines 7–10
Extract: partial

**Ref — Increment 1 stories**
Source: docs/end-to-end/discovery/stories/thin-slicing.md
Locator: Increment 1 stories list
Extract: partial

**Ref — Store module terms**
Source: docs/end-to-end/discovery/domain/domain-terms.md
Locator: Module Store section
Extract: partial

---

## Catalog

*Catalog* is the product assortment and per-*store* inventory view. *Customers* browse *products* and read *real-time stock* and *stock availability* at the *selected store*; *store employees* update *product stock levels* so on-hand counts stay current.

### catalog

- is the browsable set of *products* available through PawPlace
- presents *products* for the *customer* to explore after a *selected store* is chosen
- connects *product* identity to per-store inventory without handling payment or cart

### product

- is an item in the *catalog* offered at a *store*
- exposes detail the *customer* reads before visiting in person
- ties to *real-time stock* and *stock availability* at the *selected store*

### real-time stock

- reflects current on-hand quantity of a *product* at the *selected store*
- updates when *store employees* change *product stock levels*
- **Invariant:** *real-time stock* always refers to the *selected store*, never a aggregate across all *stores*

### stock availability

- tells the *customer* whether a *product* can be bought at the *selected store* now
- derives from *real-time stock* and business rules for sellable quantity
- supports the walk-in decision — buy in person when stock is available

### product stock levels

- are on-hand counts a *store employee* maintains for each *product* at a *store*
- feed *real-time stock* and *stock availability* when updated
- **Invariant:** only *store employees* may change *product stock levels* in this increment

### store employee *(boundary)*

- updates *product stock levels* for *products* at a *store*
- keeps *real-time stock* accurate for *customers* browsing before a walk-in visit

#### Decisions made

- *Catalog* owns assortment and inventory presentation; *Store* owns which location is selected (independence test).
- *Real-time stock* and *stock availability* are separate concepts — quantity versus buy-now signal (typing call).
- Cart, checkout, and order terms from discovery are excluded — Increment 1 stops at visibility (scope-fit test).

#### References

**Ref — Browse Catalog & Stock epic**
Source: docs/end-to-end/discovery/stories/story-map.md
Locator: lines 12–15
Extract: partial

**Ref — Increment 1 outcome**
Source: docs/end-to-end/discovery/stories/thin-slicing.md
Locator: Increment 1 outcome and stories
Extract: partial

**Ref — Catalog module terms**
Source: docs/end-to-end/discovery/domain/domain-terms.md
Locator: Module Catalog section
Extract: partial

---

# Boundary Domain

## Customer

Owned by: Order

- discovers *stores* and selects a *selected store*
- browses *catalog*, views *product* details, and reads *stock availability*
- walks in to buy in person when stock is available — no system checkout in Increment 1

#### Decisions made

- *Customer* is referenced here for walk-in behavior only; account and checkout ownership sit in Order module for Increment 2 (scope-fit test).

#### References

**Ref — Walk-in driver outcome**
Source: docs/end-to-end/discovery/stories/thin-slicing.md
Locator: Increment 1 outcome
Extract: partial

---

## Store employee

Owned by: Order

- maintains *product stock levels* at a *store*
- enables accurate *real-time stock* for *customers* before Increment 2 fulfillment workflows

#### Decisions made

- *Store employee* appears in Increment 1 only for stock maintenance; order preparation belongs to Increment 2 (scope-fit test).

#### References

**Ref — Update Product Stock Levels**
Source: docs/end-to-end/discovery/stories/story-map.md
Locator: line 15
Extract: partial
