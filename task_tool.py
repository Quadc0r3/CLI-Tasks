"""
task_tool.py – Einstiegspunkt der Anwendung.
Verwaltet das CLI-Routing via argparse und orchestriert die Module.
"""

from __future__ import annotations

import argparse
import sys

import input_handler
import render
import task_service

VERSION = "0.1.0"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task_tool",
        description="CLI Task-Manager – verwalte deine Aufgaben im Terminal.",
        add_help=True,
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "create",
        help="Erstelle einen neuen Task (öffnet interaktiven Wizard).",
    )

    return parser


def _cmd_create() -> None:
    title, description, priority = input_handler.run_create_wizard()
    task = task_service.create(title, description, priority)
    render.task_created(task)


def main() -> None:
    parser = _build_parser()

    # Kein Argument → help anzeigen (gemäß CLI-Interaktionsdesign)
    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    if args.command == "create":
        _cmd_create()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
