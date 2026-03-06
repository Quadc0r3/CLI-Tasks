"""
serialize.py – Persistenz: Lesen und Schreiben der tasks.json.
Entspricht Task 8 (Persistenzkonzept) des Projekts.
Keine Business-Logik – ausschließlich I/O und (De-)Serialisierung.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
from pathlib import Path

from models import Task

_TASKS_FILE = "tasks_.json"
_DEFAULT_PATH = Path.home() / ".tasktool"

_base_path = _DEFAULT_PATH
_file_path = _base_path / _TASKS_FILE
_backup_path = _base_path / f"{_TASKS_FILE}.bak"
_temp_path = _base_path / f"{_TASKS_FILE}.tmp"

_EMPTY: dict = {"meta": {"version": "0.1.0", "last_id": 0}, "tasks": []}

_logger = logging.getLogger(__name__)


def configure(base_path: Path) -> None:
    """Überschreibt den Basis-Pfad – ausschließlich für Tests."""
    global _base_path, _file_path, _backup_path, _temp_path
    _base_path = base_path
    _file_path = base_path / _TASKS_FILE
    _backup_path = base_path / f"{_TASKS_FILE}.bak"
    _temp_path = base_path / f"{_TASKS_FILE}.tmp"


def read() -> tuple[list[Task], dict]:
    """Liest Tasks und Meta aus der JSON-Datei.
    Raises ValueError bei beschädigter Datei, PermissionError bei fehlenden Rechten.
    """
    _ensure_dir()

    if not _file_path.exists():
        _logger.debug("Keine Datei gefunden unter %s – leere Struktur", _file_path)
        return list(_EMPTY["tasks"]), dict(_EMPTY["meta"])

    _logger.debug("Lese %s", _file_path)

    try:
        with open(_file_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
    except json.JSONDecodeError as exc:
        _logger.error("JSON-Fehler in %s: %s", _file_path, exc)
        raise ValueError(
            f"Datei '{_file_path}' ist beschädigt. Backup: {_backup_path}"
        ) from exc
    except PermissionError as exc:
        _logger.error("Keine Leseberechtigung für %s", _file_path)
        raise PermissionError(f"Keine Leseberechtigung für '{_file_path}'.") from exc

    tasks = _parse_tasks(json_data.get("tasks", []))
    meta = _sanitize_meta(json_data.get("meta", dict(_EMPTY["meta"])), tasks)

    _logger.debug("Gelesene Tasks: %d", len(tasks))
    return tasks, meta


def _parse_tasks(raw: list[dict]) -> list[Task]:
    """Deserialisiert Tasks; überspringt ungültige Einträge."""
    tasks = []
    for entry in raw:
        try:
            tasks.append(Task.from_dict(entry))
        except (KeyError, ValueError, TypeError) as exc:
            _logger.error("Ungültiger Task-Eintrag übersprungen: %s", exc)
    return tasks


def _sanitize_meta(meta: dict, tasks: list[Task]) -> dict:
    """Korrigiert negative oder inkonsistente last_id."""
    last_id = max(0, meta.get("last_id", 0))
    if tasks:
        last_id = max(last_id, max(t.id for t in tasks))
    meta["last_id"] = last_id
    return meta


def _ensure_dir() -> None:
    """Erstellt das Datenverzeichnis falls nötig."""
    try:
        _base_path.mkdir(parents=True, exist_ok=True)
    except PermissionError as exc:
        raise PermissionError(
            f"Keine Schreibberechtigung für Verzeichnis '{_base_path}'."
        ) from exc


def write(tasks: list[Task], meta: dict) -> None:
    """Schreibt Tasks und Meta atomar in die JSON-Datei.
    Raises PermissionError bei fehlenden Schreibrechten.
    """
    _ensure_dir()
    json_data = {"meta": meta, "tasks": [t.to_dict() for t in tasks]}
    try:
        if _file_path.exists():
            shutil.copy(_file_path, _backup_path)
        with open(_temp_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)
        os.replace(_temp_path, _file_path)
    except PermissionError as exc:
        _logger.error("Keine Schreibberechtigung: %s", exc)
        raise PermissionError(f"Keine Schreibberechtigung für '{_file_path}'.") from exc
    _logger.info("Gespeichert: %s (%d Tasks)", _file_path, len(tasks))