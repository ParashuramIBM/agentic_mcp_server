#!/usr/bin/env python
"""
Test script for VS Code MCP Server
Run this to verify your MCP server is working
"""
import asyncio
import json
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_mcp_server():
    """Test MCP server functionality"""
    print("=" * 50)
    print("Testing VS Code MCP Server")
    print("=" * 50)
    
    # Import server
    from server import VSCodeMCPServer
    
    # Create server instance
    print("\n1. Initializing server...")
    server = VSCodeMCPServer()
    print("   ✓ Server initialized")
    
    # Test tool listing
    print("\n2. Testing tool listing...")
    tools = await server.server.list_tools()
    print(f"   ✓ Found {len(tools)} tools:")
    for tool in tools:
        print(f"     - {tool.name}: {tool.description[:50]}...")
    
    # Test configuration
    print("\n3. Checking configuration...")
    print(f"   ✓ GitHub Token: {'Configured' if server.config.github_token else 'Missing'}")
    print(f"   ✓ Risk thresholds: auto={server.config.risk_auto_fix_threshold}, review={server.config.risk_human_review_threshold}")
    print(f"   ✓ Log level: {server.config.log_level}")
    
    # Test GitHub connection (if token provided)
    if server.config.github_token:
        print("\n4. Testing GitHub connection...")
        try:
            # Try to get current user info
            user = await server.github_tools.get_workflow_run("octocat/Hello-World", None)
            print("   ✓ GitHub API connection successful")
        except Exception as e:
            print(f"   ⚠ GitHub connection test failed: {str(e)}")
    else:
        print("\n4. GitHub token not configured - skipping API tests")
    
    print("\n" + "=" * 50)
    print("Server is ready for VS Code!")
    print("=" * 50)
    print("\nTo use in VS Code:")
    print("1. Install Continue extension")
    print("2. The MCP server will be automatically detected")
    print("3. Use the tools in Continue chat")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())