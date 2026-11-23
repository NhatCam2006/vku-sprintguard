# Sprint 1 Summary — Velocity & Burndown

**Project:** VKU SprintGuard · GitHub Projects v2 `#1` (`NhatCam2006`) · Sprint 1 scope: Issues `#1`–`#14` = **42 SP**

## Burndown across snapshots

| Snapshot | Source | Done (SP) | In Review (SP) | Remaining Sprint 1 (SP) | Status counts (Sprint 1 + 2) |
|---|---|---:|---:|---:|---|
| Start (M2) | `sprint1_start.json` | 0 | — | 42 | Backlog 5 · Ready 11 · In Progress 1 · In Review 2 · Done 0 |
| Day 1 EOD (M2) | `sprint1_day1_eod.json` | 6 | 0 | 36 | Backlog 5 · Ready 11 · In Progress 1 · Done 2 (`#1`, `#2`) |
| Mid (M3 merged) | `sprint1_mid_m3.json` | 24 | 0 | 18 | Backlog 5 · Ready 6 (`#9`–`#14`) · Done 8 (`#1`–`#8`) |
| End Review (M5) | `sprint1_end_review.json` | 24 | 18 | 18 (pending PM Gate 2 merge) | Backlog 5 · In Review 6 (`#9`–`#14`) · Done 8 |

## Velocity

- **Delivered & merged:** 24 SP (`#1`–`#8`: setup, board, backend core M3).
- **Delivered, awaiting PM Gate 2:** 18 SP (`#9`–`#13` frontend M4 + localhost E2E in PR #23; `#14` closure docs in PR #24).
- **Committed vs. completed:** 42 / 42 SP implemented and QA-verified; 24 SP counted Done until PR #23/#24 merge.
- **Sprint 2 (`#15`–`#19`, 21 SP):** untouched in Backlog (no scope leak).

## M5 verification evidence

- PR #23: `tsc`, `eslint`, `vitest` (4/4), and `vite build` all exited 0. The backend on :8000 and Vite on :5173 ran at the same time. CORS from `http://localhost:5173` was allowed, and Live Preview of `vku-sprintguard` returned 10 nodes, 9 edges and 1 timeline week. CI passed on backend and frontend.
