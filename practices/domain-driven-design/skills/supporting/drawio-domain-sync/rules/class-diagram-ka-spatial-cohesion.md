# Rule: Key Abstraction spatial cohesion

**Scanner:** `class-diagram-run-audit-after-every-render`

A passing diagram clusters classes that belong to the same Key Abstraction close together, with visible spatial separation between different Key Abstractions on the same page. A failing diagram scatters related classes across the canvas or jams unrelated Key Abstractions together so readers cannot see where one concept boundary ends and another begins.

## When this applies

- A diagram page contains classes from more than one Key Abstraction (e.g. when cross-KA relationships are shown on the same page for context).
- A single Key Abstraction has many classes that could drift apart during manual layout or incremental edits.

## DO

Position classes within the same Key Abstraction as a tight cluster — close enough that their relationship edges are short and direct. Place different Key Abstractions with clear spatial distance between clusters so the eye immediately reads them as separate groups.

**Example:** In `domain-model-class-diagram-entitlements.drawio`, the Payment cluster (Payment, PaymentStatus, Transaction, Settlement, EffectiveDate, ReferenceNumber, FromAccount, Currency) occupies the upper-left region. The Entitlement cluster (FinanceUser, UserProfile, Entitlement, Service, Activity) occupies the centre-right. The Organization cluster (EnterpriseGroup, RelatedCompany) sits below. Each group is visually cohesive, and the gap between groups communicates the boundary.

Layout principles:
- **Within a KA:** Classes that compose or reference each other are adjacent. Parent→child edges are short. The group reads as a unit.
- **Between KAs:** A visible gap (≥200px or more) separates clusters. Cross-KA edges are longer, reinforcing that the connection crosses a boundary.
- **Instance notes near their class:** Coloured instance notes sit beside the class they describe, inside the KA cluster — not floating in the gap between KAs.

## DO NOT

Interleave classes from different Key Abstractions without spatial separation:

```
Payment  UserProfile  Transaction  Entitlement  Settlement  Activity
```

When classes from different KAs are mixed in a flat row or scattered randomly, the diagram fails to communicate which concepts belong together and which relationships cross abstraction boundaries. The reader must trace every edge to understand structure rather than seeing it at a glance.

## Guidance

- On multi-KA pages, mentally draw a bounding box around each KA's classes. If the boxes overlap, reposition until they separate.
- Cross-KA edges (e.g. Payment → FinanceUser) naturally become longer; this is correct — the visual length communicates that the relationship spans a boundary.
- When a page has only one KA, cohesion is satisfied by default — just avoid scattering classes unnecessarily far apart.

**Source:** Engagement convention (drawio-domain-sync skill) — Key Abstraction layout pattern from entitlements diagram.
