from app.core.schemas import (
    AuditReport,
    AuditSignal,
    AuditSummary,
    Graph3D,
    GraphEdge,
    GraphNode,
    InterviewQuestion,
    RepoInfo,
    TimelineWeek,
)


def get_sample_audits() -> list[AuditReport]:
    """Return 3 pre-validated Deep AI Audit sample records for local demo and testing."""
    student_team_audit = AuditReport(
        audit_id="aud_sample_student_team",
        created_at="2026-11-23T08:00:00Z",
        mode="deep_ai_audit",
        repo=RepoInfo(
            name="vku-edutrack-capstone",
            url="https://github.com/vku-capstone/vku-edutrack-capstone",
            context="student_team",
            context_reasoning=(
                "Nhóm đồ án gồm 3 sinh viên VKU phân chia rõ Backend, Frontend và QA/Docs, "
                "làm việc qua Pull Request và GitHub Projects trong 2 Sprint."
            ),
        ),
        summary=AuditSummary(
            overview=(
                "Nhịp độ đóng góp rải đều trong 5 tuần đầu nhưng xuất hiện 1 đợt commit dồn "
                "vào tuần W46 ở cụm thanh toán và báo cáo. Kiến trúc tách lớp rõ ràng, "
                "cần hỏi đáp sâu về module payment và phân quyền."
            ),
            human_notes=(
                "PM xác nhận tuần W46 nhóm tích hợp cổng thanh toán sandbox nên phát sinh "
                "nhiều dòng cấu hình mẫu, không phải sao chép mã nguồn."
            ),
        ),
        graph_3d=Graph3D(
            nodes=[
                GraphNode(
                    id="author:minhquan-vku",
                    type="author",
                    label="Trần Minh Quân",
                    role="Team Lead / Backend",
                    size=56,
                    status="healthy",
                ),
                GraphNode(
                    id="author:thuylinh-vku",
                    type="author",
                    label="Nguyễn Thùy Linh",
                    role="Frontend Engineer",
                    size=44,
                    status="healthy",
                ),
                GraphNode(
                    id="author:hoangnam-vku",
                    type="author",
                    label="Lê Hoàng Nam",
                    role="Auth / QA & Docs",
                    size=28,
                    status="probe",
                ),
                GraphNode(
                    id="mod:backend/api",
                    type="module",
                    label="backend/api",
                    size=1420,
                    churn=26,
                    status="healthy",
                ),
                GraphNode(
                    id="mod:backend/payment",
                    type="module",
                    label="backend/payment",
                    size=1980,
                    churn=19,
                    status="risk",
                ),
                GraphNode(
                    id="mod:backend/auth",
                    type="module",
                    label="backend/auth",
                    size=860,
                    churn=15,
                    status="probe",
                ),
                GraphNode(
                    id="mod:backend/models",
                    type="module",
                    label="backend/models",
                    size=640,
                    churn=12,
                    status="healthy",
                ),
                GraphNode(
                    id="mod:backend/tests",
                    type="module",
                    label="backend/tests",
                    size=780,
                    churn=14,
                    status="healthy",
                ),
                GraphNode(
                    id="mod:frontend/dashboard",
                    type="module",
                    label="frontend/dashboard",
                    size=1540,
                    churn=24,
                    status="healthy",
                ),
                GraphNode(
                    id="mod:frontend/checkout",
                    type="module",
                    label="frontend/checkout",
                    size=1120,
                    churn=17,
                    status="probe",
                ),
                GraphNode(
                    id="mod:frontend/components",
                    type="module",
                    label="frontend/components",
                    size=920,
                    churn=20,
                    status="healthy",
                ),
                GraphNode(
                    id="mod:frontend/hooks",
                    type="module",
                    label="frontend/hooks",
                    size=510,
                    churn=11,
                    status="healthy",
                ),
                GraphNode(
                    id="mod:docs/architecture",
                    type="module",
                    label="docs/architecture",
                    size=480,
                    churn=9,
                    status="healthy",
                ),
                GraphNode(
                    id="mod:docs/testing",
                    type="module",
                    label="docs/testing",
                    size=410,
                    churn=8,
                    status="healthy",
                ),
            ],
            edges=[
                GraphEdge(source="author:minhquan-vku", target="mod:backend/api", weight=22),
                GraphEdge(source="author:minhquan-vku", target="mod:backend/payment", weight=18),
                GraphEdge(source="author:minhquan-vku", target="mod:backend/models", weight=10),
                GraphEdge(source="author:minhquan-vku", target="mod:backend/tests", weight=8),
                GraphEdge(source="author:thuylinh-vku", target="mod:frontend/dashboard", weight=21),
                GraphEdge(source="author:thuylinh-vku", target="mod:frontend/checkout", weight=15),
                GraphEdge(
                    source="author:thuylinh-vku", target="mod:frontend/components", weight=18
                ),
                GraphEdge(source="author:thuylinh-vku", target="mod:frontend/hooks", weight=11),
                GraphEdge(source="author:hoangnam-vku", target="mod:backend/auth", weight=14),
                GraphEdge(source="author:hoangnam-vku", target="mod:backend/tests", weight=6),
                GraphEdge(source="author:hoangnam-vku", target="mod:docs/architecture", weight=9),
                GraphEdge(source="author:hoangnam-vku", target="mod:docs/testing", weight=8),
                GraphEdge(source="author:minhquan-vku", target="mod:backend/auth", weight=3),
                GraphEdge(source="author:thuylinh-vku", target="mod:backend/api", weight=4),
            ],
        ),
        timeline_2d=[
            TimelineWeek(week="2026-W42", commits=14, additions=680, deletions=110, anomaly=False),
            TimelineWeek(week="2026-W43", commits=16, additions=820, deletions=190, anomaly=False),
            TimelineWeek(week="2026-W44", commits=12, additions=540, deletions=130, anomaly=False),
            TimelineWeek(week="2026-W45", commits=15, additions=710, deletions=160, anomaly=False),
            TimelineWeek(week="2026-W46", commits=34, additions=2950, deletions=420, anomaly=True),
            TimelineWeek(week="2026-W47", commits=11, additions=490, deletions=140, anomaly=False),
        ],
        signals=[
            AuditSignal(
                id="sig_team_01",
                node_id="mod:backend/payment",
                level="risk",
                title="Đợt đẩy code khối lượng lớn thiếu review chéo ở module thanh toán",
                description=(
                    "Module backend/payment nhận 1.980 dòng thay đổi trong tuần 2026-W46 "
                    "chủ yếu từ một thành viên duy nhất (94% số lần chạm) và thiếu test lỗi mạng."
                ),
                evidence_ref="commit:a4f91c2",
                critic_note=(
                    "Đã kiểm tra diff commit:a4f91c2: phần lớn là xử lý webhook VNPay sandbox, "
                    "nhưng việc thiếu unit test cho kịch bản chữ ký sai vẫn giữ ở mức risk."
                ),
            ),
            AuditSignal(
                id="sig_team_02",
                node_id="mod:backend/auth",
                level="probe",
                title="Cơ chế làm mới JWT và phân quyền RBAC chỉ do 1 thành viên nắm giữ",
                description=(
                    "Thành viên Lê Hoàng Nam thực hiện 14/17 lượt sửa trên backend/auth "
                    "trong PR#19 mà không có bình luận review chi tiết từ Team Lead."
                ),
                evidence_ref="PR#19",
                critic_note=(
                    "Code tuân thủ chuẩn FastAPI Security nên hạ từ risk xuống probe; "
                    "giảng viên nên hỏi trực tiếp cơ chế thu hồi refresh token."
                ),
            ),
            AuditSignal(
                id="sig_team_03",
                node_id="mod:frontend/checkout",
                level="probe",
                title="Xử lý trạng thái thanh toán bất đồng bộ trên giao diện Checkout",
                description=(
                    "PR#24 cập nhật luồng polling kết quả giao dịch nhưng chưa thấy "
                    "xử lý rõ trường hợp người dùng đóng tab giữa chừng."
                ),
                evidence_ref="PR#24",
                critic_note=(
                    "Logic UI gọn gàng, chỉ cần hỏi thêm sinh viên Frontend về trải nghiệm "
                    "khôi phục đơn hàng khi mất kết nối."
                ),
            ),
        ],
        interview_questions=[
            InterviewQuestion(
                author_id="author:minhquan-vku",
                author_name="Trần Minh Quân",
                question=(
                    "Trong commit:a4f91c2 ở module backend/payment, em làm thế nào để đảm bảo "
                    "tính idempotent khi cổng thanh toán gửi trùng webhook callback 2 lần?"
                ),
                evidence_ref="commit:a4f91c2",
            ),
            InterviewQuestion(
                author_id="author:hoangnam-vku",
                author_name="Lê Hoàng Nam",
                question=(
                    "Ở PR#19 (backend/auth), nếu access token bị lộ trước khi hết hạn thì hệ thống "
                    "kiểm tra hay thu hồi quyền truy cập của người dùng bằng cách nào?"
                ),
                evidence_ref="PR#19",
            ),
            InterviewQuestion(
                author_id="author:thuylinh-vku",
                author_name="Nguyễn Thùy Linh",
                question=(
                    "Trong PR#24 (frontend/checkout), khi API backend trả về lỗi 429 hoặc timeout, "
                    "state của form thanh toán được khóa và thông báo lại cho người dùng ra sao?"
                ),
                evidence_ref="PR#24",
            ),
        ],
    )

    solo_audit = AuditReport(
        audit_id="aud_sample_solo",
        created_at="2026-11-23T09:00:00Z",
        mode="deep_ai_audit",
        repo=RepoInfo(
            name="vku-sprintguard",
            url="https://github.com/NhatCam2006/vku-sprintguard",
            context="solo",
            context_reasoning=(
                "Dự án cá nhân (1 Human PM/Dev @NhatCam2006 điều phối AI Swarm). "
                "Hệ thống tự động tắt cảnh báo Bus Factor 1 người để tránh báo động giả, "
                "chuyển trọng tâm sang kiểm tra kỷ luật tách PR, CI tự động và độ phủ test."
            ),
        ),
        summary=AuditSummary(
            overview=(
                "Dự án Solo tuân thủ nghiêm ngặt quy trình Feature Branch, Pull Request "
                "và GitHub Actions CI. Cấu trúc tách rõ backend/core, frontend 3D và "
                "docs/planning. Không phạt lỗi một người gánh toàn bộ repo; chỉ gắn tín hiệu "
                "probe ở các cụm thuật toán gom cụm 3D và đồng bộ MCP để giảng viên hỏi sâu."
            ),
            human_notes=(
                "Sinh viên thực hiện theo mô hình 1 Human PM + Antigravity Swarm, "
                "mọi PR đều có kiểm thử pytest và vitest tự động trước khi merge."
            ),
        ),
        graph_3d=Graph3D(
            nodes=[
                GraphNode(
                    id="author:nhatcam2006",
                    type="author",
                    label="Đinh Nhật Cảm (NhatCam2006)",
                    role="Human PM / Full-Stack Architect",
                    size=64,
                    status="healthy",
                ),
                GraphNode(
                    id="mod:backend/core",
                    type="module",
                    label="backend/core",
                    size=1280,
                    churn=18,
                    status="probe",
                ),
                GraphNode(
                    id="mod:backend/db",
                    type="module",
                    label="backend/db",
                    size=540,
                    churn=9,
                    status="healthy",
                ),
                GraphNode(
                    id="mod:backend/tests",
                    type="module",
                    label="backend/tests",
                    size=860,
                    churn=14,
                    status="healthy",
                ),
                GraphNode(
                    id="mod:frontend/components",
                    type="module",
                    label="frontend/components",
                    size=1350,
                    churn=16,
                    status="probe",
                ),
                GraphNode(
                    id="mod:frontend/styles",
                    type="module",
                    label="frontend/styles",
                    size=420,
                    churn=7,
                    status="healthy",
                ),
                GraphNode(
                    id="mod:docs/planning",
                    type="module",
                    label="docs/planning",
                    size=980,
                    churn=12,
                    status="healthy",
                ),
            ],
            edges=[
                GraphEdge(source="author:nhatcam2006", target="mod:backend/core", weight=18),
                GraphEdge(source="author:nhatcam2006", target="mod:backend/db", weight=9),
                GraphEdge(source="author:nhatcam2006", target="mod:backend/tests", weight=14),
                GraphEdge(source="author:nhatcam2006", target="mod:frontend/components", weight=16),
                GraphEdge(source="author:nhatcam2006", target="mod:frontend/styles", weight=7),
                GraphEdge(source="author:nhatcam2006", target="mod:docs/planning", weight=12),
            ],
        ),
        timeline_2d=[
            TimelineWeek(week="2026-W45", commits=10, additions=620, deletions=80, anomaly=False),
            TimelineWeek(week="2026-W46", commits=14, additions=940, deletions=150, anomaly=False),
            TimelineWeek(week="2026-W47", commits=18, additions=1180, deletions=210, anomaly=False),
        ],
        signals=[
            AuditSignal(
                id="sig_solo_01",
                node_id="mod:backend/core",
                level="probe",
                title="Thuật toán giới hạn 40 cụm module và kiểm soát hạn mức GitHub API",
                description=(
                    "Module backend/core chịu trách nhiệm gom cụm cây thư mục 2 cấp và gọi "
                    "GitHub REST API. Cần xác minh cách xử lý khi repo mục tiêu vượt quá 40 module."
                ),
                evidence_ref="PR#16",
                critic_note=(
                    "Ngữ cảnh Solo: việc 1 tác giả sở hữu 100% commit là hoàn toàn hợp lệ. "
                    "Chỉ đặt mức probe để giảng viên kiểm tra hiểu biết sâu về thuật toán."
                ),
            ),
            AuditSignal(
                id="sig_solo_02",
                node_id="mod:frontend/components",
                level="probe",
                title="Tối ưu hiệu năng dựng đồ thị 3D và điều hướng Camera Fly-to",
                description=(
                    "Cụm frontend/components kết hợp Three.js / react-force-graph-3d với "
                    "chế độ lọc X-Ray và Focus Mode trên nền sáng Interstellar."
                ),
                evidence_ref="commit:6d27bc6",
                critic_note=(
                    "Mã nguồn tách component rõ ràng, không dùng thư viện thừa; "
                    "giữ mức probe để hỏi đáp về cơ chế đồng bộ state giữa Side Inspector và 3D."
                ),
            ),
        ],
        interview_questions=[
            InterviewQuestion(
                author_id="author:nhatcam2006",
                author_name="Đinh Nhật Cảm (NhatCam2006)",
                question=(
                    "Vì sao em chọn ngưỡng gom tối đa 40 module ở độ sâu 2 cấp thư mục trong "
                    "backend/core mà không vẽ trực tiếp từng file lẻ lên không gian 3D?"
                ),
                evidence_ref="PR#16",
            ),
            InterviewQuestion(
                author_id="author:nhatcam2006",
                author_name="Đinh Nhật Cảm (NhatCam2006)",
                question=(
                    "Khi người dùng dán một repo công khai lên Live 3D Preview mà không cấu hình "
                    "GITHUB_TOKEN, backend bảo vệ hạn mức 60 request/giờ của GitHub API ra sao?"
                ),
                evidence_ref="commit:6d27bc6",
            ),
        ],
    )

    open_source_audit = AuditReport(
        audit_id="aud_sample_open_source",
        created_at="2026-11-23T09:30:00Z",
        mode="deep_ai_audit",
        repo=RepoInfo(
            name="fastapi-mcp-bridge",
            url="https://github.com/oss-vietnam/fastapi-mcp-bridge",
            context="open_source",
            context_reasoning=(
                "Dự án mã nguồn mở cộng đồng với nhóm Maintainer cốt lõi và nhiều Contributor "
                "đóng góp qua Pull Request độc lập, có quy trình release định kỳ."
            ),
        ),
        summary=AuditSummary(
            overview=(
                "Cộng đồng đóng góp sôi nổi trên các nhánh adapter và tài liệu. "
                "Tuy nhiên cụm lõi transport SSE/Stdio đang tập trung cao vào 1 Maintainer "
                "và có PR refactor lớn cần kiểm tra tương thích ngược."
            ),
            human_notes=(
                "Dữ liệu mẫu đối chiếu ngữ cảnh Open Source giúp phân biệt hành vi "
                "Maintainer cốt lõi với mô hình nhóm sinh viên đồng cấp."
            ),
        ),
        graph_3d=Graph3D(
            nodes=[
                GraphNode(
                    id="author:alex-maintainer",
                    type="author",
                    label="Alex Nguyen (Core Maintainer)",
                    role="Lead Maintainer",
                    size=60,
                    status="healthy",
                ),
                GraphNode(
                    id="author:baotran-oss",
                    type="author",
                    label="Bảo Trân",
                    role="Core Contributor",
                    size=38,
                    status="healthy",
                ),
                GraphNode(
                    id="author:david-dev",
                    type="author",
                    label="David Pham",
                    role="Adapter Contributor",
                    size=25,
                    status="healthy",
                ),
                GraphNode(
                    id="author:mai-docs",
                    type="author",
                    label="Mai Lê",
                    role="Docs & Examples",
                    size=19,
                    status="healthy",
                ),
                GraphNode(
                    id="mod:src/transport",
                    type="module",
                    label="src/transport",
                    size=1640,
                    churn=28,
                    status="probe",
                ),
                GraphNode(
                    id="mod:src/schema_gen",
                    type="module",
                    label="src/schema_gen",
                    size=1120,
                    churn=21,
                    status="healthy",
                ),
                GraphNode(
                    id="mod:src/auth_guard",
                    type="module",
                    label="src/auth_guard",
                    size=890,
                    churn=16,
                    status="probe",
                ),
                GraphNode(
                    id="mod:tests/integration",
                    type="module",
                    label="tests/integration",
                    size=940,
                    churn=18,
                    status="healthy",
                ),
                GraphNode(
                    id="mod:examples/quickstart",
                    type="module",
                    label="examples/quickstart",
                    size=520,
                    churn=11,
                    status="healthy",
                ),
            ],
            edges=[
                GraphEdge(source="author:alex-maintainer", target="mod:src/transport", weight=24),
                GraphEdge(source="author:alex-maintainer", target="mod:src/schema_gen", weight=12),
                GraphEdge(source="author:baotran-oss", target="mod:src/schema_gen", weight=14),
                GraphEdge(source="author:baotran-oss", target="mod:tests/integration", weight=15),
                GraphEdge(source="author:david-dev", target="mod:src/auth_guard", weight=13),
                GraphEdge(source="author:david-dev", target="mod:tests/integration", weight=6),
                GraphEdge(source="author:mai-docs", target="mod:examples/quickstart", weight=11),
            ],
        ),
        timeline_2d=[
            TimelineWeek(week="2026-W43", commits=19, additions=890, deletions=240, anomaly=False),
            TimelineWeek(week="2026-W44", commits=22, additions=1020, deletions=310, anomaly=False),
            TimelineWeek(week="2026-W45", commits=17, additions=740, deletions=190, anomaly=False),
            TimelineWeek(week="2026-W46", commits=21, additions=960, deletions=280, anomaly=False),
        ],
        signals=[
            AuditSignal(
                id="sig_oss_01",
                node_id="mod:src/transport",
                level="probe",
                title="Tập trung tri thức cao ở tầng giao vận src/transport",
                description=(
                    "Core Maintainer nắm 85% số lần chỉnh sửa ở src/transport; "
                    "cần thêm tài liệu hướng dẫn kiến trúc để contributor mới dễ tham gia review."
                ),
                evidence_ref="PR#108",
                critic_note=(
                    "Trong dự án Open Source, việc Lead Maintainer giữ nhịp module lõi là bình "
                    "thường, nhưng vẫn đánh dấu probe để khuyến nghị bổ sung reviewer phụ."
                ),
            ),
            AuditSignal(
                id="sig_oss_02",
                node_id="mod:src/auth_guard",
                level="probe",
                title="Mở rộng middleware xác thực Header Token cho nhiều client",
                description=(
                    "PR#112 bổ sung cơ chế xoay vòng API key cho MCP transport, "
                    "cần kiểm tra thêm test case khi header rỗng."
                ),
                evidence_ref="PR#112",
                critic_note="Đã có integration test cơ bản, chỉ cần xác nhận thêm edge case.",
            ),
        ],
        interview_questions=[
            InterviewQuestion(
                author_id="author:alex-maintainer",
                author_name="Alex Nguyen (Core Maintainer)",
                question=(
                    "Trong PR#108, cơ chế đóng kết nối grace period của src/transport hoạt động "
                    "như thế nào khi client ngắt kết nối đột ngột?"
                ),
                evidence_ref="PR#108",
            ),
            InterviewQuestion(
                author_id="author:david-dev",
                author_name="David Pham",
                question=(
                    "Ở PR#112 (src/auth_guard), vì sao bạn chọn so sánh khóa bằng hằng số thời "
                    "gian thay vì toán tử so sánh chuỗi thông thường?"
                ),
                evidence_ref="PR#112",
            ),
        ],
    )

    return [student_team_audit, solo_audit, open_source_audit]
