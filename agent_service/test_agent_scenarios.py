#!/usr/bin/env python3
"""
Comprehensive test cases for the Agent Service
Tests various scenarios to ensure real LLM responses and proper functionality
"""

import asyncio
import json
import time
from typing import Dict, Any, List
import aiohttp
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

class AgentServiceTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
        self.test_results = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def health_check(self) -> bool:
        """Test if the agent service is running"""
        try:
            async with self.session.get(f"{self.base_url}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Health Check: {data.get('status', 'unknown')}")
                    return True
                else:
                    print(f"❌ Health Check Failed: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Health Check Error: {e}")
            return False
    
    async def test_scenario(self, 
                           scenario_name: str,
                           user_message: str,
                           expertise_level: str = "INTERMEDIATE",
                           expected_keywords: List[str] = None,
                           timeout: int = 120) -> Dict[str, Any]:
        """Test a specific scenario"""
        print(f"\n🧪 Testing: {scenario_name}")
        print(f"📝 Query: {user_message}")
        print(f"👤 Expertise: {expertise_level}")
        
        request_data = {
            "conversation_id": f"test-{int(time.time())}",
            "user_message": user_message,
            "user_profile": {
                "id": "test-user",
                "email": "test@example.com",
                "expertise_level": expertise_level
            },
            "workflow_type": "SEQUENTIAL",
            "conversation_history": []
        }
        
        start_time = time.time()
        
        try:
            timeout_obj = aiohttp.ClientTimeout(total=timeout)
            async with self.session.post(
                f"{self.base_url}/api/agent/process",
                json=request_data,
                timeout=timeout_obj
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    result = {
                        "scenario": scenario_name,
                        "status": "FAILED",
                        "error": f"HTTP {response.status}: {error_text}",
                        "duration": time.time() - start_time
                    }
                    print(f"❌ Failed: {result['error']}")
                    return result
                
                data = await response.json()
                duration = time.time() - start_time
                
                # Analyze the response
                analysis = self.analyze_response(data, expected_keywords, scenario_name)
                
                result = {
                    "scenario": scenario_name,
                    "status": "SUCCESS" if analysis["is_valid"] else "FAILED",
                    "duration": duration,
                    "response_data": data,
                    "analysis": analysis,
                    "user_message": user_message,
                    "expertise_level": expertise_level
                }
                
                # Print results
                if analysis["is_valid"]:
                    print(f"✅ Success ({duration:.1f}s)")
                    print(f"📊 Content: {data.get('data', {}).get('content', '')}")
                    print(f"📊 Content Length: {len(data.get('data', {}).get('content', ''))}")
                    print(f"🎯 Keywords Found: {analysis['keywords_found']}")
                    if analysis.get('agents_used'):
                        print(f"🤖 Agents Used: {len(analysis['agents_used'])}")
                else:
                    print(f"❌ Failed: {analysis['issues']}")
                
                return result
                
        except asyncio.TimeoutError:
            result = {
                "scenario": scenario_name,
                "status": "TIMEOUT",
                "error": f"Request timed out after {timeout}s",
                "duration": time.time() - start_time
            }
            print(f"⏰ Timeout after {timeout}s")
            return result
            
        except Exception as e:
            result = {
                "scenario": scenario_name,
                "status": "ERROR",
                "error": str(e),
                "duration": time.time() - start_time
            }
            print(f"💥 Error: {e}")
            return result
    
    def analyze_response(self, data: Dict[str, Any], expected_keywords: List[str], scenario: str) -> Dict[str, Any]:
        """Analyze the response for quality and correctness"""
        analysis = {
            "is_valid": True,
            "issues": [],
            "keywords_found": [],
            "content_quality": {},
            "agents_used": []
        }
        
        # Check if response has the expected structure
        if not data.get("success"):
            analysis["is_valid"] = False
            analysis["issues"].append("Response not successful")
            return analysis
        
        response_data = data.get("data", {})
        content = response_data.get("content", "")
        
        # Check for dummy/placeholder content
        dummy_indicators = [
            "lorem ipsum",
            "placeholder",
            "dummy data",
            "test content",
            "sample text",
            "TODO",
            "FIXME"
        ]
        
        content_lower = content.lower()
        for indicator in dummy_indicators:
            if indicator in content_lower:
                analysis["is_valid"] = False
                analysis["issues"].append(f"Contains dummy content: {indicator}")
        
        # Check content length (should be substantial for real responses)
        if len(content) < 100:
            analysis["is_valid"] = False
            analysis["issues"].append(f"Content too short: {len(content)} characters")
        
        # Check for expected keywords
        if expected_keywords:
            for keyword in expected_keywords:
                if keyword.lower() in content_lower:
                    analysis["keywords_found"].append(keyword)
        
        # Check metadata for agent execution
        metadata = data.get("metadata", {})
        agents_used = metadata.get("agents_used", [])
        analysis["agents_used"] = agents_used
        
        if not agents_used:
            analysis["issues"].append("No agents reported as used")
        
        # Check for architecture-specific content
        if "architecture" in scenario.lower():
            arch_keywords = ["component", "service", "database", "api", "frontend", "backend"]
            arch_found = [kw for kw in arch_keywords if kw in content_lower]
            if len(arch_found) < 2:
                analysis["issues"].append("Insufficient architecture-specific content")
        
        # Check response structure
        expected_fields = ["content", "message_type", "confidence_score"]
        for field in expected_fields:
            if field not in response_data:
                analysis["issues"].append(f"Missing field: {field}")
        
        # Analyze content quality
        analysis["content_quality"] = {
            "length": len(content),
            "has_structure": any(marker in content for marker in ["##", "**", "•", "1.", "2."]),
            "has_technical_terms": len([kw for kw in ["architecture", "design", "pattern", "service", "component"] if kw in content_lower]) > 0
        }
        
        return analysis
    
    async def run_comprehensive_tests(self):
        """Run all test scenarios"""
        print("🚀 Starting Comprehensive Agent Service Tests")
        print("=" * 60)
        
        # Check health first
        if not await self.health_check():
            print("❌ Agent service is not healthy. Aborting tests.")
            return
        
        # Define test scenarios
        test_scenarios = [
            {
                "name": "Simple E-commerce Architecture",
                "message": "I need to design a simple e-commerce website architecture",
                "expertise": "BEGINNER",
                "keywords": ["database", "frontend", "backend", "payment"],
                "timeout": 90
            },
            {
                "name": "Microservices Architecture",
                "message": "Design a microservices architecture for a high-traffic social media platform",
                "expertise": "ADVANCED",
                "keywords": ["microservices", "scalability", "load balancer", "api gateway"],
                "timeout": 120
            },
            {
                "name": "Real-time Trading Platform",
                "message": "I need a real-time cryptocurrency trading platform with sub-millisecond latency",
                "expertise": "EXPERT",
                "keywords": ["real-time", "latency", "trading", "performance"],
                "timeout": 150
            },
            {
                "name": "Healthcare System Architecture",
                "message": "Design a HIPAA-compliant healthcare management system",
                "expertise": "INTERMEDIATE",
                "keywords": ["security", "compliance", "healthcare", "privacy"],
                "timeout": 120
            },
            {
                "name": "IoT Architecture",
                "message": "Create an architecture for an IoT sensor network with 10,000 devices",
                "expertise": "ADVANCED",
                "keywords": ["iot", "sensors", "mqtt", "edge computing"],
                "timeout": 120
            },
            {
                "name": "Machine Learning Pipeline",
                "message": "Design an ML pipeline for real-time fraud detection",
                "expertise": "EXPERT",
                "keywords": ["machine learning", "pipeline", "fraud", "real-time"],
                "timeout": 120
            },
            {
                "name": "Mobile App Backend",
                "message": "I need a backend architecture for a mobile chat application",
                "expertise": "INTERMEDIATE",
                "keywords": ["mobile", "chat", "websocket", "push notifications"],
                "timeout": 100
            },
            {
                "name": "Cloud Migration Strategy",
                "message": "Help me migrate a monolithic application to cloud-native architecture",
                "expertise": "ADVANCED",
                "keywords": ["cloud", "migration", "containers", "kubernetes"],
                "timeout": 120
            }
        ]
        
        # Run all scenarios
        for scenario in test_scenarios:
            result = await self.test_scenario(
                scenario["name"],
                scenario["message"],
                scenario["expertise"],
                scenario["keywords"],
                scenario["timeout"]
            )
            self.test_results.append(result)
            
            # Brief pause between tests
            await asyncio.sleep(2)
        
        # Generate summary report
        self.generate_report()
    
    def generate_report(self):
        """Generate a comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        successful_tests = len([r for r in self.test_results if r["status"] == "SUCCESS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAILED"])
        timeout_tests = len([r for r in self.test_results if r["status"] == "TIMEOUT"])
        error_tests = len([r for r in self.test_results if r["status"] == "ERROR"])
        
        print(f"📈 Overall Results:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Successful: {successful_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   ⏰ Timeouts: {timeout_tests}")
        print(f"   💥 Errors: {error_tests}")
        print(f"   📊 Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        
        # Average response time for successful tests
        successful_results = [r for r in self.test_results if r["status"] == "SUCCESS"]
        if successful_results:
            avg_duration = sum(r["duration"] for r in successful_results) / len(successful_results)
            print(f"   ⏱️  Average Response Time: {avg_duration:.1f}s")
        
        print(f"\n📋 Detailed Results:")
        for result in self.test_results:
            status_emoji = {
                "SUCCESS": "✅",
                "FAILED": "❌", 
                "TIMEOUT": "⏰",
                "ERROR": "💥"
            }
            
            print(f"\n{status_emoji.get(result['status'], '❓')} {result['scenario']}")
            print(f"   Status: {result['status']}")
            print(f"   Duration: {result['duration']:.1f}s")
            
            if result["status"] == "SUCCESS":
                analysis = result.get("analysis", {})
                content_length = len(result.get("response_data", {}).get("data", {}).get("content", ""))
                print(f"   Content Length: {content_length} chars")
                print(f"   Keywords Found: {analysis.get('keywords_found', [])}")
                print(f"   Agents Used: {len(analysis.get('agents_used', []))}")
                
                if analysis.get("issues"):
                    print(f"   ⚠️  Issues: {analysis['issues']}")
            else:
                print(f"   Error: {result.get('error', 'Unknown error')}")
        
        # Quality Analysis
        print(f"\n🔍 Quality Analysis:")
        successful_with_analysis = [r for r in self.test_results if r["status"] == "SUCCESS" and "analysis" in r]
        
        if successful_with_analysis:
            avg_content_length = sum(
                len(r.get("response_data", {}).get("data", {}).get("content", ""))
                for r in successful_with_analysis
            ) / len(successful_with_analysis)
            
            total_agents_used = sum(
                len(r.get("analysis", {}).get("agents_used", []))
                for r in successful_with_analysis
            ) / len(successful_with_analysis)
            
            print(f"   📝 Average Content Length: {avg_content_length:.0f} characters")
            print(f"   🤖 Average Agents Used: {total_agents_used:.1f}")
            
            # Check for dummy content issues
            dummy_issues = sum(
                1 for r in successful_with_analysis
                if any("dummy" in issue.lower() for issue in r.get("analysis", {}).get("issues", []))
            )
            
            if dummy_issues == 0:
                print(f"   ✅ No dummy content detected in any responses")
            else:
                print(f"   ⚠️  {dummy_issues} responses contained dummy content")
        
        print(f"\n🎯 Recommendations:")
        if successful_tests / total_tests >= 0.8:
            print("   ✅ Agent service is performing well!")
        else:
            print("   ⚠️  Agent service needs attention - low success rate")
        
        if timeout_tests > 0:
            print("   ⏰ Consider optimizing response times or increasing timeouts")
        
        if failed_tests > 0:
            print("   🔧 Review failed test cases for potential improvements")

async def main():
    """Main test runner"""
    async with AgentServiceTester() as tester:
        await tester.run_comprehensive_tests()

if __name__ == "__main__":
    print("🧪 Agent Service Comprehensive Test Suite")
    print("Testing real LLM responses and functionality")
    print("-" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n💥 Test suite error: {e}")
