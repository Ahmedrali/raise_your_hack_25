"""
Logging configuration for the Agent Service.
Provides structured logging with clear agent execution tracking.
"""

import structlog
import logging
import sys
from typing import Any, Dict
from src.config.settings import settings


def configure_logging():
    """Configure structured logging for the application."""
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper())
    )
    
    # Configure processors based on format setting
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="ISO"),
        _add_agent_context,
        _add_performance_context,
    ]
    
    if settings.log_format.lower() == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.extend([
            structlog.dev.ConsoleRenderer(colors=True),
        ])
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level.upper())
        ),
        cache_logger_on_first_use=True,
    )


def _add_agent_context(logger: Any, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add agent-specific context to log entries."""
    # Add service identification
    event_dict["service"] = "agent-service"
    event_dict["version"] = "1.0.0"
    
    # Add agent execution tracking
    if "agent" in event_dict:
        event_dict["component"] = f"agent.{event_dict['agent']}"
    elif "workflow_execution_id" in event_dict:
        event_dict["component"] = "workflow.orchestrator"
    elif "request_id" in event_dict:
        event_dict["component"] = "api.endpoint"
    else:
        event_dict["component"] = "system"
    
    return event_dict


def _add_performance_context(logger: Any, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add performance tracking context to log entries."""
    # Mark performance-critical events
    if any(key in event_dict for key in ["execution_time_seconds", "total_request_time_seconds"]):
        event_dict["metric_type"] = "performance"
    
    # Mark agent lifecycle events
    if event_dict.get("event", "").startswith(("🚀", "📋", "📝", "🔍", "🏗️", "🤔", "💼", "🎓", "📚", "✅", "💥", "🎉")):
        event_dict["metric_type"] = "agent_lifecycle"
    
    # Mark LLM interaction events
    if event_dict.get("event", "").startswith(("🤖", "❌")):
        event_dict["metric_type"] = "llm_interaction"
    
    return event_dict


def get_logger(name: str = None) -> structlog.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)


# Convenience function for agent execution logging
def log_agent_start(logger: structlog.BoundLogger, agent_name: str, conversation_id: str, description: str = ""):
    """Log the start of agent execution with standard format."""
    logger.info(
        f"🔄 AGENT START: {agent_name}",
        agent=agent_name,
        conversation_id=conversation_id,
        description=description,
        phase="start"
    )


def log_agent_complete(logger: structlog.BoundLogger, agent_name: str, conversation_id: str, 
                      execution_time: float, result_summary: Dict[str, Any] = None):
    """Log the completion of agent execution with standard format."""
    logger.info(
        f"✅ AGENT COMPLETE: {agent_name}",
        agent=agent_name,
        conversation_id=conversation_id,
        execution_time_seconds=execution_time,
        result_summary=result_summary or {},
        phase="complete"
    )


def log_agent_error(logger: structlog.BoundLogger, agent_name: str, conversation_id: str, 
                   error: Exception, execution_time: float = 0):
    """Log agent execution errors with standard format."""
    logger.error(
        f"❌ AGENT ERROR: {agent_name}",
        agent=agent_name,
        conversation_id=conversation_id,
        error=str(error),
        error_type=type(error).__name__,
        execution_time_seconds=execution_time,
        phase="error"
    )


# Performance monitoring helpers
def log_performance_metrics(logger: structlog.BoundLogger, metrics: Dict[str, Any]):
    """Log performance metrics in a standardized format."""
    logger.info(
        "📊 PERFORMANCE METRICS",
        **metrics,
        metric_type="performance_summary"
    )


def log_workflow_summary(logger: structlog.BoundLogger, conversation_id: str, summary: Dict[str, Any]):
    """Log workflow execution summary."""
    logger.info(
        "📋 WORKFLOW SUMMARY",
        conversation_id=conversation_id,
        **summary,
        metric_type="workflow_summary"
    )