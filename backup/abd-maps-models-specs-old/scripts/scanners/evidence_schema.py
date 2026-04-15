"""Scanner: evidence files must be valid JSON.

Rule: evidence-schema-valid
Rule file: rules/evidence-schema-valid.md

Validates that each evidence file parses as valid JSON.

Usage (standalone):
    python scripts/scanners/evidence_schema.py [--evidence <dir>]

Default evidence dir: evidence/
Exit code 0 = no violations. Exit code 1 = violations found.
"""
import argparse
import json
import sys
from pathlib import Path

RULE_ID = "evidence-schema-valid"
REQUIRED_FILES = ["actions.json", "decisions.json", "states.json", "relationships.json"]


def scan(evidence_dir: Path) -> list[tuple[str, str]]:
    """Return list of (file, message) for invalid JSON."""
    violations = []
    for fname in REQUIRED_FILES:
        p = evidence_dir / fname
        if not p.exists():
            continue  # skip — evidence-files-exist handles that
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            violations.append((fname, f"Invalid JSON: {e}"))
    return violations


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    scripts_dir = script_dir.parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    try:
        from _config import default_evidence_dir

        default_evidence = str(default_evidence_dir())
    except ImportError as e:
        print(f"Error: could not import _config: {e}", file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser(
        description=f"Evidence schema scanner. Rule: {RULE_ID}"
    )
    parser.add_argument(
        "--evidence",
        default=default_evidence,
    )
    args = parser.parse_args()

    evidence_dir = Path(args.evidence)
    violations = scan(evidence_dir)

    if violations:
        for fname, msg in violations:
            print(f"[{RULE_ID}] {fname}: {msg}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
