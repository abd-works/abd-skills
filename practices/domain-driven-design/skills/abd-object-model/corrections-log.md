﻿# Corrections log

Project: abd-object-model skill
Source: abd-object-model skill (pipeline runs)

---

## Entry: Engagement prefix on output filename is optional

- **Status:** confirmed
- **Context:** DDD phase output filename
- **DO / DO NOT:** DO default to the bare phase name — `domain-language.md`, `key-abstractions.md`, `ubiquitous-language.md`, `crc.md`, `object-model.md`, `walkthrough.md`. DO add a `<name>-` engagement prefix only when you need disambiguation: multiple products in the same workspace, or the user asks for it. DO NOT mandate the prefix as the only valid form. The skill template comments now show `[<name>-]<phase>.md` to signal optionality.
- **Example (wrong, mandatory prefix):** Always writing `paw-place-ubiquitous-language.md` even though the engagement workspace only ever holds one product.
- **Example (correct):** Default to `ubiquitous-language.md`. If the same workspace also hosts a `barkery-` product line and a `paw-place-` product line, prefix both to disambiguate: `paw-place-ubiquitous-language.md`, `barkery-ubiquitous-language.md`.
- **Likely source:** the original skill text required `<name>-<phase>.md` unconditionally; in single-product engagements the prefix was redundant noise.