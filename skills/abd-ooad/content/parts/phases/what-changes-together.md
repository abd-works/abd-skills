# What changes together — payments example

**Skill:** abd-ooad — **Step 17:** **cohesion** and **bounded context** hints.

**Upstream:** `tension-as-a-signal.md`.

> **Continual refinement:** Aligns with **abd-maps-models-specs** [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md) (*Domain concept* template, *Continual refinement — class definition + diagram*). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Clusters

| Cluster | Changes when | Stable boundary hint |
|---------|--------------|----------------------|
| **Payment** | PSP outcome, settlement, refunds | **Payments BC** — core aggregate. |
| **Order / cart** | Line items, locks | **Checkout / order BC** — **refs** Payment by id. |
| **Catalog / price** | SKUs, regional rules | **Catalog BC** — **not** embedded in Payment row. |
| **Compliance** | Sanctions list, country rules | **Policy** service — **updates** independent of Payment schema. |
| **Warehouse** | Pick, ship | **Fulfillment BC** — reacts to **payment.settled** / order events. |

**Payment** should **not** own **SKU** or **inventory** — **correlation ids** only.

---

## Carry forward → Step 18

**Validate** with **scenarios** — happy path, sanctions, partial capture, idempotency replay.

---

## Continual refinement (this step)

- **Delta:** **cohesion clusters** — **Payment** vs **Order** vs **Catalog** vs **Compliance** vs **Warehouse**; use to sanity-check **module** boundaries and **depends_on** in **`map-model-spec.json`**.

---

## Action Checklist

- [ ] Have you identified distinct cohesion clusters (groups of classes that change together)?
- [ ] Have you confirmed that each cluster maps to a clear bounded context or module boundary?
- [ ] Have you verified that no cluster has cross-cutting dependencies that violate the module boundary?
- [ ] Have you updated `map-model-spec.json` `depends_on` entries to reflect cohesion findings?
- [ ] Have you noted carry-forward items to Step 18 (validate with scenarios)?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
