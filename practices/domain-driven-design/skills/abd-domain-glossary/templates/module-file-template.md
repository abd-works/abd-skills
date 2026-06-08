<!--
  Domain Scan — per-module file (combined boundaries + KAs + terms + source refs).

  Copy to: <workspace>/domain/modules/<module-name>.md

  Contract:
    - ONE file per module. Boundaries AND vocabulary in a single document.
    - Module scope, KA inventory, KA intro paragraphs, subordinate terms with
      behavioral bullets, decisions, and source references grouped by KA.
    - KA intro paragraph = term definition for the KA. Do NOT add ### ka_name block.
    - #### Decisions made and #### References per term — h4, never h3.
    - --- separator after every term block.
    - *italicized* domain terms throughout.
    - No bold on ## KA or ### term headings.
    - Source references point to files on disk; no verbatim content outside
      ```source``` blocks under #### References.
    - For rejected.md and unallocated.md, each reference includes a Reason: line.
-->

# Module: [{{ModuleName}}]

Scope: {{bounded scope description — what region of the domain this module covers}}.

**Key Abstractions (term grouping)**:
- **{{KAName}}**: {{term1}}, {{term2}}, {{term3}}, …
- **{{AnotherKAName}}**: {{term4}}, {{term5}}, …

**Moved to other modules**:
- {{moved_term}} → {{DestinationModule}}

---

# Core Domain

## {{KAName}}

*{{KAName}}* is {{definition — what it owns, what unique role it plays, how it
relates to other KAs, what responsibilities it performs, what must always be true.
Weave naturally. This paragraph is the term definition for the KA itself.}}

#### Decisions made

- {{why these terms belong together under this KA}}

### {{subordinate_term}}

- {{behavioral line with *italicized domain terms*}}
- {{behavioral line}}

#### References

**Ref — {{ref_title}}**
Source: {{relative/path/to/source/file.md}}
Locator: {{line_range or section pointer}}
Extract: {{whole or partial}}

```source
{{verbatim text copied byte-for-byte from the source}}
```

---

### {{another_subordinate_term}}

- {{behavioral line with *italicized domain terms*}}

#### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{line_range}}
Extract: {{whole or partial}}

```source
{{verbatim text}}
```

---

## {{AnotherKAName}}

*{{AnotherKAName}}* is {{definition…}}

### {{subordinate_term}}

- {{behavioral line}}

#### Decisions made

- {{…}}

#### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{locator}}
Extract: {{whole or partial}}

```source
{{verbatim text}}
```

---

# Boundary Domain

### {{boundary_term}} *(owned by: {{OwningModule}})*

- {{behavioral line: how this module sees or depends on this concept}}

#### Decisions made

- {{boundary placement reasoning}}

#### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{line_range}}
Extract: {{whole or partial}}

```source
{{verbatim text}}
```

---

<!-- EXAMPLE — delete this section after using the template. -->

## Example (filled — Check Resolution module)

```markdown
# Module: [Check Resolution]

Scope: The d20 resolution mechanic, checks, degrees of success, conditions.

**Key Abstractions (term grouping)**:
- **Check**: Difficulty Class (DC), degree of success, degree of failure, modifier
- **Condition**: condition value, condition track

---

# Core Domain

## Check

A *check* is the core resolution mechanic of the system — a *d20* roll plus a
*trait rank* and any *modifiers* compared against a *Difficulty Class*. It is the
single authority on whether a character action succeeds and by how much.

### Difficulty Class (DC)

- The *DC* is a number set by the GM that a *check* result must equal or exceed.
- A standard difficulty scale runs from Very Easy (DC 0) through Nigh-Impossible (DC 40).

#### Decisions made

- *Degree of success* stays under *Check* — it has no meaning outside a *check* (independence test).
- *DC* belongs here, not as its own KA — it exists only in relation to a *check* (independence test).

#### References

**Ref — Game Play**
Source: context/rules/HeroesHandbook-rules__chunk_009.md
Locator: lines 809–874
Extract: whole

```source
GAME PLAY
…verbatim text…
```

---

### degree of success

- A *degree of success* is determined by how much the *check* result exceeds the *DC*.
- Every 5 points above the *DC* adds one degree.

#### References

**Ref — Degrees of Success**
Source: context/rules/HeroesHandbook-rules__chunk_009.md
Locator: lines 875–910
Extract: whole

```source
DEGREES OF SUCCESS
…verbatim text…
```

---

# Boundary Domain

### Power Effect *(owned by: Power)*

- A *power effect* sets the *DC* for resistance *checks*; this module depends on
  that value without defining the *effect* itself.

#### Decisions made

- *Power effect* is owned by the *Power* module — it has broad meaning outside
  *check* resolution (module-fit test).

#### References

**Ref — Attack Checks**
Source: context/rules/HeroesHandbook-rules__chunk_016.md
Locator: lines 1195–1237
Extract: whole

```source
ATTACK CHECKS
…verbatim text…
```

---
```
