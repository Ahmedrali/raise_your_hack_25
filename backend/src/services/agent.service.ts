import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { AgentServiceRequest, AgentServiceResponse } from '../types/api';

export class AgentService {
  private client: AxiosInstance;
  private readonly maxRetries = 3;
  private readonly timeout = 120000; // 120 seconds (2 minutes) for real LLM processing

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
    let lastError: Error = new Error('Unknown error');

    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      try {
        // Transform the request to match agent service expected format
        const agentRequest = {
          conversation_id: request.data.conversationId,
          user_message: request.data.userMessage,
          conversation_history: request.data.conversationHistory || [],
          user_profile: {
            id: request.data.userProfile.id,
            email: request.data.userProfile.email,
            expertise_level: request.data.userProfile.expertiseLevel
          },
          business_context: request.data.businessContext ? {
            industry: request.data.businessContext.industry,
            company_size: request.data.businessContext.companySize,
            budget_range: request.data.businessContext.budgetRange,
            timeline: request.data.businessContext.timeline
          } : undefined,
          workflow_type: request.options?.workflowType?.toUpperCase() || 'SEQUENTIAL',
          options: request.options || {}
        };

        console.log('Sending request to agent service:', JSON.stringify(agentRequest, null, 2));
        const response = await this.client.post('/api/agent/process', agentRequest);
        return response.data;
      } catch (error: any) {
        lastError = error;
        console.error(`Agent service attempt ${attempt} failed:`, error.message);
        console.error('Error details:', error.response?.data);

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
        message: lastError.message,
        details: (lastError as any)?.response?.data || null
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
