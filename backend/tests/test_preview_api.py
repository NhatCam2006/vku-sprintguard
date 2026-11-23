import httpx
import pytest
from fastapi.testclient import TestClient

import app.main as main_module
from app.core.github_client import (
    GitHubRateLimitError,
    GitHubUpstreamError,
    RepoNotFoundError,
    fetch_repo_telemetry,
    parse_github_repo_url,
)
from app.main import app


def test_parse_github_repo_url_valid_and_invalid() -> None:
    assert parse_github_repo_url("https://github.com/NhatCam2006/vku-sprintguard") == (
        "NhatCam2006",
        "vku-sprintguard",
    )
    assert parse_github_repo_url("https://github.com/owner/repo.git/") == ("owner", "repo")
    assert parse_github_repo_url("https://github.com/owner/repo/tree/main") == ("owner", "repo")

    with pytest.raises(ValueError):
        parse_github_repo_url("https://gitlab.com/owner/repo")

    with pytest.raises(ValueError):
        parse_github_repo_url("https://github.com/only-owner")

    with pytest.raises(ValueError):
        parse_github_repo_url("not-a-url")


def test_preview_endpoint_happy_path(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_fetch(owner: str, repo: str, token: str | None = None) -> dict:
        assert owner == "NhatCam2006"
        assert repo == "vku-sprintguard"
        return {
            "commits": [
                {
                    "sha": "6d27bc633c14",
                    "author_login": "NhatCam2006",
                    "author_name": "Đinh Nhật Cảm",
                    "date": "2026-11-23T09:00:00Z",
                    "message": "feat: initial backend core",
                    "files": [
                        {
                            "filename": "backend/app/main.py",
                            "additions": 120,
                            "deletions": 10,
                        },
                        {
                            "filename": "backend/uv.lock",
                            "additions": 3000,
                            "deletions": 0,
                        },
                    ],
                }
            ],
            "prs": [{"number": 21, "title": "docs: add snapshots", "state": "closed"}],
        }

    monkeypatch.setattr(main_module, "fetch_repo_telemetry", fake_fetch)

    client = TestClient(app)
    resp = client.post(
        "/api/preview",
        json={"repo_url": "https://github.com/NhatCam2006/vku-sprintguard"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["mode"] == "live_preview"
    assert data["repo"]["name"] == "vku-sprintguard"
    assert data["repo"]["context"] == "solo"
    node_ids = {n["id"] for n in data["graph_3d"]["nodes"]}
    assert "author:NhatCam2006" in node_ids
    assert "mod:backend/app" in node_ids


def test_preview_endpoint_error_mappings(monkeypatch: pytest.MonkeyPatch) -> None:
    client = TestClient(app)

    # Invalid URL -> 400
    resp_invalid = client.post("/api/preview", json={"repo_url": "https://example.com/foo"})
    assert resp_invalid.status_code == 400

    # 404 RepoNotFoundError -> 404
    def raise_not_found(owner: str, repo: str, token: str | None = None) -> dict:
        raise RepoNotFoundError("Repo not found")

    monkeypatch.setattr(main_module, "fetch_repo_telemetry", raise_not_found)
    resp_404 = client.post("/api/preview", json={"repo_url": "https://github.com/missing/repo"})
    assert resp_404.status_code == 404

    # 429 GitHubRateLimitError -> 429
    def raise_rate_limit(owner: str, repo: str, token: str | None = None) -> dict:
        raise GitHubRateLimitError("Rate limit hit")

    monkeypatch.setattr(main_module, "fetch_repo_telemetry", raise_rate_limit)
    resp_429 = client.post("/api/preview", json={"repo_url": "https://github.com/owner/repo"})
    assert resp_429.status_code == 429

    # 502 GitHubUpstreamError -> 502
    def raise_upstream(owner: str, repo: str, token: str | None = None) -> dict:
        raise GitHubUpstreamError("Upstream failure")

    monkeypatch.setattr(main_module, "fetch_repo_telemetry", raise_upstream)
    resp_502 = client.post("/api/preview", json={"repo_url": "https://github.com/owner/repo"})
    assert resp_502.status_code == 502


def test_fetch_repo_telemetry_with_mock_httpx(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeClient:
        def __init__(self, *args: object, **kwargs: object) -> None:
            pass

        def __enter__(self) -> "FakeClient":
            return self

        def __exit__(self, *args: object) -> None:
            pass

        def get(self, url: str, params: dict | None = None) -> httpx.Response:
            req = httpx.Request("GET", f"https://api.github.com{url}")
            if url.endswith("/commits"):
                return httpx.Response(
                    200,
                    json=[
                        {
                            "sha": "abc1234567",
                            "author": {"login": "NhatCam2006"},
                            "commit": {
                                "author": {
                                    "name": "Đinh Nhật Cảm",
                                    "date": "2026-11-23T09:00:00Z",
                                },
                                "message": "feat: add backend core",
                            },
                        }
                    ],
                    request=req,
                )
            if "/commits/" in url:
                return httpx.Response(
                    200,
                    json={
                        "sha": "abc1234567",
                        "files": [
                            {
                                "filename": "backend/app/main.py",
                                "additions": 50,
                                "deletions": 2,
                            }
                        ],
                    },
                    request=req,
                )
            if url.endswith("/pulls"):
                return httpx.Response(
                    200,
                    json=[
                        {
                            "number": 10,
                            "title": "feat: m3 backend",
                            "state": "open",
                            "user": {"login": "NhatCam2006"},
                            "created_at": "2026-11-23T09:10:00Z",
                        }
                    ],
                    request=req,
                )
            return httpx.Response(404, request=req)

    monkeypatch.setattr(httpx, "Client", FakeClient)
    data = fetch_repo_telemetry("NhatCam2006", "vku-sprintguard", token="test-token")
    assert len(data["commits"]) == 1
    assert data["commits"][0]["sha"] == "abc1234567"
    assert len(data["commits"][0]["files"]) == 1
    assert len(data["prs"]) == 1
