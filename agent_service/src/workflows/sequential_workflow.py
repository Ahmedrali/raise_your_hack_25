from typing import Dict, Any
import asyncio
from src.models.agent_models import WorkflowState
from src.agents.orchestrator import OrchestratorAgent
from src.agents.requirements_agent import RequirementsAgent
from src.agents.research_agent import ResearchAgent
from src.agents.architecture_agent import ArchitectureAgent
from src.agents.why_reasoning_agent import WhyReasoningAgent
from src.agents.business_impact_agent import BusinessImpactAgent
from src.agents.educational_agent import EducationalAgent
from src.agents.documentation_agent import DocumentationAgent
import structlog

logger = structlog.get_logger()

class SequentialWorkflow:
    """Sequential workflow for comprehensive step-by-step architecture analysis."""
    
    def __init__(self):
        self.name = "sequential"
        self.agents = {
            "orchestrator": OrchestratorAgent(),
            "requirements": RequirementsAgent(),
            "research": ResearchAgent(),
            "architecture": ArchitectureAgent(),
            "why_reasoning": WhyReasoningAgent(),
            "business_impact": BusinessImpactAgent(),
            "educational": EducationalAgent(),
            "documentation": DocumentationAgent(),
        }

    async def execute(self, initial_state: WorkflowState) -> Dict[str, Any]:
        """Execute comprehensive sequential workflow."""
        if not self.validate_state(initial_state):
            raise ValueError("Invalid initial state for sequential workflow")
        
        workflow_start_time = logger.bind(
            workflow_execution_id=f"wf_{initial_state.conversation_id}_{int(__import__('time').time())}"
        )
        
        workflow_start_time.info("🚀 WORKFLOW EXECUTION STARTED",
                                conversation_id=initial_state.conversation_id,
                                total_agents=len(self.agents),
                                user_query_preview=initial_state.user_query[:100] + "..." if len(initial_state.user_query) > 100 else initial_state.user_query,
                                user_expertise=initial_state.user_profile.expertise_level,
                                workflow_type="SEQUENTIAL")
        
        execution_times = {}
        step_results = {}
        
        try:
            # Step 1: Orchestrator - Plan the workflow
            step_start = __import__('time').time()
            step_logger = logger.bind(
                step_number=1,
                step_name="orchestrator",
                agent_type="OrchestratorAgent"
            )
            
            step_logger.info("📋 AGENT EXECUTION START: Orchestrator Planning",
                           conversation_id=initial_state.conversation_id,
                           step_description="Analyzing query and creating orchestration plan")
            
            orchestrator_result = await self.agents["orchestrator"].process(initial_state)
            execution_times["orchestrator"] = round(__import__('time').time() - step_start, 2)
            
            initial_state.orchestrator_plan = orchestrator_result.get("orchestrator_plan", {})
            initial_state.completed_steps.append("orchestrator")
            initial_state.current_step = "requirements"
            step_results["orchestrator"] = {
                "success": True,
                "workflow_type": initial_state.orchestrator_plan.get("workflow_type"),
                "agents_required": initial_state.orchestrator_plan.get("agents_required", []),
                "complexity_score": initial_state.orchestrator_plan.get("complexity_score")
            }
            
            step_logger.info("✅ AGENT EXECUTION COMPLETE: Orchestrator",
                           conversation_id=initial_state.conversation_id,
                           execution_time_seconds=execution_times["orchestrator"],
                           result_summary=step_results["orchestrator"])
            
            # Step 2: Requirements Analysis
            step_start = __import__('time').time()
            step_logger = logger.bind(
                step_number=2,
                step_name="requirements",
                agent_type="RequirementsAgent"
            )
            
            step_logger.info("📝 AGENT EXECUTION START: Requirements Analysis",
                           conversation_id=initial_state.conversation_id,
                           step_description="Analyzing and clarifying architectural requirements")
            
            requirements_result = await self.agents["requirements"].process(initial_state)
            execution_times["requirements"] = round(__import__('time').time() - step_start, 2)
            
            initial_state.requirements_analysis = requirements_result.get("requirements_analysis", {})
            initial_state.completed_steps.append("requirements")
            initial_state.current_step = "research"
            step_results["requirements"] = {
                "success": True,
                "functional_requirements_count": len(initial_state.requirements_analysis.get("functional_requirements", [])),
                "non_functional_requirements_count": len(initial_state.requirements_analysis.get("non_functional_requirements", [])),
                "clarification_questions_count": len(initial_state.requirements_analysis.get("clarification_questions", []))
            }
            
            step_logger.info("✅ AGENT EXECUTION COMPLETE: Requirements",
                           conversation_id=initial_state.conversation_id,
                           execution_time_seconds=execution_times["requirements"],
                           result_summary=step_results["requirements"])
            
            # Step 3: Research - Gather patterns and best practices
            step_start = __import__('time').time()
            step_logger = logger.bind(
                step_number=3,
                step_name="research",
                agent_type="ResearchAgent"
            )
            
            step_logger.info("🔍 AGENT EXECUTION START: Research & Pattern Analysis",
                           conversation_id=initial_state.conversation_id,
                           step_description="Gathering current market and technical intelligence")
            
            research_result = await self.agents["research"].process(initial_state)
            execution_times["research"] = round(__import__('time').time() - step_start, 2)
            
            initial_state.research_data = research_result.get("research_data", {})
            initial_state.completed_steps.append("research")
            initial_state.current_step = "architecture"
            step_results["research"] = {
                "success": True,
                "patterns_found": len(initial_state.research_data.get("architectural_patterns", [])),
                "technologies_analyzed": len(initial_state.research_data.get("technology_recommendations", [])),
                "market_insights_count": len(initial_state.research_data.get("market_analysis", []))
            }
            
            step_logger.info("✅ AGENT EXECUTION COMPLETE: Research",
                           conversation_id=initial_state.conversation_id,
                           execution_time_seconds=execution_times["research"],
                           result_summary=step_results["research"])
            
            # Step 4: Architecture Design
            step_start = __import__('time').time()
            step_logger = logger.bind(
                step_number=4,
                step_name="architecture",
                agent_type="ArchitectureAgent"
            )
            
            step_logger.info("🏗️ AGENT EXECUTION START: Architecture Design",
                           conversation_id=initial_state.conversation_id,
                           step_description="Designing technical solutions and patterns")
            
            architecture_result = await self.agents["architecture"].process(initial_state)
            execution_times["architecture"] = round(__import__('time').time() - step_start, 2)
            
            initial_state.architecture_design = architecture_result.get("architecture_design", {})
            initial_state.completed_steps.append("architecture")
            initial_state.current_step = "why_reasoning"
            step_results["architecture"] = {
                "success": True,
                "components_designed": len(initial_state.architecture_design.get("components", [])),
                "connections_mapped": len(initial_state.architecture_design.get("connections", [])),
                "architecture_pattern": initial_state.architecture_design.get("architecture_overview", {}).get("pattern"),
                "has_visualization_data": bool(initial_state.architecture_design.get("visualization_data"))
            }
            
            step_logger.info("✅ AGENT EXECUTION COMPLETE: Architecture",
                           conversation_id=initial_state.conversation_id,
                           execution_time_seconds=execution_times["architecture"],
                           result_summary=step_results["architecture"])
            
            # Step 5: Why Reasoning - Explain decisions
            step_start = __import__('time').time()
            step_logger = logger.bind(
                step_number=5,
                step_name="why_reasoning",
                agent_type="WhyReasoningAgent"
            )
            
            step_logger.info("🤔 AGENT EXECUTION START: Why Reasoning Analysis",
                           conversation_id=initial_state.conversation_id,
                           step_description="Providing comprehensive decision explanations")
            
            why_reasoning_result = await self.agents["why_reasoning"].process(initial_state)
            execution_times["why_reasoning"] = round(__import__('time').time() - step_start, 2)
            
            initial_state.why_reasoning = why_reasoning_result.get("why_reasoning", {})
            initial_state.completed_steps.append("why_reasoning")
            initial_state.current_step = "business_impact"
            step_results["why_reasoning"] = {
                "success": True,
                "architectural_decisions_count": len(initial_state.why_reasoning.get("architectural_decisions", [])),
                "trade_offs_analyzed": len(initial_state.why_reasoning.get("trade_offs", [])),
                "alternatives_considered": len(initial_state.why_reasoning.get("alternatives", []))
            }
            
            step_logger.info("✅ AGENT EXECUTION COMPLETE: Why Reasoning",
                           conversation_id=initial_state.conversation_id,
                           execution_time_seconds=execution_times["why_reasoning"],
                           result_summary=step_results["why_reasoning"])
            
            # Step 6: Business Impact Analysis
            step_start = __import__('time').time()
            step_logger = logger.bind(
                step_number=6,
                step_name="business_impact",
                agent_type="BusinessImpactAgent"
            )
            
            step_logger.info("💼 AGENT EXECUTION START: Business Impact Analysis",
                           conversation_id=initial_state.conversation_id,
                           step_description="Analyzing ROI, risks, and business implications")
            
            business_impact_result = await self.agents["business_impact"].process(initial_state)
            execution_times["business_impact"] = round(__import__('time').time() - step_start, 2)
            
            initial_state.business_impact = business_impact_result.get("business_impact", {})
            initial_state.completed_steps.append("business_impact")
            initial_state.current_step = "educational"
            step_results["business_impact"] = {
                "success": True,
                "roi_analysis": bool(initial_state.business_impact.get("financial_analysis")),
                "risk_assessment": bool(initial_state.business_impact.get("risk_analysis")),
                "implementation_timeline": bool(initial_state.business_impact.get("timeline_impact")),
                "overall_recommendation": initial_state.business_impact.get("executive_summary", {}).get("recommendation")
            }
            
            step_logger.info("✅ AGENT EXECUTION COMPLETE: Business Impact",
                           conversation_id=initial_state.conversation_id,
                           execution_time_seconds=execution_times["business_impact"],
                           result_summary=step_results["business_impact"])
            
            # Step 7: Educational Content Generation
            step_start = __import__('time').time()
            step_logger = logger.bind(
                step_number=7,
                step_name="educational",
                agent_type="EducationalAgent"
            )
            
            step_logger.info("🎓 AGENT EXECUTION START: Educational Content Generation",
                           conversation_id=initial_state.conversation_id,
                           step_description="Creating adaptive learning content")
            
            educational_result = await self.agents["educational"].process(initial_state)
            execution_times["educational"] = round(__import__('time').time() - step_start, 2)
            
            initial_state.educational_content = educational_result.get("educational_content", {})
            initial_state.completed_steps.append("educational")
            initial_state.current_step = "documentation"
            step_results["educational"] = {
                "success": True,
                "key_concepts_count": len(initial_state.educational_content.get("key_concepts", [])),
                "learning_path_steps": len(initial_state.educational_content.get("learning_path", [])),
                "assessment_questions": len(initial_state.educational_content.get("assessment_questions", [])),
                "adapted_to_expertise": initial_state.user_profile.expertise_level
            }
            
            step_logger.info("✅ AGENT EXECUTION COMPLETE: Educational",
                           conversation_id=initial_state.conversation_id,
                           execution_time_seconds=execution_times["educational"],
                           result_summary=step_results["educational"])
            
            # Step 8: Documentation Generation
            step_start = __import__('time').time()
            step_logger = logger.bind(
                step_number=8,
                step_name="documentation",
                agent_type="DocumentationAgent"
            )
            
            step_logger.info("📚 AGENT EXECUTION START: Documentation Generation",
                           conversation_id=initial_state.conversation_id,
                           step_description="Generating professional documentation")
            
            documentation_result = await self.agents["documentation"].process(initial_state)
            execution_times["documentation"] = round(__import__('time').time() - step_start, 2)
            
            initial_state.documentation = documentation_result.get("documentation", {})
            initial_state.completed_steps.append("documentation")
            initial_state.current_step = "completed"
            step_results["documentation"] = {
                "success": True,
                "sections_generated": len(initial_state.documentation.get("sections", [])),
                "technical_specs": bool(initial_state.documentation.get("technical_specifications")),
                "implementation_guide": bool(initial_state.documentation.get("implementation_guide")),
                "document_format": initial_state.documentation.get("format", "markdown")
            }
            
            step_logger.info("✅ AGENT EXECUTION COMPLETE: Documentation",
                           conversation_id=initial_state.conversation_id,
                           execution_time_seconds=execution_times["documentation"],
                           result_summary=step_results["documentation"])
            
            # Compile comprehensive final response
            final_response = self._compile_comprehensive_response(initial_state)
            
            total_execution_time = sum(execution_times.values())
            workflow_start_time.info("🎉 WORKFLOW EXECUTION COMPLETED SUCCESSFULLY",
                                   conversation_id=initial_state.conversation_id,
                                   total_execution_time_seconds=round(total_execution_time, 2),
                                   steps_completed=len(initial_state.completed_steps),
                                   execution_breakdown=execution_times,
                                   workflow_summary={
                                       "total_agents_executed": len(execution_times),
                                       "longest_step": max(execution_times.items(), key=lambda x: x[1])[0],
                                       "longest_step_time": max(execution_times.values()),
                                       "shortest_step": min(execution_times.items(), key=lambda x: x[1])[0],
                                       "shortest_step_time": min(execution_times.values()),
                                       "average_step_time": round(total_execution_time / len(execution_times), 2)
                                   })
            
            return final_response
            
        except Exception as e:
            total_execution_time = sum(execution_times.values()) if execution_times else 0
            workflow_start_time.error("💥 WORKFLOW EXECUTION FAILED", 
                                    error=str(e),
                                    error_type=type(e).__name__,
                                    conversation_id=initial_state.conversation_id,
                                    current_step=initial_state.current_step,
                                    completed_steps=initial_state.completed_steps,
                                    failed_after_seconds=round(total_execution_time, 2),
                                    execution_times_before_failure=execution_times,
                                    step_results_before_failure=step_results)
            raise

    def validate_state(self, state: WorkflowState) -> bool:
        """Validate workflow state."""
        required_fields = ["conversation_id", "user_query", "user_profile"]
        return all(hasattr(state, field) and getattr(state, field) for field in required_fields)

    def _compile_comprehensive_response(self, state: WorkflowState) -> Dict[str, Any]:
        """Compile comprehensive final response from all workflow agents."""
        
        # Generate comprehensive response content
        content = self._generate_comprehensive_content(state)
        
        # Extract next questions and suggestions from all agents
        next_questions = self._extract_comprehensive_questions(state)
        suggested_actions = self._extract_comprehensive_actions(state)
        
        # Compile all agent outputs
        agent_outputs = {
            "orchestrator_plan": getattr(state, 'orchestrator_plan', {}),
            "requirements_analysis": getattr(state, 'requirements_analysis', {}),
            "research_data": getattr(state, 'research_data', {}),
            "architecture_design": getattr(state, 'architecture_design', {}),
            "why_reasoning": getattr(state, 'why_reasoning', {}),
            "business_impact": getattr(state, 'business_impact', {}),
            "educational_content": getattr(state, 'educational_content', {}),
            "documentation": getattr(state, 'documentation', {})
        }
        
        return {
            "success": True,
            "workflow_type": "SEQUENTIAL",
            "conversation_id": state.conversation_id,
            "final_content": content,
            "next_questions": next_questions,
            "suggested_actions": suggested_actions,
            "completed_steps": state.completed_steps,
            "confidence_score": self._calculate_overall_confidence(agent_outputs),
            "agent_outputs": agent_outputs,
            "metadata": {
                "workflow_completed": True,
                "total_steps": len(state.completed_steps),
                "final_step": state.current_step,
                "agents_executed": len(self.agents),
                "processing_summary": self._generate_processing_summary(state)
            }
        }

    def _generate_comprehensive_content(self, state: WorkflowState) -> str:
        """Generate comprehensive response content from all agents."""
        content_parts = [
            f"I've completed a comprehensive analysis of your request: {state.user_query}",
            "",
            "## Executive Summary"
        ]
        
        # Add business impact summary if available
        if business_impact := getattr(state, 'business_impact', {}):
            if exec_summary := business_impact.get("executive_summary", {}):
                content_parts.extend([
                    f"**Overall Impact**: {exec_summary.get('overall_impact', 'Positive').title()}",
                    f"**Recommendation**: {exec_summary.get('recommendation', 'Proceed').title()}",
                    ""
                ])
                
                if benefits := exec_summary.get("key_benefits", []):
                    content_parts.append("**Key Benefits:**")
                    for benefit in benefits[:3]:
                        content_parts.append(f"• {benefit}")
                    content_parts.append("")
        
        # Add architecture overview
        if architecture_design := getattr(state, 'architecture_design', {}):
            if overview := architecture_design.get("architecture_overview", {}):
                content_parts.extend([
                    "## Architecture Overview",
                    f"**Pattern**: {overview.get('pattern', 'Not specified').title()}",
                    f"**Description**: {overview.get('description', 'Architecture design completed')}",
                    ""
                ])
            
            if components := architecture_design.get("components", []):
                content_parts.append("**Key Components:**")
                for comp in components[:4]:
                    content_parts.append(f"• **{comp.get('name', '')}**: {comp.get('description', '')}")
                content_parts.append("")
        
        # Add key insights from why reasoning
        if why_reasoning := getattr(state, 'why_reasoning', {}):
            if decisions := why_reasoning.get("architectural_decisions", []):
                content_parts.extend([
                    "## Key Architectural Decisions",
                    ""
                ])
                for decision in decisions[:2]:
                    content_parts.extend([
                        f"**{decision.get('decision', '')}**",
                        f"*Rationale*: {decision.get('rationale', '')}",
                        ""
                    ])
        
        # Add learning opportunities
        if educational_content := getattr(state, 'educational_content', {}):
            if concepts := educational_content.get("key_concepts", []):
                content_parts.extend([
                    "## Learning Opportunities",
                    "Based on your expertise level, here are key concepts to explore:",
                    ""
                ])
                for concept in concepts[:2]:
                    content_parts.extend([
                        f"**{concept.get('concept', '')}**: {concept.get('definition', '')}",
                        ""
                    ])
        
        content_parts.extend([
            "## Next Steps",
            "I've prepared a complete architecture design with detailed documentation, business impact analysis, and educational resources.",
            "",
            "**Immediate Actions:**",
            "1. Review the detailed architecture design and documentation",
            "2. Examine the business impact analysis and ROI projections", 
            "3. Explore the educational content to deepen your understanding",
            "4. Consider the implementation roadmap and timeline",
            "",
            "Would you like me to elaborate on any specific aspect of the analysis?"
        ])
        
        return "\n".join(content_parts)

    def _extract_comprehensive_questions(self, state: WorkflowState) -> list:
        """Extract relevant next questions from all agents."""
        questions = []
        
        # Get questions from requirements analysis
        if requirements := getattr(state, 'requirements_analysis', {}):
            questions.extend(requirements.get("clarification_questions", []))
        
        # Get questions from educational content
        if educational := getattr(state, 'educational_content', {}):
            if assessment := educational.get("assessment_questions", []):
                for q in assessment[:2]:
                    questions.append(q.get("question", ""))
        
        # Add default questions if none found
        if not questions:
            questions = [
                "Would you like me to explain any specific architectural decisions in more detail?",
                "Are there particular aspects of the implementation you'd like to focus on?",
                "Do you have questions about the business impact or ROI analysis?",
                "Would you like to explore the educational content for any specific technologies?"
            ]
        
        return questions[:4]  # Limit to 4 questions

    def _extract_comprehensive_actions(self, state: WorkflowState) -> list:
        """Extract suggested actions from all agents."""
        actions = []
        
        # Get actions from business impact
        if business_impact := getattr(state, 'business_impact', {}):
            if timeline := business_impact.get("timeline_impact", {}):
                if milestones := timeline.get("business_value_realization", []):
                    for milestone in milestones[:2]:
                        actions.append(f"Achieve {milestone.get('milestone', '')} within {milestone.get('timeline', '')}")
        
        # Get actions from architecture design
        if architecture := getattr(state, 'architecture_design', {}):
            if phases := architecture.get("implementation_phases", []):
                for phase in phases[:2]:
                    actions.append(f"Phase {phase.get('phase', '')}: {phase.get('name', '')} ({phase.get('duration', '')})")
        
        # Add default actions if none found
        if not actions:
            actions = [
                "Review and approve the architecture design document",
                "Begin implementation planning and team preparation",
                "Set up development environment and initial infrastructure",
                "Start with the first implementation phase"
            ]
        
        return actions[:4]  # Limit to 4 actions

    def _calculate_overall_confidence(self, agent_outputs: Dict[str, Any]) -> float:
        """Calculate overall confidence score from all agents."""
        confidence_scores = []
        
        for agent_name, output in agent_outputs.items():
            if isinstance(output, dict) and "confidence_score" in output:
                confidence_scores.append(output["confidence_score"])
        
        if confidence_scores:
            return sum(confidence_scores) / len(confidence_scores)
        return 0.85  # Default confidence

    def _generate_processing_summary(self, state: WorkflowState) -> Dict[str, Any]:
        """Generate summary of processing completed."""
        return {
            "agents_completed": state.completed_steps,
            "total_agents": len(self.agents),
            "workflow_status": "completed",
            "has_architecture_design": hasattr(state, 'architecture_design'),
            "has_business_impact": hasattr(state, 'business_impact'),
            "has_educational_content": hasattr(state, 'educational_content'),
            "has_documentation": hasattr(state, 'documentation'),
            "comprehensive_analysis": True
        }

    async def get_workflow_status(self) -> Dict[str, Any]:
        """Get workflow status and health."""
        return {
            "workflow": self.name,
            "status": "healthy",
            "agents_count": len(self.agents)
        }
