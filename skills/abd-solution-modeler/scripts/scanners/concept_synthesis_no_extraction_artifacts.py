"""Scanner: no extraction artifacts as concepts (All X, truncations, fragments)."""
import json
import re
from .base import BaseScanner, Violation

_ARTIFACT_PATTERNS = [
    re.compile(r"^All\s+\w+$", re.I),
    re.compile(r"^(Afflic|Communica|Compli|Transac|Rev|Cust)\w*$", re.I),
    re.compile(r"^COST PER (RANK|ITEM)\s+\w*$", re.I),
]
# M&M domain: valid concepts that match artifact patterns
_MM_RETAIN = frozenset({"Affliction", "Communication", "Complication"})


class ConceptSynthesisNoExtractionArtifactsScanner(BaseScanner):
    rule_id = "concept_synthesis-no-extraction-artifacts"

    def scan(self, content: str, source_path=None) -> list[Violation]:
        violations = []
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return [Violation(rule_id=self.rule_id, message="Invalid JSON", location=str(source_path or ""))]
        concepts = data.get("concepts", {})
        for name in concepts:
            if name in _MM_RETAIN:
                continue
            for pat in _ARTIFACT_PATTERNS:
                if pat.search(name):
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message=f"Extraction artifact '{name}' should be merged or removed",
                        location=str(source_path or ""),
                        snippet=name,
                    ))
                    break
        return violations
