import hmac
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.core.github_client import (
    GitHubRateLimitError,
    GitHubUpstreamError,
    RepoNotFoundError,
    fetch_repo_telemetry,
    parse_github_repo_url,
)
from app.core.module_clusterer import build_preview_audit
from app.core.schemas import (
    AuditListResponse,
    AuditPublishResponse,
    AuditReport,
    HealthResponse,
    PreviewRequest,
)
from app.db.sqlite_store import SQLiteStore
from app.seed.sample_audits import get_sample_audits


def get_store() -> SQLiteStore:
    """Instantiate SQLiteStore with current SPRINTGUARD_DB_PATH environment variable."""
    return SQLiteStore(os.getenv("SPRINTGUARD_DB_PATH", "data/sprintguard.db"))


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    store = get_store()
    store.seed_defaults_if_empty(get_sample_audits())
    yield


app = FastAPI(
    title="VKU SprintGuard API",
    version="0.1.0",
    description="Decision Support System for Auditing Student Software Projects",
    lifespan=lifespan,
)

raw_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
)
cors_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    store = get_store()
    count = store.seed_defaults_if_empty(get_sample_audits())
    return HealthResponse(status="ok", database="ok", seeded_audits=count)


@app.get("/api/audits", response_model=AuditListResponse)
def list_audits() -> AuditListResponse:
    store = get_store()
    store.seed_defaults_if_empty(get_sample_audits())
    return AuditListResponse(audits=store.list_audits())


@app.get("/api/audits/{audit_id}", response_model=AuditReport)
def get_audit_detail(audit_id: str) -> AuditReport:
    store = get_store()
    store.seed_defaults_if_empty(get_sample_audits())
    report = store.get_audit(audit_id)
    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Audit report '{audit_id}' not found.",
        )
    return report


@app.post(
    "/api/audits",
    response_model=AuditPublishResponse,
    status_code=status.HTTP_201_CREATED,
)
def publish_audit(
    report: AuditReport,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> AuditPublishResponse:
    expected_key = os.getenv("PUBLISH_API_KEY", "").strip()
    if not expected_key or not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or unconfigured X-API-Key header.",
        )
    if not hmac.compare_digest(x_api_key.strip(), expected_key):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid X-API-Key header.",
        )

    store = get_store()
    store.upsert_audit(report)
    return AuditPublishResponse(audit_id=report.audit_id, status="stored")


@app.post("/api/preview", response_model=AuditReport)
def create_live_preview(payload: PreviewRequest) -> AuditReport:
    try:
        owner, repo_name = parse_github_repo_url(payload.repo_url)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    canonical_url = f"https://github.com/{owner}/{repo_name}"
    try:
        telemetry = fetch_repo_telemetry(owner, repo_name)
    except RepoNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except GitHubRateLimitError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
        ) from exc
    except GitHubUpstreamError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    return build_preview_audit(
        owner=owner,
        repo_name=repo_name,
        repo_url=canonical_url,
        commits=telemetry.get("commits", []),
        prs=telemetry.get("prs", []),
    )
