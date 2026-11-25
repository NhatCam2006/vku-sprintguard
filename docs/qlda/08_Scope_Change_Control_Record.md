# Scope Change Control Record (CCB Log & Change Requests)

**Project:** VKU SprintGuard (`VKU-SPM-GUARD`)  
**PM / CCB Chair:** Đinh Nhật Cảm (`24Ite019`, `@NhatCam2006`)  
**Academic Supervisor:** Dr. Nguyen Thanh Tuan / TS. Nguyễn Thanh Tuấn  
**Governance Authority:** Change Control Board (CCB) — Human PM (`@NhatCam2006`) + `coordinator` + `architect-mcp`  
**Repository:** `https://github.com/NhatCam2006/vku-sprintguard`

---

## 1. Change Control Process & Governance Policy

Per VKU Software Project Management standards and Project Charter §5 & §12, any modification to the approved Scope Baseline (`02_WBS_and_Dictionary.md`), architecture, or core user-facing data contracts must follow the 4-step Change Control Board (CCB) workflow:
1. **Change Request (CR) Submission:** Document business/technical justification, affected WBS items, and triple-constraint impact (Scope, Schedule, Cost/Quality).
2. **Impact Analysis:** Technical Lead (`architect-mcp`) and Scrum Master (`coordinator`) assess risk, backward compatibility, and test coverage impact.
3. **CCB Decision:** Human PM (`Đinh Nhật Cảm`) formally approves, defers, or rejects the CR.
4. **Controlled Implementation & Verification:** Executed on a dedicated feature branch, verified by automated GitHub Actions CI (`ruff`, `pytest`, `tsc`, `eslint`, `vitest`, `npm run build`), reviewed, and merged to `main`.

---

## 2. Master Change Control Log

| CR ID | Title | Submitted Date | Category | Affected WBS / PRs | Schedule Impact | Cost Impact | CCB Decision | Implementation Status |
| :---: | :--- | :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| **CR-001** | Architecture Pivot to Antigravity `sprintguard-mcp` (5-Station Harness) & SQLite Local-First Auto-Seed | 23/11/2026 (M1/M6) | Architecture & Infrastructure | `1.2.2`, `1.5.1`, `1.5.2` (`PR #22`, `PR #25`) | `0 days` (Absorbed within Sprint 1–2 baseline) | **-$15 to -$50/mo saved** ($0 API & hosting) | **APPROVED** | **Implemented & Verified** (`8efa088`, `e807f39`) |
| **CR-002** | Explainable 3D Audit & Anti-Hallucination Vietnamese UI (`key_files`, `commit_highlights`, 4-Tab Inspector) | 25/11/2026 (M7) | Functional UX & Anti-Hallucination | `1.2.1`, `1.5.1`, `1.6.1` (`PR #28`) | `0 days` (Completed within Day 5–6 buffer) | `$0` | **APPROVED** | **Implemented & Verified** (`67ca6b0`, `aud_deep_faa0899d`) |

---

## 3. Detailed Change Request Records

### CR-001: Architecture Pivot to Antigravity `sprintguard-mcp` & SQLite Local-First Auto-Seed

| Field | Details |
| :--- | :--- |
| **CR Identifier** | `CR-001` |
| **Requested By** | `architect-mcp` & Human PM (`Đinh Nhật Cảm`, `24Ite019`) |
| **Date Raised / Approved** | `23/11/2026` (Approved prior to M3/M6 implementation; locked in Charter §5.2) |
| **Status** | **APPROVED & IMPLEMENTED** |

#### 3.1. Problem & Justification
The initial conceptual design considered a server-side `LangGraph` orchestration pipeline calling external LLM APIs (`Groq` / `OpenAI`) with a hosted cloud database. During M1 feasibility analysis, three critical risks were identified:
1. **Cost & Key Exposure:** External LLM APIs violate the `$0` project budget constraint and risk rate-limit failures or key leaks in a public academic repository (`R7`).
2. **Black-Box Hallucinations:** Unconstrained server-side LLM chains could fabricate commit SHAs or issue unfair 0–100 grades without instructor oversight.
3. **Deployment Fragility:** Premature cloud hosting (`Vercel`/`Render`) would introduce cold-start latency and ephemeral disk loss before Sprint 1 core features were verified.

#### 3.2. Approved Scope Modification
- **Replaced** server-side `LangGraph + Groq API` with a local **`FastMCP` server (`sprintguard-mcp`)** exposing **6 stateful tools** (`start_repo_audit`, `submit_context`, `inspect_evidence`, `submit_findings`, `submit_critic_review`, `publish_audit`) enforcing a strict **5-Station State Machine** (`IDLE` → `COLLECTED` → `CONTEXT_SET` → `FINDINGS_SUBMITTED` → `AWAITING_HUMAN_APPROVAL` → `PUBLISHED`), `valid_refs` Evidence Grounding, and mandatory Human-in-the-Loop (HITL) approval.
- **Adopted Local-First SQLite Auto-Seed:** `backend/app/db/sqlite_store.py` initializes `data/sprintguard.db` locally and idempotently seeds 3 reference Deep Audits on startup, enabling instant offline/localhost demos (`127.0.0.1:8000` + `127.0.0.1:5173`) at `$0` cost.

#### 3.3. Triple-Constraint Impact & Verification
- **Scope:** Zero reduction in user-facing diagnostic value; stronger anti-hallucination guarantees via `HarnessGuardError`.
- **Schedule:** `0 days` slip — Sprint 1 (`42` SP) and Sprint 2 M6 (`PR #25`, `e807f39`) delivered on schedule.
- **Cost:** `$0` total runtime and AI cost.
- **Verification Evidence:** `PR #22` (`8efa088`), `PR #25` (`e807f39`, commits `92977f3`, `63e456a`), live Dogfooding audit `aud_deep_995a9cba` (`PR #27`, `4d03a0a`), and 100% green CI.

---

### CR-002: Explainable 3D Audit & Anti-Hallucination Vietnamese UI

| Field | Details |
| :--- | :--- |
| **CR Identifier** | `CR-002` |
| **Requested By** | Human PM (`Đinh Nhật Cảm`, `24Ite019`) following M7 Dogfooding & UAT dry-run |
| **Date Raised / Approved** | `25/11/2026` (Day 6, prior to M8 closure) |
| **Status** | **APPROVED & IMPLEMENTED (`PR #28`)** |

#### 3.1. Problem & Justification
During M7 Dogfooding inspection (`aud_deep_995a9cba`), the PM observed that while the 3D Ownership Graph accurately rendered module clusters and signals, clicking a module node only showed structural counts (`commits`, `churn`) without explaining *what* the module does in Vietnamese or linking directly to the exact source files and GitHub commits. For a 16-minute VKU oral defense, instructors need instant, verifiable drill-down from any 3D sphere to real GitHub evidence to eliminate any suspicion of AI hallucination.

#### 3.2. Approved Scope Modification
1. **Backend & MCP Schema Extension (`c876e76`):**
   - Extended `GraphNode` in `backend/app/core/schemas.py` with backward-compatible fields: `description` (Vietnamese module explanation), `key_files` (real file paths extracted from git diffs), and `commit_highlights` (authentic commit SHA, message, author, date, and clickable GitHub URL).
   - Updated `module_clusterer.py` and `mcp_server/harness.py` so deterministic telemetry and MCP Deep Audits populate `key_files` and `commit_highlights` strictly from real GitHub API payloads (zero fabricated paths or SHAs).
2. **Frontend 4-Tab Vietnamese Inspector (`8ba2815`):**
   - Upgraded `frontend/src/components/SideInspector.tsx` into a structured **4-tab Vietnamese Inspector** (`Tổng quan`, `Chi tiết nút`, `Tín hiệu & Phản biện`, `Câu hỏi vấn đáp`) displaying node descriptions, `key_files` badges, and clickable `https://github.com/.../commit/<sha>` links.

#### 3.3. Triple-Constraint Impact & Verification
- **Scope:** Additive, backward-compatible schema & UI enhancement (`PR #28`). Existing seeded audits and Sprint 1 APIs remained 100% compatible.
- **Schedule:** `0 days` slip — implemented, tested, and merged (`67ca6b0`) on Day 6 prior to M8 Evidence Package generation. (Tracked under `R12` & `R13` in Wave 2 Risk Register.)
- **Cost & Quality:** `$0` cost. Automated QA expanded to **`22` `pytest` tests + `6` `vitest` tests**, all passing (`100%` CI green).
- **Live Verification Evidence:** Published and verified live Deep AI Audit **`aud_deep_faa0899d`** on external repository `fastapi/typer` after reloading `sprintguard-mcp`, confirming Vietnamese `description`, real `key_files`, and clickable GitHub commit links rendered accurately in the 3D Dashboard.

---

## 4. Formal CCB Sign-Off

| Role | Name | Decision | Date |
| :--- | :--- | :---: | :---: |
| **CCB Chair / Human PM** | Đinh Nhật Cảm (`24Ite019`, `@NhatCam2006`) | **Approved (`CR-001`, `CR-002`)** | `25/11/2026` |
| **Technical Lead (AI Swarm)** | Antigravity `architect-mcp` | **Verified & Implemented** | `25/11/2026` |
| **QA & Release Governance** | Antigravity `docs-release` / `qa-docs` | **Audited (`PR #22`, `#25`, `#28`)** | `25/11/2026` |
