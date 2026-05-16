---
name: abd-lo-fi
description: >-
  Turn one screen from the initial information architecture plus its acceptance
  criteria and the domain terms that appear in its stories into a lo-fi
  wireframe — drawn on an abd-canvas whiteboard and saved as a versioned
  artifact.
---
# abd-lo-fi

## Purpose

A lo-fi wireframe is the first place stories, acceptance criteria, and domain vocabulary meet a layout. It is also the first place precision really matters: every label on the screen should be a term a domain expert recognises, every behaviour the screen affords should map to a specific acceptance criterion, and every region should come from the initial information architecture. This skill packages that pass — pick one screen, gather only the acceptance criteria and domain terms that belong to its stories, drive the `abd-canvas` agent with a structured prompt, and save the result — so the wireframe stays honest to the team's stories and domain instead of drifting into invented vocabulary or designer guesswork.

---

## When to use this skill

Load this skill when **any** of the following apply:

- You have an **initial information architecture** from `abd-initial-information-architecture` and want to **draw one of its screens** as a lo-fi wireframe.
- You have a screen, its **acceptance criteria**, and the **domain terms** that appear in its stories, and you want the labels and affordances on the screen to be **exactly** those terms and criteria.
- The current wireframe **drifted** from the stories or domain (invented labels, missing acceptance criteria, controls that no story justifies) and you want to regenerate it cleanly.
- You want to compare an existing UI sketch against the stories and acceptance criteria and surface gaps **at the layout level**, before any visual design work.

---

## What is a lo-fi wireframe

A **lo-fi wireframe** is a low-fidelity, layout-only drawing of one screen. It shows:

- The **named regions** of the screen (from the initial IA) as containers.
- The **affordances** each region offers (controls, lists, inputs, messages) labelled with **domain terms verbatim**.
- The **acceptance criteria** for the screen's stories rendered exactly as in the source, attached to the canvas where reviewers can read them next to the layout.

It does not show visual design (colour, typography, brand polish, exact spacing). It does not implement code. It does not invent vocabulary. It is a structural conversation in domain language about what this screen affords and what conditions it must satisfy.

---

## Core concepts

### Screen scope

A lo-fi pass covers exactly one screen, identified by its name on the initial IA (`docs/ux/initial-ia.tldr` produced by `abd-initial-information-architecture`). Only the stories, acceptance criteria, and domain terms that belong to that screen are in scope. Pulling in stories from another screen "for context" is a fail condition because it drags vocabulary the user will not see on this screen onto the canvas.

### Domain terms — verbatim, screen-scoped

The domain terms shown on the wireframe come from the ubiquitous-language (UL) file, copied character-for-character — definitions included where the prompt shows them. Only terms whose stories appear on this screen may be included. A term defined in the UL but not referenced by any of this screen's stories does not belong on this canvas.

### Acceptance criteria — verbatim

The acceptance criteria attached to the wireframe come from the acceptance-criteria file, copied character-for-character. Reworded, shortened, merged, or paraphrased criteria are a fail. The canvas is the place the AC become visible to a reviewer; mutating them on the way to the canvas destroys their authority.

### Affordance

An **affordance** is a place on the screen that a user can act on or read — a button, a list, an input field, an error area, a status indicator. Every affordance must trace back to an acceptance criterion or a domain term in scope. Affordances without that traceback are decoration; they belong in `abd-hi-fi` or `abd-interface-design`, not here.

### User flow

The order in which a user moves through the affordances on this screen to complete a task. The wireframe should not actively obstruct that flow: the primary action sits in the eye-path, prerequisite information sits where the user looks for it, and the user does not need to scroll or hunt for affordances that the acceptance criteria say are required.

### Feedback and error states

Where the acceptance criteria require feedback (success, in-progress, error, validation), the wireframe shows the region where that feedback appears, labelled in domain terms. The exact copy is verbatim from AC; if the AC do not specify copy, the region shows a placeholder marked clearly as a placeholder.

### Accessibility, at the lo-fi level

Lo-fi accessibility is structural: heading order is implied by the layout, every input has a visible label drawn from the UL or AC, and meaning is never conveyed by colour alone. Pixel-level accessibility (contrast, focus styles, ARIA roles) belongs in `abd-interface-design`.

### Rules

`rules/*.md` validate the output (the drawn canvas and the saved `lo-fi.tldr` / `lo-fi.svg`). Build steps live in **Build**.

---

## The shape of a good lo-fi wireframe

```
SCREEN: game directory prompt

REGIONS (from initial IA):
  prompt panel
    - heading: "COH game directory not found or invalid"
    - explanatory text area
  path input area
    - "COH game directory path" input
    - "Browse..." control
  error message area
    - validation error placeholder (shown when path is wrong)
  continue control area
    - "Continue" control (enabled only when COH game directory is valid)

ACCEPTANCE CRITERIA attached to canvas:
  Story: Validate City of Heroes Game Directory
    1. WHEN the application starts THEN the system checks that the stored
       COH game directory path exists on disk and contains the expected
       content AND proceeds to open the crowd manager if the check passes
    [...verbatim, all AC for this screen...]
```

Every label is a UL term or copy from the AC. Every affordance traces back to a specific AC. The acceptance criteria are placed beside the layout so a reviewer can read both at once.

---

## Build

**Goal:** Read the inputs for one screen, drive the `abd-canvas` agent with a structured prompt that contains the screen name, the regions from the initial IA, the verbatim acceptance criteria, and the verbatim screen-scoped domain terms, and save the drawn wireframe as `lo-fi.tldr` and `lo-fi.svg` in the engagement's `docs/ux/` folder.

1. **Resolve inputs.** Confirm five inputs are available: a path to `story-map.md`, a path to the ubiquitous-language file, a path to the acceptance-criteria file, the screen name (must match a screen on the initial IA), and a mode (`interactive` or `headless`). If any is missing, ask the user.

2. **Look up the screen on the initial IA.** Open `docs/ux/initial-ia.tldr` (or `.svg`) and find the screen by name. Read its regions — the named surfaces — and the system stories grouped inside it. These define the structural skeleton of the wireframe.

3. **Collect the in-scope stories.** From the story map, list every story attached to this screen (user-visible stories plus the grouped system stories). Do not include stories from any other screen.

4. **Extract acceptance criteria, verbatim.** From the AC file, copy every acceptance criterion for every in-scope story, character-for-character, into a single block. Preserve the story headings, numbering, and clause wording exactly.

5. **Extract domain terms, screen-scoped and verbatim.** From the UL file, copy every term whose definition is referenced by an in-scope story for this screen. Each term: its name and its full definition, verbatim. Do not include terms that belong only to other screens.

6. **Author or update `docs/ux/lo-fi.md` first.** Copy `templates/lo-fi.md` into the engagement's `docs/ux/` folder (or open the existing one) and fill in: screen name, source paths, description, regions (carried over from the initial IA), affordances per region with `Trace` column pointing at the AC clause or UL term that justifies each one, in-scope stories, UL excerpt (verbatim, screen-scope only), and AC (verbatim). This markdown is the structured spec the canvas is drawn from; the canvas is never authored without it.

7. **Resolve the abd-canvas location.** Look up `$env:ABD_CANVAS_PATH`. If unset, default to `C:\dev\abd-canvas`. If the folder does not exist, stop and tell the user where to clone or install the canvas.

8. **Run interactive or headless mode.**

   - **Interactive:** run `npm install` if `node_modules` is missing, then `npm run dev` in the canvas folder. Open `http://localhost:5173` via the browser MCP. Fill `templates/lo-fi-prompt.md` from `docs/ux/lo-fi.md` and paste it into the canvas chat panel. Let the agent draw.
   - **Headless:** POST the filled prompt (also derived from `docs/ux/lo-fi.md`) to the canvas agent HTTP endpoint, wait for completion, and write the returned `.tldr` snapshot directly to disk. No browser involved.

9. **Save canvas outputs.** When the agent finishes, click the `Save .tldr` button in the canvas helper-button row (interactive) or write the snapshot to disk (headless) at `<engagement>/docs/ux/lo-fi.tldr`. Then export an SVG of the same canvas to `<engagement>/docs/ux/lo-fi.svg`. Overwrite both files on every run.

10. **Sync canvas changes back into `lo-fi.md`.** Read the updated canvas. If the agent renamed an affordance, moved one between regions, added a region that was missing, or changed any label, update `docs/ux/lo-fi.md` to match — same regions, same affordances, same labels, same traces. Append a row to the change log with date, direction (`canvas → md`), and a one-line summary.

11. **Apply the rules, then review like a peer.** Walk every file under `rules/` against the drawn canvas, the saved files, and the markdown spec. Fix every violation before declaring success.

12. **Keep the bundled rules block honest.** Whenever you change a file under `rules/`, re-run the bundler so the rule prose inlined at the end of this `SKILL.md` matches what is on disk:

```bash
python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/user-experience-design/abd-lo-fi
```

- **Outputs:** `docs/ux/lo-fi.md` (structured spec), `docs/ux/lo-fi.tldr` (canvas), `docs/ux/lo-fi.svg` (flat export) — three artifacts in the engagement's deliverables folder, kept in sync.
- **Per format:** `.md` is the structured spec — created first, updated after canvas changes. `.tldr` is the round-tripable canvas. `.svg` is the flat artifact for documentation and reviews.
- **While writing:** Labels and copy are verbatim from the UL and the AC. Every affordance traces to an AC or a UL term. No invented vocabulary. No visual design.

---

## Validate

**Goal:** Read the saved canvas as reviewers, not a second authoring pass.

- **Who is checking:** the product owner reads the AC block beside the layout and verifies every criterion is rendered somewhere on the screen; a domain expert verifies every label is a UL term used the way the UL defines it; a UX practitioner checks the user flow for friction and the structural accessibility of the layout.
- **Cross-artifact parity:** the `.tldr` and `.svg` are exports of the same canvas.

Walk the canvas and confirm:

- Every region on the canvas matches a region from the initial IA for this screen.
- Every label is a UL term verbatim or copy from an AC clause.
- Every acceptance criterion for an in-scope story is shown on the canvas, character-for-character.
- No story or domain term from another screen appears on the canvas.
- Every affordance traces back to an AC clause or a UL term.
- `docs/ux/lo-fi.tldr` and `docs/ux/lo-fi.svg` both exist and reflect the current canvas.

---

## Deploy

This skill ships IDE-deployable files under `ide-files/`. Deploy them from the repo root using the standard repo-level script:

```powershell
cd C:\dev\agilebydesign-skills
.\scripts\deploy-skills.ps1 -ide cursor -Force
```

`deploy-skills.ps1` auto-discovers every skill under `skills/` with a `SKILL.md` and links its `ide-files/*.mdc` into `<deploy-root>/.cursor/rules/` and `ide-files/*.prompt.md` into `<deploy-root>/.cursor/commands/`.

| File | Deploy target |
| --- | --- |
| `ide-files/abd-lo-fi.mdc` | `.cursor/rules/` (Cursor always-on rule) |
| `ide-files/abd-lo-fi.instructions.md` | `.github/` when `-ide vscode` is used (same body as `.mdc` after frontmatter) |
| `ide-files/abd-lo-fi.prompt.md` | `.cursor/commands/`; also `.github/prompts/` under VS Code |

---

<!-- execute_rules:bundle_rules:begin -->
<!-- Rule prose is generated from rules/*.md — edit rules, then run:
     python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/user-experience-design/abd-lo-fi
-->
<!-- execute_rules:bundle_rules:end -->
