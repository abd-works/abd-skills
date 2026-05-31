---
state: crc
---

# Module: [PawPlace mini — Increment 1]

Scope: Increment 1 (Walk-in driver) — Sprint 1 (Find a store) and Sprint 2 (Stock visibility) integrated below. No cart or checkout (Increment 2).

**Core terms**:
- store
- store map
- store list
- distance to store
- selected store
- catalog
- product
- real-time stock
- stock availability
- product stock levels

**Key Abstractions (term grouping)**:
- **Store**: store, store map, store list, distance to store, selected store
- **Catalog**: catalog, product, real-time stock, stock availability, product stock levels

---

# Core Domain

## Increment 1 — Sprint 1: Find a store

Store-locator specification scope from increment exploration `ubiquitous-language.md` and `acceptance-criteria.md` (View Store Map, View Store List, Calculate Distance to Store).

## **Store**

*Store* is the physical PawPlace retail location a *customer* discovers and selects before browsing *catalog*. Sprint 1 covers discovery views, proximity ranking, and *selected store* context only.

### **Store**
retail location identity           | (name and identifying details)
geographic placement               | (coordinates for map presentation)
surface identity on store map      | Store Map
surface identity on store list     | Store List
receive proximity rank             | Distance To Store

### **Stores**
every retail location              | Store
supply discovery inventory         | Store Map, Store List, Distance To Store
                                    |   invariant: every store in inventory appears on both store map and store list without prior search or filter

### **Store Map**
geographic store layout            | Store, Stores
show every store as selectable location | Store, Stores, Customer
present all locations together     | Stores
support store selection            | Customer, Selected Store, Store
omit stock availability before selected store | Selected Store
                                    |   invariant: store map never shows per-store stock availability before a selected store exists

### **Store List**
store name and detail rows         | Store, Stores
show as alternative to store map   | Store Map
present readable comparison rows   | Store, Stores, Customer
preserve discovery context on map switch | Store Map, Customer
show every store before selection  | Stores
support store selection            | Customer, Selected Store, Store
omit stock availability before selected store | Selected Store
                                    |   invariant: store list never shows per-store stock availability before a selected store exists

### **Distance To Store**
proximity ranking per store        | Store, Stores
calculate distance from customer location | Customer, Store
sort stores nearest first          | Stores
show proximity alongside store on map | Store Map, Store
show proximity alongside store on list | Store List, Store
omit distance values until location shared | Customer
recalculate ranking on location change | Customer, Stores
                                    |   invariant: distance values appear only after the customer shares location
                                    |   invariant: nearest store appears first when ranking is active

### **Selected Store**
active shopping context store      | Store
set from store map selection       | Store Map, Customer, Store
set from store list selection      | Store List, Customer, Store
                                    |   invariant: without a selected store the system must not show per-store stock availability
                                    |   invariant: exactly one selected store scopes exit from discovery to catalog browsing

### references

**Ref — Store module ubiquitous language**
Source: docs/increments/1-walk-in-driver/exploration/domain/ubiquitous-language.md
Locator: Store KA, lines 31–64
Extract: partial

```source
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
```

**Ref — Store locator acceptance criteria**
Source: docs/increments/1-walk-in-driver/exploration/stories/acceptance-criteria.md
Locator: View Store Map, View Store List, Calculate Distance to Store
Extract: partial

```source
## Story: View Store Map
…
1. **WHEN** the *customer* opens the *store map*
   **THEN** the system displays every *store* as a selectable location on the map
…
4. **WHEN** multiple *stores* exist
   **THEN** the *store map* presents all locations together without requiring the *customer* to search or filter first

## Story: View Store List
…
3. **WHEN** the *customer* compares *stores* in the *store list*
   **THEN** entries are readable without a map-centric layout
   **AND** the *customer* can switch to the *store map* without losing the current discovery context

## Story: Calculate Distance to Store
…
2. **WHEN** the *customer* has not shared location
   **THEN** the system still shows *stores* on the *store map* and *store list*
   **BUT** no *distance to store* values appear until location is provided
```

### decisions made

- Introduced *Stores* as a collection class — discovery inventory and nearest-first sorting apply to the group, not a single *Store* (collection-class rule).
- *Selected store* is a separate concept carrying session context, not a property on *Store* (typing call from exploration UL).
- *Store map* and *store list* are peer presentation concepts; *distance to store* combines with either without replacing them (AC and UL alignment).
- Catalog and stock concepts appear only as boundary invariants — out of Sprint 1 CRC scope but preserved on *Selected Store* (scope-fit test).

---

## Increment 1 — Sprint 2: Stock visibility

Catalog and stock specification scope from increment exploration `ubiquitous-language.md` and `acceptance-criteria.md` (View Product Details, Display Real-Time Stock Availability, Update Product Stock Levels).

## **Catalog**

*Catalog* is the product assortment and per-*store* inventory view. Sprint 2 covers *product* detail, *real-time stock*, *stock availability* at the *selected store*, and *product stock levels* maintenance by *store employees* — no cart or checkout.

### **Catalog**
browsable product assortment           | Products
present products after selected store  | Selected Store, Products, Customer
connect product identity to inventory  | Product, Real-Time Stock, Stock Availability
exclude payment and cart actions       | Customer
                                        |   invariant: catalog browse requires a selected store before listing products
                                        |   invariant: catalog does not handle payment, shopping cart, or checkout in this increment

### **Products**
every catalog product                  | Product
supply browse inventory                | Catalog, Customer
                                        |   invariant: product list appears only when a selected store scopes the browse context

### **Product**
catalog item identity                  | (name and describing details)
detail for walk-in decision            | Catalog, Customer
tie to per-store inventory             | Real-Time Stock, Stock Availability, Selected Store
                                        |   invariant: product detail remains scoped to the current selected store

### **Real-Time Stock**
current on-hand quantity at store      | Product, Selected Store, Product Stock Levels
reflect latest product stock levels    | Product Stock Levels, Product
update on employee stock save          | Product Stock Levels, Store Employee
                                        |   invariant: real-time stock always refers to the selected store, never an aggregate across all stores

### **Stock Availability**
buy-now signal at selected store       | Real-Time Stock, Product, Selected Store
show available when sellable quantity  | Real-Time Stock, Customer
show unavailable when zero on hand       | Real-Time Stock, Customer
derive from real-time stock rules        | Real-Time Stock
                                        |   invariant: stock availability tells whether the product can be bought at the selected store now
                                        |   invariant: stock availability never offers online purchase, backorder, or cart actions in this increment

### **Product Stock Levels**
on-hand count per product at store     | Product, Store
editable quantity for store employee   | Store Employee, Product
feed real-time stock on save           | Real-Time Stock, Stock Availability
reject invalid quantity update         | Store Employee
                                        |   invariant: only store employees may change product stock levels in this increment
                                        |   invariant: updating counts for one store does not change other stores for the same product

### references

**Ref — Catalog module ubiquitous language**
Source: docs/increments/1-walk-in-driver/exploration/domain/ubiquitous-language.md
Locator: Catalog KA, lines 96–156
Extract: partial

```source
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
```

**Ref — Catalog and stock acceptance criteria**
Source: docs/increments/1-walk-in-driver/exploration/stories/acceptance-criteria.md
Locator: View Product Details, Display Real-Time Stock Availability, Update Product Stock Levels
Extract: partial

```source
## Story: View Product Details
…
1. **WHEN** the *customer* has a *selected store* and opens the *catalog*
   **THEN** the system lists *products* available to explore at that store context
…
4. **WHEN** the *customer* attempts to browse *catalog* without a *selected store*
   **THEN** the system prompts the *customer* to choose a *store* first

## Story: Display Real-Time Stock Availability
…
1. **WHEN** the *customer* views *product* detail with a *selected store*
   **THEN** the system displays *real-time stock* for that *product* at the *selected store*
…
5. **WHEN** the system renders stock for a *product*
   **THEN** counts apply only to the *selected store*
   **BUT** never aggregates on-hand quantity across all *stores* in one number

## Story: Update Product Stock Levels
…
2. **WHEN** the *store employee* submits a valid updated quantity for a *product* at a *store*
   **THEN** the system saves the new *product stock levels*
   **AND** *real-time stock* and *stock availability* for *customers* reflect the change at that *store*
```

### decisions made

- Introduced *Products* as a collection class — browse inventory applies to the assortment, not a single *Product* (collection-class rule).
- *Real-time stock* and *stock availability* are separate concepts — quantity versus buy-now signal (typing call from exploration UL).
- *Product stock levels* owns employee-maintained counts; *Real-Time Stock* owns customer-visible reflection (state-carrier split).
- Cart, checkout, and payment excluded — Sprint 2 stops at visibility per increment scope (scope-fit test).

---

# Boundary Domain

### **Customer**
discover stores on store map         | Store Map, Stores
discover stores on store list        | Store List, Stores
choose selected store from map       | Store Map, Selected Store, Store
choose selected store from list      | Store List, Selected Store, Store
share location for proximity ranking | Distance To Store
switch between map and list views    | Store Map, Store List
browse catalog after selected store  | Catalog, Products, Selected Store
open product detail from catalog     | Product, Catalog, Selected Store
read stock availability on detail    | Stock Availability, Real-Time Stock, Product
return to catalog without losing store | Catalog, Selected Store
walk in to buy when stock available  | Stock Availability, Product
prompt to choose store before catalog | Selected Store, Catalog

### **Store Employee**
open stock maintenance for store       | Store, Product Stock Levels, Products
edit on-hand quantity per product      | Product Stock Levels, Product, Store
submit valid stock level update        | Product Stock Levels, Real-Time Stock, Stock Availability
receive rejection on invalid quantity  | Product Stock Levels
scope updates to one store only        | Store, Product Stock Levels
                                        |   invariant: store employee cannot access stock maintenance when acting as customer

### references

**Ref — Customer boundary sketch**
Source: docs/increments/1-walk-in-driver/exploration/domain/ubiquitous-language.md
Locator: Store > customer (boundary), lines 66–69
Extract: partial

```source
### customer *(boundary)*

- discovers *stores* and chooses a *selected store*
- browses *catalog* and reads *stock availability* before visiting in person
```

**Ref — Store employee boundary sketch**
Source: docs/increments/1-walk-in-driver/exploration/domain/ubiquitous-language.md
Locator: Catalog > store employee (boundary), lines 130–133
Extract: partial

```source
### store employee *(boundary)*

- updates *product stock levels* for *products* at a *store*
- keeps *real-time stock* accurate for *customers* browsing before a walk-in visit
```

### decisions made

- *Customer* owns discovery and catalog browse actions; presentation concepts (*Store Map*, *Store List*, *Catalog*) own layout — receiver-not-responsible-for-receiving (CRC rule).
- *Store employee* appears for stock maintenance only; order preparation belongs to Increment 2 (scope-fit test).
- Sprint 1 boundary covered store-locator stories; Sprint 2 extends *Customer* and adds *Store Employee*.
