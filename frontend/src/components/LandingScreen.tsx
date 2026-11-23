import { type FormEvent, useState } from 'react';
import {
  AlertCircle,
  ArrowRight,
  Box,
  GitBranch,
  Loader2,
  Orbit,
  Radio,
  Sparkles,
} from 'lucide-react';
import type { AuditListItem, HealthResponse, RepoContext } from '../types/audit';

const SAMPLE_REPO_URL = 'https://github.com/NhatCam2006/vku-sprintguard';

const CONTEXT_LABELS: Record<RepoContext, string> = {
  solo: 'SOLO',
  student_team: 'STUDENT TEAM',
  open_source: 'OPEN SOURCE',
};

interface LandingScreenProps {
  health: HealthResponse | null;
  audits: AuditListItem[];
  isLoadingAudits: boolean;
  isPreviewLoading: boolean;
  isAuditLoadingId: string | null;
  errorMessage: string | null;
  onSelectAudit: (auditId: string) => void;
  onLaunchPreview: (repoUrl: string) => void;
  onExploreDemo: () => void;
}

export default function LandingScreen({
  health,
  audits,
  isLoadingAudits,
  isPreviewLoading,
  isAuditLoadingId,
  errorMessage,
  onSelectAudit,
  onLaunchPreview,
  onExploreDemo,
}: LandingScreenProps) {
  const [repoUrl, setRepoUrl] = useState('');

  const isOnline = health?.status === 'ok';

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const trimmed = repoUrl.trim();
    if (!trimmed || isPreviewLoading) return;
    onLaunchPreview(trimmed);
  };

  return (
    <div className="min-h-screen bg-[#FFFFFF] text-[#09090B] flex flex-col">
      <header className="border-b border-[#E4E4E7] bg-[#FFFFFF]">
        <div className="max-w-6xl mx-auto px-6 py-4 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 border border-[#09090B] bg-[#09090B] text-[#FFFFFF] flex items-center justify-center">
              <Orbit className="w-4 h-4" aria-hidden="true" />
            </div>
            <div>
              <h1 className="font-display text-sm font-bold tracking-[0.2em] uppercase text-[#09090B]">
                VKU SPRINTGUARD
              </h1>
              <p className="text-[11px] uppercase tracking-[0.14em] text-[#52525B]">
                3D Repository Telemetry &amp; Audit Mission Control
              </p>
            </div>
          </div>

          <div
            data-testid="landing-health-pill"
            className="inline-flex items-center gap-2 border border-[#E4E4E7] bg-[#FAFAFA] px-3 py-1.5 text-xs font-medium tracking-wider uppercase tabular-nums"
          >
            <span
              className={`w-2 h-2 rounded-full ${isOnline ? 'bg-[#09090B]' : 'bg-[#DC2626]'}`}
              aria-hidden="true"
            />
            <span>
              {isOnline ? `ONLINE · ${health.seeded_audits} SEEDED` : 'OFFLINE'}
            </span>
          </div>
        </div>
      </header>

      <main className="flex-1 orbital-grid">
        <div className="max-w-6xl mx-auto px-6 py-12 space-y-12">
          <section className="max-w-3xl space-y-4">
            <div className="inline-flex items-center gap-2 border border-[#E4E4E7] bg-[#FFFFFF] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.16em] text-[#52525B]">
              <Radio className="w-3.5 h-3.5 text-[#09090B]" aria-hidden="true" />
              <span>Decision Support System · Evidence First</span>
            </div>
            <h2 className="font-display text-3xl sm:text-4xl font-semibold tracking-tight text-[#09090B] leading-tight">
              Inspect repository structure, ownership signals, and weekly sprint velocity in 3D.
            </h2>
            <p className="text-sm sm:text-base text-[#52525B] leading-relaxed">
              VKU SprintGuard is a Decision Support System for lecturers, PMs, and teams — designed
              to surface concrete Git evidence and interview probes,{' '}
              <strong className="font-semibold text-[#09090B]">
                not automated 0–100 grading
              </strong>
              .
            </p>
          </section>

          <section
            aria-label="Live 3D Preview"
            className="border border-[#E4E4E7] bg-[#FFFFFF] p-6 space-y-4"
          >
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div>
                <h3 className="font-display text-xs font-bold uppercase tracking-[0.18em] text-[#09090B]">
                  Live 3D Preview
                </h3>
                <p className="text-xs text-[#52525B] mt-1">
                  Paste any public GitHub repository URL to compute a real-time 3D ownership graph
                  and weekly telemetry strip.
                </p>
              </div>
              <span className="text-[11px] font-medium uppercase tracking-widest text-[#52525B] border border-[#E4E4E7] bg-[#FAFAFA] px-2.5 py-1">
                POST /api/preview
              </span>
            </div>

            <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3">
              <div className="relative flex-1">
                <GitBranch
                  className="w-4 h-4 text-[#52525B] absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none"
                  aria-hidden="true"
                />
                <input
                  type="url"
                  aria-label="GitHub repository URL"
                  value={repoUrl}
                  onChange={(event) => setRepoUrl(event.target.value)}
                  placeholder={SAMPLE_REPO_URL}
                  required
                  className="w-full h-11 pl-10 pr-4 border border-[#E4E4E7] bg-[#FAFAFA] text-sm text-[#09090B] placeholder:text-[#71717A] focus:outline-none focus:border-[#09090B] focus:bg-[#FFFFFF] transition-colors"
                />
              </div>
              <button
                type="submit"
                disabled={isPreviewLoading || !repoUrl.trim()}
                className="h-11 px-5 bg-[#09090B] text-[#FFFFFF] text-xs font-semibold uppercase tracking-[0.14em] inline-flex items-center justify-center gap-2 hover:bg-[#27272A] disabled:opacity-50 disabled:cursor-not-allowed transition-colors cursor-pointer"
              >
                {isPreviewLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" />
                    <span>Computing 3D Graph…</span>
                  </>
                ) : (
                  <>
                    <span>Launch Live 3D Preview</span>
                    <ArrowRight className="w-4 h-4" aria-hidden="true" />
                  </>
                )}
              </button>
            </form>

            <div className="flex flex-wrap items-center gap-2 text-xs text-[#52525B]">
              <span>Quick-fill:</span>
              <button
                type="button"
                onClick={() => setRepoUrl(SAMPLE_REPO_URL)}
                className="border border-[#E4E4E7] bg-[#FAFAFA] hover:border-[#09090B] hover:text-[#09090B] px-2.5 py-1 font-mono text-[11px] transition-colors cursor-pointer"
              >
                {SAMPLE_REPO_URL}
              </button>
            </div>

            {errorMessage && (
              <div
                role="alert"
                className="border border-[#DC2626] bg-[#FFFFFF] px-4 py-3 text-xs text-[#DC2626] flex items-start gap-2.5"
              >
                <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" aria-hidden="true" />
                <span>{errorMessage}</span>
              </div>
            )}
          </section>

          <section aria-label="Pre-Seeded Deep AI Audits" className="space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h3 className="font-display text-xs font-bold uppercase tracking-[0.18em] text-[#09090B] flex items-center gap-2">
                  <Sparkles className="w-3.5 h-3.5" aria-hidden="true" />
                  <span>Pre-Seeded Deep AI Audits</span>
                </h3>
                <p className="text-xs text-[#52525B] mt-1">
                  Curated multi-context benchmarks with signals, critic notes, and targeted
                  interview questions.
                </p>
              </div>
              {(!isOnline || audits.length === 0) && !isLoadingAudits && (
                <button
                  type="button"
                  onClick={onExploreDemo}
                  className="border border-[#09090B] bg-[#FFFFFF] text-[#09090B] hover:bg-[#09090B] hover:text-[#FFFFFF] px-4 py-2 text-xs font-semibold uppercase tracking-[0.14em] transition-colors cursor-pointer"
                >
                  Explore Demo Workspace
                </button>
              )}
            </div>

            {isLoadingAudits ? (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {[0, 1, 2].map((index) => (
                  <div
                    key={index}
                    className="border border-[#E4E4E7] bg-[#FFFFFF] p-5 h-52 animate-pulse flex flex-col justify-between"
                  >
                    <div className="space-y-3">
                      <div className="h-4 w-24 bg-[#E4E4E7]" />
                      <div className="h-5 w-40 bg-[#E4E4E7]" />
                      <div className="h-12 w-full bg-[#FAFAFA]" />
                    </div>
                    <div className="h-9 w-full bg-[#E4E4E7]" />
                  </div>
                ))}
              </div>
            ) : audits.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {audits.map((audit) => {
                  const isOpening = isAuditLoadingId === audit.audit_id;
                  return (
                    <article
                      key={audit.audit_id}
                      data-testid={`seeded-card-${audit.audit_id}`}
                      className="border border-[#E4E4E7] bg-[#FFFFFF] p-5 flex flex-col justify-between gap-5 hover:border-[#09090B] transition-colors"
                    >
                      <div className="space-y-3">
                        <div className="flex items-center justify-between gap-2">
                          <span className="border border-[#09090B] bg-[#FAFAFA] px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.14em] text-[#09090B]">
                            {CONTEXT_LABELS[audit.repo.context]}
                          </span>
                          <span className="text-[11px] text-[#52525B] tabular-nums">
                            {audit.node_count} nodes · {audit.signal_count} signals
                          </span>
                        </div>

                        <div>
                          <h4 className="font-display text-sm font-semibold text-[#09090B] break-words">
                            {audit.repo.name}
                          </h4>
                          <p className="text-xs text-[#52525B] mt-2 line-clamp-3 leading-relaxed">
                            {audit.summary.overview}
                          </p>
                        </div>
                      </div>

                      <button
                        type="button"
                        disabled={Boolean(isAuditLoadingId)}
                        onClick={() => onSelectAudit(audit.audit_id)}
                        className="w-full h-10 border border-[#09090B] bg-[#FFFFFF] text-[#09090B] hover:bg-[#09090B] hover:text-[#FFFFFF] disabled:opacity-50 text-xs font-semibold uppercase tracking-[0.12em] inline-flex items-center justify-center gap-2 transition-colors cursor-pointer"
                      >
                        {isOpening ? (
                          <>
                            <Loader2 className="w-3.5 h-3.5 animate-spin" aria-hidden="true" />
                            <span>Loading Mission Control…</span>
                          </>
                        ) : (
                          <>
                            <Box className="w-3.5 h-3.5" aria-hidden="true" />
                            <span>Open 3D Mission Control</span>
                          </>
                        )}
                      </button>
                    </article>
                  );
                })}
              </div>
            ) : (
              <div className="border border-[#E4E4E7] bg-[#FAFAFA] p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="space-y-1">
                  <p className="text-sm font-medium text-[#09090B]">
                    Backend audit catalog unavailable
                  </p>
                  <p className="text-xs text-[#52525B]">
                    Start the FastAPI backend on localhost:8000 or launch the built-in offline demo
                    workspace to inspect 3D Mission Control.
                  </p>
                </div>
                <button
                  type="button"
                  onClick={onExploreDemo}
                  className="shrink-0 h-10 px-4 bg-[#09090B] text-[#FFFFFF] hover:bg-[#27272A] text-xs font-semibold uppercase tracking-[0.12em] transition-colors cursor-pointer"
                >
                  Explore Demo Workspace
                </button>
              </div>
            )}
          </section>
        </div>
      </main>
    </div>
  );
}
