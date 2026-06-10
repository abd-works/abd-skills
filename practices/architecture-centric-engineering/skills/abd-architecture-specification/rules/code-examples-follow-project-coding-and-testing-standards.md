### Rule: Code examples follow the project's coding and testing standards

Every code block inside a `Walkthrough Example` must obey the **coding standard the project has agreed** for production code and the **testing standard the project has agreed** for test code. The reference document does not invent style — it inherits the team's existing guide. When the project uses **abd-clean-code** and **abd-story-acceptance-test**, those are the standards and the samples must follow them. When the project uses a different style guide, project-specific patterns, or a corporate standard, the samples must follow *that*. The reference cites whichever standards apply at the bottom of each mechanism section so a reviewer can find them. Passing means a snippet would survive review under the standard the project actually uses. Failing means a snippet violates the chosen standard, contradicts an in-scope guide, or invents conventions that do not match any agreed source.

#### DO

- Identify the **coding standard in scope** before writing the production-code sample. In an agilebydesign-skills-anchored project this is usually `abd-clean-code` (domain language, small functions, constructor injection, no anemic data bags); in another project it may be a different guide.

  **Example (pass):** The project's `agents/coding-standards.md` says "no service-with-anemic-bag patterns" and the project loads `abd-clean-code`. The Walkthrough Example ships an `InvoiceService` that delegates to entity methods on `Invoice` — no `Manager`, no `process()`, dependencies in the constructor.

- Identify the **testing standard in scope** before writing the test snippet. Default is `abd-story-acceptance-test` (class per story, method per scenario, Given/When/Then helpers, no defensive checks) when the project has it in scope.

  **Example (pass):**
  ```typescript
  class TestInvoiceCreationFailures {
    helper = new InvoiceServerHelper();
    async test_invalid_invoice_returns_422_with_validation_message() {
      await this.helper.givenUserLoggedIn();
      await this.helper.whenUserSubmitsInvoiceWithMissingAmount();
      await this.helper.thenResponseIs422WithMessage('amount is required');
    }
  }
  ```

- Cite the standards used at the bottom of the mechanism section so the reader can find them.

  **Example (pass):** End-of-mechanism line: `Code follows the project's coding standard (abd-clean-code in scope here); tests follow the project's testing standard (abd-story-acceptance-test in scope here).`

- If the project's standard differs from the agilebydesign defaults, **say so explicitly** at the top of the reference so readers know which guide the samples obey.

  **Example (pass):** Below the title: `> Coding standard: company-python-style.md. Testing standard: in-house pytest patterns.`

#### DO NOT

- Ship a code sample that violates the in-scope standard because "this is just an illustration".

  **Example (fail):** Project uses `abd-clean-code`; the sample is
  ```typescript
  export class RecipientManager {
    process(data: any) { /* ... */ }
  }
  ```
  — `Manager` class, `process` method, `any` parameter, no constructor dependencies. Whatever the project's standard is, this violates a clean-code guide.

- Ship a test snippet with defensive `try/catch` or branching assertions when the project's testing standard forbids them.

  **Example (fail):**
  ```typescript
  try {
    const r = await svc.createInvoice(input);
    if (r.ok) expect(r.value).toBeDefined();
  } catch (e) { /* ignore */ }
  ```
  — defensive try, conditional assertion, swallowed exception. Violates `abd-story-acceptance-test` (and any sensible testing guide).

- Pick conventions out of thin air when the project has no documented standard yet.

  **Example (fail):** The project has no coding-standards document and no clean-code skill. The reference's samples use a `Service` + anemic `Recipient` interface and rationalize it as "industry standard". The team has no way to peer-review against an agreed source — pause and agree a coding standard before authoring code samples.

**Source:** Practice-skill authoring convention (abd-architecture-specification). The reference document inherits the team's existing code-style and test-style decisions rather than imposing new ones.
