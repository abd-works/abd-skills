# Scanner Report — abd-ubiquitous-language

**Workspace:** C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain
**Date:** 2026-05-30 11:54:13

---

## Scanner Execution Status

### 🟩 Overall Status: HEALTHY

| Status | Count | Description |
|--------|-------|-------------|
| 🟩 Executed Successfully | 6 | Scanners ran without errors |
| 🟩 Clean Rules | 4 | No violations found |
| 🟨 Rules with Warnings | 2 | Found 65 warning violation(s) |

**Total Rules:** 6
- **Rules with Scanners:** 6
  - 🟩 **Executed Successfully:** 6

---

### Scanner Results

| Status | Rule | Violations |
|--------|------|------------|
| 🟨 WARNINGS | Domain-Terms-Coverage | 63 |
| 🟨 WARNINGS | One-Responsibility-Per-Bullet | 2 |
| 🟩 CLEAN | Core-Domain-Excludes-Ui | 0 |
| 🟩 CLEAN | Domain-Grounded-Verbs | 0 |
| 🟩 CLEAN | No-Premature-Design-Commitments | 0 |
| 🟩 CLEAN | Property-Stub | 0 |

---

## Violations

### 🟨 Domain-Terms-Coverage — 63 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'kanban board' appears un-italicized in bullet: '- **Invariant:** the *kanban board* is the single source of truth for which *ski' | warning |
| 2 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'kanban board' appears un-italicized in bullet: '- **Invariant:** a *ticket's* *scope level* must match the scope declared by its' | warning |
| 3 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'kanban board' appears un-italicized in bullet: '- **Invariant:** a *stage* is complete only when every *skill* defined in the *k' | warning |
| 4 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'kanban board' appears un-italicized in bullet: '- *Stage*, *ticket*, *board position*, *skill progress*, *stage work required*, ' | warning |
| 5 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'team' appears un-italicized in bullet: '- waits in **stage done** after all *skills* complete — does not advance automat' | warning |
| 6 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'team' appears un-italicized in bullet: '- **Invariant:** a *ticket* never advances to the next *stage* automatically — a' | warning |
| 7 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'team' appears un-italicized in bullet: '- has a **queue** — *tickets* from the previous *stage*'s done waiting to be pic' | warning |
| 8 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'team' appears un-italicized in bullet: '- *Skill* and *agent* are the core concepts — role, executor/reviewer variant, a' | warning |
| 9 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'ticket' appears un-italicized in bullet: '- **Invariant:** every *ticket* occupies exactly one *stage* at any given time' | warning |
| 10 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'ticket' appears un-italicized in bullet: '- when picked up from stage done, either advances to the next same-scope *stage*' | warning |
| 11 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'ticket' appears un-italicized in bullet: '- **Invariant:** the *kanban board* is the single source of truth for which *ski' | warning |
| 12 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'ticket' appears un-italicized in bullet: '- **Invariant:** a *ticket's* *scope level* must match the scope declared by its' | warning |
| 13 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'ticket' appears un-italicized in bullet: '- **Invariant:** a *ticket* never advances to the next *stage* automatically — a' | warning |
| 14 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'ticket' appears un-italicized in bullet: '- has a **queue** — *tickets* from the previous *stage*'s done waiting to be pic' | warning |
| 15 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'ticket' appears un-italicized in bullet: '- has **in progress** — *tickets* at this *stage* where *skill* work is underway' | warning |
| 16 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'ticket' appears un-italicized in bullet: '- has **done** — *tickets* at this *stage* where all *skills* are complete, wait' | warning |
| 17 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'ticket' appears un-italicized in bullet: '- **Invariant:** a *ticket* cannot skip a *stage* or move backward' | warning |
| 18 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'ticket' appears un-italicized in bullet: '- **Invariant:** a *ticket* in the queue of *stage* N was in the done state of *' | warning |
| 19 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'ticket' appears un-italicized in bullet: '- is an autonomous worker that starts work on *skills* for active *tickets* and ' | warning |
| 20 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'ticket' appears un-italicized in bullet: '- pulls *tickets* from the backlog into the first *stage*' | warning |
| 21 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'skill progress' appears un-italicized in bullet: '- **Invariant:** a *stage* is complete only when every *skill* defined in the *k' | warning |
| 22 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'stage' appears un-italicized in bullet: '- defines an ordered set of *stages*, each with a *scope level* and an ordered l' | warning |
| 23 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'stage' appears un-italicized in bullet: '- **Invariant:** every *ticket* occupies exactly one *stage* at any given time' | warning |
| 24 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'stage' appears un-italicized in bullet: '- holds a *scope level* matching its current *stage's* scope in the *kanban boar' | warning |
| 25 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'stage' appears un-italicized in bullet: '- waits in **stage done** after all *skills* complete — does not advance automat' | warning |
| 26 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'stage' appears un-italicized in bullet: '- **Invariant:** the *kanban board* is the single source of truth for which *ski' | warning |
| 27 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'stage' appears un-italicized in bullet: '- **Invariant:** a *ticket's* *scope level* must match the scope declared by its' | warning |
| 28 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'stage' appears un-italicized in bullet: '- **Invariant:** scatter only occurs when the next *stage's* *scope level* is fi' | warning |
| 29 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'stage' appears un-italicized in bullet: '- **Invariant:** a *ticket* never advances to the next *stage* automatically — a' | warning |
| 30 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'stage' appears un-italicized in bullet: '- **Invariant:** a *stage* is complete only when every *skill* defined in the *k' | warning |
| 31 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'stage' appears un-italicized in bullet: '- has a **queue** — *tickets* from the previous *stage*'s done waiting to be pic' | warning |
| 32 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'stage' appears un-italicized in bullet: '- has **in progress** — *tickets* at this *stage* where *skill* work is underway' | warning |
| 33 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'stage' appears un-italicized in bullet: '- has **done** — *tickets* at this *stage* where all *skills* are complete, wait' | warning |
| 34 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'stage' appears un-italicized in bullet: '- **Invariant:** a *ticket* cannot skip a *stage* or move backward' | warning |
| 35 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'stage' appears un-italicized in bullet: '- **Invariant:** a *ticket* in the queue of *stage* N was in the done state of *' | warning |
| 36 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'skill' appears un-italicized in bullet: '- defines an ordered set of *stages*, each with a *scope level* and an ordered l' | warning |
| 37 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'skill' appears un-italicized in bullet: '- is the single source of truth for which *skills* each *stage* requires — *skil' | warning |
| 38 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'skill' appears un-italicized in bullet: '- *tickets* flow through its *stages*; *skills* act on each *ticket* at its curr' | warning |
| 39 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'skill' appears un-italicized in bullet: '- waits in **stage done** after all *skills* complete — does not advance automat' | warning |
| 40 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'skill' appears un-italicized in bullet: '- **Invariant:** the *kanban board* is the single source of truth for which *ski' | warning |
| 41 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'skill' appears un-italicized in bullet: '- **Invariant:** a *stage* is complete only when every *skill* defined in the *k' | warning |
| 42 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'skill' appears un-italicized in bullet: '- has a **queue** — *tickets* from the previous *stage*'s done waiting to be pic' | warning |
| 43 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'skill' appears un-italicized in bullet: '- has **in progress** — *tickets* at this *stage* where *skill* work is underway' | warning |
| 44 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'skill' appears un-italicized in bullet: '- has **done** — *tickets* at this *stage* where all *skills* are complete, wait' | warning |
| 45 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'skill' appears un-italicized in bullet: '- is the ordered list of *skills* required by a *stage*' | warning |
| 46 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'skill' appears un-italicized in bullet: '- *Stage*, *ticket*, *board position*, *skill progress*, *stage work required*, ' | warning |
| 47 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'skill' appears un-italicized in bullet: '- is an autonomous worker that starts work on *skills* for active *tickets* and ' | warning |
| 48 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'skill' appears un-italicized in bullet: '- operates under one of four named delivery roles — product-owner, business-expe' | warning |
| 49 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'skill' appears un-italicized in bullet: '- **Invariant:** an *agent* may only start work on *skills* that require its rol' | warning |
| 50 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'agent' appears un-italicized in bullet: '- is acted upon by a *team* configured as *team* — the number of executor/review' | warning |
| 51 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'agent' appears un-italicized in bullet: '- records the *agent role* performing execution and the *agent role* performing ' | warning |
| 52 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'agent' appears un-italicized in bullet: '- each *skill* is performed by an *agent role*' | warning |
| 53 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'agent' appears un-italicized in bullet: '- is the executor/reviewer pair counts per *agent role* configured on the board' | warning |
| 54 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'agent' appears un-italicized in bullet: '- holds a count per *agent role* that can be incremented or decremented' | warning |
| 55 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'agent' appears un-italicized in bullet: '- **Invariant:** defaults to one executor and one reviewer per *agent role* when' | warning |
| 56 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'agent' appears un-italicized in bullet: '- is performed by an *agent role*' | warning |
| 57 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'agent' appears un-italicized in bullet: '- **Invariant:** an *agent* may only start work on *skills* that require its rol' | warning |
| 58 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'agent' appears un-italicized in bullet: '- **Invariant:** the *kanban lead* is a separate orchestrating role, not an *age' | warning |
| 59 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'agent' appears un-italicized in bullet: '- **Invariant:** an *agent* is considered inactive once its *heartbeat* age exce' | warning |
| 60 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'agent' appears un-italicized in bullet: '- monitors *heartbeats* to determine which *agents* are alive' | warning |
| 61 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'agent' appears un-italicized in bullet: '- *Heartbeat* belongs here — it exists to report agent liveness and has no meani' | warning |
| 62 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'heartbeat' appears un-italicized in bullet: '- **Invariant:** an *agent* is considered inactive once its *heartbeat* age exce' | warning |
| 63 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Term 'heartbeat' appears un-italicized in bullet: '- monitors *heartbeats* to determine which *agents* are alive' | warning |

### 🟨 One-Responsibility-Per-Bullet — 2 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Bullet joins two clauses with '; ' — split into one bullet per responsibility: '- waits in **stage done** after all *skills* complete — does not advance automatically; a team membe' | warning |
| 2 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\docs\domain\ubiquitous-language.md` | Bullet contains two em-dashes — likely fusing two responsibilities: '- operates under one of four named delivery roles — product-owner, business-expert, ux-designer, or ' | warning |
