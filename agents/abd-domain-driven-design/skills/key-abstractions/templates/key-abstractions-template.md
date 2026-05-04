<!--
  key-abstractions — template for the growing module file after KA enrichment.

  The file already exists at state: domain-language.
  This skill enriches it in place. Key changes this phase makes:

    1. Inserts ## **Key Abstraction** grouping headings above the term groups they own
    2. Writes a prose definition paragraph for each ## KA
    3. Adds ### Ubiquitous Language under each ## KA (containing #### **term** sub-sections)
    4. Adds ### Decisions made under each ## KA
    5. Adds fenced `source` blocks beneath every **Ref —** entry
    6. Records any moved terms in **Moved to other modules**
    7. Bumps state to key-abstractions

  Structure per KA:
    ## **KA Name**
      prose definition paragraph
      ### Ubiquitous Language
        #### **term**
          - behavioral line
          #### References
            **Ref —** ...
      ---
      ### Decisions made
        - decision

  Boundary Domain is one flat section:
    # Boundary Domain
      ### Ubiquitous Language
        #### **boundary_term** *(owned by: Module)*
          - behavioral line
      ---
      ### References

  Contract:
    - Every term from domain-language stage is preserved, unchanged, under exactly one ## KA
    - #### **term** Domain Language bullets: unchanged
    - References: source blocks added beneath every Ref entry
    - Terms moved out recorded in **Moved to other modules** list
    - No Intent:, Shape hint:, Tension:, or other labeled sub-sections — prose only in KA definition
-->

---
state: key-abstractions
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

{{1–2 paragraphs of flowing prose defining this Key Abstraction. Covers what
unique role it plays, what it owns (boundary), what it does (responsibilities),
and what must always be true (rules/invariants). Woven together naturally —
not as labeled sections. Mentions interactions with other KAs by name.}}

### Ubiquitous Language

#### **{{term_name}}**
- {{behavioral line from domain-language — unchanged}}
- {{behavioral line from domain-language — unchanged}}

#### References

**Ref — {{title}}**
Source: {{source chunk path — unchanged}}
Locator: {{locator — unchanged}}
Extract: whole

```source
{{verbatim text copied byte-for-byte from the source chunk}}
```

#### **{{another_term}}**
- {{behavioral line — unchanged}}

#### References

**Ref — {{title}}**
Source: {{source chunk path}}
Locator: {{locator}}
Extract: whole

```source
{{verbatim text}}
```

---

### Decisions made

- {{independence-test call, module-fit call, grouping call, or open question with reasoning}}

---

## **{{AnotherKAName}}**

{{Prose definition paragraph(s) for this KA.}}

### Ubiquitous Language

#### **{{term_name}}**
- {{behavioral line — unchanged}}

#### References

**Ref — {{title}}**
Source: {{source chunk path}}
Locator: {{locator}}
Extract: whole

```source
{{verbatim text}}
```

---

### Decisions made

- {{…}}

---

# Boundary Domain

### Ubiquitous Language

#### **{{boundary_term}}** *(owned by: {{Module}})*
- {{behavioral line — unchanged}}

#### References

**Ref — {{title}}**
Source: {{source chunk path}}
Locator: {{locator}}
Extract: whole

```source
{{verbatim text from boundary term's source chunk}}
```

---

<!-- EXAMPLE — delete this section after using the template. -->

## Example (filled — Check Resolution module)

```markdown
---
state: key-abstractions
---

# Module: [Check Resolution]

Scope: The d20 resolution mechanic (roll + modifier vs DC), checks (routine,
opposed, resistance), degrees of success/failure, and conditions.

---

# Core Domain

## **Check**

A check is the core resolution mechanic — the single mechanism through which
any uncertain outcome in the game is determined. It owns the roll-plus-modifier-
versus-DC formula and serves as the single source of truth for whether an action
succeeds or fails.

### Ubiquitous Language

#### **check**
- A check is d20 + trait rank (plus modifiers) vs DC; equal or above is success.
- Whenever a character attempts something where outcome is in doubt, it requires a check.

#### References

**Ref — Game Play**
Source: context/rules/HeroesHandbook-rules__chunk_009.md
Locator: lines 809–874
Extract: whole

```source
GAME PLAY
…verbatim text from chunk…
```

#### **Difficulty Class (DC)**
- The DC is a number set by the GM that a check result must equal or exceed.
- A standard difficulty scale runs from Very Easy (DC 0) through Nigh-Impossible (DC 40).

#### References

**Ref — Ch1 The Basics**
Source: context/rules/HeroesHandbook-rules__chunk_005.md
Locator: lines 244–284
Extract: whole

```source
CH1 THE BASICS
…verbatim text from chunk…
```

---

### Decisions made

- Degree is a part of Check, not its own KA — it has no meaning outside a check.
- DC is kept under Check rather than made standalone — it is always set in context of a check.

---

# Boundary Domain

### Ubiquitous Language

#### **Power Effect** *(owned by: Power)*
- An effect is the basic building block of a power; it describes what a power does in game terms.

#### References

**Ref — Attack Checks**
Source: context/rules/HeroesHandbook-rules__chunk_016.md
Locator: lines 1195–1237
Extract: whole

```source
ATTACK CHECKS
…verbatim text from chunk…
```
```
