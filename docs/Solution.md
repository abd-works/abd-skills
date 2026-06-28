# Eval solution — practice skills

## Solution in one sentence

**Promote every confirmed correction into rerunnable fixtures with scanner expectations, so the skill package improves from real failures and stays fixed across future sessions.**

---

## Problem

Practice skills already have rules, scanners, session correction logs, and a `fix-skill` pass. What they lack is **regression memory**: when a rule or scanner changes, nothing reruns the failures that taught us the rule in the first place.

Logs record good and bad examples. They do not **guard** against the same mistake coming back.

---

## Solution

Add an **eval layer** to each practice skill that adopts it:

1. **During session** — correction loop unchanged: log wrong → fix artifact → log correct on confirm.
2. **On confirm** — **promote** `Example (wrong)` and `Example (correct)` into `eval/fixtures/`.
3. **Register expectation** — append a case to `eval/cases.json` (which scanners must pass or fail).
4. **Before/after fix-skill** — run eval; skill source changes must keep all cases green.
5. **Recurring failures** — `Likely source: automation gap` → add or tighten scanner; fail fixture proves it works.

The model does not learn. **The skill package learns** — rules, scanners, templates, and instructions harden from production corrections.

---

## Closed loop

```text
Wrong output
  → log Example (wrong)
  → fix artifact
  → log Example (correct), Status: confirmed
  → PROMOTE to eval/fixtures/fail + eval/fixtures/pass
  → append eval/cases.json
  → post-session: theme log → fix-skill (rules / scanners / SKILL / templates)
  → run eval (must be green)
  → next session runs against improved skill package
```

**Promotion** is the hinge. Everything else you already have slots into this loop.

---

## Two eval layers

### Layer 1 — Mechanical (build first)

Run existing Python scanners against promoted fixture files.

| | |
|---|---|
| **Input** | `eval/fixtures/pass/<case>/` and `eval/fixtures/fail/<case>/` |
| **Check** | Pass fixtures: zero violations. Fail fixtures: named scanners must fire. |
| **When** | Rule is structural — format, headings, forbidden patterns, file shape |
| **Reference** | `stages/engineering/abd-secure-code/test/` |

### Layer 2 — Rule verdict on frozen fixtures (add later)

Re-run per-rule PASS/FAIL from `rules/*.md` against saved artifacts — the same AI verdict you already do in validate, but on fixtures instead of fresh generation.

| | |
|---|---|
| **When** | Scanners green but meaning still wrong; semantic / judgment rules |
| **How** | Rubric = `rules/*.md`; optional LLM-as-judge at temperature 0; human on themes |
| **Not** | Model training, fine-tuning, or replacing scanners for structural rules |

**Order:** Layer 1 + promotion first. Layer 2 only after promotion is habitual on at least one pilot skill.

---

## Per-skill layout

```text
practices/<family>/skills/<skill-name>/
  rules/
  scanners/
  skill-errors-log.md
  eval/
    cases.json
    fixtures/
      pass/<case-slug>/     ← Example (correct)
      fail/<case-slug>/     ← Example (wrong)
    report.md               ← generated; gitignore
```

### `cases.json` shape

```json
{
  "skill": "abd-domain-language",
  "fixtures": {
    "pass/minimal-ka": {
      "workspace": "fixtures/pass/minimal-ka",
      "expect_zero_violations": true,
      "scanners": ["domain-terms-coverage-scanner"]
    },
    "fail/unitalicized-terms": {
      "workspace": "fixtures/fail/unitalicized-terms",
      "must_violate": ["domain-terms-coverage-scanner"]
    }
  }
}
```

### Repo scripts (to build)

| Script | Job |
| --- | --- |
| `common/scripts/promote_correction_to_eval.py` | Confirmed log entry → fixtures + `cases.json` row |
| `common/scripts/run_skill_eval.py` | Run `cases.json` expectations; write `eval/report.md`; exit non-zero on regression |

Wire `fix-skill` step 0: **run eval before editing sources; re-run until green after.**

---

## Promotion rules

| When | Do |
| --- | --- |
| `Status: confirmed` + `automation gap` | Always promote fail fixture; add `must_violate` scanner; promote pass if Example (correct) exists |
| Same rule fails in 2+ sessions | Promote |
| One-off typo | Do not promote — fix artifact only |
| CDD correction marked reusable | Promote to target skill’s `eval/` (orchestrator or specialist) |
| Any `fix-skill` change to rules/scanners | Run eval before merge |

---

## Skill types

### Deliverable skills (pilot here)

`abd-domain-language`, `abd-story-mapping`, `abd-story-acceptance-criteria`, `abd-secure-code`, etc.

- Artifacts are named files under `docs/`
- Promote wrong/correct file content into fixtures
- Pair with existing or new scanners
- **First pilot:** `abd-domain-language`

### Orchestrator skills (second wave)

`abd-context-driven-delivery`

- Artifacts are session journal + `process-checklist.md`, not one deliverable file
- Promote only **reusable** corrections (journal excerpts, checklist snippets)
- Keep eval thin — structural session rules only
- **Defer** until deliverable pilot is green

---

## Rollout

| Phase | What |
| --- | --- |
| **0** | Agree this solution; pick pilot (`abd-domain-language`) |
| **1** | Manual promotion: 1–2 real corrections → fixtures + `cases.json`; run scanners by hand |
| **2** | `promote_correction_to_eval.py` + `run_skill_eval.py`; `fix-skill` runs eval |
| **3** | Layer 2 rule grader (optional) |
| **4** | CDD orchestrator eval (optional) |
| **5** | CI on skills with `eval/` when rules or scanners change |

---

## What this is not

- Not model training or reinforcement learning
- Not a replacement for session correction logs
- Not required on every skill on day one
- Not the same as `deploy-skills` or `npx skills add` (those are install/discovery; eval is quality/regression)
- Not an excuse to skip AI per-rule verdict on live generation — eval complements validate, does not replace it

---

## Existing pieces this solution uses

| Piece | Path |
| --- | --- |
| Correction process | `common/instructions/log-and-fix-skill-errors.instructions.md` |
| Fix skill source | `common/prompts/fix-skill.prompt.md` |
| Validate workflow | `common/skill-workflow.md` |
| Scanner driver | `common/scripts/run_scanners.py` |
| Fixture pattern reference | `stages/engineering/abd-secure-code/test/` |
| Planning detail / open questions | `docs/eval-loop-planning.md` |
