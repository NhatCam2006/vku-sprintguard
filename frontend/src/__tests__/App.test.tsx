import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import App from '../App';

vi.mock('react-force-graph-3d', () => ({
  default: ({ graphData }: { graphData: { nodes: unknown[]; links: unknown[] } }) => (
    <div
      data-testid="mock-force-graph-3d"
      data-node-count={graphData.nodes.length}
      data-link-count={graphData.links.length}
    />
  ),
}));

describe('App Day-1 Smoke Render', () => {
  it('renders VKU SPRINTGUARD heading and 3D graph wrapper', () => {
    render(<App />);
    expect(screen.getByRole('heading', { name: /VKU SPRINTGUARD/i })).toBeInTheDocument();
    expect(screen.getByTestId('graph-wrapper')).toBeInTheDocument();
    const mockGraph = screen.getByTestId('mock-force-graph-3d');
    expect(mockGraph).toHaveAttribute('data-node-count', '3');
    expect(mockGraph).toHaveAttribute('data-link-count', '2');
  });
});
