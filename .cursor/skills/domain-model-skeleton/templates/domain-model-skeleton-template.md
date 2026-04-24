## Domain model skeleton -- {{project_or_slice_name}}

Output file: **`domain-model-skeleton.md`** in the engagement `abd-ooad/` folder. Later skills may append to the same file. **Never delete old `note:` lines — each pass appends.**

**Stereotypes:** In this file, use **`<<Anchor>>` only** on each module’s core class. Do **not** use `<<Entity>>`, `<<Aggregate>>`, `<<Value Object>>`, `<<Abstract>>`, etc. here — those belong in later skills. Supporting classes are plain names + `note:`.

**Section titles:** Use `## [{{AnchorName}}]` only — **not** `## [{{AnchorName}} module]`. The word *module* describes the grouping in documentation; it is not part of the heading (e.g. `## [Series]`, not `## [Series module]`).

---

## [{{AnchorName}}]

note: [dms] {{AnchorName}} -- {{one sentence: what this anchor slice owns}}

{{CoreClassName}} : <<Anchor>>
note: [dms] {{why this is the module’s core / anchor}}

SupportingClassName
note: [dms] {{one sentence; no <<…>> stereotypes in this file except Anchor on the line above}}

AnotherClass
note: [dms] …

+ {{property}}:{{Type}}                              (optional — only if the scan already names it; no class stereotypes)
+ {{method}}({{param}}:{{Type}}, ...): {{ReturnType}} (optional — same)

-----

---

## Note labels (skill tag first)

| Tag | Skill | Labels added (typical for that note) |
|-----|-------|-------------------------------------|
| `[dms]` | **domain-model-skeleton** (`domain-model-skeleton.md`) | `High Confidence Anchor`, `Sibling Candidate`, `Tension` — same registry vocabulary as scan fidelity |
| `[p1]` | nouns-verbs-rules-and-states | `Anchor Boundary`, `Sibling Candidate`, `Tension`, `Follow-up` |
| `[p3]` | raw-candidates | `Provisionally Classified`, `Tension`, `Follow-up` |
| `[p4]` | thing-vs-data-about-a-thing | `Classified`, `Renamed`, `Tension`, `Follow-up` |
| `[p5]` | responsibilities-and-collaborators | `Classified`, `Tension`, `Follow-up` |
| `[p6]` | properties-and-operations | `Classified`, `Promoted`, `Tension`, `Follow-up` |
| `[p7]` | relationships-and-cardinality | `Classified`, `Tension`, `Follow-up` |
| `[p8]` | invariants-in-the-model | `Invariant`, `Tension`, `Follow-up` |
| `[p9]` | watch-for-bloated-classes | `Bloat Signal`, `Role Separation`, `Follow-up` |
| `[p10]` | smashed-abstractions-and-hidden-roles | `Role Separation`, `Classified`, `Tension`, `Follow-up` |
| `[p11]` | inheritance-when-behavior-generalizes | `Classified`, `Promoted`, `Tension`, `Follow-up` |
| `[p12]` | abstract-classes-and-interfaces | `Classified`, `Promoted`, `Tension`, `Follow-up` |
| `[p13]` | prefer-composition | `Classified`, `Tension`, `Follow-up` |
| `[p14]` | model-state-transitions | `State Candidate`, `Invariant`, `Tension`, `Follow-up` |
| `[p15]` | iterative-refinement | `Renamed`, `Classified`, `Tension`, `Follow-up` |
| `[p16]` | tension-as-a-signal | `Tension`, `Renamed`, `Follow-up` |
| `[p17]` | design-bounded-contexts | `Cohesion Group`, `Bounded Context`, `Tension`, `Follow-up` |
| `[p18]` | validate-with-scenarios | `Scenario Gap`, `Invariant`, `Follow-up` |
| `[p19]` | refine-names | `Renamed`, `Promoted`, `Follow-up` |

---

## Example (skeleton fidelity)

*Only `<<Anchor>>` on the core class; supporting lines have no `<<…>>` stereotypes.*

## [Payment]

note: [dms] Payment -- owns all money movement and connector routing for a transaction

Payment : <<Anchor>>
note: [dms] High Confidence Anchor -- every flow routes through settlement here

RoutingContext
note: [dms] Sibling Candidate -- currency+region pair; Entity vs value object decided in a later phase

+ id:UniqueID
+ state:PaymentState

-----

*For a **full** integrated domain model with `<<Entity>>`, invariants, and later tags (`[p3]`…`[p19]`), use the workspace’s **domain model** template after skeleton + extraction — not this skeleton-only file.*

---

## Patterns — subtype heading & invariant lines (optional at skeleton fidelity)

At scan / skeleton fidelity, **`domain-model-skeleton.md`** is the structure for **modules, one `<<Anchor>>` per module, and plain supporting class names** — before deeper phases extend the file or the same path with full tags.

### Subtype heading (inheritance visible in the doc)

When the source already names a superclass, you *may* sketch it — still **no** `<<Entity>>` / `<<Abstract>>` here; only the core module class uses `<<Anchor>>`:

```markdown
### **WireTransfer** : **Payment**

note: [dms] WireTransfer -- country-specific wire settlement; extends Payment lifecycle
```

(For a root type with no parent, use a single class name and no `: Base` part — see **Payment** in **Example** above.)

### Invariant lines

Full `Invariant:` sublines on members belong in **later** passes (see integrated **domain model** template). At skeleton fidelity, capture strong rules in **`[dms]` notes** if needed; do not require full `Invariant:` formatting to ship the skeleton.
