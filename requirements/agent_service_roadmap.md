# 🤖 AGENT_SERVICE_DETAILED_ROADMAP.md
## Python + LangGraph + AI Agent Implementation Guide

---

## 📋 **OVERVIEW**

This roadmap provides complete technical specifications for building the Agentic Architect agent service using Python, LangGraph, and AI orchestration. It includes all workflow implementations, agent specializations, external API integrations, and coordination logic required for autonomous execution.

**Technology Stack**:
- **Runtime**: Python 3.11+ with asyncio
- **Framework**: FastAPI 0.104+ for HTTP endpoints
- **Orchestration**: LangGraph 0.0.40+ for workflow management
- **AI**: Groq API with Llama-3.3-70b model
- **Search**: Tavily API for real-time information retrieval
- **State Management**: Redis for agent coordination
- **Testing**: pytest + pytest-asyncio for comprehensive testing

---

## 🏗️ **COMPLETE PROJECT STRUCTURE**

### **STEP 1: Project Setup & Dependencies**

#### **1.1 Directory Structure**
```
agent_service/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py
│   │   ├── orchestrator.py
│   │   ├── requirements_agent.py
│   │   ├── research_agent.py
│   │   ├── architecture_agent.py
│   │   ├── why_reasoning_agent.py
│   │   ├── business_impact_agent.py
│   │   ├── educational_agent.py
│   │   └── documentation_agent.py
│   ├── workflows/
│   │   ├── __init__.py
│   │   ├── base_workflow.py
│   │   ├── sequential_workflow.py
│   │   ├── parallel_workflow.py
│   │   ├── conditional_workflow.py
│   │   └── iterative_workflow.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── groq_service.py
│   │   ├── tavily_service.py
│   │   ├── coordination_service.py
│   │   └── state_management.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── agent_models.py
│   │   ├── workflow_models.py
│   │   └── response_models.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes.py
│   │   └── middleware.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── logging.py
│   └── utils/
│       ├── __init__.py
│       ├── prompts.py
│       ├── validation.py
│       └── error_handling.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── requirements.txt
├── pyproject.toml
├── docker-compose.yml
└── README.md
```

#### **1.2 Dependencies Configuration**
```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "agentic-architect-service"
version = "1.0.0"
description = "AI Agent Service for Architecture Consulting"
dependencies = [
    "fastapi==0.104.1",
    "uvicorn[standard]==0.24.0",
    "langgraph==0.0.40",
    "langchain==0.0.340",
    "groq==0.4.1",
    "tavily-python==0.3.1",
    "redis==5.0.1",
    "pydantic==2.5.0",
    "pydantic-settings==2.1.0",
    "httpx==0.25.2",
    "tenacity==8.2.3",
    "structlog==23.2.0",
    "prometheus-client==0.19.0",
    "pytest==7.4.3",
    "pytest-asyncio==0.21.1",
    "pytest-cov==4.1.0",
    "black==23.11.0",
    "isort==5.12.0",
    "mypy==1.7.0"
]

[tool.black]
line-length = 88
target-version = ['py311']

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

#### **1.3 Environment Configuration**
```python
# src/config/settings.py
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
    groq_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"
    groq_temperature: float = 0.3
    groq_max_tokens: int = 4000
    groq_rate_limit_per_minute: int = 30
    
    tavily_api_key: str
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
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # Logging settings
    log_level: str = "INFO"
    log_format: str = "json"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

### **STEP 2: Core Models & Data Structures**

#### **2.1 Agent Models**
```python
# src/models/agent_models.py
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union
from enum import Enum
from datetime import datetime

class ExpertiseLevel(str, Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    EXPERT = "EXPERT"

class WorkflowType(str, Enum):
    SEQUENTIAL = "SEQUENTIAL"
    PARALLEL = "PARALLEL"
    CONDITIONAL = "CONDITIONAL"
    ITERATIVE = "ITERATIVE"

class MessageRole(str, Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"

class BusinessContext(BaseModel):
    industry: Optional[str] = None
    company_size: Optional[str] = None
    budget_range: Optional[str] = None
    timeline: Optional[str] = None
    compliance_requirements: List[str] = Field(default_factory=list)
    existing_technologies: List[str] = Field(default_factory=list)

class UserProfile(BaseModel):
    id: str
    email: str
    expertise_level: ExpertiseLevel
    business_role: Optional[str] = None
    business_context: Optional[BusinessContext] = None
    preferences: Dict[str, Any] = Field(default_factory=dict)

class ConversationMessage(BaseModel):
    role: MessageRole
    content: str
    message_type: str = "TEXT"
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime

class AgentRequest(BaseModel):
    type: str  # 'process_conversation', 'generate_architecture', 'analyze_requirements'
    data: Dict[str, Any]
    options: Dict[str, Any] = Field(default_factory=dict)

class DecisionFactor(BaseModel):
    factor: str
    importance: int = Field(ge=1, le=5)
    explanation: str
    business_impact: str

class Tradeoff(BaseModel):
    benefit: str
    cost: str
    impact_level: int = Field(ge=1, le=5)
    quantified_metrics: Dict[str, Any] = Field(default_factory=dict)

class Alternative(BaseModel):
    name: str
    description: str
    pros: List[str]
    cons: List[str]
    viability_score: int = Field(ge=1, le=5)
    use_cases: List[str]

class WhyReasoning(BaseModel):
    decision_factors: List[DecisionFactor]
    tradeoffs: List[Tradeoff]
    alternatives: List[Alternative]
    principles: List[str]
    business_alignment: List[str]
    confidence_level: int = Field(ge=1, le=5)

class ROIAnalysis(BaseModel):
    initial_investment: Dict[str, float]
    ongoing_costs: Dict[str, float]
    expected_benefits: Dict[str, float]
    payback_period_months: int
    net_present_value: float
    confidence_level: int = Field(ge=1, le=5)

class RiskAssessment(BaseModel):
    technical_risks: List[Dict[str, Any]]
    business_risks: List[Dict[str, Any]]
    mitigation_strategies: List[Dict[str, Any]]
    overall_risk_level: int = Field(ge=1, le=5)

class BusinessImpact(BaseModel):
    roi_analysis: ROIAnalysis
    risk_assessment: RiskAssessment
    competitive_advantages: List[str]
    market_positioning: str
    strategic_alignment: str
    success_metrics: List[str]

class ArchitectureComponent(BaseModel):
    id: str
    name: str
    type: str
    description: str
    responsibilities: List[str]
    technologies: List[str]
    scaling_factors: List[str]
    business_value: str

class ArchitectureConnection(BaseModel):
    id: str
    from_component: str
    to_component: str
    type: str
    protocol: str
    description: str
    data_flow: Optional[Dict[str, Any]] = None

class ArchitectureData(BaseModel):
    components: List[ArchitectureComponent]
    connections: List[ArchitectureConnection]
    layers: List[Dict[str, Any]]
    patterns: List[Dict[str, Any]]
    technologies: List[Dict[str, Any]]
    metadata: Dict[str, Any] = Field(default_factory=dict)

class EducationalContent(BaseModel):
    concepts: List[Dict[str, Any]]
    examples: List[Dict[str, Any]]
    exercises: List[Dict[str, Any]]
    resources: List[Dict[str, Any]]
    progress_tracking: Dict[str, Any]
    business_context: Dict[str, Any]

class AgentResponse(BaseModel):
    content: str
    message_type: str
    architecture_update: Optional[ArchitectureData] = None
    why_reasoning: Optional[WhyReasoning] = None
    business_impact: Optional[BusinessImpact] = None
    educational_content: Optional[EducationalContent] = None
    suggested_actions: List[str] = Field(default_factory=list)
    next_questions: List[str] = Field(default_factory=list)
    confidence_score: float = Field(ge=0.0, le=1.0, default=0.8)

class WorkflowState(BaseModel):
    conversation_id: str
    user_query: str
    user_profile: UserProfile
    business_context: Optional[BusinessContext] = None
    orchestrator_plan: Dict[str, Any] = Field(default_factory=dict)
    requirements_analysis: Dict[str, Any] = Field(default_factory=dict)
    research_findings: Dict[str, Any] = Field(default_factory=dict)
    architecture_design: Dict[str, Any] = Field(default_factory=dict)
    why_reasoning: Dict[str, Any] = Field(default_factory=dict)
    business_impact: Dict[str, Any] = Field(default_factory=dict)
    educational_content: Dict[str, Any] = Field(default_factory=dict)
    documentation: Dict[str, Any] = Field(default_factory=dict)
    current_step: str = "orchestrator"
    completed_steps: List[str] = Field(default_factory=list)
    workflow_type: WorkflowType = WorkflowType.SEQUENTIAL
    metadata: Dict[str, Any] = Field(default_factory=dict)
```

### **STEP 3: External Service Integrations**

#### **3.1 Groq API Service**
```python
# src/services/groq_service.py
import asyncio
import time
from typing import Dict, List, Optional, Any
from groq import AsyncGroq
from tenacity import retry, stop_after_attempt, wait_exponential
import structlog
from src.config.settings import settings
from src.utils.error_handling import GroqServiceError

logger = structlog.get_logger()

class GroqService:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.groq_api_key)
        self.model = settings.groq_model
        self.temperature = settings.groq_temperature
        self.max_tokens = settings.groq_max_tokens
        
        # Rate limiting
        self.rate_limiter = RateLimiter(
            max_requests=settings.groq_rate_limit_per_minute,
            time_window=60
        )
        
        # Token usage tracking
        self.total_tokens_used = 0
        self.requests_made = 0

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def query(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Query Groq API with comprehensive error handling and rate limiting.
        """
        await self.rate_limiter.acquire()
        
        try:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})

            logger.info(
                "Making Groq API request",
                model=self.model,
                prompt_length=len(prompt),
                system_message_length=len(system_message) if system_message else 0
            )

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                stream=False
            )

            if not response.choices or not response.choices[0].message:
                raise GroqServiceError("No response content received from Groq")

            content = response.choices[0].message.content
            if not content:
                raise GroqServiceError("Empty response content from Groq")

            # Track usage
            self.requests_made += 1
            if response.usage:
                self.total_tokens_used += response.usage.total_tokens

            logger.info(
                "Groq API request successful",
                response_length=len(content),
                tokens_used=response.usage.total_tokens if response.usage else 0,
                total_requests=self.requests_made
            )

            return content

        except Exception as e:
            logger.error("Groq API request failed", error=str(e))
            raise GroqServiceError(f"Groq API request failed: {str(e)}")

    async def query_with_context(
        self,
        prompt: str,
        conversation_history: List[Dict[str, str]],
        system_message: Optional[str] = None,
        max_context_messages: int = 10
    ) -> str:
        """
        Query with conversation context, managing context window.
        """
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})

        # Add conversation history (limited to prevent context overflow)
        recent_history = conversation_history[-max_context_messages:]
        messages.extend(recent_history)
        
        # Add current prompt
        messages.append({"role": "user", "content": prompt})

        # Estimate token count and truncate if necessary
        estimated_tokens = self._estimate_token_count(messages)
        if estimated_tokens > (self.max_tokens * 0.8):  # Leave room for response
            messages = self._truncate_messages(messages, int(self.max_tokens * 0.6))

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=False
            )

            return response.choices[0].message.content or ""

        except Exception as e:
            logger.error("Groq API context query failed", error=str(e))
            raise GroqServiceError(f"Groq API context query failed: {str(e)}")

    def _estimate_token_count(self, messages: List[Dict[str, str]]) -> int:
        """Rough estimation of token count (4 chars ≈ 1 token for English)."""
        total_chars = sum(len(msg["content"]) for msg in messages)
        return int(total_chars / 4)

    def _truncate_messages(
        self, 
        messages: List[Dict[str, str]], 
        max_tokens: int
    ) -> List[Dict[str, str]]:
        """Truncate messages to fit within token limit."""
        max_chars = max_tokens * 4
        current_chars = 0
        truncated = []
        
        # Always keep system message and last user message
        if messages[0]["role"] == "system":
            truncated.append(messages[0])
            current_chars += len(messages[0]["content"])
            messages = messages[1:]
        
        # Keep the most recent messages
        for msg in reversed(messages):
            msg_chars = len(msg["content"])
            if current_chars + msg_chars > max_chars:
                break
            truncated.insert(-1 if truncated and truncated[-1]["role"] == "user" else len(truncated), msg)
            current_chars += msg_chars
        
        return truncated

    async def health_check(self) -> bool:
        """Check if Groq service is available."""
        try:
            response = await self.query("Hello", max_tokens=10)
            return bool(response and len(response) > 0)
        except Exception:
            return False

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics."""
        return {
            "total_tokens_used": self.total_tokens_used,
            "requests_made": self.requests_made,
            "rate_limit_remaining": self.rate_limiter.get_remaining_quota()
        }

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            now = time.time()
            # Remove old requests outside the time window
            self.requests = [req_time for req_time in self.requests if now - req_time < self.time_window]
            
            if len(self.requests) >= self.max_requests:
                sleep_time = self.time_window - (now - self.requests[0])
                if sleep_time > 0:
                    logger.info(f"Rate limit reached, sleeping for {sleep_time:.2f} seconds")
                    await asyncio.sleep(sleep_time)
                    return await self.acquire()
            
            self.requests.append(now)

    def get_remaining_quota(self) -> int:
        now = time.time()
        recent_requests = [req_time for req_time in self.requests if now - req_time < self.time_window]
        return max(0, self.max_requests - len(recent_requests))
```

#### **3.2 Tavily Search Service**
```python
# src/services/tavily_service.py
import asyncio
from typing import Dict, List, Optional, Any
from tavily import TavilyClient
from tenacity import retry, stop_after_attempt, wait_exponential
import structlog
from src.config.settings import settings
from src.utils.error_handling import TavilyServiceError

logger = structlog.get_logger()

class TavilyService:
    def __init__(self):
        self.client = TavilyClient(api_key=settings.tavily_api_key)
        self.max_results = settings.tavily_max_results
        self.search_depth = settings.tavily_search_depth
        
        # Usage tracking
        self.searches_made = 0
        self.total_results_retrieved = 0

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def search(
        self,
        query: str,
        max_results: Optional[int] = None,
        search_depth: Optional[str] = None,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform comprehensive search with filtering and pagination.
        """
        try:
            logger.info(
                "Performing Tavily search",
                query=query,
                max_results=max_results or self.max_results,
                search_depth=search_depth or self.search_depth
            )

            # Build search parameters
            search_params = {
                "query": query,
                "max_results": max_results or self.max_results,
                "search_depth": search_depth or self.search_depth,
                "include_raw_content": True,
                "include_answer": True
            }

            # Add domain filtering if specified
            if include_domains:
                search_params["include_domains"] = include_domains
            if exclude_domains:
                search_params["exclude_domains"] = exclude_domains

            # Execute search in a thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.client.search(**search_params)
            )

            if not response or "results" not in response:
                raise TavilyServiceError("No results returned from Tavily search")

            results = response["results"]
            
            # Process and enhance results
            processed_results = []
            for result in results:
                processed_result = {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "raw_content": result.get("raw_content", ""),
                    "score": result.get("score", 0.0),
                    "published_date": result.get("published_date"),
                    "domain": self._extract_domain(result.get("url", "")),
                    "content_type": self._classify_content_type(result),
                    "relevance_score": self._calculate_relevance_score(result, query)
                }
                processed_results.append(processed_result)

            # Sort by relevance score
            processed_results.sort(key=lambda x: x["relevance_score"], reverse=True)

            # Update usage statistics
            self.searches_made += 1
            self.total_results_retrieved += len(processed_results)

            logger.info(
                "Tavily search completed",
                results_count=len(processed_results),
                total_searches=self.searches_made
            )

            return processed_results

        except Exception as e:
            logger.error("Tavily search failed", error=str(e), query=query)
            raise TavilyServiceError(f"Tavily search failed: {str(e)}")

    async def search_with_context(
        self,
        query: str,
        business_context: Optional[Dict[str, Any]] = None,
        technical_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Enhanced search with business and technical context.
        """
        # Build context-aware search queries
        search_queries = [query]
        
        if business_context:
            if industry := business_context.get("industry"):
                search_queries.append(f"{query} {industry} industry")
            if company_size := business_context.get("company_size"):
                search_queries.append(f"{query} {company_size} business")

        if technical_context:
            if technologies := technical_context.get("technologies"):
                for tech in technologies[:3]:  # Limit to top 3
                    search_queries.append(f"{query} {tech}")

        # Execute searches concurrently
        search_tasks = [
            self.search(q, max_results=5) for q in search_queries[:4]  # Limit queries
        ]
        
        search_results = await asyncio.gather(*search_tasks, return_exceptions=True)
        
        # Aggregate and deduplicate results
        all_results = []
        seen_urls = set()
        
        for i, results in enumerate(search_results):
            if isinstance(results, Exception):
                logger.warning(f"Search query {i} failed: {results}")
                continue
                
            for result in results:
                url = result.get("url", "")
                if url not in seen_urls:
                    result["search_query"] = search_queries[i]
                    all_results.append(result)
                    seen_urls.add(url)

        # Categorize results
        categorized_results = self._categorize_search_results(all_results)
        
        return {
            "query": query,
            "total_results": len(all_results),
            "categorized_results": categorized_results,
            "business_insights": self._extract_business_insights(all_results, business_context),
            "technical_insights": self._extract_technical_insights(all_results, technical_context),
            "search_metadata": {
                "queries_used": search_queries,
                "search_timestamp": asyncio.get_event_loop().time()
            }
        }

    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except Exception:
            return ""

    def _classify_content_type(self, result: Dict[str, Any]) -> str:
        """Classify content type based on URL and content."""
        url = result.get("url", "").lower()
        title = result.get("title", "").lower()
        
        if any(domain in url for domain in ["github.com", "stackoverflow.com"]):
            return "technical"
        elif any(domain in url for domain in ["forbes.com", "bloomberg.com", "wsj.com"]):
            return "business"
        elif any(word in title for word in ["tutorial", "guide", "how to"]):
            return "educational"
        elif any(word in title for word in ["news", "announces", "releases"]):
            return "news"
        else:
            return "general"

    def _calculate_relevance_score(self, result: Dict[str, Any], query: str) -> float:
        """Calculate relevance score based on multiple factors."""
        score = result.get("score", 0.0)
        
        # Boost score based on content quality indicators
        title = result.get("title", "").lower()
        content = result.get("content", "").lower()
        query_lower = query.lower()
        
        # Title relevance
        if query_lower in title:
            score += 0.2
        
        # Content depth
        if len(content) > 500:
            score += 0.1
        
        # Recent content boost
        if result.get("published_date"):
            # Boost recent content (simplified)
            score += 0.05
        
        # Domain authority boost
        authoritative_domains = [
            "aws.amazon.com", "cloud.google.com", "docs.microsoft.com",
            "martinfowler.com", "highscalability.com", "ieee.org"
        ]
        domain = self._extract_domain(result.get("url", ""))
        if any(auth_domain in domain for auth_domain in authoritative_domains):
            score += 0.15
        
        return min(score, 1.0)

    def _categorize_search_results(self, results: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize search results by type."""
        categories = {
            "technical": [],
            "business": [],
            "educational": [],
            "news": [],
            "general": []
        }
        
        for result in results:
            content_type = result.get("content_type", "general")
            categories[content_type].append(result)
        
        # Sort each category by relevance score
        for category in categories:
            categories[category].sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        return categories

    def _extract_business_insights(
        self, 
        results: List[Dict[str, Any]], 
        business_context: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Extract business-relevant insights from search results."""
        insights = []
        
        for result in results:
            if result.get("content_type") == "business":
                content = result.get("content", "")
                # Simple keyword-based insight extraction
                if any(word in content.lower() for word in ["roi", "cost", "savings", "revenue"]):
                    insights.append(f"Financial insight from {result.get('title', 'Unknown')}")
                if any(word in content.lower() for word in ["competitive", "advantage", "market"]):
                    insights.append(f"Market insight from {result.get('title', 'Unknown')}")
        
        return insights[:5]  # Limit to top 5 insights

    def _extract_technical_insights(
        self, 
        results: List[Dict[str, Any]], 
        technical_context: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Extract technical insights from search results."""
        insights = []
        
        for result in results:
            if result.get("content_type") == "technical":
                content = result.get("content", "")
                # Simple keyword-based insight extraction
                if any(word in content.lower() for word in ["performance", "scalability", "optimization"]):
                    insights.append(f"Performance insight from {result.get('title', 'Unknown')}")
                if any(word in content.lower() for word in ["security", "vulnerability", "compliance"]):
                    insights.append(f"Security insight from {result.get('title', 'Unknown')}")
        
        return insights[:5]  # Limit to top 5 insights

    async def health_check(self) -> bool:
        """Check if Tavily service is available."""
        try:
            results = await self.search("test query", max_results=1)
            return len(results) >= 0  # Even 0 results means service is working
        except Exception:
            return False

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics."""
        return {
            "searches_made": self.searches_made,
            "total_results_retrieved": self.total_results_retrieved,
            "average_results_per_search": (
                self.total_results_retrieved / self.searches_made 
                if self.searches_made > 0 else 0
            )
        }
```

### **STEP 4: Core Agent Implementations**

#### **4.1 Base Agent Class**
```python
# src/agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import structlog
from src.models.agent_models import WorkflowState, UserProfile, BusinessContext
from src.services.groq_service import GroqService
from src.services.tavily_service import TavilyService

logger = structlog.get_logger()

class BaseAgent(ABC):
    """Base class for all specialized agents."""
    
    def __init__(self, name: str):
        self.name = name
        self.groq_service = GroqService()
        self.tavily_service = TavilyService()
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
        context_prompt = self._build_context_prompt(prompt, state)
        system = system_prompt or self.get_system_prompt()
        
        return await self.groq_service.query(
            prompt=context_prompt,
            system_message=system
        )

    def _build_context_prompt(self, prompt: str, state: WorkflowState) -> str:
        """Build comprehensive context prompt."""
        context_parts = [
            f"User Query: {state.user_query}",
            f"User Expertise: {state.user_profile.expertise_level}",
        ]
        
        if state.user_profile.business_role:
            context_parts.append(f"Business Role: {state.user_profile.business_role}")
        
        if state.business_context:
            context_parts.append(f"Business Context: {state.business_context}")
        
        if state.requirements_analysis:
            context_parts.append(f"Requirements: {state.requirements_analysis}")
        
        if state.research_findings:
            context_parts.append(f"Research: {state.research_findings}")
        
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
```

#### **4.2 Orchestrator Agent**
```python
# src/agents/orchestrator.py
from typing import Dict, Any
import json
from src.agents.base_agent import BaseAgent
from src.models.agent_models import WorkflowState, WorkflowType

class OrchestratorAgent(BaseAgent):
    """Orchestrator agent that plans and coordinates workflow execution."""
    
    def __init__(self):
        super().__init__("orchestrator")

    async def process(self, state: WorkflowState) -> Dict[str, Any]:
        """Analyze query and create orchestration plan."""
        self.logger.info("Creating orchestration plan", conversation_id=state.conversation_id)
        
        try:
            orchestration_prompt = self._build_orchestration_prompt(state)
            response = await self.query_groq_with_context(
                orchestration_prompt, 
                state
            )
            
            plan = self._parse_orchestration_response(response)
            
            self.logger.info(
                "Orchestration plan created",
                workflow_type=plan.get("workflow_type"),
                agents_required=len(plan.get("agents_required", []))
            )
            
            return {"orchestrator_plan": plan}
            
        except Exception as e:
            self.logger.error("Orchestration planning failed", error=str(e))
            # Return fallback plan
            return {"orchestrator_plan": self._get_fallback_plan(state)}

    def get_system_prompt(self) -> str:
        return """
You are the Orchestrator Agent for the Agentic Architect platform. Your role is to analyze user queries and create optimal execution plans that coordinate specialized agents to deliver comprehensive architectural guidance with integrated business intelligence.

CORE RESPONSIBILITIES:
1. Analyze query complexity (technical and business)
2. Determine optimal workflow type (sequential/parallel/conditional/iterative)
3. Select required specialized agents
4. Plan integration of why reasoning and business intelligence
5. Estimate processing time and resource requirements

AVAILABLE SPECIALIZED AGENTS:
- Requirements Agent: Analyzes and clarifies architectural requirements
- Research Agent: Gathers current market and technical intelligence
- Architecture Agent: Designs technical solutions and patterns
- Why Reasoning Agent: Provides comprehensive decision explanations
- Business Impact Agent: Analyzes ROI, risks, and business implications
- Educational Agent: Creates adaptive learning content
- Documentation Agent: Generates professional documentation

WORKFLOW TYPES:
1. SEQUENTIAL: Step-by-step for thorough analysis (most common)
2. PARALLEL: Simultaneous processing for urgent decisions
3. CONDITIONAL: Branching logic based on complexity assessment
4. ITERATIVE: Repeated refinement for learning-focused sessions

ORCHESTRATION PRINCIPLES:
- Always include Why Reasoning and Business Impact agents
- Adapt agent selection to user expertise level
- Consider business context in all decisions
- Optimize for both technical accuracy and business value
- Ensure educational value in every interaction

Return your analysis as valid JSON with detailed orchestration plan.
        """

    def _build_orchestration_prompt(self, state: WorkflowState) -> str:
        """Build comprehensive orchestration prompt."""
        base_prompt = f"""
QUERY ANALYSIS REQUEST:
User Query: "{state.user_query}"
User Expertise: {state.user_profile.expertise_level}
Business Role: {state.user_profile.business_role or 'Not specified'}
Business Context: {state.business_context or 'Not provided'}

ORCHESTRATION ANALYSIS REQUIRED:

1. QUERY COMPLEXITY ANALYSIS:
   - Technical complexity level (1-5)
   - Business complexity level (1-5)
   - Required depth of why reasoning
   - Required depth of business analysis
   - Urgency assessment

2. WORKFLOW SELECTION:
   - Choose optimal workflow type (sequential/parallel/conditional/iterative)
   - Justify workflow choice based on complexity analysis
   - Estimate total processing time
   - Identify critical path dependencies

3. AGENT COORDINATION PLAN:
   - Which agents are required for this query?
   - What is the optimal agent execution order?
   - How should agents share context and build on each other?
   - How to integrate why reasoning and business intelligence?

4. USER EXPERIENCE OPTIMIZATION:
   - How to adapt technical explanations to user expertise level?
   - How to adapt business explanations to user role/context?
   - What educational opportunities exist in this query?
   - How to structure response for maximum learning value?

5. SUCCESS CRITERIA:
   - What constitutes a successful response for this query?
   - How to measure user satisfaction and learning?
   - What follow-up questions should be anticipated?
   - How to ensure both technical and business value delivery?

Return detailed orchestration plan as JSON with specific agent instructions and integration requirements.
        """
        
        return self.get_user_adapted_prompt(base_prompt, state.user_profile)

    def _parse_orchestration_response(self, response: str) -> Dict[str, Any]:
        """Parse orchestration response into structured plan."""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                plan = json.loads(json_match.group())
                return self._validate_orchestration_plan(plan)
            else:
                # Fallback parsing
                return self._extract_plan_from_text(response)
        except Exception as e:
            self.logger.warning("Failed to parse orchestration response", error=str(e))
            return self._get_default_plan()

    def _validate_orchestration_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and complete orchestration plan."""
        # Ensure required fields
        plan.setdefault("workflow_type", "SEQUENTIAL")
        plan.setdefault("agents_required", ["requirements", "research", "architecture", "why_reasoning", "business_impact", "educational"])
        plan.setdefault("estimated_duration_minutes", 15)
        plan.setdefault("complexity_score", 3)
        
        # Ensure why reasoning and business impact are always included
        if "why_reasoning" not in plan["agents_required"]:
            plan["agents_required"].append("why_reasoning")
        if "business_impact" not in plan["agents_required"]:
            plan["agents_required"].append("business_impact")
        
        # Validate workflow type
        valid_workflows = ["SEQUENTIAL", "PARALLEL", "CONDITIONAL", "ITERATIVE"]
        if plan["workflow_type"] not in valid_workflows:
            plan["workflow_type"] = "SEQUENTIAL"
        
        return plan

    def _extract_plan_from_text(self, response: str) -> Dict[str, Any]:
        """Extract plan from text response using keywords."""
        workflow_type = "SEQUENTIAL"
        if "parallel" in response.lower():
            workflow_type = "PARALLEL"
        elif "conditional" in response.lower():
            workflow_type = "CONDITIONAL"
        elif "iterative" in response.lower():
            workflow_type = "ITERATIVE"
        
        # Extract mentioned agents
        agent_keywords = {
            "requirements": ["requirements", "requirement"],
            "research": ["research", "search"],
            "architecture": ["architecture", "design"],
            "why_reasoning": ["why", "reasoning", "decision"],
            "business_impact": ["business", "roi", "impact"],
            "educational": ["educational", "learning", "teaching"],
            "documentation": ["documentation", "document"]
        }
        
        agents_required = []
        response_lower = response.lower()
        for agent, keywords in agent_keywords.items():
            if any(keyword in response_lower for keyword in keywords):
                agents_required.append(agent)
        
        # Ensure minimum required agents
        if not agents_required:
            agents_required = ["requirements", "architecture", "why_reasoning", "business_impact"]
        
        return {
            "workflow_type": workflow_type,
            "agents_required": agents_required,
            "estimated_duration_minutes": 15,
            "complexity_score": 3,
            "justification": "Extracted from text analysis"
        }

    def _get_fallback_plan(self, state: WorkflowState) -> Dict[str, Any]:
        """Get fallback orchestration plan."""
        return {
            "workflow_type": "SEQUENTIAL",
            "agents_required": ["requirements", "research", "architecture", "why_reasoning", "business_impact", "educational"],
            "estimated_duration_minutes": 20,
            "complexity_score": 3,
            "justification": "Fallback plan due to orchestration error",
            "integration_requirements": {
                "why_reasoning": "mandatory",
                "business_impact": "mandatory",
                "educational_adaptation": True
            }
        }

    def _get_default_plan(self) -> Dict[str, Any]:
        """Get default orchestration plan."""
        return {
            "workflow_type": "SEQUENTIAL",
            "agents_required": ["requirements", "architecture", "why_reasoning", "business_impact"],
            "estimated_duration_minutes": 15,
            "complexity_score": 2,
            "justification": "Default sequential plan"
        }
```

#### **4.3 Requirements Analysis Agent**
```python
# src/agents/requirements_agent.py
from typing import Dict, Any
import json
from src.agents.base_agent import BaseAgent
from src.models.agent_models import WorkflowState

class RequirementsAgent(BaseAgent):
    """Requirements agent that analyzes and clarifies architectural requirements."""
    
    def __init__(self):
        super().__init__("requirements")

    async def process(self, state: WorkflowState) -> Dict[str, Any]:
        """Analyze requirements with business context."""
        self.logger.info("Analyzing requirements", conversation_id=state.conversation_id)
        
        try:
            requirements_prompt = self._build_requirements_prompt(state)
            response = await self.query_groq_with_context(
                requirements_prompt, 
                state
            )
            
            analysis = self._parse_requirements_response(response)
            
            self.logger.info(
                "Requirements analysis completed",
                functional_requirements=len(analysis.get("functional_requirements", [])),
                non_functional_requirements=len(analysis.get("non_functional_requirements", []))
            )
            
            return {"requirements_analysis": analysis}
            
        except Exception as e:
            self.logger.error("Requirements analysis failed", error=str(e))
            return {"requirements_analysis": self._get_fallback_analysis(state)}

    def get_system_prompt(self) -> str:
        return """
You are the Requirements Analysis Agent for the Agentic Architect platform. Your role is to thoroughly analyze user requirements and translate them into comprehensive architectural specifications with integrated business context.

CORE RESPONSIBILITIES:
1. Extract and clarify functional requirements
2. Identify non-functional requirements (performance, security, scalability)
3. Analyze business requirements and constraints
4. Identify missing or ambiguous requirements
5. Assess technical and business risks
6. Provide requirement prioritization based on business value

ANALYSIS FRAMEWORK:
1. FUNCTIONAL REQUIREMENTS:
   - Core features and capabilities
   - User interactions and workflows
   - Data processing requirements
   - Integration requirements

2. NON-FUNCTIONAL REQUIREMENTS:
   - Performance and scalability targets
   - Security and compliance needs
   - Availability and reliability requirements
   - Maintainability and operability needs

3. BUSINESS REQUIREMENTS:
   - Business objectives and success metrics
   - Budget and timeline constraints
   - Compliance and regulatory requirements
   - Market and competitive considerations

4. CONSTRAINTS AND ASSUMPTIONS:
   - Technology constraints
   - Resource limitations
   - External dependencies
   - Risk factors

REQUIREMENT ANALYSIS PRINCIPLES:
- Ask clarifying questions for ambiguous requirements
- Consider both current and future business needs
- Identify potential conflicts between requirements
- Assess feasibility and implementation complexity
- Connect technical requirements to business value

Return structured JSON with comprehensive requirements analysis and business alignment.
        """

    def _build_requirements_prompt(self, state: WorkflowState) -> str:
        """Build comprehensive requirements analysis prompt."""
        base_prompt = f"""
REQUIREMENTS ANALYSIS REQUEST:
User Query: "{state.user_query}"
Business Context: {state.business_context or 'Not provided'}
User Expertise: {state.user_profile.expertise_level}
Business Role: {state.user_profile.business_role or 'Not specified'}

COMPREHENSIVE REQUIREMENTS ANALYSIS:

1. FUNCTIONAL REQUIREMENTS EXTRACTION:
   - What are the core features and capabilities needed?
   - What user interactions and workflows are required?
   - What data processing and storage requirements exist?
   - What integration points are needed?
   - What business processes must be supported?

2. NON-FUNCTIONAL REQUIREMENTS ANALYSIS:
   - Performance requirements (throughput, latency, concurrency)
   - Scalability requirements (user growth, data growth, transaction volume)
   - Security requirements (authentication, authorization, data protection)
   - Availability and reliability requirements (uptime, disaster recovery)
   - Compliance requirements (regulatory, industry standards)

3. BUSINESS REQUIREMENTS ASSESSMENT:
   - What business objectives does this system support?
   - What are the success metrics and KPIs?
   - What are the budget and timeline constraints?
   - What market or competitive factors influence requirements?
   - What ROI expectations exist?

4. CONSTRAINT AND RISK ANALYSIS:
   - What technology constraints exist?
   - What resource limitations must be considered?
   - What external dependencies exist?
   - What technical and business risks are present?

5. REQUIREMENT PRIORITIZATION:
   - Which requirements are must-have vs nice-to-have?
   - What is the business value of each requirement?
   - What are the implementation complexity and costs?
   - What is the recommended implementation sequence?

6. CLARIFICATION QUESTIONS:
   - What additional information is needed?
   - What assumptions need validation?
   - What potential conflicts or gaps exist?

Return detailed JSON with structured requirements analysis including business impact assessment.
        """
        
        return self.get_user_adapted_prompt(base_prompt, state.user_profile)

    def _parse_requirements_response(self, response: str) -> Dict[str, Any]:
        """Parse requirements response into structured analysis."""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                return self._validate_requirements_analysis(analysis)
            else:
                # Fallback parsing
                return self._extract_requirements_from_text(response)
        except Exception as e:
            self.logger.warning("Failed to parse requirements response", error=str(e))
            return self._get_default_analysis()

    def _validate_requirements_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and complete requirements analysis."""
        # Ensure required fields
        analysis.setdefault("functional_requirements", [])
        analysis.setdefault("non_functional_requirements", [])
        analysis.setdefault("business_requirements", [])
        analysis.setdefault("constraints", [])
        analysis.setdefault("risks", [])
        analysis.setdefault("clarification_questions", [])
        analysis.setdefault("priority_matrix", {})
        
        # Validate structure
        if not isinstance(analysis["functional_requirements"], list):
            analysis["functional_requirements"] = []
        if not isinstance(analysis["non_functional_requirements"], list):
            analysis["non_functional_requirements"] = []
        
        return analysis

    def _extract_requirements_from_text(self, response: str) -> Dict[str, Any]:
        """Extract requirements from text response."""
        lines = response.split('\n')
        
        functional_reqs = []
        non_functional_reqs = []
        business_reqs = []
        questions = []
        
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            line_lower = line.lower()
            if 'functional' in line_lower and 'requirement' in line_lower:
                current_section = 'functional'
            elif 'non-functional' in line_lower or 'performance' in line_lower:
                current_section = 'non_functional'
            elif 'business' in line_lower and 'requirement' in line_lower:
                current_section = 'business'
            elif 'question' in line_lower or 'clarification' in line_lower:
                current_section = 'questions'
            elif line.startswith('- ') or line.startswith('* '):
                requirement = line[2:].strip()
                if current_section == 'functional':
                    functional_reqs.append(requirement)
                elif current_section == 'non_functional':
                    non_functional_reqs.append(requirement)
                elif current_section == 'business':
                    business_reqs.append(requirement)
                elif current_section == 'questions':
                    questions.append(requirement)
        
        return {
            "functional_requirements": functional_reqs,
            "non_functional_requirements": non_functional_reqs,
            "business_requirements": business_reqs,
            "constraints": [],
            "risks": [],
            "clarification_questions": questions,
            "priority_matrix": {}
        }

    def _get_fallback_analysis(self, state: WorkflowState) -> Dict[str, Any]:
        """Get fallback requirements analysis."""
        return {
            "functional_requirements": [
                "Core system functionality as described in user query",
                "User interface for interaction",
                "Data persistence capabilities"
            ],
            "non_functional_requirements": [
                "System performance and responsiveness",
                "Security and data protection",
                "Scalability for future growth"
            ],
            "business_requirements": [
                "Alignment with business objectives",
                "Cost-effective implementation",
                "Timely delivery"
            ],
            "constraints": [
                "Budget limitations",
                "Timeline constraints",
                "Technology stack preferences"
            ],
            "risks": [
                "Technical implementation complexity",
                "Integration challenges",
                "Performance bottlenecks"
            ],
            "clarification_questions": [
                "What is the expected user load?",
                "What are the performance requirements?",
                "What integrations are needed?"
            ],
            "priority_matrix": {
                "high": ["Core functionality", "Security"],
                "medium": ["Performance optimization", "Integrations"],
                "low": ["Advanced features", "UI enhancements"]
            }
        }

    def _get_default_analysis(self) -> Dict[str, Any]:
        """Get default requirements analysis."""
        return {
            "functional_requirements": ["Basic system functionality"],
            "non_functional_requirements": ["Performance", "Security"],
            "business_requirements": ["Business value delivery"],
            "constraints": ["Resource limitations"],
            "risks": ["Implementation complexity"],
            "clarification_questions": ["Need more details"],
            "priority_matrix": {}
        }
```

### **STEP 5: LangGraph Workflow Implementations**

#### **5.1 Base Workflow Class**
```python
# src/workflows/base_workflow.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from langgraph.graph import StateGraph, START, END
import structlog
from src.models.agent_models import WorkflowState

logger = structlog.get_logger()

class BaseWorkflow(ABC):
    """Base class for all workflow implementations."""
    
    def __init__(self, name: str):
        self.name = name
        self.graph = None
        self.logger = logger.bind(workflow=name)

    @abstractmethod
    async def build_graph(self) -> StateGraph:
        """Build the workflow graph."""
        pass

    @abstractmethod
    async def execute(self, initial_state: WorkflowState) -> Dict[str, Any]:
        """Execute the workflow with the given initial state."""
        pass

    def validate_state(self, state: WorkflowState) -> bool:
        """Validate workflow state."""
        required_fields = ["conversation_id", "user_query", "user_profile"]
        return all(hasattr(state, field) and getattr(state, field) for field in required_fields)

    async def get_workflow_status(self) -> Dict[str, Any]:
        """Get workflow status and health."""
        return {
            "workflow": self.name,
            "status": "healthy" if self.graph else "not_initialized",
            "graph_nodes": len(self.graph.nodes) if self.graph else 0
        }
```

#### **5.2 Sequential Workflow Implementation**
```python
# src/workflows/sequential_workflow.py
from typing import Dict, Any
from langgraph.graph import StateGraph, START, END
from src.workflows.base_workflow import BaseWorkflow
from src.models.agent_models import WorkflowState
from src.agents.orchestrator import OrchestratorAgent
from src.agents.requirements_agent import RequirementsAgent
from src.agents.research_agent import ResearchAgent
from src.agents.architecture_agent import ArchitectureAgent
from src.agents.why_reasoning_agent import WhyReasoningAgent
from src.agents.business_impact_agent import BusinessImpactAgent
from src.agents.educational_agent import EducationalAgent
from src.agents.documentation_agent import DocumentationAgent

class SequentialWorkflow(BaseWorkflow):
    """Sequential workflow for thorough step-by-step analysis."""
    
    def __init__(self):
        super().__init__("sequential")
        self.agents = {
            "orchestrator": OrchestratorAgent(),
            "requirements": RequirementsAgent(),
            "research": ResearchAgent(),
            "architecture": ArchitectureAgent(),
            "why_reasoning": WhyReasoningAgent(),
            "business_impact": BusinessImpactAgent(),
            "educational": EducationalAgent(),
            "documentation": DocumentationAgent()
        }

    async def build_graph(self) -> StateGraph:
        """Build sequential workflow graph."""
        from langgraph.graph import StateGraph
        
        # Define state graph
        workflow = StateGraph(WorkflowState)
        
        # Add nodes for each agent
        workflow.add_node("orchestrator", self._orchestrator_node)
        workflow.add_node("requirements", self._requirements_node)
        workflow.add_node("research", self._research_node)
        workflow.add_node("architecture", self._architecture_node)
        workflow.add_node("why_reasoning", self._why_reasoning_node)
        workflow.add_node("business_impact", self._business_impact_node)
        workflow.add_node("educational", self._educational_node)
        workflow.add_node("documentation", self._documentation_node)
        
        # Define sequential edges
        workflow.add_edge(START, "orchestrator")
        workflow.add_edge("orchestrator", "requirements")
        workflow.add_edge("requirements", "research")
        workflow.add_edge("research", "architecture")
        workflow.add_edge("architecture", "why_reasoning")
        workflow.add_edge("why_reasoning", "business_impact")
        workflow.add_edge("business_impact", "educational")
        workflow.add_edge("educational", "documentation")
        workflow.add_edge("documentation", END)
        
        self.graph = workflow.compile()
        return self.graph

    async def execute(self, initial_state: WorkflowState) -> Dict[str, Any]:
        """Execute sequential workflow."""
        if not self.validate_state(initial_state):
            raise ValueError("Invalid initial state for sequential workflow")
        
        self.logger.info("Starting sequential workflow execution", 
                        conversation_id=initial_state.conversation_id)
        
        try:
            if not self.graph:
                await self.build_graph()
            
            # Execute workflow
            result = await self.graph.ainvoke(initial_state)
            
            # Compile final response
            final_response = self._compile_final_response(result)
            
            self.logger.info("Sequential workflow completed successfully",
                           conversation_id=initial_state.conversation_id)
            
            return final_response
            
        except Exception as e:
            self.logger.error("Sequential workflow execution failed", 
                            error=str(e), conversation_id=initial_state.conversation_id)
            raise

    # Node implementations
    async def _orchestrator_node(self, state: WorkflowState) -> WorkflowState:
        """Execute orchestrator agent."""
        try:
            result = await self.agents["orchestrator"].process(state)
            state.orchestrator_plan = result.get("orchestrator_plan", {})
            state.completed_steps.append("orchestrator")
            state.current_step = "requirements"
            return state
        except Exception as e:
            self.logger.error("Orchestrator node failed", error=str(e))
            # Continue with fallback plan
            state.orchestrator_plan = {"workflow_type": "SEQUENTIAL", "agents_required": ["requirements", "architecture"]}
            state.completed_steps.append("orchestrator")
            state.current_step = "requirements"
            return state

    async def _requirements_node(self, state: WorkflowState) -> WorkflowState:
        """Execute requirements agent."""
        try:
            result = await self.agents["requirements"].process(state)
            state.requirements_analysis = result.get("requirements_analysis", {})
            state.completed_steps.append("requirements")
            state.current_step = "research"
            return state
        except Exception as e:
            self.logger.error("Requirements node failed", error=str(e))
            state.requirements_analysis = {"error": str(e)}
            state.completed_steps.append("requirements")
            state.current_step = "research"
            return state

    async def _research_node(self, state: WorkflowState) -> WorkflowState:
        """Execute research agent."""
        try:
            result = await self.agents["research"].process(state)
            state.research_findings = result.get("research_findings", {})
            state.completed_steps.append("research")
            state.current_step = "architecture"
            return state
        except Exception as e:
            self.logger.error("Research node failed", error=str(e))
            state.research_findings = {"error": str(e)}
            state.completed_steps.append("research")
            state.current_step = "architecture"
            return state

    async def _architecture_node(self, state: WorkflowState) -> WorkflowState:
        """Execute architecture agent."""
        try:
            result = await self.agents["architecture"].process(state)
            state.architecture_design = result.get("architecture_design", {})
            state.completed_steps.append("architecture")
            state.current_step = "why_reasoning"
            return state
        except Exception as e:
            self.logger.error("Architecture node failed", error=str(e))
            state.architecture_design = {"error": str(e)}
            state.completed_steps.append("architecture")
            state.current_step = "why_reasoning"
            return state

    async def _why_reasoning_node(self, state: WorkflowState) -> WorkflowState:
        """Execute why reasoning agent."""
        try:
            result = await self.agents["why_reasoning"].process(state)
            state.why_reasoning = result.get("why_reasoning", {})
            state.completed_steps.append("why_reasoning")
            state.current_step = "business_impact"
            return state
        except Exception as e:
            self.logger.error("Why reasoning node failed", error=str(e))
            state.why_reasoning = {"error": str(e)}
            state.completed_steps.append("why_reasoning")
            state.current_step = "business_impact"
            return state

    async def _business_impact_node(self, state: WorkflowState) -> WorkflowState:
        """Execute business impact agent."""
        try:
            result = await self.agents["business_impact"].process(state)
            state.business_impact = result.get("business_impact", {})
            state.completed_steps.append("business_impact")
            state.current_step = "educational"
            return state
        except Exception as e:
            self.logger.error("Business impact node failed", error=str(e))
            state.business_impact = {"error": str(e)}
            state.completed_steps.append("business_impact")
            state.current_step = "educational"
            return state

    async def _educational_node(self, state: WorkflowState) -> WorkflowState:
        """Execute educational agent."""
        try:
            result = await self.agents["educational"].process(state)
            state.educational_content = result.get("educational_content", {})
            state.completed_steps.append("educational")
            state.current_step = "documentation"
            return state
        except Exception as e:
            self.logger.error("Educational node failed", error=str(e))
            state.educational_content = {"error": str(e)}
            state.completed_steps.append("educational")
            state.current_step = "documentation"
            return state

    async def _documentation_node(self, state: WorkflowState) -> WorkflowState:
        """Execute documentation agent."""
        try:
            result = await self.agents["documentation"].process(state)
            state.documentation = result.get("documentation", {})
            state.completed_steps.append("documentation")
            state.current_step = "completed"
            return state
        except Exception as e:
            self.logger.error("Documentation node failed", error=str(e))
            state.documentation = {"error": str(e)}
            state.completed_steps.append("documentation")
            state.current_step = "completed"
            return state

    def _compile_final_response(self, state: WorkflowState) -> Dict[str, Any]:
        """Compile final response from workflow state."""
        return {
            "success": True,
            "workflow_type": "SEQUENTIAL",
            "conversation_id": state.conversation_id,
            "orchestrator_plan": state.orchestrator_plan,
            "requirements_analysis": state.requirements_analysis,
            "research_findings": state.research_findings,
            "architecture_design": state.architecture_design,
            "why_reasoning": state.why_reasoning,
            "business_impact": state.business_impact,
            "educational_content": state.educational_content,
            "documentation": state.documentation,
            "completed_steps": state.completed_steps,
            "metadata": {
                "workflow_completed": True,
                "total_steps": len(state.completed_steps),
                "final_step": state.current_step
            }
        }
```

### **STEP 6: FastAPI Application Setup**

#### **6.1 Main Application**
```python
# src/api/main.py
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import structlog
import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any

from src.config.settings import settings
from src.api.routes import router
from src.api.middleware import setup_middleware
from src.services.groq_service import GroqService
from src.services.tavily_service import TavilyService
from src.workflows.sequential_workflow import SequentialWorkflow
from src.workflows.parallel_workflow import ParallelWorkflow
from src.workflows.conditional_workflow import ConditionalWorkflow
from src.workflows.iterative_workflow import IterativeWorkflow

# Setup structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.dev.ConsoleRenderer() if settings.debug else structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Global services
services = {}
workflows = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Agentic Architect Agent Service")
    
    # Initialize services
    services["groq"] = GroqService()
    services["tavily"] = TavilyService()
    
    # Initialize workflows
    workflows["sequential"] = SequentialWorkflow()
    workflows["parallel"] = ParallelWorkflow()
    workflows["conditional"] = ConditionalWorkflow()
    workflows["iterative"] = IterativeWorkflow()
    
    # Build workflow graphs
    for name, workflow in workflows.items():
        try:
            await workflow.build_graph()
            logger.info(f"Workflow {name} initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize workflow {name}", error=str(e))
    
    # Health check services
    for name, service in services.items():
        try:
            if hasattr(service, 'health_check'):
                healthy = await service.health_check()
                logger.info(f"Service {name} health check", healthy=healthy)
        except Exception as e:
            logger.warning(f"Service {name} health check failed", error=str(e))
    
    logger.info("Agent service startup completed")
    yield
    
    # Shutdown
    logger.info("Shutting down Agentic Architect Agent Service")
    # Cleanup services if needed
    services.clear()
    workflows.clear()

# Create FastAPI application
app = FastAPI(
    title="Agentic Architect Agent Service",
    description="AI Agent Service for Architecture Consulting with Business Intelligence",
    version=settings.version,
    lifespan=lifespan
)

# Setup middleware
setup_middleware(app)

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
```

### **STEP 7: API Routes Implementation**

#### **7.1 Agent Processing Routes**
```python
# src/api/routes.py
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
from src.workflows.parallel_workflow import ParallelWorkflow
from src.workflows.conditional_workflow import ConditionalWorkflow
from src.workflows.iterative_workflow import IterativeWorkflow

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
    data: Optional[AgentResponse] = None
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
            WorkflowType.PARALLEL: ParallelWorkflow(),
            WorkflowType.CONDITIONAL: ConditionalWorkflow(),
            WorkflowType.ITERATIVE: IterativeWorkflow()
        }
        
        # Build graphs if not already built
        for wf_type, workflow in workflows.items():
            if not workflow.graph:
                await workflow.build_graph()
    
    return workflows.get(workflow_type)

@router.post("/agent/process", response_model=ProcessConversationResponse)
async def process_conversation(request: ProcessConversationRequest):
    """Main endpoint for processing conversation requests with AI agents."""
    logger.info(
        "Processing conversation request",
        conversation_id=request.conversation_id,
        workflow_type=request.workflow_type,
        user_expertise=request.user_profile.expertise_level
    )
    
    try:
        # Build workflow state from request
        workflow_state = WorkflowState(
            conversation_id=request.conversation_id,
            user_query=request.user_message or "Continue conversation",
            user_profile=request.user_profile,
            business_context=request.business_context,
            workflow_type=request.workflow_type,
            metadata={
                "conversation_history": request.conversation_history,
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
        agent_response = AgentResponse(
            content=result.get("final_content", "Analysis completed successfully"),
            message_type="ARCHITECTURE_ANALYSIS",
            architecture_update=result.get("architecture_design"),
            why_reasoning=result.get("why_reasoning"),
            business_impact=result.get("business_impact"),
            educational_content=result.get("educational_content"),
            suggested_actions=result.get("suggested_actions", []),
            next_questions=result.get("next_questions", []),
            confidence_score=result.get("confidence_score", 0.8)
        )
        
        logger.info(
            "Conversation processing completed",
            conversation_id=request.conversation_id,
            execution_time=execution_time,
            workflow_type=request.workflow_type
        )
        
        return ProcessConversationResponse(
            success=True,
            data=agent_response,
            metadata={
                "execution_time_seconds": execution_time,
                "workflow_type": request.workflow_type.value,
                "agents_used": result.get("completed_steps", []),
                "processing_metadata": result.get("metadata", {})
            }
        )
        
    except Exception as e:
        logger.error(
            "Conversation processing failed",
            conversation_id=request.conversation_id,
            error=str(e)
        )
        
        return ProcessConversationResponse(
            success=False,
            error={
                "code": "PROCESSING_FAILED",
                "message": str(e),
                "conversation_id": request.conversation_id
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
    
    for workflow_type in WorkflowType:
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
    
    agents = {
        "orchestrator": OrchestratorAgent(),
        "requirements": RequirementsAgent(),
        "research": ResearchAgent(),
        "architecture": ArchitectureAgent(),
        "why_reasoning": WhyReasoningAgent(),
        "business_impact": BusinessImpactAgent(),
        "educational": EducationalAgent()
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
        "timestamp": datetime.utcnow().isoformat()
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
    
### **STEP 8: Remaining Specialized Agent Implementations**

#### **8.1 Research Agent**
```python
# src/agents/research_agent.py
from typing import Dict, Any, List
import json
import asyncio
from src.agents.base_agent import BaseAgent
from src.models.agent_models import WorkflowState

class ResearchAgent(BaseAgent):
    """Research agent that gathers current market and technical intelligence."""
    
    def __init__(self):
        super().__init__("research")

    async def process(self, state: WorkflowState) -> Dict[str, Any]:
        """Conduct comprehensive research with business context."""
        self.logger.info("Starting research process", conversation_id=state.conversation_id)
        
        try:
            research_tasks = await self._plan_research_tasks(state)
            research_results = await self._execute_research_tasks(research_tasks, state)
            analyzed_findings = await self._analyze_research_results(research_results, state)
            
            self.logger.info(
                "Research completed",
                total_sources=len(research_results.get("sources", [])),
                technical_insights=len(analyzed_findings.get("technical_insights", [])),
                business_insights=len(analyzed_findings.get("business_insights", []))
            )
            
            return {"research_findings": analyzed_findings}
            
        except Exception as e:
            self.logger.error("Research process failed", error=str(e))
            return {"research_findings": self._get_fallback_research(state)}

    def get_system_prompt(self) -> str:
        return """
You are the Research Agent for the Agentic Architect platform. Your role is to gather comprehensive, current market and technical intelligence to inform architectural decisions with strong business context.

CORE RESPONSIBILITIES:
1. Conduct targeted technical research on architectural patterns and technologies
2. Gather business intelligence on market trends and competitive landscape  
3. Identify current best practices and emerging technologies
4. Analyze cost, performance, and business impact data
5. Synthesize findings into actionable architectural insights

RESEARCH METHODOLOGY:
1. TECHNICAL RESEARCH:
   - Current architectural patterns and their adoption
   - Technology performance benchmarks and comparisons
   - Security considerations and compliance requirements
   - Scalability patterns and real-world case studies
   - Integration challenges and solutions

2. BUSINESS RESEARCH:
   - Market trends and competitive analysis
   - Cost analysis and ROI data
   - Industry-specific requirements and constraints
   - Vendor landscape and technology partnerships
   - Implementation timeline and resource requirements

3. SYNTHESIS AND ANALYSIS:
   - Connect technical capabilities to business outcomes
   - Identify technology risks and mitigation strategies
   - Recommend implementation priorities based on business value
   - Provide evidence-based decision support

RESEARCH PRINCIPLES:
- Prioritize recent, authoritative sources
- Focus on real-world implementations and case studies
- Include quantitative data where available
- Consider both technical and business perspectives
- Validate information across multiple sources

Return comprehensive research findings with clear business implications and actionable insights.
        """

    async def _plan_research_tasks(self, state: WorkflowState) -> List[Dict[str, Any]]:
        """Plan research tasks based on requirements and context."""
        planning_prompt = f"""
Based on the user query: "{state.user_query}"
Requirements analysis: {state.requirements_analysis}
Business context: {state.business_context}

Plan comprehensive research tasks that will provide both technical and business intelligence.

Research areas to cover:
1. Technical architecture patterns
2. Technology stack evaluation
3. Performance and scalability data
4. Security and compliance considerations
5. Cost analysis and business impact
6. Competitive landscape analysis
7. Implementation case studies

Return JSON array of research tasks with specific search queries and focus areas.
        """
        
        response = await self.query_groq_with_context(planning_prompt, state)
        
        try:
            tasks = json.loads(response) if response.startswith('[') else []
            return tasks if tasks else self._get_default_research_tasks(state)
        except:
            return self._get_default_research_tasks(state)

    async def _execute_research_tasks(self, tasks: List[Dict[str, Any]], state: WorkflowState) -> Dict[str, Any]:
        """Execute research tasks using Tavily search."""
        all_results = []
        technical_results = []
        business_results = []
        
        # Execute searches concurrently but with rate limiting
        semaphore = asyncio.Semaphore(3)  # Limit concurrent searches
        
        async def execute_single_task(task):
            async with semaphore:
                try:
                    query = task.get("query", "")
                    search_type = task.get("type", "general")
                    
                    if search_type == "business":
                        results = await self.tavily_service.search_with_context(
                            query,
                            business_context=state.business_context.__dict__ if state.business_context else None
                        )
                        business_results.extend(results.get("categorized_results", {}).get("business", []))
                    else:
                        results = await self.tavily_service.search(
                            query,
                            max_results=5
                        )
                        technical_results.extend(results)
                    
                    return {
                        "task": task,
                        "results": results,
                        "success": True
                    }
                except Exception as e:
                    self.logger.warning(f"Research task failed: {e}", task=task)
                    return {
                        "task": task,
                        "error": str(e),
                        "success": False
                    }
        
        # Execute all tasks
        task_results = await asyncio.gather(
            *[execute_single_task(task) for task in tasks],
            return_exceptions=True
        )
        
        # Compile results
        successful_tasks = [r for r in task_results if isinstance(r, dict) and r.get("success")]
        
        return {
            "tasks_executed": len(tasks),
            "successful_tasks": len(successful_tasks),
            "technical_sources": technical_results,
            "business_sources": business_results,
            "task_results": successful_tasks
        }

    async def _analyze_research_results(self, research_results: Dict[str, Any], state: WorkflowState) -> Dict[str, Any]:
        """Analyze research results and synthesize insights."""
        analysis_prompt = f"""
Analyze the following research results and synthesize key insights for architectural decision-making:

Technical Sources: {len(research_results.get('technical_sources', []))} sources
Business Sources: {len(research_results.get('business_sources', []))} sources

User Context:
- Query: {state.user_query}
- Expertise: {state.user_profile.expertise_level}
- Business Role: {state.user_profile.business_role}
- Requirements: {state.requirements_analysis}

Provide analysis in the following areas:
1. Technical insights and recommendations
2. Business implications and opportunities
3. Risk assessment and mitigation strategies
4. Cost-benefit analysis
5. Implementation priorities
6. Competitive intelligence
7. Technology roadmap recommendations

Focus on actionable insights that connect technical capabilities to business outcomes.
Return structured JSON with detailed analysis.
        """
        
        response = await self.query_groq_with_context(analysis_prompt, state)
        
        try:
            analysis = json.loads(response) if response.startswith('{') else {}
            return self._validate_research_analysis(analysis, research_results)
        except:
            return self._get_fallback_analysis(research_results)

    def _get_default_research_tasks(self, state: WorkflowState) -> List[Dict[str, Any]]:
        """Get default research tasks when planning fails."""
        return [
            {"query": f"{state.user_query} architecture patterns", "type": "technical"},
            {"query": f"{state.user_query} best practices", "type": "technical"},
            {"query": f"{state.user_query} performance benchmarks", "type": "technical"},
            {"query": f"{state.user_query} business case ROI", "type": "business"},
            {"query": f"{state.user_query} market trends", "type": "business"}
        ]

    def _validate_research_analysis(self, analysis: Dict[str, Any], research_results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and enhance research analysis."""
        analysis.setdefault("technical_insights", [])
        analysis.setdefault("business_insights", [])
        analysis.setdefault("risk_assessment", {})
        analysis.setdefault("cost_analysis", {})
        analysis.setdefault("recommendations", [])
        analysis.setdefault("competitive_intelligence", {})
        analysis.setdefault("sources_analyzed", research_results.get("tasks_executed", 0))
        
        return analysis

    def _get_fallback_research(self, state: WorkflowState) -> Dict[str, Any]:
        """Get fallback research when process fails."""
        return {
            "technical_insights": [
                "Consider current architectural best practices",
                "Evaluate scalability and performance requirements",
                "Review security and compliance needs"
            ],
            "business_insights": [
                "Assess total cost of ownership",
                "Consider time-to-market implications",
                "Evaluate competitive positioning"
            ],
            "risk_assessment": {
                "technical_risks": ["Implementation complexity", "Technology maturity"],
                "business_risks": ["Budget overrun", "Timeline delays"],
                "mitigation_strategies": ["Phased implementation", "Proof of concept"]
            },
            "recommendations": [
                "Start with MVP implementation",
                "Focus on core business value",
                "Plan for iterative improvement"
            ],
            "sources_analyzed": 0,
            "fallback": True
        }

    def _get_fallback_analysis(self, research_results: Dict[str, Any]) -> Dict[str, Any]:
        """Get fallback analysis when parsing fails."""
        return {
            "technical_insights": ["Research data available but analysis failed"],
            "business_insights": ["Business context available but synthesis failed"],
            "risk_assessment": {"note": "Manual analysis required"},
            "sources_analyzed": research_results.get("tasks_executed", 0),
            "analysis_failed": True
        }
```

#### **8.2 Architecture Agent**
```python
# src/agents/architecture_agent.py
from typing import Dict, Any, List
import json
from src.agents.base_agent import BaseAgent
from src.models.agent_models import WorkflowState, ArchitectureData, ArchitectureComponent, ArchitectureConnection

class ArchitectureAgent(BaseAgent):
    """Architecture agent that designs technical solutions and patterns."""
    
    def __init__(self):
        super().__init__("architecture")

    async def process(self, state: WorkflowState) -> Dict[str, Any]:
        """Design comprehensive architecture with business alignment."""
        self.logger.info("Starting architecture design", conversation_id=state.conversation_id)
        
        try:
            design_approach = await self._determine_design_approach(state)
            architecture_design = await self._create_architecture_design(state, design_approach)
            validated_design = await self._validate_architecture_design(architecture_design, state)
            
            self.logger.info(
                "Architecture design completed",
                components=len(validated_design.get("components", [])),
                connections=len(validated_design.get("connections", [])),
                patterns=len(validated_design.get("patterns", []))
            )
            
            return {"architecture_design": validated_design}
            
        except Exception as e:
            self.logger.error("Architecture design failed", error=str(e))
            return {"architecture_design": self._get_fallback_architecture(state)}

    def get_system_prompt(self) -> str:
        return """
You are the Architecture Agent for the Agentic Architect platform. Your role is to design comprehensive, scalable, and business-aligned technical architectures based on requirements and research findings.

CORE RESPONSIBILITIES:
1. Design complete system architectures with all components and connections
2. Select appropriate architectural patterns and design principles
3. Specify technology stacks and integration approaches
4. Ensure scalability, security, and performance requirements are met
5. Align technical decisions with business objectives and constraints

ARCHITECTURE DESIGN PRINCIPLES:
1. BUSINESS ALIGNMENT:
   - Every component must have clear business value
   - Technology choices must support business objectives
   - Cost and complexity must be justified by business benefits
   - Implementation approach must fit business timeline and resources

2. TECHNICAL EXCELLENCE:
   - Follow established architectural patterns and best practices
   - Ensure separation of concerns and loose coupling
   - Design for scalability, reliability, and maintainability
   - Include comprehensive security and compliance considerations

3. PRACTICAL IMPLEMENTATION:
   - Consider team skills and organizational capabilities
   - Provide clear technology stack recommendations
   - Include migration and deployment strategies
   - Plan for monitoring, testing, and operations

ARCHITECTURE COMPONENTS:
- System components with clear responsibilities
- Data flow and integration patterns
- Security and compliance layers
- Scalability and performance optimizations
- Monitoring and observability features
- Deployment and operational considerations

Return complete architecture specification with detailed component descriptions, connections, and business justifications.
        """

    async def _determine_design_approach(self, state: WorkflowState) -> Dict[str, Any]:
        """Determine the architectural design approach based on context."""
        approach_prompt = f"""
Based on the requirements analysis and research findings, determine the optimal architectural design approach:

Requirements: {state.requirements_analysis}
Research Findings: {state.research_findings}
Business Context: {state.business_context}
User Expertise: {state.user_profile.expertise_level}

Consider:
1. Architectural style (monolithic, microservices, serverless, hybrid)
2. Technology stack preferences and constraints
3. Scalability and performance requirements
4. Security and compliance needs
5. Business timeline and budget constraints
6. Team capabilities and organizational factors

Recommend the most appropriate design approach with justification.
Return JSON with approach recommendations and reasoning.
        """
        
        response = await self.query_groq_with_context(approach_prompt, state)
        
        try:
            approach = json.loads(response) if response.startswith('{') else {}
            return self._validate_design_approach(approach)
        except:
            return self._get_default_design_approach()

    async def _create_architecture_design(self, state: WorkflowState, approach: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed architecture design."""
        design_prompt = f"""
Create a comprehensive architecture design based on:

Requirements: {state.requirements_analysis}
Research Findings: {state.research_findings}
Design Approach: {approach}
Business Context: {state.business_context}

Generate a complete architecture specification including:

1. SYSTEM COMPONENTS:
   - Core application components with responsibilities
   - Data storage and management components
   - Integration and communication components
   - Security and authentication components
   - Monitoring and observability components

2. COMPONENT CONNECTIONS:
   - Data flow between components
   - API and service communication patterns
   - Integration protocols and mechanisms
   - Security boundaries and access controls

3. ARCHITECTURAL PATTERNS:
   - Design patterns applied (MVC, Repository, Factory, etc.)
   - Integration patterns (API Gateway, Message Queue, etc.)
   - Data patterns (CQRS, Event Sourcing, etc.)
   - Security patterns (OAuth, JWT, Zero Trust, etc.)

4. TECHNOLOGY STACK:
   - Programming languages and frameworks
   - Databases and data storage solutions
   - Infrastructure and deployment platforms
   - Third-party services and integrations

5. BUSINESS JUSTIFICATION:
   - How each component delivers business value
   - Cost-benefit analysis for technology choices
   - Risk mitigation through architectural decisions
   - Alignment with business objectives and constraints

Return detailed JSON architecture specification with complete component and connection definitions.
        """
        
        response = await self.query_groq_with_context(design_prompt, state)
        
        try:
            design = json.loads(response) if response.startswith('{') else {}
            return self._enhance_architecture_design(design, state)
        except:
            return self._get_fallback_design(state)

    async def _validate_architecture_design(self, design: Dict[str, Any], state: WorkflowState) -> Dict[str, Any]:
        """Validate architecture design against requirements."""
        validation_prompt = f"""
Validate the following architecture design against requirements and best practices:

Architecture Design: {design}
Requirements: {state.requirements_analysis}
Business Context: {state.business_context}

Validation Areas:
1. Requirements coverage - are all functional and non-functional requirements addressed?
2. Scalability - will the architecture scale to meet expected load?
3. Security - are security requirements properly addressed?
4. Performance - will the architecture meet performance expectations?
5. Cost efficiency - is the architecture cost-effective for the business?
6. Implementation feasibility - can this be built with available resources?

Provide validation results and any necessary adjustments.
Return JSON with validation status and recommendations.
        """
        
        response = await self.query_groq_with_context(validation_prompt, state)
        
        try:
            validation = json.loads(response) if response.startswith('{') else {}
            return self._apply_validation_feedback(design, validation)
        except:
            return design  # Return original design if validation fails

    def _validate_design_approach(self, approach: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and enhance design approach."""
        approach.setdefault("architectural_style", "microservices")
        approach.setdefault("technology_preferences", [])
        approach.setdefault("scalability_approach", "horizontal")
        approach.setdefault("security_approach", "zero-trust")
        approach.setdefault("deployment_strategy", "cloud-native")
        approach.setdefault("justification", "Default approach selected")
        
        return approach

    def _get_default_design_approach(self) -> Dict[str, Any]:
        """Get default design approach."""
        return {
            "architectural_style": "microservices",
            "technology_preferences": ["cloud-native", "containerized"],
            "scalability_approach": "horizontal",
            "security_approach": "zero-trust",
            "deployment_strategy": "kubernetes",
            "justification": "Modern cloud-native approach for scalability and flexibility"
        }

    def _enhance_architecture_design(self, design: Dict[str, Any], state: WorkflowState) -> Dict[str, Any]:
        """Enhance architecture design with additional details."""
        # Ensure required structure
        design.setdefault("components", [])
        design.setdefault("connections", [])
        design.setdefault("patterns", [])
        design.setdefault("technology_stack", {})
        design.setdefault("business_justification", {})
        design.setdefault("deployment_architecture", {})
        design.setdefault("security_architecture", {})
        design.setdefault("monitoring_strategy", {})
        
        # Add metadata
        design["metadata"] = {
            "designed_for": state.user_query,
            "expertise_level": state.user_profile.expertise_level,
            "business_context": state.business_context.__dict__ if state.business_context else {},
            "design_timestamp": "2025-07-05"
        }
        
        return design

    def _get_fallback_architecture(self, state: WorkflowState) -> Dict[str, Any]:
        """Get fallback architecture when design fails."""
        return {
            "components": [
                {
                    "id": "api-gateway",
                    "name": "API Gateway",
                    "type": "gateway",
                    "description": "Entry point for all client requests",
                    "responsibilities": ["Request routing", "Authentication", "Rate limiting"],
                    "technologies": ["Kong", "AWS API Gateway"],
                    "business_value": "Centralized request management and security"
                },
                {
                    "id": "application-service",
                    "name": "Application Service",
                    "type": "service",
                    "description": "Core business logic implementation",
                    "responsibilities": ["Business logic", "Data processing"],
                    "technologies": ["Node.js", "Python", "Java"],
                    "business_value": "Implements core business functionality"
                },
                {
                    "id": "database",
                    "name": "Database",
                    "type": "database",
                    "description": "Data persistence layer",
                    "responsibilities": ["Data storage", "Data integrity"],
                    "technologies": ["PostgreSQL", "MongoDB"],
                    "business_value": "Reliable data storage and retrieval"
                }
            ],
            "connections": [
                {
                    "id": "gateway-to-service",
                    "from_component": "api-gateway",
                    "to_component": "application-service",
                    "type": "synchronous",
                    "protocol": "HTTP/REST",
                    "description": "Request forwarding from gateway to service"
                },
                {
                    "id": "service-to-database",
                    "from_component": "application-service",
                    "to_component": "database",
                    "type": "synchronous",
                    "protocol": "SQL/TCP",
                    "description": "Data access from service to database"
                }
            ],
            "patterns": ["API Gateway", "Layered Architecture"],
            "technology_stack": {
                "frontend": ["React", "TypeScript"],
                "backend": ["Node.js", "Express"],
                "database": ["PostgreSQL"],
                "infrastructure": ["Docker", "Kubernetes"]
            },
            "business_justification": {
                "cost_effective": "Uses proven, cost-effective technologies",
                "scalable": "Can scale horizontally as needed",
                "maintainable": "Clear separation of concerns"
            },
            "fallback": True
        }

    def _get_fallback_design(self, state: WorkflowState) -> Dict[str, Any]:
        """Get fallback design when creation fails."""
        return self._get_fallback_architecture(state)

    def _apply_validation_feedback(self, design: Dict[str, Any], validation: Dict[str, Any]) -> Dict[str, Any]:
        """Apply validation feedback to design."""
        if validation.get("adjustments_needed"):
            design["validation_notes"] = validation.get("recommendations", [])
            design["validation_status"] = "needs_review"
        else:
            design["validation_status"] = "approved"
        
        return design
```

#### **8.3 Why Reasoning Agent**
```python
# src/agents/why_reasoning_agent.py
from typing import Dict, Any, List
import json
from src.agents.base_agent import BaseAgent
from src.models.agent_models import WorkflowState, WhyReasoning, DecisionFactor, Tradeoff, Alternative

class WhyReasoningAgent(BaseAgent):
    """Why reasoning agent that provides comprehensive decision explanations."""
    
    def __init__(self):
        super().__init__("why_reasoning")

    async def process(self, state: WorkflowState) -> Dict[str, Any]:
        """Generate comprehensive why reasoning for architectural decisions."""
        self.logger.info("Generating why reasoning", conversation_id=state.conversation_id)
        
        try:
            reasoning_analysis = await self._analyze_decision_factors(state)
            tradeoff_analysis = await self._analyze_tradeoffs(state)
            alternatives_analysis = await self._analyze_alternatives(state)
            principles_analysis = await self._extract_principles(state)
            
            comprehensive_reasoning = self._synthesize_reasoning(
                reasoning_analysis, tradeoff_analysis, alternatives_analysis, principles_analysis, state
            )
            
            self.logger.info(
                "Why reasoning completed",
                decision_factors=len(comprehensive_reasoning.get("decision_factors", [])),
                tradeoffs=len(comprehensive_reasoning.get("tradeoffs", [])),
                alternatives=len(comprehensive_reasoning.get("alternatives", []))
            )
            
            return {"why_reasoning": comprehensive_reasoning}
            
        except Exception as e:
            self.logger.error("Why reasoning generation failed", error=str(e))
            return {"why_reasoning": self._get_fallback_reasoning(state)}

    def get_system_prompt(self) -> str:
        return """
You are the Why Reasoning Agent for the Agentic Architect platform. Your mission is to provide deep, comprehensive reasoning that builds genuine understanding of architectural decisions and their business implications.

CORE RESPONSIBILITIES:
1. Analyze decision factors that drive architectural choices
2. Explain trade-offs with quantified impacts where possible
3. Present realistic alternatives that were considered
4. Extract architectural principles being applied
5. Connect technical decisions to business outcomes

REASONING FRAMEWORK:
1. DECISION FACTORS ANALYSIS:
   - Identify 3-5 key factors that influenced each architectural choice
   - Explain how each factor contributed to the final decision
   - Rate the importance of each factor (1-5 scale)
   - Provide specific examples and evidence

2. TRADE-OFF BREAKDOWN:
   - Clearly articulate benefits gained from chosen approach
   - Identify specific costs or limitations introduced
   - Quantify trade-offs where possible (performance, cost, complexity)
   - Explain why benefits outweigh costs in this context

3. ALTERNATIVE APPROACHES:
   - Present 2-3 realistic alternatives that were genuinely considered
   - Explain why each alternative was not chosen
   - Describe scenarios where each alternative would be better
   - Rate viability of each alternative (1-5 scale)

4. ARCHITECTURAL PRINCIPLES:
   - Identify fundamental principles demonstrated by decisions
   - Explain how principles apply to other situations
   - Define boundaries where principles don't apply
   - Provide concrete examples of principle application

5. BUSINESS IMPACT CONNECTION:
   - Link technical decisions to business outcomes
   - Identify metrics that show decision success
   - Assess business risks mitigated or introduced
   - Quantify business value where possible

REASONING PRINCIPLES:
- Be specific, not generic - avoid architectural platitudes
- Provide evidence and examples for all claims
- Acknowledge uncertainty and make assumptions explicit
- Focus on learning - help users understand decision-making frameworks
- Connect everything to business context and user goals

Return comprehensive reasoning that genuinely builds understanding and decision-making capability.
        """

    async def _analyze_decision_factors(self, state: WorkflowState) -> Dict[str, Any]:
        """Analyze key factors that drove architectural decisions."""
        factors_prompt = f"""
Analyze the key factors that drove the architectural decisions in this design:

Architecture Design: {state.architecture_design}
Requirements: {state.requirements_analysis}
Research Findings: {state.research_findings}
Business Context: {state.business_context}

For each major architectural decision, identify and analyze:

1. DECISION FACTORS:
   - What were the 3-5 key factors that influenced this choice?
   - How did each factor contribute to the final decision?
   - What specific evidence or constraints made each factor important?
   - Rate the importance of each factor (1-5 scale)

2. FACTOR INTERACTION:
   - How did different factors conflict or reinforce each other?
   - Which factor was most critical in breaking ties?
   - What would change if any factor had different constraints?

Focus on specific, concrete factors rather than generic architectural concerns.
Provide evidence and examples for each factor identified.

Return detailed JSON analysis of decision factors with importance ratings and specific evidence.
        """
        
        response = await self.query_groq_with_context(factors_prompt, state)
        
        try:
            analysis = json.loads(response) if response.startswith('{') else {}
            return self._validate_decision_factors(analysis)
        except:
            return self._get_default_decision_factors()

    async def _analyze_tradeoffs(self, state: WorkflowState) -> Dict[str, Any]:
        """Analyze trade-offs in architectural decisions."""
        tradeoffs_prompt = f"""
Analyze the trade-offs in the architectural decisions made:

Architecture Design: {state.architecture_design}
Requirements: {state.requirements_analysis}
Business Context: {state.business_context}

For each significant architectural choice, analyze:

1. BENEFITS GAINED:
   - What specific advantages does this approach provide?
   - How do these benefits address the requirements?
   - What business value is delivered by these benefits?
   - Can any benefits be quantified (performance, cost, time)?

2. COSTS INCURRED:
   - What limitations or challenges does this approach introduce?
   - What complexity is added to the system?
   - What operational or maintenance costs are introduced?
   - Are there performance or scalability limitations?

3. TRADE-OFF ANALYSIS:
   - Why do the benefits outweigh the costs in this specific context?
   - What metrics would indicate if the trade-off was successful?
   - Under what conditions would this trade-off become unfavorable?
   - How could the costs be mitigated without losing the benefits?

Provide specific, quantified analysis where possible. Avoid generic statements.

Return detailed JSON analysis of trade-offs with quantified impacts where possible.
        """
        
        response = await self.query_groq_with_context(tradeoffs_prompt, state)
        
        try:
            analysis = json.loads(response) if response.startswith('{') else {}
            return self._validate_tradeoffs(analysis)
        except:
            return self._get_default_tradeoffs()

    async def _analyze_alternatives(self, state: WorkflowState) -> Dict[str, Any]:
        """Analyze alternative approaches that were considered."""
        alternatives_prompt = f"""
Identify and analyze realistic alternative approaches that could have been chosen:

Architecture Design: {state.architecture_design}
Requirements: {state.requirements_analysis}
Research Findings: {state.research_findings}

For the major architectural decisions made, identify:

1. REALISTIC ALTERNATIVES:
   - What other approaches were genuinely viable options?
   - What would each alternative approach look like?
   - What are the pros and cons of each alternative?
   - Rate the viability of each alternative (1-5 scale)

2. DECISION RATIONALE:
   - Why was each alternative not chosen?
   - What specific factors made the chosen approach better?
   - Under what circumstances would each alternative be preferable?
   - What would need to change to make an alternative more attractive?

3. ALTERNATIVE SCENARIOS:
   - If requirements were different, which alternatives would be better?
   - If business context changed, how would the decision change?
   - What future conditions might favor switching to an alternative?

Focus on genuine alternatives that were actually considered, not straw man options.
Provide specific analysis of why each alternative wasn't chosen.

Return detailed JSON analysis of alternatives with viability ratings and specific scenarios.
        """
        
        response = await self.query_groq_with_context(alternatives_prompt, state)
        
        try:
            analysis = json.loads(response) if response.startswith('{') else {}
            return self._validate_alternatives(analysis)
        except:
            return self._get_default_alternatives()

    async def _extract_principles(self, state: WorkflowState) -> Dict[str, Any]:
        """Extract architectural principles demonstrated by decisions."""
        principles_prompt = f"""
Extract the architectural principles demonstrated by the design decisions:

Architecture Design: {state.architecture_design}
Decision Context: {state.requirements_analysis}

Identify:

1. DEMONSTRATED PRINCIPLES:
   - What fundamental architectural principles are being applied?
   - How does each decision demonstrate these principles?
   - Provide concrete examples of principle application

2. PRINCIPLE BOUNDARIES:
   - Where do these principles apply and where don't they?
   - What are the limitations of each principle?
   - When would you violate these principles and why?

3. LEARNING OPPORTUNITIES:
   - How can these principles be applied to other situations?
   - What decision-making framework do these principles create?
   - How do these principles evolve with changing requirements?

Focus on actionable principles that can guide future decisions.
Avoid generic principles that don't provide specific guidance.

Return JSON analysis of architectural principles with application examples and boundaries.
        """
        
        response = await self.query_groq_with_context(principles_prompt, state)
        
        try:
            analysis = json.loads(response) if response.startswith('{') else {}
            return self._validate_principles(analysis)
        except:
            return self._get_default_principles()

    def _synthesize_reasoning(
        self, 
        factors: Dict[str, Any], 
        tradeoffs: Dict[str, Any], 
        alternatives: Dict[str, Any], 
        principles: Dict[str, Any], 
        state: WorkflowState
    ) -> Dict[str, Any]:
        """Synthesize all reasoning components into comprehensive analysis."""
        return {
            "decision_factors": factors.get("factors", []),
            "tradeoffs": tradeoffs.get("tradeoffs", []),
            "alternatives": alternatives.get("alternatives", []),
            "principles": principles.get("principles", []),
            "business_alignment": self._extract_business_alignment(state),
            "confidence_level": self._calculate_confidence_level(factors, tradeoffs, alternatives),
            "learning_points": self._extract_learning_points(factors, tradeoffs, alternatives, principles),
            "decision_framework": self._create_decision_framework(factors, tradeoffs, alternatives, principles),
            "success_metrics": self._define_success_metrics(state),
            "reasoning_metadata": {
                "generated_for": state.user_query,
                "user_expertise": state.user_profile.expertise_level,
                "business_role": state.user_profile.business_role,
                "reasoning_completeness": "comprehensive"
            }
        }

    def _validate_decision_factors(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validate decision factors analysis."""
        analysis.setdefault("factors", [])
        return analysis

    def _validate_tradeoffs(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validate trade-offs analysis."""
        analysis.setdefault("tradeoffs", [])
        return analysis

    def _validate_alternatives(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validate alternatives analysis."""
        analysis.setdefault("alternatives", [])
        return analysis

    def _validate_principles(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validate principles analysis."""
        analysis.setdefault("principles", [])
        return analysis

    def _extract_business_alignment(self, state: WorkflowState) -> List[str]:
        """Extract business alignment points."""
        return [
            "Architecture supports business scalability requirements",
            "Technology choices align with budget constraints",
            "Implementation timeline fits business needs",
            "Risk profile acceptable for business context"
        ]

    def _calculate_confidence_level(self, factors: Dict, tradeoffs: Dict, alternatives: Dict) -> int:
        """Calculate confidence level in reasoning."""
        # Simple heuristic based on completeness
        completeness_score = 0
        if factors.get("factors"): completeness_score += 2
        if tradeoffs.get("tradeoffs"): completeness_score += 2
        if alternatives.get("alternatives"): completeness_score += 1
        
        return min(5, max(1, completeness_score))

    def _extract_learning_points(self, factors: Dict, tradeoffs: Dict, alternatives: Dict, principles: Dict) -> List[str]:
        """Extract key learning points."""
        return [
            "Decision-making requires balancing multiple competing factors",
            "Every architectural choice involves trade-offs that must be explicit",
            "Understanding alternatives helps validate chosen approach",
            "Architectural principles provide decision-making frameworks"
        ]

    def _create_decision_framework(self, factors: Dict, tradeoffs: Dict, alternatives: Dict, principles: Dict) -> Dict[str, Any]:
        """Create decision-making framework."""
        return {
            "step_1": "Identify key decision factors and their importance",
            "step_2": "Analyze trade-offs for each potential approach",
            "step_3": "Evaluate realistic alternative solutions",
            "step_4": "Apply relevant architectural principles",
            "step_5": "Validate decision against business objectives"
        }

    def _define_success_metrics(self, state: WorkflowState) -> List[str]:
        """Define metrics for measuring decision success."""
        return [
            "System meets all functional requirements",
            "Performance targets achieved within budget",
            "Implementation completed within timeline",
            "Operational costs within projected range",
            "Business objectives supported effectively"
        ]

    def _get_fallback_reasoning(self, state: WorkflowState) -> Dict[str, Any]:
        """Get fallback reasoning when generation fails."""
        return {
            "decision_factors": [
                {
                    "factor": "Requirements compliance",
                    "importance": 5,
                    "explanation": "Architecture must meet all specified requirements",
                    "business_impact": "Ensures solution delivers expected value"
                }
            ],
            "tradeoffs": [
                {
                    "benefit": "Scalable architecture",
                    "cost": "Increased initial complexity",
                    "impact_level": 3,
                    "justification": "Long-term benefits outweigh short-term costs"
                }
            ],
            "alternatives": [
                {
                    "name": "Simpler monolithic approach",
                    "description": "Single-tier application architecture",
                    "pros": ["Faster initial development", "Lower complexity"],
                    "cons": ["Limited scalability", "Harder to maintain"],
                    "viability_score": 3
                }
            ],
            "principles": ["Separation of concerns", "Scalability by design"],
            "confidence_level": 3,
            "fallback": True
        }

    def _get_default_decision_factors(self) -> Dict[str, Any]:
        """Get default decision factors."""
        return {
            "factors": [
                {
                    "factor": "Business requirements",
                    "importance": 5,
                    "explanation": "Must meet core business needs"
                }
            ]
        }

    def _get_default_tradeoffs(self) -> Dict[str, Any]:
        """Get default trade-offs."""
        return {
            "tradeoffs": [
                {
                    "benefit": "Meets requirements",
                    "cost": "Implementation complexity",
                    "impact_level": 3
                }
            ]
        }

    def _get_default_alternatives(self) -> Dict[str, Any]:
        """Get default alternatives."""
        return {
            "alternatives": [
                {
                    "name": "Alternative approach",
                    "description": "Different implementation strategy",
                    "viability_score": 3
                }
            ]
        }

    def _get_default_principles(self) -> Dict[str, Any]:
        """Get default principles."""
        return {
            "principles": [
                "Design for business value",
                "Balance complexity with benefits"
            ]
        }
    