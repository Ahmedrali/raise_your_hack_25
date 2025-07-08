#!/usr/bin/env python3
"""
Quick test to verify agent service functionality
"""

import asyncio
import aiohttp
import json
import time

async def quick_test():
    print("🚀 Quick Agent Service Test")
    print("-" * 30)
    
    async with aiohttp.ClientSession() as session:
        # Test 1: Health Check
        print("1️⃣ Testing Health Check...")
        try:
            async with session.get("http://localhost:8000/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ Health: {data.get('status')}")
                    print(f"   🔧 Services: {list(data.get('services', {}).keys())}")
                else:
                    print(f"   ❌ Health check failed: {response.status}")
                    return
        except Exception as e:
            print(f"   ❌ Health check error: {e}")
            return
        
        # Test 2: Simple Agent Request
        print("\n2️⃣ Testing Simple Agent Request...")
        request_data = {
            "conversation_id": "quick-test",
            "user_message": "What are the main components of a web application?",
            "user_profile": {
                "id": "test-user",
                "email": "test@example.com",
                "expertise_level": "BEGINNER"
            },
            "workflow_type": "SEQUENTIAL"
        }
        
        start_time = time.time()
        try:
            timeout = aiohttp.ClientTimeout(total=60)  # 1 minute timeout
            async with session.post(
                "http://localhost:8000/api/agent/process",
                json=request_data,
                timeout=timeout
            ) as response:
                
                duration = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    
                    print(f"   ✅ Response received ({duration:.1f}s)")
                    
                    # Analyze response
                    if data.get("success"):
                        response_data = data.get("data", {})
                        content = response_data.get("content", "")
                        
                        print(f"   📝 Content length: {len(content)} characters")
                        print(f"   🎯 Message type: {response_data.get('message_type')}")
                        print(f"   📊 Confidence: {response_data.get('confidence_score', 'N/A')}")
                        
                        # Check metadata
                        metadata = data.get("metadata", {})
                        agents_used = metadata.get("agents_used", [])
                        print(f"   🤖 Agents used: {len(agents_used)} ({', '.join(agents_used[:3])}{'...' if len(agents_used) > 3 else ''})")
                        
                        # Check for real content (not dummy)
                        dummy_indicators = ["lorem ipsum", "placeholder", "dummy", "test content"]
                        has_dummy = any(indicator in content.lower() for indicator in dummy_indicators)
                        
                        if has_dummy:
                            print("   ⚠️  Warning: Response may contain dummy content")
                        else:
                            print("   ✅ Response appears to be real content")
                        
                        # Show content preview
                        preview = content[:200] + "..." if len(content) > 200 else content
                        print(f"\n   📖 Content Preview:")
                        print(f"   {preview}")
                        
                        # Check for technical terms
                        tech_terms = ["component", "architecture", "database", "frontend", "backend", "api"]
                        found_terms = [term for term in tech_terms if term.lower() in content.lower()]
                        print(f"\n   🔧 Technical terms found: {found_terms}")
                        
                        if len(found_terms) >= 2:
                            print("   ✅ Response contains appropriate technical content")
                        else:
                            print("   ⚠️  Response may lack technical depth")
                        
                    else:
                        print(f"   ❌ Agent response not successful: {data}")
                        
                else:
                    error_text = await response.text()
                    print(f"   ❌ Request failed: {response.status}")
                    print(f"   Error: {error_text}")
                    
        except asyncio.TimeoutError:
            print(f"   ⏰ Request timed out after 60 seconds")
        except Exception as e:
            print(f"   ❌ Request error: {e}")
        
        print(f"\n🏁 Quick test completed!")

if __name__ == "__main__":
    asyncio.run(quick_test())
