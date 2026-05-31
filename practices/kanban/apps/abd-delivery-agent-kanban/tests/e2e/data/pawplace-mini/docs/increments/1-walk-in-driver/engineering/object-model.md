---
state: domain-model
sprint_scope: Increment 1 — Sprint 1 (Find a store) and Sprint 2 (Stock visibility)
---

# Module: [PawPlace mini — Increment 1]

Scope: Sprint 1 (Find a store) — View Store Map, View Store List, Calculate Distance to Store; Sprint 2 (Stock visibility) — View Product Details, Display Real-Time Stock Availability, Update Product Stock Levels. Typed surface derived from `docs/increments/1-walk-in-driver/specification/crc.md` and `specification-by-example.md`.

---

# Core Domain

## Increment 1 — Sprint 1: Find a store

*Store* is the physical PawPlace retail location a *customer* discovers and selects before browsing *catalog*. The typed model covers discovery inventory (*Stores*), peer presentation concepts (*Store Map*, *Store List*), proximity ranking (*Distance To Store*), and session context (*Selected Store*).

## **Store**

### **Store** << Entity >>

+ Store(retailLocationIdentity: String, geographicPlacement: GeographicPlacement)
------
+ retailLocationIdentity: String
	Invariant: must identify the retail location for map and list presentation
+ geographicPlacement: GeographicPlacement
	Invariant: must carry coordinates or address used for map placement and distance calculation

### **GeographicPlacement** << ValueObject >>

+ GeographicPlacement(streetAddress: String, latitude: Decimal, longitude: Decimal)
------
+ streetAddress: String
+ latitude: Decimal
+ longitude: Decimal
	Invariant: latitude and longitude must be present when distance ranking is required

### **Stores** << Entity >>

Initialisation: factory loads every active *Store* from persistence at discovery open — caller receives a fully populated inventory.
------
+ << aggregation >> everyRetailLocation: List<Store>
	Invariant: must include every store in discovery inventory without prior search or filter
+ storeMap: Store Map
+ storeList: Store List
+ distanceToStore: Distance To Store
----
+ supplyDiscoveryInventory(): Stores
	Invariant: every store in inventory appears on both store map and store list without prior search or filter
	Interaction:
		activeStores: List<Store> = loadEveryRetailLocation()
		return new Stores(everyRetailLocation: activeStores)
+ sortNearestFirst(customerLocation: CustomerLocation): List<Store>
	Invariant: nearest store appears first when ranking is active
	Interaction:
		rankedStores: List<Store> = distanceToStore.sortStoresNearestFirst(stores: everyRetailLocation, customerLocation: customerLocation)
		return rankedStores
+ presentAllLocationsTogether(): List<Store>
	Invariant: multiple stores appear together without requiring search or filter first
	Interaction:
		return everyRetailLocation

### **Store Map** << Service >>

Initialisation: constructed with a *Stores* inventory reference at discovery open.
------
+ stores: Stores
----
+ showEveryStoreAsSelectableLocation(customer: Customer): List<StoreMapEntry>
	Invariant: every store in inventory appears as a selectable location on the map
	Interaction:
		entries: List<StoreMapEntry> = for each store in stores.everyRetailLocation: StoreMapEntry.fromStore(store: store)
		return entries
+ presentAllLocationsTogether(): List<Store>
	Invariant: all locations appear together without search or filter
	Interaction:
		return stores.presentAllLocationsTogether()
+ supportStoreSelection(customer: Customer, store: Store, selectedStore: Selected Store): Selected Store
	Invariant: selection produces exactly one selected store for downstream catalog scope
	Interaction:
		chosenStore: Selected Store = selectedStore.setFromStoreMap(customer: customer, store: store)
		return chosenStore
+ omitStockAvailabilityBeforeSelectedStore(selectedStore: Selected Store): void
	Invariant: store map never shows per-store stock availability before a selected store exists
	Interaction:
		if selectedStore.isUnset():
			return
		// no stock availability surface on map rows in Sprint 1 discovery

### **Store List** << Service >>

Initialisation: constructed with a *Stores* inventory reference at discovery open.
------
+ stores: Stores
----
+ showAsAlternativeToStoreMap(): Store List
	Invariant: list view is available as an alternative to map-centric layout
+ presentReadableComparisonRows(customer: Customer): List<StoreListRow>
	Invariant: entries are readable without a map-centric layout
	Interaction:
		rows: List<StoreListRow> = for each store in stores.everyRetailLocation: StoreListRow.fromStore(store: store)
		return rows
+ preserveDiscoveryContextOnMapSwitch(customer: Customer, storeMap: Store Map): void
	Invariant: switching to store map retains the same compared stores and selection candidate
	Interaction:
		storeMap.presentAllLocationsTogether()
+ showEveryStoreBeforeSelection(): List<Store>
	Invariant: every store appears before a selected store is set
	Interaction:
		return stores.everyRetailLocation
+ supportStoreSelection(customer: Customer, store: Store, selectedStore: Selected Store): Selected Store
	Invariant: selection from list produces exactly one selected store
	Interaction:
		chosenStore: Selected Store = selectedStore.setFromStoreList(customer: customer, store: store)
		return chosenStore
+ omitStockAvailabilityBeforeSelectedStore(selectedStore: Selected Store): void
	Invariant: store list never shows per-store stock availability before a selected store exists
	Interaction:
		if selectedStore.isUnset():
			return

### **StoreMapEntry** << ValueObject >>

+ StoreMapEntry.fromStore(store: Store): StoreMapEntry
------
+ store: Store
+ distanceToStore: Decimal
	Invariant: distance value appears only after customer shares location

### **StoreListRow** << ValueObject >>

+ StoreListRow.fromStore(store: Store): StoreListRow
------
+ store: Store
+ distanceToStore: Decimal
	Invariant: distance value appears only after customer shares location

### **Distance To Store** << Service >>

Initialisation: stateless service — invoked by *Stores*, *Store Map*, and *Store List* when customer location is available.
------
+ calculateDistanceFromCustomer(customerLocation: CustomerLocation, store: Store): Decimal
	Invariant: distance values appear only after the customer shares location
	Interaction:
		placement: GeographicPlacement = store.geographicPlacement
		return haversineDistance(from: customerLocation, to: placement)
+ sortStoresNearestFirst(stores: List<Store>, customerLocation: CustomerLocation): List<Store>
	Invariant: nearest store appears first when ranking is active
	Interaction:
		ranked: List<Store> = sort stores by calculateDistanceFromCustomer(customerLocation: customerLocation, store: store) ascending
		return ranked
+ showProximityAlongsideStoreOnMap(storeMap: Store Map, customerLocation: CustomerLocation): List<StoreMapEntry>
	Invariant: map rows include distance when ranking is active
	Interaction:
		entries: List<StoreMapEntry> = storeMap.showEveryStoreAsSelectableLocation(customer: customerLocation.customer)
		return entries.withDistance(from: customerLocation)
+ showProximityAlongsideStoreOnList(storeList: Store List, customerLocation: CustomerLocation): List<StoreListRow>
	Invariant: list rows include distance when ranking is active
	Interaction:
		rows: List<StoreListRow> = storeList.presentReadableComparisonRows(customer: customerLocation.customer)
		return rows.withDistance(from: customerLocation)
+ omitDistanceValuesUntilLocationShared(customer: Customer): void
	Invariant: no distance values appear until location is provided
	Interaction:
		if customer.hasNotSharedLocation():
			return
+ recalculateRankingOnLocationChange(customer: Customer, stores: Stores, newLocation: CustomerLocation): List<Store>
	Invariant: changed location recalculates proximity for all stores
	Interaction:
		return sortStoresNearestFirst(stores: stores.everyRetailLocation, customerLocation: newLocation)

### **Selected Store** : **Store** << Entity >>

+ Selected Store.unset(): Selected Store
+ Selected Store.fromStore(store: Store): Selected Store
------
+ isActive: Boolean
	Invariant: without a selected store the system must not show per-store stock availability
	Invariant: exactly one selected store scopes exit from discovery to catalog browsing
----
+ setFromStoreMap(customer: Customer, store: Store): Selected Store
	Interaction:
		return Selected Store.fromStore(store: store)
+ setFromStoreList(customer: Customer, store: Store): Selected Store
	Interaction:
		return Selected Store.fromStore(store: store)
+ isUnset(): Boolean
	Interaction:
		return isActive == false

### references

**Ref — Store module CRC (Sprint 1)**
Source: docs/increments/1-walk-in-driver/specification/crc.md
Locator: Increment 1 — Sprint 1: Find a store
Extract: partial

```source
### **Stores**
every retail location              | Store
supply discovery inventory         | Store Map, Store List, Distance To Store
                                    |   invariant: every store in inventory appears on both store map and store list without prior search or filter

### **Selected Store**
active shopping context store      | Store
set from store map selection       | Store Map, Customer, Store
set from store list selection      | Store List, Customer, Store
                                    |   invariant: without a selected store the system must not show per-store stock availability
                                    |   invariant: exactly one selected store scopes exit from discovery to catalog browsing
```

**Ref — Store locator specification by example**
Source: docs/increments/1-walk-in-driver/specification/specification-by-example.md
Locator: View Store Map, View Store List, Calculate Distance to Store
Extract: partial

```source
When **Customer** *Alex Rivera* opens the **Store Map**
Then **Store Map** shows **Store** *Downtown PawPlace* as a selectable location …
  And **Stores** presents all locations together without search or filter

When **Customer** *Alex Rivera* has not shared location with **Distance To Store**
Then no *distance to store* values appear on the **Store Map** or **Store List**
```

### decisions made

- *Stores* is a collection entity owning discovery inventory and delegating to peer presentation services — matches CRC collection-class rule.
- *Store Map* and *Store List* are services, not UI components — layout and rendering defer to `interface-design.md` (receiver-not-responsible-for-receiving).
- *Selected Store* subtypes *Store* and carries session context; unset factory supports discovery-before-selection invariants.
- *GeographicPlacement*, *StoreMapEntry*, and *StoreListRow* extracted as value objects — CRC properties need typed shapes for distance and address.
- Catalog, *Product*, and stock classes omitted — Sprint 1 stops at store discovery per increment scope (scope-fit test).

---

## Increment 1 — Sprint 2: Stock visibility

*Catalog* is the product assortment and per-*store* inventory view after *selected store* is set. The typed model covers browse inventory (*Products*, *Product*), customer-visible counts (*Real-Time Stock*, *Stock Availability*), and employee-maintained *Product Stock Levels* — no cart, checkout, or payment in this increment.

## **Catalog**

### **Catalog** << Service >>

Initialisation: constructed with *Products* assortment reference when customer enters catalog routes.
------
+ products: Products
+ selectedStore: Selected Store
----
+ presentProductsAfterSelectedStore(customer: Customer, selectedStore: Selected Store, products: Products, productStockLevels: Product Stock Levels): List<ProductCatalogRow>
	Invariant: catalog browse requires a selected store before listing products
	Interaction:
		if selectedStore.isUnset():
			return emptyList()
		scopedProducts: List<Product> = products.supplyBrowseInventory(catalog: this, customer: customer, selectedStore: selectedStore, productStockLevels: productStockLevels)
		return ProductCatalogRow.fromProducts(products: scopedProducts)
+ connectProductIdentityToInventory(product: Product, realTimeStock: Real-Time Stock, stockAvailability: Stock Availability, selectedStore: Selected Store, productStockLevels: Product Stock Levels): ProductDetailView
	Invariant: product detail remains scoped to the current selected store
	Interaction:
		onHandQuantity: Decimal = realTimeStock.showOnHandQuantityAtStore(product: product, selectedStore: selectedStore, productStockLevels: productStockLevels)
		availability: StockAvailabilityStatus = stockAvailability.deriveFromRealTimeStockRules(realTimeStock: realTimeStock, product: product, selectedStore: selectedStore, productStockLevels: productStockLevels)
		return ProductDetailView.fromProduct(product: product, realTimeStock: onHandQuantity, stockAvailability: availability, selectedStore: selectedStore)
+ excludePaymentAndCartActions(customer: Customer): void
	Invariant: catalog does not handle payment, shopping cart, or checkout in this increment
	Interaction:
		return
+ promptChooseStoreWhenUnset(customer: Customer, selectedStore: Selected Store): void
	Invariant: customer must choose a store before product rows appear
	Interaction:
		if selectedStore.isUnset():
			customer.receiveChooseStorePrompt()
			return

### **Products** << Entity >>

Initialisation: factory loads every *Product* in the global assortment — browse scope applied per *selected store* at presentation time.
------
+ << aggregation >> everyCatalogProduct: List<Product>
	Invariant: product list appears only when a selected store scopes the browse context
----
+ supplyBrowseInventory(catalog: Catalog, customer: Customer, selectedStore: Selected Store, productStockLevels: Product Stock Levels): List<Product>
	Invariant: list includes only products offered at the scoped store context
	Interaction:
		scopedProducts: List<Product> = filter everyCatalogProduct where product.isOfferedAtStore(store: selectedStore, productStockLevels: productStockLevels)
		return scopedProducts
+ loadMaintenanceInventory(store: Store): List<ProductStockRow>
	Invariant: stock maintenance lists every product with on-hand quantity at the active store
	Interaction:
		rows: List<ProductStockRow> = for each product in everyCatalogProduct: ProductStockRow.fromProductAndStore(product: product, store: store)
		return rows

### **Product** << Entity >>

+ Product(catalogItemIdentity: String, description: String, unitPrice: Money)
------
+ catalogItemIdentity: String
	Invariant: identity names what the customer considers buying in person
+ description: String
+ unitPrice: Money
----
+ presentDetailForWalkInDecision(catalog: Catalog, customer: Customer, selectedStore: Selected Store): Product
	Invariant: detail remains scoped to the current selected store
	Interaction:
		return this
+ tieToPerStoreInventory(catalog: Catalog, realTimeStock: Real-Time Stock, stockAvailability: Stock Availability, selectedStore: Selected Store, productStockLevels: Product Stock Levels): ProductDetailView
	Interaction:
		return catalog.connectProductIdentityToInventory(product: this, realTimeStock: realTimeStock, stockAvailability: stockAvailability, selectedStore: selectedStore, productStockLevels: productStockLevels)
+ isOfferedAtStore(store: Store, productStockLevels: Product Stock Levels): Boolean
	Interaction:
		return productStockLevels.hasLevelFor(product: this, store: store)

### **Real-Time Stock** << Entity >>

Initialisation: stateless reader — reflects *Product Stock Levels* for customer-visible quantity at one store.
------
+ showOnHandQuantityAtStore(product: Product, selectedStore: Selected Store, productStockLevels: Product Stock Levels): Decimal
	Invariant: real-time stock always refers to the selected store, never an aggregate across all stores
	Interaction:
		return productStockLevels.onHandCountFor(product: product, store: selectedStore)
+ reflectLatestProductStockLevels(productStockLevels: Product Stock Levels, product: Product, store: Store): Decimal
	Invariant: quantity reflects the latest product stock levels recorded for that store
	Interaction:
		return productStockLevels.onHandCountFor(product: product, store: store)
+ updateOnEmployeeStockSave(productStockLevels: Product Stock Levels, storeEmployee: Store Employee, product: Product, store: Store): Decimal
	Interaction:
		savedCount: Decimal = productStockLevels.persistValidUpdate(storeEmployee: storeEmployee, product: product, store: store)
		return savedCount

### **Stock Availability** << Service >>

Initialisation: stateless — derives buy-now signal from *Real-Time Stock* at *selected store*.
------
+ deriveFromRealTimeStockRules(realTimeStock: Real-Time Stock, product: Product, selectedStore: Selected Store, productStockLevels: Product Stock Levels): StockAvailabilityStatus
	Invariant: stock availability tells whether the product can be bought at the selected store now
	Interaction:
		onHandQuantity: Decimal = realTimeStock.showOnHandQuantityAtStore(product: product, selectedStore: selectedStore, productStockLevels: productStockLevels)
		if onHandQuantity > 0:
			return StockAvailabilityStatus.available()
		return StockAvailabilityStatus.unavailable()
+ showAvailableWhenSellable(realTimeStock: Real-Time Stock, product: Product, selectedStore: Selected Store, productStockLevels: Product Stock Levels): StockAvailabilityStatus
	Invariant: positive on-hand quantity yields available for walk-in decision
	Interaction:
		return deriveFromRealTimeStockRules(realTimeStock: realTimeStock, product: product, selectedStore: selectedStore, productStockLevels: productStockLevels)
+ showUnavailableWhenZero(realTimeStock: Real-Time Stock, product: Product, selectedStore: Selected Store, productStockLevels: Product Stock Levels): StockAvailabilityStatus
	Invariant: zero on-hand yields unavailable without online purchase, backorder, or cart actions
	Interaction:
		return deriveFromRealTimeStockRules(realTimeStock: realTimeStock, product: product, selectedStore: selectedStore, productStockLevels: productStockLevels)
+ omitOnlinePurchaseWhenUnavailable(stockAvailability: StockAvailabilityStatus, catalog: Catalog, customer: Customer): void
	Invariant: stock availability never offers online purchase, backorder, or cart actions in this increment
	Interaction:
		if stockAvailability.isUnavailable():
			catalog.excludePaymentAndCartActions(customer: customer)

### **Product Stock Levels** << Entity >>

Initialisation: persistence-backed counts keyed by *Product* and *Store*.
------
+ << aggregation >> levelsByProductAndStore: Map<ProductStoreKey, Decimal>
	Invariant: only store employees may change product stock levels in this increment
	Invariant: updating counts for one store does not change other stores for the same product
----
+ onHandCountFor(product: Product, store: Store): Decimal
	Interaction:
		return levelsByProductAndStore.get(ProductStoreKey(product: product, store: store))
+ hasLevelFor(product: Product, store: Store): Boolean
	Interaction:
		return levelsByProductAndStore.contains(ProductStoreKey(product: product, store: store))
+ editQuantity(storeEmployee: Store Employee, product: Product, store: Store, proposedQuantity: Decimal): ProductStockLevels
	Invariant: editable quantity applies to one product at one store
	Interaction:
		return this.withPendingEdit(storeEmployee: storeEmployee, product: product, store: store, proposedQuantity: proposedQuantity)
+ persistValidUpdate(storeEmployee: Store Employee, product: Product, store: Store): Decimal
	Interaction:
		proposedQuantity: Decimal = pendingEditFor(product: product, store: store)
		if proposedQuantity < 0 or proposedQuantity.isNotNumeric():
			rejectInvalidQuantityUpdate(storeEmployee: storeEmployee)
			return onHandCountFor(product: product, store: store)
		levelsByProductAndStore = levelsByProductAndStore.put(ProductStoreKey(product: product, store: store), proposedQuantity)
		return proposedQuantity
+ rejectInvalidQuantityUpdate(storeEmployee: Store Employee): void
	Interaction:
		storeEmployee.receiveValidationRejection()
		return
+ feedRealTimeStockOnSave(realTimeStock: Real-Time Stock, stockAvailability: Stock Availability, product: Product, store: Store, selectedStore: Selected Store): void
	Interaction:
		realTimeStock.reflectLatestProductStockLevels(productStockLevels: this, product: product, store: store)
		stockAvailability.deriveFromRealTimeStockRules(realTimeStock: realTimeStock, product: product, selectedStore: selectedStore, productStockLevels: this)

### **ProductCatalogRow** << ValueObject >>

+ ProductCatalogRow.fromProducts(products: List<Product>): List<ProductCatalogRow>
------
+ product: Product
+ catalogItemIdentity: String
	Invariant: row identifies the product clearly enough to open detail without per-row stock availability

### **ProductDetailView** << ValueObject >>

+ ProductDetailView.fromProduct(product: Product, realTimeStock: Decimal, stockAvailability: StockAvailabilityStatus, selectedStore: Selected Store): ProductDetailView
------
+ product: Product
+ realTimeStock: Decimal
+ stockAvailability: StockAvailabilityStatus
+ selectedStore: Selected Store
	Invariant: detail view never aggregates on-hand quantity across stores

### **ProductStockRow** << ValueObject >>

+ ProductStockRow.fromProductAndStore(product: Product, store: Store): ProductStockRow
------
+ product: Product
+ onHandCount: Decimal
+ editable: Boolean
	Invariant: maintenance row offers editable on-hand quantity for store employee

### **StockAvailabilityStatus** << ValueObject >>

+ StockAvailabilityStatus.available(): StockAvailabilityStatus
+ StockAvailabilityStatus.unavailable(): StockAvailabilityStatus
------
+ label: String
----
+ isAvailable(): Boolean
+ isUnavailable(): Boolean

### **Money** << ValueObject >>

+ Money(amount: Decimal, currency: String)
------
+ amount: Decimal
+ currency: String

### **ProductStoreKey** << ValueObject >>

+ ProductStoreKey(product: Product, store: Store)
------
+ product: Product
+ store: Store

### references

**Ref — Catalog module CRC (Sprint 2)**
Source: docs/increments/1-walk-in-driver/specification/crc.md
Locator: Increment 1 — Sprint 2: Stock visibility
Extract: partial

```source
### **Catalog**
present products after selected store  | Selected Store, Products, Customer
                                        |   invariant: catalog browse requires a selected store before listing products

### **Real-Time Stock**
                                        |   invariant: real-time stock always refers to the selected store, never an aggregate across all stores

### **Product Stock Levels**
                                        |   invariant: updating counts for one store does not change other stores for the same product
```

**Ref — Catalog and stock specification by example**
Source: docs/increments/1-walk-in-driver/specification/specification-by-example.md
Locator: Sprint 2 — View Product Details, Display Real-Time Stock Availability, Update Product Stock Levels
Extract: partial

```source
When **Customer** *Alex Rivera* opens **Catalog** scoped to **Selected Store** *Downtown PawPlace*
Then **Products** lists **Product** *Premium Salmon Kibble*, **Product** *Reflective Dog Leash*, and **Product** *Limited Edition Cat Tree*

When **Customer** *Alex Rivera* views **Product** *Premium Salmon Kibble* detail
Then **Real-Time Stock** … shows on-hand quantity *12*
  And **Stock Availability** … is *available*

When **Store Employee** *Jordan Lee* submits **Product Stock Levels** *-3* …
Then **Product Stock Levels** rejects the update with a clear message
```

### decisions made

- *Products* is a collection entity owning browse inventory; per-store scope applied at list presentation — matches CRC collection-class rule.
- *Catalog* is a service owning browse and detail orchestration — list layout and stock-on-detail-only defer to `interface-design.md` (receiver-not-responsible-for-receiving).
- *Real-Time Stock* and *Stock Availability* split quantity reflection from buy-now signal — matches CRC state-carrier split.
- *Product Stock Levels* owns employee-maintained counts; saves feed *Real-Time Stock* and *Stock Availability* at the same store only.
- *ProductCatalogRow* omits per-row stock — catalog list shows identity only per spec-by-example and interface-design.
- Cart, checkout, and payment excluded — Sprint 2 stops at visibility per increment scope (scope-fit test).

---

# Boundary Domain

### **Customer** << Entity >>

Initialisation: anonymous session instance — no account required in Increment 1 Sprint 1.
------
+ displayName: String
+ customerLocation: CustomerLocation
+ selectedStore: Selected Store
----
+ openStoreMap(stores: Stores, storeMap: Store Map): List<StoreMapEntry>
	Interaction:
		return storeMap.showEveryStoreAsSelectableLocation(customer: this)
+ openStoreList(stores: Stores, storeList: Store List): List<StoreListRow>
	Interaction:
		return storeList.presentReadableComparisonRows(customer: this)
+ selectStoreFromMap(store: Store, storeMap: Store Map, selectedStore: Selected Store): Selected Store
	Interaction:
		chosen: Selected Store = storeMap.supportStoreSelection(customer: this, store: store, selectedStore: selectedStore)
		this.selectedStore = chosen
		return chosen
+ selectStoreFromList(store: Store, storeList: Store List, selectedStore: Selected Store): Selected Store
	Interaction:
		chosen: Selected Store = storeList.supportStoreSelection(customer: this, store: store, selectedStore: selectedStore)
		this.selectedStore = chosen
		return chosen
+ shareLocation(location: CustomerLocation, distanceToStore: Distance To Store, stores: Stores): List<Store>
	Invariant: sharing location enables nearest-first ranking on map and list
	Interaction:
		this.customerLocation = location
		return distanceToStore.recalculateRankingOnLocationChange(customer: this, stores: stores, newLocation: location)
+ switchBetweenMapAndListViews(storeMap: Store Map, storeList: Store List): void
	Invariant: discovery context preserved when toggling presentation
	Interaction:
		storeList.preserveDiscoveryContextOnMapSwitch(customer: this, storeMap: storeMap)
+ hasNotSharedLocation(): Boolean
	Interaction:
		return customerLocation.isEmpty()

### **CustomerLocation** << ValueObject >>

+ CustomerLocation(latitude: Decimal, longitude: Decimal)
+ CustomerLocation.empty(): CustomerLocation
------
+ latitude: Decimal
+ longitude: Decimal
+ customer: Customer
----
+ isEmpty(): Boolean
	Interaction:
		return latitude == null and longitude == null

### references

**Ref — Customer boundary sketch**
Source: docs/increments/1-walk-in-driver/specification/crc.md
Locator: Boundary Domain — Customer
Extract: partial

```source
### **Customer**
discover stores on store map         | Store Map, Stores
discover stores on store list        | Store List, Stores
choose selected store from map       | Store Map, Selected Store, Store
choose selected store from list      | Store List, Selected Store, Store
share location for proximity ranking | Distance To Store
switch between map and list views    | Store Map, Store List
```

### decisions made

- *Customer* owns discovery and selection actions; *Store Map* and *Store List* own presentation layout — CRC receiver-not-responsible rule preserved at typed layer.
- *CustomerLocation* extracted as value object — geolocation input is immutable per share event; recalculation creates new ranking on *Stores*.
- *Store Employee* omitted from Sprint 1 boundary — stock maintenance belongs to Sprint 2 (scope-fit test).

---

## Increment 1 — Sprint 2: Stock visibility

Sprint 2 extends the *Customer* boundary with catalog browse and stock-reading actions; introduces *Store Employee* for *Product Stock Levels* maintenance.

### **Customer** << Entity >>

Sprint 2 operations extend the Sprint 1 *Customer* boundary (same session instance).
----
+ browseCatalogAfterSelectedStore(catalog: Catalog, products: Products, productStockLevels: Product Stock Levels): List<ProductCatalogRow>
	Invariant: catalog browse requires a selected store before listing products
	Interaction:
		return catalog.presentProductsAfterSelectedStore(customer: this, selectedStore: this.selectedStore, products: products, productStockLevels: productStockLevels)
+ openProductDetailFromCatalog(product: Product, catalog: Catalog, realTimeStock: Real-Time Stock, stockAvailability: Stock Availability, productStockLevels: Product Stock Levels): ProductDetailView
	Interaction:
		return product.tieToPerStoreInventory(catalog: catalog, realTimeStock: realTimeStock, stockAvailability: stockAvailability, selectedStore: this.selectedStore, productStockLevels: productStockLevels)
+ readStockAvailabilityOnDetail(product: Product, catalog: Catalog, realTimeStock: Real-Time Stock, stockAvailability: Stock Availability, productStockLevels: Product Stock Levels): ProductDetailView
	Interaction:
		detailView: ProductDetailView = openProductDetailFromCatalog(product: product, catalog: catalog, realTimeStock: realTimeStock, stockAvailability: stockAvailability, productStockLevels: productStockLevels)
		stockAvailability.omitOnlinePurchaseWhenUnavailable(stockAvailability: detailView.stockAvailability, catalog: catalog, customer: this)
		return detailView
+ returnToCatalogWithoutLosingStore(catalog: Catalog, products: Products, productStockLevels: Product Stock Levels): List<ProductCatalogRow>
	Invariant: selected store persists when returning from product detail
	Interaction:
		return browseCatalogAfterSelectedStore(catalog: catalog, products: products, productStockLevels: productStockLevels)
+ walkInToBuyWhenStockAvailable(stockAvailability: Stock Availability, product: Product, realTimeStock: Real-Time Stock, productStockLevels: Product Stock Levels): void
	Invariant: customer may decide to visit in person when stock availability is available
	Interaction:
		availability: StockAvailabilityStatus = stockAvailability.showAvailableWhenSellable(realTimeStock: realTimeStock, product: product, selectedStore: this.selectedStore, productStockLevels: productStockLevels)
		if availability.isAvailable():
			return
+ promptToChooseStoreBeforeCatalog(catalog: Catalog): void
	Interaction:
		catalog.promptChooseStoreWhenUnset(customer: this, selectedStore: this.selectedStore)
+ receiveChooseStorePrompt(): void
	Interaction:
		return

### **Store Employee** << Entity >>

Initialisation: staff session bound to one *Store* maintenance context.
------
+ displayName: String
+ activeStore: Store
----
+ openStockMaintenanceForStore(store: Store, products: Products, productStockLevels: Product Stock Levels): List<ProductStockRow>
	Interaction:
		this.activeStore = store
		return products.loadMaintenanceInventory(store: store)
+ editOnHandQuantityPerProduct(productStockLevels: Product Stock Levels, product: Product, store: Store, proposedQuantity: Decimal): Product Stock Levels
	Interaction:
		return productStockLevels.editQuantity(storeEmployee: this, product: product, store: store, proposedQuantity: proposedQuantity)
+ submitValidStockLevelUpdate(productStockLevels: Product Stock Levels, realTimeStock: Real-Time Stock, stockAvailability: Stock Availability, product: Product, store: Store, selectedStore: Selected Store): Decimal
	Interaction:
		savedCount: Decimal = productStockLevels.persistValidUpdate(storeEmployee: this, product: product, store: store)
		productStockLevels.feedRealTimeStockOnSave(realTimeStock: realTimeStock, stockAvailability: stockAvailability, product: product, store: store, selectedStore: selectedStore)
		return savedCount
+ receiveRejectionOnInvalidQuantity(productStockLevels: Product Stock Levels, product: Product, store: Store): Decimal
	Interaction:
		productStockLevels.rejectInvalidQuantityUpdate(storeEmployee: this)
		return productStockLevels.onHandCountFor(product: product, store: store)
+ receiveValidationRejection(): void
	Interaction:
		return
+ scopeUpdatesToOneStoreOnly(store: Store, productStockLevels: Product Stock Levels, product: Product): void
	Invariant: updating counts for one store does not change other stores for the same product
	Interaction:
		return

### references

**Ref — Customer and store employee boundary CRC (Sprint 2)**
Source: docs/increments/1-walk-in-driver/specification/crc.md
Locator: Boundary Domain — Sprint 2 responsibilities
Extract: partial

```source
### **Customer**
browse catalog after selected store  | Catalog, Products, Selected Store
read stock availability on detail    | Stock Availability, Real-Time Stock, Product
prompt to choose store before catalog | Selected Store, Catalog

### **Store Employee**
submit valid stock level update        | Product Stock Levels, Real-Time Stock, Stock Availability
                                        |   invariant: store employee cannot access stock maintenance when acting as customer
```

**Ref — Customer and employee specification by example**
Source: docs/increments/1-walk-in-driver/specification/specification-by-example.md
Locator: Sprint 2 boundary scenarios
Extract: partial

```source
When **Customer** *Alex Rivera* attempts to open **Catalog**
Then **Catalog** prompts **Customer** *Alex Rivera* to choose a **Store** first

When **Customer** *Alex Rivera* is not a **Store Employee**
Then stock maintenance for **Product Stock Levels** is not available to **Customer** *Alex Rivera*
```

### decisions made

- Sprint 2 *Customer* operations extend the Sprint 1 entity in place — one anonymous session carries discovery through catalog browse (no duplicate customer type).
- *Store Employee* is a separate boundary actor — stock maintenance unavailable to customers per CRC invariant.
- *Catalog* owns presentation; *Customer* owns browse and read intents — receiver-not-responsible-for-receiving preserved.

