<!--
  key-abstraction-identification — Key Abstractions, sub-allocating verbatim source.

  Copy to: <workspace>/abd-ooad/key-abstractions.md

  Contract:
    - `module-partitioning.md` is OPTIONAL. When present: one `## Module: [Name]`
      per partition module, partition order, one-for-one. When absent: use
      `## Key Abstraction:` under the H1 and/or a few lightweight `## Module:`
      groupings if helpful — do not block on partitioning.
    - Under each module (when used), `### Resolutions` (settle pass) then
      `### Key Abstraction: Name` sub-sections in settled order.
      A Key Abstraction lives in exactly one module when modules exist.
    - Every Key Abstraction carries: Intent (one source-grounded sentence),
      Core terms (bullets — from partition list when you have it, else from
      source), Shape hint (free-form prose — never a `<<Tag>>`), optional
      Tension, and at least one `**Extract — ...**` with verbatim source.
    - Multi-subject passages: break the upstream extract into pieces; each piece
      is its own `**Extract — ...**` under the **one** Key Abstraction (concept)
      it supports (`Extract: partial`, `Part:`). Repeat the same `Source:` on
      each partial so reviewers can find all pieces — no separate index heading.
    - Optional `## [Unallocated]` at end of file, rare, with `Reason:`.
    - Source bodies inside ```source blocks are VERBATIM — no paraphrase,
      cleanup, or reformatting. `[…]` on its own line is allowed for an
      explicit gap; describe it in `Part:`.

  NO CLASS-LEVEL COMMITMENTS AT THIS RUNG:
    - No stereotypes, typed properties, method signatures, cardinality arrows,
      super/sub splits (taxonomy may sit inside one abstraction), or
      cross-module relationship arrows — Tension notes only.

  ============================================================================
  WHERE INFORMATION LIVES (front matter vs. per-abstraction sections)
  ============================================================================
  Front matter stays thin: source pointer(s) + counts. Put abstraction detail
  only under `### Key Abstraction:` blocks.
-->

# Key Abstractions — {{project_name}}

Source: {{module-partitioning.md at `{{path}}` when used; else note corpus roots}}
Modules: {{N or 0}}     Key Abstractions: {{K}}

---

## Module: [{{ModuleName}}]

*Scope (optional one-liner): {{tight note — from partition or your grouping.}}*

### Resolutions

- **Merge / Split / Promotion / Demotion:** {{none, or each logged with Evidence:}}
- {{Each closed draft Tension from identification — Evidence:}}
<!-- Optional before first Key Abstraction: ### Deferred tensions — only when a tension cannot close on module-internal evidence. -->

### Key Abstraction: {{KAName}}

Intent: {{one source-grounded sentence — do NOT borrow another abstraction's Core terms to make the sentence work.}}.

Core terms (absorbed from this module's Core terms list, or from source if no partition):

- {{noun phrase}}
- {{noun phrase}}
- …

Shape hint: {{free-form prose — never a `<<Tag>>`.}}.

Tension: {{optional — omit if none.}}.

**Extract — {{short title}}**
Source: module-partitioning.md — Module: [{{ModuleName}}] — "{{partition extract title}}"
Locator: {{e.g. Ch.1 §The Core Mechanic}}
Extract: whole

```source
{{verbatim text — byte for byte from module-partitioning.md or corpus}}
```

**Extract — {{short title}}**
Source: module-partitioning.md — Module: [{{ModuleName}}] — "{{partition extract title}}"
Locator: {{partition locator}}
Extract: partial
Part: {{which slice — e.g. first paragraph only, lines 9–14}}

```source
{{verbatim slice}}
```

---

### Key Abstraction: {{AnotherKAName}}

Intent: {{one source-grounded sentence}}.

Core terms:

- {{noun phrase}}
- …

Shape hint: {{free-form prose}}.

**Extract — {{short title}}**
Source: module-partitioning.md — Module: [{{ModuleName}}] — "{{partition extract title}}"
Locator: {{partition locator}}
Extract: whole

```source
{{verbatim text}}
```

---

## Module: [{{AnotherModule}}]

(Repeat: `## Module:` then `### Key Abstraction:` sections in source order.)

---

## [Unallocated]

<!--
  OPTIONAL — rare. Only slices you truly cannot place after cutting; each
  extract needs `Reason:`.
-->

---

<!--
  WORKED EXAMPLE (comment only) — payments/banking, illustrative.

  ## Module: [Funds Transfer]

  ### Key Abstraction: Funds Transfer
  … overview extract whole …

  **Extract — Module opener (partial)**
  Source: … "Funds Transfer module opener"
  Extract: partial
  Part: sentences on generic transfer / reconciliation

  ### Key Abstraction: Wire Transfer
  …

  **Extract — Module opener (partial)**
  Source: … "Funds Transfer module opener"  (same Source as sibling)
  Extract: partial
  Part: sentences on wires / KYC
-->
