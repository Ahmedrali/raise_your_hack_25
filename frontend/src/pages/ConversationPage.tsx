import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import styled from 'styled-components';
import ConversationPanel from '../components/ConversationPanel';
import VisualizationPanel from '../components/VisualizationPanel';
import DocumentationPanel from '../components/DocumentationPanel';
import MarkdownRenderer from '../components/MarkdownRenderer';
import {
  Conversation,
  ConversationMessage,
  ArchitectureData,
  WhyReasoning,
  BusinessImpact,
  EducationalContent,
  DiagramType
} from '../types';
import apiService from '../services/api';

const PageContainer = styled.div`
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f7fafc;
`;

const Header = styled.header`
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 1rem 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
`;

const HeaderTitle = styled.h1`
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
`;

const HeaderSubtitle = styled.p`
  font-size: 0.9rem;
  color: #718096;
  margin: 0.25rem 0 0 0;
`;

const MainContent = styled.div`
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1rem;
  padding: 1rem;
  overflow: hidden;
`;

const LoadingContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  flex-direction: column;
  gap: 1rem;
`;

const LoadingSpinner = styled.div`
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const LoadingText = styled.p`
  color: #4a5568;
  font-size: 1.1rem;
`;

const ErrorContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  flex-direction: column;
  gap: 1rem;
  padding: 2rem;
`;

const ErrorMessage = styled.div`
  background: #fed7d7;
  color: #c53030;
  padding: 1rem 2rem;
  border-radius: 8px;
  text-align: center;
  max-width: 500px;
`;

const RetryButton = styled.button`
  background: #667eea;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    background: #5a67d8;
  }
`;

const ConversationPage: React.FC = () => {
  const { id: conversationId } = useParams<{ id: string }>();
  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<ConversationMessage[]>([]);
  const [currentArchitecture, setCurrentArchitecture] = useState<ArchitectureData | null>(null);
  const [whyReasoning, setWhyReasoning] = useState<WhyReasoning | null>(null);
  const [businessImpact, setBusinessImpact] = useState<BusinessImpact | null>(null);
  const [educationalContent, setEducationalContent] = useState<EducationalContent | null>(null);
  const [selectedDiagramType, setSelectedDiagramType] = useState<DiagramType>('SYSTEM_OVERVIEW');
  const [activeDocTab, setActiveDocTab] = useState('reasoning');
  const [isLoading, setIsLoading] = useState(true);
  const [isMessageLoading, setIsMessageLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load conversation data
  useEffect(() => {
    if (conversationId) {
      loadConversation();
    }
  }, [conversationId]);

  const loadConversation = async () => {
    if (!conversationId) return;

    try {
      setIsLoading(true);
      setError(null);
      
      const conversationData = await apiService.getConversation(conversationId);
      setConversation(conversationData);
      setMessages(conversationData.messages || []);
      
      // Extract latest architecture data from messages
      const latestArchMessage = conversationData.messages
        ?.slice()
        .reverse()
        .find(msg => msg.messageType === 'ARCHITECTURE_UPDATE' && msg.metadata?.agentResponse?.architectureUpdate);
      
      if (latestArchMessage?.metadata?.agentResponse) {
        const agentResponse = latestArchMessage.metadata.agentResponse;
        setCurrentArchitecture(agentResponse.architectureUpdate || null);
        setWhyReasoning(agentResponse.whyReasoning || null);
        setBusinessImpact(agentResponse.businessImpact || null);
        setEducationalContent(agentResponse.educationalContent || null);
      }
      
    } catch (err: any) {
      setError(err.message || 'Failed to load conversation');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (content: string) => {
    if (!conversationId || !content.trim()) return;

    try {
      setIsMessageLoading(true);
      setError(null);

      // Add user message to UI immediately
      const userMessage: ConversationMessage = {
        id: `temp-${Date.now()}`,
        role: 'USER',
        content: content.trim(),
        messageType: 'TEXT',
        timestamp: new Date().toISOString(),
        sequenceNumber: messages.length + 1
      };
      setMessages(prev => [...prev, userMessage]);

      // Send message to backend
      const response = await apiService.sendMessage(conversationId, {
        content: content.trim(),
        messageType: 'TEXT'
      });

      // Add agent response to messages
      const agentMessage: ConversationMessage = {
        id: response.messageId,
        role: 'ASSISTANT',
        content: response.agentResponse.content,
        messageType: response.agentResponse.messageType as any,
        metadata: { agentResponse: response.agentResponse },
        timestamp: new Date().toISOString(),
        sequenceNumber: messages.length + 2
      };

      setMessages(prev => {
        // Remove temp user message and add both real messages
        const withoutTemp = prev.filter(msg => !msg.id.startsWith('temp-'));
        return [...withoutTemp, userMessage, agentMessage];
      });

      // Update architecture data if provided
      if (response.agentResponse.architectureUpdate) {
        setCurrentArchitecture(response.agentResponse.architectureUpdate);
      }
      if (response.agentResponse.whyReasoning) {
        setWhyReasoning(response.agentResponse.whyReasoning);
      }
      if (response.agentResponse.businessImpact) {
        setBusinessImpact(response.agentResponse.businessImpact);
      }
      if (response.agentResponse.educationalContent) {
        setEducationalContent(response.agentResponse.educationalContent);
      }

    } catch (err: any) {
      setError(err.message || 'Failed to send message');
      // Remove the temporary user message on error
      setMessages(prev => prev.filter(msg => !msg.id.startsWith('temp-')));
    } finally {
      setIsMessageLoading(false);
    }
  };

  const handleDiagramTypeChange = (type: DiagramType) => {
    setSelectedDiagramType(type);
  };

  const handleDocTabChange = (tab: string) => {
    setActiveDocTab(tab);
  };

  if (isLoading) {
    return (
      <LoadingContainer>
        <LoadingSpinner />
        <LoadingText>Loading conversation...</LoadingText>
      </LoadingContainer>
    );
  }

  if (error && !conversation) {
    return (
      <ErrorContainer>
        <ErrorMessage>{error}</ErrorMessage>
        <RetryButton onClick={loadConversation}>
          Retry
        </RetryButton>
      </ErrorContainer>
    );
  }

  return (
    <PageContainer>
      <Header>
        <HeaderTitle>
          {conversation?.title || 'Architecture Consultation'}
        </HeaderTitle>
        <HeaderSubtitle>
          {conversation?.status === 'ACTIVE' ? 'Active Session' : conversation?.status} • 
          {messages.length} messages • 
          {conversation?.workflowType || 'Sequential'} workflow
        </HeaderSubtitle>
      </Header>

      <MainContent>
        <ConversationPanel
          conversation={conversation}
          messages={messages}
          onSendMessage={handleSendMessage}
          isLoading={isMessageLoading}
        />

        <VisualizationPanel
          architecture={currentArchitecture}
          diagramType={selectedDiagramType}
          onDiagramTypeChange={handleDiagramTypeChange}
          isLoading={false}
        />

        <DocumentationPanel
          whyReasoning={whyReasoning}
          businessImpact={businessImpact}
          educationalContent={educationalContent}
          activeTab={activeDocTab}
          onTabChange={handleDocTabChange}
        />
      </MainContent>

      {error && (
        <div style={{ 
          position: 'fixed', 
          bottom: '1rem', 
          right: '1rem', 
          background: '#fed7d7', 
          color: '#c53030', 
          padding: '1rem', 
          borderRadius: '8px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          zIndex: 1000
        }}>
          {error}
        </div>
      )}
    </PageContainer>
  );
};

export default ConversationPage;
