<!--
  Normative shape for the key-abstractions phase output.

  Output: <deliverables-folder>/[<name>-]key-abstractions.md
          (or <deliverables-folder>/modules/<module-name>-key-abstractions.md
           for multi-module engagements)

  This skill produces a STANDALONE file. It is not enriched in place by later
  phase skills (domain-sketch, CRC, object-model). Each later DDD phase skill
  writes its own file using the same flat heading shape.

  Consistent shape:

    ## KAName

    [Analytical intro paragraph(s) with *italicized domain terms* — role,
     boundary, responsibilities, relationships, invariants — woven naturally]

    ### ka_name_as_a_term             ← MUST appear first; matches the KA
    - behavioral line with *italicized domain terms*

    ### Decisions made
    - independence-test result, module-fit result, grouping call

    ### References
    **Ref — title**
    Source: ...
    Locator: ...
    Extract: whole

    ```source
    verbatim
    ```

    ---

    ### another_term
    - behavioral line with *italicized domain terms*

    ### References
    **Ref — title**
    Source: ...

    ---

  Contract:
    - One file per phase. Do not enrich a prior file in place.
    - The KA's own term is listed FIRST under the ## KA heading.
    - Bullets live directly under each ### term heading — no sub-headings.
    - Every domain term referenced in a behavioral line is *italicized*.
    - ### Decisions made and ### References per term (not bundled per KA).
    - --- separators between term blocks.
    - No bold on KA headings or term headings.
    - The flat **Core terms** list stays as the inventory in the header.
    - A separate **Key Abstractions (term grouping)** list shows the structure.
-->

---
state: key-abstractions
---

# Module: [{{ModuleName}}]

Scope: {{bounded slice or engagement scope — same as domain-language}}

**Core terms**:
- {{term1}}
- {{term2}}
- …

**Key Abstractions (term grouping)**:
- **{{KAName}}**: {{ka_name_as_a_term}}, {{term1}}, {{term2}}, …
- **{{AnotherKAName}}**: {{another_ka_as_a_term}}, {{term3}}, {{term4}}, …

**Moved to other modules**:
- {{moved_term}} → {{DestinationModule}}

---

# Core Domain

## {{KAName}}

{{Analytical intro paragraph(s) with *italicized domain terms*. Covers what
unique role it plays, what it owns (boundary), what it does (responsibilities),
its relationships with other KAs, and what must always be true (rules /
invariants). Woven together naturally — not as labeled sections. This is the
deepest definition of the KA: it should be rich enough that a domain expert
can read it and challenge it.}}

### {{ka_name_as_a_term}}

- {{behavioral line with *italicized domain terms*: what it owns, what it enforces, how it relates to other KAs}}
- {{behavioral line}}

### Decisions made

- {{independence-test result}}
- {{module-fit result}}
- {{grouping call or open question}}

### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{locator}}
Extract: {{whole or partial}}

```source
{{verbatim text copied byte-for-byte from the source}}
```

---

### {{another_term}}

- {{behavioral line with *italicized domain terms* — carried from domain-language, unchanged in meaning}}

### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{locator}}
Extract: {{whole or partial}}

```source
{{verbatim text}}
```

---

## {{AnotherKAName}}

{{Analytical intro paragraph(s) with *italicized domain terms*.}}

### {{another_ka_as_a_term}}

- {{behavioral line with *italicized domain terms*}}

### Decisions made

- {{…}}

### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{locator}}
Extract: {{whole or partial}}

```source
{{verbatim text}}
```

---

# Boundary Domain

## {{boundary_module_or_concept}}

Owned by: {{owning_module}}

### {{boundary_term}}

- {{behavioral line with *italicized domain terms*: how this module sees or depends on it}}

### Decisions made

- {{boundary placement reasoning}}

### References

**Ref — {{ref_title}}**
Source: {{source_path}}
Locator: {{locator}}
Extract: {{whole or partial}}

```source
{{verbatim text}}
```

---
