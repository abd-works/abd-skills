# Shared secrets (skills repo)

Put **machine-local** API keys here so **abd-context-to-memory** (and any script that imports `skills/abd-context-to-memory/scripts/_config.py`) can load them without copying keys into each project.

## Files (optional; either or both)

| File       | Purpose                                      |
|-----------|-----------------------------------------------|
| `.secrets`| `OPENAI_API_KEY=...` (dotenv-style, one per line) |
| `.env`    | Same format; use if you prefer the usual name   |

Do **not** commit real keys. Add `conf/.secrets` to `.gitignore` if your team keeps this file only locally.

## Format

```
OPENAI_API_KEY=sk-...
```

Lines starting with `#` are ignored by `python-dotenv`.

## Load order

1. `conf/.secrets` then `conf/.env` (repo root = parent of `skills/`)
2. `skills/abd-context-to-memory/.env`
3. Current working directory `.env` (overrides earlier values for the same keys)

Repo `conf/` files are loaded with **override enabled** so a correct key in `conf/.secrets` wins over a stale `OPENAI_API_KEY` left in your shell or OS environment. Your project’s cwd `.env` still loads last and can override repo conf for that run.
