from typing import Dict, Any, List
import json
from src.agents.base_agent import BaseAgent
from src.models.agent_models import WorkflowState

class WhyReasoningAgent(BaseAgent):
    """Why reasoning agent that provides detailed explanations for architectural decisions."""
    
    def __init__(self):
        super().__init__("why_reasoning")

    async def process(self, state: WorkflowState) -> Dict[str, Any]:
        """Generate comprehensive reasoning for architectural decisions."""
        self.logger.info("Generating why reasoning", conversation_id=state.conversation_id)
        
        try:
            # Get context from previous agents
            orchestrator_plan = getattr(state, 'orchestrator_plan', {})
            requirements = getattr(state, 'requirements_analysis', {})
            research_data = getattr(state, 'research_data', {})
            architecture_design = getattr(state, 'architecture_design', {})
            
            # Build reasoning prompt
            reasoning_prompt = self._build_reasoning_prompt(
                state, orchestrator_plan, requirements, research_data, architecture_design
            )
            
            # Generate reasoning
            reasoning_response = await self.groq_service.query(
                reasoning_prompt,
                system_message=self.get_system_prompt()
            )
            
            # Parse reasoning
            why_reasoning = self._parse_reasoning_response(reasoning_response)
            
            # Enhance with decision rationale
            why_reasoning["decision_rationale"] = self._generate_decision_rationale(
                requirements, research_data, architecture_design
            )
            
            self.logger.info("Why reasoning completed", 
                           conversation_id=state.conversation_id,
                           decisions_explained=len(why_reasoning.get("architectural_decisions", [])))
            
            return {
                "success": True,
                "why_reasoning": why_reasoning,
                "agent": self.name,
                "confidence": why_reasoning.get("confidence_score", 0.9)
            }
            
        except Exception as e:
            self.logger.error("Why reasoning failed", error=str(e), conversation_id=state.conversation_id)
            return {
                "success": False,
                "error": str(e),
                "why_reasoning": self._get_fallback_reasoning(),
                "agent": self.name
            }

    def get_system_prompt(self) -> str:
        """Get the system prompt for why reasoning agent."""
        return """
You are the Why Reasoning Agent for the Agentic Architect platform. Your role is to provide clear, comprehensive explanations for all architectural decisions, helping users understand the rationale behind design choices.

REASONING OBJECTIVES:
1. Explain the "why" behind every architectural decision
2. Connect decisions to specific requirements and constraints
3. Highlight trade-offs and alternatives considered
4. Provide educational context for design patterns and technologies
5. Adapt explanations to user expertise level

REASONING METHODOLOGY:
- Analyze each architectural component and design decision
- Trace decisions back to specific requirements or constraints
- Explain trade-offs between different approaches
- Provide context on industry best practices
- Include potential risks and mitigation strategies
- Offer learning opportunities and deeper insights

OUTPUT FORMAT:
Return a JSON object with:
{
  "architectural_decisions": [
    {
      "decision": "specific_architectural_decision",
      "rationale": "detailed_explanation_of_why",
      "requirements_addressed": ["requirement_1", "requirement_2"],
      "trade_offs": {
        "pros": ["advantage_1", "advantage_2"],
        "cons": ["limitation_1", "limitation_2"]
      },
      "alternatives_considered": [
        {
          "alternative": "alternative_approach",
          "why_not_chosen": "reason_for_rejection"
        }
      ],
      "risk_factors": ["risk_1", "risk_2"],
      "implementation_complexity": "low|medium|high",
      "business_impact": "positive|neutral|negative"
    }
  ],
  "pattern_explanations": [
    {
      "pattern": "architecture_pattern_name",
      "why_chosen": "explanation_of_selection",
      "use_case_fit": "how_it_fits_this_scenario",
      "learning_context": "educational_background_info"
    }
  ],
  "technology_justifications": [
    {
      "technology": "technology_name",
      "category": "frontend|backend|database|infrastructure",
      "selection_criteria": ["criterion_1", "criterion_2"],
      "why_best_fit": "detailed_justification",
      "ecosystem_benefits": ["benefit_1", "benefit_2"],
      "potential_concerns": ["concern_1", "concern_2"]
    }
  ],
  "design_principles": [
    {
      "principle": "design_principle_name",
      "application": "how_applied_in_this_design",
      "importance": "why_this_principle_matters",
      "examples": ["example_1", "example_2"]
    }
  ],
  "scalability_reasoning": {
    "approach": "chosen_scalability_approach",
    "justification": "why_this_approach_is_optimal",
    "growth_scenarios": ["scenario_1", "scenario_2"],
    "bottleneck_analysis": ["potential_bottleneck_1", "potential_bottleneck_2"]
  },
  "security_reasoning": {
    "security_model": "chosen_security_approach",
    "threat_analysis": ["threat_1", "threat_2"],
    "mitigation_strategies": ["strategy_1", "strategy_2"],
    "compliance_considerations": ["consideration_1", "consideration_2"]
  },
  "educational_insights": [
    {
      "topic": "educational_topic",
      "explanation": "detailed_explanation",
      "why_important": "relevance_to_this_project",
      "further_reading": ["resource_1", "resource_2"]
    }
  ],
  "implementation_guidance": {
    "critical_path": ["step_1", "step_2", "step_3"],
    "success_factors": ["factor_1", "factor_2"],
    "common_pitfalls": ["pitfall_1", "pitfall_2"],
    "validation_checkpoints": ["checkpoint_1", "checkpoint_2"]
  },
  "confidence_score": 0.0-1.0
}

Provide explanations that are clear, educational, and help users understand both the technical and business reasoning behind architectural decisions.
"""

    def _build_reasoning_prompt(self, state: WorkflowState, orchestrator_plan: Dict, 
                              requirements: Dict, research_data: Dict, architecture_design: Dict) -> str:
        """Build reasoning prompt based on all available context."""
        user_query = state.user_query
        expertise_level = state.user_profile.expertise_level.value if state.user_profile.expertise_level else "intermediate"
        
        prompt_parts = [
            f"Provide comprehensive reasoning for the architectural decisions made for: {user_query}",
            f"User expertise level: {expertise_level}",
            "",
            "CONTEXT TO ANALYZE:"
        ]
        
        # Add requirements context
        if requirements:
            prompt_parts.append("REQUIREMENTS:")
            if functional_reqs := requirements.get("functional_requirements", []):
                prompt_parts.append("Functional:")
                for req in functional_reqs[:5]:
                    prompt_parts.append(f"- {req}")
            
            if non_functional_reqs := requirements.get("non_functional_requirements", []):
                prompt_parts.append("Non-Functional:")
                for req in non_functional_reqs[:5]:
                    prompt_parts.append(f"- {req}")
        
        # Add research context
        if research_data:
            prompt_parts.append("\nRESEARCH FINDINGS:")
            if patterns := research_data.get("architecture_patterns", []):
                prompt_parts.append("Patterns Considered:")
                for pattern in patterns[:3]:
                    prompt_parts.append(f"- {pattern.get('name', '')}: {pattern.get('description', '')}")
        
        # Add architecture decisions to explain
        if architecture_design:
            prompt_parts.append("\nARCHITECTURE DECISIONS TO EXPLAIN:")
            
            if overview := architecture_design.get("architecture_overview", {}):
                prompt_parts.append(f"Pattern: {overview.get('pattern', 'Not specified')}")
                prompt_parts.append(f"Description: {overview.get('description', 'Not specified')}")
            
            if components := architecture_design.get("components", []):
                prompt_parts.append("Components:")
                for comp in components[:5]:
                    prompt_parts.append(f"- {comp.get('name', '')}: {comp.get('technology', '')}")
            
            if tech_stack := architecture_design.get("technology_stack", {}):
                prompt_parts.append("Technology Stack:")
                for category, tech in tech_stack.items():
                    prompt_parts.append(f"- {category}: {tech}")
        
        # Add business context
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
            "Please provide detailed reasoning that explains:",
            "1. Why each architectural decision was made",
            "2. How decisions address specific requirements",
            "3. What alternatives were considered and why they were rejected",
            "4. What trade-offs were made and their implications",
            "5. How the design aligns with best practices",
            "6. What risks exist and how they're mitigated",
            "",
            f"Adapt the explanation depth and technical detail to {expertise_level} level."
        ])
        
        return "\n".join(prompt_parts)

    def _parse_reasoning_response(self, response: str) -> Dict[str, Any]:
        """Parse reasoning response from LLM."""
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
            
            reasoning_data = json.loads(json_str)
            
            # Validate and set defaults
            self._validate_reasoning_data(reasoning_data)
            
            return reasoning_data
            
        except Exception as e:
            self.logger.warning("Failed to parse reasoning response", error=str(e))
            return self._get_fallback_reasoning()

    def _validate_reasoning_data(self, data: Dict[str, Any]) -> None:
        """Validate and set defaults for reasoning data."""
        data.setdefault("architectural_decisions", [])
        data.setdefault("pattern_explanations", [])
        data.setdefault("technology_justifications", [])
        data.setdefault("design_principles", [])
        data.setdefault("scalability_reasoning", {})
        data.setdefault("security_reasoning", {})
        data.setdefault("educational_insights", [])
        data.setdefault("implementation_guidance", {})
        data.setdefault("confidence_score", 0.9)

    def _generate_decision_rationale(self, requirements: Dict, research_data: Dict, 
                                   architecture_design: Dict) -> Dict[str, Any]:
        """Generate additional decision rationale based on context."""
        rationale = {
            "requirements_traceability": [],
            "research_influence": [],
            "design_coherence": []
        }
        
        # Trace requirements to architecture decisions
        functional_reqs = requirements.get("functional_requirements", [])
        components = architecture_design.get("components", [])
        
        for req in functional_reqs[:3]:
            rationale["requirements_traceability"].append({
                "requirement": req,
                "addressed_by": [comp.get("name", "") for comp in components[:2]],
                "how": "Component provides necessary functionality"
            })
        
        # Show research influence
        patterns = research_data.get("architecture_patterns", [])
        chosen_pattern = architecture_design.get("architecture_overview", {}).get("pattern", "")
        
        for pattern in patterns[:2]:
            if pattern.get("name", "").lower() in chosen_pattern.lower():
                rationale["research_influence"].append({
                    "research_finding": pattern.get("name", ""),
                    "influence": "Pattern selection based on research recommendation",
                    "benefit": pattern.get("pros", ["Improved architecture"])[0] if pattern.get("pros") else "Better design"
                })
        
        return rationale

    def _get_fallback_reasoning(self) -> Dict[str, Any]:
        """Get fallback reasoning data."""
        return {
            "architectural_decisions": [
                {
                    "decision": "Layered architecture pattern selection",
                    "rationale": "Chosen for its simplicity and clear separation of concerns, making it easier to understand and maintain",
                    "requirements_addressed": ["Maintainability", "Team productivity", "Clear structure"],
                    "trade_offs": {
                        "pros": ["Simple to understand", "Clear separation", "Easy to test"],
                        "cons": ["Potential performance overhead", "Tight coupling between layers"]
                    },
                    "alternatives_considered": [
                        {
                            "alternative": "Microservices architecture",
                            "why_not_chosen": "Too complex for current team size and requirements"
                        }
                    ],
                    "risk_factors": ["Performance bottlenecks", "Monolithic deployment"],
                    "implementation_complexity": "low",
                    "business_impact": "positive"
                },
                {
                    "decision": "React for frontend technology",
                    "rationale": "Selected for its large ecosystem, component reusability, and team familiarity",
                    "requirements_addressed": ["User experience", "Development speed", "Maintainability"],
                    "trade_offs": {
                        "pros": ["Large ecosystem", "Component reusability", "Strong community"],
                        "cons": ["Learning curve", "Frequent updates", "Bundle size"]
                    },
                    "alternatives_considered": [
                        {
                            "alternative": "Vue.js",
                            "why_not_chosen": "Team has more experience with React"
                        }
                    ],
                    "risk_factors": ["Technology churn", "Dependency management"],
                    "implementation_complexity": "medium",
                    "business_impact": "positive"
                }
            ],
            "pattern_explanations": [
                {
                    "pattern": "Layered Architecture",
                    "why_chosen": "Provides clear separation of concerns and is well-understood by development teams",
                    "use_case_fit": "Perfect for applications with well-defined business logic and data access patterns",
                    "learning_context": "One of the most fundamental architectural patterns, forming the basis for many enterprise applications"
                }
            ],
            "technology_justifications": [
                {
                    "technology": "PostgreSQL",
                    "category": "database",
                    "selection_criteria": ["ACID compliance", "Performance", "Feature richness"],
                    "why_best_fit": "Provides robust data consistency and advanced features needed for complex business logic",
                    "ecosystem_benefits": ["Excellent tooling", "Strong community", "Enterprise support"],
                    "potential_concerns": ["Vertical scaling limits", "Complexity for simple use cases"]
                },
                {
                    "technology": "Node.js",
                    "category": "backend",
                    "selection_criteria": ["JavaScript ecosystem", "Performance", "Development speed"],
                    "why_best_fit": "Enables full-stack JavaScript development and has excellent performance for I/O operations",
                    "ecosystem_benefits": ["NPM ecosystem", "Rapid development", "JSON handling"],
                    "potential_concerns": ["Single-threaded limitations", "Callback complexity"]
                }
            ],
            "design_principles": [
                {
                    "principle": "Separation of Concerns",
                    "application": "Each layer has distinct responsibilities - presentation, business logic, and data access",
                    "importance": "Reduces complexity and improves maintainability by isolating different aspects of the system",
                    "examples": ["UI components only handle presentation", "Business logic isolated in service layer"]
                },
                {
                    "principle": "Single Responsibility",
                    "application": "Each component and service has a single, well-defined purpose",
                    "importance": "Makes the system easier to understand, test, and modify",
                    "examples": ["Authentication service only handles auth", "Database layer only manages data access"]
                }
            ],
            "scalability_reasoning": {
                "approach": "Horizontal scaling with load balancing",
                "justification": "Allows the system to handle increased load by adding more instances rather than upgrading hardware",
                "growth_scenarios": ["Increased user base", "Higher transaction volume"],
                "bottleneck_analysis": ["Database connections", "Memory usage", "Network I/O"]
            },
            "security_reasoning": {
                "security_model": "JWT-based authentication with role-based authorization",
                "threat_analysis": ["Unauthorized access", "Data breaches", "Session hijacking"],
                "mitigation_strategies": ["Token expiration", "HTTPS encryption", "Input validation"],
                "compliance_considerations": ["Data privacy", "Access logging", "Audit trails"]
            },
            "educational_insights": [
                {
                    "topic": "Layered Architecture Benefits",
                    "explanation": "Layered architecture provides clear separation between different concerns of the application",
                    "why_important": "Understanding this pattern is fundamental to building maintainable enterprise applications",
                    "further_reading": ["Clean Architecture by Robert Martin", "Patterns of Enterprise Application Architecture"]
                },
                {
                    "topic": "Database Selection Criteria",
                    "explanation": "Choosing the right database depends on data structure, consistency requirements, and scalability needs",
                    "why_important": "Database choice significantly impacts application performance and scalability",
                    "further_reading": ["Designing Data-Intensive Applications", "Database design fundamentals"]
                }
            ],
            "implementation_guidance": {
                "critical_path": ["Set up development environment", "Implement core data models", "Build API layer", "Create frontend components"],
                "success_factors": ["Clear requirements", "Good testing strategy", "Regular code reviews"],
                "common_pitfalls": ["Over-engineering", "Insufficient testing", "Poor error handling"],
                "validation_checkpoints": ["Unit tests passing", "Integration tests working", "Performance benchmarks met"]
            },
            "decision_rationale": {
                "requirements_traceability": [
                    {
                        "requirement": "User authentication and authorization",
                        "addressed_by": ["Authentication Service", "API Gateway"],
                        "how": "JWT tokens provide secure authentication with role-based access control"
                    }
                ],
                "research_influence": [
                    {
                        "research_finding": "Layered architecture pattern",
                        "influence": "Pattern selection based on team expertise and project complexity",
                        "benefit": "Reduced development time and improved maintainability"
                    }
                ],
                "design_coherence": [
                    "All components follow consistent design patterns",
                    "Technology choices complement each other",
                    "Architecture supports both current and future requirements"
                ]
            },
            "confidence_score": 0.85
        }
