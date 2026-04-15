#!/usr/bin/env python3
"""Phase 4: Build hypothesis.json from concept signals (concepts + registries format).

Reads concept_signals/concept_signals.json (single combined file from Phase 3)
and produces hypothesis.json with the concept-anchored structure:
- concepts: {ConceptName: {term_ids, performs, receives, states, decisions, relationships}}
- registries: {actions, decisions, states, relationships}
- concept_guidance: {priority_concepts, concept_aliases, ...} for Phase 5 evidence extraction

Phase 3 does not extract decisions, states, or relationships — those are left empty.
Phase 5 (evidence_extraction_guided) will extract them from chunks using concept_guidance.
"""
import argparse
import json
import re
import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent

# Noise terms to exclude from concepts (section headers, junk). Domain-agnostic only.
# Excludes "powers", "abilities", "ranks" — those are often core domain concepts (e.g. M&M Powers).
# Domain-specific junk (e.g. "POWERS EXTRAS", "SECRET ORIGINS DEFENSES Once") goes in
# extraction_config.noise_filters or concept_guidance.noise_filters.
_NOISE_TERMS = {
    "chapter", "basics", "source", "file",
}

# Discourse adverbs and common non-concept words (stop words)
_DISCOURSE_AND_JUNK = {
    "actually", "essentially", "basically", "typically", "generally",
    "simply", "really", "whenever", "when", "what", "for", "they", "this",
    "one", "like", "all", "see", "activa",  # truncation of Activation
    "you", "your",  # second-person pronouns
    "he", "she", "we", "do", "does", "etc", "and", "or", "the", "a", "an",
    "it", "is", "as", "to", "of", "in", "on", "at", "its", "him", "her",
    "us", "them", "if", "but", "so", "be", "been", "being", "have", "has",
    "had", "can", "may", "will", "would", "could", "should", "must",
    "doctor", "dr", "mr", "mrs", "ms", "miss", "mister", "mistress",
    "thus", "that", "too", "while", "whatever",
    "whether", "whe",  # whe = truncation
    "what", "who", "which", "where", "why", "how",
    "for example", "for instance", "such as", "as well as",
}


def _is_noise_concept(name: str, noise_set: set[str] | None = None) -> bool:
    """Return True if concept name is junk (discourse, fragment, truncation)."""
    if not name or len(name) < 2 or len(name) > 80:
        return True
    # More than 3 words = section-header truncation (e.g. "HEROES Although Emerald City")
    if len(name.split()) > 3:
        return True
    n = name.strip()
    low = n.lower()
    terms = noise_set if noise_set is not None else _NOISE_TERMS
    if low in terms or low in _DISCOURSE_AND_JUNK:
        return True
    # Recurring junk: "+15 for a", "DC 5", "DC DC", "for a", "for the", "and the"
    if re.match(r"^\+?\d+\s+for\s+a\b", low):
        return True
    if re.match(r"^dc\s+dc$", low) or re.match(r"^dc\s+\d+$", low):
        return True
    # Discourse phrases: "for example", "for instance", "such as"
    if low in ("for example", "for instance", "such as", "as well as"):
        return True
    # "If X" / "How X" / "When X" / "While X" / "Whatever X" etc — conjunction/question-word fragments
    if re.match(r"^(if|how|when|what|who|where|why|which|whether|while|whatever)\s+", low):
        return True
    # Sentence fragments: "A Weaken", "A Summoner", "A Variable" — article + noun
    if re.match(r"^A\s+\w", n):
        return True
    if re.match(r"^An\s+\w", n):
        return True
    # "The Xxxx" — definite article + noun
    if re.match(r"^The\s+\w", n):
        return True
    # Sentence fragments: ends with " You", " The", " This"
    if n.endswith(" You") or n.endswith(" The") or n.endswith(" This"):
        return True
    # All-caps header fragments: "RANKED You", "RANKED TEAMWORK GENERAL You"
    if re.match(r"^[A-Z][A-Z0-9\s]+You$", n):
        return True
    return False


def _load_noise_filters(out_path: Path) -> set[str]:
    """Merge noise_filters from _NOISE_TERMS, extraction_config, and workspace concept_guidance."""
    merged = set(_NOISE_TERMS)
    # extraction_config (Phase 2 output, same dir as hypothesis)
    ext_cfg_path = out_path.parent / "extraction_config.json"
    if ext_cfg_path.exists():
        try:
            cfg = json.loads(ext_cfg_path.read_text(encoding="utf-8"))
            for x in cfg.get("noise_filters", []) or []:
                if isinstance(x, str) and x.strip():
                    merged.add(x.strip().lower())
        except (json.JSONDecodeError, OSError):
            pass
    # workspace concept_guidance
    cg_path = out_path.parent.parent / "concept_guidance.json"
    if cg_path.exists():
        try:
            cg = json.loads(cg_path.read_text(encoding="utf-8"))
            for x in cg.get("noise_filters", []) or []:
                if isinstance(x, str) and x.strip():
                    merged.add(x.strip().lower())
            for x in cg.get("concept_exclusions", []) or []:
                if isinstance(x, str) and x.strip():
                    merged.add(x.strip().lower())
        except (json.JSONDecodeError, OSError):
            pass
    return merged


def _load_json(path: Path) -> list | dict:
    if not path.exists():
        return [] if "candidates" in path.name or "actions" in path.name else {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


# Leading determiners/possessives to strip for merging (Your Awareness -> Awareness, Her Damage -> Damage)
_LEADING_DETERMINERS = (
    "Your ", "Her ", "His ", "Its ", "Their ", "Our ", "My ", "Them ",
    "The ", "A ", "An ",
)


def _normalize_concept_name(name: str) -> str:
    """Normalize for matching: strip determiners, collapse whitespace, canonical case."""
    if not name or not isinstance(name, str):
        return ""
    n = re.sub(r"\s+", " ", name.strip())
    for prefix in _LEADING_DETERMINERS:
        if n.startswith(prefix):
            n = n[len(prefix) :].strip()
            break
    # Canonical case so "DEXTERITY" and "Dexterity" merge (tf_weights vs dependency_verbs)
    if n:
        n = n.title()
    return n


def _dep_id_to_act_id(dep_id: str) -> str:
    """Map dep_XXXX to act_XXXX."""
    if dep_id.startswith("dep_"):
        return "act_" + dep_id[4:]
    return dep_id


def _load_signals(signals_dir: Path) -> dict:
    """Load combined concept_signals.json; fall back to separate files for compatibility."""
    combined = signals_dir / "concept_signals.json"
    if combined.exists():
        return _load_json(combined) or {}
    return {
        "tf_weights": _load_json(signals_dir / "term_candidates.json"),
        "dependency_verbs": _load_json(signals_dir / "dependency_actions.json"),
        "actor_detection": _load_json(signals_dir / "actor_candidates.json"),
        "centrality": _load_json(signals_dir / "centrality_scores.json"),
    }


def _collect_chunk_ids_per_concept(signals: dict) -> dict[str, set[str]]:
    """Aggregate chunk IDs per concept from all signals that have chunk refs.

    Sources:
    - tf_weights: chunk_ids per term
    - np_mining: chunk_ids per phrase
    - dependency_verbs: source_chunk -> subject, object
    - definition_patterns: source_chunk -> concept
    - table_mining: source_chunk -> each header (concept)
    - enumeration_patterns: source_chunk -> parent_concept, children
    - contrast_patterns: source_chunk -> each concept
    - verb_interaction.sample_interactions: source_chunk -> subject, object
    """
    chunk_ids: dict[str, set[str]] = {}

    def _add(concept: str, cid: str) -> None:
        if not concept or not cid:
            return
        if concept not in chunk_ids:
            chunk_ids[concept] = set()
        chunk_ids[concept].add(cid)

    # tf_weights
    for t in signals.get("tf_weights", []) or []:
        if not isinstance(t, dict):
            continue
        name = _normalize_concept_name(t.get("name", ""))
        for cid in t.get("chunk_ids", []) or []:
            _add(name, cid)

    # np_mining
    for np in signals.get("np_mining", []) or []:
        if not isinstance(np, dict):
            continue
        name = _normalize_concept_name(np.get("phrase", ""))
        for cid in np.get("chunk_ids", []) or []:
            _add(name, cid)

    # dependency_verbs
    for d in signals.get("dependency_verbs", []) or []:
        if not isinstance(d, dict):
            continue
        cid = d.get("source_chunk", "")
        for name in (_normalize_concept_name(d.get("subject", "")), _normalize_concept_name(d.get("object", ""))):
            _add(name, cid)

    # definition_patterns
    for d in signals.get("definition_patterns", []) or []:
        if not isinstance(d, dict):
            continue
        name = _normalize_concept_name(d.get("concept", ""))
        cid = d.get("source_chunk", "")
        _add(name, cid)

    # table_mining: headers are concepts
    for t in signals.get("table_mining", []) or []:
        if not isinstance(t, dict):
            continue
        cid = t.get("source_chunk", "")
        for h in t.get("headers", []) or []:
            name = _normalize_concept_name(h if isinstance(h, str) else str(h))
            _add(name, cid)

    # enumeration_patterns: parent + children
    for e in signals.get("enumeration_patterns", []) or []:
        if not isinstance(e, dict):
            continue
        cid = e.get("source_chunk", "")
        parent = _normalize_concept_name(e.get("parent_concept", ""))
        _add(parent, cid)
        for c in e.get("children", []) or []:
            child = _normalize_concept_name(c if isinstance(c, str) else str(c))
            _add(child, cid)

    # contrast_patterns
    for c in signals.get("contrast_patterns", []) or []:
        if not isinstance(c, dict):
            continue
        cid = c.get("source_chunk", "")
        for x in c.get("concepts", []) or []:
            name = _normalize_concept_name(x if isinstance(x, str) else str(x))
            _add(name, cid)

    # verb_interaction.sample_interactions
    vi = signals.get("verb_interaction", {}) or {}
    for i in vi.get("sample_interactions", []) or []:
        if not isinstance(i, dict):
            continue
        cid = i.get("source_chunk", "")
        for key in ("subject", "object"):
            name = _normalize_concept_name(i.get(key, ""))
            _add(name, cid)

    return chunk_ids


def _build_concepts_and_registries(signals: dict, noise_set: set[str] | None = None) -> dict:
    """Build concepts + registries from concept signals."""
    terms = signals.get("tf_weights", [])
    deps = signals.get("dependency_verbs", [])
    actors = signals.get("actor_detection", [])

    if not isinstance(terms, list):
        terms = []
    if not isinstance(deps, list):
        deps = []
    if not isinstance(actors, list):
        actors = []

    # Collect all concept names
    concepts_set: set[str] = set()
    term_to_ids: dict[str, list[str]] = {}  # concept name -> [term_id, ...]

    for t in terms:
        if not isinstance(t, dict):
            continue
        tid = t.get("term_id", "")
        name = _normalize_concept_name(t.get("name", ""))
        if not name or not tid:
            continue
        if _is_noise_concept(name, noise_set):
            continue
        concepts_set.add(name)
        term_to_ids.setdefault(name, []).append(tid)

    for a in actors:
        if not isinstance(a, dict):
            continue
        name = _normalize_concept_name(a.get("name", ""))
        if not name or _is_noise_concept(name, noise_set):
            continue
        concepts_set.add(name)
        # Actors may not have term_ids; leave empty if not in terms

    for d in deps:
        if not isinstance(d, dict):
            continue
        subj = _normalize_concept_name(d.get("subject", ""))
        obj = _normalize_concept_name(d.get("object", ""))
        if subj and not _is_noise_concept(subj, noise_set):
            concepts_set.add(subj)
        if obj and not _is_noise_concept(obj, noise_set):
            concepts_set.add(obj)

    # Add concepts from remaining signals (per evidence-signal-extraction-design: merge all signals)
    def _add_concept(name: str) -> None:
        n = _normalize_concept_name(name)
        if n and not _is_noise_concept(n, noise_set):
            concepts_set.add(n)

    for d in signals.get("definition_patterns", []) or []:
        if isinstance(d, dict):
            _add_concept(d.get("concept", ""))

    for np in signals.get("np_mining", []) or []:
        if isinstance(np, dict):
            _add_concept(np.get("phrase", ""))

    for t in signals.get("table_mining", []) or []:
        if isinstance(t, dict):
            for h in t.get("headers", []) or []:
                _add_concept(h if isinstance(h, str) else str(h))

    for e in signals.get("enumeration_patterns", []) or []:
        if isinstance(e, dict):
            _add_concept(e.get("parent_concept", ""))
            for c in e.get("children", []) or []:
                _add_concept(c if isinstance(c, str) else str(c))

    for c in signals.get("contrast_patterns", []) or []:
        if isinstance(c, dict):
            for x in c.get("concepts", []) or []:
                _add_concept(x if isinstance(x, str) else str(x))

    vi = signals.get("verb_interaction", {}) or {}
    for i in vi.get("sample_interactions", []) or []:
        if isinstance(i, dict):
            _add_concept(i.get("subject", ""))
            _add_concept(i.get("object", ""))
    for cv in vi.get("concept_verb_scores", []) or []:
        if isinstance(cv, dict):
            _add_concept(cv.get("concept", ""))

    co = signals.get("cooccurrence", {}) or {}
    for edge in co.get("edges", []) or []:
        if isinstance(edge, dict):
            _add_concept(edge.get("from", ""))
            _add_concept(edge.get("to", ""))

    for tm in signals.get("topic_modeling", []) or []:
        if isinstance(tm, dict):
            _add_concept(tm.get("topic_term", ""))
            for rt in tm.get("representative_terms", []) or []:
                _add_concept(rt if isinstance(rt, str) else str(rt))

    for cent in signals.get("centrality", []) or []:
        if isinstance(cent, dict):
            _add_concept(cent.get("concept", ""))

    # Initialize concept entries (chunk_ids added later from _collect_chunk_ids_per_concept)
    index: dict[str, dict[str, list]] = {}
    for c in sorted(concepts_set):
        index[c] = {
            "term_ids": list(dict.fromkeys(term_to_ids.get(c, []))),
            "performs": [],
            "receives": [],
            "states": [],
            "decisions": [],
            "relationships": [],
        }

    # Build actions registry and link performs/receives
    actions_registry: dict[str, dict] = {}
    for d in deps:
        if not isinstance(d, dict):
            continue
        dep_id = d.get("dep_id", "")
        subj = _normalize_concept_name(d.get("subject", ""))
        obj = _normalize_concept_name(d.get("object", ""))
        pred = (d.get("predicate") or "").strip()
        raw = (d.get("raw") or "").strip()
        if not dep_id:
            continue
        # Blank subject/object when they're noise; skip action when both are noise
        if subj and _is_noise_concept(subj, noise_set):
            subj = ""
        if obj and _is_noise_concept(obj, noise_set):
            obj = ""
        if not subj and not obj:
            continue
        act_id = _dep_id_to_act_id(dep_id)
        actions_registry[act_id] = {
            "subject": subj,
            "predicate": pred,
            "object": obj,
            "raw": raw,
        }
        if subj and subj in index:
            if act_id not in index[subj]["performs"]:
                index[subj]["performs"].append(act_id)
        if obj and obj in index:
            if act_id not in index[obj]["receives"]:
                index[obj]["receives"].append(act_id)

    return {
        "concepts": index,
        "registries": {
            "actions": actions_registry,
            "decisions": {},
            "states": {},
            "relationships": {},
        },
    }


def _build_concept_guidance(signals: dict, concepts: dict, noise_set: set[str] | None = None) -> dict:
    """Derive concept_guidance for Phase 5 evidence extraction."""
    terms = signals.get("tf_weights", [])
    actors = signals.get("actor_detection", [])
    centrality = signals.get("centrality", [])

    if not isinstance(terms, list):
        terms = []
    if not isinstance(actors, list):
        actors = []
    if not isinstance(centrality, list):
        centrality = []

    # Priority concepts: empty by default. Auto-derived from tf_weights/actors has no value
    # (scores modifiers, section headers, etc.). Workspace concept_guidance.json can provide
    # curated priority_concepts when needed.
    priority: list[str] = []

    # Aliases: empty by default. Workspace can provide solution/concept_guidance.json
    # with concept_aliases (domain-specific, e.g. M&M: Agility→AGL).
    aliases: dict[str, list[str]] = {}

    # Mechanisms and variation_axes: placeholders; AI/human can refine
    mechanisms: list[str] = []
    variation_axes: list[str] = []

    actor_names = [
        _normalize_concept_name(a.get("name", ""))
        for a in actors if isinstance(a, dict) and a.get("name")
    ]
    actor_names = [n for n in actor_names if n]

    noise_filters = sorted(noise_set) if noise_set else list(_NOISE_TERMS)

    return {
        "priority_concepts": priority,
        "concept_aliases": aliases,
        "mechanisms": mechanisms,
        "actors": actor_names,
        "variation_axes": variation_axes,
        "noise_filters": noise_filters,
        "focus_sections": [],
    }


# Index-phase curation: merge aliases, singular/plural, artifacts; remove nonsense and categories.
# Phase 5 (concept_synthesis) is AI-only; this programmatic cleanup belongs in Phase 4.
_INDEX_ARTIFACT_MERGES = [
    ("All Will", "Will"),
    ("All Magic", "Magic"),
    ("Afflic", "Affliction"),
    ("Communica", "Communication"),
    ("Compli", "Complication"),
    ("Continu", "Continuous"),
    ("Burst Area Afflic", "Burst Area Affliction"),
    ("COST PER RANK An", "COST PER RANK"),
]
_INDEX_REMOVE_NONSENSE = {
    "Choshech", "Cline", "Choose", "Choose One", "Although", "Because", "Another", "Any",
    "Apply", "Alternately", "Although Illusion", "AND CHARGES Lots", "Buzcinski",
    "Cortney Cline", "Angel Island", "Blackbird", "Blood Monk", "Cryptid Clans",
    "Crown Tower", "Cloaking Device", "Ambient Plant", "Avison", "Avian", "Asian",
    "Battleships", "Bombers", "Bandit", "Caliber", "Center", "Category", "Clock",
    "Clothing", "Com", "Cost", "Controlled",
}
_INDEX_REMOVE_CATEGORIES = {
    "ACTION", "ADVANTAGES", "ADVENTURE", "COMBAT", "DEFENSE", "DEFENSES",
    "ABILITIES Constructs", "COST PER RANK", "THE BASICS", "For", "The",
    "Opposed", "Okay", "MUTANTS", "Powers",
}


def _curate_index(hypothesis: dict) -> None:
    """Apply index-phase curation: merge aliases/plural/artifacts, remove nonsense and categories."""
    concepts = hypothesis.get("concepts", {})
    actions = hypothesis.get("registries", {}).get("actions", {})
    cg = hypothesis.get("concept_guidance", {})
    aliases_cfg = cg.get("concept_aliases", {})

    def merge_list(a: list, b: list) -> list:
        seen = set()
        out = []
        for x in (a or []) + (b or []):
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    def merge_concept_into(target: dict, source: dict) -> None:
        for field in ("term_ids", "chunk_ids", "performs", "receives", "states", "decisions", "relationships"):
            a, b = target.get(field, []), source.get(field, [])
            if isinstance(a, list) and isinstance(b, list):
                target[field] = merge_list(a, b)

    alias_to_canon = {}
    for canon, alias_list in (aliases_cfg or {}).items():
        for a in (alias_list if isinstance(alias_list, list) else [alias_list]):
            alias_to_canon[a.upper()] = canon
            alias_to_canon[a] = canon

    keys_upper = {k.upper(): k for k in concepts}

    def resolve_canonical(name: str) -> str | None:
        u = name.upper()
        return keys_upper.get(u) or next((k for k in concepts if k.upper() == u), None)

    # 1. Merge concept_aliases (AGL -> Agility, etc.)
    for alias_upper, canon in alias_to_canon.items():
        if alias_upper not in keys_upper:
            continue
        alias_key = keys_upper[alias_upper]
        canon_key = resolve_canonical(canon)
        if alias_key == canon_key:
            continue
        if canon_key and canon_key in concepts:
            merge_concept_into(concepts[canon_key], concepts[alias_key])
        else:
            concepts[canon] = concepts.pop(alias_key)
            canon_key = canon
        for act in actions.values():
            if act.get("subject") == alias_key:
                act["subject"] = canon_key
            if act.get("object") == alias_key:
                act["object"] = canon_key
        if alias_key in concepts:
            del concepts[alias_key]
        keys_upper = {k.upper(): k for k in concepts}

    # 2. Merge singular/plural (prefer singular as canonical)
    def singular_plural_pairs() -> list[tuple[str, str]]:
        pairs = []
        for name in list(concepts.keys()):
            if name.endswith("s") and len(name) > 1:
                singular = name[:-1]
                if singular.upper() in keys_upper:
                    canon = keys_upper[singular.upper()]
                    if canon != name:
                        pairs.append((name, canon))
        return pairs

    for alias, canon in singular_plural_pairs():
        if alias in concepts and canon in concepts:
            merge_concept_into(concepts[canon], concepts[alias])
            for act in actions.values():
                if act.get("subject") == alias:
                    act["subject"] = canon
                if act.get("object") == alias:
                    act["object"] = canon
            del concepts[alias]
            keys_upper = {k.upper(): k for k in concepts}

    # 3. Merge extraction artifacts
    for alias, canon in _INDEX_ARTIFACT_MERGES:
        if alias not in concepts:
            continue
        canon_key = resolve_canonical(canon)
        if canon_key and canon_key in concepts:
            merge_concept_into(concepts[canon_key], concepts[alias])
        else:
            concepts[canon] = concepts.pop(alias)
            canon_key = canon
        for act in actions.values():
            if act.get("subject") == alias:
                act["subject"] = canon_key
            if act.get("object") == alias:
                act["object"] = canon_key
        if alias in concepts:
            del concepts[alias]
        keys_upper = {k.upper(): k for k in concepts}

    # 4. Remove nonsense
    for name in list(concepts.keys()):
        if name in _INDEX_REMOVE_NONSENSE:
            for act in actions.values():
                if act.get("subject") == name:
                    act["subject"] = ""
                if act.get("object") == name:
                    act["object"] = ""
            del concepts[name]

    # 5. Remove categories
    for name in list(concepts.keys()):
        if name in _INDEX_REMOVE_CATEGORIES:
            for act in actions.values():
                if act.get("subject") == name:
                    act["subject"] = ""
                if act.get("object") == name:
                    act["object"] = ""
            del concepts[name]

    # 6. Remove concepts with no evidence (e.g. np_mining-only, never linked to chunk/term/action)
    for name in list(concepts.keys()):
        c = concepts[name]
        if not any(c.get(f, []) for f in ("term_ids", "chunk_ids", "performs", "receives", "states", "decisions", "relationships")):
            for act in actions.values():
                if act.get("subject") == name:
                    act["subject"] = ""
                if act.get("object") == name:
                    act["object"] = ""
            del concepts[name]

    # Rebuild performs/receives from actions
    for c in concepts.values():
        c["performs"] = []
        c["receives"] = []
    for act_id, act in actions.items():
        subj, obj = act.get("subject", ""), act.get("object", "")
        if subj in concepts and act_id not in concepts[subj]["performs"]:
            concepts[subj]["performs"].append(act_id)
        if obj in concepts and act_id not in concepts[obj]["receives"]:
            concepts[obj]["receives"].append(act_id)


def _render_hypothesis_md(hypothesis: dict) -> str:
    """Render hypothesis.json to markdown: full concept-anchored view per spec.

    Each concept is a section with term_ids, performs (resolved actions), receives,
    states, decisions, relationships. Actions are shown inline as Subject predicate Object.
    """
    lines = [
        "# Hypothesis",
        "",
        "Concept-anchored view of `hypothesis.json`. Each concept lists its evidence.",
        "",
    ]

    # concept_guidance (full)
    cg = hypothesis.get("concept_guidance", {})
    lines.extend(["## concept_guidance", ""])
    lines.append("**priority_concepts:**")
    for c in cg.get("priority_concepts", []):
        lines.append(f"- {c}")
    lines.append("")
    lines.append("**actors:**")
    for a in cg.get("actors", []):
        lines.append(f"- {a}")
    lines.append("")
    lines.append("**concept_aliases:**")
    for k, v in cg.get("concept_aliases", {}).items():
        lines.append(f"- {k} → {', '.join(str(x) for x in v)}")
    lines.append("")
    lines.append("**noise_filters:** " + ", ".join(str(x) for x in cg.get("noise_filters", [])))
    lines.append("")
    lines.append("---")
    lines.append("")

    # concepts: each as a full section with resolved actions
    concepts = hypothesis.get("concepts", {})
    actions_reg = hypothesis.get("registries", {}).get("actions", {})

    lines.append("## concepts")
    lines.append("")
    lines.append(f"*{len(concepts)} concepts*")
    lines.append("")

    for name, data in sorted(concepts.items()):
        term_ids = data.get("term_ids", [])
        performs = data.get("performs", [])
        receives = data.get("receives", [])
        states = data.get("states", [])
        decisions = data.get("decisions", [])
        relationships = data.get("relationships", [])

        lines.append(f"### {name}")
        lines.append("")

        chunk_ids = data.get("chunk_ids", [])
        lines.append("- **term_ids:** " + (", ".join(term_ids) if term_ids else "—"))
        lines.append("- **chunk_ids:** " + (", ".join(chunk_ids[:20]) + (" …" if len(chunk_ids) > 20 else "") if chunk_ids else "—"))
        lines.append("")

        if performs:
            lines.append("- **performs:**")
            for act_id in performs:
                a = actions_reg.get(act_id, {})
                subj = a.get("subject", "")
                pred = a.get("predicate", "")
                obj = a.get("object", "")
                raw = (a.get("raw", "") or "")[:100].replace("\n", " ")
                lines.append(f"  - `{act_id}` {subj} **{pred}** {obj}")
                if raw:
                    lines.append(f"    > {raw}...")
            lines.append("")
        else:
            lines.append("- **performs:** —")
            lines.append("")

        if receives:
            lines.append("- **receives:**")
            for act_id in receives:
                a = actions_reg.get(act_id, {})
                subj = a.get("subject", "")
                pred = a.get("predicate", "")
                obj = a.get("object", "")
                raw = (a.get("raw", "") or "")[:100].replace("\n", " ")
                lines.append(f"  - `{act_id}` {subj} **{pred}** {obj}")
                if raw:
                    lines.append(f"    > {raw}...")
            lines.append("")
        else:
            lines.append("- **receives:** —")
            lines.append("")

        lines.append("- **states:** " + (", ".join(states) if states else "—"))
        lines.append("- **decisions:** " + (", ".join(decisions) if decisions else "—"))
        lines.append("- **relationships:** " + (", ".join(str(r) for r in relationships) if relationships else "—"))
        lines.append("")

    # Appendix: actions registry
    lines.append("---")
    lines.append("")
    lines.append("## registries.actions")
    lines.append("")
    for act_id, a in sorted(actions_reg.items()):
        subj = a.get("subject", "")
        pred = a.get("predicate", "")
        obj = a.get("object", "")
        raw = (a.get("raw", "") or "")[:120].replace("\n", " ")
        lines.append(f"- **{act_id}** {subj} {pred} {obj}")
        if raw:
            lines.append(f"  `{raw}...`")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Phase 4: Build hypothesis.json from concept signals (concepts + registries format)"
    )
    parser.add_argument(
        "--input-dir", "-i",
        help="Directory with concept signals (default: workspace solution/concept_signals)",
    )
    parser.add_argument(
        "--output", "-o",
        help="Output path for hypothesis.json (default: workspace solution/generated/hypothesis.json)",
    )
    args = parser.parse_args()

    if str(_SKILL_DIR / "scripts") not in sys.path:
        sys.path.insert(0, str(_SKILL_DIR / "scripts"))
    from _config import concept_signals_dir, hypothesis_path

    signals_dir = Path(args.input_dir).resolve() if args.input_dir else concept_signals_dir()
    out_path = Path(args.output).resolve() if args.output else hypothesis_path()

    if not signals_dir.exists():
        print(f"Concept signals dir not found: {signals_dir}", file=sys.stderr)
        sys.exit(1)

    noise_set = _load_noise_filters(out_path)
    signals = _load_signals(signals_dir)
    core = _build_concepts_and_registries(signals, noise_set)
    concept_guidance = _build_concept_guidance(signals, core["concepts"], noise_set)

    # Merge workspace concept_guidance if present (domain-specific curation)
    workspace_cg = out_path.parent.parent / "concept_guidance.json"
    if workspace_cg.exists():
        try:
            ws = json.loads(workspace_cg.read_text(encoding="utf-8"))
            if isinstance(ws.get("concept_aliases"), dict):
                concept_guidance["concept_aliases"].update(ws["concept_aliases"])
            if isinstance(ws.get("priority_concepts"), list) and ws["priority_concepts"]:
                concept_guidance["priority_concepts"] = ws["priority_concepts"]
        except (json.JSONDecodeError, OSError):
            pass

    # Phase 4: Add chunk_ids per concept (all chunks that touch each concept)
    chunk_ids_map = _collect_chunk_ids_per_concept(signals)
    for name, data in core["concepts"].items():
        ids = chunk_ids_map.get(name, set())
        data["chunk_ids"] = sorted(ids) if ids else []

    hypothesis = {
        "concepts": core["concepts"],
        "registries": core["registries"],
        "concept_guidance": concept_guidance,
    }

    _curate_index(hypothesis)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(hypothesis, indent=2, ensure_ascii=False), encoding="utf-8")

    md_path = out_path.with_suffix(".md")
    md_path.write_text(_render_hypothesis_md(hypothesis), encoding="utf-8")

    n_concepts = len(core["concepts"])
    n_actions = len(core["registries"]["actions"])
    print(f"Built hypothesis: {n_concepts} concepts, {n_actions} actions -> {out_path}")
    print(f"Markdown render -> {md_path}")


if __name__ == "__main__":
    main()
