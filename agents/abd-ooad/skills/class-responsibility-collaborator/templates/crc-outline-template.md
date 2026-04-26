<!--
  crc.md — domain outline style (CRC fidelity).

  Copy to: <workspace>/abd-ooad/crc.md

  Mirrors bots/crc_bot/.../domain_outline.md: one module header, then concepts
  as names; responsibilities indented under each concept. CRC uses three labeled
  lines instead of a single responsibility:collaborators line.
-->

## Module: [{{ModuleName}}]

{{ConceptName}}
    responsible: {{one sentence — what this concept owns}}
    not_responsible: {{deliberate exclusions — at least one plausible wrong owner}}
    collaborators: {{TypeA, TypeB, ...}}

{{SubtypeName}} : {{BaseConcept}}
    responsible: {{full sentence or delta vs base}}
    not_responsible: {{...}}
    collaborators: {{...}}

---

## Module: [{{AnotherModule}}]

{{ConceptName}}
    responsible: {{...}}
    not_responsible: {{...}}
    collaborators: {{...}}

---

Instructions:

- Group concepts by module; module names match `object-sketch.md` `## Module: [Name]` when present.
- One concept name per block (no `###` heading — the name is the first line, like domain outline).
- Subtype / generalization: `ChildConcept : ParentConcept` on the first line of that block.
- `collaborators:` lists other domain concepts this one works with (from sketch `uses` / edges).
- English only; no operation signatures (those belong in properties-methods-and-relationships).
- Omit lifecycle and declarative invariants here — use **elaborate-business-logic** / `business-logic.md`.
