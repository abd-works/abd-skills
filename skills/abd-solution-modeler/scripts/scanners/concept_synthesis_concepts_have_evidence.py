"""Scanner: all concepts must have evidence (term_ids, chunk_ids, performs, receives)."""
import json
from .base import BaseScanner, Violation


class ConceptSynthesisConceptsHaveEvidenceScanner(BaseScanner):
    rule_id = "concept_synthesis-concepts-have-evidence"

    def scan(self, content: str, source_path=None) -> list[Violation]:
        violations = []
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return [Violation(rule_id=self.rule_id, message="Invalid JSON", location=str(source_path or ""))]
        concepts = data.get("concepts", {})
        for name, c in concepts.items():
            term_ids = c.get("term_ids") or []
            chunk_ids = c.get("chunk_ids") or []
            performs = c.get("performs") or []
            receives = c.get("receives") or []
            if not (term_ids or chunk_ids or performs or receives):
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message=f"Concept '{name}' has no evidence (term_ids, chunk_ids, performs, receives)",
                    location=str(source_path or ""),
                    snippet=name,
                ))
        return violations
