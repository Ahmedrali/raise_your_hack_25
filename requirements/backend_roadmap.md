# ⚙️ BACKEND_DETAILED_ROADMAP.md
## Express + TypeScript + PostgreSQL Implementation Guide

---

## 📋 **OVERVIEW**

This roadmap provides complete technical specifications for building the Agentic Architect backend service. It includes actual database schemas, API specifications, service implementations, and integration patterns required for autonomous AI agent execution.

**Technology Stack**:
- **Runtime**: Node.js 18+ with TypeScript 5.0+
- **Framework**: Express.js 4.18+ with async/await patterns
- **Database**: PostgreSQL 15+ with Prisma ORM 5.0+
- **Authentication**: JWT with bcryptjs hashing
- **Validation**: Zod for request/response validation
- **Testing**: Jest + Supertest for comprehensive testing

---

## 🗄️ **COMPLETE DATABASE SCHEMA**

### **STEP 1: Database Setup & Configuration**

#### **1.1 PostgreSQL Database Creation**
```sql
-- Execute these commands in PostgreSQL
CREATE DATABASE agentic_architect_db;
CREATE USER agentic_user WITH ENCRYPTED PASSWORD 'secure_password_2025';
GRANT ALL PRIVILEGES ON DATABASE agentic_architect_db TO agentic_user;

-- Connect to the database
\c agentic_architect_db;

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

#### **1.2 Environment Configuration**
```bash
# .env file
DATABASE_URL="postgresql://agentic_user:secure_password_2025@localhost:5432/agentic_architect_db"
JWT_SECRET="your-256-bit-secret-key-here-make-it-long-and-random"
JWT_EXPIRY="24h"
NODE_ENV="development"
PORT=3001
AGENT_SERVICE_URL="http://localhost:8000"
CORS_ORIGIN="http://localhost:3000"
```

#### **1.3 Prisma Schema Definition**
```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id                String   @id @default(uuid()) @db.Uuid
  email             String   @unique @db.VarChar(255)
  password_hash     String   @db.VarChar(255)
  first_name        String?  @db.VarChar(100)
  last_name         String?  @db.VarChar(100)
  expertise_level   ExpertiseLevel @default(INTERMEDIATE)
  business_role     String?  @db.VarChar(100)
  business_context  Json?    @db.JsonB
  preferences       Json?    @db.JsonB
  created_at        DateTime @default(now()) @db.Timestamp(6)
  updated_at        DateTime @updatedAt @db.Timestamp(6)
  last_login        DateTime? @db.Timestamp(6)
  
  // Relationships
  conversations     Conversation[]
  learning_progress LearningProgress[]
  user_sessions     UserSession[]
  
  @@map("users")
}

model UserSession {
  id         String   @id @default(uuid()) @db.Uuid
  user_id    String   @db.Uuid
  token_hash String   @db.VarChar(255)
  expires_at DateTime @db.Timestamp(6)
  created_at DateTime @default(now()) @db.Timestamp(6)
  user_agent String?  @db.Text
  ip_address String?  @db.VarChar(45)
  
  // Relationships
  user User @relation(fields: [user_id], references: [id], onDelete: Cascade)
  
  @@map("user_sessions")
}

model Conversation {
  id                String             @id @default(uuid()) @db.Uuid
  user_id           String             @db.Uuid
  title             String             @db.VarChar(255)
  session_data      Json               @db.JsonB
  workflow_type     WorkflowType       @default(SEQUENTIAL)
  status            ConversationStatus @default(ACTIVE)
  user_requirements String             @db.Text
  user_context      Json               @db.JsonB
  agent_context     Json?              @db.JsonB
  final_architecture Json?             @db.JsonB
  why_reasoning     Json?              @db.JsonB
  business_impact   Json?              @db.JsonB
  educational_content Json?            @db.JsonB
  created_at        DateTime           @default(now()) @db.Timestamp(6)
  updated_at        DateTime           @updatedAt @db.Timestamp(6)
  completed_at      DateTime?          @db.Timestamp(6)
  
  // Relationships
  user             User               @relation(fields: [user_id], references: [id], onDelete: Cascade)
  messages         ConversationMessage[]
  architectures    Architecture[]
  exports          ArchitectureExport[]
  
  @@map("conversations")
}

model ConversationMessage {
  id              String           @id @default(uuid()) @db.Uuid
  conversation_id String           @db.Uuid
  role            MessageRole      @default(USER)
  content         String           @db.Text
  message_type    MessageType      @default(TEXT)
  metadata        Json?            @db.JsonB
  agent_reasoning Json?            @db.JsonB
  timestamp       DateTime         @default(now()) @db.Timestamp(6)
  sequence_number Int
  
  // Relationships
  conversation Conversation @relation(fields: [conversation_id], references: [id], onDelete: Cascade)
  
  @@unique([conversation_id, sequence_number])
  @@map("conversation_messages")
}

model Architecture {
  id                 String            @id @default(uuid()) @db.Uuid
  conversation_id    String            @db.Uuid
  title              String            @db.VarChar(255)
  description        String?           @db.Text
  architecture_data  Json              @db.JsonB
  diagram_type       DiagramType       @default(SYSTEM_OVERVIEW)
  visualization_config Json?           @db.JsonB
  why_reasoning      Json              @db.JsonB
  business_impact    Json              @db.JsonB
  technical_decisions Json             @db.JsonB
  alternatives_considered Json?        @db.JsonB
  version            Int               @default(1)
  status             ArchitectureStatus @default(DRAFT)
  created_at         DateTime          @default(now()) @db.Timestamp(6)
  updated_at         DateTime          @updatedAt @db.Timestamp(6)
  
  // Relationships
  conversation Conversation @relation(fields: [conversation_id], references: [id], onDelete: Cascade)
  exports      ArchitectureExport[]
  
  @@map("architectures")
}

model ArchitectureExport {
  id              String     @id @default(uuid()) @db.Uuid
  conversation_id String     @db.Uuid
  architecture_id String?    @db.Uuid
  export_type     ExportType @default(PDF)
  export_data     Json       @db.JsonB
  file_path       String?    @db.VarChar(500)
  download_count  Int        @default(0)
  expires_at      DateTime?  @db.Timestamp(6)
  created_at      DateTime   @default(now()) @db.Timestamp(6)
  
  // Relationships
  conversation Conversation  @relation(fields: [conversation_id], references: [id], onDelete: Cascade)
  architecture Architecture? @relation(fields: [architecture_id], references: [id], onDelete: SetNull)
  
  @@map("architecture_exports")
}

model LearningProgress {
  id                String   @id @default(uuid()) @db.Uuid
  user_id           String   @db.Uuid
  topic             String   @db.VarChar(200)
  current_level     ExpertiseLevel @default(BEGINNER)
  progress_data     Json     @db.JsonB
  mastery_indicators Json    @db.JsonB
  last_interaction  DateTime @default(now()) @db.Timestamp(6)
  total_interactions Int     @default(0)
  time_spent_minutes Int     @default(0)
  achievements      Json?    @db.JsonB
  
  // Relationships
  user User @relation(fields: [user_id], references: [id], onDelete: Cascade)
  
  @@unique([user_id, topic])
  @@map("learning_progress")
}

// Enums
enum ExpertiseLevel {
  BEGINNER
  INTERMEDIATE
  ADVANCED
  EXPERT
}

enum WorkflowType {
  SEQUENTIAL
  PARALLEL
  CONDITIONAL
  ITERATIVE
}

enum ConversationStatus {
  ACTIVE
  COMPLETED
  PAUSED
  ARCHIVED
}

enum MessageRole {
  USER
  ASSISTANT
  SYSTEM
}

enum MessageType {
  TEXT
  ARCHITECTURE_UPDATE
  EDUCATIONAL_CONTENT
  BUSINESS_ANALYSIS
  WHY_REASONING
}

enum DiagramType {
  SYSTEM_OVERVIEW
  MICROSERVICES
  DATA_FLOW
  DEPLOYMENT
  SECURITY
  NETWORK
}

enum ArchitectureStatus {
  DRAFT
  REVIEW
  APPROVED
  IMPLEMENTED
}

enum ExportType {
  PDF
  MARKDOWN
  JSON
  MERMAID
  POWERPOINT
}
```

### **STEP 2: Database Migration & Seeding**

#### **2.1 Migration Setup**
```bash
# Install Prisma CLI and generate client
npm install prisma @prisma/client
npx prisma generate
npx prisma db push
```

#### **2.2 Seed Data Implementation**
```typescript
// prisma/seed.ts
import { PrismaClient, ExpertiseLevel, WorkflowType } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  // Create demo users
  const hashedPassword = await bcrypt.hash('demo123', 12);
  
  const demoUser = await prisma.user.create({
    data: {
      email: 'demo@agenticarchitect.com',
      password_hash: hashedPassword,
      first_name: 'Demo',
      last_name: 'User',
      expertise_level: ExpertiseLevel.INTERMEDIATE,
      business_role: 'Software Architect',
      business_context: {
        industry: 'Technology',
        companySize: 'startup',
        budgetRange: 'moderate',
        timeline: 'aggressive'
      },
      preferences: {
        visualization_style: 'modern',
        explanation_depth: 'detailed',
        business_focus: true
      }
    }
  });

  // Create sample conversation
  const sampleConversation = await prisma.conversation.create({
    data: {
      user_id: demoUser.id,
      title: 'E-commerce Platform Architecture',
      user_requirements: 'Need to design a scalable e-commerce platform for 100K users',
      user_context: {
        expertise: 'intermediate',
        businessRole: 'Software Architect',
        timeline: '6 months',
        budget: '$500K'
      },
      workflow_type: WorkflowType.SEQUENTIAL,
      session_data: {
        phase: 'requirements_gathering',
        progress: 0.3,
        lastActivity: new Date().toISOString()
      }
    }
  });

  // Create sample messages
  await prisma.conversationMessage.createMany({
    data: [
      {
        conversation_id: sampleConversation.id,
        role: 'USER',
        content: 'I need help designing an e-commerce platform architecture',
        message_type: 'TEXT',
        sequence_number: 1
      },
      {
        conversation_id: sampleConversation.id,
        role: 'ASSISTANT',
        content: 'I\'d be happy to help you design an e-commerce platform. Let me ask some questions to understand your requirements better.',
        message_type: 'TEXT',
        sequence_number: 2
      }
    ]
  });

  console.log('Database seeded successfully!');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

#### **2.3 Database Validation Queries**
```sql
-- Verify all tables created correctly
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE table_schema = 'public' 
ORDER BY table_name, ordinal_position;

-- Verify relationships
SELECT
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
  AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
  AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY';

-- Verify seed data
SELECT 'users' as table_name, COUNT(*) as row_count FROM users
UNION ALL
SELECT 'conversations', COUNT(*) FROM conversations
UNION ALL
SELECT 'conversation_messages', COUNT(*) FROM conversation_messages;
```

---

## 🔧 **COMPLETE API IMPLEMENTATION**

### **STEP 3: Core Express Application Setup**

#### **3.1 Application Structure**
```typescript
// src/app.ts
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import rateLimit from 'express-rate-limit';
import { PrismaClient } from '@prisma/client';
import { errorHandler, notFoundHandler } from './middleware/error-handling';
import { authMiddleware } from './middleware/auth';
import { validationMiddleware } from './middleware/validation';
import { loggingMiddleware } from './middleware/logging';

// Route imports
import authRoutes from './routes/auth';
import userRoutes from './routes/users';
import conversationRoutes from './routes/conversations';
import architectureRoutes from './routes/architectures';
import exportRoutes from './routes/exports';
import healthRoutes from './routes/health';

const app = express();
const prisma = new PrismaClient();

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
  credentials: true
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.'
});
app.use(limiter);

// Body parsing and compression
app.use(compression());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Logging
app.use(loggingMiddleware);

// Database connection middleware
app.use((req, res, next) => {
  req.prisma = prisma;
  next();
});

// Health check (before auth)
app.use('/api/health', healthRoutes);

// Authentication routes (no auth required)
app.use('/api/auth', authRoutes);

// Protected routes
app.use('/api/users', authMiddleware, userRoutes);
app.use('/api/conversations', authMiddleware, conversationRoutes);
app.use('/api/architectures', authMiddleware, architectureRoutes);
app.use('/api/exports', authMiddleware, exportRoutes);

// Error handling
app.use(notFoundHandler);
app.use(errorHandler);

export default app;
```

#### **3.2 TypeScript Interfaces & Types**
```typescript
// src/types/api.ts
import { ExpertiseLevel, WorkflowType, ConversationStatus } from '@prisma/client';

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

export interface WhyReasoning {
  decisionFactors: DecisionFactor[];
  tradeoffs: Tradeoff[];
  alternatives: Alternative[];
  principles: ArchitecturalPrinciple[];
  businessAlignment: BusinessAlignment[];
}

export interface BusinessImpact {
  roiAnalysis: ROIAnalysis;
  riskAssessment: RiskAssessment;
  competitiveAdvantage: CompetitiveAdvantage[];
  implementationCost: ImplementationCost;
  timeToMarket: TimeToMarket;
}

export interface EducationalContent {
  concepts: ConceptExplanation[];
  examples: RealWorldExample[];
  exercises: HandsOnExercise[];
  resources: LearningResource[];
  progressTracking: ProgressUpdate;
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
```

### **STEP 4: Authentication & Authorization Implementation**

#### **4.1 Authentication Service**
```typescript
// src/services/auth.service.ts
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { PrismaClient } from '@prisma/client';
import { CreateUserRequest, LoginRequest, LoginResponse, UserProfile } from '../types/api';

export class AuthService {
  constructor(private prisma: PrismaClient) {}

  async createUser(userData: CreateUserRequest): Promise<UserProfile> {
    // Check if user already exists
    const existingUser = await this.prisma.user.findUnique({
      where: { email: userData.email }
    });

    if (existingUser) {
      throw new Error('User already exists with this email');
    }

    // Hash password
    const passwordHash = await bcrypt.hash(userData.password, 12);

    // Create user
    const user = await this.prisma.user.create({
      data: {
        email: userData.email,
        password_hash: passwordHash,
        first_name: userData.firstName,
        last_name: userData.lastName,
        expertise_level: userData.expertiseLevel || 'INTERMEDIATE',
        business_role: userData.businessRole,
        business_context: userData.businessContext || {},
      }
    });

    return this.mapUserToProfile(user);
  }

  async login(credentials: LoginRequest): Promise<LoginResponse> {
    // Find user
    const user = await this.prisma.user.findUnique({
      where: { email: credentials.email }
    });

    if (!user) {
      throw new Error('Invalid credentials');
    }

    // Verify password
    const isValidPassword = await bcrypt.compare(credentials.password, user.password_hash);
    if (!isValidPassword) {
      throw new Error('Invalid credentials');
    }

    // Update last login
    await this.prisma.user.update({
      where: { id: user.id },
      data: { last_login: new Date() }
    });

    // Generate JWT
    const token = jwt.sign(
      { userId: user.id, email: user.email },
      process.env.JWT_SECRET!,
      { expiresIn: process.env.JWT_EXPIRY || '24h' }
    );

    // Create session record
    await this.prisma.userSession.create({
      data: {
        user_id: user.id,
        token_hash: await bcrypt.hash(token, 8),
        expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000) // 24 hours
      }
    });

    return {
      user: this.mapUserToProfile(user),
      token,
      expiresIn: process.env.JWT_EXPIRY || '24h'
    };
  }

  async validateToken(token: string): Promise<UserProfile | null> {
    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET!) as any;
      
      const user = await this.prisma.user.findUnique({
        where: { id: decoded.userId }
      });

      return user ? this.mapUserToProfile(user) : null;
    } catch (error) {
      return null;
    }
  }

  async logout(userId: string, token: string): Promise<void> {
    const tokenHash = await bcrypt.hash(token, 8);
    
    await this.prisma.userSession.deleteMany({
      where: {
        user_id: userId,
        token_hash: tokenHash
      }
    });
  }

  private mapUserToProfile(user: any): UserProfile {
    return {
      id: user.id,
      email: user.email,
      firstName: user.first_name,
      lastName: user.last_name,
      expertiseLevel: user.expertise_level,
      businessRole: user.business_role,
      businessContext: user.business_context,
      preferences: user.preferences,
      createdAt: user.created_at
    };
  }
}
```

#### **4.2 Authentication Middleware**
```typescript
// src/middleware/auth.ts
import { Request, Response, NextFunction } from 'express';
import { AuthService } from '../services/auth.service';

export interface AuthenticatedRequest extends Request {
  user?: UserProfile;
}

export async function authMiddleware(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
) {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({
        success: false,
        error: {
          code: 'UNAUTHORIZED',
          message: 'No valid authorization token provided'
        }
      });
    }

    const token = authHeader.substring(7); // Remove 'Bearer ' prefix
    const authService = new AuthService(req.prisma);
    const user = await authService.validateToken(token);

    if (!user) {
      return res.status(401).json({
        success: false,
        error: {
          code: 'INVALID_TOKEN',
          message: 'Invalid or expired token'
        }
      });
    }

    req.user = user;
    next();
  } catch (error) {
    console.error('Auth middleware error:', error);
    res.status(500).json({
      success: false,
      error: {
        code: 'AUTH_ERROR',
        message: 'Authentication error occurred'
      }
    });
  }
}
```

### **STEP 5: Conversation Management Service**

#### **5.1 Conversation Service Implementation**
```typescript
// src/services/conversation.service.ts
import { PrismaClient, WorkflowType, ConversationStatus } from '@prisma/client';
import {
  StartConversationRequest,
  StartConversationResponse,
  SendMessageRequest,
  SendMessageResponse,
  AgentServiceRequest
} from '../types/api';
import { AgentService } from './agent.service';

export class ConversationService {
  constructor(
    private prisma: PrismaClient,
    private agentService: AgentService
  ) {}

  async startConversation(
    userId: string,
    request: StartConversationRequest
  ): Promise<StartConversationResponse> {
    // Create conversation record
    const conversation = await this.prisma.conversation.create({
      data: {
        user_id: userId,
        title: request.title || this.generateConversationTitle(request.userRequirements),
        user_requirements: request.userRequirements,
        user_context: request.userContext,
        workflow_type: request.workflowType || WorkflowType.SEQUENTIAL,
        session_data: {
          phase: 'requirements_gathering',
          progress: 0.1,
          startTime: new Date().toISOString()
        }
      }
    });

    // Get user profile for agent context
    const user = await this.prisma.user.findUnique({
      where: { id: userId }
    });

    // Send initial request to agent service
    const agentRequest: AgentServiceRequest = {
      type: 'process_conversation',
      data: {
        conversationId: conversation.id,
        conversationHistory: [],
        userProfile: {
          id: user!.id,
          email: user!.email,
          expertiseLevel: user!.expertise_level,
          businessRole: user!.business_role,
          businessContext: user!.business_context as any
        },
        businessContext: request.userContext.businessContext
      },
      options: {
        workflowType: request.workflowType,
        urgency: 'medium',
        depth: 'detailed'
      }
    };

    const agentResponse = await this.agentService.processRequest(agentRequest);

    if (!agentResponse.success || !agentResponse.data) {
      throw new Error('Failed to initialize conversation with agent service');
    }

    // Create initial user message
    await this.prisma.conversationMessage.create({
      data: {
        conversation_id: conversation.id,
        role: 'USER',
        content: request.userRequirements,
        message_type: 'TEXT',
        sequence_number: 1
      }
    });

    // Create initial agent response
    await this.prisma.conversationMessage.create({
      data: {
        conversation_id: conversation.id,
        role: 'ASSISTANT',
        content: agentResponse.data.content,
        message_type: agentResponse.data.messageType as any,
        metadata: {
          agentResponse: agentResponse.data,
          processingMetadata: agentResponse.metadata
        },
        agent_reasoning: agentResponse.data.whyReasoning,
        sequence_number: 2
      }
    });

    return {
      conversationId: conversation.id,
      firstQuestions: agentResponse.data.nextQuestions || [],
      suggestedFollowUps: agentResponse.data.suggestedActions || [],
      estimatedDuration: this.estimateConversationDuration(request.userContext)
    };
  }

  async sendMessage(
    userId: string,
    conversationId: string,
    request: SendMessageRequest
  ): Promise<SendMessageResponse> {
    // Verify conversation ownership
    const conversation = await this.prisma.conversation.findFirst({
      where: {
        id: conversationId,
        user_id: userId
      },
      include: {
        messages: {
          orderBy: { sequence_number: 'asc' }
        },
        user: true
      }
    });

    if (!conversation) {
      throw new Error('Conversation not found or access denied');
    }

    // Get next sequence number
    const nextSequence = Math.max(...conversation.messages.map(m => m.sequence_number), 0) + 1;

    // Create user message
    const userMessage = await this.prisma.conversationMessage.create({
      data: {
        conversation_id: conversationId,
        role: 'USER',
        content: request.content,
        message_type: request.messageType || 'TEXT',
        metadata: request.context,
        sequence_number: nextSequence
      }
    });

    // Prepare agent request with conversation history
    const agentRequest: AgentServiceRequest = {
      type: 'process_conversation',
      data: {
        conversationId,
        userMessage: request.content,
        conversationHistory: conversation.messages.map(msg => ({
          role: msg.role,
          content: msg.content,
          messageType: msg.message_type,
          metadata: msg.metadata,
          timestamp: msg.timestamp
        })),
        userProfile: {
          id: conversation.user.id,
          email: conversation.user.email,
          expertiseLevel: conversation.user.expertise_level,
          businessRole: conversation.user.business_role,
          businessContext: conversation.user.business_context as any
        },
        businessContext: conversation.user_context.businessContext
      },
      options: {
        workflowType: conversation.workflow_type,
        urgency: 'medium',
        depth: 'detailed'
      }
    };

    // Get agent response
    const agentResponse = await this.agentService.processRequest(agentRequest);

    if (!agentResponse.success || !agentResponse.data) {
      throw new Error('Failed to get response from agent service');
    }

    // Create agent response message
    const agentMessage = await this.prisma.conversationMessage.create({
      data: {
        conversation_id: conversationId,
        role: 'ASSISTANT',
        content: agentResponse.data.content,
        message_type: agentResponse.data.messageType as any,
        metadata: {
          agentResponse: agentResponse.data,
          processingMetadata: agentResponse.metadata
        },
        agent_reasoning: agentResponse.data.whyReasoning,
        sequence_number: nextSequence + 1
      }
    });

    // Update conversation with any architecture changes
    if (agentResponse.data.architectureUpdate) {
      await this.updateConversationArchitecture(
        conversationId,
        agentResponse.data.architectureUpdate,
        agentResponse.data.whyReasoning,
        agentResponse.data.businessImpact
      );
    }

    // Update conversation session data
    await this.prisma.conversation.update({
      where: { id: conversationId },
      data: {
        session_data: {
          ...conversation.session_data as any,
          lastActivity: new Date().toISOString(),
          progress: this.calculateConversationProgress(conversation.messages.length + 2),
          phase: this.determineConversationPhase(agentResponse.data)
        },
        agent_context: agentResponse.metadata,
        updated_at: new Date()
      }
    });

    return {
      messageId: agentMessage.id,
      agentResponse: agentResponse.data,
      conversationUpdate: {
        progress: this.calculateConversationProgress(conversation.messages.length + 2),
        phase: this.determineConversationPhase(agentResponse.data),
        estimatedCompletion: this.estimateCompletion(conversation)
      }
    };
  }

  private async updateConversationArchitecture(
    conversationId: string,
    architectureData: any,
    whyReasoning: any,
    businessImpact: any
  ): Promise<void> {
    await this.prisma.architecture.create({
      data: {
        conversation_id: conversationId,
        title: 'Architecture Update',
        architecture_data: architectureData,
        why_reasoning: whyReasoning,
        business_impact: businessImpact,
        technical_decisions: architectureData.decisions || {},
        diagram_type: 'SYSTEM_OVERVIEW',
        status: 'DRAFT'
      }
    });
  }

  private generateConversationTitle(requirements: string): string {
    // Simple title generation based on keywords
    const keywords = ['microservices', 'api', 'database', 'frontend', 'backend', 'mobile', 'cloud'];
    const found = keywords.find(keyword => 
      requirements.toLowerCase().includes(keyword)
    );
    
    const timestamp = new Date().toISOString().split('T')[0];
    return found 
      ? `${found.charAt(0).toUpperCase() + found.slice(1)} Architecture - ${timestamp}`
      : `Architecture Discussion - ${timestamp}`;
  }

  private estimateConversationDuration(userContext: any): number {
    // Estimate in minutes based on complexity and user expertise
    const baseTime = 15;
    const expertiseMultiplier = {
      'BEGINNER': 1.5,
      'INTERMEDIATE': 1.0,
      'ADVANCED': 0.8,
      'EXPERT': 0.6
    };
    
    return Math.round(baseTime * (expertiseMultiplier[userContext.expertise] || 1.0));
  }

  private calculateConversationProgress(messageCount: number): number {
    // Simple progress calculation based on message count
    // Typical conversation: 10-20 messages
    return Math.min(messageCount / 15, 1.0);
  }

  private determineConversationPhase(agentResponse: any): string {
    if (agentResponse.nextQuestions && agentResponse.nextQuestions.length > 0) {
      return 'requirements_gathering';
    }
    if (agentResponse.architectureUpdate) {
      return 'architecture_design';
    }
    if (agentResponse.educationalContent) {
      return 'education_delivery';
    }
    return 'completion';
  }

  private estimateCompletion(conversation: any): Date {
    const avgResponseTime = 2; // minutes
    const remainingMessages = Math.max(10 - conversation.messages.length, 0);
    return new Date(Date.now() + remainingMessages * avgResponseTime * 60 * 1000);
  }
}
```

### **STEP 6: Agent Service Integration**

#### **6.1 Agent Service HTTP Client**
```typescript
// src/services/agent.service.ts
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { AgentServiceRequest, AgentServiceResponse } from '../types/api';

export class AgentService {
  private client: AxiosInstance;
  private readonly maxRetries = 3;
  private readonly timeout = 30000; // 30 seconds

  constructor() {
    this.client = axios.create({
      baseURL: process.env.AGENT_SERVICE_URL || 'http://localhost:8000',
      timeout: this.timeout,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    });

    // Add request interceptor for logging
    this.client.interceptors.request.use(
      (config) => {
        console.log(`Agent Service Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        console.error('Agent Service Request Error:', error);
        return Promise.reject(error);
      }
    );

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => {
        console.log(`Agent Service Response: ${response.status} ${response.config.url}`);
        return response;
      },
      (error) => {
        console.error('Agent Service Response Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  async processRequest(request: AgentServiceRequest): Promise<AgentServiceResponse> {
    let lastError: Error;

    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      try {
        const response = await this.client.post('/api/agent/process', request);
        return response.data;
      } catch (error: any) {
        lastError = error;
        console.error(`Agent service attempt ${attempt} failed:`, error.message);

        if (attempt === this.maxRetries) {
          break;
        }

        // Exponential backoff: wait 2^attempt seconds
        await this.delay(Math.pow(2, attempt) * 1000);
      }
    }

    // All retries failed, return error response
    return {
      success: false,
      error: {
        code: 'AGENT_SERVICE_ERROR',
        message: lastError!.message,
        details: lastError!.response?.data || null
      }
    };
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await this.client.get('/health');
      return response.status === 200;
    } catch (error) {
      console.error('Agent service health check failed:', error);
      return false;
    }
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

### **STEP 7: Complete API Routes Implementation**

#### **7.1 Authentication Routes**
```typescript
// src/routes/auth.ts
import { Router } from 'express';
import { z } from 'zod';
import { AuthService } from '../services/auth.service';
import { validationMiddleware } from '../middleware/validation';

const router = Router();

// Validation schemas
const createUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  firstName: z.string().optional(),
  lastName: z.string().optional(),
  expertiseLevel: z.enum(['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT']).optional(),
  businessRole: z.string().optional(),
  businessContext: z.object({
    industry: z.string().optional(),
    companySize: z.enum(['startup', 'small', 'medium', 'large', 'enterprise']).optional(),
    budgetRange: z.enum(['limited', 'moderate', 'significant', 'unlimited']).optional(),
    timeline: z.enum(['immediate', 'weeks', 'months', 'flexible']).optional()
  }).optional()
});

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1)
});

// Routes
router.post('/register', validationMiddleware(createUserSchema), async (req, res) => {
  try {
    const authService = new AuthService(req.prisma);
    const user = await authService.createUser(req.body);
    
    res.status(201).json({
      success: true,
      data: { user }
    });
  } catch (error: any) {
    res.status(400).json({
      success: false,
      error: {
        code: 'REGISTRATION_FAILED',
        message: error.message
      }
    });
  }
});

router.post('/login', validationMiddleware(loginSchema), async (req, res) => {
  try {
    const authService = new AuthService(req.prisma);
    const loginResult = await authService.login(req.body);
    
    res.json({
      success: true,
      data: loginResult
    });
  } catch (error: any) {
    res.status(401).json({
      success: false,
      error: {
        code: 'LOGIN_FAILED',
        message: error.message
      }
    });
  }
});

router.post('/logout', async (req, res) => {
  try {
    const authHeader = req.headers.authorization;
    if (authHeader && authHeader.startsWith('Bearer ')) {
      const token = authHeader.substring(7);
      // Token invalidation would happen here
      // For now, just return success
    }
    
    res.json({
      success: true,
      message: 'Logged out successfully'
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: {
        code: 'LOGOUT_ERROR',
        message: error.message
      }
    });
  }
});

export default router;
```

#### **7.2 Conversation Routes**
```typescript
// src/routes/conversations.ts
import { Router } from 'express';
import { z } from 'zod';
import { ConversationService } from '../services/conversation.service';
import { AgentService } from '../services/agent.service';
import { validationMiddleware } from '../middleware/validation';

const router = Router();

// Validation schemas
const startConversationSchema = z.object({
  title: z.string().optional(),
  userRequirements: z.string().min(10),
  userContext: z.object({
    expertise: z.enum(['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT']),
    businessRole: z.string().optional(),
    businessContext: z.object({
      industry: z.string().optional(),
      companySize: z.string().optional(),
      budgetRange: z.string().optional(),
      timeline: z.string().optional()
    }).optional()
  }),
  workflowType: z.enum(['SEQUENTIAL', 'PARALLEL', 'CONDITIONAL', 'ITERATIVE']).optional()
});

const sendMessageSchema = z.object({
  content: z.string().min(1),
  messageType: z.enum(['TEXT', 'ARCHITECTURE_UPDATE', 'CLARIFICATION']).optional(),
  context: z.record(z.any()).optional()
});

// Routes
router.post('/', validationMiddleware(startConversationSchema), async (req, res) => {
  try {
    const agentService = new AgentService();
    const conversationService = new ConversationService(req.prisma, agentService);
    
    const result = await conversationService.startConversation(req.user!.id, req.body);
    
    res.status(201).json({
      success: true,
      data: result
    });
  } catch (error: any) {
    res.status(400).json({
      success: false,
      error: {
        code: 'CONVERSATION_START_FAILED',
        message: error.message
      }
    });
  }
});

router.get('/', async (req, res) => {
  try {
    const conversations = await req.prisma.conversation.findMany({
      where: { user_id: req.user!.id },
      orderBy: { updated_at: 'desc' },
      take: 20,
      include: {
        _count: {
          select: { messages: true }
        }
      }
    });
    
    res.json({
      success: true,
      data: { conversations }
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: {
        code: 'CONVERSATION_FETCH_FAILED',
        message: error.message
      }
    });
  }
});

router.get('/:conversationId', async (req, res) => {
  try {
    const conversation = await req.prisma.conversation.findFirst({
      where: {
        id: req.params.conversationId,
        user_id: req.user!.id
      },
      include: {
        messages: {
          orderBy: { sequence_number: 'asc' }
        },
        architectures: {
          orderBy: { created_at: 'desc' }
        }
      }
    });

    if (!conversation) {
      return res.status(404).json({
        success: false,
        error: {
          code: 'CONVERSATION_NOT_FOUND',
          message: 'Conversation not found or access denied'
        }
      });
    }
    
    res.json({
      success: true,
      data: { conversation }
    });
  } catch (error: any) {
    res.status(500).json({
      success: false,
      error: {
        code: 'CONVERSATION_FETCH_FAILED',
        message: error.message
      }
    });
  }
});

router.post('/:conversationId/messages', validationMiddleware(sendMessageSchema), async (req, res) => {
  try {
    const agentService = new AgentService();
    const conversationService = new ConversationService(req.prisma, agentService);
    
    const result = await conversationService.sendMessage(
      req.user!.id,
      req.params.conversationId,
      req.body
    );
    
    res.json({
      success: true,
      data: result
    });
  } catch (error: any) {
    res.status(400).json({
      success: false,
      error: {
        code: 'MESSAGE_SEND_FAILED',
        message: error.message
      }
    });
  }
});

export default router;
```

### **STEP 8: Error Handling & Middleware**

#### **8.1 Error Handling Middleware**
```typescript
// src/middleware/error-handling.ts
import { Request, Response, NextFunction } from 'express';

export interface ApiError extends Error {
  statusCode?: number;
  code?: string;
  details?: any;
}

export function errorHandler(
  error: ApiError,
  req: Request,
  res: Response,
  next: NextFunction
) {
  console.error('API Error:', error);

  const statusCode = error.statusCode || 500;
  const code = error.code || 'INTERNAL_SERVER_ERROR';
  const message = error.message || 'An unexpected error occurred';

  res.status(statusCode).json({
    success: false,
    error: {
      code,
      message,
      details: process.env.NODE_ENV === 'development' ? error.details : undefined
    }
  });
}

export function notFoundHandler(req: Request, res: Response) {
  res.status(404).json({
    success: false,
    error: {
      code: 'NOT_FOUND',
      message: `Route ${req.method} ${req.path} not found`
    }
  });
}
```

#### **8.2 Validation Middleware**
```typescript
// src/middleware/validation.ts
import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';

export function validationMiddleware(schema: z.ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      schema.parse(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: 'Request validation failed',
            details: error.errors
          }
        });
      } else {
        next(error);
      }
    }
  };
}
```

### **STEP 9: Testing Implementation**

#### **9.1 Test Setup & Configuration**
```typescript
// src/tests/setup.ts
import { PrismaClient } from '@prisma/client';
import { execSync } from 'child_process';

const prisma = new PrismaClient();

export async function setupTestDatabase() {
  // Reset database
  await prisma.$executeRaw`TRUNCATE TABLE users CASCADE`;
  await prisma.$executeRaw`TRUNCATE TABLE conversations CASCADE`;
  await prisma.$executeRaw`TRUNCATE TABLE conversation_messages CASCADE`;
  
  // Seed test data
  const testUser = await prisma.user.create({
    data: {
      email: 'test@example.com',
      password_hash: '$2a$12$test.hash.here',
      first_name: 'Test',
      last_name: 'User',
      expertise_level: 'INTERMEDIATE'
    }
  });

  return { testUser };
}

export async function teardownTestDatabase() {
  await prisma.$disconnect();
}
```

#### **9.2 API Integration Tests**
```typescript
// src/tests/api/conversations.test.ts
import request from 'supertest';
import app from '../../app';
import { setupTestDatabase, teardownTestDatabase } from '../setup';

describe('Conversation API', () => {
  let authToken: string;
  let testUser: any;

  beforeAll(async () => {
    const setup = await setupTestDatabase();
    testUser = setup.testUser;

    // Login to get auth token
    const loginResponse = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'test@example.com',
        password: 'testpass123'
      });

    authToken = loginResponse.body.data.token;
  });

  afterAll(async () => {
    await teardownTestDatabase();
  });

  describe('POST /api/conversations', () => {
    it('should create a new conversation', async () => {
      const response = await request(app)
        .post('/api/conversations')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          userRequirements: 'I need help designing a microservices architecture',
          userContext: {
            expertise: 'INTERMEDIATE',
            businessRole: 'Software Architect'
          }
        });

      expect(response.status).toBe(201);
      expect(response.body.success).toBe(true);
      expect(response.body.data.conversationId).toBeDefined();
      expect(response.body.data.firstQuestions).toBeInstanceOf(Array);
    });

    it('should reject invalid user requirements', async () => {
      const response = await request(app)
        .post('/api/conversations')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          userRequirements: 'short',
          userContext: {
            expertise: 'INTERMEDIATE'
          }
        });

      expect(response.status).toBe(400);
      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });
  });

  describe('GET /api/conversations', () => {
    it('should return user conversations', async () => {
      const response = await request(app)
        .get('/api/conversations')
        .set('Authorization', `Bearer ${authToken}`);

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.data.conversations).toBeInstanceOf(Array);
    });
  });
});
```

### **STEP 10: Performance Optimization**

#### **10.1 Database Connection Pooling**
```typescript
// src/config/database.ts
import { PrismaClient } from '@prisma/client';

export const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL
    }
  },
  log: process.env.NODE_ENV === 'development' ? ['query', 'info', 'warn', 'error'] : ['error']
});

// Connection pooling configuration
export const databaseConfig = {
  connectionLimit: parseInt(process.env.DB_POOL_SIZE || '10'),
  idleTimeout: parseInt(process.env.DB_IDLE_TIMEOUT || '30000'),
  acquireTimeout: parseInt(process.env.DB_ACQUIRE_TIMEOUT || '10000')
};
```

#### **10.2 Response Caching**
```typescript
// src/middleware/cache.ts
import { Request, Response, NextFunction } from 'express';

const cache = new Map<string, { data: any; timestamp: number; ttl: number }>();

export function cacheMiddleware(ttlSeconds: number = 300) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (req.method !== 'GET') {
      return next();
    }

    const cacheKey = `${req.originalUrl || req.url}:${req.user?.id || 'anonymous'}`;
    const cached = cache.get(cacheKey);

    if (cached && Date.now() - cached.timestamp < cached.ttl * 1000) {
      return res.json(cached.data);
    }

    // Override res.json to cache the response
    const originalJson = res.json;
    res.json = function(body: any) {
      if (res.statusCode === 200) {
        cache.set(cacheKey, {
          data: body,
          timestamp: Date.now(),
          ttl: ttlSeconds
        });
      }
      return originalJson.call(this, body);
    };

    next();
  };
}

// Cleanup old cache entries periodically
setInterval(() => {
  const now = Date.now();
  for (const [key, value] of cache.entries()) {
    if (now - value.timestamp > value.ttl * 1000) {
      cache.delete(key);
    }
  }
}, 60000); // Cleanup every minute
```

---

## 🚀 **DEPLOYMENT & PRODUCTION**

### **STEP 11: Production Configuration**

#### **11.1 Environment Variables**
```bash
# .env.production
NODE_ENV=production
PORT=3001
DATABASE_URL=postgresql://prod_user:secure_password@localhost:5432/agentic_architect_prod
JWT_SECRET=your-very-secure-256-bit-secret-key-for-production
JWT_EXPIRY=24h
CORS_ORIGIN=https://your-frontend-domain.com
AGENT_SERVICE_URL=https://your-agent-service-domain.com

# Performance settings
DB_POOL_SIZE=20
DB_IDLE_TIMEOUT=30000
DB_ACQUIRE_TIMEOUT=10000

# Monitoring
LOG_LEVEL=info
SENTRY_DSN=your-sentry-dsn-here
```

#### **11.2 Production Startup Script**
```typescript
// src/server.ts
import app from './app';
import { prisma } from './config/database';

const PORT = process.env.PORT || 3001;

async function startServer() {
  try {
    // Test database connection
    await prisma.$connect();
    console.log('✅ Database connected successfully');

    // Start server
    const server = app.listen(PORT, () => {
      console.log(`🚀 Backend server running on port ${PORT}`);
      console.log(`📊 Environment: ${process.env.NODE_ENV}`);
    });

    // Graceful shutdown
    process.on('SIGTERM', async () => {
      console.log('SIGTERM received, shutting down gracefully');
      server.close(async () => {
        await prisma.$disconnect();
        process.exit(0);
      });
    });

  } catch (error) {
    console.error('❌ Failed to start server:', error);
    process.exit(1);
  }
}

startServer();
```

---

## ✅ **VALIDATION & SUCCESS CRITERIA**

### **Backend Completion Checklist**
- [ ] **Database**: PostgreSQL schema deployed with all tables and relationships
- [ ] **Authentication**: JWT-based auth system working with secure password hashing
- [ ] **API Endpoints**: All REST endpoints functional with proper validation
- [ ] **Agent Integration**: HTTP client successfully communicating with Python agent service
- [ ] **Error Handling**: Comprehensive error handling and logging throughout
- [ ] **Testing**: Unit and integration tests with >80% coverage
- [ ] **Performance**: API responses consistently <500ms
- [ ] **Security**: All routes properly protected and validated
- [ ] **Documentation**: API documentation complete and accurate

### **Integration Success Metrics**
- [ ] **Agent Communication**: Backend successfully sends requests to agent service
- [ ] **Database Operations**: All CRUD operations working correctly
- [ ] **Authentication Flow**: Complete login/logout cycle functional
- [ ] **Conversation Management**: Full conversation lifecycle working
- [ ] **Real-time Updates**: Architecture updates properly persisted and retrievable

---

**🎯 This backend roadmap provides complete technical implementation details for autonomous AI agent execution! 🚀**