import React, { useEffect, useRef, useState } from 'react';
import styled from 'styled-components';
import * as d3 from 'd3';
import { VisualizationPanelProps, DiagramType, ArchitectureComponent, ArchitectureConnection } from '../types';

const PanelContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
`;

const PanelHeader = styled.div`
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const PanelTitle = styled.h3`
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #2d3748;
`;

const DiagramTypeSelect = styled.select`
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9rem;
  background: white;
  cursor: pointer;

  &:focus {
    outline: none;
    border-color: #667eea;
  }
`;

const VisualizationContainer = styled.div`
  flex: 1;
  position: relative;
  overflow: hidden;
`;

const SVGContainer = styled.div`
  width: 100%;
  height: 100%;
  
  svg {
    width: 100%;
    height: 100%;
  }
`;

const EmptyState = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #718096;
  padding: 2rem;
`;

const EmptyStateIcon = styled.div`
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
`;

const LoadingSpinner = styled.div`
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top: 3px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const ComponentTooltip = styled.div`
  position: absolute;
  background: rgba(0, 0, 0, 0.9);
  color: white;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.85rem;
  pointer-events: none;
  z-index: 1000;
  max-width: 250px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const Controls = styled.div`
  padding: 0.75rem 1.5rem;
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
  display: flex;
  gap: 0.5rem;
  align-items: center;
`;

const ControlButton = styled.button`
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    background: #f7fafc;
  }

  &:active {
    background: #edf2f7;
  }
`;

const ZoomInfo = styled.span`
  font-size: 0.8rem;
  color: #718096;
  margin-left: auto;
`;

interface ComponentNode extends ArchitectureComponent {
  x?: number;
  y?: number;
  fx?: number | null;
  fy?: number | null;
}

interface ConnectionLink extends ArchitectureConnection {
  source: ComponentNode;
  target: ComponentNode;
}

const VisualizationPanel: React.FC<VisualizationPanelProps> = ({
  architecture,
  diagramType,
  onDiagramTypeChange,
  isLoading
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [tooltip, setTooltip] = useState<{ x: number; y: number; content: string } | null>(null);
  const [zoomLevel, setZoomLevel] = useState(1);

  useEffect(() => {
    if (architecture && svgRef.current && containerRef.current) {
      renderDiagram();
    }
  }, [architecture, diagramType]);

  const renderDiagram = () => {
    if (!architecture || !svgRef.current || !containerRef.current) return;

    const svg = d3.select(svgRef.current);
    const container = containerRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Clear previous content
    svg.selectAll("*").remove();

    // Set up SVG dimensions
    svg.attr("width", width).attr("height", height);

    // Create zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 3])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
        setZoomLevel(event.transform.k);
      });

    svg.call(zoom);

    // Create main group for zoomable content
    const g = svg.append("g");

    // Handle enhanced architecture data structure
    let components = architecture.components || [];
    let connections = architecture.connections || [];
    
    // Check if we have visualization_data from the new architecture agent
    if (architecture.visualization_data?.d3_data) {
      const d3Data = architecture.visualization_data.d3_data;
      components = d3Data.nodes?.map((node: any) => ({
        id: node.id,
        name: node.name,
        type: node.type,
        description: node.description || '',
        responsibilities: [node.description || ''],
        technologies: [node.technology || ''],
        scalingFactors: [],
        businessValue: ''
      })) || components;
      
      connections = d3Data.links?.map((link: any) => ({
        id: `${link.source}-${link.target}`,
        fromComponent: link.source,
        toComponent: link.target,
        type: link.type,
        protocol: link.type,
        description: link.description || '',
        dataFlow: null
      })) || connections;
    }

    // Prepare data
    const nodes: ComponentNode[] = components.map((comp, index) => ({
      ...comp,
      x: architecture.visualization_data?.d3_data?.nodes?.[index]?.x || Math.random() * (width - 200) + 100,
      y: architecture.visualization_data?.d3_data?.nodes?.[index]?.y || Math.random() * (height - 200) + 100
    }));

    const links: ConnectionLink[] = connections.map(conn => {
      const source = nodes.find(n => n.id === conn.fromComponent);
      const target = nodes.find(n => n.id === conn.toComponent);
      return {
        ...conn,
        source: source!,
        target: target!
      };
    }).filter(link => link.source && link.target);

    // Create force simulation
    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id((d: any) => d.id).distance(150))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(60));

    // Create links
    const link = g.append("g")
      .selectAll("line")
      .data(links)
      .enter().append("line")
      .attr("stroke", "#94a3b8")
      .attr("stroke-width", 2)
      .attr("stroke-dasharray", (d: ConnectionLink) => 
        d.type === 'asynchronous' ? "5,5" : "none"
      );

    // Create link labels
    const linkLabels = g.append("g")
      .selectAll("text")
      .data(links)
      .enter().append("text")
      .attr("font-size", "10px")
      .attr("fill", "#64748b")
      .attr("text-anchor", "middle")
      .text((d: ConnectionLink) => d.protocol);

    // Create nodes
    const node = g.append("g")
      .selectAll("g")
      .data(nodes)
      .enter().append("g")
      .attr("cursor", "pointer")
      .call(d3.drag<SVGGElement, ComponentNode>()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));

    // Add node circles
    node.append("circle")
      .attr("r", 40)
      .attr("fill", (d: ComponentNode) => getComponentColor(d.type))
      .attr("stroke", "#ffffff")
      .attr("stroke-width", 3)
      .attr("filter", "drop-shadow(0 2px 4px rgba(0,0,0,0.1))");

    // Add node labels
    node.append("text")
      .attr("text-anchor", "middle")
      .attr("dy", "0.35em")
      .attr("font-size", "11px")
      .attr("font-weight", "600")
      .attr("fill", "white")
      .text((d: ComponentNode) => truncateText(d.name, 12));

    // Add node type labels
    node.append("text")
      .attr("text-anchor", "middle")
      .attr("dy", "1.5em")
      .attr("font-size", "8px")
      .attr("fill", "rgba(255,255,255,0.8)")
      .text((d: ComponentNode) => d.type.toUpperCase());

    // Add hover effects
    node
      .on("mouseenter", (event, d: ComponentNode) => {
        const [x, y] = d3.pointer(event, container);
        setTooltip({
          x: x + 10,
          y: y - 10,
          content: `${d.name}\nType: ${d.type}\nResponsibilities: ${d.responsibilities.slice(0, 2).join(', ')}\nTechnologies: ${d.technologies.slice(0, 2).join(', ')}`
        });
      })
      .on("mouseleave", () => {
        setTooltip(null);
      });

    // Update positions on simulation tick
    simulation.on("tick", () => {
      link
        .attr("x1", (d: any) => d.source.x)
        .attr("y1", (d: any) => d.source.y)
        .attr("x2", (d: any) => d.target.x)
        .attr("y2", (d: any) => d.target.y);

      linkLabels
        .attr("x", (d: any) => (d.source.x + d.target.x) / 2)
        .attr("y", (d: any) => (d.source.y + d.target.y) / 2);

      node
        .attr("transform", (d: ComponentNode) => `translate(${d.x},${d.y})`);
    });

    // Drag functions
    function dragstarted(event: any, d: ComponentNode) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event: any, d: ComponentNode) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event: any, d: ComponentNode) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
  };

  const getComponentColor = (type: string): string => {
    const colors: Record<string, string> = {
      'service': '#667eea',
      'database': '#48bb78',
      'cache': '#ed8936',
      'gateway': '#9f7aea',
      'ui': '#38b2ac',
      'external': '#718096'
    };
    return colors[type] || '#718096';
  };

  const truncateText = (text: string, maxLength: number): string => {
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
  };

  const handleZoomIn = () => {
    if (svgRef.current) {
      const svg = d3.select(svgRef.current);
      svg.transition().call(
        d3.zoom<SVGSVGElement, unknown>().scaleBy as any,
        1.5
      );
    }
  };

  const handleZoomOut = () => {
    if (svgRef.current) {
      const svg = d3.select(svgRef.current);
      svg.transition().call(
        d3.zoom<SVGSVGElement, unknown>().scaleBy as any,
        1 / 1.5
      );
    }
  };

  const handleResetZoom = () => {
    if (svgRef.current) {
      const svg = d3.select(svgRef.current);
      svg.transition().call(
        d3.zoom<SVGSVGElement, unknown>().transform as any,
        d3.zoomIdentity
      );
    }
  };

  if (isLoading) {
    return (
      <PanelContainer>
        <PanelHeader>
          <PanelTitle>Architecture Visualization</PanelTitle>
        </PanelHeader>
        <EmptyState>
          <LoadingSpinner />
          <p>Generating architecture diagram...</p>
        </EmptyState>
      </PanelContainer>
    );
  }

  if (!architecture) {
    return (
      <PanelContainer>
        <PanelHeader>
          <PanelTitle>Architecture Visualization</PanelTitle>
          <DiagramTypeSelect
            value={diagramType}
            onChange={(e) => onDiagramTypeChange(e.target.value as DiagramType)}
          >
            <option value="SYSTEM_OVERVIEW">System Overview</option>
            <option value="MICROSERVICES">Microservices</option>
            <option value="DATA_FLOW">Data Flow</option>
            <option value="DEPLOYMENT">Deployment</option>
            <option value="SECURITY">Security</option>
            <option value="NETWORK">Network</option>
          </DiagramTypeSelect>
        </PanelHeader>
        <EmptyState>
          <EmptyStateIcon>🏗️</EmptyStateIcon>
          <h4>No architecture to visualize</h4>
          <p>Start a conversation to generate architecture diagrams and visualizations.</p>
        </EmptyState>
      </PanelContainer>
    );
  }

  return (
    <PanelContainer>
      <PanelHeader>
        <PanelTitle>Architecture Visualization</PanelTitle>
        <DiagramTypeSelect
          value={diagramType}
          onChange={(e) => onDiagramTypeChange(e.target.value as DiagramType)}
        >
          <option value="SYSTEM_OVERVIEW">System Overview</option>
          <option value="MICROSERVICES">Microservices</option>
          <option value="DATA_FLOW">Data Flow</option>
          <option value="DEPLOYMENT">Deployment</option>
          <option value="SECURITY">Security</option>
          <option value="NETWORK">Network</option>
        </DiagramTypeSelect>
      </PanelHeader>

      <VisualizationContainer ref={containerRef}>
        <SVGContainer>
          <svg ref={svgRef}></svg>
        </SVGContainer>
        
        {tooltip && (
          <ComponentTooltip
            style={{
              left: tooltip.x,
              top: tooltip.y
            }}
          >
            {tooltip.content.split('\n').map((line, index) => (
              <div key={index}>{line}</div>
            ))}
          </ComponentTooltip>
        )}
      </VisualizationContainer>

      <Controls>
        <ControlButton onClick={handleZoomIn}>Zoom In</ControlButton>
        <ControlButton onClick={handleZoomOut}>Zoom Out</ControlButton>
        <ControlButton onClick={handleResetZoom}>Reset</ControlButton>
        <ZoomInfo>Zoom: {Math.round(zoomLevel * 100)}%</ZoomInfo>
      </Controls>
    </PanelContainer>
  );
};

export default VisualizationPanel;
