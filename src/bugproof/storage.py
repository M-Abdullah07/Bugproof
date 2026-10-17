"""Short SQLite transactions; provider I/O belongs outside this module."""

import sqlite3
import json
import time
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
                CREATE TABLE IF NOT EXISTS case_states (
                    case_id TEXT PRIMARY KEY REFERENCES cases(id),
                    version INTEGER NOT NULL DEFAULT 1, state_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id),
                    kind TEXT NOT NULL, data_json TEXT NOT NULL, at REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS approvals (
                    id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id),
                    fingerprint TEXT NOT NULL, payload_json TEXT NOT NULL,
                    reviewer TEXT NOT NULL, expires REAL NOT NULL, revoked INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS actions (
                    id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id),
                    kind TEXT NOT NULL, status TEXT NOT NULL, result_json TEXT,
                    error TEXT, updated REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS lab_fixtures (
                    id TEXT PRIMARY KEY, build TEXT NOT NULL, retry_key TEXT,
                    payload_json TEXT, orders_json TEXT NOT NULL DEFAULT '[]'
                );
                CREATE TABLE IF NOT EXISTS action_snapshots (
                    action_id TEXT PRIMARY KEY REFERENCES actions(id), context_json TEXT NOT NULL
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

    def case(self, case_id):
        with self.connection() as c:
            row = c.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()
            if not row:
                raise ValueError("Case not found")
            data = dict(row)
            data["source"] = json.loads(data.pop("source_json"))
            state = c.execute("SELECT * FROM case_states WHERE case_id=?", (case_id,)).fetchone()
            data["state"] = json.loads(state["state_json"]) if state else {}
            data["version"] = state["version"] if state else 0
            data["actions"] = [dict(r) for r in c.execute("SELECT * FROM actions WHERE case_id=?", (case_id,))]
            for action in data["actions"]:
                action["result"] = json.loads(action.pop("result_json") or "null")
            data["history"] = [dict(r) for r in c.execute("SELECT kind,data_json,at FROM history WHERE case_id=? ORDER BY id DESC LIMIT 30", (case_id,))]
            data["delivery_status"]=next((json.loads(r["data_json"])["status"] for r in data["history"] if r["kind"]=="publication_complete" and json.loads(r["data_json"]).get("case_version")==data["version"]),None)
            return data

    def ingest(self, mailbox, thread, source):
        encoded = json.dumps(source, sort_keys=True)
        with self.connection() as c:
            c.execute("BEGIN IMMEDIATE")
            row = c.execute("SELECT * FROM cases WHERE mailbox_id=? AND thread_id=?", (mailbox, thread)).fetchone()
            if row and row["source_json"] == encoded:
                return row["id"], False
            case_id = row["id"] if row else uuid4().hex
            if row:
                c.execute("UPDATE cases SET source_json=?, source_revision=source_revision+1 WHERE id=?", (encoded, case_id))
                c.execute("UPDATE approvals SET revoked=1 WHERE case_id=?", (case_id,))
                c.execute("UPDATE case_states SET version=version+1,state_json=? WHERE case_id=?", (json.dumps({"status":"needs_investigation"}), case_id))
            else:
                c.execute("INSERT INTO cases VALUES(?,?,?,?,?,?)", (case_id,mailbox,thread,1,encoded,str(time.time())))
                c.execute("INSERT INTO case_states(case_id,state_json) VALUES(?,?)", (case_id,json.dumps({"status":"needs_investigation"})))
            c.execute("INSERT INTO history(case_id,kind,data_json,at) VALUES(?,?,?,?)", (case_id,"source",encoded,time.time()))
            return case_id, True

    def save_state(self, case_id, state, version, kind="state"):
        with self.connection() as c:
            c.execute("BEGIN IMMEDIATE")
            changed = c.execute("UPDATE case_states SET version=version+1,state_json=? WHERE case_id=? AND version=?", (json.dumps(state),case_id,version)).rowcount
            if not changed:
                raise ValueError("Case changed while this operation ran. Reload and review.")
            c.execute("UPDATE approvals SET revoked=1 WHERE case_id=?", (case_id,))
            c.execute("INSERT INTO history(case_id,kind,data_json,at) VALUES(?,?,?,?)", (case_id,kind,json.dumps(state),time.time()))

    def add_approval(self, case, fingerprint, payload, reviewer, ttl):
        approval_id = uuid4().hex
        with self.connection() as c:
            c.execute("BEGIN IMMEDIATE")
            current = c.execute("SELECT version FROM case_states WHERE case_id=?", (case["id"],)).fetchone()
            if current[0] != case["version"]:
                raise ValueError("Case changed; review again")
            c.execute("INSERT INTO approvals VALUES(?,?,?,?,?,?,0)", (approval_id,case["id"],fingerprint,json.dumps(payload),reviewer,time.time()+ttl))
        return approval_id

    def approval(self, case_id, approval_id, fingerprint):
        with self.connection() as c:
            row = c.execute("SELECT * FROM approvals WHERE id=? AND case_id=?", (approval_id,case_id)).fetchone()
            if not row or row["revoked"] or row["expires"] < time.time() or row["fingerprint"] != fingerprint:
                raise ValueError("Approval missing, expired or stale. Review exact actions again.")
            return dict(row)

    def claim(self, case, approval_id, fingerprint, action_id, kind, context=None):
        with self.connection() as c:
            c.execute("BEGIN IMMEDIATE")
            approval = c.execute("SELECT * FROM approvals WHERE id=? AND case_id=?", (approval_id,case["id"])).fetchone()
            current = c.execute("SELECT version FROM case_states WHERE case_id=?", (case["id"],)).fetchone()
            if not approval or approval["revoked"] or approval["expires"] < time.time() or approval["fingerprint"] != fingerprint or current[0] != case["version"]:
                raise ValueError("Approval no longer authorizes this action")
            old = c.execute("SELECT * FROM actions WHERE id=?", (action_id,)).fetchone()
            if old:
                if old["status"]=="failed":
                    c.execute("UPDATE actions SET status='running',result_json=NULL,error=NULL,updated=? WHERE id=?", (time.time(),action_id))
                    c.execute("UPDATE action_snapshots SET context_json=? WHERE action_id=?", (json.dumps(context or {}),action_id))
                    return {"id":action_id,"status":"running"},True
                return dict(old), False
            c.execute("INSERT INTO actions(id,case_id,kind,status,updated) VALUES(?,?,?,'running',?)", (action_id,case["id"],kind,time.time()))
            c.execute("INSERT INTO action_snapshots VALUES(?,?)", (action_id,json.dumps(context or {})))
            return {"id":action_id,"status":"running"}, True

    def action_snapshot(self, action_id):
        with self.connection() as c:
            row=c.execute("SELECT context_json FROM action_snapshots WHERE action_id=?", (action_id,)).fetchone()
            return json.loads(row[0]) if row else {}

    def action_result(self, action_id, status, result=None, error=None):
        with self.connection() as c:
            c.execute("UPDATE actions SET status=?,result_json=?,error=?,updated=? WHERE id=?", (status,json.dumps(result),error,time.time(),action_id))

    def event(self, case_id, kind, data):
        with self.connection() as c:
            c.execute("INSERT INTO history(case_id,kind,data_json,at) VALUES(?,?,?,?)", (case_id,kind,json.dumps(data),time.time()))
