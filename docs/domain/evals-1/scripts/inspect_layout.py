"""Quick inspection of class positions on a drawio page, with name extraction."""
from __future__ import annotations
import re
import sys
sys.path.insert(0, r'c:\dev\abd-skills\practices\domain-driven-design\skills\supporting\drawio-domain-sync\scripts')
from drawio_tools import load_drawio, get_page


NAME_RE = re.compile(r"<b>([^<]+)</b>")


def _extract_class_name(raw: str) -> str:
    if not raw:
        return "?"
    m = NAME_RE.search(raw)
    if m:
        return m.group(1).strip()
    # fallback: strip HTML
    txt = re.sub(r"<[^>]+>", "", raw).strip().split("\n")[0].strip()
    return txt[:40] if txt else "?"


def inspect(path: str, page: str) -> None:
    _, mx = load_drawio(path)
    _, root = get_page(mx, page)
    print(f"=== {path} :: {page} ===")
    print("CLASSES (sorted by y, then x):")
    rows = []
    id_to_name: dict[str, str] = {}
    for cell in root.iter("mxCell"):
        if cell.get("vertex") == "1":
            geom = cell.find("mxGeometry")
            if geom is None:
                continue
            raw = cell.get("value") or ""
            name = _extract_class_name(raw)
            cid = cell.get("id") or "?"
            id_to_name[cid] = name
            try:
                x = float(geom.get("x") or 0)
                y = float(geom.get("y") or 0)
                w = float(geom.get("width") or 0)
                h = float(geom.get("height") or 0)
            except ValueError:
                continue
            rows.append((y, x, cid, name, w, h))
    rows.sort()
    for y, x, cid, name, w, h in rows:
        print(f"  [{cid:>3}] {name:30s}  x={x:>6.0f} y={y:>6.0f} w={w:>4.0f} h={h:>4.0f}")

    print()
    print("EDGES (resolved):")
    for cell in root.iter("mxCell"):
        if cell.get("edge") == "1":
            src = cell.get("source")
            tgt = cell.get("target")
            style = cell.get("style") or ""
            arrow = "INHERIT" if "endArrow=block" in style else "ASSOC"
            sname = id_to_name.get(src or "", src or "?")
            tname = id_to_name.get(tgt or "", tgt or "?")
            print(f"  {cell.get('id'):>3}: {sname:30s} --[{arrow}]--> {tname}")


if __name__ == "__main__":
    inspect(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "AbdSkill")
