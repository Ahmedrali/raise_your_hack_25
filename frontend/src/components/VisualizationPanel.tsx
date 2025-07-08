import React, { useEffect, useRef, useState, useCallback } from 'react';
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
  group?: string | number;
}

interface ConnectionLink extends ArchitectureConnection {
  source: ComponentNode;
  target: ComponentNode;
}

// Enhanced helper function for two-layer architecture filtering
const filterByDiagramType = (
  components: any[], 
  connections: any[], 
  diagramType: DiagramType,
  architecture: any
) => {
  switch (diagramType) {
    case 'SYSTEM_OVERVIEW':
      // BUSINESS/LOGICAL VIEW: Focus on business capabilities, data flow, and user interactions
      return {
        filteredComponents: components.filter(c => {
          // Show business-focused components: frontend, business services, main databases
          return ['frontend', 'service', 'database', 'external', 'gateway'].includes(c.type) ||
                 c.businessValue || c.isExternal;
        }).map(c => ({
          ...c,
          businessCapability: getBusinessCapability(c, architecture?.layers?.systemOverview?.businessCapabilities),
          coreSystem: getCoreSystem(c, architecture?.layers?.systemOverview?.coreSystems),
          dataDomain: getDataDomain(c, architecture?.layers?.systemOverview?.dataDomains),
          layerPosition: c.systemOverviewPosition || c.layerAssignments?.system_overview,
          isExternal: isExternalIntegration(c, architecture?.layers?.systemOverview?.externalIntegrations),
          // Business-focused visualization
          displayMode: 'business_logical'
        })),
        filteredConnections: connections.filter(c => 
          // Show business-critical and data flow connections only
          c.dependencyStrength === 'critical' || c.dependencyStrength === 'important' ||
          c.type === 'data-flow' || c.dataFlow
        ),
        layoutStyle: 'business_logical',
        groupingStrategy: 'by_business_domain'
      };
    
    case 'DEPLOYMENT':
      // INFRASTRUCTURE/DEPLOYMENT VIEW: Focus on infrastructure, scaling, security zones
      return {
        filteredComponents: components.filter(c => {
          // Show ALL components including infrastructure: load balancers, caches, monitoring, etc.
          return true; // Don't filter - show complete infrastructure
        }).map(c => ({
          ...c,
          infrastructureZone: getInfrastructureZone(c, architecture?.layers?.deployment?.infrastructureZones),
          containerCluster: getContainerCluster(c, architecture?.layers?.deployment?.containerClusters),
          securityZone: getSecurityZone(c, architecture?.layers?.deployment?.infrastructureZones),
          layerPosition: c.deploymentPosition || c.layerAssignments?.deployment,
          scalingProfile: getScalingProfile(c),
          // Infrastructure-focused visualization
          displayMode: 'infrastructure_deployment'
        })),
        filteredConnections: connections.map(c => ({
          ...c,
          // Show ALL network connections including infrastructure details
          networkPath: c.protocolDisplay,
          securityLevel: c.securityLevel,
          trafficVolume: c.trafficVolume,
          displayMode: 'network_topology'
        })),
        layoutStyle: 'infrastructure_topology',
        groupingStrategy: 'by_infrastructure_layer'
      };

    // Keep existing cases for backward compatibility
    case 'MICROSERVICES':
      return {
        filteredComponents: components.filter(c => c.type === 'service' || c.type === 'gateway'),
        filteredConnections: connections.filter(c => 
          components.some(comp => comp.id === c.fromComponent && (comp.type === 'service' || comp.type === 'gateway')) &&
          components.some(comp => comp.id === c.toComponent && (comp.type === 'service' || comp.type === 'gateway'))
        ),
        layoutStyle: 'cluster'
      };
    case 'DATA_FLOW':
      return {
        filteredComponents: components.filter(c => c.type === 'database' || c.type === 'cache' || c.type === 'service'),
        filteredConnections: connections.filter(c => c.type?.includes('data') || c.protocol?.includes('database')),
        layoutStyle: 'flow'
      };
    case 'SECURITY':
      return {
        filteredComponents: components.filter(c => c.type === 'gateway' || c.type === 'service'),
        filteredConnections: connections.filter(c => c.type?.includes('auth') || c.protocol?.includes('https')),
        layoutStyle: 'security'
      };
    case 'NETWORK':
      return {
        filteredComponents: components,
        filteredConnections: connections,
        layoutStyle: 'network'
      };
    default:
      return {
        filteredComponents: components,
        filteredConnections: connections,
        layoutStyle: 'overview'
      };
  }
};

// Helper functions for System Overview layer
const getBusinessCapability = (component: any, capabilities: any[] = []) => {
  const found = capabilities.find(cap => 
    cap.components?.includes(component.id)
  );
  
  // Fallback for frontend components that might not be properly mapped
  if (!found && (component.type === 'frontend' || component.type === 'ui' || component.type === 'web' || component.type === 'mobile')) {
    return {
      capability: 'User Interface',
      priority: 'high',
      complexity: 'medium',
      user_facing: true
    };
  }
  
  return found;
};

const getCoreSystem = (component: any, coreSystems: any[] = []) => {
  const found = coreSystems.find(sys => 
    sys.components?.includes(component.id)
  );
  
  // Fallback for frontend components that might not be properly mapped
  if (!found && (component.type === 'frontend' || component.type === 'ui' || component.type === 'web' || component.type === 'mobile')) {
    return {
      system: 'User Interface Layer',
      criticality: 'high',
      user_facing: true
    };
  }
  
  return found;
};

const getDataDomain = (component: any, dataDomains: any[] = []) => {
  return dataDomains.find(domain => 
    domain.components?.includes(component.id)
  );
};

const isExternalIntegration = (component: any, externalIntegrations: any[] = []) => {
  return externalIntegrations.some(integration => 
    integration.system === component.name || integration.components?.includes(component.id)
  );
};

// Helper functions for Deployment layer
const getInfrastructureZone = (component: any, zones: any[] = []) => {
  const found = zones.find(zone => 
    zone.components?.includes(component.id)
  );
  
  // Fallback for frontend components that might not be properly mapped
  if (!found && (component.type === 'frontend' || component.type === 'ui' || component.type === 'web' || component.type === 'mobile')) {
    return {
      zone: 'Public Zone',
      zone_type: 'dmz',
      security_level: 'medium',
      network_access: 'public'
    };
  }
  
  return found;
};

const getContainerCluster = (component: any, clusters: any[] = []) => {
  return clusters.find(cluster => 
    cluster.components?.includes(component.id)
  );
};

const getSecurityZone = (component: any, zones: any[] = []) => {
  const zone = zones.find(z => z.components?.includes(component.id));
  return zone?.security_level || 'medium';
};

const getScalingProfile = (component: any) => {
  return {
    type: component.scalingFactors?.[0] || 'horizontal',
    importance: component.visualImportance || 5,
    criticality: component.businessCriticality || 'medium'
  };
};

// Enhanced helper function to get node positions based on layout style and layer
const getNodePosition = (
  index: number, 
  diagramType: DiagramType, 
  layoutStyle: string, 
  width: number, 
  height: number,
  component?: any,
  groupingStrategy?: string,
  components?: any[]
) => {
  const centerX = width / 2;
  const centerY = height / 2;
  const radius = Math.min(width, height) / 3;

  switch (layoutStyle) {
    case 'business_logical':
      // BUSINESS VIEW: Clear layered approach (Frontend -> Services -> Data)
      const componentIndex = components?.findIndex(c => c.id === component?.id) ?? index;
      
      if (component?.type === 'frontend' || component?.type === 'ui' || component?.name?.toLowerCase().includes('frontend')) {
        return {
          x: centerX + (componentIndex % 2 - 0.5) * 300,
          y: 120, // Top layer - Frontend
          group: 'presentation_layer'
        };
      }
      if (component?.type === 'load_balancer' || component?.name?.toLowerCase().includes('load balancer')) {
        return {
          x: centerX - 200,
          y: 200, // Upper middle - Load balancer
          group: 'infrastructure_layer'
        };
      }
      if (component?.type === 'gateway' || component?.name?.toLowerCase().includes('gateway')) {
        return {
          x: centerX,
          y: 250, // Middle layer - Gateway
          group: 'gateway_layer'
        };
      }
      if (component?.type === 'service' || component?.name?.toLowerCase().includes('service')) {
        const serviceCount = components?.filter(c => c.type === 'service' || c.name?.toLowerCase().includes('service')).length || 1;
        const serviceIndex = components?.filter(c => (c.type === 'service' || c.name?.toLowerCase().includes('service')) && c.id <= component.id).length - 1 || 0;
        return {
          x: centerX + (serviceIndex - (serviceCount - 1) / 2) * 200,
          y: centerY + 50, // Business logic layer
          group: 'business_logic_layer'
        };
      }
      if (component?.type === 'cache' || component?.name?.toLowerCase().includes('cache') || component?.name?.toLowerCase().includes('redis')) {
        return {
          x: centerX - 250,
          y: height - 150, // Data layer - Cache
          group: 'data_layer'
        };
      }
      if (component?.type === 'database' || component?.name?.toLowerCase().includes('database') || component?.name?.toLowerCase().includes('mongo')) {
        return {
          x: centerX + 150,
          y: height - 120, // Data layer - Database
          group: 'data_layer'
        };
      }
      if (component?.type === 'external') {
        return {
          x: width - 150,
          y: centerY + (componentIndex % 2 - 0.5) * 100,
          group: 'external_systems'
        };
      }
      break;

    case 'infrastructure_topology':
      // DEPLOYMENT VIEW: Network topology with security zones
      if (component?.infrastructureZone?.zone_type === 'dmz') {
        return {
          x: 120 + (index % 3) * 80,
          y: 120,
          group: 'dmz_zone'
        };
      }
      if (component?.infrastructureZone?.zone_type === 'application') {
        return {
          x: centerX + (index % 4 - 1.5) * 120,
          y: centerY,
          group: 'application_zone'
        };
      }
      if (component?.infrastructureZone?.zone_type === 'data') {
        return {
          x: centerX + (index % 2 - 0.5) * 150,
          y: height - 120,
          group: 'data_zone'
        };
      }
      if (component?.infrastructureZone?.zone_type === 'management') {
        return {
          x: width - 120,
          y: 120 + (index % 3) * 80,
          group: 'management_zone'
        };
      }
      // Infrastructure components (load balancers, monitoring, etc.)
      if (['load_balancer', 'monitoring', 'cache', 'cdn'].includes(component?.type)) {
        return {
          x: 80 + (index % 2) * 120,
          y: centerY + (index % 3 - 1) * 100,
          group: 'infrastructure_layer'
        };
      }
      break;

    case 'business_capability':
      // Legacy fallback
      if (component?.businessCapability) {
        const capIndex = component.businessCapability.priority === 'high' ? 0 : 
                        component.businessCapability.priority === 'medium' ? 1 : 2;
        return {
          x: 150 + (capIndex * 250),
          y: 120 + (component.businessCapability.complexity === 'high' ? 0 : 50),
          group: 'capability'
        };
      }
      break;

    case 'infrastructure_zones':
      // Deployment: Zone-based positioning
      if (component?.infrastructureZone) {
        const zonePositions = {
          'dmz': { x: 100, y: 100 },
          'application': { x: centerX, y: centerY },
          'data': { x: width - 100, y: height - 100 },
          'management': { x: centerX, y: 100 }
        };
        const zonePos = zonePositions[component.infrastructureZone.zone_type] || 
                      zonePositions['application'];
        
        return {
          x: zonePos.x + (Math.random() - 0.5) * 80,
          y: zonePos.y + (Math.random() - 0.5) * 80,
          group: component.infrastructureZone.zone_type
        };
      }
      break;

    case 'hierarchical':
      return {
        x: centerX + (index % 3 - 1) * 150,
        y: 100 + Math.floor(index / 3) * 120
      };
    
    case 'flow':
      return {
        x: 100 + index * (width - 200) / Math.max(1, index),
        y: centerY + Math.sin(index) * 50
      };
    
    case 'cluster':
      const angle = (index * 2 * Math.PI) / 6;
      return {
        x: centerX + Math.cos(angle) * radius,
        y: centerY + Math.sin(angle) * radius
      };
    
    default:
      return {
        x: Math.random() * (width - 200) + 100,
        y: Math.random() * (height - 200) + 100
      };
  }

  // Fallback positioning
  return {
    x: 100 + (index % 4) * 150,
    y: 100 + Math.floor(index / 4) * 120
  };
};

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

  const renderDiagram = useCallback(() => {
    if (!architecture || !svgRef.current || !containerRef.current) {
      console.log('VisualizationPanel: Missing prerequisites', {
        hasArchitecture: !!architecture,
        hasSvgRef: !!svgRef.current,
        hasContainerRef: !!containerRef.current
      });
      return;
    }

    const svg = d3.select(svgRef.current);
    const container = containerRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Clear previous content
    svg.selectAll("*").remove();

    // Set up SVG dimensions
    svg.attr("width", width).attr("height", height);

    // Handle enhanced architecture data structure
    let components = architecture.components || [];
    let connections = architecture.connections || [];
    
    // Architecture data validation - log only if needed for debugging
    if (components.length === 0) {
      console.warn('VisualizationPanel: No components found in architecture data');
    }
    
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

    // Debug logging for architecture data
    console.log('VisualizationPanel: Architecture Debug', {
      originalComponentsCount: components.length,
      componentTypes: components.map(c => c.type),
      componentNames: components.map(c => c.name),
      diagramType,
      hasArchitecture: !!architecture,
      architectureKeys: architecture ? Object.keys(architecture) : [],
      hasVisualizationData: !!(architecture?.visualization_data),
      hasD3Data: !!(architecture?.visualization_data?.d3_data)
    });

    // Enhanced filtering and adjustment based on diagram type
    const { filteredComponents, filteredConnections, layoutStyle, groupingStrategy } = filterByDiagramType(
      components, 
      connections, 
      diagramType,
      architecture
    );

    console.log('VisualizationPanel: After Filtering', {
      filteredComponentsCount: filteredComponents.length,
      filteredComponentTypes: filteredComponents.map(c => c.type),
      filteredComponentNames: filteredComponents.map(c => c.name)
    });

    // Validation: Ensure we have components to render
    if (filteredComponents.length === 0) {
      console.warn('VisualizationPanel: No components after filtering for', diagramType);
      return;
    }

    // Create zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 3])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
        setZoomLevel(event.transform.k);
      });

    svg.call(zoom);

    // Add diagram type indicator
    svg.append("text")
      .attr("x", 10)
      .attr("y", 25)
      .attr("font-size", "14px")
      .attr("font-weight", "600")
      .attr("fill", "#667eea")
      .text(`${diagramType.replace('_', ' ')} View`);

    // Create main group for zoomable content
    const g = svg.append("g");

    // Prepare data using enhanced filtered components and connections
    const nodes: ComponentNode[] = filteredComponents.map((comp, index) => {
      const position = getNodePosition(index, diagramType, layoutStyle, width, height, comp, groupingStrategy, filteredComponents);
      return {
        ...comp,
        x: position.x,
        y: position.y,
        group: position.group || comp.group
      };
    });

    // Nodes created successfully
    if (nodes.length === 0) {
      console.warn('VisualizationPanel: No nodes created for rendering');
    }

    // If no nodes, render a debug message
    if (nodes.length === 0) {
      console.log('VisualizationPanel: No nodes to render, showing debug info');
      g.append("text")
        .attr("x", width / 2)
        .attr("y", height / 2)
        .attr("text-anchor", "middle")
        .attr("font-size", "16px")
        .attr("fill", "#e53e3e")
        .text(`No components found. Components: ${components.length}, Diagram: ${diagramType}`);
      
      // Add debugging info
      g.append("text")
        .attr("x", width / 2)
        .attr("y", height / 2 + 30)
        .attr("text-anchor", "middle")
        .attr("font-size", "12px")
        .attr("fill", "#718096")
        .text(`Architecture object: ${JSON.stringify(architecture).substring(0, 100)}...`);
      
      return;
    }

    const links: ConnectionLink[] = filteredConnections.map(conn => {
      const source = nodes.find(n => n.id === conn.fromComponent);
      const target = nodes.find(n => n.id === conn.toComponent);
      return {
        ...conn,
        source: source!,
        target: target!
      };
    }).filter(link => link.source && link.target);

    console.log('VisualizationPanel: Connection Debug', {
      filteredConnectionsCount: filteredConnections.length,
      linksCreated: links.length,
      sampleConnections: filteredConnections.slice(0, 3),
      sampleLinks: links.slice(0, 3)
    });

    // Create force simulation - disable for business logical view to maintain layer positioning
    const useForceSimulation = layoutStyle !== 'business_logical';
    
    const simulation = useForceSimulation 
      ? d3.forceSimulation(nodes)
          .force("link", d3.forceLink(links).id((d: any) => d.id).distance(150))
          .force("charge", d3.forceManyBody().strength(-300))
          .force("center", d3.forceCenter(width / 2, height / 2))
          .force("collision", d3.forceCollide().radius(60))
      : d3.forceSimulation(nodes)
          .force("collision", d3.forceCollide().radius(60)) // Only collision detection
          .alpha(0) // Immediately stop simulation
          .stop();

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

    // Add enhanced node circles with business criticality sizing
    node.append("circle")
      .attr("r", (d: ComponentNode) => {
        const baseSize = 40;
        const importance = d.visualImportance || 5;
        const criticalityMultiplier = d.businessCriticality === 'high' ? 1.2 : 
                                     d.businessCriticality === 'low' ? 0.8 : 1;
        return baseSize * (importance / 5) * criticalityMultiplier;
      })
      .attr("fill", (d: ComponentNode) => getEnhancedComponentColor(d))
      .attr("stroke", (d: ComponentNode) => {
        if (d.businessCriticality === 'high') return "#f56565";
        if (d.isExternal) return "#805ad5";
        return "#ffffff";
      })
      .attr("stroke-width", (d: ComponentNode) => d.businessCriticality === 'high' ? 4 : 3)
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
    const updatePositions = () => {
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
    };

    if (useForceSimulation) {
      simulation.on("tick", updatePositions);
    } else {
      // For business logical view, update positions immediately
      updatePositions();
    }

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
  }, [architecture, diagramType, onDiagramTypeChange]);

  useEffect(() => {
    if (architecture && svgRef.current && containerRef.current) {
      renderDiagram();
    }
  }, [architecture, diagramType, renderDiagram]);

  const getComponentColor = (type: string): string => {
    const colors: Record<string, string> = {
      'service': '#667eea',
      'database': '#48bb78',
      'cache': '#ed8936',
      'gateway': '#9f7aea',
      'ui': '#38b2ac',
      'external': '#718096',
      'frontend': '#38b2ac'
    };
    return colors[type] || '#718096';
  };

  const getEnhancedComponentColor = (component: ComponentNode): string => {
    // Layer-specific coloring
    if (diagramType === 'SYSTEM_OVERVIEW') {
      if (component.isExternal) return '#805ad5'; // Purple for external
      if (component.businessCapability?.priority === 'high') return '#e53e3e'; // Red for high priority
      if (component.coreSystem?.criticality === 'high') return '#38a169'; // Green for critical systems
    }
    
    if (diagramType === 'DEPLOYMENT') {
      const zoneColors = {
        'dmz': '#e53e3e',        // Red for DMZ
        'application': '#667eea', // Blue for application tier
        'data': '#48bb78',        // Green for data tier
        'management': '#ed8936'   // Orange for management
      };
      if (component.infrastructureZone?.zone_type) {
        return zoneColors[component.infrastructureZone.zone_type] || '#667eea';
      }
    }
    
    // Fallback to original coloring
    return getComponentColor(component.type);
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
            <option value="SYSTEM_OVERVIEW">📋 System Overview</option>
            <option value="DEPLOYMENT">🏗️ Deployment Architecture</option>
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
          <option value="SYSTEM_OVERVIEW">📋 System Overview</option>
          <option value="DEPLOYMENT">🏗️ Deployment Architecture</option>
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
