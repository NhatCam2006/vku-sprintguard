from typing import Any

from app.core.diff_filter import filter_changed_files, is_ignored_path
from app.core.module_clusterer import build_preview_audit, map_path_to_module


def test_is_ignored_path_strips_lockfiles_minified_and_build_dirs() -> None:
    assert is_ignored_path("package-lock.json") is True
    assert is_ignored_path("frontend/pnpm-lock.yaml") is True
    assert is_ignored_path("backend/uv.lock") is True
    assert is_ignored_path("Cargo.lock") is True
    assert is_ignored_path("assets/app.min.js") is True
    assert is_ignored_path("styles/main.min.css") is True
    assert is_ignored_path("bundle.js.map") is True
    assert is_ignored_path("frontend/dist/index.js") is True
    assert is_ignored_path("node_modules/react/index.js") is True
    assert is_ignored_path("backend/.venv/lib/site.py") is True
    assert is_ignored_path("backend/__pycache__/main.cpython-311.pyc") is True

    assert is_ignored_path("backend/app/main.py") is False
    assert is_ignored_path("frontend/src/App.tsx") is False
    assert is_ignored_path("README.md") is False


def test_filter_changed_files_keeps_only_clean_files() -> None:
    raw = [
        {"filename": "package-lock.json", "additions": 5000, "deletions": 200},
        {"filename": "frontend/dist/bundle.js", "additions": 1200, "deletions": 0},
        {"filename": "backend/app/main.py", "additions": 45, "deletions": 5},
    ]
    filtered = filter_changed_files(raw)
    assert len(filtered) == 1
    assert filtered[0]["filename"] == "backend/app/main.py"


def test_map_path_to_module_two_level_depth() -> None:
    assert map_path_to_module("README.md") == "root"
    assert map_path_to_module("backend/main.py") == "backend"
    assert map_path_to_module("backend/app/main.py") == "backend/app"
    assert map_path_to_module("frontend/src/components/Graph3D.tsx") == "frontend/src"


def test_build_preview_audit_caps_40_modules_into_other() -> None:
    files = [
        {
            "filename": f"pkg_{i:02d}/sub/file.py",
            "additions": 100 - i,
            "deletions": 1,
        }
        for i in range(45)
    ]
    commits: list[dict[str, Any]] = [
        {
            "sha": "1234567890abcdef",
            "author_login": "dev1",
            "author_name": "Dev One",
            "date": "2026-11-20T10:00:00Z",
            "files": files,
        }
    ]
    report = build_preview_audit(
        owner="vku",
        repo_name="large-repo",
        repo_url="https://github.com/vku/large-repo",
        commits=commits,
    )
    module_nodes = [n for n in report.graph_3d.nodes if n.type == "module"]
    assert len(module_nodes) == 40
    module_ids = {n.id for n in module_nodes}
    assert "mod:other" in module_ids


def test_build_preview_audit_status_heuristics_and_timeline_anomaly() -> None:
    commits: list[dict[str, Any]] = []
    # 5 normal weeks with 2 commits each
    for w_idx, day in enumerate(["01", "08", "15", "22"], start=1):
        for c in range(2):
            commits.append(
                {
                    "sha": f"aaaa{w_idx}{c}0",
                    "author_login": "alice",
                    "author_name": "Alice",
                    "date": f"2026-10-{day}T10:00:00Z",
                    "files": [
                        {
                            "filename": "backend/core/service.py",
                            "additions": 30,
                            "deletions": 10,
                        }
                    ],
                }
            )
    # Add second author bob touching shared module
    commits.append(
        {
            "sha": "bbbb111",
            "author_login": "bob",
            "author_name": "Bob",
            "date": "2026-10-15T12:00:00Z",
            "files": [
                {
                    "filename": "frontend/ui/view.tsx",
                    "additions": 40,
                    "deletions": 5,
                }
            ],
        }
    )
    # Anomaly week in November with massive dump commit >= 2500 lines
    commits.append(
        {
            "sha": "deadbeef123",
            "author_login": "bob",
            "author_name": "Bob",
            "date": "2026-11-05T15:00:00Z",
            "files": [
                {
                    "filename": "backend/dump/huge.py",
                    "additions": 2600,
                    "deletions": 50,
                }
            ],
        }
    )

    report = build_preview_audit(
        owner="vku",
        repo_name="team-project",
        repo_url="https://github.com/vku/team-project",
        commits=commits,
    )
    assert report.mode == "live_preview"
    assert report.repo.context == "student_team"

    nodes_by_id = {n.id: n for n in report.graph_3d.nodes}
    # alice owns 8/8 touches on backend/core in a 2-author repo -> risk
    assert nodes_by_id["mod:backend/core"].status == "risk"
    # single commit dump >= 2500 on backend/dump -> risk
    assert nodes_by_id["mod:backend/dump"].status == "risk"

    anomalies = [w for w in report.timeline_2d if w.anomaly]
    assert len(anomalies) >= 1
    assert any(s.evidence_ref == "commit:deadbee" for s in report.signals)
