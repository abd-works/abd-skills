# Domain model Markdown

The **domain model** lives in workspace **`domain*.md`** files; **Draw.io** diagrams are **visual twins** of that content — update markdown first, then render or hand-sync the diagram (see **class-diagrams**, **using-diagram-cli**).

**Phase 1 — scan:** **`domain-scan-results.md`**, **`domain-scan-model.md`**, then **`domain-scan-model.drawio`**.

**Phase 2 — `domain-noun-verb.md`:** anchor sections, **Candidate …** lists, class boxes. Slice files are **domain content only** — no skill paths or process boilerplate in the artifact body.

**Phase 3 — raw candidates:** Prefer **`domain-raw-candidates.md`** — classes under anchors with notes. Optional single tabular roll-up (**`raw-candidate-list.md`** or appendix to **`domain-noun-verb.md`**) — **not** the same tables twice plus an integrated file.

**Templates:** **`templates/domain model template.md`**, **`templates/domain-raw-candidates-template.md`**.

---

## Domain concept template

Each concept is documented under a clear heading, for example:

```markdown
## **Payment**

**Responsibilities:** …

### Properties
- Money amount

### Operations
- initiate() → Authorization
```

From **Phase 6** onward (`add-properties-semantically-tight`), prefer **typed** members (see **Notation evolution**). Earlier phases stay informal (bullets and prose).

---

## Markdown and diagram

The Markdown spec and the class diagram are **two views of the same model** — keep them aligned when both exist (**class-diagrams**).

---

## **newly added** tag (optional)

In long-running examples, **newly added** on a line marks a property or operation that first appears in *this* file — useful for deltas across files.

---

## Notation evolution

| Phase range | Markdown style |
|-------------|----------------|
| **2–5** | Informal: bullets, candidates, responsibilities; typed `- <type> property` lines from **Phase 6** onward. |
| **Phase 6+** | Formal: `- <Type> propertyName`, `operationName(...) → ReturnType`. |

---

## Subtype sections

When you introduce substitutable specializations, add an explicit subtype heading so structure is visible in spec and diagrams:

```markdown
### **Subtype** : **PaymentMethod**
```

---

## Invariants

Attach invariants to the property or operation they constrain:

```markdown
**Invariant:** …
```

---

## Class diagram and spec

When you maintain **`map-model-spec.json`** or similar, re-run the project’s diagram script after material changes so Draw.io stays aligned.

- **Class diagrams** — templates, relationships, keeping `.md` and `.drawio` aligned.  
- **Using the Diagram CLI** — `scripts/drawio_cli.py`.

---

## Related library shards

| Topic | File |
|--------|------|
| Term tracking | [term-registry.md](term-registry.md) |
| Strategy-led runs | [strategy-led-generation.md](strategy-led-generation.md) |
| Layout | [class-diagram-layout-rules.md](class-diagram-layout-rules.md) |
