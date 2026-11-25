import {
  AlertTriangle,
  Crosshair,
  FileText,
  Layers,
  MessageSquare,
  ShieldAlert,
  ShieldCheck,
} from 'lucide-react';
import type { AuditReport, GraphNode, NodeStatus, RepoContext } from '../types/audit';

export type InspectorTab = 'overview' | 'signals' | 'interview';

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

interface SideInspectorProps {
  report: AuditReport;
  activeTab: InspectorTab;
  selectedNode: GraphNode | null;
  onTabChange: (tab: InspectorTab) => void;
  onSelectNodeId: (nodeId: string) => void;
}

export default function SideInspector({
  report,
  activeTab,
  selectedNode,
  onTabChange,
  onSelectNodeId,
}: SideInspectorProps) {
  const authorCount = report.graph_3d.nodes.filter((n) => n.type === 'author').length;
  const moduleCount = report.graph_3d.nodes.filter((n) => n.type === 'module').length;
  const anomalyWeeks = report.timeline_2d.filter((w) => w.anomaly).length;

  return (
    <aside
      aria-label="Audit Side Inspector"
      data-testid="side-inspector"
      className="w-full lg:w-[34%] lg:min-w-[340px] border-t lg:border-t-0 lg:border-l border-[#E4E4E7] bg-[#FAFAFA] flex flex-col min-h-0"
    >
      <div
        role="tablist"
        aria-label="Inspector views"
        className="grid grid-cols-3 border-b border-[#E4E4E7] bg-[#FFFFFF] shrink-0"
      >
        {(
          [
            { id: 'overview', label: 'Overview', icon: FileText },
            { id: 'signals', label: 'Nodes & Signals', icon: Layers },
            { id: 'interview', label: 'Interview Q&A', icon: MessageSquare },
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
              className={`px-2 py-3 text-[11px] font-semibold uppercase tracking-[0.1em] inline-flex items-center justify-center gap-1.5 border-b-2 transition-colors cursor-pointer ${
                isActive
                  ? 'border-[#09090B] text-[#09090B] bg-[#FAFAFA]'
                  : 'border-transparent text-[#52525B] hover:text-[#09090B]'
              }`}
            >
              <Icon className="w-3.5 h-3.5 shrink-0" aria-hidden="true" />
              <span className="truncate">{label}</span>
            </button>
          );
        })}
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {activeTab === 'overview' && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-2.5">
              {[
                { label: 'Authors', value: authorCount },
                { label: 'Modules', value: moduleCount },
                { label: 'Signals', value: report.signals.length },
                { label: 'Anomaly Weeks', value: anomalyWeeks, highlight: anomalyWeeks > 0 },
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
                  <ShieldCheck className="w-3 h-3 shrink-0" aria-hidden="true" />
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

        {activeTab === 'signals' && (
          <div className="space-y-4">
            <div
              data-testid="selected-node-card"
              className="border border-[#E4E4E7] bg-[#FFFFFF] p-3.5 space-y-2.5"
            >
              <div className="flex items-center justify-between gap-2">
                <h3 className="font-display text-[11px] font-bold uppercase tracking-[0.14em] text-[#09090B]">
                  Selected Node
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
                <div className="space-y-2">
                  <div>
                    <p className="text-sm font-semibold text-[#09090B] break-words">
                      {selectedNode.label}
                    </p>
                    <p className="text-[11px] font-mono text-[#52525B]">{selectedNode.id}</p>
                  </div>
                  <dl className="grid grid-cols-2 gap-2 pt-1 text-xs tabular-nums">
                    <div className="border border-[#E4E4E7] bg-[#FAFAFA] px-2.5 py-1.5">
                      <dt className="text-[10px] uppercase tracking-wider text-[#52525B]">Type</dt>
                      <dd className="font-semibold text-[#09090B] uppercase">
                        {selectedNode.type}
                      </dd>
                    </div>
                    <div className="border border-[#E4E4E7] bg-[#FAFAFA] px-2.5 py-1.5">
                      <dt className="text-[10px] uppercase tracking-wider text-[#52525B]">Size</dt>
                      <dd className="font-semibold text-[#09090B]">{selectedNode.size}</dd>
                    </div>
                    {selectedNode.churn !== null && selectedNode.churn !== undefined && (
                      <div className="border border-[#E4E4E7] bg-[#FAFAFA] px-2.5 py-1.5">
                        <dt className="text-[10px] uppercase tracking-wider text-[#52525B]">
                          Churn
                        </dt>
                        <dd className="font-semibold text-[#09090B]">{selectedNode.churn}</dd>
                      </div>
                    )}
                    {selectedNode.role && (
                      <div className="border border-[#E4E4E7] bg-[#FAFAFA] px-2.5 py-1.5">
                        <dt className="text-[10px] uppercase tracking-wider text-[#52525B]">
                          Role
                        </dt>
                        <dd className="font-semibold text-[#09090B]">{selectedNode.role}</dd>
                      </div>
                    )}
                  </dl>
                </div>
              ) : (
                <p className="text-xs text-[#52525B]">
                  Click any author or module node in the 3D canvas — or click a signal below — to
                  inspect its telemetry metadata.
                </p>
              )}
            </div>

            <div className="space-y-2.5">
              <h3 className="font-display text-[11px] font-bold uppercase tracking-[0.14em] text-[#09090B]">
                Audit Signals ({report.signals.length})
              </h3>

              {report.signals.length === 0 ? (
                <div className="border border-[#E4E4E7] bg-[#FFFFFF] p-3.5 text-xs text-[#52525B]">
                  No probe or risk signals flagged for this repository.
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

                  return (
                    <button
                      key={signal.id}
                      type="button"
                      data-testid={`signal-item-${signal.id}`}
                      onClick={() => onSelectNodeId(signal.node_id)}
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
                        <span className="truncate">Evidence: {signal.evidence_ref}</span>
                        <span className="inline-flex items-center gap-1 text-[10px] font-sans font-semibold uppercase tracking-wider text-[#52525B] shrink-0">
                          <Crosshair className="w-3 h-3 text-[#09090B]" aria-hidden="true" />
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
                    </button>
                  );
                })
              )}
            </div>
          </div>
        )}

        {activeTab === 'interview' && (
          <div className="space-y-3">
            <h3 className="font-display text-[11px] font-bold uppercase tracking-[0.14em] text-[#09090B]">
              Targeted Interview Questions ({report.interview_questions.length})
            </h3>

            {report.mode === 'live_preview' && report.interview_questions.length === 0 ? (
              <div className="border border-[#E4E4E7] bg-[#FFFFFF] p-4 space-y-2">
                <p className="text-xs font-semibold text-[#09090B]">
                  Live 3D Preview Mode
                </p>
                <p className="text-xs text-[#52525B] leading-relaxed">
                  Deep AI interview questions and critic-verified defense probes are generated
                  during a full Deep AI Audit. Switch to a pre-seeded Deep AI Audit in the top bar
                  to inspect sample Q&amp;A.
                </p>
              </div>
            ) : report.interview_questions.length === 0 ? (
              <div className="border border-[#E4E4E7] bg-[#FFFFFF] p-4 text-xs text-[#52525B]">
                No interview questions available for this audit.
              </div>
            ) : (
              report.interview_questions.map((item, index) => (
                <article
                  key={`${item.author_id}-${index}`}
                  className="border border-[#E4E4E7] bg-[#FFFFFF] p-3.5 space-y-2.5"
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-xs font-semibold text-[#09090B]">
                      {item.author_name}
                    </span>
                    <span className="border border-[#E4E4E7] bg-[#FAFAFA] px-2 py-0.5 text-[10px] font-mono text-[#52525B]">
                      {item.evidence_ref}
                    </span>
                  </div>
                  <p className="text-xs text-[#09090B] leading-relaxed">{item.question}</p>
                </article>
              ))
            )}
          </div>
        )}
      </div>
    </aside>
  );
}
