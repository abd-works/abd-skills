# abd-architecture-reference

Read `skills/architecture-centric-delivery/abd-architecture-reference/SKILL.md` and follow the Agent Instructions to generate runnable code files that implement one architecture mechanism.

Choose the mode:
- **Project mode** — a real `architecture-reference.md` is in scope; generate every file listed in its File Structure block, implementing the walkthrough example.
- **Hello-world mode** — no project context is available; use the built-in Simple Calculator scenario (three-layer Python CLI, error-handling mechanism) and generate `calculator.py`, `cli.py`, `tests/test_calculator.py`, and `tests/test_cli.py`.

Every generated file must be syntactically correct and immediately runnable. The domain layer raises typed exceptions; the presentation layer has exactly one `try/except` per domain exception type. Running `pytest` on the test files must produce a passing suite.
