"""
task_service.py – Business-Logik für Task-Operationen zur Laufzeit.
"""

from __future__ import annotations

from datetime import datetime, timezone

import serialize
from models import ALLOWED_TRANSITIONS, Priority, Status, Task


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


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
    return task


def edit(title: str, description: str | None, priority: Priority, task_id: int) -> Task:
    """Bearbeitet einen Task und persistiert ihn."""
    tasks, meta = serialize.read()
    task = next((t for t in tasks if t.id == task_id), None)

    if task is None:
        raise ValueError(f"Task #{task_id} nicht gefunden.")

    task.title = title
    task.description = description
    task.priority = priority
    task.updated_at = _now()

    serialize.write(tasks, meta)
    return task


def get_task(task_id: int) -> Task | None:
    """Gibt einen einzelnen Task anhand der ID zurück, oder None."""
    tasks, _ = serialize.read()
    return next((t for t in tasks if t.id == task_id), None)


def set_status(task_id: int, target: Status) -> Task:
    """Setzt den Status eines Tasks – nur erlaubte Übergänge gemäß ALLOWED_TRANSITIONS."""
    tasks, meta = serialize.read()
    task = next((t for t in tasks if t.id == task_id), None)

    if task is None:
        raise ValueError(f"Task #{task_id} nicht gefunden.")

    if target not in ALLOWED_TRANSITIONS[task.status]:
        raise ValueError(
            f"Ungültiger Übergang: '{task.status.value}' → '{target.value}'."
        )

    task.status = target
    task.done_at = _now() if target is Status.DONE else None
    task.updated_at = _now()

    serialize.write(tasks, meta)
    return task