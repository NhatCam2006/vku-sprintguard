import { Activity, AlertTriangle } from 'lucide-react';
import type { TimelineWeek } from '../types/audit';

interface Timeline2DProps {
  weeks: TimelineWeek[];
}

export default function Timeline2D({ weeks }: Timeline2DProps) {
  const maxCommits = Math.max(1, ...weeks.map((week) => week.commits));
  const anomalyCount = weeks.filter((week) => week.anomaly).length;

  return (
    <section
      aria-label="2D Weekly Commit Telemetry"
      data-testid="timeline-2d"
      className="border-t border-[#E4E4E7] bg-[#FFFFFF] px-4 py-3 shrink-0"
    >
      <div className="flex items-center justify-between gap-2 mb-2.5">
        <div className="flex items-center gap-2">
          <Activity className="w-3.5 h-3.5 text-[#09090B]" aria-hidden="true" />
          <h2 className="font-display text-[11px] font-bold uppercase tracking-[0.16em] text-[#09090B]">
            Weekly Commit Telemetry
          </h2>
        </div>
        <div className="flex items-center gap-3 text-[11px] text-[#52525B] tabular-nums">
          <span>{weeks.length} weeks</span>
          {anomalyCount > 0 && (
            <span className="inline-flex items-center gap-1 text-[#DC2626] font-semibold uppercase tracking-wider">
              <AlertTriangle className="w-3 h-3" aria-hidden="true" />
              {anomalyCount} anomaly
            </span>
          )}
        </div>
      </div>

      {weeks.length === 0 ? (
        <p className="text-xs text-[#52525B] py-4">No weekly commit telemetry available.</p>
      ) : (
        <div className="flex items-end gap-2.5 overflow-x-auto pb-1">
          {weeks.map((week) => {
            const heightPercent = Math.max(14, Math.round((week.commits / maxCommits) * 100));
            return (
              <div
                key={week.week}
                data-testid={`timeline-week-${week.week}`}
                data-anomaly={week.anomaly ? 'true' : 'false'}
                className={`min-w-[104px] flex-1 border px-2.5 py-2 flex flex-col justify-between gap-1.5 ${
                  week.anomaly
                    ? 'border-[#DC2626] bg-[#FFFFFF]'
                    : 'border-[#E4E4E7] bg-[#FAFAFA]'
                }`}
              >
                <div className="flex items-center justify-between gap-1">
                  <span
                    className={`font-display text-[11px] font-semibold tabular-nums ${
                      week.anomaly ? 'text-[#DC2626]' : 'text-[#09090B]'
                    }`}
                  >
                    {week.week}
                  </span>
                  {week.anomaly && (
                    <span className="bg-[#DC2626] text-[#FFFFFF] px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-wider">
                      ANOMALY
                    </span>
                  )}
                </div>

                <div className="h-10 flex items-end gap-1.5">
                  <div className="w-full h-full bg-[#E4E4E7]/50 flex items-end">
                    <div
                      style={{ height: `${heightPercent}%` }}
                      className={`w-full transition-all ${
                        week.anomaly ? 'bg-[#DC2626]' : 'bg-[#18181B]'
                      }`}
                    />
                  </div>
                </div>

                <div className="flex items-center justify-between text-[10px] tabular-nums">
                  <span
                    className={`font-semibold ${
                      week.anomaly ? 'text-[#DC2626]' : 'text-[#18181B]'
                    }`}
                  >
                    {week.commits} commits
                  </span>
                  <span className="text-[#71717A]">
                    +{week.additions}/-{week.deletions}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}
