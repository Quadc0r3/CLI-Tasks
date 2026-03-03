"""
models.py – Datenmodell: Task-Entity und Enumerations.
Entspricht Task 6 (Datenmodell) des Projekts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Priority(Enum):
    HIGH   = "hoch"
    MEDIUM = "mittel"
    LOW    = "niedrig"


class Status(Enum):
    OPEN        = "offen"
    IN_PROGRESS = "in Bearbeitung"
    DONE        = "abgeschlossen"


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
