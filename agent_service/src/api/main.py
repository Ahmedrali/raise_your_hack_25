from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import structlog
import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any

from src.config.settings import settings
from src.api.routes import router
from src.services.groq_service import GroqService
from src.services.simple_tavily_service import SimpleTavilyService
from src.workflows.sequential_workflow import SequentialWorkflow

# Import and setup enhanced logging
from src.utils.logging_config import configure_logging, get_logger

# Configure structured logging
configure_logging()
logger = get_logger("main")

# Global services
services = {}
workflows = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("🚀 STARTING AGENTIC ARCHITECT AGENT SERVICE",
               service="agent-service",
               version=settings.version,
               debug_mode=settings.debug,
               log_level=settings.log_level)
    
    # Initialize services
    logger.info("🔧 INITIALIZING EXTERNAL SERVICES")
    services["groq"] = GroqService()
    services["tavily"] = SimpleTavilyService()
    
    # Initialize workflows
    logger.info("🔄 INITIALIZING WORKFLOWS")
    workflows["sequential"] = SequentialWorkflow()
    
    # Health check services
    logger.info("🏥 PERFORMING SERVICE HEALTH CHECKS")
    service_statuses = {}
    for name, service in services.items():
        try:
            if hasattr(service, 'health_check'):
                healthy = await service.health_check()
                service_statuses[name] = "healthy" if healthy else "unhealthy"
                logger.info(f"✅ SERVICE HEALTH CHECK: {name}",
                          service_name=name,
                          status="healthy" if healthy else "unhealthy")
            else:
                service_statuses[name] = "no_health_check"
                logger.info(f"⚠️ SERVICE HEALTH CHECK: {name}",
                          service_name=name,
                          status="no_health_check")
        except Exception as e:
            service_statuses[name] = "error"
            logger.error(f"❌ SERVICE HEALTH CHECK FAILED: {name}",
                        service_name=name,
                        error=str(e))
    
    logger.info("🎉 AGENT SERVICE STARTUP COMPLETED",
               total_services=len(services),
               total_workflows=len(workflows),
               service_statuses=service_statuses)
    yield
    
    # Shutdown
    logger.info("🛑 SHUTTING DOWN AGENTIC ARCHITECT AGENT SERVICE")
    # Cleanup services if needed
    services.clear()
    workflows.clear()
    logger.info("✅ AGENT SERVICE SHUTDOWN COMPLETED")

# Create FastAPI application
app = FastAPI(
    title="Agentic Architect Agent Service",
    description="AI Agent Service for Architecture Consulting with Business Intelligence",
    version=settings.version,
    lifespan=lifespan
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routes
app.include_router(router, prefix="/api")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    service_health = {}
    
    for name, service in services.items():
        try:
            if hasattr(service, 'health_check'):
                healthy = await service.health_check()
                service_health[name] = "healthy" if healthy else "unhealthy"
            else:
                service_health[name] = "unknown"
        except Exception as e:
            service_health[name] = f"error: {str(e)}"
    
    workflow_health = {}
    for name, workflow in workflows.items():
        try:
            status = await workflow.get_workflow_status()
            workflow_health[name] = status["status"]
        except Exception as e:
            workflow_health[name] = f"error: {str(e)}"
    
    overall_status = "healthy"
    if any(status != "healthy" for status in service_health.values()):
        overall_status = "degraded"
    if any("error" in str(status) for status in service_health.values()):
        overall_status = "unhealthy"
    
    return {
        "status": overall_status,
        "service": "agentic-architect-agent-service",
        "version": settings.version,
        "services": service_health,
        "workflows": workflow_health,
        "timestamp": asyncio.get_event_loop().time()
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error("Unhandled exception", error=str(exc), path=str(request.url))
    return HTTPException(
        status_code=500,
        detail={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "code": "INTERNAL_ERROR"
        }
    )

# Dependency to get services
async def get_services():
    return services

# Dependency to get workflows
async def get_workflows():
    return workflows

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
