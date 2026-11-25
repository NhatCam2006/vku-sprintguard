import { forwardRef, useImperativeHandle } from 'react';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import App from '../App';
import { FALLBACK_AUDIT_REPORT } from '../api/client';
import type { AuditListItem, AuditReport, HealthResponse } from '../types/audit';

const zoomToFitMock = vi.fn();
const cameraPositionMock = vi.fn();

vi.mock('react-force-graph-3d', () => {
  interface MockProps {
    graphData: { nodes: Array<{ id: string }>; links: Array<{ source: string; target: string }> };
    nodeColor?: (node: object) => string;
    linkColor?: (link: object) => string;
    onNodeClick?: (node: object) => void;
  }

  const MockForceGraph3D = forwardRef((props: MockProps, ref) => {
    useImperativeHandle(ref, () => ({
      zoomToFit: zoomToFitMock,
      cameraPosition: cameraPositionMock,
    }));

    const firstNode = props.graphData.nodes[0];
    const lastNode = props.graphData.nodes[props.graphData.nodes.length - 1];
    const firstNodeColor = firstNode && props.nodeColor ? props.nodeColor(firstNode) : '';
    const lastNodeColor = lastNode && props.nodeColor ? props.nodeColor(lastNode) : '';

    return (
      <div
        data-testid="mock-force-graph-3d"
        data-node-count={props.graphData.nodes.length}
        data-link-count={props.graphData.links.length}
        data-first-node-color={firstNodeColor}
        data-last-node-color={lastNodeColor}
      >
        {props.graphData.nodes.map((node) => (
          <button
            key={node.id}
            type="button"
            data-testid={`mock-node-${node.id}`}
            onClick={() => props.onNodeClick?.(node)}
          >
            {node.id}
          </button>
        ))}
      </div>
    );
  });

  MockForceGraph3D.displayName = 'MockForceGraph3D';
  return { default: MockForceGraph3D };
});

const MOCK_HEALTH: HealthResponse = {
  status: 'ok',
  database: 'ok',
  seeded_audits: 3,
};

const MOCK_AUDITS: AuditListItem[] = [
  {
    audit_id: 'aud_sample_student_team',
    created_at: '2026-04-12T08:30:00Z',
    mode: 'deep_ai_audit',
    repo: FALLBACK_AUDIT_REPORT.repo,
    summary: FALLBACK_AUDIT_REPORT.summary,
    node_count: FALLBACK_AUDIT_REPORT.graph_3d.nodes.length,
    signal_count: FALLBACK_AUDIT_REPORT.signals.length,
  },
  {
    audit_id: 'aud_sample_solo',
    created_at: '2026-04-11T08:30:00Z',
    mode: 'deep_ai_audit',
    repo: {
      name: 'NhatCam2006/solo-capstone',
      url: 'https://github.com/NhatCam2006/solo-capstone',
      context: 'solo',
      context_reasoning: 'Single maintainer with steady commits.',
    },
    summary: {
      overview: 'Consistent solo cadence across 4 weeks.',
      human_notes: 'No bus-factor warning needed in solo mode.',
    },
    node_count: 4,
    signal_count: 1,
  },
  {
    audit_id: 'aud_sample_open_source',
    created_at: '2026-04-10T08:30:00Z',
    mode: 'deep_ai_audit',
    repo: {
      name: 'oss-org/graph-engine',
      url: 'https://github.com/oss-org/graph-engine',
      context: 'open_source',
      context_reasoning: 'Distributed maintainers and PR contributors.',
    },
    summary: {
      overview: 'Healthy review dispersion across core modules.',
      human_notes: 'Review release branch churn.',
    },
    node_count: 9,
    signal_count: 2,
  },
];

const MOCK_LIVE_PREVIEW_REPORT: AuditReport = {
  audit_id: 'live_preview_001',
  created_at: '2026-04-14T10:00:00Z',
  mode: 'live_preview',
  repo: {
    name: 'NhatCam2006/vku-sprintguard',
    url: 'https://github.com/NhatCam2006/vku-sprintguard',
    context: 'student_team',
    context_reasoning: 'Computed from live GitHub commit history.',
  },
  summary: {
    overview: 'Live 3D topology preview computed from recent commits.',
    human_notes: '',
  },
  graph_3d: {
    nodes: [
      {
        id: 'author:NhatCam2006',
        type: 'author',
        label: 'NhatCam2006',
        role: 'Maintainer',
        size: 12,
        churn: 620,
        status: 'healthy',
      },
      {
        id: 'mod:frontend/src',
        type: 'module',
        label: 'frontend/src',
        role: null,
        size: 10,
        churn: 480,
        status: 'probe',
      },
    ],
    edges: [{ source: 'author:NhatCam2006', target: 'mod:frontend/src', weight: 8 }],
  },
  timeline_2d: [
    { week: '2026-W15', commits: 16, additions: 740, deletions: 120, anomaly: true },
  ],
  signals: [],
  interview_questions: [],
};

function makeJsonResponse(body: unknown, status = 200): Response {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
  } as Response;
}

describe('VKU SprintGuard Mission Control', () => {
  beforeEach(() => {
    zoomToFitMock.mockClear();
    cameraPositionMock.mockClear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  function mockOnlineFetch() {
    return vi.spyOn(globalThis, 'fetch').mockImplementation(async (input, init) => {
      const url = typeof input === 'string' ? input : input.toString();
      if (url.endsWith('/health')) {
        return makeJsonResponse(MOCK_HEALTH);
      }
      if (url.endsWith('/api/audits')) {
        return makeJsonResponse({ audits: MOCK_AUDITS });
      }
      if (url.includes('/api/audits/aud_sample_student_team')) {
        return makeJsonResponse(FALLBACK_AUDIT_REPORT);
      }
      if (url.endsWith('/api/preview') && init?.method === 'POST') {
        const parsed = JSON.parse(String(init.body)) as { repo_url: string };
        if (parsed.repo_url.includes('invalid-repo')) {
          return makeJsonResponse({ detail: 'Repository not found on GitHub.' }, 404);
        }
        return makeJsonResponse(MOCK_LIVE_PREVIEW_REPORT);
      }
      return makeJsonResponse({ detail: 'Not found' }, 404);
    });
  }

  it('renders minimalist Landing screen with seeded audit cards and Live 3D Preview form', async () => {
    mockOnlineFetch();
    render(<App />);

    expect(screen.getByRole('heading', { name: /VKU SPRINTGUARD/i })).toBeInTheDocument();
    expect(screen.getByText(/not automated 0–100 grading/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByTestId('landing-health-pill')).toHaveTextContent('ONLINE · 3 SEEDED');
    });

    expect(screen.getByTestId('seeded-card-aud_sample_student_team')).toBeInTheDocument();
    expect(screen.getByTestId('seeded-card-aud_sample_solo')).toBeInTheDocument();
    expect(screen.getByTestId('seeded-card-aud_sample_open_source')).toBeInTheDocument();

    const quickFill = screen.getByRole('button', {
      name: 'https://github.com/NhatCam2006/vku-sprintguard',
    });
    fireEvent.click(quickFill);
    expect(screen.getByLabelText(/GitHub repository URL/i)).toHaveValue(
      'https://github.com/NhatCam2006/vku-sprintguard',
    );
  });

  it('opens a seeded audit in Mission Control with 3D Graph, Timeline anomaly, SideInspector tabs, and Focus Mode', async () => {
    mockOnlineFetch();
    render(<App />);

    const studentCard = await screen.findByTestId('seeded-card-aud_sample_student_team');
    fireEvent.click(within(studentCard).getByRole('button', { name: /Open 3D Mission Control/i }));

    await waitFor(() => {
      expect(screen.getByTestId('graph-wrapper')).toBeInTheDocument();
    });

    // TopBar & 3D graph counts
    expect(screen.getByText('DEEP AI AUDIT')).toBeInTheDocument();
    expect(screen.getByTestId('topbar-health-pill')).toHaveTextContent('ONLINE · 3 SEEDED');
    const mockGraph = screen.getByTestId('mock-force-graph-3d');
    expect(mockGraph).toHaveAttribute('data-node-count', '6');
    expect(mockGraph).toHaveAttribute('data-link-count', '4');

    // Timeline2D anomaly marker
    const anomalyWeek = screen.getByTestId('timeline-week-2026-W15');
    expect(anomalyWeek).toHaveAttribute('data-anomaly', 'true');
    expect(within(anomalyWeek).getByText('ANOMALY')).toBeInTheDocument();

    // SideInspector: Overview -> Nodes & Signals -> click signal -> Interview Q&A
    expect(screen.getByText(/PM Human Notes/i)).toBeInTheDocument();

    fireEvent.click(screen.getByRole('tab', { name: /Nodes & Signals/i }));
    fireEvent.click(screen.getByTestId('signal-item-sig-01'));
    expect(screen.getByTestId('selected-node-card')).toHaveTextContent('backend/auth');

    fireEvent.click(screen.getByRole('tab', { name: /Interview Q&A/i }));
    expect(screen.getByText(/Walk through the Week 15 auth token refresh rewrite/i)).toBeInTheDocument();

    // Focus Mode via Filter by Member chip dims unrelated nodes (docs/tests is last node, unconnected to Minh)
    fireEvent.click(screen.getByTestId('author-chip-author:minh'));
    expect(screen.getByTestId('graph-wrapper')).toHaveAttribute('data-focus-author', 'author:minh');
    expect(screen.getByTestId('focus-mode-indicator')).toBeInTheDocument();
    expect(screen.getByTestId('mock-force-graph-3d')).toHaveAttribute(
      'data-last-node-color',
      'rgba(212,212,216,0.12)',
    );

    // Reset Camera clears Focus Mode and triggers zoomToFit(400)
    fireEvent.click(screen.getByRole('button', { name: /Reset Camera/i }));
    expect(screen.getByTestId('graph-wrapper')).toHaveAttribute('data-focus-author', '');
    expect(zoomToFitMock).toHaveBeenCalledWith(400);
  });

  it('submits Live 3D Preview and displays inline FastAPI error details on failure', async () => {
    mockOnlineFetch();
    render(<App />);

    await screen.findByTestId('seeded-card-aud_sample_student_team');

    const input = screen.getByLabelText(/GitHub repository URL/i);
    fireEvent.change(input, { target: { value: 'https://github.com/org/invalid-repo' } });
    fireEvent.click(screen.getByRole('button', { name: /Launch Live 3D Preview/i }));

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent('Repository not found on GitHub.');
    });

    fireEvent.change(input, {
      target: { value: 'https://github.com/NhatCam2006/vku-sprintguard' },
    });
    fireEvent.click(screen.getByRole('button', { name: /Launch Live 3D Preview/i }));

    await waitFor(() => {
      expect(screen.getByText('LIVE 3D PREVIEW')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('tab', { name: /Interview Q&A/i }));
    expect(screen.getByText(/Live 3D Preview Mode/i)).toBeInTheDocument();
  });

  it('toggles X-Ray mode to dim healthy nodes and resets it with Reset Camera', async () => {
    mockOnlineFetch();
    render(<App />);

    const studentCard = await screen.findByTestId('seeded-card-aud_sample_student_team');
    fireEvent.click(within(studentCard).getByRole('button', { name: /Open 3D Mission Control/i }));

    await waitFor(() => {
      expect(screen.getByTestId('graph-wrapper')).toBeInTheDocument();
    });

    const xRayToggle = screen.getByTestId('xray-toggle');
    expect(xRayToggle).toHaveAttribute('aria-pressed', 'false');
    expect(screen.getByTestId('graph-wrapper')).toHaveAttribute('data-xray-mode', 'false');
    expect(screen.queryByTestId('xray-mode-indicator')).not.toBeInTheDocument();

    fireEvent.click(xRayToggle);

    expect(xRayToggle).toHaveAttribute('aria-pressed', 'true');
    expect(screen.getByTestId('graph-wrapper')).toHaveAttribute('data-xray-mode', 'true');
    expect(screen.getByTestId('xray-mode-indicator')).toHaveTextContent('X-Ray Active');
    expect(screen.getByTestId('mock-force-graph-3d')).toHaveAttribute(
      'data-last-node-color',
      'rgba(212,212,216,0.10)',
    );

    fireEvent.click(screen.getByRole('button', { name: /Reset Camera/i }));

    expect(xRayToggle).toHaveAttribute('aria-pressed', 'false');
    expect(screen.getByTestId('graph-wrapper')).toHaveAttribute('data-xray-mode', 'false');
    expect(screen.queryByTestId('xray-mode-indicator')).not.toBeInTheDocument();
    expect(zoomToFitMock).toHaveBeenCalledWith(400);
  });

  it('triggers Camera Fly-to on signal click and renders Critic Defense Review and PM HITL notes', async () => {
    mockOnlineFetch();
    render(<App />);

    const studentCard = await screen.findByTestId('seeded-card-aud_sample_student_team');
    fireEvent.click(within(studentCard).getByRole('button', { name: /Open 3D Mission Control/i }));

    await waitFor(() => {
      expect(screen.getByTestId('graph-wrapper')).toBeInTheDocument();
    });

    const hitlCard = screen.getByTestId('pm-hitl-notes-card');
    expect(hitlCard).toHaveTextContent('HITL Verified · Read-only');
    expect(hitlCard).toHaveTextContent(FALLBACK_AUDIT_REPORT.audit_id);
    expect(hitlCard).toHaveTextContent(FALLBACK_AUDIT_REPORT.summary.human_notes);

    fireEvent.click(screen.getByRole('tab', { name: /Nodes & Signals/i }));
    const signalButton = screen.getByTestId('signal-item-sig-01');
    expect(signalButton).toHaveTextContent('Fly to Node');

    const criticBox = screen.getByTestId('critic-note-sig-01');
    expect(criticBox).toHaveTextContent('Critic Defense Review');
    expect(criticBox).toHaveTextContent(FALLBACK_AUDIT_REPORT.signals[0].critic_note);

    fireEvent.click(signalButton);

    expect(screen.getByTestId('graph-wrapper')).toHaveAttribute(
      'data-fly-target',
      'mod:backend/auth',
    );
    expect(cameraPositionMock).toHaveBeenCalledWith(
      { x: 0, y: 0, z: 85 },
      { x: 0, y: 0, z: 0 },
      800,
    );
  });

  it('falls back cleanly when backend is offline via Explore Demo Workspace', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValue(new Error('Network offline'));
    render(<App />);

    await waitFor(() => {
      expect(screen.getByTestId('landing-health-pill')).toHaveTextContent('OFFLINE');
    });

    const demoButtons = screen.getAllByRole('button', { name: /Explore Demo Workspace/i });
    fireEvent.click(demoButtons[0]);

    expect(screen.getByTestId('graph-wrapper')).toBeInTheDocument();
    expect(screen.getByText('vku-sprint-demo/campus-nav')).toBeInTheDocument();
  });
});
