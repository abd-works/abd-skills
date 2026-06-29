# Generate — abd-domain-language

Follow every file in `rules/`; fill templates exactly.

## Read context

Read these files before generating:

- **`reference/concepts.md`** — Domain Language, terms, KAs, concepts, two tests, three outcomes, modeling decisions (concept vs subtype vs property vs instance), italicized-term resolution, decisions/references per KA, three passes, and the consistent file shape.
- **`../../reference/oo-concepts.md`** — OO fundamentals (what is a class, inheritance and subtypes). Read the **`### Inheritance and subtypes`** section before classifying terms. **Do not** read or apply `### Decomposing responsibilities` — that applies at domain model stage and beyond.

**Read `oo-concepts.md` before touching any term. This is not optional.**

## Classify terms — mandatory interactive step

For every term that could be a concept, subtype, property, or instance: **you must ask before you classify**. This step is not optional and is not error-recovery — it is the process.

For each ambiguous term:

1. Use `AskQuestion` to present the viable typing options (concept / subtype of X / property of X / instance of X).
2. Include one sentence of reasoning for each option — why it fits, what it implies.
3. Wait for the user's answer before writing the block.

**Never classify a term by assumption.** "It seemed obvious" is not a valid reason to skip the question. If you are uncertain, you are certain you must ask.

## Output shape

| Template | Deliverable |
| --- | --- |
| `templates/domain-language-template.md` | The Domain Language file with Terms list, KA intros, concept blocks, decisions, and references. |
| `templates/domain.json` | Domain JSON with concept names, attributes, and inheritance. |

## Quality bar

Every KA intro opens with "*KAName* is …". Every concept has verb-led behavior bullets. Every `*italicized*` term resolves to a heading, stub, or parenthetical primitive. One `#### Decisions made` and one `#### References` per KA, after all concept blocks.
