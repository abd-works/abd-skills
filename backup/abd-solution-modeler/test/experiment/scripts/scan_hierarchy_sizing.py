"""Scanner: hierarchy — approximately 4 to 9 children per node.

Rule: hierarchy-approximately-4-to-9-children
Rule file: test/experiment/rules/hierarchy-approximately-4-to-9-children.md

Flags nodes with more than 9 children. Does not flag low counts (2–3) at Step 2.
Epic: count sub_epics if present, else stories. Sub-epic: count stories.

Usage (standalone):
    python test/experiment/scripts/scan_hierarchy_sizing.py [--input <path>]

Default input: test/experiment/output.json
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


RULE_ID = "hierarchy-approximately-4-to-9-children"
MAX_CHILDREN = 9


def scan(data: dict, source_path: str = "") -> list[Violation]:
    violations: list[Violation] = []

    for pair_idx, pair in enumerate(data.get("modules_and_epics", [])):
        epic = pair.get("epic", {})
        epic_name = epic.get("name", f"<unnamed-epic-{pair_idx}>")
        eloc = f"modules_and_epics[{pair_idx}].epic['{epic_name}']"

        # Epic children: sub_epics if present, else stories, else confirming_stories
        sub_epics = epic.get("sub_epics", [])
        stories = epic.get("stories", [])
        confirming = epic.get("confirming_stories", [])

        if sub_epics:
            count = len(sub_epics)
            if count > MAX_CHILDREN:
                violations.append(Violation(
                    rule_id=RULE_ID,
                    message=f"epic has {count} sub-epics (max {MAX_CHILDREN}) — split or regroup",
                    location=f"{eloc}.sub_epics",
                    snippet=epic_name,
                ))
            # Check each sub-epic's story count
            for seidx, sub in enumerate(sub_epics):
                if isinstance(sub, dict):
                    sub_name = sub.get("name", f"<sub-epic-{seidx}>")
                    sub_stories = sub.get("stories", [])
                    sc = len([s for s in sub_stories if isinstance(s, dict)]) or len([s for s in sub_stories if isinstance(s, str)])
                    if sc > MAX_CHILDREN:
                        violations.append(Violation(
                            rule_id=RULE_ID,
                            message=f"sub-epic '{sub_name}' has {sc} stories (max {MAX_CHILDREN}) — split or regroup",
                            location=f"{eloc}.sub_epics['{sub_name}'].stories",
                            snippet=sub_name,
                        ))
        elif stories:
            count = len([s for s in stories if isinstance(s, dict)])
            if count > MAX_CHILDREN:
                violations.append(Violation(
                    rule_id=RULE_ID,
                    message=f"epic has {count} stories (max {MAX_CHILDREN}) — add sub-epics or regroup",
                    location=f"{eloc}.stories",
                    snippet=epic_name,
                ))
        elif confirming:
            count = len(confirming)
            if count > MAX_CHILDREN:
                violations.append(Violation(
                    rule_id=RULE_ID,
                    message=f"epic has {count} confirming_stories (max {MAX_CHILDREN}) — add sub-epics or regroup",
                    location=f"{eloc}.confirming_stories",
                    snippet=epic_name,
                ))

    return violations


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    experiment_dir = script_dir.parent

    parser = argparse.ArgumentParser(
        description=f"Hierarchy sizing scanner. Rule: {RULE_ID}"
    )
    parser.add_argument(
        "--input",
        default=str(experiment_dir / "output.json"),
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        alt = experiment_dir / "output.json"
        if alt.exists():
            input_path = alt
        else:
            print(f"ERROR: Input file not found: {args.input}")
            return 1

    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {input_path}: {e}")
        return 1

    violations = scan(data, source_path=str(input_path))

    if not violations:
        print(f"PASS [{RULE_ID}] — no node exceeds {MAX_CHILDREN} children in {input_path.name}")
        return 0

    print(f"VIOLATIONS [{RULE_ID}] — {len(violations)} node(s) exceed {MAX_CHILDREN} children in {input_path.name}")
    print(f"  Rule: test/experiment/rules/hierarchy-approximately-4-to-9-children.md\n")
    for v in violations:
        print(f"  [{v.severity.upper()}] {v.location}")
        print(f"         {v.message}")
        if v.snippet:
            print(f"         snippet: {v.snippet!r}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
