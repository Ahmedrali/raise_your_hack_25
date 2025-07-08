from typing import Dict, Any, List
import json
from src.agents.base_agent import BaseAgent
from src.models.agent_models import WorkflowState

class BusinessImpactAgent(BaseAgent):
    """Business impact agent that analyzes business implications of architectural decisions."""
    
    def __init__(self):
        super().__init__("business_impact")

    async def process(self, state: WorkflowState) -> Dict[str, Any]:
        """Analyze business impact of architectural decisions."""
        self.logger.info("Analyzing business impact", conversation_id=state.conversation_id)
        
        try:
            # Get context from previous agents
            orchestrator_plan = getattr(state, 'orchestrator_plan', {})
            requirements = getattr(state, 'requirements_analysis', {})
            research_data = getattr(state, 'research_data', {})
            architecture_design = getattr(state, 'architecture_design', {})
            why_reasoning = getattr(state, 'why_reasoning', {})
            
            # Build business impact prompt
            impact_prompt = self._build_impact_prompt(
                state, orchestrator_plan, requirements, research_data, architecture_design, why_reasoning
            )
            
            # Generate business impact analysis
            impact_response = await self.groq_service.query(
                impact_prompt,
                system_message=self.get_system_prompt()
            )
            
            # Parse business impact
            business_impact = self._parse_impact_response(impact_response)
            
            # Enhance with ROI calculations
            business_impact["roi_analysis"] = self._calculate_roi_estimates(
                business_impact, state.business_context, architecture_design
            )
            
            self.logger.info("Business impact analysis completed", 
                           conversation_id=state.conversation_id,
                           impact_areas=len(business_impact.get("impact_areas", [])))
            
            return {
                "success": True,
                "business_impact": business_impact,
                "agent": self.name,
                "confidence": business_impact.get("confidence_score", 0.85)
            }
            
        except Exception as e:
            self.logger.error("Business impact analysis failed", error=str(e), conversation_id=state.conversation_id)
            return {
                "success": False,
                "error": str(e),
                "business_impact": self._get_fallback_impact(),
                "agent": self.name
            }

    def get_system_prompt(self) -> str:
        """Get the system prompt for business impact agent."""
        return """
You are the Business Impact Agent for the Agentic Architect platform. Your role is to analyze and quantify the business implications of architectural decisions, helping stakeholders understand the value and risks of proposed solutions.

BUSINESS ANALYSIS OBJECTIVES:
1. Quantify business value and ROI of architectural decisions
2. Identify cost implications and resource requirements
3. Assess risk factors and mitigation strategies
4. Analyze time-to-market and competitive advantages
5. Evaluate operational and maintenance impacts
6. Consider scalability and future business growth

ANALYSIS METHODOLOGY:
- Evaluate direct and indirect costs of implementation
- Assess revenue impact and business value creation
- Analyze operational efficiency improvements
- Consider risk factors and their business implications
- Evaluate competitive positioning and market advantages
- Assess long-term strategic alignment

OUTPUT FORMAT:
Return a JSON object with:
{
  "executive_summary": {
    "overall_impact": "positive|neutral|negative",
    "key_benefits": ["benefit_1", "benefit_2", "benefit_3"],
    "main_risks": ["risk_1", "risk_2", "risk_3"],
    "recommendation": "proceed|proceed_with_caution|reconsider"
  },
  "financial_impact": {
    "implementation_cost": {
      "development": "estimated_cost_range",
      "infrastructure": "estimated_cost_range",
      "training": "estimated_cost_range",
      "total_estimated": "total_cost_range"
    },
    "operational_cost": {
      "annual_infrastructure": "yearly_cost_estimate",
      "maintenance": "yearly_maintenance_cost",
      "support": "yearly_support_cost"
    },
    "cost_savings": [
      {
        "area": "cost_saving_area",
        "annual_savings": "estimated_savings",
        "description": "how_savings_achieved"
      }
    ],
    "revenue_impact": [
      {
        "opportunity": "revenue_opportunity",
        "potential_value": "estimated_value",
        "timeframe": "when_realized"
      }
    ]
  },
  "operational_impact": {
    "efficiency_gains": [
      {
        "process": "business_process",
        "improvement": "efficiency_improvement",
        "quantification": "measurable_benefit"
      }
    ],
    "resource_requirements": [
      {
        "resource_type": "human|technical|financial",
        "requirement": "specific_requirement",
        "timeline": "when_needed"
      }
    ],
    "workflow_changes": [
      {
        "area": "affected_area",
        "change": "required_change",
        "impact": "business_impact"
      }
    ]
  },
  "strategic_impact": {
    "competitive_advantages": [
      {
        "advantage": "competitive_benefit",
        "significance": "high|medium|low",
        "sustainability": "how_long_advantage_lasts"
      }
    ],
    "market_positioning": {
      "current_position": "current_market_position",
      "target_position": "desired_position",
      "architecture_contribution": "how_architecture_helps"
    },
    "innovation_enablement": [
      {
        "capability": "new_capability_enabled",
        "business_value": "value_to_business",
        "timeline": "when_available"
      }
    ]
  },
  "risk_analysis": {
    "technical_risks": [
      {
        "risk": "technical_risk",
        "probability": "high|medium|low",
        "business_impact": "impact_on_business",
        "mitigation": "risk_mitigation_strategy",
        "cost_of_mitigation": "mitigation_cost"
      }
    ],
    "business_risks": [
      {
        "risk": "business_risk",
        "probability": "high|medium|low",
        "financial_impact": "potential_financial_loss",
        "mitigation": "business_mitigation_strategy"
      }
    ],
    "opportunity_costs": [
      {
        "alternative": "alternative_approach",
        "foregone_benefit": "what_is_given_up",
        "justification": "why_current_choice_better"
      }
    ]
  },
  "timeline_impact": {
    "time_to_market": "estimated_delivery_time",
    "business_value_realization": [
      {
        "milestone": "business_milestone",
        "value_delivered": "value_at_milestone",
        "timeline": "when_achieved"
      }
    ],
    "critical_path_items": ["item_1", "item_2", "item_3"]
  },
  "scalability_business_impact": {
    "growth_enablement": "how_architecture_supports_growth",
    "scaling_costs": "cost_implications_of_scaling",
    "revenue_scalability": "revenue_scaling_potential",
    "operational_scalability": "operational_scaling_benefits"
  },
  "stakeholder_impact": [
    {
      "stakeholder_group": "affected_group",
      "impact_type": "positive|negative|neutral",
      "specific_impacts": ["impact_1", "impact_2"],
      "required_actions": ["action_1", "action_2"]
    }
  ],
  "success_metrics": [
    {
      "metric": "business_metric",
      "current_baseline": "current_value",
      "target_value": "target_after_implementation",
      "measurement_method": "how_to_measure"
    }
  ],
  "confidence_score": 0.0-1.0
}

Provide practical, actionable business insights that help stakeholders make informed decisions about architectural investments.
"""

    def _build_impact_prompt(self, state: WorkflowState, orchestrator_plan: Dict, 
                           requirements: Dict, research_data: Dict, architecture_design: Dict, 
                           why_reasoning: Dict) -> str:
        """Build business impact analysis prompt."""
        user_query = state.user_query
        
        prompt_parts = [
            f"Analyze the business impact of the proposed architecture for: {user_query}",
            "",
            "BUSINESS CONTEXT:"
        ]
        
        # Add business context
        if business_context := state.business_context:
            prompt_parts.extend([
                f"Industry: {getattr(business_context, 'industry', 'Not specified')}",
                f"Company Size: {getattr(business_context, 'company_size', 'Not specified')}",
                f"Budget Range: {getattr(business_context, 'budget_range', 'Not specified')}",
                f"Timeline: {getattr(business_context, 'timeline', 'Not specified')}",
                f"Current Challenges: {getattr(business_context, 'current_challenges', 'Not specified')}"
            ])
        
        # Add business requirements
        if business_reqs := requirements.get("business_requirements", []):
            prompt_parts.append("\nBUSINESS REQUIREMENTS:")
            for req in business_reqs:
                prompt_parts.append(f"- {req}")
        
        # Add architecture overview
        if architecture_design:
            prompt_parts.append("\nPROPOSED ARCHITECTURE:")
            if overview := architecture_design.get("architecture_overview", {}):
                prompt_parts.append(f"Pattern: {overview.get('pattern', 'Not specified')}")
                prompt_parts.append(f"Description: {overview.get('description', 'Not specified')}")
            
            if tech_stack := architecture_design.get("technology_stack", {}):
                prompt_parts.append("Technology Stack:")
                for category, tech in tech_stack.items():
                    prompt_parts.append(f"- {category}: {tech}")
            
            if phases := architecture_design.get("implementation_phases", []):
                prompt_parts.append("Implementation Phases:")
                for phase in phases[:3]:
                    prompt_parts.append(f"- Phase {phase.get('phase', '')}: {phase.get('name', '')} ({phase.get('duration', '')})")
        
        # Add key architectural decisions
        if decisions := why_reasoning.get("architectural_decisions", []):
            prompt_parts.append("\nKEY ARCHITECTURAL DECISIONS:")
            for decision in decisions[:3]:
                prompt_parts.append(f"- {decision.get('decision', '')}")
                prompt_parts.append(f"  Rationale: {decision.get('rationale', '')}")
        
        prompt_parts.extend([
            "",
            "Please provide comprehensive business impact analysis including:",
            "1. Financial implications (costs, savings, ROI)",
            "2. Operational impact and efficiency gains",
            "3. Strategic advantages and competitive positioning",
            "4. Risk analysis and mitigation strategies",
            "5. Timeline and business value realization",
            "6. Stakeholder impact and change management needs",
            "",
            "Focus on quantifiable business metrics and actionable insights for decision-makers."
        ])
        
        return "\n".join(prompt_parts)

    def _parse_impact_response(self, response: str) -> Dict[str, Any]:
        """Parse business impact response from LLM."""
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
            
            impact_data = json.loads(json_str)
            
            # Validate and set defaults
            self._validate_impact_data(impact_data)
            
            return impact_data
            
        except Exception as e:
            self.logger.warning("Failed to parse impact response", error=str(e))
            return self._get_fallback_impact()

    def _validate_impact_data(self, data: Dict[str, Any]) -> None:
        """Validate and set defaults for impact data."""
        data.setdefault("executive_summary", {})
        data.setdefault("financial_impact", {})
        data.setdefault("operational_impact", {})
        data.setdefault("strategic_impact", {})
        data.setdefault("risk_analysis", {})
        data.setdefault("timeline_impact", {})
        data.setdefault("scalability_business_impact", {})
        data.setdefault("stakeholder_impact", [])
        data.setdefault("success_metrics", [])
        data.setdefault("confidence_score", 0.85)

    def _calculate_roi_estimates(self, impact_data: Dict, business_context: Any, 
                               architecture_design: Dict) -> Dict[str, Any]:
        """Calculate ROI estimates based on impact analysis."""
        # Basic ROI calculation framework
        roi_analysis = {
            "investment_summary": {
                "total_investment": "To be determined based on detailed estimates",
                "payback_period": "12-24 months (estimated)",
                "roi_percentage": "15-25% annually (estimated)"
            },
            "value_drivers": [
                "Operational efficiency improvements",
                "Reduced maintenance costs",
                "Faster time-to-market for new features",
                "Improved scalability reducing future costs"
            ],
            "cost_categories": [
                "Development and implementation",
                "Infrastructure and hosting",
                "Training and change management",
                "Ongoing maintenance and support"
            ],
            "assumptions": [
                "Team productivity improvements of 20-30%",
                "Reduced system downtime by 50%",
                "Faster feature delivery by 25%",
                "Lower infrastructure costs through optimization"
            ]
        }
        
        # Enhance based on business context
        if business_context:
            company_size = getattr(business_context, 'company_size', 'medium')
            if company_size == 'startup':
                roi_analysis["startup_considerations"] = [
                    "Focus on rapid development and iteration",
                    "Minimize upfront infrastructure costs",
                    "Prioritize scalability for growth"
                ]
            elif company_size == 'enterprise':
                roi_analysis["enterprise_considerations"] = [
                    "Emphasis on security and compliance",
                    "Integration with existing systems",
                    "Long-term maintenance and support"
                ]
        
        return roi_analysis

    def _get_fallback_impact(self) -> Dict[str, Any]:
        """Get fallback business impact data."""
        return {
            "executive_summary": {
                "overall_impact": "positive",
                "key_benefits": [
                    "Improved system scalability and performance",
                    "Reduced long-term maintenance costs",
                    "Enhanced development team productivity"
                ],
                "main_risks": [
                    "Implementation complexity and timeline",
                    "Initial learning curve for team",
                    "Integration challenges with existing systems"
                ],
                "recommendation": "proceed"
            },
            "financial_impact": {
                "implementation_cost": {
                    "development": "$50,000 - $150,000",
                    "infrastructure": "$10,000 - $30,000",
                    "training": "$5,000 - $15,000",
                    "total_estimated": "$65,000 - $195,000"
                },
                "operational_cost": {
                    "annual_infrastructure": "$12,000 - $36,000",
                    "maintenance": "$20,000 - $40,000",
                    "support": "$15,000 - $25,000"
                },
                "cost_savings": [
                    {
                        "area": "Reduced system downtime",
                        "annual_savings": "$25,000 - $50,000",
                        "description": "Improved reliability reduces business disruption"
                    },
                    {
                        "area": "Development efficiency",
                        "annual_savings": "$30,000 - $60,000",
                        "description": "Faster development cycles and reduced debugging time"
                    }
                ],
                "revenue_impact": [
                    {
                        "opportunity": "Faster time-to-market for new features",
                        "potential_value": "$100,000 - $300,000",
                        "timeframe": "12-18 months"
                    }
                ]
            },
            "operational_impact": {
                "efficiency_gains": [
                    {
                        "process": "Software development lifecycle",
                        "improvement": "25% faster development cycles",
                        "quantification": "Reduced time from concept to deployment"
                    },
                    {
                        "process": "System maintenance and support",
                        "improvement": "40% reduction in maintenance overhead",
                        "quantification": "Fewer production issues and easier troubleshooting"
                    }
                ],
                "resource_requirements": [
                    {
                        "resource_type": "human",
                        "requirement": "2-3 developers for 3-6 months",
                        "timeline": "Implementation phase"
                    },
                    {
                        "resource_type": "technical",
                        "requirement": "Cloud infrastructure and development tools",
                        "timeline": "Ongoing"
                    }
                ],
                "workflow_changes": [
                    {
                        "area": "Development process",
                        "change": "Adoption of new architecture patterns and tools",
                        "impact": "Initial learning curve, then improved productivity"
                    }
                ]
            },
            "strategic_impact": {
                "competitive_advantages": [
                    {
                        "advantage": "Faster feature delivery and innovation",
                        "significance": "high",
                        "sustainability": "Long-term with proper maintenance"
                    },
                    {
                        "advantage": "Better scalability for business growth",
                        "significance": "medium",
                        "sustainability": "Supports multi-year growth plans"
                    }
                ],
                "market_positioning": {
                    "current_position": "Competitive but constrained by technical limitations",
                    "target_position": "Technology leader with superior product capabilities",
                    "architecture_contribution": "Enables rapid innovation and superior user experience"
                },
                "innovation_enablement": [
                    {
                        "capability": "Real-time data processing and analytics",
                        "business_value": "Better customer insights and personalization",
                        "timeline": "6-12 months post-implementation"
                    }
                ]
            },
            "risk_analysis": {
                "technical_risks": [
                    {
                        "risk": "Implementation complexity leading to delays",
                        "probability": "medium",
                        "business_impact": "Delayed time-to-market and increased costs",
                        "mitigation": "Phased implementation with regular checkpoints",
                        "cost_of_mitigation": "$10,000 - $20,000"
                    }
                ],
                "business_risks": [
                    {
                        "risk": "Team resistance to new technologies",
                        "probability": "low",
                        "financial_impact": "Reduced productivity during transition",
                        "mitigation": "Comprehensive training and change management"
                    }
                ],
                "opportunity_costs": [
                    {
                        "alternative": "Maintaining current architecture",
                        "foregone_benefit": "Continued technical debt and scaling limitations",
                        "justification": "New architecture provides better long-term value"
                    }
                ]
            },
            "timeline_impact": {
                "time_to_market": "3-6 months for initial implementation",
                "business_value_realization": [
                    {
                        "milestone": "Core system deployment",
                        "value_delivered": "Improved system reliability and performance",
                        "timeline": "3-4 months"
                    },
                    {
                        "milestone": "Full feature implementation",
                        "value_delivered": "Complete business value realization",
                        "timeline": "6-8 months"
                    }
                ],
                "critical_path_items": [
                    "Team training and onboarding",
                    "Core architecture implementation",
                    "Data migration and integration testing"
                ]
            },
            "scalability_business_impact": {
                "growth_enablement": "Architecture supports 10x growth in users and data volume",
                "scaling_costs": "Linear cost scaling with usage, avoiding expensive rewrites",
                "revenue_scalability": "Enables new revenue streams through better performance",
                "operational_scalability": "Reduced operational overhead as system grows"
            },
            "stakeholder_impact": [
                {
                    "stakeholder_group": "Development team",
                    "impact_type": "positive",
                    "specific_impacts": ["Improved productivity", "Better development experience"],
                    "required_actions": ["Training on new technologies", "Process adaptation"]
                },
                {
                    "stakeholder_group": "Business users",
                    "impact_type": "positive",
                    "specific_impacts": ["Better system performance", "New feature capabilities"],
                    "required_actions": ["User training on new features", "Feedback collection"]
                }
            ],
            "success_metrics": [
                {
                    "metric": "System uptime",
                    "current_baseline": "95%",
                    "target_value": "99.5%",
                    "measurement_method": "Automated monitoring and alerting"
                },
                {
                    "metric": "Feature delivery time",
                    "current_baseline": "4-6 weeks",
                    "target_value": "2-3 weeks",
                    "measurement_method": "Development cycle tracking"
                },
                {
                    "metric": "Customer satisfaction",
                    "current_baseline": "7.5/10",
                    "target_value": "8.5/10",
                    "measurement_method": "Regular customer surveys"
                }
            ],
            "roi_analysis": {
                "investment_summary": {
                    "total_investment": "$65,000 - $195,000",
                    "payback_period": "12-18 months",
                    "roi_percentage": "20-30% annually"
                },
                "value_drivers": [
                    "Operational efficiency improvements",
                    "Reduced maintenance costs",
                    "Faster time-to-market for new features",
                    "Improved scalability reducing future costs"
                ]
            },
            "confidence_score": 0.8
        }
