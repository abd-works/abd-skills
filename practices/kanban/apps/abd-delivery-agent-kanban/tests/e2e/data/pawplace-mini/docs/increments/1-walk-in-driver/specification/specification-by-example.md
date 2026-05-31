# Specification by Example — PawPlace mini — Increment 1

**Sources / context:** `docs/increments/1-walk-in-driver/specification/crc.md`, `docs/increments/1-walk-in-driver/exploration/stories/acceptance-criteria.md`, `docs/increments/1-walk-in-driver/exploration/ux/find-store-map-state.json`, `docs/increments/1-walk-in-driver/exploration/ux/product-details-state.json`, `docs/increments/1-walk-in-driver/exploration/ux/update-stock-state.json`

Scope: Sprint 1 (Find a store) and Sprint 2 (Stock visibility) integrated below. No cart, checkout, or payment in this increment.

---

## Background

Given **Stores** supplies discovery inventory with **Store** *Downtown PawPlace* at geographic placement *123 Main St*
  And **Store** *Westside PawPlace* at geographic placement *456 Oak Ave*
  And **Store** *Uptown PawPlace* at geographic placement *789 Pine Rd*
  And **Customer** *Alex Rivera* has no **Selected Store**

---

## Story: View Store Map

**Story type:** user

**Sources / context:** CRC — Store Map, Stores, Selected Store; AC View Store Map

---

## Scenarios

### Scenario 1: Every store appears as a selectable location on the store map

Given **Customer** *Alex Rivera* has not shared location with **Distance To Store**
When **Customer** *Alex Rivera* opens the **Store Map**
Then **Store Map** shows **Store** *Downtown PawPlace* as a selectable location with retail location identity *Downtown PawPlace* and geographic placement *123 Main St*
  And **Store Map** shows **Store** *Westside PawPlace* as a selectable location with retail location identity *Westside PawPlace* and geographic placement *456 Oak Ave*
  And **Store Map** shows **Store** *Uptown PawPlace* as a selectable location with retail location identity *Uptown PawPlace* and geographic placement *789 Pine Rd*
  And **Stores** presents all locations together without search or filter

### Scenario 2: Store selection on the map sets the selected store

Given **Customer** *Alex Rivera* is viewing the **Store Map**
When **Customer** *Alex Rivera* selects **Store** *Westside PawPlace* on the **Store Map**
Then **Selected Store** is **Store** *Westside PawPlace*
  And **Customer** *Alex Rivera* sees retail location identity *Westside PawPlace* and geographic placement *456 Oak Ave* to confirm the choice

### Scenario 3: Store map omits stock availability before a selected store exists

Given **Customer** *Alex Rivera* is viewing the **Store Map**
  And **Customer** *Alex Rivera* has no **Selected Store**
When **Customer** *Alex Rivera* browses every **Store** on the **Store Map**
Then **Store Map** does not show per-store *stock availability* for any **Store**
  And **Stores** remains browsable on the **Store Map**

### Scenario 4: Multiple stores require no prior search or filter

Given **Stores** includes **Store** *Downtown PawPlace*, **Store** *Westside PawPlace*, and **Store** *Uptown PawPlace*
When **Customer** *Alex Rivera* opens the **Store Map**
Then **Store Map** presents **Store** *Downtown PawPlace*, **Store** *Westside PawPlace*, and **Store** *Uptown PawPlace* together
  And **Customer** *Alex Rivera* did not search or filter **Stores** first

---

## Story: View Store List

**Story type:** user

**Sources / context:** CRC — Store List, Stores, Selected Store; AC View Store List

---

## Scenarios

### Scenario 1: Store list offers an alternative to the store map

Given **Customer** *Alex Rivera* opens store discovery
When **Customer** *Alex Rivera* views the **Store List**
Then **Store List** shows **Store** *Downtown PawPlace* with retail location identity *Downtown PawPlace* and geographic placement *123 Main St*
  And **Store List** shows **Store** *Westside PawPlace* with retail location identity *Westside PawPlace* and geographic placement *456 Oak Ave*
  And **Store List** shows **Store** *Uptown PawPlace* with retail location identity *Uptown PawPlace* and geographic placement *789 Pine Rd*
  And **Store List** is available as an alternative to the **Store Map**

### Scenario 2: Store selection from the list sets the selected store

Given **Customer** *Alex Rivera* is viewing the **Store List**
When **Customer** *Alex Rivera* selects **Store** *Downtown PawPlace* from the **Store List**
Then **Selected Store** is **Store** *Downtown PawPlace*
  And **Customer** *Alex Rivera* can proceed to browse *catalog* scoped to **Selected Store** *Downtown PawPlace*

### Scenario 3: Store list rows are readable and map switch preserves discovery context

Given **Customer** *Alex Rivera* is comparing **Stores** on the **Store List**
  And **Store List** ranks **Store** *Downtown PawPlace* above **Store** *Westside PawPlace* when **Distance To Store** is active
When **Customer** *Alex Rivera* switches from the **Store List** to the **Store Map**
Then **Store Map** still presents **Store** *Downtown PawPlace*, **Store** *Westside PawPlace*, and **Store** *Uptown PawPlace*
  And **Customer** *Alex Rivera* retains the same discovery context without losing the compared **Stores**

### Scenario 4: Store list hides stock availability until a selected store is set

Given **Customer** *Alex Rivera* is viewing the **Store List**
  And **Customer** *Alex Rivera* has no **Selected Store**
When **Customer** *Alex Rivera* reads every row on the **Store List**
Then **Store List** lists every **Store** in **Stores**
  And **Store List** does not show per-store *stock availability* for any **Store**

---

## Story: Calculate Distance to Store

**Story type:** user

**Sources / context:** CRC — Distance To Store, Stores, Store Map, Store List; AC Calculate Distance to Store

---

## Scenarios

### Scenario 1: Shared location ranks stores nearest first on map and list

Given **Customer** *Alex Rivera* shares location at *43.6532° N, 79.3832° W*
When **Distance To Store** calculates proximity ranking per **Store** for **Stores**
Then **Stores** sorts with **Store** *Downtown PawPlace* first at *2.1 km*
  And **Store** *Westside PawPlace* ranks second at *4.8 km*
  And **Store** *Uptown PawPlace* ranks third at *6.3 km*
  And **Store Map** shows *distance to store* alongside **Store** *Downtown PawPlace*, **Store** *Westside PawPlace*, and **Store** *Uptown PawPlace*
  And **Store List** shows *distance to store* alongside each **Store** row with **Store** *Downtown PawPlace* at the top

### Scenario 2: Stores remain visible without distance values when location is not shared

Given **Customer** *Alex Rivera* has not shared location with **Distance To Store**
When **Customer** *Alex Rivera* views the **Store Map** and the **Store List**
Then **Store Map** still shows **Store** *Downtown PawPlace*, **Store** *Westside PawPlace*, and **Store** *Uptown PawPlace*
  And **Store List** still lists every **Store** in **Stores**
  And no *distance to store* values appear on the **Store Map** or **Store List**

### Scenario 3: Nearest store is easy to spot when ranking is active

Given **Customer** *Alex Rivera* shares location at *43.6532° N, 79.3832° W*
  And **Distance To Store** has calculated proximity ranking per **Store**
When **Customer** *Alex Rivera* opens the **Store List**
Then the first row is **Store** *Downtown PawPlace* at *2.1 km*
  And **Customer** *Alex Rivera* can spot the nearest **Store** without scanning the full **Stores** inventory

### Scenario 4: Changed location recalculates distance and resort order

Given **Customer** *Alex Rivera* previously shared location at *43.6532° N, 79.3832° W*
  And **Distance To Store** ranked **Store** *Downtown PawPlace* first at *2.1 km*
When **Customer** *Alex Rivera* shares a new location at *43.7000° N, 79.4000° W*
Then **Distance To Store** recalculates proximity ranking per **Store** for all **Stores**
  And **Stores** sorts with **Store** *Westside PawPlace* first at *1.4 km*
  And **Store** *Downtown PawPlace* ranks second at *3.2 km*
  And **Store Map** and **Store List** update *distance to store* values to reflect the new nearest-first order

---

## Background — Sprint 2

Given **Customer** *Alex Rivera* has **Selected Store** *Downtown PawPlace*
  And **Products** in **Catalog** scoped to **Selected Store** *Downtown PawPlace* include **Product** *Premium Salmon Kibble*, **Product** *Reflective Dog Leash*, and **Product** *Limited Edition Cat Tree*
  And **Product Stock Levels** for **Product** *Premium Salmon Kibble* at **Store** *Downtown PawPlace* are *12*
  And **Product Stock Levels** for **Product** *Reflective Dog Leash* at **Store** *Downtown PawPlace* are *5*
  And **Product Stock Levels** for **Product** *Limited Edition Cat Tree* at **Store** *Downtown PawPlace* are *0*
  And **Product Stock Levels** for **Product** *Premium Salmon Kibble* at **Store** *Westside PawPlace* are *8*

---

## Story: View Product Details

**Story type:** user

**Sources / context:** CRC — Catalog, Products, Product, Selected Store; AC View Product Details

---

## Scenarios

### Scenario 1: Catalog lists products scoped to the selected store

Given **Customer** *Alex Rivera* has **Selected Store** *Downtown PawPlace*
When **Customer** *Alex Rivera* opens **Catalog** scoped to **Selected Store** *Downtown PawPlace*
Then **Products** lists **Product** *Premium Salmon Kibble*, **Product** *Reflective Dog Leash*, and **Product** *Limited Edition Cat Tree*
  And each row identifies the **Product** clearly enough to open detail

### Scenario 2: Product detail names what the customer considers buying in person

Given **Customer** *Alex Rivera* has **Selected Store** *Downtown PawPlace*
When **Customer** *Alex Rivera* selects **Product** *Premium Salmon Kibble* from **Catalog**
Then **Product** detail shows catalog item identity *Premium Salmon Kibble*
  And **Product** detail describes *grain-free salmon recipe for adult dogs* for the walk-in decision
  And **Product** detail shows unit price *$24.99*

### Scenario 3: Product detail stays scoped to selected store without cart actions

Given **Customer** *Alex Rivera* has **Selected Store** *Downtown PawPlace*
  And **Customer** *Alex Rivera* is viewing **Product** *Reflective Dog Leash* detail
When **Customer** *Alex Rivera* reads the full **Product** summary
Then **Product** detail remains scoped to **Selected Store** *Downtown PawPlace*
  And **Catalog** does not offer *shopping cart*, *checkout*, or *payment* actions on the detail view

### Scenario 4: Catalog browse without selected store prompts store choice first

Given **Customer** *Alex Rivera* has no **Selected Store**
When **Customer** *Alex Rivera* attempts to open **Catalog**
Then **Catalog** prompts **Customer** *Alex Rivera* to choose a **Store** first
  And **Products** does not list **Product** rows until **Selected Store** exists
  And no per-store *stock availability* appears before **Selected Store** is set

### Scenario 5: Back to catalog preserves selected store context

Given **Customer** *Alex Rivera* has **Selected Store** *Downtown PawPlace*
  And **Customer** *Alex Rivera* is viewing **Product** *Premium Salmon Kibble* detail
When **Customer** *Alex Rivera* returns to **Catalog** from **Product** detail
Then **Catalog** still scopes **Products** to **Selected Store** *Downtown PawPlace*
  And **Customer** *Alex Rivera* can open another **Product** without re-selecting a **Store**

---

## Story: Display Real-Time Stock Availability

**Story type:** system

**Sources / context:** CRC — Real-Time Stock, Stock Availability, Product, Selected Store, Product Stock Levels; AC Display Real-Time Stock Availability

---

## Scenarios

### Scenario 1: Product detail shows real-time stock at the selected store

Given **Customer** *Alex Rivera* has **Selected Store** *Downtown PawPlace*
  And **Product Stock Levels** for **Product** *Premium Salmon Kibble* at **Store** *Downtown PawPlace* are *12*
When **Customer** *Alex Rivera* views **Product** *Premium Salmon Kibble* detail
Then **Real-Time Stock** for **Product** *Premium Salmon Kibble* at **Selected Store** *Downtown PawPlace* shows on-hand quantity *12*
  And **Real-Time Stock** reflects the latest **Product Stock Levels** recorded for **Store** *Downtown PawPlace*

### Scenario 2: Sellable quantity shows stock availability as available now

Given **Customer** *Alex Rivera* has **Selected Store** *Downtown PawPlace*
  And **Real-Time Stock** for **Product** *Reflective Dog Leash* at **Selected Store** *Downtown PawPlace* is *5*
When **Customer** *Alex Rivera* views **Product** *Reflective Dog Leash* detail
Then **Stock Availability** for **Product** *Reflective Dog Leash* at **Selected Store** *Downtown PawPlace* is *available*
  And **Customer** *Alex Rivera* can decide to walk in and buy **Product** *Reflective Dog Leash* in person

### Scenario 3: Zero on-hand shows unavailable without cart or backorder actions

Given **Customer** *Alex Rivera* has **Selected Store** *Downtown PawPlace*
  And **Real-Time Stock** for **Product** *Limited Edition Cat Tree* at **Selected Store** *Downtown PawPlace* is *0*
When **Customer** *Alex Rivera* views **Product** *Limited Edition Cat Tree* detail
Then **Stock Availability** for **Product** *Limited Edition Cat Tree* at **Selected Store** *Downtown PawPlace* is *unavailable*
  And **Catalog** does not offer *online purchase*, *backorder*, or *shopping cart* actions for **Product** *Limited Edition Cat Tree*

### Scenario 4: Employee stock save updates the next customer stock view

Given **Store Employee** *Jordan Lee* maintains **Product Stock Levels** for **Store** *Downtown PawPlace*
  And **Product Stock Levels** for **Product** *Premium Salmon Kibble* at **Store** *Downtown PawPlace* are *12*
When **Store Employee** *Jordan Lee* saves **Product Stock Levels** *3* for **Product** *Premium Salmon Kibble* at **Store** *Downtown PawPlace*
  And **Customer** *Alex Rivera* with **Selected Store** *Downtown PawPlace* opens **Product** *Premium Salmon Kibble* detail
Then **Real-Time Stock** for **Product** *Premium Salmon Kibble* at **Selected Store** *Downtown PawPlace* shows on-hand quantity *3*
  And **Stock Availability** for **Product** *Premium Salmon Kibble* at **Selected Store** *Downtown PawPlace* is *available*

### Scenario 5: Stock counts apply only to selected store never aggregate all stores

Given **Customer** *Alex Rivera* has **Selected Store** *Downtown PawPlace*
  And **Product Stock Levels** for **Product** *Premium Salmon Kibble* at **Store** *Downtown PawPlace* are *12*
  And **Product Stock Levels** for **Product** *Premium Salmon Kibble* at **Store** *Westside PawPlace* are *8*
When **Customer** *Alex Rivera* views **Product** *Premium Salmon Kibble* detail
Then **Real-Time Stock** shows on-hand quantity *12* for **Selected Store** *Downtown PawPlace* only
  And **Real-Time Stock** does not aggregate *20* across **Store** *Downtown PawPlace* and **Store** *Westside PawPlace*

---

## Story: Update Product Stock Levels

**Story type:** user

**Sources / context:** CRC — Product Stock Levels, Real-Time Stock, Stock Availability, Store Employee; AC Update Product Stock Levels

---

## Scenarios

### Scenario 1: Stock maintenance lists products with editable on-hand quantities

Given **Store Employee** *Jordan Lee* opens stock maintenance for **Store** *Downtown PawPlace*
When **Store Employee** *Jordan Lee* views the stock list for **Store** *Downtown PawPlace*
Then the list shows **Product** *Premium Salmon Kibble* with **Product Stock Levels** *12*
  And the list shows **Product** *Reflective Dog Leash* with **Product Stock Levels** *5*
  And the list shows **Product** *Limited Edition Cat Tree* with **Product Stock Levels** *0*
  And each row offers an editable on-hand quantity for **Product Stock Levels**

### Scenario 2: Valid quantity save updates real-time stock and stock availability

Given **Store Employee** *Jordan Lee* is editing **Product Stock Levels** for **Product** *Reflective Dog Leash* at **Store** *Downtown PawPlace*
  And current **Product Stock Levels** are *5*
When **Store Employee** *Jordan Lee* submits **Product Stock Levels** *2* for **Product** *Reflective Dog Leash* at **Store** *Downtown PawPlace*
Then **Product Stock Levels** for **Product** *Reflective Dog Leash* at **Store** *Downtown PawPlace* persist as *2*
  And **Real-Time Stock** for **Product** *Reflective Dog Leash* at **Store** *Downtown PawPlace* reflects on-hand quantity *2*
  And **Stock Availability** for **Product** *Reflective Dog Leash* at **Store** *Downtown PawPlace* remains *available*

### Scenario 3: Invalid quantity is rejected and prior levels stay unchanged

Given **Store Employee** *Jordan Lee* is editing **Product Stock Levels** for **Product** *Premium Salmon Kibble* at **Store** *Downtown PawPlace*
  And current **Product Stock Levels** are *12*
When **Store Employee** *Jordan Lee* submits **Product Stock Levels** *-3* for **Product** *Premium Salmon Kibble* at **Store** *Downtown PawPlace*
Then **Product Stock Levels** rejects the update with a clear message
  And **Product Stock Levels** for **Product** *Premium Salmon Kibble* at **Store** *Downtown PawPlace* remain *12*
  And **Real-Time Stock** for **Product** *Premium Salmon Kibble* at **Store** *Downtown PawPlace* still shows on-hand quantity *12*

### Scenario 4: Stock update at one store leaves other stores unchanged

Given **Product Stock Levels** for **Product** *Premium Salmon Kibble* at **Store** *Downtown PawPlace* are *12*
  And **Product Stock Levels** for **Product** *Premium Salmon Kibble* at **Store** *Westside PawPlace* are *8*
When **Store Employee** *Jordan Lee* saves **Product Stock Levels** *4* for **Product** *Premium Salmon Kibble* at **Store** *Downtown PawPlace*
Then **Product Stock Levels** for **Product** *Premium Salmon Kibble* at **Store** *Downtown PawPlace* are *4*
  And **Product Stock Levels** for **Product** *Premium Salmon Kibble* at **Store** *Westside PawPlace* remain *8*

### Scenario 5: Customer cannot access stock maintenance but still reads stock availability

Given **Customer** *Alex Rivera* has **Selected Store** *Downtown PawPlace*
  And **Customer** *Alex Rivera* is not a **Store Employee**
When **Customer** *Alex Rivera* browses **Catalog** and opens **Product** *Premium Salmon Kibble* detail
Then stock maintenance for **Product Stock Levels** is not available to **Customer** *Alex Rivera*
  And **Customer** *Alex Rivera* still reads **Stock Availability** and **Real-Time Stock** on **Product** detail
