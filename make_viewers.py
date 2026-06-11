"""Generate viewer HTML pages for drawio and markdown skill examples."""
import pathlib, json, html

catalog = pathlib.Path(r'c:\dev\abd-skills\catalog')
viewer_dir = catalog / 'viewer'
viewer_dir.mkdir(exist_ok=True)

def drawio_html(xml: str) -> str:
    data = json.dumps({'highlight': '#0000ff', 'nav': False, 'resize': True, 'fit': True, 'xml': xml})
    safe = data.replace("'", "&#39;")
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<style>* {margin:0;padding:0;box-sizing:border-box} body {background:#fff;overflow:hidden}</style>"
        "</head><body>"
        "<div class='mxgraph' style='width:100vw;height:100vh;' data-mxgraph='" + safe + "'></div>"
        "<script src='https://viewer.diagrams.net/js/viewer-static.min.js'></script>"
        "</body></html>"
    )

def md_html(md_text: str) -> str:
    try:
        import markdown as _md
        body = _md.markdown(md_text, extensions=['tables', 'fenced_code'])
    except Exception:
        body = '<pre>' + html.escape(md_text) + '</pre>'
    css = """
body {font-family: 'Segoe UI', system-ui, sans-serif; font-size: 14px; line-height: 1.65;
  color: #1a1a1e; background: #fff; padding: 32px; max-width: 820px; margin: 0 auto;}
h1 {font-size: 22px; font-weight: 700; margin: 0 0 16px; color: #111;}
h2 {font-size: 17px; font-weight: 600; margin: 24px 0 10px; color: #111;
    border-bottom: 1px solid #e0e0e0; padding-bottom: 4px;}
h3 {font-size: 14px; font-weight: 600; margin: 16px 0 6px;}
p {margin: 0 0 12px;} ul,ol {margin: 0 0 12px; padding-left: 24px;} li {margin-bottom: 4px;}
code {background:#f4f4f6; border-radius:3px; padding:1px 5px; font-family:monospace; font-size:13px;}
pre {background:#f4f4f6; border-radius:6px; padding:14px; overflow-x:auto; margin:0 0 14px;}
pre code {background:none; padding:0;}
table {border-collapse:collapse; width:100%; margin:0 0 14px;}
th,td {border:1px solid #ddd; padding:7px 10px; text-align:left;}
th {background:#f0f0f2; font-weight:600;}
blockquote {border-left:3px solid #e5531a; margin:0 0 14px; padding:6px 14px; color:#555;}
"""
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<style>" + css + "</style></head><body>" + body + "</body></html>"
    )

skills_root = pathlib.Path(r'c:\dev\abd-skills\practices')
pages = []
seen = set()

for drawio in skills_root.rglob('example.drawio'):
    dir_name = drawio.parent.parent.name
    if dir_name in seen:
        continue
    seen.add(dir_name)
    xml = drawio.read_text(encoding='utf-8')
    out = viewer_dir / (dir_name + '-drawio.html')
    out.write_text(drawio_html(xml), encoding='utf-8')
    preview_png = str(drawio.parent / '_preview.png')
    pages.append({'dir': dir_name, 'url': 'viewer/' + dir_name + '-drawio.html',
                  'out': preview_png, 'type': 'drawio'})
    print('drawio:', dir_name)

for pattern in ('example.md', 'examples.md'):
    for md in skills_root.rglob(pattern):
        dir_name = md.parent.parent.name
        if dir_name in seen:
            continue
        seen.add(dir_name)
        text = md.read_text(encoding='utf-8')
        out = viewer_dir / (dir_name + '-md.html')
        out.write_text(md_html(text), encoding='utf-8')
        preview_png = str(md.parent / '_preview.png')
        pages.append({'dir': dir_name, 'url': 'viewer/' + dir_name + '-md.html',
                      'out': preview_png, 'type': 'md'})
        print('md:    ', dir_name)

(viewer_dir / 'pages.json').write_text(json.dumps(pages, indent=2))
print('Total:', len(pages))
