# Thin slicing -- incremental backlog

## Product / context

**Product:** Delivery Agent Kanban — real-time board for an agentic delivery pipeline.

**Spine vs optional:** The spine for manual mode is: toggle mode → assign agent → execute skill → persist and reflect result. Parallel execution on a single ticket is spine (core value proposition). Cancel/revoke of an in-flight assignment is optional (context gap — not yet confirmed).

## Increments

### Increment 1: `Manual skill assignment`

**Outcome:** The *Delivery Lead* switches to *manual mode*, drags a *Team Member Agent* onto a *ticket*, and watches the assigned *skill* execute — with each state transition (in progress, skill done, ticket done) reflected on the board in real time.

**Slicing notes:** This is the full vertical slice for manual mode: UI toggle → state file mechanism → agent detection and delegation → skill execution → board reflection. Parallel execution of multiple skills on a single ticket is included because it is core to the value proposition (manual mode's advantage over automatic sequential flow). The existing polling and file-watching infrastructure (Poll Board Changes, Watch War Room Files) is reused — no new transport is introduced.

**Stories in this increment** *(order reflects flow within the slice):*

- *Toggle Manual Mode*
- *Persist Board Mode Setting*
- *Read Board Mode Setting And Switches to Manual Mode*
- *Drag Team Member Agent onto Ticket*
- *Record Action Intent in State File*
- *Detect State File Change*
- *Delegate Skill to Team Member Agent*
- *Execute Assigned Skill on Ticket*
- *Advance Ticket to In Progress on First Skill Start*
- *Move Ticket to In Progress on Agent Advance*
- *Persist Skill Completion to Board State*
- *Update Skill Status on Completion*
- *Complete Ticket When All Skills Finish*
- *Move Ticket to Done on Agent Completion*
