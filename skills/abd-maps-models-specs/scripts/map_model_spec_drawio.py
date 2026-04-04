# Vendored API: implementation lives in agilebydesign-skills ``src/drawio/model_to_drawio.py``
# (UML class diagram — ``CLASS_STYLE`` / ``build_class_html``). Not story-map epic/sub-epic styling.
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_DRAWIO_SRC = _REPO_ROOT / "src" / "drawio"
if str(_DRAWIO_SRC) not in sys.path:
    sys.path.insert(0, str(_DRAWIO_SRC))

from model_to_drawio import map_model_spec_to_drawio_xml, write_map_model_class_diagram

__all__ = ["map_model_spec_to_drawio_xml", "write_map_model_class_diagram"]
