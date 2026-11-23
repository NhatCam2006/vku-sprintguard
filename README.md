# VKU SprintGuard

**Decision Support System & Multi-Agent Repository Auditor for Software Project Management (VKU — Pathway 3 & CLO4).**

Instead of relying on rigid 0–100 automated grading, VKU SprintGuard combines deterministic GitHub telemetry with an Antigravity-powered **MCP State-Machine Harness** and an **Interstellar Light Minimalism 3D Dashboard** (`Clustered 3D Network`, `2D Commit Rhythm Timeline`, and `Side Inspector`) to help instructors and project managers inspect project health, uncover risks, and generate evidence-grounded defense questions.

## Core Architecture

- **MCP State-Machine Harness (`mcp_server/`):** 6-tool `FastMCP` server enforcing a 5-stage audit pipeline (`collect_repo` → `detect_context` → `analyze_evidence` → `critic_review` → `publish_audit`) with **Evidence Grounding**, **Pydantic Schema Validation**, and a mandatory **Human-in-the-Loop (HITL)** approval gate.
- **Backend & Core Engine (`backend/`):** Python 3.11 + FastAPI + HTTPX + SQLite (with startup auto-seed for ephemeral free-tier hosting such as Render), supporting both live GitHub 3D previews and published Deep AI Audits.
- **3D Web Dashboard (`frontend/`):** React + TypeScript + Vite + Tailwind CSS + `react-force-graph-3d` on a crisp white-and-monochrome palette (`#FFFFFF` / `#09090B`) using **Montserrat** and **Inter**, with selective amber (`probe`) and red (`risk`) accents.

## Planned Structure

```text
vku-sprintguard/
├── .github/workflows/   # Automated CI checks (lint, unit tests, build)
├── backend/             # FastAPI API, GitHub telemetry engine & SQLite store
├── mcp_server/          # FastMCP 6-tool server & 5-stage audit harness
├── skills/              # Antigravity SKILL.md workflow instructions
├── frontend/            # React 3D Mission Control Web App
└── docs/                # Planning baseline & QLDA project artifacts
```

## Planning & Governance

- Planning & architecture baseline: [docs/planning/VKU-SprintGuard-Blueprint.md](docs/planning/VKU-SprintGuard-Blueprint.md)
- Project decisions & Swarm roster: [docs/planning/PROJECT-DECISIONS.md](docs/planning/PROJECT-DECISIONS.md)
