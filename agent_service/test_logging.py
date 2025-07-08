#!/usr/bin/env python3
"""
Test script to verify the enhanced logging functionality.
"""

import sys
import os
import asyncio
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.logging_config import configure_logging, get_logger
from src.models.agent_models import WorkflowState, UserProfile
from src.workflows.sequential_workflow import SequentialWorkflow


async def test_logging():
    """Test the logging functionality with a mock workflow execution."""
    
    # Configure logging
    configure_logging()
    logger = get_logger("test")
    
    print("=" * 80)
    print("🧪 TESTING ENHANCED AGENT LOGGING SYSTEM")
    print("=" * 80)
    
    # Test basic logging
    logger.info("📋 LOGGING TEST STARTED", 
               test_type="agent_logging_verification",
               timestamp=datetime.utcnow().isoformat())
    
    # Create mock workflow state
    user_profile = UserProfile(
        id="test-user-123",
        email="test@example.com",
        expertise_level="INTERMEDIATE"
    )
    
    workflow_state = WorkflowState(
        conversation_id="test-conv-456",
        user_query="Design a scalable microservices architecture for an e-commerce platform",
        user_profile=user_profile
    )
    
    # Test workflow logging (but don't actually run the agents)
    workflow = SequentialWorkflow()
    
    logger.info("🔍 TESTING WORKFLOW LOGGING STRUCTURE")
    
    # Simulate agent execution logging
    test_agents = [
        ("orchestrator", "📋", "Analyzing query and creating orchestration plan"),
        ("requirements", "📝", "Analyzing and clarifying architectural requirements"),
        ("research", "🔍", "Gathering current market and technical intelligence"),
        ("architecture", "🏗️", "Designing technical solutions and patterns"),
        ("why_reasoning", "🤔", "Providing comprehensive decision explanations"),
        ("business_impact", "💼", "Analyzing ROI, risks, and business implications"),
        ("educational", "🎓", "Creating adaptive learning content"),
        ("documentation", "📚", "Generating professional documentation")
    ]
    
    for i, (agent_name, emoji, description) in enumerate(test_agents, 1):
        step_logger = logger.bind(
            step_number=i,
            step_name=agent_name,
            agent_type=f"{agent_name.title()}Agent"
        )
        
        step_logger.info(f"{emoji} AGENT EXECUTION START: {agent_name.title()}",
                        conversation_id=workflow_state.conversation_id,
                        step_description=description)
        
        # Simulate some processing time
        await asyncio.sleep(0.1)
        
        execution_time = 0.5 + (i * 0.2)  # Mock execution time
        step_results = {
            "success": True,
            "mock_result_count": i * 2,
            "processing_phase": f"step_{i}"
        }
        
        step_logger.info(f"✅ AGENT EXECUTION COMPLETE: {agent_name.title()}",
                        conversation_id=workflow_state.conversation_id,
                        execution_time_seconds=execution_time,
                        result_summary=step_results)
    
    # Test workflow completion logging
    total_time = sum(0.5 + (i * 0.2) for i in range(1, 9))
    
    completion_logger = logger.bind(
        workflow_execution_id=f"wf_{workflow_state.conversation_id}_{int(datetime.now().timestamp())}"
    )
    
    completion_logger.info("🎉 WORKFLOW EXECUTION COMPLETED SUCCESSFULLY",
                          conversation_id=workflow_state.conversation_id,
                          total_execution_time_seconds=round(total_time, 2),
                          steps_completed=8,
                          execution_breakdown={agent: round(0.5 + (i * 0.2), 2) for i, (agent, _, _) in enumerate(test_agents, 1)},
                          workflow_summary={
                              "total_agents_executed": 8,
                              "longest_step": "documentation",
                              "longest_step_time": round(0.5 + (8 * 0.2), 2),
                              "shortest_step": "orchestrator", 
                              "shortest_step_time": round(0.5 + (1 * 0.2), 2),
                              "average_step_time": round(total_time / 8, 2)
                          })
    
    # Test error logging
    error_logger = logger.bind(
        step_number=9,
        step_name="test_error",
        agent_type="TestAgent"
    )
    
    error_logger.error("💥 WORKFLOW EXECUTION FAILED",
                      error="Mock error for testing",
                      error_type="TestException",
                      conversation_id=workflow_state.conversation_id,
                      current_step="test_error",
                      completed_steps=["orchestrator", "requirements"],
                      failed_after_seconds=5.5)
    
    # Test performance metrics
    logger.info("📊 PERFORMANCE METRICS",
               conversation_id=workflow_state.conversation_id,
               total_requests=1,
               average_response_time=total_time,
               success_rate=1.0,
               agent_performance={
                   "fastest_agent": "orchestrator",
                   "slowest_agent": "documentation",
                   "total_llm_calls": 8
               },
               metric_type="performance_summary")
    
    logger.info("✅ LOGGING TEST COMPLETED SUCCESSFULLY",
               test_duration_seconds=round(total_time + 1, 2),
               total_log_entries=25,
               test_status="passed")
    
    print("\n" + "=" * 80)
    print("✅ LOGGING TEST COMPLETED - Check the output above for structured logs")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_logging())