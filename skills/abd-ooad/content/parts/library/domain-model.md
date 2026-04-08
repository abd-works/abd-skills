# Domain model Markdown

This skill’s **domain model** is captured in Markdown  a parallel **Draw.io** class diagram. Use **`templates/domain model template.md`** for companion docs; align with **`templates/domain model template.drawio`** when both exist.

**Phase 2 — `domain-noun-verb.md`:** anchor sections, **Candidate …** lists, full or pared class boxes. Slice files are **content only** — no skill paths or process meta in the artifact body.

**Phase 3 — bucket roll-up:** sort candidates into **entities**, **value objects**, **processes**, **policies**, **roles**, **events** (tables in **`raw-candidate-list.md`** or appended to **`domain-noun-verb.md`**). Same **content-only** rule: no skill/process boilerplate in slice files.

**Optional — `domain-raw-candidates.md`:** same Phase 3 content as **classes under anchor modules** (`### Name : << Entity >>` / `<< ValueObject >>` / `<< Process >>` / …), notes below — **not** a second copy of bucket tables. Cross-cutting material → **`## Cross-anchor`** or appendix. **`templates/domain-raw-candidates-template.md`**.

---

## Domain concept template

Each **domain concept** (class, interface, value object, or aggregate) is documented under a clear heading, for example:

```markdown
## **Payment**

**Responsibilities:** …

### Properties
- Money amount
- …

### Operations
- initiate() → Authorization
```

From **Step 5** onward, prefer **typed** members (see **Notation evolution** below). Earlier steps stay **pre-notation** (bullets and prose).

---

## Continual refinement — class definition + diagram

**Continual refinement** means you **grow** the model across steps: each step file may add or tighten concepts. The Markdown spec and the class diagram are **two views of the same model** — update both when your project uses dual artifacts so they do not drift (see **[Class diagrams](class-diagrams.md)**).

---

## **newly added** tag

In the **worked example** threads (e.g. payments), the marker **newly added** (bold tag on a line) means: this **property** or **operation** line appears for the **first time** in *this* step’s file. Use it to see the **delta** from the previous step.

---

## Notation evolution

| Phase | Markdown style |
|--------|------------------|
| **Steps 1–4** | Informal: bullets, short phrases, responsibilities, candidate names; typed `- <type> property` lines arrive in Step 5. |
| **Step 5+** | Formal typed members: `- <Type> propertyName`, `operationName(...) → ReturnType`. |

---

## Subtype sections

When you introduce substitutable specializations, add an explicit subtype heading so the structure is visible in the spec and in diagrams:

```markdown
### **Subtype** : **PaymentMethod**
```

Put **`**newly added**`** on subtype **operation** (or property) lines when that member is **first** introduced for that subtype.

---

## Invariants

Attach invariants to the **property** or **operation** they constrain, using a dedicated line:

```markdown
**Invariant:** …
```

Mark **`**newly added**`** when you **first** attach an invariant to a given member line.

---

## Early steps: terms, mechanisms, story map

Before typed properties exist, align extracted **nouns, verbs, rules, states** with your workspace’s **terms & mechanisms** and **shaped story map** (or equivalent). That is the same “grow the model as you go” idea: informal extraction first, then formal types.

---

## Class diagram and spec (visual twin)

When you maintain a machine-readable spec such as **`map-model-spec.json`**, re-run your project’s class-diagram render script (for example **`render_map_model_class_diagram.py`**) after material changes so the **Draw.io** diagram stays the **visual twin** of the spec.

- **[Class diagrams](class-diagrams.md)** — templates, relationship types, keeping `.md` and `.drawio` aligned.  
- **[Using the Diagram CLI](using-diagram-cli.md)** — building diagrams with **`scripts/drawio_cli.py`**.

---

## Related library shards

| Topic | File |
|--------|------|
| Term tracking across steps | [term-registry.md](term-registry.md) |
| Strategy-led runs | [strategy-led-generation.md](strategy-led-generation.md) |
| Layout and lanes | [class-diagram-layout-rules.md](class-diagram-layout-rules.md) |
