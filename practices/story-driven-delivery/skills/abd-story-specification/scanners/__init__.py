"""
**Specification-by-example** scanner implementations (scenario emphasis, …).

**Generic bases:** :class:`Scanner`, violations, :class:`ScanFilesContext`, and the
**scanner_runner** CLI driver live under ``skills/execute-skill-using-skills-rules/scripts/``.
**Story graph** types (:class:`StoryScanner`, :class:`StoryMap`, …) live in
**story-graph-ops** (``skills/supporting/story-graph-ops/scripts/``).

``run_scanners.py`` sets ``PYTHONPATH`` (story-graph-ops + execute-skill-using-skills-rules scripts).
"""
