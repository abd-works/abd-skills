---
scanner: refs-per-term
---

# Rule: Refs per term — every term must carry at least one Ref entry

**Scanner:** `scanners/refs-per-term-scanner.py` — **`RefsPerTermScanner`**

Every `###` term heading in the module file must be followed by at least one full-format Ref entry (`**Ref — …**` with `Source:`, `Locator:`, `Extract:` lines) before the next `###` heading. Refs are allocated per term under `#### References`, not collected in a separate inventory.

## DO

- Place `#### References` with Ref entries directly after the behavioral lines of each term.

  **Example (pass):**
  ```
  ### check

  - A check is d20 + trait rank vs DC; equal or above is success.

  #### References

  **Ref — Game Play**
  Source: context/rules/HeroesHandbook-rules__chunk_009.md
  Locator: lines 809–874
  Extract: whole
  ```

- Use the full format for every Ref: `**Ref — title**`, `Source:`, `Locator:`, `Extract:`.

- Ensure every term — Core terms and boundary terms — has at least one Ref.

## DO NOT

- Collect Refs in a separate inventory section at the top or bottom of the file — they belong with the term they evidence.

  **Example (fail):** A `## References` section at the end lists all Refs by chunk number, with no connection to individual terms.

- Leave a term with behavioral lines but no Ref entry — every behavioral claim must be traceable.

  **Example (fail):** `### routine check` has three behavioral lines but no `#### References` section beneath them.

- Use an abbreviated inline format instead of the full format.

  **Example (fail):** `Refs: chunk_004 (lines 202–243)` — missing `Source:`, `Locator:`, `Extract:` structure.
