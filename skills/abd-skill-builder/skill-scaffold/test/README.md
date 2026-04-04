# test/

Automated verification for this skill.

## Structure

```
test/
├── fixture/          — small self-contained skill trees used as test inputs
│   └── <fixture-name>/
│       ├── SKILL.md
│       ├── skill-config.json
│       ├── conf/
│       ├── content/parts/
│       └── rules/
└── test_*.py         — test suites (pytest)
```

## Running tests

```
pytest test/
```

## Adding a fixture

Copy `skill-scaffold/` (this folder's sibling), strip it down to the minimal
content needed for your test, and place it under `test/fixture/<fixture-name>/`.
