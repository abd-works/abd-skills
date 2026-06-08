# Paste when spawning one team member agent (fixture mode)

Replace `<role>` with `product-owner`, `business-expert`, `ux-designer`, or `engineer`.

```text
Read <workspace>/AGENT-SEED.md FIRST — fixture mode team member executor.

Bootstrap:
  workspace: <absolute-path-to-pawplace-stubs>
  delivery-role: <role>

Then read practices/kanban/agents/<role>/AGENT.md and agents/reference/skill-fixture-mode.md.
Arm AGENT_LOOP_TICK_<role> pull loop on turn 1.

After pull or manual assignment, run apply_skill_fixture.py (see AGENT-SEED.md).
Do NOT run practice skills. Never exit after one skill.
```

Example workspace path after reset:

`C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\e2e\data\pawplace-stubs`
