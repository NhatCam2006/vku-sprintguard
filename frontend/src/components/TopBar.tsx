import { type FormEvent, useState } from 'react';
import { ArrowLeft, Loader2, Play, ScanEye } from 'lucide-react';
import type {
  AuditListItem,
  AuditMode,
  AuditReport,
  HealthResponse,
  RepoContext,
} from '../types/audit';

const CONTEXT_LABELS: Record<RepoContext, string> = {
  solo: 'SOLO',
  student_team: 'STUDENT TEAM',
  open_source: 'OPEN SOURCE',
};

const MODE_LABELS: Record<AuditMode, string> = {
  deep_ai_audit: 'DEEP AI AUDIT',
  live_preview: 'LIVE 3D PREVIEW',
};

interface TopBarProps {
  report: AuditReport;
  audits: AuditListItem[];
  health: HealthResponse | null;
  isPreviewLoading: boolean;
  xRayMode: boolean;
  onToggleXRay: () => void;
  onBackToLanding: () => void;
  onSelectAudit: (auditId: string) => void;
  onLaunchPreview: (repoUrl: string) => void;
}

export default function TopBar({
  report,
  audits,
  health,
  isPreviewLoading,
  xRayMode,
  onToggleXRay,
  onBackToLanding,
  onSelectAudit,
  onLaunchPreview,
}: TopBarProps) {
  const [urlInput, setUrlInput] = useState('');
  const isOnline = health?.status === 'ok';

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const trimmed = urlInput.trim();
    if (!trimmed || isPreviewLoading) return;
    onLaunchPreview(trimmed);
  };

  return (
    <header className="border-b border-[#E4E4E7] bg-[#FFFFFF] px-4 py-2.5 flex flex-wrap items-center justify-between gap-3">
      <div className="flex flex-wrap items-center gap-2.5 min-w-0">
        <button
          type="button"
          onClick={onBackToLanding}
          className="h-8 px-2.5 border border-[#E4E4E7] bg-[#FAFAFA] hover:border-[#09090B] text-xs font-medium text-[#09090B] inline-flex items-center gap-1.5 transition-colors cursor-pointer"
        >
          <ArrowLeft className="w-3.5 h-3.5" aria-hidden="true" />
          <span>Landing</span>
        </button>

        <span className="font-display text-xs font-bold tracking-[0.18em] uppercase text-[#09090B]">
          VKU SPRINTGUARD
        </span>

        <span className="text-[#E4E4E7]" aria-hidden="true">
          /
        </span>

        <span
          className="text-xs font-semibold text-[#09090B] truncate max-w-[200px]"
          title={report.repo.name}
        >
          {report.repo.name}
        </span>

        <span className="border border-[#09090B] bg-[#FAFAFA] px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.12em] text-[#09090B]">
          {CONTEXT_LABELS[report.repo.context]}
        </span>

        <span className="border border-[#E4E4E7] bg-[#FFFFFF] px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.12em] text-[#52525B]">
          {MODE_LABELS[report.mode]}
        </span>
      </div>

      <div className="flex flex-wrap items-center gap-2 flex-1 justify-center max-w-xl">
        {audits.length > 0 && (
          <select
            aria-label="Switch seeded audit"
            value={audits.some((a) => a.audit_id === report.audit_id) ? report.audit_id : ''}
            onChange={(event) => {
              if (event.target.value) onSelectAudit(event.target.value);
            }}
            className="h-8 px-2.5 border border-[#E4E4E7] bg-[#FAFAFA] text-xs text-[#09090B] focus:outline-none focus:border-[#09090B]"
          >
            <option value="" disabled>
              Seeded audits…
            </option>
            {audits.map((item) => (
              <option key={item.audit_id} value={item.audit_id}>
                {item.repo.name} ({CONTEXT_LABELS[item.repo.context]})
              </option>
            ))}
          </select>
        )}

        <form onSubmit={handleSubmit} className="flex items-center gap-1.5 flex-1 min-w-[220px]">
          <input
            type="url"
            aria-label="Quick GitHub URL preview"
            value={urlInput}
            onChange={(event) => setUrlInput(event.target.value)}
            placeholder="https://github.com/owner/repo"
            className="h-8 flex-1 min-w-0 px-2.5 border border-[#E4E4E7] bg-[#FAFAFA] text-xs text-[#09090B] placeholder:text-[#71717A] focus:outline-none focus:border-[#09090B] focus:bg-[#FFFFFF]"
          />
          <button
            type="submit"
            disabled={isPreviewLoading || !urlInput.trim()}
            className="h-8 px-3 bg-[#09090B] text-[#FFFFFF] hover:bg-[#27272A] disabled:opacity-50 text-[11px] font-semibold uppercase tracking-[0.12em] inline-flex items-center gap-1.5 transition-colors cursor-pointer shrink-0"
          >
            {isPreviewLoading ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin" aria-hidden="true" />
            ) : (
              <Play className="w-3 h-3" aria-hidden="true" />
            )}
            <span>Preview 3D</span>
          </button>
        </form>
      </div>

      <div className="flex items-center gap-2 shrink-0">
        <button
          type="button"
          data-testid="xray-toggle"
          aria-pressed={xRayMode}
          onClick={onToggleXRay}
          className={`h-8 px-2.5 border text-[11px] font-semibold uppercase tracking-[0.12em] inline-flex items-center gap-1.5 transition-colors cursor-pointer shrink-0 ${
            xRayMode
              ? 'bg-[#09090B] text-[#FFFFFF] border-[#09090B]'
              : 'bg-[#FAFAFA] text-[#09090B] border-[#E4E4E7] hover:border-[#09090B]'
          }`}
        >
          <ScanEye className="w-3.5 h-3.5 shrink-0" aria-hidden="true" />
          <span>X-Ray</span>
          {xRayMode && (
            <span className="w-1.5 h-1.5 rounded-full bg-[#DC2626]" aria-hidden="true" />
          )}
        </button>

        <div
          data-testid="topbar-health-pill"
          className="inline-flex items-center gap-2 border border-[#E4E4E7] bg-[#FAFAFA] px-2.5 py-1 text-[11px] font-medium uppercase tracking-wider tabular-nums shrink-0"
        >
          <span
            className={`w-2 h-2 rounded-full ${isOnline ? 'bg-[#09090B]' : 'bg-[#DC2626]'}`}
            aria-hidden="true"
          />
          <span>{isOnline ? `ONLINE · ${health.seeded_audits} SEEDED` : 'OFFLINE'}</span>
        </div>
      </div>
    </header>
  );
}
