import {
  StartConversationRequest,
  StartConversationResponse,
  SendMessageRequest,
  SendMessageResponse,
  AgentServiceRequest,
  WorkflowType,
  ConversationStatus
} from '../types/api';
import { AgentService } from './agent.service';

export class ConversationService {
  constructor(
    private prisma: any,
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
        userMessage: request.userRequirements,
        conversationHistory: [],
        userProfile: {
          id: user!.id,
          email: user!.email,
          expertiseLevel: user!.expertise_level,
          businessRole: user!.business_role,
          businessContext: user!.business_context as any,
          createdAt: user!.created_at
        },
        ...(request.userContext.businessContext && { businessContext: request.userContext.businessContext })
      },
      options: {
        ...(request.workflowType && { workflowType: request.workflowType }),
        urgency: 'medium' as const,
        depth: 'detailed' as const
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
    const nextSequence = Math.max(...conversation.messages.map((m: any) => m.sequence_number), 0) + 1;

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
        conversationHistory: conversation.messages.map((msg: any) => ({
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
          businessContext: conversation.user.business_context as any,
          createdAt: conversation.user.created_at
        },
        businessContext: (conversation.user_context as any)?.businessContext
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
          ...(conversation.session_data as any),
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
    const expertiseMultiplier: Record<string, number> = {
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
