# manual-repair-loop — Logging a Human-Fixed Issue

Use this when the **user found and fixed the problem themselves** without running
the agentic repair loop. The goal is to make sure the original bad output and the
corrected output are captured as fixtures so the skill and underlying scripts can
be improved and the failure becomes a regression test.

---

## When to use this

- The user spotted a diagram problem (visual, structural, routing, etc.)
- They edited or regenerated the diagram manually to fix it
- The scanner/rules may or may not have caught it — either way, no AI iteration loop was run
- They want the failure and the fix captured for future learning

---

## Step 1 — Locate the original bad artifact

Check these sources in order:

1. **`evals/` folder** next to the generated diagram — the last `run-n` output
   before the user's fix is the fail artifact.
2. **`skill-errors-log.md`** inside the skill folder — if the user already logged
   the error there, the "Example (wrong)" entry points to what went wrong.
3. **CDD session journal** (`docs/cdd-sessions/<date>-<topic>/cdd-session-journal.md`)
   — the `## Corrections` section records what the output did wrong and what it
   should have done.
4. **Chat history** — the turn where the user described or showed the problem.

---

## Step 2 — Locate the corrected artifact

The fixed diagram is one of:

- The file the user edited directly
- A newly regenerated diagram the user approved
- Shown or described in the chat immediately after the fix

---

## Step 3 — Capture the fail fixture

Extract the relevant page(s) from the bad artifact using `eval/extract_pages.py`:

```bash
python eval/extract_pages.py <bad-diagram.drawio> eval/fail/<slug>/diagram.drawio <page-name>
```

If the bad artifact is already a single page, copy it directly. If the failure
spans all tabs (e.g. a full first-run output), copy the whole file unchanged.

Follow the fixture format from **agentic-repair-loop.md § "3. Capture fail fixtures"** for the
`cases.json` entry, marking all affected scanners as `"expect": "violate"`.

---

## Step 4 — Capture the pass fixture

Extract the relevant page(s) from the corrected artifact:

```bash
python eval/extract_pages.py <fixed-diagram.drawio> eval/pass/<slug>/diagram.drawio <page-name>
```

Follow the fixture format from **agentic-repair-loop.md § "6. Capture pass fixtures"** for the
`cases.json` entry, marking all scanners as `"expect": "clean"`.

---

## Step 5 — Check whether the scanner/rule gap needs fixing

Run `audit_diagram_report()` against the original bad artifact:

- **If it reports a violation** — the scanner already catches this class of
  problem. No scanner change needed; the fixture alone is enough.
- **If it passes (false negative)** — follow **agentic-repair-loop.md Entry B** to fix the
  scanner or rule until it detects the problem, then re-verify against both
  the fail and pass fixtures.

---

## Step 6 — Improve the skill / script

If the fix reveals a systematic issue in how the CLI generates routing (not a
one-off), improve `drawio_domain_cli.py` so future outputs don't repeat it.
Document the change in `evals/SUMMARY.md`.

---

## File map

| Path | Purpose |
|------|---------|
| `eval/fail/<slug>/diagram.drawio` | Bad artifact (pre-fix) |
| `eval/pass/<slug>/diagram.drawio` | Good artifact (post-fix) |
| `eval/cases.json` | Fixture registry — add entries for both |
| `skill-errors-log.md` | Source of the logged error (read-only here) |
