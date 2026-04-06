# Term Registry

## What a Term Is

A **Term** is any concept identified from the source material that may become part of the domain model. At the time of identification, a Term is not committed to a model role — it might become a class, a property, a value type, an association, or nothing at all. The registry tracks Terms as the modeling phases determine what each one actually is.

This is distinct from other uses of "actor" in this domain:
- In MM3E and FoundryVTT, "Actor" has a specific system meaning (a character, creature, or entity in the game world).
- In the registry, everything is a Term until the model says otherwise.

**File:** `<workspace>/abd-ooad/term-registry.md`
**Never embedded** inside step outputs — it lives in its own file and is referenced from each step's model doc.

---

## Step Reference — Short Names

Use these short names in the **Step** column of the registry when adding or updating a row.

| Short Name | Phase | Description |
|-----------|-------|-------------|
| SETUP | workspace-and-config | Workspace initialization |
| SCAN | domain-scan | Source scan and anchor identification |
| NOUNS | nouns-verbs-rules-and-states | Extract nouns, verbs, rules, states |
| CANDS | raw-candidate-list | Raw candidate class list |
| THINGS | thing-vs-data-about-a-thing | Separate things from data-about-things |
| RESP | responsibilities-before-operations | Assign responsibilities |
| PROPS | add-properties-semantically-tight | Add semantically tight properties |
| OPS | turn-verbs-into-operations | Turn verbs into operations |
| RELS | relationships-and-cardinality | Relationships and cardinality |
| INV | invariants-in-the-model | Identify invariants |
| BLOAT | watch-for-bloated-classes | Detect bloated classes |
| ROLES | smashed-abstractions-and-hidden-roles | Uncover hidden roles |
| INHERIT | inheritance-when-behavior-generalizes | Apply inheritance |
| ABST | abstract-classes-and-interfaces | Abstract classes and interfaces |
| COMP | prefer-composition | Prefer composition over inheritance |
| STATES | model-state-transitions | Model state transitions |
| ITER | iterative-refinement | Iterative refinement pass |
| TENSION | tension-as-a-signal | Resolve tensions |
| COHESION | what-changes-together | What changes together |
| VALIDATE | validate-with-scenarios | Validate with scenarios |
| NAMES | refine-names | Refine class and concept names |
| LAYERS | model-in-layers | Model in layers |

---

## Registry Columns

| Column | Values | Notes |
|--------|--------|-------|
| **Term** | Concept name from the source | Exact word or phrase as found — rename in the NAMES step if needed |
| **Classification** | anchor / candidate / tension / module | Lifecycle stage. Maps to UML stereotype in diagram once promoted to class |
| **Step** | Short name from table above (SCAN, NOUNS, …) | Step that first identified this Term |
| **Confidence** | High / Medium / Low | How sure we are this belongs in the model |
| **Status** | Active / Ambiguous / Deferred / Rejected / Promoted | Current state |
| **Notes** | Free text | Why it was flagged, what needs investigating, decisions made |
| **Module?** | Yes / No / Investigate | Will this eventually become a standalone module |

**Classification values** (once a Term is confirmed as a class, this maps to its UML `<<stereotype>>` in the diagram):

- `anchor` — High-confidence, core, stable. Identified at SCAN. Will definitely be in the model.
- `candidate` — Plausible, needs validation. Added during extraction steps.
- `tension` — Boundary ambiguous or conflicting. Needs resolution before model role can be assigned.
- `module` — Ready to be promoted to a standalone module.

---

## Registry Format

```markdown
# Term Registry — {{project_name}}

_Last updated: {{step_short_name}} — {{date}}_

| Term       | Classification | Step  | Confidence | Status    | Notes | Module? |
|------------|---------------|-------|------------|-----------|-------|---------|
| Character  | anchor        | SCAN  | High       | Active    | Central entity; all rules attach to it | Yes |
| Power      | anchor        | SCAN  | High       | Active    | Core superheroic capability unit | Yes |
| Condition  | anchor        | SCAN  | High       | Active    | Named state applied after check resolution | Yes |
| Device     | tension       | SCAN  | Medium     | Ambiguous | Removable Power or Equipment? Boundary unclear | Investigate |
| ability    | candidate     | NOUNS | High       | Active    | One of six core scores; probably a property of Character, not a class | No |
```
