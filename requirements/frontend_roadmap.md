# 🖥️ FRONTEND_DETAILED_ROADMAP.md
## React + TypeScript + Advanced Visualization Implementation Guide

---

## 📋 **OVERVIEW**

This roadmap provides complete technical specifications for building the Agentic Architect frontend application. It includes React architecture, TypeScript interfaces, real-time visualization components, and integration patterns required for autonomous AI agent execution.

**Technology Stack**:
- **Framework**: React 18+ with TypeScript 5.0+
- **State Management**: Zustand for global state + React Query for server state
- **Visualization**: D3.js 7+ for custom charts + Mermaid.js for diagrams
- **UI Components**: Tailwind CSS 3+ with custom component library
- **Build Tool**: Vite 5+ for fast development and optimized builds
- **Testing**: Vitest + React Testing Library for comprehensive testing

---

## 🏗️ **COMPLETE PROJECT STRUCTURE**

### **STEP 1: Project Setup & Configuration**

#### **1.1 Project Initialization**
```bash
# Create React project with TypeScript
npm create vite@latest agentic-architect-frontend -- --template react-ts
cd agentic-architect-frontend

# Install core dependencies
npm install \
  @tanstack/react-query \
  zustand \
  d3 \
  mermaid \
  axios \
  react-router-dom \
  tailwindcss \
  @tailwindcss/forms \
  @tailwindcss/typography \
  lucide-react \
  framer-motion \
  react-hot-toast

# Install development dependencies
npm install -D \
  @types/d3 \
  @types/node \
  @vitejs/plugin-react \
  autoprefixer \
  postcss \
  tailwindcss \
  vitest \
  @testing-library/react \
  @testing-library/jest-dom \
  @testing-library/user-event \
  jsdom \
  eslint \
  @typescript-eslint/eslint-plugin \
  @typescript-eslint/parser \
  prettier
```

#### **1.2 Directory Structure**
```
src/
├── components/
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Modal.tsx
│   │   ├── Tabs.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── ErrorBoundary.tsx
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   ├── MainLayout.tsx
│   │   └── PanelLayout.tsx
│   ├── conversation/
│   │   ├── ConversationPanel.tsx
│   │   ├── MessageList.tsx
│   │   ├── MessageInput.tsx
│   │   ├── ConversationHistory.tsx
│   │   └── UserProfile.tsx
│   ├── visualization/
│   │   ├── VisualizationPanel.tsx
│   │   ├── ArchitectureDiagram.tsx
│   │   ├── D3Visualization.tsx
│   │   ├── MermaidDiagram.tsx
│   │   ├── InteractiveChart.tsx
│   │   └── DiagramControls.tsx
│   ├── documentation/
│   │   ├── DocumentationTabs.tsx
│   │   ├── ArchitectureDoc.tsx
│   │   ├── BusinessAnalysis.tsx
│   │   ├── TechnicalSpecs.tsx
│   │   ├── ExportDialog.tsx
│   │   └── EducationalContent.tsx
│   └── business/
│       ├── ROIAnalysis.tsx
│       ├── RiskAssessment.tsx
│       ├── CompetitiveAnalysis.tsx
│       └── BusinessMetrics.tsx
├── hooks/
│   ├── useConversation.ts
│   ├── useVisualization.ts
│   ├── useWebSocket.ts
│   ├── useLocalStorage.ts
│   ├── useDebounce.ts
│   └── useErrorHandler.ts
├── services/
│   ├── api.ts
│   ├── conversationService.ts
│   ├── architectureService.ts
│   ├── authService.ts
│   ├── exportService.ts
│   └── websocketService.ts
├── store/
│   ├── conversationStore.ts
│   ├── visualizationStore.ts
│   ├── userStore.ts
│   ├── uiStore.ts
│   └── index.ts
├── types/
│   ├── conversation.ts
│   ├── architecture.ts
│   ├── business.ts
│   ├── user.ts
│   ├── api.ts
│   └── visualization.ts
├── utils/
│   ├── formatters.ts
│   ├── validators.ts
│   ├── constants.ts
│   ├── helpers.ts
│   └── errorHandling.ts
├── styles/
│   ├── globals.css
│   ├── components.css
│   └── visualizations.css
└── tests/
    ├── components/
    ├── hooks/
    ├── services/
    ├── utils/
    └── setup.ts
```

#### **1.3 Configuration Files**

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:3001',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          d3: ['d3'],
          mermaid: ['mermaid'],
        },
      },
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/tests/setup.ts',
  },
});
```

```json
// tailwind.config.js
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          900: '#1e3a8a',
        },
        secondary: {
          50: '#f0fdf4',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
          900: '#14532d',
        },
        accent: {
          50: '#fdf4ff',
          500: '#a855f7',
          600: '#9333ea',
          700: '#7c3aed',
          900: '#581c87',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
```

---

## 🎯 **COMPLETE TYPE DEFINITIONS**

### **STEP 2: TypeScript Interface Specifications**

#### **2.1 Core Types**
```typescript
// src/types/conversation.ts
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

export enum ExpertiseLevel {
  BEGINNER = 'BEGINNER',
  INTERMEDIATE = 'INTERMEDIATE',
  ADVANCED = 'ADVANCED',
  EXPERT = 'EXPERT',
}

export interface BusinessContext {
  industry?: string;
  companySize?: 'startup' | 'small' | 'medium' | 'large' | 'enterprise';
  budgetRange?: 'limited' | 'moderate' | 'significant' | 'unlimited';
  timeline?: 'immediate' | 'weeks' | 'months' | 'flexible';
  complianceRequirements?: string[];
  existingTechnologies?: string[];
}

export interface UserPreferences {
  visualizationStyle?: 'modern' | 'classic' | 'minimal';
  explanationDepth?: 'brief' | 'detailed' | 'comprehensive';
  businessFocus?: boolean;
  technicalDepth?: 'high' | 'medium' | 'low';
  theme?: 'light' | 'dark' | 'auto';
}

export interface Conversation {
  id: string;
  userId: string;
  title: string;
  status: ConversationStatus;
  userRequirements: string;
  userContext: ConversationUserContext;
  workflowType: WorkflowType;
  sessionData: ConversationSessionData;
  createdAt: string;
  updatedAt: string;
  completedAt?: string;
  messages: ConversationMessage[];
  architectures: Architecture[];
  finalArchitecture?: Architecture;
  whyReasoning?: WhyReasoning;
  businessImpact?: BusinessImpact;
  educationalContent?: EducationalContent;
}

export enum ConversationStatus {
  ACTIVE = 'ACTIVE',
  COMPLETED = 'COMPLETED',
  PAUSED = 'PAUSED',
  ARCHIVED = 'ARCHIVED',
}

export enum WorkflowType {
  SEQUENTIAL = 'SEQUENTIAL',
  PARALLEL = 'PARALLEL',
  CONDITIONAL = 'CONDITIONAL',
  ITERATIVE = 'ITERATIVE',
}

export interface ConversationMessage {
  id: string;
  conversationId: string;
  role: MessageRole;
  content: string;
  messageType: MessageType;
  metadata?: Record<string, any>;
  agentReasoning?: Record<string, any>;
  timestamp: string;
  sequenceNumber: number;
}

export enum MessageRole {
  USER = 'USER',
  ASSISTANT = 'ASSISTANT',
  SYSTEM = 'SYSTEM',
}

export enum MessageType {
  TEXT = 'TEXT',
  ARCHITECTURE_UPDATE = 'ARCHITECTURE_UPDATE',
  EDUCATIONAL_CONTENT = 'EDUCATIONAL_CONTENT',
  BUSINESS_ANALYSIS = 'BUSINESS_ANALYSIS',
  WHY_REASONING = 'WHY_REASONING',
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

export interface ConversationSessionData {
  phase: string;
  progress: number;
  lastActivity: string;
  estimatedCompletion?: string;
  currentFocus?: string;
  completedMilestones?: string[];
}
```

#### **2.2 Architecture Types**
```typescript
// src/types/architecture.ts
export interface Architecture {
  id: string;
  conversationId: string;
  title: string;
  description?: string;
  architectureData: ArchitectureData;
  diagramType: DiagramType;
  visualizationConfig?: VisualizationConfig;
  whyReasoning: WhyReasoning;
  businessImpact: BusinessImpact;
  technicalDecisions: Record<string, any>;
  alternativesConsidered?: Alternative[];
  version: number;
  status: ArchitectureStatus;
  createdAt: string;
  updatedAt: string;
}

export interface ArchitectureData {
  components: ArchitectureComponent[];
  connections: ArchitectureConnection[];
  layers: ArchitectureLayer[];
  patterns: ArchitecturePattern[];
  technologies: TechnologyChoice[];
  metadata: ArchitectureMetadata;
  deploymentStrategy?: DeploymentStrategy;
  securityModel?: SecurityModel;
  scalingStrategy?: ScalingStrategy;
}

export interface ArchitectureComponent {
  id: string;
  name: string;
  type: ComponentType;
  description: string;
  responsibilities: string[];
  technologies: string[];
  scalingFactors: ScalingFactor[];
  businessValue: string;
  position?: ComponentPosition;
  dependencies: string[];
  interfaces: ComponentInterface[];
  metrics?: ComponentMetrics;
}

export interface ArchitectureConnection {
  id: string;
  fromComponent: string;
  toComponent: string;
  type: ConnectionType;
  protocol: string;
  description: string;
  dataFlow?: DataFlowSpec;
  securityRequirements?: string[];
  performanceRequirements?: PerformanceSpec;
}

export interface ArchitectureLayer {
  id: string;
  name: string;
  type: LayerType;
  components: string[];
  description: string;
  responsibilities: string[];
  position: number;
}

export interface ArchitecturePattern {
  id: string;
  name: string;
  type: PatternType;
  description: string;
  applicableComponents: string[];
  benefits: string[];
  tradeoffs: string[];
  implementation: PatternImplementation;
}

export enum DiagramType {
  SYSTEM_OVERVIEW = 'SYSTEM_OVERVIEW',
  MICROSERVICES = 'MICROSERVICES',
  DATA_FLOW = 'DATA_FLOW',
  DEPLOYMENT = 'DEPLOYMENT',
  SECURITY = 'SECURITY',
  NETWORK = 'NETWORK',
}

export enum ComponentType {
  SERVICE = 'service',
  DATABASE = 'database',
  CACHE = 'cache',
  GATEWAY = 'gateway',
  UI = 'ui',
  EXTERNAL = 'external',
  QUEUE = 'queue',
  STORAGE = 'storage',
}

export enum ConnectionType {
  SYNCHRONOUS = 'synchronous',
  ASYNCHRONOUS = 'asynchronous',
  DATA_FLOW = 'data-flow',
  DEPENDENCY = 'dependency',
  NETWORK = 'network',
}

export interface ComponentPosition {
  x: number;
  y: number;
  width?: number;
  height?: number;
  layer?: number;
}

export interface VisualizationConfig {
  layout: 'hierarchical' | 'force-directed' | 'circular' | 'grid';
  theme: 'light' | 'dark' | 'auto';
  showLabels: boolean;
  showConnections: boolean;
  highlightCriticalPath: boolean;
  interactiveMode: boolean;
  zoomLevel: number;
  panPosition: { x: number; y: number };
  selectedComponents: string[];
  hiddenComponents: string[];
  componentStyles: Record<string, ComponentStyle>;
  connectionStyles: Record<string, ConnectionStyle>;
}

export interface ComponentStyle {
  color?: string;
  backgroundColor?: string;
  borderColor?: string;
  borderWidth?: number;
  fontSize?: number;
  fontWeight?: string;
  opacity?: number;
  shape?: 'rectangle' | 'circle' | 'diamond' | 'hexagon';
}

export interface ConnectionStyle {
  color?: string;
  width?: number;
  dashArray?: string;
  opacity?: number;
  showArrow?: boolean;
  labelPosition?: 'start' | 'middle' | 'end';
}
```

#### **2.3 Business Intelligence Types**
```typescript
// src/types/business.ts
export interface BusinessImpact {
  roiAnalysis: ROIAnalysis;
  riskAssessment: RiskAssessment;
  competitiveAdvantages: CompetitiveAdvantage[];
  marketPositioning: MarketPositioning;
  strategicAlignment: StrategicAlignment;
  successMetrics: SuccessMetric[];
  implementationCost: ImplementationCost;
  timeToMarket: TimeToMarket;
  businessValue: BusinessValue;
}

export interface ROIAnalysis {
  initialInvestment: CostBreakdown;
  ongoingCosts: CostBreakdown;
  expectedBenefits: BenefitBreakdown;
  paybackPeriodMonths: number;
  netPresentValue: number;
  internalRateOfReturn: number;
  confidenceLevel: number;
  assumptions: string[];
  sensitivityAnalysis?: SensitivityAnalysis;
}

export interface CostBreakdown {
  development: number;
  infrastructure: number;
  licensing: number;
  personnel: number;
  training: number;
  maintenance: number;
  other: number;
  total: number;
  breakdown: CostItem[];
}

export interface BenefitBreakdown {
  costSavings: number;
  revenueIncrease: number;
  productivityGains: number;
  riskMitigation: number;
  competitiveAdvantage: number;
  total: number;
  breakdown: BenefitItem[];
}

export interface RiskAssessment {
  technicalRisks: Risk[];
  businessRisks: Risk[];
  operationalRisks: Risk[];
  financialRisks: Risk[];
  mitigationStrategies: MitigationStrategy[];
  overallRiskLevel: RiskLevel;
  riskMatrix: RiskMatrix;
}

export interface Risk {
  id: string;
  name: string;
  description: string;
  category: RiskCategory;
  probability: number; // 1-5 scale
  impact: number; // 1-5 scale
  riskScore: number; // probability * impact
  mitigationActions: string[];
  owner?: string;
  status: RiskStatus;
}

export enum RiskLevel {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH',
  CRITICAL = 'CRITICAL',
}

export interface CompetitiveAdvantage {
  id: string;
  name: string;
  description: string;
  category: AdvantageCategory;
  impact: ImpactLevel;
  sustainability: SustainabilityLevel;
  timeToRealize: number; // months
  evidence: string[];
  metrics: string[];
}

export interface MarketPositioning {
  currentPosition: string;
  targetPosition: string;
  differentiators: string[];
  competitorAnalysis: CompetitorAnalysis[];
  marketTrends: MarketTrend[];
  opportunityAssessment: OpportunityAssessment;
}

export interface SuccessMetric {
  id: string;
  name: string;
  description: string;
  category: MetricCategory;
  targetValue: number;
  currentValue?: number;
  unit: string;
  measurementFrequency: MeasurementFrequency;
  dataSource: string;
  owner: string;
  kpiType: KPIType;
}

export enum MetricCategory {
  FINANCIAL = 'FINANCIAL',
  OPERATIONAL = 'OPERATIONAL',
  CUSTOMER = 'CUSTOMER',
  TECHNICAL = 'TECHNICAL',
  BUSINESS = 'BUSINESS',
}

export enum KPIType {
  LEADING = 'LEADING',
  LAGGING = 'LAGGING',
  DIAGNOSTIC = 'DIAGNOSTIC',
}
```

#### **2.4 Why Reasoning Types**
```typescript
// src/types/reasoning.ts
export interface WhyReasoning {
  decisionFactors: DecisionFactor[];
  tradeoffs: Tradeoff[];
  alternatives: Alternative[];
  principles: ArchitecturalPrinciple[];
  businessAlignment: BusinessAlignment[];
  confidenceLevel: number;
  learningPoints: LearningPoint[];
  decisionFramework: DecisionFramework;
  successMetrics: string[];
  reasoningMetadata: ReasoningMetadata;
}

export interface DecisionFactor {
  id: string;
  factor: string;
  importance: number; // 1-5 scale
  explanation: string;
  businessImpact: string;
  evidence: string[];
  weight: number;
  category: FactorCategory;
}

export interface Tradeoff {
  id: string;
  decision: string;
  benefit: string;
  cost: string;
  impactLevel: number; // 1-5 scale
  quantifiedMetrics: Record<string, TradeoffMetric>;
  contextualFactors: string[];
  mitigationStrategies: string[];
  justification: string;
}

export interface TradeoffMetric {
  value: number;
  unit: string;
  confidence: number;
  timeframe: string;
  comparisonBaseline?: number;
}

export interface Alternative {
  id: string;
  name: string;
  description: string;
  pros: string[];
  cons: string[];
  viabilityScore: number; // 1-5 scale
  useCases: string[];
  implementationComplexity: ComplexityLevel;
  costImplication: CostImplication;
  timeToImplement: number; // months
  riskLevel: RiskLevel;
  businessFit: BusinessFit;
}

export interface ArchitecturalPrinciple {
  id: string;
  name: string;
  description: string;
  rationale: string;
  implications: string[];
  examples: PrincipleExample[];
  boundaries: string[];
  relatedPrinciples: string[];
  category: PrincipleCategory;
}

export interface BusinessAlignment {
  id: string;
  businessObjective: string;
  technicalDecision: string;
  alignmentScore: number; // 1-5 scale
  supportingEvidence: string[];
  metrics: string[];
  risksToAlignment: string[];
  strengthening_actions: string[];
}

export interface LearningPoint {
  id: string;
  concept: string;
  explanation: string;
  applicationExample: string;
  relatedConcepts: string[];
  difficultyLevel: DifficultyLevel;
  importance: ImportanceLevel;
  category: LearningCategory;
}

export interface DecisionFramework {
  steps: FrameworkStep[];
  principles: string[];
  checkpoints: string[];
  tools: string[];
  adaptations: FrameworkAdaptation[];
}

export enum ComplexityLevel {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH',
  VERY_HIGH = 'VERY_HIGH',
}

export enum DifficultyLevel {
  BEGINNER = 'BEGINNER',
  INTERMEDIATE = 'INTERMEDIATE',
  ADVANCED = 'ADVANCED',
  EXPERT = 'EXPERT',
}

export enum ImportanceLevel {
  NICE_TO_KNOW = 'NICE_TO_KNOW',
  IMPORTANT = 'IMPORTANT',
  CRITICAL = 'CRITICAL',
  FUNDAMENTAL = 'FUNDAMENTAL',
}
```

---

## 🔧 **CORE COMPONENT IMPLEMENTATIONS**

### **STEP 3: State Management with Zustand**

#### **3.1 Conversation Store**
```typescript
// src/store/conversationStore.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import {
  Conversation,
  ConversationMessage,
  ConversationStatus,
  WorkflowType,
  ExpertiseLevel,
} from '@/types/conversation';

interface ConversationState {
  // State
  conversations: Conversation[];
  activeConversation: Conversation | null;
  isLoading: boolean;
  error: string | null;
  
  // Conversation Management
  createConversation: (params: CreateConversationParams) => Promise<Conversation>;
  loadConversation: (conversationId: string) => Promise<void>;
  updateConversation: (conversationId: string, updates: Partial<Conversation>) => void;
  deleteConversation: (conversationId: string) => Promise<void>;
  
  // Message Management
  sendMessage: (conversationId: string, content: string) => Promise<ConversationMessage>;
  addMessage: (conversationId: string, message: ConversationMessage) => void;
  updateMessage: (conversationId: string, messageId: string, updates: Partial<ConversationMessage>) => void;
  
  // UI State
  setActiveConversation: (conversation: Conversation | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearConversations: () => void;
  
  // Real-time Updates
  subscribeToUpdates: (conversationId: string) => void;
  unsubscribeFromUpdates: (conversationId: string) => void;
}

interface CreateConversationParams {
  title?: string;
  userRequirements: string;
  expertiseLevel: ExpertiseLevel;
  businessRole?: string;
  businessContext?: any;
  workflowType?: WorkflowType;
}

export const useConversationStore = create<ConversationState>()(
  devtools(
    persist(
      (set, get) => ({
        // Initial state
        conversations: [],
        activeConversation: null,
        isLoading: false,
        error: null,

        // Conversation Management
        createConversation: async (params: CreateConversationParams) => {
          set({ isLoading: true, error: null });
          
          try {
            const response = await fetch('/api/conversations', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
              },
              body: JSON.stringify({
                title: params.title,
                userRequirements: params.userRequirements,
                userContext: {
                  expertise: params.expertiseLevel,
                  businessRole: params.businessRole,
                  businessContext: params.businessContext,
                },
                workflowType: params.workflowType || WorkflowType.SEQUENTIAL,
              }),
            });

            if (!response.ok) {
              throw new Error('Failed to create conversation');
            }

            const { data } = await response.json();
            const conversation: Conversation = {
              id: data.conversationId,
              userId: 'current-user', // TODO: Get from auth context
              title: params.title || `Conversation ${new Date().toLocaleDateString()}`,
              status: ConversationStatus.ACTIVE,
              userRequirements: params.userRequirements,
              userContext: {
                expertise: params.expertiseLevel,
                businessRole: params.businessRole,
                businessContext: params.businessContext,
              },
              workflowType: params.workflowType || WorkflowType.SEQUENTIAL,
              sessionData: {
                phase: 'requirements_gathering',
                progress: 0.1,
                lastActivity: new Date().toISOString(),
              },
              createdAt: new Date().toISOString(),
              updatedAt: new Date().toISOString(),
              messages: [],
              architectures: [],
            };

            set((state) => ({
              conversations: [...state.conversations, conversation],
              activeConversation: conversation,
              isLoading: false,
            }));

            return conversation;
          } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown error';
            set({ error: errorMessage, isLoading: false });
            throw error;
          }
        },

        loadConversation: async (conversationId: string) => {
          set({ isLoading: true, error: null });
          
          try {
            const response = await fetch(`/api/conversations/${conversationId}`, {
              headers: {
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
              },
            });

            if (!response.ok) {
              throw new Error('Failed to load conversation');
            }

            const { data } = await response.json();
            const conversation = data.conversation;

            set((state) => ({
              conversations: state.conversations.map((c) =>
                c.id === conversationId ? conversation : c
              ),
              activeConversation: conversation,
              isLoading: false,
            }));
          } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown error';
            set({ error: errorMessage, isLoading: false });
          }
        },

        updateConversation: (conversationId: string, updates: Partial<Conversation>) => {
          set((state) => ({
            conversations: state.conversations.map((c) =>
              c.id === conversationId ? { ...c, ...updates, updatedAt: new Date().toISOString() } : c
            ),
            activeConversation:
              state.activeConversation?.id === conversationId
                ? { ...state.activeConversation, ...updates, updatedAt: new Date().toISOString() }
                : state.activeConversation,
          }));
        },

        deleteConversation: async (conversationId: string) => {
          try {
            const response = await fetch(`/api/conversations/${conversationId}`, {
              method: 'DELETE',
              headers: {
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
              },
            });

            if (!response.ok) {
              throw new Error('Failed to delete conversation');
            }

            set((state) => ({
              conversations: state.conversations.filter((c) => c.id !== conversationId),
              activeConversation:
                state.activeConversation?.id === conversationId ? null : state.activeConversation,
            }));
          } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown error';
            set({ error: errorMessage });
            throw error;
          }
        },

        // Message Management
        sendMessage: async (conversationId: string, content: string) => {
          set({ isLoading: true, error: null });
          
          try {
            const response = await fetch(`/api/conversations/${conversationId}/messages`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
              },
              body: JSON.stringify({
                content,
                messageType: 'TEXT',
              }),
            });

            if (!response.ok) {
              throw new Error('Failed to send message');
            }

            const { data } = await response.json();
            
            // Add user message
            const userMessage: ConversationMessage = {
              id: `user-${Date.now()}`,
              conversationId,
              role: 'USER',
              content,
              messageType: 'TEXT',
              timestamp: new Date().toISOString(),
              sequenceNumber: get().activeConversation?.messages.length || 0,
            };

            // Add assistant message
            const assistantMessage: ConversationMessage = {
              id: data.messageId,
              conversationId,
              role: 'ASSISTANT',
              content: data.agentResponse.content,
              messageType: data.agentResponse.messageType,
              metadata: data.agentResponse,
              timestamp: new Date().toISOString(),
              sequenceNumber: (get().activeConversation?.messages.length || 0) + 1,
            };

            set((state) => ({
              conversations: state.conversations.map((c) =>
                c.id === conversationId
                  ? {
                      ...c,
                      messages: [...c.messages, userMessage, assistantMessage],
                      updatedAt: new Date().toISOString(),
                    }
                  : c
              ),
              activeConversation:
                state.activeConversation?.id === conversationId
                  ? {
                      ...state.activeConversation,
                      messages: [...state.activeConversation.messages, userMessage, assistantMessage],
                      updatedAt: new Date().toISOString(),
                    }
                  : state.activeConversation,
              isLoading: false,
            }));

            return assistantMessage;
          } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown error';
            set({ error: errorMessage, isLoading: false });
            throw error;
          }
        },

        addMessage: (conversationId: string, message: ConversationMessage) => {
          set((state) => ({
            conversations: state.conversations.map((c) =>
              c.id === conversationId
                ? { ...c, messages: [...c.messages, message] }
                : c
            ),
            activeConversation:
              state.activeConversation?.id === conversationId
                ? { ...state.activeConversation, messages: [...state.activeConversation.messages, message] }
                : state.activeConversation,
          }));
        },

        updateMessage: (conversationId: string, messageId: string, updates: Partial<ConversationMessage>) => {
          set((state) => ({
            conversations: state.conversations.map((c) =>
              c.id === conversationId
                ? {
                    ...c,
                    messages: c.messages.map((m) =>
                      m.id === messageId ? { ...m, ...updates } : m
                    ),
                  }
                : c
            ),
            activeConversation:
              state.activeConversation?.id === conversationId
                ? {
                    ...state.activeConversation,
                    messages: state.activeConversation.messages.map((m) =>
                      m.id === messageId ? { ...m, ...updates } : m
                    ),
                  }
                : state.activeConversation,
          }));
        },

        // UI State
        setActiveConversation: (conversation: Conversation | null) => {
          set({ activeConversation: conversation });
        },

        setLoading: (loading: boolean) => {
          set({ isLoading: loading });
        },

        setError: (error: string | null) => {
          set({ error });
        },

        clearConversations: () => {
          set({
            conversations: [],
            activeConversation: null,
            isLoading: false,
            error: null,
          });
        },

        // Real-time Updates (WebSocket implementation)
        subscribeToUpdates: (conversationId: string) => {
          // TODO: Implement WebSocket subscription
          console.log(`Subscribing to updates for conversation ${conversationId}`);
        },

        unsubscribeFromUpdates: (conversationId: string) => {
          // TODO: Implement WebSocket unsubscription
          console.log(`Unsubscribing from updates for conversation ${conversationId}`);
        },
      }),
      {
        name: 'conversation-store',
        partialize: (state) => ({
          conversations: state.conversations,
          activeConversation: state.activeConversation,
        }),
      }
    ),
    { name: 'conversation-store' }
  )
);
```

#### **3.2 Visualization Store**
```typescript
// src/store/visualizationStore.ts
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import {
  Architecture,
  ArchitectureData,
  VisualizationConfig,
  DiagramType,
  ComponentStyle,
  ConnectionStyle,
} from '@/types/architecture';

interface VisualizationState {
  // State
  currentArchitecture: Architecture | null;
  visualizationConfig: VisualizationConfig;
  selectedComponents: string[];
  hoveredComponent: string | null;
  isLoading: boolean;
  error: string | null;
  
  // Diagram Management
  setArchitecture: (architecture: Architecture) => void;
  updateArchitectureData: (data: Partial<ArchitectureData>) => void;
  
  // Visualization Configuration
  updateVisualizationConfig: (updates: Partial<VisualizationConfig>) => void;
  setDiagramType: (type: DiagramType) => void;
  setLayout: (layout: VisualizationConfig['layout']) => void;
  setTheme: (theme: VisualizationConfig['theme']) => void;
  
  // Component Interaction
  selectComponent: (componentId: string) => void;
  selectMultipleComponents: (componentIds: string[]) => void;
  deselectComponent: (componentId: string) => void;
  clearSelection: () => void;
  setHoveredComponent: (componentId: string | null) => void;
  
  // Component Styling
  updateComponentStyle: (componentId: string, style: Partial<ComponentStyle>) => void;
  updateConnectionStyle: (connectionId: string, style: Partial<ConnectionStyle>) => void;
  resetStyles: () => void;
  
  // View Management
  zoomIn: () => void;
  zoomOut: () => void;
  resetZoom: () => void;
  setZoom: (level: number) => void;
  panTo: (x: number, y: number) => void;
  centerView: () => void;
  
  // Component Visibility
  hideComponent: (componentId: string) => void;
  showComponent: (componentId: string) => void;
  hideMultipleComponents: (componentIds: string[]) => void;
  showAllComponents: () => void;
  
  // Export/Import
  exportConfiguration: () => VisualizationConfig;
  importConfiguration: (config: VisualizationConfig) => void;
  
  // Utility
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

const defaultVisualizationConfig: VisualizationConfig = {
  layout: 'hierarchical',
  theme: 'light',
  showLabels: true,
  showConnections: true,
  highlightCriticalPath: false,
  interactiveMode: true,
  zoomLevel: 1,
  panPosition: { x: 0, y: 0 },
  selectedComponents: [],
  hiddenComponents: [],
  componentStyles: {},
  connectionStyles: {},
};

export const useVisualizationStore = create<VisualizationState>()(
  devtools(
    (set, get) => ({
      // Initial state
      currentArchitecture: null,
      visualizationConfig: defaultVisualizationConfig,
      selectedComponents: [],
      hoveredComponent: null,
      isLoading: false,
      error: null,

      // Diagram Management
      setArchitecture: (architecture: Architecture) => {
        set({
          currentArchitecture: architecture,
          visualizationConfig: {
            ...get().visualizationConfig,
            ...architecture.visualizationConfig,
          },
        });
      },

      updateArchitectureData: (data: Partial<ArchitectureData>) => {
        const current = get().currentArchitecture;
        if (!current) return;

        set({
          currentArchitecture: {
            ...current,
            architectureData: {
              ...current.architectureData,
              ...data,
            },
          },
        });
      },

      // Visualization Configuration
      updateVisualizationConfig: (updates: Partial<VisualizationConfig>) => {
        set((state) => ({
          visualizationConfig: {
            ...state.visualizationConfig,
            ...updates,
          },
        }));
      },

      setDiagramType: (type: DiagramType) => {
        set((state) => {
          if (!state.currentArchitecture) return state;
          
          return {
            currentArchitecture: {
              ...state.currentArchitecture,
              diagramType: type,
            },
          };
        });
      },

      setLayout: (layout: VisualizationConfig['layout']) => {
        set((state) => ({
          visualizationConfig: {
            ...state.visualizationConfig,
            layout,
          },
        }));
      },

      setTheme: (theme: VisualizationConfig['theme']) => {
        set((state) => ({
          visualizationConfig: {
            ...state.visualizationConfig,
            theme,
          },
        }));
      },

      // Component Interaction
      selectComponent: (componentId: string) => {
        set((state) => ({
          selectedComponents: [componentId],
          visualizationConfig: {
            ...state.visualizationConfig,
            selectedComponents: [componentId],
          },
        }));
      },

      selectMultipleComponents: (componentIds: string[]) => {
        set((state) => ({
          selectedComponents: componentIds,
          visualizationConfig: {
            ...state.visualizationConfig,
            selectedComponents: componentIds,
          },
        }));
      },

      deselectComponent: (componentId: string) => {
        set((state) => {
          const newSelection = state.selectedComponents.filter(id => id !== componentId);
          return {
            selectedComponents: newSelection,
            visualizationConfig: {
              ...state.visualizationConfig,
              selectedComponents: newSelection,
            },
          };
        });
      },

      clearSelection: () => {
        set((state) => ({
          selectedComponents: [],
          visualizationConfig: {
            ...state.visualizationConfig,
            selectedComponents: [],
          },
        }));
      },

      setHoveredComponent: (componentId: string | null) => {
        set({ hoveredComponent: componentId });
      },

      // Component Styling
      updateComponentStyle: (componentId: string, style: Partial<ComponentStyle>) => {
        set((state) => ({
          visualizationConfig: {
            ...state.visualizationConfig,
            componentStyles: {
              ...state.visualizationConfig.componentStyles,
              [componentId]: {
                ...state.visualizationConfig.componentStyles[componentId],
                ...style,
              },
            },
          },
        }));
      },

      updateConnectionStyle: (connectionId: string, style: Partial<ConnectionStyle>) => {
        set((state) => ({
          visualizationConfig: {
            ...state.visualizationConfig,
            connectionStyles: {
              ...state.visualizationConfig.connectionStyles,
              [connectionId]: {
                ...state.visualizationConfig.connectionStyles[connectionId],
                ...style,
              },
            },
          },
        }));
      },

      resetStyles: () => {
        set((state) => ({
          visualizationConfig: {
            ...state.visualizationConfig,
            componentStyles: {},
            connectionStyles: {},
          },
        }));
      },

      // View Management
      zoomIn: () => {
        set((state) => ({
          visualizationConfig: {
            ...state.visualizationConfig,
            zoomLevel: Math.min(state.visualizationConfig.zoomLevel * 1.2, 5),
          },
        }));
      },

      zoomOut: () => {
        set((state) => ({
          visualizationConfig: {
            ...state.visualizationConfig,
            zoomLevel: Math.max(state.visualizationConfig.zoomLevel / 1.2, 0.1),
          },
        }));
      },

      resetZoom: () => {
        set((state) => ({
          visualizationConfig: {
            ...state.visualizationConfig,
            zoomLevel: 1,
            panPosition: { x: 0, y: 0 },
          },
        }));
      },

      setZoom: (level: number) => {
        set((state) => ({
          visualizationConfig: {
            ...state.visualizationConfig,
            zoomLevel: Math.max(0.1, Math.min(5, level)),
          },
        }));
      },

      panTo: (x: number, y: number) => {
        set((state) => ({
          visualizationConfig: {
            ...state.visualizationConfig,
            panPosition: { x, y },
          },
        }));
      },

      centerView: () => {
        set((state) => ({
          visualizationConfig: {
            ...state.visualizationConfig,
            panPosition: { x: 0, y: 0 },
            zoomLevel: 1,
          },
        }));
      },

      // Component Visibility
      hideComponent: (componentId: string) => {
        set((state) => ({
          visualizationConfig: {
            ...state.visualizationConfig,
            hiddenComponents: [...state.visualizationConfig.hiddenComponents, componentId],
          },
        }));
      },

      showComponent: (componentId: string) => {
        set((state) => ({
          visualizationConfig: {
            ...state.visualizationConfig,
            hiddenComponents: state.visualizationConfig.hiddenComponents.filter(id => id !== componentId),
          },
        }));
      },

      hideMultipleComponents: (componentIds: string[]) => {
        set((state) => ({
          visualizationConfig: {
            ...state.visualizationConfig,
            hiddenComponents: [
              ...state.visualizationConfig.hiddenComponents,
              ...componentIds.filter(id => !state.visualizationConfig.hiddenComponents.includes(id)),
            ],
          },
        }));
      },

      showAllComponents: () => {
        set((state) => ({
          visualizationConfig: {
            ...state.visualizationConfig,
            hiddenComponents: [],
          },
        }));
      },

      // Export/Import
      exportConfiguration: () => {
        return get().visualizationConfig;
      },

      importConfiguration: (config: VisualizationConfig) => {
        set({ visualizationConfig: config });
      },

      // Utility
      setLoading: (loading: boolean) => {
        set({ isLoading: loading });
      },

      setError: (error: string | null) => {
        set({ error });
      },
    }),
    { name: 'visualization-store' }
  )
);
```

### **STEP 4: Main Layout Components**

#### **4.1 Main Application Layout**
```tsx
// src/components/layout/MainLayout.tsx
import React, { useState, useEffect } from 'react';
import { ErrorBoundary } from '@/components/ui/ErrorBoundary';
import { Header } from './Header';
import { Sidebar } from './Sidebar';
import { ConversationPanel } from '@/components/conversation/ConversationPanel';
import { VisualizationPanel } from '@/components/visualization/VisualizationPanel';
import { DocumentationTabs } from '@/components/documentation/DocumentationTabs';
import { useConversationStore } from '@/store/conversationStore';
import { useVisualizationStore } from '@/store/visualizationStore';
import { cn } from '@/utils/helpers';

interface MainLayoutProps {
  children?: React.ReactNode;
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [documentationOpen, setDocumentationOpen] = useState(false);
  const { activeConversation } = useConversationStore();
  const { currentArchitecture } = useVisualizationStore();

  // Auto-open documentation when architecture is available
  useEffect(() => {
    if (currentArchitecture && !documentationOpen) {
      setDocumentationOpen(true);
    }
  }, [currentArchitecture, documentationOpen]);

  return (
    <ErrorBoundary>
      <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
        {/* Sidebar */}
        <div
          className={cn(
            'transition-all duration-300 ease-in-out bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex-shrink-0',
            sidebarOpen ? 'w-80' : 'w-16'
          )}
        >
          <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
        </div>

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* Header */}
          <Header />

          {/* Content Panels */}
          <div className="flex-1 flex min-h-0">
            {/* Left Panel - Conversation */}
            <div className="w-2/5 min-w-96 flex flex-col border-r border-gray-200 dark:border-gray-700">
              <ConversationPanel />
            </div>

            {/* Right Panel - Visualization */}
            <div className="flex-1 flex flex-col min-w-0">
              <VisualizationPanel />
            </div>
          </div>

          {/* Bottom Panel - Documentation (Collapsible) */}
          {documentationOpen && (
            <div className="h-80 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
              <DocumentationTabs
                onClose={() => setDocumentationOpen(false)}
                conversation={activeConversation}
                architecture={currentArchitecture}
              />
            </div>
          )}

          {/* Documentation Toggle Button */}
          {!documentationOpen && currentArchitecture && (
            <button
              onClick={() => setDocumentationOpen(true)}
              className="fixed bottom-4 right-4 bg-primary-600 text-white px-4 py-2 rounded-lg shadow-lg hover:bg-primary-700 transition-colors"
            >
              Show Documentation
            </button>
          )}
        </div>

        {/* Custom children overlay (for modals, etc.) */}
        {children}
      </div>
    </ErrorBoundary>
  );
};
```

#### **4.2 Conversation Panel Component**
```tsx
// src/components/conversation/ConversationPanel.tsx
import React, { useState, useRef, useEffect } from 'react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { ConversationHistory } from './ConversationHistory';
import { UserProfile } from './UserProfile';
import { useConversationStore } from '@/store/conversationStore';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { Button } from '@/components/ui/Button';
import { Settings, History, User, MessageSquare } from 'lucide-react';
import { cn } from '@/utils/helpers';

export const ConversationPanel: React.FC = () => {
  const [showHistory, setShowHistory] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const {
    activeConversation,
    isLoading,
    error,
    sendMessage,
    createConversation,
  } = useConversationStore();

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [activeConversation?.messages]);

  const handleSendMessage = async (content: string) => {
    if (!activeConversation) return;
    
    try {
      await sendMessage(activeConversation.id, content);
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  const handleStartNewConversation = async (userRequirements: string) => {
    try {
      await createConversation({
        userRequirements,
        expertiseLevel: 'INTERMEDIATE', // TODO: Get from user profile
        businessRole: 'Software Architect', // TODO: Get from user profile
        workflowType: 'SEQUENTIAL',
      });
    } catch (error) {
      console.error('Failed to start conversation:', error);
    }
  };

  if (showHistory) {
    return (
      <div className="h-full flex flex-col">
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
              Conversation History
            </h2>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowHistory(false)}
            >
              Back to Chat
            </Button>
          </div>
        </div>
        <ConversationHistory onSelectConversation={() => setShowHistory(false)} />
      </div>
    );
  }

  if (showProfile) {
    return (
      <div className="h-full flex flex-col">
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
              User Profile
            </h2>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowProfile(false)}
            >
              Back to Chat
            </Button>
          </div>
        </div>
        <UserProfile onSave={() => setShowProfile(false)} />
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col bg-white dark:bg-gray-800">
      {/* Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <MessageSquare className="w-5 h-5 text-primary-600" />
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
              {activeConversation?.title || 'Architecture Consultation'}
            </h2>
          </div>
          
          <div className="flex items-center space-x-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowProfile(true)}
              title="User Profile"
            >
              <User className="w-4 h-4" />
            </Button>
            
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowHistory(true)}
              title="Conversation History"
            >
              <History className="w-4 h-4" />
            </Button>
          </div>
        </div>

        {/* Conversation Status */}
        {activeConversation && (
          <div className="mt-2 flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
            <span>
              Status: {activeConversation.status} | 
              Progress: {Math.round((activeConversation.sessionData?.progress || 0) * 100)}%
            </span>
            <span>
              {activeConversation.messages.length} messages
            </span>
          </div>
        )}
      </div>

      {/* Error Display */}
      {error && (
        <div className="mx-4 mt-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <p className="text-sm text-red-700 dark:text-red-400">{error}</p>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-hidden">
        {activeConversation ? (
          <>
            <MessageList
              messages={activeConversation.messages}
              isLoading={isLoading}
            />
            <div ref={messagesEndRef} />
          </>
        ) : (
          <div className="h-full flex items-center justify-center">
            <div className="text-center max-w-md px-4">
              <MessageSquare className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                Start a New Conversation
              </h3>
              <p className="text-gray-500 dark:text-gray-400 mb-4">
                Describe your architecture requirements and I'll help you design the perfect solution.
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Loading Indicator */}
      {isLoading && (
        <div className="px-4 py-2 border-t border-gray-200 dark:border-gray-700">
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <LoadingSpinner size="sm" />
            <span>Processing your request...</span>
          </div>
        </div>
      )}

      {/* Message Input */}
      <div className="border-t border-gray-200 dark:border-gray-700">
        <MessageInput
          onSendMessage={activeConversation ? handleSendMessage : handleStartNewConversation}
          disabled={isLoading}
          placeholder={
            activeConversation
              ? "Continue the conversation..."
              : "Describe your architecture requirements..."
          }
        />
      </div>
    </div>
  );
};
```

### **STEP 5: Advanced Visualization Components**

#### **5.1 D3.js Architecture Visualization**
```tsx
// src/components/visualization/D3Visualization.tsx
import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { ArchitectureData, ArchitectureComponent, ArchitectureConnection, VisualizationConfig } from '@/types/architecture';
import { useVisualizationStore } from '@/store/visualizationStore';
import { cn } from '@/utils/helpers';

interface D3VisualizationProps {
  data: ArchitectureData;
  config: VisualizationConfig;
  width?: number;
  height?: number;
  className?: string;
  onComponentClick?: (component: ArchitectureComponent) => void;
  onComponentHover?: (component: ArchitectureComponent | null) => void;
}

interface D3Node extends d3.SimulationNodeDatum {
  id: string;
  component: ArchitectureComponent;
  x?: number;
  y?: number;
  fx?: number | null;
  fy?: number | null;
}

interface D3Link extends d3.SimulationLinkDatum<D3Node> {
  source: string | D3Node;
  target: string | D3Node;
  connection: ArchitectureConnection;
}

export const D3Visualization: React.FC<D3VisualizationProps> = ({
  data,
  config,
  width = 800,
  height = 600,
  className,
  onComponentClick,
  onComponentHover,
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const simulationRef = useRef<d3.Simulation<D3Node, D3Link> | null>(null);
  const [dimensions, setDimensions] = useState({ width, height });
  
  const {
    selectComponent,
    setHoveredComponent,
    updateVisualizationConfig,
  } = useVisualizationStore();

  // Responsive dimensions
  useEffect(() => {
    const handleResize = () => {
      if (svgRef.current) {
        const rect = svgRef.current.parentElement?.getBoundingClientRect();
        if (rect) {
          setDimensions({
            width: rect.width,
            height: rect.height,
          });
        }
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize();

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Main visualization effect
  useEffect(() => {
    if (!svgRef.current || !data.components.length) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove(); // Clear previous render

    // Prepare data
    const nodes: D3Node[] = data.components
      .filter(component => !config.hiddenComponents.includes(component.id))
      .map(component => ({
        id: component.id,
        component,
        x: component.position?.x,
        y: component.position?.y,
      }));

    const links: D3Link[] = data.connections
      .filter(conn => 
        nodes.find(n => n.id === conn.fromComponent) &&
        nodes.find(n => n.id === conn.toComponent)
      )
      .map(connection => ({
        source: connection.fromComponent,
        target: connection.toComponent,
        connection,
      }));

    // Create main group with zoom behavior
    const g = svg.append('g').attr('class', 'main-group');

    // Setup zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 5])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
        updateVisualizationConfig({
          zoomLevel: event.transform.k,
          panPosition: { x: event.transform.x, y: event.transform.y },
        });
      });

    svg.call(zoom);

    // Apply saved zoom/pan state
    const initialTransform = d3.zoomIdentity
      .translate(config.panPosition.x, config.panPosition.y)
      .scale(config.zoomLevel);
    svg.call(zoom.transform, initialTransform);

    // Create simulation based on layout type
    let simulation: d3.Simulation<D3Node, D3Link>;

    switch (config.layout) {
      case 'force-directed':
        simulation = d3.forceSimulation(nodes)
          .force('link', d3.forceLink<D3Node, D3Link>(links).id(d => d.id).distance(100))
          .force('charge', d3.forceManyBody().strength(-300))
          .force('center', d3.forceCenter(dimensions.width / 2, dimensions.height / 2))
          .force('collision', d3.forceCollide().radius(50));
        break;

      case 'hierarchical':
        simulation = createHierarchicalLayout(nodes, links, dimensions);
        break;

      case 'circular':
        simulation = createCircularLayout(nodes, links, dimensions);
        break;

      case 'grid':
        simulation = createGridLayout(nodes, links, dimensions);
        break;

      default:
        simulation = d3.forceSimulation(nodes)
          .force('center', d3.forceCenter(dimensions.width / 2, dimensions.height / 2));
    }

    simulationRef.current = simulation;

    // Create links
    const linkGroup = g.append('g').attr('class', 'links');
    const link = linkGroup
      .selectAll('line')
      .data(links)
      .enter()
      .append('line')
      .attr('class', 'connection')
      .attr('stroke', d => getConnectionColor(d.connection, config))
      .attr('stroke-width', d => getConnectionWidth(d.connection, config))
      .attr('stroke-dasharray', d => getConnectionDashArray(d.connection, config))
      .attr('opacity', 0.7);

    // Add connection labels
    if (config.showLabels) {
      const linkLabels = linkGroup
        .selectAll('text')
        .data(links)
        .enter()
        .append('text')
        .attr('class', 'connection-label')
        .attr('text-anchor', 'middle')
        .attr('dy', -5)
        .attr('font-size', '10px')
        .attr('fill', config.theme === 'dark' ? '#9CA3AF' : '#6B7280')
        .text(d => d.connection.protocol);
    }

    // Create nodes
    const nodeGroup = g.append('g').attr('class', 'nodes');
    const node = nodeGroup
      .selectAll('g')
      .data(nodes)
      .enter()
      .append('g')
      .attr('class', 'node')
      .style('cursor', 'pointer')
      .call(d3.drag<SVGGElement, D3Node>()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended)
      );

    // Add component shapes
    node.each(function(d) {
      const nodeElement = d3.select(this);
      const shape = getComponentShape(d.component);
      const style = config.componentStyles[d.id] || {};
      
      switch (shape) {
        case 'circle':
          nodeElement
            .append('circle')
            .attr('r', 30)
            .attr('fill', style.backgroundColor || getComponentColor(d.component, config))
            .attr('stroke', style.borderColor || '#374151')
            .attr('stroke-width', style.borderWidth || 2);
          break;
          
        case 'rectangle':
        default:
          nodeElement
            .append('rect')
            .attr('width', 80)
            .attr('height', 50)
            .attr('x', -40)
            .attr('y', -25)
            .attr('rx', 8)
            .attr('fill', style.backgroundColor || getComponentColor(d.component, config))
            .attr('stroke', style.borderColor || '#374151')
            .attr('stroke-width', style.borderWidth || 2);
      }
    });

    // Add component icons
    node.append('text')
      .attr('class', 'component-icon')
      .attr('text-anchor', 'middle')
      .attr('dy', 5)
      .attr('font-size', '16px')
      .text(d => getComponentIcon(d.component));

    // Add component labels
    if (config.showLabels) {
      node.append('text')
        .attr('class', 'component-label')
        .attr('text-anchor', 'middle')
        .attr('dy', 40)
        .attr('font-size', '12px')
        .attr('font-weight', 'bold')
        .attr('fill', config.theme === 'dark' ? '#F9FAFB' : '#111827')
        .text(d => d.component.name);
    }

    // Add interaction handlers
    node
      .on('click', (event, d) => {
        event.stopPropagation();
        selectComponent(d.id);
        onComponentClick?.(d.component);
      })
      .on('mouseenter', (event, d) => {
        setHoveredComponent(d.id);
        onComponentHover?.(d.component);
        
        // Highlight connected components
        highlightConnectedComponents(d.id, nodeGroup, linkGroup);
      })
      .on('mouseleave', () => {
        setHoveredComponent(null);
        onComponentHover?.(null);
        
        // Remove highlights
        removeHighlights(nodeGroup, linkGroup);
      });

    // Update positions on simulation tick
    simulation.on('tick', () => {
      link
        .attr('x1', d => (d.source as D3Node).x!)
        .attr('y1', d => (d.source as D3Node).y!)
        .attr('x2', d => (d.target as D3Node).x!)
        .attr('y2', d => (d.target as D3Node).y!);

      if (config.showLabels) {
        linkGroup.selectAll('text')
          .attr('x', d => ((d.source as D3Node).x! + (d.target as D3Node).x!) / 2)
          .attr('y', d => ((d.source as D3Node).y! + (d.target as D3Node).y!) / 2);
      }

      node.attr('transform', d => `translate(${d.x},${d.y})`);
    });

    // Drag handlers
    function dragstarted(event: d3.D3DragEvent<SVGGElement, D3Node, unknown>, d: D3Node) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event: d3.D3DragEvent<SVGGElement, D3Node, unknown>, d: D3Node) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event: d3.D3DragEvent<SVGGElement, D3Node, unknown>, d: D3Node) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    // Cleanup
    return () => {
      simulation.stop();
    };

  }, [data, config, dimensions, selectComponent, setHoveredComponent, updateVisualizationConfig, onComponentClick, onComponentHover]);

  // Apply selection highlighting
  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    
    // Reset all selections
    svg.selectAll('.node rect, .node circle')
      .attr('stroke-width', 2)
      .attr('opacity', 1);

    // Highlight selected components
    config.selectedComponents.forEach(componentId => {
      svg.select(`[data-component-id="${componentId}"] rect, [data-component-id="${componentId}"] circle`)
        .attr('stroke-width', 4)
        .attr('stroke', '#3B82F6');
    });
  }, [config.selectedComponents]);

  return (
    <div className={cn('w-full h-full', className)}>
      <svg
        ref={svgRef}
        width={dimensions.width}
        height={dimensions.height}
        className="w-full h-full"
        style={{ 
          background: config.theme === 'dark' ? '#1F2937' : '#F9FAFB',
        }}
      >
        {/* Gradient definitions for enhanced visuals */}
        <defs>
          <linearGradient id="service-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#3B82F6" />
            <stop offset="100%" stopColor="#1D4ED8" />
          </linearGradient>
          <linearGradient id="database-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#10B981" />
            <stop offset="100%" stopColor="#047857" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  );
};

// Helper functions
function createHierarchicalLayout(nodes: D3Node[], links: D3Link[], dimensions: { width: number; height: number }) {
  // Simple hierarchical layout - position nodes in layers
  const layers = new Map<string, number>();
  
  // Assign layers based on dependencies
  nodes.forEach((node, index) => {
    layers.set(node.id, Math.floor(index / Math.ceil(nodes.length / 3)));
  });

  const layerHeight = dimensions.height / (layers.size + 1);
  
  nodes.forEach(node => {
    const layer = layers.get(node.id) || 0;
    node.x = (layer + 1) * (dimensions.width / (layers.size + 1));
    node.y = dimensions.height / 2;
    node.fx = node.x;
    node.fy = node.y;
  });

  return d3.forceSimulation(nodes)
    .force('link', d3.forceLink<D3Node, D3Link>(links).id(d => d.id))
    .force('collision', d3.forceCollide().radius(50));
}

function createCircularLayout(nodes: D3Node[], links: D3Link[], dimensions: { width: number; height: number }) {
  const radius = Math.min(dimensions.width, dimensions.height) / 3;
  const angleStep = (2 * Math.PI) / nodes.length;
  
  nodes.forEach((node, index) => {
    const angle = index * angleStep;
    node.x = dimensions.width / 2 + radius * Math.cos(angle);
    node.y = dimensions.height / 2 + radius * Math.sin(angle);
    node.fx = node.x;
    node.fy = node.y;
  });

  return d3.forceSimulation(nodes)
    .force('link', d3.forceLink<D3Node, D3Link>(links).id(d => d.id));
}

function createGridLayout(nodes: D3Node[], links: D3Link[], dimensions: { width: number; height: number }) {
  const cols = Math.ceil(Math.sqrt(nodes.length));
  const rows = Math.ceil(nodes.length / cols);
  const cellWidth = dimensions.width / cols;
  const cellHeight = dimensions.height / rows;
  
  nodes.forEach((node, index) => {
    const col = index % cols;
    const row = Math.floor(index / cols);
    node.x = (col + 0.5) * cellWidth;
    node.y = (row + 0.5) * cellHeight;
    node.fx = node.x;
    node.fy = node.y;
  });

  return d3.forceSimulation(nodes)
    .force('link', d3.forceLink<D3Node, D3Link>(links).id(d => d.id));
}

function getComponentColor(component: ArchitectureComponent, config: VisualizationConfig): string {
  const typeColors = {
    service: '#3B82F6',
    database: '#10B981',
    cache: '#F59E0B',
    gateway: '#8B5CF6',
    ui: '#EF4444',
    external: '#6B7280',
    queue: '#F97316',
    storage: '#14B8A6',
  };
  
  return typeColors[component.type] || '#6B7280';
}

function getComponentIcon(component: ArchitectureComponent): string {
  const typeIcons = {
    service: '⚙️',
    database: '🗄️',
    cache: '💾',
    gateway: '🚪',
    ui: '🖥️',
    external: '🌐',
    queue: '📨',
    storage: '📦',
  };
  
  return typeIcons[component.type] || '📦';
}

function getComponentShape(component: ArchitectureComponent): 'rectangle' | 'circle' | 'diamond' {
  const shapeMap = {
    service: 'rectangle',
    database: 'circle',
    cache: 'circle',
    gateway: 'diamond',
    ui: 'rectangle',
    external: 'rectangle',
    queue: 'rectangle',
    storage: 'circle',
  } as const;
  
  return shapeMap[component.type] || 'rectangle';
}

function getConnectionColor(connection: ArchitectureConnection, config: VisualizationConfig): string {
  const typeColors = {
    synchronous: '#3B82F6',
    asynchronous: '#10B981',
    'data-flow': '#F59E0B',
    dependency: '#6B7280',
    network: '#8B5CF6',
  };
  
  return typeColors[connection.type] || '#6B7280';
}

function getConnectionWidth(connection: ArchitectureConnection, config: VisualizationConfig): number {
  const typeWidths = {
    synchronous: 2,
    asynchronous: 2,
    'data-flow': 3,
    dependency: 1,
    network: 2,
  };
  
  return typeWidths[connection.type] || 2;
}

function getConnectionDashArray(connection: ArchitectureConnection, config: VisualizationConfig): string | null {
  if (connection.type === 'dependency') {
    return '5,5';
  }
  return null;
}

function highlightConnectedComponents(componentId: string, nodeGroup: d3.Selection<d3.BaseType, any, d3.BaseType, any>, linkGroup: d3.Selection<d3.BaseType, any, d3.BaseType, any>) {
  // Highlight connected nodes and links
  nodeGroup.selectAll('.node')
    .style('opacity', 0.3);
  
  linkGroup.selectAll('line')
    .style('opacity', 0.1);
  
  // Highlight the selected node
  nodeGroup.select(`[data-component-id="${componentId}"]`)
    .style('opacity', 1);
  
  // Highlight connected links and nodes
  linkGroup.selectAll('line')
    .filter((d: any) => d.source.id === componentId || d.target.id === componentId)
    .style('opacity', 0.8)
    .style('stroke-width', 3);
}

function removeHighlights(nodeGroup: d3.Selection<d3.BaseType, any, d3.BaseType, any>, linkGroup: d3.Selection<d3.BaseType, any, d3.BaseType, any>) {
  nodeGroup.selectAll('.node')
    .style('opacity', 1);
  
  linkGroup.selectAll('line')
    .style('opacity', 0.7)
    .style('stroke-width', null);
}
```

---

## ✅ **VALIDATION & SUCCESS CRITERIA**

### **Frontend Completion Checklist**
- [ ] **Project Setup**: React + TypeScript + Vite configured with all dependencies
- [ ] **State Management**: Zustand stores implemented for conversation, visualization, and UI state
- [ ] **Type Safety**: Complete TypeScript interfaces for all data structures
- [ ] **Component Architecture**: Modular component structure with clear separation of concerns
- [ ] **Visualization**: Advanced D3.js and Mermaid.js implementations with interactive features
- [ ] **API Integration**: Complete service layer with error handling and retry logic