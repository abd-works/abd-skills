#!/usr/bin/env python3
"""Tests for KanbanBoard.find_next_eligible() — advancing past done skills on same role."""
from __future__ import annotations

import sys
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


class TestFindNextEligible(unittest.TestCase):
    def test_po_advances_from_done_story_mapping_to_thin_slicing(self) -> None:
        kb = KanbanBoard(
            name="test",
            stages=[
                StageDef(
                    name="discovery",
                    scope="partition",
                    stage_work_required=[
                        SkillDef(skill="abd-domain-terms", role="business-expert"),
                        SkillDef(skill="abd-story-mapping", role="product-owner"),
                        SkillDef(skill="abd-thin-slicing", role="product-owner"),
                    ],
                ),
            ],
        )
        ticket = Ticket(
            ticket_id="2-partition",
            lineage=["P"],
            scope_level="partition",
            stage="discovery",
            priority=1,
            skill_progress={
                "abd-domain-terms": SkillProgress(
                    execution_status="done",
                    agent="business-expert",
                    review_status="done",
                ),
                "abd-story-mapping": SkillProgress(
                    execution_status="done",
                    agent="product-owner",
                    review_status="done",
                ),
            },
        )
        match = kb.find_next_eligible([ticket], "product-owner")
        self.assertIsNotNone(match)
        assert match is not None
        self.assertEqual(match[1], "abd-thin-slicing")

    def test_engineer_arch_reference_after_exploration_priors(self) -> None:
        kb = KanbanBoard(
            name="test",
            stages=[
                StageDef(
                    name="exploration",
                    scope="increment",
                    stage_work_required=[
                        SkillDef(skill="abd-ubiquitous-language", role="business-expert"),
                        SkillDef(skill="abd-acceptance-criteria", role="product-owner"),
                        SkillDef(skill="abd-architecture-reference", role="engineer"),
                    ],
                ),
            ],
        )
        ticket = Ticket(
            ticket_id="1-inc",
            lineage=["P"],
            scope_level="increment",
            stage="exploration",
            priority=1,
            skill_progress={
                "abd-ubiquitous-language": SkillProgress(
                    execution_status="done", agent="business-expert", review_status="done"
                ),
                "abd-acceptance-criteria": SkillProgress(
                    execution_status="done", agent="product-owner", review_status="done"
                ),
            },
        )
        match = kb.find_next_eligible([ticket], "engineer")
        self.assertIsNotNone(match)
        assert match is not None
        self.assertEqual(match[1], "abd-architecture-reference")

    def test_engineer_arch_template_after_specification_priors(self) -> None:
        kb = KanbanBoard(
            name="test",
            stages=[
                StageDef(
                    name="specification",
                    scope="sprint",
                    stage_work_required=[
                        SkillDef(skill="abd-class-responsibility-collaborator", role="business-expert"),
                        SkillDef(skill="abd-specification-by-example", role="product-owner"),
                        SkillDef(skill="abd-architecture-template", role="engineer"),
                    ],
                ),
            ],
        )
        ticket = Ticket(
            ticket_id="1-sprint",
            lineage=["P"],
            scope_level="sprint",
            stage="specification",
            priority=1,
            skill_progress={
                "abd-class-responsibility-collaborator": SkillProgress(
                    execution_status="done", agent="business-expert", review_status="done"
                ),
                "abd-specification-by-example": SkillProgress(
                    execution_status="done", agent="product-owner", review_status="done"
                ),
            },
        )
        match = kb.find_next_eligible([ticket], "engineer")
        self.assertIsNotNone(match)
        assert match is not None
        self.assertEqual(match[1], "abd-architecture-template")


if __name__ == "__main__":
    unittest.main()
