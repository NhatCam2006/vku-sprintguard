import ForceGraph3D from 'react-force-graph-3d';

interface SmokeNode {
  id: string;
  label: string;
  type: 'author' | 'module';
  color: string;
}

interface SmokeLink {
  source: string;
  target: string;
}

const SMOKE_GRAPH_DATA: { nodes: SmokeNode[]; links: SmokeLink[] } = {
  nodes: [
    { id: 'author:NhatCam2006', label: 'NhatCam2006', type: 'author', color: '#09090B' },
    { id: 'mod:backend/app', label: 'backend/app', type: 'module', color: '#09090B' },
    { id: 'mod:frontend/src', label: 'frontend/src', type: 'module', color: '#D97706' },
  ],
  links: [
    { source: 'author:NhatCam2006', target: 'mod:backend/app' },
    { source: 'author:NhatCam2006', target: 'mod:frontend/src' },
  ],
};

export default function App() {
  return (
    <main className="min-h-screen bg-[#FFFFFF] text-[#09090B] flex flex-col">
      <header className="border-b border-[#E4E4E7] px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-sm font-bold tracking-widest uppercase text-[#09090B]">
            VKU SPRINTGUARD
          </h1>
          <p className="text-xs text-[#52525B]">
            Interstellar Light Minimalism — Day-1 Node 26 + 3D Graph Smoke Build
          </p>
        </div>
        <span className="text-xs font-mono border border-[#E4E4E7] bg-[#FAFAFA] px-2.5 py-1 rounded">
          M1 Ready
        </span>
      </header>
      <section
        aria-label="3D Graph Smoke Canvas"
        data-testid="graph-wrapper"
        className="flex-1 min-h-[480px] bg-[#FFFFFF] relative overflow-hidden"
      >
        <ForceGraph3D
          graphData={SMOKE_GRAPH_DATA}
          backgroundColor="#FFFFFF"
          linkColor={() => '#D4D4D8'}
          nodeLabel={(node) => (node as SmokeNode).label}
          nodeColor={(node) => (node as SmokeNode).color}
        />
      </section>
    </main>
  );
}
