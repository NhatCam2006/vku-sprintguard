---
name: sprintguard-auditor
description: Conduct evidence-grounded, 5-station software engineering audits of student or team GitHub repositories using the sprintguard-mcp server, ending with a mandatory Human-in-the-Loop (HITL) approval gate before publishing to VKU SprintGuard.
---

# VKU SprintGuard Auditor Skill

## Core Philosophy: Decision Support, Never Automated Grading

VKU SprintGuard is a **Decision Support System** for instructors and project managers — **never** an automated 0–100 grader or cheating detector.

- **Never** assign numerical grades (e.g., `85/100`), pass/fail verdicts, or accusations of plagiarism/slacking.
- **Always** frame findings as objective engineering signals (`healthy`, `probe`, `risk`) and actionable oral-defense interview questions grounded in real repository history.
- **Always** respect repository context: do not flag single-author Bus Factor on a `solo` project, and distinguish lockfile/generated churn from genuine code changes.

## Mandatory 5-Station Audit Workflow

You MUST execute the `sprintguard-mcp` tools in strict order. The harness enforces the state machine and will reject out-of-order calls.

### Station 1 — Telemetry Collection (`start_repo_audit`)
- Call `start_repo_audit(repo_url)` with the target GitHub repository URL.
- Inspect the returned `session_id`, `authors`, `modules_count`, `node_ids_sample`, `timeline_2d`, and `valid_refs_sample`.
- State becomes `COLLECTED`.

### Station 2 — Context Calibration (`submit_context`)
- Classify `repo_type` as `"solo"`, `"student_team"`, or `"open_source"` with clear `context_reasoning`.
- Infer realistic `member_roles` (e.g., `"Backend Lead"`, `"Frontend Dev"`, `"Docs & QA"`) from commit patterns and module ownership.
- Call `submit_context(session_id, repo_type, context_reasoning, member_roles)`.
- State becomes `CONTEXT_SET`.

### Station 3 — Evidence Inspection & Findings (`inspect_evidence` -> `submit_findings`)
- Before flagging any `probe` or `risk` signal, use `inspect_evidence(session_id, target_type, target_id)` on suspicious commits (`commit:<sha>`) or PRs (`PR#<num>`) to verify actual source diffs (lockfiles and build artifacts are automatically filtered out).
- **Strict Evidence Grounding**: Every `probe` or `risk` signal MUST cite a real `evidence_ref` from `valid_refs` (such as `commit:<7-char-sha>` or `PR#<number>`) and a real `node_id` from the session graph. Fabricated references are rejected by the harness.
- Call `submit_findings(session_id, signals)`.
- State becomes `FINDINGS_SUBMITTED`.

### Station 4 — Adversarial Self-Critique (`submit_critic_review`)
- Switch into a skeptical reviewer mindset and challenge your own findings:
  - Could a large commit be a legitimate initial scaffold, asset import, or branch merge?
  - Could an apparent silo be a deliberate Frontend/Backend split in a `student_team`?
  - Downgrade false positives (`new_level="healthy"` or `drop=True`) and attach concise `critic_note` explanations to remaining signals.
- Call `submit_critic_review(session_id, adjustments, draft_summary)`.
- State becomes `AWAITING_HUMAN_APPROVAL`.

### Mandatory Human-in-the-Loop (HITL) Pause
- **STOP immediately after `submit_critic_review`.**
- Present `draft_summary`, the active signals with their `evidence_ref` and `critic_note`, and proposed oral-defense questions to the Human PM/Instructor.
- Ask for explicit approval and any `human_notes` (e.g., "Student B handled Figma and sprint planning off-Git").
- **NEVER** call `publish_audit` with `human_approved=True` until the human explicitly confirms.

### Station 5 — Publish Approved Report (`publish_audit`)
- Incorporate the human's `human_notes` and craft grounded `interview_questions` (each citing a real `evidence_ref` from the session).
- Call `publish_audit(session_id, human_approved=True, human_notes, interview_questions, final_summary)`.
- Return the published `audit_id` and `dashboard_url` to the user.
