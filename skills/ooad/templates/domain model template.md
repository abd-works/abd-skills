## Domain model -- {{project_or_slice_name}}

One file per workspace. All phases write into this file. **Never delete old `note:` lines -- each phase appends.**

---

## [{{AnchorName}} module]

note: {{AnchorName}} module -- {{one sentence: what this module owns}}
note: * -- see Note labels table and Example below

{{ClassName}} << {{kind}}? >>                         (stub added p3; ? = provisional; p4 confirms or demotes)
note: {{ClassName}} -- {{one sentence: why this class exists / what it owns}}
note: * -- see Note labels table and Example below

+ {{property}}:{{Type}}                              (added p6; opt + cardinality p7; Invariant p8)
+ {{method}}({{param}}:{{Type}}, ...): {{ReturnType}} (added p6; opt + cardinality p7; Invariant p8)

-----

---

## Note labels by phase

| Tag | Phase | Labels added |
|-----|-------|-------------|
| `[p0]` | domain-scan | `High Confidence Anchor`, `Sibling Candidate`, `Tension` |
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

## Example

*Only notes that fired are written -- not one per phase.*

## [Payment module]

note: Payment module -- owns all money movement and connector routing for a transaction
note: [p0] High Confidence Anchor -- every spec flow routes through this module; no other candidate owns settlement
note: [p9] Role Separation -- RoutingContext extracted; module boundary tightened around lifecycle not routing dimensions

Payment << Entity? >>                                         (stub p3; confirmed p4)
note: Payment -- owns lifecycle and state transitions for a single money movement attempt
note: [p0] High Confidence Anchor -- appears in every flow; all capture and settlement routes through it
note: [p3] Provisionally Classified -- Entity?; appears as named thing in every flow; identity suspected
note: [p4] Classified -- Entity; confirmed identity (payment id), lifecycle (state machine), owns behavior
note: [p8] Invariant -- SETTLED cannot return to AUTHORIZED; state machine is append-only past capture
note: [p14] State Candidate -- states: INITIATED, AUTHORIZED, CAPTURED, SETTLED, FAILED
+ id:UniqueID                                              (p5)
+ idempotencyKey:String                                    (p5)
+ state:PaymentState                                       (p5)
     opt  PaymentState [1..1]                              (p7)
+ authorize(connectorRef:ConnectorId): AuthResult          (p6)
     opt  ConnectorId [1..1], AuthResult [1..1]            (p7)
     Invariant: state must be METHOD_SELECTED before authorize  (p8)
-----

RoutingContext :
note: RoutingContext -- currency+region pair that selects a connector; immutable once set
note: [p5] Promoted -- was a loose property on Payment; recurred across three operations so extracted as VO
+ currency:Currency                                        (p5)
     opt  Currency [1..1]                                  (p7)
+ region:RegionCode                                        (p5)
     opt  RegionCode [1..1]                                (p7)
-----

---

## Patterns — subtype heading & invariant lines

Use this skill’s **Markdown companion** for structure the diagram must mirror.

### Subtype heading (inheritance visible in the doc)

When a specialization has a real superclass, make it explicit:

```markdown
### **WireTransfer** : **Payment**

note: WireTransfer -- country-specific wire settlement; extends Payment lifecycle
```

(For a root type with no parent, use a single class name and no `: Base` part — see **Payment** in **Example** above.)

### Invariant lines

Attach constraints **under** the property or operation they apply to — use the `Invariant:` line style already shown on **`authorize`** under **Payment** in **Example** above. Do **not** gather invariants in a separate section at module level.

```markdown
+ submit():Result
     Invariant: state must be READY before submit
```

