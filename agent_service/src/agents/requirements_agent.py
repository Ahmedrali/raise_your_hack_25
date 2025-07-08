from typing import Dict, Any
import json
from src.agents.base_agent import BaseAgent
from src.models.agent_models import WorkflowState

class RequirementsAgent(BaseAgent):
    """Requirements agent that analyzes and clarifies architectural requirements."""
    
    def __init__(self):
        super().__init__("requirements")

    async def process(self, state: WorkflowState) -> Dict[str, Any]:
        """Analyze requirements with business context."""
        self.logger.info("Analyzing requirements", conversation_id=state.conversation_id)
        
        try:
            requirements_prompt = self._build_requirements_prompt(state)
            response = await self.query_groq_with_context(
                requirements_prompt, 
                state
            )
            
            analysis = self._parse_requirements_response(response)
            
            self.logger.info(
                "Requirements analysis completed",
                functional_requirements=len(analysis.get("functional_requirements", [])),
                non_functional_requirements=len(analysis.get("non_functional_requirements", []))
            )
            
            return {"requirements_analysis": analysis}
            
        except Exception as e:
            self.logger.error("Requirements analysis failed", error=str(e))
            return {"requirements_analysis": self._get_fallback_analysis(state)}

    def get_system_prompt(self) -> str:
        return """
You are the Requirements Analysis Agent for the Agentic Architect platform. Your role is to thoroughly analyze user requirements and translate them into comprehensive architectural specifications with integrated business context.

CORE RESPONSIBILITIES:
1. Extract and clarify functional requirements
2. Identify non-functional requirements (performance, security, scalability)
3. Analyze business requirements and constraints
4. Identify missing or ambiguous requirements
5. Assess technical and business risks
6. Provide requirement prioritization based on business value

ANALYSIS FRAMEWORK:
1. FUNCTIONAL REQUIREMENTS:
   - Core features and capabilities
   - User interactions and workflows
   - Data processing requirements
   - Integration requirements

2. NON-FUNCTIONAL REQUIREMENTS:
   - Performance and scalability targets
   - Security and compliance needs
   - Availability and reliability requirements
   - Maintainability and operability needs

3. BUSINESS REQUIREMENTS:
   - Business objectives and success metrics
   - Budget and timeline constraints
   - Compliance and regulatory requirements
   - Market and competitive considerations

4. CONSTRAINTS AND ASSUMPTIONS:
   - Technology constraints
   - Resource limitations
   - External dependencies
   - Risk factors

Return structured JSON with comprehensive requirements analysis and business alignment.
        """

    def _build_requirements_prompt(self, state: WorkflowState) -> str:
        """Build comprehensive requirements analysis prompt."""
        base_prompt = f"""
REQUIREMENTS ANALYSIS REQUEST:
User Query: "{state.user_query}"
Business Context: {state.business_context or 'Not provided'}
User Expertise: {state.user_profile.expertise_level}
Business Role: {state.user_profile.business_role or 'Not specified'}

COMPREHENSIVE REQUIREMENTS ANALYSIS:

1. FUNCTIONAL REQUIREMENTS EXTRACTION:
   - What are the core features and capabilities needed?
   - What user interactions and workflows are required?
   - What data processing and storage requirements exist?
   - What integration points are needed?
   - What business processes must be supported?

2. NON-FUNCTIONAL REQUIREMENTS ANALYSIS:
   - Performance requirements (throughput, latency, concurrency)
   - Scalability requirements (user growth, data growth, transaction volume)
   - Security requirements (authentication, authorization, data protection)
   - Availability and reliability requirements (uptime, disaster recovery)
   - Compliance requirements (regulatory, industry standards)

3. BUSINESS REQUIREMENTS ASSESSMENT:
   - What business objectives does this system support?
   - What are the success metrics and KPIs?
   - What are the budget and timeline constraints?
   - What market or competitive factors influence requirements?
   - What ROI expectations exist?

4. CONSTRAINT AND RISK ANALYSIS:
   - What technology constraints exist?
   - What resource limitations must be considered?
   - What external dependencies exist?
   - What technical and business risks are present?

5. REQUIREMENT PRIORITIZATION:
   - Which requirements are must-have vs nice-to-have?
   - What is the business value of each requirement?
   - What are the implementation complexity and costs?
   - What is the recommended implementation sequence?

6. CLARIFICATION QUESTIONS:
   - What additional information is needed?
   - What assumptions need validation?
   - What potential conflicts or gaps exist?

Return detailed JSON with structured requirements analysis including business impact assessment.
        """
        
        return self.get_user_adapted_prompt(base_prompt, state.user_profile)

    def _parse_requirements_response(self, response: str) -> Dict[str, Any]:
        """Parse requirements response into structured analysis."""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                return self._validate_requirements_analysis(analysis)
            else:
                # Fallback parsing
                return self._extract_requirements_from_text(response)
        except Exception as e:
            self.logger.warning("Failed to parse requirements response", error=str(e))
            return self._get_default_analysis()

    def _validate_requirements_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and complete requirements analysis."""
        # Ensure required fields
        analysis.setdefault("functional_requirements", [])
        analysis.setdefault("non_functional_requirements", [])
        analysis.setdefault("business_requirements", [])
        analysis.setdefault("constraints", [])
        analysis.setdefault("risks", [])
        analysis.setdefault("clarification_questions", [])
        analysis.setdefault("priority_matrix", {})
        
        # Validate structure
        if not isinstance(analysis["functional_requirements"], list):
            analysis["functional_requirements"] = []
        if not isinstance(analysis["non_functional_requirements"], list):
            analysis["non_functional_requirements"] = []
        
        return analysis

    def _extract_requirements_from_text(self, response: str) -> Dict[str, Any]:
        """Extract requirements from text response."""
        lines = response.split('\n')
        
        functional_reqs = []
        non_functional_reqs = []
        business_reqs = []
        questions = []
        
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            line_lower = line.lower()
            if 'functional' in line_lower and 'requirement' in line_lower:
                current_section = 'functional'
            elif 'non-functional' in line_lower or 'performance' in line_lower:
                current_section = 'non_functional'
            elif 'business' in line_lower and 'requirement' in line_lower:
                current_section = 'business'
            elif 'question' in line_lower or 'clarification' in line_lower:
                current_section = 'questions'
            elif line.startswith('- ') or line.startswith('* '):
                requirement = line[2:].strip()
                if current_section == 'functional':
                    functional_reqs.append(requirement)
                elif current_section == 'non_functional':
                    non_functional_reqs.append(requirement)
                elif current_section == 'business':
                    business_reqs.append(requirement)
                elif current_section == 'questions':
                    questions.append(requirement)
        
        return {
            "functional_requirements": functional_reqs,
            "non_functional_requirements": non_functional_reqs,
            "business_requirements": business_reqs,
            "constraints": [],
            "risks": [],
            "clarification_questions": questions,
            "priority_matrix": {}
        }

    def _get_fallback_analysis(self, state: WorkflowState) -> Dict[str, Any]:
        """Get fallback requirements analysis."""
        return {
            "functional_requirements": [
                "Core system functionality as described in user query",
                "User interface for interaction",
                "Data persistence capabilities"
            ],
            "non_functional_requirements": [
                "System performance and responsiveness",
                "Security and data protection",
                "Scalability for future growth"
            ],
            "business_requirements": [
                "Alignment with business objectives",
                "Cost-effective implementation",
                "Timely delivery"
            ],
            "constraints": [
                "Budget limitations",
                "Timeline constraints",
                "Technology stack preferences"
            ],
            "risks": [
                "Technical implementation complexity",
                "Integration challenges",
                "Performance bottlenecks"
            ],
            "clarification_questions": [
                "What is the expected user load?",
                "What are the performance requirements?",
                "What integrations are needed?"
            ],
            "priority_matrix": {
                "high": ["Core functionality", "Security"],
                "medium": ["Performance optimization", "Integrations"],
                "low": ["Advanced features", "UI enhancements"]
            }
        }

    def _get_default_analysis(self) -> Dict[str, Any]:
        """Get default requirements analysis."""
        return {
            "functional_requirements": ["Basic system functionality"],
            "non_functional_requirements": ["Performance", "Security"],
            "business_requirements": ["Business value delivery"],
            "constraints": ["Resource limitations"],
            "risks": ["Implementation complexity"],
            "clarification_questions": ["Need more details"],
            "priority_matrix": {}
        }
