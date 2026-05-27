# Corrections log — abd-author-practice-skill

## Entry — Purpose referenced previous skill output instead of stating the conceptual gap

- **Context:** `abd-author-practice-skill` rule "Opening sections give outcomes not package mechanics"
- **DO:** State the conceptual problem the practice solves — the gap in understanding, not what pipeline step came before. Purpose should be self-contained: a reader who has never seen the skill pipeline should still understand why the practice matters.
- **DO NOT:** Open Purpose by naming a prior skill's output ("After the Ubiquitous Language…", "Once you have a story map…") as the entry condition. That couples Purpose to pipeline sequencing rather than explaining the practice's value.
- **Example (wrong):** "After the Ubiquitous Language you know *what concepts exist* and roughly *what they do*, but three questions are still open…"
- **Example (correct):** "This skill refines a collection of domain concepts from context and defines each concept's ownership, rejected concerns, collaborators, lifecycle states, and invariants — all in one structured pass."
- **Likely source:** `instruction not read` — the rule caught paths and tooling but did not explicitly call out referencing prior skill outputs as a form of pipeline coupling.

## Entry — Purpose should open with "This skill…" stating what it does and produces

- **Context:** `abd-author-practice-skill` rule "Opening sections give outcomes not package mechanics"
- **DO:** Start Purpose with "This skill…" followed by what it does, what it produces, and how it works — still brief, still one or two paragraphs. The reader should immediately know the skill's function.
- **DO NOT:** Open Purpose with an abstract problem statement or rhetorical framing ("Knowing X is not enough…", "Teams need…") before saying what the skill actually does. Lead with the skill's action, not the gap.
- **Example (wrong):** "Knowing *what concepts exist* and roughly *what they do* is not enough — three questions stay open…"
- **Example (correct):** "This skill refines a collection of domain concepts from context and defines each concept's ownership, rejected concerns, collaborators, lifecycle states, and invariants — all in one structured pass."
- **Likely source:** `unclear expectation` — the rule said "outcome language" but did not specify that Purpose should lead with the skill as subject.

## Entry — Purpose described output format instead of what the practice gives the team

- **Context:** `abd-author-practice-skill` rule "Opening sections give outcomes not package mechanics"
- **DO:** Describe what the practice gives the team — shared understanding, decisions made, risks surfaced, agreements reached — not the shape of the deliverable. Purpose is about value, not format.
- **DO NOT:** Describe the output structure in Purpose ("Each concept gets a block with fields X, Y, Z…", "The output is a scannable record…"). Format belongs in Core concepts, Build, or templates.
- **Example (wrong):** "Each concept gets a CRC block that locks down what it is responsible for, what it explicitly refuses, and which other concepts it works with, then extends that block with state transitions and declarative constraints when the concept carries state."
- **Example (correct):** "The result is a shared understanding of every concept's authority and boundaries: what each one owns, what it must not own, who it depends on, how it changes over time, and what must always remain true. Teams use this to catch misplaced responsibilities, surface hidden coupling, and agree on lifecycle rules before anyone writes code or walks a scenario."
- **Likely source:** `unclear expectation` — the rule distinguished mechanics from outcomes but did not explicitly separate output format from team value.

## Entry — Corrections not logged automatically when output was fixed

- **Context:** `abd-author-practice-skill` IDE rule and `execute-rules-gate` workspace rule
- **DO:** Log the correction entry to `<target-skill>/corrections-log.md` **in the same turn** you fix the output. Every time the user points out a problem and you fix it, that is a correction — log it immediately without being asked.
- **DO NOT:** Fix the output and then wait for the user to say "correction?" or "log it" before writing the entry. The log is part of the fix, not a separate request.
- **Example (wrong):** User says "don't talk about format blocks", assistant rewrites the paragraph but does not touch corrections-log.md until user asks "correction?"
- **Example (correct):** User says "don't talk about format blocks", assistant rewrites the paragraph AND appends a corrections-log entry in the same turn.
- **Likely source:** `instruction not read` — the rule said to log corrections but did not say "in the same turn" or "do not wait to be asked".

## Entry — "When to use" used front-matter state check coupled to another skill's output

- **Context:** `abd-author-practice-skill` rule "Opening sections give outcomes not package mechanics"
- **DO:** Write "When to use" triggers as situations the reader recognizes — conceptual conditions about the domain or the user's intent, not file-level preconditions tied to another skill's output marker.
- **DO NOT:** Use another skill's front-matter state value (e.g. `state: ubiquitous-language`) as a "When to use" trigger. That couples this skill's entry condition to another skill's implementation detail.
- **Example (wrong):** "The module file's front matter shows `state: ubiquitous-language`."
- **Example (correct):** "You have a set of domain concepts with behaviors identified but ownership, boundaries, and lifecycle rules are not yet explicit."
- **Likely source:** `unclear expectation` — the rule prohibited paths and pipeline mechanics but did not explicitly call out front-matter state checks as a form of tight coupling.
