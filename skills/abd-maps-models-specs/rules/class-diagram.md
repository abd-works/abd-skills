---
rule_id: class-diagram
---

## Class diagram: readable layout and edges

**Artifacts:** Emitted **`map-model-class-diagram.drawio`** next to **`map-model-spec.json`** (under workspace `output_dir`, usually `spec/`). Optionally **`class-diagram-layout-plan.json`** in the same folder supplies **logical** clusters and order (no coordinates); the emitter maps that to placement, then scanners run on the `.drawio` as today. Authoring guidance for **manual** layout in Draw.io matches this rule; the pipeline emitter should follow the same conventions when a layout plan is present.

This rule is **partly machine-checked** by `scripts/scanners/class_diagram_layout.py` when the Draw.io file exists: **fails** on duplicate directed edges between the same class pair or overlapping class rectangles; **warns** on self-loops, very high per-class edge count, or extreme edge density (heuristics — not full aesthetic judgment). See also [`class-diagram-from-spec.md`](../content/parts/library/class-diagram-from-spec.md).

**Illustrative examples (open in Draw.io):** at the skill root, **`examples/class-diagram-good.drawio`** (readable flow) and **`examples/class-diagram-bad.drawio`** (intentionally crowded: duplicate edges, self-loop, all-to-all). Paths are sibling to **`rules/`** — `examples/…`.

**Intent:** A class diagram should be **readable** along a **primary direction** (left→right and/or top→bottom). **Anchor** the canvas on **entry / scope** concepts; walk **abstract → concrete** and **core aggregates → parts** — do **not** lead with peripheral concepts. **Inheritance** may use angled connectors; **associations** should prefer **orthogonal** segments (horizontal/vertical with 90° corners). Avoid **overlapping** class boxes, **duplicate** connectors between the same pair, **self-loops** except when the model truly requires recursive structure (justify in spec). Prefer **multiple pages** or **swimlanes** over a single dense canvas.

**DO**

- Lay out classes so a reviewer can **follow the story** (e.g. user/session → space → memory → retrieval) in **lanes** or **rows**, not a uniform grid of unrelated neighbors.
- Route **association** edges with **orthogonal** style where the tool allows; keep **crossing** and **bundle** count low — rearrange nodes before accepting spaghetti.
- Split **very large** models across **pages** or **diagrams** rather than shrinking everything into one unreadable sheet.
- After automated render, **adjust** positions and edge waypoints in Draw.io when the scanner or review flags density or overlap.

**DON'T**

- Place **every** class on a **fixed grid** with **default edge routing** only — produces edge soup (see bad example).
- Add **duplicate** directed edges between the same two classes for the same relationship.
- Use **self-edges** on ordinary aggregates without a modeled recursive need.
- Allow **overlapping** class rectangles or **extreme** fan-in/fan-out on a single class without refactoring the diagram or the model.

```text
Good:  DomainRoot → Aggregate → Part   (primary row)
       Aggregate → SideConcept         (branch downward)

Bad:   N×M grid + all-pairs edges + duplicate A→B + self-loop on a random hot class
```
