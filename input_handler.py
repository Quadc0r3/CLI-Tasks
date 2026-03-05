"""
input_handler.py – Eingabe-Verwaltung und Create-Wizard.
Validiert alle Nutzereingaben vor der Weitergabe an task_service.
"""

from __future__ import annotations

import argparse

import render
from models import Priority, Status

_PRIORITY_MAP: dict[str, Priority] = {
    "high": Priority.HIGH,
    "mid":  Priority.MEDIUM,
    "low":  Priority.LOW,
}
_PRIORITY_HINT = "high / mid / low"

_STATUS_MAP: dict[str, Status] = {
    "open": Status.OPEN,
    "inprog": Status.IN_PROGRESS,
    "done": Status.DONE,
    "reopen": Status.OPEN,
    "in_progress": Status.IN_PROGRESS,
}


def _prompt(label: str, required: bool = True, default: str = "") -> str:
    """Liest eine Eingabezeile vom Nutzer."""
    suffix = f" [{default}]" if default and not required else ""
    marker = " *" if required else ""
    return input(f"  {label}{marker}{suffix}: ").strip()


def _ask_title() -> str:
    while True:
        title = _prompt("Titel")
        if title:
            return title
        render.error("Titel darf nicht leer sein.")


def _ask_description() -> str | None:
    value = _prompt("Beschreibung (Enter zum Überspringen)", required=False)
    return value if value else None


def _ask_priority() -> Priority:
    while True:
        raw = _prompt(f"Priorität ({_PRIORITY_HINT})", required=False, default="mid")
        key = (raw or "mid").lower()
        if key in _PRIORITY_MAP:
            return _PRIORITY_MAP[key]
        render.error(f"Ungültige Priorität '{raw}'. Erlaubt: {_PRIORITY_HINT}")


def _ask_info() -> tuple[str, str | None, Priority]:
    title = _ask_title()
    description = _ask_description()
    priority = _ask_priority()
    return title, description, priority


def run_create_wizard() -> tuple[str, str | None, Priority]:
    """Interaktiver Wizard zum Erstellen eines Tasks. Gibt (title, description, priority) zurück."""
    print("\n  Neuen Task erstellen (* = Pflichtfeld)\n")
    return _ask_info()


def run_edit_wizard() -> tuple[str, str | None, Priority]:
    print("\n Task bearbeiten\n")
    return _ask_info()


def parse_status(status: str) -> Status:
    try:
        return _STATUS_MAP[status.lower()]
    except KeyError:
        render.error(f"Ungültiger Status '{status}'. Erlaubt: {', '.join(_STATUS_MAP.keys())}")
        raise argparse.ArgumentTypeError


def parse_priority(priority: str) -> Priority:
    try:
        return _PRIORITY_MAP[priority.lower()]
    except KeyError:
        render.error(f"Ungültige Priority '{priority}'. Erlaubt: {', '.join(_PRIORITY_MAP.keys())}")
        raise argparse.ArgumentTypeError
