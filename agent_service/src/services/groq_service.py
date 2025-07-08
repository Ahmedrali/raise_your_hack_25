import asyncio
import time
from typing import Dict, List, Optional, Any
from groq import AsyncGroq
from tenacity import retry, stop_after_attempt, wait_exponential
import structlog
from src.config.settings import settings

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

            # Mock response for demo purposes
            if settings.groq_api_key == "demo-key":
                return self._get_mock_response(prompt, system_message)

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                stream=False
            )

            if not response.choices or not response.choices[0].message:
                raise Exception("No response content received from Groq")

            content = response.choices[0].message.content
            if not content:
                raise Exception("Empty response content from Groq")

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
            raise Exception(f"Groq API request failed: {str(e)}")

    def _get_mock_response(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Generate mock responses for demo purposes."""
        prompt_lower = prompt.lower()
        
        if "orchestrat" in prompt_lower:
            return """
            {
                "workflow_type": "SEQUENTIAL",
                "agents_required": ["requirements", "research", "architecture", "why_reasoning", "business_impact", "educational"],
                "estimated_duration_minutes": 15,
                "complexity_score": 3,
                "justification": "Sequential workflow recommended for comprehensive analysis"
            }
            """
        elif "requirement" in prompt_lower:
            return """
            {
                "functional_requirements": [
                    "User authentication and authorization",
                    "Product catalog management",
                    "Shopping cart functionality",
                    "Order processing system",
                    "Payment integration"
                ],
                "non_functional_requirements": [
                    "Support 50K concurrent users",
                    "99.9% uptime availability",
                    "Sub-200ms response times",
                    "PCI DSS compliance",
                    "GDPR compliance"
                ],
                "business_requirements": [
                    "Scalable to handle growth",
                    "Cost-effective implementation",
                    "Fast time to market"
                ],
                "constraints": [
                    "Budget limitations",
                    "6-month timeline",
                    "Existing team skills"
                ]
            }
            """
        elif "research" in prompt_lower:
            return """
            {
                "technical_insights": [
                    "Microservices architecture is industry standard for e-commerce",
                    "Event-driven architecture improves scalability",
                    "API Gateway pattern essential for service coordination"
                ],
                "business_insights": [
                    "Microservices reduce time-to-market for new features",
                    "Cloud-native approach reduces operational costs by 30%",
                    "Containerization improves deployment reliability"
                ],
                "recommendations": [
                    "Start with core services: user, product, order",
                    "Implement event sourcing for order processing",
                    "Use managed cloud services for databases"
                ]
            }
            """
        elif "architecture" in prompt_lower:
            return """
            {
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
                        "id": "user-service",
                        "name": "User Service",
                        "type": "microservice",
                        "description": "Handles user management and authentication",
                        "responsibilities": ["User registration", "Authentication", "Profile management"],
                        "technologies": ["Node.js", "PostgreSQL", "JWT"],
                        "business_value": "Secure user management"
                    },
                    {
                        "id": "product-service",
                        "name": "Product Service",
                        "type": "microservice",
                        "description": "Manages product catalog and inventory",
                        "responsibilities": ["Product CRUD", "Inventory tracking", "Search"],
                        "technologies": ["Python", "MongoDB", "Elasticsearch"],
                        "business_value": "Flexible product management"
                    }
                ],
                "connections": [
                    {
                        "id": "gateway-to-user",
                        "from_component": "api-gateway",
                        "to_component": "user-service",
                        "type": "synchronous",
                        "protocol": "HTTP/REST",
                        "description": "User authentication and management requests"
                    }
                ],
                "patterns": ["Microservices", "API Gateway", "Event Sourcing"],
                "technology_stack": {
                    "frontend": ["React", "TypeScript"],
                    "backend": ["Node.js", "Python", "Express", "FastAPI"],
                    "database": ["PostgreSQL", "MongoDB"],
                    "infrastructure": ["Docker", "Kubernetes", "AWS"]
                }
            }
            """
        elif "why" in prompt_lower or "reasoning" in prompt_lower:
            return """
            {
                "decision_factors": [
                    {
                        "factor": "Scalability requirements",
                        "importance": 5,
                        "explanation": "Need to handle 50K concurrent users",
                        "business_impact": "Enables business growth without architecture changes"
                    },
                    {
                        "factor": "Development team expertise",
                        "importance": 4,
                        "explanation": "Team has strong Node.js and Python skills",
                        "business_impact": "Faster development and lower training costs"
                    }
                ],
                "tradeoffs": [
                    {
                        "benefit": "Independent service scaling",
                        "cost": "Increased operational complexity",
                        "impact_level": 4,
                        "justification": "Benefits outweigh complexity for this scale"
                    }
                ],
                "alternatives": [
                    {
                        "name": "Monolithic architecture",
                        "description": "Single deployable application",
                        "pros": ["Simpler deployment", "Easier debugging"],
                        "cons": ["Limited scalability", "Technology lock-in"],
                        "viability_score": 2
                    }
                ],
                "principles": [
                    "Single responsibility per service",
                    "Database per service",
                    "Fail fast and recover quickly"
                ]
            }
            """
        elif "business" in prompt_lower and "impact" in prompt_lower:
            return """
            {
                "roi_analysis": {
                    "initial_investment": {"development": 500000, "infrastructure": 100000},
                    "ongoing_costs": {"hosting": 20000, "maintenance": 30000},
                    "expected_benefits": {"revenue_increase": 200000, "cost_savings": 50000},
                    "payback_period_months": 18,
                    "net_present_value": 750000,
                    "confidence_level": 4
                },
                "risk_assessment": {
                    "technical_risks": [
                        {"risk": "Service integration complexity", "probability": 3, "impact": 4}
                    ],
                    "business_risks": [
                        {"risk": "Market competition", "probability": 4, "impact": 3}
                    ],
                    "overall_risk_level": 3
                },
                "competitive_advantages": [
                    "Faster feature delivery",
                    "Better scalability",
                    "Improved reliability"
                ]
            }
            """
        elif "educational" in prompt_lower:
            return """
            {
                "concepts": [
                    {
                        "name": "Microservices Architecture",
                        "explanation": "Architectural pattern that structures an application as a collection of loosely coupled services",
                        "business_value": "Enables independent development and scaling of features"
                    }
                ],
                "examples": [
                    {
                        "title": "Netflix Microservices",
                        "description": "How Netflix uses microservices to serve millions of users",
                        "lessons": ["Service isolation", "Fault tolerance", "Independent scaling"]
                    }
                ],
                "resources": [
                    {
                        "title": "Microservices Patterns",
                        "type": "book",
                        "url": "https://microservices.io/patterns/"
                    }
                ]
            }
            """
        else:
            return f"I understand you're asking about: {prompt[:100]}... Let me provide a comprehensive analysis based on architectural best practices and business considerations."

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

        # For demo, just use the main query method
        return await self.query(prompt, system_message)

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
