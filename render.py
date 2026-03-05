"""
render.py – Ausgabe an das CLI.
Zuständig für alle visuellen Darstellungen; keine Business-Logik.
"""

from __future__ import annotations

from models import Priority, Status, Task

# ANSI-Farbcodes
_RESET  = "\033[0m"
_BOLD   = "\033[1m"
_RED    = "\033[31m"
_YELLOW = "\033[33m"
_GREEN  = "\033[32m"
_CYAN   = "\033[36m"
_DIM    = "\033[2m"

_STATUS_COLOR: dict[Status, str] = {
    Status.OPEN: _YELLOW,
    Status.IN_PROGRESS: _CYAN,
    Status.DONE: _GREEN,
}


def _priority_color(priority: Priority) -> str:
    return {
        Priority.HIGH:   _RED,
        Priority.MEDIUM: _YELLOW,
        Priority.LOW:    _GREEN,
    }[priority]


def task_created(task: Task) -> None:
    """Bestätigungsausgabe nach erfolgreichem Erstellen eines Tasks."""
    print(f"\n{_BOLD}{_GREEN}✓ Task erstellt{_RESET}")
    show_task(task)


def task_edited(task: Task) -> None:
    """Bestätigungsausgabe nach erfolgreichem Bearbeiten eines Tasks."""
    print(f"\n{_BOLD}{_CYAN}✓ Task bearbeitet{_RESET}")
    show_task(task)


def task_status_changed(task: Task) -> None:
    """Bestätigungsausgabe nach erfolgreichem Statuswechsel."""
    status_color = _STATUS_COLOR[task.status]
    print(f"\n{_BOLD}{status_color}✓ Status geändert → {task.status.value}{_RESET}")
    show_task(task)


def show_tasks(tasks: list[Task]) -> None:
    """Ausgabe aller Tasks."""
    for task in tasks:
        show_task(task)


def show_task(task: Task) -> None:
    """Ausgabe eines Tasks."""
    prio_color = _priority_color(task.priority)
    status_color = _STATUS_COLOR[task.status]
    print(f"  {_DIM}{'─' * 36}{_RESET}")
    print(f"  {_DIM}ID         {_RESET} {_BOLD}#{task.id}{_RESET}")
    print(f"  {_DIM}Titel      {_RESET} {task.title}")

    if task.description:
        print(f"  {_DIM}Beschr.    {_RESET} {task.description}")

    print(f"  {_DIM}Priorität  {_RESET} {prio_color}{task.priority.value}{_RESET}")
    print(f"  {_DIM}Status     {_RESET} {status_color}{task.status.value}{_RESET}")
    print(f"  {_DIM}Erstellt   {_RESET} {task.created_at}")

    if task.updated_at:
        print(f"  {_DIM}Bearbeitet {_RESET} {task.updated_at}")

    if task.done_at:
        print(f"  {_DIM}Erledigt   {_RESET} {task.done_at}")

    print()


def error(message: str) -> None:
    print(f"\n{_RED}{_BOLD}✗ Fehler:{_RESET} {message}\n")


def info(message: str) -> None:
    print(f"{_DIM}{message}{_RESET}")