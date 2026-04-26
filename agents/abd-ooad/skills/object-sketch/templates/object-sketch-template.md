<!--
  Structural skeleton only: placeholders and separator shapes for object-sketch.md.
  Section order and in-concept layout are normative here; SKILL.md holds rules and relationships.

  Copy to: <workspace>/abd-ooad/object-sketch.md

  Workflow: optional extracted-domain-logic.md (extract-domain-logic); key-abstractions.md
  when present; refine into concept blocks (Domain-logic + ### Concept / ### Subtype *is a type of* Base).
  Do not maintain a parallel "Key abstractions (carry-forward)" section that
  duplicates the whole key-abstractions.md module - that file stays canonical for
  identification narrative.

  Evidence is always under Extract headings: module **`### Extract`** (inventory bullets:
  Source, Locator, optional short quote), and every concept/subtype **`#### Extract - ...`**
  (Source, Locator, Extract whole|partial, blank line, verbatim or explicit pointer to a
  module **`### Extract`** bullet). [Unallocated] and [Rejected] use the same **`### Extract`**
  pattern.

  Domain-logic (below): markdown list of short bullets, each one a testable rule
  from the book/spec - random draws, comparisons, thresholds, stepped outcomes,
  modifiers, state changes. Skip descriptive prose that does not change outcomes.
-->

# Object sketch - {{project_name}}

Scope: {{e.g. Chapter 1; bounded slice of source context}}
Sources: {{extracted-domain-logic.md if used}}; {{key-abstractions.md if used}}; {{source / spec pointer}}
Seed: {{which file was copied first when materializing this sketch — see object-sketch Agent instructions}}

---

## Module: [{{ModuleName}}]

### Extract

- Source: {{source or doc id}} | Locator: {{section or pointer}}
- Source: {{...}} | Locator: {{...}}
- {{Reason: ...}}  <-- only if this module is intentionally empty

## Domain-logic

{{Domain logic sentences extracted from source (one rule per line; paraphrase or quote tight rule text from the source)}}

- {{e.g. Outcome is decided by comparing a total to a target number; at or above succeeds.}}
- {{e.g. Margin above or below the target is bucketed into discrete levels; fractions truncated.}}
- ...

### {{Concept}}    <-- title case if more than one word

{{Intent}} <--- purpose and responsibility of the concept; which other concepts it works with to fulfil that responsibility and how (2-3 sentences max)

----
{{verb noun phrase}}  <--- natural english language sentences
{{verb noun phrase}}
{{verb noun phrase}}

-----
{{phrase for collaboration / relationship with other concept }}  <--- natural english language sentences
{{phrase for collaboration / relationship with other concept }}

----
Shape hint: {{...}}
Tension: {{...}}  <--    Optional 

#### Core terms 
- {{term}}
- {{term}}

#### Extract - {{title}}
Source: {{where this extract came from - e.g. key-abstractions row, file path, or doc id}}
Locator: {{chapter / section}}
Extract: {{whole | partial}}

{{Verbatim source text - no fenced code block; preserve text as-is for identification.}}

### {{Subtype concept}} *is a type of* {{Base concept}}   <-- plain English generalization (not Colon syntax)

{{Intent}}

----
{{verb noun phrase}}
{{verb noun phrase}}

-----
{{phrase for collaboration / relationship with other concept }}

----
Shape hint: {{...}}
Tension: {{...}}  <-- optional

#### Core terms
- {{term}}
- {{term}}

#### Extract - {{title}}
Source: {{...}}
Locator: {{...}}
Extract: {{whole | partial}}

{{Verbatim source text - or one line pointing at the module ### Extract bullet index that holds the quote.}}

## Module: [Unallocated]

### Extract

- {{parked passages - Source | Locator}}

## Domain-logic

- {{optional rules that apply to parked material}}

## Module: [Rejected]

### Extract

- {{rejected passages - Source | Locator and why rejected in one line if needed}}

## Domain-logic

- {{optional}}
