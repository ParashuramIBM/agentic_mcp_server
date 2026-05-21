#!/usr/bin/env python3
"""
Test All MCP Tools
Comprehensive testing script for all MCP server tools
"""

import asyncio
import json
from typing import Dict, Any
import sys
import os

# For testing via stdio (simulating MCP client)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MCPToolTester:
    """Test all MCP tools exposed by the server"""
    
    def __init__(self):
        self.test_results = []
    
    def print_header(self, text: str):
        """Print formatted header"""
        print("\n" + "=" * 80)
        print(f"  {text}")
        print("=" * 80)
    
    def print_result(self, tool_name: str, success: bool, result: Any):
        """Print test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"\n{status} - {tool_name}")
        if success:
            print(f"Result: {json.dumps(result, indent=2)[:500]}...")
        else:
            print(f"Error: {result}")
    
    async def test_devops_automation(self) -> bool:
        """Test devops_automation tool"""
        self.print_header("Test 1: devops_automation Tool")
        
        print("\n📋 Test Case: Create Dockerfile for Python FastAPI")
        
        # Simulate tool call
        arguments = {
            "task": "Create a production-ready Dockerfile for Python FastAPI application",
            "environment": "production",
            "context": {
                "language": "python",
                "framework": "fastapi",
                "app_name": "my-api"
            }
        }
        
        print(f"Arguments: {json.dumps(arguments, indent=2)}")
        
        try:
            # Import and call the tool handler
            from src.mcp.mcp_server import LangGraphMCPServer
            server = LangGraphMCPServer()
            result = await server._execute_devops_task(arguments)
            
            self.print_result("devops_automation", True, result)
            self.test_results.append(("devops_automation", True))
            return True
        except Exception as e:
            self.print_result("devops_automation", False, str(e))
            self.test_results.append(("devops_automation", False))
            return False
    
    async def test_code_review(self) -> bool:
        """Test code_review tool"""
        self.print_header("Test 2: code_review Tool")
        
        print("\n📋 Test Case: Review Python code")
        
        sample_code = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total

def process_data(data):
    result = []
    for i in range(len(data)):
        result.append(data[i] * 2)
    return result
"""
        
        arguments = {
            "code": sample_code,
            "language": "python",
            "focus_areas": ["performance", "best_practices", "security"]
        }
        
        print(f"Code length: {len(sample_code)} characters")
        print(f"Focus areas: {arguments['focus_areas']}")
        
        try:
            from src.mcp.mcp_server import LangGraphMCPServer
            server = LangGraphMCPServer()
            result = await server._execute_code_review(arguments)
            
            self.print_result("code_review", True, result)
            self.test_results.append(("code_review", True))
            return True
        except Exception as e:
            self.print_result("code_review", False, str(e))
            self.test_results.append(("code_review", False))
            return False
    
    async def test_service_orchestration(self) -> bool:
        """Test service_orchestration tool"""
        self.print_header("Test 3: service_orchestration Tool")
        
        print("\n📋 Test Case: Orchestrate microservices deployment")
        
        arguments = {
            "services": ["api-gateway", "auth-service", "user-service", "payment-service"],
            "workflow_type": "deployment",
            "requirements": {
                "environment": "production",
                "strategy": "blue-green",
                "health_checks": True
            }
        }
        
        print(f"Services: {', '.join(arguments['services'])}")
        print(f"Workflow: {arguments['workflow_type']}")
        
        try:
            from src.mcp.mcp_server import LangGraphMCPServer
            server = LangGraphMCPServer()
            result = await server._execute_orchestration(arguments)
            
            self.print_result("service_orchestration", True, result)
            self.test_results.append(("service_orchestration", True))
            return True
        except Exception as e:
            self.print_result("service_orchestration", False, str(e))
            self.test_results.append(("service_orchestration", False))
            return False
    
    async def test_multi_agent_task(self) -> bool:
        """Test multi_agent_task tool"""
        self.print_header("Test 4: multi_agent_task Tool")
        
        print("\n📋 Test Case: Complex multi-agent task")
        
        arguments = {
            "task": "Create a complete DevOps setup including Dockerfile, Kubernetes manifests, and CI/CD pipeline for a Node.js Express microservices application",
            "agents": ["devops_agent", "code_review_agent"],
            "context": {
                "architecture": "microservices",
                "language": "nodejs",
                "framework": "express",
                "cloud": "aws"
            }
        }
        
        print(f"Task: {arguments['task'][:100]}...")
        print(f"Agents: {', '.join(arguments['agents'])}")
        
        try:
            from src.mcp.mcp_server import LangGraphMCPServer
            server = LangGraphMCPServer()
            result = await server._execute_multi_agent_task(arguments)
            
            self.print_result("multi_agent_task", True, result)
            self.test_results.append(("multi_agent_task", True))
            return True
        except Exception as e:
            self.print_result("multi_agent_task", False, str(e))
            self.test_results.append(("multi_agent_task", False))
            return False
    
    async def test_get_agent_status(self) -> bool:
        """Test get_agent_status tool"""
        self.print_header("Test 5: get_agent_status Tool")
        
        print("\n📋 Test Case: Get status of all agents")
        
        arguments = {}
        
        try:
            from src.mcp.mcp_server import LangGraphMCPServer
            server = LangGraphMCPServer()
            result = await server._get_agent_status(arguments)
            
            self.print_result("get_agent_status", True, result)
            self.test_results.append(("get_agent_status", True))
            return True
        except Exception as e:
            self.print_result("get_agent_status", False, str(e))
            self.test_results.append(("get_agent_status", False))
            return False
    
    async def test_all_resources(self) -> bool:
        """Test all MCP resources"""
        self.print_header("Test 6: MCP Resources")
        
        resources = [
            "langgraph://agent/status",
            "langgraph://workflow/state",
            "langgraph://execution/history",
            "langgraph://config/settings"
        ]
        
        all_passed = True
        
        for resource_uri in resources:
            print(f"\n📋 Testing resource: {resource_uri}")
            
            try:
                from src.mcp.mcp_server import LangGraphMCPServer
                from pydantic import AnyUrl
                
                server = LangGraphMCPServer()
                result = await server.server._read_resource_handler(AnyUrl(resource_uri))
                
                print(f"✅ Resource accessible: {resource_uri}")
                print(f"   Content: {result[:200]}...")
            except Exception as e:
                print(f"❌ Resource failed: {resource_uri}")
                print(f"   Error: {e}")
                all_passed = False
        
        self.test_results.append(("resources", all_passed))
        return all_passed
    
    async def run_all_tests(self):
        """Run all tests"""
        self.print_header("🧪 MCP Tools Comprehensive Test Suite")
        
        print("\nThis will test all 5 MCP tools and 4 resources")
        print("Each test simulates a real MCP tool call\n")
        
        # Run all tests
        await self.test_devops_automation()
        await self.test_code_review()
        await self.test_service_orchestration()
        await self.test_multi_agent_task()
        await self.test_get_agent_status()
        await self.test_all_resources()
        
        # Print summary
        self.print_header("📊 Test Summary")
        
        passed = sum(1 for _, success in self.test_results if success)
        total = len(self.test_results)
        
        print(f"\n✅ Passed: {passed}/{total}")
        print(f"❌ Failed: {total - passed}/{total}")
        
        print("\n📋 Detailed Results:")
        for tool_name, success in self.test_results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {status} - {tool_name}")
        
        if passed == total:
            print("\n🎉 All tests passed! Your MCP server is fully functional.")
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Check the errors above.")
        
        print("\n" + "=" * 80)


async def main():
    """Main entry point"""
    tester = MCPToolTester()
    
    try:
        await tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n\n👋 Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("=" * 80)
    print("  MCP Tools Test Suite")
    print("  Testing all tools exposed by LangGraph MCP Server")
    print("=" * 80)
    
    asyncio.run(main())

# Made with Bob
