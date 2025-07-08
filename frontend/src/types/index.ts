// User and Authentication Types
export interface User {
  id: string;
  email: string;
  firstName?: string;
  lastName?: string;
  expertiseLevel: ExpertiseLevel;
  businessRole?: string;
  businessContext?: BusinessContext;
  preferences?: UserPreferences;
  createdAt: string;
}

export type ExpertiseLevel = 'BEGINNER' | 'INTERMEDIATE' | 'ADVANCED' | 'EXPERT';

export interface BusinessContext {
  industry?: string;
  companySize?: 'startup' | 'small' | 'medium' | 'large' | 'enterprise';
  budgetRange?: 'limited' | 'moderate' | 'significant' | 'unlimited';
  timeline?: 'immediate' | 'weeks' | 'months' | 'flexible';
  compliance?: string[];
  existingTech?: string[];
}

export interface UserPreferences {
  visualizationStyle?: 'modern' | 'classic' | 'minimal';
  explanationDepth?: 'brief' | 'detailed' | 'comprehensive';
  businessFocus?: boolean;
  technicalDepth?: 'high' | 'medium' | 'low';
}

// Conversation Types
export interface Conversation {
  id: string;
  title: string;
  status: 'ACTIVE' | 'COMPLETED' | 'PAUSED' | 'ARCHIVED';
  userRequirements: string;
  userContext: ConversationUserContext;
  workflowType: WorkflowType;
  createdAt: string;
  updatedAt: string;
  messages: ConversationMessage[];
  architectures?: Architecture[];
}

export type WorkflowType = 'SEQUENTIAL' | 'PARALLEL' | 'CONDITIONAL' | 'ITERATIVE';

export interface ConversationUserContext {
  expertise: ExpertiseLevel;
  businessRole?: string;
  businessContext?: BusinessContext;
  projectType?: string;
  timeline?: string;
  budget?: string;
  existingConstraints?: string[];
}

export interface ConversationMessage {
  id: string;
  role: 'USER' | 'ASSISTANT' | 'SYSTEM';
  content: string;
  messageType: 'TEXT' | 'ARCHITECTURE_UPDATE' | 'EDUCATIONAL_CONTENT' | 'BUSINESS_ANALYSIS' | 'WHY_REASONING';
  metadata?: Record<string, any>;
  timestamp: string;
  sequenceNumber: number;
}

// Architecture Types
export interface Architecture {
  id: string;
  title: string;
  description?: string;
  architectureData: ArchitectureData;
  diagramType: DiagramType;
  whyReasoning: WhyReasoning;
  businessImpact: BusinessImpact;
  status: 'DRAFT' | 'REVIEW' | 'APPROVED' | 'IMPLEMENTED';
  createdAt: string;
  updatedAt: string;
}

export type DiagramType = 'SYSTEM_OVERVIEW' | 'MICROSERVICES' | 'DATA_FLOW' | 'DEPLOYMENT' | 'SECURITY' | 'NETWORK';

export interface ArchitectureData {
  components: ArchitectureComponent[];
  connections: ArchitectureConnection[];
  layers: ArchitectureLayer[] | {
    systemOverview?: {
      businessCapabilities?: Array<{
        capability: string;
        components: string[];
        business_value: string;
        complexity: 'low' | 'medium' | 'high';
        priority: 'high' | 'medium' | 'low';
      }>;
      coreSystems?: Array<{
        system: string;
        components: string[];
        purpose: string;
        criticality: 'high' | 'medium' | 'low';
        user_facing: boolean;
      }>;
      externalIntegrations?: Array<{
        system: string;
        type: 'third_party' | 'internal' | 'saas';
        data_flow: 'inbound' | 'outbound' | 'bidirectional';
        security_level: 'high' | 'medium' | 'low';
        dependency_level: 'critical' | 'important' | 'optional';
      }>;
      dataDomains?: Array<{
        domain: string;
        components: string[];
        sensitivity: 'high' | 'medium' | 'low';
        data_types: string[];
      }>;
    };
    deployment?: {
      infrastructureZones?: Array<{
        zone: string;
        components: string[];
        security_level: 'high' | 'medium' | 'low';
        network_access: 'public' | 'private' | 'isolated';
        zone_type: 'dmz' | 'application' | 'data' | 'management';
      }>;
      containerClusters?: Array<{
        cluster: string;
        components: string[];
        scaling: 'auto' | 'manual' | 'none';
        replicas: string;
        resource_requirements: 'high' | 'medium' | 'low';
      }>;
      networkTopology?: {
        load_balancers?: Array<{
          name: string;
          type: 'application' | 'network';
          targets: string[];
        }>;
        security_groups?: Array<{
          name: string;
          components: string[];
          rules: string[];
        }>;
      };
    };
  };
  patterns: ArchitecturePattern[];
  technologies: TechnologyChoice[];
  metadata: Record<string, any>;
  diagramTypes?: string[];
  visualizationMetadata?: {
    total_components?: number;
    total_connections?: number;
    complexity_score?: number;
    recommended_default_view?: string;
  };
  layerData?: {
    system_overview?: {
      layout_type?: string;
      grouping_strategy?: string;
    };
    deployment?: {
      layout_type?: string;
      grouping_strategy?: string;
    };
  };
  visualization_data?: {
    d3_data?: {
      nodes?: Array<{
        id: string;
        name: string;
        type: string;
        description?: string;
        technology?: string;
        x?: number;
        y?: number;
        group?: number;
      }>;
      links?: Array<{
        source: string;
        target: string;
        type: string;
        description?: string;
        data_flow?: string;
      }>;
    };
    mermaid_diagram?: string;
    diagram_types?: string[];
    layout_options?: string[];
  };
}

export interface ArchitectureComponent {
  id: string;
  name: string;
  type: 'service' | 'database' | 'cache' | 'gateway' | 'ui' | 'external' | 'frontend';
  description: string;
  responsibilities: string[];
  technologies: string[];
  scalingFactors: string[];
  businessValue: string;
  position?: { x: number; y: number };
  
  // Enhanced visualization properties
  visualImportance?: number;
  businessCriticality?: 'high' | 'medium' | 'low';
  iconCategory?: 'frontend' | 'backend' | 'database' | 'infrastructure' | 'external';
  technologyBadges?: string[];
  layerAssignments?: {
    system_overview?: string;
    deployment?: string;
  };
  healthIndicators?: {
    monitoring_required?: boolean;
    performance_critical?: boolean;
    availability_target?: string;
  };
  systemOverviewPosition?: {
    x?: number;
    y?: number;
    priority?: string;
  };
  deploymentPosition?: {
    x?: number;
    y?: number;
    zone?: string;
  };
  
  // Layer-specific enhancements
  businessCapability?: {
    capability?: string;
    priority?: 'high' | 'medium' | 'low';
    complexity?: 'high' | 'medium' | 'low';
    business_value?: string;
  };
  coreSystem?: {
    system?: string;
    criticality?: 'high' | 'medium' | 'low';
    user_facing?: boolean;
    purpose?: string;
  };
  dataDomain?: {
    domain?: string;
    sensitivity?: 'high' | 'medium' | 'low';
    data_types?: string[];
  };
  isExternal?: boolean;
  infrastructureZone?: {
    zone?: string;
    zone_type?: 'dmz' | 'application' | 'data' | 'management';
    security_level?: 'high' | 'medium' | 'low';
    network_access?: 'public' | 'private' | 'isolated';
  };
  containerCluster?: {
    cluster?: string;
    scaling?: 'auto' | 'manual' | 'none';
    replicas?: string;
    resource_requirements?: 'high' | 'medium' | 'low';
  };
  scalingProfile?: {
    type?: string;
    importance?: number;
    criticality?: string;
  };
}

export interface ArchitectureConnection {
  id: string;
  fromComponent: string;
  toComponent: string;
  type: 'synchronous' | 'asynchronous' | 'data-flow' | 'dependency' | 'http' | 'grpc' | 'message_queue' | 'database' | 'websocket';
  protocol: string;
  description: string;
  dataFlow?: DataFlowSpec;
  
  // Enhanced visualization properties
  protocolDisplay?: string;
  trafficVolume?: 'high' | 'medium' | 'low';
  latencyRequirement?: 'real_time' | 'near_real_time' | 'batch';
  securityLevel?: 'high' | 'medium' | 'low';
  dependencyStrength?: 'critical' | 'important' | 'optional';
  lineStyle?: 'solid' | 'dashed' | 'dotted';
  animationType?: 'bidirectional' | 'unidirectional' | 'pulsing';
  
  // Network topology enhancements
  networkPath?: string;
}

export interface ArchitectureLayer {
  id: string;
  name: string;
  description: string;
  components: string[];
  level: number;
}

export interface ArchitecturePattern {
  id: string;
  name: string;
  description: string;
  applicableComponents: string[];
  benefits: string[];
  tradeoffs: string[];
}

export interface TechnologyChoice {
  id: string;
  name: string;
  category: string;
  description: string;
  justification: string;
  alternatives: string[];
}

export interface DataFlowSpec {
  dataType: string;
  volume: string;
  frequency: string;
  security: string[];
}

// Why Reasoning Types
export interface WhyReasoning {
  decisionFactors: DecisionFactor[];
  tradeoffs: Tradeoff[];
  alternatives: Alternative[];
  principles: string[];
  businessAlignment: string[];
  confidenceLevel: number;
}

export interface DecisionFactor {
  factor: string;
  importance: number;
  explanation: string;
  businessImpact: string;
}

export interface Tradeoff {
  benefit: string;
  cost: string;
  impactLevel: number;
  quantifiedMetrics?: Record<string, any>;
}

export interface Alternative {
  name: string;
  description: string;
  pros: string[];
  cons: string[];
  viabilityScore: number;
  useCases: string[];
}

// Business Impact Types
export interface SuccessMetric {
  metric: string;
  current_baseline: string;
  target_value: string;
  measurement_method: string;
}

export interface BusinessImpact {
  roiAnalysis: ROIAnalysis;
  riskAssessment: RiskAssessment;
  competitiveAdvantages: string[];
  marketPositioning: string;
  strategicAlignment: string;
  successMetrics: (string | SuccessMetric)[];
}

export interface ROIAnalysis {
  initialInvestment: Record<string, number>;
  ongoingCosts: Record<string, number>;
  expectedBenefits: Record<string, number>;
  paybackPeriodMonths: number;
  netPresentValue: number;
  confidenceLevel: number;
}

export interface RiskAssessment {
  technicalRisks: Risk[];
  businessRisks: Risk[];
  mitigationStrategies: MitigationStrategy[];
  overallRiskLevel: number;
}

export interface Risk {
  id: string;
  description: string;
  probability: number;
  impact: number;
  category: string;
}

export interface MitigationStrategy {
  id: string;
  riskId: string;
  strategy: string;
  cost: number;
  effectiveness: number;
}

// Educational Content Types
export interface EducationalContent {
  concepts: ConceptExplanation[];
  examples: RealWorldExample[];
  exercises: HandsOnExercise[];
  resources: LearningResource[];
  progressTracking: ProgressUpdate;
}

export interface ConceptExplanation {
  id: string;
  concept: string;
  explanation: string;
  difficulty: ExpertiseLevel;
  relatedConcepts: string[];
  businessRelevance: string;
}

export interface RealWorldExample {
  id: string;
  title: string;
  description: string;
  company?: string;
  industry?: string;
  outcome: string;
  lessonsLearned: string[];
}

export interface HandsOnExercise {
  id: string;
  title: string;
  description: string;
  difficulty: ExpertiseLevel;
  estimatedTime: number;
  steps: string[];
  expectedOutcome: string;
}

export interface LearningResource {
  id: string;
  title: string;
  type: 'article' | 'video' | 'book' | 'course' | 'documentation';
  url: string;
  description: string;
  difficulty: ExpertiseLevel;
}

export interface ProgressUpdate {
  conceptsLearned: string[];
  skillsGained: string[];
  nextSteps: string[];
  recommendedResources: string[];
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  metadata?: Record<string, any>;
}

export interface StartConversationRequest {
  title?: string;
  userRequirements: string;
  userContext: ConversationUserContext;
  workflowType?: WorkflowType;
}

export interface StartConversationResponse {
  conversationId: string;
  firstQuestions: string[];
  suggestedFollowUps: string[];
  estimatedDuration: number;
}

export interface SendMessageRequest {
  content: string;
  messageType?: 'TEXT' | 'ARCHITECTURE_UPDATE' | 'CLARIFICATION';
  context?: Record<string, any>;
}

export interface SendMessageResponse {
  messageId: string;
  agentResponse: AgentResponse;
  conversationUpdate?: ConversationUpdate;
}

export interface AgentResponse {
  content: string;
  messageType: string;
  architectureUpdate?: ArchitectureData;
  whyReasoning?: WhyReasoning;
  businessImpact?: BusinessImpact;
  educationalContent?: EducationalContent;
  suggestedActions: string[];
  nextQuestions: string[];
  confidenceScore: number;
}

export interface ConversationUpdate {
  progress: number;
  phase: string;
  estimatedCompletion: string;
}

// UI Component Types
export interface ConversationPanelProps {
  conversation: Conversation | null;
  messages: ConversationMessage[];
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

export interface VisualizationPanelProps {
  architecture: ArchitectureData | null;
  diagramType: DiagramType;
  onDiagramTypeChange: (type: DiagramType) => void;
  isLoading: boolean;
}

export interface DocumentationPanelProps {
  whyReasoning: WhyReasoning | null;
  businessImpact: BusinessImpact | null;
  educationalContent: EducationalContent | null;
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export interface ArchitectureDiagramProps {
  data: ArchitectureData;
  type: DiagramType;
  width: number;
  height: number;
  onComponentClick?: (component: ArchitectureComponent) => void;
  onConnectionClick?: (connection: ArchitectureConnection) => void;
}
