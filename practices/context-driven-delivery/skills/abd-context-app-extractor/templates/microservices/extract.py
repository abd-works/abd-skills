"""
extract.py  —  abd-context-app-extractor / Phase 0 scout (microservices)

Copy this file into <repo>/scripts/extract.py, then:
  1. Fill in BASE_URL and ENDPOINTS.
  2. Run:  python scripts/extract.py

Outputs (relative to repo root):
  docs/extracted-context/api-extraction/extraction-overview.md
  docs/extracted-context/api-extraction/openapi.yaml       ← reconstructed spec
  docs/extracted-context/api-extraction/har/<slug>.har     ← raw network trace

Prerequisites:
  pip install httpx PyYAML
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import httpx
import yaml


# ---------------------------------------------------------------------------
# ✏️  CONFIGURE — fill these in for your service
# ---------------------------------------------------------------------------

APP_NAME = "my-service"
BASE_URL = "http://localhost:3000"

# Authentication — choose one and fill it in, or leave both None for open APIs
AUTH_BEARER_TOKEN: Optional[str] = None      # "eyJhbGciOi..."
AUTH_BASIC: Optional[tuple[str, str]] = None # ("user", "pass")

# ✏️  Replace with your actual endpoints
ENDPOINTS: list[dict] = [
    # REST examples
    {
        "slug":         "01-health",
        "method":       "GET",
        "path":         "/health",
        "body":         None,
        "user_intent":  "Verify the service is running.",
        "domain_focus": [],
        "ux_focus":     [],
        "notes":        "Health check endpoint.",
    },
    {
        "slug":         "02-list-items",
        "method":       "GET",
        "path":         "/api/items",
        "body":         None,
        "user_intent":  "List all items.",
        "domain_focus": ["item"],
        "ux_focus":     [],
        "notes":        "Returns paginated list of items.",
    },
    {
        "slug":         "03-create-item",
        "method":       "POST",
        "path":         "/api/items",
        "body":         {"name": "Example Item", "description": "Scout sample"},
        "user_intent":  "Create a new item.",
        "domain_focus": ["item"],
        "ux_focus":     [],
        "notes":        "Creates an item. Returns 201 with created resource.",
    },
    # Add more endpoints here...
]


# ---------------------------------------------------------------------------
# Output paths — do not change
# ---------------------------------------------------------------------------

REPO_ROOT     = Path(__file__).resolve().parent.parent
EXTRACT_ROOT  = REPO_ROOT / "docs" / "extracted-context" / "api-extraction"
HAR_DIR       = EXTRACT_ROOT / "har"
HAR_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# HAR helpers
# ---------------------------------------------------------------------------

def build_har_entry(
    method: str,
    url: str,
    request_body: Any,
    response: httpx.Response,
    elapsed_ms: float,
) -> dict:
    req_body_text = json.dumps(request_body) if request_body else ""
    return {
        "startedDateTime": datetime.now(timezone.utc).isoformat(),
        "time": elapsed_ms,
        "request": {
            "method": method.upper(),
            "url": url,
            "httpVersion": "HTTP/1.1",
            "headers": [{"name": k, "value": v} for k, v in response.request.headers.items()],
            "queryString": [],
            "postData": {"mimeType": "application/json", "text": req_body_text} if req_body_text else None,
            "bodySize": len(req_body_text.encode()),
            "headersSize": -1,
        },
        "response": {
            "status": response.status_code,
            "statusText": str(response.status_code),
            "httpVersion": "HTTP/1.1",
            "headers": [{"name": k, "value": v} for k, v in response.headers.items()],
            "content": {
                "size": len(response.content),
                "mimeType": response.headers.get("content-type", "application/json"),
                "text": response.text,
            },
            "redirectURL": "",
            "bodySize": len(response.content),
            "headersSize": -1,
        },
        "cache": {},
        "timings": {"send": 0, "wait": elapsed_ms, "receive": 0},
    }


# ---------------------------------------------------------------------------
# OpenAPI reconstruction
# ---------------------------------------------------------------------------

def update_openapi(spec: dict, endpoint: dict, response: httpx.Response) -> None:
    """Add or update an endpoint entry in the reconstructed OpenAPI spec."""
    path   = endpoint["path"]
    method = endpoint["method"].lower()

    spec.setdefault("paths", {}).setdefault(path, {})[method] = {
        "summary": endpoint["user_intent"],
        "tags":    endpoint["domain_focus"],
        "responses": {
            str(response.status_code): {
                "description": f"Status {response.status_code}",
                "content": {
                    "application/json": {
                        "example": response.json() if "application/json" in response.headers.get("content-type", "") else {}
                    }
                },
            }
        },
    }
    if endpoint.get("body"):
        spec["paths"][path][method]["requestBody"] = {
            "content": {
                "application/json": {
                    "example": endpoint["body"]
                }
            }
        }


# ---------------------------------------------------------------------------
# Write extraction-overview.md
# ---------------------------------------------------------------------------

def write_overview(entries: list[dict]) -> None:
    all_domain = sorted({t for e in entries for t in e["domain_focus"]})

    lines = [
        f"# {APP_NAME} — Extraction Overview",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "Phase: scout (abd-context-app-extractor Phase 0)",
        "Source: scripts/extract.py via httpx.",
        "",
        "---",
        f"app: {APP_NAME}",
        'surface: "microservice"',
        'phase: "scout"',
        'automation_tool: "httpx"',
        'har_dir: "./har/"',
        'primary_views: ["domain", "story"]',
        "tags:",
        f"  domain: [{', '.join(repr(t) for t in all_domain)}]",
        "---",
        "",
    ]

    for e in entries:
        lines += [
            f"## {e['slug']} — {e['method']} {e['path']}",
            "",
            f"- status: {e['status']}",
            f'- user_intent: "{e["user_intent"]}"',
            f'- domain_focus: [{", ".join(repr(t) for t in e["domain_focus"])}]',
            f'- har: "./har/{e["slug"]}.har"',
            "- notes: |",
            *[f"  {line}" for line in e.get("notes", "").splitlines()],
            "",
            "---",
            "",
        ]

    out_path = EXTRACT_ROOT / "extraction-overview.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nExtraction overview: {out_path}")
    print(f"HAR files:           {HAR_DIR}/")
    print(f"Endpoints recorded:  {len(entries)}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    # Build auth headers
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if AUTH_BEARER_TOKEN:
        headers["Authorization"] = f"Bearer {AUTH_BEARER_TOKEN}"

    auth = AUTH_BASIC  # httpx accepts tuple[str,str] for Basic auth

    openapi_spec: dict = {
        "openapi": "3.0.0",
        "info": {"title": APP_NAME, "version": "scout"},
        "servers": [{"url": BASE_URL}],
        "paths": {},
    }

    entries: list[dict] = []

    with httpx.Client(base_url=BASE_URL, headers=headers, auth=auth, timeout=30) as client:
        for ep in ENDPOINTS:
            url = BASE_URL + ep["path"]
            print(f"→ {ep['method']} {ep['path']}  [{ep['slug']}]")

            t0 = time.monotonic()
            try:
                if ep["method"].upper() in ("GET", "DELETE", "HEAD"):
                    response = client.request(ep["method"], ep["path"])
                else:
                    response = client.request(ep["method"], ep["path"], json=ep.get("body"))
            except Exception as exc:
                print(f"  [ERROR] {exc}")
                continue
            elapsed_ms = (time.monotonic() - t0) * 1000

            print(f"  Status: {response.status_code}  ({elapsed_ms:.0f}ms)")

            # Write HAR
            har = {
                "log": {
                    "version": "1.2",
                    "creator": {"name": "abd-context-app-extractor", "version": "0.1"},
                    "entries": [build_har_entry(ep["method"], url, ep.get("body"), response, elapsed_ms)],
                }
            }
            har_path = HAR_DIR / f"{ep['slug']}.har"
            har_path.write_text(json.dumps(har, indent=2), encoding="utf-8")

            # Update OpenAPI spec
            update_openapi(openapi_spec, ep, response)

            entries.append({**ep, "status": response.status_code})

    # Write OpenAPI YAML
    openapi_path = EXTRACT_ROOT / "openapi.yaml"
    openapi_path.write_text(yaml.dump(openapi_spec, sort_keys=False), encoding="utf-8")
    print(f"\nOpenAPI spec: {openapi_path}")

    write_overview(entries)


if __name__ == "__main__":
    main()
