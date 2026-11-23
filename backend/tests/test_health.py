from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_returns_ok_status(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    db_file = tmp_path / "test_health.db"
    monkeypatch.setenv("SPRINTGUARD_DB_PATH", str(db_file))

    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "database": "ok", "seeded_audits": 3}
