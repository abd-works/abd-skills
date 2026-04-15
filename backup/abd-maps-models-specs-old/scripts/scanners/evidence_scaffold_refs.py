"""Scanner: evidence must reference only scaffold concepts.

Rule: evidence-scaffold-refs
Rule file: rules/evidence-scaffold-refs.md

Flags concept IDs in evidence files that do not exist in map-model-spec.json.

Supports evidence structures:
- Top-level keys: {"ConceptA": [...], "ConceptB": [...]}
- Nested: {"concepts": {"ConceptA": [...], "ConceptB": [...]}}

Usage (standalone):
    python scripts/scanners/evidence_scaffold_refs.py [--scaffold <path>] [--evidence <dir>]

Default: map-model-spec.json, evidence/
Exit code 0 = no violations. Exit code 1 = violations found.
"""
import argparse
import json
import sys
from pathlib import Path

RULE_ID = "evidence-scaffold-refs"
REQUIRED_FILES = ["actions.json", "decisions.json", "states.json", "relationships.json"]


def _collect_scaffold_concepts(scaffold: dict) -> set[str]:
    """Extract all concept names from map-model-spec.json."""
    concepts = set()
    for pair in scaffold.get("modules_and_epics", []):
        module = pair.get("module", {})
        for c in module.get("concepts", []):
            name = c.get("name", "").strip()
            if name:
                concepts.add(name)
    return concepts


def _collect_evidence_concepts(data: dict) -> set[str]:
    """Extract concept keys from evidence file (top-level or nested)."""
    concepts = set()
    if "concepts" in data and isinstance(data["concepts"], dict):
        concepts.update(k for k in data["concepts"].keys() if k.strip())
    else:
        # Top-level keys
        for k, v in data.items():
            if k in ("concepts", "metadata") or not isinstance(v, (dict, list)):
                continue
            concepts.add(k)
    return concepts


def scan(scaffold_path: Path, evidence_dir: Path) -> list[tuple[str, str, str]]:
    """Return list of (file, concept, message)."""
    violations = []

    if not scaffold_path.exists():
        return [(None, None, f"Scaffold not found: {scaffold_path}")]

    scaffold = json.loads(scaffold_path.read_text(encoding="utf-8"))
    scaffold_concepts = _collect_scaffold_concepts(scaffold)

    for fname in REQUIRED_FILES:
        p = evidence_dir / fname
        if not p.exists():
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue  # schema scanner handles that

        evidence_concepts = _collect_evidence_concepts(data)
        for c in evidence_concepts:
            if c not in scaffold_concepts:
                violations.append((fname, c, f"Concept '{c}' not in scaffold"))

    return violations


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    scripts_dir = script_dir.parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    try:
        from _config import default_evidence_dir, default_map_model_spec_path

        default_scaffold = str(default_map_model_spec_path())
        default_evidence = str(default_evidence_dir())
    except ImportError as e:
        print(f"Error: could not import _config: {e}", file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser(
        description=f"Evidence scaffold refs scanner. Rule: {RULE_ID}"
    )
    parser.add_argument(
        "--scaffold",
        default=default_scaffold,
    )
    parser.add_argument(
        "--evidence",
        default=default_evidence,
    )
    args = parser.parse_args()

    scaffold_path = Path(args.scaffold)
    evidence_dir = Path(args.evidence)
    violations = scan(scaffold_path, evidence_dir)

    if violations:
        for item in violations:
            fname, concept, msg = item
            if fname:
                print(f"[{RULE_ID}] {fname}: {msg}")
            else:
                print(f"[{RULE_ID}] {msg}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
