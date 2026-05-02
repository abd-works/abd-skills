<!--
  key-abstractions — template for the growing module file after KA enrichment.

  The file already exists at state: domain-language.
  This skill enriches it in place. Key changes this phase makes:

    1. Inserts ## <Key Abstraction> grouping headings above the ### term groups they own
    2. Writes a prose definition paragraph for each ## KA (role, boundary,
       responsibilities, rules/invariants — woven into flowing prose)
    3. Adds #### Decisions made under each ## KA prose definition
    4. Adds fenced `source` blocks beneath every **Ref —** entry
    5. Records any moved terms in **Moved to other modules**
    6. Bumps state to key-abstractions

  Contract:
    - Every ### term from UDL stage is preserved, unchanged, under exactly one ## KA
    - #### Domain Language bullets: unchanged
    - #### References: source blocks added beneath every Ref entry
    - # Boundary Domain terms: ## heading, Owned by: preserved, source blocks added
    - Terms moved out recorded in **Moved to other modules** list
    - No Intent:, Shape hint:, Tension:, labeled sections (Role:, Boundary:, etc.) — prose only
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

## {{KAName}}

{{1–2 paragraphs of flowing prose defining this Key Abstraction. Covers what
unique role it plays, what it owns (boundary), what it does (responsibilities),
and what must always be true (rules/invariants). Woven together naturally —
not as labeled sections. Mentions interactions with other KAs by name.}}

#### Decisions made

- {{independence-test call, module-fit call, grouping call, or open question with reasoning}}
- {{…}}

### {{term_name}}

#### Domain Language

- {{behavioral line from UDL — unchanged}}
- {{behavioral line from UDL — unchanged}}

#### References

**Ref — {{title}}**
Source: {{source chunk path — unchanged}}
Locator: {{locator — unchanged}}
Extract: whole

```source
{{verbatim text copied byte-for-byte from the source chunk}}
```

---

### {{another_term}}

#### Domain Language

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

## {{AnotherKAName}}

{{Prose definition paragraph(s) for this KA.}}

#### Decisions made

- {{…}}

### {{term_name}}

#### Domain Language

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

# Boundary Domain

## {{boundary_term}}

Owned by: {{module — unchanged}}

#### Domain Language

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

## Example (filled)

```markdown
---
state: key-abstractions
---

# Module: [Check Resolution]

Scope: The d20 resolution mechanic (roll + modifier vs DC), checks (routine,
opposed, resistance), degrees of success/failure, measurements and the
Rank/Measure table, and conditions (basic and combined).

**Core terms**:
- d20
- check
- Difficulty Class (DC)
- modifier
- condition

**Moved to other modules**:
- hero point → Combat
- extra effort → Combat

---

# Core Domain

## Check

A check is the core resolution mechanic — the single mechanism through which
any uncertain outcome in the game is determined. It interacts with Trait
(supplying the modifier), Difficulty Class (setting the threshold), and Degree
(interpreting the margin). The check owns the roll-plus-modifier-versus-DC
formula and serves as the single source of truth for whether an action succeeds
or fails; no other abstraction may duplicate this determination. A check must
always produce a binary success/failure result. The GM sets the DC; the player
rolls and applies modifiers.

#### Decisions made

- Degree is a part of Check, not its own KA — it has no meaning outside a check (independence test).
- DC is kept under Check rather than made standalone — it is always set in the context of a check.
- Modifier stays under Check — it is the numeric contribution of a trait to a specific check, not an independent concept.

### check

#### Domain Language

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

### Difficulty Class (DC)

#### Domain Language

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

# Boundary Domain

## Effect / power effect

Owned by: Power

#### Domain Language

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
