import React from 'react';
import ReactMarkdown from 'react-markdown';
import styled from 'styled-components';

const MarkdownContainer = styled.div`
  line-height: 1.6;
  color: #2d3748;

  h1, h2, h3, h4, h5, h6 {
    margin: 1.5rem 0 1rem 0;
    font-weight: 600;
    color: #1a202c;
  }

  h1 {
    font-size: 1.8rem;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 0.5rem;
  }

  h2 {
    font-size: 1.5rem;
    color: #667eea;
  }

  h3 {
    font-size: 1.3rem;
    color: #4a5568;
  }

  h4 {
    font-size: 1.1rem;
    color: #4a5568;
  }

  p {
    margin: 1rem 0;
    line-height: 1.7;
  }

  ul, ol {
    margin: 1rem 0;
    padding-left: 2rem;
  }

  li {
    margin: 0.5rem 0;
    line-height: 1.6;
  }

  blockquote {
    border-left: 4px solid #667eea;
    padding-left: 1rem;
    margin: 1rem 0;
    background: #f8fafc;
    border-radius: 0 6px 6px 0;
    padding: 1rem;
    font-style: italic;
  }

  code {
    background: #edf2f7;
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-family: 'Fira Code', Monaco, 'Consolas', 'Ubuntu Mono', monospace;
    font-size: 0.9rem;
    color: #e53e3e;
  }

  pre {
    background: #2d3748;
    color: #e2e8f0;
    padding: 1rem;
    border-radius: 6px;
    overflow-x: auto;
    margin: 1rem 0;
    
    code {
      background: transparent;
      color: inherit;
      padding: 0;
    }
  }

  strong {
    font-weight: 600;
    color: #1a202c;
  }

  em {
    font-style: italic;
    color: #4a5568;
  }

  a {
    color: #667eea;
    text-decoration: none;
    
    &:hover {
      text-decoration: underline;
    }
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    
    th, td {
      border: 1px solid #e2e8f0;
      padding: 0.75rem;
      text-align: left;
    }
    
    th {
      background: #f8fafc;
      font-weight: 600;
    }
  }

  hr {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 2rem 0;
  }
`;

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content, className }) => {
  return (
    <MarkdownContainer className={className}>
      <ReactMarkdown>{content}</ReactMarkdown>
    </MarkdownContainer>
  );
};

export default MarkdownRenderer;