# Four-View Taxonomy Reference

This document defines the complete tag vocabulary for the four practice views. Every tag assigned to a chunk must use values from this reference. Tags are hierarchical — use the deepest level the content supports.

---

## Story View

Tags for content about user interactions, behaviors, processes, flows, acceptance criteria, scenarios, and user journeys.

### Tag hierarchy

| Tag | Type | Description |
|-----|------|-------------|
| `story.epic` | free text (verb–noun) | Top-level capability area. Name follows verb–noun convention from story mapping (e.g. "Manage Orders", "Browse Catalog"). |
| `story.sub_epic` | free text (verb–noun) | Flow or feature area within an epic (e.g. "Process Order", "Search Products"). |
| `story.story` | free text (verb–noun) | Leaf-level behavior within a sub-epic (e.g. "Submit Order", "Filter by Category"). |
| `story.actor` | enum | Who performs the action: `user`, `system`, `technical`. |
| `story.increment` | free text | Delivery slice or release grouping the behavior belongs to (e.g. "MVI-1", "Sprint 3 scope"). |
| `story.fidelity` | enum | How refined the content is: `outline` (high-level), `exploration` (acceptance criteria), `specification` (concrete scenarios), `executable` (test-ready). |
| `story.path_type` | enum | Kind of path through the behavior: `spine` (happy path), `optional` (enhancement), `alternate` (valid variation), `error` (failure handling), `edge` (boundary condition). |

### What qualifies for Story view

- Descriptions of what users or systems **do** — workflows, processes, steps, interactions
- Acceptance criteria or acceptance-test-style conditions (WHEN/THEN)
- Scenario narratives with actors, triggers, and outcomes
- Feature descriptions that name behaviors, not just data
- User journey maps, flow diagrams described in prose
- Front-to-back interaction sequences (UI action through to backend response)

### What does NOT qualify

- Pure data definitions with no behavioral context (Domain view)
- Technology platform descriptions with no user interaction (Architecture view)
- Screen layouts described without the user action they support (UX view)

---

## Domain View

Tags for content about system functions, data structures, business rules, invariants, domain vocabulary, entity relationships, and state transitions.

### Tag hierarchy

| Tag | Type | Description |
|-----|------|-------------|
| `domain.bounded_context` | free text | Strategic boundary in the domain (e.g. "Sales", "Fulfillment"). Use when content explicitly names or implies a context boundary. |
| `domain.module` | free text | Scope partition within a bounded context (e.g. "Order Management", "Customer Profile"). |
| `domain.module_kind` | enum | Classification of what the module governs: `resolution` (lookup/matching), `measure` (metrics/quantities), `actor` (people/roles), `temporal` (scheduling/time), `state_vocabulary` (status/lifecycle), `resource_economy` (inventory/allocation), `behavior_catalog` (rules/policies), `constraint` (validation/limits). |
| `domain.key_abstraction` | free text | A building-block concept group within a module (e.g. "Order", "Payment", "Customer"). |
| `domain.term` | free text | A specific concept within a key abstraction (e.g. "Order Line", "Shipping Address", "Payment Method"). |
| `domain.stereotype` | enum | DDD building-block classification: `entity`, `value_object`, `aggregate`, `service`, `domain_event`, `repository`, `factory`, `specification`. |
| `domain.fidelity` | enum | How far the domain model has been refined: `partition` (module boundaries), `terms` (named concepts), `ubiquitous_language` (defined vocabulary), `domain_model` (responsibilities and collaborators), `domain_specification` (typed relationships), `building_blocks` (DDD stereotypes). |

### What qualifies for Domain view

- Business vocabulary definitions, glossary entries, term lists
- Data model descriptions — entities, attributes, relationships
- Business rules, invariants, constraints, validation logic
- State machines and lifecycle descriptions (e.g. order statuses)
- Aggregate boundaries and consistency rules
- Domain events and what triggers them
- Descriptions of what the system **knows** and **enforces** (vs what it **does** for users)

### What does NOT qualify

- Pure workflow descriptions with no data or rule content (Story view)
- Implementation details of how data is stored or transmitted (Architecture view)
- How domain data is displayed on screen (UX view)

---

## Architecture View

Tags for content about system components, platforms, technology choices, deployment topology, integration points, cross-cutting mechanisms, patterns, and non-functional requirements.

### Tag hierarchy

| Tag | Type | Description |
|-----|------|-------------|
| `arch.depth` | enum | Architectural detail level: `outline` (context, topology, principles), `blueprint` (named components, mechanisms, data model), `reference` (detailed mechanism design, code patterns), `implementation` (runnable code guidance), `nfr` (SLI/SLO/SLA targets). |
| `arch.platform` | free text | Named platform or runtime (e.g. "AWS ECS", "Azure Functions", "PostgreSQL", "React"). |
| `arch.layer` | free text | Logical layer in the architecture (e.g. "Presentation", "Domain", "Infrastructure", "API Gateway"). |
| `arch.component` | free text | Named architectural component (e.g. "Order Service", "Payment Gateway", "Message Broker"). |
| `arch.mechanism` | free text (semi-enum) | Cross-cutting concern: `security`, `error_handling`, `logging`, `validation`, `configuration`, `caching`, `communication`, `persistence`, or a custom mechanism name. |
| `arch.pattern` | free text | Named design or architecture pattern (e.g. "repository", "saga", "outbox", "CQRS", "circuit breaker"). |
| `arch.provenance` | enum | Whether the component is built or bought: `custom` (team-written code), `ootb` (out-of-the-box platform feature), `configured` (platform feature with significant configuration), `extended` (platform feature with custom extensions). |
| `arch.nfr_category` | enum | Non-functional requirement category: `performance`, `availability`, `security`, `usability`, `maintainability`, `interoperability`. |

### What qualifies for Architecture view

- System context diagrams or descriptions (what connects to what)
- Deployment topology — where components run, how they scale
- Technology stack choices and rationale
- Component descriptions with responsibilities and interfaces
- Cross-cutting mechanism descriptions (how errors are handled, how logging works)
- Integration patterns and protocols
- Non-functional requirements with measurable targets
- Architectural decision records (ADRs) or trade-off discussions
- Custom vs out-of-the-box distinctions for platform capabilities

### What does NOT qualify

- Business rules that happen to be enforced in code (Domain view)
- User workflows through the system (Story view)
- Screen layouts and UI component choices (UX view)

---

## UX View

Tags for content about screens, layouts, navigation, controls, wireframes, mockups, visual design, and accessibility requirements.

### Tag hierarchy

| Tag | Type | Description |
|-----|------|-------------|
| `ux.screen` | free text | Named screen or page (e.g. "Order Dashboard", "Product Detail", "Checkout"). |
| `ux.region` | free text | Named area within a screen (e.g. "Header", "Filter Sidebar", "Order Summary Panel"). |
| `ux.content_type` | free text | Domain concept the user sees on this screen (e.g. "Order List", "Product Card", "Customer Profile"). |
| `ux.nav_component` | free text | Cross-screen navigation element (e.g. "Main Menu", "Breadcrumb", "Tab Bar"). |
| `ux.control_type` | free text | Specific UI control (e.g. "data table", "dropdown", "date picker", "search box", "tree view"). |
| `ux.interaction` | free text | Conditional state or interaction mode (e.g. "empty state", "error state", "loading", "disabled", "hover", "selected"). |
| `ux.fidelity` | enum | Design detail level: `ia` (information architecture — screen inventory and transitions), `mockup` (lo-fi wireframe with controls and layout), `interface` (hi-fi production-ready design or code). |

### What qualifies for UX view

- Screen inventories and site maps
- Wireframe descriptions — layout, regions, controls
- Navigation structure — what links to what, breadcrumbs, menus
- UI component specifications — control types, states, behaviors
- Mockup annotations — what appears where, in which state
- Accessibility requirements for specific screens or controls
- Visual design specifications — colors, typography, spacing (when described in prose)
- Responsive layout descriptions — what changes at which breakpoint

### What does NOT qualify

- Backend API contract details with no UI surface (Architecture view)
- Business rules that drive what appears on screen (Domain view — the rule itself; UX view only for how the result is displayed)
- Pure user journey descriptions with no screen or layout detail (Story view)

---

## Cross-view overlap guidance

Some content legitimately informs multiple views. Tag all applicable views — do not force a single assignment.

| Content example | Primary views | Rationale |
|----------------|---------------|-----------|
| "The order submission form validates address format before calling the order service" | story, ux, domain | Story: user submits order. UX: form with validation feedback. Domain: address validation rule. |
| "Orders transition from Pending to Confirmed when payment succeeds" | domain | State machine — pure domain. |
| "The order service runs on AWS ECS with auto-scaling to handle 1000 orders/minute" | architecture | Platform, deployment, NFR — no user behavior or domain rule. |
| "The dashboard shows a filterable table of orders with status badges" | ux | Screen layout and controls — no new behavior or domain concept. |
| "Users can cancel an order from the order detail screen if status is Pending" | story, ux, domain | Story: cancel behavior. UX: screen and action. Domain: status constraint. |
| "Payment processing uses Stripe API with webhook callbacks for async confirmation" | architecture, domain | Architecture: integration pattern, external platform. Domain: payment confirmation event. |

When in doubt, tag broadly and let downstream skills filter by the view they need.
