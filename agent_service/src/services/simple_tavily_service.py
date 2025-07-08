import asyncio
from typing import Dict, List, Optional, Any
import structlog
from src.config.settings import settings

logger = structlog.get_logger()

class SimpleTavilyService:
    def __init__(self):
        self.api_key = settings.tavily_api_key
        self.max_results = settings.tavily_max_results
        self.search_depth = settings.tavily_search_depth
        
        # Usage tracking
        self.searches_made = 0
        self.total_results_retrieved = 0

    async def search(
        self,
        query: str,
        max_results: Optional[int] = None,
        search_depth: Optional[str] = None,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform comprehensive search with mock results.
        """
        try:
            logger.info(
                "Performing mock Tavily search",
                query=query,
                max_results=max_results or self.max_results,
                search_depth=search_depth or self.search_depth
            )

            # Mock search results for demo purposes
            results = self._get_mock_search_results(query)

            # Update usage statistics
            self.searches_made += 1
            self.total_results_retrieved += len(results)

            logger.info(
                "Mock Tavily search completed",
                results_count=len(results),
                total_searches=self.searches_made
            )

            return results

        except Exception as e:
            logger.error("Mock Tavily search failed", error=str(e), query=query)
            raise Exception(f"Mock Tavily search failed: {str(e)}")

    def _get_mock_search_results(self, query: str) -> List[Dict[str, Any]]:
        """Generate mock search results for demo purposes."""
        query_lower = query.lower()
        
        base_results = []
        
        if "microservices" in query_lower or "architecture" in query_lower:
            base_results = [
                {
                    "title": "Microservices Architecture Patterns",
                    "url": "https://microservices.io/patterns/",
                    "content": "Comprehensive guide to microservices patterns including API Gateway, Service Discovery, and Circuit Breaker patterns.",
                    "score": 0.95,
                    "domain": "microservices.io",
                    "content_type": "technical",
                    "relevance_score": 0.9
                },
                {
                    "title": "Building Microservices: Best Practices",
                    "url": "https://aws.amazon.com/microservices/",
                    "content": "AWS guide on building scalable microservices with cloud-native technologies and best practices.",
                    "score": 0.88,
                    "domain": "aws.amazon.com",
                    "content_type": "technical",
                    "relevance_score": 0.85
                },
                {
                    "title": "Microservices vs Monolith: Business Impact Analysis",
                    "url": "https://martinfowler.com/articles/microservices.html",
                    "content": "Martin Fowler's analysis of when to use microservices and their business implications.",
                    "score": 0.92,
                    "domain": "martinfowler.com",
                    "content_type": "business",
                    "relevance_score": 0.88
                }
            ]
        elif "e-commerce" in query_lower:
            base_results = [
                {
                    "title": "E-commerce Architecture Scalability Patterns",
                    "url": "https://highscalability.com/ecommerce-architecture/",
                    "content": "How major e-commerce platforms handle millions of users with distributed architecture patterns.",
                    "score": 0.93,
                    "domain": "highscalability.com",
                    "content_type": "technical",
                    "relevance_score": 0.91
                },
                {
                    "title": "E-commerce Platform ROI Analysis",
                    "url": "https://forrester.com/ecommerce-platform-roi/",
                    "content": "Forrester research on ROI of different e-commerce platform architectures and their business impact.",
                    "score": 0.87,
                    "domain": "forrester.com",
                    "content_type": "business",
                    "relevance_score": 0.84
                }
            ]
        elif "performance" in query_lower or "scalability" in query_lower:
            base_results = [
                {
                    "title": "High Performance Architecture Patterns",
                    "url": "https://docs.microsoft.com/performance-patterns/",
                    "content": "Microsoft's guide to performance optimization patterns for distributed systems.",
                    "score": 0.89,
                    "domain": "docs.microsoft.com",
                    "content_type": "technical",
                    "relevance_score": 0.86
                },
                {
                    "title": "Scalability Cost Analysis for Startups",
                    "url": "https://techcrunch.com/scalability-costs/",
                    "content": "Analysis of scalability investment costs and returns for growing technology companies.",
                    "score": 0.82,
                    "domain": "techcrunch.com",
                    "content_type": "business",
                    "relevance_score": 0.79
                }
            ]
        else:
            base_results = [
                {
                    "title": f"Architecture Best Practices for {query}",
                    "url": "https://example.com/architecture-guide",
                    "content": f"Comprehensive guide covering architectural considerations for {query} including scalability, security, and performance.",
                    "score": 0.85,
                    "domain": "example.com",
                    "content_type": "technical",
                    "relevance_score": 0.8
                }
            ]

        return base_results

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

        # Execute searches sequentially for simplicity
        all_results = []
        seen_urls = set()
        
        for i, search_query in enumerate(search_queries[:4]):  # Limit queries
            try:
                results = await self.search(search_query, max_results=5)
                for result in results:
                    url = result.get("url", "")
                    if url not in seen_urls:
                        result["search_query"] = search_query
                        all_results.append(result)
                        seen_urls.add(url)
            except Exception as e:
                logger.warning(f"Search query {i} failed: {e}")

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
        """Check if service is available."""
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
