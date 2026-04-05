"""Tests for scripts/base/workspace_checklists.py."""
from __future__ import annotations

import unittest

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_BASE = ROOT / "scripts" / "base"
if str(SCRIPTS_BASE) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_BASE))

from workspace_checklists import (  # noqa: E402
    extract_action_checklist_lines,
    render_process_checklist,
)


class TestExtractActionChecklist(unittest.TestCase):
    def test_section_preferred(self) -> None:
        md = """# X

## Action Checklist

- [ ] one
- [ ] two

## Output

nope
"""
        self.assertEqual(
            extract_action_checklist_lines(md),
            ["- [ ] one", "- [ ] two"],
        )

    def test_fallback_all_tasks(self) -> None:
        md = """# No section

- [ ] a
- [x] b
"""
        self.assertEqual(
            extract_action_checklist_lines(md),
            ["- [ ] a", "- [x] b"],
        )


class TestRenderProcess(unittest.TestCase):
    def test_headings(self) -> None:
        text = render_process_checklist(
            "my-skill",
            ("workspace-and-config", "author"),
            {"workspace-and-config": "Workspace"},
        )
        self.assertIn("- [ ] **workspace-and-config** — Workspace", text)
        self.assertIn("- [ ] **author** — Author", text)


if __name__ == "__main__":
    unittest.main()
