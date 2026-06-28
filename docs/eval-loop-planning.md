# Eval loop planning — practice skills

**Status:** Exploration / planning only — no implementation committed yet.  
**Purpose:** Decide how an evaluation framework closes the gap between session corrections and durable skill improvement.

---

## The problem we are solving

Practice skills already have:

1. **Rules** — decidable pass/fail specs (`rules/*.md`)
2. **Scanners** — mechanical enforcement where rules are structural (`scanners/*-scanner.py`, `run_scanners.py`)
3. **Session correction loop** — log wrong → fix artifact → log correct → later fix skill source
4. **AI per-rule verdict** — re-read rules and emit PASS/FAIL on generated output

What is **not** closed today:

- Confirmed corrections live in **logs** (`skill-errors-log.md`, session journal `## Corrections`)
- Logs are good for humans and for a post-session `fix-skill` pass
- Logs are **not** rerunnable — nothing automatically checks “did we break this again?” when a rule or scanner changes

The missing piece is **promotion**: turning confirmed wrong/correct pairs into **fixtures with expectations** that can be run again.

This is not “the model learns.” It is **the skill package learns** — rules, scanners, templates, and instructions harden from real failures.

---

## What we already have (inventory)

| Piece | Location | Role |
| --- | --- | --- |
| Correction process | `common/instructions/log-and-fix-skill-errors.instructions.md` | Fix output first; log DO/DO NOT + Example (wrong); fill Example (correct) on confirm |
| Fix skill source | `common/prompts/fix-skill.prompt.md` | Read log → change rules / SKILL / scanners / templates |
| Validate workflow | `common/skill-workflow.md` § Validate | AI pass + scanner pass together |
| Rule checklist | `common/rule-checklist.md` | Read rules → scanners → per-rule verdict → adversarial intent |
| Scanner driver | `common/scripts/run_scanners.py` | Run paired scanners; write `scanner-report/` |
| Reference eval pattern | `stages/engineering/abd-secure-code/test/` | `fixtures/`, `scanner_expectations.json`, pytest — **only skill with this today** |
| CDD session corrections | `abd-context-driven-delivery` SKILL § Corrections | Session-local; journal format with wrong/correct examples |
| CDD correction hooks | `practices/context-driven-delivery/scripts/detect-correction.*` | Writes `docs/sessions/corrections-pending.md` |

---

## The closed loop (target state)

```text
Session
  └─ output wrong
       └─ log Example (wrong) in skill-errors-log or session journal
            └─ fix artifact until right
                 └─ log Example (correct), Status: confirmed
                      └─ PROMOTE → eval/fixtures/fail + eval/fixtures/pass
                           └─ append eval/cases.json (expected scanners / rules)
                                └─ post-session: theme log → fix-skill
                                     └─ run eval BEFORE and AFTER skill change
                                          └─ green = skill package improved without regression
```

**Promotion** is the hinge. Without it, the correction loop improves one artifact once. With it, the same failure becomes a permanent guardrail.

---

## Eval pass on each fixture — scanner then AI

**Reject:** “Structural rules → scanners only; semantic rules → AI only.”

**Per rule, per fixture:** scanner (if any) → AI verdict on matching `rules/<rule>.md`. See `docs/Solution.md` for full model, context tags, layout, and run frequency.

---

## Skill types — eval differs by role

### A. Deliverable skills (most practice skills)

**Examples:** `abd-domain-language`, `abd-story-mapping`, `abd-story-acceptance-criteria`, `abd-secure-code`

**Artifacts:** Named files under `docs/` (or engagement paths in `cdd-context-index.md`)

**Eval fits well:**

- Promote wrong/correct markdown (or code) into `eval/fixtures/`
- Pair with existing or new scanners
- `Likely source: automation gap` → add or tighten scanner + fail fixture

**Pilot candidate:** `abd-domain-language` — has scanners, clear structural rules, real correction potential.

### B. Orchestrator skills (CDD)

**Example:** `abd-context-driven-delivery`

**Artifacts:** Session journal, `process-checklist.md`, routing transcripts — not a single deliverable file.

**Eval is harder:**

- Many rules are behavioral (“don’t self-generate”, “confirm entry point first”)
- Evidence lives in **session narrative**, not one template
- Session corrections are **intentionally session-local** until promoted

**Options (to decide, not build yet):**

1. **Promote only reusable corrections** from session journal into orchestrator `eval/fixtures/` (journal excerpts, checklist snippets)
2. **Keep CDD eval thin** — 3–5 high-value structural rules only (checklist shape, correction entry completeness)
3. **Defer CDD eval** — let deliverable skills prove the promotion pattern first; CDD inherits later

**Recommendation for planning:** Start with deliverable skills. Treat CDD as a second wave after promotion + `run_skill_eval` exist and one pilot skill is green.

---

## Proposed folder convention (per skill, when ready)

```text
practices/<family>/skills/<skill-name>/
  rules/                          # already exists on many skills
  scanners/                       # already exists on many skills
  skill-errors-log.md             # engagement corrections (or under skill package)
  eval/                           # NEW — when skill adopts eval
    cases.json                    # fixture list + expectations
    fixtures/
      pass/<case-slug>/           # Example (correct) promoted here
      fail/<case-slug>/           # Example (wrong) promoted here
    report.md                     # generated; gitignore
```

**`cases.json` minimum shape:**

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

Repo-level scripts (future, not built):

- `common/scripts/promote_correction_to_eval.py` — confirmed log entry → fixtures + cases row
- `common/scripts/run_skill_eval.py` — run eval scanners per `cases.json`; non-zero on regression

---

## Promotion rules (when to create a fixture)

| Trigger | Action |
| --- | --- |
| Correction `Status: confirmed` + `Likely source: automation gap` | **Always promote** — add fail fixture; add `must_violate` scanner; add pass fixture if Example (correct) exists |
| Same rule fails in 2+ sessions | Promote — recurring failure deserves regression |
| One-off context typo | **Do not promote** — fix artifact only |
| CDD session correction marked reusable | User agrees → promote to CDD `eval/` or target specialist skill’s `eval/` |
| fix-skill changes a rule or scanner | **Run eval** before merge |

---

## Phased rollout (decision-friendly)

### Phase 0 — Agree (this doc)

- [ ] Confirm promotion is the missing loop (not “store good/bad somewhere”)
- [ ] Confirm Layer 1 before Layer 2
- [ ] Pick pilot skill: **recommend `abd-domain-language`**, not CDD
- [ ] Decide whether `eval/report.md` is gitignored generated output

### Phase 1 — Pilot on one deliverable skill (manual promotion OK)

- [ ] Add `eval/` to pilot skill only
- [ ] Manually copy 1–2 confirmed corrections into `fixtures/pass` and `fixtures/fail`
- [ ] Wire `cases.json` to existing scanners (no new scanners required for first case)
- [ ] Document promote steps in pilot skill’s Validate section (or link here)

### Phase 2 — Repo tooling

- [ ] `promote_correction_to_eval.py`
- [ ] `run_skill_eval.py` (thin wrapper over existing scanners + cases.json)
- [ ] Add `fix-skill` step 0: run eval; must be green after edits

### Phase 3 — Layer 2 (optional)

- [ ] Define when LLM rule-grader runs vs human-only
- [ ] Keep grader rubric = `rules/*.md` text; no duplicated rule prose

### Phase 4 — Orchestrator (CDD)

- [ ] Only after Phase 1–2 proven on deliverable skills
- [ ] Decide: session journal excerpts vs checklist-only fixtures
- [ ] Align with CDD “corrections are session-local unless promoted” policy

### Phase 5 — CI (optional)

- [ ] On changes to `rules/`, `scanners/`, `SKILL.md` under skills with `eval/`: run `run_skill_eval.py`

---

## Open questions

1. **Where does `skill-errors-log.md` live?** Per skill package vs engagement `docs/` — promotion script must handle both (instructions mention both patterns).
2. **npx skills vs deploy vs eval** — deploy copies to `.cursor/skills/`; eval is separate from Cursor skill autocomplete. Document so nobody conflates them.
3. **Fixture scale** — no arbitrary cap; one case per promoted failure mode; coverage map rules over time (see `docs/Solution.md`).
4. **Who runs eval?** Human after session, agent before `fix-skill`, CI on PR — all three?
5. **CDD corrections-pending hook** — does promotion integrate with `detect-correction.sh` or stay manual?
6. **Practice skills not in `npx skills` registry** — eval is the quality path for those; catalog install is a separate concern.

---

## Explicit non-goals (for now)

- Do not build eval for every skill at once
- Do not add Layer 2 LLM grader until Layer 1 promotion works on one pilot
- Do not treat eval as model training or fine-tuning
- Do not block deploy on eval until CI phase is agreed
- Do not rewrite CDD as a deliverable skill — it remains an orchestrator

---

## Next step (human decision)

1. Read this doc  
2. Confirm pilot skill (`abd-domain-language` recommended)  
3. Bring one real confirmed correction from that skill’s log (or a recent session)  
4. Manually sketch what the promoted `fail/` and `pass/` files would look like — **no scripts yet**  
5. Only then approve Phase 1 implementation  

---

## References in this repo

- `common/skill-workflow.md` — Validate output (AI + scanner)
- `common/rule-checklist.md` — four-step validate mindset
- `common/instructions/log-and-fix-skill-errors.instructions.md` — correction fields including `Likely source`
- `common/prompts/fix-skill.prompt.md` — source fix targets including scanners
- `stages/engineering/abd-secure-code/test/README.md` — existing fixture/scanner test pattern
- `practices/context-driven-delivery/skills/abd-context-driven-delivery/SKILL.md` — § Corrections (session-local)
