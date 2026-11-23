# Sprint 1 Start Board Snapshot (`sprint1_start`)

## 1. Board Overview & Snapshot Metadata

| Field | Value |
| :--- | :--- |
| **Project Title** | VKU SprintGuard — Sprint & Kanban Board |
| **Project Number** | `#1` |
| **Project URL** | https://github.com/users/NhatCam2006/projects/1 |
| **Repository** | `NhatCam2006/vku-sprintguard` |
| **Snapshot Stage** | `sprint1_start` (Pre-Close Baseline) |
| **Captured At (UTC)** | `2026-11-23T09:15:01Z` |
| **Source JSON** | `docs/qlda/board_snapshots/sprint1_start.json` |
| **Baseline Verification** | `0` issues closed (`#1`–`#19` all `OPEN`), `0` SP in `Done`, `42` SP remaining in `Sprint 1` |

## 2. Board Columns & Custom Fields

### 2.1 `Status` Columns (`PVTSSF_lAHOC1bhgc4Bs1a_zhrBpRw`)

| Order | Column Name | Option ID | Purpose |
| :---: | :--- | :--- | :--- |
| 1 | `Backlog` | `0e2fea83` | Queued for Sprint 1 or deferred to Sprint 2 |
| 2 | `Ready` | `ac20e6a9` | Refined and ready to start in active Sprint |
| 3 | `In Progress` | `564db825` | Actively being implemented on a feature branch |
| 4 | `In Review` | `f8d031ff` | PR opened, CI running, awaiting qa-docs & PM review |
| 5 | `Done` | `c231a99a` | Merged into main and verified against DoD |

### 2.2 Custom Fields

| Field Name | Field ID | Type | Configuration / Options |
| :--- | :--- | :--- | :--- |
| `Story Points` | `PVTF_lAHOC1bhgc4Bs1a_zhrBpo0` | `NUMBER` (`ProjectV2Field`) | Numeric effort estimate per WBS item |
| `Iteration` | `PVTIF_lAHOC1bhgc4Bs1a_zhrBpo4` | `ITERATION` (`ProjectV2IterationField`) | `Sprint 1` (`8a440d3a`, `2026-11-23`, 3d), `Sprint 2` (`2a565f13`, `2026-11-26`, 4d) |

## 3. Complete 19-Item Board Inventory

| Issue # | WBS ID | Title | Iteration | Story Points | Initial Board Status | GitHub State | Milestone |
| :---: | :---: | :--- | :---: | :---: | :--- | :---: | :--- |
| `#1` | `1.1.1` | [WBS 1.1.1] docs(qlda): Author Project Charter (13 sections), WBS & Dictionary, Risk Register Wave 1, and .env.example | `Sprint 1` | `3` | `In Review` | `OPEN` | Sprint 1: Initiation & Local-First MVP |
| `#2` | `1.1.2` | [WBS 1.1.2] ci(github): Configure GitHub Actions CI and verify Python 3.11 (uv) + Node 26 (react-force-graph-3d) builds | `Sprint 1` | `3` | `In Review` | `OPEN` | Sprint 1: Initiation & Local-First MVP |
| `#3` | `1.1.3` | [WBS 1.1.3] chore(github): Initialize Milestones, 19 WBS Issues, Branch Protection (PR+CI), and 5-column Projects v2 Board | `Sprint 1` | `2` | `In Progress` | `OPEN` | Sprint 1: Initiation & Local-First MVP |
| `#4` | `1.2.1` | [WBS 1.2.1] feat(backend): Implement FastAPI app skeleton, Pydantic v2 schemas, CORS, and /health endpoint | `Sprint 1` | `3` | `Ready` | `OPEN` | Sprint 1: Initiation & Local-First MVP |
| `#5` | `1.2.2` | [WBS 1.2.2] feat(backend): Implement SQLite store with startup idempotent auto-seed of sample Deep Audits | `Sprint 1` | `3` | `Ready` | `OPEN` | Sprint 1: Initiation & Local-First MVP |
| `#6` | `1.2.3` | [WBS 1.2.3] feat(backend): Implement audit read and API-key-protected publish endpoints (/api/audits) | `Sprint 1` | `2` | `Ready` | `OPEN` | Sprint 1: Initiation & Local-First MVP |
| `#7` | `1.2.4` | [WBS 1.2.4] feat(backend): Implement GitHub REST client, diff filter, 2-level module clusterer, Timeline 2D, and POST /api/preview | `Sprint 1` | `5` | `Ready` | `OPEN` | Sprint 1: Initiation & Local-First MVP |
| `#8` | `1.2.5` | [WBS 1.2.5] test(backend): Add pytest unit/API test suite and pass ruff lint/format with zero errors | `Sprint 1` | `3` | `Ready` | `OPEN` | Sprint 1: Initiation & Local-First MVP |
| `#9` | `1.3.1` | [WBS 1.3.1] feat(frontend): Set up Interstellar Light Minimalism theme, API client, and Minimalist Landing Screen | `Sprint 1` | `3` | `Ready` | `OPEN` | Sprint 1: Initiation & Local-First MVP |
| `#10` | `1.3.2` | [WBS 1.3.2] feat(frontend): Build Clustered 3D Network Canvas (Graph3DCanvas.tsx) with Focus Mode and Reset Camera | `Sprint 1` | `5` | `Ready` | `OPEN` | Sprint 1: Initiation & Local-First MVP |
| `#11` | `1.3.3` | [WBS 1.3.3] feat(frontend): Build Timeline2D, TopBar (/health badge & Live URL input), and read-only SideInspector | `Sprint 1` | `3` | `Ready` | `OPEN` | Sprint 1: Initiation & Local-First MVP |
| `#12` | `1.3.4` | [WBS 1.3.4] test(frontend): Add vitest component tests and pass tsc, eslint, and Vite production build | `Sprint 1` | `2` | `Ready` | `OPEN` | Sprint 1: Initiation & Local-First MVP |
| `#13` | `1.4.1` | [WBS 1.4.1] test(e2e): Verify simultaneous localhost backend/frontend, Live 3D Preview on vku-sprintguard, and E2E Tiers 1-5 | `Sprint 1` | `3` | `Ready` | `OPEN` | Sprint 1: Initiation & Local-First MVP |
| `#14` | `1.1.4` | [WBS 1.1.4] docs(qlda): Capture Sprint 1 board snapshots (Start/Mid/End) and update Risk Register Wave 1 with Sprint 1 actuals | `Sprint 1` | `2` | `Ready` | `OPEN` | Sprint 1: Initiation & Local-First MVP |
| `#15` | `1.5.1` | [WBS 1.5.1] feat(mcp): Build sprintguard-mcp FastMCP server with 6 tools, 5-station State Machine, Evidence Grounding, and HITL [Deferred] | `Sprint 2` | `5` | `Backlog` | `OPEN` | Sprint 2: MCP Harness, Dogfooding & Final Evidence (Deferred) |
| `#16` | `1.5.2` | [WBS 1.5.2] feat(mcp): Author Antigravity SKILL.md, configure mcp_config.json (uv run), and test all 6 MCP tools live [Deferred] | `Sprint 2` | `3` | `Backlog` | `OPEN` | Sprint 2: MCP Harness, Dogfooding & Final Evidence (Deferred) |
| `#17` | `1.6.1` | [WBS 1.6.1] feat(frontend): Add Camera Fly-to, X-Ray signal filter, and Critic/HITL Inspector polish [Deferred] | `Sprint 2` | `3` | `Backlog` | `OPEN` | Sprint 2: MCP Harness, Dogfooding & Final Evidence (Deferred) |
| `#18` | `1.6.2` | [WBS 1.6.2] test(uat): Run Dogfooding audit on vku-sprintguard, execute VKU Peer UAT, and optionally deploy HTTPS if requested [Deferred] | `Sprint 2` | `5` | `Backlog` | `OPEN` | Sprint 2: MCP Harness, Dogfooding & Final Evidence (Deferred) |
| `#19` | `1.1.5` | [WBS 1.1.5] docs(qlda): Finalize 8 Google Drive deliverables (Report, CR-001, Wave 2 Risks, Retros, Slides) and tag v1.0.0 [Deferred] | `Sprint 2` | `5` | `Backlog` | `OPEN` | Sprint 2: MCP Harness, Dogfooding & Final Evidence (Deferred) |

## 4. Story Points Summary

### 4.1 By Sprint / Iteration

| Iteration | Issues | Issue Range | Total Story Points | Done SP | Remaining SP |
| :--- | :---: | :--- | :---: | :---: | :---: |
| `Sprint 1` | `14` | `#1`–`#14` | `42` | `0` | `42` |
| `Sprint 2` *(Deferred)* | `5` | `#15`–`#19` | `21` | `0` | `21` |
| **Total** | **`19`** | **`#1`–`#19`** | **`63`** | **`0`** | **`63`** |

### 4.2 By Initial Status Column

| Status Column | Item Count | Story Points |
| :--- | :---: | :---: |
| `Backlog` | `5` | `21` |
| `Ready` | `11` | `34` |
| `In Progress` | `1` | `2` |
| `In Review` | `2` | `6` |
| `Done` | `0` | `0` |

## 5. Independent Verification Commands

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" auth status
& "C:\Program Files\GitHub CLI\gh.exe" project view 1 --owner NhatCam2006 --format json
& "C:\Program Files\GitHub CLI\gh.exe" project field-list 1 --owner NhatCam2006 --limit 30 --format json
& "C:\Program Files\GitHub CLI\gh.exe" project item-list 1 --owner NhatCam2006 --limit 50 --format json
& "C:\Program Files\GitHub CLI\gh.exe" issue list --repo NhatCam2006/vku-sprintguard --limit 50 --state all --json number,state
```
