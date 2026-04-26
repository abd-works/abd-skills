---
name: properties-methods-and-relationships
description: >-
  Produce domain-model.md: properties, operations with types, relationships and
  cardinality per skills/ooad/content/parts/phases/properties-methods-and-relationships.md.
  Layout and Example in skills/ooad/templates/domain model template.md — module
  blurb, grouped properties/methods with ---- clusters, ----- between classes,
  Invariant lines tabbed under members, UPPER_CASE typed constants, explicit
  Child : Parent subtypes. Input: crc.md, business-logic.md, domain-walkthrough.md,
  object-sketch.md. Output: abd-ooad/domain-model.md.
---

# properties-methods-and-relationships

## Purpose

Convert CRC responsibilities into a **typed** domain surface in **`domain-model.md`**:

1. **Properties** - what the object must know to fulfil its responsibility.
2. **Operations** - `methodName(param: Type): ReturnType`.
3. **Relationships** - composition vs association, cardinality (`1..1`, `0..*`, etc.).

Use **`business-logic.md`** to inform operations and properties that **enforce invariants** or **encode state**. Put **declarative invariant lines** (tab-indented, `Invariant: ...`) **under the property or method** they constrain, per **`domain model template.md` Example**. Prefer a short invariant at the member; keep long lifecycle prose in **`business-logic.md`**.

## Inputs / outputs

| Input | Output |
| --- | --- |
| `crc.md`, `business-logic.md`, `domain-walkthrough.md`, `object-sketch.md` | `abd-ooad/domain-model.md` |

## Layout

Follow **`skills/ooad/templates/domain model template.md`** (read the **Conventions** and **Example** there):

- `## [Module: name]` plus a short module paragraph.
- `ClassName << Entity? >>` or `<< ValueObject? >>` as needed; optional `Child : Parent`.
- **`----`** separates **clusters** inside a class (related properties + their methods).
- **`-----`** separates **whole classes**.
- **Typed constants / enum-like sets:** group name + `UPPER_CASE` names and values.
- **Ignore** the template's **Note labels by tag** table and optional `note:` / `[pN]` lines unless the user opts in.

**Source in this artifact:** If you inline identification quotes, use **`#### Source`** before verbatim text (same collapsible convention as **object-sketch**). Do not default to fenced **source** blocks.

## Rules

- Work **properties first**, then operations, then relationships (same phase doc).
- No UI, infrastructure, or pure application orchestration on domain types unless explicitly domain.

## Templates

`templates/domain-model-scaffold.md`

## Validate

- Every CRC class with a typed surface has properties justified by its **Responsible for** / **`responsible:`** line.
- Every relationship has two ends and cardinality where modeled.
- Walkthrough scenarios can still be stepped with the new names (spot-check).

---

<!-- execute_rules:bundle_rules:begin -->
<!-- No rules/*.md for this skill yet. -->
<!-- execute_rules:bundle_rules:end -->
