# Discovery

## Purpose

Transform raw context — business goals, stakeholder conversations, documents — into a structured story map that represents the product as a hierarchy of actors, epics, features, and stories.

A story map is a collaborative method for breaking work down. It provides a structure to guide collaborative thought in order to achieve shared understanding. The map is a lightweight, two-dimensional arrangement of stories: a sequential narrative from left to right, and a prioritization from top to bottom. It establishes approximately 80% of scope initially, with room for incremental growth, and creates the backlog the team will deliver against.

Discovery focuses on **what you are working on**, not **the way you work** — it is important to understand the distinction. The output is a highly visible representation of end-to-end product scope and a site for conversation that is accessible and useful for setting context.

## Why this stage matters

- **Alignment:** Creates shared understanding among the team building the product and stakeholders affected by the product.
- **Decomposition:** Systematically breaks a project into smaller units of business value that support iterative delivery.
- **Scope visibility:** A cross-functional team (SMEs, analysts, developers, testers, delivery lead) acquires various viewpoints early, reducing costly surprises downstream.
- **Backlog creation:** The map directly produces an ordered backlog — not a flat list, but a structured representation of user journeys.

## Team role

**Product Owner**

## Practice skill

`abd-story-mapping` — Patton-style story mapping: epics, sub-epics, stories, verb–noun naming, actors via `story_type`.

## Entry conditions

- Workspace is set and accessible.
- At least one context source exists: scope brief, business document, stakeholder notes, or prior material under `<workspace>/context/` or attached to the session.

## Expected outputs

- `story-graph.json` (or `docs/story/story-graph.json`) with at least one epic, its sub-epics, and leaf stories.
- Rendered story map artifacts in `templates/` (`story-map.md` and `story-map.txt`) with the same tree coverage.

## Key questions (is this stage done?)

1. Can someone new to the project read the map left-to-right and understand the end-to-end user journey?
2. Does the map cover the actors who will interact with the product, not just one perspective?
3. Are epics named as verb–noun activities (what users do), not noun-only labels?
4. Is there enough story depth that the team could estimate at the epic level?
5. Has the team walked through the map together and confirmed it represents their shared understanding?
6. Are there any known user journeys or business goals from the scope that are not yet represented?

## Conditions of success

- The map reads as a **narrative**: a stakeholder can walk through it left to right and see the product's flow.
- Every epic has at least one sub-epic; every sub-epic has at least one story — no orphan branches.
- Stories use verb–noun naming and are assigned to an actor.
- Domain vocabulary is captured and consistent across the map — actors, concepts, and terms that will carry through all downstream stages.
- The map is a site for conversation, not a final document — it is understood that it will grow incrementally.

## Exit gate

1. `story-graph.json` passes structural validation: `story_graph_cli.py read --file <path>` exits 0.
2. Practice skill scanners pass: `run_scanners.py --skill-root <abd-story-mapping> --workspace <workspace>` exits 0.
3. Every epic has at least one sub-epic; every sub-epic has at least one story.
4. Stories use verb–noun naming and are assigned to an actor.
5. Rendered templates (`story-map.md`, `story-map.txt`) exist and reflect the graph.
6. The user has confirmed the map at a team-member checkpoint.

## Handoff to next stage

Pass forward:
- Path to `story-graph.json`.
- Rendered map files.
- Any open questions or areas flagged for deeper exploration.
- Actor and domain vocabulary established during mapping.
