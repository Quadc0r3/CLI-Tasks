"""
task_service.py – Business-Logik für Task-Operationen zur Laufzeit.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

import serialize
from models import ALLOWED_TRANSITIONS, Priority, Status, Task

_logger = logging.getLogger(__name__)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def _find_task(tasks: list[Task], task_id: int) -> Task | None:
    """Sucht einen Task anhand der ID; gibt None zurück wenn nicht gefunden."""
    return next((t for t in tasks if t.id == task_id), None)


def create(title: str, description: str | None, priority: Priority) -> Task:
    """Erstellt einen neuen Task und persistiert ihn."""
    tasks, meta = serialize.read()

    meta["last_id"] += 1
    task = Task(
        id=          meta["last_id"],
        title=       title,
        description= description,
        priority=    priority,
        status=      Status.OPEN,
        created_at=_now(),
    )

    tasks.append(task)
    serialize.write(tasks, meta)
    _logger.info(
        "Task #%d '%s' erstellt (status: %s, priority: %s)",
        task.id, task.title, task.status.value, task.priority.value,
    )
    return task


def edit(title: str, description: str | None, priority: Priority, task_id: int) -> Task:
    """Bearbeitet einen Task und persistiert ihn."""
    tasks, meta = serialize.read()
    task = _find_task(tasks, task_id)

    if task is None:
        raise ValueError(f"Task #{task_id} nicht gefunden.")

    task.title = title
    task.description = description
    task.priority = priority
    task.updated_at = _now()

    serialize.write(tasks, meta)
    _logger.info(
        "Task #%d '%s' bearbeitet (status: %s, priority: %s)",
        task.id, task.title, task.status.value, task.priority.value,
    )
    return task


def get_task(task_id: int) -> Task | None:
    """Gibt einen einzelnen Task anhand der ID zurück, oder None."""
    tasks, _ = serialize.read()
    task = _find_task(tasks, task_id)
    if task is None:
        _logger.warning("Task #%d nicht gefunden", task_id)
    return task


def get_all_tasks() -> list[Task]:
    """Gibt alle Tasks zurück."""
    tasks, _ = serialize.read()
    if not tasks:
        _logger.warning("Keine Tasks gefunden")
    return tasks


def set_status(task_id: int, target: Status) -> Task:
    """Setzt den Status eines Tasks – nur erlaubte Übergänge gemäß ALLOWED_TRANSITIONS."""
    tasks, meta = serialize.read()
    task = _find_task(tasks, task_id)

    if task is None:
        _logger.error("Task #%d nicht gefunden", task_id)
        raise ValueError(f"Task #{task_id} nicht gefunden.")

    if target not in ALLOWED_TRANSITIONS[task.status]:
        _logger.error("Ungültiger Übergang: %s -> %s", task.status.value, target.value)
        raise ValueError(
            f"Ungültiger Übergang: '{task.status.value}' → '{target.value}'."
        )

    task.status = target
    task.done_at = _now() if target is Status.DONE else None
    task.updated_at = _now()

    serialize.write(tasks, meta)
    _logger.info(
        "Task #%d Status: %s -> %s", task.id, task.status.value, target.value
    )
    return task


def delete(task_id: int) -> Task:
    """Löscht einen Task anhand der ID. Gibt den gelöschten Task zurück."""
    tasks, meta = serialize.read()
    task = _find_task(tasks, task_id)

    if task is None:
        _logger.error("Task #%d nicht gefunden", task_id)
        raise ValueError(f"Task #{task_id} nicht gefunden.")

    tasks.remove(task)
    serialize.write(tasks, meta)
    _logger.info("Task #%d gelöscht", task_id)
    return task


def delete_done() -> int:
    """Löscht alle Tasks mit Status DONE. Gibt Anzahl gelöschter Tasks zurück."""
    tasks, meta = serialize.read()
    remaining = [t for t in tasks if t.status is not Status.DONE]
    count = len(tasks) - len(remaining)

    if count == 0:
        _logger.warning("Keine erledigten Tasks gefunden")

    serialize.write(remaining, meta)
    _logger.info("%d Tasks gelöscht", count)
    return count


def delete_all() -> int:
    """Löscht alle Tasks. Gibt Anzahl gelöschter Tasks zurück."""
    tasks, meta = serialize.read()
    count = len(tasks)
    serialize.write([], meta)
    _logger.info("%d Tasks gelöscht", count)
    return count