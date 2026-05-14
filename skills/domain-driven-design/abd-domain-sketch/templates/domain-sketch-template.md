<!--
  Normative shape for the domain-sketch phase output.

  Output: <deliverables-folder>/[<name>-]domain-sketch.md
          (or <deliverables-folder>/modules/<module-name>-domain-sketch.md
           for multi-module engagements)

  This skill produces a STANDALONE file. It does not enrich the prior phase's
  file in place. It is a fresh artifact in the same flat heading shape.

  Consistent shape:

    ## KAName

    [Analytical intro paragraph(s) with *italicized domain terms*]

    ### ka_name_as_a_concept            ← MUST appear first; matches the KA
    - verb-led behavior with *italicized domain terms*
    - **Invariant:** rule that must always hold

    ### Decisions made
    - typing call, scope call, structural call, or open question

    ### References
    **Ref — title**
    Source: ...
    Locator: ...
    Extract: whole

    ---

    ### another_concept
    - verb-led behavior with *italicized domain terms*

    ### Decisions made
    - ...

    ### References
    **Ref — title**
    Source: ...

    ---

    ### SubtypeName *is a type of* BaseName
    - delta behavior with *italicized domain terms*

    ### References
    **Ref — title**
    Source: ...

    ---

    ### property_term
    - is a property of *parent_concept* — brief note

    ### References
    **Ref — title**
    Source: ...

    ---

  Contract:
    - One file per phase. Do not enrich a prior file in place.
    - The KA's own concept is listed FIRST under the ## KA heading.
    - Bullets live directly under each ### concept heading — no sub-headings.
    - Every domain term referenced in a behavior bullet is *italicized*.
    - ### Decisions made and ### References per concept (not bundled per KA).
    - --- separators between concept blocks.
    - No bold on concept headings or KA headings.
    - Subtypes use the English heading form *is a type of*.
    - Behavior + produced result on the same bullet (", producing a [result]").
    - Property/instance terms get a stub heading with classification note.
-->

---
state: domain-sketch
---

# Module: [{{ModuleName}}]

_{{Brief summary of concepts modeled in this file.}}_

Scope: {{bounded slice or engagement scope}}

---

{{Analytical overview paragraph(s): how the module's core mechanic works end-to-end, what the key invariants are, and how concepts relate. Use *italicized domain terms* throughout.}}

---

# Core Domain

## {{KAName}}

{{Analytical intro paragraph(s): what this KA is for, what it owns, who it cooperates with. Use *italicized domain terms* throughout.}}

### {{ka_name_as_a_concept}}

- {{verb-led behavior with *italicized domain terms*}}
- {{verb-led behavior, producing a *{{result}}* when relevant}}
- **Invariant:** {{rule that must always hold}}

### Decisions made

- {{typing call, scope call, structural call, or open question with reasoning}}

### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{locator}}
Extract: {{whole or partial}}

---

### {{another_concept}}

- {{verb-led behavior with *italicized domain terms*}}
- {{verb-led behavior with *italicized domain terms*}}
- **Invariant:** {{rule}}

### Decisions made

- {{...}}

### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{locator}}
Extract: {{whole or partial}}

---

### {{SubtypeName}} *is a type of* {{BaseName}}

- {{delta behavior — only what the subtype adds, with *italicized domain terms*}}

### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{locator}}
Extract: {{whole or partial}}

---

### {{property_or_instance_term}}

- is a {{property / instance / type property}} of *{{parent_concept}}* — {{brief note on classification}}

### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{locator}}
Extract: {{whole or partial}}

---

## {{AnotherKAName}}

{{Analytical intro paragraph(s) with *italicized domain terms*.}}

### {{another_ka_as_a_concept}}

- {{verb-led behavior with *italicized domain terms*}}
- **Invariant:** {{rule}}

### Decisions made

- {{...}}

### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{locator}}
Extract: {{whole or partial}}

---

# Boundary Domain

## {{boundary_module_or_concept}}

Owned by: {{owning_module}}

- {{verb-led behavior describing what this module sees of it, with *italicized domain terms*}}

### Decisions made

- {{boundary placement reasoning}}

### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{locator}}
Extract: {{whole or partial}}

---

<!-- EXAMPLE — delete this section after using the template. -->

## Example (filled — Check Resolution module, abbreviated)

```markdown
---
state: domain-sketch
---

# Module: [Check Resolution]

_Object model for all Check Resolution terms. Concepts: Trait, Rank, Check, Check Result, Condition._

Scope: The d20 resolution mechanic (roll + modifier vs DC), checks, degrees, conditions.

---

All uncertain outcomes are resolved with one mechanic: roll *d20*, add all appropriate *modifiers*, compare against a *Difficulty Class*; meeting or exceeding the *DC* is success. Each *check* is tied to exactly one *trait*.

---

# Core Domain

## Trait

A *trait* is the base abstraction for every quantifiable game characteristic a *character* possesses — *abilities*, *skills*, *defenses*, *powers*, and *advantages* are all *traits*. *Trait* owns the concept of *rank*: every *trait* has exactly one *rank*, a single numeric measure of its effectiveness, and that *rank* is the value that flows into *checks* as the *modifier*.

### Trait

- is a *quantifiable characteristic* of a *character*
- has exactly one *rank* — the single numeric value measuring its effectiveness
- supplies its *rank* as the primary *modifier* for any *check* made using it; without a *trait* there is no *check*

### Decisions made

- *Trait* is owned by this module as the base abstraction — other modules (*Ability*, *Skill*, *Power*, *Advantage*) define specific traits.
- *Rank* is a concept — simple, but with its own scale, invariant, and interactions with *Check* and *Measurement*.

### References

**Ref — Ranks & Measures**
Source: context/rules/HeroesHandbook-rules__chunk_008.md
Locator: lines 376–808
Extract: whole

---

### Rank

- is a single numeric value carried by a *trait* — the measure of that *trait's* effectiveness
- supplies the base *modifier* for a *check* — the *trait's* *rank* flows directly into the *roll total*
- **Invariant:** *ranks* must never be added directly; convert to *measures*, perform arithmetic on the *measures*, then convert back to a *rank*

### Decisions made

- *Rank* is a concept, not a property of *Trait* — it has its own scale (doubling), its own invariant (no direct addition), and its own interactions.

### References

**Ref — Ranks & Measures**
Source: context/rules/HeroesHandbook-rules__chunk_008.md
Locator: lines 376–808
Extract: whole

---

## Check

A *check* is the core resolution mechanic. It binds together a *d20* roll, a *trait*-derived *modifier*, and a *Difficulty Class* into one comparison: *roll* plus *modifier* versus *DC*, with success on a match or exceed.

### check

- is made *using* the *trait* of a *character*
- is made *against* a *difficulty class* set by the *GM*
- is resolved by *rolling* a *d20*, adding the *trait rank* and the *circumstance modifier*, comparing the *roll total* to the *difficulty class*, producing a *check result*
- **Invariant:** shape is always *roll total* versus *difficulty class*; subtypes only vary how *total* or *DC* is produced

### Decisions made

- *Check* alone owns *success/failure* for uncertain outcomes.
- *d20* is the instrument a *check* rolls — a property, not a separate concept.

### References

**Ref — Game Play**
Source: context/rules/HeroesHandbook-rules__chunk_009.md
Locator: lines 809–874
Extract: whole

---

### d20

- is the instrument a *check* rolls — a property of *check*, not a separate concept

### References

**Ref — The Die**
Source: context/rules/HeroesHandbook-rules__chunk_004.md
Locator: lines 202–243
Extract: whole

---

### opposed check *is a type of* check

- is made against an *opposing character's* *check result* as the *difficulty class*
- on a *tie*, the *higher bonus* wins; if *bonuses* also tie, a *tie-break d20* decides

### References

**Ref — Opposed Checks**
Source: context/rules/HeroesHandbook-rules__chunk_014.md
Locator: lines 1102–1146
Extract: whole

---

# Boundary Domain

## Effect / power effect

Owned by: Power

- has a *rank* that determines the *resistance check* DC (DC = *rank* + 10)
- may impose one or more *conditions* on a *character* based on *degree of failure*

### Decisions made

- The "ongoing" quality is a property of an effect, not a separate concept.

### References

**Ref — Resistance and Ongoing Effects**
Source: context/rules/HeroesHandbook-rules__chunk_209.md
Locator: lines 14791–14830
Extract: whole

---
```
