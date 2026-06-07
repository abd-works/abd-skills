# Corrections log

Project: kanban agents — work-queue eligibility
Source: `practices/kanban/agents/reference/work-queue.md` and `practices/kanban/reference/agents-and-skills.md`

---

## Entry: Executor eligibility must require prior review_status: done

- **Status:** confirmed
- **Context:** work-queue.md "Start next skill" algorithm; agents-and-skills.md "Agents" eligibility rule
- **DO / DO NOT:** **DO** require all prior skills to have BOTH `execution_status: done` AND `review_status: done` before an executor can start the next skill. A skill is "prior-complete" only when both execution and review are approved.
- **Example (wrong):**
  Prior rule: "find the next skill where all prior skills have `execution_status: done`" — omitted review gate. Result: kanban lead spawned PO executor for `abd-acceptance-criteria` while `abd-domain-language` was still under review. The PO worked from unreviewed UL output.
- **Example (correct):**
  "find the next skill where all prior skills have `execution_status: done` AND `review_status: done`" — executor only starts after the reviewer has approved the prior skill.
- **Likely source:** prompt gap

---

## Entry: Reviewers fix simple mechanical issues in place

- **Status:** confirmed
- **Context:** reviewer-workflow.md Step 5/6; work-queue.md Rework section
- **DO / DO NOT:** **DO** fix simple mechanical issues (missing stubs, typos, formatting, unresolved references) directly in the artifact and mark review as PASS. Only mark FAIL and bounce to executor for substantive problems (wrong model, missing abstraction, incorrect invariants, structural redesign).
- **Example (wrong):**
  Reviewer found two missing boundary stubs (`*product details page*`, `*stock availability*`) — a two-line fix. Marked `review_status: failed`, reset executor to `not_started`, spawned a full rework agent. One full rework cycle wasted on a mechanical fix.
- **Example (correct):**
  Reviewer finds the same two missing stubs. Adds `### product details page *(boundary)*` and `### stock availability *(boundary)*` directly. Re-runs scanner to confirm resolution. Marks `review_status: done`. No rework cycle needed.
- **Likely source:** prompt gap

---

## Entry: Kanban lead must pull from backlog when agents are idle

- **Status:** confirmed
- **Context:** kanban-lead AGENT.md Step 3d — Pull from backlog; scan cycle behavior
- **DO / DO NOT:** **DO** pull the next backlog ticket to active whenever an agent role has no eligible work on any active ticket. Multiple tickets in flight is normal. Do not single-thread the board on one ticket while agents sit idle.
- **Example (wrong):**
  Business-expert finished UL on inc-8. Next skill on inc-8 is AC (product-owner role). Kanban lead left inc-9 in backlog and waited — business-expert sat idle with nothing to do.
- **Example (correct):**
  Business-expert finished UL on inc-8. Kanban lead immediately pulls inc-9 from backlog to active and spawns business-expert for UL on inc-9. Two tickets in flight: PO works AC on inc-8, BE works UL on inc-9.
- **Likely source:** prompt gap

---

## Entry: Team member agents must signal ready and poll — not exit after one scan

- **Status:** confirmed
- **Context:** work-queue.md / executor-workflow.md Step 7 — agents idle while backlog tickets wait for kanban lead pull
- **DO / DO NOT:** **DO** after finishing a skill: scan active tickets downstream-first (right to left); if no eligible skill, append `agent_ready` to `metrics-log.jsonl`, update heartbeat with `status: ready`, and poll `board.json` every 30s. **DO NOT** exit after a single "no pending work" scan; **DO NOT** pull tickets from backlog to active yourself.
- **Example (wrong):**
  Business-expert finished domain model on inc-8-sprint-1. No other BE skill on active tickets. Agent reported idle and stopped. inc-8-sprint-3 (domain model) sat in backlog under Exploration Done — kanban lead never got a signal to pull it.
- **Example (correct):**
  Business-expert finished sprint-1. No eligible skill on active tickets. Agent appends `agent_ready`, sets heartbeat `status: ready`, polls board every 30s downstream-first. Kanban lead scan reads `agent_ready`, pulls inc-8-sprint-3 to active. Agent's next poll finds domain model and starts work.
- **Likely source:** prompt gap

---

## Entry: Arm tick loop with notify_on_output before scan cycle 1

- **Status:** confirmed
- **Context:** kanban-lead AGENT.md; session-bootstrap.md; PawPlace engagement — subagent `084052ff-6e1d-4ada-9c36-475267f52651` ran one scan then exited while shell loop ticked unwired
- **DO / DO NOT:** **DO** on turn 1: start `AGENT_LOOP_TICK_kanban_lead` in a **direct** PowerShell shell with `block_until_ms: 0` and `notify_on_output` pattern `^AGENT_LOOP_TICK_kanban_lead`; smoke-check first tick; run scan cycle 1; end turn waiting for next tick. **DO NOT** start a loop shell without `notify_on_output`; **DO NOT** nest `while ($true)` inside `powershell -Command`; **DO NOT** spawn kanban-lead as background Task without loop wiring; **DO NOT** exit after scan cycle 1.
- **Example (wrong):**
  Started loop shell with `block_until_ms: 0` only. Spawned kanban-lead Task subagent. Subagent ran scan cycle 1, spawned BE agents, exited. Loop printed ticks to terminal file for hours — no agent woke for cycle 2+.
- **Example (correct):**
  Turn 1: direct `while ($true) { Start-Sleep -Seconds 5; Write-Output 'AGENT_LOOP_TICK_kanban_lead {...}' }` with `notify_on_output`. Await first tick (~10s smoke). Run scan cycle 1. Update heartbeat. End turn. Tick 2 wakes agent → scan cycle 2 → spawn UX on eligible sprints.
- **Likely source:** prompt gap

---

## Entry: All stages use kanban.json pull order — continuous pull for every role

- **Status:** confirmed
- **Context:** pull-model.md; work-queue.md; all stage files; PawPlace — agents idle while UX/engineer work existed on active sprints
- **DO / DO NOT:** **DO** read stages from `kanban.json` and scan reverse order. **DO** arm `AGENT_LOOP_TICK_<role>` on turn 1 for BE, PO, UX, Engineer. **DO** pull across shaping through engineering. **DO NOT** hardcode stage lists; **DO NOT** spawn reviewer agents; **DO NOT** exit after one skill.
- **Example (wrong):**
  BE finished domain model on all sprints and exited. Four sprints still needed UX interface-design. No UX pull loop running. Kanban lead did not spawn UX because scan cycle stopped after cycle 1.
- **Example (correct):**
  Kanban lead scan: eligible UX skills on 4 sprints → spawn UX executor with pull loop. UX turn 1: arm loop, scan engineering→…→shaping, claim interface-design on inc-8-sprint-4, deliver, pull next.
- **Likely source:** prompt gap

---
