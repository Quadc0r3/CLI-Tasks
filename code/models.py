"""
models.py – Datenmodell: Task-Entity und Enumerations.
Entspricht Task 6 (Datenmodell) des Projekts.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum


class Priority(Enum):
    HIGH   = "hoch"
    MEDIUM = "mittel"
    LOW    = "niedrig"


class Status(Enum):
    OPEN        = "offen"
    IN_PROGRESS = "in Bearbeitung"
    DONE        = "abgeschlossen"


# Erlaubte Statusübergänge gemäß Datenmodell (Task 6)
ALLOWED_TRANSITIONS: dict[Status, set[Status]] = {
    Status.OPEN: {Status.IN_PROGRESS, Status.DONE},
    Status.IN_PROGRESS: {Status.DONE},
    Status.DONE: {Status.OPEN},
}


@dataclass
class Task:
    id:          int
    title:       str
    description: str | None
    priority:    Priority
    status:      Status
    created_at:  str
    updated_at:  str | None = None
    done_at:     str | None = None
    tags:        list[str]  = field(default_factory=list)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["priority"] = self.priority.value
        data["status"] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Task:
        d = data.copy()
        d["priority"] = Priority(d["priority"])
        d["status"] = Status(d["status"])
        return cls(**d)