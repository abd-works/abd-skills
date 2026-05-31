# Acceptance Criteria — Increment 1: Walk-in driver

Scope: *Customer* finds a *store*, browses *catalog*, sees *real-time stock* at the *selected store*, and walks in to buy in person. No *shopping cart*, guest checkout, or payment in this increment.

Sources: increment `ubiquitous-language.md`, discovery `story-map.md`, `thin-slicing.md` (Increment 1 stories only).

---

## Story: View Store Map

**Story type:** user

### Domain terms

- *Customer* — discovers *stores* and chooses a *selected store*
- *Store* — PawPlace retail location where customers shop in person
- *Store Map* — map view of *store* locations for choosing where to shop
- *Selected Store* — the *store* the *customer* picks as context for *catalog* and *stock availability*

### Acceptance criteria

1. **WHEN** the *customer* opens the *store map*
   **THEN** the system displays every *store* as a selectable location on the map
   **AND** each *store* shows identity and location information from the *store* record
   **Evidence:** `ubiquitous-language.md` — Store > *store map*, "shows *store* locations"; `story-map.md` — line 8, View Store Map

2. **WHEN** the *customer* selects a *store* on the *store map*
   **THEN** the system sets that *store* as the *selected store*
   **AND** the *customer* sees enough detail to confirm the choice before browsing *catalog*
   **Evidence:** `ubiquitous-language.md` — Store > *selected store*, "the *store* the *customer* picks"; `information-architecture.md` — Find Store — Map / view map

3. **WHEN** the *customer* views the *store map* before choosing a *selected store*
   **THEN** all *stores* remain browsable on the map
   **BUT** the system does not show per-store *stock availability* until a *selected store* is chosen
   **Evidence:** `ubiquitous-language.md` — Store > *selected store* invariant, "without a *selected store*, the system must not show per-store *stock availability*"

4. **WHEN** multiple *stores* exist
   **THEN** the *store map* presents all locations together without requiring the *customer* to search or filter first
   **Evidence:** `story-map.md` — Find a Store epic, lines 7–10; `thin-slicing.md` — Increment 1 outcome, store discovery before catalog

---

## Story: View Store List

**Story type:** user

### Domain terms

- *Customer* — discovers *stores* and chooses a *selected store*
- *Store* — PawPlace retail location
- *Store List* — list view of *store* names and details as an alternative to the *store map*
- *Selected Store* — active shopping context for downstream *catalog* views

### Acceptance criteria

1. **WHEN** the *customer* opens store discovery
   **THEN** the system offers a *store list* as an alternative to the *store map*
   **AND** each row shows a *store* name with identifying details
   **Evidence:** `ubiquitous-language.md` — Store > *store list*, "presents *store* names and details"; `story-map.md` — line 9, View Store List

2. **WHEN** the *customer* selects a *store* from the *store list*
   **THEN** the system sets that *store* as the *selected store*
   **AND** the *customer* can proceed to browse *catalog* scoped to that location
   **Evidence:** `ubiquitous-language.md` — Store > *store list*, "supports selecting a *store*, producing a *selected store*"; `information-architecture.md` — Find Store — List / view list

3. **WHEN** the *customer* compares *stores* in the *store list*
   **THEN** entries are readable without a map-centric layout
   **AND** the *customer* can switch to the *store map* without losing the current discovery context
   **Evidence:** `ubiquitous-language.md` — Store > *store list*, "lets the *customer* compare *stores* without a map-centric layout"

4. **WHEN** the *customer* has not yet chosen a *selected store*
   **THEN** the *store list* still lists every *store*
   **BUT** per-store *stock availability* remains hidden until a *selected store* is set
   **Evidence:** `ubiquitous-language.md` — Store > *selected store* invariant; Catalog intro, "*catalog* browse … scoped to exactly one *selected store*"

---

## Story: Calculate Distance to Store

**Story type:** user

### Domain terms

- *Customer* — provides location context for proximity ranking
- *Store* — retail location receiving a proximity rank
- *Distance To Store* — proximity ranking of *stores* relative to the *customer*
- *Store Map* / *Store List* — discovery surfaces that may show ranked results

### Acceptance criteria

1. **WHEN** the *customer* shares location for store discovery
   **THEN** the system calculates *distance to store* for each *store*
   **AND** *stores* sort with nearest locations first
   **Evidence:** `ubiquitous-language.md` — Store > *distance to store*, "ranks *stores* by proximity"; `story-map.md` — line 10, Calculate Distance to Store

2. **WHEN** the *customer* has not shared location
   **THEN** the system still shows *stores* on the *store map* and *store list*
   **BUT** no *distance to store* values appear until location is provided
   **Evidence:** `ubiquitous-language.md` — Store > *distance to store*, "helps the *customer* prioritize nearby *stores*"; optional location implied by ranking concept

3. **WHEN** *distance to store* has been calculated
   **THEN** proximity appears alongside each *store* in both the *store map* and *store list* presentations
   **AND** the nearest *store* is easy to spot at the top of ranked results
   **Evidence:** `information-architecture.md` — story trace, Calculate Distance on Map and List; `thin-slicing.md` — Increment 1, find the store before seeing stock

4. **WHEN** the *customer* changes shared location
   **THEN** the system recalculates *distance to store* for all *stores*
   **AND** sort order updates to reflect the new nearest-first ranking
   **Evidence:** `ubiquitous-language.md` — Store > *distance to store*, "may combine with *store map* or *store list* presentation"

---

## Story: View Product Details

**Story type:** user

### Domain terms

- *Customer* — browses *catalog* after choosing a *selected store*
- *Catalog* — browsable set of *products* available through PawPlace
- *Product* — item in the *catalog* offered at a *store*
- *Selected Store* — scopes which *catalog* and stock context apply

### Acceptance criteria

1. **WHEN** the *customer* has a *selected store* and opens the *catalog*
   **THEN** the system lists *products* available to explore at that store context
   **AND** each row identifies the *product* clearly enough to open detail
   **Evidence:** `ubiquitous-language.md` — Catalog > *catalog*, "presents *products* … after a *selected store* is chosen"; `story-map.md` — line 13, View Product Details

2. **WHEN** the *customer* selects a *product* from the *catalog*
   **THEN** the system shows *product* detail the *customer* reads before visiting in person
   **AND** the detail view names the *product* and describes what the *customer* is considering buying
   **Evidence:** `ubiquitous-language.md` — Catalog > *product*, "exposes detail the *customer* reads before visiting in person"; `information-architecture.md` — Browse Catalog → Product Details

3. **WHEN** the *customer* views *product* detail
   **THEN** the view remains scoped to the current *selected store*
   **BUT** no *shopping cart*, checkout, or payment actions appear in this increment
   **Evidence:** `ubiquitous-language.md` — scope note, "Excludes shopping cart, guest checkout, payment"; `thin-slicing.md` — Increment 1, no checkout in system

4. **WHEN** the *customer* attempts to browse *catalog* without a *selected store*
   **THEN** the system prompts the *customer* to choose a *store* first
   **BUT** does not show per-store *stock availability* until a *selected store* exists
   **Evidence:** `ubiquitous-language.md` — Store > *selected store* invariant; Catalog > *real-time stock* invariant, "always refers to the *selected store*"

5. **WHEN** the *customer* finishes reading *product* detail
   **THEN** the *customer* can return to the *catalog* list without losing the *selected store*
   **Evidence:** `information-architecture.md` — Browse Catalog / product list navigation; `thin-slicing.md` — Increment 1 walk-in journey, browse then visit store

---

## Story: Display Real-Time Stock Availability

**Story type:** system

### Domain terms

- *Product* — item whose on-hand quantity is shown
- *Selected Store* — single retail location for stock scoping
- *Real-Time Stock* — current on-hand quantity at the *selected store*
- *Stock Availability* — whether the *product* can be bought at the *selected store* now

### Acceptance criteria

1. **WHEN** the *customer* views *product* detail with a *selected store*
   **THEN** the system displays *real-time stock* for that *product* at the *selected store*
   **AND** the quantity reflects the latest *product stock levels* recorded for that location
   **Evidence:** `ubiquitous-language.md` — Catalog > *real-time stock*; `story-map.md` — line 14, Display Real-Time Stock Availability

2. **WHEN** *real-time stock* indicates sellable quantity
   **THEN** the system shows *stock availability* as available now at the *selected store*
   **AND** the *customer* can decide to walk in and buy in person
   **Evidence:** `ubiquitous-language.md` — Catalog > *stock availability*, "tells the *customer* whether a *product* can be bought at the *selected store* now"

3. **WHEN** *real-time stock* is zero at the *selected store*
   **THEN** the system shows *stock availability* as unavailable at that location
   **BUT** does not offer online purchase, backorder, or cart actions in this increment
   **Evidence:** `thin-slicing.md` — Increment 1, no checkout; `ubiquitous-language.md` — scope excludes cart and checkout

4. **WHEN** a *store employee* updates *product stock levels* for the *selected store*
   **THEN** the next *customer* view of *product* detail shows updated *real-time stock* and *stock availability*
   **Evidence:** `ubiquitous-language.md` — Catalog > *product stock levels*, "feed *real-time stock* … when updated"; `story-map.md` — Update Product Stock Levels feeds this story

5. **WHEN** the system renders stock for a *product*
   **THEN** counts apply only to the *selected store*
   **BUT** never aggregates on-hand quantity across all *stores* in one number
   **Evidence:** `ubiquitous-language.md` — Catalog > *real-time stock* invariant, "never aggregate across all *stores*"

---

## Story: Update Product Stock Levels

**Story type:** user

### Domain terms

- *Store Employee* — maintains on-hand counts so stock views stay accurate
- *Store* — location where counts are maintained
- *Product* — catalog item receiving a stock count
- *Product Stock Levels* — on-hand counts the *store employee* maintains per *product* at a *store*
- *Real-Time Stock* / *Stock Availability* — customer-visible outcomes updated after saves

### Acceptance criteria

1. **WHEN** the *store employee* opens the stock maintenance view for a *store*
   **THEN** the system lists *products* with current *product stock levels* at that *store*
   **AND** each row offers an editable on-hand quantity
   **Evidence:** `ubiquitous-language.md` — Catalog > *product stock levels*; `information-architecture.md` — Update Stock / stock list; `story-map.md` — line 15

2. **WHEN** the *store employee* submits a valid updated quantity for a *product* at a *store*
   **THEN** the system saves the new *product stock levels*
   **AND** *real-time stock* and *stock availability* for *customers* reflect the change at that *store*
   **Evidence:** `ubiquitous-language.md` — Catalog > *product stock levels*, "feed *real-time stock* and *stock availability* when updated"

3. **WHEN** the *store employee* enters an invalid quantity (negative or non-numeric)
   **THEN** the system rejects the update with a clear message
   **BUT** the previous *product stock levels* remain unchanged
   **Evidence:** `ubiquitous-language.md` — Catalog > *real-time stock* invariant, accurate counts must not be corrupted; standard validation — flagged as assumption in exploration

4. **WHEN** the *store employee* updates *product stock levels* for one *store*
   **THEN** only that *store*'s counts change for the *product*
   **BUT** other *stores*' *product stock levels* for the same *product* stay as they were
   **Evidence:** `ubiquitous-language.md` — Catalog > *real-time stock*, scoped to *selected store*; multi-store discovery in Store module

5. **WHEN** a *customer* is not a *store employee*
   **THEN** the stock maintenance view is not available
   **BUT** the *customer* can still read *stock availability* on *product* detail
   **Evidence:** `ubiquitous-language.md` — Catalog > *product stock levels* invariant, "only *store employees* may change *product stock levels* in this increment"
