# Variant classification

**Goal:** Per family: **enum vs `extends`** **before** property churn. Default bias toward **`separate_concepts`** when evidence shows distinct behavioral contracts.

**Normative for Phase 7:** this document. [`process.md`](../process.md) is pipeline **summary** only (table row)—not the procedure.

## Steps

1. For each variant family, record the **decision**: enum vs subtypes vs other **before** bulk property assignment.

2. Align with **Explicit variant representation** in [`principles.md`](../library/principles.md) / plan principles table.

3. **Apply the LSP threshold for `separate_concepts` vs `enum`:**

   | Signal | Decision |
   |---|---|
   | Variants share **all** operations and state — only a label differs | `enum` on the parent concept |
   | Variants share **most** operations but **one or more** have unique state, operations, or lifecycle | `separate_concepts` with `extends` (Base:Extension naming) |
   | Variants have **no shared** operations — grouping is naming convenience only | `separate_concepts` as siblings (no inheritance) |
   | Insufficient evidence to distinguish | `defer` with trigger condition |

   **Bias:** When in doubt between `enum` and `separate_concepts`, prefer `separate_concepts`. It is cheaper to later collapse two concepts into an enum than to retroactively split an enum into concepts that needed distinct behavior all along. Record the specific behavioral difference that justifies `separate_concepts` in the `rationale` field of `variant_classification.json`.

4. **Cross-reference the promotion ledger:** If a candidate was decided as `extend` in the promotion ledger (see [domain-types.md](domain-types.md)), the variant classification **must** be `separate_concepts` — not `enum`. The ledger decision takes precedence.

## Exit

Written **variant decision** per family before bulk modeling. Each decision records:
- The variant family name
- The chosen representation (`enum`, `separate_concepts`, `defer`)
- LSP-grounded rationale (which behavioral differences justify the choice)
- Cross-reference to promotion ledger entries when applicable
