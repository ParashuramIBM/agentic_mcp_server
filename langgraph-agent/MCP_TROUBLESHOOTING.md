# MCP Context Studio Troubleshooting Guide

This guide helps resolve common issues when integrating with MCP Context Studio.

## 🔍 Common Issues

### Issue 1: 401 Unauthorized (Agent API)

**Error:**
```
401 Client Error: Unauthorized for url: https://servicesessentials.ibm.com/agenticapps/a2a/...
```

**Cause:** AGENTIC_STUDIO_API_KEY not set or invalid

**Solution:**
```bash
# Set your agent API key
export AGENTIC_STUDIO_API_KEY="your-api-key-here"

# Verify it's set
echo $AGENTIC_STUDIO_API_KEY

# Or add to .env file
echo "AGENTIC_STUDIO_API_KEY=your-key" >> .env
```

Get your API key from: https://agentstudio.servicesessentials.ibm.com/settings

### Issue 2: 406 Not Acceptable (MCP Server)

**Error:**
```
406 Client Error: Not Acceptable for url: https://servicesessentials.ibm.com/mcp-gateway/...
```

**Cause:** MCP server may not support the `search_context` tool or requires different headers

**Solutions:**

#### Option A: Check Available Tools First

```python
from mcp_client_standalone import MCPContextStudioClient

client = MCPContextStudioClient()

# List what tools are actually available
tools = client.list_tools()
print("Available tools:")
for tool in tools:
    print(f"  - {tool.get('name')}: {tool.get('description')}")
```

#### Option B: Try Different MCP Methods

```python
# Instead of search_context, try listing resources
resources = client.list_resources()
print(f"Found {len(resources)} resources")

# Or try reading a specific resource
if resources:
    resource = client.read_resource(resources[0]['uri'])
    print(resource)
```

#### Option C: Use Agent Without MCP Context

If MCP is not working, you can still use the agent directly:

```python
from agent_client import AgentClient

client = AgentClient()

# Use agent without MCP context
result = client.create_dockerfile("python", "fastapi")
print(result.artifacts["dockerfile"])
```

### Issue 3: Token Expired

**Error:**
```
401 Unauthorized or 403 Forbidden
```

**Cause:** MCP tokens have expired (check exp field in JWT)

**Solution:**
1. Go to MCP Gateway settings
2. Generate new tokens
3. Update environment variables:
```bash
export MCP_BEARER_TOKEN="new-bearer-token"
export MCP_API_KEY="new-api-key"
```

### Issue 4: Network/Connectivity Issues

**Error:**
```
Connection timeout or Connection refused
```

**Solution:**
```bash
# Test connectivity
curl -v https://servicesessentials.ibm.com/mcp-gateway/service/gateway/servers/8ccdd203bdee4014b08e82eedb6046e2/mcp

# Check if behind proxy
echo $HTTP_PROXY
echo $HTTPS_PROXY

# If behind proxy, configure requests
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```

## 🔧 Debugging Steps

### Step 1: Verify Environment Variables

```bash
# Check all required variables are set
echo "Agent API Key: ${AGENTIC_STUDIO_API_KEY:0:20}..."
echo "MCP Bearer: ${MCP_BEARER_TOKEN:0:20}..."
echo "MCP API Key: ${MCP_API_KEY:0:20}..."
```

### Step 2: Test Agent Connection Only

```python
from agent_client import AgentClient

try:
    client = AgentClient()
    card = client.get_agent_card()
    print(f"✅ Agent connected: {card['name']}")
except Exception as e:
    print(f"❌ Agent connection failed: {e}")
```

### Step 3: Test MCP Connection Only

```python
from mcp_client_standalone import MCPContextStudioClient

try:
    client = MCPContextStudioClient()
    if client.test_connection():
        print("✅ MCP connected")
        tools = client.list_tools()
        print(f"Available tools: {[t['name'] for t in tools]}")
    else:
        print("❌ MCP connection failed")
except Exception as e:
    print(f"❌ MCP error: {e}")
```

### Step 4: Use Fallback Mode

If MCP is not working, use the agent in standalone mode:

```python
from agent_client import AgentClient

class FallbackAgent:
    """Agent that works without MCP context"""
    
    def __init__(self):
        self.client = AgentClient()
    
    def create_dockerfile(self, language, framework):
        """Create Dockerfile with built-in best practices"""
        message = f"""Create a production-ready Dockerfile for {language} {framework}.

Include these best practices:
- Multi-stage build
- Non-root user
- Minimal base image
- Security hardening
- Health checks
"""
        return self.client.invoke(message, {
            "language": language,
            "framework": framework
        })

# Use fallback agent
agent = FallbackAgent()
result = agent.create_dockerfile("python", "fastapi")
print(result.artifacts["dockerfile"])
```

## 📊 Diagnostic Script

Save this as `diagnose.py`:

```python
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
        print(f"   Capabilities: {', '.join(card.get('capabilities', [])[:3])}")
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
    
    if agent_ok and not mcp_ok:
        print("\n💡 Recommendation: Use agent in standalone mode (without MCP)")
    elif not agent_ok:
        print("\n💡 Recommendation: Check AGENTIC_STUDIO_API_KEY")
    elif agent_ok and mcp_ok:
        print("\n🎉 All systems operational!")

if __name__ == "__main__":
    main()
```

Run it:
```bash
python diagnose.py
```

## 🎯 Recommended Approach

Given the current errors, here's the recommended approach:

### 1. Use Agent Without MCP (Immediate Solution)

```python
from agent_client import AgentClient

# This works without MCP
client = AgentClient()
result = client.create_dockerfile("python", "fastapi")
print(result.artifacts["dockerfile"])
```

### 2. Fix Agent API Key

```bash
# Get your API key from Agentic Studio
export AGENTIC_STUDIO_API_KEY="your-actual-api-key"
```

### 3. Investigate MCP Tools

```python
# Find out what MCP actually supports
from mcp_client_standalone import MCPContextStudioClient

client = MCPContextStudioClient()
tools = client.list_tools()

print("MCP supports these tools:")
for tool in tools:
    print(f"  - {tool['name']}")
```

### 4. Use Alternative MCP Methods

If `search_context` doesn't work, try:
- `list_resources()` - List available resources
- `read_resource(uri)` - Read specific resource
- Check tool documentation for correct parameters

## 📞 Support

If issues persist:
1. Check MCP Gateway documentation
2. Verify your MCP server permissions
3. Contact support: #ica-procode-agents

## ✅ Working Configuration

Minimal working setup without MCP:

```python
# .env file
AGENTIC_STUDIO_API_KEY=your-key-here

# Python code
from agent_client import AgentClient

client = AgentClient()
result = client.create_dockerfile("python", "fastapi")
# This works!
```

Add MCP later when connectivity is resolved.