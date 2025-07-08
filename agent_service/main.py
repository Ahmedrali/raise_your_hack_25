#!/usr/bin/env python3
"""
Agentic Architect Agent Service
Main entry point for the FastAPI application
"""

import uvicorn
from src.config.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
