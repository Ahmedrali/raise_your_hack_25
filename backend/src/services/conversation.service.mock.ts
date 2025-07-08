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

export class MockConversationService {
  constructor(
    private agentService: AgentService
  ) {}

  async startConversation(
    userId: string,
    request: StartConversationRequest
  ): Promise<StartConversationResponse> {
    // Create mock conversation record
    const conversationId = `conv-${Date.now()}`;
    
    console.log('Creating conversation with agent service...', {
      conversationId,
      userId,
      workflowType: request.workflowType
    });

    // Create mock user profile
    const userProfile = {
      id: userId,
      email: 'mock@example.com',
      expertiseLevel: request.userContext.expertise,
      businessRole: request.userContext.businessRole || 'Developer',
      businessContext: request.userContext.businessContext || {},
      createdAt: new Date()
    };

    // Send initial request to agent service - using the correct format for the agent service API
    const agentRequest = {
      conversation_id: conversationId,
      user_message: request.userRequirements,
      conversation_history: [],
      user_profile: {
        id: userProfile.id,
        email: userProfile.email,
        expertise_level: userProfile.expertiseLevel,
        business_role: userProfile.businessRole,
        business_context: userProfile.businessContext
      },
      business_context: request.userContext.businessContext || null,
      workflow_type: request.workflowType || 'SEQUENTIAL',
      options: {
        urgency: 'medium',
        depth: 'detailed'
      }
    };

    console.log('Sending request to agent service...', {
      agentServiceUrl: process.env.AGENT_SERVICE_URL || 'http://localhost:8000',
      requestType: 'process_conversation'
    });

    const agentResponse = await this.agentService.processRequest(agentRequest);

    if (!agentResponse.success || !agentResponse.data) {
      console.error('Agent service failed:', agentResponse.error);
      throw new Error(`Failed to initialize conversation with agent service: ${agentResponse.error?.message || 'Unknown error'}`);
    }

    console.log('Agent service responded successfully', {
      conversationId,
      hasContent: !!agentResponse.data.content,
      hasQuestions: !!(agentResponse.data.nextQuestions && agentResponse.data.nextQuestions.length > 0)
    });

    return {
      conversationId: conversationId,
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
    console.log('Processing message with agent service...', {
      conversationId,
      userId,
      messageLength: request.content.length
    });

    // Create mock conversation history
    const conversationHistory = [
      {
        role: 'USER',
        content: request.content,
        messageType: 'TEXT',
        timestamp: new Date()
      }
    ];

    // Create mock user profile
    const userProfile = {
      id: userId,
      email: 'mock@example.com',
      expertiseLevel: 'ADVANCED' as any,
      businessRole: 'CTO',
      businessContext: {},
      createdAt: new Date()
    };

    // Prepare agent request with conversation history - using the correct format for the agent service API
    const agentRequest = {
      conversation_id: conversationId,
      user_message: request.content,
      conversation_history: conversationHistory,
      user_profile: {
        id: userProfile.id,
        email: userProfile.email,
        expertise_level: userProfile.expertiseLevel,
        business_role: userProfile.businessRole,
        business_context: userProfile.businessContext
      },
      business_context: null,
      workflow_type: 'SEQUENTIAL',
      options: {
        urgency: 'medium',
        depth: 'detailed'
      }
    };

    console.log('Sending message request to agent service...', {
      agentServiceUrl: process.env.AGENT_SERVICE_URL || 'http://localhost:8000',
      requestType: 'process_conversation'
    });

    // Get agent response
    const agentResponse = await this.agentService.processRequest(agentRequest);

    if (!agentResponse.success || !agentResponse.data) {
      console.error('Agent service failed for message:', agentResponse.error);
      throw new Error(`Failed to get response from agent service: ${agentResponse.error?.message || 'Unknown error'}`);
    }

    console.log('Agent service responded to message successfully', {
      conversationId,
      hasContent: !!agentResponse.data.content,
      hasQuestions: !!(agentResponse.data.nextQuestions && agentResponse.data.nextQuestions.length > 0),
      hasActions: !!(agentResponse.data.suggestedActions && agentResponse.data.suggestedActions.length > 0)
    });

    const messageId = `msg-${Date.now()}`;

    return {
      messageId: messageId,
      agentResponse: agentResponse.data,
      conversationUpdate: {
        progress: 0.5,
        phase: this.determineConversationPhase(agentResponse.data),
        estimatedCompletion: new Date(Date.now() + 10 * 60 * 1000) // 10 minutes from now
      }
    };
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
}
