"""
task_service.py – Business-Logik für Task-Operationen zur Laufzeit.
Aktuell implementiert: create.
"""

from __future__ import annotations

from datetime import datetime, timezone

import serialize
from models import Priority, Status, Task


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
        created_at=  datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
    )

    tasks.append(task)
    serialize.write(tasks, meta)
    return task


def edit(title: str, description: str | None, priority: Priority, task_id: int) -> Task:
    """Bearbeitet einen Task und persistiert ihn."""
    tasks, meta = serialize.read()
    current_task = tasks.pop(tasks.index(get_task(task_id)))

    task = current_task
    task.title = title
    task.description = description
    task.priority = priority
    task.updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

    tasks.append(task)
    serialize.write(tasks, meta)
    return task


def get_task(task_id: int) -> Task:
    tasks, meta = serialize.read()
    task = next(filter(lambda t: t.id == task_id, tasks), None)
    return task
