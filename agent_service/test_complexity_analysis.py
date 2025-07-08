#!/usr/bin/env python3
"""
Test the new LLM-based complexity analysis system
"""

import asyncio
import json
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.architecture_agent import ArchitectureAgent
from models.agent_models import WorkflowState, UserProfile, ExpertiseLevel

async def test_complexity_analysis():
    """Test the new intelligent complexity analysis system."""
    print("🧠 Testing LLM-based Complexity Analysis")
    print("=" * 50)
    
    # Initialize architecture agent
    arch_agent = ArchitectureAgent()
    
    # Test cases with different complexity levels
    test_cases = [
        {
            "name": "Simple Web App",
            "query": "I need a simple blog website with user registration",
            "expected_complexity": "simple"
        },
        {
            "name": "Cryptocurrency Trading Platform", 
            "query": "I need a real-time cryptocurrency trading platform with sub-millisecond latency",
            "expected_complexity": "enterprise"
        },
        {
            "name": "E-commerce Platform",
            "query": "I want to build an online marketplace for buying and selling products",
            "expected_complexity": "moderate"
        },
        {
            "name": "High-Frequency Trading System",
            "query": "Build a high-frequency algorithmic trading system for financial markets with microsecond latency requirements",
            "expected_complexity": "enterprise"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}️⃣ Testing: {test_case['name']}")
        print(f"Query: {test_case['query']}")
        print("-" * 40)
        
        try:
            # Test the complexity analysis
            analysis = await arch_agent._analyze_system_complexity(test_case['query'])
            
            print(f"🎯 Complexity Level: {analysis.get('complexity_level')}")
            print(f"⚡ Criticality Level: {analysis.get('criticality_level')}")
            print(f"🚀 Performance Requirements: {analysis.get('performance_requirements')}")
            print(f"📈 Scale Requirements: {analysis.get('scale_requirements')}")
            print(f"🏗️ Domain Type: {analysis.get('domain_type')}")
            print(f"📦 Component Count: {analysis.get('required_components_count')}")
            print(f"🔧 Infrastructure Needs: {', '.join(analysis.get('infrastructure_needs', []))}")
            print(f"💡 Reasoning: {analysis.get('reasoning')}")
            
            # Check if complexity matches expectation
            actual_complexity = analysis.get('complexity_level')
            expected_complexity = test_case['expected_complexity']
            
            if actual_complexity == expected_complexity:
                print(f"✅ Complexity assessment correct!")
            else:
                print(f"⚠️ Complexity assessment differs (expected: {expected_complexity}, got: {actual_complexity})")
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Complexity Analysis Test Complete!")

async def test_full_crypto_architecture():
    """Test full architecture generation for cryptocurrency trading platform."""
    print("\n\n🏗️ Testing Full Crypto Architecture Generation")
    print("=" * 50)
    
    # Create test state
    user_profile = UserProfile(
        id="test-user",
        email="test@example.com", 
        expertise_level=ExpertiseLevel.ADVANCED
    )
    
    state = WorkflowState(
        conversation_id="crypto-test",
        user_query="I need a real-time cryptocurrency trading platform with sub-millisecond latency",
        user_profile=user_profile
    )
    
    # Initialize agent
    arch_agent = ArchitectureAgent()
    
    try:
        print("📊 Generating architecture...")
        result = await arch_agent.process(state)
        
        if result.get("success"):
            architecture = result.get("architecture_design", {})
            
            # Analyze components
            components = architecture.get("components", [])
            connections = architecture.get("connections", [])
            
            print(f"✅ Architecture generated successfully!")
            print(f"📦 Components: {len(components)}")
            print(f"🔗 Connections: {len(connections)}")
            
            # Show components
            print("\n🧩 Components:")
            for comp in components[:10]:  # Show first 10
                name = comp.get("name", "Unknown")
                comp_type = comp.get("type", "unknown")
                criticality = comp.get("visualization_metadata", {}).get("business_criticality", "medium")
                print(f"  • {name} ({comp_type}) - Criticality: {criticality}")
            
            if len(components) > 10:
                print(f"  ... and {len(components) - 10} more components")
            
            # Check if high-performance components are included
            high_perf_indicators = [
                "cache", "redis", "memory", "low latency", "real-time", 
                "load balancer", "gateway", "websocket", "streaming"
            ]
            
            found_indicators = []
            for comp in components:
                comp_text = f"{comp.get('name', '')} {comp.get('description', '')} {comp.get('technology', '')}".lower()
                for indicator in high_perf_indicators:
                    if indicator in comp_text and indicator not in found_indicators:
                        found_indicators.append(indicator)
            
            print(f"\n🚀 High-performance features found: {found_indicators}")
            
            if len(found_indicators) >= 3:
                print("✅ Architecture appears optimized for high-performance trading!")
            else:
                print("⚠️ Architecture may need more high-performance optimizations")
            
            # Check visualization data
            viz_data = architecture.get("visualization_data", {})
            if viz_data:
                complexity_score = viz_data.get("visualization_metadata", {}).get("complexity_score", 0)
                print(f"📊 Architecture Complexity Score: {complexity_score}/10")
            
        else:
            print(f"❌ Architecture generation failed: {result.get('error')}")
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    print("\n🏁 Full Architecture Test Complete!")

async def identify_static_checks():
    """Identify other static checks that could benefit from LLM intelligence."""
    print("\n\n🔍 Identifying Other Static Checks for LLM Enhancement")
    print("=" * 60)
    
    static_checks_to_enhance = [
        {
            "area": "Technology Selection",
            "current_static_approach": "Hardcoded technology mappings based on keywords",
            "llm_enhancement": "Intelligent technology selection based on requirements, scale, team expertise, and industry best practices",
            "example": "Instead of 'database' -> 'PostgreSQL', analyze requirements for consistency, scale, performance needs"
        },
        {
            "area": "Security Requirements Detection",
            "current_static_approach": "Keyword scanning for 'security', 'auth', 'compliance'",
            "llm_enhancement": "Context-aware security analysis based on domain (fintech=high, blog=medium), data sensitivity, regulatory requirements",
            "example": "Trading platform automatically gets SOX compliance, encryption, audit logging without explicit mention"
        },
        {
            "area": "Scalability Pattern Selection",
            "current_static_approach": "Fixed patterns based on component count or keywords",
            "llm_enhancement": "Intelligent pattern selection based on actual usage patterns, growth projections, and business model",
            "example": "SaaS platform gets multi-tenant architecture, gaming gets geo-distributed, fintech gets event sourcing"
        },
        {
            "area": "Infrastructure Sizing",
            "current_static_approach": "Simple mappings: small/medium/large based on component count",
            "llm_enhancement": "Performance-based sizing considering latency requirements, throughput, availability targets",
            "example": "Sub-millisecond trading gets dedicated bare metal, batch processing gets spot instances"
        },
        {
            "area": "Integration Pattern Detection",
            "current_static_approach": "Generic REST/HTTP assumptions",
            "llm_enhancement": "Context-aware protocol selection based on latency, consistency, and volume requirements",
            "example": "Real-time systems get WebSocket/gRPC, batch systems get message queues, sync systems get HTTP"
        },
        {
            "area": "Monitoring & Observability Requirements",
            "current_static_approach": "Basic logging + metrics for all systems",
            "llm_enhancement": "Risk-based observability design considering business impact, compliance, and operational complexity",
            "example": "Financial systems get comprehensive audit trails, dev tools get APM, customer-facing gets UX monitoring"
        },
        {
            "area": "Data Architecture Patterns",
            "current_static_approach": "Simple CRUD database selection",
            "llm_enhancement": "Data access pattern analysis for CQRS, event sourcing, polyglot persistence decisions",
            "example": "Analytics workloads get data lakes, transactional systems get ACID databases, search gets specialized stores"
        },
        {
            "area": "Deployment Strategy Selection",
            "current_static_approach": "Default containerization recommendations",
            "llm_enhancement": "Context-aware deployment strategy based on team expertise, compliance, and operational requirements",
            "example": "Startups get serverless, enterprises get Kubernetes, regulated industries get on-premise options"
        },
        {
            "area": "Business Impact Assessment",
            "current_static_approach": "Generic ROI templates and risk categories",
            "llm_enhancement": "Industry-specific impact analysis with relevant metrics, competitive advantages, and risk factors",
            "example": "E-commerce gets conversion rate impact, SaaS gets churn reduction, trading gets latency-revenue correlation"
        },
        {
            "area": "Implementation Roadmap Planning",
            "current_static_approach": "Linear phase-based implementation plans",
            "llm_enhancement": "Risk-driven, value-focused implementation sequences based on dependencies and business priorities",
            "example": "MVP gets core user journey first, enterprise gets security foundation first, trading gets market data pipeline first"
        }
    ]
    
    for i, check in enumerate(static_checks_to_enhance, 1):
        print(f"\n{i}. {check['area']}")
        print(f"   Current: {check['current_static_approach']}")
        print(f"   LLM Enhancement: {check['llm_enhancement']}")
        print(f"   Example: {check['example']}")
    
    print(f"\n📊 Total areas identified for LLM enhancement: {len(static_checks_to_enhance)}")
    print("\n💡 Priority Implementation Order:")
    print("1. Security Requirements Detection (high business impact)")
    print("2. Technology Selection (fundamental architecture decisions)")
    print("3. Scalability Pattern Selection (performance critical)")
    print("4. Integration Pattern Detection (system cohesion)")
    print("5. Infrastructure Sizing (cost optimization)")
    
    print("\n🏁 Static Check Analysis Complete!")

async def main():
    """Run all tests."""
    await test_complexity_analysis()
    await test_full_crypto_architecture() 
    await identify_static_checks()

if __name__ == "__main__":
    asyncio.run(main())