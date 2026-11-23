import hashlib
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import PurePosixPath
from statistics import median
from typing import Any

from app.core.diff_filter import filter_changed_files
from app.core.schemas import (
    AuditReport,
    AuditSignal,
    AuditSummary,
    Graph3D,
    GraphEdge,
    GraphNode,
    RepoContext,
    RepoInfo,
    SignalLevel,
    TimelineWeek,
)

MAX_MODULES = 40


def map_path_to_module(path: str) -> str:
    """Cluster a file path into a 2-level module bucket.

    Examples:
      - 'a/b/c.py' -> 'a/b'
      - 'a/b.py'   -> 'a'
      - 'README.md' -> 'root'
    """
    normalized = path.strip().replace("\\", "/").strip("/")
    if not normalized:
        return "root"
    parts = PurePosixPath(normalized).parts
    if len(parts) <= 1:
        return "root"
    if len(parts) == 2:
        return parts[0]
    return f"{parts[0]}/{parts[1]}"


def _parse_iso_week(date_str: str | None) -> str:
    if not date_str:
        now = datetime.now(UTC)
        iso = now.isocalendar()
        return f"{iso.year}-W{iso.week:02d}"
    cleaned = date_str.strip()
    if cleaned.endswith("Z"):
        cleaned = cleaned[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(cleaned)
    except ValueError:
        dt = datetime.now(UTC)
    iso = dt.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def _infer_repo_context(
    author_commits: dict[str, int], total_commits: int
) -> tuple[RepoContext, str]:
    num_authors = len(author_commits)
    if num_authors <= 1:
        sole_author = next(iter(author_commits.keys()), "unknown")
        return (
            "solo",
            f"Dự án Solo (1 tác giả hoạt động: {sole_author}). "
            "Không áp dụng cảnh báo Bus Factor 1 người.",
        )

    top_author, top_count = max(author_commits.items(), key=lambda item: item[1])
    top_share = top_count / max(1, total_commits)
    if num_authors <= 2 and top_share >= 0.90:
        return (
            "solo",
            f"Dự án Solo có hỗ trợ phụ ({top_author} đóng góp {top_share:.0%} tổng số commit). "
            "Không phạt lỗi tập trung 1 người.",
        )

    if num_authors <= 6:
        return (
            "student_team",
            f"Nhóm đồ án ({num_authors} thành viên đóng góp trên kho mã nguồn).",
        )

    return (
        "open_source",
        f"Dự án cộng đồng / Open Source ({num_authors} contributors tham gia đóng góp).",
    )


def build_preview_audit(
    owner: str,
    repo_name: str,
    repo_url: str,
    commits: list[dict[str, Any]],
    prs: list[dict[str, Any]] | None = None,
) -> AuditReport:
    """Build a deterministic Live 3D Preview AuditReport from GitHub commits and PR telemetry."""
    prs = prs or []

    author_commits: dict[str, int] = defaultdict(int)
    author_labels: dict[str, str] = {}
    module_touches: dict[str, int] = defaultdict(int)
    module_lines: dict[str, int] = defaultdict(int)
    module_author_touches: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    module_max_single_commit_delta: dict[str, tuple[int, str]] = {}

    week_commits: dict[str, int] = defaultdict(int)
    week_additions: dict[str, int] = defaultdict(int)
    week_deletions: dict[str, int] = defaultdict(int)
    week_top_sha: dict[str, tuple[int, str]] = {}

    first_valid_sha = ""

    for commit in commits:
        sha = str(commit.get("sha") or "")[:7]
        if sha and not first_valid_sha:
            first_valid_sha = sha

        author_login = str(
            commit.get("author_login")
            or (commit.get("author") or {}).get("login")
            or ((commit.get("commit") or {}).get("author") or {}).get("name")
            or "unknown"
        ).strip()
        if not author_login:
            author_login = "unknown"

        author_name = str(
            commit.get("author_name")
            or ((commit.get("commit") or {}).get("author") or {}).get("name")
            or author_login
        ).strip()
        author_labels.setdefault(author_login, author_name)
        author_commits[author_login] += 1

        date_str = str(
            commit.get("date")
            or ((commit.get("commit") or {}).get("author") or {}).get("date")
            or ""
        )
        week_key = _parse_iso_week(date_str)
        week_commits[week_key] += 1

        raw_files = commit.get("files") or []
        clean_files = filter_changed_files(raw_files)

        commit_add = 0
        commit_del = 0
        per_mod_commit_delta: dict[str, int] = defaultdict(int)

        if clean_files:
            for f in clean_files:
                path = str(f.get("filename") or f.get("path") or "")
                mod = map_path_to_module(path)
                adds = int(f.get("additions") or 0)
                dels = int(f.get("deletions") or 0)
                delta = adds + dels

                commit_add += adds
                commit_del += dels
                module_touches[mod] += 1
                module_lines[mod] += max(1, delta)
                module_author_touches[mod][author_login] += 1
                per_mod_commit_delta[mod] += delta
        elif raw_files:
            # All changed files in this commit were filtered lockfiles/build artifacts
            pass
        else:
            # Fallback when commit list endpoint had no per-file breakdown
            mod = "root"
            adds = int(commit.get("additions") or 0)
            dels = int(commit.get("deletions") or 0)
            delta = adds + dels
            commit_add += adds
            commit_del += dels
            module_touches[mod] += 1
            module_lines[mod] += max(1, delta)
            module_author_touches[mod][author_login] += 1
            per_mod_commit_delta[mod] += delta

        for mod, mod_delta in per_mod_commit_delta.items():
            prev_max, _ = module_max_single_commit_delta.get(mod, (0, ""))
            if mod_delta >= prev_max:
                module_max_single_commit_delta[mod] = (mod_delta, sha or "HEAD")

        week_additions[week_key] += commit_add
        week_deletions[week_key] += commit_del
        commit_total_delta = commit_add + commit_del
        prev_w_delta, _ = week_top_sha.get(week_key, (-1, ""))
        if commit_total_delta > prev_w_delta and sha:
            week_top_sha[week_key] = (commit_total_delta, sha)

    # Cap at 40 largest modules; merge overflow into "other"
    sorted_modules = sorted(
        module_touches.keys(),
        key=lambda m: (module_lines[m], module_touches[m], m),
        reverse=True,
    )

    if len(sorted_modules) > MAX_MODULES:
        kept_set = set(sorted_modules[: MAX_MODULES - 1])
        if "other" in kept_set:
            kept_set = set(sorted_modules[:MAX_MODULES])

        merged_touches: dict[str, int] = defaultdict(int)
        merged_lines: dict[str, int] = defaultdict(int)
        merged_author_touches: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        merged_max_delta: dict[str, tuple[int, str]] = {}

        for mod in sorted_modules:
            target_mod = mod if mod in kept_set else "other"
            merged_touches[target_mod] += module_touches[mod]
            merged_lines[target_mod] += module_lines[mod]
            for login, cnt in module_author_touches[mod].items():
                merged_author_touches[target_mod][login] += cnt
            mod_max, mod_sha = module_max_single_commit_delta.get(mod, (0, ""))
            cur_max, _ = merged_max_delta.get(target_mod, (0, ""))
            if mod_max >= cur_max:
                merged_max_delta[target_mod] = (mod_max, mod_sha)

        module_touches = merged_touches
        module_lines = merged_lines
        module_author_touches = merged_author_touches
        module_max_single_commit_delta = merged_max_delta

    total_commits = sum(author_commits.values())
    context, context_reasoning = _infer_repo_context(author_commits, total_commits)
    num_authors = len(author_commits)

    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []
    signals: list[AuditSignal] = []

    for login, commit_count in sorted(author_commits.items(), key=lambda item: (-item[1], item[0])):
        nodes.append(
            GraphNode(
                id=f"author:{login}",
                type="author",
                label=author_labels.get(login, login),
                role="Contributor",
                size=max(1, commit_count),
                status="healthy",
            )
        )

    final_modules = sorted(
        module_touches.keys(),
        key=lambda m: (-module_lines[m], -module_touches[m], m),
    )

    for mod in final_modules:
        touches = module_touches[mod]
        lines = module_lines[mod]
        authors_map = module_author_touches[mod]
        top_author, top_author_touches = max(
            authors_map.items(), key=lambda item: item[1], default=("unknown", 0)
        )
        top_share = top_author_touches / max(1, touches)
        max_single_delta, max_sha = module_max_single_commit_delta.get(mod, (0, first_valid_sha))
        evidence_sha = max_sha or first_valid_sha or "HEAD"

        status: SignalLevel = "healthy"
        if max_single_delta >= 2500:
            status = "risk"
            signals.append(
                AuditSignal(
                    id=f"sig_dump_{len(signals) + 1:02d}",
                    node_id=f"mod:{mod}",
                    level="risk",
                    title=f"Đợt đẩy code khối lượng lớn vào module {mod}",
                    description=(
                        f"Phát hiện commit đơn lẻ thay đổi {max_single_delta} dòng trong "
                        f"module '{mod}' (ngưỡng cảnh báo >= 2500 dòng)."
                    ),
                    evidence_ref=f"commit:{evidence_sha}",
                    critic_note=(
                        "Live Preview Heuristic: Cần kiểm tra xem đây là code tự viết hay "
                        "tệp dữ liệu tĩnh/code sinh tự động."
                    ),
                )
            )
        elif num_authors > 1 and touches >= 5 and top_share >= 0.85:
            status = "risk"
            signals.append(
                AuditSignal(
                    id=f"sig_silo_{len(signals) + 1:02d}",
                    node_id=f"mod:{mod}",
                    level="risk",
                    title=f"Tập trung sở hữu mã nguồn cao tại module {mod}",
                    description=(
                        f"Thành viên '{top_author}' thực hiện {top_author_touches}/{touches} "
                        f"({top_share:.0%}) lượt chạm tại '{mod}' trong dự án nhiều thành viên."
                    ),
                    evidence_ref=f"commit:{evidence_sha}",
                    critic_note=(
                        "Live Preview Heuristic: Khuyến nghị giảng viên hỏi chéo các thành viên "
                        "khác về luồng xử lý của module này."
                    ),
                )
            )
        elif (num_authors > 1 and touches >= 3 and top_share >= 0.70) or touches >= 15:
            status = "probe"
            signals.append(
                AuditSignal(
                    id=f"sig_probe_{len(signals) + 1:02d}",
                    node_id=f"mod:{mod}",
                    level="probe",
                    title=f"Điểm nóng thay đổi hoặc tập trung tri thức tại {mod}",
                    description=(
                        f"Module '{mod}' có {touches} lượt chỉnh sửa (tác giả chính '{top_author}' "
                        f"chiếm {top_share:.0%}). Nên đặt câu hỏi kiểm tra hiểu biết khi bảo vệ."
                    ),
                    evidence_ref=f"commit:{evidence_sha}",
                    critic_note="Live Preview Heuristic: Tín hiệu gợi ý hỏi đáp chuyên môn.",
                )
            )

        nodes.append(
            GraphNode(
                id=f"mod:{mod}",
                type="module",
                label=mod,
                size=max(1, lines),
                churn=touches,
                status=status,
            )
        )

        for login, weight in sorted(authors_map.items(), key=lambda item: (-item[1], item[0])):
            if weight >= 1:
                edges.append(
                    GraphEdge(
                        source=f"author:{login}",
                        target=f"mod:{mod}",
                        weight=weight,
                    )
                )

    # Timeline 2D calculation with median anomaly rule
    sorted_weeks = sorted(week_commits.keys())
    commits_series = [week_commits[w] for w in sorted_weeks]
    delta_series = [week_additions[w] + week_deletions[w] for w in sorted_weeks]

    med_commits = float(median(commits_series)) if commits_series else 0.0
    med_delta = float(median(delta_series)) if delta_series else 0.0
    multi_week = len(sorted_weeks) >= 2

    timeline_2d: list[TimelineWeek] = []
    for w in sorted_weeks:
        c_cnt = week_commits[w]
        adds = week_additions[w]
        dels = week_deletions[w]
        total_delta = adds + dels

        if multi_week:
            is_anomaly = c_cnt >= max(5, 2 * med_commits) or total_delta >= max(1000, 3 * med_delta)
        else:
            is_anomaly = total_delta >= 2500

        timeline_2d.append(
            TimelineWeek(
                week=w,
                commits=c_cnt,
                additions=adds,
                deletions=dels,
                anomaly=bool(is_anomaly),
            )
        )

        if is_anomaly:
            _, w_sha = week_top_sha.get(w, (0, first_valid_sha or "HEAD"))
            target_node_id = (
                f"mod:{final_modules[0]}"
                if final_modules
                else (nodes[0].id if nodes else "mod:root")
            )
            signals.append(
                AuditSignal(
                    id=f"sig_week_{len(signals) + 1:02d}",
                    node_id=target_node_id,
                    level="probe",
                    title=f"Biến động nhịp độ commit bất thường trong tuần {w}",
                    description=(
                        f"Tuần {w} ghi nhận {c_cnt} commits (+{adds}/-{dels} dòng), "
                        "cao đột biến so với mức trung vị của dự án."
                    ),
                    evidence_ref=f"commit:{w_sha or 'HEAD'}",
                    critic_note=(
                        "Live Preview Heuristic: Kiểm tra xem tuần này có gộp nhánh lớn "
                        "hoặc chạy nước rút trước hạn nộp hay không."
                    ),
                )
            )

    if prs:
        first_pr_num = prs[0].get("number")
        if first_pr_num and final_modules and not signals:
            signals.append(
                AuditSignal(
                    id="sig_pr_01",
                    node_id=f"mod:{final_modules[0]}",
                    level="probe",
                    title=f"Đối chiếu quy trình Pull Request trên {final_modules[0]}",
                    description=(
                        f"Dự án có {len(prs)} Pull Request gần nhất (tiêu biểu PR#{first_pr_num})."
                    ),
                    evidence_ref=f"PR#{first_pr_num}",
                    critic_note="Live Preview Heuristic: Gợi ý đối chiếu lịch sử review PR.",
                )
            )

    digest = hashlib.sha1(f"{owner}/{repo_name}".encode()).hexdigest()[:8]
    now_iso = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    overview = (
        f"Live 3D Preview cho {owner}/{repo_name}: phân tích {total_commits} commits, "
        f"{len(prs)} PRs từ {num_authors} tác giả trên {len(final_modules)} cụm module "
        f"(ngữ cảnh tự động: {context})."
    )

    return AuditReport(
        audit_id=f"aud_preview_{digest}",
        created_at=now_iso,
        mode="live_preview",
        repo=RepoInfo(
            name=repo_name,
            url=repo_url,
            context=context,
            context_reasoning=context_reasoning,
        ),
        summary=AuditSummary(
            overview=overview,
            human_notes=(
                "Bản xem nhanh Live 3D Preview từ GitHub REST API (chưa qua vòng phản biện "
                "Deep AI Audit 5 trạm trên Antigravity MCP)."
            ),
        ),
        graph_3d=Graph3D(nodes=nodes, edges=edges),
        timeline_2d=timeline_2d,
        signals=signals,
        interview_questions=[],
    )
