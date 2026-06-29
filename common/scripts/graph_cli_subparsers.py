"""Shared argparse subparser registration for graph-ops CLIs."""
from __future__ import annotations

from argparse import _SubParsersAction
from typing import Callable


def add_read_parser(
    sub: _SubParsersAction,
    *,
    command_handler: Callable,
    help_text: str = "Load, validate, and print JSON",
) -> None:
    read_parser = sub.add_parser("read", help=help_text)
    read_parser.add_argument("--file", required=True)
    read_parser.add_argument("--pretty", action="store_true")
    read_parser.set_defaults(func=command_handler)


def add_names_parser(sub: _SubParsersAction, *, command_handler: Callable, help_text: str) -> None:
    names_parser = sub.add_parser("names", help=help_text)
    names_parser.add_argument("--file", required=True)
    names_parser.set_defaults(func=command_handler)


def add_search_parser(sub: _SubParsersAction, *, command_handler: Callable, help_text: str) -> None:
    search_parser = sub.add_parser("search", help=help_text)
    search_parser.add_argument("--file", required=True)
    search_parser.add_argument("--substring", required=True)
    search_parser.set_defaults(func=command_handler)


def add_sha_parser(sub: _SubParsersAction, *, command_handler: Callable, help_text: str) -> None:
    sha_parser = sub.add_parser("sha", help=help_text)
    sha_parser.add_argument("--file", required=True)
    sha_parser.set_defaults(func=command_handler)


def add_write_parser(sub: _SubParsersAction, *, command_handler: Callable, help_text: str) -> None:
    write_parser = sub.add_parser("write", help=help_text)
    write_parser.add_argument("--file", required=True)
    write_parser.add_argument("--input", default="-")
    write_parser.add_argument("--expect-sha", dest="expect_sha", default=None)
    write_parser.add_argument("--no-lock", dest="no_lock", action="store_true")
    write_parser.add_argument("--force", action="store_true")
    write_parser.set_defaults(func=command_handler)
