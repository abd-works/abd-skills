#!/usr/bin/env python3
"""
artifact_graph_cli.py — Cross-view artifact graph maintenance tool.

Commands:
  read        Load and print the graph (validates schema)
  validate    Check all links resolve to registered nodes and real files
  link        Add cross-view links for a story
  lookup      Show all artifacts linked to a story or concept
  reverse     Show all stories that link to a given domain/ux/arch node
  drift       Compare graph links against actual artifact file presence
  init        Create an empty artifact-graph.json from the template
  stats       Print link coverage statistics

Usage:
  python artifact_graph_cli.py read     --file <path>
  python artifact_graph_cli.py validate --file <path> [--root <workspace-root>]
  python artifact_graph_cli.py link     --file <path> --story "Name"
                                        [--domain "Module.Concept" ...]
                                        [--ux "screen-slug" ...]
                                        [--arch "mechanism-id" ...]
  python artifact_graph_cli.py lookup   --file <path> --story "Name"
  python artifact_graph_cli.py reverse  --file <path> --domain "Module.Concept"
  python artifact_graph_cli.py reverse  --file <path> --ux "screen-slug"
  python artifact_graph_cli.py reverse  --file <path> --arch "mechanism-id"
  python artifact_graph_cli.py drift    --file <path> [--root <workspace-root>]
  python artifact_graph_cli.py init     --file <path> [--product "Name"]
  python artifact_graph_cli.py stats    --file <path>
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

SCHEMA = "abd-artifact-graph/v1"

EMPTY_GRAPH: Dict[str, Any] = {
    "schema": SCHEMA,
    "product": "",
    "artifact_registry": {
        "story_graph": "docs/stories/story-map/story-graph.json",
        "domain_language": "docs/domain/language/domain-language.md",
        "domain_model": "docs/domain/model/domain-model.md",
        "domain_glossary": "docs/domain/glossary/domain-glossary.md",
        "ux_information_architecture": "docs/ux/information-architecture/information-architecture.md",
        "ux_mockup_index": "docs/ux/mockup/mockups.md",
        "architecture_blueprint": "docs/architecture/blueprint/architecture-blueprint.md",
    },
    "domain_nodes": {},
    "ux_nodes": {},
    "arch_nodes": {},
    "story_links": {},
}


# ---------------------------------------------------------------------------
# Load / save
# ---------------------------------------------------------------------------

def _load(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        _die(f"File not found: {path}")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if data.get("schema") != SCHEMA:
        _die(
            f"Unexpected schema '{data.get('schema')}' — expected '{SCHEMA}'. "
            "Use 'init' to create a valid graph."
        )
    return data


def _save(path: Path, data: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_read(args: argparse.Namespace) -> None:
    path = Path(args.file)
    data = _load(path)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_validate(args: argparse.Namespace) -> None:
    path = Path(args.file)
    data = _load(path)
    root = Path(args.root) if args.root else path.parent.parent

    errors: List[str] = []

    domain_nodes: Dict[str, Any] = data.get("domain_nodes", {})
    ux_nodes: Dict[str, Any] = data.get("ux_nodes", {})
    arch_nodes: Dict[str, Any] = data.get("arch_nodes", {})
    story_links: Dict[str, Any] = data.get("story_links", {})

    # Check node files exist
    for node_id, node in domain_nodes.items():
        f = root / node.get("file", "")
        if not f.exists():
            errors.append(f"domain_node '{node_id}' → file not found: {node.get('file')}")

    for node_id, node in ux_nodes.items():
        f = root / node.get("file", "")
        if not f.exists():
            errors.append(f"ux_node '{node_id}' → file not found: {node.get('file')}")

    for node_id, node in arch_nodes.items():
        f = root / node.get("file", "")
        if not f.exists():
            errors.append(f"arch_node '{node_id}' → file not found: {node.get('file')}")

    # Check story_links reference valid nodes
    for story, links in story_links.items():
        for ref in links.get("domain", []):
            if ref not in domain_nodes:
                errors.append(f"story '{story}' → domain ref '{ref}' not in domain_nodes")
        for ref in links.get("ux", []):
            if ref not in ux_nodes:
                errors.append(f"story '{story}' → ux ref '{ref}' not in ux_nodes")
        for ref in links.get("arch", []):
            if ref not in arch_nodes:
                errors.append(f"story '{story}' → arch ref '{ref}' not in arch_nodes")

    if errors:
        print(f"VALIDATION FAILED — {len(errors)} error(s):", file=sys.stderr)
        for e in errors:
            print(f"  • {e}", file=sys.stderr)
        sys.exit(1)
    else:
        story_count = len(story_links)
        linked = sum(
            1 for s in story_links.values()
            if s.get("domain") or s.get("ux") or s.get("arch")
        )
        print(
            f"OK — {len(domain_nodes)} domain nodes, {len(ux_nodes)} ux nodes, "
            f"{len(arch_nodes)} arch nodes, {story_count} stories ({linked} with links)"
        )


def cmd_link(args: argparse.Namespace) -> None:
    path = Path(args.file)
    data = _load(path)
    story_name: str = args.story
    story_links: Dict[str, Any] = data.setdefault("story_links", {})

    entry = story_links.setdefault(story_name, {
        "epic": args.epic or "",
        "sub_epic": args.sub_epic or "",
        "domain": [],
        "ux": [],
        "arch": [],
    })

    if args.epic:
        entry["epic"] = args.epic
    if args.sub_epic:
        entry["sub_epic"] = args.sub_epic

    for ref in args.domain or []:
        if ref not in entry.get("domain", []):
            entry.setdefault("domain", []).append(ref)

    for ref in args.ux or []:
        if ref not in entry.get("ux", []):
            entry.setdefault("ux", []).append(ref)

    for ref in args.arch or []:
        if ref not in entry.get("arch", []):
            entry.setdefault("arch", []).append(ref)

    _save(path, data)
    print(f"Updated links for story: {story_name!r}")
    print(json.dumps(entry, indent=2))


def cmd_lookup(args: argparse.Namespace) -> None:
    path = Path(args.file)
    data = _load(path)
    story_name: str = args.story
    story_links: Dict[str, Any] = data.get("story_links", {})

    if story_name not in story_links:
        print(f"No links registered for story: {story_name!r}")
        return

    links = story_links[story_name]
    domain_nodes = data.get("domain_nodes", {})
    ux_nodes = data.get("ux_nodes", {})
    arch_nodes = data.get("arch_nodes", {})

    print(f"Story: {story_name}")
    if links.get("epic"):
        print(f"  Epic: {links['epic']}")
    if links.get("sub_epic"):
        print(f"  Sub-epic: {links['sub_epic']}")

    print("\n  Domain concepts:")
    for ref in links.get("domain", []):
        node = domain_nodes.get(ref, {})
        file_path = node.get("file", "(not registered)")
        print(f"    • {ref} → {file_path}")

    print("\n  UX screens:")
    for ref in links.get("ux", []):
        node = ux_nodes.get(ref, {})
        label = node.get("label", ref)
        file_path = node.get("file", "(not registered)")
        print(f"    • {label} ({ref}) → {file_path}")

    print("\n  Architecture mechanisms:")
    for ref in links.get("arch", []):
        node = arch_nodes.get(ref, {})
        label = node.get("label", ref)
        file_path = node.get("file", "(not registered)")
        print(f"    • {label} ({ref}) → {file_path}")


def cmd_reverse(args: argparse.Namespace) -> None:
    path = Path(args.file)
    data = _load(path)
    story_links: Dict[str, Any] = data.get("story_links", {})

    target_key: Optional[str] = None
    target_id: Optional[str] = None

    if args.domain:
        target_key = "domain"
        target_id = args.domain
    elif args.ux:
        target_key = "ux"
        target_id = args.ux
    elif args.arch:
        target_key = "arch"
        target_id = args.arch
    else:
        _die("Provide one of --domain, --ux, or --arch")

    matching = [
        story for story, links in story_links.items()
        if target_id in links.get(target_key, [])
    ]

    if not matching:
        print(f"No stories link to {target_key} node: {target_id!r}")
        return

    print(f"Stories linking to {target_key} node '{target_id}':")
    for story in matching:
        epic = story_links[story].get("epic", "")
        sub = story_links[story].get("sub_epic", "")
        loc = f"{epic} > {sub}" if sub else epic
        print(f"  • {story}" + (f"  [{loc}]" if loc else ""))


def cmd_drift(args: argparse.Namespace) -> None:
    """Report links that point to domain_nodes/ux_nodes/arch_nodes whose files are missing."""
    path = Path(args.file)
    data = _load(path)
    root = Path(args.root) if args.root else path.parent.parent

    domain_nodes = data.get("domain_nodes", {})
    ux_nodes = data.get("ux_nodes", {})
    arch_nodes = data.get("arch_nodes", {})
    story_links = data.get("story_links", {})
    registry = data.get("artifact_registry", {})

    missing_files: List[str] = []
    dangling_links: List[str] = []

    # Registry files
    for key, rel_path in registry.items():
        f = root / rel_path
        if not f.exists():
            missing_files.append(f"registry[{key}]: {rel_path}")

    # Node files
    for nid, node in domain_nodes.items():
        f = root / node.get("file", "")
        if not f.exists():
            missing_files.append(f"domain_node[{nid}]: {node.get('file')}")

    for nid, node in ux_nodes.items():
        f = root / node.get("file", "")
        if not f.exists():
            missing_files.append(f"ux_node[{nid}]: {node.get('file')}")

    for nid, node in arch_nodes.items():
        f = root / node.get("file", "")
        if not f.exists():
            missing_files.append(f"arch_node[{nid}]: {node.get('file')}")

    # Story links → node existence
    for story, links in story_links.items():
        for ref in links.get("domain", []):
            if ref not in domain_nodes:
                dangling_links.append(f"story[{story!r}].domain → '{ref}' not in domain_nodes")
        for ref in links.get("ux", []):
            if ref not in ux_nodes:
                dangling_links.append(f"story[{story!r}].ux → '{ref}' not in ux_nodes")
        for ref in links.get("arch", []):
            if ref not in arch_nodes:
                dangling_links.append(f"story[{story!r}].arch → '{ref}' not in arch_nodes")

    if not missing_files and not dangling_links:
        print("No drift detected — all registered files exist and all links resolve.")
        return

    if missing_files:
        print(f"MISSING FILES ({len(missing_files)}):")
        for m in missing_files:
            print(f"  • {m}")

    if dangling_links:
        print(f"\nDANGLING LINKS ({len(dangling_links)}):")
        for d in dangling_links:
            print(f"  • {d}")

    sys.exit(1)


def cmd_init(args: argparse.Namespace) -> None:
    path = Path(args.file)
    if path.exists() and not args.force:
        _die(f"File already exists: {path}. Use --force to overwrite.")
    graph = dict(EMPTY_GRAPH)
    if args.product:
        graph["product"] = args.product
    path.parent.mkdir(parents=True, exist_ok=True)
    _save(path, graph)
    print(f"Created: {path}")


def cmd_stats(args: argparse.Namespace) -> None:
    path = Path(args.file)
    data = _load(path)

    story_links = data.get("story_links", {})
    domain_nodes = data.get("domain_nodes", {})
    ux_nodes = data.get("ux_nodes", {})
    arch_nodes = data.get("arch_nodes", {})

    total = len(story_links)
    with_domain = sum(1 for s in story_links.values() if s.get("domain"))
    with_ux = sum(1 for s in story_links.values() if s.get("ux"))
    with_arch = sum(1 for s in story_links.values() if s.get("arch"))
    fully_linked = sum(
        1 for s in story_links.values()
        if s.get("domain") and s.get("ux")
    )
    no_links = sum(
        1 for s in story_links.values()
        if not s.get("domain") and not s.get("ux") and not s.get("arch")
    )

    print(f"Product:          {data.get('product', '(unnamed)')}")
    print(f"Domain nodes:     {len(domain_nodes)}")
    print(f"UX nodes:         {len(ux_nodes)}")
    print(f"Arch nodes:       {len(arch_nodes)}")
    print(f"Stories tracked:  {total}")
    print(f"  with domain:    {with_domain}")
    print(f"  with ux:        {with_ux}")
    print(f"  with arch:      {with_arch}")
    print(f"  domain + ux:    {fully_linked}")
    print(f"  no links yet:   {no_links}")
    if total:
        pct = round(100 * fully_linked / total)
        print(f"  coverage:       {pct}% (domain+ux)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="artifact_graph_cli.py",
        description="Maintain the cross-view artifact graph (artifact-graph.json).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # read
    p_read = sub.add_parser("read", help="Load and print the graph")
    p_read.add_argument("--file", required=True)

    # validate
    p_val = sub.add_parser("validate", help="Validate all links and node file paths")
    p_val.add_argument("--file", required=True)
    p_val.add_argument("--root", help="Workspace root for resolving file paths")

    # link
    p_link = sub.add_parser("link", help="Add/update cross-view links for a story")
    p_link.add_argument("--file", required=True)
    p_link.add_argument("--story", required=True, help="Exact story name")
    p_link.add_argument("--epic", help="Epic name (for context)")
    p_link.add_argument("--sub-epic", dest="sub_epic", help="Sub-epic name (for context)")
    p_link.add_argument("--domain", nargs="+", metavar="MODULE.CONCEPT",
                        help="Domain node IDs to link (e.g. Catalog.Product)")
    p_link.add_argument("--ux", nargs="+", metavar="SCREEN-SLUG",
                        help="UX node IDs to link (e.g. product-search)")
    p_link.add_argument("--arch", nargs="+", metavar="MECHANISM-ID",
                        help="Arch node IDs to link (e.g. catalog-api)")

    # lookup
    p_look = sub.add_parser("lookup", help="Show all artifacts linked to a story")
    p_look.add_argument("--file", required=True)
    p_look.add_argument("--story", required=True)

    # reverse
    p_rev = sub.add_parser("reverse", help="Show all stories linking to a given node")
    p_rev.add_argument("--file", required=True)
    p_rev.add_argument("--domain", metavar="MODULE.CONCEPT")
    p_rev.add_argument("--ux", metavar="SCREEN-SLUG")
    p_rev.add_argument("--arch", metavar="MECHANISM-ID")

    # drift
    p_drift = sub.add_parser("drift", help="Detect missing files and dangling links")
    p_drift.add_argument("--file", required=True)
    p_drift.add_argument("--root", help="Workspace root for resolving file paths")

    # init
    p_init = sub.add_parser("init", help="Create an empty artifact-graph.json")
    p_init.add_argument("--file", required=True)
    p_init.add_argument("--product", help="Product name")
    p_init.add_argument("--force", action="store_true", help="Overwrite existing file")

    # stats
    p_stats = sub.add_parser("stats", help="Print link coverage statistics")
    p_stats.add_argument("--file", required=True)

    args = parser.parse_args()

    dispatch = {
        "read": cmd_read,
        "validate": cmd_validate,
        "link": cmd_link,
        "lookup": cmd_lookup,
        "reverse": cmd_reverse,
        "drift": cmd_drift,
        "init": cmd_init,
        "stats": cmd_stats,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
