"""Scanner: names must be unique within their scope.

Rule: no-duplicates
Rule file: rules/no-duplicates.md

Highlights duplicate concept names within a module and duplicate module names
across the output. Does NOT determine which to keep or how to rename.
The AI resolves each violation.

Usage (standalone):
    python scripts/mms_scan_no_duplicates.py [--input <path>]

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


RULE_ID = "no-duplicates"


def scan(data: dict, source_path: str = "") -> list[Violation]:
    violations: list[Violation] = []
    seen_module_names: dict[str, int] = {}

    for pair_idx, pair in enumerate(data.get("modules_and_epics", [])):
        module = pair.get("module", {})
        module_name = module.get("name", "").strip()

        if not module_name:
            continue

        mloc = f"modules_and_epics[{pair_idx}].module['{module_name}']"

        # Duplicate module name
        if module_name in seen_module_names:
            violations.append(Violation(
                rule_id=RULE_ID,
                message=f"Duplicate module name '{module_name}' — also at pair index {seen_module_names[module_name]}",
                location=mloc,
                snippet=module_name,
            ))
        else:
            seen_module_names[module_name] = pair_idx

        # Duplicate concept names within module
        seen_concept_names: dict[str, int] = {}
        for cidx, concept in enumerate(module.get("concepts", [])):
            cname = concept.get("name", "").strip()
            if not cname:
                continue
            if cname in seen_concept_names:
                violations.append(Violation(
                    rule_id=RULE_ID,
                    message=f"Duplicate concept name '{cname}' within module '{module_name}' — also at index {seen_concept_names[cname]}",
                    location=f"{mloc}.concepts['{cname}']",
                    snippet=cname,
                ))
            else:
                seen_concept_names[cname] = cidx

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
        description=f"Duplicate name scanner. Rule: {RULE_ID}"
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
        print(f"PASS [{RULE_ID}] — no duplicate names found in {input_path.name}")
        return 0

    print(f"VIOLATIONS [{RULE_ID}] — {len(violations)} duplicate(s) in {input_path.name}")
    print(f"  Rule: rules/no-duplicates.md")
    print(f"  AI must determine: merge | rename | remove\n")
    for v in violations:
        print(f"  [{v.severity.upper()}] {v.location}")
        print(f"         {v.message}")
        if v.snippet:
            print(f"         snippet: {v.snippet!r}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
