"""Evidence scoring for map-model-spec concepts.

Supports the richer Step 2 structure: chunk_evidence with evidence_type and note.
Weights: definition > rule > example/table > mention.
"""
EVIDENCE_TYPE_WEIGHTS = {
    "definition": 5,
    "rule": 4,
    "example": 3,
    "table": 3,
    "mention": 1,
}


def concept_evidence_score(concept: dict) -> float:
    """Score a concept's evidence from chunk_evidence. Higher = stronger evidence."""
    evidence = concept.get("chunk_evidence", [])
    if not evidence:
        # Fallback: plain chunk_ids count as mention
        chunk_ids = concept.get("chunk_ids", [])
        return len(chunk_ids) * EVIDENCE_TYPE_WEIGHTS["mention"]
    return sum(
        EVIDENCE_TYPE_WEIGHTS.get(
            (e.get("evidence_type") or "mention").lower(),
            EVIDENCE_TYPE_WEIGHTS["mention"],
        )
        for e in evidence
    )


def concept_evidence_summary(concept: dict) -> dict[str, int]:
    """Count evidence by type for a concept."""
    counts: dict[str, int] = {}
    evidence = concept.get("chunk_evidence", [])
    if not evidence:
        chunk_ids = concept.get("chunk_ids", [])
        if chunk_ids:
            counts["mention"] = len(chunk_ids)
        return counts
    for e in evidence:
        t = (e.get("evidence_type") or "mention").lower()
        counts[t] = counts.get(t, 0) + 1
    return counts
