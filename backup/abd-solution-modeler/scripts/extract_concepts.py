#!/usr/bin/env python3
"""Phase 3: Extract concept signals from chunks (unguided).

Implements all 12 evidence-signal techniques from the evidence-signal-extraction design.
Runs extraction using extraction_config.json if present, else defaults.
Evidence speaks first; concepts follow.

Output: concept_signals/concept_signals.json + concept_signals/concept_signals.md (JSON + markdown render for human review)
"""
import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent

# --- Defaults (used when no extraction_config.json) ---

_DEFAULT_CONFIG = {
    "tf_weights": {
        "heading": 5,
        "table_header": 4,
        "definition_sentence": 3,
        "capitalized_noun": 2,
        "regular": 1,
        "bold_term": 3,
        "list_item_lead": 2,
    },
    "definition_patterns": [
        r"\b([A-Z][A-Za-z0-9]*(?:\s+[A-Z][A-Za-z0-9]*){0,3})\s+(?:is|represents|refers to|describes|means)\s+",
    ],
    "dependency_verbs": [
        "has", "have", "contains", "includes", "uses", "requires",
        "applies", "targets", "modifies", "affects",
    ],
    "np_mining": {
        "min_frequency": 2,
        "max_words": 4,
        "prioritize_compound": True,
    },
    "cooccurrence": {
        "window_size": "chunk",
        "min_count": 2,
        "max_edges": 300,
    },
    "table_mining": {
        "header_pattern": r"^\s*\|([^|]+)\|",
        "concept_columns": ["header", "row_label"],
        "ignore_patterns": ["page", "chapter", "table of contents"],
    },
    "enumeration_patterns": [
        r"types of ([A-Z][a-zA-Z ]+) include",
        r"([A-Z][a-zA-Z ]+) may be",
        r"([A-Z][a-zA-Z ]+) categories are",
        r"([A-Z][a-zA-Z ]+) can be one of",
        r"forms of ([A-Z][a-zA-Z ]+)",
    ],
    "contrast_patterns": [
        r"[Uu]nlike ([A-Z][a-zA-Z ]+),\s+([A-Z][a-zA-Z ]+)",
        r"([A-Z][a-zA-Z ]+) differs from ([A-Z][a-zA-Z ]+)",
        r"[Ww]hile ([A-Z][a-zA-Z ]+).*,\s+([A-Z][a-zA-Z ]+)",
        r"[Ii]n contrast to ([A-Z][a-zA-Z ]+)",
        r"[Aa]s opposed to ([A-Z][a-zA-Z ]+)",
    ],
    "actor_detection": {
        "actor_verbs": [
            "rolls", "selects", "chooses", "determines", "decides",
            "assigns", "activates", "initiates", "creates", "submits",
        ],
        "known_actors": [],
        "actor_noun_pattern": r"(character|player|user|system|gamemaster|admin|manager|operator)",
    },
    "topic_modeling": {
        "n_clusters": 8,
        "min_cluster_size": 3,
        "stop_words": [
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "to", "of", "and", "in", "for", "on", "with", "at", "by", "from",
            "or", "but", "not", "this", "that", "it", "its", "you", "your",
        ],
        "domain_stop_words": [],
    },
    "centrality": {
        "metric": "degree",
        "top_n": 20,
        "threshold": 0.02,
    },
    "verb_interaction": {
        "min_verb_frequency": 3,
        "verb_patterns": [],
        "exclude_verbs": [
            "is", "are", "was", "were", "has", "have", "had",
            "can", "may", "should", "would", "could", "will", "shall",
            "do", "does", "did", "been", "being", "be",
        ],
        "prioritize_domain_verbs": True,
    },
    "noise_filters": [
        "table of contents", "appendix", "index", "license",
        "copyright", "acknowledgments", "foreword", "preface",
    ],
}

# --- Helpers ---

def _load_json(path: Path) -> dict | list:
    if not path.exists():
        return {} if "config" in str(path) else []
    return json.loads(path.read_text(encoding="utf-8"))


def _load_chunks(context_path: Path) -> list[dict]:
    data = _load_json(context_path)
    if isinstance(data, list):
        return data
    return data.get("chunks", data.get("rule_chunks", []))


def _cfg(config: dict, key: str):
    """Get config value with fallback to defaults."""
    if key in config:
        return config[key]
    return _DEFAULT_CONFIG.get(key)


def _title_terms(text: str) -> list[str]:
    pats = re.findall(r"\b([A-Z][A-Za-z0-9]*(?:\s+[A-Z][A-Za-z0-9]*){0,4})\b", text)
    return [p.strip() for p in pats if 2 < len(p.strip()) < 50]


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"[.!?;]\s+", text) if len(s.strip()) > 10]


def _words(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z]+", text.lower())


def _is_noise(text: str, noise_filters: list[str]) -> bool:
    text_lower = text.lower()
    return any(nf in text_lower for nf in noise_filters)


def _is_exclamation_heavy(text: str, config: dict) -> bool:
    """Filter chunks where most sentences end with '!'. Returns False (no filter) by default."""
    return False


def _get_exclude_terms(config: dict) -> set[str]:
    """Terms to exclude (global_exclude.terms + all_caps_structural)."""
    ge = config.get("global_exclude", {})
    terms = set(t for t in ge.get("terms", []))
    terms.update(t for t in ge.get("all_caps_structural", []))
    return terms


def _get_allow_short_forms(config: dict) -> set[str]:
    """Short forms to keep despite exclusion rules."""
    return set(config.get("allow_short_forms", []))


def _is_excluded_term(term: str, config: dict) -> bool:
    """Exclude if in exclude list or all-caps structural; keep if in allow_short_forms."""
    allow = _get_allow_short_forms(config)
    if term in allow:
        return False
    exclude = _get_exclude_terms(config)
    return term in exclude


# --- Signal 1: TF + Structural Weighting ---

def _extract_term_candidates(chunks: list[dict], config: dict) -> list[dict]:
    weights = _cfg(config, "tf_weights")
    noise = _cfg(config, "noise_filters")
    heading_w = weights.get("heading", 5)
    table_header_w = weights.get("table_header", 4)
    def_sentence_w = weights.get("definition_sentence", 3)
    bold_w = weights.get("bold_term", 3)
    cap_noun_w = weights.get("capitalized_noun", 2)
    list_lead_w = weights.get("list_item_lead", 2)
    regular_w = weights.get("regular", 1)

    counts: Counter = Counter()
    weighted: dict[str, float] = defaultdict(float)
    chunk_ids: dict[str, set[str]] = defaultdict(set)

    for chunk in chunks:
        text = chunk.get("text", "")
        if _is_noise(text, noise) or _is_exclamation_heavy(text, config):
            continue
        cid = chunk.get("chunk_id", "")
        for line in text.split("\n"):
            stripped = line.strip()
            if not stripped:
                continue
            w = regular_w
            if stripped.startswith("#"):
                w = heading_w
            elif stripped.startswith("|"):
                w = table_header_w
            elif re.match(r"^[A-Z].*\b(is|represents|refers to|describes)\b", stripped):
                w = def_sentence_w
            elif stripped.startswith("- ") or stripped.startswith("* "):
                w = list_lead_w

            for bold_m in re.finditer(r"\*\*([A-Z][A-Za-z0-9 ]+)\*\*", line):
                term = bold_m.group(1).strip()
                if len(term) > 2:
                    counts[term] += 1
                    weighted[term] += bold_w
                    if cid:
                        chunk_ids[term].add(cid)

            for term in _title_terms(line):
                key = term.strip()
                if len(key) > 2:
                    counts[key] += 1
                    weighted[key] += w
                    if cid:
                        chunk_ids[key].add(cid)

    out = []
    for i, (term, count) in enumerate(counts.most_common(200)):
        if count < 2:
            continue
        if _is_excluded_term(term, config):
            continue
        entry: dict = {
            "term_id": f"term_{i:04d}",
            "name": term,
            "count": count,
            "weighted_score": round(weighted[term], 2),
        }
        if chunk_ids.get(term):
            entry["chunk_ids"] = sorted(chunk_ids[term])
        out.append(entry)
    return out


# --- Signal 2: Definition Sentence Detection ---

def _extract_definition_candidates(chunks: list[dict], config: dict) -> list[dict]:
    patterns = _cfg(config, "definition_patterns")
    noise = _cfg(config, "noise_filters")
    def_filters = config.get("definition_filters", {})
    min_words = def_filters.get("min_concept_word_count", 1)
    min_raw = def_filters.get("min_raw_length", 0)
    exclude_concepts = set(c.lower() for c in def_filters.get("exclude_concepts", []))
    compiled = [re.compile(p) for p in patterns]
    out = []
    for chunk in chunks:
        text = chunk.get("text", "")
        if _is_noise(text, noise) or _is_exclamation_heavy(text, config):
            continue
        cid = chunk.get("chunk_id", "")
        for pat in compiled:
            for m in pat.finditer(text):
                concept = m.group(1).strip()
                raw = text[max(0, m.start() - 20): m.end() + 80]
                if len(concept) <= 2:
                    continue
                if _is_excluded_term(concept, config):
                    continue
                if concept.lower() in exclude_concepts:
                    continue
                if not any(ch.isupper() for ch in concept):
                    continue
                if len(concept.split()) < min_words:
                    continue
                if len(raw) < min_raw:
                    continue
                out.append({
                    "definition_id": f"def_{len(out):04d}",
                    "concept": concept,
                    "source_chunk": cid,
                    "raw": raw,
                })
    return out


# --- Signal 3: Dependency Pattern Mining (SVO) ---

def _extract_dependency_actions(chunks: list[dict], config: dict) -> list[dict]:
    verbs = _cfg(config, "dependency_verbs")
    noise = _cfg(config, "noise_filters")
    verb_re = re.compile(r"\b(" + "|".join(re.escape(v) for v in verbs) + r")\b", re.IGNORECASE)
    out = []
    for chunk in chunks:
        text = chunk.get("text", "")
        if _is_noise(text, noise) or _is_exclamation_heavy(text, config):
            continue
        cid = chunk.get("chunk_id", "")
        for sent in _sentences(text):
            m = verb_re.search(sent)
            if not m or len(sent) < 40:
                continue
            before = sent[:m.start()]
            after = sent[m.end():]
            before_terms = _title_terms(before)
            after_terms = _title_terms(after)
            if not before_terms or not after_terms:
                continue
            subj, obj = before_terms[-1], after_terms[0]
            if _is_excluded_term(subj, config) or _is_excluded_term(obj, config):
                continue
            pred = m.group(1).lower()
            out.append({
                "dep_id": f"dep_{len(out):04d}",
                "subject": subj,
                "predicate": pred,
                "object": obj,
                "source_chunk": cid,
                "raw": sent[:200],
            })
    return out


# --- Signal 4: Noun Phrase Mining ---

def _extract_np_candidates(chunks: list[dict], config: dict) -> list[dict]:
    np_cfg = _cfg(config, "np_mining")
    noise = _cfg(config, "noise_filters")
    min_freq = np_cfg.get("min_frequency", 2)
    max_words = np_cfg.get("max_words", 4)
    np_re = re.compile(
        r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1," + str(max_words - 1) + r"})\b"
    )

    counts: Counter = Counter()
    chunk_ids: dict[str, set[str]] = defaultdict(set)
    for chunk in chunks:
        text = chunk.get("text", "")
        if _is_noise(text, noise) or _is_exclamation_heavy(text, config):
            continue
        cid = chunk.get("chunk_id", "")
        for m in np_re.finditer(text):
            phrase = m.group(1).strip()
            if len(phrase) > 4:
                counts[phrase] += 1
                if cid:
                    chunk_ids[phrase].add(cid)

    exclude_head = set(np_cfg.get("exclude_head_nouns", []))
    out = []
    for i, (phrase, count) in enumerate(counts.most_common(150)):
        if count < min_freq:
            continue
        words = phrase.split()
        head = words[-1] if words else ""
        if head in exclude_head:
            continue
        entry: dict = {
            "np_id": f"np_{i:04d}",
            "phrase": phrase,
            "word_count": len(words),
            "count": count,
            "head_noun": head,
        }
        if chunk_ids.get(phrase):
            entry["chunk_ids"] = sorted(chunk_ids[phrase])
        out.append(entry)
    return out


# --- Signal 5: Co-occurrence Graphs ---

def _extract_cooccurrence(chunks: list[dict], term_candidates: list[dict], config: dict) -> dict:
    co_cfg = _cfg(config, "cooccurrence")
    noise = _cfg(config, "noise_filters")
    min_count = co_cfg.get("min_count", 2)
    max_edges = co_cfg.get("max_edges", 300)

    term_set = {t["name"] for t in term_candidates}
    pairs: Counter = Counter()
    for chunk in chunks:
        text = chunk.get("text", "")
        if _is_noise(text, noise) or _is_exclamation_heavy(text, config):
            continue
        terms_in = [t for t in _title_terms(text) if t in term_set]
        seen = []
        for t in terms_in:
            if t not in seen:
                seen.append(t)
        for i, a in enumerate(seen):
            for b in seen[i + 1:]:
                if a != b:
                    key = (min(a, b), max(a, b))
                    pairs[key] += 1

    edges = [
        {"from": a, "to": b, "count": c}
        for (a, b), c in pairs.most_common(max_edges)
        if c >= min_count
    ]
    return {"edges": edges, "node_count": len(term_set)}


# --- Signal 6: Table Mining ---

def _extract_table_vocabularies(chunks: list[dict], config: dict) -> list[dict]:
    tbl_cfg = _cfg(config, "table_mining")
    noise = _cfg(config, "noise_filters")
    header_pat = re.compile(tbl_cfg.get("header_pattern", r"^\s*\|([^|]+)\|"), re.MULTILINE)
    ignore = [p.lower() for p in tbl_cfg.get("ignore_patterns", [])]

    out = []
    for chunk in chunks:
        text = chunk.get("text", "")
        if _is_noise(text, noise) or _is_exclamation_heavy(text, config):
            continue
        cid = chunk.get("chunk_id", "")
        for m in header_pat.finditer(text):
            raw_headers = m.group(0)
            headers = [h.strip() for h in raw_headers.split("|") if h.strip()]
            headers = [h for h in headers if not any(ig in h.lower() for ig in ignore)]
            if headers and not all(c == "-" or c == ":" for h in headers for c in h):
                out.append({
                    "table_id": f"tbl_{len(out):04d}",
                    "headers": headers,
                    "source_chunk": cid,
                })
    return out


# --- Signal 7: Enumeration Pattern Detection ---

def _extract_enumeration_candidates(chunks: list[dict], config: dict) -> list[dict]:
    patterns = _cfg(config, "enumeration_patterns")
    noise = _cfg(config, "noise_filters")
    enum_filters = config.get("enumeration_filters", {})
    min_parent_words = enum_filters.get("min_parent_word_count", 1)
    min_children = enum_filters.get("min_children_count", 1)
    exclude_starts = enum_filters.get("exclude_parent_starts", [])
    compiled = [re.compile(p, re.IGNORECASE) for p in patterns]
    out = []
    for chunk in chunks:
        text = chunk.get("text", "")
        if _is_noise(text, noise) or _is_exclamation_heavy(text, config):
            continue
        cid = chunk.get("chunk_id", "")
        for pat in compiled:
            for m in pat.finditer(text):
                parent = m.group(1).strip()
                if len(parent.split()) < min_parent_words:
                    continue
                if any(parent.startswith(s) for s in exclude_starts):
                    continue
                after = text[m.end(): m.end() + 200]
                children = [c.strip() for c in re.split(r"[,;]|\band\b", after) if c.strip()]
                children = [c for c in children[:10] if len(c) > 1 and len(c) < 50]
                if len(children) < min_children:
                    continue
                if parent and children:
                    out.append({
                        "enum_id": f"enum_{len(out):04d}",
                        "parent_concept": parent,
                        "children": children,
                        "source_chunk": cid,
                        "raw": text[max(0, m.start() - 10): m.end() + 100],
                    })
    return out


# --- Signal 8: Contrast Detection ---

def _extract_contrast_candidates(chunks: list[dict], config: dict) -> list[dict]:
    patterns = _cfg(config, "contrast_patterns")
    noise = _cfg(config, "noise_filters")
    compiled = [re.compile(p) for p in patterns]
    out = []
    for chunk in chunks:
        text = chunk.get("text", "")
        if _is_noise(text, noise) or _is_exclamation_heavy(text, config):
            continue
        cid = chunk.get("chunk_id", "")
        for pat in compiled:
            for m in pat.finditer(text):
                groups = [g.strip() for g in m.groups() if g and g.strip()]
                groups = [g for g in groups if not _is_excluded_term(g, config)]
                if groups:
                    out.append({
                        "contrast_id": f"con_{len(out):04d}",
                        "concepts": groups,
                        "source_chunk": cid,
                        "raw": text[max(0, m.start() - 20): m.end() + 80],
                    })
    return out


# --- Signal 9: Actor Detection ---

def _extract_actor_candidates(chunks: list[dict], config: dict) -> list[dict]:
    actor_cfg = _cfg(config, "actor_detection")
    noise = _cfg(config, "noise_filters")
    actor_verbs = actor_cfg.get("actor_verbs", [])
    known = actor_cfg.get("known_actors", [])
    known_lower = {k.lower() for k in known}
    noun_pat = re.compile(actor_cfg.get("actor_noun_pattern", ""), re.IGNORECASE)
    verb_re = re.compile(r"\b(" + "|".join(re.escape(v) for v in actor_verbs) + r")\b", re.IGNORECASE) if actor_verbs else None

    actor_counts: Counter = Counter()
    actor_actions: dict[str, list[str]] = defaultdict(list)

    for chunk in chunks:
        text = chunk.get("text", "")
        if _is_noise(text, noise) or _is_exclamation_heavy(text, config):
            continue
        for sent in _sentences(text):
            for nm in noun_pat.finditer(sent):
                actor = nm.group(1).strip().title()
                actor_counts[actor] += 1
            if verb_re:
                for vm in verb_re.finditer(sent):
                    verb = vm.group(1).lower()
                    before = sent[:vm.start()]
                    before_terms = _title_terms(before)
                    if before_terms:
                        actor = before_terms[-1]
                        actor_lower = actor.lower()
                        if actor_lower not in known_lower and not noun_pat.search(actor):
                            continue
                        actor_counts[actor] += 1
                        actor_actions[actor].append(verb)

    for a in known:
        actor_counts[a] += 0

    exclude_actors = {a.lower() for a in actor_cfg.get("exclude_actors", [])}
    out = []
    for i, (actor, count) in enumerate(actor_counts.most_common(30)):
        if count < 1:
            continue
        if actor.lower() in exclude_actors:
            continue
        out.append({
            "actor_id": f"actor_{i:04d}",
            "name": actor,
            "count": count,
            "sample_actions": list(set(actor_actions.get(actor, [])))[:5],
        })
    return out


# --- Signal 10: Topic Modeling (simple TF-based clustering) ---

def _extract_topic_clusters(chunks: list[dict], config: dict) -> list[dict]:
    """Lightweight topic clustering using term co-occurrence without external deps."""
    topic_cfg = _cfg(config, "topic_modeling")
    noise = _cfg(config, "noise_filters")
    n_clusters = topic_cfg.get("n_clusters", 8)
    stop = set(topic_cfg.get("stop_words", []) + topic_cfg.get("domain_stop_words", []))

    chunk_terms: list[list[str]] = []
    for chunk in chunks:
        text = chunk.get("text", "")
        if _is_noise(text, noise) or _is_exclamation_heavy(text, config):
            continue
        title_terms = [t.lower() for t in _title_terms(text)]
        terms = [t for t in title_terms if t not in stop and not _is_excluded_term(t.title(), config)]
        if terms:
            chunk_terms.append(terms)

    if not chunk_terms:
        return []

    all_terms = Counter()
    for terms in chunk_terms:
        all_terms.update(set(terms))
    top_terms = [t for t, _ in all_terms.most_common(n_clusters * 5)]

    clusters: dict[str, list[str]] = defaultdict(list)
    for terms in chunk_terms:
        best_topic = None
        best_count = 0
        for tt in top_terms[:n_clusters]:
            c = terms.count(tt)
            if c > best_count:
                best_count = c
                best_topic = tt
        if best_topic:
            representative = Counter(terms).most_common(5)
            clusters[best_topic].extend([t for t, _ in representative])

    out = []
    for i, (topic, members) in enumerate(clusters.items()):
        unique = list(dict.fromkeys(members))[:10]
        out.append({
            "cluster_id": f"topic_{i:04d}",
            "topic_term": topic,
            "representative_terms": unique,
            "chunk_count": sum(1 for terms in chunk_terms if topic in terms),
        })
    return out[:n_clusters]


# --- Signal 11: Graph Centrality ---

def _extract_centrality_scores(cooccurrence: dict, dependency_actions: list[dict], config: dict) -> list[dict]:
    cent_cfg = _cfg(config, "centrality")
    top_n = cent_cfg.get("top_n", 20)

    degree: Counter = Counter()

    for edge in cooccurrence.get("edges", []):
        w = edge.get("count", 1)
        a, b = edge.get("from", ""), edge.get("to", "")
        if a and not _is_excluded_term(a, config):
            degree[a] += w
        if b and not _is_excluded_term(b, config):
            degree[b] += w

    for dep in dependency_actions:
        subj = dep.get("subject", "")
        obj = dep.get("object", "")
        if subj and not _is_excluded_term(subj, config):
            degree[subj] += 2
        if obj and not _is_excluded_term(obj, config):
            degree[obj] += 2

    total = sum(degree.values()) or 1
    out = []
    for i, (node, deg) in enumerate(degree.most_common(top_n)):
        if _is_excluded_term(node, config):
            continue
        out.append({
            "rank": i + 1,
            "concept": node,
            "degree": deg,
            "normalized": round(deg / total, 4),
        })
    return out[:top_n]


# --- Signal 12: Verb-Centered Interaction Graph ---

def _extract_verb_interaction_graph(chunks: list[dict], config: dict) -> dict:
    verb_cfg = _cfg(config, "verb_interaction")
    noise = _cfg(config, "noise_filters")
    min_freq = verb_cfg.get("min_verb_frequency", 3)
    exclude = set(verb_cfg.get("exclude_verbs", []))
    extra_patterns = verb_cfg.get("verb_patterns", [])
    allowed_verbs = set(v.lower() for v in config.get("dependency_verbs", []))
    for pattern in extra_patterns:
        parts = pattern.split()
        if len(parts) >= 2 and parts[1].lower() not in {"x", "y"}:
            allowed_verbs.add(parts[1].lower())
    verb_re = re.compile(r"\b([a-z]{3,}(?:s|es|ed|ing)?)\b")
    interactions: list[dict] = []
    verb_counts: Counter = Counter()
    concept_verb: dict[str, Counter] = defaultdict(Counter)

    for chunk in chunks:
        text = chunk.get("text", "")
        if _is_noise(text, noise) or _is_exclamation_heavy(text, config):
            continue
        cid = chunk.get("chunk_id", "")
        for sent in _sentences(text):
            terms = _title_terms(sent)
            if len(terms) < 1:
                continue
            verbs_found = [
                m.group(1) for m in verb_re.finditer(sent.lower())
                if m.group(1) not in exclude and (not allowed_verbs or m.group(1) in allowed_verbs)
            ]
            for v in verbs_found:
                verb_counts[v] += 1
                for t in terms:
                    concept_verb[t][v] += 1

            if len(terms) >= 2 and verbs_found:
                interactions.append({
                    "subject": terms[0],
                    "verb": verbs_found[0],
                    "object": terms[1] if len(terms) > 1 else "",
                    "source_chunk": cid,
                })

    freq_verbs = [v for v, c in verb_counts.most_common(50) if c >= min_freq]

    exclude_concepts = set(verb_cfg.get("exclude_concepts", []))
    concept_scores: Counter = Counter()
    for concept, verbs in concept_verb.items():
        if concept in exclude_concepts or _is_excluded_term(concept, config):
            continue
        score = sum(c for v, c in verbs.items() if v in freq_verbs)
        if score > 0:
            concept_scores[concept] = score

    return {
        "top_verbs": freq_verbs[:30],
        "concept_verb_scores": [
            {"concept": c, "score": s}
            for c, s in concept_scores.most_common(30)
        ],
        "sample_interactions": interactions[:100],
    }


# --- Markdown render for human review ---

def _sanitize(s: str) -> str:
    """Normalize newlines for markdown display."""
    return (s or "").replace("\n", " ").strip()


def _render_concept_signals_md(combined: dict) -> str:
    """Render concept_signals JSON to markdown: full spec-compliant output, no truncation."""
    lines = [
        "# Concept Signals",
        "",
        "Full render of `concept_signals.json`. All 12 signals with complete content.",
        "",
    ]

    # noise_filters (if present)
    noise = combined.get("noise_filters", [])
    if noise:
        lines.extend(["## noise_filters", ""])
        lines.append(", ".join(str(x) for x in noise))
        lines.append("")
        lines.append("---")
        lines.append("")

    # 1. tf_weights — full table with term_id, name, count, weighted_score
    tf = combined.get("tf_weights", [])
    lines.extend(["## 1. tf_weights", "", f"*{len(tf)} terms*", ""])
    if tf:
        lines.extend(["| term_id | name | count | weighted_score |", "|---------|------|-------|----------------|"])
        for t in tf:
            lines.append(f"| {t.get('term_id', '')} | {t.get('name', '')} | {t.get('count', 0)} | {t.get('weighted_score', 0)} |")
    lines.append("")

    # 2. definition_patterns — full: definition_id, concept, raw, source_chunk
    defs = combined.get("definition_patterns", [])
    lines.extend(["## 2. definition_patterns", "", f"*{len(defs)} definitions*", ""])
    if defs:
        for d in defs:
            def_id = d.get("definition_id", "")
            concept = _sanitize(d.get("concept", ""))
            raw = _sanitize(d.get("raw", ""))
            chunk = d.get("source_chunk", "")
            lines.append(f"- **{def_id}** | concept: {concept} | chunk: {chunk}")
            lines.append(f"  > {raw}")
        lines.append("")
    else:
        lines.append("—")
        lines.append("")

    # 3. dependency_verbs — full: dep_id, subject predicate object, raw
    deps = combined.get("dependency_verbs", [])
    lines.extend(["## 3. dependency_verbs", "", f"*{len(deps)} dependencies*", ""])
    if deps:
        for d in deps:
            dep_id = d.get("dep_id", "")
            subj = d.get("subject", "")
            pred = d.get("predicate", "")
            obj = d.get("object", "")
            raw = _sanitize(d.get("raw", ""))
            lines.append(f"- **{dep_id}** {subj} **{pred}** {obj}")
            lines.append(f"  > {raw}")
        lines.append("")
    else:
        lines.append("—")
        lines.append("")

    # 4. np_mining — full
    nps = combined.get("np_mining", [])
    lines.extend(["## 4. np_mining", "", f"*{len(nps)} noun phrases*", ""])
    if nps:
        lines.extend(["| phrase | count | head_noun |", "|--------|-------|-----------|"])
        for n in nps:
            lines.append(f"| {n.get('phrase', '')} | {n.get('count', 0)} | {n.get('head_noun', '')} |")
    lines.append("")

    # 5. cooccurrence — full edges
    co = combined.get("cooccurrence", {})
    edges = co.get("edges", [])
    lines.extend(["## 5. cooccurrence", "", f"*{co.get('node_count', 0)} nodes, {len(edges)} edges*", ""])
    if edges:
        lines.extend(["| from | to | count |", "|------|-----|-------|"])
        for e in edges:
            lines.append(f"| {e.get('from', '')} | {e.get('to', '')} | {e.get('count', 0)} |")
    lines.append("")

    # 6. table_mining — full
    tbls = combined.get("table_mining", [])
    lines.extend(["## 6. table_mining", "", f"*{len(tbls)} tables*", ""])
    if tbls:
        for t in tbls:
            headers = t.get("headers", [])
            lines.append(f"- {', '.join(str(h) for h in headers)}")
    else:
        lines.append("—")
    lines.append("")

    # 7. enumeration_patterns — full
    enums = combined.get("enumeration_patterns", [])
    lines.extend(["## 7. enumeration_patterns", "", f"*{len(enums)} enumerations*", ""])
    if enums:
        for e in enums:
            parent = e.get("parent_concept", "")
            children = e.get("children", [])
            lines.append(f"- **{parent}**: {', '.join(str(c) for c in children)}")
    lines.append("")

    # 8. contrast_patterns — full
    contrasts = combined.get("contrast_patterns", [])
    lines.extend(["## 8. contrast_patterns", "", f"*{len(contrasts)} contrasts*", ""])
    if contrasts:
        for c in contrasts:
            concepts = c.get("concepts", [])
            raw = _sanitize(c.get("raw", ""))
            lines.append(f"- {', '.join(str(x) for x in concepts)}")
            if raw:
                lines.append(f"  > {raw}")
    lines.append("")

    # 9. actor_detection — full
    actors = combined.get("actor_detection", [])
    lines.extend(["## 9. actor_detection", "", f"*{len(actors)} actors*", ""])
    if actors:
        for a in actors:
            name = a.get("name", "")
            count = a.get("count", 0)
            lines.append(f"- {name} (count: {count})")
    lines.append("")

    # 10. topic_modeling — full
    topics = combined.get("topic_modeling", [])
    lines.extend(["## 10. topic_modeling", "", f"*{len(topics)} clusters*", ""])
    if topics:
        for t in topics:
            terms = t.get("terms", [])
            lines.append(f"- {', '.join(str(x) for x in terms)}")
    lines.append("")

    # 11. centrality — full
    cent = combined.get("centrality", [])
    lines.extend(["## 11. centrality", "", f"*{len(cent)} ranked concepts*", ""])
    if cent:
        lines.extend(["| rank | concept | degree | normalized |", "|------|---------|--------|------------|"])
        for c in cent:
            lines.append(f"| {c.get('rank', 0)} | {c.get('concept', '')} | {c.get('degree', 0)} | {c.get('normalized', 0)} |")
    lines.append("")

    # 12. verb_interaction — full
    vi = combined.get("verb_interaction", {})
    top_verbs = vi.get("top_verbs", [])
    concept_scores = vi.get("concept_verb_scores", [])
    sample = vi.get("sample_interactions", [])
    lines.extend([
        "## 12. verb_interaction", "",
        f"*top_verbs: {len(top_verbs)}, concept_verb_scores: {len(concept_scores)}, sample_interactions: {len(sample)}*", "",
    ])
    lines.append("**top_verbs:**")
    for v in top_verbs:
        lines.append(f"- {v}")
    lines.append("")
    lines.append("**concept_verb_scores:**")
    if concept_scores:
        lines.extend(["| concept | score |", "|---------|-------|"])
        for s in concept_scores:
            lines.append(f"| {s.get('concept', '')} | {s.get('score', 0)} |")
    lines.append("")
    lines.append("**sample_interactions:**")
    for i in sample:
        lines.append(f"- {i.get('subject', '')} **{i.get('verb', '')}** {i.get('object', '')}")
    lines.append("")

    return "\n".join(lines)


# --- Main ---

def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 3: Extract concept signals (all 12 techniques)")
    parser.add_argument("--input", "-i", help="Path to context_chunks.json")
    parser.add_argument("--config", "-c", help="Path to extraction_config.json (optional)")
    parser.add_argument("--output-dir", "-o", help="Output directory")
    parser.add_argument("--render-only", action="store_true", help="Re-render concept_signals.md from existing JSON")
    args = parser.parse_args()

    if args.render_only:
        out_dir = Path(args.output_dir or ".").resolve()
        json_path = out_dir / "concept_signals.json"
        if not json_path.exists():
            print(f"concept_signals.json not found: {json_path}", file=__import__("sys").stderr)
            __import__("sys").exit(1)
        combined = json.loads(json_path.read_text(encoding="utf-8"))
        md_path = out_dir / "concept_signals.md"
        md_path.write_text(_render_concept_signals_md(combined), encoding="utf-8")
        print(f"Rendered concept_signals.md -> {md_path}")
        return

    in_path = Path(args.input).resolve()
    out_dir = Path(args.output_dir).resolve()
    config_path = Path(args.config).resolve() if args.config else None

    config = _load_json(config_path) if config_path and config_path.exists() else {}

    chunks = _load_chunks(in_path)
    if not chunks:
        print("No chunks found.", file=__import__("sys").stderr)
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    # Signal 1
    term_candidates = _extract_term_candidates(chunks, config)
    # Signal 2
    definition_candidates = _extract_definition_candidates(chunks, config)
    # Signal 3
    dependency_actions = _extract_dependency_actions(chunks, config)
    # Signal 4
    np_candidates = _extract_np_candidates(chunks, config)
    # Signal 5
    cooccurrence_graph = _extract_cooccurrence(chunks, term_candidates, config)
    # Signal 6
    table_vocabularies = _extract_table_vocabularies(chunks, config)
    # Signal 7
    enumeration_candidates = _extract_enumeration_candidates(chunks, config)
    # Signal 8
    contrast_candidates = _extract_contrast_candidates(chunks, config)
    # Signal 9
    actor_candidates = _extract_actor_candidates(chunks, config)
    # Signal 10
    topic_clusters = _extract_topic_clusters(chunks, config)
    # Signal 11
    centrality_scores = _extract_centrality_scores(cooccurrence_graph, dependency_actions, config)
    # Signal 12
    verb_interaction_graph = _extract_verb_interaction_graph(chunks, config)

    combined = {
        "tf_weights": term_candidates,
        "definition_patterns": definition_candidates,
        "dependency_verbs": dependency_actions,
        "np_mining": np_candidates,
        "cooccurrence": cooccurrence_graph,
        "table_mining": table_vocabularies,
        "enumeration_patterns": enumeration_candidates,
        "contrast_patterns": contrast_candidates,
        "actor_detection": actor_candidates,
        "topic_modeling": topic_clusters,
        "centrality": centrality_scores,
        "verb_interaction": verb_interaction_graph,
        "noise_filters": _cfg(config, "noise_filters"),
    }

    (out_dir / "concept_signals.json").write_text(
        json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (out_dir / "concept_signals.md").write_text(
        _render_concept_signals_md(combined), encoding="utf-8"
    )

    print(
        f"Extracted 12 signals -> {out_dir / 'concept_signals.json'}:\n"
        f"  tf_weights:          {len(term_candidates)} terms\n"
        f"  definition_patterns: {len(definition_candidates)} definitions\n"
        f"  dependency_verbs:    {len(dependency_actions)} dependencies\n"
        f"  np_mining:           {len(np_candidates)} NPs\n"
        f"  cooccurrence:        {len(cooccurrence_graph.get('edges', []))} edges\n"
        f"  table_mining:        {len(table_vocabularies)} tables\n"
        f"  enumeration_patterns:{len(enumeration_candidates)} enumerations\n"
        f"  contrast_patterns:   {len(contrast_candidates)} contrasts\n"
        f"  actor_detection:     {len(actor_candidates)} actors\n"
        f"  topic_modeling:      {len(topic_clusters)} clusters\n"
        f"  centrality:          {len(centrality_scores)} ranked\n"
        f"  verb_interaction:    {len(verb_interaction_graph.get('top_verbs', []))} verbs, "
        f"{len(verb_interaction_graph.get('concept_verb_scores', []))} concepts"
    )
    print(f"Markdown render -> {out_dir / 'concept_signals.md'}")


if __name__ == "__main__":
    main()
