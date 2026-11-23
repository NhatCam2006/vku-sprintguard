# SOFTWARE PROJECT CHARTER

**Course:** Software Project Management (`Quản trị dự án phần mềm (5)`)  
**Academic Supervisor / Instructor:** Dr. Nguyen Thanh Tuan / TS. Nguyễn Thanh Tuấn  
**Submission Deadline:** End of Week 2 (Milestone M1)  
**Document Version:** Version 1.0 (Draft — Pending PM Gate 1 Approval)  
**Recommended Length:** 3 – 5 pages (Concise, actionable, and bounded — not an exhaustive SRS)

---

> ⚠️ **MANDATORY POLICY — AUTHENTIC PROJECTS ONLY:**  
> Every section in this charter must be populated with **authentic, verifiable data from your team's real software engineering project**. Placeholder text (*lorem ipsum*), imaginary scenarios, and synthetic projects are strictly prohibited. The project must have a live GitHub repository, an active GitHub Project board, real stakeholders or users, and concrete technical constraints. Charters failing the "Authentic Project" criteria will be returned for revision before the team is permitted to proceed to Week 3 Work Breakdown Structure (WBS) decomposition.

---

## 1. PROJECT GENERAL INFORMATION

| Item | Details |
| :--- | :--- |
| **Project Name** | VKU SprintGuard |
| **Project Acronym / Key** | `VKU-SPM-GUARD` |
| **Course Cohort** | `Quản trị dự án phần mềm (5)` (`Software Project Management (5)`) |
| **Team Name / Identifier** | VKU SprintGuard — Team Solo PM + Antigravity AI Swarm (`24Ite019`) |
| **Creation Date** | 23/11/2026 |
| **Document Version** | Version 1.0 (Draft — Pending PM Gate 1 Approval) |
| **Primary GitHub Repository** | `https://github.com/NhatCam2006/vku-sprintguard` |
| **GitHub Project Board URL** | Pending PM `gh auth refresh -s project,read:project` at Gate 1 (Milestone M2) |

---

## 2. PROJECT SOURCING & REAL-WORLD CONTEXT

*Select `[x]` one of the three approved sourcing pathways according to the course syllabus:*

- [ ] **Pathway 1: Capstone Project from Concurrent Engineering Course**  
  *(e.g., Capstone project from Cross-Platform Mobile Development, AI Engineering, or Web Engineering)*
- [ ] **Pathway 2: Real External Client / Freelance Project / Industry Partner**  
  *(A genuine external business, startup, or freelance client who will formally review and accept the deliverables)*
- [x] **Pathway 3: Real Campus / Department / Student Organization Need at VKU**  
  *(An authenticated operational need from VKU Faculty of Computer Science supporting instructors, capstone evaluation committees, and student project teams in auditing authentic GitHub software project execution.)*

**Context Summary:** In Software Project Management and IT capstone courses at the Vietnam-Korea University of Information and Communication Technology (VKU), instructors and defense committees must audit dozens of student GitHub repositories to verify the *Authentic Project Rule* (distributed commits, genuine teamwork vs. last-minute commit dumps, balanced module ownership, and PR/CI discipline). Student teams also need an objective self-audit tool before defense. `VKU SprintGuard` directly serves this VKU academic operational need, with real VKU peer project teams testing the system on their actual course repositories during UAT.

---

## 3. EXECUTIVE SUMMARY & BUSINESS CASE

- **Operational Background:** At VKU's Faculty of Computer Science, course instructors (such as Dr. Nguyen Thanh Tuan / TS. Nguyễn Thanh Tuấn) and capstone defense panels evaluate student software projects through GitHub repositories, Kanban boards, and a 16-minute live oral defense (including a 5-minute Q&A). Currently, inspecting repository authenticity requires manually browsing dozens of commit pages, pull requests, and directory trees across multiple student repositories under tight grading schedules.
- **Core Problem Statement:** Raw GitHub metrics (line counts or total commits) frequently misjudge real student contributions—penalizing solo projects for lacking peer PR approvals, misclassifying teammates who focus on tests/documentation/UI rather than high-LOC code, or failing to flag late "commit dumps" and unreviewed Mega-PRs buried inside noisy lockfile diffs. Rigid automated 0–100 grading tools create false positives and grading disputes rather than actionable insight.
- **Proposed Software Solution:** `VKU SprintGuard` is a **Decision Support System** ("X-Ray + diagnostic assistant", not an automated 0–100 grader) combining deterministic Python GitHub telemetry, an **Interstellar Light Minimalism** 3D Web Dashboard (`Clustered 3D Network`, `2D Commit Rhythm Timeline`, `Side Inspector`), and (in Sprint 2) an Antigravity-connected **MCP 5-Station State-Machine Harness** (`collect_repo` → `detect_context` → `analyze_evidence` → `critic_review` → `publish_audit`) with Evidence Grounding and mandatory Human-in-the-Loop (HITL) sign-off. In Sprint 1, the system delivers a Local-First (`localhost`) FastAPI + SQLite + React 3D MVP capable of displaying pre-seeded Deep Audits and running instant **Live 3D Previews** on any public GitHub repository (starting with `NhatCam2006/vku-sprintguard`).

---

## 4. SMART PROJECT OBJECTIVES

1. **Objective 1 (Core Functional Capability — Local-First MVP & MCP Harness):**  
   Deliver the Sprint 1 Local-First MVP (`backend/` FastAPI + SQLite startup auto-seed + `POST /api/preview` + `frontend/` React Interstellar 3D Graph Type A & Timeline 2D) running simultaneously on `localhost:8000` and `localhost:5173` within Day 3 (Milestone M5); then deliver the Sprint 2 6-tool `sprintguard-mcp` 5-station harness with `valid_refs` Evidence Grounding and HITL gate by Day 6.
2. **Objective 2 (Operational & User Validation):**  
   Validate the Live 3D Preview pipeline against `https://github.com/NhatCam2006/vku-sprintguard` and 3 pre-seeded Deep Audit profiles during Sprint 1 (Day 3), and complete authentic UAT with VKU student capstone peers on their real repositories with formal written acceptance sign-off during Sprint 2 (before Week 13 Closure).
3. **Objective 3 (Engineering Rigor & Quality Gate):**  
   Maintain 100% Conventional Commits across dedicated feature branches, enforce automated GitHub Actions CI (`ruff`, `pytest`, `tsc`, `eslint`, `vitest`, `npm run build` exiting `0`) on every Pull Request, track 100% of WBS items on the 5-column GitHub Projects v2 board (with `Story Points`, `Iteration`, and multi-stage board snapshots), and prevent unreviewed merges to `main`.
4. **Objective 4 (Delivery Mode & Evidence Package Handover):**  
   Complete 100% of Sprint 1 verification locally on `localhost` with zero premature cloud deployment, and in Sprint 2 compile the complete 8-file Google Drive Evidence Package (`01`–`08`, including past-tense 7-chapter technical report, formula-driven Risk Register `.xlsx`, and `CR-001` record), tag release `v1.0.0`, and deploy via public HTTPS (Vercel/Render) only if requested by the PM at the final stage.

---

## 5. PROJECT SCOPE & BOUNDARIES

### 5.1. In-Scope (Committed Deliverables & Features)
- **Core Module 1 — Backend Telemetry, Persistence & Preview Engine (`backend/`, Sprint 1):**
  - FastAPI application (`app/main.py`) with CORS for `localhost`, `GET /health`, `GET /api/audits`, `GET /api/audits/{audit_id}`, `POST /api/audits` (protected by `PUBLISH_API_KEY`), and `POST /api/preview`.
  - SQLite persistence (`sqlite_store.py`) with idempotent startup auto-seed of pre-committed sample Deep Audit reports.
  - GitHub REST API client (`github_client.py` via `httpx`, capped at 100 commits + 30 PRs, optional `GITHUB_TOKEN`), `diff_filter.py` (stripping lockfiles, minified assets, and build directories), and `module_clusterer.py` (2-level directory depth, max 40 largest modules + `other/`, deterministic `timeline_2d` anomaly detection, Pydantic v2 `schemas.py`).
- **Core Module 2 — Interstellar Light Minimalism 3D Web Dashboard (`frontend/`, Sprint 1 + Sprint 2 Polish):**
  - Minimalist white-background (`#FFFFFF` / `#09090B`) UI with `Montserrat` + `Inter` (`tabular-nums`), Landing Screen (GitHub URL input + sample Deep Audit cards), Top Bar (`/health` indicator + URL input), Clustered 3D Network (`Graph3DCanvas.tsx` with Focus Mode and `[Reset Camera]`), `Timeline2D.tsx` weekly commit bar chart, and read-only `SideInspector.tsx` (Sprint 1), followed by Sprint 2 Deep AI Inspector polish (Camera Fly-to, X-Ray filter, Critic/HITL display).
- **Core Module 3 — MCP State-Machine Harness, Dogfooding & Peer UAT (`mcp_server/`, `skills/`, Sprint 2 Deferred):**
  - `sprintguard-mcp` (`FastMCP` server + 5-station State Machine + `valid_refs` Evidence Grounding + HITL approval gate), `skills/sprintguard-auditor/SKILL.md`, Antigravity `mcp_config.json` integration, Dogfooding audit of `NhatCam2006/vku-sprintguard`, and VKU Peer UAT.
- **Engineering & Governance Deliverables (Sprint 1 Initiation + Sprint 2 Closure):**
  - Public GitHub repository with distributed commit history, 5-column GitHub Projects v2 board (`Story Points`, `Iteration`, board snapshots), Milestones, 1:1 WBS GitHub Issues, GitHub Actions CI, QLDA documentation (`docs/qlda/`), and the 8-file Google Drive Evidence Package + Release `v1.0.0`.

### 5.2. Explicitly Out-of-Scope (Scope Boundaries)
- Automated hard numeric grading (0–100 scorecards) replacing instructor judgment (prohibited by Decision Support System philosophy).
- Server-side `LangGraph` pipelines or paid/external LLM API integrations such as Groq/OpenAI (replaced by Antigravity Brain via `sprintguard-mcp` at $0 API cost — `CR-001`).
- Premature cloud deployment (`Vercel`, `Render`, `Cloudflare Pages`, `Hugging Face Spaces`) during Sprint 1 Local-First execution (deferred until PM explicitly requests HTTPS deployment at the final stage).
- Institutional VKU SSO/LDAP integration, multi-tenant user registration, paid cloud infrastructure, or non-GitHub VCS/PM platforms (GitLab, Bitbucket, Jira, Trello, Notion).

---

## 6. STAKEHOLDER REGISTER & ENGAGEMENT MATRIX

### 6.1. Stakeholder Register

| Stakeholder / Entity | Role in Project | Power | Interest | Engagement Strategy |
| :--- | :--- | :---: | :---: | :--- |
| **Course Instructor / Supervisor (Dr. Nguyen Thanh Tuan / TS. Nguyễn Thanh Tuấn)** | Academic evaluator, milestone auditor & VKU domain authority | High | High | **Manage Closely**: Formal checkpoint submissions (M1–M10), rubric compliance, and final 16-minute defense evaluation. |
| **Human PM / Project Lead (Đinh Nhật Cảm — `24Ite019`)** | Product owner, PR merge authority, HITL approver & coordinator | High | High | **Manage Closely**: Approves Sprint plans, executes Gate 1/Gate 2 reviews, merges all PRs to `main`, coordinates UAT. |
| **Antigravity AI Engineering Swarm (`coordinator`, `architect-mcp`, `backend-dev`, `frontend-3d`, `qa-docs`)** | Architecture, implementation, testing, PR review & QLDA documentation | High | High | **Collaborate Daily**: Worktree-isolated branches, interface contracts, Conventional Commits, automated CI, QA review gates. |
| **VKU Student Peer Testers (Pathway 3 Pilot Users)** | End users validating Live 3D Preview & Deep Audit utility on real repos | Low | High | **Keep Informed**: Guided UAT scenarios in Sprint 2 and formal acceptance feedback (`07_Stakeholder_Acceptance_Signoff.pdf`). |
| **GitHub Platform & Local/Free-Tier Infrastructure** | VCS, CI runners, GitHub REST API & optional free hosting constraints | High | Low | **Keep Satisfied**: Respect API rate limits (max 100 commits/30 PRs, optional PAT), $0 budget, zero committed secrets. |

### 6.2. Power-Interest Matrix

```text
High Power  │  MANAGE CLOSELY                         │  KEEP SATISFIED
            │  - Course Instructor (TS. Nguyễn Thanh  │  - GitHub Platform & API Rate Limits
            │    Tuấn)                                │  - Local Runtime / Free-Tier Infra
            │  - Human PM (Đinh Nhật Cảm)             │
            │  - Antigravity AI Engineering Swarm     │
────────────┼─────────────────────────────────────────┼──────────────────────────────
Low Power   │  KEEP INFORMED                          │  MONITOR
            │  - VKU Student Peer Capstone Testers    │  - External Open-Source Community
            │  - Defense Audience / VKU CS Peers      │  - Unaffiliated Public Repo Owners
            └─────────────────────────────────────────┴──────────────────────────────
                           High Interest                           Low Interest
```

---

## 7. PROJECT MANAGEMENT STACK & GITHUB ECOSYSTEM

*The project strictly utilizes the **unified GitHub platform** as its complete engineering and project management suite. External tracking tools (e.g., Jira, Trello, Asana, ClickUp) are not permitted.*

| Project Management Domain | GitHub Tool / Feature | Governance Standard |
| :--- | :--- | :--- |
| **Source Code Repository** | **GitHub Repository (`NhatCam2006/vku-sprintguard`)** | Branch protection on `main`; direct push to `main` forbidden; commit history must follow Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `ci:`, `chore:`). |
| **Project Tracking & Board** | **GitHub Projects v2 (Board & Table)** | Exact 5 Kanban columns: `Backlog`, `Ready`, `In Progress`, `In Review`, `Done`; custom fields `Story Points` (Number) and `Iteration` (`Sprint 1`, `Sprint 2`) configured before closing the first Issue; multi-stage board snapshots exported. |
| **Task & Work Package Management** | **GitHub Issues** | Strict 1:1 mapping per leaf WBS work package (`<= 2 days` effort). Every issue includes Acceptance Criteria, Assignee, Milestone, `Story Points`, and `Iteration`. |
| **Code Review & Quality Control** | **GitHub Pull Requests (PRs)** | All changes enter `main` via feature-branch PR referencing an issue (`Refs #N` or `Resolves #N`) with self-testing notes. **Single-Account Rule:** Because `@NhatCam2006` is the sole GitHub account, *"Require 1 approving review"* is **NOT** enabled (GitHub forbids self-approval); instead, `qa-docs` posts an independent PASS/FAIL review comment with command evidence and the Human PM inspects and merges each PR. |
| **Milestone Tracking** | **GitHub Milestones** | Configured for `Sprint 1: Initiation & Local-First MVP` and `Sprint 2: MCP Harness, Dogfooding & Final Evidence (Deferred)`, aligned with VKU checkpoints `M1`–`M10`. |
| **Continuous Integration & Delivery** | **GitHub Actions (`.github/workflows/ci.yml`)** | Automated workflow on every PR running Backend (`uv` Python 3.11: `ruff`, `pytest`) and Frontend (Node 26: `tsc`, `eslint`, `vitest`, `npm run build`), blocking merge on non-zero exit. |

---

## 8. HIGH-LEVEL MILESTONES & SCHEDULE

*Aligned with the 10 formal checkpoints of the course and mapped to the accelerated 6-day Sprint 1 (Days 1–3) + Sprint 2 (Days 4–6, Deferred) execution cadence:*

| Milestone | Target Week / Sprint Day | Major Deliverables | Responsible Role |
| :---: | :---: | :--- | :--- |
| **M1** | Week 2 (Day 1 — Sprint 1) | Approved Project Charter (13 sections), `.env.example`, `.github/workflows/ci.yml`, Day-1 Python 3.11 + Node 26 `react-force-graph-3d` build verification | Human PM (`@NhatCam2006`), `coordinator`, `qa-docs`, `architect-mcp`, `frontend-3d` |
| **M2** | Weeks 3–4 (Day 1–2 — Sprint 1) | WBS & WBS Dictionary (100% Rule), 19 GitHub Issues, GitHub Projects v2 5-column Board (`Story Points`, `Iteration`) & Sprint 1 Start Snapshot | `coordinator`, `qa-docs`, Human PM |
| **M3** | Week 5 (Day 2 — Sprint 1) | Sprint 1 Backend Core (`backend/` FastAPI, SQLite auto-seed, GitHub REST client, Diff Filter, 2-level Module Clusterer, Timeline 2D, `/api/preview`, `pytest` + `ruff`) | `backend-dev`, `architect-mcp` |
| **M4** | Weeks 6–7 (Day 3 — Sprint 1) | Sprint 1 Frontend 3D (`frontend/` Interstellar Light Minimalism, Landing Screen, `Graph3DCanvas.tsx`, `Timeline2D.tsx`, read-only `SideInspector.tsx`, `tsc`/`eslint`/`vitest`/build) | `frontend-3d` |
| **M5** | Weeks 8–9 (Day 3 — Sprint 1 Closure) | Sprint 1 Localhost E2E Acceptance (`localhost:8000` + `:5173`, Live 3D Preview on `vku-sprintguard`, Tiers 1–5), Board Mid/End Snapshots, Risk Register Wave 1 actuals update -> **PM Sprint 1 Stop Gate** | `qa-docs`, `coordinator`, Human PM |
| **M6** | Weeks 9–10 (Day 4 — Sprint 2 Deferred) | `sprintguard-mcp` (6 tools, 5-station State Machine, `valid_refs` Evidence Grounding, HITL), `skills/sprintguard-auditor/SKILL.md`, Antigravity `mcp_config.json` live test | `architect-mcp` |
| **M7** | Weeks 11–12 (Days 5–6 — Sprint 2 Deferred) | Deep AI Side Inspector polish, Dogfooding audit, Risk Register Wave 2 update & Scope Change Control Record (`CR-001`) | `frontend-3d`, `qa-docs`, `coordinator` |
| **M8** | Week 13 (Day 6 — Sprint 2 Deferred) | VKU Peer UAT execution, Stakeholder Acceptance Sign-Off (`07_Stakeholder_Acceptance_Signoff.pdf`), Sprint 1 & Final Retrospectives (`05_Sprint_Retrospectives.pdf`) | Human PM, `qa-docs` |
| **M9** | Week 14 (Day 6 — Sprint 2 Deferred) | Complete 8-file Google Drive Evidence Package (`01`–`08`, `01_Final_Technical_Report.pdf` in 100% past tense), Release `v1.0.0`, optional HTTPS deploy if PM requests | `qa-docs`, `coordinator`, Human PM |
| **M10** | Week 15 (Defense — Sprint 2 Deferred) | 16-minute Final Oral Defense & Live System Demonstration (6m slides, 5m live demo, 5m Q&A) before VKU Evaluation Committee | Human PM (`Đinh Nhật Cảm`) |

---

## 9. DEVELOPMENT METHODOLOGY & CADENCE

### 9.1. Chosen Development Methodology
- [ ] **Iterative & Incremental Development** (Timeboxed 2–3 week delivery cycles with progressive feature refinement)
- [ ] **Agile Flow / Kanban** (Continuous delivery prioritized by pull limits and work-in-progress constraints)
- [x] **Hybrid (Milestone-Gated Iterative)** (Predictable architectural and governance milestones combined with flexible feature iterations)
- [ ] **Structured Sequential / Waterfall** (Phase-gated progression suited for strictly fixed, pre-defined technical specifications)

### 9.2. Methodology Justification
- **Requirement Volatility & Discovery:** While the core QLDA rubric (M1–M10) is fixed by the course syllabus, visual encoding in the 3D Graph, deterministic anomaly thresholds, and AI prompt/harness behavior require iterative refinement across Sprint 1 (Local-First MVP) and Sprint 2 (MCP Harness & Peer UAT).
- **Stakeholder Availability:** Human PM (`Đinh Nhật Cảm`) reviews and merges every PR at explicit Milestone Gates (`Gate 1` after M1 Initiation, `Gate 2` at M5 Sprint 1 Closure, and UAT sign-off in Sprint 2), pairing naturally with milestone-gated iterations and a 5-column Kanban flow.
- **Technical Risk Management:** Using `Node v26.13.1` with `react-force-graph-3d` and integrating `FastMCP` with Antigravity requires early Day-1 build-smoke validation and explicit contract locking (`schemas.py`, REST routes) before parallel Backend/Frontend execution.

---

## 10. TEAM ORGANIZATION & GOVERNANCE ROLES

*Transparent **1 Human PM + Antigravity AI Swarm** operating model per `VKU-SprintGuard-Blueprint.md` §8.2 and `PROJECT-DECISIONS.md` §3:*

| # | Member Name | Student ID | GitHub Username | Project Role | Primary Responsibilities |
| :-: | :--- | :---: | :---: | :--- | :--- |
| 1 | **Đinh Nhật Cảm** *(Human PM)* | `24Ite019` | `@NhatCam2006` | **Project Lead / PM** | Owns product vision, approves Sprint plans & HITL checkpoints, runs `gh auth refresh` & local verification, reviews and merges all PRs to `main`, coordinates VKU peer UAT and final defense. |
| 2 | **Antigravity `coordinator`** *(AI Orchestrator)* | N/A (AI Agent) | `@NhatCam2006` *(via Swarm)* | **Scrum Master / Coordinator** | Maintains 6-day Sprint 1/2 cadence, delegates WBS issues across isolated worktrees, enforces Prevention Points & PM stop gates; never auto-merges `main`. |
| 3 | **Antigravity `architect-mcp`** *(AI Tech Lead)* | N/A (AI Agent) | `@NhatCam2006` *(via Swarm)* | **Technical Lead / Architect** | Designs repo architecture, Pydantic v2 `schemas.py`, `.github/workflows/ci.yml`, `.env.example`, and (Sprint 2) `mcp_server/` 6-tool State Machine + `SKILL.md`. |
| 4 | **Antigravity `backend-dev`** *(AI Backend Dev)* | N/A (AI Agent) | `@NhatCam2006` *(via Swarm)* | **Backend Engineer** | Implements FastAPI endpoints (`/health`, `/api/audits`, `/api/preview`), SQLite store + startup auto-seed, `github_client.py`, `diff_filter.py`, `module_clusterer.py`, and `pytest` + `ruff`. |
| 5 | **Antigravity `frontend-3d`** *(AI Frontend Dev)* | N/A (AI Agent) | `@NhatCam2006` *(via Swarm)* | **Frontend / 3D Engineer** | Implements Interstellar Light Minimalism theme, Landing Screen, `Graph3DCanvas.tsx`, `Timeline2D.tsx`, `SideInspector.tsx`, and `tsc`/`eslint`/`vitest`/Vite build on Node 26. |
| 6 | **Antigravity `qa-docs`** *(AI QA & QLDA Docs)* | N/A (AI Agent) | `@NhatCam2006` *(via Swarm)* | **QA & Documentation Engineer** | Executes independent PR reviews (PASS/FAIL comments with real command outputs), captures multi-stage board snapshots, authors QLDA docs (`docs/qlda/`), and compiles the 8 Drive deliverables. |

---

## 11. CONSTRAINTS, ASSUMPTIONS & INITIAL RISKS

### 11.1. Project Constraints (Triple Constraint)
- **Schedule:** Accelerated 6-day build cadence mapped to the 15-week VKU course checkpoints (`M1`–`M10`), with a mandatory **Sprint 1 Local-First completion & stop gate at Day 3 (M5)** before Sprint 2 (`Days 4–6`).
- **Budget & Infrastructure:** `$0` total budget. Sprint 1 operates strictly Local-First (`127.0.0.1:8000` + `127.0.0.1:5173`) using SQLite and GitHub Free; any optional Sprint 2 deployment must use `$0` free-tier platforms (e.g., Vercel / Cloudflare Pages / Render) and $0 AI API cost via Antigravity MCP.
- **Technology Stack:** `Python 3.11.9` + `uv 0.13.7`, `FastAPI`, `Pydantic v2`, `HTTPX`, `SQLite`, `ruff`, `pytest`; `Node v26.13.1` + `npm 11.6.4`, `React`, `TypeScript`, `Vite`, `Tailwind CSS`, `react-force-graph-3d`, `vitest`, `eslint`; `FastMCP` (Sprint 2).

### 11.2. Key Assumptions
- Human PM (`@NhatCam2006`) will execute `gh auth refresh -s project,read:project` at Gate 1 and review/merge open PRs in a timely manner.
- Public GitHub REST API remains accessible for Live 3D Preview tests (`NhatCam2006/vku-sprintguard`), with optional `GITHUB_TOKEN` available if the 60 req/hr unauthenticated limit is approached.
- `react-force-graph-3d` builds cleanly under `Node v26.13.1` (verified via Day-1 smoke build in M1).
- VKU student peers are available in Sprint 2 to run UAT on real course repositories.

### 11.3. Top 3 Initial Project Risks

| Initial Risk | Probability | Impact | Proactive Response & Mitigation Plan |
| :--- | :---: | :---: | :--- |
| **1. GitHub CLI `read:project` scope gap & single-account PR review deadlock** | High | High | Prompt PM to run `gh auth refresh -s project,read:project` at Gate 1 before M2 board setup; configure branch protection WITHOUT *"Require 1 approving review"* and enforce CI + `qa-docs` comment + PM merge. |
| **2. Node `v26.13.1` incompatibility with `react-force-graph-3d` / Three.js** | Medium | High | Execute `npm install` + `npm run build` build-smoke test on Day 1 (M1) before parallel Sprint 1 frontend development; lock compatible dependency versions in `package-lock.json`. |
| **3. Scope creep from Sprint 2 (`mcp_server/`, `SKILL.md`, cloud deploy) into Sprint 1** | Medium | High | Enforce strict WBS Sprint 1 vs. Sprint 2 separation, Charter §5.2 boundaries, and an explicit PM Gate 2 stop checkpoint after M5 Localhost E2E verification. |

---

## 12. SUCCESS CRITERIA & DEFINITION OF DONE (DoD)

### 12.1. Project Success Criteria
1. **Functional Completeness:** 100% of Sprint 1 In-Scope capabilities operate cleanly on `localhost` (`/health` HTTP 200, SQLite auto-seeded sample Deep Audits, Live 3D Preview of `NhatCam2006/vku-sprintguard` in white Interstellar 3D UI), followed in Sprint 2 by the verified 6-tool `sprintguard-mcp` harness.
2. **Authentic Validation:** Real distributed commit/PR history on `NhatCam2006/vku-sprintguard`, verifiable multi-stage GitHub Projects board history, evolving Risk Register (Wave 1 actuals + Wave 2), and formal VKU peer UAT acceptance sign-off in Sprint 2.
3. **Engineering Integrity:** Zero lint/type/test/build errors in CI (`ruff`, `pytest`, `tsc`, `eslint`, `vitest`, `npm run build`), zero committed secrets or `docs/reference/` files, and complete 8-file Evidence Package matching `MilestoneRubric.md` and `EvidencePackageChecklist.md`.

### 12.2. Engineering Definition of Done (DoD) for Every Work Item
*A GitHub Issue or work item may only be transitioned to the `Done` column on the GitHub Project board when all the following criteria are satisfied:*
- [ ] Source code/documentation is implemented, formatted, and verified locally (`ruff`/`pytest` and/or `tsc`/`eslint`/`vitest`/`npm run build`).
- [ ] A GitHub Pull Request is opened from a feature branch with a clear description referencing the issue (e.g., `Resolves #N`).
- [ ] Independent `qa-docs` Review Comment (`PASS` with verbatim command outputs) and Human PM check are recorded on the Pull Request (per Single-Account Branch Protection Rule in §7).
- [ ] Automated GitHub Actions CI workflow (linting, unit tests, build test) passes with green status (`exit code 0`).
- [ ] Security & hygiene scan verified: no API keys, `.env` files, tokens, `*.db` binaries, or gitignored `docs/reference/` files committed to Git.
- [ ] Pull Request is reviewed and merged into `main` by the Human PM (`@NhatCam2006`) and verified on the target environment (`localhost:8000` + `localhost:5173` for Sprint 1; optional HTTPS if requested in Sprint 2).
- [ ] All Acceptance Criteria specified in the GitHub Issue are verified by `qa-docs`.
- [ ] The associated GitHub Issue is closed and moved to `Done` on the GitHub Project board, with board snapshot history updated at milestone checkpoints.

---

## 13. FORMAL APPROVALS & SIGN-OFF

*By signing below, the signatories endorse this Project Charter, granting the project team formal authorization to proceed with Work Breakdown Structure (WBS) decomposition and project execution in accordance with the defined scope and schedule.*

| Project Lead / Team Representative | Project Sponsor / Client Stakeholder | Academic Supervisor / Course Instructor |
| :---: | :---: | :---: |
| *(Signature & Full Name)* | *(Signature & Full Name)* | *(Signature & Full Name)* |
| <br><br><br> | <br><br><br> | <br><br><br> |
| **Đinh Nhật Cảm (MSSV: 24Ite019)** | **VKU Pilot Stakeholder (Pathway 3 — Sprint 2 UAT Sign-off)** | **Dr. Nguyen Thanh Tuan (TS. Nguyễn Thanh Tuấn)** |
| Date: ...... / ...... / 2026 | Date: ...... / ...... / 2026 | Date: ...... / ...... / 2026 |
