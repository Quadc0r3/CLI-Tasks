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
from models import Status, Priority, Task

VERSION = "0.1.13"


def _add_id_arg(parser: argparse.ArgumentParser, help_text: str) -> None:
    """Registriert das Pflicht-Argument 'id' an einem Subparser."""
    parser.add_argument("id", type=int, help=help_text)


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

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("create", help="Erstelle einen neuen Task (öffnet interaktiven Wizard).")
    _add_id_arg(sub.add_parser("edit", help="Bearbeite einen Task."), "ID des Tasks.")
    _add_id_arg(sub.add_parser("show", help="Zeige Details eines Tasks."), "ID des Tasks.")
    _add_id_arg(sub.add_parser("done", help="Setze Task auf 'abgeschlossen'."), "ID des Tasks.")
    _add_id_arg(sub.add_parser("reopen", help="Setze Task auf 'offen'."), "ID des Tasks.")

    list_parser = sub.add_parser("list", help="Liste alle Tasks.")
    list_parser.add_argument("--all", action="store_true", help="Zeige auch abgeschlossene Tasks.")
    list_parser.add_argument("--status", type=input_handler.parse_status, choices=list(Status),
                             help="Filtere nach Status (open, in_progress, done).")
    list_parser.add_argument("--priority", type=input_handler.parse_priority, choices=list(Priority),
                             help="Filtere nach Priority (high, mid, low).")
    list_parser.add_argument("--sort", choices=["id", "title", "status", "priority"], help="Sortiere nach.")
    # list_parser.add_argument("--search", help="Suche nach Titel, Beschreibung oder Tags.")

    return parser


def _cmd_create() -> None:
    title, description, priority = input_handler.run_create_wizard()
    task = task_service.create(title, description, priority)
    render.task_created(task)


def _cmd_edit(task_id: int) -> None:
    _cmd_show(task_id)
    title, description, priority = input_handler.run_edit_wizard()
    task = task_service.edit(title, description, priority, task_id)
    render.task_edited(task)


def _cmd_show(task_id: int) -> None:
    task = task_service.get_task(task_id)
    if task is None:
        render.error(f"Task #{task_id} nicht gefunden.")
        return
    render.show_task(task)


def _cmd_set_status(task_id: int, target: Status) -> None:
    try:
        task = task_service.set_status(task_id, target)
        render.task_status_changed(task)
    except ValueError as exc:
        render.error(str(exc))


def _cmd_list(args) -> None:
    tasks = task_service.get_all_tasks()
    if tasks is None:
        render.error("Keine Tasks gefunden.")
        return

    # Task-Filterung
    if not args.all:
        tasks = [t for t in tasks if t.status != Status.DONE]
    if args.status:
        tasks = [t for t in tasks if t.status == args.status]
    if args.priority:
        tasks = [t for t in tasks if t.priority == args.priority]

    # Task-Sortierung
    _sort(tasks, args.sort or "id")

    render.show_tasks(tasks)


def _sort(tasks: list[Task], sort_by: str) -> list[Task]:
    return sorted(
        tasks,
        key=lambda t: getattr(t, sort_by),
        reverse=sort_by in ("id", "priority", "title", "status"),
    )

def main() -> None:
    parser = _build_parser()

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    switch = {
        "create": lambda: _cmd_create(),
        "edit": lambda: _cmd_edit(args.id),
        "show": lambda: _cmd_show(args.id),
        "done": lambda: _cmd_set_status(args.id, Status.DONE),
        "reopen": lambda: _cmd_set_status(args.id, Status.OPEN),
        "list": lambda: _cmd_list(args),
    }

    command_function = switch.get(args.command, parser.print_help)
    command_function()


if __name__ == "__main__":
    main()