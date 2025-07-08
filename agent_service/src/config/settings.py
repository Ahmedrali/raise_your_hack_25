from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Application settings
    app_name: str = "Agentic Architect Service"
    version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # External API settings
    groq_api_key: str = "demo-key"
    groq_model: str = "llama-3.3-70b-versatile"
    groq_temperature: float = 0.3
    groq_max_tokens: int = 4000
    groq_rate_limit_per_minute: int = 30
    
    tavily_api_key: str = "demo-key"
    tavily_max_results: int = 10
    tavily_search_depth: str = "advanced"
    
    # Redis settings for state management
    redis_url: str = "redis://localhost:6379/0"
    redis_max_connections: int = 20
    
    # Performance settings
    max_concurrent_workflows: int = 10
    workflow_timeout_seconds: int = 300
    cache_ttl_seconds: int = 3600
    
    # Security settings
    api_key: Optional[str] = None
    allowed_origins: str = "http://localhost:3000,http://localhost:3001"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    # Logging settings
    log_level: str = "INFO"
    log_format: str = "json"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
