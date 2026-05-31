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
        (S) System --> Read Agent Heartbeat Ages
    (E) Serve Board Snapshot
        (S) System --> Return Board Snapshot via API
        (S) System --> Return Not Modified on Matching ETag
        (S) System --> Report Error When Board File Missing

(E) Poll Board Changes
    (S) System --> Poll Board Snapshot at Interval
    (S) System --> Skip Fetch on Matching ETag
    (S) System --> Detect Ticket Position Changes Between Polls
    (S) System --> Show Loading State During Fetch
    (S) System --> Show Error on Poll Failure

(E) Manage Agent Pool
    (E) Display Agent Pool
        (S) System --> Render Agent Avatars by Role
        (S) System --> Show Role Engagement in Agent Pool
        (S) System --> Indicate Agent Liveness from Heartbeat
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

## Consolidation Notes (for AC phase)

### Adjust Executor Count for Role
Consolidates increment (+1) and decrement (-1) into one parameterized story.
AC must specify per variant:
- Increment: adds one executor slot for the role; no upper bound enforced by UI
- Decrement: removes one executor slot; button disabled at zero (cannot go below zero)
- Both: server persists updated WIP policy to board.json and returns refreshed snapshot

## Context Gaps
- `scatter_from` and `scatter_to` fields defined on Ticket schema but not rendered in any board component — confirm whether cross-stage scatter visualization is planned.
- `metricsLogFile`, `strategyFile`, and `manifestFile` paths defined in `PlanningPaths` but not consumed by any board feature — confirm whether these feed future dashboard views.
- Board is read-only visualization (no manual ticket movement or state changes by the Delivery Lead, except WIP policy) — confirm whether manual ticket management is planned or if read-only agent-driven state is the intended design.
