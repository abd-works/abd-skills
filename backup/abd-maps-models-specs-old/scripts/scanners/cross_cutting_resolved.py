"""Scanner: all cross-cutting items must be resolved.

Rule: cross-cutting-resolved
Rule file: rules/cross-cutting-resolved.md

Flags non-empty cross_cutting_notes — unresolved [cross-cutting] items
must be resolved before evidence extraction.

Usage (standalone):
    python scripts/scanners/cross_cutting_resolved.py [--input <path>]

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


RULE_ID = "cross-cutting-resolved"


def scan(data: dict, source_path: str = "") -> list[Violation]:
    violations: list[Violation] = []

    notes = data.get("cross_cutting_notes")
    if notes is None:
        return violations

    # String: non-empty after strip = unresolved
    if isinstance(notes, str):
        if notes.strip():
            violations.append(Violation(
                rule_id=RULE_ID,
                message="cross_cutting_notes is non-empty — unresolved [cross-cutting] items remain",
                location="cross_cutting_notes",
                snippet=notes.strip()[:200] + ("..." if len(notes.strip()) > 200 else ""),
            ))
        return violations

    # List: non-empty = unresolved
    if isinstance(notes, list) and len(notes) > 0:
        violations.append(Violation(
            rule_id=RULE_ID,
            message=f"cross_cutting_notes has {len(notes)} unresolved item(s)",
            location="cross_cutting_notes",
            snippet=str(notes)[:200] + ("..." if len(str(notes)) > 200 else ""),
        ))

    return violations


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    scripts_dir = script_dir.parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    try:
        from _config import default_map_model_spec_path

        default_input = str(default_map_model_spec_path())
    except ImportError as e:
        print(f"Error: could not import _config: {e}", file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser(
        description=f"Cross-cutting resolved scanner. Rule: {RULE_ID}"
    )
    parser.add_argument(
        "--input",
        default=default_input,
    )
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        return 2

    data = json.loads(path.read_text(encoding="utf-8"))
    violations = scan(data, str(path))

    if violations:
        for v in violations:
            print(f"[{v.rule_id}] {v.location}: {v.message}")
            if v.snippet:
                print(f"  snippet: {v.snippet[:100]}...")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
