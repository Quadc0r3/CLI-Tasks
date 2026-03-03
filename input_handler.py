"""
input_handler.py – Eingabe-Verwaltung und Create-Wizard.
Validiert alle Nutzereingaben vor der Weitergabe an task_service.
"""

from __future__ import annotations

from models import Priority
import render

_PRIORITY_MAP: dict[str, Priority] = {
    "high": Priority.HIGH,
    "mid":  Priority.MEDIUM,
    "low":  Priority.LOW,
}
_PRIORITY_HINT = "high / mid / low"


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


def run_create_wizard() -> tuple[str, str | None, Priority]:
    """Interaktiver Wizard zum Erstellen eines Tasks. Gibt (title, description, priority) zurück."""
    print("\n  Neuen Task erstellen (* = Pflichtfeld)\n")
    title       = _ask_title()
    description = _ask_description()
    priority    = _ask_priority()
    return title, description, priority
