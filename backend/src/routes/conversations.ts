import { Router } from 'express';
import { z } from 'zod';
import { validationMiddleware } from '../middleware/validation';
import { AuthenticatedRequest } from '../middleware/auth';
import { ConversationService } from '../services/conversation.service';
import { AgentService } from '../services/agent.service';
import PrismaService from '../services/prisma.service';

const router = Router();

// Initialize services
const prisma = PrismaService.getInstance();
const agentService = new AgentService();
const conversationService = new ConversationService(prisma, agentService);

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
router.post('/', validationMiddleware(startConversationSchema), async (req: AuthenticatedRequest, res) => {
  try {
    if (!req.user) {
      res.status(401).json({
        success: false,
        error: {
          code: 'UNAUTHORIZED',
          message: 'User not authenticated'
        }
      });
      return;
    }

    // Map the request to the expected format
    const startConversationRequest = {
      userRequirements: req.body.userRequirements,
      userContext: {
        expertise: req.body.userContext.expertise,
        businessRole: req.body.userContext.businessRole,
        businessContext: req.body.userContext.businessContext
      },
      workflowType: req.body.workflowType || 'SEQUENTIAL'
    };

    console.log('Starting conversation with agent service...', {
      userId: req.user.id,
      userRequirements: startConversationRequest.userRequirements.substring(0, 100) + '...'
    });

    const result = await conversationService.startConversation(req.user.id, startConversationRequest);
    
    res.status(201).json({
      success: true,
      data: result
    });
  } catch (error: any) {
    console.error('Conversation start failed:', error);
    res.status(400).json({
      success: false,
      error: {
        code: 'CONVERSATION_START_FAILED',
        message: error.message || 'Failed to start conversation'
      }
    });
  }
});

router.get('/', async (req: AuthenticatedRequest, res) => {
  try {
    if (!req.user) {
      res.status(401).json({
        success: false,
        error: {
          code: 'UNAUTHORIZED',
          message: 'User not authenticated'
        }
      });
      return;
    }

    const conversations = await prisma.conversation.findMany({
      where: {
        user_id: req.user.id
      },
      select: {
        id: true,
        title: true,
        status: true,
        created_at: true,
        updated_at: true,
        _count: {
          select: {
            messages: true
          }
        }
      },
      orderBy: {
        updated_at: 'desc'
      }
    });
    
    res.json({
      success: true,
      data: { 
        conversations: conversations.map((conv: any) => ({
          id: conv.id,
          title: conv.title,
          status: conv.status,
          createdAt: conv.created_at.toISOString(),
          updatedAt: conv.updated_at.toISOString(),
          _count: conv._count
        }))
      }
    });
  } catch (error: any) {
    console.error('Failed to fetch conversations:', error);
    res.status(500).json({
      success: false,
      error: {
        code: 'CONVERSATION_FETCH_FAILED',
        message: error.message
      }
    });
  }
});

router.get('/:conversationId', async (req: AuthenticatedRequest, res) => {
  try {
    const { conversationId } = req.params;
    
    if (!req.user) {
      res.status(401).json({
        success: false,
        error: {
          code: 'UNAUTHORIZED',
          message: 'User not authenticated'
        }
      });
      return;
    }

    const conversation = await prisma.conversation.findFirst({
      where: {
        id: conversationId!,
        user_id: req.user.id
      },
      include: {
        messages: {
          orderBy: {
            sequence_number: 'asc'
          }
        },
        architectures: {
          orderBy: {
            created_at: 'desc'
          }
        }
      }
    });

    if (!conversation) {
      res.status(404).json({
        success: false,
        error: {
          code: 'CONVERSATION_NOT_FOUND',
          message: 'Conversation not found or access denied'
        }
      });
      return;
    }
    
    res.json({
      success: true,
      data: { 
        conversation: {
          id: conversation.id,
          title: conversation.title,
          status: conversation.status,
          userRequirements: conversation.user_requirements,
          createdAt: conversation.created_at.toISOString(),
          updatedAt: conversation.updated_at.toISOString(),
          messages: conversation.messages.map((msg: any) => ({
            id: msg.id,
            role: msg.role,
            content: msg.content,
            messageType: msg.message_type,
            timestamp: msg.timestamp.toISOString(),
            sequenceNumber: msg.sequence_number,
            metadata: msg.metadata,
            agentReasoning: msg.agent_reasoning
          })),
          architectures: conversation.architectures.map((arch: any) => ({
            id: arch.id,
            title: arch.title,
            description: arch.description,
            architectureData: arch.architecture_data,
            diagramType: arch.diagram_type,
            status: arch.status,
            createdAt: arch.created_at.toISOString(),
            updatedAt: arch.updated_at.toISOString()
          }))
        }
      }
    });
  } catch (error: any) {
    console.error('Failed to fetch conversation:', error);
    res.status(500).json({
      success: false,
      error: {
        code: 'CONVERSATION_FETCH_FAILED',
        message: error.message
      }
    });
  }
});

router.post('/:conversationId/messages', validationMiddleware(sendMessageSchema), async (req: AuthenticatedRequest, res) => {
  try {
    const { conversationId } = req.params;
    
    if (!req.user) {
      res.status(401).json({
        success: false,
        error: {
          code: 'UNAUTHORIZED',
          message: 'User not authenticated'
        }
      });
      return;
    }

    const sendMessageRequest = {
      content: req.body.content,
      messageType: req.body.messageType || 'TEXT',
      context: req.body.context || {}
    };

    console.log('Sending message to agent service...', {
      conversationId,
      userId: req.user.id,
      messageLength: sendMessageRequest.content.length
    });

    const result = await conversationService.sendMessage(req.user.id, conversationId!, sendMessageRequest);
    
    res.json({
      success: true,
      data: result
    });
  } catch (error: any) {
    console.error('Message send failed:', error);
    res.status(400).json({
      success: false,
      error: {
        code: 'MESSAGE_SEND_FAILED',
        message: error.message || 'Failed to send message'
      }
    });
  }
});

export default router;
