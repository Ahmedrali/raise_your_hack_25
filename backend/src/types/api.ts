// Enums (duplicated from Prisma schema until client is generated)
export enum ExpertiseLevel {
  BEGINNER = 'BEGINNER',
  INTERMEDIATE = 'INTERMEDIATE',
  ADVANCED = 'ADVANCED',
  EXPERT = 'EXPERT'
}

export enum WorkflowType {
  SEQUENTIAL = 'SEQUENTIAL',
  PARALLEL = 'PARALLEL',
  CONDITIONAL = 'CONDITIONAL',
  ITERATIVE = 'ITERATIVE'
}

export enum ConversationStatus {
  ACTIVE = 'ACTIVE',
  COMPLETED = 'COMPLETED',
  PAUSED = 'PAUSED',
  ARCHIVED = 'ARCHIVED'
}

// Request/Response Types
export interface CreateUserRequest {
  email: string;
  password: string;
  firstName?: string;
  lastName?: string;
  expertiseLevel?: ExpertiseLevel;
  businessRole?: string;
  businessContext?: BusinessContext;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  user: UserProfile;
  token: string;
  expiresIn: string;
}

export interface UserProfile {
  id: string;
  email: string;
  firstName?: string;
  lastName?: string;
  expertiseLevel: ExpertiseLevel;
  businessRole?: string;
  businessContext?: BusinessContext;
  preferences?: UserPreferences;
  createdAt: Date;
}

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

export interface ConversationUserContext {
  expertise: ExpertiseLevel;
  businessRole?: string;
  businessContext?: BusinessContext;
  projectType?: string;
  timeline?: string;
  budget?: string;
  existingConstraints?: string[];
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
  suggestedActions?: string[];
  nextQuestions?: string[];
}

export interface ArchitectureData {
  components: ArchitectureComponent[];
  connections: ArchitectureConnection[];
  layers: ArchitectureLayer[];
  patterns: ArchitecturePattern[];
  technologies: TechnologyChoice[];
  metadata: ArchitectureMetadata;
}

export interface ArchitectureComponent {
  id: string;
  name: string;
  type: 'service' | 'database' | 'cache' | 'gateway' | 'ui' | 'external';
  description: string;
  responsibilities: string[];
  technologies: string[];
  scalingFactors: ScalingFactor[];
  businessValue: string;
}

export interface ArchitectureConnection {
  id: string;
  from: string;
  to: string;
  type: 'synchronous' | 'asynchronous' | 'data-flow' | 'dependency';
  protocol: string;
  description: string;
  dataFlow?: DataFlowSpec;
}

export interface ArchitectureLayer {
  id: string;
  name: string;
  type: string;
  components: string[];
  description: string;
  responsibilities: string[];
  position: number;
}

export interface ArchitecturePattern {
  id: string;
  name: string;
  type: string;
  description: string;
  applicableComponents: string[];
  benefits: string[];
  tradeoffs: string[];
  implementation: PatternImplementation;
}

export interface TechnologyChoice {
  id: string;
  name: string;
  category: string;
  version?: string;
  justification: string;
  alternatives: string[];
  pros: string[];
  cons: string[];
}

export interface ArchitectureMetadata {
  designedFor: string;
  expertiseLevel: ExpertiseLevel;
  businessContext: BusinessContext;
  designTimestamp: string;
  version: number;
}

export interface ScalingFactor {
  factor: string;
  impact: 'low' | 'medium' | 'high';
  description: string;
}

export interface DataFlowSpec {
  dataType: string;
  volume: string;
  frequency: string;
  format: string;
  security: string[];
}

export interface PatternImplementation {
  steps: string[];
  codeExamples: Record<string, string>;
  configuration: Record<string, any>;
  dependencies: string[];
}

export interface WhyReasoning {
  decisionFactors: DecisionFactor[];
  tradeoffs: Tradeoff[];
  alternatives: Alternative[];
  principles: ArchitecturalPrinciple[];
  businessAlignment: BusinessAlignment[];
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
  quantifiedMetrics: Record<string, any>;
}

export interface Alternative {
  name: string;
  description: string;
  pros: string[];
  cons: string[];
  viabilityScore: number;
  useCases: string[];
}

export interface ArchitecturalPrinciple {
  name: string;
  description: string;
  rationale: string;
  implications: string[];
  examples: string[];
}

export interface BusinessAlignment {
  businessObjective: string;
  technicalDecision: string;
  alignmentScore: number;
  supportingEvidence: string[];
}

export interface BusinessImpact {
  roiAnalysis: ROIAnalysis;
  riskAssessment: RiskAssessment;
  competitiveAdvantage: CompetitiveAdvantage[];
  implementationCost: ImplementationCost;
  timeToMarket: TimeToMarket;
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
  name: string;
  description: string;
  probability: number;
  impact: number;
  mitigationActions: string[];
}

export interface MitigationStrategy {
  risk: string;
  strategy: string;
  cost: number;
  effectiveness: number;
}

export interface CompetitiveAdvantage {
  advantage: string;
  description: string;
  impact: string;
  sustainability: string;
}

export interface ImplementationCost {
  development: number;
  infrastructure: number;
  maintenance: number;
  total: number;
  breakdown: CostItem[];
}

export interface CostItem {
  category: string;
  amount: number;
  description: string;
  recurring: boolean;
}

export interface TimeToMarket {
  estimatedMonths: number;
  phases: Phase[];
  criticalPath: string[];
  risks: string[];
}

export interface Phase {
  name: string;
  duration: number;
  dependencies: string[];
  deliverables: string[];
}

export interface EducationalContent {
  concepts: ConceptExplanation[];
  examples: RealWorldExample[];
  exercises: HandsOnExercise[];
  resources: LearningResource[];
  progressTracking: ProgressUpdate;
}

export interface ConceptExplanation {
  concept: string;
  explanation: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  relatedConcepts: string[];
}

export interface RealWorldExample {
  title: string;
  description: string;
  company?: string;
  outcome: string;
  lessonsLearned: string[];
}

export interface HandsOnExercise {
  title: string;
  description: string;
  steps: string[];
  expectedOutcome: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
}

export interface LearningResource {
  title: string;
  type: 'article' | 'video' | 'book' | 'course' | 'documentation';
  url?: string;
  description: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
}

export interface ProgressUpdate {
  conceptsLearned: string[];
  skillsGained: string[];
  nextSteps: string[];
  recommendedResources: string[];
}

export interface ConversationUpdate {
  progress: number;
  phase: string;
  estimatedCompletion: Date;
}

// Agent Service Integration Types
export interface AgentServiceRequest {
  type: 'process_conversation' | 'generate_architecture' | 'analyze_requirements';
  data: {
    conversationId: string;
    userMessage?: string;
    conversationHistory: ConversationMessage[];
    userProfile: UserProfile;
    businessContext?: BusinessContext;
  };
  options?: {
    workflowType?: WorkflowType;
    urgency?: 'low' | 'medium' | 'high';
    depth?: 'basic' | 'detailed' | 'comprehensive';
  };
}

export interface ConversationMessage {
  role: string;
  content: string;
  messageType: string;
  metadata?: any;
  timestamp: Date;
}

export interface AgentServiceResponse {
  success: boolean;
  data?: AgentResponse;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  metadata?: {
    processingTime: number;
    agentsUsed: string[];
    workflowType: string;
  };
}

// API Response wrapper
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  metadata?: {
    timestamp: string;
    requestId?: string;
    processingTime?: number;
  };
}

// Error types
export interface ApiError extends Error {
  statusCode?: number;
  code?: string;
  details?: any;
}
