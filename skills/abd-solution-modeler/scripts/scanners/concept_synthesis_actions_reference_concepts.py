"""Scanner: action subject/object must reference valid concepts."""
import json
from .base import BaseScanner, Violation


class ConceptSynthesisActionsReferenceConceptsScanner(BaseScanner):
    rule_id = "concept_synthesis-actions-reference-concepts"

    def scan(self, content: str, source_path=None) -> list[Violation]:
        violations = []
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return [Violation(rule_id=self.rule_id, message="Invalid JSON", location=str(source_path or ""))]
        concepts = set(data.get("concepts", {}).keys())
        actions = data.get("registries", {}).get("actions", {})
        for act_id, act in actions.items():
            subj = (act.get("subject") or "").strip()
            obj = (act.get("object") or "").strip()
            if subj and subj not in concepts:
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message=f"Action {act_id} subject '{subj}' not in concepts",
                    location=str(source_path or ""),
                    snippet=act.get("raw", "")[:80],
                ))
            if obj and obj not in concepts:
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message=f"Action {act_id} object '{obj}' not in concepts",
                    location=str(source_path or ""),
                    snippet=act.get("raw", "")[:80],
                ))
        return violations
