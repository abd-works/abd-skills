---
rule_id: foundation-coverage-before-deepen
phases: [step6]
order: 18
impact: HIGH
---

## Foundation coverage gate before Pass 2 (deepen)

After **Pass 1** (taxonomy / structure / dependency check on the JSON) and **before** pair ordering and **Pass 2 (deepen)**, verify that the **foundational spine** is **covered** by the planned deepen pairs.

**DO**

- List every concept that is still **`hypothesis`** (or missing `evidence_stage`) under a **`module.foundational: true`** module, plus any concept that **`depends_on`** marks as **provider** for others.
- Ensure each such concept appears in **at least one** deepen pair’s scope (module + epic subtree), or explicitly defer with `open_questions` and a reason. Prefer providers at **`scaffolded`** before you deepen dependents.
- Order pairs so **providers** (modules/concepts that others **`depends_on`**) are **deepened before** dependents when possible — same ordering principle as `module-depends-on.md`.

**DON'T**

- Start deepen on peripheral modules while a **core** foundational concept still has only `inferred` stage and no pair assigned.
- Treat Pass 1 as complete if **`depends_on`** is empty but cross-module concept names clearly overlap — reconcile or record dependencies first.
