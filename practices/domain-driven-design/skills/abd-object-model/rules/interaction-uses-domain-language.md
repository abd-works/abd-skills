# Rule: Interaction variable names use domain language

**Scanner:** Manual review

Variable names inside an `Interaction:` block must use domain language drawn from the ubiquitous language, Ubiquitous Language, or CRC — not generic technical placeholders. If a name is ambiguous, trace up the chain: CRC responsibility → Ubiquitous Language → ubiquitous language → source references.

## DO

- Name variables after the domain concept they represent.

  **Example (pass):** Resolving a check:
  ```
  roll: Integer = d20.roll()
  total: Integer = trait.rank + roll + circumstanceModifier.value
  success: Boolean = total >= dc.value
  margin: Integer = total - dc.value
  result: CheckResult = new CheckResult(rollTotal: total, dc: dc, isSuccess: success, margin: margin)
  ```

  **Example (pass):** Converting ranks to measures and back:
  ```
  throwingDistanceMeasure: Number = Measurement.lookup(rank: strengthRank, type: THROWING_DISTANCE).value
  massMeasure: Number = Measurement.lookup(rank: massRank, type: THROWING_DISTANCE).value
  combined: Number = throwingDistanceMeasure - massMeasure
  throwingDistanceRank: Rank = Measurement.rankFor(measure: combined, type: THROWING_DISTANCE)
  return throwingDistanceRank
  ```

## DO NOT

- Use generic placeholders that could mean anything.

  **Example (fail):**
  ```
  measureA: Number = Measurement.lookup(rank: this, type: type).value
  measureB: Number = Measurement.lookup(rank: other, type: type).value
  ```
  `measureA` and `measureB` say nothing about what is being measured. Name them after the domain quantities: `strengthMeasure`, `massMeasure`, `travelDistanceMeasure`, etc.

- Use single-letter names, index names, or temp/result/data patterns.

  **Example (fail):**
  ```
  r: Integer = d20.roll()
  t: Integer = trait.rank + r
  res: CheckResult = getResult(t)
  ```

## When names are unclear

Trace up the chain:
1. Check the CRC responsibility name and its collaborator names
2. Check the Ubiquitous Language description of the behavior
3. Check the ubiquitous language definition
4. Check the source references

The right name is almost always already in the source material.

**Source:** Engagement convention (object-model skill).
