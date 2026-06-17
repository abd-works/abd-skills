<!--
  Normative shape for the domain-language output.

  Output: <deliverables-folder>/[<name>-]domain-language.md
          (or <deliverables-folder>/modules/<module-name>-domain-language.md
           for multi-module engagements)

  STANDALONE file. Does not enrich a prior phase file in place.
  and use its KAs directly — do not re-extract terms or re-identify KAs.

  For multi-module scope in a single file: wrap each module in a
  # Module: [ModuleName] section with its own Terms, KA grouping, Core Domain,
  and Boundary Domain. The file header summarises the overall scope.

  Consistent shape:

    ## KAName                                   ← h2, no bold

    *KAName* is [definition as term — role, boundary, responsibilities,
    relationships, invariants woven naturally. This IS the term definition.]

    ### ka_name_as_a_concept                    ← MUST appear first; matches the KA
    - bullet telling the concept's story with *italicized domain terms*
    - **Invariant:** rule that must always hold

    ### another_concept
    - bullet telling the concept's story with *italicized domain terms*

    ### SubtypeName *is a type of* BaseName
    - delta behavior — only what the subtype adds

    ### property_term
    - is a property of *parent_concept* — brief classification note

    ### boundary_term *(boundary)*              ← scoped view; only what THIS KA depends on
    - bullet describing only the aspects this KA actually depends on, with *italicized domain terms*

    #### Decisions made                         ← ONE per KA, after ALL concept blocks
    - independence test, scope-fit test, typing call, or open question

    #### References                             ← ONE per KA, after Decisions made
    **Ref — title**
    Source: ...
    Locator: ...
    Extract: whole

    ---                                         ← separator between KAs

  Contract:
    - Terms header: flat list with term + short plain-English definition only (no source references).
    - Boundary/moved-out terms carry a parenthetical note in the Terms list.
    - Each KA anchors at least 3–5 terms (subordinate concepts, subtypes, properties). A KA with
      fewer than three terms is not a KA — merge it under an existing KA or downgrade it.
    - KA intro paragraph (*KAName* is …) IS the term definition. No separate ### ka_name definition block.
    - The KA's own concept is listed FIRST under the ## KA heading, with bullets telling its story.
    - Bullets live directly under each ### concept heading — no #### sub-headings.
    - Every domain term in a bullet, invariant, or KA intro paragraph is *italicized*.
    - ONE #### Decisions made and ONE #### References per KA, after all its concept blocks.
    - --- separators between KAs.
    - No bold on ## KA or ### concept headings.
    - Subtypes use the English heading form: ### SubtypeName *is a type of* BaseName.
    - Behavior + produced result on the same bullet (", producing a *result*").
    - Pure properties (no independent behavior/invariants) are mentioned only in the parent concept's bullets — no stub heading.
    - A property earns its own ### heading only when it has its own invariant, behavior, or cross-concept interaction.
    - Boundary entries carry Owned by: ModuleName (exactly one module).
    - If a boundary term is relevant to more than one KA, each KA includes its own scoped stub
      (### boundary_term *(boundary)*) showing only the behaviors that KA depends on.
      The # Boundary Domain entry is the canonical record; per-KA stubs are scoped views.
-->

# Module: [{{ModuleName}}]

_{{Brief summary of concepts modeled in this file.}}_

Scope: {{bounded slice or engagement scope}}

**Terms**:
- **{{KAName}}**
  - **{{ka_term}}** — {{short plain-English definition}}
  - **{{subordinate_term1}}** — {{short plain-English definition}}
  - **{{subordinate_term2}}** — {{short plain-English definition}}
- **{{AnotherKAName}}**
  - **{{another_ka_term}}** — {{short plain-English definition}}
  - **{{subordinate_term3}}** — {{short plain-English definition}}

_{{Analytical overview: how the module's core mechanic works end-to-end, what the key invariants are, and how the KAs relate. Use *italicized domain terms* throughout.}}_

---

# Core Domain

## {{KAName}}

*{{KAName}}* is {{definition — what it owns, what unique role it plays, how it
relates to other KAs, what responsibilities it performs, what must always be true.
Weave naturally. This paragraph is the term definition for the KA itself.}}

### {{ka_name_as_a_concept}}

- {{bullet that naturally tells part of the concept's story — could be what it is for, what it owns,
  how it relates to *another concept*, what it does, or what must always be true.
  Every domain term is *italicized*. Write as many bullets as the source warrants.
  Let the story flow; do not fill in one bullet per aspect.}}
- **Invariant:** {{rule with *italicized domain terms* — only if the source states one}}

### {{subordinate_concept}}

- {{same principle — as many bullets as the source warrants, in the order that reads naturally,
  covering whichever aspects (role, boundary, relationships, responsibilities, rules) the source supports.
  Every domain term is *italicized*.}}
- **Invariant:** {{rule with *italicized domain terms* — only if the source states one}}

### {{SubtypeName}} *is a type of* {{BaseName}}

- {{delta behavior — only what the subtype adds, with *italicized domain terms*}}

    ### {{property_with_own_behavior_or_invariant}}    ← only when the property has its own invariant, behavior, or cross-concept interaction

    - {{behavior or invariant that justifies the heading}}
    - **Invariant:** {{rule — only if source states one}}

    ### {{boundary_term}} *(boundary)*

- {{only the aspects of this boundary concept that this KA actually depends on, with *italicized domain terms*}}

#### Decisions made

- {{independence test result}}
- {{scope-fit test result}}
- {{typing call (concept vs property vs subtype vs instance) or open question}}

#### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{locator}}
Extract: {{whole or partial}}

---

## {{AnotherKAName}}

*{{AnotherKAName}}* is {{definition…}}

### {{another_ka_as_a_concept}}

- {{bullet telling the concept's story with *italicized domain terms*}}
- **Invariant:** {{rule}}

#### Decisions made

- {{…}}

#### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{locator}}
Extract: {{whole or partial}}

---

# Boundary Domain

## {{boundary_concept}}

Owned by: {{OwningModule}}

- {{bullet describing what this scope depends on, with *italicized domain terms*}}

#### Decisions made

- {{boundary placement reasoning}}

#### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{locator}}
Extract: {{whole or partial}}

---

<!-- EXAMPLE — delete this section after using the template. -->

## Example (filled — Check Resolution module, abbreviated)

```markdown
# Module: [Check Resolution]

_Concept sketch for the d20 resolution mechanic._

Scope: How any uncertain action is resolved: roll + modifier vs DC, with degree of success or failure.

**Terms**:
- **Trait**
  - **trait** — any quantifiable game characteristic a character possesses
  - **rank** — the single numeric measure of a trait's effectiveness
- **Check**
  - **check** — the core resolution mechanic: d20 + modifier vs Difficulty Class
  - **difficulty class (DC)** — the number a check must equal or exceed to succeed
  - **degree of success** — how much a check result exceeds the DC
  - **d20** — the die a check rolls *(property of check)*
  - **opposed check** — a check made against another character's check result as the DC *(subtype of check)*

---

All uncertain outcomes are resolved with one mechanic: roll *d20*, add all appropriate *modifiers*, compare against a *Difficulty Class*; meeting or exceeding the *DC* is success. Each *check* is tied to exactly one *trait*.

---

# Core Domain

## Trait

*Trait* is the base abstraction for every quantifiable game characteristic a *character* possesses — *abilities*, *skills*, *defenses*, *powers*, and *advantages* are all *traits*. *Trait* owns the concept of *rank*: every *trait* has exactly one *rank*, a single numeric measure of its effectiveness, and that *rank* is the value that flows into *checks* as the *modifier*.

### trait

- is a *quantifiable characteristic* of a *character*
- has exactly one *rank* — the single numeric value measuring its effectiveness
- supplies its *rank* as the primary *modifier* for any *check* made using it; without a *trait* there is no *check*

### rank

- is a single numeric value carried by a *trait* — the measure of that *trait's* effectiveness
- supplies the base *modifier* for a *check* — the *trait's* *rank* flows directly into the *roll total*
- **Invariant:** *ranks* must never be added directly; convert to *measures*, perform arithmetic on the *measures*, then convert back to a *rank*

#### Decisions made

- *Trait* is owned by this module as the base abstraction — other modules (*Ability*, *Skill*, *Power*, *Advantage*) define specific traits (independence test).
- *Rank* is a concept, not a property of *Trait* — it has its own scale (doubling), its own invariant (no direct addition), and its own interactions with *Check*.

#### References

**Ref — Ranks & Measures**
Source: context/rules/HeroesHandbook-rules__chunk_008.md
Locator: lines 376–808
Extract: whole

---

## Check

*Check* is the core resolution mechanic. It binds together a *d20* roll, a *trait*-derived *modifier*, and a *Difficulty Class* into one comparison: *roll total* versus *DC*, with success on a match or exceed. *Check* owns the resolution itself; what comes out the other side — the *degree of success* or *failure* — is its result.

### check

- is made *using* the *trait* of a *character*
- is made *against* a *difficulty class* set by the *GM*
- is resolved by *rolling* a *d20*, adding the *trait rank* and the *circumstance modifier*, comparing the *roll total* to the *difficulty class*, producing a *check result*
- **Invariant:** shape is always *roll total* versus *difficulty class*; subtypes only vary how *total* or *DC* is produced

### difficulty class (DC)

- is a number set by the *GM* that a *check* must equal or exceed to succeed
- ranges across a standard *difficulty scale* from Very Easy (DC 0) to Nigh-Impossible (DC 40)

### opposed check *is a type of* check

- is made against an *opposing character's* *check result* as the *difficulty class*
- on a *tie*, the *higher bonus* wins; if *bonuses* also tie, a *tie-break d20* decides

### d20

- is the instrument a *check* rolls — a property of *check*, not a separate concept

### power effect *(boundary)*

- sets the *DC* for *resistance checks* as DC = *rank* + 10

#### Decisions made

- *Check* alone owns *success/failure* for uncertain outcomes (independence test).
- *DC* belongs here, not as its own KA — it exists only in relation to a *check* (independence test).
- *d20* is the instrument a *check* rolls — a property, not a concept; mentioned in the *check* bullet only.

#### References

**Ref — Game Play**
Source: context/rules/HeroesHandbook-rules__chunk_009.md
Locator: lines 809–874
Extract: whole

**Ref — Opposed Checks**
Source: context/rules/HeroesHandbook-rules__chunk_014.md
Locator: lines 1102–1146
Extract: whole

**Ref — The Die**
Source: context/rules/HeroesHandbook-rules__chunk_004.md
Locator: lines 202–243
Extract: whole

---

# Boundary Domain

## Effect / power effect

Owned by: Power

- has a *rank* that determines the *resistance check* DC (DC = *rank* + 10)
- may impose one or more *conditions* on a *character* based on *degree of failure*

#### Decisions made

- *Power effect* is owned by the *Power* module — it has broad meaning outside this scope (scope-fit test).

#### References

**Ref — Resistance and Ongoing Effects**
Source: context/rules/HeroesHandbook-rules__chunk_209.md
Locator: lines 14791–14830
Extract: whole

---
```
