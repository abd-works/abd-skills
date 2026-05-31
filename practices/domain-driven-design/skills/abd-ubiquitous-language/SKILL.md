---
name: abd-ubiquitous-language
catalog_garden_tier: practice
catalog_garden_order: 3
catalogue_one_liner: >-
  Shared vocabulary with concept behavior in one file; terms, KAs, and concept blocks.
description: >-
  Build a shared, rigorous vocabulary for the scope you are modeling — extract
  terms, group them into Key Abstractions, and sketch each concept's behavior —
  all in one file every downstream artifact can rely on.
  Use when the user asks to "build the ubiquitous language", "extract domain terms",
  "identify Key Abstractions", "sketch the domain", or when a scope has source material
  but no agreed vocabulary or concept sketch yet.
---
# abd-ubiquitous-language

## Purpose

Build a shared, rigorous vocabulary for the scope you are modeling so that domain experts and modelers agree on what each term means, what each concept does, and which rules must always hold — and capture that agreement in **one** living document the whole team uses without translation. The scope of one run can be a single module, several modules, or a whole-system sweep; the skill and its output shape stay the same.

This is a three-pass skill. It reads source, extracts terms with definitions, groups them into Key Abstractions, sketches each concept's behavior and properties, and writes **one** file. The final output is a robust domain model that describes domain concepts in a structured, plain-English form — before anyone commits to classes, methods, or properties.

---

## Output file

**Deliverables folder:** see `../agent-protocol.md` — Output file resolution.

**File name:** `ubiquitous-language.md`. Add a `<name>-` prefix only when disambiguation is needed. For multi-module engagements: `<deliverables-folder>/modules/<module-name>-ubiquitous-language.md`. When the scope spans more than one module in a single file, organize with `# Module: [ModuleName]` sections.

---

## Agent Instructions

> **MANDATORY — read `../agent-protocol.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — ubiquitous language, terms, KAs, concepts, two tests, three outcomes, modeling decisions (concept vs subtype vs property vs instance), italicized-term resolution, decisions/references per KA, three passes, and the consistent file shape.
- **`../../reference/oo-concepts.md`** — OO fundamentals (what is a class, inheritance and subtypes). Read the **`### Inheritance and subtypes`** section before classifying terms. **Do not** read or apply `### Decomposing responsibilities` — that applies at CRC stage and beyond.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Produce output from every template:**

| Template | What to produce |
| --- | --- |
| `templates/ubiquitous-language-template.md` | The ubiquitous language file with Terms list, KA intros, concept blocks, decisions, and references. |
| `templates/domain.json` | Domain JSON with concept names, attributes, and inheritance. |

**Quality bar:** Every KA intro opens with "*KAName* is …". Every concept has verb-led behavior bullets. Every `*italicized*` term resolves to a heading, stub, or parenthetical primitive. One `#### Decisions made` and one `#### References` per KA, after all concept blocks. State marker set to `ubiquitous-language`.

### 3. Validate

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-ubiquitous-language \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../agent-protocol.md`.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers.

- **One file** — named `[<name>-]ubiquitous-language.md`. No separate domain-language or key-abstractions files alongside.
- **Each KA anchors at least 3–5 terms** — subordinate concepts, subtypes, and properties included. A KA with fewer than three terms is not a KA; merge it under an existing KA or downgrade it to a subordinate concept.
- **State marker** — front matter reads `state: ubiquitous-language`.
- **Terms list in header** — a single hierarchical `**Terms**` list.
- **Every KA has an intro paragraph** — opens with "*KAName* is …".
- **Every KA's own concept appears first** — the first `### concept` under each `## KA` matches the KA name.
- **Every concept has verb-led behavior bullets** — active voice; the concept is the subject.
- **Domain terms italicized** — every domain term in bullets, invariants, and KA intro paragraphs.
- **Italicized terms resolve** — every `*italicized*` term resolves to a heading, stub, or parenthetical primitive.
- **No bold on headings** — `## KAName`, `### concept`, and subtype headings carry no bold.
- **One `#### Decisions made` per KA** — after all concept blocks.
- **One `#### References` per KA** — after `#### Decisions made`.
- **Boundary entries have a single named owner** — `Owned by: ModuleName`.
- **Properties with independent behavior visible** — properties that have their own invariants, behavior, or interactions get a `###` stub; properties that are only "a property of X" are mentioned in the parent concept's bullets only.
- **No premature design commitments** — no UML stereotypes, typed properties, method signatures, or cardinality notation.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
