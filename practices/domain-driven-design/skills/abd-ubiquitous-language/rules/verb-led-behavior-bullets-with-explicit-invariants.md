# Rule: Concept bullets tell the concept's story; invariants are explicit

**Scanner:** Manual review

Every concept block carries bullets that tell the concept's story naturally — what it is for, what it owns, how it relates to other concepts, what it does, what must always be true. Bullets can express any of those aspects; they are not restricted to behavior only. The active-verb test applies: the implicit subject ("a *concept*") should naturally start the sentence with a verb. Rules that must always hold are separate `**Invariant:**` bullets. Failing means a concept has only noun-style label bullets, or an invariant is buried inside a bullet without the marker.

## DO

- Write bullets in whatever order tells the concept's story naturally — role, boundary, relationships, responsibilities, rules. The implicit subject starts with an active verb.

  **Example (pass):**
  ```
  ### check
  - is made *using* the *trait* of a *character*
  - is resolved by *rolling* a *d20*, comparing the *roll total* to the *difficulty class*,
    producing a *check result*
  ```

- Use `**Invariant:**` for rules that must always hold.

  **Example (pass):**
  ```
  ### rank
  - is a single numeric value carried by a *trait*
  - **Invariant:** *ranks* must never be added directly; convert to *measures* first
  ```

## DO NOT

- Write noun-style bullets when active-verb form is available.

  **Example (fail):**
  ```
  ### check
  - the check mechanic
  - d20 plus trait rank vs DC
  ```

- Bury an always-true rule inside a behavior bullet without the `**Invariant:**` marker.

  **Example (fail):** `- is a numeric value, and ranks must never be added directly`

**Source:** Inherited from abd-ubiquitous-language — active-verb test and invariant marker.
