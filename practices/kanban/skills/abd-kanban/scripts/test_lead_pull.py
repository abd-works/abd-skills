#!/usr/bin/env python3
"""Tests for KanbanLead.pull_backlog() — partition and increment pull."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from delivery_model import SkillProgress, Ticket, load_board, save_board  # noqa: E402
from kanban_lead import KanbanLead  # noqa: E402


class TestPullBacklogToActive(unittest.TestCase):
    def test_generic_pull_fills_each_stage_independently(self) -> None:
        """Both discovery (partition) and exploration (increment) pull when capacity exists."""
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            wr = ws / "docs" / "planning" / "delivery-war-room"
            wr.mkdir(parents=True)
            (wr / "kanban.json").write_text(
                json.dumps({
                    "definitions": {
                        "test": {
                            "stages": [
                                {"name": "discovery", "scope": "partition", "stage_work_required": []},
                                {"name": "exploration", "scope": "increment", "stage_work_required": []},
                            ],
                        },
                    },
                }),
                encoding="utf-8",
            )
            board = {
                "schema": "abd-delivery-kanban/v2",
                "stage_configuration": "test",
                "backlog": [
                    Ticket(
                        ticket_id="1-inc-a",
                        lineage=["P", "Inc A"],
                        scope_level="increment",
                        stage="exploration",
                        priority=1,
                    ).to_dict(),
                    Ticket(
                        ticket_id="3-partition-b",
                        lineage=["P", "Partition B"],
                        scope_level="partition",
                        stage="discovery",
                        priority=3,
                    ).to_dict(),
                ],
                "active": [],
                "done": [],
                "archived": [],
            }
            save_board(ws, board)

            lead = KanbanLead(ws)
            actions = lead.pull_backlog()

            self.assertTrue(len(actions) > 0)
            after = load_board(ws)
            active_ids = {t["ticket_id"] for t in after["active"]}
            self.assertIn("3-partition-b", active_ids)
            self.assertIn("1-inc-a", active_ids)
            self.assertEqual(len(after["backlog"]), 0)


class TestRollingPull(unittest.TestCase):
    def test_pulls_when_first_skill_done_on_active_increments(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            wr = ws / "docs" / "planning" / "delivery-war-room"
            wr.mkdir(parents=True)
            (wr / "kanban.json").write_text(
                json.dumps({
                    "definitions": {
                        "test": {
                            "team": {"business-expert": 3},
                            "stages": [{
                                "name": "exploration",
                                "scope": "increment",
                                "stage_work_required": [
                                    {"skill": "abd-ubiquitous-language", "role": "business-expert"},
                                ],
                            }],
                        },
                    },
                }),
                encoding="utf-8",
            )
            ul_done = SkillProgress(
                execution_status="done",
                agent="business-expert",
                review_status="done",
                reviewer="business-expert",
            )
            board = {
                "schema": "abd-delivery-kanban/v2",
                "stage_configuration": "test",
                "team": {"business-expert": 3},
                "backlog": [
                    Ticket(
                        ticket_id="1-inc-next",
                        lineage=["P", "Next"],
                        scope_level="increment",
                        stage="exploration",
                        priority=4,
                    ).to_dict(),
                ],
                "active": [
                    Ticket(
                        ticket_id="1-inc-done",
                        lineage=["P", "Done"],
                        scope_level="increment",
                        stage="exploration",
                        priority=1,
                        skill_progress={"abd-ubiquitous-language": ul_done},
                    ).to_dict(),
                ],
                "done": [],
                "archived": [],
            }
            save_board(ws, board)

            lead = KanbanLead(ws)
            actions = lead.pull_backlog()

            pulled_ids = [a.split(":")[1] for a in actions if a.startswith("pulled:")]
            self.assertIn("1-inc-next", pulled_ids)
            after = load_board(ws)
            active_ids = [t["ticket_id"] for t in after["active"]]
            self.assertIn("1-inc-next", active_ids)


if __name__ == "__main__":
    unittest.main()
