import { useCallback, useEffect, useMemo, useState } from 'react';
import { AlertCircle } from 'lucide-react';
import {
  FALLBACK_AUDIT_REPORT,
  fetchAuditById,
  fetchAudits,
  fetchHealth,
  runLivePreview,
} from './api/client';
import Graph3DCanvas from './components/Graph3DCanvas';
import LandingScreen from './components/LandingScreen';
import SideInspector, { type InspectorTab } from './components/SideInspector';
import Timeline2D from './components/Timeline2D';
import TopBar from './components/TopBar';
import type { AuditListItem, AuditReport, GraphNode, HealthResponse } from './types/audit';

export default function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [audits, setAudits] = useState<AuditListItem[]>([]);
  const [isLoadingAudits, setIsLoadingAudits] = useState(true);

  const [activeReport, setActiveReport] = useState<AuditReport | null>(null);
  const [isPreviewLoading, setIsPreviewLoading] = useState(false);
  const [isAuditLoadingId, setIsAuditLoadingId] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [inspectorTab, setInspectorTab] = useState<InspectorTab>('overview');
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [focusedAuthorId, setFocusedAuthorId] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    async function loadBootstrap() {
      setIsLoadingAudits(true);
      const [healthResult, auditsResult] = await Promise.allSettled([
        fetchHealth(),
        fetchAudits(),
      ]);

      if (!isMounted) return;

      if (healthResult.status === 'fulfilled') {
        setHealth(healthResult.value);
      } else {
        setHealth(null);
      }

      if (auditsResult.status === 'fulfilled') {
        setAudits(auditsResult.value);
      } else {
        setAudits([]);
      }

      setIsLoadingAudits(false);
    }

    void loadBootstrap();

    return () => {
      isMounted = false;
    };
  }, []);

  const enterMissionControl = useCallback((report: AuditReport) => {
    setActiveReport(report);
    setSelectedNodeId(null);
    setFocusedAuthorId(null);
    setInspectorTab('overview');
    setErrorMessage(null);
  }, []);

  const handleSelectAudit = useCallback(
    async (auditId: string) => {
      setIsAuditLoadingId(auditId);
      setErrorMessage(null);
      try {
        const report = await fetchAuditById(auditId);
        enterMissionControl(report);
      } catch (err) {
        const message =
          err instanceof Error ? err.message : 'Unable to load the selected audit report.';
        setErrorMessage(message);
      } finally {
        setIsAuditLoadingId(null);
      }
    },
    [enterMissionControl],
  );

  const handleLaunchPreview = useCallback(
    async (repoUrl: string) => {
      setIsPreviewLoading(true);
      setErrorMessage(null);
      try {
        const report = await runLivePreview(repoUrl);
        enterMissionControl(report);
      } catch (err) {
        const message =
          err instanceof Error ? err.message : 'Live 3D Preview request failed.';
        setErrorMessage(message);
      } finally {
        setIsPreviewLoading(false);
      }
    },
    [enterMissionControl],
  );

  const handleExploreDemo = useCallback(() => {
    enterMissionControl(FALLBACK_AUDIT_REPORT);
  }, [enterMissionControl]);

  const handleSelectNode = useCallback((node: GraphNode) => {
    setSelectedNodeId(node.id);
    setInspectorTab('signals');
  }, []);

  const handleSelectNodeId = useCallback((nodeId: string) => {
    setSelectedNodeId(nodeId);
    setInspectorTab('signals');
  }, []);

  const handleResetView = useCallback(() => {
    setSelectedNodeId(null);
    setFocusedAuthorId(null);
  }, []);

  const selectedNode = useMemo(() => {
    if (!activeReport || !selectedNodeId) return null;
    return activeReport.graph_3d.nodes.find((node) => node.id === selectedNodeId) ?? null;
  }, [activeReport, selectedNodeId]);

  if (!activeReport) {
    return (
      <LandingScreen
        health={health}
        audits={audits}
        isLoadingAudits={isLoadingAudits}
        isPreviewLoading={isPreviewLoading}
        isAuditLoadingId={isAuditLoadingId}
        errorMessage={errorMessage}
        onSelectAudit={(id) => void handleSelectAudit(id)}
        onLaunchPreview={(url) => void handleLaunchPreview(url)}
        onExploreDemo={handleExploreDemo}
      />
    );
  }

  return (
    <div className="h-screen bg-[#FFFFFF] text-[#09090B] flex flex-col overflow-hidden">
      <TopBar
        report={activeReport}
        audits={audits}
        health={health}
        isPreviewLoading={isPreviewLoading}
        onBackToLanding={() => {
          setActiveReport(null);
          setErrorMessage(null);
        }}
        onSelectAudit={(id) => void handleSelectAudit(id)}
        onLaunchPreview={(url) => void handleLaunchPreview(url)}
      />

      {errorMessage && (
        <div
          role="alert"
          className="border-b border-[#DC2626] bg-[#FFFFFF] px-4 py-2 text-xs text-[#DC2626] flex items-center gap-2 shrink-0"
        >
          <AlertCircle className="w-3.5 h-3.5 shrink-0" aria-hidden="true" />
          <span>{errorMessage}</span>
        </div>
      )}

      <main className="flex-1 flex flex-col lg:flex-row min-h-0 overflow-hidden">
        <div className="flex-1 lg:w-[66%] flex flex-col min-h-0 overflow-hidden">
          <Graph3DCanvas
            graphData={activeReport.graph_3d}
            selectedNodeId={selectedNodeId}
            focusedAuthorId={focusedAuthorId}
            onSelectNode={handleSelectNode}
            onFocusAuthor={setFocusedAuthorId}
            onResetView={handleResetView}
          />
          <Timeline2D weeks={activeReport.timeline_2d} />
        </div>

        <SideInspector
          report={activeReport}
          activeTab={inspectorTab}
          selectedNode={selectedNode}
          onTabChange={setInspectorTab}
          onSelectNodeId={handleSelectNodeId}
        />
      </main>
    </div>
  );
}
