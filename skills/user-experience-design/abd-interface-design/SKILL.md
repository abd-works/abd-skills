---
name: abd-interface-design
description: >-
  Translate the approved hi-fi mockup for a screen into production-grade,
  functional, accessible interface code in the chosen framework — without
  changing the domain labels, acceptance criteria, or visual decisions.
---
# abd-interface-design

## Purpose

Hi-fi mockups settle look and feel. The interface stage is where they become real code — and where most teams quietly stop honouring the upstream artifacts because "we're shipping now". This skill keeps that integrity: the implementation renders the same regions, the same affordances, the same labels, the same acceptance criteria, and the same visual decisions as the approved hi-fi, in production-grade code that an end user can actually use. It treats acceptance criteria as the testable surface (every clause is a working behaviour with a check), treats the ubiquitous language as the public vocabulary (labels and copy stay verbatim from the UL and AC), and treats accessibility and performance as constraints that are met, not aspirations that are mentioned. The result is one screen implemented in the chosen framework, traceable end-to-end from story to running interface.

---

## When to use this skill

Load this skill when **any** of the following apply:

- The hi-fi mockup for a screen is **approved** and you want to **implement** it in code.
- A current implementation has **drifted** from the hi-fi or the AC (mismatched labels, missing affordances, generic visual treatment, broken accessibility) and you want to bring it back.
- You are starting a screen from an approved hi-fi and need a **traceable** path from acceptance criteria → behaviours → tests → production code.
- A reviewer needs to verify that every AC is implemented and every UL label is used verbatim in the running UI.

---

## What is an interface implementation

A screen implementation under this skill is:

- **Functional**: every affordance does what its AC say it should do. Errors render, validations run, transitions to other screens fire when their triggers fire.
- **Production-grade**: real code in the chosen framework (React, Vue, WPF, etc.), structured the way the host project structures other features, with the project's lint, format, and test conventions.
- **Faithful to upstream**: the regions, affordances, labels, AC, and visual decisions match the approved lo-fi and hi-fi. No new vocabulary, no new affordances, no new visual styles.
- **Accessible**: meets the host project's accessibility floor (typically WCAG 2.2 AA for web). Keyboard reachable, focus visible, labels associated with inputs, errors announced, colour-independent state cues.
- **Measurable**: the behaviours described by AC are covered by tests, and any performance constraints declared by the host project (frame budget, response time, payload size) are met.

It is not a redesign and it is not a refactor of unrelated code.

---

## Core concepts

### Carry-over from upstream

The initial IA, lo-fi, and hi-fi are inputs. Their regions, affordances, labels, acceptance criteria, typography roles, colour roles, density, and spacing scale are settled. The implementation maps each of those into the chosen framework's primitives — it does not redecide them.

### Production-grade and functional

The code is not a "demo" or "shell". Every affordance on the screen does what its AC say it does. State management uses the project's existing patterns. Side effects are real or properly mocked at boundaries the project already has. The code passes the project's lint, format, and type-check gates without being silenced.

### Memorable differentiation

The committed aesthetic direction from the hi-fi survives into the running code: the typographic roles are real CSS variables, design tokens, or theme values; the colour roles are real values, not generic defaults; the density and spacing scale are real spacing tokens. The running screen looks like the mockup, not like an untouched component library.

### Accessibility in implementation

Implementation-level accessibility is concrete: each input has a programmatic label (`<label for>` or framework equivalent), focus order matches reading order, focus styles are visible (not removed by `outline: none` with no replacement), errors are programmatically associated with their inputs (`aria-describedby`), state is announced when it changes (`aria-live` where appropriate), and the entire screen is keyboard reachable.

### Performance constraints

If the host project declares performance constraints (initial paint, time-to-interactive, frame budget for animations, bundle size budget), the implementation meets them. If it does not declare them, the implementation does not regress whatever the project's current baseline is.

### Traceability — AC to test to running screen

Each acceptance criterion is implemented as a working behaviour and is covered by a test that asserts that behaviour, using the project's existing test framework. The test names reference the criterion (story title and clause number) so a reviewer can map each test back to the source AC.

### Rules

`rules/*.md` validate the output (running screen + committed code). Build steps live in **Build**.

---

## The shape of a good interface implementation

```
src/screens/game-directory-prompt/
  GameDirectoryPrompt.tsx           # the screen component
  GameDirectoryPrompt.styles.ts     # styles using project tokens
  validatePath.ts                   # logic for AC clauses
  __tests__/GameDirectoryPrompt.test.tsx
                                    # one test per AC clause, named:
                                    #   "Validate COH Game Directory — AC 1"
                                    #   "Prompt for Game Directory if Invalid — AC 3"
```

The running screen renders the regions and affordances from the hi-fi, uses the declared typography and colour roles via project tokens, satisfies every AC clause, and passes the project's lint / format / type-check / accessibility / performance gates.

---

## Build

**Goal:** Implement one screen in the chosen framework, mapping every region, affordance, label, AC clause, and visual decision from upstream into running code and tests.

1. **Resolve inputs.** Confirm: path to the approved hi-fi (`docs/ux/hi-fi.tldr` and/or `.svg`), path to the lo-fi (for region reference), path to the AC file, the screen name, the target framework (React, Vue, WPF, etc.), and the host project root (where `package.json` / `*.csproj` / equivalent lives). Confirm the host project's lint, format, test, accessibility, and performance gates by reading its config files.

2. **Discover host conventions.** Inspect how the host project organises features (folder layout, component shape, state management pattern, styling approach, token system, test conventions). The new screen follows those conventions — it is not an outlier.

3. **Carry over upstream decisions.** Pull labels, copy, AC, regions, affordance set, typography roles, colour roles, density, and spacing scale from the lo-fi and hi-fi exactly. Resolve them to the host's tokens or theme values; do not introduce new vocabulary or new style decisions.

4. **Author or update `docs/ux/interface-design.md` first.** Copy `templates/interface-design.md` into the engagement's `docs/ux/` folder (or open the existing one) and fill in: screen name, source paths, framework, host project root, discovered host conventions (folder layout, state management, styling, tokens, test framework, gates), carried-over decisions, the AC → behaviour → test mapping (one row per AC clause), the accessibility checklist with planned statuses, and the performance budget table. This markdown is the structured spec the implementation is written against; code is never written without it.

5. **Implement the screen.** Build the component(s) using the host framework's primitives. Each region is a container; each affordance is an interactive primitive with the verbatim label. Inputs are labelled programmatically. Focus order matches reading order. Errors are programmatically associated. State cues use text or icon in addition to colour.

6. **Implement AC behaviours.** Every AC clause becomes a working behaviour. Validation runs as the AC describe; error messages are the verbatim AC copy; transitions to other screens fire when their triggers fire. No clause is silently deferred.

7. **Write tests.** One test per AC clause, named to reference the story and clause number (matching the `Test name` column in `docs/ux/interface-design.md`). Tests use the host project's existing test framework. Tests assert observable behaviour, not implementation detail.

8. **Pass the host project's gates.** Lint, format, type-check, accessibility checks (axe or equivalent), and performance budget checks all pass. If a gate is silenced or skipped, write a note in `corrections-log.md` explaining why and bring it back as soon as the cause is fixed.

9. **Verify against the hi-fi visually.** Open the running screen beside the hi-fi `.svg`. Typography, colour, spacing, and hierarchy match. Differences are intentional (browser/native rendering of the same role) or are fixed.

10. **Sync implementation changes back into `interface-design.md`.** Update the AC → behaviour → test mapping with current statuses (pending / passing / failing), the accessibility checklist with current results, and the performance table with current measurements. Append a row to the change log with date, direction (`code → md`), and a one-line summary.

11. **Apply the rules, then review like a peer.** Walk every file under `rules/` against the running screen, the committed code, and the markdown spec. Fix every violation before declaring success.

12. **Keep the bundled rules block honest.** Whenever you change a file under `rules/`, re-run the bundler so the rule prose inlined at the end of this `SKILL.md` matches what is on disk:

```bash
python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/user-experience-design/abd-interface-design
```

- **Outputs:** `docs/ux/interface-design.md` (structured spec), plus working code on disk in the host project (screen component, supporting modules, tests), plus updates to the project's screen index/router if relevant. The spec and the code are kept in sync.
- **Per format:** `.md` is the structured spec — created first, updated after code changes. Code passes the project's gates without silenced warnings or skipped tests.
- **While writing:** labels and AC are verbatim, visual decisions match the hi-fi roles, every AC clause has a test, accessibility constraints hold, performance constraints hold.

---

## Validate

**Goal:** Read the committed code and the running screen as reviewers.

- **Who is checking:** the product owner runs the screen and walks every AC clause; a developer reviews the diff against the host project's conventions; an accessibility reviewer keyboard-navigates the screen and runs axe; a designer compares the running screen to the hi-fi side by side.
- **Cross-artifact parity:** the implementation matches the hi-fi visually and matches the lo-fi structurally. The test names trace to AC clauses by name and number.

Walk the implementation and confirm:

- Every region, affordance, and label from the hi-fi appears in the running screen with the same wording.
- Every acceptance criterion is implemented and has at least one test named for its story and clause number.
- The host project's lint, format, type-check, accessibility, and performance gates pass without silencing.
- Every input has a programmatic label; focus order matches reading order; focus is visible; state cues are not colour-only.
- Typography roles, colour roles, and the spacing scale map to host project tokens or theme values, used consistently.

---

## Deploy

This skill ships IDE-deployable files under `ide-files/`. Deploy them from the repo root using the standard repo-level script:

```powershell
cd C:\dev\agilebydesign-skills
.\scripts\deploy-skills.ps1 -ide cursor -Force
```

| File | Deploy target |
| --- | --- |
| `ide-files/abd-interface-design.mdc` | `.cursor/rules/` (Cursor always-on rule) |
| `ide-files/abd-interface-design.instructions.md` | `.github/` when `-ide vscode` is used (same body as `.mdc` after frontmatter) |
| `ide-files/abd-interface-design.prompt.md` | `.cursor/commands/`; also `.github/prompts/` under VS Code |

---

<!-- execute_rules:bundle_rules:begin -->
<!-- Rule prose is generated from rules/*.md — edit rules, then run:
     python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/user-experience-design/abd-interface-design
-->
<!-- execute_rules:bundle_rules:end -->
