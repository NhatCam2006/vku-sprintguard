from typing import Literal

from pydantic import BaseModel, Field

RepoContext = Literal["solo", "student_team", "open_source"]
SignalLevel = Literal["healthy", "probe", "risk"]
AuditMode = Literal["deep_ai_audit", "live_preview"]
NodeType = Literal["author", "module"]


class RepoInfo(BaseModel):
    name: str
    url: str
    context: RepoContext
    context_reasoning: str


class AuditSummary(BaseModel):
    overview: str
    human_notes: str = ""


class GraphNode(BaseModel):
    id: str
    type: NodeType
    label: str
    role: str | None = None
    size: int = Field(ge=0)
    churn: int | None = None
    status: SignalLevel = "healthy"


class GraphEdge(BaseModel):
    source: str
    target: str
    weight: int = Field(ge=1)


class Graph3D(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]


class TimelineWeek(BaseModel):
    week: str
    commits: int = Field(ge=0)
    additions: int = Field(ge=0)
    deletions: int = Field(ge=0)
    anomaly: bool = False


class AuditSignal(BaseModel):
    id: str
    node_id: str
    level: SignalLevel
    title: str
    description: str
    evidence_ref: str
    critic_note: str = ""


class InterviewQuestion(BaseModel):
    author_id: str
    author_name: str
    question: str
    evidence_ref: str


class AuditReport(BaseModel):
    audit_id: str
    created_at: str
    mode: AuditMode
    repo: RepoInfo
    summary: AuditSummary
    graph_3d: Graph3D
    timeline_2d: list[TimelineWeek]
    signals: list[AuditSignal] = Field(default_factory=list)
    interview_questions: list[InterviewQuestion] = Field(default_factory=list)


class AuditListItem(BaseModel):
    audit_id: str
    created_at: str
    mode: AuditMode
    repo: RepoInfo
    summary: AuditSummary
    node_count: int
    signal_count: int


class AuditListResponse(BaseModel):
    audits: list[AuditListItem]


class AuditPublishResponse(BaseModel):
    audit_id: str
    status: Literal["stored"] = "stored"


class PreviewRequest(BaseModel):
    repo_url: str


class HealthResponse(BaseModel):
    status: str = "ok"
    database: str = "ok"
    seeded_audits: int
