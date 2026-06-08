# abd-secure-code scanner tests

Fixtures and pytest regression for all **three supported languages** (Python, Java, JavaScript).

## Layout

```
test/
  fixtures/
    secure-sample/src/     # clean patterns — scanners must pass (0 violations)
    insecure-sample/src/   # bad_patterns.* — scanners must detect violations
    green-belt/e0523/      # per-challenge snippets (batch wiring / corpus)
  scanner_expectations.json
  test_scanners.py
```

## Run

From repo root or skill root:

```powershell
python -m pytest architecture-centric-engineering/skills/abd-secure-code/test/test_scanners.py -v
```

Or from this folder:

```powershell
cd architecture-centric-engineering/skills/abd-secure-code
python -m pytest test/test_scanners.py -v
```

## What is asserted

| Fixture | Expectation |
| --- | --- |
| **secure-sample** | All 24 `no_*` scanners × 3 languages → exit 0 |
| **insecure-sample** | Scanners listed in `scanner_expectations.json` → exit 1 (violations found) |

Green belt challenge fixtures are validated separately via `scripts/validate_batch_wiring.py` (corpus paths in `secure-code-warrior`).

## Adding coverage

When you add a rule scanner:

1. Add a failing pattern to `fixtures/insecure-sample/src/bad_patterns.{py,js,java}`.
2. Confirm secure sample still passes.
3. Add the scanner stem to `must_violate` for that language in `scanner_expectations.json`.
4. Re-run pytest.
