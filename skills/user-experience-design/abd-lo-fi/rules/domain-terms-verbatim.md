# Rule: Domain terms appear on the canvas verbatim

**Scanner:** AI review

Every domain term on the wireframe — label, region name, affordance name, anchored definition — is copied character-for-character from the ubiquitous-language (UL) file. Paraphrasing, shortening, capitalising differently, or rewording the definition is a fail.

## DO

- Copy term names exactly as the UL spells them.

  **Example (pass):** UL defines `COH game directory` — the canvas shows `COH game directory` as the input label, with the same casing and spacing.

- Where the prompt embeds term definitions, copy the entire definition body verbatim.

  **Example (pass):**
  ```
  - COH game directory — the file-system path to the City of Heroes installation,
    validated at startup; provides the root path for the COH data directory
    where the crowd repository JSON file is stored; ...
  ```

## DO NOT

- Paraphrase, shorten, or summarise the term.

  **Example (fail):** UL defines `COH game directory` — canvas shows `Game folder`, `COH path`, `City of Heroes folder`, or `COH dir`.

- Reword the definition while keeping the term name.

  **Example (fail):** UL definition starts with "the file-system path to the City of Heroes installation, validated at startup" — canvas summary reads "the install path checked when the app starts". Even if technically correct, this is a fail.

- Re-capitalise or sentence-case a term that the UL writes lowercase.

  **Example (fail):** UL writes `crowd manager` (lowercase) — canvas shows `Crowd Manager` or `CrowdManager`.
