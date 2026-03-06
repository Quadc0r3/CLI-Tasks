"""
tests/test_task_service.py – Unit-Tests für task_service und serialize.

Struktur:
  - Fixtures (conftest-Stil, lokal definiert)
  - TestSerialize   – read/write mit echtem tmp-Verzeichnis
  - TestCreate      – task_service.create()
  - TestEdit        – task_service.edit()
  - TestGetTask     – task_service.get_task() / get_all_tasks()
  - TestSetStatus   – task_service.set_status() inkl. Übergangsprüfung
  - TestDelete      – task_service.delete()
  - TestDeleteDone  – task_service.delete_done()
  - TestDeleteAll   – task_service.delete_all()

Isolierung:
  - serialize-Tests nutzen tmp_path (echtes Dateisystem, isoliert)
  - service-Tests mocken serialize.read / serialize.write vollständig
    → kein Dateisystem, kein Home-Verzeichnis involviert
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

import serialize
import task_service
from models import ALLOWED_TRANSITIONS, Priority, Status, Task


# ─────────────────────────────────────────────────────────────────────────────
# Hilfsfunktionen
# ─────────────────────────────────────────────────────────────────────────────

def make_task(
        id: int = 1,
        title: str = "Test-Task",
        description: str | None = None,
        priority: Priority = Priority.MEDIUM,
        status: Status = Status.OPEN,
        created_at: str = "2026-01-01T00:00:00",
        updated_at: str | None = None,
        done_at: str | None = None,
) -> Task:
    """Erstellt einen Task mit sinnvollen Standardwerten."""
    return Task(
        id=id,
        title=title,
        description=description,
        priority=priority,
        status=status,
        created_at=created_at,
        updated_at=updated_at,
        done_at=done_at,
    )


def make_meta(last_id: int = 1) -> dict:
    return {"version": "0.1.0", "last_id": last_id}


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_serialize_paths(tmp_path):
    """
    Konfiguriert serialize vor jedem Test auf ein isoliertes tmp-Verzeichnis
    und stellt danach den Original-Pfad wieder her.
    Gilt für alle Tests (autouse=True).
    """
    serialize.configure(tmp_path / "tasktool")
    yield
    serialize.configure(Path.home() / ".tasktool")


@pytest.fixture
def one_task() -> tuple[list[Task], dict]:
    """Ein einzelner offener Task + passendes Meta-Dict."""
    task = make_task(id=1, title="Einkaufen", priority=Priority.HIGH)
    return [task], make_meta(last_id=1)


@pytest.fixture
def three_tasks() -> tuple[list[Task], dict]:
    """Drei Tasks mit unterschiedlichem Status."""
    tasks = [
        make_task(id=1, title="Alpha", status=Status.OPEN, priority=Priority.HIGH),
        make_task(id=2, title="Beta", status=Status.IN_PROGRESS, priority=Priority.MEDIUM),
        make_task(id=3, title="Gamma", status=Status.DONE, priority=Priority.LOW),
    ]
    return tasks, make_meta(last_id=3)


# ─────────────────────────────────────────────────────────────────────────────
# TestSerialize – echtes Dateisystem via tmp_path
# ─────────────────────────────────────────────────────────────────────────────

class TestSerialize:

    def test_read_returns_empty_when_no_file_exists(self, tmp_path):
        serialize.configure(tmp_path / "fresh")
        tasks, meta = serialize.read()
        assert tasks == []
        assert meta["last_id"] == 0

    def test_write_then_read_roundtrip(self, tmp_path):
        serialize.configure(tmp_path / "rw")
        task = make_task(id=1, title="Roundtrip", priority=Priority.HIGH)
        meta = make_meta(last_id=1)

        serialize.write([task], meta)
        tasks_back, meta_back = serialize.read()

        assert len(tasks_back) == 1
        assert tasks_back[0].id == 1
        assert tasks_back[0].title == "Roundtrip"
        assert tasks_back[0].priority == Priority.HIGH
        assert meta_back["last_id"] == 1

    def test_write_creates_backup_on_second_write(self, tmp_path):
        base = tmp_path / "backup_test"
        serialize.configure(base)
        task = make_task(id=1)
        meta = make_meta(last_id=1)

        serialize.write([task], meta)  # erste Datei
        serialize.write([task], meta)  # soll Backup anlegen

        assert (base / "tasks_.json.bak").exists()

    def test_read_invalid_json_returns_empty(self, tmp_path):
        base = tmp_path / "corrupt"
        serialize.configure(base)
        base.mkdir(parents=True)
        (base / "tasks_.json").write_text("{ kein gültiges json !!!}", encoding="utf-8")

        tasks, meta = serialize.read()

        assert tasks == []
        assert meta["last_id"] == 0

    def test_write_stores_correct_json_structure(self, tmp_path):
        base = tmp_path / "structure"
        serialize.configure(base)
        task = make_task(id=5, title="Struktur-Test", priority=Priority.LOW)
        meta = make_meta(last_id=5)

        serialize.write([task], meta)

        raw = json.loads((base / "tasks_.json").read_text(encoding="utf-8"))
        assert raw["meta"]["last_id"] == 5
        assert len(raw["tasks"]) == 1
        assert raw["tasks"][0]["title"] == "Struktur-Test"
        assert raw["tasks"][0]["priority"] == Priority.LOW.value

    def test_roundtrip_preserves_all_fields(self, tmp_path):
        base = tmp_path / "fields"
        serialize.configure(base)
        task = make_task(
            id=7,
            title="Vollständig",
            description="Mit Beschreibung",
            priority=Priority.HIGH,
            status=Status.DONE,
            created_at="2026-03-01T10:00:00",
            updated_at="2026-03-02T11:00:00",
            done_at="2026-03-02T11:00:00",
        )
        serialize.write([task], make_meta(last_id=7))
        tasks_back, _ = serialize.read()

        t = tasks_back[0]
        assert t.description == "Mit Beschreibung"
        assert t.status == Status.DONE
        assert t.done_at == "2026-03-02T11:00:00"
        assert t.updated_at == "2026-03-02T11:00:00"


# ─────────────────────────────────────────────────────────────────────────────
# TestCreate
# ─────────────────────────────────────────────────────────────────────────────

class TestCreate:

    def test_create_returns_task_with_correct_fields(self):
        empty_meta = make_meta(last_id=0)
        with patch("serialize.read", return_value=([], empty_meta)), \
                patch("serialize.write") as mock_write:
            task = task_service.create("Neuer Task", "Beschreibung", Priority.HIGH)

        assert task.id == 1
        assert task.title == "Neuer Task"
        assert task.description == "Beschreibung"
        assert task.priority == Priority.HIGH
        assert task.status == Status.OPEN
        assert task.created_at is not None

    def test_create_increments_last_id(self):
        meta = make_meta(last_id=4)
        with patch("serialize.read", return_value=([], meta)), \
                patch("serialize.write"):
            task = task_service.create("Task #5", None, Priority.LOW)

        assert task.id == 5

    def test_create_calls_write_with_new_task(self):
        meta = make_meta(last_id=0)
        with patch("serialize.read", return_value=([], meta)), \
                patch("serialize.write") as mock_write:
            task = task_service.create("Write-Test", None, Priority.MEDIUM)

        mock_write.assert_called_once()
        written_tasks, written_meta = mock_write.call_args[0]
        assert len(written_tasks) == 1
        assert written_tasks[0].title == "Write-Test"
        assert written_meta["last_id"] == 1

    def test_create_without_description(self):
        with patch("serialize.read", return_value=([], make_meta(last_id=0))), \
                patch("serialize.write"):
            task = task_service.create("Kein Beschr.", None, Priority.LOW)

        assert task.description is None

    def test_create_sets_status_open(self):
        with patch("serialize.read", return_value=([], make_meta(last_id=0))), \
                patch("serialize.write"):
            task = task_service.create("Status-Check", None, Priority.MEDIUM)

        assert task.status == Status.OPEN


# ─────────────────────────────────────────────────────────────────────────────
# TestEdit
# ─────────────────────────────────────────────────────────────────────────────

class TestEdit:

    def test_edit_updates_fields(self, one_task):
        tasks, meta = one_task
        with patch("serialize.read", return_value=(tasks, meta)), \
                patch("serialize.write"):
            task = task_service.edit("Neuer Titel", "Neue Beschr.", Priority.LOW, task_id=1)

        assert task.title == "Neuer Titel"
        assert task.description == "Neue Beschr."
        assert task.priority == Priority.LOW
        assert task.updated_at is not None

    def test_edit_raises_for_unknown_id(self):
        with patch("serialize.read", return_value=([], make_meta())):
            with pytest.raises(ValueError, match="#99"):
                task_service.edit("X", None, Priority.LOW, task_id=99)

    def test_edit_does_not_change_status(self, one_task):
        tasks, meta = one_task
        original_status = tasks[0].status
        with patch("serialize.read", return_value=(tasks, meta)), \
                patch("serialize.write"):
            task = task_service.edit("Titel", None, Priority.HIGH, task_id=1)

        assert task.status == original_status


# ─────────────────────────────────────────────────────────────────────────────
# TestGetTask
# ─────────────────────────────────────────────────────────────────────────────

class TestGetTask:

    def test_get_task_returns_correct_task(self, one_task):
        tasks, meta = one_task
        with patch("serialize.read", return_value=(tasks, meta)):
            task = task_service.get_task(1)
        assert task is not None
        assert task.id == 1

    def test_get_task_returns_none_for_unknown_id(self, one_task):
        tasks, meta = one_task
        with patch("serialize.read", return_value=(tasks, meta)):
            task = task_service.get_task(999)
        assert task is None

    def test_get_all_tasks_returns_all(self, three_tasks):
        tasks, meta = three_tasks
        with patch("serialize.read", return_value=(tasks, meta)):
            result = task_service.get_all_tasks()
        assert len(result) == 3

    def test_get_all_tasks_returns_empty_list(self):
        with patch("serialize.read", return_value=([], make_meta())):
            result = task_service.get_all_tasks()
        assert result == []


# ─────────────────────────────────────────────────────────────────────────────
# TestSetStatus
# ─────────────────────────────────────────────────────────────────────────────

class TestSetStatus:

    # ── erlaubte Übergänge ──────────────────────────────────────────────────

    def test_open_to_in_progress(self, one_task):
        tasks, meta = one_task
        assert tasks[0].status == Status.OPEN
        with patch("serialize.read", return_value=(tasks, meta)), \
                patch("serialize.write"):
            task = task_service.set_status(1, Status.IN_PROGRESS)

        assert task.status == Status.IN_PROGRESS

    def test_open_to_done(self, one_task):
        tasks, meta = one_task
        with patch("serialize.read", return_value=(tasks, meta)), \
                patch("serialize.write"):
            task = task_service.set_status(1, Status.DONE)

        assert task.status == Status.DONE
        assert task.done_at is not None

    def test_in_progress_to_done(self):
        task = make_task(id=1, status=Status.IN_PROGRESS)
        with patch("serialize.read", return_value=([task], make_meta())), \
                patch("serialize.write"):
            result = task_service.set_status(1, Status.DONE)

        assert result.status == Status.DONE

    def test_done_to_open_clears_done_at(self):
        task = make_task(id=1, status=Status.DONE, done_at="2026-01-01T00:00:00")
        with patch("serialize.read", return_value=([task], make_meta())), \
                patch("serialize.write"):
            result = task_service.set_status(1, Status.OPEN)

        assert result.status == Status.OPEN
        assert result.done_at is None

    # ── verbotene Übergänge ─────────────────────────────────────────────────

    def test_in_progress_to_open_raises(self):
        task = make_task(id=1, status=Status.IN_PROGRESS)
        with patch("serialize.read", return_value=([task], make_meta())):
            with pytest.raises(ValueError, match="Ungültiger Übergang"):
                task_service.set_status(1, Status.OPEN)

    def test_done_to_in_progress_raises(self):
        task = make_task(id=1, status=Status.DONE)
        with patch("serialize.read", return_value=([task], make_meta())):
            with pytest.raises(ValueError, match="Ungültiger Übergang"):
                task_service.set_status(1, Status.IN_PROGRESS)

    # ── alle erlaubten Übergänge aus ALLOWED_TRANSITIONS ───────────────────

    @pytest.mark.parametrize("from_status,to_status", [
        (from_s, to_s)
        for from_s, targets in ALLOWED_TRANSITIONS.items()
        for to_s in targets
    ])
    def test_all_allowed_transitions_succeed(self, from_status, to_status):
        task = make_task(id=1, status=from_status)
        with patch("serialize.read", return_value=([task], make_meta())), \
                patch("serialize.write"):
            result = task_service.set_status(1, to_status)

        assert result.status == to_status

    # ── Fehlerfall: Task nicht gefunden ─────────────────────────────────────

    def test_set_status_raises_for_unknown_id(self):
        with patch("serialize.read", return_value=([], make_meta())):
            with pytest.raises(ValueError, match="#42"):
                task_service.set_status(42, Status.DONE)

    # ── updated_at wird gesetzt ─────────────────────────────────────────────

    def test_set_status_sets_updated_at(self, one_task):
        tasks, meta = one_task
        assert tasks[0].updated_at is None
        with patch("serialize.read", return_value=(tasks, meta)), \
                patch("serialize.write"):
            task = task_service.set_status(1, Status.DONE)

        assert task.updated_at is not None


# ─────────────────────────────────────────────────────────────────────────────
# TestDelete
# ─────────────────────────────────────────────────────────────────────────────

class TestDelete:

    def test_delete_returns_deleted_task(self, one_task):
        tasks, meta = one_task
        with patch("serialize.read", return_value=(tasks, meta)), \
                patch("serialize.write"):
            deleted = task_service.delete(1)

        assert deleted.id == 1
        assert deleted.title == "Einkaufen"

    def test_delete_removes_task_from_written_list(self, one_task):
        tasks, meta = one_task
        with patch("serialize.read", return_value=(tasks, meta)), \
                patch("serialize.write") as mock_write:
            task_service.delete(1)

        written_tasks, _ = mock_write.call_args[0]
        assert all(t.id != 1 for t in written_tasks)

    def test_delete_raises_for_unknown_id(self):
        with patch("serialize.read", return_value=([], make_meta())):
            with pytest.raises(ValueError, match="#77"):
                task_service.delete(77)

    def test_delete_reduces_task_count(self, three_tasks):
        tasks, meta = three_tasks
        with patch("serialize.read", return_value=(tasks, meta)), \
                patch("serialize.write") as mock_write:
            task_service.delete(2)

        written_tasks, _ = mock_write.call_args[0]
        assert len(written_tasks) == 2
        assert all(t.id != 2 for t in written_tasks)


# ─────────────────────────────────────────────────────────────────────────────
# TestDeleteDone
# ─────────────────────────────────────────────────────────────────────────────

class TestDeleteDone:

    def test_delete_done_removes_only_done_tasks(self, three_tasks):
        tasks, meta = three_tasks
        with patch("serialize.read", return_value=(tasks, meta)), \
                patch("serialize.write") as mock_write:
            count = task_service.delete_done()

        assert count == 1
        written_tasks, _ = mock_write.call_args[0]
        assert all(t.status != Status.DONE for t in written_tasks)
        assert len(written_tasks) == 2

    def test_delete_done_returns_zero_when_none_done(self, one_task):
        tasks, meta = one_task  # alle OPEN
        with patch("serialize.read", return_value=(tasks, meta)), \
                patch("serialize.write"):
            count = task_service.delete_done()

        assert count == 0

    def test_delete_done_returns_correct_count_multiple(self):
        tasks = [
            make_task(id=1, status=Status.DONE),
            make_task(id=2, status=Status.DONE),
            make_task(id=3, status=Status.OPEN),
        ]
        with patch("serialize.read", return_value=(tasks, make_meta(last_id=3))), \
                patch("serialize.write"):
            count = task_service.delete_done()

        assert count == 2

    def test_delete_done_on_empty_list_returns_zero(self):
        with patch("serialize.read", return_value=([], make_meta())), \
                patch("serialize.write"):
            count = task_service.delete_done()

        assert count == 0


# ─────────────────────────────────────────────────────────────────────────────
# TestDeleteAll
# ─────────────────────────────────────────────────────────────────────────────

class TestDeleteAll:

    def test_delete_all_returns_correct_count(self, three_tasks):
        tasks, meta = three_tasks
        with patch("serialize.read", return_value=(tasks, meta)), \
                patch("serialize.write"):
            count = task_service.delete_all()

        assert count == 3

    def test_delete_all_writes_empty_list(self, three_tasks):
        tasks, meta = three_tasks
        with patch("serialize.read", return_value=(tasks, meta)), \
                patch("serialize.write") as mock_write:
            task_service.delete_all()

        written_tasks, _ = mock_write.call_args[0]
        assert written_tasks == []

    def test_delete_all_on_empty_returns_zero(self):
        with patch("serialize.read", return_value=([], make_meta())), \
                patch("serialize.write"):
            count = task_service.delete_all()

        assert count == 0
