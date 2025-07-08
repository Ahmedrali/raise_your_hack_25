from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union
from enum import Enum
from datetime import datetime

class ExpertiseLevel(str, Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    EXPERT = "EXPERT"

class WorkflowType(str, Enum):
    SEQUENTIAL = "SEQUENTIAL"
    PARALLEL = "PARALLEL"
    CONDITIONAL = "CONDITIONAL"
    ITERATIVE = "ITERATIVE"

class MessageRole(str, Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"

class BusinessContext(BaseModel):
    industry: Optional[str] = None
    company_size: Optional[str] = None
    budget_range: Optional[str] = None
    timeline: Optional[str] = None
    compliance_requirements: List[str] = Field(default_factory=list)
    existing_technologies: List[str] = Field(default_factory=list)

class UserProfile(BaseModel):
    id: str
    email: str
    expertise_level: ExpertiseLevel
    business_role: Optional[str] = None
    business_context: Optional[BusinessContext] = None
    preferences: Dict[str, Any] = Field(default_factory=dict)

class ConversationMessage(BaseModel):
    role: MessageRole
    content: str
    message_type: str = "TEXT"
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime

class AgentRequest(BaseModel):
    type: str  # 'process_conversation', 'generate_architecture', 'analyze_requirements'
    data: Dict[str, Any]
    options: Dict[str, Any] = Field(default_factory=dict)

class DecisionFactor(BaseModel):
    factor: str
    importance: int = Field(ge=1, le=5)
    explanation: str
    business_impact: str

class Tradeoff(BaseModel):
    benefit: str
    cost: str
    impact_level: int = Field(ge=1, le=5)
    quantified_metrics: Dict[str, Any] = Field(default_factory=dict)

class Alternative(BaseModel):
    name: str
    description: str
    pros: List[str]
    cons: List[str]
    viability_score: int = Field(ge=1, le=5)
    use_cases: List[str]

class WhyReasoning(BaseModel):
    decision_factors: List[DecisionFactor]
    tradeoffs: List[Tradeoff]
    alternatives: List[Alternative]
    principles: List[str]
    business_alignment: List[str]
    confidence_level: int = Field(ge=1, le=5)

class ROIAnalysis(BaseModel):
    initial_investment: Dict[str, float]
    ongoing_costs: Dict[str, float]
    expected_benefits: Dict[str, float]
    payback_period_months: int
    net_present_value: float
    confidence_level: int = Field(ge=1, le=5)

class RiskAssessment(BaseModel):
    technical_risks: List[Dict[str, Any]]
    business_risks: List[Dict[str, Any]]
    mitigation_strategies: List[Dict[str, Any]]
    overall_risk_level: int = Field(ge=1, le=5)

class BusinessImpact(BaseModel):
    roi_analysis: ROIAnalysis
    risk_assessment: RiskAssessment
    competitive_advantages: List[str]
    market_positioning: str
    strategic_alignment: str
    success_metrics: List[str]

class ArchitectureComponent(BaseModel):
    id: str
    name: str
    type: str
    description: str
    responsibilities: List[str]
    technologies: List[str]
    scaling_factors: List[str]
    business_value: str

class ArchitectureConnection(BaseModel):
    id: str
    from_component: str
    to_component: str
    type: str
    protocol: str
    description: str
    data_flow: Optional[Dict[str, Any]] = None

class ArchitectureData(BaseModel):
    components: List[ArchitectureComponent]
    connections: List[ArchitectureConnection]
    layers: List[Dict[str, Any]]
    patterns: List[Dict[str, Any]]
    technologies: List[Dict[str, Any]]
    metadata: Dict[str, Any] = Field(default_factory=dict)

class EducationalContent(BaseModel):
    concepts: List[Dict[str, Any]]
    examples: List[Dict[str, Any]]
    exercises: List[Dict[str, Any]]
    resources: List[Dict[str, Any]]
    progress_tracking: Dict[str, Any]
    business_context: Dict[str, Any]

class AgentResponse(BaseModel):
    content: str
    message_type: str
    architecture_update: Optional[ArchitectureData] = None
    why_reasoning: Optional[WhyReasoning] = None
    business_impact: Optional[BusinessImpact] = None
    educational_content: Optional[EducationalContent] = None
    suggested_actions: List[str] = Field(default_factory=list)
    next_questions: List[str] = Field(default_factory=list)
    confidence_score: float = Field(ge=0.0, le=1.0, default=0.8)

class WorkflowState(BaseModel):
    conversation_id: str
    user_query: str
    user_profile: UserProfile
    business_context: Optional[BusinessContext] = None
    orchestrator_plan: Dict[str, Any] = Field(default_factory=dict)
    requirements_analysis: Dict[str, Any] = Field(default_factory=dict)
    research_findings: Dict[str, Any] = Field(default_factory=dict)
    research_data: Dict[str, Any] = Field(default_factory=dict)  # Alias for research_findings
    architecture_design: Dict[str, Any] = Field(default_factory=dict)
    why_reasoning: Dict[str, Any] = Field(default_factory=dict)
    business_impact: Dict[str, Any] = Field(default_factory=dict)
    educational_content: Dict[str, Any] = Field(default_factory=dict)
    documentation: Dict[str, Any] = Field(default_factory=dict)
    current_step: str = "orchestrator"
    completed_steps: List[str] = Field(default_factory=list)
    workflow_type: WorkflowType = WorkflowType.SEQUENTIAL
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
