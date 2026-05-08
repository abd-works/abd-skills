# Corrections log

Project: abd-scenario-walkthrough skill
Source: abd-scenario-walkthrough skill (pipeline runs)

---

## Entry: Engagement prefix on output filename is optional

- **Status:** confirmed
- **Context:** DDD phase output filename
- **DO / DO NOT:** DO default to the bare phase name — `domain-language.md`, `key-abstractions.md`, `domain-sketch.md`, `crc.md`, `object-model.md`, `walkthrough.md`. DO add a `<name>-` engagement prefix only when you need disambiguation: multiple products in the same workspace, or the user asks for it. DO NOT mandate the prefix as the only valid form. The skill template comments now show `[<name>-]<phase>.md` to signal optionality.
- **Example (wrong, mandatory prefix):** Always writing `paw-place-domain-sketch.md` even though the engagement workspace only ever holds one product.
- **Example (correct):** Default to `domain-sketch.md`. If the same workspace also hosts a `barkery-` product line and a `paw-place-` product line, prefix both to disambiguate: `paw-place-domain-sketch.md`, `barkery-domain-sketch.md`.
- **Likely source:** the original skill text required `<name>-<phase>.md` unconditionally; in single-product engagements the prefix was redundant noise.