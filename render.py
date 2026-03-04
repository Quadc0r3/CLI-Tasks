"""
render.py – Ausgabe an das CLI.
Zuständig für alle visuellen Darstellungen; keine Business-Logik.
"""

from __future__ import annotations

from models import Priority, Task

# ANSI-Farbcodes
_RESET  = "\033[0m"
_BOLD   = "\033[1m"
_RED    = "\033[31m"
_YELLOW = "\033[33m"
_GREEN  = "\033[32m"
_CYAN   = "\033[36m"
_DIM    = "\033[2m"


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


def task_edited(task: Task):
    """Bestätigungsausgabe nach erfolgreichem Bearbeiten eines Tasks."""
    print(f"\n{_BOLD}{_CYAN}✓ Task bearbeitet{_RESET}")
    show_task(task)


def show_task(task: Task) -> None:
    """Ausgabe eines Tasks."""
    prio_color = _priority_color(task.priority)
    print(f"  {_DIM}{'─' * 36}{_RESET}")
    print(f"  {_DIM}ID         {_RESET} {_BOLD}#{task.id}{_RESET}")
    print(f"  {_DIM}Titel      {_RESET} {task.title}")

    if task.description:
        print(f"  {_DIM}Beschr.    {_RESET} {task.description}")

    print(f"  {_DIM}Priorität  {_RESET} {prio_color}{task.priority.value}{_RESET}")
    print(f"  {_DIM}Status     {_RESET} {_CYAN}{task.status.value}{_RESET}")
    print(f"  {_DIM}Erstellt   {_RESET} {task.created_at}")

    if task.updated_at:
        print(f"  {_DIM}Bearbeitet {_RESET} {task.updated_at}")
    print()

def error(message: str) -> None:
    print(f"\n{_RED}{_BOLD}✗ Fehler:{_RESET} {message}\n")


def info(message: str) -> None:
    print(f"{_DIM}{message}{_RESET}")
