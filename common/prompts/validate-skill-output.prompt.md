I just generated output for a skill. Now validate it.

1. Re-read every file in **`rules/`** for the active skill. For each rule emit:
   `Rule: <name>  ->  PASS` or `Rule: <name>  ->  FAIL  <offending line or reason>`
   No rule may be silently skipped. Fix every FAIL.

2. Run the scanners:
   `python common/scripts/run_scanners.py --skill-root <skill> --workspace <abs-path>`
   Fix all violations and re-run until clean.

See **`common/skill-workflow.md`** § Validate output for the full process.
