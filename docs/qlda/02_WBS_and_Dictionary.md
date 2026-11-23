# Work Breakdown Structure (WBS) & WBS Dictionary

**Project:** VKU SprintGuard (`VKU-SPM-GUARD`)  
**PM / Lead:** Đinh Nhật Cảm (`24Ite019`, `@NhatCam2006`)  
**Course:** Software Project Management (`Quản trị dự án phần mềm (5)`) · **Instructor:** Dr. Nguyen Thanh Tuan / TS. Nguyễn Thanh Tuấn  
**Milestone Alignment:** M1/M2 (Weeks 2–4 — Initiation & Baseline Planning)  
**Repository:** `https://github.com/NhatCam2006/vku-sprintguard`

---

## 1. Scope Baseline & 100% Rule Verification

Per `Project-Guidelines.md` and `MilestoneRubric.md`, this WBS follows the **Deliverable-Oriented 100% Rule**:
- Every leaf work package (`1.x.y`) represents a concrete, verifiable **deliverable** (not a generic ongoing activity), sized at 1–2 weeks in semester-equivalent effort and decomposed 1:1 into **GitHub Issues** (`<= 2 days` accelerated execution effort each).
- **100% In-Scope Coverage:** Branches `1.1` through `1.6` (19 leaf work packages, `61` total Story Points) cover **100%** of the committed capabilities and governance deliverables in **Project Charter §5.1**:
  - `1.1` → Charter §5.1 Engineering & Governance Deliverables (QLDA docs, CI, GitHub Ecosystem, Evidence Package)
  - `1.2` → Charter §5.1 Core Module 1 (`backend/` Telemetry, Persistence & Preview Engine)
  - `1.3` → Charter §5.1 Core Module 2 (`frontend/` Interstellar Light Minimalism 3D Web Dashboard — Sprint 1)
  - `1.4` → Charter §4 Objective 1–2 & §12.1 Sprint 1 Localhost Integration & E2E Acceptance
  - `1.5` → Charter §5.1 Core Module 3 (`mcp_server/`, `skills/` — **Sprint 2 Deferred**)
  - `1.6` → Charter §5.1 Core Module 2 Polish & Core Module 3 UAT/Dogfooding (**Sprint 2 Deferred**)
- **0% Out-of-Scope Leakage:** None of the **Charter §5.2** exclusions appear in this WBS (no 0–100 automated grading, no server-side `LangGraph`/paid Groq/OpenAI APIs, no premature cloud deployment during Sprint 1 Local-First execution, no VKU SSO/LDAP or non-GitHub tracking tools).

### Scope Separation: Sprint 1 (Active) vs. Sprint 2 (Deferred)
| Scope Partition | WBS Branches | Issues | Story Points | Execution Status |
| :--- | :--- | :---: | :---: | :--- |
| **Sprint 1 — Initiation & Local-First MVP** (`Days 1–3`) | `1.1.1`–`1.1.4`, `1.2.1`–`1.2.5`, `1.3.1`–`1.3.4`, `1.4.1` | `#1`–`#14` (14 issues) | `40` | **ACTIVE** (Stops at PM Gate 2 after M5 Localhost E2E) |
| **Sprint 2 — MCP Harness, Dogfooding & Final Evidence** (`Days 4–6`) | `1.1.5`, `1.5.1`–`1.5.2`, `1.6.1`–`1.6.2` | `#15`–`#19` (5 issues) | `21` | **DEFERRED** (Out of scope for current run) |

---

## 2. Deliverable-Oriented WBS Tree (`1.0 VKU SprintGuard`)

```text
1.0 VKU SprintGuard (Pathway 3 — Decision Support System & 3D Repo Auditor)
├── 1.1 Project Governance, QLDA Baseline & GitHub Ecosystem
│   ├── 1.1.1 Initiation QLDA Package & Environment Template [Sprint 1 — Day 1 / M1] -> Issue #1
│   ├── 1.1.2 GitHub Actions CI Workflow & Day-1 Python 3.11 / Node 26 Build Smoke [Sprint 1 — Day 1 / M1] -> Issue #2
│   ├── 1.1.3 GitHub Milestones, 1:1 WBS Issues, Branch Protection & 5-Col Projects v2 Board [Sprint 1 — Day 1-2 / M1-M2] -> Issue #3
│   ├── 1.1.4 Sprint 1 Board Snapshots (Start/Mid/End) & Risk Register Wave 1 Actuals [Sprint 1 — Day 3 / M5] -> Issue #14
│   └── 1.1.5 Final VKU Evidence Package (8 Drive Files), CR-001, Wave 2 Risks & Release v1.0.0 [Sprint 2 DEFERRED — Day 6] -> Issue #19
├── 1.2 Backend Core & Telemetry Engine (backend/)
│   ├── 1.2.1 FastAPI App Skeleton, Pydantic v2 Schemas, CORS & /health Endpoint [Sprint 1 — Day 2 / M3] -> Issue #4
│   ├── 1.2.2 SQLite Persistence Store & Idempotent Startup Auto-Seed (3 Sample Audits) [Sprint 1 — Day 2 / M3] -> Issue #5
│   ├── 1.2.3 Audit Read & API-Key-Protected Publish Endpoints (/api/audits) [Sprint 1 — Day 2 / M3] -> Issue #6
│   ├── 1.2.4 GitHub REST Client, Diff Filter, 2-Level Module Clusterer, Timeline 2D & POST /api/preview [Sprint 1 — Day 2 / M3] -> Issue #7
│   └── 1.2.5 Backend Automated QA Suite (pytest Unit/API Tests & ruff Lint/Format) [Sprint 1 — Day 2 / M3] -> Issue #8
├── 1.3 Interstellar 3D Web Dashboard (frontend/)
│   ├── 1.3.1 Interstellar Light Minimalism Theme, API Client & Minimalist Landing Screen [Sprint 1 — Day 3 / M4] -> Issue #9
│   ├── 1.3.2 Clustered 3D Network Canvas (Graph3DCanvas.tsx) w/ Focus Mode & Reset Camera [Sprint 1 — Day 3 / M4] -> Issue #10
│   ├── 1.3.3 Timeline 2D Bar Chart, Top Bar (/health + URL Input) & Read-Only Side Inspector [Sprint 1 — Day 3 / M4] -> Issue #11
│   └── 1.3.4 Frontend Automated QA Suite (tsc, eslint, vitest & Vite Production Build) [Sprint 1 — Day 3 / M4] -> Issue #12
├── 1.4 Localhost Integration & Sprint 1 E2E Acceptance
│   └── 1.4.1 Simultaneous Localhost Dual-Server E2E (Tiers 1–5) & Live Preview on vku-sprintguard [Sprint 1 — Day 3 / M5] -> Issue #13
├── 1.5 MCP State-Machine Harness & Antigravity Skill (mcp_server/, skills/) [SPRINT 2 DEFERRED]
│   ├── 1.5.1 sprintguard-mcp FastMCP Server (6 Tools, 5-Station State Machine, Evidence Grounding, HITL) [Sprint 2 DEFERRED — Day 4] -> Issue #15
│   └── 1.5.2 Antigravity Auditor Skill (SKILL.md), mcp_config.json Registration & 6-Tool Live Test [Sprint 2 DEFERRED — Day 4] -> Issue #16
└── 1.6 Deep AI Inspector Polish, Dogfooding & Peer UAT [SPRINT 2 DEFERRED]
    ├── 1.6.1 Deep AI Side Inspector Enhancements (Camera Fly-to, X-Ray Filter, Critic/HITL Notes) [Sprint 2 DEFERRED — Day 5] -> Issue #17
    └── 1.6.2 Dogfooding Audit on vku-sprintguard, VKU Peer UAT & Optional Final HTTPS Deploy [Sprint 2 DEFERRED — Day 5-6] -> Issue #18
```

---

## 3. WBS Dictionary & 1:1 GitHub Issue Mapping

Every leaf work package maps **1:1** to an open GitHub Issue under Milestone `#1` (`Sprint 1: Initiation & Local-First MVP`) or Milestone `#2` (`Sprint 2: MCP Harness, Dogfooding & Final Evidence (Deferred)`).

| WBS ID | Work Package / Deliverable Name | Scope & Deliverable Description | Acceptance Criteria (DoD Summary) | Sprint & Milestone | Accelerated Effort | Story Points | Owner Role | GitHub Issue |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :--- | :---: |
| `1.1.1` | Initiation QLDA Package & Environment Template | `docs/qlda/01_Project_Charter.md` (13 sections), `02_WBS_and_Dictionary.md`, `03_Risk_Register_Wave1.md`, `.env.example` | Charter matches all 13 template sections with PM Đinh Nhật Cảm (`24Ite019`); WBS passes 100% Rule; Risk Register uses 6-col schema; `.env.example` committed while `docs/reference/` stays gitignored. | Sprint 1 (`M1`) | 0.5 day | `3` | `qa-docs` / `coordinator` | [`#1`](https://github.com/NhatCam2006/vku-sprintguard/issues/1) |
| `1.1.2` | GitHub Actions CI & Day-1 Toolchain Verification | `.github/workflows/ci.yml` + minimal `backend/` (`uv` Python 3.11) & `frontend/` (Node 26 `react-force-graph-3d`) smoke scaffolds | `ci.yml` runs `backend` (`ruff` + `pytest`) & `frontend` (`tsc` + `eslint` + `vitest` + `npm run build`) on PRs; both pass locally & in CI with exit `0`. | Sprint 1 (`M1`) | 0.5 day | `3` | `architect-mcp` + `frontend-3d` | [`#2`](https://github.com/NhatCam2006/vku-sprintguard/issues/2) |
| `1.1.3` | GitHub Milestones, Issues, Branch Protection & Projects v2 Board | Milestones `#1`–`#2`, 19 WBS Issues, Classic Branch Protection on `main`, and 5-column Projects v2 board (`Story Points`, `Iteration`) | Milestones & 19 Issues created; branch protection enforces PR + CI without 1-approving-review deadlock; after PM Gate 1 `read:project` refresh, 5-col board created & linked before closing Issue `#1`. | Sprint 1 (`M1`–`M2`) | 0.5 day | `2` | `coordinator` + `Human PM` | [`#3`](https://github.com/NhatCam2006/vku-sprintguard/issues/3) |
| `1.2.1` | FastAPI Skeleton, Pydantic v2 Schemas, CORS & `/health` | `backend/app/core/schemas.py` (`Blueprint §4.3` models), CORS middleware (`localhost:5173`), `GET /health` | Full Audit/Graph3D/Timeline2D/Signal/PreviewRequest schemas validated; `GET /health` returns HTTP `200` with `status`, `database`, `seeded_audits`. | Sprint 1 (`M3`) | 0.5 day | `3` | `architect-mcp` / `backend-dev` | [`#4`](https://github.com/NhatCam2006/vku-sprintguard/issues/4) |
| `1.2.2` | SQLite Store & Startup Idempotent Auto-Seed | `backend/app/db/sqlite_store.py` & `backend/app/seed/sample_audits.py` (3 sample Deep Audits) | SQLite initializes at `SPRINTGUARD_DB_PATH` (`data/sprintguard.db`, gitignored); startup seeds 3 profiles (`solo`, `student_team`, `open_source`) idempotently. | Sprint 1 (`M3`) | 0.5 day | `3` | `backend-dev` | [`#5`](https://github.com/NhatCam2006/vku-sprintguard/issues/5) |
| `1.2.3` | Audit Read & Protected Publish Endpoints (`/api/audits`) | `GET /api/audits`, `GET /api/audits/{audit_id}`, `POST /api/audits` (`X-API-Key` validation) | List returns summaries (`node_count`, `signal_count`); detail returns full Audit or `404`; publish validates `X-API-Key` (`401`/`403` invalid, `422` bad schema, `201` stored). | Sprint 1 (`M3`) | 0.5 day | `2` | `backend-dev` | [`#6`](https://github.com/NhatCam2006/vku-sprintguard/issues/6) |
| `1.2.4` | GitHub Client, Diff Filter, Module Clusterer, Timeline 2D & `/api/preview` | `github_client.py` (`httpx`, 100 commits + 30 PRs), `diff_filter.py`, `module_clusterer.py` (2-level, <=40 modules + `other`), `POST /api/preview` | Strips lockfiles/minified/build artifacts; clusters deterministically; computes `risk`/`probe`/`healthy` & weekly `anomaly`; analyzes `NhatCam2006/vku-sprintguard` cleanly. | Sprint 1 (`M3`) | 1.0 day | `5` | `backend-dev` | [`#7`](https://github.com/NhatCam2006/vku-sprintguard/issues/7) |
| `1.2.5` | Backend Automated QA Suite (`pytest` + `ruff`) | Comprehensive unit & API tests in `backend/tests/` + `ruff` lint/format compliance | Covers schemas, SQLite idempotency, `/health`, `/api/audits`, `diff_filter`, `module_clusterer`, and mocked/live `/api/preview`; `uv run pytest` & `uv run ruff check .` exit `0`. | Sprint 1 (`M3`) | 0.5 day | `3` | `backend-dev` | [`#8`](https://github.com/NhatCam2006/vku-sprintguard/issues/8) |
| `1.3.1` | Interstellar Theme, API Client & Minimalist Landing Screen | Tailwind/CSS light tokens (`#FFFFFF`/`#09090B`), `api/client.ts`, `types/audit.ts`, `LandingScreen.tsx` | Displays GitHub URL Live Preview form + pre-seeded Deep Audit cards; handles loading/error states cleanly; enters Mission Control on selection. | Sprint 1 (`M4`) | 0.5 day | `3` | `frontend-3d` | [`#9`](https://github.com/NhatCam2006/vku-sprintguard/issues/9) |
| `1.3.2` | Clustered 3D Network Canvas (`Graph3DCanvas.tsx`) | White orbital `react-force-graph-3d` Type A canvas, author polyhedra, status-colored module spheres, Focus Mode, `[Reset Camera]` | Authors `#09090B`; modules white/black, `#D97706` amber, `#DC2626` red; edges `#D4D4D8`; Focus Mode dims unrelated nodes/edges to ~10%; `[Reset Camera]` works. | Sprint 1 (`M4`) | 1.0 day | `5` | `frontend-3d` | [`#10`](https://github.com/NhatCam2006/vku-sprintguard/issues/10) |
| `1.3.3` | Timeline 2D, TopBar & Read-Only Side Inspector | `Timeline2D.tsx`, `TopBar.tsx` (`/health` badge + URL input), read-only `SideInspector.tsx` (`[Overview] [Node] [Q&A]`) | Timeline highlights `anomaly: true` weeks in `#DC2626`; TopBar shows live `/health`; SideInspector renders context, signals, and questions without HITL mutation buttons. | Sprint 1 (`M4`) | 0.5 day | `3` | `frontend-3d` | [`#11`](https://github.com/NhatCam2006/vku-sprintguard/issues/11) |
| `1.3.4` | Frontend Automated QA Suite (`tsc`, `eslint`, `vitest`, `build`) | Component & client unit tests in `frontend/src/__tests__/` with safe WebGL mocking in jsdom | `npx tsc --noEmit`, `npm run lint`, `npm run test`, and `npm run build` all pass with exit `0` locally and in CI. | Sprint 1 (`M4`) | 0.5 day | `2` | `frontend-3d` | [`#12`](https://github.com/NhatCam2006/vku-sprintguard/issues/12) |
| `1.4.1` | Simultaneous Localhost E2E Acceptance (Tiers 1–5) | Dual-server `localhost:8000` + `localhost:5173` E2E verification & Live 3D Preview on `NhatCam2006/vku-sprintguard` | `/health` 200, SQLite auto-seed verified, Live 3D Preview renders valid nodes/edges/timeline with zero runtime/console errors; Tiers 1–5 pass; zero cloud deploy configs. | Sprint 1 (`M5`) | 0.5 day | `3` | `qa-docs` + E2E | [`#13`](https://github.com/NhatCam2006/vku-sprintguard/issues/13) |
| `1.1.4` | Sprint 1 Board Snapshots & Risk Register Wave 1 Actuals | `docs/qlda/board_snapshots/` (Start, Mid, End) + updated `03_Risk_Register_Wave1.md` with real Sprint 1 outcomes | Three verifiable board snapshots saved; Week 6 checklist in `03_Risk_Register_Wave1.md` completed with actual Sprint 1 materialized risks; PM Gate 2 summary delivered. | Sprint 1 (`M5`) | 0.5 day | `2` | `qa-docs` + `coordinator` | [`#14`](https://github.com/NhatCam2006/vku-sprintguard/issues/14) |
| `1.5.1` | `sprintguard-mcp` FastMCP Server (6 Tools & 5-Station Harness) | `mcp_server/server.py` & `harness.py` implementing 5-station state machine, `valid_refs` Evidence Grounding & HITL `[Deferred]` | Exposes all 6 MCP tools, enforces station transitions & `valid_refs`, pauses at `AWAITING_HUMAN_APPROVAL`, publishes via `PUBLISH_API_KEY`. | Sprint 2 (`M6`, Deferred) | 1.0 day | `5` | `architect-mcp` | [`#15`](https://github.com/NhatCam2006/vku-sprintguard/issues/15) |
| `1.5.2` | Antigravity Skill (`SKILL.md`), `mcp_config.json` & 6-Tool Live Test | `skills/sprintguard-auditor/SKILL.md` + `mcp_config.json` (`uv run`) registration & live tool verification `[Deferred]` | Skill guides Antigravity across 5 stations + HITL; all 6 tools verified end-to-end against local backend. | Sprint 2 (`M6`, Deferred) | 0.5 day | `3` | `architect-mcp` | [`#16`](https://github.com/NhatCam2006/vku-sprintguard/issues/16) |
| `1.6.1` | Deep AI Side Inspector Polish (Fly-to, X-Ray, Critic/HITL) | Camera Fly-to on signal click, `[X-Ray]` filter toggle, `critic_note` & PM `human_notes` display `[Deferred]` | Clicking signal smoothly flies camera to node; `[X-Ray]` dims healthy nodes; displays Critic & HITL audit notes. | Sprint 2 (`M7`, Deferred) | 0.5 day | `3` | `frontend-3d` | [`#17`](https://github.com/NhatCam2006/vku-sprintguard/issues/17) |
| `1.6.2` | Dogfooding Audit, VKU Peer UAT & Optional Final HTTPS Deploy | Live Deep Audit of `NhatCam2006/vku-sprintguard`, VKU peer UAT sign-off, optional HTTPS deploy if PM requests `[Deferred]` | Dogfooding audit published; VKU peer teams test & sign `07_Stakeholder_Acceptance_Signoff.pdf`; HTTPS deploy executed only on PM request. | Sprint 2 (`M7`–`M8`, Deferred) | 1.0 day | `5` | `Human PM` + `coordinator` | [`#18`](https://github.com/NhatCam2006/vku-sprintguard/issues/18) |
| `1.1.5` | Final 8 Google Drive Deliverables, `CR-001`, Wave 2 Risks & `v1.0.0` | Complete 8-file Drive Evidence Package (`01`–`08`), past-tense 7-chapter report, Excel formulas, Retros, Slides & tag `v1.0.0` `[Deferred]` | All 8 Drive files pass `EvidencePackageChecklist.md` & `MilestoneRubric.md`; release tag `v1.0.0` published on GitHub. | Sprint 2 (`M8`–`M10`, Deferred) | 1.0 day | `5` | `qa-docs` + `Human PM` | [`#19`](https://github.com/NhatCam2006/vku-sprintguard/issues/19) |

---

## 4. Six-Day Execution Roadmap (Sprint 1 Active vs. Sprint 2 Deferred)

| Day | Sprint & Status | Project Milestones | Planned Deliverables & Gate Actions | PR Cadence |
| :---: | :--- | :--- | :--- | :--- |
| **Day 1** | **Sprint 1 (Active — Local-First)** | `M1` (Initiation, CI & Toolchain) & `M2` (Board Setup after Gate 1) | Survey repo & `gh auth status`; author `01_Project_Charter.md`, `02_WBS_and_Dictionary.md`, `03_Risk_Register_Wave1.md`, `.env.example`; create `.github/workflows/ci.yml`; run Python 3.11 (`uv`) + Node `v26.13.1` (`react-force-graph-3d`) build smoke; create Milestones & 19 WBS Issues; configure `main` Branch Protection (PR + CI only) -> **PM Gate 1** (PM runs `gh auth refresh -s project,read:project` & merges PR #1) -> create 5-column Projects v2 Board (`Story Points`, `Iteration`) & save Sprint 1 Start snapshot. | **PR #1** (held open for PM Gate 1 merge) |
| **Day 2** | **Sprint 1 (Active — Local-First)** | `M3` (Sprint 1 Backend Core) | Implement `backend/` (`schemas.py`, `sqlite_store.py` + 3 pre-seeded sample Deep Audits, `main.py` w/ CORS & `/health`, `/api/audits`, `github_client.py`, `diff_filter.py`, `module_clusterer.py`, `POST /api/preview`, `pytest` + `ruff`); capture Mid-Sprint board snapshot. | **PR #2** (kept open for PM review/merge) |
| **Day 3** | **Sprint 1 (Active — Local-First)** | `M4` (Frontend 3D) & `M5` (Localhost E2E & Sprint 1 Closure) | Implement `frontend/` (Interstellar white theme, Minimalist Landing Screen, `Graph3DCanvas.tsx` Type A + Focus Mode + Reset Camera, `Timeline2D.tsx`, TopBar w/ `/health`, read-only `SideInspector.tsx`, `tsc`/`eslint`/`vitest`/build); run simultaneous `localhost:8000` + `:5173` E2E Tiers 1–5 including Live 3D Preview of `NhatCam2006/vku-sprintguard`; capture End-Sprint board snapshot & update `03_Risk_Register_Wave1.md` with Sprint 1 actuals -> **PM Gate 2 (STOP BEFORE SPRINT 2)**. | **PR #3** (Frontend) & **PR #4** (E2E + Sprint 1 Closure, kept open for PM merge) |
| **Day 4** | **Sprint 2 (DEFERRED — Out of Scope for Current Run)** | `M6` (MCP Harness) | Build `mcp_server/server.py` & `harness.py` (6 tools, 5-station State Machine, `valid_refs` Evidence Grounding, HITL), `skills/sprintguard-auditor/SKILL.md`, register in Antigravity `mcp_config.json` (`uv run`), test all 6 tools live. | Deferred PRs |
| **Day 5** | **Sprint 2 (DEFERRED — Out of Scope for Current Run)** | `M7` (Inspector & Dogfooding) | Add Camera Fly-to, X-Ray filter, and full Critic/HITL inspector polish; run Dogfooding Deep AI Audit on `NhatCam2006/vku-sprintguard`; start VKU Peer UAT. | Deferred PRs |
| **Day 6** | **Sprint 2 (DEFERRED — Out of Scope for Current Run)** | `M8`–`M10` (Closure & Evidence) | Collect VKU Peer UAT sign-off, record `CR-001` & Risk Register Wave 2, compile Sprint 1 & Final Retrospectives, export all 8 Google Drive deliverables (past-tense report), tag `v1.0.0`, optional HTTPS deploy if PM requests. | Deferred PRs |
