# QUYẾT ĐỊNH DỰ ÁN & BÀN GIAO SWARM: VKU SPRINTGUARD

**Mục đích file:** Đóng gói toàn bộ thông tin hành chính, cấu hình môi trường thực tế, 6 điểm phòng ngừa kỹ thuật, bảng phân vai Swarm và 7 nhánh quyết định đã chốt sau phiên `/grill-me` ngày 23/11/2026 để **Coordinator / Swarm** ở phiên làm việc mới đọc vào là chạy ngay, không cần hỏi lại từ đầu.

> **Quy tắc ưu tiên tài liệu:** Khi có điểm tinh chỉnh sau `/grill-me`, **`PROJECT-DECISIONS.md` ưu tiên cao hơn `VKU-SprintGuard-Blueprint.md`** — cụ thể ở 3 điểm: *(1)* Màn hình mở đầu (Landing) giữ tối giản trước rồi bấm mới vào không gian 3D Mission Control; *(2)* Backend dùng SQLite + tự động nạp sẵn (seed) các bản Deep Audit đã chốt trong repo khi khởi động để không mất dữ liệu demo; *(3)* **Local-First (tạm bỏ bước deploy cloud Vercel/Render)** — ưu tiên xây dựng và kiểm thử chạy mượt 100% trên máy cục bộ (`localhost`) trước, chỉ cân nhắc deploy HTTPS ở chặng cuối nếu cần nộp Form VKU.

---

## 1. Thông tin Hành chính & Môi trường máy đã kiểm tra

### 1.1. Thông tin môn học & Repository thật
- **Học phần:** Quản trị dự án phần mềm — **Lớp học phần: `Quản trị dự án phần mềm (5)`**
- **Đơn vị:** Khoa Khoa học Máy tính — Trường ĐH CNTT & TT Việt - Hàn (VKU)
- **Giảng viên phụ trách:** TS. Nguyễn Thanh Tuấn
- **Tên dự án & Project Key:** `VKU SprintGuard` (đề xuất key: `VKU-SPM-GUARD`)
- **Sourcing Pathway:** Pathway 3 — Giải quyết bài toán vận hành thực tế tại VKU (hỗ trợ giảng viên và sinh viên kiểm toán đồ án IT)
- **GitHub Repository (đã kiểm tra truy cập bằng `git ls-remote`):** `https://github.com/NhatCam2006/vku-sprintguard` (Public, remote `origin` đã trỏ sẵn)
- **Workspace gốc bắt buộc cho Swarm:** Mở đoạn chat mới `/teamwork` **trực tiếp tại thư mục `d:\_Study\Home\Project Management\vku-sprintguard\`** (đã khởi tạo sẵn `.git` và commit đầu tiên) để `workspace: "share"` (`git worktree`) của các worker hoạt động 100% không lỗi.
- **Thông tin còn chờ PM bổ sung khi mở chat mới:**
  - `[CHỜ ĐIỀN]` Họ và tên đầy đủ của sinh viên
  - `[CHỜ ĐIỀN]` Mã số sinh viên (MSSV)

### 1.2. Hiện trạng máy cục bộ (đã kiểm tra thực tế)
- **Git global config:** `user.name = NhatCam2006` | `user.email = camdn.24ite@vku.udn.vn`
- **Git credential helper:** đang trống (cần chạy `gh auth login` 1 lần trước khi push/tạo PR từ CLI).
- **Công cụ đã cài sẵn (`FOUND`):**
  - `git`
  - `python` **3.11.9** & `uv` **0.13.7** *(đã tạo `.python-version = 3.11` để cố định môi trường chuẩn local và sẵn sàng nếu sau này deploy)*
  - `node` **v26.13.1** & `npm` **11.6.4** *(Lưu ý: Node rất mới — `frontend-3d` bắt buộc chạy `npm install` + `npm run build` kiểm chứng tương thích `react-force-graph-3d` ngay Ngày 1)*
  - `gh` **v2.105.0** *(GitHub CLI đã cài sẵn — chỉ cần PM chạy `gh auth login`)*

### 1.3. Tổ chức tài liệu trong `vku-sprintguard/` (Tách bạch Tracked vs. Ignored)
- **Track trong Git (`docs/planning/` — mọi worker ở các worktree đều đọc được):**
  - `docs/planning/PROJECT-DECISIONS.md` — Tài liệu chốt quyết định và bàn giao Swarm này.
  - `docs/planning/VKU-SprintGuard-Blueprint.md` — Kiến trúc sản phẩm, Harness 5 trạm, 6 MCP tools, JSON schema và giao diện Web 3D.
- **Giữ cục bộ, KHÔNG push lên repo public (`docs/reference/` — đã đưa vào `.gitignore`):**
  - `docs/reference/Project-Guidelines.md`
  - `docs/reference/EvidencePackageChecklist.md`
  - `docs/reference/MilestoneRubric.md`
  - `docs/reference/RiskRegisterTemplate.md`
  - *(Coordinator đọc trực tiếp các file này ở main worktree; nếu có thêm `Project-Charter-Template.md` thì thả vào `docs/reference/`, nếu không có thì dùng chuẩn 13 mục PMBOK trong `Project-Guidelines.md`.)*

---

## 2. Bảng Quyết định Chốt (7/7 nhánh `/grill-me` + 6 Điểm phòng ngừa kỹ thuật)

| Hạng mục | Quyết định đã chốt | Ghi chú thực thi cho Coordinator / Swarm |
| :--- | :--- | :--- |
| **1. Tách bạch 2 lớp** | Quy trình làm dự án tuân theo `Project-Guidelines.md`; nghiệp vụ phần mềm tuân theo `VKU-SprintGuard-Blueprint.md`. | Không gộp nhầm tiêu chuẩn chấm bài QLDA thành quy tắc chấm điểm cứng trong sản phẩm. |
| **2. Cách thức vận hành đội ngũ** | **Antigravity Native Swarm** có 1 Coordinator nắm toàn bộ bức tranh, chia việc cho các worker theo phân quyền cứng và báo cáo ngắn gọn cho PM chốt. | Mỗi tính năng/story đi qua branch riêng, Conventional Commits, Pull Request + Review độc lập, GitHub Actions CI trước khi merge vào `main`. |
| **3. Kiến trúc AI & MCP (Cách 1)** | **Antigravity Brain qua `sprintguard-mcp`** (6 tools, State Machine 5 trạm, Critic Review, Evidence Grounding, HITL bắt buộc) + **Web Dashboard** dùng chung 1 lõi Python (`core/`). | **Không** dùng LangGraph/Groq API; đẩy thẳng JSON kết quả từ MCP lên `POST /api/audits` (bảo vệ bằng `PUBLISH_API_KEY`), **không** xuất file `.json` backup trên máy. |
| **4. Triết lý đánh giá sản phẩm** | **Decision Support System** (không chấm điểm cứng 0–100). | Tự nhận diện ngữ cảnh (`solo` / `student_team` / `open_source`), gắn 3 mức tín hiệu (`healthy` / `probe` / `risk`) kèm `evidence_ref` thật và câu hỏi phỏng vấn cho Giảng viên. |
| **5. Giao diện Web 3D & Landing UX** | Phong cách **Interstellar Light Minimalism** nền trắng (`#FFFFFF`), 95% đơn sắc trắng–đen–xám, chỉ tô Vàng (`#D97706`) / Đỏ (`#DC2626`) khi có tín hiệu `probe`/`risk`; 2 font **Montserrat + Inter**. | Đồ thị **Kiểu A — Clustered 3D Network** (15–40 nodes) + Timeline 2D + Side Inspector. **Màn hình mở đầu tối giản:** ô nhập link GitHub (Live 3D Preview) + thẻ chọn nhanh các bản Deep Audit mẫu; bấm vào mới mở không gian 3D Mission Control. |
| **6. Tiến độ & GitHub Ecosystem** | **Rải đều 5–7 ngày**, merge PR/Issue thật mỗi ngày, tách rõ **Sprint 1** & **Sprint 2**. | Tuyệt đối không làm giả ngày commit quá khứ. Quản lý trên **GitHub Projects 5 cột** (`Backlog → Ready → In Progress → In Review → Done`), gắn Milestone Sprint 1/2, có Burndown chart và Release tag `v1.0.0`. |
| **7. Môi trường chạy & Lưu trữ (Local-First)** | **Tạm bỏ bước deploy cloud (Vercel/Render)**; tập trung chạy mượt 100% trên máy cục bộ (`localhost`). | Dùng **SQLite + tự động nạp sẵn (seed) các bản Deep Audit đã chốt trong repo** khi server khởi động để mở lên là có dữ liệu demo ngay. Sau khi bản local hoàn hảo mới cân nhắc deploy HTTPS (Vercel/Render) nếu cần cho Form VKU. |
| **8. Stakeholder & UAT thật** | **Pathway 3:** Có bạn bè tại VKU dùng thử bản Live trên repo thật của họ để xác nhận UAT. | Swarm chuẩn bị sẵn kịch bản test UAT và biểu mẫu/email xác nhận cho `07_Stakeholder_Acceptance_Signoff.pdf`. |
| **9. Bộ 8 file nộp Google Drive** | Swarm **xuất trọn bộ file hoàn chỉnh** (`PDF`, `.xlsx` có công thức cho Risk Register, Slide `.pptx`/`.pdf` 8–10 trang) theo đúng `Project-Guidelines.md` và các template trong `docs/reference/`. | Toàn bộ `01_Final_Technical_Report.pdf` viết ở **thì quá khứ**. Ghi nhận quyết định đổi từ LangGraph/Groq sang MCP Harness vào `06_Scope_Change_Control_Record.pdf` (CR-001). PM kiểm tra lại, ký xác nhận và đính bằng chứng UAT thật trước khi mở Drive công khai. |

### 6 Điểm phòng ngừa kỹ thuật & Chống mất điểm QLDA (Bắt buộc tuân thủ)
1. **Branch Protection cho tài khoản đơn (`NhatCam2006`):** **KHÔNG** bật *"Require 1 approving review"* trên GitHub vì GitHub cấm chủ PR tự bấm Approve PR của chính mình (sẽ tự khóa merge). Thay vào đó, bật **Require Pull Request + Require GitHub Actions CI status checks PASS**, và ghi nhận **Review Comment của `qa-docs` + self-check của PM** trực tiếp dưới mỗi PR.
2. **GitHub Projects Burndown Chart phải dựng từ Ngày 1:** Phải tạo đủ 5 cột (`Backlog → Ready → In Progress → In Review → Done`), thêm trường **`Story Points` (Number)** và **`Iteration` (`Sprint 1`, `Sprint 2`)** ngay Ngày 1 **trước khi đóng Issue đầu tiên**, và lưu ảnh/export lịch sử board qua từng đợt Sprint 1 & Sprint 2.
3. **Kiểm chứng tương thích Node v26.13.1 & Python 3.11 ngay Ngày 1:** `frontend-3d` phải chạy `npm install` + `npm run build` với `react-force-graph-3d` ngay khi dựng khung để phát hiện sớm lỗi build trên Node 26; Backend khóa `.python-version = 3.11` qua `uv`.
4. **Tích hợp & Kiểm thử MCP thực tế trong Sprint 2:** Phải ghi và thực thi bước đăng ký `mcp_server/server.py` (chạy bằng `uv run`) vào `mcp_config.json` của Antigravity, reload MCP và test gọi thật đủ **6 MCP tools** (kèm HITL dừng hỏi PM và đẩy thẳng lên Web App) trước khi quay video demo.
5. **Risk Register phải ghi rủi ro thực tế và có sự tiến hóa:** Ghi nhận các rủi ro **thực sự đã xảy ra** trong Sprint 1 và cập nhật trạng thái/rủi ro mới ở Sprint 2 (cấm chỉ viết rủi ro chung chung giả định hoặc để 2 đợt giống hệt nhau).
6. **Văn phong báo cáo tổng kết:** `01_Final_Technical_Report.pdf` bắt buộc viết 100% ở **thì quá khứ**, tổng hợp thực tế theo 7 chương chuẩn (không copy lặp nguyên si slide bài giảng).

---

## 3. Đội hình 5 Agent Swarm, Phân quyền cứng & Phân bổ Model

### Chiến lược chọn Model (Tối ưu Quota: Neon gánh việc nặng — Opus & Argon gánh việc gọn)
- **Phạm vi model được phép dùng:** Chỉ sử dụng đúng 3 dòng model: **`Gemini 4 Neon`**, **`Claude Opus 5.5`**, và **`Gemini 4 Argon`** *(tuyệt đối không dùng `Gemini 3.8 Flash` hay `Claude Sonnet 5.5`)*.
- **Nguyên tắc phân bổ:**
  - **`Gemini 4 Neon (High)`** cho toàn bộ **4 vai nặng chạy dài & nhiều lượt** (`coordinator`, `architect-mcp`, `backend-dev`, `frontend-3d`).
  - **`Claude Opus 5.5 (Medium)`** cho vai gọn, ít lượt hơn (`qa-docs` — review PR độc lập & xuất tài liệu); khi Opus hết quota thì đổi nóng sang **`Gemini 4 Argon (Medium)`** rồi mới về **`Gemini 4 Neon (Medium)`** để tận dụng sạch quota Opus/Argon cho các đầu việc gọn.
- **Cơ chế đổi model nóng khi hết quota:** Nếu bất kỳ vai nào (kể cả `coordinator`) chạm hết quota giữa chừng, dùng ngay lệnh `swarm(action="model", name="<worker>", model="<model dự phòng>")` để chuyển nóng sang model còn quota trong bộ 3 trên. Cách này **giữ nguyên toàn bộ lịch sử hội thoại và công việc đang làm dở** để worker chạy tiếp ngay *(tuyệt đối không `kill` rồi `add` lại từ đầu)*.

### Bảng Phân vai & Quyền hạn (Hard Boundaries)

| Thành viên | Model chính (Dự phòng khi hết quota) | Workspace Mode | Được phép làm (*Ownership*) | Cấm làm (*Hard Boundaries*) |
| :--- | :--- | :--- | :--- | :--- |
| **👤 `Human PM`** *(Bạn — `NhatCam2006`)* | Con người | — | Duyệt Sprint Plan, chốt các PR vào `main`, xác nhận HITL, chạy thử kiểm chứng trên máy cục bộ, phối hợp bạn bè test UAT & ký hồ sơ (chỉ deploy HTTPS sau cùng nếu cần). | Không phải tự ngồi viết code thủ công. |
| **🧭 `coordinator`** *(PM Lead / Scrum Master)* | `Gemini 4 Neon (High)` *(`Gemini 4 Argon Medium` / `Claude Opus 5.5 Medium`)* | Main repo (`vku-sprintguard/`) | Giữ bức tranh tổng thể, chia Story theo nhịp 5–7 ngày, giao task cho worker, kiểm tra chéo trước khi báo bạn, **duy nhất được merge vào `main` sau khi `qa-docs` PASS**. | Không ôm viết code tính năng thay worker; không bỏ qua cổng QA/Review. |
| **🏛️ `architect-mcp`** *(Tech Lead & MCP Harness)* | `Gemini 4 Neon (High)` *(`Claude Opus 5.5 Medium` / `Gemini 4 Argon High`)* | `share` (worktree riêng) | Thiết kế cấu trúc repo, `schemas.py`, toàn bộ `mcp_server/` (6 tools + State Machine 5 trạm + Evidence Grounding), `skills/sprintguard-auditor/SKILL.md`, `.github/workflows/ci.yml`. | Không sửa code `frontend/`; không tự merge `main`. |
| **⚙️ `backend-dev`** *(Backend Engineer)* | `Gemini 4 Neon (High)` *(`Gemini 4 Argon High` / `Claude Opus 5.5 Medium`)* | `share` (worktree riêng) | Code toàn bộ `backend/app/` (GitHub API client, diff filter, module clusterer 15–40 nodes, Timeline 2D, FastAPI endpoints, SQLite + auto-seed dữ liệu mẫu) & `backend/tests/` (`pytest`). | Không sửa `frontend/` và `mcp_server/`; không tự merge `main`. |
| **🎨 `frontend-3d`** *(Frontend 3D Engineer)* | `Gemini 4 Neon (High)` *(`Gemini 4 Argon High` / `Claude Opus 5.5 Medium`)* | `share` (worktree riêng) | Code toàn bộ `frontend/` (Landing tối giản nền trắng + Graph 3D Interstellar Kiểu A + Timeline 2D + Side Inspector + Focus/Fly-to/X-Ray + font Montserrat/Inter) & `vitest`/build. | Không sửa `backend/` và `mcp_server/`; không tự merge `main`. |
| **🔍 `qa-docs`** *(QA Reviewer & Hồ sơ QLDA — việc gọn/ít lượt)* | `Claude Opus 5.5 (Medium)` *(`Gemini 4 Argon Medium` → `Gemini 4 Neon Medium`)* | `inherit` | Review PR độc lập (PASS/FAIL kèm bằng chứng lệnh chạy thật), lưu ảnh/snapshot lịch sử board Sprint 1 & 2, soạn & xuất trọn bộ **8 file Drive** (`PDF`, `.xlsx` có công thức, Slide 8–10 trang). | **Cấm sửa code tính năng của Dev** (lỗi trả về đúng worker sửa); không tự merge `main`. |

---

## 4. Prompt khởi động mẫu (Mở cửa sổ mới tại `vku-sprintguard/` rồi dán)

Hãy mở cửa sổ Antigravity trực tiếp tại thư mục **`d:\_Study\Home\Project Management\vku-sprintguard`** (đã có `.git`), gõ `/teamwork` và dán đoạn sau:

```text
Đọc kỹ các tài liệu nền trong repo: `docs/planning/PROJECT-DECISIONS.md`, `docs/planning/VKU-SprintGuard-Blueprint.md`, và toàn bộ file tham chiếu trong `docs/reference/` (`Project-Guidelines.md`, `EvidencePackageChecklist.md`, `MilestoneRubric.md`, `RiskRegisterTemplate.md`, cùng `Project-Charter-Template.md` nếu có).

Thông tin cá nhân của tôi (Human PM):
- Họ tên: [Điền họ tên]
- MSSV: [Điền MSSV]
- Lớp: Quản trị dự án phần mềm (5)
- GitHub Repository: https://github.com/NhatCam2006/vku-sprintguard (đã khởi tạo git local & remote origin)

Hãy đóng vai `coordinator` (model Gemini 4 Neon High) điều phối Antigravity Swarm đúng theo Bảng Phân vai, 6 Điểm phòng ngừa và Model ở Phần 2–3 của `docs/planning/PROJECT-DECISIONS.md` (chỉ dùng bộ 3 Neon / Opus / Argon; nếu vai nào hết quota thì dùng `swarm(action="model")` đổi nóng sang model dự phòng trong bộ 3, không kill worker):
1. Kiểm tra lại hiện trạng repo, GitHub auth (`gh auth status`) và tóm tắt thật ngắn gọn lộ trình 5–7 ngày (tách Sprint 1 & Sprint 2, rải commit/PR thật từng ngày) cho tôi duyệt.
2. Spawn các worker đúng model đã chốt (`architect-mcp`, `backend-dev`, `frontend-3d` đều dùng `gemini-4-neon-high` với `workspace: "share"`; `qa-docs` dùng `claude-opus-5-5-medium` và chuyển nóng sang `gemini-4-argon-medium` khi hết quota với `workspace: "inherit"`) để lập bộ hồ sơ khởi tạo (`Project Charter`, `WBS`, `Risk Register` đợt 1), thiết lập GitHub Projects 5 cột + Story Points + Iteration + CI, và kiểm chứng build trên Node 26 / Python 3.11 rồi triển khai từng bước Sprint 1 (**ưu tiên chạy mượt 100% trên máy cục bộ `localhost`, tạm bỏ qua bước deploy cloud cho tới khi tôi yêu cầu ở chặng cuối**).

Luôn tóm tắt ngắn gọn, dễ hiểu ở mỗi cổng kiểm soát để tôi (PM) duyệt trước khi merge vào `main`.
```
