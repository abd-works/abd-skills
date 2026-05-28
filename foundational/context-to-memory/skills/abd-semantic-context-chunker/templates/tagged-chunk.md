# Tagged Chunk Template

Each chunk file produced by **abd-semantic-context-chunker** uses YAML front matter to carry its identity, source lineage, size, view assignments, and hierarchical tags. The body of the chunk file is the original markdown content from the source document.

## Front matter shape

```yaml
---
chunk_id: {{source_stem}}__chunk_{{NN}}
source_file: {{path_relative_to_source_folder}}
section_path: "{{heading_trail_from_source}}"
chunk_size_chars: {{character_count}}
primary_views: [{{view_1}}, {{view_2}}]
tags:
  {{view_1}}:
    {{tag_level_1}}: {{value}}
    {{tag_level_2}}: {{value}}
  {{view_2}}:
    {{tag_level_1}}: {{value}}
evidence_type: {{prose|table|list|diagram_description|mixed}}
---

{{original_markdown_content}}
```

## Field reference

| Field | Required | Description |
|-------|----------|-------------|
| `chunk_id` | yes | Unique identifier: source file stem + `__chunk_` + zero-padded sequence number. |
| `source_file` | yes | Path to the original markdown file, relative to the source folder. |
| `section_path` | yes | Heading trail from the source document (e.g. `"Chapter 2 > Order Processing > Validation"`). |
| `chunk_size_chars` | yes | Character count of the chunk body (excluding front matter). |
| `primary_views` | yes | Non-empty list of views this chunk informs: `story`, `domain`, `architecture`, `ux`. |
| `tags` | yes | Nested object with one key per assigned view; each key holds hierarchical tags from the taxonomy. |
| `evidence_type` | yes | Content shape: `prose` (paragraphs), `table` (data tables), `list` (bullet/numbered lists), `diagram_description` (diagram annotations), `mixed` (combination). |

## Example: multi-view chunk (filled)

```yaml
---
chunk_id: requirements__chunk_03
source_file: markdown/Requirements.md
section_path: "Chapter 2 > Order Processing > Submit Order"
chunk_size_chars: 2140
primary_views: [story, domain]
tags:
  story:
    epic: Manage Orders
    sub_epic: Process Order
    story: Submit Order
    actor: user
    fidelity: outline
    path_type: spine
  domain:
    module: Order Management
    key_abstraction: Order
    term: Order Line
    stereotype: entity
evidence_type: prose
---

## Submit Order

When a customer completes the checkout form, the system creates a new Order with one
Order Line per item in the cart. Each Order Line records the product SKU, quantity, and
unit price at the time of order. The Order captures the shipping address, billing
address, and selected shipping method.

Before persisting the Order, the system validates that every line item has available
stock and that the total does not exceed the customer's credit limit. If validation
fails, the order is rejected with a specific error code per failing rule.

Upon successful creation, the system assigns an order number (sequential, prefixed with
the year) and transitions the order status to Pending. A confirmation email is sent to
the customer with the order summary and estimated delivery date.
```

## Example: single-view chunk (architecture)

```yaml
---
chunk_id: tech-overview__chunk_02
source_file: markdown/Tech-Overview.md
section_path: "Deployment > Container Platform"
chunk_size_chars: 1850
primary_views: [architecture]
tags:
  architecture:
    depth: outline
    platform: AWS ECS
    component: Container Platform
    provenance: ootb
evidence_type: prose
---

## Container Platform

The application runs on AWS ECS with Fargate launch type, eliminating the need for
EC2 instance management. Each service (Order, Product, Customer) runs as a separate
ECS service with its own task definition and auto-scaling policy.

Fargate tasks are configured with 0.5 vCPU and 1 GB memory for standard services.
The Order Service scales to 2 vCPU / 4 GB during peak hours based on a CloudWatch
alarm tied to request latency (p99 > 500ms triggers scale-out).

All services register with an Application Load Balancer that performs path-based
routing: `/api/orders/*` to Order Service, `/api/products/*` to Product Service,
and so on. Health checks run every 30 seconds against `/health` endpoints.
```

## Example: pass-through file (not chunked)

```yaml
---
chunk_id: glossary__passthrough
source_file: markdown/glossary.md
section_path: ""
chunk_size_chars: 920
primary_views: [domain]
tags:
  domain:
    module: Order Management
evidence_type: list
---

- **Order** — A customer's request to purchase one or more products.
- **Order Line** — A single product entry within an order, with quantity and price.
- **SKU** — Stock Keeping Unit; unique product identifier.
- **Backorder** — An order placed for a product currently out of stock.
```
