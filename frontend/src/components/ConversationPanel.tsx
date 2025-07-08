import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import { ConversationPanelProps, ConversationMessage } from '../types';
import MarkdownRenderer from './MarkdownRenderer';

const PanelContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
`;

const PanelHeader = styled.div`
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
`;

const PanelTitle = styled.h3`
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #2d3748;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const MessageBubble = styled.div<{ $isUser: boolean }>`
  max-width: 85%;
  padding: 1rem 1.25rem;
  border-radius: 18px;
  align-self: ${props => props.$isUser ? 'flex-end' : 'flex-start'};
  background: ${props => props.$isUser 
    ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' 
    : '#f7fafc'};
  color: ${props => props.$isUser ? 'white' : '#2d3748'};
  border: ${props => props.$isUser ? 'none' : '1px solid #e2e8f0'};
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  word-wrap: break-word;
  line-height: 1.5;
`;

const MessageMeta = styled.div<{ $isUser: boolean }>`
  font-size: 0.75rem;
  color: ${props => props.$isUser ? 'rgba(255, 255, 255, 0.8)' : '#718096'};
  margin-top: 0.5rem;
  text-align: ${props => props.$isUser ? 'right' : 'left'};
`;

const MessageType = styled.span`
  background: rgba(255, 255, 255, 0.2);
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  margin-left: 0.5rem;
`;

const InputContainer = styled.div`
  padding: 1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
`;

const InputForm = styled.form`
  display: flex;
  gap: 0.75rem;
  align-items: flex-end;
`;

const MessageInput = styled.textarea`
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  resize: none;
  min-height: 44px;
  max-height: 120px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: border-color 0.2s;

  &:focus {
    outline: none;
    border-color: #667eea;
  }

  &::placeholder {
    color: #a0aec0;
  }
`;

const SendButton = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  white-space: nowrap;

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
`;

const LoadingIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  color: #718096;
  font-style: italic;
`;

const LoadingDots = styled.div`
  display: flex;
  gap: 0.25rem;

  span {
    width: 6px;
    height: 6px;
    background: #cbd5e0;
    border-radius: 50%;
    animation: bounce 1.4s ease-in-out infinite both;

    &:nth-child(1) { animation-delay: -0.32s; }
    &:nth-child(2) { animation-delay: -0.16s; }
    &:nth-child(3) { animation-delay: 0s; }
  }

  @keyframes bounce {
    0%, 80%, 100% {
      transform: scale(0);
    } 40% {
      transform: scale(1);
    }
  }
`;

const EmptyState = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #718096;
  padding: 2rem;
`;

const EmptyStateIcon = styled.div`
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
`;

const SuggestedQuestions = styled.div`
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const SuggestedQuestion = styled.button`
  background: #edf2f7;
  border: 1px solid #e2e8f0;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 0.9rem;
  color: #4a5568;

  &:hover {
    background: #e2e8f0;
  }
`;

const ConversationPanel: React.FC<ConversationPanelProps> = ({
  conversation,
  messages,
  onSendMessage,
  isLoading
}) => {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Auto-resize textarea
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.style.height = 'auto';
      inputRef.current.style.height = `${inputRef.current.scrollHeight}px`;
    }
  }, [inputValue]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue.trim());
      setInputValue('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleSuggestedQuestion = (question: string) => {
    if (!isLoading) {
      onSendMessage(question);
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const getMessageTypeLabel = (type: string) => {
    switch (type) {
      case 'ARCHITECTURE_UPDATE': return 'Architecture';
      case 'EDUCATIONAL_CONTENT': return 'Learning';
      case 'BUSINESS_ANALYSIS': return 'Business';
      case 'WHY_REASONING': return 'Reasoning';
      default: return 'Message';
    }
  };

  return (
    <PanelContainer>
      <PanelHeader>
        <PanelTitle>Conversation</PanelTitle>
      </PanelHeader>

      <MessagesContainer>
        {messages.length === 0 ? (
          <EmptyState>
            <EmptyStateIcon>💬</EmptyStateIcon>
            <h4>Start your architecture consultation</h4>
            <p>Ask questions about your system design, requirements, or architecture patterns.</p>
            
            <SuggestedQuestions>
              <SuggestedQuestion onClick={() => handleSuggestedQuestion("What are the key architectural decisions I need to make?")}>
                What are the key architectural decisions I need to make?
              </SuggestedQuestion>
              <SuggestedQuestion onClick={() => handleSuggestedQuestion("How should I handle scalability requirements?")}>
                How should I handle scalability requirements?
              </SuggestedQuestion>
              <SuggestedQuestion onClick={() => handleSuggestedQuestion("What security considerations should I include?")}>
                What security considerations should I include?
              </SuggestedQuestion>
            </SuggestedQuestions>
          </EmptyState>
        ) : (
          <>
            {messages.map((message) => (
              <MessageBubble key={message.id} $isUser={message.role === 'USER'}>
                {message.role === 'ASSISTANT' ? (
                  <MarkdownRenderer content={message.content} />
                ) : (
                  message.content
                )}
                <MessageMeta $isUser={message.role === 'USER'}>
                  {formatTimestamp(message.timestamp)}
                  {message.role === 'ASSISTANT' && (
                    <MessageType>
                      {getMessageTypeLabel(message.messageType)}
                    </MessageType>
                  )}
                </MessageMeta>
              </MessageBubble>
            ))}
            
            {isLoading && (
              <LoadingIndicator>
                <LoadingDots>
                  <span></span>
                  <span></span>
                  <span></span>
                </LoadingDots>
                AI is analyzing your request...
              </LoadingIndicator>
            )}
            
            <div ref={messagesEndRef} />
          </>
        )}
      </MessagesContainer>

      <InputContainer>
        <InputForm onSubmit={handleSubmit}>
          <MessageInput
            ref={inputRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about architecture patterns, scalability, security, or any technical question..."
            disabled={isLoading}
            rows={1}
          />
          <SendButton type="submit" disabled={!inputValue.trim() || isLoading}>
            Send
          </SendButton>
        </InputForm>
      </InputContainer>
    </PanelContainer>
  );
};

export default ConversationPanel;
