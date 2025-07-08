from typing import Dict, Any
import json
from src.agents.base_agent import BaseAgent
from src.models.agent_models import WorkflowState

class ResearchAgent(BaseAgent):
    """Research agent that gathers relevant information and best practices."""
    
    def __init__(self):
        super().__init__("research")

    async def process(self, state: WorkflowState) -> Dict[str, Any]:
        """Conduct research on architecture patterns and technologies."""
        self.logger.info("Conducting research", conversation_id=state.conversation_id)
        
        try:
            # Get research context from orchestrator plan
            orchestrator_plan = getattr(state, 'orchestrator_plan', {})
            requirements = getattr(state, 'requirements_analysis', {})
            
            # Build research prompt
            research_prompt = self._build_research_prompt(state, orchestrator_plan, requirements)
            
            # Get research from Groq
            research_response = await self.groq_service.query(
                research_prompt,
                system_message=self.get_system_prompt()
            )
            
            # Parse research results
            research_data = self._parse_research_response(research_response)
            
            # Conduct additional searches if needed
            if search_queries := research_data.get("search_queries", []):
                search_results = []
                for query in search_queries[:3]:  # Limit to 3 searches
                    results = await self.tavily_service.search(query)
                    search_results.extend(results[:2])  # Top 2 results per query
                
                research_data["external_sources"] = search_results
            
            self.logger.info("Research completed", 
                           conversation_id=state.conversation_id,
                           patterns_found=len(research_data.get("architecture_patterns", [])))
            
            return {
                "success": True,
                "research_data": research_data,
                "agent": self.name,
                "confidence": research_data.get("confidence_score", 0.8)
            }
            
        except Exception as e:
            self.logger.error("Research failed", error=str(e), conversation_id=state.conversation_id)
            return {
                "success": False,
                "error": str(e),
                "research_data": self._get_fallback_research(),
                "agent": self.name
            }

    def get_system_prompt(self) -> str:
        """Get the system prompt for research agent."""
        return """
You are the Research Agent for the Agentic Architect platform. Your role is to gather comprehensive information about architecture patterns, technologies, and best practices relevant to the user's requirements.

RESEARCH OBJECTIVES:
1. Identify relevant architecture patterns and design principles
2. Research appropriate technologies and frameworks
3. Find industry best practices and case studies
4. Gather performance and scalability insights
5. Identify potential challenges and solutions

RESEARCH METHODOLOGY:
- Analyze requirements to determine research focus areas
- Identify key architecture patterns (microservices, serverless, monolithic, etc.)
- Research technology stacks and their trade-offs
- Find relevant case studies and implementation examples
- Gather performance benchmarks and scalability data

OUTPUT FORMAT:
Return a JSON object with:
{
  "architecture_patterns": [
    {
      "name": "pattern_name",
      "description": "detailed_description",
      "use_cases": ["use_case_1", "use_case_2"],
      "pros": ["advantage_1", "advantage_2"],
      "cons": ["limitation_1", "limitation_2"],
      "complexity": "low|medium|high"
    }
  ],
  "technology_recommendations": [
    {
      "category": "database|backend|frontend|infrastructure",
      "technology": "technology_name",
      "rationale": "why_recommended",
      "alternatives": ["alt_1", "alt_2"],
      "maturity": "experimental|stable|mature"
    }
  ],
  "best_practices": [
    {
      "area": "security|performance|scalability|maintainability",
      "practice": "best_practice_description",
      "implementation": "how_to_implement"
    }
  ],
  "case_studies": [
    {
      "company": "company_name",
      "scenario": "similar_use_case",
      "solution": "architecture_approach",
      "outcomes": "results_achieved"
    }
  ],
  "search_queries": ["query_1", "query_2"],
  "confidence_score": 0.0-1.0
}

Focus on practical, actionable insights that will help in architecture design decisions.
"""

    def _build_research_prompt(self, state: WorkflowState, orchestrator_plan: Dict, requirements: Dict) -> str:
        """Build research prompt based on context."""
        user_query = state.user_query
        expertise_level = state.user_profile.expertise_level.value if state.user_profile.expertise_level else "intermediate"
        
        prompt_parts = [
            f"Research architecture solutions for: {user_query}",
            f"User expertise level: {expertise_level}",
            "",
            "REQUIREMENTS CONTEXT:"
        ]
        
        if functional_reqs := requirements.get("functional_requirements", []):
            prompt_parts.append("Functional Requirements:")
            for req in functional_reqs[:5]:
                prompt_parts.append(f"- {req}")
        
        if non_functional_reqs := requirements.get("non_functional_requirements", []):
            prompt_parts.append("Non-Functional Requirements:")
            for req in non_functional_reqs[:5]:
                prompt_parts.append(f"- {req}")
        
        if business_context := state.business_context:
            prompt_parts.extend([
                "",
                "BUSINESS CONTEXT:",
                f"Industry: {getattr(business_context, 'industry', 'Not specified')}",
                f"Company Size: {getattr(business_context, 'company_size', 'Not specified')}",
                f"Budget: {getattr(business_context, 'budget_range', 'Not specified')}"
            ])
        
        prompt_parts.extend([
            "",
            "Please provide comprehensive research covering architecture patterns, technology recommendations, best practices, and relevant case studies.",
            "Focus on solutions that match the expertise level and business context."
        ])
        
        return "\n".join(prompt_parts)

    def _parse_research_response(self, response: str) -> Dict[str, Any]:
        """Parse research response from LLM."""
        try:
            # Try to extract JSON from response
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "{" in response and "}" in response:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                json_str = response[json_start:json_end]
            else:
                raise ValueError("No JSON found in response")
            
            research_data = json.loads(json_str)
            
            # Validate and clean data
            research_data.setdefault("architecture_patterns", [])
            research_data.setdefault("technology_recommendations", [])
            research_data.setdefault("best_practices", [])
            research_data.setdefault("case_studies", [])
            research_data.setdefault("search_queries", [])
            research_data.setdefault("confidence_score", 0.8)
            
            return research_data
            
        except Exception as e:
            self.logger.warning("Failed to parse research response", error=str(e))
            return self._get_fallback_research()

    def _get_fallback_research(self) -> Dict[str, Any]:
        """Get fallback research data."""
        return {
            "architecture_patterns": [
                {
                    "name": "Microservices Architecture",
                    "description": "Distributed architecture pattern with loosely coupled services",
                    "use_cases": ["Large scale applications", "Team autonomy", "Technology diversity"],
                    "pros": ["Scalability", "Technology flexibility", "Team independence"],
                    "cons": ["Complexity", "Network overhead", "Data consistency challenges"],
                    "complexity": "high"
                },
                {
                    "name": "Layered Architecture",
                    "description": "Traditional n-tier architecture with clear separation of concerns",
                    "use_cases": ["Enterprise applications", "Well-defined domains", "Team familiarity"],
                    "pros": ["Simplicity", "Clear structure", "Easy to understand"],
                    "cons": ["Tight coupling", "Performance overhead", "Limited scalability"],
                    "complexity": "low"
                }
            ],
            "technology_recommendations": [
                {
                    "category": "backend",
                    "technology": "Node.js with Express",
                    "rationale": "Fast development, JavaScript ecosystem, good performance",
                    "alternatives": ["Python Django", "Java Spring Boot"],
                    "maturity": "mature"
                },
                {
                    "category": "database",
                    "technology": "PostgreSQL",
                    "rationale": "ACID compliance, rich feature set, excellent performance",
                    "alternatives": ["MySQL", "MongoDB"],
                    "maturity": "mature"
                }
            ],
            "best_practices": [
                {
                    "area": "security",
                    "practice": "Implement authentication and authorization at all layers",
                    "implementation": "Use JWT tokens, role-based access control, input validation"
                },
                {
                    "area": "performance",
                    "practice": "Implement caching strategies",
                    "implementation": "Redis for session storage, CDN for static assets, database query optimization"
                }
            ],
            "case_studies": [
                {
                    "company": "Netflix",
                    "scenario": "Large-scale video streaming platform",
                    "solution": "Microservices with event-driven architecture",
                    "outcomes": "Massive scale, high availability, rapid feature development"
                }
            ],
            "search_queries": [
                "microservices architecture best practices",
                "scalable web application design patterns"
            ],
            "confidence_score": 0.7
        }
