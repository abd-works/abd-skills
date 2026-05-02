<!--
  Normative shape for the growing module file after domain-language enrichment.

  Default output: <workspace>/abd-domain-driven-design/modules/<module-name>.md
  Copy-output snapshot (when the user says "copy output"):
    <workspace>/abd-domain-driven-design/modules/<module-name>-domain-language.md

  If the module file already exists, enrich it in place.
  If it does not exist, create it with this structure.

  The file grows additively across phases:
    UL    → creates # Core Domain / ### Term / #### Domain Language / #### References
    KA    → inserts ## Key Abstraction grouping + prose description; adds #### Decisions made; adds source blocks
    DS    → adds #### Domain Sketch under each ### Term; deduplicates references
-->

---
state: domain-language
---

# Module: [{{ModuleName}}]

Scope: {{bounded slice or engagement scope}}

**Core terms**:
- {{term1}}
- {{term2}}
- …

---

# Core Domain

<!--
  One ### heading per Core term, in partition order.
  Every Core term must appear — none may be silently dropped.
  Each term carries:
    - #### Domain Language   short prose bullets (behavior, interactions, rules, flows)
    - #### References            full Ref entries tracing every behavioral claim to source
-->

### {{term_name}}

#### Domain Language

- {{short line: behavior, interaction, rule, or flow}}
- {{…}}

#### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{line_range or section pointer}}
Extract: {{whole or partial}}

---

### {{next_term_name}}

#### Domain Language

- {{…}}

#### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{line_range}}
Extract: {{whole or partial}}

---

# Boundary Domain

<!--
  Concepts this module depends on but does not own.
  Each gets a ## heading, an Owned by: field, and the same #### sections as core terms.
  No KA grouping — boundary terms sit directly under # Boundary Domain.
-->

## {{boundary_term_name}}

Owned by: {{owning_module_name}}

#### Domain Language

- {{short line: how this module depends on the concept}}
- {{…}}

#### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{line_range}}
Extract: {{whole or partial}}

---

<!-- EXAMPLE — delete this section after using the template. -->

## Example (filled)

```markdown
---
state: domain-language
---

# Module: [Check Resolution]

Scope: The d20 resolution mechanic, checks, degrees, conditions.

**Core terms**:
- check
- Difficulty Class (DC)

---

# Core Domain

### check

#### Domain Language

- A check is d20 + trait rank (plus modifiers) vs DC; equal or above is success.
- Whenever a character attempts something where outcome is in doubt, it requires a check.
- The GM decides what kind of check applies and sets the DC.

#### References

**Ref — Game Play**
Source: context/rules/HeroesHandbook-rules__chunk_009.md
Locator: lines 809–874
Extract: whole

---

### Difficulty Class (DC)

#### Domain Language

- The DC is a number set by the GM that a check result must equal or exceed.
- A standard difficulty scale runs from Very Easy (DC 0) through Nigh-Impossible (DC 40).

#### References

**Ref — Ch1 The Basics**
Source: context/rules/HeroesHandbook-rules__chunk_005.md
Locator: lines 244–284
Extract: whole

---

# Boundary Domain

## Effect / power effect

Owned by: Power

#### Domain Language

- An effect is the basic building block of a power; it describes what a power does in game terms.
- Resistance check DC is typically 10 + effect rank.

#### References

**Ref — Attack Checks**
Source: context/rules/HeroesHandbook-rules__chunk_016.md
Locator: lines 1195–1237
Extract: whole
```
