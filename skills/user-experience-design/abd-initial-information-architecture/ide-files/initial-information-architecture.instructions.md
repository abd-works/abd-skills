# Initial information architecture skill

When the user asks for an **information architecture**, **site map**, **screen flow**, **screen inventory**, **navigation**, or **content model** for an increment, epic, sprint, or other scope, use **`skills/user-experience-design/abd-initial-information-architecture/SKILL.md`**. Read that skill and its bundled rules before drawing.

## Required flow

1. **Resolve three inputs:** path to `story-map.md`, scope filter (increment number, epic name, sprint, etc.), path to the ubiquitous-language file for that scope. If any is missing, ask — do not guess.
2. **Apply the bundled rules while drawing**, not after. The rules cover: UX terms for structural pieces, domain term names (linked) for subject matter, regions are named regions only (no controls), system stories grouped with the closest visible-trigger screen, labels are clear and consistently named, mental-model alignment over technical decomposition.
3. **Author `docs/ux/initial-ia.md` first**, then **launch abd-canvas** at `$env:ABD_CANVAS_PATH` (default `C:\dev\abd-canvas`), drive the chat panel with `templates/initial-ia-prompt.md`, then save `<engagement>/docs/ux/initial-ia.tldr` and `<engagement>/docs/ux/initial-ia.svg`. Sync canvas changes back into `initial-ia.md`.
4. **Log mistakes inside this skill — immediately, same turn.** When output is wrong, follow the workspace `correct-output` rule and write the entry to `skills/user-experience-design/abd-initial-information-architecture/corrections-log.md` in the same turn you fix the output.

## Key constraints

- Stories and the ubiquitous language are **sources**, not subjects. On the canvas, story and domain references appear as **names + links**, never as full definitions or acceptance criteria.
- UX terms carry the structure (screen, region, sidebar, header, footer, primary nav, content type, action, label, tag). Domain term names (linked) carry the subject matter.
- Regions list named surfaces only — no controls, no copy, no wireframe detail (those belong in `abd-lo-fi`).
- System stories never get their own screen; they group with the closest user-visible screen.
- Screens reflect the user's mental model, not the technical decomposition (no services, view models, durable objects).

## When this rule does NOT apply

- Lo-fi or hi-fi wireframing (use `abd-lo-fi` or `abd-hi-fi`).
- Production interface implementation (use `abd-interface-design`).
- Editing the saved `.tldr` or `.svg` outside the canvas (always edit on the canvas and re-save).
