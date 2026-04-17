"""Minimal rule object for scanner_bases without a host bot ``actions.rules`` dependency."""
from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class RuleLike(Protocol):
    """Anything :class:`scanner_bases.violation.Violation` accepts (``name`` + ``rule_file``)."""

    name: str
    rule_file: str


class SimpleRule:
    """Use when running scanners from ``run_scanners.py`` without the full bot Rule type."""

    __slots__ = ("name", "rule_file")

    def __init__(self, name: str, rule_file: str = "") -> None:
        self.name = name
        self.rule_file = rule_file
