import React from 'react';
import styled from 'styled-components';
import { DocumentationPanelProps, DecisionFactor, Tradeoff, Alternative, SuccessMetric } from '../types';

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

const TabContainer = styled.div`
  display: flex;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
`;

const Tab = styled.button<{ $active: boolean }>`
  flex: 1;
  padding: 0.75rem 1rem;
  border: none;
  background: ${props => props.$active ? 'white' : 'transparent'};
  color: ${props => props.$active ? '#667eea' : '#718096'};
  font-weight: ${props => props.$active ? '600' : '400'};
  font-size: 0.9rem;
  cursor: pointer;
  border-bottom: ${props => props.$active ? '2px solid #667eea' : '2px solid transparent'};
  transition: all 0.2s;

  &:hover {
    background: ${props => props.$active ? 'white' : '#edf2f7'};
    color: ${props => props.$active ? '#667eea' : '#4a5568'};
  }
`;

const ContentContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
`;

const EmptyState = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  color: #718096;
  padding: 2rem;
`;

const EmptyStateIcon = styled.div`
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
`;

const Section = styled.div`
  margin-bottom: 2rem;

  &:last-child {
    margin-bottom: 0;
  }
`;

const SectionTitle = styled.h4`
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #2d3748;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const SectionIcon = styled.span`
  font-size: 1.2rem;
`;

const Card = styled.div`
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;

  &:last-child {
    margin-bottom: 0;
  }
`;

const CardTitle = styled.h5`
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
`;

const CardContent = styled.p`
  margin: 0;
  color: #4a5568;
  line-height: 1.5;
`;

const ImportanceBar = styled.div<{ level: number }>`
  width: 100%;
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  margin: 0.5rem 0;
  position: relative;
  overflow: hidden;
`;

const ImportanceBarFill = styled.div<{ level: number }>`
  width: ${props => Math.min(100, Math.max(0, ((props.level || 0) / 5) * 100))}%;
  height: 100%;
  background: linear-gradient(90deg, #48bb78, #38a169);
  border-radius: 3px;
  transition: width 0.3s ease;
`;

const ScoreIndicator = styled.span<{ score: number }>`
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  background: ${props => {
    if (props.score >= 4) return '#c6f6d5';
    if (props.score >= 3) return '#fef5e7';
    return '#fed7d7';
  }};
  color: ${props => {
    if (props.score >= 4) return '#22543d';
    if (props.score >= 3) return '#744210';
    return '#742a2a';
  }};
`;

const List = styled.ul`
  margin: 0.5rem 0;
  padding-left: 1.5rem;
  color: #4a5568;
`;

const ListItem = styled.li`
  margin-bottom: 0.25rem;
  line-height: 1.4;
`;

const MetricGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
`;

const MetricCard = styled.div`
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 1rem;
  text-align: center;
`;

const MetricValue = styled.div`
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 0.25rem;
`;

const MetricLabel = styled.div`
  font-size: 0.9rem;
  color: #718096;
`;

const ConceptCard = styled(Card)`
  border-left: 4px solid #667eea;
`;

const ExampleCard = styled(Card)`
  border-left: 4px solid #48bb78;
`;

const ResourceLink = styled.a`
  color: #667eea;
  text-decoration: none;
  font-weight: 500;

  &:hover {
    text-decoration: underline;
  }
`;

const DocumentationPanel: React.FC<DocumentationPanelProps> = ({
  whyReasoning,
  businessImpact,
  educationalContent,
  activeTab,
  onTabChange
}) => {
  const renderWhyReasoning = () => {
    if (!whyReasoning) {
      return (
        <EmptyState>
          <EmptyStateIcon>🤔</EmptyStateIcon>
          <h4>No reasoning available</h4>
          <p>Decision reasoning will appear here as the AI analyzes your architecture.</p>
        </EmptyState>
      );
    }

    return (
      <div>
        <Section>
          <SectionTitle>
            <SectionIcon>⚖️</SectionIcon>
            Decision Factors
          </SectionTitle>
          {whyReasoning.decisionFactors?.map((factor: DecisionFactor, index: number) => (
            <Card key={index}>
              <CardTitle>{factor.factor}</CardTitle>
              <ImportanceBar level={factor.importance}>
                <ImportanceBarFill level={factor.importance} />
              </ImportanceBar>
              <CardContent>{factor.explanation}</CardContent>
              <div style={{ marginTop: '0.5rem', fontSize: '0.9rem', color: '#667eea' }}>
                <strong>Business Impact:</strong> {factor.businessImpact}
              </div>
            </Card>
          ))}
        </Section>

        <Section>
          <SectionTitle>
            <SectionIcon>🔄</SectionIcon>
            Trade-offs
          </SectionTitle>
          {whyReasoning.tradeoffs?.map((tradeoff: Tradeoff, index: number) => (
            <Card key={index}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <div>
                  <CardTitle style={{ color: '#38a169' }}>✅ Benefit</CardTitle>
                  <CardContent>{tradeoff.benefit}</CardContent>
                </div>
                <div>
                  <CardTitle style={{ color: '#e53e3e' }}>❌ Cost</CardTitle>
                  <CardContent>{tradeoff.cost}</CardContent>
                </div>
              </div>
              <div style={{ marginTop: '1rem', textAlign: 'center' }}>
                <ScoreIndicator score={tradeoff.impactLevel}>
                  Impact Level: {tradeoff.impactLevel}/5
                </ScoreIndicator>
              </div>
            </Card>
          ))}
        </Section>

        <Section>
          <SectionTitle>
            <SectionIcon>🔀</SectionIcon>
            Alternatives Considered
          </SectionTitle>
          {whyReasoning.alternatives?.map((alternative: Alternative, index: number) => (
            <Card key={index}>
              <CardTitle>
                {alternative.name}
                <ScoreIndicator score={alternative.viabilityScore} style={{ marginLeft: '1rem' }}>
                  Viability: {alternative.viabilityScore}/5
                </ScoreIndicator>
              </CardTitle>
              <CardContent>{alternative.description}</CardContent>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '1rem' }}>
                <div>
                  <strong style={{ color: '#38a169' }}>Pros:</strong>
                  <List>
                    {alternative.pros?.map((pro, i) => (
                      <ListItem key={i}>{pro}</ListItem>
                    ))}
                  </List>
                </div>
                <div>
                  <strong style={{ color: '#e53e3e' }}>Cons:</strong>
                  <List>
                    {alternative.cons?.map((con, i) => (
                      <ListItem key={i}>{con}</ListItem>
                    ))}
                  </List>
                </div>
              </div>
            </Card>
          ))}
        </Section>

        <Section>
          <SectionTitle>
            <SectionIcon>📏</SectionIcon>
            Architectural Principles
          </SectionTitle>
          <List>
            {whyReasoning.principles?.map((principle, index) => (
              <ListItem key={index}>{principle}</ListItem>
            ))}
          </List>
        </Section>
      </div>
    );
  };

  const renderBusinessImpact = () => {
    if (!businessImpact) {
      return (
        <EmptyState>
          <EmptyStateIcon>💼</EmptyStateIcon>
          <h4>No business analysis available</h4>
          <p>Business impact analysis will appear here as the AI evaluates your architecture.</p>
        </EmptyState>
      );
    }

    return (
      <div>
        <Section>
          <SectionTitle>
            <SectionIcon>💰</SectionIcon>
            ROI Analysis
          </SectionTitle>
          <MetricGrid>
            <MetricCard>
              <MetricValue>${businessImpact.roiAnalysis?.netPresentValue?.toLocaleString() || 'N/A'}</MetricValue>
              <MetricLabel>Net Present Value</MetricLabel>
            </MetricCard>
            <MetricCard>
              <MetricValue>{businessImpact.roiAnalysis?.paybackPeriodMonths || 'N/A'}</MetricValue>
              <MetricLabel>Payback Period (months)</MetricLabel>
            </MetricCard>
            <MetricCard>
              <MetricValue>{businessImpact.roiAnalysis?.confidenceLevel || 'N/A'}/5</MetricValue>
              <MetricLabel>Confidence Level</MetricLabel>
            </MetricCard>
          </MetricGrid>
        </Section>

        <Section>
          <SectionTitle>
            <SectionIcon>⚠️</SectionIcon>
            Risk Assessment
          </SectionTitle>
          <Card>
            <CardTitle>Overall Risk Level</CardTitle>
            <div style={{ textAlign: 'center', margin: '1rem 0' }}>
              <ScoreIndicator score={6 - (businessImpact.riskAssessment?.overallRiskLevel || 3)}>
                {businessImpact.riskAssessment?.overallRiskLevel || 3}/5
              </ScoreIndicator>
            </div>
          </Card>
        </Section>

        <Section>
          <SectionTitle>
            <SectionIcon>🚀</SectionIcon>
            Competitive Advantages
          </SectionTitle>
          <List>
            {businessImpact.competitiveAdvantages?.map((advantage, index) => (
              <ListItem key={index}>{advantage}</ListItem>
            ))}
          </List>
        </Section>

        <Section>
          <SectionTitle>
            <SectionIcon>📊</SectionIcon>
            Success Metrics
          </SectionTitle>
          <List>
            {businessImpact.successMetrics?.map((metric, index) => {
              if (typeof metric === 'string') {
                return <ListItem key={index}>{metric}</ListItem>;
              } else {
                const metricObj = metric as SuccessMetric;
                return (
                  <ListItem key={index}>
                    {`${metricObj.metric}: ${metricObj.current_baseline} → ${metricObj.target_value} (${metricObj.measurement_method})`}
                  </ListItem>
                );
              }
            })}
          </List>
        </Section>
      </div>
    );
  };

  const renderEducationalContent = () => {
    if (!educationalContent) {
      return (
        <EmptyState>
          <EmptyStateIcon>🎓</EmptyStateIcon>
          <h4>No educational content available</h4>
          <p>Learning materials and explanations will appear here as you explore architecture concepts.</p>
        </EmptyState>
      );
    }

    return (
      <div>
        <Section>
          <SectionTitle>
            <SectionIcon>💡</SectionIcon>
            Key Concepts
          </SectionTitle>
          {educationalContent.concepts?.map((concept, index) => (
            <ConceptCard key={index}>
              <CardTitle>{concept.concept}</CardTitle>
              <CardContent>{concept.explanation}</CardContent>
              <div style={{ marginTop: '0.5rem', fontSize: '0.9rem', color: '#667eea' }}>
                <strong>Business Relevance:</strong> {concept.businessRelevance}
              </div>
            </ConceptCard>
          ))}
        </Section>

        <Section>
          <SectionTitle>
            <SectionIcon>🏢</SectionIcon>
            Real-World Examples
          </SectionTitle>
          {educationalContent.examples?.map((example, index) => (
            <ExampleCard key={index}>
              <CardTitle>{example.title}</CardTitle>
              <CardContent>{example.description}</CardContent>
              {example.company && (
                <div style={{ marginTop: '0.5rem', fontSize: '0.9rem', color: '#48bb78' }}>
                  <strong>Company:</strong> {example.company} ({example.industry})
                </div>
              )}
              <div style={{ marginTop: '0.5rem', fontSize: '0.9rem', color: '#667eea' }}>
                <strong>Outcome:</strong> {example.outcome}
              </div>
            </ExampleCard>
          ))}
        </Section>

        <Section>
          <SectionTitle>
            <SectionIcon>📚</SectionIcon>
            Learning Resources
          </SectionTitle>
          {educationalContent.resources?.map((resource, index) => (
            <Card key={index}>
              <CardTitle>
                <ResourceLink href={resource.url} target="_blank" rel="noopener noreferrer">
                  {resource.title}
                </ResourceLink>
              </CardTitle>
              <CardContent>{resource.description}</CardContent>
              <div style={{ marginTop: '0.5rem', fontSize: '0.9rem', color: '#718096' }}>
                Type: {resource.type} • Difficulty: {resource.difficulty}
              </div>
            </Card>
          ))}
        </Section>
      </div>
    );
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'reasoning':
        return renderWhyReasoning();
      case 'business':
        return renderBusinessImpact();
      case 'learning':
        return renderEducationalContent();
      default:
        return renderWhyReasoning();
    }
  };

  return (
    <PanelContainer>
      <PanelHeader>
        <PanelTitle>Documentation & Analysis</PanelTitle>
      </PanelHeader>

      <TabContainer>
        <Tab
          $active={activeTab === 'reasoning'}
          onClick={() => onTabChange('reasoning')}
        >
          Why Reasoning
        </Tab>
        <Tab
          $active={activeTab === 'business'}
          onClick={() => onTabChange('business')}
        >
          Business Impact
        </Tab>
        <Tab
          $active={activeTab === 'learning'}
          onClick={() => onTabChange('learning')}
        >
          Learning
        </Tab>
      </TabContainer>

      <ContentContainer>
        {renderContent()}
      </ContentContainer>
    </PanelContainer>
  );
};

export default DocumentationPanel;
