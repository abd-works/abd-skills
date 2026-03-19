"""Scanner: every epic must have at least two confirming story names.

Rule: epic-requires-confirming-stories
Rule file: rules/epic-requires-confirming-stories.md

Highlights epics with fewer than two confirming stories. Does NOT determine
what the missing stories should be. The AI resolves each violation.

Usage (standalone):
    python scripts/mms_scan_epic_requires_confirming_stories.py [--input <path>]

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


RULE_ID = "epic-requires-confirming-stories"
MIN_STORIES = 2


def scan(data: dict, source_path: str = "") -> list[Violation]:
    violations: list[Violation] = []

    for pair_idx, pair in enumerate(data.get("modules_and_epics", [])):
        epic = pair.get("epic", {})
        epic_name = epic.get("name", f"<unnamed-epic-{pair_idx}>").strip()
        eloc = f"modules_and_epics[{pair_idx}].epic['{epic_name}']"

        confirming = epic.get("confirming_stories", [])
        if not isinstance(confirming, list):
            confirming = []

        # Filter out empty strings
        valid = [s for s in confirming if isinstance(s, str) and s.strip()]

        if len(valid) < MIN_STORIES:
            violations.append(Violation(
                rule_id=RULE_ID,
                message=(
                    f"epic has {len(valid)} confirming story name(s) — "
                    f"at least {MIN_STORIES} required"
                ),
                location=eloc,
                snippet=epic_name,
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
        description=f"Epic confirming stories scanner. Rule: {RULE_ID}"
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
        print(f"PASS [{RULE_ID}] — all epics have at least {MIN_STORIES} confirming stories in {input_path.name}")
        return 0

    print(f"VIOLATIONS [{RULE_ID}] — {len(violations)} epic(s) in {input_path.name}")
    print(f"  Rule: rules/epic-requires-confirming-stories.md")
    print(f"  AI must determine: add stories | flag [uncertain] | collapse into another epic\n")
    for v in violations:
        print(f"  [{v.severity.upper()}] {v.location}")
        print(f"         {v.message}")
        if v.snippet:
            print(f"         snippet: {v.snippet!r}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
