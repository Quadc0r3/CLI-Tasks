"""
serialize.py – Persistenz: Lesen und Schreiben der tasks.json.
Entspricht Task 8 (Persistenzkonzept) des Projekts.
Keine Business-Logik – ausschließlich I/O und (De-)Serialisierung.
"""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

from models import Priority, Status, Task

_DEFAULT_DIR = Path.home() / ".tasktool"
_DATA_DIR    = Path(os.environ.get("TASKTOOL_DATA_DIR", _DEFAULT_DIR))
TASKS_FILE   = _DATA_DIR / "tasks.json"
_BACKUP_FILE = _DATA_DIR / "tasks.json.bak"
_TEMP_FILE   = _DATA_DIR / "tasks.json.tmp"

_EMPTY_STORE: dict = {"meta": {"version": "1.0", "last_id": 0}, "tasks": []}


def _ensure_dir() -> None:
    _DATA_DIR.mkdir(parents=True, exist_ok=True)


def _task_to_dict(task: Task) -> dict:
    return {
        "id":          task.id,
        "title":       task.title,
        "description": task.description,
        "priority":    task.priority.value,
        "status":      task.status.value,
        "created_at":  task.created_at,
        "updated_at":  task.updated_at,
        "done_at":     task.done_at,
        "tags":        task.tags,
    }


def _dict_to_task(data: dict) -> Task:
    return Task(
        id=          data["id"],
        title=       data["title"],
        description= data.get("description"),
        priority=    Priority(data["priority"]),
        status=      Status(data["status"]),
        created_at=  data["created_at"],
        updated_at=  data.get("updated_at"),
        done_at=     data.get("done_at"),
        tags=        data.get("tags", []),
    )


def read() -> tuple[list[Task], dict]:
    """Lädt tasks.json. Gibt (tasks, meta) zurück."""
    _ensure_dir()

    if not TASKS_FILE.exists():
        return [], dict(_EMPTY_STORE["meta"])

    with open(TASKS_FILE, encoding="utf-8") as f:
        try:
            store = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(
                f"Datei konnte nicht geladen werden – Format ungültig.\n"
                f"Backup verfügbar unter: {_BACKUP_FILE}"
            )

    tasks = [_dict_to_task(t) for t in store.get("tasks", [])]
    meta  = store.get("meta", dict(_EMPTY_STORE["meta"]))
    return tasks, meta


def write(tasks: list[Task], meta: dict) -> None:
    """Schreibt tasks atomar in tasks.json; erstellt vorher ein Backup."""
    _ensure_dir()

    if TASKS_FILE.exists():
        shutil.copy2(TASKS_FILE, _BACKUP_FILE)

    store = {
        "meta":  meta,
        "tasks": [_task_to_dict(t) for t in tasks],
    }

    with open(_TEMP_FILE, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)

    os.replace(_TEMP_FILE, TASKS_FILE)
