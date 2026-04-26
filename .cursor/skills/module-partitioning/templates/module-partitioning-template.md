<!--
  Module Partitioning — verbatim source allocation by module.

  Copy to: <workspace>/abd-ooad/module-partitioning.md

  Contract:
    - Modules are flat by default; nest with ### only when the source itself
      supports a real sub-module (own bounded scope, own extract set).
    - Every meaningful chunk of source is allocated to exactly one of:
        a named module, ## [Unallocated], or ## [Rejected].
    - Source text inside fenced ```source blocks is VERBATIM — no edits,
      no paraphrase, no reformatting. The `[…]` marker on its own line is
      the only allowed editorial mark for an explicit gap, and the gap
      MUST be described in the `Part:` header line.
    - Every extract gets a header block. Whole vs partial is mandatory;
      `Part:` is mandatory when partial; `Reason:` is mandatory in
      Unallocated and Rejected.

  Module names use [Brackets] in the heading and DO NOT have a "module"
  suffix (e.g. `## [Combat]`, not `## [Combat module]`). Reserved names:
  `## [Unallocated]` and `## [Rejected]` — top-level only, never nested.

  ============================================================================
  WHERE INFORMATION LIVES (front matter vs. per-module sections)
  ============================================================================
  The file front matter is intentionally **thin**: source pointer + counts.
  Do **not** place per-module descriptions, scope statements, term lists,
  rationale, or "module list" prose in the front matter. Every piece of
  information about a particular module lives **inside that module's
  section**, under its own heading.

  Each module section has the same shape, in this order:
    1.  ## Module: [{{Name}}]                  — the heading
    2.  Scope: ...                             — one or two sentences,
                                                 source-grounded, what the
                                                 module covers (and, if useful,
                                                 what it does NOT cover).
    3.  **Core terms**                         — bullet list of source-grounded
                                                 noun phrases that appear
                                                 inside this module's extracts.
                                                 No targets, no values, no
                                                 stereotypes, no evidence IDs,
                                                 no Notes labels — those belong
                                                 to term-registry, not here.
    4.  **Extract — ...**                      — one or more verbatim extracts.

  If you find yourself writing a paragraph in the front matter that explains
  what a particular module is about, stop and move it under that module's
  heading instead.
-->

# Module Partitioning — {{project_name}}

Source: {{corpus root or scan-map reference}}
Top-level modules: {{N}}     Unallocated: {{count}}     Rejected: {{count}}

---

## Module: [{{ModuleName}}]

Scope: {{one or two source-grounded sentences — what bounded scope this module covers, and (if useful) what it explicitly does NOT cover. Keep it tight.}}.

**Core terms** (source-grounded noun phrases that appear inside this module's extracts):

- {{noun phrase the source uses}}
- {{noun phrase the source uses}}
- {{noun phrase the source uses}}
- …

**Extract — {{short title}}**
Source: {{chunk_id_or_file}} — "{{section_path}}"
Locator: {{precise locator: chapter / page / lines / code range / etc.}}
Extract: whole

```source
{{verbatim text — copy bytes from the source, do not edit, do not paraphrase}}
```

**Extract — {{short title}}**
Source: {{chunk_id_or_file}} — "{{section_path}}"
Locator: {{precise locator}}
Extract: partial
Part: {{which slice of the source was copied — e.g. "paragraphs 1–2 of 'Refund Eligibility' subsection", "the three-bullet list under 'The following limits apply to outbound wires:'", "lines 14–22 of the chunk"}}
Also relates to: [{{OtherModule}}] — {{one-line why this allocation is contested}}

```source
{{verbatim slice — preserve original line breaks, bullets, page numbers, OCR artifacts}}
[…]
{{continuation, if there is an explicit gap; describe the gap in the `Part:` line above}}
```

---

## Module: [{{AnotherModule}}]

Scope: {{source-grounded one-liner — what this module covers}}.

**Core terms** (source-grounded noun phrases that appear inside this module's extracts):

- {{noun phrase}}
- {{noun phrase}}
- …

**Extract — {{short title}}**
Source: {{chunk}} — "{{section path}}"
Locator: {{locator}}
Extract: whole

```source
{{verbatim text}}
```

---

<!--
  NEST ONLY WHEN THE SOURCE SUPPORTS A REAL SUB-MODULE.
  A sub-module needs its own bounded scope and its own extract set; if you
  cannot describe its scope in one source-grounded sentence, collapse the
  nesting and keep the parent flat.
-->

## Module: [{{NestedParent}}]

Scope: {{source-grounded one-liner for the parent module}}.

**Core terms** (source-grounded noun phrases for the parent's own extracts):

- {{noun phrase}}
- …

### [{{NestedChild}}]

Scope: {{source-grounded one-liner for the sub-module}}.

**Core terms** (source-grounded noun phrases for the sub-module's own extracts):

- {{noun phrase}}
- …

**Extract — {{short title}}**
Source: {{chunk}} — "{{section path}}"
Locator: {{locator}}
Extract: whole

```source
{{verbatim text}}
```

---

## Module: [Unallocated]

**Core terms**: *n/a — Unallocated extracts are pending an allocation decision; their terms will be captured under whichever module receives them.*

(If empty, replace this comment with a one-line note explaining why, e.g. "Every meaningful section landed cleanly on first pass.")

**Extract — {{short title}}**
Source: {{chunk}} — "{{section path}}"
Locator: {{locator}}
Extract: whole
Reason: {{why no module fits yet — e.g. "spans Combat and Powers; revisit after Ch. 8 pass"}}

```source
{{verbatim text}}
```

---

## Module: [Rejected]

**Core terms**: *n/a — Rejected extracts are intentionally out of scope; their terms are not part of the domain model.*

(If empty, replace this comment with a one-line note explaining why, e.g. "No front matter in this corpus.")

**Extract — {{short title}}**
Source: {{chunk}} — "{{section path}}"
Locator: {{locator}}
Extract: whole
Reason: {{why out of scope — e.g. "Front matter — no rules, no domain terms", "Setting/lore prose — out of scope for a rules-domain partition"}}

```source
{{verbatim text}}
```

---

<!--
  WORKED EXAMPLE — minimal, illustrative. Drawn from a payments / banking
  domain — chosen to be DELIBERATELY DIFFERENT from the corpus you are
  partitioning, so the example illustrates the structure rather than
  prescribing answers for any specific source.

  ## Module: [Funds Transfer]

  Scope: how an instruction to move funds from one account to another is
  validated, executed, and reconciled. Covers the underlying transfer
  mechanism shared by every named transfer product.

  **Core terms** (source-grounded noun phrases that appear inside this module's extracts):

  - funds transfer
  - source account / destination account
  - debit / credit
  - reconciliation
  - Wire Transfer
  - ACH Transfer

  **Extract — Funds Transfer (overview)**
  Source: PaymentsRulebook__section_03 — "Funds Transfer"
  Locator: Ch.3 §Funds Transfer
  Extract: whole

  ```source
  A funds transfer moves a specified amount from a source account to a
  destination account in a single atomic operation. Every transfer:
  - Debits the source account by the transfer amount.
  - Credits the destination account by the transfer amount.
  - Records a matched debit/credit pair on the ledger for reconciliation.
  …
  A transfer that cannot be matched within the reconciliation window is
  escalated to the exceptions desk.
  ```

  ## Module: [Rejected]

  **Core terms**: *n/a — Rejected extracts are intentionally out of scope.*

  **Extract — Cover / Disclosures / ToC**
  Source: PaymentsRulebook__section_00 — "Cover / Regulatory Disclosures / Table of Contents"
  Locator: Front matter
  Extract: whole
  Reason: Front matter — regulatory disclosures and table of contents; no domain rules, no terms; out of scope for a rules-domain partition.

  ```source
  …front-matter text copied verbatim…
  ```
-->
