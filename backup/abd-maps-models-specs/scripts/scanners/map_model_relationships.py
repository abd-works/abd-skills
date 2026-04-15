"""Scanner: depends_on and module.depends_on reference integrity in map-model-spec.json.

Rule: map-model-relationships

Collects all concept names and module names from modules_and_epics, then verifies:
- concept.depends_on[].concept → exists in concept set. **Pre-property:** concept-only
  scaffold may use concept.depends_on alone. **Post-property:** collaborations should be
  pinned on **property** / **operation** `depends_on` (authoritative). Optional
  **concept.depends_on** may remain as a **class-diagram summary** only if every peer
  also appears in at least one property or operation `depends_on` under that concept
  (subset sync — no “floating” class-level-only edges).
- property.depends_on[].concept and operation.depends_on[].concept → exist in concept set
- module.depends_on[] dependent_concepts, provides_concepts → exist; module → module name exists

Usage:
    python scripts/scanners/map_model_relationships.py [--input <path>]

Default input: <output_dir>/maps-models-specs/map-model-spec.json
Exit 0 = pass. Exit 1 = violations. Missing file → skip (0), same as other scanners.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


RULE_ID = "map-model-relationships"


def _peer_names_from_dep_list(dep_list: list | None) -> set[str]:
    out: set[str] = set()
    if not isinstance(dep_list, list):
        return out
    for dep in dep_list:
        if not isinstance(dep, dict):
            continue
        peer = dep.get("concept")
        if isinstance(peer, str) and peer.strip():
            out.add(peer.strip())
    return out


def _member_depends_on_peer_union(concept: dict) -> set[str]:
    """Union of depends_on peers on all properties and operations under a concept."""
    u: set[str] = set()
    for prop in concept.get("properties") or []:
        if isinstance(prop, dict):
            u |= _peer_names_from_dep_list(prop.get("depends_on"))
    for op in concept.get("operations") or []:
        if isinstance(op, dict):
            u |= _peer_names_from_dep_list(op.get("depends_on"))
    return u


def _collect_names(data: dict) -> tuple[set[str], set[str]]:
    concepts: set[str] = set()
    modules: set[str] = set()
    pairs = data.get("modules_and_epics")
    if not isinstance(pairs, list):
        return concepts, modules
    for pair in pairs:
        if not isinstance(pair, dict):
            continue
        mod = pair.get("module") or {}
        if isinstance(mod, dict):
            mn = (mod.get("name") or "").strip()
            if mn:
                modules.add(mn)
            for c in mod.get("concepts") or []:
                if isinstance(c, dict):
                    n = (c.get("name") or "").strip()
                    if n:
                        concepts.add(n)
    return concepts, modules


def scan(data: dict) -> list[str]:
    errors: list[str] = []
    concepts, modules = _collect_names(data)
    pairs = data.get("modules_and_epics")
    if not isinstance(pairs, list):
        return errors

    for pair_idx, pair in enumerate(pairs):
        if not isinstance(pair, dict):
            continue
        mod = pair.get("module") or {}
        if not isinstance(mod, dict):
            continue
        module_name = mod.get("name", f"<module-{pair_idx}>")
        mloc = f"modules_and_epics[{pair_idx}].module['{module_name}']"

        for midx, row in enumerate(mod.get("depends_on") or []):
            if not isinstance(row, dict):
                continue
            loc = f"{mloc}.depends_on[{midx}]"
            prov = row.get("module")
            if isinstance(prov, str) and prov.strip():
                if prov.strip() not in modules:
                    errors.append(f"{loc}: module.depends_on.module {prov!r} — no such module name")
            for key in ("dependent_concepts", "provides_concepts"):
                arr = row.get(key)
                if not isinstance(arr, list):
                    continue
                for i, name in enumerate(arr):
                    if not isinstance(name, str) or not name.strip():
                        continue
                    if name.strip() not in concepts:
                        errors.append(
                            f"{loc}.{key}[{i}] {name!r} — not a declared concept name"
                        )

        for cidx, concept in enumerate(mod.get("concepts") or []):
            if not isinstance(concept, dict):
                continue
            cname = concept.get("name", f"<concept-{cidx}>")
            cloc = f"{mloc}.concepts['{cname}']"
            props = concept.get("properties") or []
            ops = concept.get("operations") or []
            has_members = (isinstance(props, list) and len(props) > 0) or (
                isinstance(ops, list) and len(ops) > 0
            )
            cod = concept.get("depends_on") or []
            if not isinstance(cod, list):
                cod = []
            member_peers = _member_depends_on_peer_union(concept)

            for didx, dep in enumerate(cod):
                if not isinstance(dep, dict):
                    continue
                peer = dep.get("concept")
                if isinstance(peer, str) and peer.strip():
                    pn = peer.strip()
                    if pn not in concepts:
                        errors.append(
                            f"{cloc}.depends_on[{didx}].concept {peer!r} — not a declared concept name"
                        )
                    elif has_members and pn not in member_peers:
                        errors.append(
                            f"{cloc}.depends_on[{didx}].concept {peer!r} — not listed on any property "
                            "or operation under this concept; add member-level depends_on first, or "
                            "omit class-level (class-level must be a subset of member-level peers for sync)"
                        )

            for pidx, prop in enumerate(props):
                if not isinstance(prop, dict):
                    continue
                ploc = f"{cloc}.properties[{pidx}]"
                pname = prop.get("name", f"<prop-{pidx}>")
                for didx, dep in enumerate(prop.get("depends_on") or []):
                    if not isinstance(dep, dict):
                        continue
                    peer = dep.get("concept")
                    if isinstance(peer, str) and peer.strip():
                        if peer.strip() not in concepts:
                            errors.append(
                                f"{ploc}('{pname}').depends_on[{didx}].concept {peer!r} — not a declared concept name"
                            )

            for oidx, op in enumerate(ops):
                if not isinstance(op, dict):
                    continue
                oloc = f"{cloc}.operations[{oidx}]"
                oname = op.get("name", f"<op-{oidx}>")
                for didx, dep in enumerate(op.get("depends_on") or []):
                    if not isinstance(dep, dict):
                        continue
                    peer = dep.get("concept")
                    if isinstance(peer, str) and peer.strip():
                        if peer.strip() not in concepts:
                            errors.append(
                                f"{oloc}('{oname}').depends_on[{didx}].concept {peer!r} — not a declared concept name"
                            )
    return errors


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    scripts_dir = script_dir.parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    from _config import map_model_spec_path

    parser = argparse.ArgumentParser(description=f"Map model relationship scanner. Rule: {RULE_ID}")
    parser.add_argument("--input", default=str(map_model_spec_path()))
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"map_model_relationships: no file at {input_path} — skip")
        return 0

    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {input_path}: {e}", file=sys.stderr)
        return 1

    errors = scan(data)
    if not errors:
        print(f"PASS [{RULE_ID}] — depends_on / module edges resolve in {input_path.name}")
        return 0

    print(f"VIOLATIONS [{RULE_ID}] — {len(errors)} in {input_path.name}")
    for msg in errors:
        print(f"  {msg}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
