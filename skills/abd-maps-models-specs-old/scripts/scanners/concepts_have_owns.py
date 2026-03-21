"""Scanner: every concept must have owns (decision ownership).

Rule: concepts-must-have-owns
Rule file: rules/concepts-must-have-owns.md

Flags concepts with missing or empty owns. [defer] in owns is acceptable.
The AI determines whether each violation is genuine or false positive.

Usage (standalone):
    python scripts/scanners/concepts_have_owns.py [--input <path>]

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


RULE_ID = "concepts-must-have-owns"


def scan(data: dict, source_path: str = "") -> list[Violation]:
    violations: list[Violation] = []

    for pair_idx, pair in enumerate(data.get("modules_and_epics", [])):
        module = pair.get("module", {})
        module_name = module.get("name", f"<unnamed-{pair_idx}>")
        mloc = f"modules_and_epics[{pair_idx}].module['{module_name}']"

        for cidx, concept in enumerate(module.get("concepts", [])):
            cname = concept.get("name", f"<unnamed-{cidx}>")
            cloc = f"{mloc}.concepts['{cname}']"
            owns = concept.get("owns", "").strip()

            if not owns:
                violations.append(Violation(
                    rule_id=RULE_ID,
                    message="concept.owns is missing or empty — every concept must own a decision or rule",
                    location=cloc,
                    snippet=cname,
                ))
            elif owns.lower().startswith("[defer]"):
                # [defer] is acceptable — Step 2 will resolve
                pass
            elif len(owns) < 10:
                violations.append(Violation(
                    rule_id=RULE_ID,
                    message="concept.owns is too short to describe decision ownership",
                    location=cloc,
                    snippet=owns,
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
        description=f"Concept owns scanner. Rule: {RULE_ID}"
    )
    parser.add_argument(
        "--input",
        default=default_input,
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        alt = Path(default_input)
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
        print(f"PASS [{RULE_ID}] — all concepts have owns in {input_path.name}")
        return 0

    print(f"VIOLATIONS [{RULE_ID}] — {len(violations)} concept(s) missing owns in {input_path.name}")
    print(f"  Rule: rules/concepts-must-have-owns.md\n")
    for v in violations:
        print(f"  [{v.severity.upper()}] {v.location}")
        print(f"         {v.message}")
        if v.snippet:
            print(f"         snippet: {v.snippet!r}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
