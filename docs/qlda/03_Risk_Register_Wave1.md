# Risk Register — Wave 1 (Initiation & Sprint 1)

**Project:** VKU SprintGuard (`VKU-SPM-GUARD`)  
**PM / Lead:** Đinh Nhật Cảm (`24Ite019`, `@NhatCam2006`)  
**Milestone Alignment:** Seeded at M1 (Day 1 — Initiation) · Updated with Sprint 1 Actuals at M5 (Day 3 — Week 6 Checkpoint) · Wave 2 due at M7 (Sprint 2 — Week 11 Checkpoint)

---

## Response strategies

| Strategy | Meaning | Example |
|---|---|---|
| **Avoid** | Change the plan to eliminate the risk | Drop a risky feature or deadlock-causing setting from scope |
| **Mitigate** | Reduce probability or impact | Add extra Day-1 build smoke testing for Node 26 + `react-force-graph-3d` |
| **Transfer** | Shift the risk elsewhere | Rely on GitHub REST API / Antigravity MCP Brain instead of self-hosted LLM inference |
| **Accept** | Acknowledge and monitor, do nothing active | A low-probability, low-impact risk monitored during reviews |

---

## Register

*Add rows as you identify risks. Update Status as risks materialize, get resolved, or stay open.*

| Risk | Probability | Impact | Response | Owner | Status |
|---|---|---|---|---|---|
| **R1 — Missing `read:project` / `project` OAuth scope on `gh` CLI:** Survey check `& "C:\Program Files\GitHub CLI\gh.exe" project list --owner NhatCam2006` exited `1` (`missing required scopes [read:project]`), blocking automated GitHub Projects v2 setup. | High | High | **Mitigate:** Gate M2 board creation behind PM Gate 1, prompting Human PM (`Đinh Nhật Cảm`) to run `gh auth refresh -s project,read:project` interactively immediately after reviewing PR #1 (GitHub PR #20). | Human PM (`@NhatCam2006`) / `coordinator` | **Resolved (Gate 1)** — PM ran `gh auth refresh -s project,read:project`; Project `#1` created and all board moves (M2–M5) scripted via `gh project item-edit` |
| **R2 — `gh.exe` absent from default `$env:PATH`:** `gh` v2.105.0 is installed at `C:\Program Files\GitHub CLI\gh.exe`, but bare `gh` commands fail in PowerShell sessions, breaking scripted GitHub automation. | High | Low | **Mitigate:** Standardize all Swarm/PM scripts and runbooks to invoke `& "C:\Program Files\GitHub CLI\gh.exe"` explicitly or prepend `C:\Program Files\GitHub CLI` to `$env:PATH`. | `coordinator` / `architect-mcp` | **Materialized (Day 1)** — Mitigated via explicit path |
| **R3 — Node `v26.13.1` incompatibility with `react-force-graph-3d` / Three.js / Vite:** Bleeding-edge Node 26 runtime and `typescript@7.x` vs `typescript-eslint` peer bounds may cause peer-dependency conflicts, ESM/CJS errors, or Vite production build failures. | Medium | High | **Mitigate:** Execute a Day-1 M1 build-smoke test (`npm install` + `npx tsc --noEmit` + `npm run lint` + `npm run test` + `npm run build` with `react-force-graph-3d` and pinned `typescript@~6.0.3`) before parallel Sprint 1 frontend development; lock working versions in `package-lock.json`. | `frontend-3d` | **Resolved (Sprint 1)** — Node v26.13.1 verified in M1 smoke build (CI run 45138051337) and again in M4 (PR #23: `tsc`/`lint`/`test`/`build` exit 0, CI pass) |
| **R4 — Single-account (`NhatCam2006`) GitHub Branch Protection PR merge deadlock:** Enabling GitHub's *"Require 1 approving review"* prevents `@NhatCam2006` from approving/merging PRs opened under the same account. | High | High | **Avoid:** Configure `main` branch protection with **Require Pull Request (`required_approving_review_count: 0`) + Require GitHub Actions CI status checks PASS** only; enforce independent `qa-docs` Review Comment + PM manual check before PM merge. | `coordinator` / Human PM | **Controlled** — Enforced in Charter §7 & M1 branch protection |
| **R5 — GitHub REST API 60 req/hr unauthenticated rate limit during Live 3D Preview:** Repeated `POST /api/preview` testing or multi-page commit/PR fetching may trigger HTTP `403`/`429` rejections. | Medium | Medium | **Mitigate:** Cap telemetry sampling at max **100 commits + 30 PRs**, support optional `GITHUB_TOKEN` PAT in `.env` (raising quota to 5,000 req/hr), and return structured HTTP `429` error handling to the UI. | `backend-dev` | **Mitigated (M3)** — 20-commit detail-fetch cap + optional `GITHUB_TOKEN`; live `POST /api/preview` on `vku-sprintguard` returned 200 repeatedly in M3 QA and M5 E2E without rate-limit errors |
| **R6 — WebGL / 3D "Hairball Problem" lag on large repositories in `Graph3DCanvas`:** Repositories with hundreds of files/folders degrade 3D readability and frame rate. | Medium | Medium | **Mitigate:** Implement 2-level directory clustering capped at **40 largest modules** (`other/` fallback) in `module_clusterer.py`, paired with Focus Mode dimming (~10%) and `[Reset Camera]`. | `backend-dev` / `frontend-3d` | **Mitigated (M3/M4)** — 40-module cap with `other/` fallback in `module_clusterer.py` + Focus Mode dimming in `Graph3DCanvas` (PR #22, PR #23) |
| **R7 — Accidental commit of gitignored `docs/reference/`, `.env` secrets, or SQLite `.db` binaries to public repo:** Exposing instructor templates or `PUBLISH_API_KEY`/`GITHUB_TOKEN` compromises repo hygiene and security. | Low | High | **Avoid:** Keep `docs/reference/`, `.env`, `.env.*`, and `*.db` in `.gitignore`, commit `.env.example` only, and verify `git status --short`/PR diff during every `qa-docs` PR review (Charter §12.2 DoD #5). | `architect-mcp` / `qa-docs` | **Open** — Monitored on every PR |
| **R8 — Evidence Package audit gap (single board screenshot or static Risk Register):** Submitting only a final board screenshot or an unchanging Risk Register fails `EvidencePackageChecklist.md` and `MilestoneRubric.md`. | Medium | High | **Mitigate:** Capture GitHub Projects v2 board snapshots at M2 (Start), M3/M4 (Mid), and M5 (End) into `docs/qlda/board_snapshots/`; mandate M5 update of `03_Risk_Register_Wave1.md` with actual Sprint 1 outcomes. | `qa-docs` / `coordinator` | **Resolved (M5)** — 4 snapshots saved (`sprint1_start`, `sprint1_day1_eod`, `sprint1_mid_m3`, `sprint1_end_review`) + `sprint1_summary.md`; this register updated with actuals |
| **R9 — Scope creep from Sprint 2 (`mcp_server/`, `SKILL.md`, cloud deploy) leaking into Sprint 1:** Premature MCP or Vercel/Render setup threatens Day-3 Local-First stability and violates stop-gate boundaries. | Medium | High | **Avoid:** Lock Charter §5.2 exclusions and separate Sprint 2 Issues into the deferred `Sprint 2` Milestone; enforce PM Gate 2 stop checkpoint immediately after M5 Localhost E2E acceptance. | `coordinator` / Human PM | **Controlled** — Enforced via M1 WBS |
| **R10 — `ruff` CLI absent from global Windows `PATH` & UTF-8 BOM TOML failure:** Survey confirmed `ruff` is not installed globally and Windows PowerShell `Set-Content -Encoding UTF8` inserts a BOM that breaks `pyproject.toml` parsing. | High | Low | **Mitigate:** Declare `ruff` and `pytest` as `uv` dev dependencies in `backend/pyproject.toml`, invoke exclusively via `uv run ruff` / `uv run pytest`, and write all source/TOML files in UTF-8 without BOM. | `architect-mcp` / `backend-dev` | **Materialized (Day 1)** — Mitigated in M1 setup |
| **R11 — Multi-agent model quota exhaustion (new, observed Day 1):** Running every swarm agent on a single model pool (`Gemini 4 Neon`) returned `HTTP 429` quota errors on Day 1, which stalled parallel agent work. | High | High | **Mitigate:** Moved to Native Swarm with a 3-pool model split: `Neon` for UI (`frontend-3d`), `Argon` for backend (`backend-dev`), `Opus` for QA/docs (`qa-docs`). Agents also wait on the board without polling, to save tokens. | `coordinator` | **Materialized (Day 1)**, then **Mitigated (Days 2–3)**: M3 and M4 ran without further 429s. |

---

## Week 6 checklist — first real revision

- [x] Reviewed Sprint 1: which risks *actually* materialized (not what was imagined in Week 2)?
- [x] Recorded what was done about each — did the response strategy work?
- [x] Added any new risks only visible after running one real sprint

### Sprint 1 Revision Summary

- **Materialized:** R1 (missing `gh` project scope), R2 (`gh` not on PATH), R10 (`ruff` missing and BOM-encoded TOML), and the new R11 (model quota `HTTP 429`). All four responses worked: R1 was resolved at Gate 1, R2 and R10 were mitigated during M1 setup, and R11 was mitigated by the 3-pool model split.
- **Mitigated before they hit:** R3 (Node 26 builds passed in M1 and M4), R5 (20-commit cap plus `GITHUB_TOKEN`), R6 (40-module cap plus Focus Mode), R8 (4 board snapshots saved).
- **Still controlled/monitored:** R4 (branch protection set to 0 approvals plus CI), R7 (no secrets or `.db` files in any PR diff), R9 (Sprint 2 `#15`–`#19` still in Backlog).
- **Outcome:** 42/42 SP implemented and QA-verified. 24 SP are Done; 18 SP are In Review and wait on the PM Gate 2 merge.

⚠️ A register with only hypothetical, generic risks ("scope creep," "team conflict") and nothing specific to what actually happened in Sprint 1 does not satisfy the Week 6 milestone.
