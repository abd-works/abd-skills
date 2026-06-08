### Rule: Generated templates cover every file in the reference's File Structure, with filled examples

The generated skill must ship a `templates/` set such that **every file path** named in the reference's mechanism `File Structure` blocks appears in **at least one** template entry, with a filled mini-example (not just placeholders) showing what that file looks like when correctly implemented. The filled examples are the audience contract: a practitioner reading the template should see runnable code, not headings and `{{TOKENS}}`. Passing means a reviewer can take any file path from the reference, search the templates, and find a worked example. Failing means a file from the reference has no template entry, or every entry is empty scaffolding.

#### DO

- For each mechanism, list every file path from its `File Structure` block in `templates/domain-module.template.txt` (or per-tier templates) and attach a filled mini-example to each.

  **Example (pass):** Reference's Persistence mechanism File Structure lists `packages/<domain>/server/mongo-recipients.repository.ts`. The template entry for that path shows a complete, compilable `MongoRecipientsRepository` class with constructor, `findAll`, `findByIds`, `findByEnterprise` methods — not just method stubs.

- Make filled examples runnable in isolation as much as possible — they double as smoke tests when the generated skill is invoked.

  **Example (pass):** The filled `RecipientStatus.ts` example in the template compiles standalone with `tsc --noEmit` against a minimal `tsconfig.json`; no missing import surprises.

- Cite the source mechanism above each filled example.

  **Example (pass):** Above the `RecipientStatus.ts` example, a comment line reads: `// Pattern: Value Object (Persistence mechanism, inputs/architecture-reference.md).`

#### DO NOT

- Ship a template entry whose body is `## TODO` or a bare `{{ENTITY_NAME}}` placeholder for files the reference explicitly lists.

  **Example (fail):** Template entry for `recipients.repository.ts` has body: `export class {{ENTITY}}Repository {}` and nothing else. The reader has no idea what `findAll` should look like.

- Skip files the reference names because they are "language-specific" or "framework-specific" and rely on the implementer to fill them in from memory.

  **Example (fail):** Reference's File Structure names `index.ts` and `package.json` for each tier. The template ships only the `.ts` source files; `index.ts` and `package.json` are missing. The generated skill quietly produces broken packages.

- Provide a template whose filled example contradicts the reference's named pattern.

  **Example (fail):** Reference's pattern is `Result<T, DomainException>`. The filled example in the template throws raw `Error` and uses `try/catch`. Future generated code copies the wrong pattern.

**Source:** Practice-skill authoring convention (abd-build-architecture-skill); aligns with the `templates-include-ideal-filled-examples-for-audience` rule bundled in `abd-author-practice-skill`.
