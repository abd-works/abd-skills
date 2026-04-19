# Discovery

## Purpose

Transform raw context — business goals, stakeholder conversations, documents — into a structured story map that represents the product as a hierarchy of actors, epics, features, and stories.

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
