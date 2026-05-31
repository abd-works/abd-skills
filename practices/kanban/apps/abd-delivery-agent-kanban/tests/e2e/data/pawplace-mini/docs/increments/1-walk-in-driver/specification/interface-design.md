# Interface design — PawPlace mini — Increment 1

> **Companion to** lo-fi `docs/increments/1-walk-in-driver/exploration/ux/mockups.md` and screen specs under `exploration/ux/`. Specification-stage spec; implementation and tests land in Engineering (`abd-interface-design` implementation pass → ATDD → clean code). This file is authoritative for Sprint 1 store locator and Sprint 2 catalog/stock screens.

## Metadata

| Field | Value |
| --- | --- |
| Scope | Increment 1 — Sprint 1 (Find a store): 2 screens, 3 stories · Sprint 2 (Stock visibility): 3 screens, 3 stories |
| Lo-fi reference | `docs/increments/1-walk-in-driver/exploration/ux/find-store-map.md`, `find-store-list.md`, `product-details.md`, `update-stock.md`, `mockups.md` |
| Hi-fi reference | Visual direction below (no separate hi-fi artifact — lo-fi regions + token table) |
| Acceptance criteria | `docs/increments/1-walk-in-driver/exploration/stories/acceptance-criteria.md` |
| Specification by example | `docs/increments/1-walk-in-driver/specification/specification-by-example.md` |
| Domain terms | `docs/increments/1-walk-in-driver/exploration/domain/ubiquitous-language.md` |
| CRC | `docs/increments/1-walk-in-driver/specification/crc.md` |
| Target framework | React 18 + TypeScript (Vite), Express 4 (per architecture blueprint) |
| Host project root | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\e2e\data\pawplace-mini` |
| Implementation paths | `packages/store/client/` (StoreMapView, StoreListView, FindStoreLayout, CustomerNav, SelectedStoreContext), `packages/app-client/src/pages/StoreLocatorPage.tsx`, `packages/shared/layout-tokens.ts` |
| Test path | `tests/walk-in-driver/find-a-store/find-a-store_client.test.tsx` |
| Last updated | 2026-05-31 (engineering impl pass complete) |

## Description

Sprint 1 covers guest *store discovery*: *customer* opens **Find Store — Map** or **Find Store — List**, optionally shares location for *distance to store* ranking, selects a *store* to set *selected store*, then proceeds to *catalog*. Sprint 2 covers *catalog* browse and *stock visibility*: **Browse Catalog** lists *products* scoped to *selected store*; **Product Details** shows *real-time stock* and *stock availability* for the walk-in decision; **Update Stock** lets *store employee* edit *product stock levels* so customer views stay current. Labels use ubiquitous-language terms verbatim. Per-store *stock availability* does not appear on locator screens or catalog list rows (detail only). No *shopping cart*, checkout, login, or search/filter controls in Increment 1.

---

## Sprint 1: Find a store

Ticket: `1-walk-in-driver-sprint-1`. Stories: View Store Map, View Store List, Calculate Distance to Store.

### Host project conventions (discovered / planned)

- **Folder layout:** domain modules under `packages/<module>/{shared,server,client}`; app shell in `packages/app-client` (per `architecture-blueprint.md`)
- **State management:** React component state + `SelectedStoreProvider` context; store list from `store.api.ts` mock (Engineering wires server later)
- **Styling:** inline styles from `packages/shared/layout-tokens.ts`
- **Token system:** `packages/shared/layout-tokens.ts` — implemented
- **Test framework:** Vitest + React Testing Library (unit/component), Playwright (e2e — deferred)
- **Lint / format / type gates:** `npm test` + `npm run typecheck` from pawplace-mini root
- **Accessibility check:** programmatic labels on listbox/table; `role="alert"` on geolocation errors; keyboard Enter/Space on map options
- **Performance budget:** no explicit bundle cap declared — lazy-load map tile provider if used; do not block first paint on geolocation

### Screens (carried from lo-fi)

| Screen | Layout | Route (planned) | Stories |
| --- | --- | --- | --- |
| Find Store — Map | stack | `/stores/map` | View Store Map, Calculate Distance to Store |
| Find Store — List | stack | `/stores/list` | View Store List, Calculate Distance to Store |

**Customer chrome (Sprint 1):** site header with **Find Store** (current) · **catalog** nav links. No cart link (Increment 1 excludes cart per exploration lo-fi).

**Find Store tab bar:** **Map** · **List** — toggles between routes without losing discovery context (same store inventory, selection state preserved).

#### Find Store — Map — regions and affordances

| Region | Type | Controls (verbatim labels) | Interaction |
| --- | --- | --- | --- |
| site header · Find Store · catalog | chrome | Find Store · catalog | Nav links; Find Store marks current section |
| Find Store tab bar | nav-tabs | Map (active) · List | List tab → `/stores/list` |
| store map | listbox | store pin rows: retail location identity + geographic placement; *distance to store* when ranked | Single-select; highlights *selected store* candidate |
| store map actions | toolbar | use my location · select store | use my location → browser geolocation → Distance To Store API; select store (primary) → sets *selected store* → `/catalog` |

**Conditional states:**
- No location shared: rows omit *distance to store*; default store order from API
- Location shared: rows show *distance to store*; nearest-first sort
- Store highlighted in listbox before confirm: visual selected state on one row
- No per-store *stock availability* on any row

#### Find Store — List — regions and affordances

| Region | Type | Controls (verbatim labels) | Interaction |
| --- | --- | --- | --- |
| site header · Find Store · catalog | chrome | Find Store · catalog | Same as map screen |
| Find Store tab bar | nav-tabs | Map · List (active) | Map tab → `/stores/map` |
| store list | list | columns: store · address · distance to store; use my location · select store | Tabular readable rows; nearest-first when ranked; select store (primary) → *selected store* → `/catalog` |

**Conditional states:**
- No location: *distance to store* column empty
- With location: rows sorted nearest first; first row is easiest nearest spot (AC Calculate Distance #3)

### Visual direction (specification hi-fi)

No production design images in workspace. Engineering implements these roles as CSS variables / theme tokens.

| Role | Typography / colour | Usage |
| --- | --- | --- |
| display | sans-serif, 24/32, weight 600, `#1A1A2E` | Page title region (optional h1: Find Store) |
| body | sans-serif, 16/24, weight 400, `#2D2D2D` | Store names, addresses |
| label | sans-serif, 14/20, weight 500, `#5C5C5C` | Column headers: store · address · distance to store |
| accent | `#B85C38` | Primary action: select store; active tab underline |
| surface | `#FFFFFF` | Screen background |
| surface-muted | `#F5F5F0` | List row hover / selected store highlight |
| focus | 2px solid `#B85C38`, offset 2px | Keyboard focus ring — never removed |
| spacing scale | 4 · 8 · 16 · 24 · 32 px | Region padding and list row gaps |

Map presentation may use pin emoji or SVG marker in listbox rows (lo-fi uses 📍 prefix); real map canvas is optional in mini scope — listbox pattern from lo-fi is the minimum faithful implementation.

### Implementation targets (planned — Engineering)

| Screen / concern | Primary component(s) | Server module |
| --- | --- | --- |
| Find Store — Map | `StoreMapView.tsx`, `StoreLocatorPage.tsx` | `packages/store/server/store.service.ts`, `StoreApi` |
| Find Store — List | `StoreListView.tsx` | same Store module |
| Tab bar + header | `FindStoreLayout.tsx`, `CustomerNav.tsx` | — |
| Distance ranking | `useDistanceToStore.ts` hook | `GET /api/v1/stores?lat=&lng=` or dedicated distance endpoint |
| Selected store context | `SelectedStoreProvider.tsx` | session / client state until catalog route |

---

## Sprint 2: Stock visibility

Ticket: `1-walk-in-driver-sprint-2`. Stories: View Product Details, Display Real-Time Stock Availability (system), Update Product Stock Levels.

### Host project conventions (discovered / planned)

Same as Sprint 1 unless noted:

- **Folder layout:** add `packages/catalog/{shared,server,client}` and `packages/inventory/{shared,server,client}` beside Store module
- **State management:** `SelectedStoreProvider` scopes catalog routes; employee routes use separate auth fixture / role gate
- **Employee vs customer chrome:** distinct headers — customer `Find Store · catalog`; employee `store · Sign out` (staff nav per lo-fi)
- **Real-time refresh:** Product Details polls or subscribes after employee save — Engineering chooses transport; spec requires updated counts on next customer view (AC Display Real-Time #4)

### Screens (carried from lo-fi and IA)

| Screen | Layout | Route (planned) | Stories |
| --- | --- | --- | --- |
| Browse Catalog | sidebar | `/catalog` | View Product Details |
| Product Details | stack | `/catalog/:productId` | View Product Details · Display Real-Time Stock Availability |
| Update Stock | sidebar | `/employee/stock` | Update Product Stock Levels |

**Customer chrome (Sprint 2):** site header with **Find Store** · **catalog** (current on catalog routes). No **Cart** link (Increment 1 excludes cart per exploration scope).

**Employee chrome (Update Stock):** employee header with **store** name · staff nav · **Sign out** — customer stock maintenance not reachable from customer header.

#### Browse Catalog — regions and affordances

| Region | Type | Controls (verbatim labels) | Interaction |
| --- | --- | --- | --- |
| site header · Find Store · catalog | chrome | Find Store · catalog | Nav links; catalog marks current section |
| selected store | panel | selected store name and address · change store | Read-only store context; change store → Find Store flow; scopes product list |
| product list | list | product · price · view product | Rows identify each *product*; view product → `/catalog/:productId` |
| choose store prompt | chrome | choose a store first | Shown when no *selected store*; links to Find Store; no product rows |

**Conditional states:**
- No *selected store*: choose store prompt; empty product list; no *stock availability* anywhere
- With *selected store*: product list populated from *catalog* scoped to store; no per-row *stock availability* (stock on detail only per spec-by-example)
- change store clears browse context and returns to store discovery

#### Product Details — regions and affordances

| Region | Type | Controls (verbatim labels) | Interaction |
| --- | --- | --- | --- |
| site header · Find Store · catalog | chrome | Find Store · catalog | Same customer nav |
| selected store | chrome | selected store name and address | Scopes detail; no aggregate stock across stores |
| product summary | form | product · price · description · real-time stock · stock availability | Read-only fields; *real-time stock* shows on-hand quantity at *selected store*; *stock availability* derived from quantity |
| product summary actions | toolbar | back to catalog | Returns to `/catalog` preserving *selected store* |

**Conditional states:**
- *stock availability* available: positive *real-time stock* at *selected store* — display text `available`
- *stock availability* unavailable: zero *real-time stock* — display text `unavailable`; no *shopping cart*, *checkout*, or online purchase actions
- *real-time stock* always shows single-store count — never sums other stores
- After employee save at same store: next detail view reflects updated *real-time stock* and *stock availability*

**Explicit exclusions (Increment 1):** no add to cart, checkout, payment, or backorder affordances on this screen.

#### Update Stock — regions and affordances

| Region | Type | Controls (verbatim labels) | Interaction |
| --- | --- | --- | --- |
| employee header · store · Sign out | chrome | store name · staff nav · Sign out | Employee-only route; customers receive 403 or redirect |
| store | panel | store (read-only) | Active store context for stock list |
| stock list | list | product · product stock levels · edit level · save levels | edit level enables inline quantity; save levels (primary) persists all pending edits |
| validation error area | chrome | validation message | Shown on invalid quantity submit; `role="alert"` |

**Conditional states:**
- Valid save: *product stock levels* updated at scoped store only; customer Product Details reflects change
- Invalid quantity (negative or non-numeric): validation error area message; prior *product stock levels* unchanged
- Customer attempting route: stock maintenance unavailable; customer still reads stock on Product Details

### Visual direction (specification hi-fi)

Reuse Sprint 1 customer token table for Browse Catalog and Product Details. Employee Update Stock adds:

| Role | Typography / colour | Usage |
| --- | --- | --- |
| staff-surface | `#EEF2F7` | Employee header background |
| success | `#2D6A4F` | Save confirmation toast (optional) |
| danger | `#C0392B` | Validation error text in validation error area |

*stock availability* display: text label `available` or `unavailable` with paired icon — not colour-only (accent green/muted grey allowed with text).

*product stock levels* edit: numeric input with programmatic label including *product* name; `min="0"` integer.

### Implementation targets (engineering — 2026-05-31)

| Screen / concern | Primary component(s) | Supporting module |
| --- | --- | --- |
| Browse Catalog | `packages/catalog/client/CatalogListView.tsx`, `SelectedStorePanel.tsx`, `ChooseStorePrompt.tsx`, `CustomerNav.tsx` | `packages/shared/selected-store.tsx`, `packages/catalog/shared/in-memory-catalog.ts` |
| Product Details | `packages/catalog/client/ProductDetailsView.tsx`, `StockAvailabilityBadge.tsx` | In-memory stock read via `getRealTimeStock` (server API deferred to ATDD) |
| Update Stock | `packages/inventory/client/StockMaintenanceView.tsx`, `EmployeeNav.tsx` | `RequireStoreEmployee.tsx` for customer gate |
| Tests | `tests/walk-in-driver/stock-visibility/stock-visibility_client.test.tsx` | 15 AC-named tests GREEN (Vitest + RTL) |

---

## AC → behaviour → test mapping

One row per AC clause for Sprint 1 stories. Status **passing** after engineering implementation pass (2026-05-31).

### View Store Map

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| View Store Map | 1 | Opening `/stores/map` renders every *store* as selectable listbox item with retail location identity and geographic placement | `View Store Map — AC 1: every store selectable on map` | passing |
| View Store Map | 2 | Selecting a *store* row sets *selected store*; detail visible before select store confirm | `View Store Map — AC 2: selection sets selected store` | passing |
| View Store Map | 3 | All *stores* browsable; no per-store *stock availability* before *selected store* confirmed | `View Store Map — AC 3: no stock before selection` | passing |
| View Store Map | 4 | All locations visible together without search or filter affordance | `View Store Map — AC 4: all stores no filter` | passing |

### View Store List

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| View Store List | 1 | `/stores/list` shows *store list* alternative with store name and identifying details per row | `View Store List — AC 1: list alternative with details` | passing |
| View Store List | 2 | Row selection + select store sets *selected store*; navigates to catalog scoped to store | `View Store List — AC 2: selection proceeds to catalog` | passing |
| View Store List | 3 | Readable tabular rows; Map tab switch preserves same store set and discovery context | `View Store List — AC 3: readable rows tab preserves context` | passing |
| View Store List | 4 | Every *store* listed; no per-store *stock availability* until *selected store* set | `View Store List — AC 4: no stock on list` | passing |

### Calculate Distance to Store

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| Calculate Distance to Store | 1 | use my location calculates *distance to store* per store; nearest-first sort on map and list | `Calculate Distance to Store — AC 1: location ranks nearest first` | passing |
| Calculate Distance to Store | 2 | Without location, both views still show all stores; no distance values | `Calculate Distance to Store — AC 2: stores without distance when no location` | passing |
| Calculate Distance to Store | 3 | Distance appears alongside each store on map and list; nearest at top of list | `Calculate Distance to Store — AC 3: proximity visible nearest on top` | passing |
| Calculate Distance to Store | 4 | New location share recalculates all distances and resort order on both views | `Calculate Distance to Store — AC 4: recalc on location change` | passing |

### View Product Details

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| View Product Details | 1 | `/catalog` with *selected store* lists every *product* with identity clear enough to open detail | `View Product Details — AC 1: catalog lists products at store` | implemented |
| View Product Details | 2 | view product opens detail with product name, description, unit price for walk-in decision | `View Product Details — AC 2: detail names product and description` | implemented |
| View Product Details | 3 | Detail scoped to *selected store*; no cart, checkout, or payment actions | `View Product Details — AC 3: scoped no cart checkout payment` | implemented |
| View Product Details | 4 | `/catalog` without *selected store* shows choose store prompt; no product rows or stock | `View Product Details — AC 4: no store prompts choose first` | implemented |
| View Product Details | 5 | back to catalog preserves *selected store* and product list context | `View Product Details — AC 5: back preserves selected store` | implemented |

### Display Real-Time Stock Availability

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| Display Real-Time Stock Availability | 1 | Product detail shows *real-time stock* on-hand quantity at *selected store* | `Display Real-Time Stock Availability — AC 1: shows on-hand at store` | implemented |
| Display Real-Time Stock Availability | 2 | Positive quantity shows *stock availability* `available` | `Display Real-Time Stock Availability — AC 2: sellable shows available` | implemented |
| Display Real-Time Stock Availability | 3 | Zero quantity shows *stock availability* `unavailable`; no cart/backorder | `Display Real-Time Stock Availability — AC 3: zero shows unavailable no cart` | implemented |
| Display Real-Time Stock Availability | 4 | After employee save, next customer detail shows updated stock | `Display Real-Time Stock Availability — AC 4: employee save updates customer view` | implemented |
| Display Real-Time Stock Availability | 5 | Stock count is single-store only; never aggregates all stores | `Display Real-Time Stock Availability — AC 5: no cross-store aggregate` | implemented |

### Update Product Stock Levels

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| Update Product Stock Levels | 1 | Stock list shows each *product* with editable *product stock levels* | `Update Product Stock Levels — AC 1: list editable quantities` | implemented |
| Update Product Stock Levels | 2 | Valid save persists levels and updates *real-time stock* for customers | `Update Product Stock Levels — AC 2: valid save updates real-time stock` | implemented |
| Update Product Stock Levels | 3 | Invalid quantity rejected with message; prior levels unchanged | `Update Product Stock Levels — AC 3: invalid rejected unchanged` | implemented |
| Update Product Stock Levels | 4 | Save at one store leaves other stores' levels unchanged | `Update Product Stock Levels — AC 4: other stores unchanged` | implemented |
| Update Product Stock Levels | 5 | Customer cannot access stock maintenance; still reads stock on detail | `Update Product Stock Levels — AC 5: customer blocked reads detail stock` | implemented |

---

## Accessibility implementation (Sprint 1 — implemented)

| Check | Status | Notes |
| --- | --- | --- |
| Every input has a programmatic label | done | use my location and select store are `<button>` elements with visible text |
| Focus order matches reading order | done | header nav → Map/List tabs → store rows → use my location → select store |
| Focus is visible | done | accent focus ring via browser default + token styles |
| Errors are programmatically associated | done | Geolocation denied: inline message with `role="alert"` |
| State cues are not colour-only | done | Selected store row: background + aria-selected on listbox option |
| Keyboard reachable | done | Tab/Enter/Space on listbox options; tab bar buttons keyboard accessible |
| Axe passes | done | No rules silenced in component tests |

---

## Performance constraints

| Constraint | Budget | Current | Notes |
| --- | --- | --- | --- |
| Locator screen bundle | baseline TBD | — | No heavy map SDK unless justified; listbox-first meets lo-fi |
| Initial paint | no regression vs shell | — | Render store list from SSR/API without waiting for geolocation |
| Geolocation | async, non-blocking | — | use my location does not gate first render |
| Animation | ≤16 ms/frame | — | Tab switch: opacity/transform only; respect prefers-reduced-motion |
| Catalog list render | no regression vs shell | — | Product list from API without blocking on stock fetch |
| Stock level save | async, non-blocking | — | save levels disables button during submit; inline validation on error |
| Product detail stock | fresh on navigation | — | Refetch *real-time stock* on route enter after employee updates |

---

## Change log

| Date | Direction | Summary |
| --- | --- | --- |
| 2026-05-31 | initial | Sprint 1 store locator spec from exploration lo-fi + AC + spec-by-example |
| 2026-05-31 | engineering | Sprint 1 store locator implemented in packages/store/client; 12/12 AC tests passing |
| 2026-05-31 | engineering | Sprint 2 catalog + stock UI in packages/catalog and packages/inventory; 15/15 client tests passing |
