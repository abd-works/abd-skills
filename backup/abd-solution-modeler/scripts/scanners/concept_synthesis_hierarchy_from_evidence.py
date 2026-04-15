"""Scanner: concept_hierarchy parent/child must exist in concepts."""
import json
from .base import BaseScanner, Violation


class ConceptSynthesisHierarchyFromEvidenceScanner(BaseScanner):
    rule_id = "concept_synthesis-hierarchy-from-evidence"

    def scan(self, content: str, source_path=None) -> list[Violation]:
        violations = []
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return [Violation(rule_id=self.rule_id, message="Invalid JSON", location=str(source_path or ""))]
        concepts = set(data.get("concepts", {}).keys())
        hierarchy = data.get("concept_hierarchy") or {}
        if isinstance(hierarchy, dict):
            for parent, children in hierarchy.items():
                if parent and parent not in concepts:
                    violations.append(Violation(
                        rule_id=self.rule_id,
                        message=f"Hierarchy parent '{parent}' not in concepts",
                        location=str(source_path or ""),
                        snippet=parent,
                    ))
                for child in (children or []) if isinstance(children, list) else []:
                    if child and child not in concepts:
                        violations.append(Violation(
                            rule_id=self.rule_id,
                            message=f"Hierarchy child '{child}' not in concepts",
                            location=str(source_path or ""),
                            snippet=child,
                        ))
        return violations
