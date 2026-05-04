<!--
  domain-sketch template — shows the growing module file shape AFTER domain-sketch enrichment.

  The file already exists at state: key-abstractions.
  This skill enriches it in place. Key changes this phase makes:

    1. Under each ## **KA Name**, adds ### Ubiquitous Language (containing #### **term** sub-sections)
       and ### Domain Sketch (containing #### **term** sub-sections with verb-led behavior bullets)
    2. Adds ### Decisions made at the ## KA level
    3. Deduplicates ### References across terms within the same ## KA
    4. Adds new **Ref —** entries for any behavior bullet not yet cited
    5. Bumps state to domain-sketch

  Structure per KA:
    ## **KA Name**
      intro paragraph
      ### Ubiquitous Language
        #### **term**
        #### **SubtypeName** *is a type of* **BaseName**
      ---
      ### Domain Sketch
        #### **term**
        #### **SubtypeName** *is a type of* **BaseName**
      ---
      ### Decisions made
      ### References

  Boundary Domain is one flat section:
    # Boundary Domain
      ### Ubiquitous Language
        #### **boundary_term** *(owned by: Module)*
      ---
      ### Domain Sketch
        #### **boundary_term**
      ---
      ### Decisions made
      ### References

  Contract:
    - Everything from UDL and KA stages stays unchanged:
        #### **term** Domain Language bullets — never touched
        ## KA prose definitions — never touched
        #### References already present — only deduplicated
    - ### Ubiquitous Language replaces scattered #### Domain Language headings
    - ### Domain Sketch is NEW — added per KA, with #### **term** sub-sections
    - Subtypes use the heading form #### **SubtypeName** *is a type of* **BaseName**
      and appear under the same ## KA as their base term
    - Slash terms in concept names must be flagged for resolution before CRC
    - One behavior per line — do not merge a state with its triggered action
-->

---
state: domain-sketch
---

# Module: [{{ModuleName}}]

Scope: {{scope from partition — unchanged}}

**Core terms**:
- {{term1}}
- {{term2}}
- …

**Moved to other modules**:
- {{moved_term}} → {{DestinationModule}}

---

# Core Domain

## **{{KAName}}**

{{KA prose definition — unchanged from key-abstractions stage}}

### Ubiquitous Language

#### **{{term_name}}**
- {{behavioral line — unchanged from domain-language stage}}
- {{behavioral line — unchanged from domain-language stage}}

#### **{{SubtypeName}}** *is a type of* **{{BaseName}}**
- {{behavioral line — unchanged}}

---

### Domain Sketch

#### **{{term_name}}**
- {{verb-led behavior bullet: what it does, enforces, or produces}}
- {{verb-led behavior bullet}}
- **Invariant:** {{rule that must always hold, if any}}

#### **{{SubtypeName}}** *is a type of* **{{BaseName}}**
- {{delta behavior — only what the subtype adds, not what it shares with the base}}

---

### Decisions made

- {{boundary call, scope call, structural call, or open question with reasoning}}

### References

**Ref — {{title}}**
Source: {{source chunk path}}
Locator: {{locator}}
Extract: whole

```source
{{verbatim text}}
```

---

## **{{AnotherKAName}}**

{{KA prose definition — unchanged}}

### Ubiquitous Language

#### **{{term_name}}**
- {{behavioral line — unchanged}}

---

### Domain Sketch

#### **{{term_name}}**
- {{verb-led behavior bullet}}

---

### Decisions made

### References

**Ref — {{title}}**
Source: {{source chunk path}}
Locator: {{locator}}
Extract: whole

```source
{{verbatim text}}
```

---

# Boundary Domain

### Ubiquitous Language

#### **{{boundary_term}}** *(owned by: {{Module}})*
- {{behavioral line — unchanged}}

---

### Domain Sketch

#### **{{boundary_term}}**
- {{verb-led behavior bullet describing what this module sees of it}}

---

### Decisions made

### References

**Ref — {{title}}**
Source: {{source chunk path}}
Locator: {{locator}}
Extract: whole

```source
{{verbatim text — unchanged}}
```

---

<!-- EXAMPLE — delete this section after using the template. -->

## Example (filled — Check Resolution module)

```markdown
---
state: domain-sketch
---

# Module: [Check Resolution]

Scope: The d20 resolution mechanic (roll + modifier vs DC), checks (routine,
opposed, resistance), degrees of success/failure, and conditions.

---

# Core Domain

## **Check**

A check is the core resolution mechanic — the single mechanism through which any
uncertain outcome is determined. It owns the roll-plus-modifier-versus-DC formula.

### Ubiquitous Language

#### **Check**
- A check is d20 + trait rank (plus modifiers) vs DC; equal or above is success.

#### **Opposed Check** *is a type of* **Check**
- An opposed check pits two characters against each other; higher roll wins.

---

### Domain Sketch

#### **Check**
- is resolved by *rolling* a *d20*, adding *trait rank* and *circumstance modifier* and comparing to the *difficulty class*, producing a *check result*
- may have a *circumstance modifier* applied (±2 minor, ±5 major)
- **Invariant:** always roll total versus difficulty class; subtypes only vary how total or DC is produced

#### **Opposed Check** *is a type of* **Check**
- is made against an *opposing character's check result* as the *difficulty class*
- on a *tie*, the *higher bonus* wins; if *bonuses* also tie, a *tie-break d20* decides

---

### Decisions made

- Opposed Check is a subtype — it reuses the base resolution but changes what the DC is.

### References

**Ref — Game Play**
Source: context/rules/HeroesHandbook-rules__chunk_009.md
Locator: lines 809–874
Extract: whole

```source
…verbatim text…
```

---

# Boundary Domain

### Ubiquitous Language

#### **Power Effect** *(owned by: Power)*
- An effect is the basic building block of a power; it describes what a power does.

---

### Domain Sketch

#### **Power Effect**
- has a *rank* that determines the *resistance check* DC (DC = rank + 10)
- may impose one or more *conditions* on a *character* based on *degree of failure*
- may be *ongoing* — requires a *resistance check* at end of each of the target's turns
- when the *resistance check* succeeds, the effect ends
- when ended, all *conditions* it imposed are removed

---

### Decisions made

- Power Effect is a boundary concept — condition-selection rules belong to the Power module.

### References

**Ref — Resistance and Ongoing Effects**
Source: context/rules/HeroesHandbook-rules__chunk_209.md
Locator: lines 14791–14830
Extract: whole

```source
…verbatim text…
```
```
