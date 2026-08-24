from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _id() -> str:
    return str(uuid.uuid4())


class Database:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.execute("PRAGMA journal_mode = WAL")

    def close(self) -> None:
        self.connection.close()

    def migrate(self) -> None:
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)"
        )
        applied = {r[0] for r in self.connection.execute("SELECT version FROM schema_migrations")}
        migrations = Path(__file__).resolve().parents[1] / "migrations"
        for path in sorted(migrations.glob("*.sql")):
            version = int(path.name.split("_", 1)[0])
            if version in applied:
                continue
            self.connection.executescript(path.read_text(encoding="utf-8"))
            self.connection.execute(
                "INSERT INTO schema_migrations(version, applied_at) VALUES (?, ?)",
                (version, _now()),
            )
            self.connection.commit()

    def create_user(self, email: str) -> str:
        user_id = _id()
        self.connection.execute(
            "INSERT INTO users(id, email, created_at) VALUES (?, ?, ?)",
            (user_id, email, _now()),
        )
        self.connection.commit()
        return user_id

    def create_garage(self, user_id: str, name: str) -> str:
        garage_id = _id()
        self.connection.execute(
            "INSERT INTO garages(id, user_id, name, created_at) VALUES (?, ?, ?, ?)",
            (garage_id, user_id, name, _now()),
        )
        self.connection.commit()
        return garage_id

    def tombstone_user(self, user_id: str, *, reason: str) -> str:
        now = _now()
        event_id = _id()
        with self.connection:
            exists = self.connection.execute("SELECT 1 FROM users WHERE id=?", (user_id,)).fetchone()
            if not exists:
                raise ValueError("unknown user")
            self.connection.execute(
                "INSERT INTO deletion_events(id, requested_by_user_id, reason, requested_at, status) VALUES (?, ?, ?, ?, 'pending')",
                (event_id, user_id, reason, now),
            )
            entities = [("user", user_id)] + [
                ("garage", row[0]) for row in self.connection.execute(
                    "SELECT id FROM garages WHERE user_id=? AND deleted_at IS NULL", (user_id,)
                )
            ]
            self.connection.execute("UPDATE garages SET deleted_at=? WHERE user_id=?", (now, user_id))
            self.connection.execute(
                "UPDATE users SET email=NULL, status='deleted', deleted_at=? WHERE id=?", (now, user_id)
            )
            self.connection.executemany(
                "INSERT INTO deletion_lineage(id, deletion_event_id, entity_type, entity_id, action, processed_at, details_json) VALUES (?, ?, ?, ?, 'tombstoned', ?, '{}')",
                [(_id(), event_id, kind, entity_id, now) for kind, entity_id in entities],
            )
            self.connection.execute(
                "UPDATE deletion_events SET status='completed', completed_at=? WHERE id=?", (now, event_id)
            )
        return event_id
