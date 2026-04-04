# Phase — {{code_phase_name}}

{{code_phase_description}}

## How to use this phase doc

- **Do not check off steps here.** This document is normative — it defines the steps, it does not track them.
- **Create a checklist copy in the workspace** (`<workspace>/{{skill_name}}/{{code_phase_slug}}_checklist.md`) and tick boxes there.
- **Resume point:** the first unchecked box in your workspace checklist is where you continue after any interruption.
- **Do not modify this file during a run.** If the script behaviour changes, update the phase doc and commit.

## Script

```
python scripts/{{code_phase_script}} {{args}}
```

| Argument | Required | Description |
|----------|----------|-------------|
| `{{arg_1}}` | {{yes/no}} | {{what it does}} |

## What it does

{{what the script reads, what it writes, what exit 0 means, what non-zero means}}

## Action Checklist

<!-- Canonical action list. Copy to `<workspace>/{{skill_name}}/{{code_phase_slug}}_checklist.md` before starting; tick there, not here. -->

- [ ] Confirm all inputs are present at the expected paths
- [ ] Run the script: `python scripts/{{code_phase_script}} {{args}}`
- [ ] Check exit code is 0
- [ ] Verify output (see Verification below)

## Output

<!-- What artifact or state change exit 0 leaves behind. Must be verified before moving on. -->

{{output_description}}

## Verification

<!-- Checks to confirm the script succeeded beyond exit code. -->
<!-- Focus on observable conditions: does the output file exist, does it contain expected content, are counts right, etc. -->
<!-- Rules and scanners are assembled separately — do not reference them here. -->

- {{verification_1 — e.g. open the output file and confirm it contains the expected content}}
- {{verification_2 — e.g. confirm expected number of entries were produced}}
- {{verification_3 — e.g. no placeholder values remain in the output}}

## Norms

- {{normative rule the script enforces or that the caller must satisfy}}
