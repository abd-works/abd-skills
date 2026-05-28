# Semantic Context Chunking Report

**Source folder:** `{{source_folder}}`
**Files scanned:** {{total_files}} ({{chunked_count}} chunked, {{passthrough_count}} passed through)
**Chunks produced:** {{total_chunks}}

---

## Story View ({{story_chunk_count}} chunks)

{{#each story_epics}}
### {{epic_name}} (epic)

{{#each sub_epics}}
- **{{sub_epic_name}}** (sub-epic)
{{#each chunks}}
  - `{{chunk_id}}` — {{one_line_summary}} ({{actor}}, {{path_type}})
{{/each}}
{{/each}}

{{/each}}

---

## Domain View ({{domain_chunk_count}} chunks)

{{#each domain_modules}}
### {{module_name}} (module)

{{#each key_abstractions}}
- **{{ka_name}}** (key abstraction)
{{#each chunks}}
  - `{{chunk_id}}` — {{one_line_summary}} ({{stereotype}})
{{/each}}
{{/each}}

{{/each}}

---

## Architecture View ({{arch_chunk_count}} chunks)

{{#each arch_depths}}
### {{depth_level}}

{{#each components}}
- **{{component_name}}** ({{component_type}})
{{#each chunks}}
  - `{{chunk_id}}` — {{one_line_summary}} ({{provenance}}{{#if pattern}}, pattern: {{pattern}}{{/if}})
{{/each}}
{{/each}}

{{/each}}

---

## UX View ({{ux_chunk_count}} chunks)

{{#each ux_screens}}
### {{screen_name}} (screen)

{{#each chunks}}
- `{{chunk_id}}` — {{one_line_summary}} ({{fidelity}})
{{/each}}

{{/each}}

---

## Untagged ({{untagged_count}} chunks)

{{#each untagged_chunks}}
- `{{chunk_id}}` — {{reason}}
{{/each}}

---

## Pass-through ({{passthrough_count}} files, < ~1,500 chars each)

{{#each passthrough_files}}
- `{{filename}}` — tagged: [{{primary_views}}] {{top_level_tags}}
{{/each}}

---

## Example (Pet Store engagement)

The following is a filled example for a small pet store project to show the report shape and level of detail.

# Semantic Context Chunking Report

**Source folder:** `markdown/`
**Files scanned:** 14 (9 chunked, 5 passed through)
**Chunks produced:** 47

---

## Story View (23 chunks)

### Manage Orders (epic)

- **Process Order** (sub-epic)
  - `requirements__chunk_03` — Order submission flow with address validation (user, spine)
  - `requirements__chunk_04` — Order validation rules and error handling (system, spine)
  - `requirements__chunk_05` — Payment authorization during checkout (user, spine)
- **Track Order** (sub-epic)
  - `requirements__chunk_07` — Email and SMS status notifications (system, optional)
  - `requirements__chunk_08` — Order history with filtering (user, optional)

### Manage Catalog (epic)

- **Browse Products** (sub-epic)
  - `product-spec__chunk_01` — Category navigation and product listing (user, spine)
  - `product-spec__chunk_02` — Product search with autocomplete (user, optional)
- **Manage Inventory** (sub-epic)
  - `product-spec__chunk_04` — Stock level updates and low-stock alerts (system, spine)

### Manage Customers (epic)

- **Register Customer** (sub-epic)
  - `onboarding__chunk_01` — Self-service registration with email verification (user, spine)
- **Manage Profile** (sub-epic)
  - `onboarding__chunk_03` — Address book management (user, optional)

---

## Domain View (31 chunks)

### Order Management (module)

- **Order** (key abstraction)
  - `requirements__chunk_03` — Order entity with line items and totals (aggregate)
  - `data-model__chunk_01` — Order aggregate boundary and invariants (aggregate)
  - `requirements__chunk_04` — Order validation rules (specification)
- **Payment** (key abstraction)
  - `requirements__chunk_05` — Payment authorization and capture (entity)
  - `data-model__chunk_02` — Payment transaction states (entity)

### Product Catalog (module)

- **Product** (key abstraction)
  - `product-spec__chunk_01` — Product with categories and attributes (entity)
  - `product-spec__chunk_03` — Product variant and pricing (value_object)
- **Inventory** (key abstraction)
  - `product-spec__chunk_04` — Stock level as tracked quantity (value_object)
  - `data-model__chunk_03` — Inventory reservation and release (service)

### Customer (module)

- **Customer** (key abstraction)
  - `onboarding__chunk_01` — Customer registration entity (entity)
  - `onboarding__chunk_02` — Address as value object (value_object)

---

## Architecture View (12 chunks)

### outline

- `tech-overview__chunk_01` — Platform: MERN web app, three-tier (custom)
- `tech-overview__chunk_02` — Deployment: AWS ECS with Fargate (ootb)
- `tech-overview__chunk_03` — CDN and static hosting via CloudFront (ootb)

### blueprint

- **Order Service** (component)
  - `tech-overview__chunk_05` — Service boundaries and API contract (custom)
- **Product Service** (component)
  - `tech-overview__chunk_06` — Catalog search with Elasticsearch (configured)

### reference

- **persistence** (mechanism)
  - `data-model__chunk_01` — Repository pattern for order aggregate (custom, pattern: repository)
- **error_handling** (mechanism)
  - `tech-overview__chunk_07` — Global error middleware with structured logging (custom)
- **security** (mechanism)
  - `tech-overview__chunk_08` — JWT auth with AWS Cognito (extended)

---

## UX View (8 chunks)

### Product Listing (screen)

- `wireframes__chunk_01` — Main layout: header, filter sidebar, product grid (ia)
- `wireframes__chunk_02` — Category filter tree and sort controls (mockup)

### Product Detail (screen)

- `wireframes__chunk_03` — Image gallery, pricing, add-to-cart button (mockup)

### Shopping Cart (screen)

- `wireframes__chunk_04` — Cart table with quantity controls and subtotals (mockup)

### Checkout (screen)

- `wireframes__chunk_05` — Multi-step: address, shipping, payment, confirm (mockup)
- `wireframes__chunk_06` — Address form with validation states (mockup)

### Order Dashboard (screen)

- `wireframes__chunk_07` — Filterable order table with status badges (ia)
- `wireframes__chunk_08` — Order detail modal with timeline (mockup)

---

## Untagged (0 chunks)

---

## Pass-through (5 files, < ~1,500 chars each)

- `glossary.md` — tagged: [domain] module: Order Management, module: Product Catalog
- `api-notes.md` — tagged: [architecture] depth: outline, platform: MERN
- `team-roles.md` — tagged: [story] actor: user, fidelity: outline
- `color-palette.md` — tagged: [ux] fidelity: interface
- `env-setup.md` — tagged: [architecture] depth: implementation, provenance: configured
