"""VKU SprintGuard FastMCP Server exposing the 6 stateful audit tools."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Literal

_REPO_ROOT = Path(__file__).resolve().parent.parent
_BACKEND_DIR = _REPO_ROOT / "backend"
for _p in (_REPO_ROOT, _BACKEND_DIR):
    if _p.is_dir() and str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from mcp.server.fastmcp import FastMCP  # noqa: E402

from app.core.schemas import RepoContext  # noqa: E402
from mcp_server.harness import HarnessGuardError, SprintGuardHarness  # noqa: E402

mcp = FastMCP("sprintguard-mcp")
harness = SprintGuardHarness()


def _error_response(exc: Exception, session_id: str | None = None) -> dict[str, Any]:
    state: str | None = None
    if session_id:
        try:
            state = harness.get_session(session_id).state.value
        except HarnessGuardError:
            state = None
    return {"error": str(exc), "state": state}


@mcp.tool()
def start_repo_audit(repo_url: str) -> dict[str, Any]:
    """Station 1: Collect GitHub telemetry, build 3D graph & timeline, and open an audit session."""
    try:
        return harness.start_repo_audit(repo_url=repo_url)
    except (HarnessGuardError, ValueError, Exception) as exc:
        return _error_response(exc)


@mcp.tool()
def submit_context(
    session_id: str,
    repo_type: RepoContext,
    context_reasoning: str,
    member_roles: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Station 2: Lock repository context (solo/student_team/open_source) and member roles."""
    try:
        return harness.submit_context(
            session_id=session_id,
            repo_type=repo_type,
            context_reasoning=context_reasoning,
            member_roles=member_roles,
        )
    except (HarnessGuardError, ValueError) as exc:
        return _error_response(exc, session_id=session_id)


@mcp.tool()
def submit_findings(
    session_id: str,
    signals: list[dict[str, Any]],
) -> dict[str, Any]:
    """Station 3: Submit evidence-grounded audit signals (probe/risk require real refs)."""
    try:
        return harness.submit_findings(session_id=session_id, signals=signals)
    except (HarnessGuardError, ValueError) as exc:
        return _error_response(exc, session_id=session_id)


@mcp.tool()
def inspect_evidence(
    session_id: str,
    target_type: Literal["commit", "pr"],
    target_id: str,
) -> dict[str, Any]:
    """Inspect cleaned, filtered diffs for a real commit SHA or PR number in the current session."""
    try:
        return harness.inspect_evidence(
            session_id=session_id,
            target_type=target_type,
            target_id=target_id,
        )
    except (HarnessGuardError, ValueError) as exc:
        return _error_response(exc, session_id=session_id)


@mcp.tool()
def submit_critic_review(
    session_id: str,
    adjustments: list[dict[str, Any]],
    draft_summary: str,
) -> dict[str, Any]:
    """Station 4: Apply adversarial self-critique and pause for Human-in-the-Loop approval."""
    try:
        return harness.submit_critic_review(
            session_id=session_id,
            adjustments=adjustments,
            draft_summary=draft_summary,
        )
    except (HarnessGuardError, ValueError) as exc:
        return _error_response(exc, session_id=session_id)


@mcp.tool()
def publish_audit(
    session_id: str,
    human_approved: bool,
    human_notes: str,
    interview_questions: list[dict[str, Any]],
    final_summary: str,
) -> dict[str, Any]:
    """Station 5: Publish HITL-approved Deep AI Audit report to VKU SprintGuard Backend."""
    try:
        return harness.publish_audit(
            session_id=session_id,
            human_approved=human_approved,
            human_notes=human_notes,
            interview_questions=interview_questions,
            final_summary=final_summary,
        )
    except (HarnessGuardError, ValueError) as exc:
        return _error_response(exc, session_id=session_id)


if __name__ == "__main__":
    mcp.run()
