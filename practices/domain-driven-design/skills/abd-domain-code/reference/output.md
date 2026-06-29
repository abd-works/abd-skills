# Output — abd-domain-code

This skill does **not** write under `docs/`. Domain code and tests follow the host project's conventions.

## Domain layer (`<domain-folder>`)

1. **The path the user told you to use.**
2. **`architecture-specification.md`** — domain layer section when present.
3. **Where the project already keeps domain code** — infer from existing source layout.
4. **Language-conventional domain package** — e.g. `src/domain/`, `lib/domain/`, `internal/domain/`.

## Tests (`<tests-folder>`)

1. **The path the user told you to use.**
2. **Where the project already keeps tests** — `tests/`, `test/`, `spec/`, or language-conventional test folder.
3. **The workspace root** or a sensible language-default location.

Do **not** invent a predetermined folder name. Follow abd-story-acceptance-test organization (one file per sub epic, one class per story, one method per scenario).
