"""
extract.py  —  abd-context-app-extractor / Phase 0 scout (Windows desktop)

Copy this file into <repo>/scripts/extract.py, then:
  1. Fill in APP_EXE and PAGES (screen names + navigation steps).
  2. Run:  python scripts/extract.py

Outputs (relative to repo root):
  docs/extracted-context/app-extraction/extraction-overview.md
  docs/extracted-context/app-extraction/pages/<slug>/screenshot.png
  docs/extracted-context/app-extraction/pages/<slug>/aria.yaml

Prerequisites:
  pip install pywinauto Pillow PyYAML
  # Fallback (if UIA not available):
  pip install pyautogui
"""

from __future__ import annotations

import json
import os
import time
import textwrap
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Primary: pywinauto (UIA-based — semantic element tree)
try:
    from pywinauto import Application, Desktop
    from pywinauto.controls.uiawrapper import UIAWrapper
    HAS_PYWINAUTO = True
except ImportError:
    HAS_PYWINAUTO = False

# Fallback: pyautogui (pixel-based — use only when UIA not available)
try:
    import pyautogui
    from PIL import ImageGrab
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False


# ---------------------------------------------------------------------------
# ✏️  CONFIGURE — fill these in for your application
# ---------------------------------------------------------------------------

APP_NAME = "my-desktop-app"               # used in extraction-overview.md title
PERSONA  = "Primary user persona"

# Path to the application executable
APP_EXE  = r"C:\Path\To\Your\App.exe"

# ✏️  Replace with your actual screens and navigation steps
PAGES: list[dict] = [
    {
        "slug":         "01-login",
        "view":         "Login Screen",
        "user_intent":  "Authenticate and gain access to the application.",
        "domain_focus": ["authentication"],
        "ux_focus":     ["login-form"],
        "notes":        "Entry screen. Username/password fields and Sign In button.",
        "nav_steps":    [],   # No navigation needed — this is the first screen
    },
    {
        "slug":         "02-home",
        "view":         "Home / Dashboard",
        "user_intent":  "Orient to the available features.",
        "domain_focus": [],
        "ux_focus":     ["dashboard", "sidebar"],
        "notes":        "Main window after login.",
        "nav_steps":    [
            # ✏️  Add navigation steps that open this screen, e.g.:
            # {"action": "click", "title": "Login", "control": "Sign In"}
        ],
    },
    # Add more screens here...
]


# ---------------------------------------------------------------------------
# Output paths — do not change
# ---------------------------------------------------------------------------

REPO_ROOT      = Path(__file__).resolve().parent.parent
EXTRACT_ROOT   = REPO_ROOT / "docs" / "extracted-context" / "app-extraction"
PAGES_DIR      = EXTRACT_ROOT / "pages"
PAGES_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Page model
# ---------------------------------------------------------------------------

@dataclass
class PageEntry:
    step_id:            str
    url_or_view:        str
    user_intent:        str
    domain_focus:       list[str]
    ux_focus:           list[str]
    aria_snapshot_file: str
    screenshot_file:    str
    network_summary:    list[str] = field(default_factory=list)
    notes:              str = ""


captured_pages: list[PageEntry] = []


# ---------------------------------------------------------------------------
# UIA tree dumper (pywinauto)
# ---------------------------------------------------------------------------

def dump_uia_tree(window, indent: int = 0) -> str:
    """
    Recursively dump the UIA element tree of `window` as YAML-like text.
    Captures: control_type, name/title, value, enabled state.
    """
    lines = []
    try:
        ctrl_type  = getattr(window, "control_type", lambda: "Unknown")()
        name       = getattr(window, "window_text", lambda: "")()
        is_enabled = getattr(window, "is_enabled",  lambda: True)()
        value      = ""
        try:
            value = window.legacy_properties().get("Value", "")
        except Exception:
            pass

        label = ctrl_type
        if name:
            label += f' "{name}"'
        if value:
            label += f" [{value}]"
        if not is_enabled:
            label += " (disabled)"

        lines.append("  " * indent + f"- {label}")
        for child in window.children():
            lines.append(dump_uia_tree(child, indent + 1))
    except Exception as exc:
        lines.append("  " * indent + f"- [error: {exc}]")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Capture helpers
# ---------------------------------------------------------------------------

def wait_for_render(seconds: float = 0.8) -> None:
    time.sleep(seconds)


def capture_page(window, page_cfg: dict, app) -> None:
    """
    Capture screenshot + UIA tree for `window`, then record a PageEntry.
    Falls back to pyautogui screenshot if pywinauto capture fails.
    """
    slug     = page_cfg["slug"]
    page_dir = PAGES_DIR / slug
    page_dir.mkdir(exist_ok=True)

    # Screenshot
    screenshot_path = page_dir / "screenshot.png"
    captured = False
    if HAS_PYWINAUTO:
        try:
            img = window.capture_as_image()
            img.save(str(screenshot_path))
            captured = True
        except Exception:
            pass
    if not captured and HAS_PYAUTOGUI:
        pyautogui.screenshot(str(screenshot_path))
        captured = True
    if not captured:
        print(f"  [WARN] Could not capture screenshot for {slug}")

    # UIA / accessibility tree → aria.yaml
    aria_path = page_dir / "aria.yaml"
    if HAS_PYWINAUTO:
        try:
            tree_text = dump_uia_tree(window)
            aria_path.write_text(tree_text, encoding="utf-8")
        except Exception as exc:
            aria_path.write_text(f"# UIA dump failed: {exc}\n", encoding="utf-8")
    else:
        aria_path.write_text("# pywinauto not available — install it for UIA tree\n", encoding="utf-8")

    captured_pages.append(PageEntry(
        step_id            = slug,
        url_or_view        = page_cfg["view"],
        user_intent        = page_cfg["user_intent"],
        domain_focus       = page_cfg["domain_focus"],
        ux_focus           = page_cfg["ux_focus"],
        aria_snapshot_file = f"./pages/{slug}/aria.yaml",
        screenshot_file    = f"./pages/{slug}/screenshot.png",
        notes              = page_cfg.get("notes", ""),
    ))
    print(f"  Captured: {slug}")


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------

def navigate(window, steps: list[dict]) -> None:
    """
    Execute a list of navigation steps, e.g.:
      {"action": "click",     "control": "Sign In"}
      {"action": "type_keys", "control": "Username", "keys": "user@example.com"}
      {"action": "wait",      "seconds": 1.0}
    """
    for step in steps:
        action = step.get("action", "")
        if action == "wait":
            time.sleep(step.get("seconds", 0.5))
        elif action == "click":
            try:
                ctrl_name = step["control"]
                window[ctrl_name].click_input()
                wait_for_render(0.4)
            except Exception as exc:
                print(f"  [WARN] click '{step['control']}' failed: {exc}")
        elif action == "type_keys":
            try:
                ctrl_name = step["control"]
                window[ctrl_name].type_keys(step.get("keys", ""), with_spaces=True)
                wait_for_render(0.2)
            except Exception as exc:
                print(f"  [WARN] type_keys '{step['control']}' failed: {exc}")


# ---------------------------------------------------------------------------
# Write extraction-overview.md
# ---------------------------------------------------------------------------

def write_overview() -> None:
    all_domain = sorted({t for p in captured_pages for t in p.domain_focus})
    all_ux     = sorted({t for p in captured_pages for t in p.ux_focus})

    lines = [
        f"# {APP_NAME} — Extraction Overview",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "Phase: scout (abd-context-app-extractor Phase 0)",
        "Source: scripts/extract.py via pywinauto.",
        "",
        "---",
        f"app: {APP_NAME}",
        'surface: "desktop"',
        'phase: "scout"',
        f'persona: "{PERSONA}"',
        'automation_tool: "pywinauto"',
        'pages_dir: "./pages/"',
        'primary_views: ["story", "domain", "ux"]',
        "tags:",
        f"  domain: [{', '.join(repr(t) for t in all_domain)}]",
        f"  ux:     [{', '.join(repr(t) for t in all_ux)}]",
        "---",
        "",
    ]

    for p in captured_pages:
        lines += [
            f"## {p.step_id} — {p.url_or_view}",
            "",
            f'- user_intent: "{p.user_intent}"',
            f'- domain_focus: [{", ".join(repr(t) for t in p.domain_focus)}]',
            f'- ux_focus: [{", ".join(repr(t) for t in p.ux_focus)}]',
            f'- aria_snapshot: "{p.aria_snapshot_file}"',
            f'- screenshot: "{p.screenshot_file}"',
            "- notes: |",
            *[f"  {line}" for line in p.notes.splitlines()],
            "",
            "---",
            "",
        ]

    out_path = EXTRACT_ROOT / "extraction-overview.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nExtraction overview: {out_path}")
    print(f"Pages:               {PAGES_DIR}/")
    print(f"Pages recorded:      {len(captured_pages)}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not HAS_PYWINAUTO:
        print("[ERROR] pywinauto not installed. Run: pip install pywinauto")
        return

    print(f"Launching: {APP_EXE}")
    app = Application(backend="uia").start(APP_EXE)
    wait_for_render(2.0)

    # Find the main window — adjust the title match as needed
    main_win = app.window(found_index=0)
    main_win.wait("visible", timeout=15)

    for page_cfg in PAGES:
        print(f"\n→ {page_cfg['slug']}: {page_cfg['view']}")
        navigate(main_win, page_cfg.get("nav_steps", []))
        wait_for_render(0.6)
        capture_page(main_win, page_cfg, app)

    write_overview()


if __name__ == "__main__":
    main()
