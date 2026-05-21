#!/usr/bin/env python3
"""Diagnostic script for MCP integration"""

import os
import sys


def check_env_vars():
    """Check environment variables"""
    print("=" * 60)
    print("Environment Variables")
    print("=" * 60)
    
    vars_to_check = [
        "AGENTIC_STUDIO_API_KEY",
        "MCP_BEARER_TOKEN",
        "MCP_API_KEY",
        "MCP_SERVER_URL"
    ]
    
    all_set = True
    for var in vars_to_check:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value[:20]}...")
        else:
            print(f"❌ {var}: NOT SET")
            all_set = False
    
    return all_set


def test_agent():
    """Test agent connection"""
    print("\n" + "=" * 60)
    print("Testing Agent Connection")
    print("=" * 60)
    
    try:
        from agent_client import AgentClient
        client = AgentClient()
        card = client.get_agent_card()
        print(f"✅ Agent connected: {card.get('name', 'Unknown')}")
        capabilities = card.get('capabilities', [])
        if capabilities:
            print(f"   Capabilities: {', '.join(capabilities[:3])}")
        return True
    except Exception as e:
        print(f"❌ Agent connection failed: {e}")
        return False


def test_mcp():
    """Test MCP connection"""
    print("\n" + "=" * 60)
    print("Testing MCP Connection")
    print("=" * 60)
    
    try:
        from mcp_client_standalone import MCPContextStudioClient
        client = MCPContextStudioClient()
        
        if client.test_connection():
            print("✅ MCP connected")
            
            tools = client.list_tools()
            print(f"   Tools available: {len(tools)}")
            if tools:
                print(f"   First tool: {tools[0].get('name', 'Unknown')}")
            
            resources = client.list_resources()
            print(f"   Resources available: {len(resources)}")
            
            return True
        else:
            print("❌ MCP connection failed")
            return False
    except Exception as e:
        print(f"❌ MCP error: {e}")
        return False


def main():
    """Run diagnostics"""
    print("\n" + "=" * 60)
    print("MCP Integration Diagnostics")
    print("=" * 60)
    
    env_ok = check_env_vars()
    agent_ok = test_agent()
    mcp_ok = test_mcp()
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Environment Variables: {'✅ OK' if env_ok else '❌ MISSING'}")
    print(f"Agent Connection: {'✅ OK' if agent_ok else '❌ FAILED'}")
    print(f"MCP Connection: {'✅ OK' if mcp_ok else '❌ FAILED'}")
    
    print("\n" + "=" * 60)
    print("Recommendations")
    print("=" * 60)
    
    if not env_ok:
        print("❌ Set missing environment variables:")
        print("   export AGENTIC_STUDIO_API_KEY='your-key'")
        print("   export MCP_BEARER_TOKEN='your-token'")
        print("   export MCP_API_KEY='your-key'")
    
    if agent_ok and not mcp_ok:
        print("💡 Agent works! Use it without MCP for now:")
        print("   from agent_client import AgentClient")
        print("   client = AgentClient()")
        print("   result = client.create_dockerfile('python', 'fastapi')")
    
    if not agent_ok:
        print("❌ Fix agent connection first:")
        print("   1. Get API key from: https://agentstudio.servicesessentials.ibm.com/settings")
        print("   2. export AGENTIC_STUDIO_API_KEY='your-key'")
    
    if agent_ok and mcp_ok:
        print("🎉 All systems operational!")
        print("   You can use context-enhanced agent:")
        print("   python context_enhanced_agent.py")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# Made with Bob
