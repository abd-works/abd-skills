---
name: abd-hi-fi
description: >-
  Take a lo-fi wireframe and commit it to a single intentional visual direction
  — typography, colour, hierarchy, density, aesthetic — without changing the
  domain labels, acceptance criteria, or affordance set. Save on the abd-canvas
  whiteboard.
---
# abd-hi-fi

## Purpose

Lo-fi wireframes settle structure and language. High-fidelity mockups settle look and feel — and they are the place where most lo-fi-correct designs quietly fall apart, because somebody starts making aesthetic choices "as they go" instead of committing to a direction. This skill packages the hi-fi pass as one deliberate move: pick one aesthetic direction for the screen (or the small group of screens being polished), apply it consistently across typography, colour, hierarchy, density, and component treatment, and leave the domain labels, acceptance criteria, and affordance set exactly as the lo-fi established them. The result is a mockup that is honest to the stories *and* visually intentional, drawn on `abd-canvas` and saved beside the lo-fi for review.

---

## When to use this skill

Load this skill when **any** of the following apply:

- The lo-fi for a screen is **approved** and you want a **visual treatment** of the same layout before any code is written.
- Stakeholders are debating look-and-feel (typography, colour, density, brand voice) and you want a **single canvas** that shows one committed direction.
- A previous hi-fi pass produced "AI slop" — generic gradients, default shadcn, faceless components — and you want to **redo** it with a clear conceptual direction.
- You need a visual artifact for design reviews, stakeholder approval, or vendor handoff that still honours the stories and the ubiquitous language.

---

## What is a hi-fi mockup

A **hi-fi mockup** is the lo-fi wireframe for the same screen, rendered with a committed visual direction:

- **Same regions, same affordances, same labels, same AC** as the lo-fi (those are settled).
- **One aesthetic direction** — minimal, editorial, brutalist, retro-futuristic, organic, luxury, playful, industrial, or another — chosen deliberately and named on the canvas.
- **Typography** with declared roles (display, body, label) and explicit choices for family, weight, and size relationships.
- **Colour** with declared roles (surface, ink, accent, error, success) and explicit values that meet the accessibility floor for hi-fi.
- **Hierarchy** that makes the primary action unmistakable, secondary actions calmer, and feedback unambiguous.

It does not implement code, does not commit to a framework, and does not add new behaviour that the lo-fi did not justify. The hi-fi is a visual decision, not a scope decision.

---

## Core concepts

### Committed aesthetic direction

The hi-fi pass picks **one** direction and executes it with precision. "Bold maximalism" and "refined minimalism" are both valid; "vaguely modern" is not. The chosen direction is named explicitly on the canvas (a short note: `Direction: editorial / serif headlines, generous white space, neutral palette, single accent`) so reviewers can judge the mockup against an intent, not a vibe.

### Visual hierarchy

The most important affordance on the screen — the one the acceptance criteria describe as the primary outcome — is visually unmistakable: largest active element, highest contrast, most space around it. Secondary affordances are calmer. Information regions read in the order the user needs them, not in the order they happened to be drawn.

### Typography

The hi-fi names typographic **roles** (display, heading, body, label, microcopy) and assigns explicit decisions to each (family, weight, size, line-height, tracking). Roles are reused; no one-off type styles. Domain terms shown as labels keep their UL casing — typography decisions never overwrite the ubiquitous language.

### Colour

Colour decisions are role-driven: surface (background), ink (text), accent (primary action), warning, error, success. Each role has at least one explicit value. Colour is never the only signal for meaning — error states carry both colour and text; status indicators carry both colour and label. This keeps `ucd-accessibility-hi-fi` satisfied while allowing colour to do real work.

### Density and rhythm

The mockup commits to a density (compact, comfortable, spacious) and a baseline rhythm (a small set of spacing values used everywhere). Mixing densities or improvising spacing values per region is the visual equivalent of inventing domain vocabulary in lo-fi — and is rejected for the same reason.

### Carry-over from lo-fi

The initial IA, the region layout, the affordance set, the acceptance criteria, and the domain terms are **inputs**, not subjects of redesign. If a hi-fi pass surfaces a real gap in the lo-fi or the AC, stop and fix it in the right skill (`abd-lo-fi`, `abd-information-architecture`, or the AC source) — do not paper over it in visual design.

### Dumping ground for deferred UX concepts

Concepts from the broader UX practice that did not belong in `abd-information-architecture` or `abd-lo-fi` land here when they touch visual fidelity — for example, brand consistency, visual storytelling, expressive empty states, marketing-grade polish. Concepts that belong at implementation time (focus rings, ARIA roles, performance budgets) defer to `abd-interface-design`.

### Rules

`rules/*.md` validate the output (the drawn canvas and the saved `hi-fi.tldr` / `hi-fi.svg`). Build steps live in **Build**.

---

## The shape of a good hi-fi mockup

```
SCREEN: game directory prompt

Direction: editorial / serif headlines, generous white space, neutral palette,
           single warm accent

Typography roles:
  display   — serif, 32px / 40px line, weight 600
  body      — sans, 16px / 24px line, weight 400
  label     — sans, 14px / 20px line, weight 500, +0.2 tracking
  microcopy — sans, 13px / 18px line, weight 400

Colour roles:
  surface   — #FAFAF7
  ink       — #1A1A1A
  ink-muted — #6B6B6B
  accent    — #B85C38
  error     — #B23A48 (with text label, never colour alone)

LAYOUT (same regions and affordances as lo-fi)
  prompt panel — display heading, body explanatory text
  path input area — labelled input + Browse... (secondary button)
  error message area — accent-error background tint + verbatim AC error copy
  continue control area — Continue (accent button, largest active element)

ACCEPTANCE CRITERIA (verbatim, unchanged from lo-fi)
  ...
```

The hi-fi canvas reads like a finished screen for one chosen direction. Affordances, regions, labels, and AC come directly from the lo-fi; the hi-fi adds the visual decision layer on top.

---

## Build

**Goal:** Read the approved lo-fi for the screen, commit to one aesthetic direction, render the same layout with that direction's typography, colour, hierarchy, and density, and save as `hi-fi.tldr` and `hi-fi.svg` in the engagement's `docs/ux/` folder.

1. **Resolve inputs.** Confirm: a path to the approved lo-fi (`docs/ux/lo-fi.tldr` or `.svg`), the screen name (must match the lo-fi), an optional design-system tokens file or brand guide, and the chosen aesthetic direction (or a request to propose one). If the lo-fi is not yet approved, stop and run `abd-lo-fi` first.

2. **Read the lo-fi carry-over.** Pull the region layout, affordance set, labels, and AC from the lo-fi exactly. They are inputs, not subjects of redesign. If something is missing or broken in the lo-fi, fix it there and rerun this skill.

3. **Commit to one aesthetic direction.** Pick one direction and write it on the canvas as a short note (`Direction: <name>, <three or four key adjectives>`). If the user asks for options, offer two or three named directions with one-line rationales and proceed only after one is chosen.

4. **Declare typographic roles.** Write the roles (display, heading, body, label, microcopy) and their explicit decisions (family, weight, size, line-height, tracking) on the canvas. The roles reused are the only roles allowed in the mockup — no one-off type styles.

5. **Declare colour roles.** Write the roles (surface, ink, ink-muted, accent, warning, error, success) and explicit values on the canvas. Every coloured element on the screen maps to one role.

6. **Declare density and rhythm.** Pick a density (compact, comfortable, spacious) and a small spacing scale (e.g. `4, 8, 12, 16, 24, 32, 48`). Use only those values throughout the mockup.

7. **Author or update `docs/ux/hi-fi.md` first.** Copy `templates/hi-fi.md` into the engagement's `docs/ux/` folder (or open the existing one) and fill in: screen name, source paths, description, the committed aesthetic direction (name + adjectives + rationale), the typography role table, the colour role table, density, spacing scale, and the carry-over note pointing at `docs/ux/lo-fi.md`. This markdown is the structured spec the canvas is drawn from; visual decisions are recorded here before they appear on the canvas.

8. **Resolve the abd-canvas location.** Look up `$env:ABD_CANVAS_PATH`; default to `C:\dev\abd-canvas`. If the folder does not exist, stop.

9. **Launch abd-canvas in interactive mode** and open `http://localhost:5173` via the browser MCP. Load `<engagement>/docs/ux/lo-fi.tldr` so the regions and labels are already on the canvas, then drive the agent with the hi-fi instructions read from `docs/ux/hi-fi.md` (the direction, roles, density). The agent applies the visual decisions without changing the regions or labels.

10. **Save canvas outputs.** Click `Save .tldr` to `<engagement>/docs/ux/hi-fi.tldr`, then export the canvas to `<engagement>/docs/ux/hi-fi.svg`.

11. **Sync canvas changes back into `hi-fi.md`.** Read the updated canvas. If the agent introduced a new type style, a new colour, or changed any value that appears in the role tables or the spacing scale, update `docs/ux/hi-fi.md` to match — same role tables, same density, same spacing scale. Append a row to the change log with date, direction (`canvas → md`), and a one-line summary.

12. **Apply the rules, then review like a peer.** Walk every file under `rules/` against the drawn canvas and the markdown spec. Fix every violation before declaring success.

13. **Keep the bundled rules block honest.** Whenever you change a file under `rules/`, re-run the bundler so the rule prose inlined at the end of this `SKILL.md` matches what is on disk:

```bash
python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/user-experience-design/abd-hi-fi
```

- **Outputs:** `docs/ux/hi-fi.md` (structured spec), `docs/ux/hi-fi.tldr` (canvas), `docs/ux/hi-fi.svg` (flat export) — three artifacts kept in sync.
- **Per format:** `.md` is the structured spec — created first, updated after canvas changes. `.tldr` for re-opening on the canvas; `.svg` for documentation and review.
- **While writing:** labels, AC, and affordance set carry over unchanged from the lo-fi. Only the visual decisions are new.

---

## Validate

**Goal:** Read the saved canvas as reviewers.

- **Who is checking:** the product owner verifies the AC are still rendered and still verbatim; a domain expert verifies that no UL term was reworded or recased by typography; a designer verifies that the chosen direction is committed and consistently applied; a UX practitioner verifies that the visual hierarchy makes the primary action unmistakable.
- **Cross-artifact parity:** the `.tldr` and `.svg` are exports of the same canvas.

Walk the canvas and confirm:

- The aesthetic direction is named on the canvas.
- Typography roles and colour roles are declared with explicit values.
- The same regions, affordances, labels, and AC from the lo-fi are present and unchanged in wording.
- The primary affordance is visually unmistakable.
- Colour is never the only signal for meaning.
- The density and spacing scale are consistent across regions.
- `docs/ux/hi-fi.tldr` and `docs/ux/hi-fi.svg` both exist and reflect the current canvas.

---

## Deploy

This skill ships IDE-deployable files under `ide-files/`. Deploy them from the repo root using the standard repo-level script:

```powershell
cd C:\dev\agilebydesign-skills
.\scripts\deploy-skills.ps1 -ide cursor -Force
```

| File | Deploy target |
| --- | --- |
| `ide-files/abd-hi-fi.mdc` | `.cursor/rules/` (Cursor always-on rule) |
| `ide-files/abd-hi-fi.instructions.md` | `.github/` when `-ide vscode` is used (same body as `.mdc` after frontmatter) |
| `ide-files/abd-hi-fi.prompt.md` | `.cursor/commands/`; also `.github/prompts/` under VS Code |

---

<!-- execute_rules:bundle_rules:begin -->
<!-- Rule prose is generated from rules/*.md — edit rules, then run:
     python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/user-experience-design/abd-hi-fi
-->
<!-- execute_rules:bundle_rules:end -->
