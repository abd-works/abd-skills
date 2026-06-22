"""
Generic scanner infrastructure: abstract ``Scanner``, violations, rules protocol, scan context.

No story-graph domain here — **story-graph-ops** ``scripts/story_scanner.py`` supplies
:class:`story_scanner.StoryScanner`, extending :class:`scanner_bases.scanner.Scanner`.
"""

from __future__ import annotations

from scanner_bases.scanner import Scanner
from scanner_bases.violation import Violation
from scanner_bases.simple_rule import SimpleRule, RuleLike
from scanner_bases.resources.scan_context import (
    ScanContext,
    FileCollection,
    FileScanContext,
    ScanFilesContext,
    CrossFileScanContext,
)
from scanner_bases.eval_paths import EvalPaths

__all__ = [
    "Scanner",
    "Violation",
    "SimpleRule",
    "RuleLike",
    "ScanContext",
    "FileCollection",
    "FileScanContext",
    "ScanFilesContext",
    "CrossFileScanContext",
    "EvalPaths",
]
