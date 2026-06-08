# Scanner Report — mern-technical-architecture

**Workspace:** c:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban
**Date:** 2026-06-06 00:39:24

---

## Scanner Execution Status

### 🟨 Overall Status: GOOD - Minor Issues

| Status | Count | Description |
|--------|-------|-------------|
| 🟩 Executed Successfully | 18 | Scanners ran without errors |
| 🟩 Clean Rules | 13 | No violations found |
| 🟥 Rules with Errors | 5 | Found 81 error violation(s) |

**Total Rules:** 18
- **Rules with Scanners:** 18
  - 🟩 **Executed Successfully:** 18

---

### Scanner Results

| Status | Rule | Violations |
|--------|------|------------|
| 🟥 ERRORS | Test Structure Scanner | 60 |
| 🟥 ERRORS | Casing Transform Scanner | 15 |
| 🟥 ERRORS | Infrastructure Boundary Scanner | 3 |
| 🟥 ERRORS | Share Domain Logic Scanner | 2 |
| 🟥 ERRORS | Entity Behavior Scanner | 1 |
| 🟩 CLEAN | Arg Naming Scanner | 0 |
| 🟩 CLEAN | Cross Layer Naming Scanner | 0 |
| 🟩 CLEAN | Dependency Declarations Scanner | 0 |
| 🟩 CLEAN | Domain Structure Scanner | 0 |
| 🟩 CLEAN | Interface Implementation Scanner | 0 |
| 🟩 CLEAN | Layer Purity Scanner | 0 |
| 🟩 CLEAN | Mutation Response Scanner | 0 |
| 🟩 CLEAN | Package Names Scanner | 0 |
| 🟩 CLEAN | Test Isolation Scanner | 0 |
| 🟩 CLEAN | Test Scripts Scanner | 0 |
| 🟩 CLEAN | Type Safety Scanner | 0 |
| 🟩 CLEAN | Domain Language Scanner | 0 |
| 🟩 CLEAN | View Naming Scanner | 0 |

---

## Violations

### 🟥 Test Structure Scanner — 60 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\display_agent_output_stream\open_agent_stream_panel` | Sub-epic 'open_agent_stream_panel/' is missing a server test file (expected: *_server.test.ts). | error |
| 2 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\display_agent_output_stream\open_agent_stream_panel` | Sub-epic 'open_agent_stream_panel/' is missing a client test file (expected: *_client.test.tsx). | error |
| 3 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\display_agent_output_stream\open_agent_stream_panel` | Sub-epic 'open_agent_stream_panel/' is missing a e2e test file (expected: *_e2e.spec.ts). | error |
| 4 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\display_agent_output_stream\open_agent_stream_panel` | Sub-epic 'open_agent_stream_panel/' is missing the 'helpers/' directory for shared test helpers. | error |
| 5 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\display_agent_output_stream\stream_agent_output_in_real_time` | Sub-epic 'stream_agent_output_in_real_time/' is missing a server test file (expected: *_server.test.ts). | error |
| 6 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\display_agent_output_stream\stream_agent_output_in_real_time` | Sub-epic 'stream_agent_output_in_real_time/' is missing a client test file (expected: *_client.test.tsx). | error |
| 7 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\display_agent_output_stream\stream_agent_output_in_real_time` | Sub-epic 'stream_agent_output_in_real_time/' is missing a e2e test file (expected: *_e2e.spec.ts). | error |
| 8 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\display_agent_output_stream\stream_agent_output_in_real_time` | Sub-epic 'stream_agent_output_in_real_time/' is missing the 'helpers/' directory for shared test helpers. | error |
| 9 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\display_agent_output_stream\view_multiple_agent_streams` | Sub-epic 'view_multiple_agent_streams/' is missing a server test file (expected: *_server.test.ts). | error |
| 10 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\display_agent_output_stream\view_multiple_agent_streams` | Sub-epic 'view_multiple_agent_streams/' is missing a client test file (expected: *_client.test.tsx). | error |
| 11 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\display_agent_output_stream\view_multiple_agent_streams` | Sub-epic 'view_multiple_agent_streams/' is missing a e2e test file (expected: *_e2e.spec.ts). | error |
| 12 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\display_agent_output_stream\view_multiple_agent_streams` | Sub-epic 'view_multiple_agent_streams/' is missing the 'helpers/' directory for shared test helpers. | error |
| 13 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\load_board_snapshot\compose_snapshot_from_planning_artifacts` | Sub-epic 'compose_snapshot_from_planning_artifacts/' is missing a server test file (expected: *_server.test.ts). | error |
| 14 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\load_board_snapshot\compose_snapshot_from_planning_artifacts` | Sub-epic 'compose_snapshot_from_planning_artifacts/' is missing a client test file (expected: *_client.test.tsx). | error |
| 15 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\load_board_snapshot\compose_snapshot_from_planning_artifacts` | Sub-epic 'compose_snapshot_from_planning_artifacts/' is missing a e2e test file (expected: *_e2e.spec.ts). | error |
| 16 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\load_board_snapshot\compose_snapshot_from_planning_artifacts` | Sub-epic 'compose_snapshot_from_planning_artifacts/' is missing the 'helpers/' directory for shared test helpers. | error |
| 17 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_lifecycle\bootstrap_agent_from_role_definition` | Sub-epic 'bootstrap_agent_from_role_definition/' is missing a server test file (expected: *_server.test.ts). | error |
| 18 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_lifecycle\bootstrap_agent_from_role_definition` | Sub-epic 'bootstrap_agent_from_role_definition/' is missing a client test file (expected: *_client.test.tsx). | error |
| 19 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_lifecycle\bootstrap_agent_from_role_definition` | Sub-epic 'bootstrap_agent_from_role_definition/' is missing a e2e test file (expected: *_e2e.spec.ts). | error |
| 20 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_lifecycle\bootstrap_agent_from_role_definition` | Sub-epic 'bootstrap_agent_from_role_definition/' is missing the 'helpers/' directory for shared test helpers. | error |
| 21 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_lifecycle\control_agent_lifecycle` | Sub-epic 'control_agent_lifecycle/' is missing a server test file (expected: *_server.test.ts). | error |
| 22 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_lifecycle\control_agent_lifecycle` | Sub-epic 'control_agent_lifecycle/' is missing a client test file (expected: *_client.test.tsx). | error |
| 23 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_lifecycle\control_agent_lifecycle` | Sub-epic 'control_agent_lifecycle/' is missing a e2e test file (expected: *_e2e.spec.ts). | error |
| 24 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_lifecycle\control_agent_lifecycle` | Sub-epic 'control_agent_lifecycle/' is missing the 'helpers/' directory for shared test helpers. | error |
| 25 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_lifecycle\orchestrate_delivery_cycle` | Sub-epic 'orchestrate_delivery_cycle/' is missing a server test file (expected: *_server.test.ts). | error |
| 26 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_lifecycle\orchestrate_delivery_cycle` | Sub-epic 'orchestrate_delivery_cycle/' is missing a client test file (expected: *_client.test.tsx). | error |
| 27 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_lifecycle\orchestrate_delivery_cycle` | Sub-epic 'orchestrate_delivery_cycle/' is missing a e2e test file (expected: *_e2e.spec.ts). | error |
| 28 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_lifecycle\orchestrate_delivery_cycle` | Sub-epic 'orchestrate_delivery_cycle/' is missing the 'helpers/' directory for shared test helpers. | error |
| 29 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_lifecycle\read_agent_activity` | Sub-epic 'read_agent_activity/' is missing a server test file (expected: *_server.test.ts). | error |
| 30 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_lifecycle\read_agent_activity` | Sub-epic 'read_agent_activity/' is missing a client test file (expected: *_client.test.tsx). | error |
| 31 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_lifecycle\read_agent_activity` | Sub-epic 'read_agent_activity/' is missing a e2e test file (expected: *_e2e.spec.ts). | error |
| 32 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_lifecycle\read_agent_activity` | Sub-epic 'read_agent_activity/' is missing the 'helpers/' directory for shared test helpers. | error |
| 33 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_pool\adjust_wip_policy` | Sub-epic 'adjust_wip_policy/' is missing a server test file (expected: *_server.test.ts). | error |
| 34 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_pool\adjust_wip_policy` | Sub-epic 'adjust_wip_policy/' is missing a client test file (expected: *_client.test.tsx). | error |
| 35 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_pool\adjust_wip_policy` | Sub-epic 'adjust_wip_policy/' is missing a e2e test file (expected: *_e2e.spec.ts). | error |
| 36 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_pool\adjust_wip_policy` | Sub-epic 'adjust_wip_policy/' is missing the 'helpers/' directory for shared test helpers. | error |
| 37 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_pool\display_agent_pool` | Sub-epic 'display_agent_pool/' is missing a server test file (expected: *_server.test.ts). | error |
| 38 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_pool\display_agent_pool` | Sub-epic 'display_agent_pool/' is missing a client test file (expected: *_client.test.tsx). | error |
| 39 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_pool\display_agent_pool` | Sub-epic 'display_agent_pool/' is missing a e2e test file (expected: *_e2e.spec.ts). | error |
| 40 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\manage_agent_pool\display_agent_pool` | Sub-epic 'display_agent_pool/' is missing the 'helpers/' directory for shared test helpers. | error |
| 41 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\operate_board_in_manual_mode\assign_team_member_agent_to_ticket` | Sub-epic 'assign_team_member_agent_to_ticket/' is missing a server test file (expected: *_server.test.ts). | error |
| 42 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\operate_board_in_manual_mode\assign_team_member_agent_to_ticket` | Sub-epic 'assign_team_member_agent_to_ticket/' is missing a client test file (expected: *_client.test.tsx). | error |
| 43 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\operate_board_in_manual_mode\assign_team_member_agent_to_ticket` | Sub-epic 'assign_team_member_agent_to_ticket/' is missing a e2e test file (expected: *_e2e.spec.ts). | error |
| 44 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\operate_board_in_manual_mode\assign_team_member_agent_to_ticket` | Sub-epic 'assign_team_member_agent_to_ticket/' is missing the 'helpers/' directory for shared test helpers. | error |
| 45 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\operate_board_in_manual_mode\preserve_manual_mode_on_ticket_move` | Sub-epic 'preserve_manual_mode_on_ticket_move/' is missing a server test file (expected: *_server.test.ts). | error |
| 46 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\operate_board_in_manual_mode\preserve_manual_mode_on_ticket_move` | Sub-epic 'preserve_manual_mode_on_ticket_move/' is missing a client test file (expected: *_client.test.tsx). | error |
| 47 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\operate_board_in_manual_mode\preserve_manual_mode_on_ticket_move` | Sub-epic 'preserve_manual_mode_on_ticket_move/' is missing a e2e test file (expected: *_e2e.spec.ts). | error |
| 48 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\operate_board_in_manual_mode\preserve_manual_mode_on_ticket_move` | Sub-epic 'preserve_manual_mode_on_ticket_move/' is missing the 'helpers/' directory for shared test helpers. | error |
| 49 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\visualize_delivery_board\display_board_layout` | Sub-epic 'display_board_layout/' is missing a server test file (expected: *_server.test.ts). | error |
| 50 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\visualize_delivery_board\display_board_layout` | Sub-epic 'display_board_layout/' is missing a client test file (expected: *_client.test.tsx). | error |
| 51 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\visualize_delivery_board\display_board_layout` | Sub-epic 'display_board_layout/' is missing a e2e test file (expected: *_e2e.spec.ts). | error |
| 52 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\visualize_delivery_board\display_board_layout` | Sub-epic 'display_board_layout/' is missing the 'helpers/' directory for shared test helpers. | error |
| 53 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\visualize_delivery_board\display_ticket_cards` | Sub-epic 'display_ticket_cards/' is missing a server test file (expected: *_server.test.ts). | error |
| 54 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\visualize_delivery_board\display_ticket_cards` | Sub-epic 'display_ticket_cards/' is missing a client test file (expected: *_client.test.tsx). | error |
| 55 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\visualize_delivery_board\display_ticket_cards` | Sub-epic 'display_ticket_cards/' is missing a e2e test file (expected: *_e2e.spec.ts). | error |
| 56 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\visualize_delivery_board\display_ticket_cards` | Sub-epic 'display_ticket_cards/' is missing the 'helpers/' directory for shared test helpers. | error |
| 57 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\visualize_delivery_board\inspect_skill_progress` | Sub-epic 'inspect_skill_progress/' is missing a server test file (expected: *_server.test.ts). | error |
| 58 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\visualize_delivery_board\inspect_skill_progress` | Sub-epic 'inspect_skill_progress/' is missing a client test file (expected: *_client.test.tsx). | error |
| 59 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\visualize_delivery_board\inspect_skill_progress` | Sub-epic 'inspect_skill_progress/' is missing a e2e test file (expected: *_e2e.spec.ts). | error |
| 60 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\domain\visualize_delivery_board\inspect_skill_progress` | Sub-epic 'inspect_skill_progress/' is missing the 'helpers/' directory for shared test helpers. | error |

### 🟥 Casing Transform Scanner — 15 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\shared\KanbanBoard.ts` | Property 'run_when' in KanbanBoard.ts uses snake_case. TypeScript properties must be camelCase: 'runWhen'. | error |
| 2 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\shared\KanbanBoard.ts` | Property 'stage_work_required' in KanbanBoard.ts uses snake_case. TypeScript properties must be camelCase: 'stageWorkRequired'. | error |
| 3 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\shared\KanbanBoard.ts` | Property 'ticket_id' in KanbanBoard.ts uses snake_case. TypeScript properties must be camelCase: 'ticketId'. | error |
| 4 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\shared\KanbanBoard.ts` | Property 'agent_role' in KanbanBoard.ts uses snake_case. TypeScript properties must be camelCase: 'agentRole'. | error |
| 5 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\shared\KanbanBoard.ts` | Property 'created_at' in KanbanBoard.ts uses snake_case. TypeScript properties must be camelCase: 'createdAt'. | error |
| 6 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\shared\KanbanBoard.ts` | Property 'board_mode' in KanbanBoard.ts uses snake_case. TypeScript properties must be camelCase: 'boardMode'. | error |
| 7 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\shared\KanbanBoardLoader.ts` | Property 'board_mode' in KanbanBoardLoader.ts uses snake_case. TypeScript properties must be camelCase: 'boardMode'. | error |
| 8 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\shared\Ticket.ts` | Property 'entered_stage' in Ticket.ts uses snake_case. TypeScript properties must be camelCase: 'enteredStage'. | error |
| 9 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\shared\Ticket.ts` | Property 'completed_stage' in Ticket.ts uses snake_case. TypeScript properties must be camelCase: 'completedStage'. | error |
| 10 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\shared\Ticket.ts` | Property 'scatter_from' in Ticket.ts uses snake_case. TypeScript properties must be camelCase: 'scatterFrom'. | error |
| 11 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\shared\Ticket.ts` | Property 'scatter_to' in Ticket.ts uses snake_case. TypeScript properties must be camelCase: 'scatterTo'. | error |
| 12 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\server\AgentSession.ts` | Property 'message_count' in AgentSession.ts uses snake_case. TypeScript properties must be camelCase: 'messageCount'. | error |
| 13 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\server\AgentSession.ts` | Property 'last_activity_sec' in AgentSession.ts uses snake_case. TypeScript properties must be camelCase: 'lastActivitySec'. | error |
| 14 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\server\AgentSession.ts` | Property 'final_message' in AgentSession.ts uses snake_case. TypeScript properties must be camelCase: 'finalMessage'. | error |
| 15 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\server\AgentSession.ts` | Property 'error_detail' in AgentSession.ts uses snake_case. TypeScript properties must be camelCase: 'errorDetail'. | error |

### 🟥 Infrastructure Boundary Scanner — 3 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\shared\KanbanBoard.ts` | Method 'resolvePlanningPaths' in shared/KanbanBoard.ts accepts infrastructure arg 'planningRoot'. Infrastructure context should be resolved at the controller/boundary, not passed into domain methods. | error |
| 2 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\shared\KanbanBoard.ts` | Method 'engagementWorkspaceFromPlanningRoot' in shared/KanbanBoard.ts accepts infrastructure arg 'planningRoot'. Infrastructure context should be resolved at the controller/boundary, not passed into domain methods. | error |
| 3 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\shared\KanbanBoardLoader.ts` | Method 'fromSources' in shared/KanbanBoardLoader.ts accepts infrastructure arg 'planningRoot'. Infrastructure context should be resolved at the controller/boundary, not passed into domain methods. | error |

### 🟥 Share Domain Logic Scanner — 2 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\server` | Domain 'kanban/server/' repositories do not import the Zod schema from shared/. Repositories must call Schema.parse(doc) to validate raw database documents. | error |
| 2 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\client` | Domain 'kanban/client/' does not import the Zod schema from shared/. Forms and API clients must validate user input with the shared schema via safeParse(). | warning |

### 🟥 Entity Behavior Scanner — 1 violation(s)

| # | Location | Message | Severity |
|---|----------|---------|----------|
| 1 | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\packages\kanban\server` | Domain 'kanban/server/' repository files do not import from 'mongodb'. Add a MongoDB-backed repository implementation. | error |
