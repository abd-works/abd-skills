---
rule_id: classify-variants-before-modeling
phases: [step3]
order: 25
impact: HIGH
---

## Classify variant families before you model them

When the corpus presents a family of variants under one umbrella idea, decide whether the variants share **all** of the same mechanics end-to-end, or only **some** — with real differences in how specific parts work. That choice drives whether you use a type field (enum) on one concept or defer subtypes (inheritance) for a later pass.

- **All mechanics align** — same validation shape, same lifecycle rules, same fulfillment/resolution steps; only labels, codes, or cosmetic fields differ → treat as one concept with a **type property** (`EnumType` on the parent in `map-model-spec.json`).
- **Some mechanics align, others diverge** — e.g., a shared high-level lifecycle, but **different** validation rules, fulfillment paths, settlement steps, or resolution steps between variants → **inheritance / subtype** candidate → flag `[defer]` with the chunk that proves the variants exist. Do not invent parallel subtype concepts until the scaffold pass accepts them.

This is **not** “do they share *a* mechanic?” — many variants share *something* (same noun in the source). The question is whether they share **the full set** of behavioral mechanics; partial overlap with meaningful differences in named aspects is the signal for subtyping.

There is no scanner for this rule. It is enforced by reading chunks and by the Step 6 assessment (type-field-vs-subtype).

**Recurring pattern (not a corner case):**  
Models **constantly** confuse **two levels at once**: (1) sibling variants under an umbrella that are **true extensions** — different end-to-end pipelines — vs (2) **one** of those branches where variants **only** change which data or label the **same** pipeline reads. The first belongs in **subtyping / inheritance**; the second belongs in a **type property** on that branch only. Do not flatten both into a single enum on the umbrella concept.

(Classification only; serialize extensions vs enums however your pipeline defines.)

**DO** run this test whenever you see a list of named variants under one parent idea — when variants first appear in evidence **and** when you name or refine the parent concept in the scaffold. When not all mechanics align (subtype case), record deferral on the parent concept in the scaffold (same shape as any other concept — `owns` may start with `[defer]` until harmonize); deferral is a modeling choice, not only a discovery note.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Payments",
        "concepts": [
          {
            "name": "PaymentInstruction",
            "owns": "[defer] Split wire vs ACH vs RTP into subtypes after harmonize — see chunk chunk-pay-001",
            "owns_chunk": "chunk-pay-001",
            "chunk_ids": ["chunk-pay-001"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

**DO** use a single concept with an `EnumType` property on the **branch** where **all** mechanics match and only **which data** applies differs. Do not introduce parallel subtype concepts for that branch when the source describes one flow and only a kind flag or coded field changes inputs. Sibling branches that **do** differ in pipeline stay **extensions** of the umbrella — not extra enum literals on the homogeneous branch.

**Example (illustrative — one domain; names are not normative):** umbrella **A** with extensions **B**, **C**, **D** when mechanics diverge; **B** alone carries `EnumType` for variants that share **B**’s pipeline and only switch inputs.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Combat",
        "concepts": [
          {
            "name": "Attack",
            "owns": "Common attack notion; specialized by StandardAttack, PerceptionAttack, AreaEffectAttack where mechanics diverge",
            "owns_chunk": "chunk-attack-0",
            "chunk_ids": ["chunk-attack-0"]
          },
          {
            "name": "StandardAttack",
            "owns": "Owns hit resolution for ordinary attacks; melee vs ranged shares this pipeline and only selects which defense applies (e.g. parry vs dodge)",
            "owns_chunk": "chunk-attack-standard",
            "chunk_ids": ["chunk-attack-standard"],
            "properties": [
              {
                "definition": "EnumType attack_kind { melee, ranged }",
                "chunk": "chunk-attack-standard"
              }
            ]
          },
          {
            "name": "PerceptionAttack",
            "owns": "Owns resolution when the attack uses perception-based mechanics (differs from standard attack flow)",
            "owns_chunk": "chunk-attack-perception",
            "chunk_ids": ["chunk-attack-perception"]
          },
          {
            "name": "AreaEffectAttack",
            "owns": "Owns resolution for area templates / multiple targets (differs from standard single-target flow)",
            "owns_chunk": "chunk-attack-area",
            "chunk_ids": ["chunk-attack-area"]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

Model **inheritance / extends** from **Attack** to those three in whatever form your process uses; this rule is about **getting this two-level split right** — it is one of the most common modeling mistakes in the wild.

**DO NOT** put perception and area-effect on the same `EnumType` as melee/ranged on **StandardAttack** when mechanics differ — that collapses **extensions** (different pipelines) into **labels** (same pipeline).

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Ledger",
        "concepts": [
          {
            "name": "MoneyAmount",
            "owns": "Owns numeric amount with ISO currency code",
            "owns_chunk": "chunk-fx-01",
            "chunk_ids": ["chunk-fx-01"],
            "properties": [
              {
                "definition": "EnumType currency { USD, EUR, GBP }",
                "chunk": "chunk-fx-01"
              }
            ]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

**DO NOT** create both an enum and a parallel set of subtype concepts for the same family.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Payments",
        "concepts": [
          {
            "name": "PaymentInstruction",
            "chunk_ids": ["chunk-01"],
            "properties": [
              {
                "definition": "EnumType rail { wire, ach, rtp }",
                "chunk": "chunk-01"
              }
            ]
          },
          { "name": "WireTransfer", "chunk_ids": ["chunk-01"] },
          { "name": "ACHCredit", "chunk_ids": ["chunk-01"] },
          { "name": "RTPPayment", "chunk_ids": ["chunk-01"] }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

**DO NOT** model separate subtype concepts when one aggregate and a single coded field (`status`, channel code, etc.) matches the source.

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          { "name": "OrderStatusPending", "chunk_ids": ["chunk-ord-1"] },
          { "name": "OrderStatusPaid", "chunk_ids": ["chunk-ord-1"] },
          { "name": "OrderStatusShipped", "chunk_ids": ["chunk-ord-1"] },
          { "name": "OrderStatusCancelled", "chunk_ids": ["chunk-ord-1"] }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

Prefer one concept on the same module:

```json
{
  "modules_and_epics": [
    {
      "module": {
        "name": "Retail",
        "concepts": [
          {
            "name": "Order",
            "chunk_ids": ["chunk-ord-1"],
            "properties": [
              {
                "definition": "EnumType status { pending, paid, shipped, cancelled }",
                "chunk": "chunk-ord-1"
              }
            ]
          }
        ]
      },
      "epic": { "name": "Placeholder", "stories": [] }
    }
  ]
}
```

**DO NOT** model subtypes at Step 1 when the skill says to defer — keep a single parent row and `[defer]` in `owns` (see first **DO** example) instead of adding the deferred subtype concepts as full rows until harmonize approves.
