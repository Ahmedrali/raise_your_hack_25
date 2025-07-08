from typing import Dict, Any
import json
from src.agents.base_agent import BaseAgent
from src.models.agent_models import WorkflowState, WorkflowType

class OrchestratorAgent(BaseAgent):
    """Orchestrator agent that plans and coordinates workflow execution."""
    
    def __init__(self):
        super().__init__("orchestrator")

    async def process(self, state: WorkflowState) -> Dict[str, Any]:
        """Analyze query and create orchestration plan."""
        self.logger.info("Creating orchestration plan", conversation_id=state.conversation_id)
        
        try:
            orchestration_prompt = self._build_orchestration_prompt(state)
            response = await self.query_groq_with_context(
                orchestration_prompt, 
                state
            )
            
            plan = self._parse_orchestration_response(response)
            
            self.logger.info(
                "Orchestration plan created",
                workflow_type=plan.get("workflow_type"),
                agents_required=len(plan.get("agents_required", []))
            )
            
            return {"orchestrator_plan": plan}
            
        except Exception as e:
            self.logger.error("Orchestration planning failed", error=str(e))
            # Return fallback plan
            return {"orchestrator_plan": self._get_fallback_plan(state)}

    def get_system_prompt(self) -> str:
        return """
You are the Orchestrator Agent for the Agentic Architect platform. Your role is to analyze user queries and create optimal execution plans that coordinate specialized agents to deliver comprehensive architectural guidance with integrated business intelligence.

CORE RESPONSIBILITIES:
1. Analyze query complexity (technical and business)
2. Determine optimal workflow type (sequential/parallel/conditional/iterative)
3. Select required specialized agents
4. Plan integration of why reasoning and business intelligence
5. Estimate processing time and resource requirements

AVAILABLE SPECIALIZED AGENTS:
- Requirements Agent: Analyzes and clarifies architectural requirements
- Research Agent: Gathers current market and technical intelligence
- Architecture Agent: Designs technical solutions and patterns
- Why Reasoning Agent: Provides comprehensive decision explanations
- Business Impact Agent: Analyzes ROI, risks, and business implications
- Educational Agent: Creates adaptive learning content
- Documentation Agent: Generates professional documentation

WORKFLOW TYPES:
1. SEQUENTIAL: Step-by-step for thorough analysis (most common)
2. PARALLEL: Simultaneous processing for urgent decisions
3. CONDITIONAL: Branching logic based on complexity assessment
4. ITERATIVE: Repeated refinement for learning-focused sessions

ORCHESTRATION PRINCIPLES:
- Always include Why Reasoning and Business Impact agents
- Adapt agent selection to user expertise level
- Consider business context in all decisions
- Optimize for both technical accuracy and business value
- Ensure educational value in every interaction

Return your analysis as valid JSON with detailed orchestration plan.
        """

    def _build_orchestration_prompt(self, state: WorkflowState) -> str:
        """Build comprehensive orchestration prompt."""
        base_prompt = f"""
QUERY ANALYSIS REQUEST:
User Query: "{state.user_query}"
User Expertise: {state.user_profile.expertise_level}
Business Role: {state.user_profile.business_role or 'Not specified'}
Business Context: {state.business_context or 'Not provided'}

ORCHESTRATION ANALYSIS REQUIRED:

1. QUERY COMPLEXITY ANALYSIS:
   - Technical complexity level (1-5)
   - Business complexity level (1-5)
   - Required depth of why reasoning
   - Required depth of business analysis
   - Urgency assessment

2. WORKFLOW SELECTION:
   - Choose optimal workflow type (sequential/parallel/conditional/iterative)
   - Justify workflow choice based on complexity analysis
   - Estimate total processing time
   - Identify critical path dependencies

3. AGENT COORDINATION PLAN:
   - Which agents are required for this query?
   - What is the optimal agent execution order?
   - How should agents share context and build on each other?
   - How to integrate why reasoning and business intelligence?

4. USER EXPERIENCE OPTIMIZATION:
   - How to adapt technical explanations to user expertise level?
   - How to adapt business explanations to user role/context?
   - What educational opportunities exist in this query?
   - How to structure response for maximum learning value?

5. SUCCESS CRITERIA:
   - What constitutes a successful response for this query?
   - How to measure user satisfaction and learning?
   - What follow-up questions should be anticipated?
   - How to ensure both technical and business value delivery?

Return detailed orchestration plan as JSON with specific agent instructions and integration requirements.
        """
        
        return self.get_user_adapted_prompt(base_prompt, state.user_profile)

    def _parse_orchestration_response(self, response: str) -> Dict[str, Any]:
        """Parse orchestration response into structured plan."""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                plan = json.loads(json_match.group())
                return self._validate_orchestration_plan(plan)
            else:
                # Fallback parsing
                return self._extract_plan_from_text(response)
        except Exception as e:
            self.logger.warning("Failed to parse orchestration response", error=str(e))
            return self._get_default_plan()

    def _validate_orchestration_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and complete orchestration plan."""
        # Ensure required fields
        plan.setdefault("workflow_type", "SEQUENTIAL")
        plan.setdefault("agents_required", ["requirements", "research", "architecture", "why_reasoning", "business_impact", "educational"])
        plan.setdefault("estimated_duration_minutes", 15)
        plan.setdefault("complexity_score", 3)
        
        # Ensure why reasoning and business impact are always included
        if "why_reasoning" not in plan["agents_required"]:
            plan["agents_required"].append("why_reasoning")
        if "business_impact" not in plan["agents_required"]:
            plan["agents_required"].append("business_impact")
        
        # Validate workflow type
        valid_workflows = ["SEQUENTIAL", "PARALLEL", "CONDITIONAL", "ITERATIVE"]
        if plan["workflow_type"] not in valid_workflows:
            plan["workflow_type"] = "SEQUENTIAL"
        
        return plan

    def _extract_plan_from_text(self, response: str) -> Dict[str, Any]:
        """Extract plan from text response using keywords."""
        workflow_type = "SEQUENTIAL"
        if "parallel" in response.lower():
            workflow_type = "PARALLEL"
        elif "conditional" in response.lower():
            workflow_type = "CONDITIONAL"
        elif "iterative" in response.lower():
            workflow_type = "ITERATIVE"
        
        # Extract mentioned agents
        agent_keywords = {
            "requirements": ["requirements", "requirement"],
            "research": ["research", "search"],
            "architecture": ["architecture", "design"],
            "why_reasoning": ["why", "reasoning", "decision"],
            "business_impact": ["business", "roi", "impact"],
            "educational": ["educational", "learning", "teaching"],
            "documentation": ["documentation", "document"]
        }
        
        agents_required = []
        response_lower = response.lower()
        for agent, keywords in agent_keywords.items():
            if any(keyword in response_lower for keyword in keywords):
                agents_required.append(agent)
        
        # Ensure minimum required agents
        if not agents_required:
            agents_required = ["requirements", "architecture", "why_reasoning", "business_impact"]
        
        return {
            "workflow_type": workflow_type,
            "agents_required": agents_required,
            "estimated_duration_minutes": 15,
            "complexity_score": 3,
            "justification": "Extracted from text analysis"
        }

    def _get_fallback_plan(self, state: WorkflowState) -> Dict[str, Any]:
        """Get fallback orchestration plan."""
        return {
            "workflow_type": "SEQUENTIAL",
            "agents_required": ["requirements", "research", "architecture", "why_reasoning", "business_impact", "educational"],
            "estimated_duration_minutes": 20,
            "complexity_score": 3,
            "justification": "Fallback plan due to orchestration error",
            "integration_requirements": {
                "why_reasoning": "mandatory",
                "business_impact": "mandatory",
                "educational_adaptation": True
            }
        }

    def _get_default_plan(self) -> Dict[str, Any]:
        """Get default orchestration plan."""
        return {
            "workflow_type": "SEQUENTIAL",
            "agents_required": ["requirements", "architecture", "why_reasoning", "business_impact"],
            "estimated_duration_minutes": 15,
            "complexity_score": 2,
            "justification": "Default sequential plan"
        }
