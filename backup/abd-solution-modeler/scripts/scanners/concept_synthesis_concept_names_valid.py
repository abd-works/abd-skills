"""Scanner: concept names must be valid domain terms, not instruction verbs."""
import json
from .base import BaseScanner, Violation

_INSTRUCTION_VERBS = frozenset({
    "Choose", "Apply", "Because", "Although", "Select", "Use",
    "While", "Since", "When", "If", "Then", "And", "Or",
})


class ConceptSynthesisConceptNamesValidScanner(BaseScanner):
    rule_id = "concept_synthesis-concept-names-valid"

    def scan(self, content: str, source_path=None) -> list[Violation]:
        violations = []
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return [Violation(rule_id=self.rule_id, message="Invalid JSON", location=str(source_path or ""))]
        concepts = data.get("concepts", {})
        for name in concepts:
            if name in _INSTRUCTION_VERBS:
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message=f"Concept '{name}' is an instruction verb, not a domain term",
                    location=str(source_path or ""),
                    snippet=name,
                ))
            elif name.startswith(("A ", "The ", "An ")) and len(name) < 25:
                violations.append(Violation(
                    rule_id=self.rule_id,
                    message=f"Concept '{name}' looks like article+noun fragment",
                    location=str(source_path or ""),
                    snippet=name,
                ))
        return violations
