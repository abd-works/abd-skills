---
description: >-
  Commit CDD progress. Infers stage, perspective, and scope from changed files
  and session state. Invoke as: cdd-commit, or "cdd-commit scope: <name>".
agent: agent
---

# CDD Commit

Commit the current changes as a CDD progress checkpoint. Do not run until any in-progress skill work is complete.

---

## 1. Resolve scope

Use the first match:

1. Explicit in this command — e.g. "cdd-commit scope: Voucher Redemption"
2. `cdd-context-index.md` active row at the workspace root
3. `last_commit_scope.json` value
4. Infer from changed file paths or conversation context
5. Fall back to `all`

Persist the resolved scope to `last_commit_scope.json`.

---

## 2. Infer stage and perspective from changed paths

Run `git diff --name-only HEAD` and `git status --short`. Map to stage + perspective:

| Path pattern | Stage | Perspective |
|---|---|---|
| `docs/context/` | context | — |
| `docs/domain/glossary/` | shaping | domain |
| `docs/stories/story-map/` (outline only) | shaping | stories |
| `docs/ux/` (impact-map) | shaping | ux |
| `docs/architecture/diagrams/system-context*` | shaping | architecture |
| `docs/domain/language/` | discovery | domain |
| `docs/stories/story-map/` (full) | discovery | stories |
| `docs/ux/information-architecture/` | discovery | ux |
| `docs/architecture/blueprint/` | discovery | architecture |
| `docs/domain/model/` | exploration | domain |
| `docs/stories/acceptance-criteria/` | exploration | stories |
| `docs/ux/mockup/` | exploration | ux |
| `docs/architecture/specification/` | exploration | architecture |
| `docs/domain/specification/` | specification | domain |
| `docs/domain/supporting/walkthrough*` | specification | domain |
| `docs/stories/specification/` | specification | stories |
| `docs/ux/specification/` | specification | ux |
| `src/`, `tests/`, `*.ts`, `*.js`, `*.py` | engineering | code |
| `docs/bdd/` | engineering | stories |
| `docs/domain/supporting/` | support | domain |
| `docs/cdd-sessions/` | — | skip (housekeeping) |

If `docs/cdd-sessions/` changes are the **only** changes, commit with message `cdd.session: Update journal and checklist — <scope>` and stop.

When multiple stages changed, use `<lowest-stage>→<highest-stage>` (e.g. `shaping→discovery`, `discovery→specification`).

When multiple perspectives changed at the same stage, use `multi`.

---

## 3. Build the commit message

```
cdd.<stage>.<perspective>: <what changed> — <scope>
```

- Omit `.<perspective>` when stage is `context` (no perspective)
- `<what changed>` — present tense, describe the artifact or skill output, under 60 chars
- Under 80 characters total on the first line
- No `Co-authored-by` trailers

**Examples:**

```
cdd.shaping.domain: Add voucher glossary — Redemption epic
cdd.shaping→discovery.multi: Domain language + story map — Auth feature
cdd.exploration.stories: Acceptance criteria — Login thin slice
cdd.specification.stories: Spec by example — Voucher flow — all
cdd.engineering.code: Implement redemption endpoint — Voucher feature
cdd.context: Chunk and embed onboarding docs — all
cdd.session: Update journal and checklist — Voucher feature
```

---

## 4. Execute

```bash
git add -A
git commit -m "<message>"
```

Confirm commit hash and one-line summary.
