"""Scanner: evidence-bearing fields in map-model-spec.json cite corpus chunks.

Rule: evidence-citations-required (domain / map-model-spec slice)

Supports:
- Legacy **`modules_and_epics[]`** tree (module + epic + concepts) with `chunk_ids`,
  `chunk_evidence`, `description_chunk`, `statement_chunk`, `owns_chunk`, property/operation `chunk`.
- **MM3 extensions:** `evidence_chunk_ids[]` on concepts; `evidence_chunk_id` on properties/operations
  when `chunk` is absent.

Does not validate IDs against `context_index.json` (use `scanners/context_index_contract.py` + manual review);
this scanner checks *presence* of citations, matching the old pipeline’s role.

Usage:
    python scripts/scanners/chunks_must_be_referenced.py [--input <path>]

Default input: `<output_dir>/maps-models-specs/map-model-spec.json`
Exit 0 = no violations. Exit 1 = violations found.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


@dataclass
class Violation:
    rule_id: str
    message: str
    location: str
    severity: str = "warning"
    snippet: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "message": self.message,
            "location": self.location,
            "severity": self.severity,
            "snippet": self.snippet,
        }


RULE_ID = "chunks-must-be-referenced"


def _concept_has_chunk_citation(concept: dict) -> bool:
    chunk_ids = concept.get("chunk_ids")
    if isinstance(chunk_ids, list) and len(chunk_ids) > 0:
        return True
    ce = concept.get("chunk_evidence")
    if isinstance(ce, list) and any(
        isinstance(e, dict) and (e.get("chunk_id") or "").strip() for e in ce
    ):
        return True
    eids = concept.get("evidence_chunk_ids")
    if isinstance(eids, list) and len(eids) > 0:
        return True
    return False


def _prop_or_op_has_chunk(row: dict) -> bool:
    if (row.get("chunk") or "").strip():
        return True
    if (row.get("evidence_chunk_id") or "").strip():
        return True
    return False


def scan(data: dict, source_path: str = "") -> list[Violation]:
    violations: list[Violation] = []
    pairs = data.get("modules_and_epics")
    if not isinstance(pairs, list):
        return violations

    for pair_idx, pair in enumerate(pairs):
        if not isinstance(pair, dict):
            continue
        module = pair.get("module") or {}
        epic = pair.get("epic") or {}
        module_name = module.get("name", f"<unnamed-{pair_idx}>")
        epic_name = epic.get("name", f"<unnamed-epic-{pair_idx}>")
        mloc = f"modules_and_epics[{pair_idx}].module['{module_name}']"
        eloc = f"modules_and_epics[{pair_idx}].epic['{epic_name}']"

        if (module.get("description") or "").strip() and not (
            (module.get("description_chunk") or "").strip()
            or (module.get("description_evidence_chunk") or "").strip()
        ):
            violations.append(
                Violation(
                    rule_id=RULE_ID,
                    message="module.description is populated but no description_chunk / description_evidence_chunk",
                    location=mloc,
                    snippet=module_name,
                )
            )

        for cidx, concept in enumerate(module.get("concepts") or []):
            if not isinstance(concept, dict):
                continue
            cname = concept.get("name", f"<unnamed-{cidx}>")
            cloc = f"{mloc}.concepts['{cname}']"

            if not _concept_has_chunk_citation(concept):
                violations.append(
                    Violation(
                        rule_id=RULE_ID,
                        message="concept missing chunk_ids, chunk_evidence, or evidence_chunk_ids",
                        location=cloc,
                        snippet=cname,
                    )
                )

            if (concept.get("owns") or "").strip() and not (
                (concept.get("owns_chunk") or "").strip()
                or (concept.get("owns_evidence_chunk") or "").strip()
            ):
                violations.append(
                    Violation(
                        rule_id=RULE_ID,
                        message="concept.owns is populated but owns_chunk / owns_evidence_chunk is missing",
                        location=cloc,
                        snippet=cname,
                    )
                )

            for pidx, prop in enumerate(concept.get("properties") or []):
                if not isinstance(prop, dict):
                    continue
                if (prop.get("definition") or "").strip() and not _prop_or_op_has_chunk(prop):
                    violations.append(
                        Violation(
                            rule_id=RULE_ID,
                            message="property.definition is populated but chunk / evidence_chunk_id is missing",
                            location=f"{cloc}.properties[{pidx}]",
                            snippet=(prop.get("definition") or "")[:60],
                        )
                    )

            for oidx, op in enumerate(concept.get("operations") or []):
                if not isinstance(op, dict):
                    continue
                if (op.get("definition") or "").strip() and not _prop_or_op_has_chunk(op):
                    violations.append(
                        Violation(
                            rule_id=RULE_ID,
                            message="operation.definition is populated but chunk / evidence_chunk_id is missing",
                            location=f"{cloc}.operations[{oidx}]",
                            snippet=(op.get("definition") or "")[:60],
                        )
                    )

        if (epic.get("statement") or "").strip() and not (epic.get("statement_chunk") or "").strip():
            violations.append(
                Violation(
                    rule_id=RULE_ID,
                    message="epic.statement is populated but statement_chunk is missing",
                    location=eloc,
                    snippet=epic_name,
                )
            )

        if (epic.get("pre_condition") or "").strip() and not (
            (epic.get("pre_condition_chunk") or "").strip()
        ):
            violations.append(
                Violation(
                    rule_id=RULE_ID,
                    message="epic.pre_condition is populated but pre_condition_chunk is missing",
                    location=eloc,
                    snippet=epic_name,
                )
            )

    return violations


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    scripts_dir = script_dir.parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    from _config import map_model_spec_path

    parser = argparse.ArgumentParser(description=f"Chunk citation scanner. Rule: {RULE_ID}")
    parser.add_argument("--input", default=str(map_model_spec_path()))
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"chunks_must_be_referenced: no file at {input_path} — skip")
        return 0

    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {input_path}: {e}", file=sys.stderr)
        return 1

    violations = scan(data, source_path=str(input_path))

    if not violations:
        print(f"PASS [{RULE_ID}] — no missing chunk citations in {input_path.name}")
        return 0

    print(f"VIOLATIONS [{RULE_ID}] — {len(violations)} missing citation(s) in {input_path.name}")
    for v in violations:
        print(f"  [{v.severity.upper()}] {v.location}")
        print(f"         {v.message}")
        if v.snippet:
            print(f"         snippet: {v.snippet!r}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
