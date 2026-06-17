"""
Acceptance-criteria **exploration** scanner implementations migrated from **agile_bots**
(`src/scanners/*` paired with `bots/story_bot/behaviors/exploration/rules/*.json`).

**Generic bases:** :class:`Scanner`, violations, :class:`ScanFilesContext`, and the
**scanner_runner** CLI driver live under ``skills/execute-skill-using-skills-rules/scripts/``.
**Story graph** types (:class:`StoryScanner`, :class:`StoryMap`, …) live in
**story-graph-ops** (``skills/story-graph-ops/scripts/``).

``run_scanners.py`` sets ``PYTHONPATH`` (story-graph-ops + execute-skill-using-skills-rules scripts).
"""
