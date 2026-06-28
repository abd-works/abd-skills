# Research Report: Durable improvement via correction-promoted eval

**Status:** Research only — informs `docs/Solution.md` and `docs/eval-loop-planning.md`.  
**Stance:** Impartial. User's approach is the subject under review, not the standard.

---

## Hypothesis (corrected)

> **I believe** promoting confirmed session corrections into per-skill eval fixtures (scanner then AI verdict on the matching rule) **will make practice-skill improvement durable and compounding** **for** teams running many agent sessions on formalized skills.

**North star:** the system gets better over time in a way that sticks — each engagement leaves the skill package smarter.  
**Not the goal:** regression drift as an end in itself. Rerunnable cases are how you *prove* improvement compounded and *protect* gains while you keep climbing — not why the loop exists.

---

## Problem Validation: Durable improvement from real corrections

### Signal

The problem is **not** “we need more tests.” It is: **corrections happen, but lessons do not reliably harden into the governed artifacts that shape the next session.**

| Who | What they say | Source |
| --- | --- | --- |
| EDDOps (academic) | Evaluation must drive **iterative refinement of workflows, policies, prompts, and test/safety cases** — not sit as a terminal checkpoint | [arXiv 2411.13768](https://arxiv.org/abs/2411.13768) |
| LangChain | Improvement loop: traces → failures → targeted harness changes → **validate before shipping** → repeat from a higher baseline; passing evals join the permanent suite | [Agent improvement loop](https://www.langchain.com/blog/traces-start-agent-improvement-loop) |
| LangChain (harness hill-climbing) | “Once our agent handles a case correctly, we don't want to lose that gain” — eval protects **hill-climbing**, regression is secondary to climbing | [Better harness](https://www.langchain.com/blog/better-harness-a-recipe-for-harness-hill-climbing-with-evals) |
| Braintrust / Arthur / AgentPatterns | Production failures and user corrections become **versioned cases** that make the system smarter on the next change | [Braintrust](https://www.braintrust.dev/articles/turn-llm-production-failures-into-regression-tests), [Arthur](https://www.arthur.ai/column/regression-test-datasets-ai-agents-production-failures), [AgentPatterns](https://agentpatterns.ai/verification/incident-to-eval-synthesis/) |
| web.dev | EDD: repeatable process for **improving outputs in small, confident steps** — eval is the feedback instrument, not the product | [web.dev EDD](https://web.dev/learn/ai/evaluation-driven-development) |

Your vocabulary — practice skills, `rules/`, `scanners/`, `fix-skill`, correction logs — is **niche**. The underlying problem — **one-off fixes that don't compound into governed system behavior** — is widely recognized. Industry calls it harness improvement, closed feedback loops, or eval-driven development. You call it **skill-package learning**.

**Maturity:** **Growing → Established** for “eval-driven improvement loops”; **Emerging** for formal practice-skill packages as the unit of compounding.

### Counter-signal

| Who | Argument | Implication for you |
| --- | --- | --- |
| FlowVerify | Eval suites can become **confidence machines** — green scores while behavior drifts | Fixtures from *your* confirmed corrections are higher signal than synthetic gold; still need live validate |
| EDDOps paper | Literature is **97%+ static** eval; few closed loops from failure → artifact change | You're ahead of academia on intent; execution discipline matters |
| Galileo / production anecdotes | Systems pass frozen evals then fail in the wild | Offline compounding ≠ complete assurance; online signal still needed eventually |

These counter-signals **do not** argue against durable improvement. They argue against treating eval as “done” once cases exist.

### Competing priorities (same space)

Teams also invest in: agent trajectory testing (Trajectly, agentverify), prompt/model experiments (promptfoo), security red teaming, judge calibration, production observability. Those are **complements**. Your loop owns **governed deliverable quality** compounding from session corrections.

### Maturity: **Growing**

The *improvement flywheel* is established discourse. Encoding it in per-skill packages with scanner→AI rule verdict is practitioner-specific, not commoditized.

---

## Solution Landscape: How others compound improvement

### Category 1 — Trace → case → harness change (improvement flywheel)

- **Approach:** Capture real runs; failures and **user corrections** become datasets; change prompts/tools/rules; rerun to prove you climbed.
- **Players:** [LangChain/LangSmith](https://www.langchain.com/blog/traces-start-agent-improvement-loop), Braintrust, Arthur
- **Fit for you:** **High** — your correction log *is* the trace source; promotion is trace-to-case without a SaaS

### Category 2 — Eval-driven artifact refinement (EDDOps)

- **Approach:** Evaluation backbone drives versioned changes to prompts, guardrails, **test cases**, pipelines.
- **Players:** [EDDOps arXiv](https://arxiv.org/html/2411.13768v3)
- **Fit for you:** **High** — process-level match; your “artifacts” are rules/scanners/SKILL.md

### Category 3 — Declarative eval + CI gates

- **Approach:** Golden cases, assertions, optional LLM judge; block merge on score drop.
- **Players:** [promptfoo](https://github.com/promptfoo/promptfoo), Galtea guides
- **Fit for you:** **Partial** — good CI mechanics; centers prompts/RAG not domain rule packages

### Category 4 — Skill-native eval (agentskills.io)

- **Approach:** `evals/evals.json` per skill; end-to-end task runs with assertions.
- **Players:** [agentskills.io](https://agentskills.io/skill-creation/evaluating-skills), [agent-skills-eval](https://github.com/darkrishabh/agent-skills-eval)
- **Fit for you:** **Partial** — co-located per-skill eval aligns; their cases are **task prompts**, yours are **frozen deliverable artifacts** — different layer, both useful later

### Category 5 — Hybrid static + LLM judge

- **Approach:** Cheap deterministic checks, then rubric/AI for judgment rules.
- **Players:** [Google Vera](https://github.com/google/vera), [hybrid code review arXiv](https://arxiv.org/pdf/2502.06633)
- **Fit for you:** **High** — scanner→AI on `rules/<rule>.md` is this pattern applied to practice outputs

### Category 6 — Trajectory / behavior regression

- **Approach:** Record and replay tool-call paths; assert execution correctness.
- **Players:** [Trajectly](https://github.com/trajectly/trajectly), [agentverify](https://github.com/simukappu/agentverify)
- **Fit for you:** **Low for now** — improves *how* the agent works; you own *what good deliverables look like*

### Convergence

Industry language says “regression testing”; the mechanism serves **compounding**:

> “The regression suite compounds.” — [Inference.net](https://inference.net/content/ai-regression-testing-llm-apps/)

> “A trace where a user corrected the agent is even better. The flywheel: more usage → more traces → more evals → better harness.” — [LangChain](https://www.langchain.com/blog/better-harness-a-recipe-for-harness-hill-climbing-with-evals)

Your promotion hinge is the same flywheel, with **confirmed correction** as the highest-quality trace.

---

## Approach Comparison

### Classification

**Improvement flywheel (Categories 1–2) + hybrid rule evaluation (Category 5)**, implemented on practice-skill packages instead of generic prompts.

### Strengths

| Strength | Evidence |
| --- | --- |
| Corrections as curriculum | LangChain: user-corrected traces are premium eval sources; Arthur/Braintrust: production failures are cases you “could not have invented” |
| Skill package as learning unit | EDDOps: evaluation should update **test/safety cases** and **pipeline artifacts** together — your `fix-skill` + `eval/` is that |
| Scanner then AI | Hybrid eval is industry norm for code/artifact quality; scanners narrow, AI judges rule intent |
| Context tags | Engagement-mode-aware cases — genuine differentiation vs generic golden sets |
| Cadence | Live validate every turn; eval on promotion/fix-skill — matches “hill-climb then protect gains” |

### Weaknesses

| Weakness | Risk |
| --- | --- |
| Bespoke tooling | You own runner, promotion script, reports — no LangSmith dashboard out of the box |
| AI verdict in eval | Without calibration, “proof of improvement” can be noisy — undermines the north star |
| Frozen artifacts only | Proves deliverable quality compounds; does not prove orchestration/tooling improved |
| Maintenance | Compounding requires discipline: promote the right things, retire stale cases when rules evolve |
| No online loop yet | Durable offline compounding is necessary; not sufficient at scale |

### Trade-off map

| Dimension | Your approach | LangChain/Braintrust flywheel | promptfoo | agentskills.io |
| --- | --- | --- | --- | --- |
| Compounding from corrections | **Stronger** (designed in) | **Stronger** (trace mining) | Weaker (manual cases) | Moderate |
| Domain rule alignment | **Stronger** | Weaker | Weaker | Moderate |
| Proof harness improved | Strong (eval after fix-skill) | Strong | Strong | Strong (E2E) |
| Ops maturity | Weaker | **Stronger** | **Stronger** | Growing |
| Deliverable vs task eval | **Stronger** (artifacts) | Mixed | Mixed | **Stronger** (tasks) |

### White space

**Earned:**

1. Practice-skill packages as the **governed system** that improves (not just prompts).
2. Correction-loop-native promotion wired to `skill-errors-log.md` / session journal.
3. Context-tagged fixtures for engagement mode.

**Not white space:** flywheel concept, incident-to-case, hybrid static+LLM, per-folder eval cases.

---

## Recommendation: **Double down — hybridize mechanics, not direction**

The evidence supports **durable compounding improvement** as the right frame. Your eval layer is the **memory and proof mechanism** for a loop you already run:

```text
Session correction  →  fix artifact  →  confirm
       →  promote (lesson captured)
       →  fix-skill (package upgraded)
       →  eval (proof upgrade stuck)
       →  next session starts from higher baseline
```

**Do not pivot** to generic regression-testing framing or adopt promptfoo as the system of record — wrong artifact type.

**Do borrow:**

1. **Hill-climb then protect** — LangChain's framing: eval exists so gains aren't lost while you keep improving ([source](https://www.langchain.com/blog/better-harness-a-recipe-for-harness-hill-climbing-with-evals)).
2. **User corrections as premium cases** — prioritize confirmed corrections over synthetic coverage ([source](https://www.langchain.com/blog/traces-start-agent-improvement-loop)).
3. **Judge calibration** — small human-labeled set before trusting AI verdict as “proof” ([web.dev](https://web.dev/learn/ai/evaluation-driven-development), [FlowVerify](https://www.flowverify.co/blog/llm-eval-suite-confidence-machine-not-quality-gate)).
4. **Tiered runs** — smoke on frequent commits; full eval on skill-package changes (already in Solution.md).
5. **Stale-case hygiene** — when a rule changes meaning, update or retire cases — compounding requires curation.
6. **Pilot manually** — prove promotion + eval proves fix-skill worked before automating scripts.

**What regression language is still good for:** internally, “don't lose a gain while hill-climbing” is valid. Externally and strategically, lead with **compounding improvement**.

---

## Hypothesis verdict

| Claim | Verdict |
| --- | --- |
| Problem is real (lessons don't compound) | **Yes** |
| Promotion + eval is the right mechanism | **Yes** — matches industry flywheels |
| Novel vs industry | **Process is mainstream; practice-skill packaging is differentiated** |
| Solves everything | **No** — trajectory, security, online drift need other layers |
| Worth building | **Yes** — if you accept maintenance and judge calibration |

---

## References (primary)

- EDDOps: https://arxiv.org/abs/2411.13768
- LangChain improvement loop: https://www.langchain.com/blog/traces-start-agent-improvement-loop
- LangChain harness hill-climbing: https://www.langchain.com/blog/better-harness-a-recipe-for-harness-hill-climbing-with-evals
- Braintrust production → regression: https://www.braintrust.dev/articles/turn-llm-production-failures-into-regression-tests
- Arthur golden dataset from failures: https://www.arthur.ai/column/regression-test-datasets-ai-agents-production-failures
- web.dev EDD: https://web.dev/learn/ai/evaluation-driven-development
- agentskills.io evals: https://agentskills.io/skill-creation/evaluating-skills
- Google Vera hybrid eval: https://github.com/google/vera
- FlowVerify (eval limits): https://www.flowverify.co/blog/llm-eval-suite-confidence-machine-not-quality-gate
