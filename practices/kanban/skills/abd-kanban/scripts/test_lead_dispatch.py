#!/usr/bin/env python3
"""Tests for KanbanLead.dispatch_claims() and release_stale_reserved()."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from delivery_model import SkillProgress, Ticket, load_board, save_board, write_heartbeat  # noqa: E402
from kanban_lead import KanbanLead  # noqa: E402


def _write_fixture(ws: Path) -> None:
    wr = ws / "docs" / "planning" / "delivery-war-room"
    wr.mkdir(parents=True)
    (wr / "kanban.json").write_text(
        json.dumps({
            "definitions": {
                "test": {
                    "team": {"product-owner": 2},
                    "stages": [{
                        "name": "exploration",
                        "scope": "increment",
                        "stage_work_required": [
                            {"skill": "abd-domain-language", "role": "business-expert"},
                            {"skill": "abd-acceptance-criteria", "role": "product-owner"},
                        ],
                    }],
                },
            },
        }),
        encoding="utf-8",
    )
    board = {
        "schema": "abd-delivery-kanban/v2",
        "stage_configuration": "test",
        "team": {"product-owner": 2},
        "backlog": [],
        "active": [{
            "ticket_id": "inc-1",
            "lineage": ["P", "Inc 1"],
            "scope_level": "increment",
            "stage": "exploration",
            "priority": 1,
            "skill_progress": {
                "abd-domain-language": {
                    "execution_status": "done",
                    "agent": "business-expert",
                    "review_status": "done",
                    "reviewer": "business-expert",
                },
            },
        }],
        "done": [],
        "archived": [],
    }
    save_board(ws, board)


class TestDispatchClaims(unittest.TestCase):
    def test_does_not_reserve_without_working_executor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            _write_fixture(ws)
            lead = KanbanLead(ws)
            actions = lead.dispatch_claims(("product-owner",))
            self.assertEqual(actions, [])
            board = load_board(ws)
            sp = board["active"][0]["skill_progress"].get("abd-acceptance-criteria")
            self.assertIsNone(sp)


class TestReleaseStaleReserved(unittest.TestCase):
    def test_release_stale_reserved_claim(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            _write_fixture(ws)
            wr = ws / "docs" / "planning" / "delivery-war-room"
            board = load_board(ws)
            ticket = Ticket.from_dict(board["active"][0])
            ticket.skill_progress["abd-acceptance-criteria"] = SkillProgress(
                execution_status="in_progress",
                agent="product-owner",
                start="2026-01-01T00:00:00+00:00",
            )
            board["active"][0] = ticket.to_dict()
            save_board(ws, board)
            write_heartbeat(wr, "product-owner", "reserved", "orphan claim", 1)

            lead = KanbanLead(ws)
            actions = lead.release_stale_reserved(("product-owner",), stale_seconds=0)
            self.assertTrue(actions)
            board = load_board(ws)
            self.assertNotIn(
                "abd-acceptance-criteria",
                board["active"][0].get("skill_progress", {}),
            )


class TestReleaseReadyOrphan(unittest.TestCase):
    def test_release_in_progress_when_executor_is_ready(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            _write_fixture(ws)
            wr = ws / "docs" / "planning" / "delivery-war-room"
            board = load_board(ws)
            ticket = Ticket.from_dict(board["active"][0])
            ticket.skill_progress["abd-ux-mockup"] = SkillProgress(
                execution_status="in_progress",
                agent="ux-designer",
                start="2026-01-01T00:00:00+00:00",
            )
            board["active"][0] = ticket.to_dict()
            save_board(ws, board)
            write_heartbeat(wr, "ux-designer", "ready", "no_eligible_skill_on_active_tickets", 1)

            lead = KanbanLead(ws)
            actions = lead.release_orphan_claims(("ux-designer",), stale_seconds=120)
            self.assertTrue(any(a.startswith("release_orphan:") for a in actions))
            board = load_board(ws)
            self.assertNotIn("abd-ux-mockup", board["active"][0].get("skill_progress", {}))

    def test_release_ready_orphan_even_when_stale_working_heartbeat(self) -> None:
        """Ready heartbeat wins over stale working — must not skip orphan release."""
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            _write_fixture(ws)
            wr = ws / "docs" / "planning" / "delivery-war-room"
            board = load_board(ws)
            ticket = Ticket.from_dict(board["active"][0])
            ticket.skill_progress["abd-ux-mockup"] = SkillProgress(
                execution_status="in_progress",
                agent="ux-designer",
                start="2026-01-01T00:00:00+00:00",
            )
            board["active"][0] = ticket.to_dict()
            save_board(ws, board)
            write_heartbeat(wr, "ux-designer", "working", "stale in_progress abd-ux-mockup", 1)
            write_heartbeat(wr, "ux-designer", "ready", "no_eligible_skill_on_active_tickets", 1)

            lead = KanbanLead(ws)
            actions = lead.release_orphan_claims(("ux-designer",), stale_seconds=120)
            self.assertTrue(any(a.startswith("release_orphan:") for a in actions))
            board = load_board(ws)
            self.assertNotIn("abd-ux-mockup", board["active"][0].get("skill_progress", {}))


if __name__ == "__main__":
    unittest.main()
