---
scanner: plan-shape
---

# Rule: Cross-run upstream parallelism — PO/BE do not wait for prior-run engineering

When an engagement spans **multiple runs** (Increments 1–N), restarting or resuming while a run is still in **engineering** must not leave **upstream roles idle** waiting for that engineering cycle to finish.

## DO

- Wire **`depends_on`** on **Run N+1** first slots so they open after **Run N specification stage exit** (last specification reviewer slot for that run), **not** after Run N engineering completes.
- In the plan, state **`Chain: → Run N+1 slot XX`** as the first slot of the next run that opens **in parallel** with prior-run engineering when spec is done.
- On **resume** (checklist shows active work in engineering): ensure **Run N+1 exploration and specification** `slot-NN-start.md` files exist; run **`sync_kanban_board.py`** so Run N+1 ticket appears in **`backlog`** or **`in_progress`** when pullable.
- Align with **Kanban**: one run = one ticket = one column; stage flow **in_progress → review → done** ([`../../../content/kanban.md`](../../../content/kanban.md)). Pull from **`backlog`** → first claim sets **`in_progress`** (no Ready column).
- Keep **within-run** ordering strict: exploration → specification → engineering inside each run; `depends_on` chains pairs inside the run as today.
- Let **engineer / ux-designer** on the prior run continue slots 115–118 (or equivalent) while PO/BE work Run N+1 exploration — no cross-run block on downstream roles finishing first.

## DO NOT

- Set Run N+1 first exploration slot `depends_on` to the **last engineering reviewer** of Run N (e.g. slot 118) when Run N specification already passed — that forces PO/BE to idle during engineering.
- Author only the **current run's remaining engineering** slot starts on resume and omit next-run exploration/spec starts — upstream roles will report "no pending work" incorrectly.
- Treat **`<!-- resume: slot NN next -->`** as "only this run may proceed" — upstream roles claim **any** eligible slot for their role, including the **next run** when `depends_on` allows.

## Example (wrong)

Run 5 engineering active (slots 115–118). Run 6 slot 119 (BE exploration) has:

```yaml
depends_on:
  - "118"   # Run 5 engineering reviewer — PO/BE idle until GREEN done
```

No `slot-119-start.md` on disk — BE reports no work while engineer works 115.

## Example (correct)

Run 5 specification exit = slot 110 (reviewer). Run 6 slot 119:

```yaml
run: "Run 6 — Increment 5: Pay your way"
stage: exploration
depends_on:
  - "110"   # Run 5 spec exit — parallel to Run 5 engineering 111–118
```

Delivery lead authors slots 119–136 when resuming at slot 115. BE claims 119; engineer claims 115 — both in flight.
