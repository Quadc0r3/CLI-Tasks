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

# Setup
_TASKS_FILE = "tasks_.json"
_DEFAULT_FOLDER = ".tasktool"
_DEFAULT_PATH = Path.home() / _DEFAULT_FOLDER
_DEFAULT_FILE_PATH = _DEFAULT_PATH / _TASKS_FILE
_DEFAULT_BACKUP_PATH = _DEFAULT_PATH / f"{_TASKS_FILE}.bak"
_DEFAULT_TEMP_PATH = _DEFAULT_PATH / f"{_TASKS_FILE}.tmp"

_EMPTY_TASK: dict = {"meta":
                         {"version": "0.1.0",
                          "last_id": 0,
                          },
                     "tasks": []}

_logger = logging.getLogger(__name__)

def read() -> tuple[list[Task], dict]:
    _path_exists()

    if not _DEFAULT_FILE_PATH.exists():
        _logger.debug("Keine Datei gefunden unter %s – leere Struktur", _DEFAULT_FILE_PATH)
        return _EMPTY_TASK["tasks"], _EMPTY_TASK["meta"]

    _logger.debug("Lese %s", _DEFAULT_FILE_PATH)

    with open(_DEFAULT_FILE_PATH, "r", encoding="utf-8") as f:
        try:
            json_data = json.load(f)
        except json.JSONDecodeError as exc:
            _logger.error("JSON-Fehler in %s: %s", _DEFAULT_FILE_PATH, exc)
            render.error(f"Fehler beim Laden der Datei: {exc}.\nVerwende {_DEFAULT_BACKUP_PATH} als Backup.")
            return _EMPTY_TASK["tasks"], _EMPTY_TASK["meta"]

    tasks = [Task.from_dict(t) for t in json_data.get("tasks", [])]
    meta = json_data.get("meta", _EMPTY_TASK["meta"])

    _logger.debug("Gelesene Tasks: %s", len(tasks))
    return tasks, meta


def _path_exists():
    if not _DEFAULT_PATH.exists():
        _DEFAULT_PATH.mkdir(parents=True)


def write(tasks: list[Task], meta: dict) -> None:
    _path_exists()

    if _DEFAULT_FILE_PATH.exists():
        shutil.copy(_DEFAULT_FILE_PATH, _DEFAULT_BACKUP_PATH)

    json_data = {"meta": meta, "tasks": [t.to_dict() for t in tasks]}

    with open(_DEFAULT_TEMP_PATH, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)

    os.replace(_DEFAULT_TEMP_PATH, _DEFAULT_FILE_PATH)
    _logger.info("Gespeichert: %s (%d Tasks)", _DEFAULT_FILE_PATH, len(tasks))
