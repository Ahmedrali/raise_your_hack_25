import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { ExpertiseLevel, BusinessContext, StartConversationRequest } from '../types';
import apiService from '../services/api';

const LandingContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
`;

const ContentCard = styled.div`
  background: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  width: 100%;
  text-align: center;
`;

const Title = styled.h1`
  font-size: 3rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`;

const Subtitle = styled.p`
  font-size: 1.25rem;
  color: #4a5568;
  margin-bottom: 2rem;
  line-height: 1.6;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  text-align: left;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const Label = styled.label`
  font-weight: 600;
  color: #2d3748;
  font-size: 0.9rem;
`;

const TextArea = styled.textarea`
  padding: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  resize: vertical;
  min-height: 120px;
  transition: border-color 0.2s;

  &:focus {
    outline: none;
    border-color: #667eea;
  }
`;

const Select = styled.select`
  padding: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  transition: border-color 0.2s;

  &:focus {
    outline: none;
    border-color: #667eea;
  }
`;

const Input = styled.input`
  padding: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;

  &:focus {
    outline: none;
    border-color: #667eea;
  }
`;

const SubmitButton = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
`;

const ErrorMessage = styled.div`
  background: #fed7d7;
  color: #c53030;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
`;

const LoadingSpinner = styled.div`
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid #ffffff;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 1s ease-in-out infinite;

  @keyframes spin {
    to { transform: rotate(360deg); }
  }
`;

const LoadingProgress = styled.div`
  margin-top: 1rem;
  text-align: center;
  color: #4a5568;
`;

const ProgressBar = styled.div`
  width: 100%;
  height: 8px;
  background-color: #e2e8f0;
  border-radius: 4px;
  margin: 1rem 0;
  overflow: hidden;
`;

const ProgressFill = styled.div<{ progress: number }>`
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
  width: ${props => props.progress}%;
  transition: width 0.5s ease-in-out;
`;

const LoadingSteps = styled.div`
  margin-top: 1rem;
  text-align: left;
  font-size: 0.9rem;
  color: #718096;
`;

const LoadingStep = styled.div<{ active: boolean; completed: boolean }>`
  padding: 0.5rem 0;
  color: ${props => props.completed ? '#48bb78' : props.active ? '#667eea' : '#a0aec0'};
  font-weight: ${props => props.active ? '600' : '400'};
  
  &:before {
    content: "${props => props.completed ? '✅' : props.active ? '🔄' : '⏳'}";
    margin-right: 0.5rem;
  }
`;

const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    userRequirements: '',
    expertise: 'INTERMEDIATE' as ExpertiseLevel,
    businessRole: '',
    industry: '',
    companySize: '',
    budgetRange: '',
    timeline: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const simulateProgress = () => {
    const steps = [
      { name: 'Authenticating...', duration: 500 },
      { name: 'Initializing AI agents...', duration: 1000 },
      { name: 'Planning workflow...', duration: 3000 },
      { name: 'Analyzing requirements...', duration: 8000 },
      { name: 'Researching best practices...', duration: 10000 },
      { name: 'Designing architecture...', duration: 12000 },
      { name: 'Generating explanations...', duration: 8000 },
      { name: 'Analyzing business impact...', duration: 8000 },
      { name: 'Creating learning content...', duration: 6000 },
      { name: 'Finalizing documentation...', duration: 4000 }
    ];

    let totalDuration = 0;
    steps.forEach(step => totalDuration += step.duration);
    
    let elapsed = 0;
    steps.forEach((step, index) => {
      setTimeout(() => {
        setCurrentStep(step.name);
        // Calculate progress as we start each step, not after completing it
        const progressPercent = Math.round((elapsed / totalDuration) * 85); // Max 85% until real completion
        setLoadingProgress(Math.min(progressPercent, 85)); // Ensure we never exceed 85%
      }, elapsed);
      elapsed += step.duration;
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    setLoadingProgress(0);
    setCurrentStep('Starting...');

    // Start progress simulation
    simulateProgress();

    try {
      // Validate required fields
      if (!formData.userRequirements.trim()) {
        throw new Error('Please describe your architecture requirements');
      }

      // Auto-login for demo purposes if not already authenticated
      if (!apiService.isAuthenticated()) {
        setCurrentStep('Creating user session...');
        const response = await apiService.createGuestUser();
        apiService.setToken(response.token);
      }

      // Build business context
      const businessContext: BusinessContext = {};
      if (formData.industry) businessContext.industry = formData.industry;
      if (formData.companySize) businessContext.companySize = formData.companySize as any;
      if (formData.budgetRange) businessContext.budgetRange = formData.budgetRange as any;
      if (formData.timeline) businessContext.timeline = formData.timeline as any;

      // Build conversation request
      const request: StartConversationRequest = {
        userRequirements: formData.userRequirements,
        userContext: {
          expertise: formData.expertise,
          businessRole: formData.businessRole || undefined,
          businessContext: Object.keys(businessContext).length > 0 ? businessContext : undefined
        },
        workflowType: 'SEQUENTIAL'
      };

      setCurrentStep('Processing with AI agents...');
      
      // Start conversation
      const response = await apiService.startConversation(request);
      
      setLoadingProgress(100);
      setCurrentStep('Analysis complete! Redirecting...');
      
      // Navigate to conversation page
      navigate(`/conversation/${response.conversationId}`);
    } catch (err: any) {
      setError(err.message || 'Failed to start conversation. Please try again.');
    } finally {
      setIsLoading(false);
      setLoadingProgress(0);
      setCurrentStep('');
    }
  };

  return (
    <LandingContainer>
      <ContentCard>
        <Title>Agentic Architect</Title>
        <Subtitle>
          AI-powered architecture consulting that teaches while it solves. 
          Get expert guidance on system design with comprehensive explanations and business insights.
        </Subtitle>

        {error && <ErrorMessage>{error}</ErrorMessage>}

        <Form onSubmit={handleSubmit}>
          <FormGroup>
            <Label htmlFor="userRequirements">
              Describe your architecture challenge or project *
            </Label>
            <TextArea
              id="userRequirements"
              name="userRequirements"
              value={formData.userRequirements}
              onChange={handleInputChange}
              placeholder="e.g., I need to design a scalable e-commerce platform that can handle 100K users with real-time inventory management..."
              required
            />
          </FormGroup>

          <FormGroup>
            <Label htmlFor="expertise">Your technical expertise level</Label>
            <Select
              id="expertise"
              name="expertise"
              value={formData.expertise}
              onChange={handleInputChange}
            >
              <option value="BEGINNER">Beginner - New to system architecture</option>
              <option value="INTERMEDIATE">Intermediate - Some architecture experience</option>
              <option value="ADVANCED">Advanced - Experienced architect</option>
              <option value="EXPERT">Expert - Senior/Principal architect</option>
            </Select>
          </FormGroup>

          <FormGroup>
            <Label htmlFor="businessRole">Your role (optional)</Label>
            <Input
              id="businessRole"
              name="businessRole"
              value={formData.businessRole}
              onChange={handleInputChange}
              placeholder="e.g., Software Architect, CTO, Lead Developer"
            />
          </FormGroup>

          <FormGroup>
            <Label htmlFor="industry">Industry (optional)</Label>
            <Select
              id="industry"
              name="industry"
              value={formData.industry}
              onChange={handleInputChange}
            >
              <option value="">Select industry...</option>
              <option value="Technology">Technology</option>
              <option value="E-commerce">E-commerce</option>
              <option value="Finance">Finance</option>
              <option value="Healthcare">Healthcare</option>
              <option value="Education">Education</option>
              <option value="Manufacturing">Manufacturing</option>
              <option value="Media">Media & Entertainment</option>
              <option value="Other">Other</option>
            </Select>
          </FormGroup>

          <FormGroup>
            <Label htmlFor="companySize">Company size (optional)</Label>
            <Select
              id="companySize"
              name="companySize"
              value={formData.companySize}
              onChange={handleInputChange}
            >
              <option value="">Select size...</option>
              <option value="startup">Startup (1-50 employees)</option>
              <option value="small">Small (51-200 employees)</option>
              <option value="medium">Medium (201-1000 employees)</option>
              <option value="large">Large (1001-5000 employees)</option>
              <option value="enterprise">Enterprise (5000+ employees)</option>
            </Select>
          </FormGroup>

          <FormGroup>
            <Label htmlFor="timeline">Project timeline (optional)</Label>
            <Select
              id="timeline"
              name="timeline"
              value={formData.timeline}
              onChange={handleInputChange}
            >
              <option value="">Select timeline...</option>
              <option value="immediate">Immediate (1-4 weeks)</option>
              <option value="weeks">Short-term (1-3 months)</option>
              <option value="months">Medium-term (3-12 months)</option>
              <option value="flexible">Flexible (12+ months)</option>
            </Select>
          </FormGroup>

          <SubmitButton type="submit" disabled={isLoading}>
            {isLoading ? (
              <>
                <LoadingSpinner /> {currentStep || 'Starting Analysis...'}
              </>
            ) : (
              'Start Architecture Consultation'
            )}
          </SubmitButton>

          {isLoading && (
            <LoadingProgress>
              <ProgressBar>
                <ProgressFill progress={loadingProgress} />
              </ProgressBar>
              <div style={{ fontSize: '0.9rem', color: '#667eea' }}>
                {currentStep} ({loadingProgress}%)
              </div>
              <div style={{ fontSize: '0.8rem', color: '#a0aec0', marginTop: '0.5rem' }}>
                This may take 1-3 minutes as our AI agents provide comprehensive analysis
              </div>
              <LoadingSteps>
                <LoadingStep 
                  active={currentStep === 'Analyzing requirements...'} 
                  completed={['Researching best practices...', 'Designing architecture...', 'Generating explanations...', 'Analyzing business impact...', 'Creating learning content...', 'Finalizing documentation...'].includes(currentStep) || loadingProgress >= 100}>
                  Analyzing requirements
                </LoadingStep>
                <LoadingStep 
                  active={currentStep === 'Researching best practices...'} 
                  completed={['Designing architecture...', 'Generating explanations...', 'Analyzing business impact...', 'Creating learning content...', 'Finalizing documentation...'].includes(currentStep) || loadingProgress >= 100}>
                  Researching best practices
                </LoadingStep>
                <LoadingStep 
                  active={currentStep === 'Designing architecture...'} 
                  completed={['Generating explanations...', 'Analyzing business impact...', 'Creating learning content...', 'Finalizing documentation...'].includes(currentStep) || loadingProgress >= 100}>
                  Designing architecture
                </LoadingStep>
                <LoadingStep 
                  active={currentStep === 'Generating explanations...'} 
                  completed={['Analyzing business impact...', 'Creating learning content...', 'Finalizing documentation...'].includes(currentStep) || loadingProgress >= 100}>
                  Generating explanations
                </LoadingStep>
                <LoadingStep 
                  active={['Analyzing business impact...', 'Creating learning content...', 'Finalizing documentation...'].includes(currentStep)} 
                  completed={loadingProgress >= 100}>
                  Finalizing analysis
                </LoadingStep>
              </LoadingSteps>
            </LoadingProgress>
          )}
        </Form>
      </ContentCard>
    </LandingContainer>
  );
};

export default LandingPage;
