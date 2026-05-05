"""
Story-map **shape** scanner implementations (verb–noun, outcome language, etc.).

**Generic bases:** :class:`Scanner`, violations, :class:`ScanFilesContext`, and the
**scanner_runner** CLI driver live under ``skills/execute-skill-using-skills-rules/scripts/``.
**Story graph** types (:class:`StoryScanner`, :class:`StoryMap`, …) live in
**story-graph-ops** (``skills/story-graph-ops/scripts/`` — ``story_map``, ``story_scanner``, …).

``run_scanners.py`` sets ``PYTHONPATH`` (story-graph-ops + execute-skill-using-skills-rules scripts).
"""
