(E) Visualize Delivery Board
    (E) Display Board Layout
        (S) System --> Organize Tickets into Stage Groups by Delivery Phase
        (S) System --> Show Assigned Skills per Stage
        (S) System --> Display Backlog Tickets
        (S) System --> Display Archived Tickets
        (S) System --> Derive Board Title from Ticket Lineage
        (S) System --> Show Last Sync Timestamp
        (S) Delivery Lead --> Switch Display Theme
    (E) Display Ticket Cards
        (S) System --> Render Ticket with Chip Label and Display Name
        (S) System --> Show Active Skill and Agent on Ticket
        (S) System --> Show Focus Skill Between Executions
        (S) System --> Show Review Status on Ticket
        (S) System --> Highlight Blocked Ticket
        (S) System --> Animate Ticket on Position Change
    (E) Inspect Skill Progress
        (S) Delivery Lead --> Expand Ticket Skill List
        (S) System --> Show Skill Execution and Completion Indicators
        (S) System --> Color-Code Skills by Family

(E) Load Board Snapshot
    (E) Compose Snapshot from Planning Artifacts
        (S) System --> Read Board JSON and System of Work from Disk
        (S) System --> Validate Board Data Structure
        (S) System --> Enrich Tickets with Display State
        (S) System --> Map System of Work to Stage Skill Rails
        (S) System --> Read Agent Status from Cursor SDK
    (E) Serve Board Snapshot
        (S) System --> Return Board Snapshot via API
        (S) System --> Return Not Modified on Matching ETag
        (S) System --> Report Error When Board File Missing

(E) Poll Board Changes
    (S) System --> Poll Board Snapshot at Interval
    (S) System --> Skip Fetch on Matching ETag
    (S) System --> Change ETag on Skill State Transition
    (S) System --> Detect Ticket Position Changes Between Polls
    (S) System --> Show Loading State During Fetch
    (S) System --> Show Error on Poll Failure

(E) Manage Agent Pool
    (E) Display Agent Pool
        (S) System --> Render Agent Avatars by Role
        (S) System --> Show Role Engagement in Agent Pool
        (S) System --> Indicate Agent Liveness from SDK Status
        (S) System --> Display Kanban Lead Status
    (E) Adjust WIP Policy
        (S) Delivery Lead --> Adjust Executor Count for Role
        (S) System --> Persist WIP Policy Change to Board JSON

(E) Configure Planning Folder
    (S) Delivery Lead --> Connect to Planning Folder
    (S) System --> Validate Planning Folder on Disk
    (S) System --> Persist Planning Root Configuration
    (S) Delivery Lead --> Refresh Board from Disk

(E) Watch War Room Files
    (S) System --> Start File Watcher on Planning Root Connection
    (S) System --> Monitor Kanban Directory for Board and Config Changes
    (S) System --> Invalidate Cached Snapshot on Watched File Change

(E) Manage Agent Lifecycle via Cursor SDK
    (E) Bootstrap Agent from Role Definition
        (S) System --> Resolve Agent Definition from Role
        (S) System --> Parse Skills from Agent Definition
        (S) System --> Create Agent Session via Cursor SDK
        (S) System --> Deliver Bootstrap Prompt with Workspace and Role
    (E) Control Agent Lifecycle
        (S) Kanban Lead --> Start Team Member Agent
        (S) Kanban Lead --> Stop Team Member Agent
        (S) System --> Report Agent Session Status via SDK
        (S) Kanban Lead --> Restart Stale Agent
        (S) System --> Detect Agent Completion via SDK
    (E) Read Agent Activity
        (S) System --> Stream Agent Messages via SDK
        (S) System --> Derive Agent Liveness from SDK Session State
        (S) System --> Update Skill Progress from Agent Output
    (E) Orchestrate Delivery Cycle
        (S) Kanban Lead --> Run Scan Cycle
        (S) Kanban Board --> Pull Tickets from Backlog per WIP
        (S) Ticket --> Detect Stage Completion
        (S) Kanban Board --> Scatter Ticket at Scope Boundary
        (S) Kanban Board --> Advance Ticket to Next Stage
        (S) Kanban Lead --> Dispatch Skill to Idle Team Member
        (S) Kanban Lead --> Spawn Team Member for Dead Slot

(E) Operate Board in Manual Mode
    (E) Switch Board Mode
        (S) User --> Toggle Manual Mode
        (S) App --> Persist Board Mode Setting
        (S) App --> Preserve Board Mode on Ticket Move
        (S) Kanban Lead --> Read Board Mode Setting
    (E) Assign Team Member Agent to Ticket
        (S) User --> Drag Team Member Agent onto Ticket
        (S) App --> Keep Agent Drop from Triggering Ticket Move
        (S) App --> Record Action Intent
        (S) Kanban Lead --> Process Action Intent
        (S) Kanban Lead --> Delegate Skill to Team Member Agent via SDK
        (S) Team Member Agent --> Execute Assigned Skill on Ticket
        (S) Team Member Agent --> Advance Ticket to In Progress on First Skill Start
        (S) App --> Move Ticket to In Progress on Agent Advance
        (S) Team Member Agent --> Persist Skill Completion to Board State
        (S) App --> Update Skill Status on Completion
        (S) Team Member Agent --> Complete Ticket When All Skills Finish
        (S) App --> Move Ticket to Done on Agent Completion
        (S) App --> Keep Manually Dropped Done Ticket in Done

(E) Display Agent Output Stream
    (E) Open Agent Stream Panel
        (S) User --> Expand Agent Stream by Clicking Team Member Avatar
        (S) System --> Anchor Stream Panel beside Active Ticket Stage Column
        (S) System --> Size Stream Panel to Match Stage Column Height
        (S) User --> Collapse Agent Stream Panel
    (E) View Multiple Agent Streams
        (S) User --> Open Second Agent Stream While First Is Open
        (S) System --> Stack Stream Panels Side by Side
        (S) User --> Close Individual Stream Panel
    (E) Stream Agent Output in Real Time
        (S) System --> Stream Agent Messages to Panel Like IDE Chat
        (S) System --> Show Agent Thinking Indicator in Stream
        (S) System --> Show Agent Status Changes in Stream
        (S) User --> Scroll Agent Stream History

## Consolidation Notes (for AC phase)

### Resolve Agent Definition from Role
Agent class reads `AGENT.md` from `practices/kanban/agents/{role}/AGENT.md` to locate the correct agent definition. The agent role string maps to a folder name (e.g. `engineer` → `agents/engineer/AGENT.md`). The AGENT.md contains skills, workflow, and identity.

### Parse Skills from Agent Definition
Agent class parses the AGENT.md to extract:
- Skill names to invoke (from "Your skills" section and stage work required references)
- Workflow instructions (from executor-workflow.md references)
- Role identity and bootstrap parameters

### Create Agent Session via Cursor SDK
Replaces the Python Task-tool spawn pattern. Uses `@cursor/sdk` or `cursor-sdk` to create an Agent session with:
- The bootstrap prompt (workspace, role, instance)
- MCP server configuration for the agent
- Background execution mode

### Stream Agent Messages via SDK
Replaces heartbeat-file polling. The SDK `run.stream` or `run.messages` provides real-time agent output. Each message updates the server's knowledge of agent activity without file I/O.

### Adjust Executor Count for Role
Consolidates increment (+1) and decrement (-1) into one parameterized story.
AC must specify per variant:
- Increment: adds one executor slot for the role; no upper bound enforced by UI
- Decrement: removes one executor slot; button disabled at zero (cannot go below zero)
- Both: server persists updated WIP policy to board.json and returns refreshed snapshot

### Toggle Manual Mode
Consolidates enable and disable into one toggle story.
AC must specify per variant:
- Enable: board enters manual mode; automatic lead actions (pull, scatter, advance) are suppressed; UI enables drag-assign interaction on agent pool
- Disable: board returns to automatic mode; lead resumes autonomous actions; drag-assign interaction is disabled

### Execute Assigned Skills in Parallel on Ticket (multiple agents, single ticket)
AC must specify:
- Each skill assignment starts independently; no ordering enforced among parallel skills
- Each running skill has its own SkillProgress entry with independent execution and review status
- Ticket state transitions are governed by the aggregate of all assigned skill states (see Advance/Complete stories)

### Orchestrate Delivery Cycle
Consolidates the scan cycle steps previously handled by Python scripts (`run_kanban_lead_tick.py`, `run_kanban_scan.py`, `lead_pull.py`, `lead_dispatch.py`, `scatter_ticket.py`). Each story covers one step of the scan cycle, now implemented in Node/TS on the server layer.

### Display Agent Output Stream
Click a team member avatar in the agent pool → a stream panel expands beside the stage column where that team member's active ticket lives. The panel is the same height as the stage column. Output streams like an IDE chat — messages, thinking indicators, and status changes appear in real time. Click the avatar again or a close button to collapse. Clicking a second team member while the first is open opens a second panel beside the first — multiple panels stack side by side. Each panel is independently scrollable and collapsible.

## Context Gaps
- `scatter_from` and `scatter_to` fields defined on Ticket schema but not rendered in any board component — confirm whether cross-stage scatter visualization is planned.
- `metricsLogFile`, `strategyFile`, and `manifestFile` paths defined in `PlanningPaths` but not consumed by any board feature — confirm whether these feed future dashboard views.
- Cursor SDK authentication model — confirm whether the SDK requires API keys, OAuth tokens, or relies on the IDE's existing authentication.
- Agent MCP server configuration — confirm which MCP servers each agent role should have access to when created via the SDK.
- Agent session persistence — confirm whether agent sessions should survive server restarts or are transient (re-created on server start if the board has active work).
- Chat log data retention — confirm whether streamed agent messages are persisted to disk or held in memory only for the current session.
- Cancel or remove assigned skill — confirm whether the user can revoke a manual skill assignment after it has been recorded but before the agent completes it.
