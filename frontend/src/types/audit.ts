export type AuditMode = 'deep_ai_audit' | 'live_preview';

export type RepoContext = 'solo' | 'student_team' | 'open_source';

export type NodeStatus = 'healthy' | 'probe' | 'risk';

export type GraphNodeType = 'author' | 'module';

export interface HealthResponse {
  status: string;
  database: string;
  seeded_audits: number;
}

export interface RepoMetadata {
  name: string;
  url: string;
  context: RepoContext;
  context_reasoning: string;
}

export interface AuditSummary {
  overview: string;
  human_notes: string;
}

export interface AuditListItem {
  audit_id: string;
  created_at: string;
  mode: AuditMode;
  repo: RepoMetadata;
  summary: AuditSummary;
  node_count: number;
  signal_count: number;
}

export interface AuditListResponse {
  audits: AuditListItem[];
}

export interface GraphNode {
  id: string;
  type: GraphNodeType;
  label: string;
  role?: string | null;
  size: number;
  churn?: number | null;
  status: NodeStatus;
  description?: string;
  key_files?: string[];
}

export interface GraphEdge {
  source: string;
  target: string;
  weight: number;
}

export interface Graph3DData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface TimelineWeek {
  week: string;
  commits: number;
  additions: number;
  deletions: number;
  anomaly: boolean;
}

export interface AuditSignal {
  id: string;
  node_id: string;
  level: NodeStatus;
  title: string;
  description: string;
  evidence_ref: string;
  critic_note: string;
}

export interface InterviewQuestion {
  author_id: string;
  author_name: string;
  question: string;
  evidence_ref: string;
}

export interface CommitHighlight {
  ref: string;
  url: string;
  author: string;
  date?: string;
  title: string;
  diff_summary: string;
  files_changed?: string[];
}

export interface AuditReport {
  audit_id: string;
  created_at: string;
  mode: AuditMode;
  repo: RepoMetadata;
  summary: AuditSummary;
  graph_3d: Graph3DData;
  timeline_2d: TimelineWeek[];
  signals: AuditSignal[];
  interview_questions: InterviewQuestion[];
  commit_highlights?: CommitHighlight[];
}
