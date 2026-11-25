from app.core.schemas import (
    AuditReport,
    AuditSignal,
    AuditSummary,
    CommitHighlight,
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
                    description=(
                        "Thành viên 'Trần Minh Quân' đóng góp 56/128 commit (44%), phụ trách "
                        "kiến trúc REST API, tích hợp thanh toán VNPay và tầng ORM."
                    ),
                ),
                GraphNode(
                    id="author:thuylinh-vku",
                    type="author",
                    label="Nguyễn Thùy Linh",
                    role="Frontend Engineer",
                    size=44,
                    status="healthy",
                    description=(
                        "Thành viên 'Nguyễn Thùy Linh' đóng góp 44/128 commit (34%), xây dựng "
                        "giao diện Dashboard học vụ, luồng Checkout và thư viện UI Component."
                    ),
                ),
                GraphNode(
                    id="author:hoangnam-vku",
                    type="author",
                    label="Lê Hoàng Nam",
                    role="Auth / QA & Docs",
                    size=28,
                    status="probe",
                    description=(
                        "Thành viên 'Lê Hoàng Nam' đóng góp 28/128 commit (22%), đảm nhiệm "
                        "xác thực JWT/RBAC, kiểm thử tự động và tài liệu kiến trúc hệ thống."
                    ),
                ),
                GraphNode(
                    id="mod:backend/api",
                    type="module",
                    label="backend/api",
                    size=1420,
                    churn=26,
                    status="healthy",
                    description=(
                        "Tầng định tuyến REST API chính xử lý khóa học, lịch học và hồ sơ "
                        "sinh viên với 26 lượt chạm từ cả Backend và Frontend. Phân tích "
                        "trực tiếp từ mã nguồn, không dựa vào README."
                    ),
                    key_files=[
                        "backend/api/courses.py",
                        "backend/api/enrollments.py",
                        "backend/api/dependencies.py",
                    ],
                ),
                GraphNode(
                    id="mod:backend/payment",
                    type="module",
                    label="backend/payment",
                    size=1980,
                    churn=19,
                    status="risk",
                    description=(
                        "Module tích hợp cổng thanh toán học phí VNPay Sandbox và đối soát "
                        "webhook IPN (1.980 dòng thay đổi, tập trung 94% vào 1 thành viên). "
                        "Phân tích trực tiếp từ mã nguồn, không dựa vào README."
                    ),
                    key_files=[
                        "backend/payment/vnpay_gateway.py",
                        "backend/payment/webhook_handler.py",
                        "backend/payment/reconcile.py",
                    ],
                ),
                GraphNode(
                    id="mod:backend/auth",
                    type="module",
                    label="backend/auth",
                    size=860,
                    churn=15,
                    status="probe",
                    description=(
                        "Thành phần xác thực người dùng, cấp phát JWT Access/Refresh Token và "
                        "kiểm tra phân quyền RBAC theo vai trò Giảng viên / Sinh viên. "
                        "Phân tích trực tiếp từ mã nguồn, không dựa vào README."
                    ),
                    key_files=[
                        "backend/auth/jwt_handler.py",
                        "backend/auth/rbac_guard.py",
                        "backend/auth/password.py",
                    ],
                ),
                GraphNode(
                    id="mod:backend/models",
                    type="module",
                    label="backend/models",
                    size=640,
                    churn=12,
                    status="healthy",
                    description=(
                        "Định nghĩa lược đồ cơ sở dữ liệu SQLAlchemy và Pydantic DTO cho sinh "
                        "viên, học phần và hóa đơn học phí. Phân tích trực tiếp từ mã nguồn, "
                        "không dựa vào README."
                    ),
                    key_files=[
                        "backend/models/student.py",
                        "backend/models/course.py",
                        "backend/models/invoice.py",
                    ],
                ),
                GraphNode(
                    id="mod:backend/tests",
                    type="module",
                    label="backend/tests",
                    size=780,
                    churn=14,
                    status="healthy",
                    description=(
                        "Bộ kiểm thử tự động Pytest cho các endpoint đăng ký tín chỉ và xác thực "
                        "JWT, có sự phối hợp giữa 2 thành viên. Phân tích trực tiếp từ mã nguồn, "
                        "không dựa vào README."
                    ),
                    key_files=[
                        "backend/tests/test_courses_api.py",
                        "backend/tests/test_auth_rbac.py",
                        "backend/tests/conftest.py",
                    ],
                ),
                GraphNode(
                    id="mod:frontend/dashboard",
                    type="module",
                    label="frontend/dashboard",
                    size=1540,
                    churn=24,
                    status="healthy",
                    description=(
                        "Không gian bảng điều khiển tiến độ học tập, thống kê tín chỉ và lịch "
                        "thi dành cho sinh viên VKU. Phân tích trực tiếp từ mã nguồn, không "
                        "dựa vào README."
                    ),
                    key_files=[
                        "frontend/dashboard/StudentDashboard.tsx",
                        "frontend/dashboard/CreditProgressChart.tsx",
                        "frontend/dashboard/ScheduleView.tsx",
                    ],
                ),
                GraphNode(
                    id="mod:frontend/checkout",
                    type="module",
                    label="frontend/checkout",
                    size=1120,
                    churn=17,
                    status="probe",
                    description=(
                        "Giao diện thanh toán học phí trực tuyến, tạo mã QR và polling trạng "
                        "thái giao dịch bất đồng bộ. Phân tích trực tiếp từ mã nguồn, không "
                        "dựa vào README."
                    ),
                    key_files=[
                        "frontend/checkout/PaymentFlow.tsx",
                        "frontend/checkout/TransactionPoller.ts",
                        "frontend/checkout/ReceiptModal.tsx",
                    ],
                ),
                GraphNode(
                    id="mod:frontend/components",
                    type="module",
                    label="frontend/components",
                    size=920,
                    churn=20,
                    status="healthy",
                    description=(
                        "Thư viện thành phần giao diện dùng chung (Navbar, Modal, DataTable, "
                        "StatusBadge) phục vụ toàn bộ ứng dụng React. Phân tích trực tiếp từ "
                        "mã nguồn, không dựa vào README."
                    ),
                    key_files=[
                        "frontend/components/DataTable.tsx",
                        "frontend/components/AppNavbar.tsx",
                        "frontend/components/StatusBadge.tsx",
                    ],
                ),
                GraphNode(
                    id="mod:frontend/hooks",
                    type="module",
                    label="frontend/hooks",
                    size=510,
                    churn=11,
                    status="healthy",
                    description=(
                        "Tập hợp Custom React Hooks quản lý phiên đăng nhập, gọi API có cache "
                        "và đồng bộ thông báo thời gian thực. Phân tích trực tiếp từ mã nguồn, "
                        "không dựa vào README."
                    ),
                    key_files=[
                        "frontend/hooks/useAuthSession.ts",
                        "frontend/hooks/useCourseQuery.ts",
                    ],
                ),
                GraphNode(
                    id="mod:docs/architecture",
                    type="module",
                    label="docs/architecture",
                    size=480,
                    churn=9,
                    status="healthy",
                    description=(
                        "Tài liệu thiết kế kiến trúc hệ thống, lược đồ ERD và đặc tả luồng "
                        "tích hợp thanh toán học phí. Phân tích trực tiếp từ lịch sử Git diff."
                    ),
                    key_files=[
                        "docs/architecture/system-context.md",
                        "docs/architecture/erd-schema.md",
                    ],
                ),
                GraphNode(
                    id="mod:docs/testing",
                    type="module",
                    label="docs/testing",
                    size=410,
                    churn=8,
                    status="healthy",
                    description=(
                        "Kịch bản kiểm thử chấp nhận (UAT) và báo cáo kiểm thử tích hợp qua "
                        "các Sprint đồ án. Phân tích trực tiếp từ lịch sử Git diff."
                    ),
                    key_files=[
                        "docs/testing/uat-test-cases.md",
                        "docs/testing/sprint2-qa-report.md",
                    ],
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
        commit_highlights=[
            CommitHighlight(
                ref="commit:a4f91c2",
                url="https://github.com/vku-capstone/vku-edutrack-capstone/commit/a4f91c2",
                author="minhquan-vku",
                date="2026-11-14T16:40:00Z",
                title="feat(payment): integrate VNPay sandbox gateway and IPN webhook",
                diff_summary="+1420 / -110 dòng trên 4 tệp mã nguồn thật",
                files_changed=[
                    "backend/payment/vnpay_gateway.py",
                    "backend/payment/webhook_handler.py",
                    "backend/payment/reconcile.py",
                ],
            ),
            CommitHighlight(
                ref="PR#19",
                url="https://github.com/vku-capstone/vku-edutrack-capstone/pull/19",
                author="hoangnam-vku",
                date="2026-11-10T09:15:00Z",
                title="feat(auth): implement JWT refresh rotation and RBAC middleware",
                diff_summary="+540 / -65 dòng trên 3 tệp mã nguồn thật",
                files_changed=[
                    "backend/auth/jwt_handler.py",
                    "backend/auth/rbac_guard.py",
                ],
            ),
            CommitHighlight(
                ref="PR#24",
                url="https://github.com/vku-capstone/vku-edutrack-capstone/pull/24",
                author="thuylinh-vku",
                date="2026-11-16T14:20:00Z",
                title="feat(checkout): async transaction status polling and QR receipt modal",
                diff_summary="+680 / -90 dòng trên 3 tệp mã nguồn thật",
                files_changed=[
                    "frontend/checkout/PaymentFlow.tsx",
                    "frontend/checkout/TransactionPoller.ts",
                ],
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
                    description=(
                        "Thành viên 'Đinh Nhật Cảm (NhatCam2006)' đóng góp 64/64 commit (100%), "
                        "thiết kế kiến trúc 3 tầng, điều phối AI Swarm và kiểm duyệt toàn bộ PR."
                    ),
                ),
                GraphNode(
                    id="mod:backend/core",
                    type="module",
                    label="backend/core",
                    size=1280,
                    churn=18,
                    status="probe",
                    description=(
                        "Lõi phân tích Git telemetry, bộ lọc chống nhiễu lockfile/minified, "
                        "thuật toán gom tối đa 40 cụm module 2 cấp và suy luận ngữ cảnh dự án. "
                        "Phân tích trực tiếp từ mã nguồn, không dựa vào README."
                    ),
                    key_files=[
                        "backend/app/core/module_clusterer.py",
                        "backend/app/core/diff_filter.py",
                        "backend/app/core/github_client.py",
                        "backend/app/core/schemas.py",
                    ],
                ),
                GraphNode(
                    id="mod:backend/db",
                    type="module",
                    label="backend/db",
                    size=540,
                    churn=9,
                    status="healthy",
                    description=(
                        "Tầng lưu trữ SQLite thuần với cơ chế tự động khởi tạo schema và nạp "
                        "dữ liệu mẫu idempotent khi khởi động. Phân tích trực tiếp từ mã nguồn, "
                        "không dựa vào README."
                    ),
                    key_files=[
                        "backend/app/db/sqlite_store.py",
                        "backend/app/seed/sample_audits.py",
                    ],
                ),
                GraphNode(
                    id="mod:backend/tests",
                    type="module",
                    label="backend/tests",
                    size=860,
                    churn=14,
                    status="healthy",
                    description=(
                        "Hệ thống kiểm thử tự động Pytest kiểm chứng bộ lọc diff, gom cụm 3D, "
                        "REST API endpoints và máy trạng thái MCP 6 công cụ. Phân tích trực tiếp "
                        "từ mã nguồn, không dựa vào README."
                    ),
                    key_files=[
                        "backend/tests/test_diff_filter_and_clusterer.py",
                        "backend/tests/test_mcp_harness.py",
                        "backend/tests/test_preview_api.py",
                        "backend/tests/test_schemas_and_store.py",
                    ],
                ),
                GraphNode(
                    id="mod:frontend/components",
                    type="module",
                    label="frontend/components",
                    size=1350,
                    churn=16,
                    status="probe",
                    description=(
                        "Không gian 3D Contribution Force-Graph, thanh công cụ X-Ray / Focus "
                        "Mode, biểu đồ 2D Commit Timeline và bảng Side Inspector tiếng Việt. "
                        "Phân tích trực tiếp từ mã nguồn, không dựa vào README."
                    ),
                    key_files=[
                        "frontend/src/components/Graph3DScene.tsx",
                        "frontend/src/components/SideInspector.tsx",
                        "frontend/src/components/TimelineStrip.tsx",
                    ],
                ),
                GraphNode(
                    id="mod:frontend/styles",
                    type="module",
                    label="frontend/styles",
                    size=420,
                    churn=7,
                    status="healthy",
                    description=(
                        "Hệ thống thiết kế giao diện Interstellar Light-First (#F8FAFC), bảng "
                        "màu ngữ nghĩa và bố cục cố định chống vỡ khung nhìn 3D. Phân tích "
                        "trực tiếp từ mã nguồn, không dựa vào README."
                    ),
                    key_files=[
                        "frontend/src/index.css",
                        "frontend/src/App.tsx",
                    ],
                ),
                GraphNode(
                    id="mod:docs/planning",
                    type="module",
                    label="docs/planning",
                    size=980,
                    churn=12,
                    status="healthy",
                    description=(
                        "Hồ sơ quy hoạch kiến trúc, đặc tả giao thức 5 trạm kiểm toán AI và "
                        "nhật ký quản trị Change Request (CR-001, CR-002). Phân tích trực tiếp "
                        "từ lịch sử Git diff."
                    ),
                    key_files=[
                        "docs/planning/PROJECT-CONTEXT.md",
                        "docs/planning/ARCHITECTURAL-BLUEPRINT.md",
                        "docs/planning/SPRINT-INDEX.md",
                    ],
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
        commit_highlights=[
            CommitHighlight(
                ref="PR#16",
                url="https://github.com/NhatCam2006/vku-sprintguard/pull/16",
                author="NhatCam2006",
                date="2026-11-23T06:30:00Z",
                title=(
                    "feat(backend): FastAPI SQLite audit store, diff filter & 40-module clusterer"
                ),
                diff_summary="+1280 / -45 dòng trên 6 tệp mã nguồn thật",
                files_changed=[
                    "backend/app/core/module_clusterer.py",
                    "backend/app/core/diff_filter.py",
                    "backend/app/core/github_client.py",
                    "backend/app/db/sqlite_store.py",
                ],
            ),
            CommitHighlight(
                ref="commit:6d27bc6",
                url="https://github.com/NhatCam2006/vku-sprintguard/commit/6d27bc6",
                author="NhatCam2006",
                date="2026-11-23T08:15:00Z",
                title="feat(frontend): Interstellar 3D force-graph, X-Ray filter & camera fly-to",
                diff_summary="+1350 / -80 dòng trên 4 tệp mã nguồn thật",
                files_changed=[
                    "frontend/src/components/Graph3DScene.tsx",
                    "frontend/src/components/SideInspector.tsx",
                    "frontend/src/components/TimelineStrip.tsx",
                ],
            ),
            CommitHighlight(
                ref="PR#25",
                url="https://github.com/NhatCam2006/vku-sprintguard/pull/25",
                author="NhatCam2006",
                date="2026-11-24T10:00:00Z",
                title="feat(mcp): stateful 6-tool FastMCP harness with HITL publish gate",
                diff_summary="+920 / -30 dòng trên 3 tệp mã nguồn thật",
                files_changed=[
                    "mcp_server/harness.py",
                    "mcp_server/server.py",
                    "backend/tests/test_mcp_harness.py",
                ],
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
                    description=(
                        "Thành viên 'Alex Nguyen (Core Maintainer)' đóng góp 60/142 commit (42%), "
                        "duy trì tầng giao vận lõi src/transport và phê duyệt phát hành."
                    ),
                ),
                GraphNode(
                    id="author:baotran-oss",
                    type="author",
                    label="Bảo Trân",
                    role="Core Contributor",
                    size=38,
                    status="healthy",
                    description=(
                        "Thành viên 'Bảo Trân' đóng góp 38/142 commit (27%), phát triển bộ "
                        "sinh lược đồ JSON Schema tự động và bộ kiểm thử tích hợp."
                    ),
                ),
                GraphNode(
                    id="author:david-dev",
                    type="author",
                    label="David Pham",
                    role="Adapter Contributor",
                    size=25,
                    status="healthy",
                    description=(
                        "Thành viên 'David Pham' đóng góp 25/142 commit (18%), xây dựng "
                        "middleware bảo mật API Token và kiểm thử xác thực đa client."
                    ),
                ),
                GraphNode(
                    id="author:mai-docs",
                    type="author",
                    label="Mai Lê",
                    role="Docs & Examples",
                    size=19,
                    status="healthy",
                    description=(
                        "Thành viên 'Mai Lê' đóng góp 19/142 commit (13%), biên soạn ứng dụng "
                        "mẫu Quickstart và hướng dẫn tích hợp FastMCP."
                    ),
                ),
                GraphNode(
                    id="mod:src/transport",
                    type="module",
                    label="src/transport",
                    size=1640,
                    churn=28,
                    status="probe",
                    description=(
                        "Tầng giao vận lõi quản lý luồng kết nối SSE và Stdio giữa FastAPI và "
                        "MCP Client, xử lý đóng kết nối an toàn (graceful shutdown). Phân tích "
                        "trực tiếp từ mã nguồn, không dựa vào README."
                    ),
                    key_files=[
                        "src/transport/sse_stream.py",
                        "src/transport/stdio_runner.py",
                        "src/transport/session_pool.py",
                    ],
                ),
                GraphNode(
                    id="mod:src/schema_gen",
                    type="module",
                    label="src/schema_gen",
                    size=1120,
                    churn=21,
                    status="healthy",
                    description=(
                        "Bộ chuyển đổi tự động từ kiểu dữ liệu Pydantic v2 sang đặc tả JSON "
                        "Schema tương thích công cụ MCP. Phân tích trực tiếp từ mã nguồn, "
                        "không dựa vào README."
                    ),
                    key_files=[
                        "src/schema_gen/pydantic_inspector.py",
                        "src/schema_gen/tool_manifest.py",
                    ],
                ),
                GraphNode(
                    id="mod:src/auth_guard",
                    type="module",
                    label="src/auth_guard",
                    size=890,
                    churn=16,
                    status="probe",
                    description=(
                        "Middleware kiểm tra Header Token, xoay vòng khóa API và chống tấn công "
                        "timing attack khi xác thực MCP request. Phân tích trực tiếp từ mã nguồn, "
                        "không dựa vào README."
                    ),
                    key_files=[
                        "src/auth_guard/token_verifier.py",
                        "src/auth_guard/key_rotation.py",
                    ],
                ),
                GraphNode(
                    id="mod:tests/integration",
                    type="module",
                    label="tests/integration",
                    size=940,
                    churn=18,
                    status="healthy",
                    description=(
                        "Bộ kiểm thử tích hợp toàn trình kiểm chứng luồng gọi công cụ MCP qua "
                        "SSE và xác thực token đa phiên. Phân tích trực tiếp từ mã nguồn, "
                        "không dựa vào README."
                    ),
                    key_files=[
                        "tests/integration/test_sse_lifecycle.py",
                        "tests/integration/test_auth_middleware.py",
                    ],
                ),
                GraphNode(
                    id="mod:examples/quickstart",
                    type="module",
                    label="examples/quickstart",
                    size=520,
                    churn=11,
                    status="healthy",
                    description=(
                        "Mã nguồn ví dụ khởi tạo nhanh máy chủ FastAPI kết nối MCP trong 30 "
                        "dòng lệnh dành cho cộng đồng. Phân tích trực tiếp từ mã nguồn, "
                        "không dựa vào README."
                    ),
                    key_files=[
                        "examples/quickstart/minimal_server.py",
                        "examples/quickstart/client_demo.py",
                    ],
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
        commit_highlights=[
            CommitHighlight(
                ref="PR#108",
                url="https://github.com/oss-vietnam/fastapi-mcp-bridge/pull/108",
                author="alex-maintainer",
                date="2026-11-15T11:20:00Z",
                title="refactor(transport): unified SSE and Stdio duplex session pool",
                diff_summary="+740 / -210 dòng trên 3 tệp mã nguồn thật",
                files_changed=[
                    "src/transport/sse_stream.py",
                    "src/transport/stdio_runner.py",
                    "src/transport/session_pool.py",
                ],
            ),
            CommitHighlight(
                ref="PR#112",
                url="https://github.com/oss-vietnam/fastapi-mcp-bridge/pull/112",
                author="david-dev",
                date="2026-11-18T15:05:00Z",
                title="feat(auth): constant-time header token rotation guard",
                diff_summary="+410 / -55 dòng trên 2 tệp mã nguồn thật",
                files_changed=[
                    "src/auth_guard/token_verifier.py",
                    "src/auth_guard/key_rotation.py",
                ],
            ),
        ],
    )

    return [student_team_audit, solo_audit, open_source_audit]
