"""Inspect edge waypoints on a drawio page."""
from __future__ import annotations
import re, sys
sys.path.insert(0, r'c:\dev\abd-skills\practices\domain-driven-design\skills\supporting\drawio-domain-sync\scripts')
from drawio_tools import load_drawio, get_page

NAME_RE = re.compile(r"<b>([^<]+)</b>")

def extract_name(raw):
    if not raw:
        return "?"
    m = NAME_RE.search(raw)
    if m:
        return m.group(1).strip()
    return re.sub(r"<[^>]+>", "", raw).strip().split("\n")[0][:30] or "?"

def inspect(path, page):
    _, mx = load_drawio(path)
    _, root = get_page(mx, page)
    id_to_name = {}
    for c in root.iter("mxCell"):
        if c.get("vertex") == "1":
            id_to_name[c.get("id")] = extract_name(c.get("value") or "")
    print(f"=== {page} edges ===")
    for c in root.iter("mxCell"):
        if c.get("edge") == "1":
            src = id_to_name.get(c.get("source") or "", "?")
            tgt = id_to_name.get(c.get("target") or "", "?")
            style = c.get("style") or ""
            ex = re.search(r"exitX=([^;]+)", style)
            ey = re.search(r"exitY=([^;]+)", style)
            enx = re.search(r"entryX=([^;]+)", style)
            eny = re.search(r"entryY=([^;]+)", style)
            anchors = f" exit=({ex.group(1) if ex else '_'},{ey.group(1) if ey else '_'}) entry=({enx.group(1) if enx else '_'},{eny.group(1) if eny else '_'})"
            wps = []
            geo = c.find("mxGeometry")
            if geo is not None:
                arr = geo.find("Array")
                if arr is not None:
                    for p in arr.findall("mxPoint"):
                        wps.append((p.get("x"), p.get("y")))
            wpstr = f" waypoints={wps}" if wps else " waypoints=NONE"
            print(f"  {src} -> {tgt}{anchors}{wpstr}")

if __name__ == "__main__":
    inspect(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "AbdSkill")
