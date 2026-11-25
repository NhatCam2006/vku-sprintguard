# Sprint Retrospectives — VKU SprintGuard

**Project:** VKU SprintGuard (`VKU-SPM-GUARD`)  
**PM / Lead:** Đinh Nhật Cảm (`24Ite019`, `@NhatCam2006`)  
**Academic Supervisor:** Dr. Nguyen Thanh Tuan / TS. Nguyễn Thanh Tuấn  
**Methodology:** Hybrid (Milestone-Gated Iterative) · 2 Sprints (6 Accelerated Execution Days mapped to Weeks 1–15, Milestones `M1`–`M10`)  
**Repository:** `https://github.com/NhatCam2006/vku-sprintguard`

---

## 1. Sprint 1 Retrospective — 4Ls Framework (`Liked · Learned · Lacked · Longed For`)

**Scope Reviewed:** Sprint 1 (`Days 1–3`, Milestones `M1`–`M5`, Issues `#1`–`#14`, `42` Story Points, PRs `#20`–`#24`)  
**Objective:** Deliver the Local-First MVP (`localhost:8000` FastAPI + SQLite auto-seed + `POST /api/preview` + `localhost:5173` Interstellar 3D Graph Type A & Timeline 2D) and pass PM Gate 2.

### Liked (What worked well)
1. **Day-1 Toolchain Smoke Test (`PR #20`, Issue `#2`):** Running `uv` Python 3.11 + Node `v26.13.1` with `react-force-graph-3d` on Day 1 de-risked the highest technical uncertainty (`R3`) before parallel Sprint 1 implementation began.
2. **Contract-First Parallelism (`PR #22` & `PR #23`):** Locking Pydantic v2 schemas (`backend/app/core/schemas.py`) and REST endpoints (`/health`, `/api/audits`, `/api/preview`) allowed `backend-dev` and `frontend-3d` to work in isolated git worktrees without merge conflicts.
3. **Single-Account Governance Model (`R4`):** Setting `required_approving_review_count: 0` with mandatory GitHub Actions CI + independent `qa-docs` review comments + Human PM merge avoided GitHub's self-approval deadlock while keeping 100% PR traceability.
4. **Local-First Verification (`M5`, Issue `#13`):** Dual-server localhost E2E (`127.0.0.1:8000` + `127.0.0.1:5173`) validated live 3D preview of `NhatCam2006/vku-sprintguard` (`10` nodes, `9` edges, `1` timeline week) with zero premature cloud deployment overhead.

### Learned (Key technical & PM insights)
1. **3-Pool Model Allocation Eliminates Quota Stalls (`R11`):** Day-1 `HTTP 429` quota errors taught the team to split specialized agents across distinct model pools and use event-driven `swarm_wait` instead of polling loops.
2. **Windows PowerShell Encoding & PATH Gotchas (`R2`, `R10`):** PowerShell `Set-Content -Encoding UTF8` inserts a BOM that breaks `pyproject.toml`, and `gh.exe` is outside default `$env:PATH`. Standardizing BOM-free UTF-8 and explicit `"C:\Program Files\GitHub CLI\gh.exe"` eliminated recurring friction.
3. **Chronological Board Snapshots Matter (`R8`):** Capturing 4 JSON snapshots across Sprint 1 (`sprint1_start`, `sprint1_day1_eod`, `sprint1_mid_m3`, `sprint1_end_review`) created an indisputable burndown trail (`42` → `36` → `18` → `0` remaining after Gate 2 merge).

### Lacked (Gaps identified at M5 Gate 2)
1. **Deep AI Reasoning & Adversarial Critique:** Sprint 1's `POST /api/preview` only delivered deterministic telemetry without Station 1–5 AI reasoning, `valid_refs` Evidence Grounding, or HITL sign-off (intentionally deferred to Sprint 2).
2. **Interactive 3D Investigation Aids:** The Sprint 1 read-only `SideInspector` lacked Camera Fly-to on signal click and `[X-Ray]` healthy-node dimming, making dense graph inspection slower.
3. **Vietnamese Node Explainability:** Raw module names and English-only metadata were less intuitive for VKU students and Vietnamese capstone defense committees.

### Longed For (Desired improvements for Sprint 2)
1. A stateful, `$0`-cost **MCP 5-Station Harness** (`sprintguard-mcp`) that blocks ungrounded hallucinations (`valid_refs`) and enforces PM HITL approval before publishing.
2. A **Vietnamese-first explainable 3D Inspector** linking every module directly to real `key_files` and clickable GitHub commits.
3. Live **Dogfooding** on `vku-sprintguard` and an external open-source repository to stress-test the 40-module clusterer and Critic review.

### Sprint 1 Action Items (Carried into Sprint 2 — All Completed)
| Action ID | Action Item | Owner | Target | Status in Sprint 2 |
| :---: | :--- | :--- | :---: | :--- |
| **A1-1** | Implement 6-tool `sprintguard-mcp` 5-station harness + `SKILL.md` (`#15`, `#16`) | `architect-mcp` | Day 4 (`M6`) | **Done** (`PR #25`, `e807f39`) |
| **A1-2** | Add Camera Fly-to, `[X-Ray]` filter & Critic/HITL display in `SideInspector` (`#17`) | `frontend-3d` | Day 5 (`M7`) | **Done** (`PR #26`, `bfa0c93`) |
| **A1-3** | Execute live Dogfooding audit (`aud_deep_995a9cba`) & prepare VKU Peer UAT Kit (`#18`) | `qa-docs` / PM | Day 5 (`M7`) | **Done** (`PR #27`, `4d03a0a`) |

---

## 2. Final Whole-Project Retrospective — Sailboat Framework (`Wind · Anchor · Rocks · Island`)

**Scope Reviewed:** Full Project (`Days 1–6`, Milestones `M1`–`M10`, Issues `#1`–`#19`, `63` Story Points, PRs `#20`–`#29`, Change Requests `CR-001` & `CR-002`)

```text
                        ⛵ VKU SPRINTGUARD — SAILBOAT RETROSPECTIVE
                                         🏝️ ISLAND (Goal Achieved)
                                         63 SP · 100% CI · 2 Live Deep Audits
                                         8 Google Drive Deliverables · $0 Cost
        💨 WIND (Propelling Forces)         /
        - Local-First + MCP $0 Brain       /
        - Isolated Worktrees + CI         /
        - Evidence Grounding & HITL      /
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                       |         🪨 ROCKS (Future Risks)
                                   ⚓ ANCHOR      - MCP restart after schema change (R12)
                                   - Windows PATH - GitHub PAT expiry / 60 req/hr limit
                                   - Mid-sprint   - Large monorepos > 100 commits
                                     UX scope     - Optional HTTPS deploy cold starts
```

### Wind (What propelled the project forward)
1. **`CR-001` MCP Architecture Pivot ($0 API Cost):** Replacing server-side `LangGraph + Groq API` with Antigravity `sprintguard-mcp` (6 tools, 5-station State Machine) eliminated API billing, latency failures, and key management complexity while enabling genuine Adversarial Self-Critique (Station 4) and HITL sign-off (Station 5).
2. **Strict Automated Quality Gates (`22` pytest + `6` vitest, `100%` CI pass):** Every single PR (`#20`–`#28`) passed `ruff`, `pytest`, `tsc`, `eslint`, `vitest`, and `npm run build` with exit code `0` before Human PM merge.
3. **Disciplined Change Control (`CR-002`, `PR #28`):** When the PM requested Vietnamese explainability (`GraphNode.description`, `key_files`, `commit_highlights` with clickable GitHub links, and 4-tab Vietnamese `SideInspector`), the team processed it through formal CCB impact analysis and shipped it in `PR #28` (`67ca6b0`) without slipping Day 6 closure.
4. **Authentic Dual-Repo Validation:** Live Dogfooding on `NhatCam2006/vku-sprintguard` (`aud_deep_995a9cba`) and external stress-testing on `fastapi/typer` (`aud_deep_faa0899d`) proved that the harness prevents false-positive `risk` escalation and grounds every claim in real commit SHAs.

### Anchor (What slowed us down)
1. **MCP Server Schema Caching (`R12`):** After merging `CR-002` (`c876e76`), the long-lived `sprintguard-mcp` stdio process cached the old pre-CR-002 schema until restarted, adding a debugging cycle during final live verification.
2. **Windows Environment Quirks (`R2`, `R10`):** PowerShell 5.1 syntax (`;` instead of `&&`), UTF-8 BOM issues, and non-PATH `gh.exe` required extra defensive scripting.
3. **Single-Account GitHub Constraints (`R1`, `R4`):** Initial missing `read:project` OAuth scope required a PM Gate 1 pause, and single-account ownership required custom PR review documentation instead of native GitHub Approvals.

### Rocks (Risks & watch-outs for v2.0 / future VKU cohorts)
1. **MCP Process Lifecycle Management:** Any future schema update in `backend/app/core/schemas.py` must be paired with an explicit MCP server reload checklist item (`R12`).
2. **GitHub API Sampling Ceiling:** Very large capstone monorepos (> 100 commits or > 30 PRs) may need paginated sampling or optional `GITHUB_TOKEN` configuration for VKU instructors auditing 20+ teams in one session.
3. **Optional Cloud Deployment Cold Starts:** If deployed later to free-tier Render/Vercel, SQLite persistence would need volume mounting or migration to hosted Postgres/Turso so published Deep Audits survive container restarts.

### Island (Vision achieved & Lessons for future projects)
- **Delivered:** 100% of WBS scope (`63` SP across 19 Issues), 9 merged/open feature PRs (`#20`–`#29`), 2 formal CCB Change Requests (`CR-001`, `CR-002`), 6 chronological board snapshots, 2 verified live Deep AI Audits (`aud_deep_995a9cba`, `aud_deep_faa0899d`), and the complete 8-file Google Drive QLDA Evidence Package at **$0 infrastructure and AI cost**.
- **Core Lesson Learned:** *Decision Support beats Automated Grading.* Combining deterministic GitHub telemetry (`Graph3D` + `Timeline2D`) with an evidence-grounded, HITL-gated AI Critic produces transparent, defensible insights that instructors and students trust during oral defense.
