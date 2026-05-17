### Rule: Walkthrough Example is numbered steps that name participants

The **Walkthrough Example** subsection must be an **ordered list** of steps, with each step naming the participant doing the work and the action taken — not a prose paragraph and not a bullet list. The walkthrough renders the same scenario as the sequence diagram, but in language a reviewer can read aloud while pointing at the diagram. Passing means a reader can pair each numbered step with a `participant` in the sequence diagram. Failing means the walkthrough is one block of paragraphs, uses unordered bullets, or describes "the system" / "the code" instead of naming a participant.

#### DO

- Start each step with the **participant name** in bold or as the subject of the sentence, then the action.

  **Example (pass):** `1. **Controller** validates the request body and calls service.createInvoice(input).`

- Match the number of steps to the messages in the sequence diagram (give or take one for the precondition / outcome).

  **Example (pass):** Sequence diagram has 5 messages; walkthrough has 5 numbered steps plus a 6th line for the user-visible outcome.

- Use an **ordered list** (`1.`, `2.`, `3.`), not an unordered list (`-`, `*`).

  **Example (pass):** Steps are numbered `1.` ... `4.` in markdown source.

#### DO NOT

- Write the walkthrough as a paragraph: "The controller calls the service which then calls the repository, and finally the response is mapped...".

  **Example (fail):** `### Walkthrough Example` body is two paragraphs with no list markers — the reviewer cannot map prose to diagram messages.

- Use the passive voice that hides the actor: "A request is received, validation is performed, and a response is sent".

  **Example (fail):** Step 1 reads "A request is received and validated." — which participant did the receiving? Which did the validating?

- Use bullets (`-`) instead of numbers; bullets imply a set, the walkthrough is a sequence.

  **Example (fail):** `- Controller receives the request` / `- Service is called` — no ordering, no alignment with the sequence diagram.

**Source:** Practice-skill authoring convention (abd-architecture-reference); numbered walkthroughs let a reviewer pair each step against the sequence-diagram message.
