# Rule: Many-to-many association signals a new first-class concept

**Scanner:** Manual review

When the Domain Language implies that two concepts each relate to *many* of the other (mutual many-to-many), the association itself usually needs a first-class concept with its own responsibilities — not only reciprocal collaborator lists on the two end cards. The classic signal is two entities pointing at each other with "has many" behavior on both sides (for example student–course enrollment).

## DO

- Introduce a linking concept that owns the association lifecycle, constraints, and facts that belong to the pairing — not to either end alone.

  **Example (pass):** `Student` enrolls in `Course` and `Course` has many students → add `Course Enrollment` (or domain-equivalent name) that owns enrollment date, status, seat assignment, grades — whatever the domain attaches to *this student in this course*.

- Place responsibilities that concern only the pairing on the new concept; keep the end concepts focused on their own identity and rules.

## DO NOT

- Model many-to-many only as symmetrical responsibilities on the two ends when the domain language or sketch implies facts and behavior on the link itself.

  **Example (fail):** `Student` lists `courses | Course` and `Course` lists `students | Student` with duplicated enrollment rules split across both cards and no concept for the enrollment fact.

**Source:** Engagement convention (class-responsibility-collaborator skill).
