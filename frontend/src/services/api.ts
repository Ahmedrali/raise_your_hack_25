import axios from 'axios';
import {
  ApiResponse,
  StartConversationRequest,
  StartConversationResponse,
  SendMessageRequest,
  SendMessageResponse,
  Conversation,
  User
} from '../types';

class ApiService {
  private client: any;
  private token: string | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.REACT_APP_API_URL || 'http://54.194.104.191:3001/api',
      timeout: 180000, // 3 minutes for complex agent workflows
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.clearToken();
          // Redirect to login or show auth modal
        }
        return Promise.reject(error);
      }
    );

    // Load token from localStorage
    this.loadToken();
  }

  private loadToken(): void {
    const token = localStorage.getItem('auth_token');
    if (token) {
      this.token = token;
    }
  }

  private saveToken(token: string): void {
    this.token = token;
    localStorage.setItem('auth_token', token);
  }

  private clearToken(): void {
    this.token = null;
    localStorage.removeItem('auth_token');
  }

  // Authentication methods
  async login(email: string, password: string): Promise<{ user: User; token: string }> {
    try {
      const response: any = await this.client.post('/auth/login', { email, password });
      
      if (response.data.success && response.data.data) {
        this.saveToken(response.data.data.token);
        return {
          user: response.data.data.user,
          token: response.data.data.token
        };
      }
      
      throw new Error('Login failed');
    } catch (error: any) {
      throw new Error(error.response?.data?.error?.message || 'Login failed');
    }
  }

  async register(userData: {
    email: string;
    password: string;
    firstName?: string;
    lastName?: string;
    expertiseLevel?: string;
    businessRole?: string;
    businessContext?: any;
  }): Promise<User> {
    try {
      const response: any = await this.client.post('/auth/register', userData);
      
      if (response.data.success && response.data.data) {
        return response.data.data.user;
      }
      
      throw new Error('Registration failed');
    } catch (error: any) {
      throw new Error(error.response?.data?.error?.message || 'Registration failed');
    }
  }

  async logout(): Promise<void> {
    try {
      await this.client.post('/auth/logout');
    } catch (error) {
      // Continue with logout even if API call fails
    } finally {
      this.clearToken();
    }
  }

  // Conversation methods
  async startConversation(request: StartConversationRequest): Promise<StartConversationResponse> {
    try {
      const response: any = await this.client.post('/conversations', request);
      
      if (response.data.success && response.data.data) {
        return response.data.data;
      }
      
      throw new Error('Failed to start conversation');
    } catch (error: any) {
      throw new Error(error.response?.data?.error?.message || 'Failed to start conversation');
    }
  }

  async getConversations(): Promise<Conversation[]> {
    try {
      const response: any = await this.client.get('/conversations');
      
      if (response.data.success && response.data.data) {
        return response.data.data.conversations;
      }
      
      return [];
    } catch (error: any) {
      throw new Error(error.response?.data?.error?.message || 'Failed to fetch conversations');
    }
  }

  async getConversation(conversationId: string): Promise<Conversation> {
    try {
      const response: any = await this.client.get(`/conversations/${conversationId}`);
      
      if (response.data.success && response.data.data) {
        return response.data.data.conversation;
      }
      
      throw new Error('Conversation not found');
    } catch (error: any) {
      throw new Error(error.response?.data?.error?.message || 'Failed to fetch conversation');
    }
  }

  async sendMessage(conversationId: string, request: SendMessageRequest): Promise<SendMessageResponse> {
    try {
      const response: any = await this.client.post(`/conversations/${conversationId}/messages`, request);
      
      if (response.data.success && response.data.data) {
        return response.data.data;
      }
      
      throw new Error('Failed to send message');
    } catch (error: any) {
      throw new Error(error.response?.data?.error?.message || 'Failed to send message');
    }
  }

  // Health check
  async healthCheck(): Promise<boolean> {
    try {
      const response = await this.client.get('/health');
      return response.status === 200;
    } catch (error) {
      return false;
    }
  }

  // Utility methods
  isAuthenticated(): boolean {
    return !!this.token;
  }

  getToken(): string | null {
    return this.token;
  }

  async createGuestUser(): Promise<{ user: User; token: string }> {
    try {
      const response: any = await this.client.post('/auth/guest');
      if (response.data.success && response.data.data) {
        this.setToken(response.data.data.token);
        return {
          user: response.data.data.user,
          token: response.data.data.token
        };
      }
      throw new Error('Guest user creation failed');
    } catch (error: any) {
      throw new Error(error.response?.data?.error?.message || 'Guest user creation failed');
    }
  }

  setToken(token: string): void {
    this.token = token;
    localStorage.setItem('auth_token', token);
  }
}

// Create singleton instance
const apiService = new ApiService();
export default apiService;

// Export for testing
export { ApiService };
