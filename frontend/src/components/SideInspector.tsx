import {
  AlertTriangle,
  Crosshair,
  ExternalLink,
  FileCode2,
  FileText,
  Focus,
  GitCommitHorizontal,
  Layers,
  MessageSquare,
  ShieldAlert,
  ShieldCheck,
  Users,
} from 'lucide-react';
import type { AuditReport, GraphNode, NodeStatus, RepoContext } from '../types/audit';

export type InspectorTab = 'overview' | 'components' | 'members' | 'interview';

const CONTEXT_LABELS: Record<RepoContext, string> = {
  solo: 'SOLO',
  student_team: 'STUDENT TEAM',
  open_source: 'OPEN SOURCE',
};

const STATUS_BADGE_STYLES: Record<NodeStatus, string> = {
  healthy: 'border-[#09090B] bg-[#FFFFFF] text-[#09090B]',
  probe: 'border-[#D97706] bg-[#FFFFFF] text-[#D97706]',
  risk: 'border-[#DC2626] bg-[#FFFFFF] text-[#DC2626]',
};

function resolveEvidenceGitHubUrl(repoUrl: string, evidenceRef: string): string | null {
  const cleanRepoUrl = repoUrl.trim().replace(/\/+$/, '');
  if (!cleanRepoUrl) return null;

  const commitMatch = evidenceRef.match(/\bcommit:([0-9a-f]{6,40})\b/i);
  if (commitMatch) {
    return `${cleanRepoUrl}/commit/${commitMatch[1]}`;
  }

  const prMatch = evidenceRef.match(/\bPR#(\d+)\b/i);
  if (prMatch) {
    return `${cleanRepoUrl}/pull/${prMatch[1]}`;
  }

  return null;
}

interface SideInspectorProps {
  report: AuditReport;
  activeTab: InspectorTab;
  selectedNode: GraphNode | null;
  focusedAuthorId: string | null;
  onTabChange: (tab: InspectorTab) => void;
  onSelectNodeId: (nodeId: string) => void;
  onFocusAuthor: (authorId: string | null) => void;
}

export default function SideInspector({
  report,
  activeTab,
  selectedNode,
  focusedAuthorId,
  onTabChange,
  onSelectNodeId,
  onFocusAuthor,
}: SideInspectorProps) {
  const authorNodes = report.graph_3d.nodes.filter((n) => n.type === 'author');
  const moduleNodes = report.graph_3d.nodes.filter((n) => n.type === 'module');
  const anomalyWeeks = report.timeline_2d.filter((w) => w.anomaly).length;
  const totalAuthorCommits = authorNodes.reduce((sum, node) => sum + Math.max(0, node.size), 0);

  const nodeLabelMap = new Map<string, string>(
    report.graph_3d.nodes.map((node) => [node.id, node.label]),
  );

  // Contributor breakdown for the currently selected module node.
  const selectedNodeContributors = (() => {
    if (!selectedNode) return [];
    const relevantEdges = report.graph_3d.edges.filter((edge) => edge.target === selectedNode.id);
    const totalWeight = relevantEdges.reduce((sum, edge) => sum + Math.max(0, edge.weight), 0);
    if (totalWeight <= 0) return [];

    return relevantEdges
      .map((edge) => ({
        authorId: edge.source,
        label: nodeLabelMap.get(edge.source) ?? edge.source,
        weight: edge.weight,
        percent: Math.round((edge.weight / totalWeight) * 100),
      }))
      .sort((a, b) => b.weight - a.weight);
  })();

  const commitHighlights = report.commit_highlights ?? [];

  return (
    <aside
      aria-label="Audit Side Inspector"
      data-testid="side-inspector"
      className="w-full lg:w-[34%] lg:min-w-[340px] border-t lg:border-t-0 lg:border-l border-[#E4E4E7] bg-[#FAFAFA] flex flex-col min-h-0"
    >
      <div
        role="tablist"
        aria-label="Inspector views"
        className="grid grid-cols-4 border-b border-[#E4E4E7] bg-[#FFFFFF] shrink-0"
      >
        {(
          [
            { id: 'overview', label: 'Tổng quan', icon: FileText },
            { id: 'components', label: 'Thành phần', icon: Layers },
            { id: 'members', label: 'Thành viên & Commit', icon: Users },
            { id: 'interview', label: 'Vấn đáp', icon: MessageSquare },
          ] as const
        ).map(({ id, label, icon: Icon }) => {
          const isActive = activeTab === id;
          return (
            <button
              key={id}
              type="button"
              role="tab"
              aria-selected={isActive}
              onClick={() => onTabChange(id)}
              className={`px-1.5 py-2.5 text-[10px] font-semibold tracking-[0.04em] leading-tight flex flex-col items-center justify-center gap-1 text-center border-b-2 transition-colors cursor-pointer ${
                isActive
                  ? 'border-[#09090B] text-[#09090B] bg-[#FAFAFA]'
                  : 'border-transparent text-[#52525B] hover:text-[#09090B]'
              }`}
            >
              <Icon className="w-3.5 h-3.5 shrink-0" strokeWidth={1.5} aria-hidden="true" />
              <span className="line-clamp-2">{label}</span>
            </button>
          );
        })}
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {activeTab === 'overview' && (
          <div className="space-y-4">
            <div
              data-testid="anti-hallucination-banner"
              className="border border-[#09090B] bg-[#FFFFFF] p-3.5 space-y-1.5"
            >
              <div className="flex items-center gap-1.5 text-[11px] font-display font-bold uppercase tracking-[0.12em] text-[#09090B]">
                <ShieldCheck className="w-3.5 h-3.5 shrink-0" strokeWidth={1.5} aria-hidden="true" />
                <span>Chống ảo giác — Neo bằng chứng Git thật</span>
              </div>
              <p className="text-[11px] text-[#52525B] leading-relaxed">
                Mọi mô tả thành phần, cụm module và tín hiệu kiểm toán đều được trích xuất trực
                tiếp từ lịch sử Git commits/diffs và danh sách{' '}
                <code className="font-mono text-[#09090B]">valid_refs</code> thực tế (không dựa vào{' '}
                <code className="font-mono text-[#09090B]">README.md</code>).
              </p>
            </div>

            <div className="grid grid-cols-2 gap-2.5">
              {[
                { label: 'Thành viên', value: authorNodes.length },
                { label: 'Thành phần', value: moduleNodes.length },
                { label: 'Tín hiệu', value: report.signals.length },
                { label: 'Tuần bất thường', value: anomalyWeeks, highlight: anomalyWeeks > 0 },
              ].map((stat) => (
                <div
                  key={stat.label}
                  className="border border-[#E4E4E7] bg-[#FFFFFF] p-3 flex flex-col gap-1"
                >
                  <span className="text-[10px] font-semibold uppercase tracking-[0.14em] text-[#52525B]">
                    {stat.label}
                  </span>
                  <span
                    className={`font-display text-xl font-bold tabular-nums ${
                      stat.highlight ? 'text-[#DC2626]' : 'text-[#09090B]'
                    }`}
                  >
                    {stat.value}
                  </span>
                </div>
              ))}
            </div>

            <div className="border border-[#E4E4E7] bg-[#FFFFFF] p-3.5 space-y-2">
              <div className="flex items-center justify-between gap-2">
                <h3 className="font-display text-[11px] font-bold uppercase tracking-[0.14em] text-[#09090B]">
                  Repository Context
                </h3>
                <span className="border border-[#09090B] bg-[#FAFAFA] px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.12em]">
                  {CONTEXT_LABELS[report.repo.context]}
                </span>
              </div>
              <p className="text-xs text-[#52525B] leading-relaxed">
                {report.repo.context_reasoning}
              </p>
            </div>

            <div className="border border-[#E4E4E7] bg-[#FFFFFF] p-3.5 space-y-2">
              <h3 className="font-display text-[11px] font-bold uppercase tracking-[0.14em] text-[#09090B]">
                AI Audit Overview
              </h3>
              <p className="text-xs text-[#09090B] leading-relaxed">{report.summary.overview}</p>
            </div>

            <div
              data-testid="pm-hitl-notes-card"
              className="border border-[#09090B] bg-[#FFFFFF] p-3.5 space-y-2.5"
            >
              <div className="flex items-center justify-between gap-2">
                <h3 className="font-display text-[11px] font-bold uppercase tracking-[0.14em] text-[#09090B]">
                  PM Human Notes
                </h3>
                <span className="inline-flex items-center gap-1 border border-[#09090B] bg-[#FAFAFA] px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-[#09090B]">
                  <ShieldCheck className="w-3 h-3 shrink-0" strokeWidth={1.5} aria-hidden="true" />
                  <span>HITL Verified · Read-only</span>
                </span>
              </div>
              <p className="text-xs text-[#09090B] leading-relaxed whitespace-pre-wrap">
                {report.summary.human_notes || 'No human notes recorded for this audit.'}
              </p>
              <div className="flex flex-wrap items-center justify-between gap-2 border-t border-[#E4E4E7] pt-2 text-[10px] font-mono text-[#52525B] tabular-nums">
                <span>Audit ID: {report.audit_id}</span>
                <span>Created: {report.created_at}</span>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'components' && (
          <div className="space-y-4">
            <div
              data-testid="selected-node-card"
              className="border border-[#E4E4E7] bg-[#FFFFFF] p-3.5 space-y-3"
            >
              <div className="flex items-center justify-between gap-2">
                <h3 className="font-display text-[11px] font-bold uppercase tracking-[0.14em] text-[#09090B]">
                  Thành phần đang chọn
                </h3>
                {selectedNode && (
                  <span
                    className={`border px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider ${STATUS_BADGE_STYLES[selectedNode.status]}`}
                  >
                    {selectedNode.status}
                  </span>
                )}
              </div>

              {selectedNode ? (
                <div className="space-y-3">
                  <div>
                    <p className="text-sm font-semibold text-[#09090B] break-words">
                      {selectedNode.label}
                    </p>
                    <p className="text-[11px] font-mono text-[#52525B]">{selectedNode.id}</p>
                  </div>

                  <p className="text-xs text-[#09090B] leading-relaxed border-l-2 border-[#09090B] pl-2.5 bg-[#FAFAFA] py-1.5 pr-2">
                    {selectedNode.description?.trim() ||
                      'Chưa có mô tả chi tiết cho thành phần này từ dữ liệu commit.'}
                  </p>

                  <dl className="grid grid-cols-2 gap-2 text-xs tabular-nums">
                    <div className="border border-[#E4E4E7] bg-[#FAFAFA] px-2.5 py-1.5">
                      <dt className="text-[10px] uppercase tracking-wider text-[#52525B]">Loại</dt>
                      <dd className="font-semibold text-[#09090B] uppercase">
                        {selectedNode.type}
                      </dd>
                    </div>
                    <div className="border border-[#E4E4E7] bg-[#FAFAFA] px-2.5 py-1.5">
                      <dt className="text-[10px] uppercase tracking-wider text-[#52525B]">
                        Quy mô (Commits)
                      </dt>
                      <dd className="font-semibold text-[#09090B]">{selectedNode.size}</dd>
                    </div>
                    {selectedNode.churn !== null && selectedNode.churn !== undefined && (
                      <div className="border border-[#E4E4E7] bg-[#FAFAFA] px-2.5 py-1.5">
                        <dt className="text-[10px] uppercase tracking-wider text-[#52525B]">
                          Biến động (Churn)
                        </dt>
                        <dd className="font-semibold text-[#09090B]">{selectedNode.churn}</dd>
                      </div>
                    )}
                    {selectedNode.role && (
                      <div className="border border-[#E4E4E7] bg-[#FAFAFA] px-2.5 py-1.5">
                        <dt className="text-[10px] uppercase tracking-wider text-[#52525B]">
                          Vai trò
                        </dt>
                        <dd className="font-semibold text-[#09090B]">{selectedNode.role}</dd>
                      </div>
                    )}
                  </dl>

                  {selectedNode.key_files && selectedNode.key_files.length > 0 && (
                    <div className="space-y-1.5" data-testid="selected-node-key-files">
                      <div className="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-[0.12em] text-[#52525B]">
                        <FileCode2
                          className="w-3 h-3 text-[#09090B] shrink-0"
                          strokeWidth={1.5}
                          aria-hidden="true"
                        />
                        <span>Tệp mã nguồn thật (Key Files)</span>
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {selectedNode.key_files.map((filePath) => (
                          <span
                            key={filePath}
                            className="border border-[#E4E4E7] bg-[#FAFAFA] px-2 py-0.5 text-[11px] font-mono text-[#09090B] break-all"
                          >
                            {filePath}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {selectedNodeContributors.length > 0 && (
                    <div className="space-y-2" data-testid="selected-node-contributors">
                      <div className="text-[10px] font-bold uppercase tracking-[0.12em] text-[#52525B]">
                        Tỷ trọng đóng góp thành viên
                      </div>
                      <div className="space-y-1.5">
                        {selectedNodeContributors.map((entry) => (
                          <div key={entry.authorId} className="space-y-1">
                            <div className="flex items-center justify-between text-[11px] tabular-nums">
                              <span className="font-medium text-[#09090B]">{entry.label}</span>
                              <span className="font-mono text-[#52525B]">
                                {entry.percent}% ({entry.weight} commits)
                              </span>
                            </div>
                            <div className="h-1.5 w-full bg-[#E4E4E7] overflow-hidden">
                              <div
                                className="h-full bg-[#09090B]"
                                style={{ width: `${Math.min(100, Math.max(2, entry.percent))}%` }}
                              />
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-xs text-[#52525B]">
                  Nhấp vào một thành phần (module) trên đồ thị 3D — hoặc chọn một tín hiệu kiểm toán
                  bên dưới — để xem mô tả, tệp mã nguồn thật và tỷ trọng đóng góp.
                </p>
              )}
            </div>

            <div className="space-y-2.5">
              <h3 className="font-display text-[11px] font-bold uppercase tracking-[0.14em] text-[#09090B]">
                Tín hiệu kiểm toán ({report.signals.length})
              </h3>

              {report.signals.length === 0 ? (
                <div className="border border-[#E4E4E7] bg-[#FFFFFF] p-3.5 text-xs text-[#52525B]">
                  Không có tín hiệu rủi ro hay cần thăm dò nào cho repository này.
                </div>
              ) : (
                report.signals.map((signal) => {
                  const isSelected = selectedNode?.id === signal.node_id;
                  const accentBorder =
                    signal.level === 'risk'
                      ? 'border-l-[#DC2626]'
                      : signal.level === 'probe'
                        ? 'border-l-[#D97706]'
                        : 'border-l-[#09090B]';
                  const Icon = signal.level === 'risk' ? ShieldAlert : AlertTriangle;
                  const evidenceUrl = resolveEvidenceGitHubUrl(report.repo.url, signal.evidence_ref);

                  return (
                    <div
                      key={signal.id}
                      role="button"
                      tabIndex={0}
                      data-testid={`signal-item-${signal.id}`}
                      onClick={() => onSelectNodeId(signal.node_id)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter' || e.key === ' ') {
                          e.preventDefault();
                          onSelectNodeId(signal.node_id);
                        }
                      }}
                      className={`w-full text-left border border-l-4 ${accentBorder} p-3.5 space-y-2 transition-colors cursor-pointer ${
                        isSelected
                          ? 'border-[#09090B] bg-[#FFFFFF]'
                          : 'border-[#E4E4E7] bg-[#FFFFFF] hover:border-[#09090B]'
                      }`}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex items-center gap-1.5">
                          <Icon
                            className={`w-3.5 h-3.5 shrink-0 ${
                              signal.level === 'risk'
                                ? 'text-[#DC2626]'
                                : signal.level === 'probe'
                                  ? 'text-[#D97706]'
                                  : 'text-[#09090B]'
                            }`}
                            strokeWidth={1.5}
                            aria-hidden="true"
                          />
                          <span className="text-xs font-semibold text-[#09090B]">
                            {signal.title}
                          </span>
                        </div>
                        <span
                          className={`border px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-wider shrink-0 ${STATUS_BADGE_STYLES[signal.level]}`}
                        >
                          {signal.level}
                        </span>
                      </div>

                      <p className="text-xs text-[#52525B] leading-relaxed">{signal.description}</p>

                      <div className="flex items-center justify-between gap-2 text-[11px] font-mono text-[#09090B] bg-[#FAFAFA] border border-[#E4E4E7] px-2 py-1">
                        {evidenceUrl ? (
                          <a
                            href={evidenceUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            onClick={(e) => e.stopPropagation()}
                            className="inline-flex items-center gap-1 truncate underline underline-offset-2 hover:text-[#52525B]"
                          >
                            <span className="truncate">Evidence: {signal.evidence_ref}</span>
                            <ExternalLink
                              className="w-3 h-3 shrink-0"
                              strokeWidth={1.5}
                              aria-hidden="true"
                            />
                          </a>
                        ) : (
                          <span className="truncate">Evidence: {signal.evidence_ref}</span>
                        )}
                        <span className="inline-flex items-center gap-1 text-[10px] font-sans font-semibold uppercase tracking-wider text-[#52525B] shrink-0">
                          <Crosshair
                            className="w-3 h-3 text-[#09090B]"
                            strokeWidth={1.5}
                            aria-hidden="true"
                          />
                          <span>Fly to Node</span>
                        </span>
                      </div>

                      {signal.critic_note && (
                        <div
                          data-testid={`critic-note-${signal.id}`}
                          className="border border-[#E4E4E7] bg-[#FAFAFA] p-2.5 space-y-1"
                        >
                          <div className="text-[10px] font-bold uppercase tracking-[0.12em] text-[#09090B]">
                            Critic Defense Review
                          </div>
                          <p className="text-[11px] text-[#52525B] leading-relaxed">
                            {signal.critic_note}
                          </p>
                        </div>
                      )}
                    </div>
                  );
                })
              )}
            </div>
          </div>
        )}

        {activeTab === 'members' && (
          <div className="space-y-5">
            <div className="space-y-2.5" data-testid="members-breakdown-section">
              <h3 className="font-display text-[11px] font-bold uppercase tracking-[0.14em] text-[#09090B]">
                Đóng góp thành viên ({authorNodes.length})
              </h3>

              {authorNodes.length === 0 ? (
                <div className="border border-[#E4E4E7] bg-[#FFFFFF] p-3.5 text-xs text-[#52525B]">
                  Chưa có dữ liệu thành viên cho repository này.
                </div>
              ) : (
                authorNodes.map((author) => {
                  const sharePercent =
                    totalAuthorCommits > 0
                      ? Math.round((Math.max(0, author.size) / totalAuthorCommits) * 100)
                      : 0;
                  const isFocused = focusedAuthorId === author.id;
                  const isSelected = selectedNode?.id === author.id;
                  const primaryModules = report.graph_3d.edges
                    .filter((edge) => edge.source === author.id)
                    .sort((a, b) => b.weight - a.weight)
                    .map((edge) => ({
                      id: edge.target,
                      label: nodeLabelMap.get(edge.target) ?? edge.target,
                      weight: edge.weight,
                    }));

                  return (
                    <article
                      key={author.id}
                      data-testid={`member-card-${author.id}`}
                      className={`border bg-[#FFFFFF] p-3.5 space-y-2.5 ${
                        isFocused || isSelected ? 'border-[#09090B]' : 'border-[#E4E4E7]'
                      }`}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div className="min-w-0">
                          <div className="flex items-center gap-2 flex-wrap">
                            <span className="text-xs font-semibold text-[#09090B]">
                              {author.label}
                            </span>
                            {author.role && (
                              <span className="border border-[#E4E4E7] bg-[#FAFAFA] px-1.5 py-0.5 text-[10px] font-medium text-[#52525B]">
                                {author.role}
                              </span>
                            )}
                          </div>
                          <p className="text-[11px] font-mono text-[#52525B] tabular-nums mt-0.5">
                            {author.size} commits · {sharePercent}% tổng đóng góp
                          </p>
                        </div>

                        <button
                          type="button"
                          data-testid={`focus-member-btn-${author.id}`}
                          aria-pressed={isFocused}
                          onClick={() => onFocusAuthor(isFocused ? null : author.id)}
                          className={`px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.08em] border inline-flex items-center gap-1 shrink-0 transition-colors cursor-pointer ${
                            isFocused
                              ? 'border-[#09090B] bg-[#09090B] text-[#FFFFFF]'
                              : 'border-[#E4E4E7] bg-[#FAFAFA] text-[#09090B] hover:border-[#09090B]'
                          }`}
                        >
                          <Focus className="w-3 h-3" strokeWidth={1.5} aria-hidden="true" />
                          <span>{isFocused ? 'Đang Focus' : 'Focus trên 3D'}</span>
                        </button>
                      </div>

                      <div className="h-1.5 w-full bg-[#E4E4E7] overflow-hidden">
                        <div
                          className="h-full bg-[#09090B]"
                          style={{ width: `${Math.min(100, Math.max(2, sharePercent))}%` }}
                        />
                      </div>

                      {author.description && (
                        <p className="text-xs text-[#52525B] leading-relaxed">
                          {author.description}
                        </p>
                      )}

                      {primaryModules.length > 0 && (
                        <div className="flex flex-wrap items-center gap-1.5 pt-0.5">
                          {primaryModules.map((mod) => (
                            <button
                              key={mod.id}
                              type="button"
                              onClick={() => onSelectNodeId(mod.id)}
                              className="border border-[#E4E4E7] bg-[#FAFAFA] hover:border-[#09090B] px-2 py-0.5 text-[10px] font-mono text-[#09090B] transition-colors cursor-pointer tabular-nums"
                            >
                              {mod.label} ({mod.weight})
                            </button>
                          ))}
                        </div>
                      )}
                    </article>
                  );
                })
              )}
            </div>

            <div className="space-y-2.5" data-testid="commit-highlights-section">
              <div className="flex items-center gap-1.5">
                <GitCommitHorizontal
                  className="w-3.5 h-3.5 text-[#09090B]"
                  strokeWidth={1.5}
                  aria-hidden="true"
                />
                <h3 className="font-display text-[11px] font-bold uppercase tracking-[0.14em] text-[#09090B]">
                  Commit &amp; PR tiêu biểu ({commitHighlights.length})
                </h3>
              </div>

              {commitHighlights.length === 0 ? (
                <div className="border border-[#E4E4E7] bg-[#FFFFFF] p-3.5 text-xs text-[#52525B]">
                  Chưa có commit hoặc Pull Request tiêu biểu nào được ghi nhận.
                </div>
              ) : (
                commitHighlights.map((item, idx) => (
                  <article
                    key={`${item.ref}-${idx}`}
                    data-testid={`commit-highlight-${idx}`}
                    className="border border-[#E4E4E7] bg-[#FFFFFF] p-3.5 space-y-2"
                  >
                    <div className="flex items-center justify-between gap-2 flex-wrap">
                      <div className="flex items-center gap-2 min-w-0">
                        <span className="border border-[#09090B] bg-[#FAFAFA] px-1.5 py-0.5 text-[10px] font-mono font-semibold text-[#09090B]">
                          {item.ref}
                        </span>
                        <span className="text-[11px] font-medium text-[#52525B] truncate">
                          {item.author}
                          {item.date ? ` · ${item.date}` : ''}
                        </span>
                      </div>
                      <a
                        href={item.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 text-[10px] font-semibold uppercase tracking-[0.08em] text-[#09090B] border border-[#E4E4E7] hover:border-[#09090B] bg-[#FAFAFA] px-2 py-0.5 transition-colors shrink-0"
                      >
                        <span>Mở trên GitHub</span>
                        <ExternalLink className="w-3 h-3" strokeWidth={1.5} aria-hidden="true" />
                      </a>
                    </div>

                    <p className="text-xs font-semibold text-[#09090B] leading-snug">
                      {item.title}
                    </p>
                    <p className="text-xs text-[#52525B] leading-relaxed">{item.diff_summary}</p>

                    {item.files_changed && item.files_changed.length > 0 && (
                      <div className="flex flex-wrap gap-1 pt-0.5">
                        {item.files_changed.map((filePath) => (
                          <span
                            key={filePath}
                            className="border border-[#E4E4E7] bg-[#FAFAFA] px-1.5 py-0.5 text-[10px] font-mono text-[#52525B] break-all"
                          >
                            {filePath}
                          </span>
                        ))}
                      </div>
                    )}
                  </article>
                ))
              )}
            </div>
          </div>
        )}

        {activeTab === 'interview' && (
          <div className="space-y-3">
            <h3 className="font-display text-[11px] font-bold uppercase tracking-[0.14em] text-[#09090B]">
              Câu hỏi vấn đáp ({report.interview_questions.length})
            </h3>

            {report.mode === 'live_preview' && report.interview_questions.length === 0 ? (
              <div className="border border-[#E4E4E7] bg-[#FFFFFF] p-4 space-y-2">
                <p className="text-xs font-semibold text-[#09090B]">Live 3D Preview Mode</p>
                <p className="text-xs text-[#52525B] leading-relaxed">
                  Câu hỏi vấn đáp chuyên sâu và phản biện Critic được tạo khi chạy Deep AI Audit.
                  Chọn một báo cáo Deep AI Audit có sẵn ở thanh trên để xem mẫu câu hỏi vấn đáp.
                </p>
              </div>
            ) : report.interview_questions.length === 0 ? (
              <div className="border border-[#E4E4E7] bg-[#FFFFFF] p-4 text-xs text-[#52525B]">
                Chưa có câu hỏi vấn đáp nào cho báo cáo này.
              </div>
            ) : (
              report.interview_questions.map((item, index) => {
                const evidenceUrl = resolveEvidenceGitHubUrl(report.repo.url, item.evidence_ref);
                return (
                  <article
                    key={`${item.author_id}-${index}`}
                    className="border border-[#E4E4E7] bg-[#FFFFFF] p-3.5 space-y-2.5"
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-xs font-semibold text-[#09090B]">
                        {item.author_name}
                      </span>
                      {evidenceUrl ? (
                        <a
                          href={evidenceUrl}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1 border border-[#E4E4E7] hover:border-[#09090B] bg-[#FAFAFA] px-2 py-0.5 text-[10px] font-mono text-[#09090B] transition-colors"
                        >
                          <span>{item.evidence_ref}</span>
                          <ExternalLink className="w-2.5 h-2.5" strokeWidth={1.5} aria-hidden="true" />
                        </a>
                      ) : (
                        <span className="border border-[#E4E4E7] bg-[#FAFAFA] px-2 py-0.5 text-[10px] font-mono text-[#52525B]">
                          {item.evidence_ref}
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-[#09090B] leading-relaxed">{item.question}</p>
                  </article>
                );
              })
            )}
          </div>
        )}
      </div>
    </aside>
  );
}
