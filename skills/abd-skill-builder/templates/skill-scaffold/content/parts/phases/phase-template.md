# Phase — {{phase_name}}

{{phase_description}}

## How to use this phase doc

- **Do not check off steps here.** This document is normative — it defines the steps, it does not track them.
- **Live checklist path:** `<active_skill_workspace>/{{skill_name}}/progress/{{phase_slug}}-checklist.md`. On first run of `python scripts/base/generate.py --phase {{phase_slug}}`, that file is created from **## Action Checklist** below if it does not exist yet.
- **Resume point:** the first unchecked box in your **workspace** checklist is where you continue after any interruption.
- **Do not modify this file during a run** to record progress. If steps are wrong, update the phase doc and commit — do not edit it mid-session to match what you did.

## Inputs

- {{input_1 — e.g. workspace files, prior phase output}}
- {{input_2}}

## Action Checklist

<!-- Canonical action list. Copied to `<active_skill_workspace>/{{skill_name}}/progress/{{phase_slug}}-checklist.md` when missing (see generate.py). Tick there, not here. -->

- [ ] {{action_1 — concrete action}}
- [ ] {{action_2}}
- [ ] {{action_3}}
- [ ] Verify output before moving to the next phase (see Verification below)

## Output

<!-- What artifact or state change this phase leaves behind. Must be verified before moving on. -->

{{output_description}}

## Verification

<!-- Checks to confirm the output is correct before moving on. -->
<!-- Focus on observable conditions: does the file exist, does it contain expected content, are counts right, etc. -->
<!-- Rules and scanners are assembled separately — do not reference them here. -->

- {{verification_1 — e.g. open the output file and confirm it contains the expected sections}}
- {{verification_2 — e.g. confirm expected number of entries were produced}}
- {{verification_3 — e.g. no placeholder values remain in the output}}
