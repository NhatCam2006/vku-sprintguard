from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.seed.sample_audits import get_sample_audits


@pytest.fixture()
def api_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    db_file = tmp_path / "test_audits_api.db"
    monkeypatch.setenv("SPRINTGUARD_DB_PATH", str(db_file))
    monkeypatch.setenv("PUBLISH_API_KEY", "test-secret-publish-key")
    return TestClient(app)


def test_get_audits_list_and_detail(api_client: TestClient) -> None:
    list_resp = api_client.get("/api/audits")
    assert list_resp.status_code == 200
    body = list_resp.json()
    assert "audits" in body
    assert len(body["audits"]) == 3

    detail_resp = api_client.get("/api/audits/aud_sample_student_team")
    assert detail_resp.status_code == 200
    detail = detail_resp.json()
    assert detail["audit_id"] == "aud_sample_student_team"
    assert detail["repo"]["context"] == "student_team"
    assert len(detail["graph_3d"]["nodes"]) >= 12


def test_get_audit_detail_not_found(api_client: TestClient) -> None:
    resp = api_client.get("/api/audits/aud_missing_999")
    assert resp.status_code == 404


def test_post_audit_requires_valid_api_key(
    api_client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    sample_payload = get_sample_audits()[0].model_dump()
    sample_payload["audit_id"] = "aud_published_via_mcp"

    # Missing header -> 401
    resp_missing = api_client.post("/api/audits", json=sample_payload)
    assert resp_missing.status_code == 401

    # Wrong key -> 403
    resp_wrong = api_client.post(
        "/api/audits",
        json=sample_payload,
        headers={"X-API-Key": "wrong-key"},
    )
    assert resp_wrong.status_code == 403

    # Valid key -> 201
    resp_ok = api_client.post(
        "/api/audits",
        json=sample_payload,
        headers={"X-API-Key": "test-secret-publish-key"},
    )
    assert resp_ok.status_code == 201
    assert resp_ok.json() == {"audit_id": "aud_published_via_mcp", "status": "stored"}

    # Verify persisted and retrievable
    fetch_resp = api_client.get("/api/audits/aud_published_via_mcp")
    assert fetch_resp.status_code == 200
    assert fetch_resp.json()["audit_id"] == "aud_published_via_mcp"

    # Unconfigured server PUBLISH_API_KEY -> 401
    monkeypatch.delenv("PUBLISH_API_KEY", raising=False)
    resp_unconfigured = api_client.post(
        "/api/audits",
        json=sample_payload,
        headers={"X-API-Key": "test-secret-publish-key"},
    )
    assert resp_unconfigured.status_code == 401


def test_post_audit_rejects_malformed_payload(api_client: TestClient) -> None:
    resp = api_client.post(
        "/api/audits",
        json={"audit_id": "bad_only"},
        headers={"X-API-Key": "test-secret-publish-key"},
    )
    assert resp.status_code == 422
