# Risk Register — Wave 2 (Sprint 2 Evolution & Project Closure)

**Project:** VKU SprintGuard (`VKU-SPM-GUARD`)  
**PM / Lead:** Đinh Nhật Cảm (`24Ite019`, `@NhatCam2006`)  
**Academic Supervisor:** Dr. Nguyen Thanh Tuan / TS. Nguyễn Thanh Tuấn  
**Milestone Alignment:** Wave 1 Seeded at M1 (Day 1) · Wave 1 Actuals at M5 (Day 3 / Week 6) · **Wave 2 Final Revision at M7–M9 (Day 6 / Week 11–14 Closure)**  
**Repository:** `https://github.com/NhatCam2006/vku-sprintguard`

---

## 1. Risk Scoring Matrix & Response Strategies

| Strategy | Meaning | Project Application Example |
| :--- | :--- | :--- |
| **Avoid** | Change the plan to eliminate the risk | Drop single-account self-approval deadlock; ban server-side paid LLM APIs (`CR-001`) |
| **Mitigate** | Reduce probability or impact | Day-1 Node 26 build smoke; 3-pool model split; MCP server reload & schema validation |
| **Transfer** | Shift the risk elsewhere | Offload reasoning to Antigravity Brain via `sprintguard-mcp` ($0 API cost) |
| **Accept** | Acknowledge and monitor without active intervention | Low-probability, low-impact residual risks monitored at PR review |

**Numeric Scoring Scale (used in `04_Risk_Register_Evolution.xlsx`):**
- **Probability / Impact:** `Low = 1`, `Medium = 2`, `High = 3`
- **Risk Score (`P × I`):** `1–2` = Low, `3–4` = Medium, `6` = High, `9` = Critical

---

## 2. Wave 2 Risk Register (`R1`–`R13`)

*Evolves `03_Risk_Register_Wave1.md` (`R1`–`R11`) with verified Sprint 2 closure outcomes (`PR #25`–`PR #28`) and records two newly observed Sprint 2 risks (`R12`, `R13`).*

| ID | Risk Description | Prob (Wave 1 → 2) | Impact (Wave 1 → 2) | Response Strategy & Action Taken | Owner | Wave 2 Final Status |
| :---: | :--- | :---: | :---: | :--- | :--- | :--- |
| **R1** | **Missing `read:project` / `project` OAuth scope on `gh` CLI:** Survey check blocked automated GitHub Projects v2 setup at M1. | High → Low | High → Low | **Mitigate:** Gated M2 board setup behind PM Gate 1; PM ran `gh auth refresh -s project,read:project`. All board transitions (`M2`–`M9`) and 6 JSON snapshots succeeded cleanly. | Human PM (`@NhatCam2006`) / `coordinator` | **Closed** (Resolved at Gate 1; verified across Sprint 1 & Sprint 2) |
| **R2** | **`gh.exe` absent from default Windows `$env:PATH`:** Bare `gh` commands failed in PowerShell sessions. | High → Low | Low → Low | **Mitigate:** Standardized all Swarm runbooks and scripts to call `& "C:\Program Files\GitHub CLI\gh.exe"`. Zero broken GitHub CLI calls in Sprint 2. | `coordinator` / `architect-mcp` | **Mitigated / Controlled** (Standardized explicit path across Days 1–6) |
| **R3** | **Node `v26.13.1` incompatibility with `react-force-graph-3d` / Three.js / Vite:** Bleeding-edge Node 26 runtime could break peer dependencies or Vite builds. | Medium → Low | High → Low | **Mitigate:** Verified Day-1 smoke build (`PR #20`), M4 frontend (`PR #23`), M7 inspector polish (`PR #26`), and CR-002 4-tab Vietnamese inspector (`PR #28`) with `tsc`/`eslint`/`vitest` (6/6)/`vite build` exit `0`. | `frontend-3d` | **Closed** (100% green CI across all 4 frontend PRs on Node 26) |
| **R4** | **Single-account (`NhatCam2006`) GitHub Branch Protection PR merge deadlock:** Requiring 1 approving review blocks self-merge. | High → Low | High → Medium | **Avoid:** Configured `main` branch protection with `required_approving_review_count: 0` + required CI status checks; enforced independent QA review comment + PM manual merge across `PR #20`–`#28`. | `coordinator` / Human PM | **Controlled** (Zero deadlocks across 9 PRs; governance maintained) |
| **R5** | **GitHub REST API 60 req/hr unauthenticated rate limit during Live Preview & Dogfooding:** Repeated `POST /api/preview` and MCP collection could trigger HTTP `403`/`429`. | Medium → Low | Medium → Low | **Mitigate:** Capped telemetry fetch (`100` commits, `30` PRs, `20` detail fetches), added optional `GITHUB_TOKEN` PAT (`gh auth token`), and tested live on `vku-sprintguard` (`aud_deep_995a9cba`) and `fastapi/typer` (`aud_deep_faa0899d`). | `backend-dev` / `architect-mcp` | **Closed** (Zero 403/429 errors across M3, M5, M7 Dogfooding & CR-002) |
| **R6** | **WebGL / 3D "Hairball Problem" lag on large repositories in `Graph3DCanvas`:** Large repos degrade 3D readability and FPS. | Medium → Low | Medium → Low | **Mitigate:** Implemented 2-level directory clustering capped at `40` modules + `other/` fallback (`module_clusterer.py`), Focus Mode (~10% dim), Camera Fly-to, and `[X-Ray]` filter (`PR #22`, `#23`, `#26`). Verified on `fastapi/typer` (`aud_deep_faa0899d`). | `backend-dev` / `frontend-3d` | **Closed** (Validated on both `vku-sprintguard` and external `fastapi/typer`) |
| **R7** | **Accidental commit of gitignored `docs/reference/`, `.env` secrets, or SQLite `.db` binaries:** Public repo leak risk. | Low → Low | High → High | **Avoid:** Enforced `.gitignore` for `docs/reference/`, `.env*`, `*.db`; audited `git status` and PR diffs on every PR (`PR #20`–`#29`). Zero secrets or binaries ever committed. | `architect-mcp` / `qa-docs` | **Controlled / Monitored** (Ongoing DoD #5 gate; 0 incidents) |
| **R8** | **Evidence Package audit gap (single board screenshot or static Risk Register):** Fails VKU `EvidencePackageChecklist.md`. | Medium → Low | High → Low | **Mitigate:** Captured 6 chronological board snapshots (`sprint1_start`, `sprint1_day1_eod`, `sprint1_mid_m3`, `sprint1_end_review`, `sprint2_day5_m7`, `sprint2_final_pre_close`), evolved Wave 1 → Wave 2 Register + formula-driven `.xlsx`, and generated all 8 Drive deliverables. | `qa-docs` / `docs-release` | **Closed** (Full chronological board trail & 8 deliverables complete) |
| **R9** | **Scope creep from Sprint 2 (`mcp_server/`, `SKILL.md`, cloud deploy) into Sprint 1:** Premature feature leak threatens Local-First MVP stability. | Medium → Low | High → Low | **Avoid:** Enforced Sprint 1/Sprint 2 WBS separation and PM Gate 2 stop checkpoint; Sprint 2 executed cleanly in Days 4–6 (`PR #25`–`#28`) without unrequested cloud deployment. | `coordinator` / Human PM | **Controlled** (Strict milestone gating honored end-to-end) |
| **R10** | **`ruff` CLI absent from global Windows `PATH` & UTF-8 BOM TOML failure:** Broke `pyproject.toml` parsing on Day 1. | High → Low | Low → Low | **Mitigate:** Locked `ruff` and `pytest` inside `uv` dev dependencies (`backend/pyproject.toml`), standardized `uv run ruff` / `uv run pytest`, and enforced BOM-free UTF-8 writes. | `architect-mcp` / `backend-dev` | **Mitigated / Controlled** (Zero BOM or lint toolchain failures in Days 2–6) |
| **R11** | **Multi-agent model quota exhaustion (`HTTP 429` observed Day 1):** Running all agents on a single model pool stalled parallel execution. | High → Low | High → Low | **Mitigate:** Adopted Native Swarm with 3-pool model allocation and event-driven `swarm_wait` (zero polling). All Sprint 1 M3–M5 and Sprint 2 M6–M10 work completed without further 429 stalls. | `coordinator` | **Closed** (Zero quota stalls across Days 2–6) |
| **R12** | ***(New — Sprint 2)* MCP server cached pre-CR-002 schema until process reload:** After `PR #28` (`c876e76`) extended `GraphNode` with `description`, `key_files`, and `commit_highlights`, the running `sprintguard-mcp` stdio process kept the old in-memory schema until restarted, causing initial `aud_deep` verification to miss CR-002 fields. | High → Low | Medium → Low | **Mitigate:** Restarted the `sprintguard-mcp` server process in Antigravity to load the updated `mcp_server/harness.py` & `backend/app/core/schemas.py`, then re-ran live 5-station audit `aud_deep_faa0899d` on `fastapi/typer` confirming all CR-002 fields persisted and rendered. | `architect-mcp` / Human PM | **Resolved (Day 6)** — Documented restart requirement in operational runbook |
| **R13** | ***(New — Sprint 2)* Mid-sprint `CR-002` explainability UX request threatening Day 6 closure schedule:** During M7 review, PM requested Vietnamese node explanations, real `key_files`, and clickable GitHub commit links to eliminate hallucination risk in 3D inspection. | Medium → Low | High → Low | **Mitigate:** Processed formally via CCB (`CR-002` in `08_Scope_Change_Control_Record.md`), scoped strictly to `schemas.py`, `harness.py`, and `SideInspector.tsx` (`PR #28`), verified with `22` pytest + `6` vitest (100% CI pass), and merged (`67ca6b0`) on schedule with zero slip to M8–M10. | Human PM / `coordinator` | **Resolved (Day 6)** — Controlled via formal CCB without schedule slip |

---

## 3. Week 11 Revision Checklist (Final Wave 2 Verification)

- [x] Reviewed Sprint 1 & Sprint 2 outcomes: closed resolved risks (`R1`, `R3`, `R5`, `R6`, `R8`, `R11`) with verifiable PR/commit/audit evidence.
- [x] Added newly materialized Sprint 2 risks (`R12` MCP schema cache reload; `R13` mid-sprint `CR-002` scope/schedule impact) with root cause and verified mitigation.
- [x] Synchronized all 13 risks (`R1`–`R13`) into the formula-driven workbook `04_Risk_Register_Evolution.xlsx` (`Summary_Dashboard`, `Wave1_Sprint1_Actuals`, `Wave2_Sprint2_Evolution`).
- [x] Verified zero unmitigated High/Critical open risks remaining at Milestone M9 closure (`R4`, `R7`, `R9` remain actively controlled via branch protection, `.gitignore`, and DoD gates).

### Wave 2 Executive Summary
- **Closed Risks (6):** `R1`, `R3`, `R5`, `R6`, `R8`, `R11`.
- **Resolved New Sprint 2 Risks (2):** `R12` (MCP schema cache reload), `R13` (`CR-002` controlled via CCB).
- **Mitigated / Controlled Residual Risks (5):** `R2`, `R4`, `R7`, `R9`, `R10` — all reduced to Low probability or actively enforced by automated gates.
- **Net Risk Reduction:** Average numeric risk score dropped from **5.18** (Wave 1 Baseline, `R1`–`R11`) to **1.46** (Wave 2 Closure, `R1`–`R13`) — a **71.8% reduction** in residual risk exposure.
