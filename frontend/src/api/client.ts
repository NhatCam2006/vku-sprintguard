import type {
  AuditListItem,
  AuditListResponse,
  AuditReport,
  HealthResponse,
} from '../types/audit';

const rawBaseUrl = import.meta.env.VITE_API_BASE_URL as string | undefined;
export const API_BASE_URL = (rawBaseUrl?.trim() || 'http://localhost:8000').replace(/\/+$/, '');

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

async function parseErrorDetail(response: Response): Promise<string> {
  try {
    const data: unknown = await response.json();
    if (
      data &&
      typeof data === 'object' &&
      'detail' in data &&
      typeof (data as { detail: unknown }).detail === 'string'
    ) {
      return (data as { detail: string }).detail;
    }
  } catch {
    // Fall back to HTTP status text when response body is not JSON.
  }
  return `Request failed with status ${response.status}`;
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      Accept: 'application/json',
      ...(init?.body ? { 'Content-Type': 'application/json' } : {}),
      ...init?.headers,
    },
  });

  if (!response.ok) {
    const detail = await parseErrorDetail(response);
    throw new ApiError(detail, response.status);
  }

  return (await response.json()) as T;
}

export async function fetchHealth(): Promise<HealthResponse> {
  return requestJson<HealthResponse>('/health');
}

export async function fetchAudits(): Promise<AuditListItem[]> {
  const payload = await requestJson<AuditListResponse>('/api/audits');
  return payload.audits;
}

export async function fetchAuditById(auditId: string): Promise<AuditReport> {
  return requestJson<AuditReport>(`/api/audits/${encodeURIComponent(auditId)}`);
}

export async function runLivePreview(repoUrl: string): Promise<AuditReport> {
  return requestJson<AuditReport>('/api/preview', {
    method: 'POST',
    body: JSON.stringify({ repo_url: repoUrl.trim() }),
  });
}

export const FALLBACK_AUDIT_REPORT: AuditReport = {
  audit_id: 'aud_sample_student_team',
  created_at: '2026-04-12T08:30:00Z',
  mode: 'deep_ai_audit',
  repo: {
    name: 'vku-sprint-demo/campus-nav',
    url: 'https://github.com/NhatCam2006/vku-sprintguard',
    context: 'student_team',
    context_reasoning:
      '4 active student contributors across 6 sprint weeks with uneven ownership around checkout/auth modules.',
  },
  summary: {
    overview:
      'Delivery cadence remained steady during Weeks 11–14 before a sharp Week 15 integration surge concentrated in backend/auth and frontend/map.',
    human_notes:
      'Review Week 15 merge ownership with Minh & Linh during Sprint Defense. Confirm test coverage on auth token refresh.',
  },
  graph_3d: {
    nodes: [
      {
        id: 'author:minh',
        type: 'author',
        label: 'Minh Nguyen',
        role: 'Backend Lead',
        size: 16,
        churn: 1420,
        status: 'healthy',
        description:
          'Phụ trách chính kiến trúc xác thực JWT, luồng làm mới token và tích hợp API bản đồ phía backend.',
      },
      {
        id: 'author:linh',
        type: 'author',
        label: 'Linh Tran',
        role: 'Frontend Engineer',
        size: 13,
        churn: 980,
        status: 'probe',
        description:
          'Xây dựng giao diện bản đồ điều hướng khuôn viên, quản lý trạng thái phiên người dùng và tối ưu hiển thị.',
      },
      {
        id: 'author:khoa',
        type: 'author',
        label: 'Khoa Le',
        role: 'QA & Data',
        size: 8,
        churn: 240,
        status: 'healthy',
        description:
          'Viết kịch bản kiểm thử tự động, chuẩn hóa dữ liệu địa điểm mẫu và cập nhật tài liệu vận hành sprint.',
      },
      {
        id: 'mod:backend/auth',
        type: 'module',
        label: 'backend/auth',
        role: null,
        size: 15,
        churn: 1120,
        status: 'risk',
        description:
          'Cụm xử lý đăng nhập, cấp phát và làm mới JWT token cùng middleware bảo vệ các endpoint nội bộ.',
        key_files: [
          'backend/auth/jwt_service.py',
          'backend/auth/token_refresh.py',
          'backend/auth/middleware.py',
        ],
      },
      {
        id: 'mod:frontend/map',
        type: 'module',
        label: 'frontend/map',
        role: null,
        size: 12,
        churn: 740,
        status: 'probe',
        description:
          'Thành phần bản đồ tương tác hiển thị tòa nhà VKU, dẫn đường thời gian thực và đồng bộ trạng thái phiên.',
        key_files: [
          'frontend/map/CampusMapView.tsx',
          'frontend/map/useRouteState.ts',
          'frontend/map/sessionSync.ts',
        ],
      },
      {
        id: 'mod:docs/tests',
        type: 'module',
        label: 'docs/tests',
        role: null,
        size: 7,
        churn: 210,
        status: 'healthy',
        description:
          'Bộ kiểm thử tích hợp luồng bản đồ, dữ liệu seed kiểm thử và ghi chú nghiệm thu sprint.',
        key_files: [
          'docs/tests/auth_flow.spec.ts',
          'docs/tests/campus_seed.json',
        ],
      },
    ],
    edges: [
      { source: 'author:minh', target: 'mod:backend/auth', weight: 14 },
      { source: 'author:minh', target: 'mod:frontend/map', weight: 4 },
      { source: 'author:linh', target: 'mod:frontend/map', weight: 11 },
      { source: 'author:khoa', target: 'mod:docs/tests', weight: 6 },
    ],
  },
  timeline_2d: [
    { week: '2026-W11', commits: 9, additions: 310, deletions: 45, anomaly: false },
    { week: '2026-W12', commits: 12, additions: 420, deletions: 90, anomaly: false },
    { week: '2026-W13', commits: 10, additions: 280, deletions: 110, anomaly: false },
    { week: '2026-W14', commits: 14, additions: 510, deletions: 140, anomaly: false },
    { week: '2026-W15', commits: 31, additions: 1840, deletions: 620, anomaly: true },
  ],
  signals: [
    {
      id: 'sig-01',
      node_id: 'mod:backend/auth',
      level: 'risk',
      title: 'Single-Author Bus Factor on Auth Core',
      description:
        '100% of commits in backend/auth were authored by Minh Nguyen with a late Week 15 refactor.',
      evidence_ref: 'commit:a1b2c3d',
      critic_note:
        'Single ownership is acceptable if peer-reviewed; verify whether Linh or Khoa reviewed the token flow.',
    },
    {
      id: 'sig-02',
      node_id: 'mod:frontend/map',
      level: 'probe',
      title: 'High Late-Sprint Churn in Map View',
      description:
        'frontend/map saw +610/-290 lines changed within 48 hours before demo freeze.',
      evidence_ref: 'PR#14',
      critic_note:
        'Could be legitimate UI polish; probe how state updates and edge cases were validated.',
    },
  ],
  interview_questions: [
    {
      author_id: 'author:minh',
      author_name: 'Minh Nguyen',
      question:
        'Walk through the Week 15 auth token refresh rewrite — what edge case triggered the 620-line deletion?',
      evidence_ref: 'commit:a1b2c3d',
    },
    {
      author_id: 'author:linh',
      author_name: 'Linh Tran',
      question:
        'How does frontend/map synchronize state with backend/auth when a session expires mid-navigation?',
      evidence_ref: 'PR#14',
    },
  ],
  commit_highlights: [
    {
      ref: 'commit:a1b2c3d',
      url: 'https://github.com/NhatCam2006/vku-sprintguard/commit/a1b2c3d',
      author: 'Minh Nguyen',
      date: '2026-04-11',
      title: 'refactor(auth): rewrite JWT refresh rotation and revoke stale sessions',
      diff_summary:
        'Thay đổi lớn ở tuần W15 (+480/-620 dòng), hợp nhất kiểm tra token hết hạn vào middleware dùng chung.',
      files_changed: [
        'backend/auth/jwt_service.py',
        'backend/auth/token_refresh.py',
        'backend/auth/middleware.py',
      ],
    },
    {
      ref: 'PR#14',
      url: 'https://github.com/NhatCam2006/vku-sprintguard/pull/14',
      author: 'Linh Tran',
      date: '2026-04-12',
      title: 'feat(map): sync campus navigation route state on session refresh',
      diff_summary:
        'Bổ sung cơ chế giữ nguyên tuyến đường đang xem khi token hết hạn giữa phiên điều hướng (+610/-290 dòng).',
      files_changed: [
        'frontend/map/CampusMapView.tsx',
        'frontend/map/useRouteState.ts',
        'frontend/map/sessionSync.ts',
      ],
    },
    {
      ref: 'commit:7e8f901',
      url: 'https://github.com/NhatCam2006/vku-sprintguard/commit/7e8f901',
      author: 'Khoa Le',
      date: '2026-04-10',
      title: 'test(e2e): add auth token expiry regression suite for campus map',
      diff_summary:
        'Thêm bộ kiểm thử hồi quy xác minh luồng hết phiên và dữ liệu seed cho 12 tòa nhà mẫu.',
      files_changed: ['docs/tests/auth_flow.spec.ts', 'docs/tests/campus_seed.json'],
    },
  ],
};
