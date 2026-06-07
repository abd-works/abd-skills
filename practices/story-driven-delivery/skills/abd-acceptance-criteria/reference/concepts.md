# Acceptance Criteria — Core Concepts

## What are acceptance criteria?

**Acceptance criteria** (in this skill's sense) are **story-level, behavioral statements** that say **under what conditions** the product behaves **how**, including chained outcomes and explicit negatives. They sit **above** BDD **scenarios** (which use Given/When/Then on steps).

Exploration-phase AC answer four questions for each story:

1. **When** does the behavior apply? (trigger, precondition, or variant.)
2. **Then** what is observable? (primary user- or system-visible outcome.)
3. **And** what else happens in sequence? (extra outcomes, especially multiple system reactions — chain with AND, not a new WHEN for each micro-step unless the trigger truly changes.)
4. **But** what must **not** happen? (errors, prevention, no persistence — negative paths.)

They are **not** implementation checklists (API names, class names, file formats) unless the story is explicitly `story_type: technical` and scoped that way. A good AC set can be read by a **product owner**, a **tester**, and a **developer** — all at once — and still be **machine-checkable** via rules/scanners where applicable.

**Relationship to other artifacts:**

| Artifact | Role | Typical keywords |
| --- | --- | --- |
| **acceptance_criteria** (this skill) | Story-level outcomes in the graph | WHEN, THEN, AND, BUT |
| **scenarios** (later / other workflow) | BDD flows with steps | Given, When, Then on **steps** |

Reserve **Given** for **scenarios**, not for lines inside **`acceptance_criteria`** (exploration convention).

---

## Step

AC describe **observable** user/system behavior in steps. Avoid implementation detail unless the story is explicitly technical.

- **WHEN** sets scope; **THEN** is the main observable.
- **AND** chains extra outcomes.
- **BUT** guards negatives.
- Second AC is a **delta** (error or other path), not a full repeat of the happy path.
- Language stays **behavioral**, **channel-aware** where the product has distinct surfaces, and **system-aware** when interacting with multiple system actors.

- **Prefer** language a product owner can rehearse: who did what, on which surface, and what anyone can see or verify next.
- **Prefer** channel-specific detail when the product has more than one surface — real CLI paths, quoted control labels, or API-visible outcomes — so testers know *where* to look.
- **Avoid** vague reassurance ("the system handles it") with no observable signal.
- **Never describe capability** ("the customer can override"). AC describe **state**: something is displayed, shown, provided, or available.

## Domain terms (vocabulary in AC)

**Domain terms** are words or short phrases that name the important ideas in the problem space: things (*Settlement File*, *Import Job*), their **state** (*Queued*, *Committed*), **actions** (*Confirm import*), and **rules or constraints** (*Schema Validation*, *Transactional Limit*). They align story AC with how stakeholders talk and with how tests will read — part of a shared **Domain Language**.

- Each story includes a **Domain terms** subsection **before** its acceptance criteria (see template).
- In `acceptance-criteria.md`, use *italics* and *Title Case* inside multi-word phrases in the Domain terms list and in AC lines.
- Do not italicize filler, whole sentences, or low-signal words.

## WHEN / THEN / AND / BUT

- **WHEN:** Trigger or precondition — the event or situation that starts this slice of behavior.
- **THEN:** Primary outcome — what becomes true or visible first.
- **AND:** More outcomes in the same beat — especially a second or third **system** reaction — without inventing a new trigger.
- **BUT:** What **does not** happen — errors, prevention, or "no write" guarantees on negative paths.

## Atomic AC

State the **general** case **once**; follow-on AC only describe **deltas**. Reduces duplicated WHEN/THEN blocks.

## Actor alternation

Interleave user-visible and system-visible emphasis. Avoid long runs of the same actor without switching.

## Domain consistency

As domains grow, keep **parallel** AC structure across related areas; **split stories** when one AC mixes incompatible domain behaviors.

---

## Pitfalls for agents

**Assess context coverage and don't fabricate to fill gaps.** When context is incomplete, do not invent AC — capture the gap, your assumption, and a validation action. See [`../../../reference/handling-incomplete-context.md`](../../../reference/handling-incomplete-context.md) for the shared discipline, including the context dimensions to check before writing AC.
