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

import render
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
    _ensure_dir()

    if not _file_path.exists():
        _logger.debug("Keine Datei gefunden unter %s – leere Struktur", _file_path)
        return list(_EMPTY["tasks"]), dict(_EMPTY["meta"])

    _logger.debug("Lese %s", _file_path)

    with open(_file_path, "r", encoding="utf-8") as f:
        try:
            json_data = json.load(f)
        except json.JSONDecodeError as exc:
            _logger.error("JSON-Fehler in %s: %s", _file_path, exc)
            render.error(
                f"Fehler beim Laden der Datei: {exc}.\n"
                f"Verwende {_backup_path} als Backup."
            )
            return list(_EMPTY["tasks"]), dict(_EMPTY["meta"])

    tasks = [Task.from_dict(t) for t in json_data.get("tasks", [])]
    meta = json_data.get("meta", dict(_EMPTY["meta"]))

    _logger.debug("Gelesene Tasks: %s", len(tasks))
    return tasks, meta


def _ensure_dir() -> None:
    _base_path.mkdir(parents=True, exist_ok=True)


def write(tasks: list[Task], meta: dict) -> None:
    _ensure_dir()

    if _file_path.exists():
        shutil.copy(_file_path, _backup_path)

    json_data = {"meta": meta, "tasks": [t.to_dict() for t in tasks]}

    with open(_temp_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)

    os.replace(_temp_path, _file_path)
    _logger.info("Gespeichert: %s (%d Tasks)", _file_path, len(tasks))
