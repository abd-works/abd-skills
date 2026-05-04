<!--
  Normative shape for the growing module file after domain-language enrichment.

  Default output: <workspace>/abd-domain-driven-design/modules/<module-name>-domain-language.md

  If the module file already exists, enrich it in place.
  If it does not exist, create it with this structure.

  The file grows additively across phases:
    DL  → creates # Core Domain / #### **Term** / behavior bullets / #### References
    KA  → wraps terms in ## **Key Abstraction** groups + prose; moves #### **Term** under
          ### Ubiquitous Language; adds ### Decisions made; adds source blocks
    DS  → adds ### Domain Sketch under each ## **KA**; deduplicates references
    CRC → adds ### Class Responsibility Collaborator under each ## **KA**

  Domain Language stage structure:
    # Core Domain
      #### **term**              ← bold concept heading, no ### wrapper
        - behavioral line
      #### References
        **Ref —** ...

    # Boundary Domain
      #### **boundary_term** *(owned by: Module)*
        - behavioral line
      #### References
        **Ref —** ...
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

#### **{{term_name}}**
- {{short line: behavior, interaction, rule, or flow}}
- {{…}}

#### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{line_range or section pointer}}
Extract: {{whole or partial}}

---

#### **{{next_term_name}}**
- {{…}}

#### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{line_range}}
Extract: {{whole or partial}}

---

# Boundary Domain

#### **{{boundary_term_name}}** *(owned by: {{owning_module_name}})*
- {{short line: how this module depends on the concept}}
- {{…}}

#### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{line_range}}
Extract: {{whole or partial}}

---

<!-- EXAMPLE — delete this section after using the template. -->

## Example (filled — Check Resolution module)

```markdown
---
state: domain-language
---

# Module: [Check Resolution]

Scope: The d20 resolution mechanic, checks, degrees, conditions.

**Core terms**:
- check
- Difficulty Class (DC)
- trait
- condition

---

# Core Domain

#### **check**
- A check is d20 + trait rank (plus modifiers) vs DC; equal or above is success.
- Whenever a character attempts something where outcome is in doubt, it requires a check.
- The GM decides what kind of check applies and sets the DC.

#### References

**Ref — Game Play**
Source: context/rules/HeroesHandbook-rules__chunk_009.md
Locator: lines 809–874
Extract: whole

---

#### **Difficulty Class (DC)**
- The DC is a number set by the GM that a check result must equal or exceed.
- A standard difficulty scale runs from Very Easy (DC 0) through Nigh-Impossible (DC 40).

#### References

**Ref — Ch1 The Basics**
Source: context/rules/HeroesHandbook-rules__chunk_005.md
Locator: lines 244–284
Extract: whole

---

# Boundary Domain

#### **Power Effect** *(owned by: Power)*
- An effect is the basic building block of a power; it describes what a power does in game terms.
- Resistance check DC is typically 10 + effect rank.

#### References

**Ref — Attack Checks**
Source: context/rules/HeroesHandbook-rules__chunk_016.md
Locator: lines 1195–1237
Extract: whole
```
