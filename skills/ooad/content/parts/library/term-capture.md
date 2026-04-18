# Term Capture

The full loop for identifying, recording, and refining terms across all phases — registry format, evidence extraction, and update protocol.

---

## What a Term Is

A **Term** is any concept identified from the source material that may become part of the domain model. At identification time it is not committed to a model role — it might become a class, a property, a value type, an association, or nothing. The registry tracks Terms as modeling phases determine what each one actually is.

**File:** `<workspace>/abd-ooad/term-registry.md`
---

## When to Capture

Capture term information whenever you:

- Encounter a new concept in source material
- Refine an existing term (rename, reclassify, change Target or Value)
- Promote a term (candidate → Class, Module, Property, etc.)
- Split a term into two or reject one entirely
---

## Extraction Steps

1. **Find the source passage** — the paragraph(s) that caused you to identify or change the term.
2. **Create an evidence block** — new file `<workspace>/abd-ooad/evidence/EVD-NNN.md` using `templates/evidence-block-template.md`.
   - Assign the next sequential ID (check `evidence/` for the highest current number).
   - Set `Terms:` to every term this passage supports — one passage often yields multiple terms.
   - Paste source text **verbatim** into the `evidence` code block.
   - Record locator precisely: 
      -- document: file, chapter, section, page
      -- code: code file, class , method,  line range.
3. **Update `term-registry.md`** — add or update the row; set `Evidence` column to the EVD ID(s).
   - Multiple blocks for one term: `EVD-001, EVD-003`
   - One block for multiple terms: same ID in each row

---

## Refinement Triggers

| Trigger | Action |
|---------|--------|
| First mention in source | New EVD block + new registry row |
| Passage refines understanding | New EVD block + update existing row |
| Term promoted to modelled | New EVD block at promotion phase, specify target |
| Term split into two | New EVD block for each |
| Term rejected | Keep EVD block; note rejection in it — never delete IDs |

---

## Registry Columns

Use `templates/terms-template.md` for the file format.

| Column | Role |
|--------|------|
| **Term** | Concept name from source — exact word or phrase as found; rename in `refine-names` if needed. |
| **Phase** | Short phase-id when first captured (e.g. `domain-scan`, `nouns-verbs-rules-and-states`). |
| **Target** | One or more of: `Module` \| `Class` \| `Property` \| `Operation` \| `Example` — always in that order. Use `<br>` to stack multiple. Blank = not yet modelled. |
| **Value** | Dot notation per target in same order as Target, stacked with `<br>`: `Module` for Module, `Module.Class << Stereotype >>` for Class, `Module.Class.property` for Property, `Module.Class.operation` for Operation, `Module.Class.example` for Example. Stereotype inline after Class value with spaces: `<< Anchor >>`. Blank if not yet modelled. |
| **Evidence** | EVD ID(s) pointing to `evidence/EVD-NNN.md`. Use `<br>` to stack multiple. |
| **Notes** | Labelled analysis entries. Use standard labels (see Notes Labels below) so any phase can find and filter term analysis. When the raw quote lives in an evidence block, write: *"see EVD-NNN"* and keep your analysis here. |

---

## Notes Labels

**Every piece of data that can be associated with a term goes in the term registry — not in a separate document.** Use labels in the Notes column to make entries filterable and consistent across phases.

| Label | Format | Phase(s) |
|-------|--------|----------|
| `Tension` | `Tension - **{{TensionName}}** {{what_is_ambiguous_or_conflicting}}` | domain-scan, any |
| `High Confidence Anchor` | `High Confidence Anchor - {{why_this_module_or_class_is_central}}` | domain-scan, any |
| `Sibling Candidate` | `Sibling Candidate - {{anchor_term}} {{why_related}}` | domain-scan, nouns-verbs-rules-and-states |
| `Provisionally Classified` | `Provisionally Classified - {{kind}}? {{reason}}` — kind is one of `Entity`, `ValueObject`, `Enum`, `Policy`, `Role`, `Event`, `Process`, `Property`, `Operation` | raw-candidates |
| `Classified` | `Classified - {{kind}} {{reason}}` — kind is one of `Entity`, `ValueObject`, `Enum`, `Policy`, `Role`, `Event`, `Process`, `Property`, `Operation` | thing-vs-data-about-a-thing, responsibilities-and-collaborators, properties-and-operations |
| `Anchor Boundary` | `Anchor Boundary - {{challenge_or_support}} {{evidence_summary}}` | nouns-verbs-rules-and-states |
| `Responsibility` | `Responsibility - {{one_sentence_what_this_class_is_responsible_for}}` | responsibilities-and-collaborators |
| `Collaborator` | `Collaborator - {{comma_separated_class_names_this_class_depends_on}}` | responsibilities-and-collaborators |
| `Invariant` | `Invariant - {{rule_that_must_always_hold}}` | invariants-in-the-model, model-state-transitions, any |
| `State Candidate` | `State Candidate - states: {{list}} illegal transitions: {{list}}` | model-state-transitions |
| `Bloat Signal` | `Bloat Signal - {{what_clusters_are_mixed}} suggest: {{extract}}` | watch-for-bloated-classes |
| `Role Separation` | `Role Separation - {{merged_role}} splits into: {{role_a}}, {{role_b}}` | smashed-abstractions-and-hidden-roles |
| `Cohesion Group` | `Cohesion Group - {{group_name}} changes with: {{related_terms}}` | design-bounded-contexts |
| `Scenario Gap` | `Scenario Gap - {{scenario}} exposes: {{missing_responsibility_or_operation}}` | validate-with-scenarios |
| `Promoted` | `Promoted - {{from_target}} → {{to_target}} {{reason}}` — e.g. Property → Class when a property warrants its own type | properties-and-operations, refine-names, any |
| `Rejected` | `Rejected - {{why_not_modelled}}` | any |
| `Renamed` | `Renamed - {{old_name}} → {{new_name}} {{reason}}` | refine-names |
| `Split` | `Split - into {{term_a}}, {{term_b}} {{reason}}` | any |
| `Merged` | `Merged - with {{other_term}} {{reason}}` | any |
| `Follow-up` | `Follow-up - {{question_or_action}}` | any |

Labels are free-text after the colon — use plain sentences. Multiple labels in one Notes cell are separated by `<br>`. Later phases **must** use this same convention when adding to existing rows.

---

## Targets

A single term may be modelled in many ways, captured as modelling "targets" in terms registry. Each term may als have more than one evidence passages that supports it. A single term can be both a Module and a Class; it will often be a class and property in another CLlass it can be grounded in multiple separate source passages. See `templates/terms-template.md` for format and worked examples.

---


## Phase IDs

Refer to pipeline steps only by **phase-id** — the short kebab-case slug matching `skill-config.json → phase_files` (e.g. `domain-scan`, `nouns-verbs-rules-and-states`, `refine-names`). Do not use "Phase 1 / Phase 2" as names; those ordinals drift.

---

## Evidence File Naming

```
evidence/
  EVD-001.md
  EVD-002.md
  ...
```

Pad to three digits. Never reuse or delete an ID — rejected terms keep their evidence as audit trail.

Template: `templates/evidence-block-template.md`

---

---

## References

- `templates/terms-template.md` — registry file format
- `templates/evidence-block-template.md` — evidence block format
