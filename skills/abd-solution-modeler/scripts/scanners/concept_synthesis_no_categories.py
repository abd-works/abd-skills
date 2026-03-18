"""Scanner: no section headers or structural categories as concepts."""
import json
from .base import BaseScanner, Violation

# Section headers (finance, retail, teco, generic)
_CATEGORIES = frozenset({
    "ACTION", "ADVANTAGES", "ADVENTURE", "COMBAT", "DEFENSE", "DEFENSES",
    "BALANCE SHEET", "INCOME STATEMENT", "CHECKOUT", "PRODUCT CATALOG",
    "COST PER RANK", "COST PER ITEM", "THE BASICS", "Powers", "SERVICE TIERS",
})


class ConceptSynthesisNoCategoriesScanner(BaseScanner):
    rule_id = "concept_synthesis-no-categories"

    def scan(self, content: str, source_path=None) -> list[Violation]:
        violations = []
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return [Violation(rule_id=self.rule_id, message="Invalid JSON", location=str(source_path or ""))]
        concepts = data.get("concepts", {})
        for name in concepts:
            if name in _CATEGORIES:
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message=f"Section/category '{name}' should not be a concept",
                    location=str(source_path or ""),
                    snippet=name,
                ))
        return violations
