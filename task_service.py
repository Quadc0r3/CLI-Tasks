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
