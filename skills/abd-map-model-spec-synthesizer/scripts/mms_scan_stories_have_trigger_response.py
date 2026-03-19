"""Scanner: every story must have trigger and response.

Rule: stories-must-have-trigger-response
Rule file: rules/stories-must-have-trigger-response.md

Flags stories (full objects) with missing trigger or response.
When epic has only confirming_stories (names), this scanner is N/A — skip.
When epic has stories (objects), each must have trigger and response.

Usage (standalone):
    python scripts/mms_scan_stories_have_trigger_response.py [--input <path>]

Default input: map-model-spec.json
Exit code 0 = no violations. Exit code 1 = violations found.
"""
import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Violation:
    rule_id: str
    message: str
    location: str
    severity: str = "warning"
    snippet: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "message": self.message,
            "location": self.location,
            "severity": self.severity,
            "snippet": self.snippet,
        }


RULE_ID = "stories-must-have-trigger-response"


def _collect_stories(epic: dict) -> list[tuple[str, dict]]:
    """Return [(location_prefix, story), ...] for all stories in epic."""
    stories: list[tuple[str, dict]] = []
    epic_name = epic.get("name", "")

    # Top-level stories
    for sidx, story in enumerate(epic.get("stories", [])):
        if isinstance(story, dict):
            stories.append((f"epic.stories[{sidx}]", story))
        # If story is a string (name only), skip — Step 1 format

    # Sub-epic stories
    for seidx, sub in enumerate(epic.get("sub_epics", [])):
        if isinstance(sub, dict):
            sub_name = sub.get("name", f"<sub-epic-{seidx}>")
            for sidx, story in enumerate(sub.get("stories", [])):
                if isinstance(story, dict):
                    stories.append((f"sub_epics['{sub_name}'].stories[{sidx}]", story))

    return stories


def scan(data: dict, source_path: str = "") -> list[Violation]:
    violations: list[Violation] = []

    for pair_idx, pair in enumerate(data.get("modules_and_epics", [])):
        epic = pair.get("epic", {})
        epic_name = epic.get("name", f"<unnamed-epic-{pair_idx}>")
        eloc = f"modules_and_epics[{pair_idx}].epic['{epic_name}']"

        for loc_suffix, story in _collect_stories(epic):
            sname = story.get("name", "<unnamed>")
            cloc = f"{eloc}.{loc_suffix}['{sname}']"

            trigger = story.get("trigger", "").strip()
            response = story.get("response", "").strip()

            if not trigger:
                violations.append(Violation(
                    rule_id=RULE_ID,
                    message="story.trigger is missing or empty — every story must have Actor + action",
                    location=cloc,
                    snippet=sname,
                ))
            if not response:
                violations.append(Violation(
                    rule_id=RULE_ID,
                    message="story.response is missing or empty — every story must have system/actor response",
                    location=cloc,
                    snippet=sname,
                ))

    return violations


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    try:
        from _config import default_map_model_spec_path
        default_input = str(default_map_model_spec_path())
    except ImportError:
        default_input = str(skill_dir / "map-model-spec.json")

    parser = argparse.ArgumentParser(
        description=f"Story trigger/response scanner. Rule: {RULE_ID}"
    )
    parser.add_argument(
        "--input",
        default=default_input,
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        return 1

    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {input_path}: {e}")
        return 1

    violations = scan(data, source_path=str(input_path))

    if not violations:
        print(f"PASS [{RULE_ID}] — all stories have trigger and response in {input_path.name}")
        return 0

    print(f"VIOLATIONS [{RULE_ID}] — {len(violations)} story/stories missing trigger or response in {input_path.name}")
    print(f"  Rule: rules/stories-must-have-trigger-response.md\n")
    for v in violations:
        print(f"  [{v.severity.upper()}] {v.location}")
        print(f"         {v.message}")
        if v.snippet:
            print(f"         snippet: {v.snippet!r}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
