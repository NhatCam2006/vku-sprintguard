import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import ForceGraph3D, { type ForceGraphMethods } from 'react-force-graph-3d';
import * as THREE from 'three';
import { Focus, RotateCcw, ScanEye, Users } from 'lucide-react';
import type { Graph3DData, GraphNode } from '../types/audit';

interface RenderNode extends GraphNode {
  x?: number;
  y?: number;
  z?: number;
}

interface RenderLink {
  source: string | { id?: string | number };
  target: string | { id?: string | number };
  weight: number;
}

interface Graph3DCanvasProps {
  graphData: Graph3DData;
  selectedNodeId: string | null;
  focusedAuthorId: string | null;
  xRayMode: boolean;
  flyToRequest: { nodeId: string; seq: number } | null;
  onSelectNode: (node: GraphNode) => void;
  onFocusAuthor: (authorId: string | null) => void;
  onResetView: () => void;
}

function resolveEndpointId(endpoint: string | { id?: string | number }): string {
  if (typeof endpoint === 'string') return endpoint;
  return endpoint.id !== undefined ? String(endpoint.id) : '';
}

function getModuleAccentColor(status: GraphNode['status']): string {
  if (status === 'risk') return '#DC2626';
  if (status === 'probe') return '#D97706';
  return '#FFFFFF';
}

export default function Graph3DCanvas({
  graphData,
  selectedNodeId,
  focusedAuthorId,
  xRayMode,
  flyToRequest,
  onSelectNode,
  onFocusAuthor,
  onResetView,
}: Graph3DCanvasProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const fgRef = useRef<ForceGraphMethods | undefined>(undefined);
  const [dimensions, setDimensions] = useState<{ width: number; height: number }>({
    width: 800,
    height: 520,
  });

  useEffect(() => {
    const element = containerRef.current;
    if (!element) return;

    const updateSize = () => {
      const rect = element.getBoundingClientRect();
      if (rect.width > 0 && rect.height > 0) {
        setDimensions({
          width: Math.floor(rect.width),
          height: Math.floor(rect.height),
        });
      }
    };

    updateSize();

    if (typeof ResizeObserver !== 'undefined') {
      const observer = new ResizeObserver(updateSize);
      observer.observe(element);
      return () => observer.disconnect();
    }

    window.addEventListener('resize', updateSize);
    return () => window.removeEventListener('resize', updateSize);
  }, []);

  // Clone nodes & edges so react-force-graph-3d internal object mutation never corrupts React state.
  const clonedGraphData = useMemo<{ nodes: RenderNode[]; links: RenderLink[] }>(() => {
    return {
      nodes: graphData.nodes.map((node) => ({ ...node })),
      links: graphData.edges.map((edge) => ({
        source: edge.source,
        target: edge.target,
        weight: edge.weight,
      })),
    };
  }, [graphData]);

  const authors = useMemo(
    () => graphData.nodes.filter((node) => node.type === 'author'),
    [graphData.nodes],
  );

  // Set of node IDs kept at 100% visibility when Focus Mode is active.
  const focusedNodeIds = useMemo<Set<string> | null>(() => {
    if (!focusedAuthorId) return null;
    const active = new Set<string>([focusedAuthorId]);
    for (const edge of graphData.edges) {
      if (edge.source === focusedAuthorId) active.add(edge.target);
      if (edge.target === focusedAuthorId) active.add(edge.source);
    }
    return active;
  }, [focusedAuthorId, graphData.edges]);

  // Set of node IDs kept at 100% visibility when X-Ray Mode is active (probe/risk modules + connected authors).
  const xRayNodeIds = useMemo<Set<string> | null>(() => {
    if (!xRayMode) return null;
    const flaggedModules = new Set<string>(
      graphData.nodes
        .filter((node) => node.type === 'module' && (node.status === 'probe' || node.status === 'risk'))
        .map((node) => node.id),
    );
    const authorIds = new Set<string>(
      graphData.nodes.filter((node) => node.type === 'author').map((node) => node.id),
    );
    const active = new Set<string>(flaggedModules);
    for (const edge of graphData.edges) {
      if (flaggedModules.has(edge.source) && authorIds.has(edge.target)) {
        active.add(edge.target);
      }
      if (flaggedModules.has(edge.target) && authorIds.has(edge.source)) {
        active.add(edge.source);
      }
    }
    return active;
  }, [xRayMode, graphData.nodes, graphData.edges]);

  useEffect(() => {
    if (!flyToRequest) return;
    const node = clonedGraphData.nodes.find((n) => n.id === flyToRequest.nodeId);
    if (!node) return;

    const x = node.x ?? 0;
    const y = node.y ?? 0;
    const z = node.z ?? 0;
    const camPos =
      x === 0 && y === 0 && z === 0
        ? { x: 0, y: 0, z: 85 }
        : (() => {
            const distRatio = 1 + 85 / Math.hypot(x, y, z);
            return { x: x * distRatio, y: y * distRatio, z: z * distRatio };
          })();

    fgRef.current?.cameraPosition?.(camPos, { x, y, z }, 800);
  }, [flyToRequest, clonedGraphData.nodes]);

  const isNodeDimmed = useCallback(
    (nodeId: string) =>
      Boolean(
        (focusedNodeIds && !focusedNodeIds.has(nodeId)) ||
          (xRayNodeIds && !xRayNodeIds.has(nodeId)),
      ),
    [focusedNodeIds, xRayNodeIds],
  );

  const isLinkHighlighted = useCallback(
    (link: RenderLink) => {
      const sourceId = resolveEndpointId(link.source);
      const targetId = resolveEndpointId(link.target);
      if (focusedAuthorId && sourceId !== focusedAuthorId && targetId !== focusedAuthorId) {
        return false;
      }
      if (xRayNodeIds && (!xRayNodeIds.has(sourceId) || !xRayNodeIds.has(targetId))) {
        return false;
      }
      return true;
    },
    [focusedAuthorId, xRayNodeIds],
  );

  const dimmedColor = xRayMode ? 'rgba(212,212,216,0.10)' : 'rgba(212,212,216,0.12)';
  const dimmedOpacity = xRayMode ? 0.1 : 0.12;

  const nodeColor = useCallback(
    (rawNode: object) => {
      const node = rawNode as RenderNode;
      if (isNodeDimmed(node.id)) return dimmedColor;
      if (node.type === 'author') return '#09090B';
      return getModuleAccentColor(node.status);
    },
    [isNodeDimmed, dimmedColor],
  );

  const linkColor = useCallback(
    (rawLink: object) => {
      const link = rawLink as RenderLink;
      return isLinkHighlighted(link) ? '#D4D4D8' : dimmedColor;
    },
    [isLinkHighlighted, dimmedColor],
  );

  const nodeThreeObject = useCallback(
    (rawNode: object) => {
      if (typeof window === 'undefined') return new THREE.Object3D();
      const node = rawNode as RenderNode;
      const dimmed = isNodeDimmed(node.id);
      const isSelected = selectedNodeId === node.id;
      const baseRadius = Math.max(4, Math.min(11, 3 + Math.sqrt(Math.max(1, node.size)) * 1.4));

      if (node.type === 'author') {
        const geometry = new THREE.OctahedronGeometry(baseRadius * 1.1, 0);
        const material = new THREE.MeshStandardMaterial({
          color: dimmed ? '#D4D4D8' : '#09090B',
          roughness: 0.45,
          metalness: 0.15,
          transparent: dimmed,
          opacity: dimmed ? dimmedOpacity : 1,
        });
        const mesh = new THREE.Mesh(geometry, material);

        if (isSelected && !dimmed) {
          const halo = new THREE.Mesh(
            new THREE.OctahedronGeometry(baseRadius * 1.45, 0),
            new THREE.MeshBasicMaterial({
              color: '#09090B',
              wireframe: true,
            }),
          );
          mesh.add(halo);
        }

        return mesh;
      }

      const group = new THREE.Group();
      const accent = getModuleAccentColor(node.status);
      const sphereGeometry = new THREE.SphereGeometry(baseRadius, 20, 20);
      const sphereMaterial = new THREE.MeshStandardMaterial({
        color: dimmed ? '#D4D4D8' : accent,
        roughness: 0.35,
        metalness: 0.05,
        transparent: dimmed,
        opacity: dimmed ? dimmedOpacity : 1,
      });
      group.add(new THREE.Mesh(sphereGeometry, sphereMaterial));

      // Healthy modules are crisp white spheres framed by a subtle #09090B wireframe ring.
      if (node.status === 'healthy' || isSelected) {
        const wireGeometry = new THREE.SphereGeometry(
          baseRadius * (isSelected ? 1.25 : 1.06),
          12,
          12,
        );
        const wireMaterial = new THREE.MeshBasicMaterial({
          color: dimmed ? '#D4D4D8' : '#09090B',
          wireframe: true,
          transparent: true,
          opacity: dimmed ? dimmedOpacity : isSelected ? 0.85 : 0.45,
        });
        group.add(new THREE.Mesh(wireGeometry, wireMaterial));
      }

      return group;
    },
    [isNodeDimmed, selectedNodeId, dimmedOpacity],
  );

  const handleNodeClick = useCallback(
    (rawNode: object) => {
      const clicked = rawNode as RenderNode;
      const original = graphData.nodes.find((n) => n.id === clicked.id);
      if (!original) return;

      onSelectNode(original);
      if (original.type === 'author') {
        onFocusAuthor(focusedAuthorId === original.id ? null : original.id);
      }
    },
    [focusedAuthorId, graphData.nodes, onFocusAuthor, onSelectNode],
  );

  const handleResetCamera = () => {
    onResetView();
    fgRef.current?.zoomToFit?.(400);
  };

  return (
    <section
      aria-label="3D Ownership Graph Canvas"
      data-testid="graph-wrapper"
      data-focus-author={focusedAuthorId ?? ''}
      data-xray-mode={xRayMode ? 'true' : 'false'}
      data-fly-target={flyToRequest?.nodeId ?? ''}
      ref={containerRef}
      className="relative flex-1 min-h-[380px] orbital-grid overflow-hidden"
    >
      <ForceGraph3D
        ref={fgRef}
        width={dimensions.width}
        height={dimensions.height}
        graphData={clonedGraphData}
        backgroundColor="#FFFFFF"
        nodeLabel={(rawNode) => {
          const node = rawNode as RenderNode;
          return `${node.label} (${node.type} · ${node.status})`;
        }}
        nodeColor={nodeColor}
        nodeThreeObject={nodeThreeObject}
        linkColor={linkColor}
        linkWidth={(rawLink) => {
          const link = rawLink as RenderLink;
          const base = Math.max(0.8, Math.min(3.5, Math.sqrt(Math.max(1, link.weight)) * 0.7));
          return isLinkHighlighted(link) ? base : 0.5;
        }}
        linkOpacity={0.85}
        onNodeClick={handleNodeClick}
      />

      {/* Top-left legend */}
      <div className="pointer-events-none absolute top-3 left-3 border border-[#E4E4E7] bg-[#FFFFFF]/95 px-3 py-2 flex flex-wrap items-center gap-3 text-[10px] uppercase tracking-[0.12em] text-[#52525B]">
        <span className="inline-flex items-center gap-1.5 text-[#09090B] font-semibold">
          <span className="w-2.5 h-2.5 rotate-45 bg-[#09090B] inline-block" aria-hidden="true" />
          Author
        </span>
        <span className="inline-flex items-center gap-1.5">
          <span
            className="w-2.5 h-2.5 rounded-full border border-[#09090B] bg-[#FFFFFF] inline-block"
            aria-hidden="true"
          />
          Healthy
        </span>
        <span className="inline-flex items-center gap-1.5 text-[#D97706] font-semibold">
          <span className="w-2.5 h-2.5 rounded-full bg-[#D97706] inline-block" aria-hidden="true" />
          Probe
        </span>
        <span className="inline-flex items-center gap-1.5 text-[#DC2626] font-semibold">
          <span className="w-2.5 h-2.5 rounded-full bg-[#DC2626] inline-block" aria-hidden="true" />
          Risk
        </span>
      </div>

      {/* Top-right Reset Camera control */}
      <div className="absolute top-3 right-3 flex items-center gap-2">
        {xRayMode && (
          <span
            data-testid="xray-mode-indicator"
            className="border border-[#09090B] bg-[#09090B] text-[#FFFFFF] px-2.5 py-1.5 text-[10px] font-semibold uppercase tracking-[0.14em] inline-flex items-center gap-1.5"
          >
            <ScanEye className="w-3 h-3" aria-hidden="true" />
            <span>X-Ray Active</span>
            <span className="w-1.5 h-1.5 rounded-full bg-[#DC2626]" aria-hidden="true" />
          </span>
        )}
        {focusedAuthorId && (
          <span
            data-testid="focus-mode-indicator"
            className="border border-[#09090B] bg-[#09090B] text-[#FFFFFF] px-2.5 py-1.5 text-[10px] font-semibold uppercase tracking-[0.14em] inline-flex items-center gap-1.5"
          >
            <Focus className="w-3 h-3" aria-hidden="true" />
            <span>Focus Mode</span>
          </span>
        )}
        <button
          type="button"
          onClick={handleResetCamera}
          className="h-8 px-3 border border-[#E4E4E7] bg-[#FFFFFF]/95 hover:border-[#09090B] text-[11px] font-semibold uppercase tracking-[0.12em] text-[#09090B] inline-flex items-center gap-1.5 transition-colors cursor-pointer"
        >
          <RotateCcw className="w-3.5 h-3.5" aria-hidden="true" />
          <span>Reset Camera</span>
        </button>
      </div>

      {/* Bottom-left Filter by Member bar */}
      <div
        aria-label="Filter by Member"
        data-testid="member-filter-bar"
        className="absolute bottom-3 left-3 right-3 pointer-events-none flex items-end justify-between gap-2"
      >
        <div className="pointer-events-auto border border-[#E4E4E7] bg-[#FFFFFF]/95 px-3 py-2 flex flex-wrap items-center gap-1.5 max-w-full">
          <span className="inline-flex items-center gap-1 text-[10px] font-bold uppercase tracking-[0.14em] text-[#52525B] mr-1">
            <Users className="w-3 h-3 text-[#09090B]" aria-hidden="true" />
            Filter by Member:
          </span>

          <button
            type="button"
            onClick={() => onFocusAuthor(null)}
            className={`px-2 py-1 text-[11px] font-medium border transition-colors cursor-pointer ${
              focusedAuthorId === null
                ? 'border-[#09090B] bg-[#09090B] text-[#FFFFFF]'
                : 'border-[#E4E4E7] bg-[#FAFAFA] text-[#52525B] hover:border-[#09090B] hover:text-[#09090B]'
            }`}
          >
            All ({authors.length})
          </button>

          {authors.map((author) => {
            const isFocused = focusedAuthorId === author.id;
            return (
              <button
                key={author.id}
                type="button"
                data-testid={`author-chip-${author.id}`}
                aria-pressed={isFocused}
                onClick={() => {
                  const nextFocus = isFocused ? null : author.id;
                  onFocusAuthor(nextFocus);
                  if (nextFocus) {
                    onSelectNode(author);
                  }
                }}
                className={`px-2 py-1 text-[11px] font-medium border transition-colors cursor-pointer ${
                  isFocused
                    ? 'border-[#09090B] bg-[#09090B] text-[#FFFFFF]'
                    : 'border-[#E4E4E7] bg-[#FAFAFA] text-[#09090B] hover:border-[#09090B]'
                }`}
              >
                {author.label}
              </button>
            );
          })}
        </div>
      </div>
    </section>
  );
}
