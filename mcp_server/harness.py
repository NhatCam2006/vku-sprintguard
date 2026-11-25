"""Stateful 6-tool MCP harness enforcing VKU SprintGuard's 5-station audit protocol."""

from __future__ import annotations

import os
import sys
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Literal

import httpx
from pydantic import ValidationError

_BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
if _BACKEND_DIR.is_dir() and str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from app.core.diff_filter import filter_changed_files  # noqa: E402
from app.core.github_client import (  # noqa: E402
    GITHUB_API_BASE,
    fetch_repo_telemetry,
    parse_github_repo_url,
)
from app.core.module_clusterer import build_preview_audit  # noqa: E402
from app.core.schemas import (  # noqa: E402
    AuditReport,
    AuditSignal,
    AuditSummary,
    InterviewQuestion,
    RepoContext,
    SignalLevel,
)

MAX_PATCH_CHARS_TOTAL = 4000
VALID_REPO_CONTEXTS: frozenset[str] = frozenset({"solo", "student_team", "open_source"})
VALID_SIGNAL_LEVELS: frozenset[str] = frozenset({"healthy", "probe", "risk"})


class SessionState(StrEnum):
    COLLECTED = "COLLECTED"
    CONTEXT_SET = "CONTEXT_SET"
    FINDINGS_SUBMITTED = "FINDINGS_SUBMITTED"
    AWAITING_HUMAN_APPROVAL = "AWAITING_HUMAN_APPROVAL"
    PUBLISHED = "PUBLISHED"


class HarnessGuardError(ValueError):
    """Raised when an audit step violates state, grounding, or HITL invariants."""


@dataclass
class AuditSession:
    session_id: str
    repo_url: str
    owner: str
    repo_name: str
    state: SessionState
    telemetry: dict[str, Any]
    report: AuditReport
    valid_refs: set[str] = field(default_factory=set)
    draft_summary: str = ""


def _normalize_ref(ref: str) -> str:
    return (ref or "").strip().lower()


def _build_valid_refs(telemetry: dict[str, Any]) -> set[str]:
    refs: set[str] = set()
    for commit in telemetry.get("commits") or []:
        sha = str(commit.get("sha") or "").strip()
        if not sha:
            continue
        short_sha = sha[:7]
        refs.add(sha)
        refs.add(short_sha)
        refs.add(f"commit:{short_sha}")
        refs.add(f"commit:{sha}")
    for pr in telemetry.get("prs") or []:
        number = pr.get("number")
        if number is not None and str(number).strip():
            refs.add(f"PR#{number}")
    return refs


def _is_valid_ref(ref: str, valid_refs: set[str]) -> bool:
    norm = _normalize_ref(ref)
    if not norm:
        return False
    normalized_set = {_normalize_ref(r) for r in valid_refs}
    return norm in normalized_set


def _recalculate_node_statuses(report: AuditReport) -> None:
    severity_rank = {"healthy": 0, "probe": 1, "risk": 2}
    node_status: dict[str, SignalLevel] = {}
    for sig in report.signals:
        current = node_status.get(sig.node_id, "healthy")
        if severity_rank[sig.level] > severity_rank[current]:
            node_status[sig.node_id] = sig.level

    for node in report.graph_3d.nodes:
        if node.type == "module":
            node.status = node_status.get(node.id, "healthy")


def _truncate_files_patches(
    files: list[dict[str, Any]],
    max_total_chars: int = MAX_PATCH_CHARS_TOTAL,
) -> list[dict[str, Any]]:
    remaining = max_total_chars
    cleaned: list[dict[str, Any]] = []
    for item in files:
        raw_patch = str(item.get("patch") or "")
        if remaining <= 0:
            patch = ""
        elif len(raw_patch) <= remaining:
            patch = raw_patch
            remaining -= len(raw_patch)
        else:
            patch = raw_patch[:remaining] + "\n... [truncated]"
            remaining = 0

        cleaned.append(
            {
                "filename": str(item.get("filename") or item.get("path") or ""),
                "status": str(item.get("status") or ""),
                "additions": int(item.get("additions") or 0),
                "deletions": int(item.get("deletions") or 0),
                "patch": patch,
            }
        )
    return cleaned


def _github_headers(token: str | None = None) -> dict[str, str]:
    resolved_token = token if token is not None else os.getenv("GITHUB_TOKEN", "").strip()
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "vku-sprintguard-mcp/0.1.0",
    }
    if resolved_token:
        headers["Authorization"] = f"Bearer {resolved_token}"
    return headers


class SprintGuardHarness:
    """In-memory state machine backing the 6 sprintguard-mcp tools."""

    def __init__(self) -> None:
        self._sessions: dict[str, AuditSession] = {}

    def get_session(self, session_id: str) -> AuditSession:
        session = self._sessions.get(session_id)
        if session is None:
            raise HarnessGuardError(f"Unknown session_id '{session_id}'.")
        return session

    def _require_state(self, session: AuditSession, allowed: set[SessionState]) -> None:
        if session.state not in allowed:
            allowed_names = ", ".join(sorted(s.value for s in allowed))
            raise HarnessGuardError(
                f"Invalid state transition: session '{session.session_id}' is in state "
                f"'{session.state.value}', expected one of [{allowed_names}]."
            )

    def _assert_grounded_ref(self, session: AuditSession, ref: str, label: str) -> None:
        if not _is_valid_ref(ref, session.valid_refs):
            sample = sorted(session.valid_refs)[:8]
            raise HarnessGuardError(
                f"Ungrounded evidence_ref '{ref}' on {label}. "
                f"Must match real telemetry from this session. Sample valid refs: {sample}"
            )

    def start_repo_audit(
        self,
        repo_url: str,
        token: str | None = None,
    ) -> dict[str, Any]:
        owner, repo_name = parse_github_repo_url(repo_url)
        canonical_url = f"https://github.com/{owner}/{repo_name}"
        telemetry = fetch_repo_telemetry(owner, repo_name, token=token)
        commits = telemetry.get("commits") or []
        prs = telemetry.get("prs") or []

        report = build_preview_audit(
            owner=owner,
            repo_name=repo_name,
            repo_url=canonical_url,
            commits=commits,
            prs=prs,
        )
        valid_refs = _build_valid_refs(telemetry)
        session_id = f"sess_{uuid.uuid4().hex[:12]}"
        session = AuditSession(
            session_id=session_id,
            repo_url=canonical_url,
            owner=owner,
            repo_name=repo_name,
            state=SessionState.COLLECTED,
            telemetry={"commits": commits, "prs": prs},
            report=report,
            valid_refs=valid_refs,
        )
        self._sessions[session_id] = session

        authors = [
            {"id": n.id, "label": n.label, "commits": n.size, "role": n.role}
            for n in report.graph_3d.nodes
            if n.type == "author"
        ]
        modules_count = sum(1 for n in report.graph_3d.nodes if n.type == "module")
        node_ids_sample = [n.id for n in report.graph_3d.nodes[:20]]

        return {
            "session_id": session_id,
            "state": session.state.value,
            "repo": report.repo.model_dump(),
            "authors": authors,
            "modules_count": modules_count,
            "node_ids_sample": node_ids_sample,
            "timeline_2d": [w.model_dump() for w in report.timeline_2d],
            "valid_refs_sample": sorted(valid_refs)[:15],
            "next_step": (
                "Analyze repo context and call submit_context(session_id, repo_type, "
                "context_reasoning, member_roles)."
            ),
        }

    def submit_context(
        self,
        session_id: str,
        repo_type: RepoContext,
        context_reasoning: str,
        member_roles: dict[str, str] | None = None,
        node_descriptions: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        session = self.get_session(session_id)
        self._require_state(session, {SessionState.COLLECTED, SessionState.CONTEXT_SET})

        if repo_type not in VALID_REPO_CONTEXTS:
            raise HarnessGuardError(
                f"Invalid repo_type '{repo_type}'. Must be one of {sorted(VALID_REPO_CONTEXTS)}."
            )

        session.report.repo.context = repo_type
        session.report.repo.context_reasoning = context_reasoning.strip()

        if member_roles:
            normalized_roles = {k.strip().lower(): v.strip() for k, v in member_roles.items()}
            for node in session.report.graph_3d.nodes:
                if node.type != "author":
                    continue
                login_key = node.id.removeprefix("author:").lower()
                for candidate in (node.id.lower(), login_key, node.label.lower()):
                    if candidate in normalized_roles:
                        node.role = normalized_roles[candidate]
                        break

        if node_descriptions:
            normalized_descs = {
                k.strip(): v.strip()
                for k, v in node_descriptions.items()
                if k and k.strip() and v and v.strip()
            }
            lower_descs = {k.lower(): v for k, v in normalized_descs.items()}
            for node in session.report.graph_3d.nodes:
                stripped_id = (
                    node.id.removeprefix("author:")
                    if node.type == "author"
                    else node.id.removeprefix("mod:")
                )
                if node.id in normalized_descs:
                    node.description = normalized_descs[node.id]
                elif node.id.lower() in lower_descs:
                    node.description = lower_descs[node.id.lower()]
                elif stripped_id.lower() in lower_descs:
                    node.description = lower_descs[stripped_id.lower()]
                elif node.label.lower() in lower_descs:
                    node.description = lower_descs[node.label.lower()]

        session.state = SessionState.CONTEXT_SET
        authors = [
            {"id": n.id, "label": n.label, "role": n.role}
            for n in session.report.graph_3d.nodes
            if n.type == "author"
        ]
        return {
            "session_id": session_id,
            "state": session.state.value,
            "repo": session.report.repo.model_dump(),
            "authors": authors,
            "next_step": (
                "Inspect suspicious commits/PRs with inspect_evidence if needed, then call "
                "submit_findings(session_id, signals)."
            ),
        }

    def submit_findings(
        self,
        session_id: str,
        signals: list[dict[str, Any]],
    ) -> dict[str, Any]:
        session = self.get_session(session_id)
        self._require_state(session, {SessionState.CONTEXT_SET, SessionState.FINDINGS_SUBMITTED})

        valid_node_ids = {n.id for n in session.report.graph_3d.nodes}
        validated: list[AuditSignal] = []

        for idx, raw_sig in enumerate(signals):
            try:
                sig = AuditSignal.model_validate(raw_sig)
            except ValidationError as exc:
                raise HarnessGuardError(f"Invalid signal at index {idx}: {exc}") from exc

            if sig.node_id not in valid_node_ids:
                raise HarnessGuardError(
                    f"Unknown node_id '{sig.node_id}' on signal '{sig.id}'. "
                    f"Valid node IDs sample: {sorted(valid_node_ids)[:10]}"
                )

            if sig.level in {"probe", "risk"}:
                self._assert_grounded_ref(session, sig.evidence_ref, f"signal '{sig.id}'")

            validated.append(sig)

        session.report.signals = validated
        _recalculate_node_statuses(session.report)
        session.state = SessionState.FINDINGS_SUBMITTED

        return {
            "session_id": session_id,
            "state": session.state.value,
            "signal_count": len(validated),
            "signals": [s.model_dump() for s in validated],
            "next_step": (
                "Run adversarial self-critique and call submit_critic_review(session_id, "
                "adjustments, draft_summary)."
            ),
        }

    def inspect_evidence(
        self,
        session_id: str,
        target_type: Literal["commit", "pr"],
        target_id: str,
        token: str | None = None,
    ) -> dict[str, Any]:
        session = self.get_session(session_id)
        self._require_state(
            session,
            {
                SessionState.COLLECTED,
                SessionState.CONTEXT_SET,
                SessionState.FINDINGS_SUBMITTED,
                SessionState.AWAITING_HUMAN_APPROVAL,
            },
        )

        cleaned_target = (target_id or "").strip()
        if not cleaned_target:
            raise HarnessGuardError("target_id must not be empty.")

        if target_type == "commit":
            lookup = cleaned_target
            if lookup.lower().startswith("commit:"):
                lookup = lookup.split(":", 1)[1].strip()
            lookup_lower = lookup.lower()

            matched_commit: dict[str, Any] | None = None
            for commit in session.telemetry.get("commits") or []:
                sha = str(commit.get("sha") or "")
                sha_lower = sha.lower()
                if sha_lower and (
                    sha_lower == lookup_lower
                    or (len(lookup_lower) >= 7 and sha_lower.startswith(lookup_lower))
                ):
                    matched_commit = commit
                    break

            if matched_commit is None:
                raise HarnessGuardError(
                    f"Commit '{target_id}' not found in session '{session_id}' telemetry."
                )

            sha = str(matched_commit.get("sha") or "")
            raw_files: list[dict[str, Any]] = list(matched_commit.get("files") or [])
            if not raw_files and sha:
                try:
                    with httpx.Client(
                        base_url=GITHUB_API_BASE,
                        headers=_github_headers(token),
                        timeout=15.0,
                        follow_redirects=True,
                    ) as client:
                        resp = client.get(
                            f"/repos/{session.owner}/{session.repo_name}/commits/{sha}"
                        )
                        if resp.status_code == 200 and isinstance(resp.json(), dict):
                            raw_files = list(resp.json().get("files") or [])
                except httpx.HTTPError:
                    raw_files = []

            kept_files = filter_changed_files(raw_files)
            filtered_out_count = max(0, len(raw_files) - len(kept_files))
            truncated_files = _truncate_files_patches(kept_files)

            return {
                "session_id": session_id,
                "state": session.state.value,
                "target_type": "commit",
                "ref": f"commit:{sha[:7]}",
                "sha": sha,
                "author_login": matched_commit.get("author_login", ""),
                "author_name": matched_commit.get("author_name", ""),
                "date": matched_commit.get("date", ""),
                "message": matched_commit.get("message", ""),
                "filtered_out_count": filtered_out_count,
                "files": truncated_files,
            }

        if target_type == "pr":
            lookup = cleaned_target
            if lookup.upper().startswith("PR#"):
                lookup = lookup[3:]
            elif lookup.startswith("#"):
                lookup = lookup[1:]
            try:
                pr_number = int(lookup)
            except ValueError as exc:
                raise HarnessGuardError(
                    f"Invalid PR identifier '{target_id}'. Expected PR#<number> or integer."
                ) from exc

            matched_pr: dict[str, Any] | None = None
            for pr in session.telemetry.get("prs") or []:
                if pr.get("number") == pr_number:
                    matched_pr = pr
                    break

            if matched_pr is None:
                raise HarnessGuardError(
                    f"Pull Request 'PR#{pr_number}' not found in session '{session_id}' telemetry."
                )

            raw_files = []
            try:
                with httpx.Client(
                    base_url=GITHUB_API_BASE,
                    headers=_github_headers(token),
                    timeout=15.0,
                    follow_redirects=True,
                ) as client:
                    resp = client.get(
                        f"/repos/{session.owner}/{session.repo_name}/pulls/{pr_number}/files"
                    )
                    if resp.status_code == 200 and isinstance(resp.json(), list):
                        raw_files = list(resp.json())
            except httpx.HTTPError:
                raw_files = []

            kept_files = filter_changed_files(raw_files)
            return {
                "session_id": session_id,
                "state": session.state.value,
                "target_type": "pr",
                "ref": f"PR#{pr_number}",
                "pr": matched_pr,
                "filtered_out_count": max(0, len(raw_files) - len(kept_files)),
                "files": _truncate_files_patches(kept_files),
            }

        raise HarnessGuardError(
            f"Unsupported target_type '{target_type}'. Must be 'commit' or 'pr'."
        )

    def submit_critic_review(
        self,
        session_id: str,
        adjustments: list[dict[str, Any]],
        draft_summary: str,
    ) -> dict[str, Any]:
        session = self.get_session(session_id)
        self._require_state(session, {SessionState.FINDINGS_SUBMITTED})

        signals_by_id = {s.id: s for s in session.report.signals}
        dropped_ids: set[str] = set()

        for adj in adjustments:
            sig_id = str(adj.get("signal_id") or "").strip()
            if sig_id not in signals_by_id:
                raise HarnessGuardError(f"Unknown signal_id '{sig_id}' in critic adjustments.")

            if bool(adj.get("drop", False)):
                dropped_ids.add(sig_id)
                continue

            sig = signals_by_id[sig_id]
            new_level = adj.get("new_level")
            if new_level is not None:
                if new_level not in VALID_SIGNAL_LEVELS:
                    raise HarnessGuardError(
                        f"Invalid new_level '{new_level}' for signal '{sig_id}'."
                    )
                if new_level in {"probe", "risk"}:
                    self._assert_grounded_ref(session, sig.evidence_ref, f"signal '{sig.id}'")
                sig.level = new_level

            if "critic_note" in adj and adj["critic_note"] is not None:
                sig.critic_note = str(adj["critic_note"]).strip()

        session.report.signals = [s for s in session.report.signals if s.id not in dropped_ids]
        _recalculate_node_statuses(session.report)
        session.draft_summary = draft_summary.strip()
        session.state = SessionState.AWAITING_HUMAN_APPROVAL

        return {
            "session_id": session_id,
            "state": session.state.value,
            "hitl_required": True,
            "draft_summary": session.draft_summary,
            "active_signals": [s.model_dump() for s in session.report.signals],
            "instruction": (
                "STOP and present findings to the Human PM/Instructor for approval "
                "and human_notes before calling publish_audit."
            ),
        }

    def publish_audit(
        self,
        session_id: str,
        human_approved: bool,
        human_notes: str,
        interview_questions: list[dict[str, Any]],
        final_summary: str,
        api_base_url: str | None = None,
        publish_api_key: str | None = None,
    ) -> dict[str, Any]:
        session = self.get_session(session_id)
        self._require_state(session, {SessionState.AWAITING_HUMAN_APPROVAL})

        if human_approved is not True:
            raise HarnessGuardError(
                "Human-in-the-Loop approval is required: human_approved must be True "
                "before calling publish_audit."
            )

        validated_questions: list[InterviewQuestion] = []
        for idx, raw_q in enumerate(interview_questions):
            try:
                q = InterviewQuestion.model_validate(raw_q)
            except ValidationError as exc:
                raise HarnessGuardError(
                    f"Invalid interview question at index {idx}: {exc}"
                ) from exc
            self._assert_grounded_ref(session, q.evidence_ref, f"interview_question[{idx}]")
            validated_questions.append(q)

        base = (
            (
                api_base_url
                if api_base_url is not None
                else os.getenv("SPRINTGUARD_API_URL", "http://localhost:8000")
            )
            .strip()
            .rstrip("/")
        )
        api_key = (
            publish_api_key if publish_api_key is not None else os.getenv("PUBLISH_API_KEY", "")
        ).strip()

        if not api_key:
            raise HarnessGuardError(
                "Missing PUBLISH_API_KEY: configure PUBLISH_API_KEY env var or pass "
                "publish_api_key to publish_audit."
            )

        now_iso = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        final_audit_id = f"aud_deep_{uuid.uuid4().hex[:8]}"
        final_report = session.report.model_copy(
            update={
                "audit_id": final_audit_id,
                "created_at": now_iso,
                "mode": "deep_ai_audit",
                "summary": AuditSummary(
                    overview=final_summary.strip(),
                    human_notes=human_notes.strip(),
                ),
                "graph_3d": session.report.graph_3d,
                "interview_questions": validated_questions,
                "commit_highlights": list(session.report.commit_highlights),
            }
        )

        try:
            with httpx.Client(timeout=15.0) as client:
                response = client.post(
                    f"{base}/api/audits",
                    headers={"X-API-Key": api_key},
                    json=final_report.model_dump(),
                )
        except httpx.HTTPError as exc:
            raise HarnessGuardError(
                f"Failed to connect to SprintGuard API at '{base}/api/audits': {exc}"
            ) from exc

        if response.status_code < 200 or response.status_code >= 300:
            raise HarnessGuardError(
                f"SprintGuard API rejected publish (HTTP {response.status_code}): "
                f"{response.text[:300]}"
            )

        session.report = final_report
        session.state = SessionState.PUBLISHED

        return {
            "session_id": session_id,
            "state": session.state.value,
            "audit_id": final_report.audit_id,
            "status": "published",
            "dashboard_url": f"{base}/?audit={final_report.audit_id}",
        }
