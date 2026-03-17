#!/usr/bin/env python3
"""
Domain-agnostic guided evidence extraction.

Inputs:
- rule_chunks.json
- concept_guidance.json

Outputs:
- terms.json
- actions.json
- decisions.json
- states.json
- relationships.json
- modifiers.json
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def dump_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip()).lower()

def uniq(seq):
    seen = set()
    out = []
    for item in seq:
        key = json.dumps(item, sort_keys=True, ensure_ascii=False) if isinstance(item, (dict, list)) else item
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out

def build_alias_index(guidance: dict[str, Any]) -> tuple[dict[str, str], set[str]]:
    alias_to_canonical: dict[str, str] = {}
    canonicals: set[str] = set()

    for c in guidance.get("priority_concepts", []):
        canonicals.add(c)
        alias_to_canonical[norm(c)] = c

    for canonical, aliases in guidance.get("concept_aliases", {}).items():
        canonicals.add(canonical)
        alias_to_canonical[norm(canonical)] = canonical
        for alias in aliases:
            alias_to_canonical[norm(alias)] = canonical

    return alias_to_canonical, canonicals

def matched_concepts(text: str, alias_to_canonical: dict[str, str]) -> tuple[list[str], list[str]]:
    lower = norm(text)
    concepts = set()
    aliases = set()
    for alias, canonical in alias_to_canonical.items():
        if alias and alias in lower:
            concepts.add(canonical)
            if alias != norm(canonical):
                aliases.add(alias)
    return sorted(concepts), sorted(aliases)

def chunk_score(text: str, guidance: dict[str, Any], alias_to_canonical: dict[str, str]) -> float:
    lower = text.lower()
    score = 0.0
    for section in guidance.get("focus_sections", []):
        if section.lower() in lower:
            score += 3.0
    for noise in guidance.get("noise_filters", []):
        if noise.lower() in lower:
            score -= 5.0
    concepts, _ = matched_concepts(text, alias_to_canonical)
    score += min(6.0, len(concepts) * 1.5)
    for mech in guidance.get("priority_mechanisms", []):
        if mech.lower() in lower:
            score += 1.5
    for axis in guidance.get("variation_axes", []):
        if axis.lower() in lower:
            score += 1.0
    return score

def is_noise_chunk(text: str, guidance: dict[str, Any]) -> bool:
    lower = text.lower()
    fixed_noise = [
        "table of contents",
        "copyright",
        "open game license",
        "product identity",
        "isbn",
        "www.",
    ]
    if any(x in lower for x in fixed_noise):
        return True
    if any(x.lower() in lower for x in guidance.get("noise_filters", [])):
        return True
    return False


# Chunk-level gate: skip ToC, index, and heading-only chunks before sentence splitting.
# These chunks have no sentence boundaries (.!?;) so split_sentences yields one giant blob
# that can slip through line-level gates. Only skip when chunk has NO real prose (no .!?;)
# AND has ToC signals — avoids filtering chunks that mix headers with rule text.
_TOC_INDEX_PATTERNS = [
    re.compile(r"<!--\s*Source:"),  # HTML metadata at chunk start
    re.compile(r"CHAPTER\s+\d+:", re.IGNORECASE),
    re.compile(r"\.{4,}\s*\d{1,4}"),  # "..........107" ToC dots + page
    re.compile(r"^\d{1,4}\s+[A-Z]", re.MULTILINE),  # "107 Buying..." page-first lines
]


def is_toc_or_index_chunk(text: str) -> bool:
    """
    Skip chunks that are predominantly table-of-contents, index, or heading lists.
    Only skip when chunk has no sentence boundaries (.!?;) — i.e. no real rule prose —
    AND has ToC signals. Chunks with real prose keep their headers but pass through.
    """
    if not text or len(text.strip()) < 50:
        return False
    # Must have no sentence-ending punctuation — otherwise it's real prose
    sentence_endings = sum(1 for c in text if c in ".!?;")
    if sentence_endings >= 1:
        return False  # Has real sentences, let line-level gate handle noise
    # Check for ToC signals
    normalized = re.sub(r"\s+", " ", text.strip())
    hits = 0
    for pat in _TOC_INDEX_PATTERNS:
        if pat.search(text) or pat.search(normalized):
            hits += 1
    if hits >= 2:
        return True
    if re.search(r"<!--\s*Source:", text) and (
        re.search(r"CHAPTER\s+\d", text, re.IGNORECASE)
        or re.search(r"\.{4,}\s*\d{1,4}", text)
    ):
        return True
    return False


# Structural gate: reject lines that are NOT candidate rule prose.
# Must run before extraction. See: heading extraction, fragment extraction,
# prose extraction, archetype/example contamination.
_REJECT_PATTERNS = [
    re.compile(r"^CHAPTER\s+\d", re.IGNORECASE),
    re.compile(r"^[A-Z][A-Z\s]{8,}$"),  # all-caps section labels (HERO ARCHETYPES, SKILL BASICS)
    re.compile(r"^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*\.{2,}\s*\d{1,4}\s*$"),  # "Buying Ability Ranks ....107"
    re.compile(r"\bRoll\s+1d20\b", re.IGNORECASE),
    re.compile(r";[^;]*;[^;]*;"),  # semicolon-separated list (archetype packages)
    re.compile(r"^\d+-\d+\s*$"),  # roll table row label "1-4" or "5-7"
    re.compile(r"^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+\d{1,4}\s*$"),  # "Section Name 107"
    re.compile(r"\.{4,}\s*\d{1,4}"),  # "..........107" table of contents / index
    re.compile(r"^\d{1,4}\s+[A-Z]"),  # "107 Buying Ability Ranks" page-number-first
    re.compile(r"<!--\s*Source:"),  # HTML comment metadata
    re.compile(r"file:///|-->\s*CHAPTER|section\s+\d+\s*\|"),  # HTML/file path fragments
]
# ---------------------------------------------------------------------------
# Skill-level block list defaults (always applied)
# Workspace can extend each section via evidence/block_list.json
# ---------------------------------------------------------------------------

_SKILL_BLOCK_LIST: dict = {
    "_comment": "Skill-level defaults. Workspace extends these via evidence/block_list.json.",
    "weak_object_tokens": [
        "the", "this", "that", "these", "those",
        "for", "you", "they", "them", "their",
        "some", "all", "any", "each", "both", "many", "most",
        "normally", "additionally", "essentially", "generally",
        "his", "her", "its", "our", "your",
        "perhaps", "other", "others", "another",
        "it", "he", "she", "we",
        "move", "make", "use", "take", "get",
        "like", "finally", "every", "always", "never", "often",
        "simply", "instead", "already", "still",
        "however", "therefore", "thus", "hence", "otherwise",
    ],
    "junk_predicates": [
        "then", "part of", "lead to", "leads to",
        "result in", "results in", "associated with",
        "changes to", "change to",
    ],
    "junk_term_names": [
        "source", "file", "heroeshandbook",
        "the", "a", "an",
    ],
    "stop_words": [
        "you", "your", "this", "that", "these", "those", "they", "them", "their",
        "for", "some", "each", "all", "any", "both", "many", "most", "more",
        "when", "where", "with", "once", "since", "while", "after", "before",
        "there", "here", "however", "like", "one", "two", "see", "note",
        "will", "may", "can", "must", "would", "should", "could",
        "the gm", "gm", "also", "even", "only", "just", "very",
    ],
    "reject_fragments": [
        "alternatively", "otherwise", "compare", "the gm", "the gadgeteer",
        "the battlesuit", "the construct", "the crime fighter", "the elemental",
        "the energy controller", "the martial artist", "the mimic", "the mystic",
        "the paragon", "the powerhouse", "the psychic", "the shapeshifter",
        "the speedster", "the summoner", "the weapon master", "the weather controller",
    ],
}


def _load_block_list(workspace_root: "Path | None") -> dict:
    """Merge skill defaults with workspace solution/evidence/block_list.json (if it exists)."""
    merged: dict = {k: list(v) if isinstance(v, list) else v
                    for k, v in _SKILL_BLOCK_LIST.items()}
    if not workspace_root:
        return merged
    # Try solution/evidence/ first (preferred), fall back to evidence/ at workspace root
    for candidate in [
        workspace_root / "solution" / "evidence" / "block_list.json",
        workspace_root / "evidence" / "block_list.json",
    ]:
        if candidate.exists():
            path = candidate
            break
    else:
        return merged
    if not path.exists():
        return merged
    try:
        ws = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return merged
    for section in ("weak_object_tokens", "junk_predicates", "junk_term_names", "reject_fragments", "stop_words"):
        if section in ws:
            existing = set(merged.get(section, []))
            merged[section] = list(existing | {x.lower() for x in ws[section]})
    return merged


def _make_filters(block_list: dict) -> tuple[set, set, set, set, set]:
    """Return (weak_object_tokens, junk_predicates, junk_term_names, reject_fragments, stop_words) as sets."""
    return (
        set(block_list.get("weak_object_tokens", [])),
        set(block_list.get("junk_predicates", [])),
        {n.lower() for n in block_list.get("junk_term_names", [])},
        {f.lower() for f in block_list.get("reject_fragments", [])},
        {w.lower() for w in block_list.get("stop_words", [])},
    )


# Module-level sets (populated after workspace is known; defaults used until then)
_WEAK_OBJECT_TOKENS: set = set(_SKILL_BLOCK_LIST["weak_object_tokens"])
_JUNK_PREDICATES: set = set(_SKILL_BLOCK_LIST["junk_predicates"])
_JUNK_TERM_NAMES: set = set(_SKILL_BLOCK_LIST["junk_term_names"])
_REJECT_FRAGMENTS: set = set(_SKILL_BLOCK_LIST["reject_fragments"])
_STOP_WORDS: set = {w.lower() for w in _SKILL_BLOCK_LIST["stop_words"]}


def _init_filters(workspace_root: "Path | None") -> None:
    """Call once at startup to merge workspace block list into module-level sets."""
    global _WEAK_OBJECT_TOKENS, _JUNK_PREDICATES, _JUNK_TERM_NAMES, _REJECT_FRAGMENTS, _STOP_WORDS
    bl = _load_block_list(workspace_root)
    _WEAK_OBJECT_TOKENS, _JUNK_PREDICATES, _JUNK_TERM_NAMES, _REJECT_FRAGMENTS, _STOP_WORDS = _make_filters(bl)


_LEADING_ARTICLE_RE = re.compile(r"^(a|an|the)\s+", re.IGNORECASE)


def _strip_leading_article(obj: str) -> str:
    """Strip leading 'A', 'An', 'The' from an object value."""
    return _LEADING_ARTICLE_RE.sub("", obj).strip()


def _is_weak_object(obj: str) -> bool:
    cleaned = _strip_leading_article(obj)
    first = cleaned.split()[0].lower().rstrip(".,;:") if cleaned.strip() else ""
    return first in _WEAK_OBJECT_TOKENS or not cleaned.strip()


def _is_junk_object(obj: str) -> bool:
    """Reject objects that are table fragments or junk (too long, structural)."""
    if not obj or len(obj) > 50:
        return True
    lower = obj.lower()
    junk_patterns = ("per rank effects", "one of the following", "examples of", "ex- amples of", "when the critical hit")
    return any(p in lower for p in junk_patterns)


def _is_junk_term(name: str) -> bool:
    return name.strip().lower() in _JUNK_TERM_NAMES


def is_candidate_rule_prose(sentence: str) -> bool:
    """
    Structural gate: is this line candidate rule prose?
    Reject headings, chapter labels, table rows, archetype lists, prose fragments.
    """
    s = sentence.strip()
    if len(s) < 40:  # too short for meaningful rule prose (full clause)
        return False
    if s.lower().startswith("example"):
        return False
    if "file://" in s or "-->" in s or "section " in s.lower() and "|" in s:
        return False
    lower = s.lower()
    for pat in _REJECT_PATTERNS:
        if pat.search(s):
            return False
    if lower in _REJECT_FRAGMENTS or any(lower.startswith(f) for f in _REJECT_FRAGMENTS if len(f) > 10):
        return False
    if lower.startswith("the ") and len(s.split()) <= 4:  # "The GM", "The Gadgeteer"
        return False
    if lower.startswith("you ") or lower.startswith("you'll ") or lower.startswith("you're ") or lower.startswith("you've "):
        return False
    # Reject if mostly uppercase (heading)
    alpha = sum(1 for c in s if c.isalpha())
    caps = sum(1 for c in s if c.isupper())
    if alpha > 0 and caps / alpha > 0.7 and len(s) > 15:
        return False
    return True


CONDITIONAL_RE = re.compile(
    r"\b(if|when|unless|provided that|only if|except when|on success|on failure|must|may not|cannot|can't|required|requires)\b",
    re.IGNORECASE,
)
COMPARISON_RE = re.compile(
    r"(>=|<=|==|!=|>|<|vs\.?|versus|against|compared to|equal to|at least|at most|less than|greater than)",
    re.IGNORECASE,
)
RESULT_RE = re.compile(
    r"\b(then|result(?:s|ing)? in|causes?|produces?|leads? to|becomes?|changes? to|transitions? to)\b",
    re.IGNORECASE,
)
REL_HINT_RE = re.compile(
    r"\b(has|have|contains?|includes?|consists? of|uses?|requires?|depends on|references?|belongs to|associated with|part of|composed of|inherits from|extends|specializes)\b",
    re.IGNORECASE,
)
VARIATION_RE = re.compile(
    r"\b(type|mode|variant|option|modifier|alternative|alternate|branch|flavor|extension|parameter|selective|optional)\b",
    re.IGNORECASE,
)
STATE_RE = re.compile(
    r"\b(state|status|becomes?|changes? to|transitions? to|gains?|loses?|enters?|remains?)\b",
    re.IGNORECASE,
)

_MECHANICAL_SIGNALS = [CONDITIONAL_RE, COMPARISON_RE, RESULT_RE, REL_HINT_RE, STATE_RE, VARIATION_RE]


def is_mechanical_chunk(text: str) -> bool:
    """Skip chunks with no mechanical signals (conditionals, comparisons, results, relationships, states)."""
    return sum(1 for r in _MECHANICAL_SIGNALS if r.search(text)) >= 1


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []
    parts = re.split(r"(?<=[.!?;:])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def is_heading_like(term: str) -> bool:
    """Reject title-case terms that are headings, not domain concepts."""
    if not term or len(term) < 3:
        return True
    if "\n" in term:
        return True
    if term.isupper() and len(term) > 4:
        return True
    if term.upper().startswith("CHAPTER"):
        return True
    if re.match(r"^\d+\d+$", term.strip()):  # doubled page numbers e.g. "249249"
        return True
    words = term.split()
    if len(words) > 3:
        return True
    return False


def title_terms(text: str) -> list[str]:
    pats = re.findall(r"\b([A-Z][A-Za-z0-9]*(?:\s+[A-Z][A-Za-z0-9]*){0,4})\b", text)
    return [p.strip() for p in pats if len(p.strip()) > 2 and not is_heading_like(p.strip())]


def detect_term_candidates(text: str, alias_to_canonical: dict[str, str]) -> list[str]:
    found = []
    concepts, _ = matched_concepts(text, alias_to_canonical)
    found.extend(concepts)
    for t in title_terms(text):
        found.append(t)
    for m in re.findall(r'"([^"]{2,60})"', text):
        found.append(m.strip())
    for m in re.findall(r"\b([A-Za-z][A-Za-z0-9 _/\-]{2,40}):", text):
        found.append(m.strip())
    return uniq([t for t in found if t])

def looks_mechanical(sentence: str, alias_to_canonical: dict[str, str], guidance: dict[str, Any]) -> bool:
    concepts, _ = matched_concepts(sentence, alias_to_canonical)
    lower = sentence.lower()

    score = 0
    if concepts:
        score += 2
    if CONDITIONAL_RE.search(sentence):
        score += 2
    if COMPARISON_RE.search(sentence):
        score += 1
    if RESULT_RE.search(sentence):
        score += 1
    if REL_HINT_RE.search(sentence):
        score += 1
    if STATE_RE.search(sentence):
        score += 1
    if VARIATION_RE.search(sentence):
        score += 1
    for mech in guidance.get("priority_mechanisms", []):
        if mech.lower() in lower:
            score += 1
    for axis in guidance.get("variation_axes", []):
        if axis.lower() in lower:
            score += 1
    return score >= 2

def conf(base: float, concept_hits: int, chunk_sc: float) -> float:
    value = base + min(0.25, concept_hits * 0.08) + max(-0.15, min(0.15, chunk_sc / 25.0))
    return round(max(0.0, min(1.0, value)), 2)

def extract_terms(chunks, guidance, alias_to_canonical):
    counts = Counter()
    occs = defaultdict(list)
    for chunk in chunks:
        text = chunk["text"]
        cid = chunk["chunk_id"]
        if is_noise_chunk(text, guidance):
            continue
        terms = detect_term_candidates(text, alias_to_canonical)
        for term in terms:
            canonical = alias_to_canonical.get(norm(term), term)
            counts[canonical] += 1
            occs[canonical].append(cid)
    out = []
    for i, (term, count) in enumerate(counts.most_common()):
        if count < 2 and term not in guidance.get("priority_concepts", []):
            continue
        if is_heading_like(term):
            continue
        if _is_junk_term(term):
            continue
        if term.strip().lower() in _STOP_WORDS:
            continue
        out.append({
            "term_id": f"term_{i:04d}",
            "name": term,
            "aliases": guidance.get("concept_aliases", {}).get(term, []),
            "count": count,
            "occurrences": sorted(set(occs[term])),
        })
    return out

def extract_actions(chunks, guidance, alias_to_canonical):
    out = []
    for chunk in chunks:
        text = chunk["text"]
        cid = chunk["chunk_id"]
        score = chunk_score(text, guidance, alias_to_canonical)
        if is_noise_chunk(text, guidance):
            continue
        if is_toc_or_index_chunk(text):
            continue
        if not is_mechanical_chunk(text):
            continue
        priority_set = set(guidance.get("priority_concepts", []))
        for sent in split_sentences(text):
            if not is_candidate_rule_prose(sent):
                continue
            if not looks_mechanical(sent, alias_to_canonical, guidance):
                continue
            concepts, aliases = matched_concepts(sent, alias_to_canonical)
            term_candidates = detect_term_candidates(sent, alias_to_canonical)
            rel = REL_HINT_RE.search(sent)
            res = RESULT_RE.search(sent)

            if rel and len(term_candidates) >= 2:
                subject = alias_to_canonical.get(norm(term_candidates[0]), term_candidates[0])
                obj = _strip_leading_article(alias_to_canonical.get(norm(term_candidates[1]), term_candidates[1]))
                predicate = rel.group(1).lower()
                if subject not in priority_set and obj not in priority_set:
                    continue
                if _is_weak_object(obj) or _is_junk_object(obj) or predicate in _JUNK_PREDICATES:
                    continue
                out.append({
                    "action_id": f"act_{len(out):04d}",
                    "subject": subject,
                    "predicate": predicate,
                    "object": obj,
                    "source_chunk": cid,
                    "raw": sent,
                    "matched_concepts": concepts,
                    "matched_aliases": aliases,
                    "confidence": conf(0.55, len(concepts), score),
                })
                continue

            if res and len(term_candidates) >= 2:
                subject = alias_to_canonical.get(norm(term_candidates[0]), term_candidates[0])
                obj = _strip_leading_article(alias_to_canonical.get(norm(term_candidates[-1]), term_candidates[-1]))
                predicate = res.group(1).lower()
                if subject not in priority_set and obj not in priority_set:
                    continue
                if _is_weak_object(obj) or _is_junk_object(obj) or predicate in _JUNK_PREDICATES:
                    continue
                out.append({
                    "action_id": f"act_{len(out):04d}",
                    "subject": subject,
                    "predicate": predicate,
                    "object": obj,
                    "source_chunk": cid,
                    "raw": sent,
                    "matched_concepts": concepts,
                    "matched_aliases": aliases,
                    "confidence": conf(0.55, len(concepts), score),
                })
                continue

            if len(term_candidates) >= 2 and concepts and (
                REL_HINT_RE.search(sent) or RESULT_RE.search(sent) or COMPARISON_RE.search(sent)
            ):
                subject = alias_to_canonical.get(norm(term_candidates[0]), term_candidates[0])
                obj = _strip_leading_article(alias_to_canonical.get(norm(term_candidates[1]), term_candidates[1]))
                if subject not in priority_set and obj not in priority_set:
                    continue
                if _is_weak_object(obj) or _is_junk_object(obj):
                    continue
                out.append({
                    "action_id": f"act_{len(out):04d}",
                    "subject": subject,
                    "predicate": "interacts with",
                    "object": obj,
                    "source_chunk": cid,
                    "raw": sent,
                    "matched_concepts": concepts,
                    "matched_aliases": aliases,
                    "confidence": conf(0.50, len(concepts), score),
                })
    return uniq(out)

def extract_decisions(chunks, guidance, alias_to_canonical):
    out = []
    for chunk in chunks:
        text = chunk["text"]
        cid = chunk["chunk_id"]
        score = chunk_score(text, guidance, alias_to_canonical)
        if is_noise_chunk(text, guidance):
            continue
        if is_toc_or_index_chunk(text):
            continue
        if not is_mechanical_chunk(text):
            continue
        for sent in split_sentences(text):
            if not is_candidate_rule_prose(sent):
                continue
            if not CONDITIONAL_RE.search(sent):
                continue
            if not looks_mechanical(sent, alias_to_canonical, guidance):
                continue
            concepts, aliases = matched_concepts(sent, alias_to_canonical)
            if not concepts and not (COMPARISON_RE.search(sent) or RESULT_RE.search(sent)):
                continue
            m = CONDITIONAL_RE.search(sent)
            trigger = m.group(1).lower() if m else ""
            condition = sent[m.end():].strip() if m else sent
            if len(condition) < 30:
                continue
            if condition.split()[0].lower().rstrip(".,;:") in _WEAK_OBJECT_TOKENS:
                continue
            out.append({
                "decision_id": f"dec_{len(out):04d}",
                "trigger": trigger,
                "condition": condition,
                "source_chunk": cid,
                "raw": sent,
                "matched_concepts": concepts,
                "matched_aliases": aliases,
                "confidence": conf(0.60, len(concepts), score),
            })
    return uniq(out)

def extract_states(chunks, guidance, alias_to_canonical):
    out = []
    for chunk in chunks:
        text = chunk["text"]
        cid = chunk["chunk_id"]
        score = chunk_score(text, guidance, alias_to_canonical)
        if is_noise_chunk(text, guidance):
            continue
        if is_toc_or_index_chunk(text):
            continue
        if not is_mechanical_chunk(text):
            continue
        for sent in split_sentences(text):
            if not is_candidate_rule_prose(sent):
                continue
            if not STATE_RE.search(sent):
                continue
            if not looks_mechanical(sent, alias_to_canonical, guidance):
                continue
            concepts, aliases = matched_concepts(sent, alias_to_canonical)
            term_candidates = detect_term_candidates(sent, alias_to_canonical)
            if not term_candidates:
                continue
            entity = alias_to_canonical.get(norm(term_candidates[0]), term_candidates[0])
            out.append({
                "state_id": f"st_{len(out):04d}",
                "entity": entity,
                "state_description": sent,
                "source_chunk": cid,
                "raw": sent,
                "matched_concepts": concepts,
                "matched_aliases": aliases,
                "confidence": conf(0.55, len(concepts), score),
            })
    return uniq(out)

def extract_relationships(chunks, guidance, alias_to_canonical):
    out = []
    for chunk in chunks:
        text = chunk["text"]
        cid = chunk["chunk_id"]
        score = chunk_score(text, guidance, alias_to_canonical)
        if is_noise_chunk(text, guidance):
            continue
        if is_toc_or_index_chunk(text):
            continue
        if not is_mechanical_chunk(text):
            continue
        for sent in split_sentences(text):
            if not is_candidate_rule_prose(sent):
                continue
            if not REL_HINT_RE.search(sent):
                continue
            if not looks_mechanical(sent, alias_to_canonical, guidance):
                continue
            concepts, aliases = matched_concepts(sent, alias_to_canonical)
            term_candidates = detect_term_candidates(sent, alias_to_canonical)
            if len(term_candidates) < 2:
                continue
            rel = REL_HINT_RE.search(sent).group(1).lower()
            from_entity = alias_to_canonical.get(norm(term_candidates[0]), term_candidates[0])
            to_entity = _strip_leading_article(alias_to_canonical.get(norm(term_candidates[1]), term_candidates[1]))
            if _is_weak_object(to_entity) or rel in _JUNK_PREDICATES:
                continue
            out.append({
                "relationship_id": f"rel_{len(out):04d}",
                "from_entity": from_entity,
                "type": rel,
                "to_entity": to_entity,
                "source_chunk": cid,
                "raw": sent,
                "matched_concepts": concepts,
                "matched_aliases": aliases,
                "confidence": conf(0.60, len(concepts), score),
            })
    return uniq(out)

def extract_modifiers(chunks, guidance, alias_to_canonical):
    out = []
    axes = [a.lower() for a in guidance.get("variation_axes", [])]
    for chunk in chunks:
        text = chunk["text"]
        cid = chunk["chunk_id"]
        score = chunk_score(text, guidance, alias_to_canonical)
        if is_noise_chunk(text, guidance):
            continue
        if is_toc_or_index_chunk(text):
            continue
        if not is_mechanical_chunk(text):
            continue
        for sent in split_sentences(text):
            if not is_candidate_rule_prose(sent):
                continue
            lower = sent.lower()
            if not (VARIATION_RE.search(sent) or any(axis in lower for axis in axes)):
                continue
            if not looks_mechanical(sent, alias_to_canonical, guidance):
                continue
            concepts, aliases = matched_concepts(sent, alias_to_canonical)
            out.append({
                "modifier_id": f"mod_{len(out):04d}",
                "description": sent,
                "source_chunk": cid,
                "raw": sent,
                "matched_concepts": concepts,
                "matched_aliases": aliases,
                "confidence": conf(0.50, len(concepts), score),
            })
    return uniq(out)


def main():
    parser = argparse.ArgumentParser(description="Guided evidence extraction")
    parser.add_argument("--input", "-i", required=True, help="Path to rule_chunks.json")
    parser.add_argument("--guidance", "-g", required=True, help="Path to concept_guidance.json")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory")
    args = parser.parse_args()

    rule_path = Path(args.input)
    guidance_path = Path(args.guidance)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load and merge workspace block list (evidence/block_list.json)
    import sys as _sys
    _skill_dir = Path(__file__).resolve().parent.parent
    _sys.path.insert(0, str(_skill_dir / "scripts"))
    try:
        from _config import workspace_root as _ws_root
        _init_filters(_ws_root())
    except Exception:
        _init_filters(None)

    chunks_raw = load_json(rule_path)
    chunks = chunks_raw.get("rule_chunks") or chunks_raw.get("chunks") or [] if isinstance(chunks_raw, dict) else chunks_raw

    guidance = load_json(guidance_path)
    alias_to_canonical, _ = build_alias_index(guidance)

    terms = extract_terms(chunks, guidance, alias_to_canonical)
    actions = extract_actions(chunks, guidance, alias_to_canonical)
    decisions = extract_decisions(chunks, guidance, alias_to_canonical)
    states = extract_states(chunks, guidance, alias_to_canonical)
    relationships = extract_relationships(chunks, guidance, alias_to_canonical)
    modifiers = extract_modifiers(chunks, guidance, alias_to_canonical)

    dump_json(out_dir / "terms.json", terms)
    dump_json(out_dir / "actions.json", actions)
    dump_json(out_dir / "decisions.json", decisions)
    dump_json(out_dir / "states.json", states)
    dump_json(out_dir / "relationships.json", relationships)
    dump_json(out_dir / "modifiers.json", modifiers)

    print(
        f"Wrote {len(terms)} terms, {len(actions)} actions, {len(decisions)} decisions, "
        f"{len(states)} states, {len(relationships)} relationships, {len(modifiers)} modifiers to {out_dir}"
    )


if __name__ == "__main__":
    main()
