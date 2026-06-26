---
description: >-
  Read every active Cursor rule and VS Code instruction into context so the
  agent is fully aware of all project guidance before starting work.
  Run this at the start of a session or whenever rules feel stale.
agent: agent
---

You are refreshing your active rule/instruction context. Follow every step below — do not skip any.

## Step 1 — Locate all rule and instruction files

Run the following searches and collect every file path found:
if in cursor
**Cursor rules** (`.mdc` files):
- `.cursor/rules/*.mdc` in the workspace root
- `~/.cursor/rules/*.mdc` (user-global rules)
if in vscode
**VS Code instructions** (`.instructions.md` files):
- `.github/instructions/*.instructions.md` in the workspace root
- `.vscode/instructions/*.instructions.md` in the workspace root

Use glob/shell to list them. Print the full list so the user can see what was found.

## Step 2 — Read every file

Read **each file** found in Step 1 using the Read tool. Do not summarise or truncate — read the full content.

## Step 3 — Confirm and commit

After reading all files, output a single confirmation block:

```
RULES LOADED — <N> files read
─────────────────────────────
<one line per file: filename — first non-blank non-frontmatter sentence>

I will follow all of these rules for the remainder of this session.
Any instruction that conflicts with a user request will be surfaced explicitly
rather than silently ignored.
```

## Step 4 — Stay active

For the rest of the session:
- Before starting any task, mentally check the loaded rules for relevant constraints.
- If a rule says "always do X" or "never do Y", honour it without being asked.
- If the user asks you to do something a rule prohibits, say so and ask how to proceed.
