---
scanner: story-sizing
---

# Rule: Stories have 4–9 acceptance criteria (heuristic)

**Priority:** 2  
**Scanner:** `scanners/story-sizing-scanner.py` — **`StorySizingScanner`**

Stories should have enough acceptance criteria to reflect thorough exploration. The **mechanical** scanner counts **WHEN** + **AND** tokens across all AC text (see agile_bots implementation). Target band in JSON: **4–9**; scanner implementation may use a **4–10** band — treat JSON as product intent and align scanner when reconciling.

## DO

- Target enough AC to cover the behavior (happy path, errors, edges).
- Split stories that grow too large.
- Expand under-explored stories.

## DON'T

- Pad with trivial or redundant AC.
- Leave stories severely under-specified or monolithic.
