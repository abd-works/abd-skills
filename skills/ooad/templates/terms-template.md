<!--
  Term Registry — source of truth for all term data in this project.
  One row per term. Copy to: <workspace>/abd-ooad/term-registry.md

  Evidence lives in <workspace>/abd-ooad/evidence/EVD-NNN.md — one file per source passage.
  A single evidence block can support multiple terms; cite the same ID in each row.
  Template for evidence blocks: templates/evidence-block-template.md

  Columns:
    Term        — name as it appears in source material
    Phase       — short phase-id when term was first captured (e.g. domain-scan, nouns-verbs, raw-candidates)
    Target      — one or more of: Module | Class | Property | Operation | Example — always in that order
                  use <br> to stack multiple (e.g. Module<br>Class)
                  blank = not yet modelled
    Value       — dot notation per target, stacked with <br> in same order as Target:
                    Module    -> Module
                    Class     -> Module.Class << Stereotype >>  (stereotype inline, with spaces)
                    Property  -> Module.Class.property
                    Operation -> Module.Class.operation
                    Example   -> Module.Class.example
                  blank if not yet modelled
    Evidence    — one or more EVD-NNN IDs pointing to files in evidence/
                  use <br> to stack multiple
    Notes       — classification reasoning, anchor tests, tensions, follow-ups, and analysis
                  when raw quote is in an evidence block write: "Verbatim source in EVD-NNN"

  Status column removed — if Target is blank the term is unmodelled; if filled it is modelled.
  Module column removed — module is encoded in Value via dot notation.
-->

# Term Registry — {{project_name}}

| Term | Phase | Target | Value | Evidence | Notes |
|------|-------|--------|-------|----------|-------|
| {{Term}} | {{phase-id}} | {{Module<br>Class}} | {{Module<br>Module.Class << Stereotype >>}} | {{EVD-NNN}} | {{reasoning / tensions / follow-ups}} |

---

<!--
Examples:

| Term            | Phase       | Target             | Value                                                    | Evidence           | Notes |
|-----------------|-------------|--------------------|----------------------------------------------------------|--------------------|-------|
| Character       | domain-scan | Module<br>Class    | character<br>character.Character << Anchor >>             | EVD-001            | Central anchor; everything flows through it |
| Check           | domain-scan | Module<br>Class    | resolution<br>resolution.Check << Abstract >>             | EVD-004            | Abstract — multiple subtypes suspected |
| Rank            | domain-scan | Property           | traits.Trait.rank                                        | EVD-002            | |
| Ability         | domain-scan | Class              | traits.Ability << Entity >>                              | EVD-002            | |
| DifficultyClass | domain-scan | Class              | resolution.DifficultyClass << Value Object >>            | EVD-004            | Immutable once set |
| applyDamage     | nouns-verbs | Operation          | resolution.Check.applyDamage                             | EVD-004<br>EVD-005 | Verbatim source in EVD-004 |
| critSuccess     | nouns-verbs | Example            | resolution.Degree.critSuccess                            | EVD-005            | |
| PowerLevel      | domain-scan | Property           | character.Character.powerLevel                           | EVD-001            | |
| combat          | domain-scan |                    |                                                          | EVD-006            | Not yet modelled — tension between module and process |

Corresponding evidence files in evidence/:

EVD-001.md  — Heroes Handbook Ch.1 p.3  → terms: Character, PowerLevel
EVD-002.md  — Heroes Handbook Ch.2 p.8  → terms: Rank, Ability
EVD-004.md  — Heroes Handbook Ch.4 p.22 → terms: Check, DifficultyClass, applyDamage
EVD-005.md  — Heroes Handbook Ch.4 p.24 → terms: critSuccess, applyDamage
EVD-006.md  — Heroes Handbook Ch.5 p.31 → terms: combat
-->
