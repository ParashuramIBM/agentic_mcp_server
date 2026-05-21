#!/usr/bin/env python3
"""
Example: Integrating LangGraph Agent with MCP Context Studio
Demonstrates how to enhance agent responses with enterprise context
"""

import os
import sys

# Use standalone MCP client to avoid import issues
from mcp_client_standalone import MCPContextStudioClient
from agent_client import AgentClient


def print_header(text: str):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def main():
    print_header("LangGraph Agent + MCP Context Studio Integration")
    
    # Check environment variables
    print("\n📋 Checking environment variables...")
    mcp_token = os.getenv("MCP_BEARER_TOKEN")
    mcp_key = os.getenv("MCP_API_KEY")
    agent_key = os.getenv("AGENTIC_STUDIO_API_KEY")
    
    if not mcp_token or not mcp_key:
        print("❌ MCP credentials not found!")
        print("\nPlease set:")
        print("  export MCP_BEARER_TOKEN='your-bearer-token'")
        print("  export MCP_API_KEY='your-api-key'")
        return
    
    if not agent_key:
        print("❌ Agent API key not found!")
        print("\nPlease set:")
        print("  export AGENTIC_STUDIO_API_KEY='your-api-key'")
        return
    
    print(f"✅ MCP Bearer Token: {mcp_token[:20]}...")
    print(f"✅ MCP API Key: {mcp_key[:20]}...")
    print(f"✅ Agent API Key: {agent_key[:20]}...")
    
    # Initialize clients
    print_header("1. Initializing Clients")
    
    try:
        print("\n🔧 Initializing MCP Context Studio client...")
        mcp_client = MCPContextStudioClient()
        print("✅ MCP client initialized")
        
        print("\n🔧 Initializing LangGraph Agent client...")
        agent_client = AgentClient()
        print("✅ Agent client initialized")
    except Exception as e:
        print(f"❌ Error initializing clients: {e}")
        return
    
    # Test MCP connection
    print_header("2. Testing MCP Connection")
    
    print("\n🔍 Testing connection to MCP server...")
    if mcp_client.test_connection():
        print("✅ MCP connection successful")
    else:
        print("❌ MCP connection failed")
        print("   Continuing with agent-only mode...")
    
    # List available MCP tools
    print_header("3. Listing Available MCP Tools")
    
    print("\n🔍 Querying available tools...")
    tools = mcp_client.list_tools()
    
    if tools:
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            name = tool.get('name', 'Unknown')
            desc = tool.get('description', 'No description')
            print(f"   - {name}: {desc}")
    else:
        print("⚠️  No tools found or unable to list tools")
    
    # List available resources
    print_header("4. Listing Available Resources")
    
    print("\n🔍 Querying available resources...")
    resources = mcp_client.list_resources()
    
    if resources:
        print(f"✅ Found {len(resources)} resources:")
        for resource in resources[:5]:  # Show first 5
            uri = resource.get('uri', 'Unknown')
            name = resource.get('name', 'No name')
            print(f"   - {uri}: {name}")
        if len(resources) > 5:
            print(f"   ... and {len(resources) - 5} more")
    else:
        print("⚠️  No resources found or unable to list resources")
    
    # Search context for DevOps information
    print_header("5. Searching Context for DevOps Information")
    
    print("\n🔍 Searching for 'DevOps best practices'...")
    search_results = mcp_client.search_context("DevOps best practices", limit=3)
    
    if search_results:
        print(f"✅ Found {len(search_results)} results:")
        for i, result in enumerate(search_results, 1):
            if isinstance(result, dict):
                content = result.get('content', result.get('text', 'No content'))
                print(f"\n   Result {i}:")
                print(f"   {content[:150]}...")
    else:
        print("⚠️  No search results found")
    
    # Use context to enhance agent request
    print_header("6. Creating Dockerfile with Context Enhancement")
    
    print("\n🔍 Searching for Docker security best practices...")
    docker_context = mcp_client.search_context("Docker security best practices", limit=2)
    
    # Build enhanced prompt with context
    context_info = ""
    if docker_context:
        print(f"✅ Found {len(docker_context)} context items")
        context_items = []
        for item in docker_context:
            if isinstance(item, dict):
                content = item.get('content', item.get('text', ''))
                if content:
                    context_items.append(f"- {content[:100]}...")
        context_info = "\n".join(context_items)
    else:
        print("⚠️  No context found, using standard prompt")
        context_info = "- Use multi-stage builds\n- Run as non-root user\n- Minimize image size"
    
    enhanced_message = f"""Create a production-ready Dockerfile for Python FastAPI application.

Consider these enterprise best practices:
{context_info}
"""
    
    print("\n🤖 Invoking LangGraph agent with enhanced context...")
    try:
        result = agent_client.invoke(
            message=enhanced_message,
            context={
                "environment": "production",
                "language": "python",
                "framework": "fastapi",
                "mcp_context": True
            }
        )
        
        print(f"\n✅ Status: {result.status}")
        print(f"📊 Confidence: {result.confidence_score:.2%}")
        print(f"🆔 Request ID: {result.request_id}")
        
        if result.error:
            print(f"❌ Error: {result.error}")
        elif "dockerfile" in result.artifacts:
            dockerfile = result.artifacts["dockerfile"]
            all_lines = dockerfile.split('\n')
            preview_lines = all_lines[:15]
            print(f"\n📄 Dockerfile Preview (first 15 lines):")
            for line in preview_lines:
                print(f"   {line}")
            if len(all_lines) > 15:
                remaining = len(all_lines) - 15
                print(f"   ... ({remaining} more lines)")
        else:
            print(f"\n📝 Response: {result.message[:200]}...")
    
    except Exception as e:
        print(f"❌ Error invoking agent: {e}")
    
    # Summary
    print_header("Integration Complete!")
    
    print("\n✅ Successfully demonstrated:")
    print("   1. MCP Context Studio connection")
    print("   2. Tool and resource discovery")
    print("   3. Context search and retrieval")
    print("   4. Enhanced agent invocation with context")
    
    print("\n📚 Next steps:")
    print("   - Explore context_enhanced_agent.py for advanced patterns")
    print("   - Read MCP_CONTEXT_STUDIO_INTEGRATION.md for full documentation")
    print("   - Integrate MCP context into your workflows")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# Made with Bob
