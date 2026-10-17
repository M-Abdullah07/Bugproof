"""Short SQLite transactions; provider I/O belongs outside this module."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4


class Storage:
    def __init__(self, path: Path):
        self.path = path

    @contextmanager
    def connection(self):
        connection = sqlite3.connect(self.path, timeout=5)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def initialize(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS schema_version (
                    version INTEGER PRIMARY KEY CHECK(version=1)
                );
                INSERT OR IGNORE INTO schema_version VALUES(1);
                CREATE TABLE IF NOT EXISTS app_metadata (
                    key TEXT PRIMARY KEY, value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS cases (
                    id TEXT PRIMARY KEY,
                    mailbox_id TEXT NOT NULL,
                    thread_id TEXT NOT NULL,
                    source_revision INTEGER NOT NULL CHECK(source_revision > 0),
                    source_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(mailbox_id, thread_id)
                );
            """)
            connection.execute(
                "INSERT OR IGNORE INTO app_metadata(key,value) VALUES ('installation_id',?)",
                (str(uuid4()),),
            )

    def health(self):
        with self.connection() as connection:
            return connection.execute("SELECT version FROM schema_version").fetchone()[0] == 1

    def list_cases(self):
        with self.connection() as connection:
            return [dict(row) for row in connection.execute(
                "SELECT id, mailbox_id, thread_id, source_revision, created_at "
                "FROM cases ORDER BY created_at DESC LIMIT 100"
            )]
