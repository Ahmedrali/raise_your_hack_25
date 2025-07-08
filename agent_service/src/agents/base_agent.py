from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import structlog
from src.models.agent_models import WorkflowState, UserProfile, BusinessContext
from src.services.groq_service import GroqService
from src.services.simple_tavily_service import SimpleTavilyService

logger = structlog.get_logger()

class BaseAgent(ABC):
    """Base class for all specialized agents."""
    
    def __init__(self, name: str):
        self.name = name
        self.groq_service = GroqService()
        self.tavily_service = SimpleTavilyService()
        self.logger = logger.bind(agent=name)

    @abstractmethod
    async def process(self, state: WorkflowState) -> Dict[str, Any]:
        """Process the current state and return updates."""
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent."""
        pass

    def get_user_adapted_prompt(self, base_prompt: str, user_profile: UserProfile) -> str:
        """Adapt prompt based on user's expertise level and context."""
        expertise_adaptations = {
            "BEGINNER": "Provide detailed explanations with basic concepts and avoid jargon.",
            "INTERMEDIATE": "Provide clear explanations with some technical detail.",
            "ADVANCED": "Focus on technical depth and advanced concepts.",
            "EXPERT": "Provide concise, highly technical analysis."
        }
        
        business_adaptation = ""
        if user_profile.business_role:
            business_adaptation = f"Consider the perspective of a {user_profile.business_role}."
        
        adaptation = expertise_adaptations.get(user_profile.expertise_level, "")
        
        return f"{base_prompt}\n\nUser Adaptation: {adaptation} {business_adaptation}".strip()

    async def query_groq_with_context(
        self,
        prompt: str,
        state: WorkflowState,
        system_prompt: Optional[str] = None
    ) -> str:
        """Query Groq with full context."""
        llm_start_time = __import__('time').time()
        
        self.logger.info("🤖 LLM REQUEST START",
                        conversation_id=state.conversation_id,
                        agent=self.name,
                        prompt_length=len(prompt),
                        has_system_prompt=bool(system_prompt))
        
        try:
            context_prompt = self._build_context_prompt(prompt, state)
            system = system_prompt or self.get_system_prompt()
            
            self.logger.debug("LLM request details",
                            conversation_id=state.conversation_id,
                            agent=self.name,
                            context_prompt_length=len(context_prompt),
                            system_prompt_length=len(system))
            
            response = await self.groq_service.query(
                prompt=context_prompt,
                system_message=system
            )
            
            llm_execution_time = round(__import__('time').time() - llm_start_time, 2)
            
            self.logger.info("✅ LLM REQUEST COMPLETE",
                           conversation_id=state.conversation_id,
                           agent=self.name,
                           execution_time_seconds=llm_execution_time,
                           response_length=len(response),
                           response_preview=response[:150] + "..." if len(response) > 150 else response)
            
            return response
            
        except Exception as e:
            llm_execution_time = round(__import__('time').time() - llm_start_time, 2)
            
            self.logger.error("❌ LLM REQUEST FAILED",
                            conversation_id=state.conversation_id,
                            agent=self.name,
                            error=str(e),
                            error_type=type(e).__name__,
                            failed_after_seconds=llm_execution_time)
            raise

    def _build_context_prompt(self, prompt: str, state: WorkflowState) -> str:
        """Build comprehensive context prompt with conversation history."""
        context_parts = [
            f"User Query: {state.user_query}",
            f"User Expertise: {state.user_profile.expertise_level}",
        ]
        
        if state.user_profile.business_role:
            context_parts.append(f"Business Role: {state.user_profile.business_role}")
        
        if state.business_context:
            context_parts.append(f"Business Context: {state.business_context}")
        
        # Add conversation history for context continuity
        if state.conversation_history:
            context_parts.append("\nPREVIOUS CONVERSATION CONTEXT:")
            
            # Get the last few messages for context (avoid overwhelming the prompt)
            recent_messages = state.conversation_history[-6:] if len(state.conversation_history) > 6 else state.conversation_history
            
            for msg in recent_messages:
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                message_type = msg.get('messageType', '')
                
                # Truncate very long messages but preserve key information
                if len(content) > 300:
                    content = content[:300] + "..."
                
                # Include message type for architecture updates
                if message_type == 'ARCHITECTURE_UPDATE':
                    context_parts.append(f"- {role}: [ARCHITECTURE UPDATE] {content}")
                else:
                    context_parts.append(f"- {role}: {content}")
            
            context_parts.append("NOTE: Build upon and enhance previous architectural decisions rather than replacing them completely.")
        
        if state.requirements_analysis:
            context_parts.append(f"Requirements: {state.requirements_analysis}")
        
        if state.research_findings:
            context_parts.append(f"Research: {state.research_findings}")
        
        # Add existing architecture context if available
        if state.architecture_design:
            context_parts.append(f"EXISTING ARCHITECTURE: {state.architecture_design}")
            context_parts.append("IMPORTANT: Enhance and extend the existing architecture, don't create a completely new one.")
        
        context = "\n".join(context_parts)
        return f"{context}\n\nCurrent Task: {prompt}"

    def validate_response(self, response: str) -> bool:
        """Validate agent response."""
        return bool(response and len(response.strip()) > 10)

    async def get_health_status(self) -> Dict[str, Any]:
        """Get health status of the agent."""
        try:
            groq_healthy = await self.groq_service.health_check()
            tavily_healthy = await self.tavily_service.health_check()
            
            return {
                "agent": self.name,
                "status": "healthy" if groq_healthy and tavily_healthy else "degraded",
                "groq_service": groq_healthy,
                "tavily_service": tavily_healthy
            }
        except Exception as e:
            return {
                "agent": self.name,
                "status": "unhealthy",
                "error": str(e)
            }
