"""
task_tool.py – Einstiegspunkt der Anwendung.
Verwaltet das CLI-Routing via argparse und orchestriert die Module.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

import input_handler
import render
import task_service
from models import Priority, Status, Task

VERSION = "0.1.0"


# ─────────────────────────────────────────────────────────────────────────────
# Startup
# ─────────────────────────────────────────────────────────────────────────────

def _load_env() -> None:
    """Lädt Umgebungsvariablen aus einer optionalen .env-Datei."""
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _setup_logging() -> None:
    """Konfiguriert den Root-Logger anhand von Umgebungsvariablen."""
    level_name = os.environ.get("TASKTOOL_LOG", "WARNING").upper()
    level = getattr(logging, level_name, logging.WARNING)
    log_file = os.environ.get("TASKTOOL_LOG_FILE")
    if log_file:
        log_file = Path(log_file).expanduser()
    logging.basicConfig(
        level=level,
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=log_file,
        filemode="a",
    )


# ─────────────────────────────────────────────────────────────────────────────
# Argument Parser
# ─────────────────────────────────────────────────────────────────────────────

def _add_id_arg(parser: argparse.ArgumentParser, help_text: str) -> None:
    """Registriert das Pflicht-Argument 'id' an einem Subparser."""
    parser.add_argument("id", type=int, help=help_text)


def _register_task_commands(sub) -> None:
    """Registriert create / edit / show / done / reopen."""
    sub.add_parser("create", help="Erstelle einen neuen Task (öffnet interaktiven Wizard).")
    _add_id_arg(sub.add_parser("edit", help="Bearbeite einen Task."), "ID des Tasks.")
    _add_id_arg(sub.add_parser("show", help="Zeige Details eines Tasks."), "ID des Tasks.")
    _add_id_arg(sub.add_parser("done", help="Setze Task auf 'abgeschlossen'."), "ID des Tasks.")
    _add_id_arg(sub.add_parser("reopen", help="Setze Task auf 'offen'."), "ID des Tasks.")


def _register_list_command(sub) -> None:
    """Registriert list mit Filter- und Sortieroptionen."""
    p = sub.add_parser("list", help="Liste alle Tasks.")
    p.add_argument("--all", action="store_true",
                   help="Zeige auch abgeschlossene Tasks.")
    p.add_argument("--status", type=input_handler.parse_status, choices=list(Status),
                   help="Filtere nach Status (open, in_progress, done).")
    p.add_argument("--priority", type=input_handler.parse_priority, choices=list(Priority),
                   help="Filtere nach Priority (high, mid, low).")
    p.add_argument("--sort", choices=["id", "title", "status", "priority"],
                   help="Sortiere nach.")


def _register_delete_command(sub) -> None:
    """Registriert delete mit gegenseitig ausschließenden Optionen."""
    p = sub.add_parser("delete", help="Lösche einen oder mehrere Tasks.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("id", type=int, nargs="?", help="ID des zu löschenden Tasks.")
    g.add_argument("--all", action="store_true", help="Lösche alle Tasks.")
    g.add_argument("--done", action="store_true", help="Lösche alle erledigten Tasks.")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task_tool",
        description="CLI Task-Manager – verwalte deine Aufgaben im Terminal.",
        add_help=True,
    )
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {VERSION}")
    sub = parser.add_subparsers(dest="command")
    _register_task_commands(sub)
    _register_list_command(sub)
    _register_delete_command(sub)
    return parser


# ─────────────────────────────────────────────────────────────────────────────
# Command Handler
# ─────────────────────────────────────────────────────────────────────────────

def _cmd_create() -> None:
    title, description, priority = input_handler.run_create_wizard()
    render.task_created(task_service.create(title, description, priority))


def _cmd_edit(task_id: int) -> None:
    # Bug-Fix T18: Existenz prüfen VOR der Edit-Maske
    task = task_service.get_task(task_id)
    if task is None:
        render.error(f"Task #{task_id} nicht gefunden.")
        return
    render.show_task(task)
    title, description, priority = input_handler.run_edit_wizard()
    render.task_edited(task_service.edit(title, description, priority, task_id))


def _cmd_show(task_id: int) -> None:
    task = task_service.get_task(task_id)
    if task is None:
        render.error(f"Task #{task_id} nicht gefunden.")
        return
    render.show_task(task)


def _cmd_set_status(task_id: int, target: Status) -> None:
    try:
        render.task_status_changed(task_service.set_status(task_id, target))
    except ValueError as exc:
        render.error(str(exc))


def _filter_tasks(tasks: list[Task], args) -> list[Task]:
    """Filtert Tasks anhand der list-Argumente."""
    if not args.all:
        tasks = [t for t in tasks if t.status != Status.DONE]
    if args.status:
        tasks = [t for t in tasks if t.status == args.status]
    if args.priority:
        tasks = [t for t in tasks if t.priority == args.priority]
    return tasks


def _sort(tasks: list[Task], sort_by: str) -> list[Task]:
    return sorted(
        tasks,
        key=lambda t: getattr(t, sort_by),
        reverse=sort_by in ("id", "priority", "title", "status"),
    )


def _cmd_list(args) -> None:
    render.show_tasks(_sort(_filter_tasks(task_service.get_all_tasks(), args), args.sort or "id"))


def _cmd_delete_all() -> None:
    """Löscht alle Tasks nach Bestätigung."""
    tasks = task_service.get_all_tasks()
    if not tasks:
        render.info("Keine Tasks vorhanden.")
        return
    render.info(f"  {len(tasks)} Task(s) werden gelöscht.")
    if not input_handler.confirm_delete("Alle Tasks unwiderruflich löschen?"):
        render.info("Abgebrochen.")
        return
    render.tasks_deleted(task_service.delete_all())


def _cmd_delete_done() -> None:
    """Löscht alle erledigten Tasks nach Bestätigung."""
    done_tasks = [t for t in task_service.get_all_tasks() if t.status is Status.DONE]
    if not done_tasks:
        render.info("Keine erledigten Tasks vorhanden.")
        return
    render.info(f"  {len(done_tasks)} erledigte(r) Task(s) werden gelöscht.")
    if not input_handler.confirm_delete("Alle erledigten Tasks löschen?"):
        render.info("Abgebrochen.")
        return
    render.tasks_deleted(task_service.delete_done())


def _cmd_delete_by_id(task_id: int) -> None:
    """Löscht einen einzelnen Task nach Bestätigung."""
    task = task_service.get_task(task_id)
    if task is None:
        render.error(f"Task #{task_id} nicht gefunden.")
        return
    render.show_task(task)
    if not input_handler.confirm_delete(f"Task #{task_id} unwiderruflich löschen?"):
        render.info("Abgebrochen.")
        return
    try:
        render.task_deleted(task_service.delete(task_id))
    except ValueError as exc:
        render.error(str(exc))


def _cmd_delete(args) -> None:
    if args.all:
        _cmd_delete_all()
    elif args.done:
        _cmd_delete_done()
    else:
        _cmd_delete_by_id(args.id)


# ─────────────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    _load_env()
    _setup_logging()
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
        "delete": lambda: _cmd_delete(args),
    }

    try:
        switch.get(args.command, parser.print_help)()
    except KeyboardInterrupt:
        render.info("\nAbgebrochen.")
    except (ValueError, PermissionError) as exc:
        render.error(str(exc))


if __name__ == "__main__":
    main()