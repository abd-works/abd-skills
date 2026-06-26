---
description: >-
  Commit current changes with a message tagged to CDD stage, perspectives
  completed, and scope (epic, feature, thin slice, or all).
agent: agent
---

Commit the current working changes as a CDD progress checkpoint.

**Do not start until any in-progress skill work is done.** If the user's message contains skill instructions alongside this command, complete those first.

---

## Step 1 — Read progress state

Check for these files at the workspace root (skip gracefully if absent):

- `cdd-context-index.md` — active scope (epic, feature, thin slice)
- `cdd-progress-log.md` — stages and perspectives completed this session
- `scope.json` / `last_commit_scope.json` — last persisted scope override

---

## Step 2 — Determine scope

Use the first match:

1. User stated scope explicitly in the command invocation (e.g. "scope is Voucher Redemption epic").
2. `cdd-context-index.md` active row — epic name, feature, or thin slice.
3. `last_commit_scope.json` value.
4. Infer from changed file paths and conversation context.
5. Fall back to `all`.

Persist the resolved scope to `last_commit_scope.json` with a timestamp.

---

## Step 3 — Determine stage and perspectives

Run `git diff --name-only HEAD` and `git status --short`. Map changed paths to CDD stages and perspectives:

| Changed path pattern | Stage | Perspective |
|---|---|---|
| `docs/context/` | context | — |
| `docs/shape/` or `docs/shaping/` | shaping | any |
| `docs/domain/` | discovery | domain |
| `docs/story/` | discovery | story |
| `docs/ux/` | exploration | ux |
| `docs/spec/` or `docs/scenarios/` | specification | any |
| `src/`, `tests/`, `*.ts`, `*.js`, `*.py` | engineering | code |
| `docs/architecture/` | engineering | architecture |

If `cdd-progress-log.md` lists stages/perspectives completed this session, prefer that over path inference.

---

## Step 4 — Build the commit message

Format:

```
cdd.<stage>.<perspective>: <what changed> — <scope>
```

Rules:
- `<stage>` — one of: `context`, `shaping`, `discovery`, `exploration`, `specification`, `engineering`
- `<perspective>` — omit when stage has no perspective (context) or when multiple perspectives changed (use `multi`)
- `<scope>` — epic name, feature name, thin slice label, or `all`
- Present tense; under 80 characters in the first line
- When multiple stages changed, use the highest-fidelity stage (engineering > specification > exploration > discovery > shaping > context)
- Never add `Co-authored-by` trailers

**Examples:**

```
cdd.discovery.domain: Add voucher glossary — Redemption epic
cdd.specification.multi: Add scenarios + acceptance criteria — Auth thin slice
cdd.engineering.code: Implement redemption endpoint — Voucher feature
cdd.shaping: Run Phase 2 stories — Loyalty epic
cdd.context: Chunk and embed onboarding docs — all
```

---

## Step 5 — Execute

```bash
git add -A
git commit -m "<message>"
```

Confirm the commit hash and one-line summary to the user.
