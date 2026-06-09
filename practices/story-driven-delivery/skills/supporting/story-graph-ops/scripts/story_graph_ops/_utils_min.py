"""Minimal utils vendored from agile_bots ``src/utils.py`` for story-graph-ops only."""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import List, Optional


def sanitize_json_string(text: str) -> str:
    """Remove invalid control characters from a string before JSON parse/serialize."""
    if not isinstance(text, str):
        return text
    return re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', text)


def _find_ast_node_line(file_path: Path, node_name: str, node_type: type) -> Optional[int]:
    if not file_path.exists() or not node_name or node_name == '?':
        return None
    try:
        content = file_path.read_text(encoding='utf-8')
        tree = ast.parse(content, filename=str(file_path))
        for node in ast.walk(tree):
            if isinstance(node, node_type) and node.name == node_name:
                return node.lineno
    except (SyntaxError, Exception):
        return None
    return None


def find_test_class_line(test_file_path: Path, test_class_name: str) -> Optional[int]:
    return _find_ast_node_line(test_file_path, test_class_name, ast.ClassDef)


def find_test_method_line(test_file_path: Path, test_method_name: str) -> Optional[int]:
    return _find_ast_node_line(test_file_path, test_method_name, ast.FunctionDef)


TEST_FILE_EXTENSIONS = (
    '.py', '.js', '.ts', '.tsx', '.jsx', '.mjs', '.cjs',
    '.spec.js', '.spec.ts', '.spec.tsx', '.test.ts', '.test.tsx',
    '.e2e.js', '.e2e.ts',
)


def name_to_test_stem(name: str) -> str:
    if not name or not name.strip():
        return ''
    s = name.strip().lower()
    if s.startswith('test '):
        s = s[5:].strip()
    s = re.sub(r'[^a-z0-9]+', '_', s).strip('_')
    if not s:
        return ''
    return f'test_{s}' if not s.startswith('test_') else s


def find_matching_test_files(
    test_dir: Path,
    pattern: str,
    under_path: Optional[str] = None,
) -> List[str]:
    if not pattern:
        return []
    search_dir = test_dir / under_path if under_path else test_dir
    if not search_dir.exists() or not search_dir.is_dir():
        return []
    seen_stems = set()
    result: List[str] = []
    for ext in TEST_FILE_EXTENSIONS:
        iterator = search_dir.glob(f'*{ext}') if under_path else search_dir.rglob(f'*{ext}')
        for path in iterator:
            if not path.is_file():
                continue
            stem = path.stem
            if not stem.startswith(pattern):
                continue
            rel = path.relative_to(test_dir)
            rel_str = str(rel).replace('\\', '/')
            if rel_str in seen_stems:
                continue
            seen_stems.add(rel_str)
            result.append(rel_str)
    result.sort()
    return result
