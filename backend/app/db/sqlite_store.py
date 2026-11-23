import os
import sqlite3
from pathlib import Path

from app.core.schemas import AuditListItem, AuditReport


class SQLiteStore:
    """Lightweight SQLite store for AuditReport JSON payloads."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        resolved = db_path or os.getenv("SPRINTGUARD_DB_PATH", "data/sprintguard.db")
        self.db_path = Path(resolved)

    def _connect(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS audits (
                    audit_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def seed_defaults_if_empty(self, samples: list[AuditReport]) -> int:
        """Idempotently insert sample audits without overwriting existing records.

        Returns the total number of audits in the store after seeding.
        """
        self.init_db()
        with self._connect() as conn:
            for report in samples:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO audits (audit_id, created_at, mode, payload_json)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        report.audit_id,
                        report.created_at,
                        report.mode,
                        report.model_dump_json(),
                    ),
                )
            conn.commit()
        return self.count_audits()

    def upsert_audit(self, report: AuditReport) -> None:
        self.init_db()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO audits (audit_id, created_at, mode, payload_json)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(audit_id) DO UPDATE SET
                    created_at = excluded.created_at,
                    mode = excluded.mode,
                    payload_json = excluded.payload_json
                """,
                (
                    report.audit_id,
                    report.created_at,
                    report.mode,
                    report.model_dump_json(),
                ),
            )
            conn.commit()

    def get_audit(self, audit_id: str) -> AuditReport | None:
        self.init_db()
        with self._connect() as conn:
            row = conn.execute(
                "SELECT payload_json FROM audits WHERE audit_id = ?",
                (audit_id,),
            ).fetchone()
        if row is None:
            return None
        return AuditReport.model_validate_json(row["payload_json"])

    def list_audits(self) -> list[AuditListItem]:
        self.init_db()
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT payload_json FROM audits ORDER BY created_at DESC, audit_id ASC"
            ).fetchall()
        items: list[AuditListItem] = []
        for row in rows:
            report = AuditReport.model_validate_json(row["payload_json"])
            items.append(
                AuditListItem(
                    audit_id=report.audit_id,
                    created_at=report.created_at,
                    mode=report.mode,
                    repo=report.repo,
                    summary=report.summary,
                    node_count=len(report.graph_3d.nodes),
                    signal_count=len(report.signals),
                )
            )
        return items

    def count_audits(self) -> int:
        self.init_db()
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS cnt FROM audits").fetchone()
        return int(row["cnt"]) if row is not None else 0
