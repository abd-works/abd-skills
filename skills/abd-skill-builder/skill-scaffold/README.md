# skill-scaffold

A complete, annotated template for a new `abd-skill-builder` skill.

Every folder and file here corresponds to a real folder or file in a built skill. Each file is pre-populated with the minimum viable content and inline comments explaining what to fill in.

## How to use

1. Copy this entire folder to your new skill location.
2. Rename `{{skill_name}}` placeholders throughout.
3. Work through `docs/skill-plan.md` top to bottom — the checklist tracks your progress.
4. Run `python scripts/base/build.py` to assemble `AGENTS.md` from `content/parts/`.
5. Run `python scripts/base/run_scanners.py` to verify all rules pass.

## Folder map

```
skill-scaffold/
├── conf/               Run-time settings — active workspace path and scanner bindings
├── content/
│   ├── parts/
│   │   ├── phases/     One file per phase (+ code-phase-template.md for script-driven phases)
│   │   ├── library/    Cross-cutting norms injected into every phase
│   │   └── process.md  Phase pipeline definition
│   └── built/          (static mode) pre-assembled AGENTS.md slices
├── docs/               skill-plan.md lives here
├── rules/              One .md per rule (bindings configured in conf/abd-config.json)
├── scripts/
│   ├── base/           Universal scripts from abd-skill-builder (do not modify)
│   │   ├── skill_root.py           Shared utility — resolves skill root path
│   │   ├── build.py                Assemble AGENTS.md from content/parts/
│   │   ├── generate.py             Generate a phase bundle for AI injection
│   │   ├── markers.py              Phase-scope and section marker utilities
│   │   ├── run_scanners.py         Run all scanners in conf/abd-config.json
│   │   ├── set_workspace.py        Read/write active_skill_workspace
│   │   └── list_rules_by_order.py  List rules sorted by order
│   ├── {{skill_name}}/     Skill-specific scripts (add yours here)
│   └── scanners/           One scanner per rule — scanner_{{rule_id}}.py
├── templates/          Output shape templates for AI-generated artifacts
├── test/               Fixtures and test suites
├── SKILL.md            Agent entry point
└── skill-config.json   Wires parts, rules, phases, and operator together
```
