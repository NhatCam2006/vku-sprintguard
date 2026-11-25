from pathlib import Path

import pytest
from pydantic import ValidationError

from app.core.schemas import (
    AuditReport,
    AuditSummary,
    Graph3D,
    GraphEdge,
    GraphNode,
    RepoInfo,
    TimelineWeek,
)
from app.db.sqlite_store import SQLiteStore
from app.seed.sample_audits import get_sample_audits


def test_sample_audits_validate_against_schema() -> None:
    samples = get_sample_audits()
    assert len(samples) == 3
    ids = {s.audit_id for s in samples}
    assert ids == {
        "aud_sample_student_team",
        "aud_sample_solo",
        "aud_sample_open_source",
    }
    contexts = {s.repo.context for s in samples}
    assert contexts == {"student_team", "solo", "open_source"}
    for sample in samples:
        assert sample.mode == "deep_ai_audit"
        assert len(sample.graph_3d.nodes) > 0
        assert len(sample.graph_3d.edges) > 0
        assert len(sample.timeline_2d) > 0
        assert len(sample.signals) > 0
        assert len(sample.commit_highlights) > 0
        for hl in sample.commit_highlights:
            assert hl.url.startswith("https://github.com/")
            assert hl.diff_summary != ""
        for node in sample.graph_3d.nodes:
            assert node.description.strip() != ""
            if node.type == "module":
                assert len(node.key_files) > 0


def test_pydantic_rejects_invalid_enum_and_negative_metrics() -> None:
    with pytest.raises(ValidationError):
        RepoInfo(
            name="bad-repo",
            url="https://github.com/org/bad-repo",
            context="invalid_context",  # type: ignore[arg-type]
            context_reasoning="bad context",
        )

    with pytest.raises(ValidationError):
        GraphNode(
            id="mod:a",
            type="module",
            label="a",
            size=-5,
            status="healthy",
        )

    with pytest.raises(ValidationError):
        GraphEdge(
            source="author:u1",
            target="mod:a",
            weight=0,
        )


def test_sqlite_store_seed_idempotency_and_upsert(tmp_path: Path) -> None:
    db_path = tmp_path / "nested" / "sprintguard.db"
    store = SQLiteStore(db_path)

    samples = get_sample_audits()
    count_first = store.seed_defaults_if_empty(samples)
    assert count_first == 3

    # Seeding a second time must be idempotent and not duplicate records
    count_second = store.seed_defaults_if_empty(samples)
    assert count_second == 3

    listed = store.list_audits()
    assert len(listed) == 3

    solo = store.get_audit("aud_sample_solo")
    assert solo is not None
    assert solo.repo.context == "solo"
    assert store.get_audit("aud_non_existent") is None

    # Test upsert new and update existing
    custom = AuditReport(
        audit_id="aud_custom_01",
        created_at="2026-11-23T12:00:00Z",
        mode="deep_ai_audit",
        repo=RepoInfo(
            name="custom-repo",
            url="https://github.com/vku/custom-repo",
            context="solo",
            context_reasoning="Solo project",
        ),
        summary=AuditSummary(overview="Initial overview", human_notes="Initial note"),
        graph_3d=Graph3D(
            nodes=[
                GraphNode(id="author:dev", type="author", label="Dev", size=5),
                GraphNode(id="mod:root", type="module", label="root", size=100, churn=2),
            ],
            edges=[GraphEdge(source="author:dev", target="mod:root", weight=2)],
        ),
        timeline_2d=[
            TimelineWeek(week="2026-W47", commits=2, additions=80, deletions=20, anomaly=False)
        ],
    )
    store.upsert_audit(custom)
    assert store.count_audits() == 4

    updated = custom.model_copy(
        update={"summary": AuditSummary(overview="Updated overview", human_notes="Approved")}
    )
    store.upsert_audit(updated)
    assert store.count_audits() == 4

    fetched = store.get_audit("aud_custom_01")
    assert fetched is not None
    assert fetched.summary.overview == "Updated overview"
    assert fetched.summary.human_notes == "Approved"
