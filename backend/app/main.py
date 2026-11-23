from fastapi import FastAPI

app = FastAPI(
    title="VKU SprintGuard API",
    version="0.1.0",
    description="Decision Support System for Auditing Student Software Projects",
)


@app.get("/health")
def health_check() -> dict[str, str | int]:
    return {"status": "ok", "database": "ok", "seeded_audits": 0}
