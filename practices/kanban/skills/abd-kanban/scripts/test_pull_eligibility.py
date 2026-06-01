#!/usr/bin/env python3
"""Tests for pull eligibility and mechanism registry."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from delivery_model import (  # noqa: E402
    KanbanBoard,
    SkillDef,
    SkillProgress,
    StageDef,
    Ticket,
)
from mechanism_registry import load_registry, register_mechanisms  # noqa: E402


class MechanismRegistryTests(unittest.TestCase):
    def test_register_and_load(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            (ws / "docs" / "planning" / "delivery-war-room").mkdir(parents=True)
            register_mechanisms(ws, "1-inc-a", "abd-architecture-template", ["Security"])
            reg = load_registry(ws)
            self.assertIn("Security", reg)
            self.assertEqual(reg["Security"]["ticket_id"], "1-inc-a")


class PullEligibilityTests(unittest.TestCase):
    def test_optional_skill_eligible(self) -> None:
        kb = KanbanBoard(
            name="t",
            stages=[
                StageDef(
                    name="exploration",
                    scope="increment",
                    stage_work_required=[
                        SkillDef(skill="abd-ubiquitous-language", role="business-expert"),
                        SkillDef(skill="abd-acceptance-criteria", role="product-owner"),
                        SkillDef(skill="abd-ux-mockup", role="ux-designer", optional=True),
                    ],
                ),
            ],
        )
        ticket = Ticket(
            ticket_id="1-inc",
            lineage=["P"],
            scope_level="increment",
            stage="exploration",
            skill_progress={
                "abd-ubiquitous-language": SkillProgress(
                    execution_status="done", agent="business-expert", review_status="done"
                ),
                "abd-acceptance-criteria": SkillProgress(
                    execution_status="done", agent="product-owner", review_status="done"
                ),
            },
        )
        match = kb.find_next_eligible([ticket], "ux-designer")
        self.assertIsNotNone(match)
        assert match is not None
        self.assertEqual(match[1], "abd-ux-mockup")

    def test_list_eligible_pulls_downstream_first(self) -> None:
        kb = KanbanBoard(
            name="t",
            stages=[
                StageDef(
                    name="discovery",
                    scope="partition",
                    stage_work_required=[
                        SkillDef(skill="abd-story-mapping", role="product-owner"),
                    ],
                ),
                StageDef(
                    name="exploration",
                    scope="increment",
                    stage_work_required=[
                        SkillDef(skill="abd-acceptance-criteria", role="product-owner"),
                    ],
                ),
            ],
        )
        tickets = [
            Ticket(ticket_id="disc-1", lineage=[], scope_level="partition", stage="discovery"),
            Ticket(ticket_id="exp-1", lineage=[], scope_level="increment", stage="exploration"),
        ]
        pulls = kb.list_eligible_pulls(tickets, "product-owner")
        self.assertEqual(pulls[0][0], "exp-1")


if __name__ == "__main__":
    unittest.main()
