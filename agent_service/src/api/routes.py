from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import structlog
import asyncio
from datetime import datetime

from src.models.agent_models import (
    WorkflowState, UserProfile, BusinessContext, WorkflowType,
    AgentRequest, AgentResponse, ExpertiseLevel
)
from src.workflows.sequential_workflow import SequentialWorkflow

logger = structlog.get_logger()
router = APIRouter()

# Request/Response models
class ProcessConversationRequest(BaseModel):
    conversation_id: str
    user_message: Optional[str] = None
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)
    user_profile: UserProfile
    business_context: Optional[BusinessContext] = None
    workflow_type: Optional[WorkflowType] = WorkflowType.SEQUENTIAL
    options: Dict[str, Any] = Field(default_factory=dict)

class ProcessConversationResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class WorkflowExecutionRequest(BaseModel):
    workflow_type: WorkflowType
    initial_state: WorkflowState

class WorkflowExecutionResponse(BaseModel):
    success: bool
    workflow_type: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    execution_time_seconds: float
    metadata: Dict[str, Any]

# Global workflow instances
workflows = {}

async def get_workflow(workflow_type: WorkflowType):
    """Get workflow instance by type."""
    global workflows
    
    if not workflows:
        workflows = {
            WorkflowType.SEQUENTIAL: SequentialWorkflow(),
        }
    
    return workflows.get(workflow_type)

@router.post("/agent/process", response_model=ProcessConversationResponse)
async def process_conversation(request: ProcessConversationRequest):
    """Main endpoint for processing conversation requests with AI agents."""
    request_start_time = __import__('time').time()
    request_id = f"req_{int(request_start_time)}_{request.conversation_id}"
    
    request_logger = logger.bind(
        request_id=request_id,
        endpoint="/agent/process"
    )
    
    request_logger.info(
        "🌐 API REQUEST RECEIVED",
        conversation_id=request.conversation_id,
        workflow_type=request.workflow_type.value,
        user_expertise=request.user_profile.expertise_level,
        user_message_length=len(request.user_message) if request.user_message else 0,
        conversation_history_length=len(request.conversation_history),
        has_business_context=bool(request.business_context),
        request_options=request.options
    )
    
    try:
        # Build workflow state from request
        workflow_state = WorkflowState(
            conversation_id=request.conversation_id,
            user_query=request.user_message or "Continue conversation",
            user_profile=request.user_profile,
            business_context=request.business_context,
            workflow_type=request.workflow_type,
            conversation_history=request.conversation_history,
            metadata={
                "request_timestamp": datetime.utcnow().isoformat(),
                "options": request.options
            }
        )
        
        # Get appropriate workflow
        workflow = await get_workflow(request.workflow_type)
        if not workflow:
            raise HTTPException(
                status_code=400,
                detail=f"Workflow type {request.workflow_type} not supported"
            )
        
        # Execute workflow
        start_time = asyncio.get_event_loop().time()
        result = await workflow.execute(workflow_state)
        execution_time = asyncio.get_event_loop().time() - start_time
        
        # Build agent response
        # Extract agent outputs from workflow result
        agent_outputs = result.get("agent_outputs", {})
        
        # Convert enhanced architecture design to expected format
        architecture_update = None
        if arch_design := agent_outputs.get("architecture_design"):
            # Enhanced component processing with visualization metadata
            components = []
            for comp in arch_design.get("components", []):
                viz_metadata = comp.get("visualization_metadata", {})
                components.append({
                    "id": comp.get("id", ""),
                    "name": comp.get("name", ""),
                    "type": comp.get("type", ""),
                    "description": comp.get("description", ""),
                    "responsibilities": comp.get("responsibilities", []),
                    "technologies": comp.get("technology", comp.get("technologies", [])) if isinstance(comp.get("technology"), list) else [comp.get("technology", "")],
                    "scalingFactors": comp.get("scalability", comp.get("scaling_factors", [])) if isinstance(comp.get("scalability"), list) else [comp.get("scalability", "")],
                    "businessValue": comp.get("description", comp.get("business_value", "")),
                    
                    # Enhanced visualization properties
                    "visualImportance": viz_metadata.get("visual_importance", 5),
                    "businessCriticality": viz_metadata.get("business_criticality", "medium"),
                    "iconCategory": viz_metadata.get("icon_category", "backend"),
                    "technologyBadges": viz_metadata.get("technology_badges", []),
                    "layerAssignments": viz_metadata.get("layer_assignments", {}),
                    "healthIndicators": viz_metadata.get("health_indicators", {}),
                    "systemOverviewPosition": comp.get("system_overview_position", {}),
                    "deploymentPosition": comp.get("deployment_position", {})
                })
            
            # Enhanced connection processing with visualization metadata
            connections = []
            for conn in arch_design.get("connections", []):
                data_flow = conn.get("data_flow", {"type": "request_response"})
                if isinstance(data_flow, str):
                    data_flow = {"type": data_flow}
                
                viz_metadata = conn.get("visualization_metadata", {})
                connections.append({
                    "id": f"{conn.get('from_component', '')}-{conn.get('to_component', '')}",
                    "fromComponent": conn.get("from_component", ""),
                    "toComponent": conn.get("to_component", ""),
                    "type": conn.get("connection_type", ""),
                    "protocol": conn.get("protocol", ""),
                    "description": conn.get("description", ""),
                    "dataFlow": data_flow,
                    
                    # Enhanced visualization properties
                    "protocolDisplay": viz_metadata.get("protocol_display", "HTTP/REST"),
                    "trafficVolume": viz_metadata.get("traffic_volume", "medium"),
                    "latencyRequirement": viz_metadata.get("latency_requirement", "near_real_time"),
                    "securityLevel": viz_metadata.get("security_level", "medium"),
                    "dependencyStrength": viz_metadata.get("dependency_strength", "important"),
                    "lineStyle": viz_metadata.get("line_style", "solid"),
                    "animationType": viz_metadata.get("animation_type", "unidirectional")
                })
            
            # Extract layer-specific data
            system_overview_data = arch_design.get("system_overview", {})
            deployment_data = arch_design.get("deployment_architecture", {})
            visualization_data = arch_design.get("visualization_data", {})
            
            architecture_update = {
                "components": components,
                "connections": connections,
                "layers": {
                    "systemOverview": {
                        "businessCapabilities": system_overview_data.get("business_capabilities", []),
                        "coreSystems": system_overview_data.get("core_systems", []),
                        "externalIntegrations": system_overview_data.get("external_integrations", []),
                        "dataDomains": system_overview_data.get("data_domains", [])
                    },
                    "deployment": {
                        "infrastructureZones": deployment_data.get("infrastructure_zones", []),
                        "containerClusters": deployment_data.get("container_clusters", []),
                        "networkTopology": deployment_data.get("network_topology", {})
                    }
                },
                "visualizationMetadata": visualization_data.get("visualization_metadata", {}),
                "layerData": visualization_data.get("layer_data", {}),
                "diagramTypes": ["system_overview", "deployment"],
                "patterns": [],
                "technologies": arch_design.get("technology_stack", {}),
                "metadata": {
                    **arch_design.get("metadata", {}),
                    "complexityScore": visualization_data.get("visualization_metadata", {}).get("complexity_score", 5),
                    "recommendedDefaultView": "system_overview"
                }
            }
        
        # Convert why reasoning to expected format
        why_reasoning_formatted = None
        if why_data := agent_outputs.get("why_reasoning"):
            # Extract decision factors from architectural decisions
            decision_factors = []
            for decision in why_data.get("architectural_decisions", []):
                decision_factors.append({
                    "factor": decision.get("decision", decision.get("factor", "")),
                    "importance": decision.get("importance", decision.get("priority", 3)),
                    "explanation": decision.get("rationale", decision.get("explanation", "")),
                    "businessImpact": decision.get("business_impact", decision.get("business_impact", ""))
                })
            
            # Extract tradeoffs from actual tradeoffs or create from design principles  
            tradeoffs = []
            if why_data.get("tradeoffs"):
                for tradeoff in why_data.get("tradeoffs", []):
                    tradeoffs.append({
                        "benefit": tradeoff.get("benefit", ""),
                        "cost": tradeoff.get("cost", ""),
                        "impactLevel": tradeoff.get("impact_level", tradeoff.get("severity", 3))
                    })
            else:
                # Create tradeoffs from design principles if no explicit tradeoffs
                for principle in why_data.get("design_principles", []):
                    if principle.get("principle") and principle.get("application"):
                        tradeoffs.append({
                            "benefit": f"Improved {principle.get('principle', '')}",
                            "cost": principle.get("examples", ["Implementation complexity"])[0] if principle.get("examples") else "Implementation effort",
                            "impactLevel": 3
                        })
            
            # Extract alternatives
            alternatives = []
            for alt in why_data.get("alternatives", []):
                alternatives.append({
                    "name": alt.get("name", alt.get("option", "")),
                    "description": alt.get("description", alt.get("explanation", "")),
                    "pros": alt.get("pros", alt.get("benefits", [])),
                    "cons": alt.get("cons", alt.get("drawbacks", [])),
                    "viabilityScore": alt.get("viability_score", alt.get("score", 3)),
                    "useCases": alt.get("use_cases", alt.get("scenarios", []))
                })
            
            why_reasoning_formatted = {
                "decisionFactors": decision_factors,
                "tradeoffs": tradeoffs,
                "alternatives": alternatives,
                "principles": [p.get("principle", "") for p in why_data.get("design_principles", [])],
                "businessAlignment": why_data.get("business_alignment", []),
                "confidenceLevel": max(1, min(5, int(why_data.get("confidence_score", 0.8) * 5)))
            }
        
        # Convert business impact to expected format
        business_impact_formatted = None
        if impact_data := agent_outputs.get("business_impact"):
            roi_analysis = impact_data.get("roi_analysis", {})
            risk_analysis = impact_data.get("risk_analysis", impact_data.get("risk_assessment", {}))
            
            # Extract or generate financial data
            initial_investment = roi_analysis.get("initial_investment", impact_data.get("cost_analysis", {}))
            if isinstance(initial_investment, dict) and not initial_investment:
                initial_investment = {"development": 50000, "infrastructure": 20000, "training": 10000}
            
            business_impact_formatted = {
                "roiAnalysis": {
                    "initialInvestment": initial_investment,
                    "ongoingCosts": roi_analysis.get("ongoing_costs", {"maintenance": 5000, "hosting": 2000}),
                    "expectedBenefits": roi_analysis.get("expected_benefits", {"efficiency_gains": 100000, "cost_savings": 30000}),
                    "paybackPeriodMonths": roi_analysis.get("payback_period_months", impact_data.get("payback_months", 12)),
                    "netPresentValue": roi_analysis.get("net_present_value", impact_data.get("npv", 80000)),
                    "confidenceLevel": roi_analysis.get("confidence_level", 3)
                },
                "riskAssessment": {
                    "technicalRisks": risk_analysis.get("technical_risks", [
                        {"risk": "Scalability challenges", "impact": "medium", "probability": "low", "mitigation": "Load testing and monitoring"},
                        {"risk": "Integration complexity", "impact": "high", "probability": "medium", "mitigation": "Phased implementation"}
                    ]),
                    "businessRisks": risk_analysis.get("business_risks", [
                        {"risk": "User adoption", "impact": "high", "probability": "medium", "mitigation": "Training and change management"},
                        {"risk": "Compliance requirements", "impact": "medium", "probability": "low", "mitigation": "Regular audits"}
                    ]),
                    "mitigationStrategies": risk_analysis.get("mitigation_strategies", []),
                    "overallRiskLevel": risk_analysis.get("overall_risk_level", 3)
                },
                "competitiveAdvantages": impact_data.get("competitive_advantages", [
                    "Improved system scalability",
                    "Enhanced user experience",
                    "Reduced operational costs",
                    "Faster time to market"
                ]),
                "marketPositioning": impact_data.get("market_positioning", "Enhanced competitive position through improved technology stack"),
                "strategicAlignment": impact_data.get("strategic_alignment", "Aligns with digital transformation and efficiency goals"),
                "successMetrics": impact_data.get("success_metrics", [
                    "System response time < 200ms",
                    "99.9% uptime",
                    "50% reduction in maintenance costs",
                    "User satisfaction > 4.5/5"
                ])
            }
        
        # Convert educational content to expected format
        educational_content_formatted = None
        if edu_data := agent_outputs.get("educational_content"):
            # Process concepts to ensure proper format
            concepts = []
            for concept in edu_data.get("key_concepts", []):
                if isinstance(concept, dict):
                    concepts.append({
                        "concept": concept.get("concept", concept.get("name", "")),
                        "explanation": concept.get("explanation", concept.get("description", "")),
                        "businessRelevance": concept.get("business_relevance", concept.get("relevance", ""))
                    })
                else:
                    concepts.append({
                        "concept": str(concept),
                        "explanation": f"Key architectural concept: {concept}",
                        "businessRelevance": "Important for understanding system design decisions"
                    })
            
            # Process examples
            examples = []
            for example in edu_data.get("real_world_applications", edu_data.get("examples", [])):
                if isinstance(example, dict):
                    examples.append({
                        "title": example.get("title", example.get("name", "")),
                        "description": example.get("description", example.get("explanation", "")),
                        "company": example.get("company", "Various Companies"),
                        "industry": example.get("industry", "Technology"),
                        "outcome": example.get("outcome", example.get("result", "Successful implementation"))
                    })
                else:
                    examples.append({
                        "title": str(example),
                        "description": f"Real-world implementation of {example}",
                        "company": "Industry Leaders",
                        "industry": "Technology",
                        "outcome": "Improved system performance and scalability"
                    })
            
            # Process resources to ensure they are dictionaries
            resources = []
            further_learning = edu_data.get("further_learning", edu_data.get("resources", {}))
            if isinstance(further_learning, dict):
                for key, value in further_learning.items():
                    if isinstance(value, list):
                        for item in value:
                            resources.append({
                                "title": item if isinstance(item, str) else item.get("title", str(item)),
                                "type": key,
                                "description": f"Learn more about {key}",
                                "url": "#",
                                "difficulty": "intermediate"
                            })
                    else:
                        resources.append({
                            "title": key,
                            "type": "resource",
                            "description": str(value),
                            "url": "#",
                            "difficulty": "intermediate"
                        })
            elif isinstance(further_learning, list):
                for item in further_learning:
                    if isinstance(item, dict):
                        resources.append({
                            "title": item.get("title", "Learning Resource"),
                            "type": item.get("type", "article"),
                            "description": item.get("description", ""),
                            "url": item.get("url", "#"),
                            "difficulty": item.get("difficulty", "intermediate")
                        })
                    else:
                        resources.append({
                            "title": str(item),
                            "type": "resource",
                            "description": f"Learn more about {item}",
                            "url": "#",
                            "difficulty": "intermediate"
                        })
            
            educational_content_formatted = {
                "concepts": concepts,
                "examples": examples,
                "exercises": edu_data.get("practical_exercises", [
                    {"title": "Implementation Planning", "description": "Plan the implementation steps for this architecture"},
                    {"title": "Risk Assessment", "description": "Identify and evaluate potential risks"}
                ]),
                "resources": resources,
                "progressTracking": edu_data.get("learning_progression", {
                    "currentLevel": "intermediate",
                    "nextSteps": ["Advanced patterns", "Performance optimization"]
                }),
                "businessContext": edu_data.get("business_context", {
                    "industryRelevance": "High relevance for modern software development",
                    "competitiveAdvantage": "Enables faster development and better scalability"
                })
            }
        
        # Create response dict directly to avoid Pydantic validation issues
        agent_response_dict = {
            "content": result.get("final_content", "Analysis completed successfully"),
            "messageType": "ARCHITECTURE_UPDATE",
            "architectureUpdate": architecture_update,
            "whyReasoning": why_reasoning_formatted,
            "businessImpact": business_impact_formatted,
            "educationalContent": educational_content_formatted,
            "suggestedActions": result.get("suggested_actions", []),
            "nextQuestions": result.get("next_questions", []),
            "confidenceScore": result.get("confidence_score", 0.8)
        }
        
        total_request_time = round(__import__('time').time() - request_start_time, 2)
        
        request_logger.info(
            "🎉 API REQUEST COMPLETED SUCCESSFULLY",
            conversation_id=request.conversation_id,
            total_request_time_seconds=total_request_time,
            workflow_execution_time_seconds=execution_time,
            workflow_type=request.workflow_type.value,
            agents_executed=result.get("completed_steps", []),
            confidence_score=result.get("confidence_score", 0),
            response_content_length=len(agent_response_dict["content"]),
            has_architecture_update=bool(agent_response_dict["architectureUpdate"]),
            has_why_reasoning=bool(agent_response_dict["whyReasoning"]),
            has_business_impact=bool(agent_response_dict["businessImpact"]),
            has_educational_content=bool(agent_response_dict["educationalContent"]),
            suggested_actions_count=len(agent_response_dict["suggestedActions"]),
            next_questions_count=len(agent_response_dict["nextQuestions"])
        )
        
        return ProcessConversationResponse(
            success=True,
            data=agent_response_dict,
            metadata={
                "request_id": request_id,
                "total_request_time_seconds": total_request_time,
                "workflow_execution_time_seconds": execution_time,
                "workflow_type": request.workflow_type.value,
                "agents_used": result.get("completed_steps", []),
                "processing_metadata": result.get("metadata", {}),
                "timestamp": __import__('datetime').datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        total_request_time = round(__import__('time').time() - request_start_time, 2)
        
        request_logger.error(
            "💥 API REQUEST FAILED",
            conversation_id=request.conversation_id,
            error=str(e),
            error_type=type(e).__name__,
            total_request_time_seconds=total_request_time,
            workflow_type=request.workflow_type.value,
            failed_at_stage="workflow_execution"
        )
        
        return ProcessConversationResponse(
            success=False,
            error={
                "code": "PROCESSING_FAILED",
                "message": str(e),
                "conversation_id": request.conversation_id,
                "request_id": request_id,
                "error_type": type(e).__name__,
                "total_request_time_seconds": total_request_time
            }
        )

@router.post("/workflow/execute", response_model=WorkflowExecutionResponse)
async def execute_workflow(request: WorkflowExecutionRequest):
    """Direct workflow execution endpoint for testing and debugging."""
    logger.info(
        "Executing workflow directly",
        workflow_type=request.workflow_type,
        conversation_id=request.initial_state.conversation_id
    )
    
    try:
        workflow = await get_workflow(request.workflow_type)
        if not workflow:
            raise HTTPException(
                status_code=400,
                detail=f"Workflow type {request.workflow_type} not supported"
            )
        
        start_time = asyncio.get_event_loop().time()
        result = await workflow.execute(request.initial_state)
        execution_time = asyncio.get_event_loop().time() - start_time
        
        return WorkflowExecutionResponse(
            success=True,
            workflow_type=request.workflow_type.value,
            result=result,
            execution_time_seconds=execution_time,
            metadata={
                "workflow_status": "completed",
                "steps_executed": len(result.get("completed_steps", [])),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(
            "Workflow execution failed",
            workflow_type=request.workflow_type,
            error=str(e)
        )
        
        return WorkflowExecutionResponse(
            success=False,
            workflow_type=request.workflow_type.value,
            error={
                "code": "WORKFLOW_EXECUTION_FAILED",
                "message": str(e)
            },
            execution_time_seconds=0.0,
            metadata={"error_timestamp": datetime.utcnow().isoformat()}
        )

@router.get("/workflows/status")
async def get_workflows_status():
    """Get status of all available workflows."""
    status = {}
    
    for workflow_type in [WorkflowType.SEQUENTIAL]:
        try:
            workflow = await get_workflow(workflow_type)
            if workflow:
                workflow_status = await workflow.get_workflow_status()
                status[workflow_type.value] = workflow_status
            else:
                status[workflow_type.value] = {"status": "not_available"}
        except Exception as e:
            status[workflow_type.value] = {"status": "error", "error": str(e)}
    
    return {
        "workflows": status,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/agents/health")
async def get_agents_health():
    """Get health status of all agents."""
    from src.agents.orchestrator import OrchestratorAgent
    from src.agents.requirements_agent import RequirementsAgent
    from src.agents.research_agent import ResearchAgent
    from src.agents.architecture_agent import ArchitectureAgent
    from src.agents.why_reasoning_agent import WhyReasoningAgent
    from src.agents.business_impact_agent import BusinessImpactAgent
    from src.agents.educational_agent import EducationalAgent
    from src.agents.documentation_agent import DocumentationAgent
    
    agents = {
        "orchestrator": OrchestratorAgent(),
        "requirements": RequirementsAgent(),
        "research": ResearchAgent(),
        "architecture": ArchitectureAgent(),
        "why_reasoning": WhyReasoningAgent(),
        "business_impact": BusinessImpactAgent(),
        "educational": EducationalAgent(),
        "documentation": DocumentationAgent(),
    }
    
    health_status = {}
    
    for name, agent in agents.items():
        try:
            status = await agent.get_health_status()
            health_status[name] = status
        except Exception as e:
            health_status[name] = {
                "agent": name,
                "status": "error",
                "error": str(e)
            }
    
    overall_status = "healthy"
    if any(status.get("status") != "healthy" for status in health_status.values()):
        overall_status = "degraded"
    
    return {
        "overall_status": overall_status,
        "agents": health_status,
        "timestamp": datetime.utcnow().isoformat(),
        "total_agents": len(agents)
    }

@router.get("/services/status")
async def get_services_status():
    """Get status of external services."""
    from src.services.groq_service import GroqService
    from src.services.tavily_service import TavilyService
    
    groq_service = GroqService()
    tavily_service = TavilyService()
    
    services_status = {}
    
    try:
        groq_healthy = await groq_service.health_check()
        groq_stats = groq_service.get_usage_stats()
        services_status["groq"] = {
            "status": "healthy" if groq_healthy else "unhealthy",
            "usage_stats": groq_stats
        }
    except Exception as e:
        services_status["groq"] = {"status": "error", "error": str(e)}
    
    try:
        tavily_healthy = await tavily_service.health_check()
        tavily_stats = tavily_service.get_usage_stats()
        services_status["tavily"] = {
            "status": "healthy" if tavily_healthy else "unhealthy",
            "usage_stats": tavily_stats
        }
    except Exception as e:
        services_status["tavily"] = {"status": "error", "error": str(e)}
    
    overall_status = "healthy"
    if any(status.get("status") != "healthy" for status in services_status.values()):
        overall_status = "degraded"
    
    return {
        "overall_status": overall_status,
        "services": services_status,
        "timestamp": datetime.utcnow().isoformat()
    }
