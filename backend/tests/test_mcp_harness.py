"""Unit and integration tests for the sprintguard-mcp 6-tool stateful harness."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import httpx
import pytest
from fastapi.testclient import TestClient
from mcp_server.harness import HarnessGuardError, SessionState, SprintGuardHarness
from mcp_server.server import mcp as mcp_server_instance

from app.main import app as fastapi_app


def _sample_telemetry() -> dict[str, Any]:
    return {
        "commits": [
            {
                "sha": "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678",
                "author_login": "alice",
                "author_name": "Alice Nguyen",
                "date": "2026-03-02T10:00:00Z",
                "message": "feat(auth): implement JWT login flow",
                "files": [
                    {
                        "filename": "backend/auth/service.py",
                        "status": "added",
                        "additions": 180,
                        "deletions": 0,
                        "patch": "@@ -0,0 +1,5 @@\n+def login(user):\n+    return True\n",
                    },
                    {
                        "filename": "package-lock.json",
                        "status": "modified",
                        "additions": 4500,
                        "deletions": 1200,
                        "patch": "@@ -1,3 +1,3 @@\n+lockfile noise\n",
                    },
                    {
                        "filename": "frontend/dist/bundle.min.js",
                        "status": "added",
                        "additions": 3000,
                        "deletions": 0,
                        "patch": "@@ -0,0 +1,1 @@\n+minified js\n",
                    },
                ],
            },
            {
                "sha": "99887766554433221100ffeeddccbbaa11223344",
                "author_login": "bob",
                "author_name": "Bob Tran",
                "date": "2026-03-10T14:30:00Z",
                "message": "feat(ui): build dashboard layout",
                "files": [
                    {
                        "filename": "frontend/src/App.tsx",
                        "status": "modified",
                        "additions": 120,
                        "deletions": 15,
                        "patch": "@@ -1,2 +1,4 @@\n+export function App() {}\n",
                    }
                ],
            },
        ],
        "prs": [
            {
                "number": 7,
                "title": "Add auth service and dashboard shell",
                "state": "closed",
                "user_login": "alice",
                "created_at": "2026-03-11T09:00:00Z",
            }
        ],
    }


def _patch_telemetry(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "mcp_server.harness.fetch_repo_telemetry",
        lambda owner, repo, token=None: _sample_telemetry(),
    )


def test_full_six_tool_happy_path_and_publish_to_fastapi(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _patch_telemetry(monkeypatch)
    db_path = tmp_path / "mcp_publish_test.db"
    monkeypatch.setenv("SPRINTGUARD_DB_PATH", str(db_path))
    monkeypatch.setenv("PUBLISH_API_KEY", "test-secret-publish-key")

    test_client = TestClient(fastapi_app)
    captured_requests: list[dict[str, Any]] = []

    class _RoutedHttpxClient:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        def __enter__(self) -> _RoutedHttpxClient:
            return self

        def __exit__(self, *args: Any) -> None:
            return None

        def post(
            self,
            url: str,
            headers: dict[str, str] | None = None,
            json: dict[str, Any] | None = None,
        ) -> httpx.Response:
            captured_requests.append({"url": url, "headers": headers or {}, "json": json})
            assert url.endswith("/api/audits")
            resp = test_client.post("/api/audits", headers=headers, json=json)
            return httpx.Response(status_code=resp.status_code, content=resp.content)

    monkeypatch.setattr("mcp_server.harness.httpx.Client", _RoutedHttpxClient)

    harness = SprintGuardHarness()

    # 1. start_repo_audit
    start = harness.start_repo_audit("https://github.com/vku-team/sprintguard-demo")
    session_id = start["session_id"]
    assert start["state"] == SessionState.COLLECTED.value
    assert start["modules_count"] >= 2
    assert "commit:a1b2c3d" in start["valid_refs_sample"] or any(
        ref.startswith("commit:a1b2c3d") for ref in harness.get_session(session_id).valid_refs
    )

    # 2. submit_context
    ctx = harness.submit_context(
        session_id=session_id,
        repo_type="student_team",
        context_reasoning="Two-member student team splitting backend auth and frontend UI.",
        member_roles={"alice": "Backend Lead", "bob": "Frontend Dev"},
        node_descriptions={
            "mod:backend/auth": (
                "Dịch vụ xác thực JWT và kiểm tra quyền truy cập do Alice phụ trách."
            ),
            "author:alice": "Trưởng nhóm Backend phụ trách tầng xác thực.",
        },
    )
    assert ctx["state"] == SessionState.CONTEXT_SET.value
    roles_by_id = {a["id"]: a["role"] for a in ctx["authors"]}
    assert roles_by_id["author:alice"] == "Backend Lead"
    assert roles_by_id["author:bob"] == "Frontend Dev"

    # 3. inspect_evidence (verify lockfile + dist filtered out)
    evidence = harness.inspect_evidence(
        session_id=session_id,
        target_type="commit",
        target_id="commit:a1b2c3d",
    )
    assert evidence["ref"] == "commit:a1b2c3d"
    assert evidence["filtered_out_count"] == 2
    filenames = [f["filename"] for f in evidence["files"]]
    assert filenames == ["backend/auth/service.py"]

    # 4. submit_findings
    findings = harness.submit_findings(
        session_id=session_id,
        signals=[
            {
                "id": "sig_01",
                "node_id": "mod:backend/auth",
                "level": "risk",
                "title": "Single-author ownership on auth service",
                "description": "Alice authored all commits in backend/auth.",
                "evidence_ref": "commit:a1b2c3d",
            },
            {
                "id": "sig_02",
                "node_id": "mod:frontend/src",
                "level": "probe",
                "title": "Check PR review depth on dashboard shell",
                "description": "Verify Bob and Alice cross-reviewed PR#7.",
                "evidence_ref": "PR#7",
            },
        ],
    )
    assert findings["state"] == SessionState.FINDINGS_SUBMITTED.value
    assert findings["signal_count"] == 2

    # 5. submit_critic_review
    critic = harness.submit_critic_review(
        session_id=session_id,
        adjustments=[
            {
                "signal_id": "sig_01",
                "new_level": "probe",
                "critic_note": "Expected Backend/Frontend split; ask Bob about auth flow.",
            }
        ],
        draft_summary="Healthy 2-person split; recommend light cross-module oral checks.",
    )
    assert critic["state"] == SessionState.AWAITING_HUMAN_APPROVAL.value
    assert critic["hitl_required"] is True
    assert "STOP" in critic["instruction"]

    # 6. publish_audit
    published = harness.publish_audit(
        session_id=session_id,
        human_approved=True,
        human_notes="Instructor confirmed Backend/Frontend division of labor.",
        interview_questions=[
            {
                "author_id": "author:bob",
                "author_name": "Bob Tran",
                "question": (
                    "How does your frontend call the JWT login endpoint from commit a1b2c3d?"
                ),
                "evidence_ref": "commit:a1b2c3d",
            }
        ],
        final_summary="Deep AI Audit completed with instructor context.",
        api_base_url="http://testserver",
        publish_api_key="test-secret-publish-key",
    )
    assert published["state"] == SessionState.PUBLISHED.value
    assert published["status"] == "published"
    assert published["audit_id"].startswith("aud_deep_")
    assert captured_requests[0]["headers"]["X-API-Key"] == "test-secret-publish-key"

    # Verify stored in SQLite via GET /api/audits/{audit_id}
    stored_resp = test_client.get(f"/api/audits/{published['audit_id']}")
    assert stored_resp.status_code == 200
    stored_json = stored_resp.json()
    assert stored_json["mode"] == "deep_ai_audit"
    assert stored_json["summary"]["human_notes"] == (
        "Instructor confirmed Backend/Frontend division of labor."
    )
    stored_nodes = {n["id"]: n for n in stored_json["graph_3d"]["nodes"]}
    assert stored_nodes["mod:backend/auth"]["description"] == (
        "Dịch vụ xác thực JWT và kiểm tra quyền truy cập do Alice phụ trách."
    )
    assert stored_nodes["author:alice"]["description"] == (
        "Trưởng nhóm Backend phụ trách tầng xác thực."
    )
    assert stored_nodes["mod:backend/auth"]["key_files"] == ["backend/auth/service.py"]
    assert len(stored_json["commit_highlights"]) >= 2
    assert stored_json["commit_highlights"][0]["ref"] == "commit:a1b2c3d"
    assert stored_json["commit_highlights"][0]["url"] == (
        "https://github.com/vku-team/sprintguard-demo/commit/"
        "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678"
    )


def test_out_of_order_state_transitions_and_hitl_guards(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_telemetry(monkeypatch)
    harness = SprintGuardHarness()
    start = harness.start_repo_audit("https://github.com/vku-team/sprintguard-demo")
    session_id = start["session_id"]

    # Cannot submit_findings before submit_context
    with pytest.raises(HarnessGuardError, match="Invalid state transition"):
        harness.submit_findings(session_id=session_id, signals=[])

    # Cannot publish_audit before AWAITING_HUMAN_APPROVAL
    with pytest.raises(HarnessGuardError, match="Invalid state transition"):
        harness.publish_audit(
            session_id=session_id,
            human_approved=True,
            human_notes="",
            interview_questions=[],
            final_summary="Early publish",
            publish_api_key="secret",
        )

    # Advance to AWAITING_HUMAN_APPROVAL
    harness.submit_context(session_id, "student_team", "Student team")
    harness.submit_findings(session_id, [])
    harness.submit_critic_review(session_id, [], "Draft summary")

    # Reject human_approved=False
    with pytest.raises(HarnessGuardError, match="human_approved must be True"):
        harness.publish_audit(
            session_id=session_id,
            human_approved=False,
            human_notes="Not approved yet",
            interview_questions=[],
            final_summary="Should fail",
            publish_api_key="secret",
        )


def test_evidence_grounding_rejects_fabricated_ref(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_telemetry(monkeypatch)
    harness = SprintGuardHarness()
    start = harness.start_repo_audit("https://github.com/vku-team/sprintguard-demo")
    session_id = start["session_id"]
    harness.submit_context(session_id, "student_team", "Student team")

    with pytest.raises(HarnessGuardError, match="Ungrounded evidence_ref 'commit:deadbeef'"):
        harness.submit_findings(
            session_id=session_id,
            signals=[
                {
                    "id": "sig_fake",
                    "node_id": "mod:backend/auth",
                    "level": "risk",
                    "title": "Fabricated risk",
                    "description": "Hallucinated commit ref.",
                    "evidence_ref": "commit:deadbeef",
                }
            ],
        )


def test_inspect_evidence_filters_lockfiles_and_build_dirs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_telemetry(monkeypatch)
    harness = SprintGuardHarness()
    start = harness.start_repo_audit("https://github.com/vku-team/sprintguard-demo")
    session_id = start["session_id"]

    result = harness.inspect_evidence(
        session_id=session_id,
        target_type="commit",
        target_id="a1b2c3d",
    )
    kept_names = [f["filename"] for f in result["files"]]
    assert "backend/auth/service.py" in kept_names
    assert "package-lock.json" not in kept_names
    assert "frontend/dist/bundle.min.js" not in kept_names
    assert result["filtered_out_count"] == 2


def test_fastmcp_registers_all_six_expected_tools() -> None:
    expected = {
        "start_repo_audit",
        "submit_context",
        "submit_findings",
        "inspect_evidence",
        "submit_critic_review",
        "publish_audit",
    }
    tool_manager = getattr(mcp_server_instance, "_tool_manager", None)
    if tool_manager is not None and hasattr(tool_manager, "_tools"):
        registered = set(tool_manager._tools.keys())
    else:
        import asyncio

        tools = asyncio.run(mcp_server_instance.list_tools())
        registered = {t.name for t in tools}

    assert expected.issubset(registered)
