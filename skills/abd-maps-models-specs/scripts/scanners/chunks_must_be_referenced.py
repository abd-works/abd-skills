"""Scanner: all evidence claims must cite a chunk.

Rule: chunks-must-be-referenced
Rule file: rules/chunks-must-be-referenced.md

Highlights fields that make evidence claims without citing a chunk.
Reports locations — does NOT propose fixes.
The AI determines whether each violation is a genuine gap, a false positive,
or evidence that a [defer] flag should be added.

Usage (standalone):
    python scripts/scanners/chunks_must_be_referenced.py [--input <path>]

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


RULE_ID = "chunks-must-be-referenced"


def scan(data: dict, source_path: str = "") -> list[Violation]:
    violations: list[Violation] = []

    for pair_idx, pair in enumerate(data.get("modules_and_epics", [])):
        module = pair.get("module", {})
        epic = pair.get("epic", {})
        module_name = module.get("name", f"<unnamed-{pair_idx}>")
        epic_name = epic.get("name", f"<unnamed-epic-{pair_idx}>")
        mloc = f"modules_and_epics[{pair_idx}].module['{module_name}']"
        eloc = f"modules_and_epics[{pair_idx}].epic['{epic_name}']"

        # Module description chunk
        if (module.get("description") or "").strip() and not (module.get("description_chunk") or "").strip():
            violations.append(Violation(
                rule_id=RULE_ID,
                message="module.description is populated but description_chunk is missing",
                location=mloc,
                snippet=module_name,
            ))

        # Concepts
        for cidx, concept in enumerate(module.get("concepts", [])):
            cname = concept.get("name", f"<unnamed-{cidx}>")
            cloc = f"{mloc}.concepts['{cname}']"

            # chunk_ids or chunk_evidence must be non-empty (chunk_evidence has chunk_id, evidence_type, note)
            chunk_ids = concept.get("chunk_ids", [])
            if not chunk_ids and concept.get("chunk_evidence"):
                chunk_ids = [e["chunk_id"] for e in concept["chunk_evidence"] if e.get("chunk_id")]
            if not isinstance(chunk_ids, list) or len(chunk_ids) == 0:
                violations.append(Violation(
                    rule_id=RULE_ID,
                    message="concept.chunk_ids (or chunk_evidence) is missing or empty",
                    location=cloc,
                    snippet=cname,
                ))

            # owns requires owns_chunk
            if (concept.get("owns") or "").strip() and not (concept.get("owns_chunk") or "").strip():
                violations.append(Violation(
                    rule_id=RULE_ID,
                    message="concept.owns is populated but owns_chunk is missing",
                    location=cloc,
                    snippet=cname,
                ))

            # Properties
            for pidx, prop in enumerate(concept.get("properties", [])):
                if (prop.get("definition") or "").strip() and not (prop.get("chunk") or "").strip():
                    violations.append(Violation(
                        rule_id=RULE_ID,
                        message="property.definition is populated but chunk is missing",
                        location=f"{cloc}.properties[{pidx}]",
                        snippet=prop.get("definition", "")[:60],
                    ))

            # Operations
            for oidx, op in enumerate(concept.get("operations", [])):
                if (op.get("definition") or "").strip() and not (op.get("chunk") or "").strip():
                    violations.append(Violation(
                        rule_id=RULE_ID,
                        message="operation.definition is populated but chunk is missing",
                        location=f"{cloc}.operations[{oidx}]",
                        snippet=op.get("definition", "")[:60],
                    ))

        # Epic statement chunk
        if (epic.get("statement") or "").strip() and not (epic.get("statement_chunk") or "").strip():
            violations.append(Violation(
                rule_id=RULE_ID,
                message="epic.statement is populated but statement_chunk is missing",
                location=eloc,
                snippet=epic_name,
            ))

        # Epic pre_condition chunk (only required when pre_condition is populated)
        if (epic.get("pre_condition") or "").strip() and not (epic.get("pre_condition_chunk") or "").strip():
            violations.append(Violation(
                rule_id=RULE_ID,
                message="epic.pre_condition is populated but pre_condition_chunk is missing",
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
        description=f"Chunk citation scanner. Rule: {RULE_ID}"
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
        print(f"PASS [{RULE_ID}] — no missing chunk citations in {input_path.name}")
        return 0

    print(f"VIOLATIONS [{RULE_ID}] — {len(violations)} missing citation(s) in {input_path.name}")
    print(f"  Rule: rules/chunks-must-be-referenced.md")
    print(f"  AI must determine: genuine gap | false positive | needs [defer] flag\n")
    for v in violations:
        print(f"  [{v.severity.upper()}] {v.location}")
        print(f"         {v.message}")
        if v.snippet:
            print(f"         snippet: {v.snippet!r}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
